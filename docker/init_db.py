import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MIGRATIONS_DIR = os.path.join(PROJECT_ROOT, 'migrations')
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask_migrate import stamp, upgrade
from sqlalchemy import inspect

from app import db
from app.models import Category, Topic
from app.services.user_service import get_avatar_upload_dir
from seed import app, seed_all


def init_database() -> None:
    with app.app_context():
        os.makedirs(app.instance_path, exist_ok=True)
        os.makedirs(get_avatar_upload_dir(), exist_ok=True)

        tables = set(inspect(db.engine).get_table_names())

        if 'alembic_version' in tables:
            print('[docker-init] Wykryto tabele migracji Alembic — uruchamiam flask db upgrade...')
            upgrade(directory=MIGRATIONS_DIR)
        elif 'users' not in tables:
            print('[docker-init] Nowa baza danych — tworzę schemat i ustawiam rewizję Alembic (stamp head)...')
            db.create_all()
            stamp(directory=MIGRATIONS_DIR)
        else:
            print('[docker-init] Wykryto istniejącą bazę bez alembic_version — uzupełniam ewentualne brakujące tabele...')
            db.create_all()

        auto_seed = os.environ.get('AUTO_SEED', 'auto').strip().lower()
        if auto_seed == 'always':
            print('[docker-init] AUTO_SEED=always — synchronizuję sylabus i osiągnięcia...')
            seed_all()
        elif auto_seed in ('auto', 'true', '1', 'yes'):
            if Category.query.count() == 0 and Topic.query.count() == 0:
                print('[docker-init] Baza jest pusta — uruchamiam seed sylabusa i osiągnięć...')
                seed_all()
            else:
                print('[docker-init] Baza zawiera już kategorie/tematy — pomijam automatyczny seed.')
        else:
            print('[docker-init] AUTO_SEED wyłączony — pomijam seed.')


if __name__ == '__main__':
    init_database()

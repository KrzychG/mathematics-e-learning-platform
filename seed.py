import os
import json
from app import create_app, db
from app.models import Category, Topic
from app.services.progress_service import sync_achievements_catalog
from app.services.theory_renderer_service import strip_frontmatter

app = create_app()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def get_theory_content_from_file(rel_path: str) -> str:
    if not rel_path:
        return ""
    norm_path = rel_path.replace('\\', '/')

    candidates = [
        os.path.join(BASE_DIR, 'content', 'theory', norm_path),
        os.path.join(BASE_DIR, 'app', 'content', 'theory', norm_path),
    ]
    for cand in candidates:
        if os.path.isfile(cand):
            try:
                with open(cand, 'r', encoding='utf-8') as f:
                    return strip_frontmatter(f.read()).strip()
            except Exception:
                pass

    return ""


def load_syllabus_manifest() -> list[dict]:
    syllabus_path = os.path.join(BASE_DIR, 'content', 'syllabus.json')
    if not os.path.exists(syllabus_path):
        syllabus_path = os.path.join(BASE_DIR, 'app', 'content', 'syllabus.json')
    if not os.path.exists(syllabus_path):
        return []
    with open(syllabus_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('categories', [])


def seed_all():
    with app.app_context():
        db.create_all()

        categories_data = load_syllabus_manifest()
        topics_created = 0
        theories_synced = 0

        for cat_info in categories_data:
            cat_name = cat_info['name']
            cat = Category.query.filter_by(name=cat_name).first()
            if not cat:
                cat = Category(name=cat_name)
                db.session.add(cat)
                db.session.flush()

            for t_info in cat_info.get('topics', []):
                t_name = t_info['name']
                t_desc = t_info.get('description', '')
                t_file = t_info.get('theory_file', '')
                theory_content = get_theory_content_from_file(t_file)

                top = Topic.query.filter_by(name=t_name, category_id=cat.id).first()
                if not top:
                    top = Topic(
                        category_id=cat.id,
                        name=t_name,
                        description=t_desc,
                    )
                    top.set_sanitized_theory(theory_content)
                    db.session.add(top)
                    db.session.flush()
                    topics_created += 1
                    if top.theory:
                        theories_synced += 1
                else:
                    if t_desc and not top.description:
                        top.description = t_desc
                    if theory_content and (not top.theory or top.theory.strip() != theory_content.strip()):
                        top.set_sanitized_theory(theory_content)
                        theories_synced += 1

        db.session.commit()
        if topics_created > 0:
            print(f"Utworzono {topics_created} nowych tematów w bazie danych.")
        if theories_synced > 0:
            print(f"Zsynchronizowano treść teorii dla {theories_synced} tematów z plików źródłowych.")

        achievements_created = sync_achievements_catalog(commit=True)
        if achievements_created > 0:
            print(f"Dodano {achievements_created} nowych osiągnięć do katalogu.")

        print("Baza danych została pomyślnie zsynchronizowana z sylabusem!")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Inicjalizacja i seedowanie bazy danych platformy Axioma.")
    parser.add_argument(
        '--demo',
        '--with-demo',
        action='store_true',
        help="Zasila bazę kompletnym zestawem użytkowników demonstracyjnych i historią postępów."
    )
    parser.add_argument(
        '--clean-demo',
        action='store_true',
        help="Czyści i odtwarza konta demonstracyjne od zera."
    )
    args = parser.parse_args()

    if args.demo or args.clean_demo:
        from seed_demo import seed_demo_data
        seed_demo_data(clean=args.clean_demo)
    else:
        seed_all()

import pytest
from app import db
from app.models import User
from config import TestingConfig
from werkzeug.security import generate_password_hash


class RateLimitTestingConfig(TestingConfig):
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URI = "memory://"
    RATELIMIT_STRATEGY = "fixed-window"


@pytest.fixture
def rate_limited_app(app_factory):
    app = app_factory(RateLimitTestingConfig)
    with app.app_context():
        user = User(email='limiter_test@example.com', first_name='LimiterUser', password_hash=generate_password_hash('correct_password'))
        db.session.add(user)
        db.session.commit()
        return app, user.id


def test_login_brute_force_rate_limit(rate_limited_app, post_login):
    app, _ = rate_limited_app
    client = app.test_client()
    for i in range(5):
        resp = post_login(client, 'limiter_test@example.com', f'wrong_{i}')
        assert resp.status_code == 200 and 'Nieprawidłowy e-mail lub hasło' in resp.data.decode('utf-8')
    resp_blocked = post_login(client, 'limiter_test@example.com', 'wrong_blocked')
    assert resp_blocked.status_code == 429
    html = resp_blocked.data.decode('utf-8')
    assert 'Zbyt wiele zapytań (429)' in html and 'Rate Limiting' in html

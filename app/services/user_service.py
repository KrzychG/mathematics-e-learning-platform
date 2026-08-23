import os
import secrets
from PIL import Image
from flask import current_app, flash
from app import db
from app.models import User

ALLOWED_AVATAR_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
MAX_AVATAR_SIZE_BYTES = 3 * 1024 * 1024  # 3 MB
MAX_AVATAR_DIMENSION = 4096  # Ochrona przed tzw. pixel flood
Image.MAX_IMAGE_PIXELS = 10_000_000

def get_avatar_upload_dir() -> str:
    upload_dir = current_app.config.get('AVATAR_UPLOAD_DIR') or os.path.join(
        current_app.root_path, 'static', 'uploads', 'avatars'
    )
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir


def remove_user_avatar_file(filename: str | None) -> None:
    if not filename:
        return
    upload_dir = get_avatar_upload_dir()
    file_path = os.path.join(upload_dir, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError:
            pass


def count_active_admins() -> int:
    return db.session.query(User).filter(
        User.is_admin.is_(True),
        User.is_active.is_(True),
    ).count()


def is_last_active_admin(user: User) -> bool:
    # Blokada lockoutu: nie pozwalamy usunąć ani zdegradować jedynego aktywnego administratora.
    if not user.is_admin or not user.is_active:
        return False
    return count_active_admins() <= 1


def is_blocked_last_active_admin(user: User, message: str, *, condition: bool = True, checker=None) -> bool:
    check = checker or is_last_active_admin
    if condition and check(user):
        flash(message, 'danger')
        return True
    return False


def delete_user_account(user: User) -> None:
    avatar_filename = user.avatar_filename
    db.session.delete(user)
    db.session.commit()
    remove_user_avatar_file(avatar_filename)


def safe_delete_user_account(
    user: User,
    *,
    success_msg: str | None = None,
    error_msg: str = 'Wystąpił błąd podczas usuwania konta.',
    success_category: str = 'info',
) -> bool:
    try:
        delete_user_account(user)
        if success_msg:
            flash(success_msg, success_category)
        return True
    except Exception:
        db.session.rollback()
        flash(error_msg, 'danger')
        return False


def save_user_avatar(user: User, file) -> tuple[bool, str, str]:
    # Bezpieczne wgrywanie i przetwarzanie awatara:
    # - Sprawdzamy MIME/rozszerzenie oraz rozmiar pliku (max 3 MB)
    # - img.verify() sprawdza integralność formatu
    # - Konieczny file.seek(0), bo Pillow po weryfikacji zostawia wskaźnik na końcu pliku
    # - Przeskalowanie do 512x512 filtrem Lanczos
    # - Stary plik z dysku usuwamy dopiero po udanym commicie do bazy
    if not file or not file.filename:
        return False, 'Nie wybrano pliku ze zdjęciem.', 'danger'
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in ALLOWED_AVATAR_EXTENSIONS:
        return False, 'Niedozwolony format pliku. Dopuszczalne formaty: JPG, PNG, WEBP, GIF.', 'danger'
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > MAX_AVATAR_SIZE_BYTES:
        return False, 'Plik jest zbyt duży. Maksymalny dopuszczalny rozmiar to 3 MB.', 'danger'
    try:
        img = Image.open(file)
        img.verify()
        if img.format not in {'PNG', 'JPEG', 'WEBP', 'GIF'}:
            raise ValueError('Invalid image format')
        file.seek(0)
    except Exception:
        return False, 'Plik nie jest poprawnym plikiem graficznym.', 'danger'
    upload_dir = get_avatar_upload_dir()
    old_filename = user.avatar_filename
    new_filename = f"avatar_{user.id}_{secrets.token_hex(8)}.{ext}"
    file_path = os.path.join(upload_dir, new_filename)
    try:
        file.seek(0)
        re_img = Image.open(file)
        if re_img.width > MAX_AVATAR_DIMENSION or re_img.height > MAX_AVATAR_DIMENSION:
            return False, f'Wymiary obrazu są zbyt duże (maksymalnie {MAX_AVATAR_DIMENSION}x{MAX_AVATAR_DIMENSION} px).', 'danger'
        save_format = 'JPEG' if ext in ('jpg', 'jpeg') else ext.upper()
        if save_format == 'JPEG' and re_img.mode in ('RGBA', 'P'):
            re_img = re_img.convert('RGB')
        re_img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        re_img.save(file_path, format=save_format)
    except Exception:
        remove_user_avatar_file(new_filename)
        return False, 'Nie udało się przetworzyć pliku graficznego.', 'danger'
    try:
        user.avatar_filename = new_filename
        db.session.commit()
        if old_filename and old_filename != new_filename:
            remove_user_avatar_file(old_filename)
        return True, 'Twój awatar został pomyślnie zaktualizowany!', 'success'
    except Exception:
        db.session.rollback()
        remove_user_avatar_file(new_filename)
        return False, 'Wystąpił błąd podczas zapisywania awatara.', 'danger'
def detach_user_avatar(user: User) -> str | None:
    old_filename = user.avatar_filename
    if not old_filename:
        return None
    user.avatar_filename = None
    return old_filename


def delete_user_avatar(user: User) -> tuple[bool, str, str]:
    old_filename = detach_user_avatar(user)
    if old_filename:
        try:
            db.session.commit()
            remove_user_avatar_file(old_filename)
        except Exception:
            db.session.rollback()
            return False, 'Wystąpił błąd podczas usuwania awatara.', 'danger'
    return True, 'Awatar został usunięty. Przywrócono domyślne inicjały.', 'info'

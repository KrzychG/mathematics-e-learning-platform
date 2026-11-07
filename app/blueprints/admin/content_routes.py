from flask import flash, jsonify, redirect, render_template, request, url_for

from app import db
from app.blueprints.admin.routes import admin_bp, admin_required
from app.models import Category, Topic, UNCATEGORIZED_CATEGORY_LABEL
from app.services.admin_service import paginate_clamped
from app.utils import has_duplicate, safe_db_commit

MAX_CATEGORY_NAME_LENGTH = 100
MAX_TOPIC_NAME_LENGTH = 100
MAX_TOPIC_DESC_LENGTH = 255


def _normalize_optional_id(entity_id: int | None) -> int | None:
    return entity_id if entity_id and entity_id > 0 else None


def _resolve_category_id(category_id: int | None) -> tuple[int | None, bool]:
    cat_id = _normalize_optional_id(category_id)
    if cat_id and not db.session.get(Category, cat_id):
        return None, False
    return cat_id, True


def _validate_text_length(
    value: str,
    *,
    max_len: int,
    max_msg: str,
    required_msg: str | None = None,
) -> bool:
    if required_msg and not value:
        flash(required_msg, 'danger')
        return False
    if len(value) > max_len:
        flash(max_msg, 'danger')
        return False
    return True


def _validate_category_name(name: str, exclude_category_id: int | None = None) -> bool:
    valid_len = _validate_text_length(
        name,
        required_msg='Nazwa kategorii nie może być pusta.',
        max_len=MAX_CATEGORY_NAME_LENGTH,
        max_msg=f'Nazwa kategorii może mieć maksymalnie {MAX_CATEGORY_NAME_LENGTH} znaków.',
    )
    if not valid_len:
        return False
    if has_duplicate(Category, Category.name == name, exclude_id=exclude_category_id):
        flash(f'Kategoria "{name}" już istnieje.', 'warning')
        return False
    return True


def _validate_topic_payload(
    name: str,
    category_id: int | None,
    description: str,
    exclude_topic_id: int | None = None,
) -> tuple[int | None, bool]:
    # Walidacja danych tematu w panelu CMS:
    # Sprawdza limity znaków, istnienie wybranej kategorii oraz unikalność nazwy w obrębie tej samej kategorii.
    if not _validate_text_length(
        name,
        required_msg='Nazwa tematu nie może być pusta.',
        max_len=MAX_TOPIC_NAME_LENGTH,
        max_msg=f'Nazwa tematu może mieć maksymalnie {MAX_TOPIC_NAME_LENGTH} znaków.',
    ):
        return None, False
    if not _validate_text_length(
        description,
        max_len=MAX_TOPIC_DESC_LENGTH,
        max_msg=f'Krótki opis tematu może mieć maksymalnie {MAX_TOPIC_DESC_LENGTH} znaków.',
    ):
        return None, False
    cat_id, is_valid = _resolve_category_id(category_id)
    if not is_valid:
        flash('Wybrana kategoria nie istnieje.', 'danger')
        return None, False
    if has_duplicate(
        Topic,
        Topic.category_id == cat_id,
        Topic.name == name,
        exclude_id=exclude_topic_id,
    ):
        flash(f'Temat "{name}" już istnieje w wybranej kategorii.', 'warning')
        return cat_id, False
    return cat_id, True


def _save_category_name(category: Category | None = None):
    name = request.form.get('name', '').strip()
    exclude_id = category.id if category else None
    if not _validate_category_name(name, exclude_category_id=exclude_id):
        return redirect(url_for('admin.admin_content'))
    if category is None:
        db.session.add(Category(name=name))
        success_msg = f'Dodano nową kategorię: {name}.'
        error_msg = 'Wystąpił błąd podczas dodawania kategorii.'
    else:
        category.name = name
        success_msg = f'Zaktualizowano kategorię: {name}.'
        error_msg = 'Wystąpił błąd podczas edycji kategorii.'
    safe_db_commit(success_msg=success_msg, error_msg=error_msg)
    return redirect(url_for('admin.admin_content'))


@admin_bp.route('/admin/content')
@admin_required
def admin_content():
    page = request.args.get('page', 1, type=int)
    per_page = 15
    all_categories, uncategorized_topics = Category.get_syllabus_tree()
    all_topics = [t for cat in all_categories for t in cat.topics] + list(uncategorized_topics)
    total_categories = len(all_categories)
    total_topics = len(all_topics)
    topics_with_theory = sum(1 for t in all_topics if t.has_theory)
    categories_pagination = paginate_clamped(all_categories, page=page, per_page=per_page)
    paged_categories = categories_pagination.items
    return render_template(
        'admin/admin_content.html',
        categories=paged_categories,
        all_categories=all_categories,
        categories_pagination=categories_pagination,
        uncategorized_topics=uncategorized_topics,
        total_categories=total_categories,
        total_topics=total_topics,
        topics_with_theory=topics_with_theory,
        max_cat_len=MAX_CATEGORY_NAME_LENGTH,
        max_topic_len=MAX_TOPIC_NAME_LENGTH,
        max_desc_len=MAX_TOPIC_DESC_LENGTH,
        active_tab='content',
    )
@admin_bp.route('/admin/category/new', methods=['POST'])
@admin_required
def new_category():
    return _save_category_name()
@admin_bp.route('/admin/category/<int:category_id>/edit', methods=['POST'])
@admin_required
def edit_category(category_id):
    cat = db.get_or_404(Category, category_id)
    return _save_category_name(cat)
@admin_bp.route('/admin/category/<int:category_id>/delete', methods=['POST'])
@admin_required
def delete_category(category_id):
    # Usuwanie kategorii z obsługą osieroconych tematów
    # W zależności od wyboru admina w modalu
    # - 'delete_all': kaskadowe usunięcie wszystkich tematów i powiązanych zadań/prób przez ORM
    # - 'detach': odpięcie kategorii tematy lądują w worku "Bez kategorii"
    cat = db.get_or_404(Category, category_id)
    name = cat.name
    action = request.form.get('topic_action', 'detach')
    if cat.topics:
        if action == 'delete_all':
            # Usuwamy przez ORM ze względu na kaskady zadań i postępów
            for topic in list(cat.topics):
                db.session.delete(topic)
            db.session.flush()
            success_msg = f'Usunięto kategorię "{name}" wraz ze wszystkimi przypisanymi tematami.'
        else:
            for topic in list(cat.topics):
                topic.category_id = None
            db.session.flush()
            success_msg = f'Usunięto kategorię "{name}". Przypisane tematy zostały zachowane jako "{UNCATEGORIZED_CATEGORY_LABEL}".'
    else:
        success_msg = f'Usunięto kategorię "{name}".'
    db.session.delete(cat)
    safe_db_commit(
        success_msg=success_msg,
        error_msg=f'Wystąpił błąd podczas usuwania kategorii "{name}".',
    )
    return redirect(url_for('admin.admin_content'))


def _extract_topic_form_data() -> dict:
    return {
        'name': request.form.get('name', '').strip(),
        'category_id': request.form.get('category_id', type=int),
        'description': request.form.get('description', '').strip(),
        'raw_theory': request.form.get('theory', ''),
    }


def _render_topic_edit_form(topic, categories, form_data: dict | None = None):
    context = {
        'topic': topic,
        'categories': categories,
        'max_topic_len': MAX_TOPIC_NAME_LENGTH,
        'max_desc_len': MAX_TOPIC_DESC_LENGTH,
        'active_tab': 'content',
    }
    if form_data is not None:
        context['form_data'] = form_data
    return render_template('admin/admin_topic_edit.html', **context)


@admin_bp.route('/admin/topic/new', methods=['POST'])
@admin_required
def new_topic():
    payload = _extract_topic_form_data()
    cat_id, is_valid = _validate_topic_payload(
        payload['name'], payload['category_id'], payload['description']
    )
    if not is_valid:
        return redirect(url_for('admin.admin_content'))
    topic = Topic(
        name=payload['name'],
        category_id=cat_id,
        description=payload['description'],
        theory=payload['raw_theory'],
    )
    db.session.add(topic)
    if safe_db_commit(
        success_msg=f"Utworzono nowy temat: {payload['name']}. Możesz teraz opracować jego treść w edytorze.",
        error_msg='Wystąpił błąd podczas tworzenia nowego tematu.',
    ):
        return redirect(url_for('admin.edit_topic', topic_id=topic.id))
    return redirect(url_for('admin.admin_content'))


@admin_bp.route('/admin/topic/<int:topic_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_topic(topic_id):
    topic = db.get_or_404(Topic, topic_id)
    categories = Category.query.order_by(Category.id.asc()).all()
    if request.method == 'POST':
        payload = _extract_topic_form_data()
        cat_id, is_valid = _validate_topic_payload(
            payload['name'], payload['category_id'], payload['description'], exclude_topic_id=topic.id
        )
        if is_valid:
            topic.name = payload['name']
            topic.category_id = cat_id
            topic.description = payload['description']
            topic.theory = payload['raw_theory']
            normalized_theory = topic.theory
            if safe_db_commit(
                success_msg=f'Zapisano zmiany w temacie: {topic.name}.',
                error_msg='Wystąpił błąd podczas zapisywania zmian w temacie.',
            ):
                return redirect(url_for('admin.admin_content'))
        else:
            normalized_theory = Topic.normalize_theory_value(payload['raw_theory'])
        form_data = {
            'name': payload['name'],
            'category_id': _normalize_optional_id(payload['category_id']),
            'description': payload['description'],
            'theory': normalized_theory,
        }
        return _render_topic_edit_form(topic, categories, form_data=form_data)
    return _render_topic_edit_form(topic, categories)
@admin_bp.route('/admin/topic/preview', methods=['POST'])
@admin_required
def preview_topic():
    from app.services.theory_renderer_service import render_theory_markdown
    data = request.get_json(silent=True) or {}
    raw_md = data.get('markdown', '')
    html = render_theory_markdown(raw_md)
    return jsonify({'success': True, 'html': html})


@admin_bp.route('/admin/topic/<int:topic_id>/delete', methods=['POST'])
@admin_required
def delete_topic(topic_id):
    topic = db.get_or_404(Topic, topic_id)
    name = topic.name
    db.session.delete(topic)
    safe_db_commit(
        success_msg=f'Usunięto temat "{name}".',
        error_msg=f'Nie można usunąć tematu "{name}": wystąpił błąd spójności danych.',
    )
    return redirect(url_for('admin.admin_content'))

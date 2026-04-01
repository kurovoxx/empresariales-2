from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.database import (
    get_groups, create_group, add_email_to_group, 
    get_emails_by_group, delete_email, update_group_name
)

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/')
def list_groups():
    groups = get_groups()
    return render_template('groups.html', groups=groups)

@groups_bp.route('/admin')
def admin_groups():
    groups = get_groups()
    return render_template('admin_groups.html', groups=groups)

# API: Obtener emails de un grupo
@groups_bp.route('/api/emails/<int:group_id>')
def api_get_emails(group_id):
    emails = get_emails_by_group(group_id)
    return jsonify(emails)

@groups_bp.route('/create', methods=['POST'])
def handle_create_group():
    name = request.form.get('group_name')
    if name:
        try:
            create_group(name)
            flash(f'Grupo "{name}" creado.', 'success')
        except Exception as e: flash(f'Error: {e}', 'error')
    return redirect(url_for('groups.list_groups'))

@groups_bp.route('/update_name', methods=['POST'])
def handle_update_name():
    group_id = request.form.get('group_id')
    new_name = request.form.get('new_name')
    if group_id and new_name:
        try:
            update_group_name(group_id, new_name)
            flash('Nombre de grupo actualizado.', 'success')
        except Exception as e: flash(f'Error: {e}', 'error')
    return redirect(url_for('groups.admin_groups'))

@groups_bp.route('/add_email', methods=['POST'])
def handle_add_email():
    group_id = request.form.get('group_id')
    email = request.form.get('email')
    if group_id and email:
        try:
            add_email_to_group(group_id, email)
            flash(f'Email "{email}" añadido.', 'success')
        except Exception as e: flash(f'Error: {e}', 'error')
    return redirect(url_for('groups.list_groups'))

@groups_bp.route('/delete_email/<int:email_id>')
def handle_delete_email(email_id):
    try:
        delete_email(email_id)
        flash('Email eliminado del grupo.', 'success')
    except Exception as e: flash(f'Error: {e}', 'error')
    return redirect(url_for('groups.admin_groups'))

from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.database import get_groups, get_emails_by_group
from app.services.validator import validate_excel
from app.services.processors.cyber import CyberReportProcessor
from app.services.processors.hr import HRReportProcessor
from app.services.processors.data_analysis import DataAnalysisProcessor
from app.services.mailer import send_email_with_pdf
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    groups = get_groups()
    return render_template('index.html', groups=groups)

@main_bp.route('/process', methods=['POST'])
def process():
    group_id = request.form.get('group_id')
    department = request.form.get('department')
    subject = request.form.get('subject')
    body = request.form.get('body')
    excel_file = request.files.get('excel_file')

    if not excel_file:
        flash('Por favor suba un archivo Excel.', 'error')
        return redirect(url_for('main.index'))

    # Guardar archivo temporalmente
    temp_path = os.path.join('data/temp', excel_file.filename)
    excel_file.save(temp_path)

    # 1. VALIDAR
    is_valid, result = validate_excel(temp_path, department)
    if not is_valid:
        flash(f'Error de Formato: {result}', 'error')
        if os.path.exists(temp_path): os.remove(temp_path)
        return redirect(url_for('main.index'))

    # 2. GENERAR PDF (Basado en el departamento)
    try:
        pdf_output = os.path.join('data/temp', f"reporte_{department}.pdf")
        
        if department == 'cyber':
            processor = CyberReportProcessor(result)
        elif department == 'hr':
            processor = HRReportProcessor(result)
        elif department == 'data':
            processor = DataAnalysisProcessor(result)
        else:
            flash('Departamento no soportado.', 'error')
            return redirect(url_for('main.index'))

        processor.generate_pdf(pdf_output)

        # 3. ENVIAR CORREO (Mailer)
        emails_data = get_emails_by_group(group_id)
        if emails_data:
            # Extraemos solo el campo 'email' de cada diccionario
            emails = [e['email'] for e in emails_data]
            send_email_with_pdf(emails, subject, body, pdf_output)
            flash(f'Éxito: Reporte de {department.upper()} enviado a {len(emails)} destinatarios.', 'success')
        else:
            flash(f'El PDF se generó, pero el grupo no tiene emails.', 'error')
        
        if os.path.exists(pdf_output): os.remove(pdf_output)
        
    except Exception as e:
        flash(f'Error en procesamiento: {str(e)}', 'error')
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

    return redirect(url_for('main.index'))

import os
import datetime
import shutil
from pathlib import Path
from app.models.database import get_emails_by_group
from app.services.validator import validate_excel
from app.services.processors.cyber import CyberReportProcessor
from app.services.processors.hr import HRReportProcessor
from app.services.processors.data_analysis import DataAnalysisProcessor
from app.services.mailer import send_email_with_pdf

def process_scheduled_tasks(app=None):
    # Usar rutas relativas al directorio raíz del proyecto
    base_dir = Path('data/programado')
    if not base_dir.exists():
        return

    now = datetime.datetime.now()

    for folder in base_dir.iterdir():
        if not folder.is_dir():
            continue

        info_file = folder / 'info.txt'
        if not info_file.exists():
            continue

        # Leer metadatos
        info = {}
        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        info[key.strip()] = value.strip()
        except Exception as e:
            print(f"Error leyendo info.txt en {folder.name}: {e}")
            continue

        schedule_time_str = info.get('schedule_time')
        if not schedule_time_str:
            continue

        try:
            schedule_time = datetime.datetime.fromisoformat(schedule_time_str)
        except ValueError:
            continue

        if now >= schedule_time:
            print(f"[{now}] Ejecutando envío programado: {folder.name}")
            
            group_id = info.get('group_id')
            department = info.get('department')
            
            # Envolver en el contexto de la aplicación si se proporcionó una app
            # Esto es necesario para que render_template funcione
            context_manager = app.app_context() if app else None
            
            try:
                if context_manager: context_manager.__enter__()

                with open(folder / 'asunto.txt', 'r', encoding='utf-8') as f:
                    subject = f.read()
                
                with open(folder / 'descripcion.txt', 'r', encoding='utf-8') as f:
                    body = f.read()

                excel_files = list(folder.glob('*.xlsx'))
                if not excel_files:
                    continue
                
                excel_path = excel_files[0]

                # 1. VALIDAR
                is_valid, result = validate_excel(str(excel_path), department)
                if not is_valid:
                    print(f"Error de validación: {result}")
                    continue

                # 2. GENERAR PDF
                pdf_output = folder / f"reporte_{department}.pdf"
                
                if department == 'cyber':
                    processor = CyberReportProcessor(result)
                elif department == 'hr':
                    processor = HRReportProcessor(result)
                elif department == 'data':
                    processor = DataAnalysisProcessor(result)
                else:
                    continue

                processor.generate_pdf(str(pdf_output))

                # 3. ENVIAR CORREO
                emails_data = get_emails_by_group(group_id)
                if emails_data:
                    emails = [e['email'] for e in emails_data]
                    send_email_with_pdf(emails, subject, body, str(pdf_output))
                    print(f"Éxito: Reporte enviado a {len(emails)} destinatarios.")
                    
                    # 4. LIMPIAR
                    shutil.rmtree(folder)
                
            except Exception as e:
                print(f"Error procesando envío {folder.name}: {str(e)}")
            finally:
                if context_manager: context_manager.__exit__(None, None, None)

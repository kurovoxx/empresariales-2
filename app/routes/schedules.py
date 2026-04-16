# app/routes/schedules.py
from flask import Blueprint, request, flash, redirect, url_for, render_template
import pandas as pd
import os

# 1. Crear el Blueprint (esto reemplaza al "app = Flask(__name__)")
schedule_bp = Blueprint('schedule', __name__)

# Diccionario de columnas esperadas
COLUMNAS_ESPERADAS = {
    'cyber': ['ID_Vulnerabilidad', 'Host', 'Severidad', 'Estado'],
    'data': ['Mes', 'Ventas', 'Gastos', 'Clientes_Nuevos'],
    'hr': ['ID_Empleado', 'Nombre', 'Departamento', 'Sueldo', 'Asistencia']
}

# 2. Usar @schedule_bp en lugar de @app
@schedule_bp.route('/schedule/process', methods=['POST'])
def process_schedule():
    schedule_time = request.form.get('schedule_time')
    group_id = request.form.get('group_id')
    department = request.form.get('department')
    subject = request.form.get('subject')
    body = request.form.get('body')
    excel_file = request.files.get('excel_file')

    if not all([schedule_time, group_id, department, subject, body, excel_file]):
        flash("Por favor, completa todos los campos del formulario.", "error")
        return redirect(request.url)

    if excel_file and excel_file.filename.endswith('.xlsx'):
        try:
            df = pd.read_excel(excel_file, nrows=0)
            columnas_del_excel = list(df.columns)
            columnas_requeridas = COLUMNAS_ESPERADAS.get(department, [])
            
            columnas_faltantes = [col for col in columnas_requeridas if col not in columnas_del_excel]
            
            if columnas_faltantes:
                msg = f"Formato incorrecto para '{department}'. Faltan las columnas: {', '.join(columnas_faltantes)}"
                flash(msg, 'error')
                return redirect(request.referrer)
            
            excel_file.seek(0)
            
        except Exception as e:
            flash(f"Error al leer el Excel. Detalle: {str(e)}", 'error')
            return redirect(request.referrer)
    else:
        flash("Por favor, sube un archivo con formato .xlsx válido.", "error")
        return redirect(request.referrer)

    # Simulación de éxito
    flash(f"✅ Excel validado correctamente. Reporte programado para {department}.", "success")
    
    # Redirigir (asegúrate de que 'index' exista en tus otras rutas)
    return redirect(url_for('main.index')) # Ajusta esto según cómo se llame tu ruta principal
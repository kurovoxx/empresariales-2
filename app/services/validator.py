import pandas as pd

# Esquemas de columnas por departamento
DEPARTMENT_SCHEMAS = {
    'cyber': ['ID_Vulnerabilidad', 'Host', 'Severidad', 'Estado'],
    'hr': ['ID_Empleado', 'Nombre', 'Departamento', 'Sueldo', 'Asistencia'],
    'data': ['Mes', 'Ventas', 'Gastos', 'Clientes_Nuevos']
}

def validate_excel(file_path, department):
    """
    Valida si el archivo Excel contiene las columnas requeridas para el departamento.
    Retorna (True, df) si es válido, (False, error_msg) si no.
    """
    try:
        df = pd.read_excel(file_path)
        required_columns = DEPARTMENT_SCHEMAS.get(department, [])
        
        # Verificar si todas las columnas requeridas están en el dataframe
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return False, f"Faltan las siguientes columnas: {', '.join(missing_columns)}"
        
        return True, df
    except Exception as e:
        return False, f"Error al leer el archivo: {str(e)}"

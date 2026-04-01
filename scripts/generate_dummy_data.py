import pandas as pd
import os

def generate_samples():
    os.makedirs('data/samples', exist_ok=True)
    
    # Datos de prueba para Ciberseguridad
    cyber_data = {
        'ID_Vulnerabilidad': ['CVE-2023-001', 'CVE-2023-002', 'CVE-2023-003', 'CVE-2023-004'],
        'Host': ['192.168.1.10', '192.168.1.15', '10.0.0.5', '192.168.1.10'],
        'Severidad': ['Alta', 'Crítica', 'Media', 'Baja'],
        'Estado': ['Abierto', 'En progreso', 'Cerrado', 'Abierto']
    }
    df_cyber = pd.DataFrame(cyber_data)
    df_cyber.to_excel('data/samples/cyber_report.xlsx', index=False)
    print("✓ Creado: data/samples/cyber_report.xlsx")

    # Datos de prueba para RRHH
    hr_data = {
        'ID_Empleado': [101, 102, 103, 104],
        'Nombre': ['Juan Pérez', 'María García', 'Carlos Ruiz', 'Ana López'],
        'Departamento': ['TI', 'Marketing', 'TI', 'Finanzas'],
        'Sueldo': [2500, 2800, 2400, 3100],
        'Asistencia': ['95%', '100%', '88%', '92%']
    }
    df_hr = pd.DataFrame(hr_data)
    df_hr.to_excel('data/samples/hr_report.xlsx', index=False)
    print("✓ Creado: data/samples/hr_report.xlsx")

    # Datos de prueba para Data Analysis
    data_analysis = {
        'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'Ventas': [15000, 18000, 16500, 21000, 19000, 25000],
        'Gastos': [12000, 11000, 13000, 14000, 12500, 15000],
        'Clientes_Nuevos': [45, 52, 48, 61, 55, 70]
    }
    df_data = pd.DataFrame(data_analysis)
    df_data.to_excel('data/samples/data_report.xlsx', index=False)
    print("✓ Creado: data/samples/data_report.xlsx")

if __name__ == "__main__":
    generate_samples()

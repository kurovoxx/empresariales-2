from .base import BaseReportProcessor
from datetime import datetime

class HRReportProcessor(BaseReportProcessor):
    def __init__(self, df):
        super().__init__(df, 'hr_template.html')

    def prepare_data(self):
        empleados = self.df.to_dict('records')
        
        # Calcular algunas métricas básicas
        promedio_sueldo = self.df['Sueldo'].mean()
        max_asistencia = self.df['Asistencia'].max()

        return {
            'empleados': empleados,
            'total_empleados': len(empleados),
            'promedio_sueldo': f"${promedio_sueldo:,.2f}",
            'max_asistencia': max_asistencia,
            'fecha_reporte': datetime.now().strftime('%d/%m/%Y')
        }

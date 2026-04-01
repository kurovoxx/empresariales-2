from .base import BaseReportProcessor
from datetime import datetime

class CyberReportProcessor(BaseReportProcessor):
    def __init__(self, df):
        super().__init__(df, 'cyber_template.html')

    def prepare_data(self):
        """Prepara un resumen de vulnerabilidades para la plantilla."""
        vulnerabilidades = self.df.to_dict('records')
        total_vulnerabilidades = len(vulnerabilidades)
        
        # Conteo por severidad
        severidad_counts = self.df['Severidad'].value_counts().to_dict()

        return {
            'vulnerabilidades': vulnerabilidades,
            'total': total_vulnerabilidades,
            'fecha_reporte': datetime.now().strftime('%d/%m/%Y'),
            'counts': severidad_counts
        }

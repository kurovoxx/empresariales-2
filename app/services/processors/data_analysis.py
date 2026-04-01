from .base import BaseReportProcessor
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

class DataAnalysisProcessor(BaseReportProcessor):
    def __init__(self, df):
        super().__init__(df, 'data_template.html')

    def generate_chart_base64(self):
        """Genera un gráfico de barras comparando Ventas vs Gastos."""
        plt.figure(figsize=(8, 4))
        plt.bar(self.df['Mes'], self.df['Ventas'], label='Ventas', color='skyblue')
        plt.plot(self.df['Mes'], self.df['Gastos'], label='Gastos', color='red', marker='o')
        plt.title('Rendimiento Mensual')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Guardar en buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close() # Importante cerrar el gráfico
        return img_base64

    def prepare_data(self):
        # Convertir a dict para la tabla
        datos = self.df.to_dict('records')
        chart_img = self.generate_chart_base64()

        # Calcular totales
        total_ventas = self.df['Ventas'].sum()
        total_gastos = self.df['Gastos'].sum()
        utilidad = total_ventas - total_gastos

        return {
            'datos': datos,
            'total_ventas': f"${total_ventas:,.2f}",
            'utilidad': f"${utilidad:,.2f}",
            'chart_img': chart_img,
            'fecha_reporte': datetime.now().strftime('%d/%m/%Y')
        }

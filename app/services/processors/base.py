from abc import ABC, abstractmethod
from flask import render_template
from weasyprint import HTML
import os

class BaseReportProcessor(ABC):
    def __init__(self, df, template_name):
        self.df = df
        self.template_name = template_name

    @abstractmethod
    def prepare_data(self):
        """Prepara los datos específicos para la plantilla HTML."""
        pass

    def generate_pdf(self, output_path):
        """Genera el PDF usando WeasyPrint."""
        report_data = self.prepare_data()
        html_string = render_template(f'pdf/{self.template_name}', **report_data)
        
        # Generar el PDF
        HTML(string=html_string).write_pdf(output_path)
        return output_path

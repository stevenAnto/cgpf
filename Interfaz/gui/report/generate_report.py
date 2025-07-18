from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle,
    Spacer, Image, PageBreak
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class ReportGenerator:
    def __init__(self, tmp_dir="__tmp_report"):
        self.tmp_dir = tmp_dir
        os.makedirs(self.tmp_dir, exist_ok=True)

        self.styles = getSampleStyleSheet()

        # Custom styles
        self.styles.add(ParagraphStyle('TitleCustom', fontSize=20, alignment=TA_CENTER, leading=24, spaceAfter=18))
        self.styles.add(ParagraphStyle('HeadingCustom', parent=self.styles['Heading2'],
                                       fontSize=14, leading=18, spaceBefore=6, spaceAfter=6))
        self.styles.add(ParagraphStyle('NormalSmall', parent=self.styles['Normal'],
                                       fontSize=11, leading=14, spaceAfter=6))

        # Modificar estilo Heading1 existente
        self.styles['Heading1'].fontSize = 14
        self.styles['Heading1'].spaceBefore = 12
        self.styles['Heading1'].spaceAfter = 6
        self.styles['Heading1'].outlineLevel = 1  # Nivel para TOC

        self.table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A4A4A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ])

    def convertir_a_segundos(self, t):
        partes = t.strip().split("-")
        try:
            nums = [int(p) for p in partes][::-1]
            ms = nums[0] if len(nums) > 0 else 0
            s = nums[1] if len(nums) > 1 else 0
            m = nums[2] if len(nums) > 2 else 0
            h = nums[3] if len(nums) > 3 else 0
            return h * 3600 + m * 60 + s + ms / 1000
        except:
            return 0

    def generar_charts(self, df):
        cats = df['Categoria'].value_counts().sort_index()
        fig1, ax1 = plt.subplots(figsize=(4, 4))
        ax1.pie(cats.values, labels=cats.index, autopct='%1.1f%%', startangle=90)
        ax1.set_title("Participantes por Categoría")
        ax1.axis('equal')
        pie_path = os.path.join(self.tmp_dir, "pie_categoria.png")
        fig1.tight_layout()
        fig1.savefig(pie_path)
        plt.close(fig1)

        times = np.sort(df['Tiempo_s'])
        cdf = np.arange(1, len(times) + 1) / len(times)
        fig2, ax2 = plt.subplots(figsize=(4, 4))
        ax2.step(times, cdf, where='post', label='Escalonada', color='#1f77b4')
        xs = np.linspace(times.min(), times.max(), 300)
        coefs = np.polyfit(times, cdf, deg=3)
        ys = np.clip(np.poly1d(coefs)(xs), 0, 1)
        ax2.plot(xs, ys, '-', label='Curva suave', color='#ff7f0e')
        ax2.set_title("CDF de Tiempos")
        ax2.set_xlabel("Tiempo (s)")
        ax2.set_ylabel("Proporción Acumulada")
        ax2.legend(fontsize=8)
        cdf_path = os.path.join(self.tmp_dir, "cdf_tiempos.png")
        fig2.tight_layout()
        fig2.savefig(cdf_path)
        plt.close(fig2)

        return pie_path, cdf_path

    def _add_page_number(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.drawCentredString(10.5 * cm, 1.5 * cm, f"Página {doc.page}")
        canvas.restoreState()

    def generate_report(self, csv_path, output_pdf, nombre_proyecto=""):
        df = pd.read_csv(csv_path)
        df.columns = [c.strip() for c in df.columns]
        df['Tiempo_s'] = df['Tiempo'].astype(str).apply(self.convertir_a_segundos)
        df_sorted = df.sort_values('Tiempo_s').reset_index(drop=True)
        df_sorted['Posición'] = df_sorted.index + 1

        total = len(df_sorted)
        prom = df_sorted['Tiempo_s'].mean()
        mins = df_sorted['Tiempo_s'].min()
        maxs = df_sorted['Tiempo_s'].max()

        pie_img, cdf_img = self.generar_charts(df_sorted)

        doc = SimpleDocTemplate(output_pdf, pagesize=letter,
                                leftMargin=2 * cm, rightMargin=2 * cm,
                                topMargin=2 * cm, bottomMargin=2 * cm)

        elements = []
        toc = TableOfContents()
        toc.levelStyles = [
            ParagraphStyle(fontName='Helvetica-Bold', fontSize=12, name='TOC1',
                           leftIndent=20, firstLineIndent=-20, spaceBefore=5,
                           fontColor=colors.blue, leading=16),
        ]

        # Portada
        elements.append(Spacer(1, 5 * cm))
        elements.append(Paragraph("Informe de Resultados de Carrera", self.styles['TitleCustom']))
        if nombre_proyecto:
            elements.append(Spacer(1, 1 * cm))
            elements.append(Paragraph(nombre_proyecto, self.styles['HeadingCustom']))
        elements.append(PageBreak())

        # Índice
        elements.append(Paragraph("Índice de Contenidos", self.styles['Heading1']))
        elements.append(Spacer(1, 0.3 * cm))
        elements.append(toc)
        elements.append(PageBreak())

        # Función para manejar el TOC
        def afterFlowable(flowable):
            if isinstance(flowable, Paragraph):
                style_name = flowable.style.name
                if style_name == 'Heading1' and flowable.getPlainText() != "Índice de Contenidos":
                    text = flowable.getPlainText()
                    key = f"HEAD_{text.replace(' ', '_')}"
                    doc.canv.bookmarkPage(key)
                    toc.addEntry(0, text, doc.page, key=key)

        doc.afterFlowable = afterFlowable

        # Sección 1 - Ranking
        title1 = Paragraph("1. Ranking de Resultados", self.styles['Heading1'])
        elements.append(title1)
        
        table_data = [["Posición", "Dorsal", "Nombre", "Tiempo", "Categoría"]]
        for _, row in df_sorted.iterrows():
            table_data.append([
                int(row['Posición']),
                row['Dorsal'],
                row['Nombre'],
                row['Tiempo'],
                row['Categoria']
            ])
        tbl = Table(table_data, hAlign='CENTER')
        tbl.setStyle(self.table_style)
        elements.append(tbl)
        elements.append(PageBreak())

        # Sección 2 - Gráficos
        title2 = Paragraph("2. Gráficos", self.styles['Heading1'])
        elements.append(title2)
        
        img_row = Table([
            [Image(pie_img, width=8 * cm, height=8 * cm)],
            [Image(cdf_img, width=8 * cm, height=8 * cm)]
        ], hAlign='CENTER')
        elements.append(img_row)
        elements.append(PageBreak())

        # Sección 3 - Estadísticas
        title3 = Paragraph("3. Estadísticas Generales", self.styles['Heading1'])
        elements.append(title3)

        stats_txt = (
            f"Total de participantes: {total}<br/><br/>"
            f"Tiempo promedio: {prom:.2f} s<br/><br/>"
            f"Tiempo mínimo: {mins:.2f} s<br/><br/>"
            f"Tiempo máximo: {maxs:.2f} s"
        )
        elements.append(Paragraph(stats_txt, self.styles['NormalSmall']))

        # Construir documento
        doc.multiBuild(elements, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number)

        # Limpiar imágenes temporales
        for f in os.listdir(self.tmp_dir):
            os.remove(os.path.join(self.tmp_dir, f))
        os.rmdir(self.tmp_dir)
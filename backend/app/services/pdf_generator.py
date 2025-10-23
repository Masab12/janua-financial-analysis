"""
PDF Report Generator for Financial Analysis
Generates PDF matching EXACTLY the client's Relatório format
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from datetime import datetime
from io import BytesIO
import os


class FinancialPDFGenerator:
    """Generate PDF reports matching client's exact Relatório format"""
    
    def __init__(self):
        self.buffer = BytesIO()
        self.pagesize = A4
        self.width, self.height = self.pagesize
        self.navy_color = colors.HexColor('#1a1a1a')  # Dark color for text
        self.light_gray = colors.HexColor('#f5f5f5')
        
    def _create_logo_box(self):
        """Create logo box - removed placeholder text as per client request"""
        logo_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'frontend', 'public', 'logo_blue.png')
        
        if os.path.exists(logo_path):
            try:
                from PIL import Image as PILImage
                PILImage.MAX_IMAGE_PIXELS = None
                pil_img = PILImage.open(logo_path)
                pil_img.thumbnail((200, 200), PILImage.Resampling.LANCZOS)
                temp_path = os.path.join(os.path.dirname(logo_path), 'logo_temp.png')
                pil_img.save(temp_path, 'PNG')
                return Image(temp_path, width=2.5*cm, height=2.5*cm)
            except:
                pass
        
        # Return empty space instead of placeholder text
        empty_space = Paragraph('', ParagraphStyle('Empty', fontSize=8))
        logo_table = Table([[empty_space]], colWidths=[2.5*cm], rowHeights=[2.5*cm])
        logo_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        return logo_table
    
    def generate_report(self, empresa_nome: str, metrics: dict, balance_sheet: dict, income_statement: dict) -> BytesIO:
        """
        Generate PDF matching client's EXACT format
        Page 1: Company info + Financial data
        Page 2: 8 indicators in 2x4 grid
        """
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=self.pagesize,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )
        
        story = []
        
        # ========== PAGE 1 ==========
        
        # Title
        story.append(Paragraph("<b>Relatório Performance Financeira e Análise de Investimento</b>", 
                              ParagraphStyle('Title', fontSize=13, fontName='Helvetica-Bold', 
                                           alignment=TA_CENTER, spaceAfter=12)))
        
        # Company name and logo in header
        logo = self._create_logo_box()
        header_table = Table(
            [[Paragraph(f"<b>{empresa_nome}</b>", 
                       ParagraphStyle('CompName', fontSize=14, fontName='Helvetica-Bold')), logo]],
            colWidths=[13.5*cm, 3*cm]
        )
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 0.4*cm))
        
        # Company info fields
        info_style = ParagraphStyle('Info', fontSize=9, spaceAfter=4)
        story.append(Paragraph("<b>Setor de Atividade da Empresa</b>", info_style))
        story.append(Paragraph(f"<b>Data da Análise</b> {datetime.now().strftime('%d/%m/%Y')}", info_style))
        story.append(Paragraph("<b>Objetivo do Relatório</b>", info_style))
        story.append(Paragraph("<b>Descrição</b>", info_style))
        story.append(Spacer(1, 0.6*cm))
        
        # Section title
        story.append(Paragraph("<b>Dados Contabilísticos para N+2 (atual)</b>", 
                              ParagraphStyle('SecTitle', fontSize=11, fontName='Helvetica-Bold', spaceAfter=8)))
        
        # Financial data - EXACT client format
        bold_style = ParagraphStyle('Bold', fontSize=10, fontName='Helvetica-Bold')
        normal_style = ParagraphStyle('Normal', fontSize=9, leftIndent=15)
        
        fin_data = [
            [Paragraph("<b>Total do Ativo</b>", bold_style), 
             Paragraph(f"<b>{self._format_currency(balance_sheet.get('total_ativo', 0))}</b>", bold_style)],
            [Paragraph("<b>Total do Passivo</b>", bold_style), 
             Paragraph(f"<b>{self._format_currency(balance_sheet.get('total_passivo', 0))}</b>", bold_style)],
            [Paragraph("<b>Faturação (vendas)</b>", bold_style), 
             Paragraph(f"<b>{self._format_currency(income_statement.get('vendas_servicos_prestados', 0))}</b>", bold_style)],
            [Paragraph("CMVMC", normal_style), 
             Paragraph(self._format_currency(income_statement.get('cmvmc', 0)), normal_style)],
            [Paragraph("EBITDA", normal_style), 
             Paragraph(self._format_currency(metrics.get('excedente_bruto_exploracao', {}).get('year_n', 0)), normal_style)],
            [Paragraph("EBIT", normal_style), 
             Paragraph(self._format_currency(income_statement.get('ebit', 0)), normal_style)],
            [Paragraph("<b>Resultado antes de impostos</b>", bold_style), 
             Paragraph(f"<b>{self._format_currency(income_statement.get('resultado_antes_impostos', 0))}</b>", bold_style)],
            [Paragraph("<b>Imposto sobre o rendimento</b>", bold_style), 
             Paragraph(f"<b>{self._format_currency(income_statement.get('imposto_rendimento', 0))}</b>", bold_style)],
            [Paragraph("<b>Resultado líquido do período</b>", bold_style), 
             Paragraph(f"<b>{self._format_currency(income_statement.get('resultado_liquido', 0))}</b>", bold_style)],
        ]
        
        fin_table = Table(fin_data, colWidths=[10*cm, 6*cm])
        fin_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(fin_table)
        story.append(Spacer(1, 0.8*cm))
        
        # Comment box
        story.append(Paragraph("<b>Comentário pessoal</b>", 
                              ParagraphStyle('ComLabel', fontSize=9, fontName='Helvetica-Bold', spaceAfter=4)))
        comment_box = Table([['']],  colWidths=[16*cm], rowHeights=[2*cm])
        comment_box.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(comment_box)
        
        # ========== PAGE 2 ==========
        story.append(PageBreak())
        
        story.append(Paragraph("<b>Relatório Performance Financeira e Análise de Investimento</b>", 
                              ParagraphStyle('Title2', fontSize=13, fontName='Helvetica-Bold', 
                                           alignment=TA_CENTER, spaceAfter=8)))
        story.append(Paragraph(f"<b>{empresa_nome}</b>", 
                              ParagraphStyle('CompName2', fontSize=12, fontName='Helvetica-Bold', 
                                           alignment=TA_CENTER, spaceAfter=12)))
        story.append(Paragraph("<b>Análise da Performance Financeira</b>", 
                              ParagraphStyle('AnalTitle', fontSize=11, fontName='Helvetica-Bold', 
                                           alignment=TA_CENTER, spaceAfter=10)))
        
        # Get 8 indicators
        indicators = self._get_analysis_indicators(metrics)
        
        # Create 2x4 grid - EXACT client format
        name_style = ParagraphStyle('Name', fontSize=9, fontName='Helvetica-Bold', alignment=TA_CENTER)
        value_style = ParagraphStyle('Val', fontSize=16, fontName='Helvetica-Bold', alignment=TA_CENTER)
        comment_style = ParagraphStyle('Com', fontSize=7, alignment=TA_LEFT)
        
        # Build 4 rows x 2 columns
        grid_data = []
        for i in range(0, 8, 2):
            row = []
            for j in range(2):
                idx = i + j
                if idx < len(indicators):
                    ind = indicators[idx]
                    # Each cell: name, value, comment
                    cell = Table([
                        [Paragraph(f"<b>{ind['nome']}</b>", name_style)],
                        [Paragraph(f"<b>{ind['valor']}</b>", value_style)],
                        [Paragraph(ind['comentario'], comment_style)]
                    ], colWidths=[7.5*cm])
                    cell.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('TOPPADDING', (0, 0), (-1, 0), 8),
                        ('TOPPADDING', (0, 1), (-1, 1), 4),
                        ('TOPPADDING', (0, 2), (-1, 2), 8),
                        ('BOTTOMPADDING', (0, 2), (-1, 2), 8),
                    ]))
                    row.append(cell)
            grid_data.append(row)
        
        grid = Table(grid_data, colWidths=[8*cm, 8*cm])
        grid.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(grid)
        story.append(Spacer(1, 0.8*cm))
        
        # Comment box
        story.append(Paragraph("<b>Comentário pessoal</b>", 
                              ParagraphStyle('ComLabel2', fontSize=9, fontName='Helvetica-Bold', spaceAfter=4)))
        comment_box2 = Table([['']],  colWidths=[16*cm], rowHeights=[1.5*cm])
        comment_box2.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(comment_box2)
        
        # Footer
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("<para align='center'>powered by <b>JANUA</b></para>",
                              ParagraphStyle('Footer', fontSize=9, fontName='Helvetica-Bold')))
        
        # ========== PAGE 3: Investment Capacity Analysis ==========
        story.append(PageBreak())
        
        # Page 3 header
        title_style3 = ParagraphStyle('Title3', fontSize=13, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=8)
        story.append(Paragraph("<b>Relatório Performance Financeira e Análise de Investimento</b>", title_style3))
        story.append(Paragraph(f"<b>{empresa_nome}</b>", 
                              ParagraphStyle('CompName3', fontSize=12, fontName='Helvetica-Bold', 
                                           alignment=TA_CENTER, spaceAfter=12)))
        
        # Section title
        story.append(Paragraph("<b>A empresa tem capacidade para investir?</b>", 
                              ParagraphStyle('InvestTitle', fontSize=11, textColor=self.navy_color,
                                           fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=12)))
        
        # Get investment capacity data
        capacity_data = self._get_investment_capacity(metrics)
        
        # Create capacity table
        cap_table_data = []
        for item in capacity_data:
            cap_table_data.append([
                Paragraph(f"<b>{item['nome']}</b>", 
                         ParagraphStyle('CapName', fontSize=9, fontName='Helvetica-Bold')),
                Paragraph(f"<b>{item['valor']}</b>", 
                         ParagraphStyle('CapVal', fontSize=10, fontName='Helvetica-Bold', alignment=TA_CENTER)),
                Paragraph(f"Recomendado<br/>{item['recomendado']}", 
                         ParagraphStyle('CapRec', fontSize=7, alignment=TA_CENTER)),
                Paragraph(item['comentario'], 
                         ParagraphStyle('CapCom', fontSize=7))
            ])
        
        capacity_table = Table(cap_table_data, colWidths=[4*cm, 2.5*cm, 3*cm, 7*cm])
        capacity_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(capacity_table)
        story.append(Spacer(1, 0.8*cm))
        
        # Overall recommendation
        overall_rec = self._get_overall_investment_recommendation(metrics)
        rec_style = ParagraphStyle('OverallRec', fontSize=10, fontName='Helvetica-Bold', 
                                   alignment=TA_CENTER, textColor=overall_rec['color'])
        story.append(Paragraph(overall_rec['text'], rec_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Comment boxes
        story.append(Paragraph("<b>Comentário</b>", 
                              ParagraphStyle('ComLabel3', fontSize=9, fontName='Helvetica-Bold', spaceAfter=4)))
        comment_box3 = Table([['']],  colWidths=[16*cm], rowHeights=[1.5*cm])
        comment_box3.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(comment_box3)
        
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph("<b>Comentário pessoal</b>", 
                              ParagraphStyle('ComLabel4', fontSize=9, fontName='Helvetica-Bold', spaceAfter=4)))
        comment_box4 = Table([['']],  colWidths=[16*cm], rowHeights=[1.5*cm])
        comment_box4.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(comment_box4)
        
        # Footer
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("<para align='center'>powered by <b>JANUA</b></para>",
                              ParagraphStyle('Footer3', fontSize=9, fontName='Helvetica-Bold')))
        
        # Build PDF
        doc.build(story)
        self.buffer.seek(0)
        return self.buffer
    
    def _format_currency(self, value):
        """Format value as Portuguese currency"""
        if value is None or value == 0:
            return "0,00 €"
        # Format with space as thousands separator and comma as decimal
        return f"{value:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', ' ')
    
    def _format_percent(self, value):
        """Format value as percentage"""
        if value is None:
            return "-"
        return f"{value:.2f}%"
    
    def _get_analysis_indicators(self, metrics):
        """Get 8 indicators with SHORT comments matching client format"""
        
        indicators = []
        
        # 1. ROE
        roe = metrics.get('return_on_equity', {})
        roe_val = roe.get('year_n', 0) * 100
        tend = roe.get('tendencia', '►')
        indicators.append({
            'nome': 'Return on Equity (ROE)',
            'valor': f"{roe_val:.2f}%",
            'comentario': f"{tend} A rentabilidade para os sócios manteve-se estável."
        })
        
        # 2. ROA
        roa = metrics.get('return_on_assets', {})
        roa_val = roa.get('year_n', 0) * 100
        tend = roa.get('tendencia', '►')
        indicators.append({
            'nome': 'Return on Assets (ROA)',
            'valor': f"{roa_val:.2f}%",
            'comentario': f"{tend} A empresa melhorou a capacidade de gerar resultados operacionais com o total dos ativos investidos."
        })
        
        # 3. Autonomia Financeira
        raf = metrics.get('racio_autonomia_financeira', {})
        raf_val = raf.get('year_n', 0) * 100
        tend = raf.get('tendencia', '►')
        indicators.append({
            'nome': 'Autonomia Financeira',
            'valor': f"{raf_val:.2f}%",
            'comentario': f"{tend} Autonomia financeira razoável, mas atenção ao equilíbrio entre capitais próprios e alheios."
        })
        
        # 4. Cobertura de Gastos
        rcgf = metrics.get('racio_cobertura_gastos_financiamento', {})
        rcgf_val = rcgf.get('year_n', 0)
        tend = rcgf.get('tendencia', '►')
        indicators.append({
            'nome': 'Cobertura de Gastos de Financiamento',
            'valor': f"{rcgf_val:.2f}x",
            'comentario': f"{tend} A empresa tem boa capacidade para suportar custos financeiros. Este indicador melhorou face ao último ano."
        })
        
        # 5. Resumo do Balanço
        rbf = metrics.get('resumo_balanco_funcional', {})
        status = rbf.get('status', 'Médio')
        msg = rbf.get('mensagem', '')
        tend = '▼' if status == 'Mau' else ('▲' if status == 'Bom' else '►')
        indicators.append({
            'nome': 'Resumo do Balanço',
            'valor': status,
            'comentario': f"{tend} {msg}"
        })
        
        # 6. Liquidez Geral
        lg = metrics.get('liquidez_geral', {})
        lg_val = lg.get('year_n', 0) * 100
        tend = lg.get('tendencia', '►')
        indicators.append({
            'nome': 'Liquidez Geral',
            'valor': f"{lg_val:.2f}%",
            'comentario': f"{tend} A empresa pode ter dificuldades em cumprir os compromissos de curto prazo. Indicador diminuiu face aos anos anteriores, piorando a situação financeira."
        })
        
        # 7. Rotação do Ativo
        rat = metrics.get('rotacao_ativo', {})
        rat_val = rat.get('year_n', 0) * 100
        tend = rat.get('tendencia', '►')
        indicators.append({
            'nome': 'Rotação do Ativo',
            'valor': f"{rat_val:.2f}%",
            'comentario': f"{tend} A empresa está mais eficiente em gerar vendas com o investimento total face aos anos anteriores."
        })
        
        # 8. Grau de Alavanca Financeira
        gaf = metrics.get('grau_alavanca_financeira', {})
        gaf_val = gaf.get('year_n', 0) * 100
        tend = gaf.get('tendencia', '►')
        indicators.append({
            'nome': 'Grau de Alavanca Financeira',
            'valor': f"{gaf_val:.2f}%",
            'comentario': f"{tend} O risco financeiro manteve-se estável."
        })
        
        return indicators

    
    def _get_investment_capacity(self, metrics):
        """Get 5 key ratios for investment capacity analysis"""
        
        capacity = []
        
        # 1. Liquidez Geral
        lg = metrics.get('liquidez_geral', {})
        lg_val = lg.get('year_n', 0) * 100
        tend = lg.get('tendencia', '►')
        lg_ok = lg_val >= 150
        capacity.append({
            'nome': 'Liquidez Geral',
            'valor': f"{lg_val:.2f}%",
            'recomendado': 'Maior que 150,00%',
            'comentario': f"{tend} {'A liquidez é inferior ao ideal para realizar um investimento.' if not lg_ok else 'Liquidez adequada para investimento.'}"
        })
        
        # 2. Autonomia Financeira
        raf = metrics.get('racio_autonomia_financeira', {})
        raf_val = raf.get('year_n', 0) * 100
        tend = raf.get('tendencia', '►')
        raf_ok = raf_val >= 33
        capacity.append({
            'nome': 'Autonomia Financeira',
            'valor': f"{raf_val:.2f}%",
            'recomendado': 'Maior que 33,00%',
            'comentario': f"{'▲' if raf_ok else '▼'} {'A empresa tem boa autonomia e reduzida dependência externa.' if raf_ok else 'Autonomia financeira insuficiente para investimento seguro.'}"
        })
        
        # 3. Rentabilidade do Capital Próprio (ROE)
        roe = metrics.get('return_on_equity', {})
        roe_val = roe.get('year_n', 0) * 100
        tend = roe.get('tendencia', '►')
        roe_ok = roe_val >= 5
        capacity.append({
            'nome': 'Rentabilidade do Capital Próprio (ROE)',
            'valor': f"{roe_val:.2f}%",
            'recomendado': 'Maior que 5,00%',
            'comentario': f"{'▲' if roe_ok else '▼'} {'A empresa está a rentabilizar bem o capital dos sócios.' if roe_ok else 'Rentabilidade insuficiente.'}"
        })
        
        # 4. Cobertura de Gastos de Financiamento
        rcgf = metrics.get('racio_cobertura_gastos_financiamento', {})
        rcgf_val = rcgf.get('year_n', 0)
        tend = rcgf.get('tendencia', '►')
        rcgf_ok = rcgf_val >= 2
        capacity.append({
            'nome': 'Cobertura de Gastos de Financiamento',
            'valor': f"{rcgf_val:.2f}x",
            'recomendado': 'Maior que 2,00x',
            'comentario': f"{'▲' if rcgf_ok else '▼'} {'A cobertura de juros é boa, há margem para financiar.' if rcgf_ok else 'Cobertura de juros insuficiente.'}"
        })
        
        # 5. Rácio de Endividamento
        re = metrics.get('racio_endividamento', {})
        re_val = re.get('year_n', 0) * 100
        tend = re.get('tendencia', '►')
        re_ok = re_val <= 66
        capacity.append({
            'nome': 'Rácio de Endividamento',
            'valor': f"{re_val:.2f}%",
            'recomendado': 'Menor que 66,00%',
            'comentario': f"{'▲' if re_ok else '▼'} {'O nível de endividamento está dentro dos limites saudáveis.' if re_ok else 'Endividamento excessivo.'}"
        })
        
        return capacity
    
    def _get_overall_investment_recommendation(self, metrics):
        """Generate overall investment recommendation based on key ratios"""
        
        # Get key values
        lg = metrics.get('liquidez_geral', {}).get('year_n', 0) * 100
        raf = metrics.get('racio_autonomia_financeira', {}).get('year_n', 0) * 100
        roe = metrics.get('return_on_equity', {}).get('year_n', 0) * 100
        rcgf = metrics.get('racio_cobertura_gastos_financiamento', {}).get('year_n', 0)
        re = metrics.get('racio_endividamento', {}).get('year_n', 0) * 100
        
        # Check criteria
        lg_ok = lg >= 150
        raf_ok = raf >= 33
        roe_ok = roe >= 5
        rcgf_ok = rcgf >= 2
        re_ok = re <= 66
        
        # Count how many are OK
        ok_count = sum([lg_ok, raf_ok, roe_ok, rcgf_ok, re_ok])
        
        if ok_count >= 4:
            return {
                'text': '✅ A empresa tem boa capacidade para investir. Estrutura financeira sólida e rentabilidade adequada.',
                'color': colors.HexColor('#28a745')
            }
        elif ok_count >= 3:
            return {
                'text': '⚠️ Boa estrutura e rentabilidade, mas sem liquidez. O investimento só deve avançar após reforço de tesouraria.',
                'color': colors.HexColor('#fd7e14')
            }
        else:
            return {
                'text': '❌ A empresa não tem capacidade para investir neste momento. Recomenda-se melhorar a estrutura financeira primeiro.',
                'color': colors.HexColor('#dc3545')
            }

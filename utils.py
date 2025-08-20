from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

def get_common_questions():
    """Return list of common medical questions in Indonesian"""
    return [
        "Apa diagnosis dari kondisi saya saat ini?",
        "Apa penyebab dari kondisi saya?",
        "Apakah ada tes atau pemeriksaan lebih lanjut yang saya perlukan?",
        "Apa saja pilihan pengobatan yang tersedia?",
        "Apa manfaat dan risiko dari setiap pilihan pengobatan?",
        "Apa efek samping dari obat yang diresepkan?",
        "Berapa lama saya harus minum obat ini?",
        "Apakah ada pantangan makanan atau aktivitas yang harus saya hindari?",
        "Apa yang harus saya lakukan jika gejala memburuk?",
        "Kapan saya harus kontrol kembali?",
        "Apakah kondisi ini menular?",
        "Bagaimana cara mencegah kondisi ini berulang?",
        "Apakah ada perubahan gaya hidup yang perlu saya lakukan?",
        "Apa yang bisa saya lakukan di rumah untuk membantu pemulihan?",
        "Apakah kondisi ini akan mempengaruhi aktivitas sehari-hari saya?",
        "Apa tanda-tanda bahaya yang harus saya waspadai?",
        "Apakah saya perlu rujukan ke dokter spesialis?",
        "Berapa biaya pengobatan yang diperlukan?",
        "Apakah ada pengobatan alternatif yang bisa saya coba?",
        "Bagaimana prognosis atau perkiraan kesembuhan kondisi saya?"
    ]

def generate_pdf_summary(session_state):
    """Generate PDF summary of the consultation preparation"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.HexColor('#1E40AF')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#1F2937')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Build content
    story = []
    
    # Title
    title = Paragraph("Ringkasan untuk Konsultasi Dokter", title_style)
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Patient info table
    patient_data = [
        ['Pasien:', session_state.patient_name or '-'],
        ['Dokter:', session_state.doctor_name or '-'],
        ['Tanggal:', f"{session_state.appointment_date.strftime('%d/%m/%Y')} pukul {session_state.appointment_time.strftime('%H:%M')}"]
    ]
    
    patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    # Main complaint
    story.append(Paragraph("Keluhan Utama", heading_style))
    complaint_text = session_state.main_complaint or "Tidak ada keluhan yang dicatat"
    story.append(Paragraph(complaint_text, normal_style))
    story.append(Spacer(1, 12))
    
    # Medications
    story.append(Paragraph("Daftar Obat & Suplemen", heading_style))
    if session_state.medications:
        filtered_meds = [med for med in session_state.medications if med.strip()]
        if filtered_meds:
            for i, med in enumerate(filtered_meds, 1):
                story.append(Paragraph(f"{i}. {med}", normal_style))
        else:
            story.append(Paragraph("Tidak ada obat/suplemen yang dicatat", normal_style))
    else:
        story.append(Paragraph("Tidak ada obat/suplemen yang dicatat", normal_style))
    story.append(Spacer(1, 12))
    
    # Questions
    story.append(Paragraph("Pertanyaan untuk Dokter", heading_style))
    if session_state.questions:
        filtered_questions = [q for q in session_state.questions if q.strip()]
        if filtered_questions:
            for i, question in enumerate(filtered_questions, 1):
                story.append(Paragraph(f"{i}. {question}", normal_style))
        else:
            story.append(Paragraph("Tidak ada pertanyaan yang disiapkan", normal_style))
    else:
        story.append(Paragraph("Tidak ada pertanyaan yang disiapkan", normal_style))
    story.append(Spacer(1, 12))
    
    # File attachment
    story.append(Paragraph("Lampiran File", heading_style))
    if session_state.uploaded_file:
        story.append(Paragraph(f"File terlampir: {session_state.uploaded_file.name}", normal_style))
    else:
        story.append(Paragraph("Tidak ada file yang diunggah", normal_style))
    
    # Footer
    story.append(Spacer(1, 30))
    footer_text = f"Dibuat pada: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')} WIB"
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    story.append(Paragraph(footer_text, footer_style))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF data
    buffer.seek(0)
    return buffer.getvalue()

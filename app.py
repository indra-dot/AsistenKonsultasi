import streamlit as st
import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import base64
from utils import get_common_questions, generate_pdf_summary

# Page configuration
st.set_page_config(
    page_title="Asisten Persiapan Kontrol Dokter",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'patient_name' not in st.session_state:
    st.session_state.patient_name = ""
if 'doctor_name' not in st.session_state:
    st.session_state.doctor_name = ""
if 'appointment_date' not in st.session_state:
    st.session_state.appointment_date = datetime.date.today()
if 'appointment_time' not in st.session_state:
    st.session_state.appointment_time = datetime.time(9, 0)
if 'main_complaint' not in st.session_state:
    st.session_state.main_complaint = ""
if 'medications' not in st.session_state:
    st.session_state.medications = []
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

def update_progress():
    """Update progress bar"""
    progress = st.session_state.current_step / 6
    return progress

def next_step():
    """Move to next step"""
    if st.session_state.current_step < 6:
        st.session_state.current_step += 1
        st.rerun()

def prev_step():
    """Move to previous step"""
    if st.session_state.current_step > 1:
        st.session_state.current_step -= 1
        st.rerun()

def add_medication():
    """Add new medication to list"""
    st.session_state.medications.append("")
    st.rerun()

def remove_medication(index):
    """Remove medication from list"""
    if 0 <= index < len(st.session_state.medications):
        st.session_state.medications.pop(index)
        st.rerun()

def add_question():
    """Add new question to list"""
    st.session_state.questions.append("")
    st.rerun()

def remove_question(index):
    """Remove question from list"""
    if 0 <= index < len(st.session_state.questions):
        st.session_state.questions.pop(index)
        st.rerun()

def add_common_question(question):
    """Add common question to questions list"""
    if question not in st.session_state.questions:
        st.session_state.questions.append(question)
        st.rerun()

# Main app
st.title("🏥 Asisten Persiapan Kontrol Dokter")
st.markdown("*Siapkan diri Anda agar konsultasi lebih efektif*")

# Progress bar
progress = update_progress()
st.progress(progress)
st.markdown(f"**Langkah {st.session_state.current_step} dari 6**")

# Step content
if st.session_state.current_step == 1:
    st.header("Langkah 1: Informasi Dasar")
    st.markdown("Isi data diri dan jadwal kontrol Anda.")
    
    st.session_state.patient_name = st.text_input(
        "Nama Pasien", 
        value=st.session_state.patient_name,
        placeholder="Contoh: Budi Santoso"
    )
    
    st.session_state.doctor_name = st.text_input(
        "Nama Dokter yang Dituju", 
        value=st.session_state.doctor_name,
        placeholder="Contoh: Dr. Annisa"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.appointment_date = st.date_input(
            "Tanggal Kontrol",
            value=st.session_state.appointment_date
        )
    with col2:
        st.session_state.appointment_time = st.time_input(
            "Waktu Kontrol",
            value=st.session_state.appointment_time
        )

elif st.session_state.current_step == 2:
    st.header("Langkah 2: Keluhan Utama")
    st.session_state.main_complaint = st.text_area(
        "Jelaskan apa yang Anda rasakan",
        value=st.session_state.main_complaint,
        height=200,
        placeholder="Jelaskan gejala, keluhan, atau masalah kesehatan yang Anda alami..."
    )

elif st.session_state.current_step == 3:
    st.header("Langkah 3: Obat & Suplemen")
    
    # Display existing medications
    for i, medication in enumerate(st.session_state.medications):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.session_state.medications[i] = st.text_input(
                f"Obat/Suplemen {i+1}",
                value=medication,
                key=f"med_{i}",
                placeholder="Contoh: Paracetamol 500mg, 3x sehari"
            )
        with col2:
            if st.button("❌", key=f"remove_med_{i}", help="Hapus"):
                remove_medication(i)
    
    if st.button("➕ Tambah Obat/Suplemen"):
        add_medication()

elif st.session_state.current_step == 4:
    st.header("Langkah 4: Pertanyaan untuk Dokter")
    
    # Display existing questions
    for i, question in enumerate(st.session_state.questions):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.session_state.questions[i] = st.text_input(
                f"Pertanyaan {i+1}",
                value=question,
                key=f"q_{i}",
                placeholder="Tulis pertanyaan yang ingin Anda tanyakan..."
            )
        with col2:
            if st.button("❌", key=f"remove_q_{i}", help="Hapus"):
                remove_question(i)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Tambah Pertanyaan"):
            add_question()
    
    with col2:
        if st.button("📚 Pustaka Pertanyaan"):
            st.session_state.show_question_library = True
    
    # Question library modal
    if st.session_state.get('show_question_library', False):
        st.subheader("Pustaka Pertanyaan Umum")
        st.markdown("Pilih pertanyaan yang relevan:")
        
        common_questions = get_common_questions()
        for question in common_questions:
            if st.button(f"➕ {question}", key=f"common_q_{hash(question)}"):
                add_common_question(question)
        
        if st.button("Tutup Pustaka"):
            st.session_state.show_question_library = False
            st.rerun()

elif st.session_state.current_step == 5:
    st.header("Langkah 5: Unggah File Penting (Opsional)")
    st.markdown("Anda bisa mengunggah 1 file penting seperti hasil lab terakhir (PDF/JPG/PNG).")
    
    uploaded_file = st.file_uploader(
        "Pilih file",
        type=['pdf', 'jpg', 'jpeg', 'png'],
        help="Format yang didukung: PDF, JPG, PNG"
    )
    
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.success(f"File berhasil diunggah: {uploaded_file.name}")
        st.info(f"Ukuran file: {len(uploaded_file.getvalue())/1024:.1f} KB")

elif st.session_state.current_step == 6:
    st.header("Ringkasan untuk Konsultasi")
    
    # Summary content
    st.subheader("📋 Informasi Pasien")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Pasien:** {st.session_state.patient_name}")
        st.write(f"**Dokter:** {st.session_state.doctor_name}")
    with col2:
        appointment_datetime = f"{st.session_state.appointment_date.strftime('%d/%m/%Y')} pukul {st.session_state.appointment_time.strftime('%H:%M')}"
        st.write(f"**Jadwal:** {appointment_datetime}")
    
    st.subheader("🩺 Keluhan Utama")
    if st.session_state.main_complaint:
        st.write(st.session_state.main_complaint)
    else:
        st.write("*Tidak ada keluhan yang dicatat*")
    
    st.subheader("💊 Daftar Obat & Suplemen")
    if st.session_state.medications:
        filtered_meds = [med for med in st.session_state.medications if med.strip()]
        if filtered_meds:
            for i, med in enumerate(filtered_meds, 1):
                st.write(f"{i}. {med}")
        else:
            st.write("*Tidak ada obat/suplemen yang dicatat*")
    else:
        st.write("*Tidak ada obat/suplemen yang dicatat*")
    
    st.subheader("❓ Pertanyaan untuk Dokter")
    if st.session_state.questions:
        filtered_questions = [q for q in st.session_state.questions if q.strip()]
        if filtered_questions:
            for i, question in enumerate(filtered_questions, 1):
                st.write(f"{i}. {question}")
        else:
            st.write("*Tidak ada pertanyaan yang disiapkan*")
    else:
        st.write("*Tidak ada pertanyaan yang disiapkan*")
    
    st.subheader("📎 Lampiran File")
    if st.session_state.uploaded_file:
        st.write(f"📄 {st.session_state.uploaded_file.name}")
        
        # Show image preview if uploaded file is an image
        file_extension = st.session_state.uploaded_file.name.lower().split('.')[-1]
        if file_extension in ['jpg', 'jpeg', 'png']:
            st.image(st.session_state.uploaded_file, caption="Preview Gambar", width=400)
        elif file_extension == 'pdf':
            st.info("File PDF terlampir (preview tidak tersedia)")
    else:
        st.write("*Tidak ada file yang diunggah*")
    
    # Download PDF button
    if st.button("📥 Unduh Ringkasan (PDF)", type="primary"):
        pdf_buffer = generate_pdf_summary(st.session_state)
        st.download_button(
            label="💾 Simpan PDF",
            data=pdf_buffer,
            file_name=f"ringkasan_konsultasi_{st.session_state.patient_name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

# Navigation buttons
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.session_state.current_step > 1:
        if st.button("⬅️ Kembali"):
            prev_step()

with col3:
    if st.session_state.current_step < 6:
        if st.button("Lanjut ➡️"):
            next_step()
    elif st.session_state.current_step == 6:
        if st.button("🏠 Mulai Lagi"):
            # Reset all session state
            for key in list(st.session_state.keys()):
                if key != 'current_step':
                    del st.session_state[key]
            st.session_state.current_step = 1
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 12px;'>"
    "©️ 2025 - IWP | Asisten Persiapan Kontrol Dokter"
    "</div>",
    unsafe_allow_html=True
)

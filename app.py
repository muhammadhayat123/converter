import streamlit as st
from pdf2docx import Converter
from docx2pdf import convert
import os

# Set up Streamlit app
st.set_page_config(page_title="📄 PDF ↔ DOCX Converter", layout="centered")

st.title("📄 PDF ↔ DOCX Converter")
st.write("Upload a PDF or DOCX file to convert it to the other format.")

# Upload file
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    file_path = f"temp_uploaded.{file_ext}"
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    output_path = None  # Placeholder for converted file

    # Conversion logic
    if file_ext == "pdf":
        output_path = "converted.docx"
        st.write("🔄 Converting PDF to DOCX...")
        progress = st.progress(0)  # Progress bar
        try:
            cv = Converter(file_path)
            cv.convert(output_path)
            cv.close()
            st.success("✅ Conversion Successful!")
        except Exception as e:
            st.error(f"❌ Conversion failed: {e}")
        progress.progress(100)  # Complete progress

    elif file_ext == "docx":
        output_path = "converted.pdf"
        st.write("🔄 Converting DOCX to PDF...")
        progress = st.progress(0)
        try:
            convert(file_path, output_path)
            st.success("✅ Conversion Successful!")
        except Exception as e:
            st.error(f"❌ Conversion failed: {e}")
        progress.progress(100)

    # Download button
    if output_path and os.path.exists(output_path):
        with open(output_path, "rb") as file:
            st.download_button(
                label=f"📥 Download {output_path.split('.')[-1].upper()}",
                data=file,
                file_name=output_path,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document" if file_ext == "pdf" else "application/pdf"
            )

    # Cleanup temporary files
    os.remove(file_path)
    if os.path.exists(output_path):
        os.remove(output_path)

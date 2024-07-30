import streamlit as st
import zipfile
import os
from io import StringIO
import shutil

# Define your enhancements
enhancements = {
    "Pause": lambda text: text + '...',
    "Emphasize": lambda text: f'"{text.upper()}"',
    "Emotion": lambda text: f'**{text}**',
    "Question": lambda text: text + '?',
    "Quote": lambda text: f'"{text}"'
}

# Function to apply selected enhancement
def apply_enhancement(text, part, enhancement):
    if enhancement in enhancements:
        # Replace the specified part of the text with the enhanced version
        return text.replace(part, enhancements[enhancement](part))
    return text

# Function to handle file uploads and processing
def process_files(uploaded_files, enhancement, part):
    if uploaded_files:
        # Temporary directory to store uploaded files
        temp_dir = "temp_files"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Create a list to store processed text
        enhanced_texts = []

        for uploaded_file in uploaded_files:
            # Handle text files directly
            if uploaded_file.name.endswith('.txt'):
                content = uploaded_file.read().decode("utf-8")
                enhanced_content = apply_enhancement(content, part, enhancement)
                enhanced_texts.append((uploaded_file.name, enhanced_content))
            
            # Handle zip files
            elif uploaded_file.name.endswith('.zip'):
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                    for file_name in zip_ref.namelist():
                        if file_name.endswith('.txt'):
                            with open(os.path.join(temp_dir, file_name), 'r') as f:
                                content = f.read()
                            enhanced_content = apply_enhancement(content, part, enhancement)
                            enhanced_texts.append((file_name, enhanced_content))
                
                # Clean up temporary files
                shutil.rmtree(temp_dir)

        return enhanced_texts
    return []

# Streamlit app layout
st.title("Text Enhancement Tool")

# Layout columns for input and output
col1, col2 = st.columns([2, 2])

with col1:
    st.subheader("Upload Your Files")
    uploaded_files = st.file_uploader("Upload .txt or .zip files", accept_multiple_files=True)

with col2:
    st.subheader("Enhanced Text Output")
    output_text = st.empty()

# Input text area and part text
st.subheader("Input Your Text")
input_text = st.text_area("Input your text here:", height=300)
st.subheader("Part of Text to Enhance")
part_text = st.text_input("Specify part of the text to apply enhancement to:")

st.subheader("Apply Enhancements")

# Create enhancement buttons horizontally
col1, col2, col3, col4, col5 = st.columns(5)

enhanced_texts = []

with col1:
    if st.button("Pause"):
        enhancement = "Pause"
        enhanced_texts = process_files(uploaded_files, enhancement, part_text)
        for file_name, text in enhanced_texts:
            output_text.text_area(f"Enhanced {file_name}", value=text, height=300)

with col2:
    if st.button("Emphasize"):
        enhancement = "Emphasize"
        enhanced_texts = process_files(uploaded_files, enhancement, part_text)
        for file_name, text in enhanced_texts:
            output_text.text_area(f"Enhanced {file_name}", value=text, height=300)

with col3:
    if st.button("Emotion"):
        enhancement = "Emotion"
        enhanced_texts = process_files(uploaded_files, enhancement, part_text)
        for file_name, text in enhanced_texts:
            output_text.text_area(f"Enhanced {file_name}", value=text, height=300)

with col4:
    if st.button("Question"):
        enhancement = "Question"
        enhanced_texts = process_files(uploaded_files, enhancement, part_text)
        for file_name, text in enhanced_texts:
            output_text.text_area(f"Enhanced {file_name}", value=text, height=300)

with col5:
    if st.button("Quote"):
        enhancement = "Quote"
        enhanced_texts = process_files(uploaded_files, enhancement, part_text)
        for file_name, text in enhanced_texts:
            output_text.text_area(f"Enhanced {file_name}", value=text, height=300)

# Provide download options
if enhanced_texts:
    with st.expander("Download Enhanced Text"):
        st.subheader("Download Enhanced Text")
        # Single file download
        if len(enhanced_texts) == 1:
            file_name, text = enhanced_texts[0]
            st.download_button(
                label="Download Enhanced Text",
                data=text,
                file_name=f"enhanced_{file_name}"
            )
        # Zip file download
        else:
            zip_buffer = StringIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for file_name, text in enhanced_texts:
                    zip_file.writestr(f"enhanced_{file_name}", text)
            st.download_button(
                label="Download All Enhanced Texts as ZIP",
                data=zip_buffer.getvalue(),
                file_name="enhanced_texts.zip"
            )

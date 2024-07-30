import streamlit as st
import zipfile
import io

@st.cache_data
def apply_enhancements(script, enhancements):
    """
    Apply text enhancements based on the given list of enhancements.
    """
    for enhancement in enhancements:
        action, text = enhancement['action'], enhancement['text']
        if action == 'pause':
            script = script.replace(text, f'{text}...')
        elif action == 'emphasize':
            script = script.replace(text, f'"{text.upper()}"')
        elif action == 'emotion':
            script = script.replace(text, f'**{text}**')
        elif action == 'question':
            script = script.replace(text, f'{text}?')
        elif action == 'quote':
            script = script.replace(text, f'"{text}"')
    return script

def create_zip_file(file_dict):
    """
    Create a ZIP file from a dictionary of file names and their contents.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_name, file_content in file_dict.items():
            zip_file.writestr(file_name, file_content)
    zip_buffer.seek(0)
    return zip_buffer

# Streamlit UI
st.set_page_config(page_title="Interactive Script Enhancer", layout="wide")

st.title("Interactive Script Enhancer")

st.sidebar.header("Upload & Enhance")

# Upload or input single script
upload_option = st.sidebar.selectbox("Upload or Input Script", ["Upload File", "Input Text"])

if upload_option == "Upload File":
    uploaded_file = st.sidebar.file_uploader("Upload your script file (.txt)", type="txt")
    if uploaded_file:
        script = uploaded_file.read().decode("utf-8")
        st.session_state.original_script = script  # Save original script for reference
elif upload_option == "Input Text":
    script = st.sidebar.text_area("Input your script text here:")
    if script:
        st.session_state.original_script = script  # Save original script for reference

if 'original_script' in st.session_state:
    st.sidebar.subheader("Enhancement Options")

    # Store enhancements in session state
    if 'enhancements' not in st.session_state:
        st.session_state.enhancements = []

    # Define enhancement types
    enhancement_types = ['Pause', 'Emphasize', 'Emotion', 'Question', 'Quote']

    # Enhancement pills (buttons)
    col1, col2 = st.columns([2, 2])

    with col1:
        st.subheader("Select Text Enhancements")
        enhancement_action = st.selectbox("Choose enhancement type:", enhancement_types)
        selected_text = st.text_input(f"Text to {enhancement_action.lower()}:")
        
        if st.button(f"Add {enhancement_action}"):
            if selected_text:
                action_map = {
                    "Pause": "pause",
                    "Emphasize": "emphasize",
                    "Emotion": "emotion",
                    "Question": "question",
                    "Quote": "quote"
                }
                st.session_state.enhancements.append({"action": action_map[enhancement_action], "text": selected_text})
    
    with col2:
        st.subheader("Current Enhancements")
        enhancements_list = [f'{e["action"].capitalize()} on "{e["text"]}"' for e in st.session_state.enhancements]
        if enhancements_list:
            st.write("\n".join(enhancements_list))
        else:
            st.write("No enhancements added yet.")

    st.subheader("Enhance and Download")

    if st.button("Apply Enhancements"):
        if 'original_script' in st.session_state:
            enhanced_script = apply_enhancements(st.session_state.original_script, st.session_state.enhancements)
            
            # Store the enhanced script in session state
            st.session_state.enhanced_script = enhanced_script
            
            st.subheader("Enhanced Script")
            st.text_area("Enhanced Script", enhanced_script, height=300, key="enhanced_script_display")

            # Provide download option for a single file
            st.download_button(
                label="Download Enhanced Script",
                data=enhanced_script,
                file_name="enhanced_script.txt",
                mime="text/plain"
            )

    # Bulk functionality
    st.sidebar.subheader("Bulk Enhancements")
    bulk_file = st.sidebar.file_uploader("Upload ZIP of script files", type="zip")
    if bulk_file:
        with zipfile.ZipFile(bulk_file, 'r') as zip_ref:
            file_dict = {name: zip_ref.read(name).decode('utf-8') for name in zip_ref.namelist()}
        
        enhanced_files = {}
        for file_name, content in file_dict.items():
            enhanced_script = apply_enhancements(content, st.session_state.enhancements)
            enhanced_files[file_name] = enhanced_script

        if st.button("Download All Enhanced Scripts as ZIP"):
            zip_buffer = create_zip_file(enhanced_files)
            st.download_button(
                label="Download Enhanced Scripts ZIP",
                data=zip_buffer,
                file_name="enhanced_scripts.zip",
                mime="application/zip"
            )

    st.markdown("""
    ### Enhancement Types:
    - **Pause**: Adds `...` after the selected text.
    - **Emphasize**: Capitalizes and surrounds the text with `""`.
    - **Emotion**: Surrounds the text with `**` markers.
    - **Question**: Adds `?` after the selected text.
    - **Quote**: Surrounds the text with `"`.

    ### Notes:
    - Select the text and apply the desired enhancement using the buttons.
    - The current enhancements applied will be displayed in the right column.
    - For bulk processing, upload a ZIP file with your scripts.
    """)

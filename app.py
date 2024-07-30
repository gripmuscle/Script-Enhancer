import streamlit as st
from streamlit.components.v1 import html
import zipfile
import io

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

    st.subheader("Real-time Enhanced Script")

    # Real-time editing
    enhanced_script = apply_enhancements(st.session_state.original_script, st.session_state.enhancements)
    real_time_script = st.text_area("Enhanced Script", value=enhanced_script, height=300, key="enhanced_script_display")

    # Apply button
    if st.button("Apply Enhancements"):
        if 'original_script' in st.session_state:
            st.session_state.enhanced_script = real_time_script
            st.subheader("Enhanced Script")
            st.text_area("Enhanced Script", real_time_script, height=300, key="enhanced_script_display")

            # Provide download option for a single file
            st.download_button(
                label="Download Enhanced Script",
                data=real_time_script,
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

# JavaScript code to handle context menu, text selection, and keyboard shortcuts
js_code = """
// Function to show selected text
function showSelectedText() {
    var selectedText = '';
    if (window.getSelection) {
        selectedText = window.getSelection().toString();
    } else if (document.getSelection) {
        selectedText = document.getSelection().toString();
    } else if (document.selection) {
        selectedText = document.selection.createRange().text;
    } else return;
    document.getElementById('selectedTextArea').value = selectedText;
}

// Function to handle context menu
document.addEventListener('contextmenu', function (e) {
    e.preventDefault();
    const menu = document.getElementById('contextMenu');
    const selectedText = window.getSelection().toString();
    if (selectedText) {
        menu.style.display = 'block';
        menu.style.left = e.pageX + 'px';
        menu.style.top = e.pageY + 'px';
        menu.dataset.selectedText = selectedText;
    }
});

document.addEventListener('click', function () {
    document.getElementById('contextMenu').style.display = 'none';
});

document.getElementById('contextMenu').addEventListener('click', function (e) {
    const action = e.target.dataset.action;
    if (action) {
        const selectedText = this.dataset.selectedText;
        const enhancedText = {
            'pause': selectedText + '...',
            'emphasize': '"' + selectedText.toUpperCase() + '"',
            'emotion': '**' + selectedText + '**',
            'question': selectedText + '?',
            'quote': '"' + selectedText + '"'
        }[action];
        document.body.innerHTML = document.body.innerHTML.replace(selectedText, enhancedText);
        this.style.display = 'none';
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function (e) {
    const shortcuts = {
        'P': 'pause',
        'E': 'emphasize',
        'M': 'emotion',
        'Q': 'question',
        'T': 'quote'
    };
    if (e.ctrlKey && shortcuts[e.key.toUpperCase()]) {
        e.preventDefault();
        const action = shortcuts[e.key.toUpperCase()];
        const selectedText = window.getSelection().toString();
        const enhancedText = {
            'pause': selectedText + '...',
            'emphasize': '"' + selectedText.toUpperCase() + '"',
            'emotion': '**' + selectedText + '**',
            'question': selectedText + '?',
            'quote': '"' + selectedText + '"'
        }[action];
        document.body.innerHTML = document.body.innerHTML.replace(selectedText, enhancedText);
    }
});
"""

# Wrap the JavaScript as HTML code
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        .context-menu {{
            position: absolute;
            text-align: center;
            background: lightgray;
            border: 1px solid black;
            display: none;
            z-index: 1000;
        }}
        .context-menu ul {{
            padding: 0;
            margin: 0;
            min-width: 150px;
            list-style: none;
        }}
        .context-menu ul li {{
            padding: 7px;
            border-bottom: 1px solid black;
        }}
        .context-menu ul li:last-child {{
            border-bottom: none;
        }}
        .context-menu ul li a {{
            text-decoration: none;
            color: black;
            display: block;
        }}
        .context-menu ul li:hover {{
            background: darkgray;
        }}
    </style>
</head>
<body>
    <h1>Enhanced Text Handling Example</h1>
    <p>Select any part of this text and use the context menu or keyboard shortcuts.</p>
    <textarea id="selectedTextArea" rows="5" cols="50" readonly></textarea>
    <div id="contextMenu" class="context-menu">
        <ul>
            <li><a href="#" data-action="pause">Pause</a></li>
            <li><a href="#" data-action="emphasize">Emphasize</a></li>
            <li><a href="#" data-action="emotion">Emotion</a></li>
            <li><a href="#" data-action="question">Question</a></li>
            <li><a href="#" data-action="quote">Quote</a></li>
        </ul>
    </div>
    <script>{js_code}</script>
</body>
</html>
""", unsafe_allow_html=True)

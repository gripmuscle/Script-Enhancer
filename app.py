import streamlit as st
from streamlit.components.v1 import html

# Define your enhancements
enhancement_actions = [
    "Pause",
    "Emphasize",
    "Emotion",
    "Question",
    "Quote"
]

# JavaScript code to handle context menu, text selection, and keyboard shortcuts
js_code = """
// Function to show selected text in textarea
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
        const textarea = document.getElementById('selectedTextArea');
        textarea.value = textarea.value.replace(selectedText, enhancedText);
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
        const textarea = document.getElementById('selectedTextArea');
        textarea.value = textarea.value.replace(selectedText, enhancedText);
    }
});
"""

# HTML code to display context menu and textarea
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
        .textarea-container {{
            margin-top: 20px;
        }}
        .enhancement-buttons {{
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <h1>Enhanced Text Handling Example</h1>
    <textarea id="selectedTextArea" rows="5" cols="50" placeholder="Select text and use context menu or keyboard shortcuts"></textarea>
    <div id="contextMenu" class="context-menu">
        <ul>
            {''.join(f'<li><a href="#" data-action="{action.lower()}">{action}</a></li>' for action in {", ".join(enhancement_actions)})}
        </ul>
    </div>
    <script>{js_code}</script>
</body>
</html>
"""

# Streamlit app layout
st.title("Enhanced Text Handling with Context Menu and Keyboard Shortcuts")

# Display the HTML with embedded JavaScript
html(html_code, height=800)

# Input text box directly in the main area
st.subheader("Input Your Script")
script = st.text_area("Input your script text here:", height=300)

# Create enhancement buttons dynamically
st.subheader("Apply Enhancements")
for action in enhancement_actions:
    if st.button(f"Apply {action}"):
        # Simulate enhancement application (you need to handle this on the frontend with JavaScript)
        st.write(f"Apply {action} clicked")

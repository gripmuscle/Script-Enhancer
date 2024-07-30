import streamlit as st

# Define your enhancements
enhancements = {
    "Pause": lambda text: text + '...',
    "Emphasize": lambda text: f'"{text.upper()}"',
    "Emotion": lambda text: f'**{text}**',
    "Question": lambda text: text + '?',
    "Quote": lambda text: f'"{text}"'
}

# Function to apply selected enhancement
def apply_enhancement(text, enhancement):
    if enhancement in enhancements:
        return enhancements[enhancement](text)
    return text

# Streamlit app layout
st.title("Text Enhancement Tool")

# Define layout
col1, col2 = st.columns([2, 2])

with col1:
    st.subheader("Input Your Text")
    input_text = st.text_area("Input your text here:", height=300)

with col2:
    st.subheader("Enhanced Text")
    output_text = st.empty()

# Create enhancement buttons horizontally
st.subheader("Apply Enhancements")

# Initialize a dictionary to store enhanced text
enhanced_text = input_text

if st.button("Pause"):
    enhanced_text = apply_enhancement(input_text, "Pause")
elif st.button("Emphasize"):
    enhanced_text = apply_enhancement(input_text, "Emphasize")
elif st.button("Emotion"):
    enhanced_text = apply_enhancement(input_text, "Emotion")
elif st.button("Question"):
    enhanced_text = apply_enhancement(input_text, "Question")
elif st.button("Quote"):
    enhanced_text = apply_enhancement(input_text, "Quote")

# Update the output text area with the enhanced text
output_text.text_area("Enhanced Text", value=enhanced_text, height=300)

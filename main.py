import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

# Initialize session state
if 'edited_image' not in st.session_state:
    st.session_state.edited_image = None

def edit_image(image, text_data, new_size):
    img = image.copy()
    
    # Resize image
    if new_size:
        img = img.resize(new_size)
    
    # Add text
    if text_data['text']:
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype(text_data['font'], text_data['size'])
        except:
            font = ImageFont.load_default()
        
        draw.text(
            (text_data['x'], text_data['y']),
            text_data['text'],
            fill=text_data['color'],
            font=font
        )
    
    return img

st.title("🖼️ AI Image Editor - Canva-like Tool")
st.write("Upload an image and customize it with text and resizing options!")

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    
    # Text editing controls
    st.subheader("Text Options")
    text = st.text_input("Enter Text")
    text_color = st.color_picker("Text Color", "#FFFFFF")
    text_size = st.slider("Text Size", 10, 100, 30)
    font_style = st.selectbox("Font Style", ["arial.ttf", "times.ttf", "cour.ttf"])
    text_x = st.slider("Text X Position", 0, 1000, 50)
    text_y = st.slider("Text Y Position", 0, 1000, 50)
    
    # Image resizing controls
    st.subheader("Image Resizing")
    new_width = st.number_input("Width", min_value=100, value=800)
    new_height = st.number_input("Height", min_value=100, value=600)
    
    # AI Enhancements (placeholder for future implementation)
    st.subheader("AI Enhancements")
    ai_filter = st.selectbox("AI Filters", ["None", "Enhance Colors", "Background Removal"])

# Main content area
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    original_image = Image.open(uploaded_file).convert("RGBA")
else:
    # Use default image if none uploaded
    original_image = Image.new("RGBA", (800, 600), (0, 0, 0, 255))

# Prepare text data
text_data = {
    'text': text,
    'color': text_color,
    'size': text_size,
    'font': font_style,
    'x': text_x,
    'y': text_y
}

# Edit image
edited_img = edit_image(
    original_image,
    text_data,
    (new_width, new_height)
)

# Display edited image
st.image(edited_img, caption="Edited Image", use_column_width=True)

# Download button
if edited_img:
    buf = io.BytesIO()
    edited_img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="Download Edited Image",
        data=byte_im,
        file_name="edited_image.png",
        mime="image/png"
    )

# AI Enhancements placeholder
if ai_filter != "None":
    st.write(f"Applying {ai_filter}... (This feature will

import streamlit as st
from rembg import remove
from PIL import Image
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="The VMG Groups - Background Remover",
    page_icon="✂️",
    layout="wide"
)

# --- Custom CSS for Red & White Attractive Theme ---
st.markdown("""
    <style>
    /* Main background and text colors */
    .stApp {
        background-color: #FFFFFF;
        color: #333333;
    }
    
    /* Header Styling */
    .main-title {
        color: #D32F2F;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 800;
        text-align: center;
        margin-top: -20px;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #555555;
        text-align: center;
        font-weight: 400;
        margin-bottom: 20px;
    }
    
    /* File Uploader Customization */
    section[data-testid="stFileUploader"] {
        border: 2px dashed #D32F2F !important;
        background-color: #FFEBEE !important;
        border-radius: 10px;
        padding: 20px;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #D32F2F !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        transition: 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #B71C1C !important;
        box-shadow: 0px 4px 15px rgba(211, 47, 47, 0.4);
    }
    
    /* Branded Footer Container */
    .footer-panel {
        background-color: #D32F2F;
        color: white;
        text-align: center;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI Header ---
st.markdown("<h1 class='main-title'>The VMG Groups</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='sub-title'>Professional Multi-Image Background Remover</h3>", unsafe_allow_html=True)
st.write("---")

# --- Multiple Image Upload Section ---
uploaded_files = st.file_uploader(
    "Choose one or more images...", 
    type=["jpg", "jpeg", "png", "webp", "bmp", "tiff"],
    accept_multiple_files=True
)

if uploaded_files:
    st.markdown(f"<h3 style='color: #333;'>Processing {len(uploaded_files)} image(s):</h3>", unsafe_allow_html=True)
    
    # Loop through every uploaded image file
    for index, uploaded_file in enumerate(uploaded_files):
        try:
            st.markdown(f"#### 📄 File {index + 1}: {uploaded_file.name}")
            
            # Open the image file
            image = Image.open(uploaded_file)
            
            # Split screen layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<p style='color: #D32F2F; font-weight: bold;'>Original Image</p>", unsafe_allow_html=True)
                st.image(image, use_container_width=True)
                
            with col2:
                # Local Background Removal
                with st.spinner(f"Removing background from {uploaded_file.name}..."):
                    input_bytes = uploaded_file.getvalue()
                    output_bytes = remove(input_bytes)
                    output_image = Image.open(io.BytesIO(output_bytes))
                
                st.markdown("<p style='color: #2E7D32; font-weight: bold;'>Background Removed</p>", unsafe_allow_html=True)
                st.image(output_image, use_container_width=True)
                
                # Setup download button
                buffered = io.BytesIO()
                output_image.save(buffered, format="PNG")
                
                st.download_button(
                    label=f"📥 Download {uploaded_file.name.split('.')[0]}.png",
                    data=buffered.getvalue(),
                    file_name=f"vmg_rembg_{uploaded_file.name.split('.')[0]}.png",
                    mime="image/png",
                    key=f"download_btn_{index}"
                )
                
            st.markdown("<hr style='border-top: 1px dashed #D32F2F;'>", unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")

# --- Safe Footer ---
st.markdown("<div class='footer-panel'>Client Team Workspace | Powered by The VMG Groups</div>", unsafe_allow_html=True)

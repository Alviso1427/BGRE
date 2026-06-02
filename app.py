import streamlit as st
from rembg import remove, new_session
from PIL import Image
import io

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="The VMG Groups - Background Remover",
    page_icon="✂️",
    layout="wide"
)

# --------------------------------------------------
# LOAD REMBG MODEL ONLY ONCE
# --------------------------------------------------
@st.cache_resource
def load_model():
    return new_session("u2net")

try:
    session = load_model()
except Exception as e:
    st.error(f"Failed to load rembg model: {e}")
    st.stop()

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: white;
}

.main-title {
    color: #D32F2F;
    text-align: center;
    font-weight: 800;
}

.sub-title {
    color: #666;
    text-align: center;
}

.footer-panel {
    background-color: #D32F2F;
    color: white;
    text-align: center;
    padding: 12px;
    border-radius: 8px;
    margin-top: 40px;
    font-weight: bold;
}

.stButton>button {
    background-color: #D32F2F !important;
    color: white !important;
    width: 100%;
}

section[data-testid="stFileUploader"] {
    border: 2px dashed #D32F2F;
    border-radius: 10px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    "<h1 class='main-title'>The VMG Groups</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 class='sub-title'>Professional Multi-Image Background Remover</h3>",
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------
uploaded_files = st.file_uploader(
    "Upload image(s)",
    type=["png", "jpg", "jpeg", "webp", "bmp"],
    accept_multiple_files=True
)

# --------------------------------------------------
# PROCESS IMAGES
# --------------------------------------------------
if uploaded_files:

    st.success(f"{len(uploaded_files)} image(s) uploaded")

    for idx, uploaded_file in enumerate(uploaded_files):

        st.markdown(f"### 📄 {uploaded_file.name}")

        try:
            image = Image.open(uploaded_file).convert("RGBA")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Original")
                st.image(image)

            with st.spinner("Removing background..."):

                input_bytes = uploaded_file.getvalue()

                output_bytes = remove(
                    input_bytes,
                    session=session
                )

                output_image = Image.open(
                    io.BytesIO(output_bytes)
                )

            with col2:
                st.subheader("Background Removed")
                st.image(output_image)

                download_buffer = io.BytesIO()

                output_image.save(
                    download_buffer,
                    format="PNG"
                )

                filename = (
                    uploaded_file.name.rsplit(".", 1)[0]
                    + "_no_bg.png"
                )

                st.download_button(
                    label="📥 Download PNG",
                    data=download_buffer.getvalue(),
                    file_name=filename,
                    mime="image/png",
                    key=f"download_{idx}"
                )

            st.divider()

        except Exception as e:
            st.error(
                f"Error processing {uploaded_file.name}: {e}"
            )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <div class='footer-panel'>
        Client Team Workspace | Powered by The VMG Groups
    </div>
    """,
    unsafe_allow_html=True
)

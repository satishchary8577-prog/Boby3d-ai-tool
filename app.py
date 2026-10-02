import os
import tempfile
import streamlit as st
import replicate
from PIL import Image

st.set_page_config(
    page_title="Jewelry 3D AI Studio",
    page_icon="💎",
    layout="wide"
)

st.title("💎 Jewelry 2D to 3D STL Converter")
st.write("జ్యువెలరీ డిజైన్ ఫోటోను అప్‌లోడ్ చేసి, క్యాడ్/ప్రింటింగ్ కోసం 3D మెష్ పొందండి.")

# 1. Sidebar - Setup & Settings
st.sidebar.header("⚙️ సెటప్ & టోకెన్")
api_token = st.sidebar.text_input("Replicate API Token:", type="password")

st.sidebar.markdown("---")
st.sidebar.header("🎛️ 3D క్వాలిటీ సెట్టింగ్స్")
mc_resolution = st.sidebar.slider("Mesh Resolution (డీటైలింగ్)", min_value=128, max_value=512, value=256, step=64)
foreground_ratio = st.sidebar.slider("Foreground Zoom", min_value=0.5, max_value=1.0, value=0.85, step=0.05)
remove_bg = st.sidebar.checkbox("బ్యాక్‌గ్రౌండ్ ఆటోమేటిక్‌గా తీసివేయి", value=True)

if not api_token:
    st.warning("⚠️ దయచేసి సైడ్‌బార్‌లో మీ Replicate API Token ఎంటర్ చేయండి.")
    st.stop()

os.environ["REPLICATE_API_TOKEN"] = api_token

# 2. Main Upload Section
uploaded_file = st.file_uploader(
    "జ్యువెలరీ ఫోటో ఎంచుకోండి (PNG / JPG)", 
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])
    
    image = Image.open(uploaded_file)
    with col1:
        st.subheader("అప్‌లోడ్ చేసిన ఇమేజ్")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("3D జనరేషన్")
        generate_btn = st.button("Generate 3D STL Model 🚀", use_container_width=True)

    if generate_btn:
        with st.spinner("⏳ జ్యువెలరీ మెష్‌ను AI విశ్లేషించి 3D మోడల్ జనరేట్ చేస్తోంది..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    image.save(temp_file.name)
                    temp_path = temp_file.name

                with open(temp_path, "rb") as img_file:
                    output = replicate.run(
                        "camenduru/triposr:be2a9b2b50937a3cc770ff9981881515f40393f9c66914bbd5db84ffca6a32fc",
                        input={
                            "image_path": img_file,
                            "do_remove_background": remove_bg,
                            "mc_resolution": mc_resolution,
                            "foreground_ratio": foreground_ratio
                        }
                    )

                if output:
                    st.success("🎉 జ్యువెలరీ 3D మోడల్ విజయవంతంగా తయారైంది!")
                    model_url = output if isinstance(output, str) else str(output)
                    st.markdown(f"### [👉 ఇక్కడ క్లిక్ చేసి మీ 3D ఫైల్ డౌన్‌లోడ్ చేసుకోండి]({model_url})")
            except Exception as e:
                st.error(f"❌ ఎర్రర్ వచ్చింది: {e}")

import os
import tempfile
import streamlit as st
import replicate
from PIL import Image

st.set_page_config(page_title="Jewelry 3D AI Studio", page_icon="💎", layout="wide")

st.title("💎 Jewelry 2D to 3D STL Converter")
st.write("2D ఫోటో అప్‌లోడ్ చేయండి - నేరుగా 3D మోడల్ పొందండి.")

# 1. Sidebar
st.sidebar.header("⚙️ సెటప్ & టోకెన్")
api_token = st.sidebar.text_input("Replicate API Token:", type="password")

if not api_token:
    st.warning("⚠️ దయచేసి సైడ్‌బార్‌లో మీ Replicate API Token ఎంటర్ చేయండి.")
    st.stop()

os.environ["REPLICATE_API_TOKEN"] = api_token

# 2. Upload Section
uploaded_file = st.file_uploader("జ్యువెలరీ ఫోటో ఎంచుకోండి (PNG / JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="అప్‌లోడ్ చేసిన ఫోటో", width=300)

    if st.button("Generate 3D STL Model 🚀"):
        with st.spinner("⏳ 3D మోడల్ తయారవుతోంది... దయచేసి 20-30 సెకన్లు వేచి ఉండండి..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    image.save(temp_file.name)
                    temp_path = temp_file.name

                with open(temp_path, "rb") as img_file:
                    output = replicate.run(
                        "camenduru/tripo-sr:be2a9b2b50937a3cc770ff9981881515f40393f9c66914bbd5db84ffca6a32fc",
                        input={
                            "image_path": img_file,
                            "do_remove_background": True,
                            "foreground_ratio": 0.85
                        }
                    )

                if output:
                    st.success("🎉 అద్భుతం! మీ 3D మోడల్ సిద్ధమైంది!")
                    model_url = output if isinstance(output, str) else str(output)
                    st.markdown(f"### [👉 ఇక్కడ క్లిక్ చేసి మీ 3D ఫైల్ డౌన్‌లోడ్ చేసుకోండి]({model_url})")
            except Exception as e:
                st.error(f"❌ ఎర్రర్ వచ్చింది: {e}")

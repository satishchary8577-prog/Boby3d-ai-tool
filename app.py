import os
import tempfile
import streamlit as st
import replicate
from PIL import Image

st.set_page_config(page_title="2D to 3D AI Tool", layout="wide")

st.title("Image to 3D STL Converter")
st.write("2D ఫోటో అప్‌లోడ్ చేయండి - నేరుగా 3D ఫైల్ పొందండి.")

# Sidebar Setup
st.sidebar.header("సెటప్ (Setup)")
api_token = st.sidebar.text_input("మీ Replicate API Token ఎంటర్ చేయండి:", type="password")

if not api_token:
    st.warning("⚠️ దయచేసి సైడ్‌బార్‌లో మీ Replicate API Token ఎంటర్ చేయండి.")
    st.stop()

os.environ["REPLICATE_API_TOKEN"] = api_token

# Image Upload
uploaded_file = st.file_uploader("ఫోటో ఎంచుకోండి (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="అప్‌లోడ్ చేసిన ఫోటో", use_container_width=True)

    if st.button("Generate 3D STL Model 🚀"):
        with st.spinner("AI 3D మోడల్ జనరేట్ చేస్తోంది... దయచేసి వేచి ఉండండి..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    image.save(temp_file.name)
                    temp_path = temp_file.name

                with open(temp_path, "rb") as img_file:
                    # Direct official Image-to-3D without text prompt
                    output = replicate.run(
                        "vaibhavs10/triposr:d64be933221a8d0526017b2b62d8ff5d70f07297e68fa707ea99dbbb24f2b904",
                        input={"image_path": img_file}
                    )

                if output:
                    st.success("🎉 3D మోడల్ విజయవంతంగా తయారైంది!")
                    model_url = output if isinstance(output, str) else str(output)
                    st.markdown(f"### [👉 ఇక్కడ క్లిక్ చేసి మీ 3D ఫైల్ డౌన్‌లోడ్ చేసుకోండి]({model_url})")
            except Exception as e:
                st.error(f"❌ ఎర్రర్ వచ్చింది: {e}")

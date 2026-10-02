import streamlit as st
from gradio_client import Client, handle_file
from PIL import Image
import tempfile

st.set_page_config(page_title="Jewelry 3D AI Studio", page_icon="💎", layout="wide")

st.title("💎 Jewelry 2D to 3D STL Converter")
st.write("పూర్తిగా ఉచిత AI ఇంజిన్‌తో ఫోటో నుండి 3D మోడల్ పొందండి.")

uploaded_file = st.file_uploader("జ్యువెలరీ ఫోటో ఎంచుకోండి (PNG / JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="అప్‌లోడ్ చేసిన ఇమేజ్", width=300)

    if st.button("Generate 3D Model 🚀", use_container_width=True):
        with st.spinner("⏳ ఉచిత TripoSR AI సర్వర్ ద్వారా 3D మోడల్ ప్రాసెస్ అవుతోంది... దయచేసి వేచి ఉండండి..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    image.save(temp_file.name)
                    temp_path = temp_file.name

                client = Client("stabilityai/TripoSR")
                result = client.predict(
                    image_input=handle_file(temp_path),
                    api_name="/process_image"
                )

                if result:
                    st.success("🎉 అద్భుతం! మీ జ్యువెలరీ 3D మోడల్ విజయవంతంగా సిద్ధమైంది!")
                    model_file_path = result[1] if isinstance(result, (list, tuple)) else result
                    
                    with open(model_file_path, "rb") as f:
                        st.download_button(
                            label="📥 3D ఫైల్ డౌన్‌లోడ్ చేసుకోండి (.obj)",
                            data=f,
                            file_name="jewelry_model.obj",
                            mime="application/octet-stream",
                            use_container_width=True
                        )
            except Exception as e:
                st.error(f"❌ ఎర్రర్ వచ్చింది: {e}")
                

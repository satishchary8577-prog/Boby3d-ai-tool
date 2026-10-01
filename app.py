import streamlit as st
import replicate
import requests
import trimesh
import os

# Page configurations
st.set_page_config(page_title="2D to 3D STL AI Tool", layout="centered", page_icon="🎨")

# Custom Styling for Telugu and English
st.markdown("""
    <style>
    .big-font { font-size:26px !important; font-weight: bold; color: #4A90E2; }
    .telugu-text { font-family: 'Mulish', sans-serif; color: #333; }
    .stButton>button { background-color: #4A90E2; color: white; border-radius: 8px; width: 100%; }
    .stDownloadButton>button { background-color: #2ECC71; color: white; border-radius: 8px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# Title & Description
st.markdown('<p class="big-font">Image to 3D STL Converter</p>', unsafe_allow_html=True)
st.write("2D ఫోటో అప్‌లోడ్ చేయండి - నేరుగా Rhino & ZBrush కోసం STL ఫైల్ పొందండి.")

# Sidebar for API Key
st.sidebar.header("సెటప్ (Setup)")
api_key = st.sidebar.text_input("మీ Replicate API Token ఎంటర్ చేయండి:", type="password", help="replicate.com నుండి మీ టోకెన్ పొందండి.")

# Check for API Key
if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
else:
    st.sidebar.warning("⚠️ ముందుగా API టోకెన్ ఇవ్వండి.")

# File Uploader
uploaded_file = st.file_uploader("ఫోటో ఎంచుకోండి (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"], help="క్లియర్ బ్యాక్‌గ్రౌండ్ ఉన్న ఫోటోలు బాగా పనిచేస్తాయి.")

# Main Logic
if uploaded_file is not None and api_key:
    # Display image
    st.image(uploaded_file, caption="అప్‌లోడ్ చేసిన ఫోటో", use_container_width=True)
    
    # Process Button
    if st.button("Generate 3D STL Model 🚀"):
        progress_text = "AI 3D మోడల్‌ను డిజైన్ చేస్తోంది... కొద్ది సెకన్లు ఆగండి..."
        my_bar = st.progress(0, text=progress_text)
        
        try:
            # 1. Save temp image
            my_bar.progress(10, text="ఫైల్‌ను ప్రాసెస్ చేస్తోంది...")
            temp_img_path = "temp_input.png"
            with open(temp_img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # 2. Run AI Model (Trellis)
            my_bar.progress(30, text="AI మోడల్‌ను రన్ చేస్తోంది (దీనికి టైమ్ పడుతుంది)...")
            # Using Trellis model for high quality
            output = replicate.run(
                "jeffreyxiang/trellis:latest",
                input={"image": open(temp_img_path, "rb")}
            )

            # 3. Get GLB output
            my_bar.progress(70, text="3D డేటాను డౌన్‌లోడ్ చేస్తోంది...")
            glb_url = output.get("model_file")
            if not glb_url:
                st.error("❌ 3D మోడల్ జనరేషన్ విఫలమైంది.")
                my_bar.empty()
            else:
                # Download GLB
                response = requests.get(glb_url)
                glb_path = "output.glb"
                with open(glb_path, "wb") as f:
                    f.write(response.content)

                # 4. Convert GLB to STL
                my_bar.progress(90, text="STL ఫార్మాట్‌లోకి మారుస్తోంది...")
                mesh = trimesh.load(glb_path, file_type="glb")
                stl_path = "model_output.stl"
                
                # If GLB has multiple scenes, merge them
                if isinstance(mesh, trimesh.Scene):
                    mesh = mesh.dump(concatenate=True)
                    
                mesh.export(stl_path, file_type="stl")

                my_bar.progress(100, text="సిద్ధమైంది!")
                st.success("🎉 3D STL మోడల్ విజయవంతంగా సిద్ధమైంది!")

                # Download Button
                with open(stl_path, "rb") as f:
                    st.download_button(
                        label="Download .STL File (for Rhino / ZBrush)",
                        data=f,
                        file_name=f"{uploaded_file.name.split('.')[0]}_3d.stl",
                        mime="application/sla"
                    )
                
                # Cleanup temp files
                os.remove(temp_img_path)
                os.remove(glb_path)
                os.remove(stl_path)

        except Exception as e:
            st.error(f"❌ ఎర్రర్ వచ్చింది: {e}")
            if 'my_bar' in locals():
                my_bar.empty()

elif uploaded_file is not None and not api_key:
    st.warning("⚠️ దయచేసి సైడ్‌బార్‌లో మీ Replicate API Token ఎంటర్ చేయండి.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>మీ సొంత 2D to 3D AI టూల్</p>", unsafe_allow_html=True)

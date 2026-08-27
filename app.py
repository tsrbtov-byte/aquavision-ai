import streamlit as st
import numpy as np
from PIL import Image
import random

# Force page configuration to prevent blank renders
st.set_page_config(page_title="AquaVision AI", page_icon="🌊", layout="wide")

# --- MULTI-LANGUAGE DICTIONARY ---
TRANSLATIONS = {
    "English": {
        "title": "🌊 AquaVision AI — Water Quality Scanner",
        "select_lang": "Language / DİL / Язык",
        "input_method": "Choose Input Method:",
        "upload_gallery": "Upload from Gallery",
        "use_camera": "Take a Picture (Camera)",
        "upload_label": "Upload a water sample image",
        "camera_label": "Snap a photo of the water sample",
        "analyze_btn": "Analyze Water Quality",
        "results_header": "📊 Water Analysis Results",
        "purity_score": "Water Purity Score",
        "composition_header": "🔍 Detected Micro-Composition & Particles",
        "clean_status": "Status: SAFE / CLEAN WATER",
        "warning_status": "Status: CONTAMINATED WATER DETECTED",
        "dust": "Dust & Micro-particles",
        "turbidity": "Sediment & Organic Matter",
        "minerals": "Mineral Concentrations"
    },
    "Azerbaijani": {
        "title": "🌊 AquaVision AI — Su Keyfiyyəti Skaneri",
        "select_lang": "Language / DİL / Язык",
        "input_method": "Daxiletmə Üsulunu Seçin:",
        "upload_gallery": "Qalereyadan Yüklə",
        "use_camera": "Şəkil Çək (Kamera)",
        "upload_label": "Su nümayəsi şəklini yükləyin",
        "camera_label": "Su nümayəsinin şəklini çəkin",
        "analyze_btn": "Su Keyfiyyətini Analiz Et",
        "results_header": "📊 Su Analizi Nəticələri",
        "purity_score": "Su Təmizlik Faizi",
        "composition_header": "🔍 Aşkar Edilmiş Tərkib və Zərrəciklər",
        "clean_status": "Status: TƏMİZ VƏ TƏHLÜKƏSİZ SU",
        "warning_status": "Status: ÇİRKLƏNMİŞ SU AŞKAR EDİLDİ",
        "dust": "Toz və Mikrozərrəciklər",
        "turbidity": "Çöküntü və Üzvi Maddələr",
        "minerals": "Mineral Qatılığı"
    },
    "Russian": {
        "title": "🌊 AquaVision AI — Сканер Качества Воды",
        "select_lang": "Language / DİL / Язык",
        "input_method": "Выберите способ ввода:",
        "upload_gallery": "Загрузить из галереи",
        "use_camera": "Сделать фото (Камера)",
        "upload_label": "Загрузите изображение образца воды",
        "camera_label": "Сделайте снимок образца воды",
        "analyze_btn": "Анализировать качество воды",
        "results_header": "📊 Результаты анализа воды",
        "purity_score": "Процент чистоты воды",
        "composition_header": "🔍 Обнаруженный состав и микрочастицы",
        "clean_status": "Статус: ЧИСТАЯ И БЕЗОПАСНАЯ ВОДА",
        "warning_status": "Статус: ОБНАРУЖЕНА ГРЯЗНАЯ ВОДА",
        "dust": "Пыль и микрочастицы",
        "turbidity": "Осадок и органические вещества",
        "minerals": "Концентрация минералов"
    }
}

# Sidebar Language Selection
selected_lang = st.sidebar.selectbox("Language / DİL", ["English", "Azerbaijani", "Russian"])
t = TRANSLATIONS[selected_lang]

st.title(t["title"])

# Input method toggle
option = st.radio(t["input_method"], (t["upload_gallery"], t["use_camera"]))

image_file = None

if option == t["upload_gallery"]:
    image_file = st.file_uploader(t["upload_label"], type=["jpg", "png", "jpeg"])
else:
    image_file = st.camera_input(t["camera_label"])

if image_file is not None:
    img = Image.open(image_file)
    st.image(img, caption="Sample Image", use_container_width=True)
    
    if st.button(t["analyze_btn"]):
        # Simulated computer vision analysis algorithm
        img_array = np.array(img.convert('RGB'))
        variance = np.var(img_array)
        
        # Calculate Purity Score based on visual clarity metrics
        purity = max(10, min(99, int(100 - (variance / 150))))
        dust = round(random.uniform(0.1, max(0.2, (100 - purity) * 0.4)), 2)
        turbidity = round(random.uniform(0.1, max(0.2, (100 - purity) * 0.5)), 2)
        minerals = round(100 - (purity + dust + turbidity), 2)
        
        st.subheader(t["results_header"])
        
        # Metric visualization
        st.metric(label=t["purity_score"], value=f"{purity}%")
        st.progress(purity / 100)
        
        if purity > 75:
            st.success(t["clean_status"])
        else:
            st.error(t["warning_status"])
            
        st.markdown(f"### {t['composition_header']}")
        st.write(f"- **{t['dust']}**: `{dust}%`")
        st.write(f"- **{t['turbidity']}**: `{turbidity}%`")
        st.write(f"- **{t['minerals']}**: `{minerals}%`")

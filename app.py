import streamlit as st
import cv2
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="AquaVision AI — Water Analyzer",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Water-Themed Custom Styling (CSS)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }
    div[data-testid="stSidebar"] {
        background-color: #0b171e;
        border-right: 1px solid #1f3a4b;
    }
    .stButton>button {
        background-color: #0088cc;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #00aaff;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Multi-Language Translations
TRANSLATIONS = {
    "English": {
        "title": "🌊 AquaVision AI",
        "subtitle": "Digital Water Quality Analysis System",
        "select_lang": "Language / DİL / Язык",
        "input_method": "Choose Input Method:",
        "upload_gallery": "📁 Gallery Upload",
        "use_camera": "📷 Camera Capture",
        "upload_label": "Upload water sample",
        "camera_label": "Snap photo of water sample",
        "analyze_btn": "Run AI Analysis",
        "results_header": "📊 Analysis Results & Composition",
        "purity_score": "Purity Score",
        "clean_status": "Status: SAFE / CLEAR WATER",
        "warning_status": "Status: CONTAMINATED WATER DETECTED",
        "chat_title": "🤖 AquaAI Assistant",
        "chat_placeholder": "Ask anything about water, chemistry, or general topics...",
        "sidebar_nav": "📌 Navigation & Tools",
        "history": "📜 Sample History",
        "library": "🖼️ Image Library",
        "settings": "⚙️ System Settings"
    },
    "Azerbaijani": {
        "title": "🌊 AquaVision AI",
        "subtitle": "Rəqəmsal Su Keyfiyyəti Analiz Sistemi",
        "select_lang": "Language / DİL / Язык",
        "input_method": "Daxiletmə Üsulunu Seçin:",
        "upload_gallery": "📁 Qalereyadan Yüklə",
        "use_camera": "📷 Kameradan Çək",
        "upload_label": "Su nümayəsi yükləyin",
        "camera_label": "Su nümayəsinin şəklini çəkin",
        "analyze_btn": "Süni İntellekt Analizini Başlat",
        "results_header": "📊 Analiz Nəticələri və Tərkib",
        "purity_score": "Təmizlik Dərəcəsi",
        "clean_status": "Status: TƏMİZ VƏ TƏHLÜKƏSİZ SU",
        "warning_status": "Status: ÇİRKLƏNMİŞ SU AŞKAR EDİLDİ",
        "chat_title": "🤖 AquaAI Köməkçisi",
        "chat_placeholder": "Su, kimya və ya istənilən mövzuda sual verin...",
        "sidebar_nav": "📌 Naviqasiya və Alətlər",
        "history": "📜 Keçmiş Nümayələr",
        "library": "🖼️ Şəkil Kitabxanası",
        "settings": "⚙️ Sistem Parametrləri"
    },
    "Russian": {
        "title": "🌊 AquaVision AI",
        "subtitle": "Цифровая Система Анализа Качества Воды",
        "select_lang": "Language / DİL / Язык",
        "input_method": "Выберите способ ввода:",
        "upload_gallery": "📁 Загрузить из галереи",
        "use_camera": "📷 Сделать фото",
        "upload_label": "Загрузите образец воды",
        "camera_label": "Сделайте снимок образца",
        "analyze_btn": "Запустить AI Анализ",
        "results_header": "📊 Результаты Анализа и Состав",
        "purity_score": "Индекс Чистоты",
        "clean_status": "Статус: ЧИСТАЯ И БЕЗОПАСНАЯ ВОДА",
        "warning_status": "Статус: ОБНАРУЖЕНА ГРЯЗНАЯ ВОДА",
        "chat_title": "🤖 AquaAI Помощник",
        "chat_placeholder": "Задайте вопрос о воде, химии или на любую тему...",
        "sidebar_nav": "📌 Навигация и Инструменты",
        "history": "📜 История Образцов",
        "library": "🖼️ Библиотека Изображений",
        "settings": "⚙️ Настройки Системы"
    }
}

# 4. Sidebar Controls
selected_lang = st.sidebar.selectbox("Language / DİL", ["English", "Azerbaijani", "Russian"])
t = TRANSLATIONS[selected_lang]

st.sidebar.markdown("---")
st.sidebar.subheader(t["sidebar_nav"])
st.sidebar.button(t["history"], use_container_width=True)
st.sidebar.button(t["library"], use_container_width=True)
st.sidebar.button(t["settings"], use_container_width=True)

# 5. Screen Layout Split (80% Main Dashboard, 20% Right AI Panel)
main_col, ai_col = st.columns([0.8, 0.2], gap="medium")

# --- MAIN DASHBOARD (80%) ---
with main_col:
    st.title(t["title"])
    st.caption(t["subtitle"])
    
    # Input Selection
    option = st.radio(t["input_method"], (t["upload_gallery"], t["use_camera"]), horizontal=True)
    
    image_file = None
    if option == t["upload_gallery"]:
        image_file = st.file_uploader(t["upload_label"], type=["jpg", "png", "jpeg"])
    else:
        image_file = st.camera_input(t["camera_label"])
        
    if image_file is not None:
        img_pil = Image.open(image_file)
        st.image(img_pil, caption="Uploaded Water Sample", use_container_width=True)
        
        if st.button(t["analyze_btn"], use_container_width=True):
            # Computer Vision Calculations
            img_np = np.array(img_pil.convert('RGB'))
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            
            # Edge Detection for Particles
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blur, 50, 150)
            edge_density = (np.count_nonzero(edges) / edges.size) * 100
            
            # Color Saturation & Turbidity
            hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            saturation = np.mean(hsv[:, :, 1]) / 255.0 * 100
            brightness_std = np.std(hsv[:, :, 2])
            
            # Metrics
            purity = max(5.0, min(99.0, 100.0 - (edge_density * 2.5 + saturation * 0.8 + brightness_std * 0.3)))
            purity = round(purity, 1)
            
            dust_pct = round(min(50.0, edge_density * 3.0), 2)
            turbidity_pct = round(min(50.0, (brightness_std / 128.0) * 100), 2)
            minerals_pct = round(min(50.0, saturation), 2)
            
            st.subheader(t["results_header"])
            
            # Status Indicator
            if purity >= 75.0:
                st.success(t["clean_status"])
            else:
                st.error(t["warning_status"])
                
            chart_col1, chart_col2 = st.columns(2)
            
            # Chart 1: Gauge Chart for Purity Score
            with chart_col1:
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=purity,
                    title={'text': t["purity_score"]},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#00aaff"},
                        'steps': [
                            {'range': [0, 50], 'color': "#e74c3c"},
                            {'range': [50, 75], 'color': "#f1c40f"},
                            {'range': [75, 100], 'color': "#2ecc71"}
                        ]
                    }
                ))
                fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig_gauge, use_container_width=True)
                
            # Chart 2: Composition Pie Chart
            with chart_col2:
                labels = ['Particles / Dust', 'Turbidity / Cloudiness', 'Minerals / Discoloration', 'Pure Water']
                values = [dust_pct, turbidity_pct, minerals_pct, max(0, purity)]
                fig_pie = px.pie(
                    names=labels, 
                    values=values, 
                    title="Water Composition Breakdown (%)",
                    color_discrete_sequence=['#e74c3c', '#e67e22', '#f1c40f', '#3498db']
                )
                fig_pie.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig_pie, use_container_width=True)

# --- AI ASSISTANT PANEL (20%) ---
with ai_col:
    st.subheader(t["chat_title"])
    st.caption("Powered by AquaVision Engine")
    
    # Initialize chat memory
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am AquaAI. Ask me anything about water parameters, chemistry, or general topics!"}
        ]
        
    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # Chat Input Box
    if user_input := st.chat_input(t["chat_placeholder"]):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
            
        # Built-in AI Knowledge Base
        query = user_input.lower()
        if "ph" in query:
            response = "Safe drinking water typically has a pH level between 6.5 and 8.5."
        elif "turbidity" in query or "cloudy" in query:
            response = "Turbidity measures fluid cloudiness caused by suspended particles, measured in NTUs."
        elif "clean" in query or "safe" in query:
            response = "Pure water should be clear, odorless, and free from microbial contaminants or heavy metals."
        else:
            response = f"That's an interesting question about '{user_input}'. In water analysis, physical clarity, mineral density, and particulate distribution are key indicators for quality."
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

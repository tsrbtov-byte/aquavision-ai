import streamlit as st
import cv2
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="AquaVision AI — Water Analyzer & Catalog",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Water-Themed Custom CSS
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #162a35;
        border-radius: 4px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Comprehensive Multi-Language Dictionary
TRANSLATIONS = {
    "English": {
        "title": "🌊 AquaVision AI",
        "subtitle": "Digital Water Quality Analysis & Educational Knowledge System",
        "tab_scanner": "🔍 AI Scanner",
        "tab_purify": "🧪 Emergency Purification",
        "tab_catalog": "🌍 Global Water Catalog",
        "tab_prevent": "🛡️ Pollution Prevention",
        "input_method": "Choose Input Method:",
        "upload_gallery": "📁 Gallery Upload",
        "use_camera": "📷 Camera Capture",
        "upload_label": "Upload water sample image",
        "camera_label": "Snap photo of water sample",
        "analyze_btn": "Run AI Analysis",
        "results_header": "📊 Analysis Results & Composition",
        "purity_score": "Purity Score",
        "clean_status": "Status: SAFE / CLEAR WATER",
        "warning_status": "Status: CONTAMINATED WATER DETECTED",
        "chat_title": "🤖 AquaAI Assistant",
        "chat_placeholder": "Ask about water parameters, filtration, or chemistry...",
        "sidebar_nav": "📌 System Modules",
        "purify_title": "🛠️ Emergency Water Purification (Field Methods)",
        "purify_bottle": "**1. DIY Bottle Sediment Filter:** Cut a bottle in half, poke a hole in the cap, and layer from bottom to top: fine cloth/cotton, crushed charcoal, fine sand, coarse sand, and pebbles.",
        "purify_boil": "**2. Rolling Boil:** Boil water vigorously for at least 1 full minute (3 minutes at high altitude) to eliminate pathogens.",
        "purify_sodis": "**3. SODIS (Solar Disinfection):** Place clear PET bottles filled with water in direct sunlight for 6–8 hours to kill micro-organisms with UV radiation.",
        "catalog_title": "🌍 Earth's Water Distribution Catalog",
        "prevent_title": "🛡️ Environmental Protection & Prevention Tips",
        "prevent_1": "• **Riparian Buffer Zones:** Plant native vegetation along riverbanks to absorb agricultural runoff and prevent erosion.",
        "prevent_2": "• **Waste Control:** Prevent direct disposal of untreated industrial chemicals and municipal sewage into water bodies.",
        "prevent_3": "• **Subterranean Aquifer Protection:** Reduce synthetic pesticide application to preserve groundwater quality."
    },
    "Azerbaijani": {
        "title": "🌊 AquaVision AI",
        "subtitle": "Rəqəmsal Su Keyfiyyəti Analizi və Maarifləndirici Bilik Sistemi",
        "tab_scanner": "🔍 AI Skaner",
        "tab_purify": "🧪 Fövqəladə Təmizləmə",
        "tab_catalog": "🌍 Qlobal Su Kataloqu",
        "tab_prevent": "🛡️ Çirklənmənin Qarşısının Alınması",
        "input_method": "Daxiletmə Üsulunu Seçin:",
        "upload_gallery": "📁 Qalereyadan Yüklə",
        "use_camera": "📷 Kameradan Çək",
        "upload_label": "Su nümayəsi şəklini yükləyin",
        "camera_label": "Su nümayəsinin şəklini çəkin",
        "analyze_btn": "Süni İntellekt Analizini Başlat",
        "results_header": "📊 Analiz Nəticələri və Tərkib",
        "purity_score": "Təmizlik Dərəcəsi",
        "clean_status": "Status: TƏMİZ VƏ TƏHLÜKƏSİZ SU",
        "warning_status": "Status: ÇİRKLƏNMİŞ SU AŞKAR EDİLDİ",
        "chat_title": "🤖 AquaAI Köməkçisi",
        "chat_placeholder": "Su göstəriciləri, filtrləmə və ya kimya haqqında soruşun...",
        "sidebar_nav": "📌 Sistem Modulları",
        "purify_title": "🛠️ Fövqəladə Su Təmizləmə Üsulları",
        "purify_bottle": "**1. Şüşə Qab Filtrinin Hazırlanması:** Plastik qabın dibini kəsin, qapağında dəlik açın və aşağıdan yuxarıya doğru sıx parça, əzilmiş kömür, incə qum, iri qum və daşları təbəqələndirin.",
        "purify_boil": "**2. Qaynatma Üsulu:** Bakteriya və mikrobları məhv etmək üçün suyu ən azı 1 dəqiqə intensiv qaynadın.",
        "purify_sodis": "**3. SODIS (Günəşlə Dezinfeksiya):** Şəffaf plastik qabı su ilə doldurub 6–8 saat birbaşa günəş işığı altında saxlayın.",
        "catalog_title": "🌍 Yer Kürəsinin Su Paylanması Kataloqu",
        "prevent_title": "🛡️ Ətraf Mühitin və Sularin Qorunması Tədbirləri",
        "prevent_1": "• **Bufer Zonalarının Salınması:** Çay kənarlarında bitki örtüyünün əkilməsi gübrə və çöküntü axıntılarının qarşısını alır.",
        "prevent_2": "• **Tullantı Nəzarəti:** Sənaye və məişət tullantı sularının təmizlənmədən su mənbələrinə axıdılmasının qarşısını almaq.",
        "prevent_3": "• **Yeraltı Suların Qorunması:** Kimyəvi pestisidlərin istifadəsini azaltmaqla yeraltı su qatlarını çirklənmədən qorumaq."
    },
    "Russian": {
        "title": "🌊 AquaVision AI",
        "subtitle": "Цифровая Система Анализа Качества Воды и Знаний",
        "tab_scanner": "🔍 AI Сканер",
        "tab_purify": "🧪 Аварийная Очистка",
        "tab_catalog": "🌍 Каталог Водных Ресурсов",
        "tab_prevent": "🛡️ Защита Экологии",
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
        "chat_placeholder": "Задайте вопрос о параметрах воды, фильтрации...",
        "sidebar_nav": "📌 Модули Системы",
        "purify_title": "🛠️ Аварийные Методы Очистки Воды",
        "purify_bottle": "**1. Самодельный Фильтр из Бутылки:** Отрежьте дно бутылки, сделайте отверстие в крышке и уложите слои снизу вверх: ткань, измельченный уголь, мелкий песок, крупный песок, галька.",
        "purify_boil": "**2. Кипячение:** Интенсивно кипятите воду не менее 1 минуты для полного уничтожения патогенов.",
        "purify_sodis": "**3. SODIS (Солнечная Дезинфекция):** Наполните прозрачные ПЭТ-бутылки водой и оставьте на солнце на 6–8 часов.",
        "catalog_title": "🌍 Каталог Распределения Воды на Земле",
        "prevent_title": "🛡️ Предотвращение Загрязнения Окружающей Среды",
        "prevent_1": "• **Буферные Зоны:** Посадка растений вдоль берегов рек предотвращает смыв сельскохозяйственных отходов.",
        "prevent_2": "• **Контроль Сбросов:** Исключение прямого сброса неочищенных промышленных и бытовых стоков.",
        "prevent_3": "• **Защита Подземных Вод:** Сокращение использования пестицидов для защиты водоносных горизонтов."
    }
}

# 4. Sidebar Language Controls & Navigation
selected_lang = st.sidebar.selectbox("Language / DİL", ["English", "Azerbaijani", "Russian"])
t = TRANSLATIONS[selected_lang]

st.sidebar.markdown("---")
st.sidebar.subheader(t["sidebar_nav"])
st.sidebar.info("AquaVision Engine v2.4\nDesigned for Sabahın Alimləri Project")

# 5. Screen Layout Split (80% Main Content, 20% Right AI Panel)
main_col, ai_col = st.columns([0.8, 0.2], gap="medium")

# --- MAIN WORKSPACE (80%) ---
with main_col:
    st.title(t["title"])
    st.caption(t["subtitle"])
    
    tabs = st.tabs([t["tab_scanner"], t["tab_purify"], t["tab_catalog"], t["tab_prevent"]])
    
    # --- TAB 1: AI SCANNER ---
    with tabs[0]:
        option = st.radio(t["input_method"], (t["upload_gallery"], t["use_camera"]), horizontal=True)
        image_file = None
        if option == t["upload_gallery"]:
            image_file = st.file_uploader(t["upload_label"], type=["jpg", "png", "jpeg"])
        else:
            image_file = st.camera_input(t["camera_label"])
            
        if image_file is not None:
            img_pil = Image.open(image_file)
            st.image(img_pil, caption="Sample Image", use_container_width=True)
            
            if st.button(t["analyze_btn"], use_container_width=True):
                # Computer Vision Calculations
                img_np = np.array(img_pil.convert('RGB'))
                img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
                
                gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                edges = cv2.Canny(blur, 50, 150)
                edge_density = (np.count_nonzero(edges) / edges.size) * 100
                
                hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
                saturation = np.mean(hsv[:, :, 1]) / 255.0 * 100
                brightness_std = np.std(hsv[:, :, 2])
                
                purity = max(5.0, min(99.0, 100.0 - (edge_density * 2.5 + saturation * 0.8 + brightness_std * 0.3)))
                purity = round(purity, 1)
                
                dust_pct = round(min(50.0, edge_density * 3.0), 2)
                turbidity_pct = round(min(50.0, (brightness_std / 128.0) * 100), 2)
                minerals_pct = round(min(50.0, saturation), 2)
                
                st.subheader(t["results_header"])
                if purity >= 75.0:
                    st.success(t["clean_status"])
                else:
                    st.error(t["warning_status"])
                    
                chart_col1, chart_col2 = st.columns(2)
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
                    
                with chart_col2:
                    labels = ['Dust / Particles', 'Turbidity / Cloudiness', 'Discoloration', 'Pure Water']
                    values = [dust_pct, turbidity_pct, minerals_pct, max(0, purity)]
                    fig_pie = px.pie(names=labels, values=values, title="Composition Breakdown (%)", color_discrete_sequence=['#e74c3c', '#e67e22', '#f1c40f', '#3498db'])
                    fig_pie.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                    st.plotly_chart(fig_pie, use_container_width=True)

    # --- TAB 2: EMERGENCY PURIFICATION ---
    with tabs[1]:
        st.subheader(t["purify_title"])
        st.write(t["purify_bottle"])
        st.write(t["purify_boil"])
        st.write(t["purify_sodis"])

    # --- TAB 3: WATER CATALOG ---
    with tabs[2]:
        st.subheader(t["catalog_title"])
        catalog_data = {
            "Water Type": ["Salty / Saline Oceans", "Glaciers & Ice Caps", "Groundwater Aquifers", "Surface Fresh Water"],
            "Share of Earth's Water (%)": [97.5, 1.75, 0.7, 0.01],
            "Key Characteristics": ["High Salinity (~35 g/L), Pacific, Atlantic, Caspian Sea", "Locked fresh water in Antarctica, Greenland, and high peaks", "Subterranean fresh water reservoirs used for agriculture", "Lakes, rivers, and wetlands used for direct human supply"]
        }
        st.table(catalog_data)

    # --- TAB 4: POLLUTION PREVENTION ---
    with tabs[3]:
        st.subheader(t["prevent_title"])
        st.write(t["prevent_1"])
        st.write(t["prevent_2"])
        st.write(t["prevent_3"])

# --- AI ASSISTANT PANEL (20%) ---
with ai_col:
    st.subheader(t["chat_title"])
    st.caption("Powered by AquaVision Engine")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am AquaAI. Ask me anything about water parameters, filtration, chemistry, or general topics!"}
        ]
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    if user_input := st.chat_input(t["chat_placeholder"]):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
            
        query = user_input.lower()
        if "ph" in query:
            response = "Safe drinking water typically has a pH level between 6.5 and 8.5."
        elif "turbidity" in query or "cloudy" in query:
            response = "Turbidity measures fluid cloudiness caused by suspended particles, measured in NTUs."
        elif "clean" in query or "filter" in query:
            response = "To clean dirty water, first filter out solid sediment, then boil or apply UV light/chlorine to disinfect."
        else:
            response = f"Regarding '{user_input}': In digital water analysis, measuring physical clarity, turbidity, and chemical balance are core metrics."
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

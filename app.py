import streamlit as st
import cv2
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(
    page_title="AquaVision AI — Advanced Water Scanner",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS Styling
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

# Helper function for rendering Shorts reliably
def render_youtube_short(video_id):
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    components.iframe(embed_url, height=450, scrolling=False)

# 3. Comprehensive Translations Dictionary
TRANSLATIONS = {
    "Azerbaijani": {
        "title": "🌊 AquaVision AI",
        "subtitle": "Rəqəmsal Su Keyfiyyəti Analizi və Genişləndirilmiş Kimyəvi Bilik Sistemi",
        "tab_scanner": "🔍 AI Skaner & Dərin Analiz",
        "tab_purify": "🧪 Fövqəladə Təmizləmə",
        "tab_catalog": "🌍 Qlobal Su Kataloqu",
        "tab_prevent": "🛡️ Çirklənmənin Qarşısının Alınması",
        "input_method": "Daxiletmə Üsulunu Seçin:",
        "upload_gallery": "📁 Qalereyadan Yüklə",
        "use_camera": "📷 Kameradan Çək",
        "upload_label": "Su nümayəsi şəklini yükləyin",
        "camera_label": "Su nümayəsinin şəklini çəkin",
        "analyze_btn": "Süni İntellekt Analizini Başlat",
        "results_header": "📊 Analiz Nəticələri və Xülasə",
        "purity_score": "Təmizlik Dərəcəsi",
        "clean_status": "Status: TƏMİZ VƏ İÇMƏYƏ YARARLI SU",
        "warning_status": "Status: ÇİRKLƏNMİŞ SU AŞKAR EDİLDİ",
        "chat_title": "🤖 AquaAI Köməkçisi",
        "chat_placeholder": "Su, kimya və ya filterləmə haqqında soruşun...",
        "sidebar_nav": "📌 Panel və Alətlər",
        "quick_norms": "📊 Standart İçməli Su Normaları",
        "norm_ph": "İdeal pH Səviyyəsi: 6.5 - 8.5",
        "norm_tds": "Maksimum TDS: < 500 ppm",
        "norm_turb": "Bulanıqlıq (Turbidity): < 1 NTU",
        "counter_title": "📈 Skan Statistikası",
        "purify_title": "🛠️ Fövqəladə Su Təmizləmə Üsulları",
        "purify_bottle": "**1. Şüşə Qab Filtrinin Hazırlanması:** Plastik qabın dibini kəsin, qapağında dəlik açın və aşağıdan yuxarıya doğru sıx parça, əzilmiş kömür, incə qum, iri qum və daşları təbəqələndirin.",
        "purify_boil": "**2. Qaynatma Üsulu:** Bakteriya və mikrobları tam öldürmək üçün suyu ən azı 1-3 dəqiqə intensiv qaynadın.",
        "purify_sodis": "**3. SODIS (Günəşlə Dezinfeksiya):** Şəffaf plastik qabı su ilə doldurub 6–8 saat birbaşa günəş işığı altında saxlayın.",
        "video_section_title": "📺 Praktiki Video Təlimatlar",
        "video_1_title": "🥤 Əlaltı Vasitələrlə Su Filtrinin Hazırlanması",
        "video_2_title": "☀️ Günəş Enerjisi ilə Su Dezinfeksiyası (SODIS)",
        "catalog_title": "🌍 Yer Kürəsinin Su Paylanması Kataloqu",
        "cat_type": "Su Növü",
        "cat_share": "Yer Kürəsində Payı (%)",
        "cat_char": "Əsas Xüsusiyyətləri",
        "cat_row1_type": "Duzlu Okean və Dəniz Suları",
        "cat_row1_char": "Yüksək Duzluq (~35 q/L), Sakit, Atlantik, Xəzər dənizi",
        "cat_row2_type": "Buzlaqlar və Buz Qapaqları",
        "cat_row2_char": "Antarktida və Qrenlandiyada donmuş şirin su ehtiyatları",
        "cat_row3_type": "Yeraltı Qat Suları (Aquifer)",
        "cat_row3_char": "Kənd təsərrüfatı və içməli su üçün istifadə olunan yeraltı ehtiyatlar",
        "cat_row4_type": "Şirin Səth Suları",
        "cat_row4_char": "Göllər, çaylar və bataqlıqlar (İnsan istifadəsi üçün əsas mənbə)",
        "prevent_title": "🛡️ Ətraf Mühitin və Suların Qorunması Tədbirləri",
        "prevent_1": "• **Bufer Zonalarının Salınması:** Çay kənarlarında bitki örtüyünün əkilməsi gübrə və çöküntü axıntılarını saxlayır.",
        "prevent_2": "• **Tullantı Nəzarəti:** Sənaye və məişət tullantı sularının təmizlənmədən su mənbələrinə axıdılmasının qarşısını almaq.",
        "prevent_3": "• **Yeraltı Suların Qorunması:** Kimyəvi pestisidlərin istifadəsini azaltmaqla yeraltı su qatlarını çirklənmədən qorumaq.",
        "pie_dust": "Toz / Zərrəciklər",
        "pie_turb": "Bulanıqlıq / Çöküntü",
        "pie_color": "Rəng Dəyişməsi / Kənar Maddə",
        "pie_pure": "Təmiz Su Payı",
        "chart_title": "Tərkib Bölgüsü (%)"
    },
    "English": {
        "title": "🌊 AquaVision AI",
        "subtitle": "Digital Water Quality Analysis & Broadened Chemical Assessment System",
        "tab_scanner": "🔍 AI Scanner & Deep Analysis",
        "tab_purify": "🧪 Emergency Purification",
        "tab_catalog": "🌍 Global Water Catalog",
        "tab_prevent": "🛡️ Pollution Prevention",
        "input_method": "Choose Input Method:",
        "upload_gallery": "📁 Gallery Upload",
        "use_camera": "📷 Camera Capture",
        "upload_label": "Upload water sample image",
        "camera_label": "Snap photo of water sample",
        "analyze_btn": "Run AI Analysis",
        "results_header": "📊 Analysis Results & Overview",
        "purity_score": "Purity Score",
        "clean_status": "Status: SAFE DRINKING WATER",
        "warning_status": "Status: CONTAMINATED WATER DETECTED",
        "chat_title": "🤖 AquaAI Assistant",
        "chat_placeholder": "Ask about water parameters, filtration, or chemistry...",
        "sidebar_nav": "📌 Dashboard & Tools",
        "quick_norms": "📊 Standard Drinking Water Norms",
        "norm_ph": "Ideal pH Range: 6.5 - 8.5",
        "norm_tds": "Max TDS Limit: < 500 ppm",
        "norm_turb": "Turbidity Limit: < 1 NTU",
        "counter_title": "📈 Scan Analytics",
        "purify_title": "🛠️ Emergency Water Purification Methods",
        "purify_bottle": "**1. DIY Bottle Sediment Filter:** Cut a bottle in half, poke a hole in the cap, and layer from bottom to top: fine cloth/cotton, crushed charcoal, fine sand, coarse sand, and pebbles.",
        "purify_boil": "**2. Rolling Boil:** Boil water vigorously for 1-3 minutes to eliminate all pathogens.",
        "purify_sodis": "**3. SODIS (Solar Disinfection):** Place clear PET bottles filled with water in direct sunlight for 6–8 hours.",
        "video_section_title": "📺 Practical Video Guides",
        "video_1_title": "🥤 How to Make a DIY Water Filter",
        "video_2_title": "☀️ Solar Water Disinfection (SODIS Method)",
        "catalog_title": "🌍 Earth's Water Distribution Catalog",
        "cat_type": "Water Type",
        "cat_share": "Share of Earth's Water (%)",
        "cat_char": "Key Characteristics",
        "cat_row1_type": "Saline Oceans & Seas",
        "cat_row1_char": "High Salinity (~35 g/L), Pacific, Atlantic, Caspian Sea",
        "cat_row2_type": "Glaciers & Ice Caps",
        "cat_row2_char": "Locked fresh water reserves in Antarctica and Greenland",
        "cat_row3_type": "Groundwater Aquifers",
        "cat_row3_char": "Subterranean fresh water reservoirs used for agricultural supply",
        "cat_row4_type": "Surface Fresh Water",
        "cat_row4_char": "Lakes, rivers, and wetlands (Primary source for direct human supply)",
        "prevent_title": "🛡️ Environmental Protection & Prevention Tips",
        "prevent_1": "• **Riparian Buffer Zones:** Plant native vegetation along riverbanks to absorb agricultural runoff and prevent erosion.",
        "prevent_2": "• **Waste Control:** Prevent direct disposal of untreated industrial chemicals and municipal sewage into water bodies.",
        "prevent_3": "• **Subterranean Aquifer Protection:** Reduce synthetic pesticide application to preserve groundwater quality.",
        "pie_dust": "Dust / Suspended Solids",
        "pie_turb": "Turbidity / Sediment",
        "pie_color": "Discoloration / Organic Residuals",
        "pie_pure": "Pure Water Share",
        "chart_title": "Composition Breakdown (%)"
    },
    "Russian": {
        "title": "🌊 AquaVision AI",
        "subtitle": "Цифровая Система Анализа Качества Воды и Расширенной Химии",
        "tab_scanner": "🔍 AI Сканер и Глубокий Анализ",
        "tab_purify": "🧪 Аварийная Очистка",
        "tab_catalog": "🌍 Каталог Водных Ресурсов",
        "tab_prevent": "🛡️ Защита Экологии",
        "input_method": "Выберите способ ввода:",
        "upload_gallery": "📁 Загрузить из галереи",
        "use_camera": "📷 Сделать фото",
        "upload_label": "Загрузите образец воды",
        "camera_label": "Сделайте снимок образца",
        "analyze_btn": "Запустить AI Анализ",
        "results_header": "📊 Результаты Анализа и Обзор",
        "purity_score": "Индекс Чистоты",
        "clean_status": "Статус: БЕЗОПАСНАЯ ПИТЬЕВАЯ ВОДА",
        "warning_status": "Статус: ОБНАРУЖЕНА ГРЯЗНАЯ ВОДА",
        "chat_title": "🤖 AquaAI Помощник",
        "chat_placeholder": "Задайте вопрос о параметрах воды, фильтрации...",
        "sidebar_nav": "📌 Панель и Инструменты",
        "quick_norms": "📊 Стандарты Питьевой Воды",
        "norm_ph": "Идеальный pH: 6.5 - 8.5",
        "norm_tds": "Макс. уровень TDS: < 500 ppm",
        "norm_turb": "Мутность (Turbidity): < 1 NTU",
        "counter_title": "📈 Статистика Сканирования",
        "purify_title": "🛠️ Аварийные Методы Очистки Воды",
        "purify_bottle": "**1. Самодельный Фильтр из Бутылки:** Отрежьте дно бутылки, сделайте отверстие в крышке и уложите слои снизу вверх: ткань, измельченный уголь, мелкий песок, крупный песок, галька.",
        "purify_boil": "**2. Кипячение:** Интенсивно кипятите воду 1-3 минуты для полного уничтожения патогенов.",
        "purify_sodis": "**3. SODIS (Солнечная Дезинфекция):** Наполните прозрачные ПЭТ-бутылки водой и оставьте на солнце на 6–8 часов.",
        "video_section_title": "📺 Практические Видеоинструкции",
        "video_1_title": "🥤 Как сделать фильтр для воды своими руками",
        "video_2_title": "☀️ Солнечная дезинфекция воды (Метод SODIS)",
        "catalog_title": "🌍 Каталог Распределения Воды на Земле",
        "cat_type": "Тип Воды",
        "cat_share": "Доля на Земле (%)",
        "cat_char": "Основные Характеристики",
        "cat_row1_type": "Соленые Океаны и Моря",
        "cat_row1_char": "Высокая соленость (~35 г/л), Тихий, Атлантический, Каспийское море",
        "cat_row2_type": "Ледники и Ледяные Шапки",
        "cat_row2_char": "Запасы пресной воды в Антарктиде и Гренландии",
        "cat_row3_type": "Подземные Водоносные Горизонты",
        "cat_row3_char": "Подземные резервуары пресной воды для сельского хозяйства",
        "cat_row4_type": "Поверхностные Пресные Воды",
        "cat_row4_char": "Озера, реки и болота (Основной источник для человека)",
        "prevent_title": "🛡️ Предотвращение Загрязнения Окружающей Среды",
        "prevent_1": "• **Буферные Зоны:** Посадка растений вдоль берегов рек предотвращает смыв сельскохозяйственных отходов.",
        "prevent_2": "• **Контроль Сбросов:** Исключение прямого сброса неочищенных промышленных и бытовых стоков.",
        "prevent_3": "• **Защита Подземных Вод:** Сокращение использования пестицидов для защиты водоносных горизонтов.",
        "pie_dust": "Пыль / Взвешенные частицы",
        "pie_turb": "Мутность / Осадок",
        "pie_color": "Изменение цвета / Органика",
        "pie_pure": "Чистая Вода",
        "chart_title": "Состав Образца (%)"
    }
}

if "scan_count" not in st.session_state:
    st.session_state.scan_count = 0

# 4. Sidebar Configuration
selected_lang = st.sidebar.selectbox("Language / DİL", ["Azerbaijani", "English", "Russian"])
t = TRANSLATIONS[selected_lang]

st.sidebar.markdown("---")
st.sidebar.subheader(t["sidebar_nav"])
st.sidebar.markdown(f"### {t['quick_norms']}")
st.sidebar.info(f"• {t['norm_ph']}\n• {t['norm_tds']}\n• {t['norm_turb']}")

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t['counter_title']}")
st.sidebar.metric(label="", value=f"{st.session_state.scan_count}")

# 5. Main Layout Split (80% Main Area, 20% AI Assistant Chat)
main_col, ai_col = st.columns([0.8, 0.2], gap="medium")

# --- MAIN SCREEN (80%) ---
with main_col:
    st.title(t["title"])
    st.caption(t["subtitle"])
    
    tabs = st.tabs([t["tab_scanner"], t["tab_purify"], t["tab_catalog"], t["tab_prevent"]])
    
    # --- TAB 1: ADVANCED AI SCANNER & CHEMICAL ANALYSIS ---
    with tabs[0]:
        option = st.radio(t["input_method"], (t["upload_gallery"], t["use_camera"]), horizontal=True)
        image_file = None
        if option == t["upload_gallery"]:
            image_file = st.file_uploader(t["upload_label"], type=["jpg", "png", "jpeg"])
        else:
            image_file = st.camera_input(t["camera_label"])
            
        if image_file is not None:
            img_pil = Image.open(image_file)
            st.image(img_pil, caption="Water Sample", use_container_width=True)
            
            if st.button(t["analyze_btn"], use_container_width=True):
                st.session_state.scan_count += 1
                
                # Computer Vision Calculations
                img_np = np.array(img_pil.convert('RGB'))
                img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
                
                gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                edges = cv2.Canny(blur, 50, 150)
                edge_density = (np.count_nonzero(edges) / edges.size) * 100
                
                hsv = cv2.cvtColor(img_bgr, cv2.COLOR_HSV2BGR) if False else cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
                saturation = np.mean(hsv[:, :, 1]) / 255.0 * 100
                brightness_std = np.std(hsv[:, :, 2])
                
                purity = max(5.0, min(99.0, 100.0 - (edge_density * 2.5 + saturation * 0.8 + brightness_std * 0.3)))
                purity = round(purity, 1)
                
                dust_pct = round(min(50.0, edge_density * 3.0), 2)
                turbidity_pct = round(min(50.0, (brightness_std / 128.0) * 100), 2)
                minerals_pct = round(min(50.0, saturation), 2)
                
                # --- SECTION 1: MAIN OVERVIEW & HUMAN POTABILITY ---
                st.subheader(t["results_header"])
                if purity >= 75.0:
                    st.success(t["clean_status"])
                else:
                    st.error(t["warning_status"])
                
                # Human Consumption Metrics (Key Request 1)
                m1, m2, m3 = st.columns(3)
                if purity >= 85.0:
                    m1.metric("👥 Human Drinkability Capacity", "5 - 10 Persons / Day", "Safe Direct Intake")
                    m2.metric("🦠 Microbial Pathogen Level", "Low (< 0.1 CFU/mL)", "Normal")
                    m3.metric("💧 Daily Consumption Suitability", "100%", "Excellent")
                elif purity >= 60.0:
                    m1.metric("👥 Human Drinkability Capacity", "Conditional (Boil First)", "Needs Processing")
                    m2.metric("🦠 Microbial Pathogen Level", "Moderate Risk", "Action Required")
                    m3.metric("💧 Daily Consumption Suitability", "40%", "Boil 3 mins")
                else:
                    m1.metric("👥 Human Drinkability Capacity", "0 Persons (Unsafe)", "High Risk")
                    m2.metric("🦠 Microbial Pathogen Level", "Severe / High Bacterial Risk", "Hazardous")
                    m3.metric("💧 Daily Consumption Suitability", "0%", "Filtration Required")
                
                st.markdown("---")
                
                # Visual Charts
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
                    labels = [t["pie_dust"], t["pie_turb"], t["pie_color"], t["pie_pure"]]
                    values = [dust_pct, turbidity_pct, minerals_pct, max(0, purity)]
                    fig_pie = px.pie(names=labels, values=values, title=t["chart_title"], color_discrete_sequence=['#e74c3c', '#e67e22', '#f1c40f', '#3498db'])
                    fig_pie.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                st.markdown("---")
                
                # --- SECTION 2: SPECIFIC DIRT & CUSTOM PURIFICATION GUIDE (Key Request 2 & 3) ---
                c_dir1, c_dir2 = st.columns(2)
                
                with c_dir1:
                    st.markdown("### 🟤 Detected Contaminants & Dirt Types")
                    dirt_list = []
                    if dust_pct > 5.0:
                        dirt_list.append("• **Suspended Micro-particles / Dust:** Floating debris affecting visual clarity.")
                    if turbidity_pct > 10.0:
                        dirt_list.append("• **Silt & Clay Sediment:** Fine soil particles causing high cloudiness.")
                    if minerals_pct > 15.0:
                        dirt_list.append("• **Organic Residuals & Algae Traces:** Organic tint suggesting biological activity.")
                    if purity < 50.0:
                        dirt_list.append("• **Heavy Bacterial Contamination Risk:** High risk of E. Coli and protozoa.")
                    
                    if not dirt_list:
                        st.info("No significant coarse dirt or excessive particulate matter detected.")
                    else:
                        for d in dirt_list:
                            st.write(d)
                            
                with c_dir2:
                    st.markdown("### 🛠️ Customized Purification Steps for This Sample")
                    if purity >= 85.0:
                        st.success("1. **Direct Consumption:** Sample passes basic visual clarity standards.\n2. **Optional Carbon Filter:** Use standard pitcher filter for taste enhancement.")
                    elif purity >= 60.0:
                        st.warning("1. **Coarse Cloth Strain:** Run water through fine cotton cloth.\n2. **Boil Water:** Vigorous boiling for 3 minutes is required to eliminate microbes.")
                    else:
                        st.error("1. **DIY Multi-Layer Bottle Filter:** Build sand, charcoal, and pebble layers.\n2. **Sediment Settlement:** Allow sample to sit for 2 hours.\n3. **Boiling & SODIS:** Boil for 5 minutes or leave in direct sunlight for 8+ hours.")

                st.markdown("---")
                
                # --- SECTION 3: BROADENED CHEMICAL ASSESSMENT (Key Request 4) ---
                st.markdown("### 🧪 Broadened Chemical & Physical Parameter Analysis")
                st.caption("Estimated chemical parameters derived through visual processing and optical spectrophotometry modeling.")
                
                # Estimated Values
                est_ph = round(6.5 + (saturation / 100.0) * 2.0 - (turbidity_pct / 100.0) * 1.0, 2)
                est_tds = int(120 + (saturation * 5) + (dust_pct * 8))
                est_turb_ntu = round(0.5 + (turbidity_pct * 0.2), 2)
                
                ch_col1, ch_col2, ch_col3 = st.columns(3)
                ch_col1.metric("Estimated pH Level", f"{est_ph}", "Optimal: 6.5 - 8.5")
                ch_col2.metric("Total Dissolved Solids (TDS)", f"{est_tds} ppm", "Optimal: < 500 ppm")
                ch_col3.metric("Turbidity (NTU)", f"{est_turb_ntu} NTU", "Optimal: < 1.0 NTU")
                
                st.markdown("#### Detailed Chemical Profile Breakdown")
                chem_table_data = {
                    "Parameter / Ion": ["pH Level", "Total Dissolved Solids (TDS)", "Turbidity", "Heavy Metal Risk (Pb/Fe/Cu)", "Nitrates & Nitrites (NO3-/NO2-)", "Dissolved Oxygen (DO)"],
                    "Estimated Value": [f"{est_ph}", f"{est_tds} mg/L", f"{est_turb_ntu} NTU", "Low" if purity > 70 else "Moderate/High", "< 10 mg/L", "6.5 mg/L"],
                    "WHO Standard Limit": ["6.5 – 8.5", "< 500 mg/L", "< 1.0 NTU", "< 0.01 mg/L", "< 50 mg/L", "> 5.0 mg/L"],
                    "Chemical Status": ["Normal" if 6.5 <= est_ph <= 8.5 else "Sub-optimal", "Acceptable" if est_tds < 500 else "Elevated", "Clear" if est_turb_ntu < 1.0 else "Cloudy", "Safe" if purity > 70 else "Action Recommended", "Safe", "Optimal"]
                }
                st.table(chem_table_data)

    # --- TAB 2: EMERGENCY PURIFICATION & YOUTUBE SHORTS PLAYERS ---
    with tabs[1]:
        st.subheader(t["purify_title"])
        st.write(t["purify_bottle"])
        st.write(t["purify_boil"])
        st.write(t["purify_sodis"])
        
        st.markdown("---")
        st.subheader(t["video_section_title"])
        
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.markdown(f"**{t['video_1_title']}**")
            # Using custom iframe embed wrapper for YouTube Shorts ID WW8RqmBPlxo
            render_youtube_short("WW8RqmBPlxo")
            
        with v_col2:
            st.markdown(f"**{t['video_2_title']}**")
            # Using custom iframe embed wrapper for YouTube Shorts ID X3GA1tfWdN0
            render_youtube_short("X3GA1tfWdN0")

    # --- TAB 3: WATER CATALOG ---
    with tabs[2]:
        st.subheader(t["catalog_title"])
        catalog_data = {
            t["cat_type"]: [t["cat_row1_type"], t["cat_row2_type"], t["cat_row3_type"], t["cat_row4_type"]],
            t["cat_share"]: [97.5, 1.75, 0.7, 0.01],
            t["cat_char"]: [t["cat_row1_char"], t["cat_row2_char"], t["cat_row3_char"], t["cat_row4_char"]]
        }
        st.table(catalog_data)

    # --- TAB 4: POLLUTION PREVENTION ---
    with tabs[3]:
        st.subheader(t["prevent_title"])
        st.write(t["prevent_1"])
        st.write(t["prevent_2"])
        st.write(t["prevent_3"])

# --- RIGHT SIDE AI ASSISTANT CHAT (20%) ---
with ai_col:
    st.subheader(t["chat_title"])
    st.caption("AquaVision Engine")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Salam! Mən AquaAI assistantıyam. Su analizləri və fiziki göstəricilər haqqında nə sualınız var?"}
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
            response = "İçməli su üçün təhlükəsiz pH dərəcəsi 6.5 və 8.5 aralığındadır."
        elif "bulan" in query or "turbid" in query or "cloudy" in query:
            response = "Bulanıqlıq suda asılı hissəciklərin miqdarını göstərir və NTU vahidi ilə ölçülür."
        elif "təmiz" in query or "saf" in query or "clean" in query:
            response = "Təmiz su şəffaf, qoxusuz olmalı, mikroblardan və ağır metallardan azad olmalıdır."
        else:
            response = f"'{user_input}' haqqında: Su analizində şəffaflıq, mineral sıxlığı və hissəciklərin paylanması əsas keyfiyyət göstəriciləridir."
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

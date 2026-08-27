import streamlit as st
import cv2
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# 1. Səhifə Tənzimləmələri
st.set_page_config(
    page_title="AquaVision AI — Su Analiz Sistemi",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Xüsusi Dizayn (CSS)
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

# 3. 100% TAM VƏ DƏQİQ TƏRCÜMƏ LÜĞƏTİ
TRANSLATIONS = {
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
        "chat_placeholder": "Su, kimya və ya filterləmə haqqında soruşun...",
        "sidebar_nav": "📌 Panel və Alətlər",
        "quick_norms": "📊 Standart İçməli Su Normaları",
        "norm_ph": "İdeal pH Səviyyəsi: 6.5 - 8.5",
        "norm_tds": "Maksimum TDS: < 500 ppm",
        "norm_turb": "Bulanıqlıq (Turbidity): < 1 NTU",
        "counter_title": "📈 Skan Statistikası",
        "purify_title": "🛠️ Fövqəladə Su Təmizləmə Üsulları",
        "purify_bottle": "**1. Şüşə Qab Filtrinin Hazırlanması:** Plastik qabın dibini kəsin, qapağında dəlik açın və aşağıdan yuxarıya doğru sıx parça, əzilmiş kömür, incə qum, iri qum və daşları təbəqələndirin.",
        "purify_boil": "**2. Qaynatma Üsulu:** Bakteriya və mikrobları tam öldürmək üçün suyu ən azı 1 dəqiqə intensiv qaynadın.",
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
        "sidebar_nav": "📌 Dashboard & Tools",
        "quick_norms": "📊 Standard Drinking Water Norms",
        "norm_ph": "Ideal pH Range: 6.5 - 8.5",
        "norm_tds": "Max TDS Limit: < 500 ppm",
        "norm_turb": "Turbidity Limit: < 1 NTU",
        "counter_title": "📈 Scan Analytics",
        "purify_title": "🛠️ Emergency Water Purification Methods",
        "purify_bottle": "**1. DIY Bottle Sediment Filter:** Cut a bottle in half, poke a hole in the cap, and layer from bottom to top: fine cloth/cotton, crushed charcoal, fine sand, coarse sand, and pebbles.",
        "purify_boil": "**2. Rolling Boil:** Boil water vigorously for at least 1 full minute to eliminate all pathogens.",
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
        "pie_dust": "Dust / Particles",
        "pie_turb": "Turbidity / Sediment",
        "pie_color": "Discoloration / Foreign Matter",
        "pie_pure": "Pure Water Share",
        "chart_title": "Composition Breakdown (%)"
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
        "sidebar_nav": "📌 Панель и Инструменты",
        "quick_norms": "📊 Стандарты Питьевой Воды",
        "norm_ph": "Идеальный pH: 6.5 - 8.5",
        "norm_tds": "Макс. уровень TDS: < 500 ppm",
        "norm_turb": "Мутность (Turbidity): < 1 NTU",
        "counter_title": "📈 Статистика Сканирования",
        "purify_title": "🛠️ Аварийные Методы Очистки Воды",
        "purify_bottle": "**1. Самодельный Фильтр из Бутылки:** Отрежьте дно бутылки, сделайте отверстие в крышке и уложите слои снизу вверх: ткань, измельченный уголь, мелкий песок, крупный песок, галька.",
        "purify_boil": "**2. Кипячение:** Интенсивно кипятите воду не менее 1 минуты для полного уничтожения патогенов.",
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
        "pie_dust": "Пыль / Частицы",
        "pie_turb": "Мутность / Осадок",
        "pie_color": "Изменение цвета",
        "pie_pure": "Чистая Вода",
        "chart_title": "Состав Образца (%)"
    }
}

# Session State tənzimləmələri
if "scan_count" not in st.session_state:
    st.session_state.scan_count = 0

# 4. Sol Panel (Sidebar) Tənzimləmələri
selected_lang = st.sidebar.selectbox("Language / DİL", ["Azerbaijani", "English", "Russian"])
t = TRANSLATIONS[selected_lang]

st.sidebar.markdown("---")
st.sidebar.subheader(t["sidebar_nav"])

# Sol hissəyə əlavə olunan faydalı vidjetlər:
st.sidebar.markdown(f"### {t['quick_norms']}")
st.sidebar.info(f"• {t['norm_ph']}\n• {t['norm_tds']}\n• {t['norm_turb']}")

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t['counter_title']}")
st.sidebar.metric(label="", value=f"{st.session_state.scan_count}")

# 5. Ekran Bölgüsü (80% Əsas Sahə, 20% Sağ Süni İntellekt Çatı)
main_col, ai_col = st.columns([0.8, 0.2], gap="medium")

# --- ƏSAS EKRAN (80%) ---
with main_col:
    st.title(t["title"])
    st.caption(t["subtitle"])
    
    tabs = st.tabs([t["tab_scanner"], t["tab_purify"], t["tab_catalog"], t["tab_prevent"]])
    
    # --- TAB 1: AI SKANER ---
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
                
                # Kompüter Görməsi (Computer Vision) Hesablamaları
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
                    labels = [t["pie_dust"], t["pie_turb"], t["pie_color"], t["pie_pure"]]
                    values = [dust_pct, turbidity_pct, minerals_pct, max(0, purity)]
                    fig_pie = px.pie(names=labels, values=values, title=t["chart_title"], color_discrete_sequence=['#e74c3c', '#e67e22', '#f1c40f', '#3498db'])
                    fig_pie.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                    st.plotly_chart(fig_pie, use_container_width=True)

    # --- TAB 2: FÖVQƏLADƏ TƏMİZLƏMƏ (VİDEOLAR İLƏ) ---
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
            # Əlaltı vasitələrlə filtr hazırlanması videosu
            st.video("https://youtube.com/shorts/WW8RqmBPlxo?si=GhvZ0TCBuYEiZFpu")
            
        with v_col2:
            st.markdown(f"**{t['video_2_title']}**")
            # SODIS Solar Disinfection videosu
            st.video("https://youtube.com/shorts/X3GA1tfWdN0?si=l0zp_MRS0VWPGrQj")

    # --- TAB 3: SU KATALOQU ---
    with tabs[2]:
        st.subheader(t["catalog_title"])
        catalog_data = {
            t["cat_type"]: [t["cat_row1_type"], t["cat_row2_type"], t["cat_row3_type"], t["cat_row4_type"]],
            t["cat_share"]: [97.5, 1.75, 0.7, 0.01],
            t["cat_char"]: [t["cat_row1_char"], t["cat_row2_char"], t["cat_row3_char"], t["cat_row4_char"]]
        }
        st.table(catalog_data)

    # --- TAB 4: ÇİRKLƏNMƏNİN QARŞISININ ALINMASI ---
    with tabs[3]:
        st.subheader(t["prevent_title"])
        st.write(t["prevent_1"])
        st.write(t["prevent_2"])
        st.write(t["prevent_3"])

# --- SAĞ SÜNİ İNTELLEKT ÇAT PANELİ (20%) ---
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

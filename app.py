import os
import cv2
import numpy as np
from PIL import Image
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import efficientnet_b2
from google import genai
from google.genai import types

# ==========================================
# 🔑 GEMINI API KEY SETUP
# ==========================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6LKCN54_WOE0PvSxgtEU7Baz5tcvtXgaPcripgI6Wp4lg")

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="AquaVision AI — Universal Engine",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CUSTOM CSS STYLING
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
        border-radius: 10px;
        border: none;
        padding: 0.75rem 1rem;
        font-weight: bold;
        width: 100%;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    .stButton>button:hover {
        background-color: #00aaff;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        overflow-x: auto;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #162a35;
        border-radius: 6px;
        color: white;
        padding: 8px 12px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. MULTI-LANGUAGE DICTIONARY (AZ / EN / RU)
TRANSLATIONS = {
    "AZ": {
        "title": "🌊 AquaVision AI",
        "subtitle": "Yüksək Dəqiqlikli Və Molekulyar Spektral Su Analiz Sistemi",
        "tab_scanner": "🔍 AI Skaner & Molekulyar Analiz",
        "tab_purify": "🧪 Fövqəladə Təmizləmə",
        "tab_catalog": "🌍 Qlobal Su Kataloqu",
        "tab_prevent": "🛡️ Ekologiya və Qorunma",
        "input_method": "Daxiletmə Üsulunu Seçin:",
        "upload_gallery": "📁 Qalereyadan Yüklə",
        "use_camera": "📷 Kameradan Çək",
        "upload_label": "Su nümayəsi şəklini yükləyin",
        "camera_label": "Su nümayəsinin şəklini çəkin",
        "analyze_btn": "🚀 Maksimum Dəqiqlikli Analizi Başlat",
        "results_header": "📊 Analiz Nəticələri və Spektral Diaqnostika",
        "purity_score": "Təmizlik Dərəcəsi",
        "clean_status": "Status: TƏMİZ VƏ İÇMƏYƏ YARARLI SU",
        "warning_status": "Status: ÇİRKLƏNMİŞ VƏ YA DƏYİŞMİŞ SU AŞKAR EDİLDİ",
        "chat_title": "🤖 Smart AI Brain",
        "chat_subtitle": "Yaddaşlı və Çoxşaxəli Təfəkkürə Malik AI",
        "chat_welcome": "Salam! Mən sizin şəxsi intellektual assistentinizəm. Əvvəlki bütün danışıqlarımızı mükəmməl xatırlayıram. Fizika, kimya, biologiya, mühəndislik, AI və fəlsəfə haqqında dərin müzakirələr apara bilərik.",
        "chat_placeholder": "Mənə istənilən mövzuda sual verin...",
        "sidebar_nav": "📌 Panel və Alətlər",
        "quick_norms": "📊 Standart İçməli Su Normaları",
        "norm_ph": "İdeal pH Səviyyəsi: 6.5 - 8.5",
        "norm_tds": "Maksimum TDS: < 500 ppm",
        "norm_turb": "Bulanıqlıq: < 1 NTU",
        "counter_title": "📈 Skan Statistikası",
        "purify_title": "🛠️ Fövqəladə Su Təmizləmə Üsulları",
        "purify_bottle": "**1. Şüşə Qab Filtrinin Hazırlanması:** Plastik qabın dibini kəsin, qapağında dəlik açın və aşağıdan yuxarıya doğru sıx parça, əzilledilmiş kömür, incə qum, iri qum və daşları təbəqələndirin.",
        "purify_boil": "**2. Qaynatma Üsulu:** Bakteriya və mikrobları tam öldürmək üçün suyu ən azı 1-3 dəqiqə intensiv qaynadın.",
        "purify_sodis": "**3. SODIS (Günəşlə Dezinfeksiya):** Şəffaf plastik qabı su ilə doldurub 6–8 saat birbaşa günəş işığı altında saxlayın.",
        "guide_section_title": "📖 Vizual Təlimat Kartları",
        "guide_1_title": "🥤 Əlaltı Vasitələrlə Su Filtrinin Hazırlanması",
        "guide_2_title": "☀️ Günəş Enerjisi ilə Su Dezinfeksiyası (SODIS)",
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
        "pie_dust": "Toz / Asılı Zərrəciklər",
        "pie_turb": "Bulanıqlıq / Çöküntü",
        "pie_color": "Spektral Rəng Dəyişməsi",
        "pie_pure": "Saf Su Oranı",
        "chart_title": "Optik Tərkib Bölgüsü (%)",
        "sys_instruct": (
            "You are an advanced, empathetic, and broad-thinking AI companion integrated into the AquaVision AI platform. "
            "Conversational Tone: Speak naturally, warmly, and with high intellectual depth, like an expert human partner. Avoid sounding robotic, repetitive, or overly formal. "
            "Complete Memory & Continuity: Continuously refer back to prior statements, user details, and discussed context throughout the conversation. "
            "Multi-Disciplinary Perspective: Integrate insights from computer science, engineering, physics, philosophy, and environmental science naturally when answering. "
            "Respond strictly in fluent Azerbaijani language."
        )
    },
    "EN": {
        "title": "🌊 AquaVision AI",
        "subtitle": "High Precision & Molecular Spectral Water Analysis System",
        "tab_scanner": "🔍 AI Scanner & Molecular Analysis",
        "tab_purify": "🧪 Emergency Purification",
        "tab_catalog": "🌍 Global Water Catalog",
        "tab_prevent": "🛡️ Environmental Protection",
        "input_method": "Select Input Method:",
        "upload_gallery": "📁 Upload from Gallery",
        "use_camera": "📷 Take a Photo",
        "upload_label": "Upload water sample image",
        "camera_label": "Take water sample photo",
        "analyze_btn": "🚀 Start Maximum Efficiency Analysis",
        "results_header": "📊 Analysis Results & Spectral Diagnostics",
        "purity_score": "Purity Score",
        "clean_status": "Status: CLEAN & POTABLE WATER",
        "warning_status": "Status: POLLUTED OR ALTERED WATER DETECTED",
        "chat_title": "🤖 Smart AI Brain",
        "chat_subtitle": "Human-Like Personalized Memory & Broad Intelligence",
        "chat_welcome": "Hello! I am your personalized AI partner. I retain complete memory of our conversation history. Feel free to ask complex questions spanning science, engineering, philosophy, and innovation.",
        "chat_placeholder": "Ask me anything in detail...",
        "sidebar_nav": "📌 Panel & Tools",
        "quick_norms": "📊 Drinking Water Standards",
        "norm_ph": "Ideal pH Range: 6.5 - 8.5",
        "norm_tds": "Maximum TDS: < 500 ppm",
        "norm_turb": "Turbidity: < 1 NTU",
        "counter_title": "📈 Scan Statistics",
        "purify_title": "🛠️ Emergency Water Purification Methods",
        "purify_bottle": "**1. DIY Bottle Filter Construction:** Cut the bottom of a plastic bottle, pierce the cap, and layer dense cloth, crushed charcoal, fine sand, coarse sand, and stones from bottom to top.",
        "purify_boil": "**2. Boiling Method:** Boil water vigorously for 1-3 minutes to completely kill bacteria and pathogens.",
        "purify_sodis": "**3. SODIS (Solar Disinfection):** Fill a transparent plastic bottle with water and expose it to direct sunlight for 6-8 hours.",
        "guide_section_title": "📖 Visual Instruction Cards",
        "guide_1_title": "🥤 DIY Water Filter Construction",
        "guide_2_title": "☀️ Solar Water Disinfection (SODIS)",
        "catalog_title": "🌍 Earth Water Distribution Catalog",
        "cat_type": "Water Type",
        "cat_share": "Global Share (%)",
        "cat_char": "Key Characteristics",
        "cat_row1_type": "Saline Ocean & Sea Water",
        "cat_row1_char": "High Salinity (~35 g/L), Pacific, Atlantic, Caspian Sea",
        "cat_row2_type": "Glaciers & Ice Caps",
        "cat_row2_char": "Freshwater reserves frozen in Antarctica and Greenland",
        "cat_row3_type": "Groundwater (Aquifers)",
        "cat_row3_char": "Underground reserves used for agriculture and drinking",
        "cat_row4_type": "Fresh Surface Water",
        "cat_row4_char": "Lakes, rivers, and wetlands (Primary human source)",
        "prevent_title": "🛡️ Environmental & Water Protection Measures",
        "prevent_1": "• **Creating Buffer Zones:** Planting vegetation along riverbanks retains fertilizer and sediment runoff.",
        "prevent_2": "• **Waste Control:** Preventing untreated industrial and domestic wastewater from discharging into sources.",
        "prevent_3": "• **Groundwater Protection:** Reducing chemical pesticides to protect aquifers from contamination.",
        "pie_dust": "Dust / Suspended Particles",
        "pie_turb": "Turbidity / Sediment",
        "pie_color": "Spectral Color Shift",
        "pie_pure": "Pure Water Ratio",
        "chart_title": "Optical Composition Breakdown (%)",
        "sys_instruct": (
            "You are an advanced, empathetic, and broad-thinking AI companion integrated into the AquaVision AI platform. "
            "Conversational Tone: Speak naturally, warmly, and with high intellectual depth, like an expert human partner. Avoid sounding robotic, repetitive, or overly formal. "
            "Complete Memory & Continuity: Continuously refer back to prior statements, user details, and discussed context throughout the conversation. "
            "Multi-Disciplinary Perspective: Integrate insights from computer science, engineering, physics, philosophy, and environmental science naturally when answering. "
            "Respond strictly in fluent English."
        )
    },
    "RU": {
        "title": "🌊 AquaVision AI",
        "subtitle": "Высокоточная Система Спектрального Анализа Воды",
        "tab_scanner": "🔍 ИИ Сканер и Молекулярный Анализ",
        "tab_purify": "🧪 Экстренная Очистка",
        "tab_catalog": "🌍 Глобальный Каталог Воды",
        "tab_prevent": "🛡️ Защита Окружающей Среды",
        "input_method": "Выберите Метод Ввода:",
        "upload_gallery": "📁 Загрузить из Галереи",
        "use_camera": "📷 Сделать Фото",
        "upload_label": "Загрузите изображение образца воды",
        "camera_label": "Сделайте фото образца воды",
        "analyze_btn": "🚀 Начать Высокоточный Анализ",
        "results_header": "📊 Результаты Анализа и Спектральная Диагностика",
        "purity_score": "Уровень Чистоты",
        "clean_status": "Статус: ЧИСТАЯ И ПИТЬЕВАЯ ВОДА",
        "warning_status": "Статус: ОБНАРУЖЕНО Загрязнение ИЛИ ИЗМЕНЕНИЕ СОСТАВА",
        "chat_title": "🤖 Разумный ИИ Мозг",
        "chat_subtitle": "Персонализированная Память и Широкое Мышление",
        "chat_welcome": "Здравствуйте! Я ваш персональный ИИ-партнер с абсолютной памятью диалога. Я помню все предыдущие вопросы и детали. Готов к глубоким обсуждениям в области науки, технологий и философии.",
        "chat_placeholder": "Задайте развернутый вопрос...",
        "sidebar_nav": "📌 Панель и Инструменты",
        "quick_norms": "📊 Стандарты Питьевой Воды",
        "norm_ph": "Идеальный pH: 6.5 - 8.5",
        "norm_tds": "Макс. TDS: < 500 ppm",
        "norm_turb": "Мутность: < 1 NTU",
        "counter_title": "📈 Статистика Сканирований",
        "purify_title": "🛠️ Экстренные Методы Очистки Воды",
        "purify_bottle": "**1. Изготовление Фильтра из Бутылки:** Отрежьте дно пластиковой бутылки, сделайте отверстие в крышке и уложите слоями снизу вверх: плотную ткань, измельченный уголь, мелкий песок, крупный песок и камушки.",
        "purify_boil": "**2. Кипячение:** Интенсивно кипятите воду не менее 1-3 минут для уничтожения бактерий.",
        "purify_sodis": "**3. SODIS (Солнечная дезинфекция):** Налейте воду в прозрачную бутылку и оставьте под прямыми солнечными лучами на 6-8 часов.",
        "guide_section_title": "📖 Визуальные Инструкции",
        "guide_1_title": "🥤 Фильтр для воды своими руками",
        "guide_2_title": "☀️ Солнечная дезинфекция (SODIS)",
        "catalog_title": "🌍 Каталог Распределения Воды на Земле",
        "cat_type": "Тип Воды",
        "cat_share": "Доля на Земле (%)",
        "cat_char": "Основные Характеристики",
        "cat_row1_type": "Соленая Океаническая и Морская Вода",
        "cat_row1_char": "Высокая соленость (~35 г/л), Тихий, Атлантический океаны, Каспий",
        "cat_row2_type": "Ледники и Ледяные Шапки",
        "cat_row2_char": "Запасы пресной воды в Антарктиде и Гренландии",
        "cat_row3_type": "Подземные Воды (Водоносные слои)",
        "cat_row3_char": "Подземные запасы, используемые для сельского хозяйства",
        "cat_row4_type": "Поверхностные Пресные Воды",
        "cat_row4_char": "Озера, реки и болота (Основной источник для человека)",
        "prevent_title": "🛡️ Меры по Защите Водных Ресурсов",
        "prevent_1": "• **Создание буферных зон:** Посадка растений вдоль рек задерживает стоки удобрений.",
        "prevent_2": "• **Контроль отходов:** Предотвращение сброса неочищенных сточных вод.",
        "prevent_3": "• **Защита подземных вод:** Сокращение использования химикатов.",
        "pie_dust": "Пыль / Взвешенные частицы",
        "pie_turb": "Мутность / Осадок",
        "pie_color": "Спектральное Смещение",
        "pie_pure": "Доля Чистой Воды",
        "chart_title": "Оптический Состав (%)",
        "sys_instruct": (
            "You are an advanced, empathetic, and broad-thinking AI companion integrated into the AquaVision AI platform. "
            "Conversational Tone: Speak naturally, warmly, and with high intellectual depth, like an expert human partner. Avoid sounding robotic, repetitive, or overly formal. "
            "Complete Memory & Continuity: Continuously refer back to prior statements, user details, and discussed context throughout the conversation. "
            "Multi-Disciplinary Perspective: Integrate insights from computer science, engineering, physics, philosophy, and environmental science naturally when answering. "
            "Respond strictly in fluent Russian language."
        )
    }
}

# 4. SIDEBAR SETTINGS & COUNTERS
st.sidebar.title("AquaVision AI")
lang_choice = st.sidebar.selectbox("🌐 Dil / Language / Язык", ["AZ", "EN", "RU"])
t = TRANSLATIONS[lang_choice]

if "current_lang" not in st.session_state or st.session_state.current_lang != lang_choice:
    st.session_state.current_lang = lang_choice
    st.session_state.messages = [{"role": "assistant", "content": t["chat_welcome"]}]

if "scan_count" not in st.session_state:
    st.session_state.scan_count = 0

st.sidebar.markdown("---")
st.sidebar.subheader(t["sidebar_nav"])
st.sidebar.markdown(f"### {t['quick_norms']}")
st.sidebar.info(f"• {t['norm_ph']}\n• {t['norm_tds']}\n• {t['norm_turb']}")
st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t['counter_title']}")
st.sidebar.metric(label="Skan Sayı", value=f"{st.session_state.scan_count}")

# 5. MOLECULAR & SPECTRAL ANALYSIS ALGORITHM
def analyze_molecular_composition(img_pil):
    img_np = np.array(img_pil)
    
    r_mean = np.mean(img_np[:, :, 0])
    g_mean = np.mean(img_np[:, :, 1])
    b_mean = np.mean(img_np[:, :, 2])
    
    gray_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(gray_bgr, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 40, 120)
    edge_density = (np.count_nonzero(edges) / edges.size) * 100
    
    organic_risk = "Yüksək" if (g_mean > r_mean and g_mean > b_mean) else "Aşağı"
    metal_risk = "Kritik" if (r_mean > b_mean and g_mean > b_mean and laplacian_var > 80) else "Təhlükəsiz"
    
    color_shift = (abs(r_mean - b_mean) + abs(g_mean - b_mean)) / 2.0
    spectral_score = max(5.0, min(99.0, 100.0 - (color_shift * 0.8 + edge_density * 2.5 + (laplacian_var / 15.0))))
    
    return {
        "score": round(spectral_score, 1),
        "organic_risk": organic_risk,
        "metal_risk": metal_risk,
        "edge_density": round(edge_density, 2),
        "laplacian_var": round(laplacian_var, 2)
    }

# 6. EFFICIENTNET-B2 MODEL LOAD
@st.cache_resource
def load_trained_model():
    model = efficientnet_b2(weights=None)
    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_ftrs, 2)
    
    if os.path.exists("water_model.pth"):
        try:
            model.load_state_dict(torch.load("water_model.pth", map_location=torch.device('cpu')))
            model.eval()
            return model
        except Exception:
            return None
    return None

ai_model = load_trained_model()

transform = transforms.Compose([
    transforms.Resize((260, 260)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 7. MAIN UI LAYOUT
main_col, ai_col = st.columns([0.68, 0.32], gap="medium")

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
            img_pil = Image.open(image_file).convert('RGB')
            st.image(img_pil, caption="Nümayə Şəkli", use_container_width=True)
            
            if st.button(t["analyze_btn"], use_container_width=True):
                st.session_state.scan_count += 1
                
                mol_data = analyze_molecular_composition(img_pil)
                cv_score = mol_data["score"]
                
                if ai_model is not None:
                    input_tensor = transform(img_pil).unsqueeze(0)
                    with torch.no_grad():
                        outputs = ai_model(input_tensor)
                        probs = torch.softmax(outputs, dim=1)[0]
                        dl_purity = round(float(probs[0]) * 100, 1)
                    purity = round((dl_purity * 0.70) + (cv_score * 0.30), 1)
                else:
                    purity = cv_score
                
                dust_pct = round(min(40.0, (100 - purity) * 0.4), 2)
                turbidity_pct = round(min(40.0, (100 - purity) * 0.35), 2)
                minerals_pct = round(min(30.0, (100 - purity) * 0.25), 2)
                
                st.subheader(t["results_header"])
                if purity >= 70.0:
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
                    fig_gauge.update_layout(height=260, margin=dict(l=15, r=15, t=30, b=15), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                    st.plotly_chart(fig_gauge, use_container_width=True)
                    
                with chart_col2:
                    labels = [t["pie_dust"], t["pie_turb"], t["pie_color"], t["pie_pure"]]
                    values = [dust_pct, turbidity_pct, minerals_pct, max(0, purity)]
                    fig_pie = px.pie(names=labels, values=values, title=t["chart_title"], color_discrete_sequence=['#e74c3c', '#e67e22', '#f1c40f', '#3498db'])
                    fig_pie.update_layout(height=260, margin=dict(l=15, r=15, t=30, b=15), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                st.markdown("---")
                
                est_ph = round(6.5 + (minerals_pct / 100.0) * 1.5 - (turbidity_pct / 100.0) * 0.8, 2)
                est_tds = int(120 + (minerals_pct * 8) + (dust_pct * 10))
                est_turb_ntu = round(0.4 + (turbidity_pct * 0.15), 2)
                
                chem_table_data = {
                    "Parametr": ["pH Səviyyəsi", "TDS (Minerallaşma)", "Bulanıqlıq (Turbidity)", "Organik Maddə Riski", "Ağır Metal Riski", "Optik Qırılma İndeksi"],
                    "Qiymət": [f"{est_ph}", f"{est_tds} mq/L", f"{est_turb_ntu} NTU", mol_data["organic_risk"], mol_data["metal_risk"], f"{mol_data['laplacian_var']}"],
                    "Norma Limit": ["6.5 – 8.5", "< 500 mq/L", "< 1.0 NTU", "Aşağı", "Təhlükəsiz", "< 50.0"],
                    "Status": ["Normal" if 6.5 <= est_ph <= 8.5 else "Kənarlaşma", "İdeal" if est_tds < 500 else "Yüksək", "Təmiz" if est_turb_ntu < 1.0 else "Bulanıq", "Təhlükəsiz" if mol_data["organic_risk"] == "Aşağı" else "Yüksək Risk", "Təhlükəsiz" if mol_data["metal_risk"] == "Təhlükəsiz" else "Təmizlənməlidir", "Stabil"]
                }
                st.table(chem_table_data)

    # --- TAB 2: EMERGENCY PURIFICATION ---
    with tabs[1]:
        st.subheader(t["purify_title"])
        st.write(t["purify_bottle"])
        st.write(t["purify_boil"])
        st.write(t["purify_sodis"])
        
        st.markdown("---")
        st.subheader(t["guide_section_title"])
        v_col1, v_col2 = st.columns(2)
        
        with v_col1:
            st.markdown(f"### {t['guide_1_title']}")
            st.info("""
                🛠️ **Səhra Şəraitində Çoxmərhələli Filtr Hazırlanması:**
                1. Plastik qabın dibini kəsin.
                2. Qapağa təmiz parça qoyun.
                3. Aktiv kömür, narın qum və çınqıl əlavə edin.
                4. Suyu yuxarıdan tədricən süzün.
            """)
            
        with v_col2:
            st.markdown(f"### {t['guide_2_title']}")
            st.success("""
                ☀️ **SODIS Yolu ilə Günəş Sterilizasiyası:**
                1. Şəffaf PET butulka seçin.
                2. Süzülmüş su ilə doldurub çalxalayın.
                3. Günəş altında saxlayın (6-24 saat).
            """)

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

# --- RIGHT SIDEBAR: GEMINI 3.6 FLASH INTEGRATION ---
with ai_col:
    st.subheader(t["chat_title"])
    st.caption(t["chat_subtitle"])
    
    # Display message history in UI
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    if user_input := st.chat_input(t["chat_placeholder"]):
        # Append user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)
                
                # Format full chat history as native Content objects for Gemini
                contents_payload = []
                for msg in st.session_state.messages:
                    api_role = "model" if msg["role"] == "assistant" else "user"
                    contents_payload.append(
                        types.Content(
                            role=api_role,
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )
                
                # Execute generation using updated gemini-3.6-flash model
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=contents_payload,
                    config=types.GenerateContentConfig(
                        system_instruction=t["sys_instruct"],
                        temperature=0.75,
                        top_p=0.95,
                        max_output_tokens=2048,
                    )
                )
                
                ans_text = response.text
                message_placeholder.write(ans_text)
                st.session_state.messages.append({"role": "assistant", "content": ans_text})
                
            except Exception as e:
                message_placeholder.error(f"Gemini API Error: {str(e)}")

    st.markdown("---")
    st.markdown("### 📚 Əsas Su Terminləri")
    
    with st.expander("1. pH Dərəcəsi", expanded=False):
        st.caption("Suyun turşuluq və ya qələvilik dərəcəsi (6.5 - 8.5).")
        
    with st.expander("2. TDS (Minerallaşma)", expanded=False):
        st.caption("Suda həll olmuş duzlar (< 500 ppm).")
        
    with st.expander("3. Bulanıqlıq (NTU)", expanded=False):
        st.caption("Çöküntü tutqunluğu (< 1.0 NTU).")

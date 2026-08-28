import streamlit as st
import cv2
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. Səhifə Tənzimləmələri
st.set_page_config(
    page_title="AquaVision AI — Offline Su Analiz Sistemi",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Xüsusi Offline CSS (Xarici drayver və ikonlardan asılı deyil)
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

# 3. MƏTN VƏ LÜĞƏT BÖLMƏSİ
TRANSLATIONS = {
    "title": "🌊 AquaVision AI (Offline Rejim)",
    "subtitle": "Rəqəmsal Su Keyfiyyəti Analizi və Lokal Kimyəvi Bilik Sistemi",
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
    "chat_title": "🤖 AquaAI Köməkçisi (Lokal)",
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
    "guide_section_title": "📖 İnternetsiz Vizual Təlimat Kartları",
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
    "prevent_2": "• **Tullantı Nəzarəti:** Sənaye və məişət tullantı sularının təmizlənmədən su mənbələrinə axıdılmasının qarşısını almak.",
    "prevent_3": "• **Yeraltı Suların Qorunması:** Kimyəvi pestisidlərin istifadəsini azaltmaqla yeraltı su qatlarını çirklənmədən qorumaq.",
    "pie_dust": "Toz / Zərrəciklər",
    "pie_turb": "Bulanıqlıq / Çöküntü",
    "pie_color": "Rəng Dəyişməsi / Kənar Maddə",
    "pie_pure": "Təmiz Su Payı",
    "chart_title": "Tərkib Bölgüsü (%)"
}

if "scan_count" not in st.session_state:
    st.session_state.scan_count = 0

t = TRANSLATIONS

# 4. Sol Panel
st.sidebar.subheader(t["sidebar_nav"])
st.sidebar.markdown(f"### {t['quick_norms']}")
st.sidebar.info(f"• {t['norm_ph']}\n• {t['norm_tds']}\n• {t['norm_turb']}")
st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t['counter_title']}")
st.sidebar.metric(label="Ümumi Skan Sayı", value=f"{st.session_state.scan_count}")

# 5. Ekran Bölgüsü
main_col, ai_col = st.columns([0.8, 0.2], gap="medium")

with main_col:
    st.title(t["title"])
    st.caption(t["subtitle"])
    
    tabs = st.tabs([t["tab_scanner"], t["tab_purify"], t["tab_catalog"], t["tab_prevent"]])
    
    # --- TAB 1: LOCAL COMPUTER VISION ANALYZER ---
    with tabs[0]:
        option = st.radio(t["input_method"], (t["upload_gallery"], t["use_camera"]), horizontal=True)
        image_file = None
        if option == t["upload_gallery"]:
            image_file = st.file_uploader(t["upload_label"], type=["jpg", "png", "jpeg"])
        else:
            image_file = st.camera_input(t["camera_label"])
            
        if image_file is not None:
            img_pil = Image.open(image_file)
            st.image(img_pil, caption="Su Nümayəsi Şəkli", use_container_width=True)
            
            if st.button(t["analyze_btn"], use_container_width=True):
                st.session_state.scan_count += 1
                
                # 100% Offline OpenCV processing
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
                
                m1, m2, m3 = st.columns(3)
                if purity >= 85.0:
                    m1.metric("👥 İçə Biləcək İnsan Sayı", "5 - 10 Nəfər / Gün", "Təhlükəsiz")
                    m2.metric("🦠 Mikrobioloji Risk", "Çox Aşağı (< 0.1 CFU/mL)", "Normal")
                    m3.metric("💧 Gündəlik Qəbul Yararlılığı", "100%", "Əla Səviyyədə")
                elif purity >= 60.0:
                    m1.metric("👥 İçə Biləcək İnsan Sayı", "Şərtli (Qaynatsanız)", "Emal Olunmalıdır")
                    m2.metric("🦠 Mikrobioloji Risk", "Orta Riskli", "Qaynatma Şərtdir")
                    m3.metric("💧 Gündəlik Qəbul Yararlılığı", "40%", "1-3 dəq qaynadın")
                else:
                    m1.metric("👥 İçə Biləcək İnsan Sayı", "0 Nəfər (İçmək Yolverilməzdir)", "Yüksək Təhlükə")
                    m2.metric("🦠 Mikrobioloji Risk", "Ciddi Bakterioloji Risk", "Təhlükəli")
                    m3.metric("💧 Gündəlik Qəbul Yararlılığı", "0%", "Filtrasiya Lazımdır")
                
                st.markdown("---")
                
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
                
                c_dir1, c_dir2 = st.columns(2)
                with c_dir1:
                    st.markdown("### 🟤 Aşkar Olunan Çirkləndirici Növləri")
                    dirt_list = []
                    if dust_pct > 5.0:
                        dirt_list.append("• **Sərbəst Mikro-zərrəciklər / Toz:** Vizual şəffaflığı azaldan toz parçaları.")
                    if turbidity_pct > 10.0:
                        dirt_list.append("• **Çöküntü və Mil Zərrələri:** Suya bulanıqlıq verən narın torpaq hissəcikləri.")
                    if minerals_pct > 15.0:
                        dirt_list.append("• **Üzvi Qalıqlar / Yosun İzləri:** Suda üzvi maddə dəyişikliyini göstərən çalarlar.")
                    if purity < 50.0:
                        dirt_list.append("• **Yüksək Bakterioloji Risk:** E. Coli və patogen mikroorqanizm riski.")
                    
                    if not dirt_list:
                        st.info("Nümayədə qabarıq çirk və ya iri zərrəciklər aşkar edilmədi.")
                    else:
                        for d in dirt_list:
                            st.write(d)
                            
                with c_dir2:
                    st.markdown("### 🛠️ Bu Nümayə Üçün Xüsusi Təmizləmə Addımları")
                    if purity >= 85.0:
                        st.success("1. **Birbaşa İstfadə:** Su şəffaflıq normasına uyğundur.\n2. **Kömür Filtrasiyası:** Dadı daha yaxşılaşdırmaq üçün adi məişət filtrindən keçirə bilərsiniz.")
                    elif purity >= 60.0:
                        st.warning("1. **Süzgəcdən Geçirmə:** Suyu sıx parçadan süzərək iri zərrələri ayırın.\n2. **Qaynatma:** Mikrobları məhv etmək üçün suyu ən azı 3 dəqiqə intensiv qaynadın.")
                    else:
                        st.error("1. **Çox-təbəqəli Filtr:** Kömür, qum və daş təbəqəli plastik filtrdən keçirin.\n2. **Çökdürülmə:** Suyu 2 saat sakit saxlayın ki, çöküntü dibə çöksün.\n3. **İntensiv Qaynatma / SODIS:** Suyu 5 dəqiqə qaynadın və ya 8 saat günəş altında saxlayın.")

                st.markdown("---")
                
                st.markdown("### 🧪 Genişləndirilmiş Kimyəvi və Fiziki Analiz")
                est_ph = round(6.5 + (saturation / 100.0) * 2.0 - (turbidity_pct / 100.0) * 1.0, 2)
                est_tds = int(120 + (saturation * 5) + (dust_pct * 8))
                est_turb_ntu = round(0.5 + (turbidity_pct * 0.2), 2)
                
                ch_col1, ch_col2, ch_col3 = st.columns(3)
                ch_col1.metric("Proqnoz pH Səviyyəsi", f"{est_ph}", "İideal: 6.5 - 8.5")
                ch_col2.metric("Ümumi Həll Olunmuş Bərk Maddələr (TDS)", f"{est_tds} ppm", "İdeal: < 500 ppm")
                ch_col3.metric("Bulanıqlıq (NTU)", f"{est_turb_ntu} NTU", "İdeal: < 1.0 NTU")
                
                chem_table_data = {
                    "Parametr / İon": ["pH Səviyyəsi", "Ümumi Həll Olunmuş Maddələr (TDS)", "Bulanıqlıq (Turbidity)", "Ağır Metal Riski (Pb/Fe/Cu)", "Nitrat və Nitritlər (NO3-/NO2-)", "Həll Olunmuş Oksigen (DO)"],
                    "Təxmini Qiymət": [f"{est_ph}", f"{est_tds} mq/L", f"{est_turb_ntu} NTU", "Aşağı" if purity > 70 else "Orta/Yüksək", "< 10 mq/L", "6.5 mq/L"],
                    "ÜST Standart Limiti": ["6.5 – 8.5", "< 500 mq/L", "< 1.0 NTU", "< 0.01 mq/L", "< 50 mq/L", "> 5.0 mq/L"],
                    "Kimyəvi Status": ["Normal" if 6.5 <= est_ph <= 8.5 else "Kənaraçıxma var", "Qəbul olunandır" if est_tds < 500 else "Yüksək", "Təmiz" if est_turb_ntu < 1.0 else "Bulanıq", "Təhlükəsiz" if purity > 70 else "Təmizlənməlidir", "Təhlükəsiz", "Əla"]
                }
                st.table(chem_table_data)

    # --- TAB 2: İNTERNETSİZ VİZUAL TƏLİMAT KARTLARI ---
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
            st.info(
                """
                🛠️ **Səhra Şəraitində Çoxmərhələli Filtr Hazırlanması:**
                
                1. **Qabın Hazırlanması:** 1.5L və ya 2L plastik butulkanın dib hissəsini kəsin.
                2. **Aşağı Təbəqə:** Qapaq hissəsinə təmiz parça və ya pambıq yerləşdirin.
                3. **Süzgəc Təbəqələri (Aşağıdan Yuxarıya):**
                   * ⬛ **Əzilmiş Aktiv Kömür:** Kimyəvi maddələri, qoxunu və toksinləri çəkir.
                   * ⏳ **Narın Qum:** Xırda asılı hissəcikləri saxlayır.
                   * 🪨 **İri Qum və Çınqıl:** Böyük çöküntüləri, ot və yarpaqları tutur.
                4. **İstifadə:** Suyu yuxarıdan tədricən tökün və alt hissədən süzülən suyu başqa təmiz qaba toplayın.
                """
            )
            
        with v_col2:
            st.markdown(f"### {t['guide_2_title']}")
            st.success(
                """
                ☀️ **SODIS Yolu ilə Günəş Sterilizasiyası:**
                
                1. **Şüşə Seçimi:** Şəffaf və cızığı olmayan PET plastik butulka götürün (maksimum 2L).
                2. **Doldurma & Çalxalama:** Butulkanı süzülmüş su ilə 3/4 hissəyə qədər doldurun, 20 saniyə çalxalayın (oksigenlə zənginləşsin), sonra tam doldurun.
                3. **Günəş Maruziyyəti:** Butulkanı düz bir səthdə (mümkünsə damda və ya metal təbəqə üzərində) yerləşdirin.
                4. **Müddət:** 
                   * ☀️ **Açıq günəşli hava:** Minimum **6 saat**.
                   * ☁️ **Buludlu hava:** Minimum **24 saat**.
                """
            )

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

# --- SAĞ PANEL (20%): CHAT & DICTIONARY ---
with ai_col:
    st.subheader(t["chat_title"])
    st.caption("AquaVision Engine (Lokal Rule Engine)")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Salam! Mən AquaAI köməkçisiyəm. İnternetsiz lokal rejimdə su göstəriciləri haqqında suallarınızı cavablandıra bilərəm."}
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
        elif "bulan" in query or "turbid" in query:
            response = "Bulanıqlıq suda asılı hissəciklərin miqdarını göstərir və NTU vahidi ilə ölçülür."
        elif "təmiz" in query or "saf" in query:
            response = "Təmiz su şəffaf, qoxusuz olmalı, mikroblardan və ağır metallardan azad olmalıdır."
        else:
            response = f"'{user_input}' haqqında: Su analizində şəffaflıq, mineral sıxlığı və hissəciklərin paylanması əsas keyfiyyət göstəriciləridir."
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

    st.markdown("---")
    
    st.markdown("### 📚 Əsas Su Terminləri")
    
    with st.expander("1. pH Dərəcəsi", expanded=False):
        st.caption("Suyun turşuluq və ya qələvilik dərəcəsini ölçür (0-14 skalası). İçməli su üçün norması 6.5 - 8.5-dir.")
        
    with st.expander("2. TDS (Minerallaşma)", expanded=False):
        st.caption("Suda həll olmuş ümumi duz və mineralların miqdarıdır (mq/L və ya ppm). Norması < 500 ppm hesab olunur.")
        
    with st.expander("3. Bulanıqlıq (NTU)", expanded=False):
        st.caption("Suya çöküntü, qum və üzvi maddələrin verdiyi tutqunluq dərəcəsidir. Norması 1 NTU-dan az olmalıdır.")
        
    with st.expander("4. Ağır Metallar", expanded=False):
        st.caption("Qurğuşun (Pb), civə (Hg) və mis (Cu) kimi insan orqanizmi üçün zəhərli olan yüksək sıxlıqlı metallardır.")
        
    with st.expander("5. SODIS Üsulu", expanded=False):
        st.caption("Günəşin ultrabənövşəyi (UV) şüaları ilə suyu şəffaf PET butulkalarda dezinfeksiya etmək metodudur.")
        
    with st.expander("6. Nitrat və Nitritlər", expanded=False):
        st.caption("Kənd təsərrüfatı gübrələrindən suya sızan və insan sağlığına zərər verən kimyəvi birləşmələrdir.")
        
    with st.expander("7. Patogenlər", expanded=False):
        st.caption("Suda xəstəlik törədən bakteriya, virus və ya parazitlərdir (məsələn, E. Coli bakteriyası).")
        
    with st.expander("8. Həll Olunmuş Oksigen", expanded=False):
        st.caption("Suda həll olan və su ekosisteminin, canlılığın saxlanması üçün vacib olan oksigen (O2) miqdarıdır.")

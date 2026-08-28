import streamlit as st

# Səhifə konfiqurasiyası
st.set_page_config(
    page_title="AquaVision AI",
    page_icon="💧",
    layout="wide"
)

# Tərcümə və mətn lüğəti (Azərbaycan dili üzrə)
t = {
    "title": "💧 AquaVision AI - Su Keyfiyyəti və Analiz Sistemi",
    "tab1_title": "📊 Su Analizi & Modul",
    "tab2_title": "🧪 Fövqəladə Təmizləmə Təlimatları",
    "purify_title": "🚨 Fövqəladə Halda Suyun Təmizlənməsi Üsulları",
    "purify_bottle": "💧 **1. Qablaşdırılmış / Çökdürmə Üsulu:** Suyu sakit bir qabda saxlayaraq iri hissəciklərin dibə çökməsini gözləyin.",
    "purify_boil": "🔥 **2. Qaynatma Üsulu:** Suyu ən azı 1-3 dəqiqə gur odda qaynatmaq mikrobların və bakteriyaların 99.9%-ni məhv edir.",
    "purify_sodis": "☀️ **3. SODIS (Günəş Dezinfeksiyası):** Şəffaf plastik butulkanı su ilə doldurub günəş şüası altında saxlayın.",
    "video_section_title": "📺 İnternetsiz Əlaltı Təlimat Kartları",
    "video_1_title": "🥤 Əlaltı Vasitələrlə Su Filtrinin Hazırlanması",
    "video_2_title": "☀️ Günəş Enerjisi ilə Su Dezinfeksiyası (SODIS)"
}

# Başlıq
st.title(t["title"])

# Tablar
tabs = st.tabs([t["tab1_title"], t["tab2_title"]])

# --- TAB 1: Su Analizi ---
with tabs[0]:
    st.subheader("Su Keyfiyyətinin Analizi")
    st.write("Bu bölmədə su göstəricilərini daxil edərək analiz apara bilərsiniz.")
    # Burada model və ya göstərici daxil etmə formanız yerləşir.

# --- TAB 2: Fövqəladə Təmizləmə & İnternetsiz Təlimatlar ---
with tabs[1]:
    st.subheader(t["purify_title"])
    st.write(t["purify_bottle"])
    st.write(t["purify_boil"])
    st.write(t["purify_sodis"])
    
    st.markdown("---")
    st.subheader(t["video_section_title"])
    
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        st.markdown(f"### {t['video_1_title']}")
        st.info(
            """
            🛠️ **Səhra Şəraitində Filtr Hazırlanması:**
            
            1. **Qabın Hazırlanması:** 1.5L və ya 2L plastik butulkanın dib hissəsini kəsin.
            2. **Aşağı Təbəqə:** Qapaq hissəsinə təmiz parça və ya pambıq yerləşdirin.
            3. **Süzgəc Təbəqələri (Aşağıdan Yuxarıya):**
               * ⬛ **Əzilmiş Aktiv Kömür:** Kimyəvi maddələri və qoxunu çəkir.
               * ⏳ **Narın Qum:** Xırda hissəcikləri saxlayır.
               * 🪨 **İri Qum və Çınqıl:** Böyük çöküntüləri və yarpaqları tutur.
            4. **İstifadə:** Suyu yuxarıdan tədricən tökün və alt hissədən süzülən suyu toplayın.
            """
        )
        
    with v_col2:
        st.markdown(f"### {t['video_2_title']}")
        st.success(
            """
            ☀️ **SODIS Yolu ilə Sterilizasiya:**
            
            1. **Şüşə Seçimi:** Şəffaf və cızığı olmayan PET plastik butulka götürün.
            2. **Doldurma:** Butulkanı süzülmüş su ilə 3/4 hissəyə qədər doldurun, çalxalayın (oksigenlə zənginləşsin), sonra tam doldurun.
            3. **Günəş Maruziyyəti:** Butulkanı düz bir səthdə (mümkünsə damda və ya metal təbəqə üzərində) yerləşdirin.
            4. **Müddət:** 
               * ☀️ **Açıq günəşli hava:** Minimum 6 saat.
               * ☁️ **Buludlu hava:** Minimum 24 saat.
            """
        )

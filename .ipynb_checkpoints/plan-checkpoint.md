### 🚀 PROJE: THE ALGO-RISK MANAGER
**Hedef:** Canlı borsa verisiyle çalışan, portföy stres testi ve risk analizi yapan interaktif bir web uygulaması.

---

### 📅 1. AY: MOTORU KURMAK (Backend & Financial Math)
**Scott Young Prensibi:** *Directness (Direkt Öğrenme)* - Teoriyi kitaptan okuma, veriyi eline alıp kirlet.
**Hedef:** Arayüz yok. Sadece Python kodu, matematik ve veri.

*   **Hafta 1: Veri Boru Hattı (Data Pipeline)**
    *   **Görev:** `yfinance` kütüphanesini kullanarak BIST30 (örn: GARAN.IS, THYAO.IS) ve NASDAQ (AAPL, TSLA) hisselerinin son 3 yıllık kapanış verilerini çeken fonksiyonu yaz.
    *   **Kritik Nokta:** Veri temizliği. Eksik günleri (tatiller) doldur (`fillna`) veya sil (`dropna`).
    *   **Çıktı:** Temiz bir Pandas DataFrame.

*   **Hafta 2: Getiri Hesaplamaları (Log Returns)**
    *   **Görev:** Fiyat verisinden "Günlük Yüzdesel Getiri" ve "Logaritmik Getiri" hesapla.
    *   **Soru:** Neden basit getiri değil de Log Getiri kullanıyoruz? (Bunun cevabını öğren, mülakat sorusudur).
    *   **Çıktı:** Volatiliteyi (Standart sapma) ölçebilen bir script.

*   **Hafta 3-4: Portföy Matematiği (Matrix Operations)**
    *   **Görev:** Kullanıcının seçtiği ağırlıklara göre (Örn: %50 THY, %50 Apple) portföyün beklenen getirisini ve varyansını hesaplayan matris çarpımını kodla.
    *   **Çıktı:** Varyans-Kovaryans matrisi ve tek bir risk skoru.

---

### 📅 2. AY: RİSK MODELLEMESİ (The "Economist" Part)
**Scott Young Prensibi:** *Drill (Zayıf Noktaya Saldırı)* - İşin en zor kısmı olan finansal modellemeyi izole et ve çöz.
**Hedef:** İktisatçı farkını ortaya koymak. Geleceği simüle etmek.

*   **Hafta 1-2: Value at Risk (VaR)**
    *   **Görev:** İki tür VaR hesapla:
        1.  **Parametrik VaR:** Normal dağılım varsayımıyla (Formül bazlı).
        2.  **Tarihsel VaR:** Geçmiş veriye bakarak (Simülasyon yok, geçmişte en kötü ne olmuş?).
    *   **Çıktı:** "Bu portföy yarın %95 ihtimalle en fazla X TL kaybeder" diyen bir fonksiyon.

*   **Hafta 3-4: Monte Carlo Simülasyonu (The Showstopper)**
    *   **Görev:** Geometrik Brownian Hareketi (GBM) formülünü kullanarak hisselerin gelecek 1 yılını 10.000 kere simüle et.
    *   **WebTÜFE Dersi:** WebTÜFE nasıl 1 milyon veriyi işliyorsa, sen de 10.000 senaryoyu hızlıca işleyecek `NumPy` optimizasyonu yap.
    *   **Çıktı:** Geleceğe dair olasılık dağılım grafiği verisi.

---

### 📅 3. AY: ÜRÜNLEŞTİRME & DAĞITIM (Frontend & Deploy)
**Scott Young Prensibi:** *Feedback (Geri Bildirim)* - Ürünü insanların (ve İK müdürlerinin) önüne koy.
**Hedef:** Kodlarını insanların tıklayabileceği bir web sitesine dönüştürmek.

*   **Hafta 1: Arayüz Tasarımı (Streamlit UI)**
    *   **Görev:** `Streamlit` kütüphanesini kur. Sol tarafa (Sidebar) hisse seçimi (Dropdown) ve ağırlık ayarı (Slider) koy.
    *   **Çıktı:** Sayfayı açınca hisseleri seçip "Hesapla" butonuna basılabilen bir arayüz.

*   **Hafta 2: Görselleştirme (Plotly)**
    *   **Görev:** Monte Carlo sonuçlarını statik resim olarak değil, üzerine gelince değer gösteren `Plotly` grafikleriyle çiz. (WebTÜFE grafikleri gibi interaktif olsun).
    *   **Çıktı:** Zoom yapılabilen, üzerine gelince detay gösteren profesyonel grafikler.

*   **Hafta 3-4: Canlıya Alma (Deployment)**
    *   **Görev:** Kodlarını GitHub'a yükle. Streamlit Cloud'a bağla ve "Deploy" et.
    *   **Final Çıktısı:** `algorisk-manager.streamlit.app` linki.

---

### 🏁 İLK GÖREVİN (START)

Google Tasks'e eklediğimiz şu görevle başlıyorsun:
> *"Jupyter Notebook aç, `yfinance` ile Apple ve THY hisselerinin kapanış verilerini çeken ve ekrana basan ilk scripti yaz."*

Hazır mısın?
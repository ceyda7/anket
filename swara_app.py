import streamlit as st
import pandas as pd
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="SWARA Anketi", layout="centered")

st.title("\U0001F4CB SWARA Temelli Kriter Önceliklendirme Anketi")

# --- Kriter Listesi ---
kriterler = [
    "Temizlik",
    "İyi İletişim ve Bilgilendirme",
    "Uygun Fiyatlandırma",
    "Randevu Kolaylığı",
    "Sorunun Çözüme Ulaştırılması",
    "Müşteriye Yönelik Özenli ve İlgili Hizmet",
    "İkame Araç Temini",
    "Hızlı Servis Süresi",
    "Uzman Personel",
    "Hizmet Kalitesi ve Teknik İşçilik",
    "Yedek Parçaların Hızlı Temini",
    "Güvenlik",
    "Temiz ve Düzenli Servis Alanı",
    "Garanti ve Servis Sonrası Destek"
]

st.header("1. Kriterleri Öncelik Sırasına Göre Sürükleyerek Sıralayın")
st.markdown("Yukarıdan aşağıya en önemli olandan en az önemli olana doğru sıralayınız. Her satırın yerini değiştirerek sıralama yapabilirsiniz.")

# Data editor ile sıralama
siralama_df = pd.DataFrame({"Kriter": kriterler})
siralama_df = st.data_editor(siralama_df, num_rows="fixed", use_container_width=True)

ranked = siralama_df["Kriter"].tolist()

if len(set(ranked)) < 14:
    st.warning("Tüm sıralamalar farklı olmalıdır. Aynı kriter birden fazla kez yazılamaz.")
    st.stop()

st.success("Sıralama tamamlandı!")
st.dataframe(pd.DataFrame({"Sıra": list(range(1, 15)), "Kriter": ranked}))

# --- Karşılaştırmalar ---
st.header("2. Karşılaştırmalı Önem Değerlendirmesi")
st.markdown("Her bir üst sıradaki kriterin alt sıradakine göre ne kadar daha önemli olduğunu seçiniz.")

scale_labels = {
    1: "Eşit Önemde",
    2: "Biraz Daha Önemli",
    3: "Önemli",
    4: "Çok Daha Önemli",
    5: "Aşırı Derecede Önemli"
}

comparisons = []
for i in range(13):
    label = f"{ranked[i]} → {ranked[i+1]}"
    value = st.slider(label, 1, 5, 3, format="%d")
    comparisons.append({"Üst Kriter": ranked[i], "Alt Kriter": ranked[i+1], "Önem Derecesi": value, "Açıklama": scale_labels[value]})

comp_df = pd.DataFrame(comparisons)
st.dataframe(comp_df)

# --- Google Sheets'e veri gönder ---
if st.button("Gönder ve Kaydet"):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)

        sheet = client.open("SWARA Anket Sonuçları").sheet1
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for row in comparisons:
            sheet.append_row([timestamp, row['Üst Kriter'], row['Alt Kriter'], row['Önem Derecesi'], row['Açıklama']])

        st.success("Veriler Google Sheets'e başarıyla gönderildi. Teşekkür ederiz!")
    except Exception as e:
        st.error(f"Veri gönderilirken bir hata oluştu: {e}")

# Not: Katılımcıya CSV indirme kaldırıldı
st.info("Sonuçlar anket sahibine otomatik olarak iletilmektedir. SWARA hesaplama modülü bir sonraki aşamada entegre edilecektir.")

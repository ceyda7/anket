
import streamlit as st
import pandas as pd

st.set_page_config(page_title="SWARA Anketi", layout="centered")

st.title("📋 SWARA Temelli Kriter Önceliklendirme Anketi")

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

st.header("1. Kriterleri Öncelik Sırasına Göre Giriniz")
st.markdown("En önemli olanı 1. sıraya, en az önemli olanı 14. sıraya yerleştiriniz.")

ranked = []
cols = st.columns(2)

with cols[0]:
    for i in range(7):
        choice = st.selectbox(f"{i+1}. Sıra", kriterler, key=f"r{i}")
        ranked.append(choice)
with cols[1]:
    for i in range(7, 14):
        choice = st.selectbox(f"{i+1}. Sıra", kriterler, key=f"r{i}")
        ranked.append(choice)

if len(set(ranked)) < 14:
    st.warning("Tüm sıralamalar farklı olmalıdır. Aynı kriter birden fazla seçilemez.")
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

# --- Dışa Aktarma ---
st.download_button("💾 Sonuçları CSV Olarak İndir", comp_df.to_csv(index=False).encode('utf-8'), "swarasonuclari.csv", "text/csv")

st.info("SWARA hesaplama modülü bir sonraki aşamada entegre edilecektir.")

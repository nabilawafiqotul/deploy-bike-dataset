import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pyngrok import ngrok

# Set judul aplikasi
st.title("Dashboard Penyewaan Sepeda")

@st.cache_data
def load_data():
    file_path = 'day.csv'  # Path file CSV
    return pd.read_csv(file_path)

# Load dataset
data = load_data()

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Overview", "Analisis Pengguna", "Visualisasi"])

if page == "Overview":
    st.header("Deskripsi Dataset")
    st.write(data.describe())
    st.write("Sample Data:")
    st.dataframe(data.head())

elif page == "Analisis Pengguna":
    st.header("Analisis Pengguna Sepeda")
    cnt_by_day_type = data.groupby('workingday')['cnt'].sum().reset_index()
    cnt_by_day_type['day_type'] = cnt_by_day_type['workingday'].replace({1: "Weekday", 0: "Weekend"})
    st.subheader("Jumlah Pengguna Sepeda: Weekday vs Weekend")
    st.bar_chart(cnt_by_day_type[['day_type', 'cnt']].set_index('day_type'))

    data['season_label'] = data['season'].replace({
        1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"
    })
    cnt_by_season = data.groupby('season_label')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=cnt_by_season, x='season_label', y='cnt', palette='coolwarm', ax=ax)
    ax.set_title("Jumlah Pengguna Sepeda per Musim")
    ax.set_ylabel("Jumlah Pengguna")
    st.pyplot(fig)

elif page == "Visualisasi":
    st.header("Korelasi Variabel")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    st.subheader("Distribusi Pengguna Berdasarkan Waktu")
    hour_group = data.groupby('hr')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=hour_group, x='hr', y='cnt', ax=ax)
    ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Rata-rata Penyewaan")
    st.pyplot(fig)

else:
    st.info("Silakan unggah dataset untuk memulai.")

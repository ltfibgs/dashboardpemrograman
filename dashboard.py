import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import nbformat
from nbconvert import HTMLExporter
import os

# Title
st.title('Bike Sharing Data Analysis Dashboard')

# Sidebar menu
st.sidebar.title("Menu")
menu = st.sidebar.radio("Navigate", ["Dashboard", "About Us", "More Code"])

# About Us section
if menu == "About Us":
    st.header("About Us")
    st.write("""
    - Kelompok : 3
    - Anggota :
        - 10123158 - Kaisar Ihsaan Ibrahim
        - 10123166 - Raka Setya Pramudya
        - 10123152 - Tierry Henry Hasiholan
        - 10123147 - Muhammad Lutfi Bagaskara Yodi
        - 10123155 - Firgip Budiarto
    """)

# More Code section
elif menu == "More Code":
    st.header("More Code")
    uploaded_file = st.file_uploader("Upload TugasKelompokFinal.ipynb Untuk Menampilkan Semua Code", type="ipynb")
    if uploaded_file is not None:
        with open("TugasKelompokFinal.ipynb", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.write("File uploaded successfully. Displaying the content of the Jupyter Notebook below.")
        notebook_content = uploaded_file.read()
        notebook = nbformat.reads(notebook_content, as_version=4)
        html_exporter = HTMLExporter()
        (body, resources) = html_exporter.from_notebook_node(notebook)
        st.components.v1.html(body, height=800, scrolling=True)
    elif os.path.exists("TugasKelompokFinal.ipynb"):
        with open("TugasKelompokFinal.ipynb", "r") as f:
            notebook_content = f.read()
        notebook = nbformat.reads(notebook_content, as_version=4)
        html_exporter = HTMLExporter()
        (body, resources) = html_exporter.from_notebook_node(notebook)
        st.components.v1.html(body, height=800, scrolling=True)

# Dashboard section
else:
    # File uploader for CSV files
    day_file = st.file_uploader("Upload day.csv", type="csv")
    hour_file = st.file_uploader("Upload hour.csv", type="csv")

    if day_file is not None:
        with open("day.csv", "wb") as f:
            f.write(day_file.getbuffer())
    if hour_file is not None:
        with open("hour.csv", "wb") as f:
            f.write(hour_file.getbuffer())

    if os.path.exists("day.csv") and os.path.exists("hour.csv"):
        day_data = pd.read_csv("day.csv")
        hour_data = pd.read_csv("hour.csv")

        # Ensure 'dteday' column is present in hour_data
        if 'dteday' not in hour_data.columns:
            hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])

        # Section 1: Season with the highest bike rentals
        st.header('Season with the Highest Bike Rentals')
        seasonal_rental_counts = day_data.groupby('season')['cnt'].mean()
        highest_season = max(seasonal_rental_counts)
        highest_index = seasonal_rental_counts.idxmax() + 0
        st.write(f"Season tertinggi adalah season ke {highest_index} dengan nilai {highest_season}")

        fig, ax = plt.subplots()
        ax.bar(seasonal_rental_counts.index, seasonal_rental_counts.values, color='blue')
        ax.set_title("Rata-rata Sewa Sepeda Berdasarkan Musim")
        ax.set_ylabel("Rata-rata Sewa (cnt)")
        ax.set_xlabel("Musim")
        ax.set_xticks(seasonal_rental_counts.index)
        ax.set_xticklabels([1, 2, 3, 4])
        ax.axhline(y=highest_season, color='red', linestyle='--', label='---------')
        ax.legend()
        st.pyplot(fig)

        # Section 2: Bike rentals on working days vs non-working days
        st.header('Bike Rentals: Working Days vs Non-Working Days')
        workingday_usage = day_data.groupby('workingday')['cnt'].mean()
        labels = ['Non-Working Day', 'Working Day']

        fig, ax = plt.subplots()
        ax.bar(labels, workingday_usage.values, color=['red', 'blue'])
        ax.set_title("Rata-rata Penggunaan Sepeda: Hari Kerja vs Non-Hari Kerja")
        ax.set_ylabel("Rata-rata Penggunaan (cnt)")
        ax.set_xlabel("Tipe Hari")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)

        st.write(f"Rata-rata penggunaan sepeda pada hari kerja: {workingday_usage[1]:.2f}")
        st.write(f"Rata-rata penggunaan sepeda pada hari non-kerja: {workingday_usage[0]:.2f}")

        # Section 3: Bike rentals on holidays vs non-holidays (per hour)
        st.header('Bike Rentals: Holidays vs Non-Holidays (Per Hour)')
        holiday_usage = hour_data.groupby('holiday')['cnt'].mean()
        labels = ['Non Holiday', 'Holiday']

        fig, ax = plt.subplots()
        ax.bar(labels, holiday_usage.values, color=['green', 'cyan'])
        ax.set_title("Rata-rata Penggunaan Sepeda: Hari Libur vs Hari Biasa")
        ax.set_ylabel("Rata-rata Penggunaan (cnt)")
        ax.set_xlabel("Per Jam")
        ax.grid(axis='y', linestyle='--', alpha=0.7, color='red')
        st.pyplot(fig)

        st.write(f"Rata-rata penggunaan sepeda pada hari libur (per jam): {holiday_usage[1]:.2f}")
        st.write(f"Rata-rata penggunaan sepeda pada hari biasa (per jam): {holiday_usage[0]:.2f}")

        # Section 4: Correlation between weather factors and bike rentals
        st.header('Correlation between Weather Factors and Bike Rentals')
        relevant_columns = ['hr', 'temp', 'hum', 'windspeed', 'cnt']
        data = hour_data[relevant_columns]
        correlation_matrix = data.corr()

        fig, ax = plt.subplots()
        cax = ax.matshow(correlation_matrix, cmap='coolwarm')
        fig.colorbar(cax)
        ticks = np.arange(0, len(correlation_matrix.columns), 1)
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.set_xticklabels(correlation_matrix.columns, rotation=90)
        ax.set_yticklabels(correlation_matrix.columns)
        ax.set_title('Korelasi Antar Variabel Numerik', pad=20)
        st.pyplot(fig)

        # Section 5: Monthly and hourly bike rentals
        st.header('Monthly and Hourly Bike Rentals')
        # Ensure 'dteday' column is present in hour_data
        if 'dteday' not in hour_data.columns:
            hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
        data['datetime'] = pd.to_datetime(hour_data['dteday'])
        data['month'] = data['datetime'].dt.month
        data['hour'] = data['datetime'].dt.hour

        monthly_rentals = data.groupby('month')['cnt'].sum()
        fig, ax = plt.subplots()
        monthly_rentals.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_title('Penyewaan Sepeda per Bulan')
        ax.set_xlabel('Bulan')
        ax.set_ylabel('Jumlah Penyewaan')
        ax.set_xticks(monthly_rentals.index)
        ax.set_xticklabels(monthly_rentals.index, rotation=0)
        st.pyplot(fig)

        hourly_rentals = data.groupby('hour')['cnt'].mean()
        fig, ax = plt.subplots()
        hourly_rentals.plot(kind='bar', color='orange', ax=ax)
        ax.set_title('Rata-rata Penyewaan Sepeda per Jam')
        ax.set_xlabel('Jam')
        ax.set_ylabel('Rata-rata Penyewaan')
        ax.set_xticks(hourly_rentals.index)
        ax.set_xticklabels(hourly_rentals.index, rotation=0)
        st.pyplot(fig)

        # Conclusion
        st.header('Conclusion')
        st.write(f"Season tertinggi adalah season ke {highest_index} dengan nilai {highest_season}")
        st.write(f"Rata-rata penggunaan sepeda pada hari kerja: {workingday_usage[1]:.2f}")
        st.write(f"Rata-rata penggunaan sepeda pada hari non-kerja: {workingday_usage[0]:.2f}")
        st.write(f"Rata-rata penggunaan sepeda pada hari libur (per jam): {holiday_usage[1]:.2f}")
        st.write(f"Rata-rata penggunaan sepeda pada hari biasa (per jam): {holiday_usage[0]:.2f}")
        st.write(f"Jumlah total penyewaan sepeda per bulan: {monthly_rentals.sum()}")
        st.write(f"Jumlah penyewaan tertinggi terjadi pada bulan: {monthly_rentals.idxmax()} dengan jumlah penyewaan: {monthly_rentals.max()}")
        st.write(f"Rata-rata penyewaan sepeda per jam: {hourly_rentals.mean():.2f}")
        st.write(f"Jam dengan penyewaan tertinggi adalah jam: {hourly_rentals.idxmax()} dengan rata-rata penyewaan: {hourly_rentals.max()}")
    else:
        st.write("Upload file day.csv dan hour.csv Untuk Menampilkan Pertanyaan dan Jawaban dari Analisis Data Kedua Tersebut.")

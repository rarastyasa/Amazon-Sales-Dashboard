# Amazon Sales Dashboard 📊

**Amazon Sales Dashboard** adalah aplikasi interaktif berbasis **Streamlit** untuk menganalisis data penjualan Amazon di India selama periode **April – Juni 2022**. Aplikasi ini membantu pengguna memahami performa penjualan berdasarkan kategori produk, metode pemenuhan, tren penjualan bulanan dan harian, serta kontribusi kota-kota utama.

---

## 🚀 Fitur Utama

- Menampilkan **KPI** utama: Total Sales, Total Orders, Total Quantity
- Analisis **Total Orders dan Total Sales per Kategori Produk**
- Visualisasi **Tren Penjualan Bulanan dan Harian**
- Analisis **Sales by Fulfillment** dan **Ship Service Level**
- Visualisasi **Top 10 Sales berdasarkan Ship-City**
- Menampilkan **contoh dataset** di dashboard
- Filter interaktif berdasarkan **tanggal** dan **kategori produk**

---

## 🛠️ Instalasi dan Persiapan

1. Clone repository ini:

```bash
git clone https://github.com/username/amazon-sales-dashboard.git
cd amazon-sales-dashboard
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```
---

## 🚀 Menjalankan Aplikasi
```bash
python -m streamlit run app.py
```
Buka browser dan akses http://localhost:8501 untuk melihat dashboard.

---
## 📊 Struktur Dashboard

Dashboard ini terdiri dari beberapa bagian untuk memudahkan analisis data penjualan Amazon:

1. **KPI Overview**  
   Menampilkan metrik utama: Total Sales, Total Orders, dan Total Quantity.
2. **Total Order by Category**  
   Bar chart yang menunjukkan jumlah order per kategori produk.
3. **Total Sales by Category**  
   Bar chart yang menunjukkan total penjualan per kategori produk.
4. **Monthly Sales Trend**  
   Visualisasi tren penjualan bulanan untuk melihat pola penjualan selama periode tertentu.
5. **Daily Sales Trend**  
   Visualisasi tren penjualan harian untuk melihat fluktuasi penjualan dalam satu bulan.
6. **Sales by Fulfillment & Ship Service Level**  
   Pie chart yang menampilkan distribusi metode fulfillment dan jenis layanan pengiriman yang dipilih pelanggan.
7. **Top 10 Sales by Ship-City**  
   Bar chart yang menunjukkan 10 kota dengan kontribusi penjualan terbesar.
8. **Dataset Example**  
   Menampilkan contoh data yang digunakan dalam analisis untuk referensi.

---

## 📂 Data Source

Dataset yang digunakan dalam dashboard ini diambil dari:

**[Kaggle Amazon Sales Report](https://www.kaggle.com/datasets/arpit2712/amazonsalesreport)**

---

## 💻 Teknologi

Dashboard ini dibangun menggunakan teknologi berikut:

- **Python 3.12** – Bahasa pemrograman utama.  
- **Streamlit** – Framework untuk membuat aplikasi web interaktif.  
- **Pandas** – Library untuk manipulasi dan analisis data.  
- **Altair** – Library untuk membuat visualisasi interaktif.  
---

## 🔗 Live Demo

Lihat langsung dashboard di Streamlit: [Amazon Sales Dashboard](https://amazon-sales-dashboard-2022.streamlit.app/)

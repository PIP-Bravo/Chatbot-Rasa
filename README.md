# 🤖 Chatbot RASA – SOP Fakultas Sains dan Matematika UNDIP

Project ini merupakan implementasi chatbot berbasis **Rasa Open Source Framework** untuk menjawab pertanyaan seputar Standar Operasional Prosedur (SOP) Fakultas Sains dan Matematika Universitas Diponegoro.

Chatbot ini dibangun menggunakan:

- Rasa NLU (Intent Classification & Entity Extraction)
- Rasa Core (Dialogue Management)

Studi kasus dan sumber data yang digunakan berasal dari dokumen resmi SOP Fakultas Sains dan Matematika Universitas Diponegoro.

---

# 📦 A. Panduan Instalasi Project ke Lokal

## 1️⃣ Clone Repository

1. Klik tombol **Code** pada halaman repository GitHub
2. Copy link HTTPS repository
3. Buka **VS Code**
4. Buka folder lokasi penyimpanan project
5. Buka terminal baru lalu jalankan:

```bash
git clone https://github.com/PIP-Bravo/Chatbot-Rasa.git
```

6. Masuk ke folder project:

```bash
cd Chatbot-Rasa
```

Jika berhasil, seluruh file project akan terunduh ke komputer lokal.

---

# 🐍 B. Membuat Virtual Environment

Disarankan menggunakan environment terpisah agar tidak mengganggu instalasi Python utama.

## 1️⃣ Buat Virtual Environment (Conda)

```bash
conda create -n rasa_fsm_env python==3.8.18
```

> Disarankan menggunakan Python 3.8.18   untuk kompatibilitas Rasa.

## 2️⃣ Aktifkan Environment

```bash
conda activate rasa_fsm_env
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Tunggu hingga seluruh dependency berhasil terinstall.

Jika tidak ada error, berarti instalasi berhasil.

---

# 🚀 C. Inisialisasi & Menjalankan Project RASA

Untuk dapat membuat project Rasa, jalankan:

```bash
rasa init
```

Pilih opsi default (Yes) saat diminta. Tunggu sampai semua file yang dibutuhkan dalam project Rasa muncul pada working directory. Perintah ini akan membuat struktur project standar Rasa.

---

# ⚠️ PENTING – Replace File Setelah `rasa init`

Setelah menjalankan `rasa init`, beberapa file bawaan Rasa harus diganti dengan file yang sudah disiapkan pada folder:

```
replace_some_data_with_this/
```

File yang perlu direplace:

- `data/nlu.yml`
- `data/stories.yml`
- `data/rules.yml`
- `domain.yml`
- `config.yml`
- `endpoints.yml`

Langkahnya:

1. Masuk ke folder `replace_some_data_with_this`
2. Copy seluruh file di dalamnya
3. Paste dan replace ke root project Rasa yang sudah dibuat oleh `rasa init`

Tujuan langkah ini adalah agar:

- Intent yang sudah dibuat langsung digunakan
- Stories dan rules yang telah disesuaikan dengan SOP FSM UNDIP aktif
- Konfigurasi pipeline dan policy sesuai dengan desain project ini

Jika langkah ini tidak dilakukan, maka chatbot akan menggunakan data default bawaan Rasa.

---

## 1️⃣ Train Model

Sebelum menjalankan chatbot, lakukan training:

```bash
rasa train
```

Model hasil training akan tersimpan pada folder `models/`.

---

## 2️⃣ Jalankan Chatbot

Untuk menjalankan chatbot dalam mode interaktif:

```bash
rasa shell
```

---

# 🧠 Knowledge Base yang Digunakan

Dataset intent dan response dibangun berdasarkan dokumen resmi berikut:

- SOP Pengisian IRS  
- SOP Permohonan Izin Aktif Kuliah Setelah Cuti  
- SOP Permohonan Izin Cuti Akademik  
- SOP Permohonan Izin Keterlambatan Pembayaran UKT  
- SOP Legalisir Ijazah dan Transkrip  
- SOP Pengajuan Beasiswa  
- SOP Pengajuan Proposal Kegiatan Organisasi  

Seluruh dokumen tersebut merupakan milik:

**Fakultas Sains dan Matematika  
Universitas Diponegoro**

---

# 📂 Struktur Project RASA

```
Struktur project setelah dilakukan replace:

```
.
Chatbot-Rasa/
│
├── data/
│   ├── nlu.yml
│   ├── rules.yml
│   └── stories.yml
│
├── config.yml
├── domain.yml
├── endpoints.yml
├── custom_tracker_store.py
├── evaluate.py
├── requirements.txt
└── README.md
```

Penjelasan singkat:

- `nlu.yml` → Berisi daftar intent dan contoh kalimat training
- `stories.yml` → Alur percakapan berbasis skenario
- `rules.yml` → Rule percakapan sederhana
- `domain.yml` → Mendefinisikan intent, entity, response, dan action
- `config.yml` → Pipeline NLU dan policies
- `actions/` → Custom logic (jika digunakan)

---

# 🛠 Teknologi yang Digunakan

- Python 3.8.18
- Rasa Open Source
- YAML Configuration
- Machine Learning Dialogue Policy

---

# 📌 Troubleshooting

Jika terjadi error:

- Pastikan Python versi sesuai (3.8.18)
- Pastikan environment sudah aktif
- Pastikan model sudah ditrain (`rasa train`)

Cek versi Rasa:

```bash
rasa --version
```

---

## 👤 Author

**Alfonso Clement S**

Jika terdapat pertanyaan atau kendala, silakan hubungi melalui:

Email: sutancs42@gmail.com  
GitHub: https://github.com/PIP-Bravo

---

# 🎯 Tujuan Project

Project ini dibuat sebagai implementasi:

- Conversational AI berbasis Rasa Framework
- Intent Classification dan Dialogue Management
- Chatbot berbasis dokumen SOP Fakultas Sains dan Matematika UNDIP

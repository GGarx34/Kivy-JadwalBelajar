# JadwalKita: Aplikasi Jadwal Pelajaran Interaktif

JadwalKita adalah aplikasi desktop sederhana yang dibangun dengan Python dan Kivy untuk membantu siswa dan guru dalam mengelola jadwal pelajaran. Aplikasi ini menyediakan antarmuka yang bersih untuk melihat, menambah, dan mengelola jadwal harian dengan sistem peran pengguna yang berbeda.

## Fitur Utama

* **Sistem Login Berbasis Peran**: Aplikasi memiliki dua peran pengguna:
    * [cite_start]**Guru**: Dapat melihat, menambah, mengedit, dan menghapus jadwal[cite: 26, 39, 66, 67, 68].
    * [cite_start]**Siswa**: Hanya dapat melihat jadwal yang sudah ada[cite: 25, 27, 39, 66].

* **Tampilan Jadwal Harian**:
    * [cite_start]Jadwal ditampilkan per hari dari Senin hingga Minggu[cite: 22, 60].
    * [cite_start]Widget untuk hari ini ("HARI INI") akan disorot secara otomatis[cite: 24, 60].
    * [cite_start]Setiap hari dapat diperluas atau diciutkan untuk menampilkan atau menyembunyikan detail jadwal[cite: 27].

* **Manajemen Jadwal (Khusus Guru)**:
    * [cite_start]Menambah entri jadwal baru dengan kategori "Mata Pelajaran", "Ekstrakurikuler", atau "Lainnya"[cite: 44, 45, 46, 47, 63].
    * [cite_start]Mengedit detail jadwal yang ada seperti aktivitas, ruang, dan waktu[cite: 68].
    * [cite_start]Menghapus entri jadwal dari daftar[cite: 67].

* [cite_start]**Pembaruan Data Otomatis**: Aplikasi secara otomatis akan memuat ulang jadwal jika mendeteksi ada perubahan pada file `data.json`, memungkinkan pembaruan data antar pengguna tanpa perlu me-restart aplikasi[cite: 52, 53].

## Masalah yang Diketahui (Known Issues)

1.  **Fungsi Edit Tidak Berfungsi**: Fitur untuk "EDIT" jadwal saat ini **rusak**. Aplikasi mencoba mengakses elemen antarmuka dari popup sebelum elemen tersebut selesai dibuat, sehingga data jadwal yang ada gagal dimuat ke dalam form edit.
2.  **Gulir Otomatis Tidak Reliabel**: Terdapat fitur untuk menggulir otomatis ke hari ini saat aplikasi pertama kali dibuka. Namun, fitur ini mungkin tidak selalu berfungsi karena masalah waktu (timing) dalam proses render antarmuka pengguna.

## Teknologi

* **Bahasa Pemrograman**: Python
* [cite_start]**Framework**: Kivy [cite: 73]
* **Format Data**: JSON

## Instalasi

Pastikan Anda memiliki Python versi 3.6 atau yang lebih baru terpasang di sistem Anda.

1.  **Unduh atau Kloning Repositori**
    Dapatkan semua file proyek (`app.py`, `jadwalKita.kv`, `requirements.txt`, dan direktori `assets`) dan letakkan dalam satu folder.

2.  **Buat Lingkungan Virtual (Direkomendasikan)**
    Buka terminal atau command prompt, navigasikan ke folder proyek, dan jalankan perintah:
    ```bash
    python -m venv venv
    ```
    Aktifkan lingkungan virtual:
    * **Windows:** `.\venv\Scripts\activate`
    * **macOS & Linux:** `source venv/bin/activate`

3.  **Instal Ketergantungan**
    Instal semua library yang dibutuhkan menggunakan file `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Menjalankan Aplikasi

Setelah instalasi selesai, jalankan aplikasi dari terminal di dalam folder proyek:

```bash
python app.py
```

## Kredensial Login Demo
**Anda dapat menggunakan akun bawaan berikut untuk masuk:**

  # Akun Guru:
        Username: guru#
        Password: cukuptau
        
  # Akun Siswa:
        Username: siswa
        Password: belajar

# Sistem Presensi Berbasis Face Recognition
Proyek ini merupakan sebuah sistem presensi yang menggunakan konsep _face recognition_. Sistem ini menangkap wajah pegawai sebagai bukti kehadiran.

Proyek ini bertujuan untuk mengembangkan sistem _Face Recognition_ yang akan terintegrasi dengan sistem presensi yang sudah ada, sehingga memungkinkan pencatatan kehadiran pegawai secara otomatis saat wajah mereka terdeteksi.

<div id="tabel-konten">
    <h2> Tabel konten </h2>
    <ul>
        <li>
            <a href="#Instalasi">Panduan Instalasi</a>
        </li>
        <li>
            <a href="#Penggunaan">Panduan Pengguaan</a>
        </li>
        <li>
            <a href="#Model">Pembangunan Model</a>
        </li>
    </ul>
</div>

<div id="Instalasi">
    <h2>
        <a href="#tabel-konten">Panduan Instalasi</a>
    </h2>
</div>

Hal yang perlu dipersiapkan:

1. Python versi 3.10 ke atas. [Cara Memasang Python](https://wiki.python.org/moin/BeginnersGuide/Download)
2. Library tambahan, pasang dengan cara mengetik perintah `pip install -r requirements.txt` di terminal di mana direktori file `requirements.txt` berada
3. Basis data MySQL versi 8, _import_ basis data dari direktori `db`
4. Untuk menggunakan basis data, bisa menggunakan XAMPP atau Laragon atau WAMP


<div id="Penggunaan">
    <h2>
        <a href="#tabel-konten">Panduan Penggunaan</a>
    </h2>
</div>

1. Buka terminal
2. Jalankan perintah `python app.py`
3. Jika aplikasi sudah ada tulisan _Running on http://127.0.0.1:5000_, buka browser dan akses `http://localhost:5000` atau `http://127.0.0.1:5000`
4. Klik tombol presensi untuk menangkap foto presensi
5. Setelah menekan tombol presensi, maka presensi berhasil dilakukan dengan menampilkan identitas pegawai serta bukti foto

![](./img/Screenshot%202024-05-28%20191149.png)

6. Proses presensi berhasil dilakukan dan presensi bisa dilakukan kembali dengan menekan tombol `Presensi Ulang`
7. Untuk menghentikan program, kembali ke terminal dan tekan tombol `CTRL + C`

### Menambahkan Data Pegawai Baru
1. Ketika program berjalan, klik `Pegawai Baru` di browser
2. Masukan data sesuai dengan kebutuhan yang tertera
3. Jika semua sudah terisi, klik `Submit Pegawai Baru` untuk menambahkan data pegawai tersebut ke basis data dan model secara otomatis akan dibangun ulang dengan data baru tersebut. Tunggu beberapa saat hingga model selesai dibangun
4. Jika sudah selesai, maka akan tampil pesan `Model Berhasil Diproses`. Klik `Halaman Presensi` untuk memulai presensi kembali


<div id="Model">
    <h2>
        <a href="#tabel-konten">Pembangunan Model</a>
    </h2>
</div>

Pada sistem ini, model _face recognition_ dibangun menggunakan model _deep learning Convolutional Neural Network_ (CNN). Kode program dapat diakses [di sini](https://github.com/HijazP/sistem-absensi-berbasis-face-recognition/blob/master/model/Face%20Recognition%20Using%20CNN.ipynb). 

Data yang digunakan berupa gambar 18 orang yang diidentifikasi sebagai pegawai untuk sistem absensi yang sudah ada. Data latih model dapat diakses [di sini](https://github.com/HijazP/sistem-absensi-berbasis-face-recognition/tree/master/model/Face%20Images/Face%20Images/Final%20Training%20Images). 

# Analisis Jaringan Football dan Dolphins

Analisis jaringan nyata memakai NetworkX: ukuran jaringan (derajat, clustering,
path terpendek), homophily dan assortativity, broker struktural (constraint dan
effective size ala Burt), serta eksplorasi jaringan sosial dolphins.

Proyek ini adalah Module 1 dari kursus Network Modeling and Analysis in Python
(University of Michigan).

## Data

Folder `data` berisi tiga jaringan nyata dalam format GML:

* `football1.gml`: 115 tim football kampus Amerika musim 2000, 613 pertandingan.
  Setiap node punya atribut konferensi, jumlah menang, dan jumlah kalah.
* `football2.gml`: jaringan pembanding dengan ukuran yang sama tetapi koneksi
  dibuat acak.
* `dolphins.gml`: 62 lumba lumba di Doubtful Sound, Selandia Baru, 159 relasi
  sosial. Setiap node punya atribut smelliness.

## Yang dikerjakan

1.  Verifikasi jaringan asli: assortativity konferensi `football1` = 0.6275
    (tim sekonferensi cenderung bertanding) sedangkan `football2` = 0.0096
    (acak). Lihat `charts/01_conference_assortativity.png`.
2.  Assortativity derajat = 0.1624 (sedikit assortatif) dan assortativity jumlah
    menang = negatif 0.0498 (sedikit disassortatif, tim kuat tidak khusus melawan tim kuat).
3.  Broker struktural: 6 tim punya constraint di bawah 0.15. Win rate rata rata
    10 broker teratas = 0.4531, 10 terbawah = 0.5326, korelasi constraint dengan
    win rate = 0.0902. Kesimpulan: broker tidak cenderung lebih sering menang.
    Lihat `charts/02_brokers_winrate.png`.
4.  Effective size terendah: WakeForest, Virginia, Clemson.
    Lihat `charts/03_effective_size.png`.
5.  Eksplorasi dolphins: distribusi derajat, distribusi smelliness, dan korelasi
    smelliness dengan derajat = 0.7354. Lihat `charts/04_dolphins_dist.png` dan
    `charts/05_smelliness_degree.png`.

Hasil simulasi survival dolphins dari tugas kursus: persentase survival harian
1.0000, 1.0000, 0.8548, 0.7258, 0.5806 dengan korelasi smelliness terhadap
survival = 0.8641.

## Cara menjalankan

```bash
python analyze_football.py
```

Script ini memuat data, menghitung semua metrik di atas, menyimpan chart ke
folder `charts`, dan menulis ringkasan angka ke `findings.json`.

## Tools

Python, NetworkX, pandas, NumPy, matplotlib.

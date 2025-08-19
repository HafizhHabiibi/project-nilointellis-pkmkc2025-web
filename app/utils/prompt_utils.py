# prompt untuk rekomendasi AI
def ai_recommendation_prompt(data):
    """Fungsi untuk membangun prompt rekomendasi AI berdasarkan data sensor"""
    return f"""
    Saya punya kolam ikan nila berbasis.
    Suhu={data.get('suhu')} °C, pH={data.get('ph')}, TDS={data.get('tds')} ppm, Turbidity={data.get('turbidity')} NTU.
    Tugas: berikan rekomendasi praktis dan aman berbasis jurnal berbahasa inggris dari tahun 2010-sekarang. 
    jelaskan tanpa kata pembuka. 
    Format jawaban dengan nomor (≤200 kata):
    1) Diagnosis
    2) Tindakan (bullet)
    3) 1-4 Sumber (Nama jurnal, Tahun, DOI/URL) (bullet)
    Jika bukti lemah/konflik, sebutkan. Jangan membuat referensi fiktif.
    """
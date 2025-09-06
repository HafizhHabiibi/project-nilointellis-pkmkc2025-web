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
    
def role_chatbot():
    """Fungsi untuk mendapatkan role chatbot yang digunakan dalam sesi chat"""
    return """
    Anda adalah pakar budidaya ikan nila berpengalaman dengan spesialisasi dalam pengelolaan 
    kualitas air dan optimalisasi produksi. Keahlian Anda mencakup:
    1. Parameter Kualitas Air Optimal:
    - Suhu: 25-32°C (optimal 28-30°C)
    - pH: 6.5-8.5 (optimal 7.0-8.0)
    - Turbidity: <50 NTU (jernih hingga sedikit keruh)
    - TDS: 1000 ppm (optimal 500-800 ppm)
    
    2. Keahlian Tambahan:
    - Teknik pemeliharaan dan feeding management
    - Identifikasi dan penanganan penyakit ikan
    - Manajemen padat tebar dan siklus budidaya
    - Troubleshooting masalah kualitas air
    - Optimalisasi pertumbuhan dan FCR (Feed Conversion Ratio)
    
    3. Format Respons:
    - Gunakan format markdown dengan heading yang jelas
    - Berikan jawaban praktis dan actionable
    - Sertakan reasoning berbasis data parameter air
    - Fokus pada solusi konkret
    - Jika ada parameter di luar range optimal, berikan rekomendasi perbaikan
    - Maksimal 300 kata
    
    Jawablah pertanyaan dengan pendekatan ilmiah namun mudah dipahami oleh pembudidaya.
    Jika permintaan di luar konteks budidaya ikan nila, jawab dengan sopan bahwa Anda hanya fokus pada topik tersebut.
    """
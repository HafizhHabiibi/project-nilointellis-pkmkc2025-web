def hitung_statistik(data):
    """Fungsi untuk menghitung statistik (min, max, avg) dari data sensor"""
    if not data:
        return {
            'ph': {'min': 0, 'max': 0, 'avg': 0},
            'suhu': {'min': 0, 'max': 0, 'avg': 0},
            'tds': {'min': 0, 'max': 0, 'avg': 0},
            'turbidity': {'min': 0, 'max': 0, 'avg': 0}
        }
    
    # Ambil nilai per parameter
    ph_values = [item.get('ph') for item in data if item.get('ph') is not None]
    suhu_values = [item.get('suhu') for item in data if item.get('suhu') is not None]
    tds_values = [item.get('tds') for item in data if item.get('tds') is not None]
    turbidity_values = [item.get('turbidity') for item in data if item.get('turbidity') is not None]
    
    def get_stats(values):
        if not values:
            return {'min': 0, 'max': 0, 'avg': 0}
        
        return {
            'min': round(min(values), 2),
            'max': round(max(values), 2),
            'avg': round(sum(values) / len(values), 2)
        }
    
    return {
        'ph': get_stats(ph_values),
        'suhu': get_stats(suhu_values),
        'tds': get_stats(tds_values),
        'turbidity': get_stats(turbidity_values)
    }
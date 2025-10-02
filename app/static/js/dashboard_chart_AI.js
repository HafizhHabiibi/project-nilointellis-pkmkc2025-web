const phMax = document.getElementById('phMax');
const phMin = document.getElementById('phMin');
const phAvg = document.getElementById('phAvg');
const suhuMax = document.getElementById('suhuMax');
const suhuMin = document.getElementById('suhuMin');
const suhuAvg = document.getElementById('suhuAvg');
const tdsMax = document.getElementById('tdsMax');
const tdsMin = document.getElementById('tdsMin');
const tdsAvg = document.getElementById('tdsAvg');
const turbidityMax = document.getElementById('turbidityMax');
const turbidityMin = document.getElementById('turbidityMin');
const turbidityAvg = document.getElementById('turbidityAvg');
let currentStatisticsData = null;
let currentFilterInfo = null;


flatpickr("#tanggalAwal", {
    dateFormat: "d/m/Y",
    disableMobile: "true",
});
flatpickr("#tanggalAkhir", {
    dateFormat: "d/m/Y",
    disableMobile: "true",
});
const granulitas = document.getElementById('granulitas');
const opsi = ['1 menit','5 menit','10 menit', '30 menit', '1 jam', '6 jam', '12 jam', 'hari', 'minggu', 'bulan'];

const dropdownContent = document.createElement('div');
dropdownContent.style.display = 'flex';
dropdownContent.style.flexDirection = 'column';
// dropdownContent.style.color = 'var(--hitam)';
// dropdownContent.style.backgroundColor = 'var(--primary)';

opsi.forEach(option => {
    const item = document.createElement('div');
    item.textContent = option;
    item.style.padding = '1rem 0rem';
    item.style.width = '13rem';
    item.style.cursor = 'pointer';
    item.addEventListener('click', () => {
        granulitas.value = option;
        instance.hide();
        submitForm(); // submit form waktu opsi dipilih
    });
    dropdownContent.appendChild(item);
});

const instance = tippy(granulitas, {
    content: dropdownContent,
    trigger: 'click',
    interactive: true,
    placement: 'bottom-start',
    arrow: false,
    theme: 'light',
});

// jawaban rekomendasi AI
function getAIRecommendation() {
    const modal = new bootstrap.Modal(document.getElementById('aiRecModal'));
    modal.show();

    // tampilkan spinner, kosongkan konten lama
    document.getElementById('aiRecLoading').classList.remove('d-none');
    document.getElementById('aiRecContent').innerHTML = '';

    fetch('/dashboard/get-ai-recommendation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('aiRecLoading').classList.add('d-none');
        if (data.status === 'success') {
            document.getElementById('aiRecContent').innerHTML = data.recommendation;
        } else {
            document.getElementById('aiRecContent').innerHTML =
                `<div class="alert alert-danger">Gagal: ${data.message}</div>`;
        }
    })
    .catch(error => {
        document.getElementById('aiRecLoading').classList.add('d-none');
        document.getElementById('aiRecContent').innerHTML =
            `<div class="alert alert-danger">Error: ${error}</div>`;
    });
}

function submitForm() {
    // document.getElementById('filterForm').submit();

    const form = document.getElementById('filterForm');
    const formData = new FormData(form);

    // simpan info filter saat ini
    currentFilterInfo = {
        tanggal_awal: document.getElementById('tanggalAwal').value,
        tanggal_akhir: document.getElementById('tanggalAkhir').value,
        granulitas: document.getElementById('granulitas').value
    };

    fetch ('/dashboard/filter', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log(data.data);
            currentStatisticsData = data.data; 
            updateStatistiktabel(data.data);
            updateCharts(data.data);
        } else {
            // alert('Tidak ada data ditemukan');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Terjadi kesalahan');
    });
}

// Jawaban analisis AI
function getAIAnalysis() {
    if (!currentStatisticsData || currentStatisticsData.length === 0) {
        showErrorModal('Datanya ga ada brok');
        return;
    }

    // Hitung statistik menggunakan fungsi yang sudah ada
    const stats = hitungStatistik(currentStatisticsData);
    
    // Tampilkan modal analisis
    const modal = new bootstrap.Modal(document.getElementById('aiAnalysisModal'));
    modal.show();

    // Tampilkan loading
    document.getElementById('aiAnalysisLoading').classList.remove('d-none');
    document.getElementById('aiAnalysisContent').innerHTML = '';

    // Kirim data ke backend
    fetch('/dashboard/get-ai-analyst-chart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            statistics: stats,
            filter_info: currentFilterInfo,
            raw_data: currentStatisticsData
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('aiAnalysisLoading').classList.add('d-none');
        if (data.status === 'success') {
            document.getElementById('aiAnalysisContent').innerHTML = data.analysis;
        } else {
            document.getElementById('aiAnalysisContent').innerHTML = 
                `<div class="alert alert-danger">Gagal: ${data.message}</div>`;
        }
    })
    .catch(error => {
        document.getElementById('aiAnalysisLoading').classList.add('d-none');
        document.getElementById('aiAnalysisContent').innerHTML = 
            `<div class="alert alert-danger">Error: ${error}</div>`;
    });
}

// Fungsi untuk menampilkan modal error
function showErrorModal(message) {
    const modal = new bootstrap.Modal(document.getElementById('errorModal'));
    document.getElementById('errorMessage').textContent = message;
    modal.show();
}

function updateStatistiktabel(data){
    const stats = hitungStatistik(data);

    // Update PH statistics
    document.getElementById('phMax').textContent = stats.ph.max;
    document.getElementById('phMin').textContent = stats.ph.min;
    document.getElementById('phAvg').textContent = stats.ph.avg;

    // Update Suhu statistics
    document.getElementById('suhuMax').textContent = stats.suhu.max;
    document.getElementById('suhuMin').textContent = stats.suhu.min;
    document.getElementById('suhuAvg').textContent = stats.suhu.avg;

    // Update TDS statistics
    document.getElementById('tdsMax').textContent = stats.tds.max;
    document.getElementById('tdsMin').textContent = stats.tds.min;
    document.getElementById('tdsAvg').textContent = stats.tds.avg;

    // Update Turbidity statistics
    document.getElementById('turbidityMax').textContent = stats.turbidity.max;
    document.getElementById('turbidityMin').textContent = stats.turbidity.min;
    document.getElementById('turbidityAvg').textContent = stats.turbidity.avg;
}

function hitungStatistik(data){
    if (!data || data.length === 0) {
        return {
            ph: { min: 0, max: 0, avg: 0 },
            suhu: { min: 0, max: 0, avg: 0 },
            tds: { min: 0, max: 0, avg: 0 },
            turbidity: { min: 0, max: 0, avg: 0 }
        };
    }

    // ambil nilai data per jenis nya
    const phValues = data.map(item => item.ph).filter(val => val !== null && val !== undefined);
    const suhuValues = data.map(item => item.suhu).filter(val => val !== null && val !== undefined);
    const tdsValues = data.map(item => item.tds).filter(val => val !== null && val !== undefined);
    const turbidityValues = data.map(item => item.turbidity).filter(val => val !== null && val !== undefined);

    // Helper function to calculate min, max, avg
    function getStats(values) {
        if (values.length === 0) return { min: 0, max: 0, avg: 0 };

        const min = Math.min(...values);
        const max = Math.max(...values);
        const avg = values.reduce((sum, val) => sum + val, 0) / values.length;

        return {
            min: parseFloat(min.toFixed(2)),
            max: parseFloat(max.toFixed(2)),
            avg: parseFloat(avg.toFixed(2))
        };
    }

    return {
        ph: getStats(phValues),
        suhu: getStats(suhuValues),
        tds: getStats(tdsValues),
        turbidity: getStats(turbidityValues)
    };
}

// chart dashboard sections
let phChart, suhuChart, tdsChart, turbidityChart;
const chartConfig = {
    type: "line",
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                enabled: true,
                mode: 'index',
                intersect: false,
            }
        },

        scales: {
        x: {
            display: false,
            title: { display: true, text: "Tanggal/Waktu" }
        },
    },
    },
};

// inisiasi chart
document.addEventListener('DOMContentLoaded', function() {
    const phCtx = document.getElementById('phChart').getContext('2d');
    const suhuCtx = document.getElementById('suhuChart').getContext('2d');
    const tdsCtx = document.getElementById('tdsChart').getContext('2d');
    const turbidityCtx = document.getElementById('turbidityChart').getContext('2d');

    phChart = new Chart(phCtx, {
        ...chartConfig,
        data: {
            labels: [],
            datasets: [{
                label: 'PH',
                data: [],
                borderColor: '#2EC4B6',
                backgroundColor: '#CBF3F0',
                tension: 0.3,
                fill: true,
                pointRadius: 2,
            }]
        }
    });

    suhuChart = new Chart(suhuCtx, {
        ...chartConfig,
        data: {
            labels: [],
            datasets: [{
                label: 'Suhu',
                data: [],
                borderColor: '#FFA630',
                backgroundColor: ' #FECD8D',
                tension: 0.3,
                fill: true,
                pointRadius: 2,
            }]
        }
    });

    tdsChart = new Chart(tdsCtx, {
        ...chartConfig,
        data: {
            labels: [],
            datasets: [{
                label: 'TDS',
                data: [],
                borderColor: '#2EC4B6',
                backgroundColor: '#CBF3F0',
                tension: 0.3,
                fill: true,
                pointRadius: 2,
            }]
        }
    });

    turbidityChart = new Chart(turbidityCtx, {
        ...chartConfig,
        data: {
            labels: [],
            datasets: [{
                label: 'Turbidity',
                data: [],
                borderColor: '#FFA630',
                backgroundColor: ' #FECD8D',
                tension: 0.3,
                fill: true,
                pointRadius: 2,
            }]
        }
    });
});

function updateCharts(data){
    if (!data || data.length === 0) return;

        const labels = data.map(item => {
            if (item.timestamp) {
                const date = new Date(item.timestamp);
                return date.toLocaleString('id-ID', {
                    day: '2-digit', month: '2-digit', year: '2-digit',
                    hour: '2-digit', minute: '2-digit'
                });
            } else if (item.tanggal) {
                return item.tanggal;
            } else {
                return '';
            }
        });

        // Ambil data sensor
        const phData = data.map(item => item.ph);
        const suhuData = data.map(item => item.suhu);
        const tdsData = data.map(item => item.tds);
        const turbidityData = data.map(item => item.turbidity);

        phChart.data.labels = labels;
        phChart.data.datasets[0].data = phData;
        phChart.update();

        suhuChart.data.labels = labels;
        suhuChart.data.datasets[0].data = suhuData;
        suhuChart.update();

        tdsChart.data.labels = labels;
        tdsChart.data.datasets[0].data = tdsData;
        tdsChart.update();

        // Update Turbidity Chart
        turbidityChart.data.labels = labels;
        turbidityChart.data.datasets[0].data = turbidityData;
        turbidityChart.update();
}
let charts = {}; // simpan semua chart instance

document.getElementById("btnPrediksi").addEventListener("click", async () => {
    // Reset tampilan
    document.getElementById("successBox").style.display = "none";
    document.getElementById("errorBox").style.display = "none";
    document.getElementById("loadingBox").style.display = "flex";

    try {
        let res = await fetch("/run_prediksi", { method: "POST" });
        let json = await res.json();

        document.getElementById("loadingBox").style.display = "none";

        if (json.status === "error") {
            document.getElementById("errorBox").innerText = "❌ " + json.message;
            document.getElementById("errorBox").style.display = "block";
            return;
        }

        const labels = json.data.timestamps;
        renderChart("chartPh", labels, json.data.ph, "pH");
        renderChart("chartSuhu", labels, json.data.suhu, "Suhu");
        renderChart("chartTurbidity", labels, json.data.turbidity, "Turbidity");
        renderChart("chartTds", labels, json.data.tds, "TDS");

        document.getElementById("successBox").style.display = "block";
    } catch (err) {
        document.getElementById("loadingBox").style.display = "none";
        document.getElementById("errorBox").innerText = "❌ Gagal melakukan prediksi: " + err;
        document.getElementById("errorBox").style.display = "block";
    }
});

function renderChart(canvasId, labels, data, label) {
    // Hapus chart lama dulu kalau ada
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }
    const ctx = document.getElementById(canvasId).getContext("2d");
    charts[canvasId] = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: "#2EC4B6",
                backgroundColor: "rgba(46, 196, 182, 0.2)",
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { ticks: { autoSkip: true, maxTicksLimit: 10 } },
                y: { beginAtZero: false }
            }
        }
    });
}
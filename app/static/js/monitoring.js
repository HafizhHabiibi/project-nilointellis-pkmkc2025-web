const WS_URL = "{{ ws_url if ws_url is defined else 'ws://127.0.0.1:8000' }}";

const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const placeholder = document.getElementById('placeholder');
const loading = document.getElementById('loading');
const liveCanvas = document.getElementById('liveCanvas');
const liveImg = document.getElementById('liveImg');
const streamState = document.getElementById('streamState');
const deadStatusEl = document.getElementById('deadStatus');
const sickCountEl = document.getElementById('sickCount');
const lastUpdatedEl = document.getElementById('lastUpdated');
const lastUpdatedSickEl = document.getElementById('lastUpdatedSick');

let ws = null;
let waitingForFirstFrame = false;
let firstFrameTimeout = null;

function showPlaceholder() {
  placeholder.style.opacity = 1;
  placeholder.style.pointerEvents = 'auto';
  liveCanvas.style.display = 'none';
  liveImg.style.display = 'none';
  loading.style.display = 'none';
  streamState.innerText = 'Offline';
}

function showLoading() {
  placeholder.style.opacity = 0.35;
  loading.style.display = 'flex';
  liveCanvas.style.display = 'none';
  liveImg.style.display = 'none';
  streamState.innerText = 'Starting...';
}

function showLive() {
  placeholder.style.opacity = 0;
  loading.style.display = 'none';
  liveImg.style.display = 'block';
  liveCanvas.style.display = 'none';
  streamState.innerText = 'Live';
}

async function drawFrame(arraybuffer) {
  try {
    const blob = new Blob([arraybuffer], { type: 'image/jpeg' });
    liveImg.src = URL.createObjectURL(blob);
    setTimeout(() => URL.revokeObjectURL(liveImg.src), 2000);
  } catch (err) {
    console.error('Frame decode error', err);
  }
}

function openWS() {
  if (ws) return;
  ws = new WebSocket(WS_URL);
  ws.binaryType = 'arraybuffer';
  showLoading();
  waitingForFirstFrame = true;

  firstFrameTimeout = setTimeout(() => {
    if (waitingForFirstFrame) {
      showPlaceholder();
      try { ws.close(); } catch(e) {}
      ws = null;
    }
  }, 15000);

  ws.onopen = () => {
    streamState.innerText = 'Connected (waiting frame)';
  };

  ws.onmessage = (evt) => {
    if (typeof evt.data !== 'string') {
      if (waitingForFirstFrame) {
        waitingForFirstFrame = false;
        clearTimeout(firstFrameTimeout);
        showLive();
      }
      drawFrame(evt.data);
    }
  };

  ws.onclose = () => {
    ws = null;
    showPlaceholder();
  };

  ws.onerror = () => {
    try { ws.close(); } catch(e){}
  };
}

function closeWS() {
  if (!ws) return;
  try { ws.close(); } catch(e) {}
  ws = null;
  showPlaceholder();
}

startBtn.addEventListener('click', openWS);
stopBtn.addEventListener('click', () => {
  closeWS();
});

showPlaceholder();

// ------- REFRESH STATUS -------
async function fetchDeadStatus() {
  try {
    const res = await fetch("/api/monitoring/status");
    const data = await res.json();
    deadStatusEl.innerText = (data.status && data.status.toLowerCase() === "ada ikan mati") ? "Ada" : "Tidak Ada";
    lastUpdatedEl.innerText = `Last Updated: ${data.timestamp ?? "-"}`;
    sendDeathAnalysis(data.status, data.timestamp);
  } catch (e) {
    console.error("Fetch dead status error", e);
  }
}

async function fetchSickStatus() {
  try {
    const res = await fetch("/api/monitoring/health");
    const data = await res.json();
    sickCountEl.innerText = data.count_sick ?? '0';
    lastUpdatedSickEl.innerText = `Last Updated: ${data.timestamp ?? "-"}`;
  } catch (e) {
    console.error("Fetch sick status error", e);
  }
}

async function sendDeathAnalysis(status, timestamp) {
  try {
    const res = await fetch("/monitoring/get-death-analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status, timestamp })
    });
    const result = await res.json();

    if (result.status === "success" && result.analysis) {
      document.getElementById("aiOutput").innerHTML = result.analysis;
    } else {
      document.getElementById("aiOutput").innerText = "";
    }
  } catch (e) {
    console.error("Send death analysis error", e);
  }
}

// refresh tiap 15 detik
setInterval(() => {
  fetchDeadStatus();
  fetchSickStatus();
}, 10000);

fetchDeadStatus();
fetchSickStatus();
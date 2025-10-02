let socket;

// inisiasi socket
function initializeSocket(){
    socket = io('/dashboard');
    socket.on('connect', function(){
        console.log('dashboard konek socket cuy');
    })
    socket.on('disconnect', function(){
        console.log('walawe dashboard ga konek socket ');
    })
    socket.on('sensor_update', function(res){
        if (res.type === 'realtime' && res.data) {
            updateRealtimeData(res.data);
        }
    })

}

// update realtime data
function updateRealtimeData(data) {
    document.getElementById('ph_value').textContent = data.ph ? data.ph.toFixed(2) : 'N/A';
    document.getElementById('suhu_value').textContent = data.suhu ? data.suhu.toFixed(1) : 'N/A';
    document.getElementById('tds_value').textContent = data.tds ? data.tds.toFixed(0) : 'N/A';
    document.getElementById('turbidity_value').textContent = data.turbidity ? data.turbidity.toFixed(2) : 'N/A';

}

document.addEventListener('DOMContentLoaded', function() {
    initializeSocket(); // Initialize socket di web page
});
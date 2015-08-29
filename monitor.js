/**
 * loadMonitor
 */
function loadMonitor(){
    $.getJSON("/monitor.json",
        function(data) {
            //console.log('data:', data);
            $('.value', '#cpuUsage').html(data.cpu);
            $('.value', '#cpuCount').html(data.cpu_count);
            $('.value', '#diskFreeSpace').html(data.disk);
            $('.value', '#serverLoad').html(data.load);
            $('.value', '#networkReceived').html(data.network_received);
            $('.value', '#networkSent').html(data.network_sent);
            $('.value', '#freeRam').html(data.ram);
        });
    // refresh every 5 seconds
    setTimeout("loadMonitor()", 5000);
}
loadMonitor();
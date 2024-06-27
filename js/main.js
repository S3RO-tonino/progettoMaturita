function WSConnect(){
    var ws = new WebSocket("ws://192.168.1.155:8765");
    ws.onopen = function(event){
        console.log("Connessione col server eseguita.");
    }
    ws.onerror = function(event) {
        document.getElementById("USensor").innerText = "Nessuna connessione.";
        document.getElementById("MSensor").innerText = "Nessuna connessione.";
        console.error("Errore durante la connessione al WS: ", event);
    };
    ws.onclose = function(event) {
        console.log("WS connessione terminata: ", event);
    };
    return ws;
};

ws = WSConnect();
ws.onmessage = function(event){
    try{
        var data = JSON.parse(event.data);
        console.log(data);

        if(data.ID == "start"){
            document.getElementById("allarmStatusText").innerText = "ON";
            document.getElementById("allarmSwitch").checked = true;
        }

        if(document.getElementById("allarmStatusText").innerText === "ON"){
            if(data.intrusion === true){
                var sensorName = data.name;
                var sensorData = document.getElementById(sensorName);
                sensorData.innerText=("Intrusione rilevata");
                sensorData.style.backgroundColor = "red";
            }

            else if(data.intrusion === false){
                var sensorName = data.name;
                var sensorData = document.getElementById(sensorName);
                sensorData.innerText=("Nessuna intrusione rilevata");
                sensorData.style.backgroundColor = "f2f2f2"
            }
        }
        else if(document.getElementById("allarmStatusText").innerText === "OFF"){
            document.getElementById("USensor").innerText = "Allarme disattivato."
            document.getElementById("MSensor").innerText = "Allarme disattivato."
        }
    }
    catch(e){
        console.error("Errore durante la ricezione dei dati: ", e);
    }
};

function allarmButton() {
    const checkbox = document.getElementById("allarmSwitch");
    if (document.getElementById("allarmSwitch").checked){
        document.getElementById("allarmStatusText").innerText = "ON";
    } else{
        document.getElementById("allarmStatusText").innerText = "OFF";
    }
    checkbox.checked = !checkbox.checked;
    console.log("cambiooooo", checkbox.checked);
};

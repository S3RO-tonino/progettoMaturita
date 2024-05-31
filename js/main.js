
function WSConnect() {
    try{
        console.log("Provo a connettermi al WS...")
        var ws = new WebSocket("ws://192.168.1.155:8765/");
        return ws;
    }
    catch (e) {
        console.error("Errore nella connessione al WS: ", e);
        function retryWSConnection() {
            console.log("Riprovando a connettersi al WS...");
            setInterval(WSConnect(), 7000);
        }
        retryWSConnection();
    };
};

ws = WSConnect();
ws.onmessage = function(event) {
    try {
        var data = JSON.parse(event.data);
        console.log(data);

        if(data.ID == "start"){
            document.getElementById("allarmStatusText").innerText = data.status;
        }

        else if(data.ID != "start" && data.ID != "noIntrusion" && data.intrusion == true){
            var sensorName = data.name;
            var sensorsData = document.getElementById("sensorData");

            if (sensorsData.innerText === "ND" || sensorsData.innerText === "Nessuna intrusione rilevata.") {
                sensorsData.innerText=("");
            }

            if(!document.getElementById("sensorData").innerHTML.includes(sensorName)){
                var newSensor = document.createTextNode(sensorName);
                newSensor.innerText = sensorName + "";
                sensorsData.appendChild(newSensor);
            }
        }
        else if(data.ID == "noIntrusion"){
            document.getElementById("sensorData").innerText = "Nessuna intrusione rilevata.";
        }
    }
    catch (e) {
        console.error("Errore nel parsing dei dati JSON: ", e);
    }
};

ws.onerror = function(event) {
    document.getElementById("sensorData").innerText = "Nessuna connessione, riprova.";
    console.error("Errore durante la connessione al WS: ", event);
};

ws.onclose = function(event) {
    console.log("WS connessione terminata: ", event);
};

function allarmButton() {
    if (document.getElementById("allarmSwitch").checked){
        document.getElementById("allarmStatusText").innerText = "ON";
    } else{
        document.getElementById("allarmStatusText").innerText = "OFF";
    }
};

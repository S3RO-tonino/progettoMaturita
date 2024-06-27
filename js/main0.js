function WSConnect() {
    var ws = new WebSocket("ws://192.168.1.155:8765/");
    return ws;
};

function retryWSConnection() {
    console.log("Riprovando a connettersi al WS...");
    WSConnect();
};

ws = WSConnect();
ws.onmessage = function(event) {
    try {
        var data = JSON.parse(event.data);
        console.log(data);

        if(data.ID == "start"){
            if(data.allarmStatus == "ON"){
                document.getElementById("allarmStatusText").innerText = data.allarmStatus;
                document.getElementById("allarmSwitch").check;
            }
            else{
                document.getElementById("allarmStatusText").innerText = data.allarmStatus;
                document.getElementById("allarmSwitch").uncheck;
            }
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

ws.onopen = function(event) {
    console.log("Connessione col WS eseguita.");
};

ws.onerror = function(event) {
    document.getElementById("sensorData").innerText = "Nessuna connessione.";
    console.error("Errore durante la connessione al WS: ", event);
    retryWSConnection();
};

ws.onclose = function(event) {
    console.log("WS connessione terminata: ", event);
    retryWSConnection
};

function allarmButton() {
    if (document.getElementById("allarmSwitch").checked){
        document.getElementById("allarmStatusText").innerText = "ON";
    } else{
        document.getElementById("allarmStatusText").innerText = "OFF";
    }
};

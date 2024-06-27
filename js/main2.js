function WSConnect() {
    var ws;

    try {
                    ws = new WebSocket("ws://192.168.1.155:8765/");

                    ws.onopen = function(event) {
                        statusElement.innerText = "Connessione WebSocket aperta.";
                        errorMessageElement.innerText = "";
                    };

                    ws.onmessage = function(event) {
                        var data = JSON.parse(event.data);
                        console.log("Dati ricevuti:", data);
                    };

                    ws.onerror = function(event) {
                        statusElement.innerText = "Errore durante la connessione al WebSocket.";
                        errorMessageElement.innerText = "Errore generico nella connessione al WebSocket. Tentativo di riconnessione in 10 secondi.";
                        console.error("Errore WebSocket:", event);
                    };

                    ws.onclose = function(event) {
                        statusElement.innerText = "Connessione WebSocket chiusa. Tentativo di riconnessione in 10 secondi.";
                        console.log("WebSocket chiuso:", event);
                        setTimeout(connectWebSocket, reconnectInterval); // Riprova la connessione dopo 10 secondi
                    };

                } catch (e) {
                    statusElement.innerText = "Errore durante la connessione al WebSocket.";
                    errorMessageElement.innerText = "Dettagli dell'errore: " + e.message + ". Tentativo di riconnessione in 10 secondi.";
                    console.error("Eccezione durante la connessione WebSocket:", e);
                    setTimeout(connectWebSocket, reconnectInterval); // Riprova la connessione dopo 10 secondi
                }
};
function allarmButton() {
    if (document.getElementById("allarmSwitch").checked){
        document.getElementById("allarmStatusText").innerText = "ON";
    } else{
        document.getElementById("allarmStatusText").innerText = "OFF";
    }
};

from Flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('intrusione_rilevata')
def handle_intrusion_detected:
    send('Intrusione rilevata')

if __name__ == '__main__':
    socketio.run(app)
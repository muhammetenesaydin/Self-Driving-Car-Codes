import socketio
from flask import Flask
import eventlet

# Socket.IO sunucusunu başlat
sio = socketio.Server()

# Flask uygulamasını başlat
app = Flask(__name__)

# Bağlantı kurulunca çalışacak fonksiyon
@sio.on('connect')
def connect(sid, environ):
    print("Simulator connected!")
    # Simülatör bağlandığında bir mesaj gönder
    sio.emit('message', {'data': 'Hello, Simulator!'}, room=sid)

# Simülatörden gelen telemetry verilerini işle
@sio.on('telemetry')
def telemetry(sid, data):
    print("Telemetry data received:", data)
    # Simülatörden gelen verileri işleyin

# Flask sunucusunu başlat
if __name__ == '__main__':
    print("Starting server...")
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
    print("Server started on port 4567")

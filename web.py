from app import create_app, socketio
from gevent import monkey

monkey.patch_all()

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, port=80)


from flask import Flask
from prometheus_client import make_wsgi_app, Counter
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

requests_total = Counter('http_requests_total', 'Total HTTP Requests')

@app.route('/')
def home():
    requests_total.inc()
    return '<h1>Hello from OpenShift!</h1>'

@app.route('/health')
def health():
    return {'status': 'ok'}

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

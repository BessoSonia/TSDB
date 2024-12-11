from flask import Flask, Response
import psutil
import os
import time
from prometheus_client import Gauge, generate_latest, CollectorRegistry

# Загрузка переменных окружения
EXPORTER_HOST = os.getenv("EXPORTER_HOST", "0.0.0.0")
EXPORTER_PORT = int(os.getenv("EXPORTER_PORT", 8080))
METRICS_UPDATE_INTERVAL = 5

# Настройка Flask и Prometheus
app = Flask(__name__)
registry = CollectorRegistry()

# Метрики
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage in percent', registry=registry)
memory_total = Gauge('memory_total_bytes', 'Total memory in bytes', registry=registry)
memory_used = Gauge('memory_used_bytes', 'Used memory in bytes', registry=registry)
disk_total = Gauge('disk_total_bytes', 'Total disk space in bytes', registry=registry)
disk_used = Gauge('disk_used_bytes', 'Used disk space in bytes', registry=registry)

# Функция для обновления метрик
def update_metrics():
    while True:
        cpu_usage.set(psutil.cpu_percent())
        memory_info = psutil.virtual_memory()
        memory_total.set(memory_info.total)
        memory_used.set(memory_info.used)
        disk_info = psutil.disk_usage('/')
        disk_total.set(disk_info.total)
        disk_used.set(disk_info.used)
        time.sleep(METRICS_UPDATE_INTERVAL)

@app.route('/metrics')
def metrics():
    return Response(generate_latest(registry), mimetype='text/plain')

if __name__ == '__main__':
    from threading import Thread
    metrics_thread = Thread(target=update_metrics)
    metrics_thread.daemon = True
    metrics_thread.start()
    app.run(host=EXPORTER_HOST, port=EXPORTER_PORT)

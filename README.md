# Time seriea база данных Prometheus

###  TSDB используются для сбора метрик, меняющихся по времени, которые могут быть впоследствии использованы для построения графиков, создания предупреждений и анализа тенденций производительности и состояния приложений

1. Клонируйте репозиторий и перейдите в директорию проекта:

    ```bash
    https://github.com/BessoSonia/TSDB
    cd TSDB
    ```

2. Установите зависимости

    ```bash
    pip install -r requirements.txt
    ```

3. Настройте переменные окружения

    - EXPORTER_HOST: Хост, на котором будет работать экспортер (по умолчанию — `0.0.0.0`)
    - EXPORTER_PORT: Порт, на котором будет работать экспортер (по умолчанию — `8080`)

4. Добавьте экспортера в конфигурацию Prometheus

    В файле конфигурации `prometheus.yml` добавьте следующее:
    ```yaml
    scrape_configs:
      - job_name: 'custom_exporter'
        static_configs:
          - targets: ['localhost:8080']  # Укажите адрес экспортера
    ```

    После этого перезапустите Prometheus:
    ```bash
    systemctl restart prometheus
    ```

4. Запустите приложение

    ```bash
    python exporter.py
    ```

5. Запросы PromQL

    Для визуализации и анализа метрик в Prometheus, используйте следующие запросы:

    - Использование процессоров:
        ```promql
        cpu_usage_percent
        ```

    - Использование памяти 
        
        Всего:
        ```promql
        memory_total_bytes
        ```

        Используемая:
        ```promql
        memory_used_bytes
        ```


    - Объем дисков (всего и занятый):

        Всего:
        ```promql
        disk_total_bytes
        ```

        Занято:
        ```promql
        disk_used_bytes
        ```

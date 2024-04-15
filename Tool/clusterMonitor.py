import psutil
import subprocess
from influxdb import InfluxDBClient
import time

class ClusterMonitor:
    def __init__(self, node_id, influxdb_host, influxdb_port, influxdb_username, influxdb_password, influxdb_database):
        self.node_id = node_id
        self.influxdb_host = influxdb_host
        self.influxdb_port = influxdb_port
        self.influxdb_username = influxdb_username
        self.influxdb_password = influxdb_password
        self.influxdb_database = influxdb_database
        self.monitor_interval = 5

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self):
        memory_info = psutil.virtual_memory()
        return memory_info.available

    def ping_node(self, target_ip):
        try:
            result = subprocess.run(['ping', '-c', '1', target_ip], capture_output=True, text=True)
            return "Average" in result.stdout
        except Exception as e:
            print(f"Error while pinging node: {e}")
            return None

    def send_to_influxdb(self, cpu_usage, memory_usage):
        client = InfluxDBClient(host=self.influxdb_host, port=self.influxdb_port,
                                username=self.influxdb_username, password=self.influxdb_password,
                                database=self.influxdb_database)

        json_body = [
            {
                "measurement": "cluster_metrics",
                "tags": {
                    "node_id": self.node_id,
                },
                "fields": {
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory_usage,
                }
            }
        ]

        client.write_points(json_body)

    def monitor_cluster(self):
        while True:
            cpu_usage = self.get_cpu_usage()
            memory_usage = self.get_memory_usage()

            target_ip = 'other_node_ip'
            ping_result = self.ping_node(target_ip)

            self.send_to_influxdb(cpu_usage, memory_usage)

            # 打印消息，模拟实际运行时的输出
            print(f"Node ID: {self.node_id} - CPU Usage: {cpu_usage}% - Memory Available: {memory_usage} MB")
            if ping_result is not None:
                print(f"Ping to {target_ip}: {ping_result}")

            time.sleep(self.monitor_interval)

# 替换以下参数为你实际的配置
node_id = 'edge_node_1'
influxdb_host = 'your_influxdb_host'
influxdb_port = 8086
influxdb_username = 'your_influxdb_username'
influxdb_password = 'your_influxdb_password'
influxdb_database = 'your_influxdb_database'

# 创建 ClusterMonitor 实例
cluster_monitor = ClusterMonitor(node_id, influxdb_host, influxdb_port, influxdb_username, influxdb_password, influxdb_database)

# 启动监控
cluster_monitor.monitor_cluster()

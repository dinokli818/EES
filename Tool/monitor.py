"""Modular providing monitoring in MAPE loop."""
import time
import json
import requests
from flink_rest_client import FlinkRestClient
from Tool.remote_shell import RemoteShell



class FlinkJob:
    """
    Get monitoring metrics from a Flink job.
    """
    def __init__(self, server, job_id) -> None:
        self.server = server
        self.job_id = job_id
        self.rest_api = f"http://{server}:8081/"

    def get_subtask_busy_time(self,operator_id):
        """
        Get busyTimePerSecond from operator_id using REST-API.

        Args:
            operator_id (string): Operator ID

        Returns:
            int: sum busyTimePerSecond
        """
        try:
            response = requests.get(self.rest_api
                                    +f"jobs/{self.job_id}/vertices/{operator_id}/"
                                    +"subtasks/metrics?get=busyTimeMsPerSecond"
                                    ,timeout=5)
            response.raise_for_status()
            job_info = json.loads(response.content)
            busy_times = job_info[0].get("sum", 0.0)
            return busy_times
        except requests.exceptions.RequestException as request_error:
            print("Failed to fetch Flink job info:", request_error)
            return None
   


if __name__ == "__main__":
    SERVER = "192.168.225.16"
    shell = RemoteShell(SERVER, 22, "root", "ftclftcl") #和服务器建立持久sh链接
    rest_client = FlinkRestClient.get(host=SERVER, port=8081)
    shell.execute("ntpdate cn.pool.ntp.org")
    shell.execute("cd /root/dockerComposeFlink/flink && docker compose down")
    shell.execute("cd /root/dockerComposeFlink/flink && docker compose up -d")
    time.sleep(10)
    result = rest_client.overview()
    print(result)
    PATH_TO_MY_JAR = r"D:\WorkSpace\WordCountKafka\target\WordCountKafka-1.0-SNAPSHOT.jar"

    mapPar = 2
    filename = 1
    jars = rest_client.jars.all().get("files")
    if(len(jars)==0):
        rest_client.jars.upload(path_to_jar=PATH_TO_MY_JAR)
    jar_id = rest_client.jars.all().get("files")[0].get("id")
    job_id = rest_client.jars.run(jar_id=jar_id, arguments={
                                                    "mapPar": mapPar,"filename":str(filename)+".csv"
                                                    })
    time.sleep(3000)
    # savepoints_dir = "/tmp/host/"
    # time.sleep(10)
    # response = rest_client.jobs.create_savepoint(job_id,target_directory=savepoints_dir, cancel_job=True)
    # while True:
    #     try:
    #         savepoint = response.status["operation"]["location"][5:]
    #         time.sleep(0.1)
    #     except:
    #         print("none")
    #     else:
    #         break
    # mapPar = 4
    # filename += 1
    # job_id = rest_client.jars.run(jar_id=jar_id, savepoint_path=savepoint,arguments={
    #                                              "mapPar": mapPar,"filename":str(filename)+".csv"
    #                                             }
    #                                 )
    
    # time.sleep(240)
    # job_id = rest_client.jobs.terminate(job_id=job_id)
    shell.execute("docker exec -it $(docker ps --filter name=flink-taskmanager4cpu --format={{.ID}}) bash && cat 1.csv > result.csv")
    shell.execute("docker cp $(docker ps --filter name=flink-taskmanager4cpu --format={{.ID}}):/opt/flink/result.csv /root")
    shell.execute("cd /root/dockerComposeFlink/flink && docker compose down")
    
    #jvc = rest_client.jobs.get_vertex(job_id, job_vertices[2]).subtasks.metric_names()
    #THRESHOLD = 800
    #SCALE = 1
    #while True:
        ##busy_time = rest_client.jobs.get_vertex(job_id, job_vertices[2]).subtasks.metrics(metric_names=["busyTimeMsPerSecond"])
        # if busy_time.get("busyTimeMsPerSecond").get('avg') != 0:
        #     if busy_time > THRESHOLD :
        #         SCALE += 1
        #         cmd = f"cd ./dockerComposeFlink/flink && docker compose up -d --scale taskmanager4cpu={(SCALE)}"
        #         shell.execute(cmd)
        #         print("Scaled up the cluster")
        #         time.sleep(120)
        #     elif busy_time < THRESHOLD :
        #         #scale_cluster(scale_down_factor)
        #         print("Scaled down the cluster")
        #print(busy_time.get("busyTimeMsPerSecond").get('avg'))
        #time.sleep(1)  # 每隔一段时间执行一次循环

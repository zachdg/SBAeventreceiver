import connexion
from connexion import NoContent
import requests
import json
from pykafka import KafkaClient
from datetime import datetime
import yaml

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

client = KafkaClient(hosts="{}:{}".format(app_config['kafka']['server'], app_config['kafka']['port']))
topic = client.topics[app_config['kafka']['topic']]
producer = topic.get_sync_producer()

def rideRequest(requestInfo):
    print(requestInfo)

    msg = { "type": "request",
            "datetime": datetime.now().strftime("%Y-%m-%dT%h: %M: %S"),
            "payload": requestInfo}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    # headers = {
    #     'Content-Type': 'application/json'
    # }
    # r = requests.post('http://localhost:8090/request', data=json.dumps(requestInfo), headers=headers)
    # response = r.status_code

    return NoContent, 201


def rideReport(reportInfo):
    print(reportInfo)

    msg = {"type": "report",
           "datetime": datetime.now().strftime("%Y-%m-%dT%h: %M: %S"),
           "payload": reportInfo}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))


    # headers = {
    #     'Content-Type': 'application/json'
    # }
    # r = requests.post('http://localhost:8090/report', data=json.dumps(reportInfo), headers=headers)
    # response = r.status_code

    return NoContent, 201




app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8080)


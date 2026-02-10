import paho.mqtt.client as mqtt
import json

class MQClient:
    def __init__(self,host,port,client_id,userName,password,houseId,doorId,target):
        self.host=host
        self.port=port
        self.client_id=client_id
        self.userName=userName
        self.password=password
        self.houseId=houseId
        self.doorId=doorId
        self.subscription=f"houses/{houseId}/doors/{doorId}"
        self.target = target
        self.client = None
    
    def start(self):
        self.client = mqtt.Client(client_id=self.client_id, userdata=None, protocol=mqtt.MQTTv5)
        self.client.on_connect = self.on_connect
         # enable TLS for secure connection
        self.client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
        # set username and password
        self.client.username_pw_set(self.userName, self.password)
        # connect to HiveMQ Cloud on port 8883 (default for MQTT)
        self.client.connect(self.host, self.port)
        print(f"host:{self.host,}, client_id:{self.client_id} connected")
        # setting callbacks, use separate functions like above for better visibility
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        # loop_forever for simplicity, here you need to stop the loop manually
        # you can also use loop_start and loop_stop
        self.client.loop_forever()
    
    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)
        # subscribe to all topics of encyclopedia by using the wildcard "#"
        client.subscribe(self.subscription, qos=1)
        print("subscribe:{0}".format(self.subscription))

    def on_subscribe(self,client, userdata, mid, granted_qos, properties=None):
        print("on_subscribe: " + str(mid) + " " + str(granted_qos))

        # print which topic was subscribed to
    def on_disconnect(self,client, userdata, rc):
        print("on_disconnect: " + str(client) + " " + str(userdata))
    
    def on_message(self,client, userdata, msg):
        messageRaw = msg.payload.decode()
        print("on_message:" + messageRaw)
        self.target(data=messageRaw)
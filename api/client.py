import paho.mqtt.client as mqtt

class MQClient:
    def __init__(self,host,port,client_id,userName,password):
        self.host=host
        self.port=port
        self.client_id=client_id
        self.userName=userName
        self.password=password
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
        self.client.on_disconnect = self.on_disconnect
        
    
    def publish(self,houseId,doorId,message):
        
        topic = f"houses/{houseId}/doors/{doorId}"    
        print(f"publish:{topic}:{message}")
        self.client.publish(topic,message);

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)
        
        

        # print which topic was subscribed to
    def on_disconnect(self,client, userdata, rc):
        print("on_disconnect: " + str(client) + " " + str(userdata))

from servo import ServoController
from client import MQClient

controller = ServoController()
controller.start()

def update_gpio(data):
    if(data.lower() in ["open"]):     
        print("abriendo puerta")
        controller.open()
        
    if(data.lower() in ["close"]):
        print("cerrando puerta")
        controller.close()

host="7c9d92b99d8b4d1b92904823717575d5.s1.eu.hivemq.cloud"
port=8883
client_id="mqclientid01"
userName="hivemq.webclient.1750044026669"
password="6&3bSDtT7Va*Yj:c2Fs."
houseId="100"
doorId="1"
cliente = MQClient(host,port,client_id,userName,password,houseId,doorId,update_gpio)

cliente.start()


try:
    while True:
        user_text = input("Tu: ").strip()

        if(not user_text):
            continue

        if(user_text.lower() in ["exit", "quit", "salir"]):
            print("Saliendo...")
            break
except KeyboardInterrupt:
    print("Program stopped")
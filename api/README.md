## Enviroment
```
python -m venv backend_env
source backend_env/bin/activate

pip install "fastapi[standard]"
pip install paho-mqtt
pip freeze > requirements.txt
```

## Iniciar servicio
```
source backend_env/bin/activate
uvicorn main:app --reload   
```

## Comandos
```
curl --request POST \
  --url  http://127.0.0.1:8000/doors  \
  --header 'Content-Type: application/json' \
  --data '{"houseId":"100","doorId":"1","accion":"OPEN"}'

curl --request POST \
  --url  http://127.0.0.1:8000/doors  \
  --header 'Content-Type: application/json' \
  --data '{"houseId":"100","doorId":"1","accion":"CLOSE"}'
```
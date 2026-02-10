
## Instalar Raspberry
```
python -m venv --system-site-packages venv
source venv/bin/activate

sudo apt remove python3-rpi.gpio
pip install rpi-lgpio
pip install paho-mqtt
```

## Ejecutar Raspberry
```
cd /home/admin/Downloads/raspberry
python service.py
```

## Raspberry commands
```
pinctrl -p
```
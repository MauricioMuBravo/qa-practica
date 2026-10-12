"""Receptor: escucha mensajes MQTT, valida y guarda en MySQL."""
import json, os
from datetime import datetime
import paho.mqtt.client as mqtt
import pymysql

BROKER, PUERTO = "localhost", 1883
TOPICO = "medidores/+/lecturas"
CAMPOS = ["medidor_id", "ts", "voltaje", "corriente", "kwh"]

db = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                     password=os.environ["DB_PASSWORD"], database="iot", autocommit=True)

def validar(d):
    for c in CAMPOS:
        if c not in d:
            return f"falta el campo {c}"
    try:
        v, i, k = float(d["voltaje"]), float(d["corriente"]), float(d["kwh"])
        datetime.strptime(d["ts"], "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return "tipo o formato inválido"
    if not (90 <= v <= 150):
        return f"voltaje fuera de rango ({v})"
    if i < 0 or k < 0:
        return "valor negativo"
    return None

def on_message(client, userdata, msg):
    texto = msg.payload.decode(errors="replace")
    with db.cursor() as cur:
        try:
            d = json.loads(texto)
        except json.JSONDecodeError:
            motivo = "JSON inválido"
        else:
            motivo = validar(d) if isinstance(d, dict) else "no es un objeto JSON"
        if motivo:
            cur.execute("INSERT INTO rechazadas (topico, payload, motivo) VALUES (%s,%s,%s)",
                        (msg.topic, texto, motivo))
            print("RECHAZADO:", motivo)
            return
        n = cur.execute(
            "INSERT IGNORE INTO lecturas (medidor_id, ts, voltaje, corriente, kwh) VALUES (%s,%s,%s,%s,%s)",
            (d["medidor_id"], d["ts"], d["voltaje"], d["corriente"], d["kwh"]))
        print("GUARDADO:" if n else "DUPLICADO (ignorado):", d["medidor_id"], d["ts"])

cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.on_message = on_message
cliente.connect(BROKER, PUERTO)
cliente.subscribe(TOPICO)
print("Escuchando en", TOPICO, "(Ctrl+C para salir)")
cliente.loop_forever()

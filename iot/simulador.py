"""Simulador de medidor. Uso: python3 simulador.py --medidor M-001 --n 5 --modo normal|invalido|duplicado"""
import argparse, json, random, time
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt

p = argparse.ArgumentParser()
p.add_argument("--medidor", default="M-001")
p.add_argument("--n", type=int, default=5)
p.add_argument("--modo", choices=["normal", "invalido", "duplicado"], default="normal")
a = p.parse_args()

c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
c.connect("localhost", 1883)
c.loop_start()
topico = f"medidores/{a.medidor}/lecturas"
t0 = datetime.now().replace(microsecond=0)
kwh = 100.0

def enviar(payload):
    texto = payload if isinstance(payload, str) else json.dumps(payload)
    c.publish(topico, texto, qos=1).wait_for_publish()
    print("ENVIADO:", texto)

if a.modo == "invalido":
    ts = t0.strftime("%Y-%m-%d %H:%M:%S")
    enviar({"medidor_id": a.medidor, "ts": ts, "voltaje": 9999, "corriente": 3.2, "kwh": 100})
    enviar({"medidor_id": a.medidor, "ts": ts, "corriente": 3.2, "kwh": 100})
    enviar({"medidor_id": a.medidor, "ts": ts, "voltaje": "abc", "corriente": 3.2, "kwh": 100})
    enviar("esto no es json")
else:
    for i in range(a.n):
        ts = (t0 + timedelta(seconds=i * 10)).strftime("%Y-%m-%d %H:%M:%S")
        kwh += random.uniform(0.01, 0.05)
        msg = {"medidor_id": a.medidor, "ts": ts, "voltaje": round(random.uniform(118, 126), 2),
               "corriente": round(random.uniform(2, 8), 2), "kwh": round(kwh, 3)}
        enviar(msg)
        if a.modo == "duplicado":
            enviar(msg)
        time.sleep(0.5)
c.loop_stop()

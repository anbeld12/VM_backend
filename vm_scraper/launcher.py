import subprocess
import time

# Lista de spiders activos
SPIDERS = [
    "eltiempo",
    "elespectador",
    "semana",
    "lasillavacia",
    "verdadabierta",
    "elcolombiano",
    "elpaiscali"
]

def run_spiders():
    print(f"🚀 Iniciando ciclo de monitoreo: {len(SPIDERS)} medios.")
    for spider in SPIDERS:
        print(f"🕵️  Ejecutando spider: {spider}...")
        # Ejecutamos el comando de scrapy
        subprocess.run(["scrapy", "crawl", spider])
        # Pequeña pausa para no saturar/bloquear IPs
        time.sleep(5)
    print("✅ Ciclo de monitoreo completado.")

if __name__ == "__main__":
    run_spiders()
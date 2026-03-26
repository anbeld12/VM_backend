import argparse
import os
import redis
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Lista de nombres de spiders (atributo 'name' de cada clase Spider)
SPIDERS = [
    "eltiempo",
    "elespectador",
    "semana",
    "lasillavacia",
    "verdadabierta",
    "elcolombiano",
    "elpaiscali",
    "cambio",
    "bluradio",
    "law",
    "noticiasrcn",
    "noticiascaracol",
    "las2orillas",
    "noticiasuno",
    "rtvcnoticias",
]


def flush_redis_db():
    """
    Conecta a Redis y ejecuta FLUSHDB para limpiar la caché de duplicados
    y la cola de peticiones. Lee la configuración desde variables de entorno.
    """
    host = os.getenv("REDIS_HOST", "redis")
    port = int(os.getenv("REDIS_PORT", 6379))
    print(f"🧹 Limpiando base de datos Redis en {host}:{port}...")
    try:
        r = redis.Redis(host=host, port=port)
        r.flushdb()
        print("✅ Redis vaciado correctamente. Se reprocesarán todas las URLs.")
    except redis.exceptions.ConnectionError as e:
        print(f"⚠️  No se pudo conectar a Redis para el vaciado: {e}")
        print("   Continuando con la ejecución de los spiders de todas formas...")
    except Exception as e:
        print(f"⚠️  Error inesperado al vaciar Redis: {e}")
        print("   Continuando con la ejecución de los spiders de todas formas...")


def main():
    # --- Argumentos de línea de comandos ---
    parser = argparse.ArgumentParser(
        description="Lanzador concurrente de spiders del Observatorio V&M"
    )
    parser.add_argument(
        "--flush-redis",
        action="store_true",
        help="Limpia la cola de duplicados y el scheduler en Redis antes de iniciar",
    )
    args = parser.parse_args()

    # --- Limpieza opcional de Redis ---
    if args.flush_redis:
        flush_redis_db()

    # --- Configuración del proceso de rastreo ---
    os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "observatorio_scraper.settings")
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # --- Encolar spiders dinámicamente por nombre ---
    print(f"🚀 Iniciando ciclo de monitoreo concurrente: {len(SPIDERS)} medios.")
    for spider_name in SPIDERS:
        print(f"🕵️  Añadiendo spider al pool: {spider_name}")
        process.crawl(spider_name)

    # --- Iniciar el Reactor de Twisted ---
    print("⏳ Arrancando motores en Twisted Reactor...")
    process.start()
    print("✅ Ciclo de monitoreo completado.")


if __name__ == "__main__":
    main()
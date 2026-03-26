import scrapy
from scrapy_redis.spiders import RedisSpider
from observatorio_scraper.spiders.diccionario import TERMINOS_ESTRATEGICOS

class CMISpider(RedisSpider):
    name = "cmi"
    allowed_domains = ["canal1.com.co"]
    start_urls = ["https://noticias.canal1.com.co/nacional/"]

    def parse(self, response):
        # Enlaces a noticias en Canal 1 / CM&
        enlaces = response.css('a::attr(href)').getall()
        for enlace in enlaces:
            if '/nacional/' in enlace or '/judicial/' in enlace:
                yield response.follow(enlace, self.parse_noticia)

    def parse_noticia(self, response):
        titulo = response.css('h1::text, .post-title::text').get()
        # Selectores genéricos para contenido
        parrafos = response.css('div.entry-content p::text, .post-content p::text, p::text').getall()
        
        contenido = ' '.join([p.strip() for p in parrafos if len(p.strip()) > 40])
        
        if not titulo or len(contenido) < 200:
            return

        texto_para_filtrar = f"{titulo} {contenido}".lower()
        encontrados = [t for t in TERMINOS_ESTRATEGICOS if t.lower() in texto_para_filtrar]

        if encontrados:
            item = {}
            item['titulo'] = titulo.strip()
            item['contenido'] = contenido
            item['url'] = response.url
            item['fuente'] = 'CM&'
            item['fecha_publicacion'] = response.css('time::attr(datetime), .post-date::text').get()
            yield item

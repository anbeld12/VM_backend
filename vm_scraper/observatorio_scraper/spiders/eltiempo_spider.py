import scrapy
from scrapy_redis.spiders import RedisSpider
from datetime import datetime
from observatorio_scraper.spiders.diccionario import TERMINOS_ESTRATEGICOS # <-- Importamos el diccionario global

class ElTiempoSpider(RedisSpider):
    name = "eltiempo"
    allowed_domains = ["eltiempo.com"]
    start_urls = ["https://www.eltiempo.com/justicia/conflicto-y-narcotrafico"]

    def parse(self, response):
        enlaces_noticias = response.css('a::attr(href)').getall()
        for enlace in enlaces_noticias:
            if '/justicia/' in enlace or '/politica/' in enlace:
                url_completa = response.urljoin(enlace)
                yield scrapy.Request(url_completa, callback=self.parse_noticia)

    def parse_noticia(self, response):
        titulo = response.css('h1::text, h1 span::text').get()
        parrafos = response.css('div.articulo-contenido p::text, div.cont_articulo p::text, .articulo p::text').getall()
        
        if not parrafos:
            parrafos = response.css('p::text').getall()
            
        contenido = ' '.join([p.strip() for p in parrafos if len(p.strip()) > 40])
        
        if not titulo or len(contenido) < 200:
            return

        texto_para_filtrar = f"{titulo} {contenido}".lower()
        
        # <-- Usamos la variable importada
        encontrados = [t for t in TERMINOS_ESTRATEGICOS if t.lower() in texto_para_filtrar]

        if encontrados:
            item = {}
            item['titulo'] = titulo.strip()
            item['contenido'] = contenido
            item['url'] = response.url
            item['fuente'] = 'El Tiempo'
            item['fecha_publicacion'] = response.css('time::attr(datetime), span.fecha::text').get()
            yield item
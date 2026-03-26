import scrapy
from scrapy_redis.spiders import RedisSpider
from observatorio_scraper.spiders.diccionario import TERMINOS_ESTRATEGICOS

class LaFMSpider(RedisSpider):
    name = "lafm"
    allowed_domains = ["lafm.com.co"]
    start_urls = ["https://www.lafm.com.co/colombia"]

    def parse(self, response):
        # Enlaces a noticias en La FM
        enlaces = response.css('a::attr(href)').getall()
        for enlace in enlaces:
            if '/colombia/' in enlace or '/judicial/' in enlace:
                yield response.follow(enlace, self.parse_noticia)

    def parse_noticia(self, response):
        titulo = response.css('h1::text, h1 span::text').get()
        # Selectores genéricos para contenido
        parrafos = response.css('div.article-body p::text, div.content p::text, p::text').getall()
        
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
            item['fuente'] = 'La FM'
            item['fecha_publicacion'] = response.css('time::attr(datetime), .date::text').get()
            yield item

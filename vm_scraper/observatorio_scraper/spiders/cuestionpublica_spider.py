import scrapy
from scrapy_redis.spiders import RedisSpider
from observatorio_scraper.spiders.diccionario import TERMINOS_ESTRATEGICOS

class CuestionPublicaSpider(RedisSpider):
    name = "cuestionpublica"
    allowed_domains = ["cuestionpublica.com"]
    start_urls = ["https://cuestionpublica.com/"]

    def parse(self, response):
        # Enlaces a noticias en Cuestión Pública
        enlaces = response.css('a::attr(href)').getall()
        for enlace in enlaces:
            # Filtro genérico para evitar secciones irrelevantes si es posible
            if enlace.startswith('https://cuestionpublica.com/') and len(enlace) > 30:
                yield response.follow(enlace, self.parse_noticia)

    def parse_noticia(self, response):
        titulo = response.css('h1::text, .entry-title::text').get()
        # Selectores genéricos para contenido
        parrafos = response.css('div.entry-content p::text, .elementor-widget-container p::text, p::text').getall()
        
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
            item['fuente'] = 'Cuestión Pública'
            item['fecha_publicacion'] = response.css('time::attr(datetime), .published::text').get()
            yield item

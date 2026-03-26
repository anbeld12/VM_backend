import scrapy
from scrapy_redis.spiders import RedisSpider
from observatorio_scraper.spiders.diccionario import TERMINOS_ESTRATEGICOS

class CambioSpider(RedisSpider):
    name = "cambio"
    allowed_domains = ["cambiocolombia.com"]
    start_urls = ["https://cambiocolombia.com/pais"]

    def parse(self, response):
        # Selectores comunes para enlaces de noticias
        enlaces = response.css('article a::attr(href), h2 a::attr(href), h3 a::attr(href)').getall()
        for enlace in set(enlaces):
            url_completa = response.urljoin(enlace)
            yield scrapy.Request(url_completa, callback=self.parse_noticia)

    def parse_noticia(self, response):
        titulo = response.css('h1::text, article h1::text, .article-title::text').get()
        
        # Selectores de párrafos comunes
        parrafos = response.css('article p::text, .article-content p::text, .p-content p::text').getall()
        if not parrafos:
            parrafos = response.css('p::text').getall()
            
        contenido = ' '.join([p.strip() for p in parrafos if len(p.strip()) > 40])
        
        if not titulo or len(contenido) < 200:
            return

        texto_para_filtrar = f"{titulo} {contenido}".lower()
        
        # Filtro de relevancia utilizando términos estratégicos
        encontrados = [t for t in TERMINOS_ESTRATEGICOS if t.lower() in texto_para_filtrar]

        if encontrados:
            yield {
                'titulo': titulo.strip(),
                'contenido': contenido,
                'url': response.url,
                'fuente': 'Cambio',
                'fecha_publicacion': response.css('meta[property="article:published_time"]::attr(content), time::attr(datetime), .date::text').get()
            }

import scrapy
from observatorio_scraper.spiders.diccionario import TERMINOS_ESTRATEGICOS

class SemanaSpider(scrapy.Spider):
    name = "semana"
    allowed_domains = ["semana.com"]
    start_urls = ["https://www.semana.com/nacion/"]

    def parse(self, response):
        enlaces = response.css('h2 a::attr(href), article a::attr(href)').getall()
        for enlace in enlaces:
            url_completa = response.urljoin(enlace)
            yield scrapy.Request(url_completa, callback=self.parse_noticia)

    def parse_noticia(self, response):
        titulo = response.css('h1::text').get()
        
        parrafos = response.css('article p::text, .article-content p::text, #main-content p::text').getall()
        # Fallback genérico si no encuentra párrafos con clases específicas
        if not parrafos:
            parrafos = response.css('p::text').getall()
            
        contenido = ' '.join([p.strip() for p in parrafos if len(p.strip()) > 40])
        
        if not titulo or len(contenido) < 200:
            return

        texto_para_filtrar = f"{titulo} {contenido}".lower()
        
        encontrados = [t for t in TERMINOS_ESTRATEGICOS if t.lower() in texto_para_filtrar]

        if encontrados:
            yield {
                'titulo': titulo.strip(),
                'contenido': contenido,
                'url': response.url,
                'fuente': 'Revista Semana',
                'fecha_publicacion': response.css('meta[property="article:published_time"]::attr(content), time::attr(datetime)').get()
            }

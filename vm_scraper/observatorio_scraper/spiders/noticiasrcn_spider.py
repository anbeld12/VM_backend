import scrapy
from scrapy_redis.spiders import RedisSpider
from observatorio_scraper.spiders.diccionario import TERMINOS_ESTRATEGICOS

class NoticiasRCNSpider(RedisSpider):
    name = "noticiasrcn"
    allowed_domains = ["noticiasrcn.com"]
    start_urls = ["https://www.noticiasrcn.com/colombia"]

    def parse(self, response):
        enlaces = response.css('article a::attr(href), h2 a::attr(href), .card-title a::attr(href)').getall()
        for enlace in set(enlaces):
            url_completa = response.urljoin(enlace)
            yield scrapy.Request(url_completa, callback=self.parse_noticia)

    def parse_noticia(self, response):
        titulo = response.css('h1::text, article h1::text').get()
        
        parrafos = response.css('article p::text, .article-body p::text, .main-content p::text').getall()
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
                'fuente': 'Noticias RCN',
                'fecha_publicacion': response.css('meta[property="article:published_time"]::attr(content), time::attr(datetime)').get()
            }

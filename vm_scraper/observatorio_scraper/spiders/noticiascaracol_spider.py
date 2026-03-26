import scrapy
from scrapy_redis.spiders import RedisSpider
from observatorio_scraper.spiders.diccionario import TERMINOS_ESTRATEGICOS

class NoticiasCaracolSpider(RedisSpider):
    name = "noticiascaracol"
    allowed_domains = ["noticias.caracoltv.com"]
    start_urls = ["https://noticias.caracoltv.com/colombia"]

    def parse(self, response):
        enlaces = response.css('.Promo-title a::attr(href), .Card-title a::attr(href), article a::attr(href)').getall()
        for enlace in set(enlaces):
            url_completa = response.urljoin(enlace)
            yield scrapy.Request(url_completa, callback=self.parse_noticia)

    def parse_noticia(self, response):
        titulo = response.css('h1::text, .ArticlePage-headline::text').get()
        
        parrafos = response.css('article p::text, .ArticlePage-articleBody p::text, .RichTextArticleBody p::text').getall()
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
                'fuente': 'Noticias Caracol',
                'fecha_publicacion': response.css('meta[property="article:published_time"]::attr(content), time::attr(datetime)').get()
            }

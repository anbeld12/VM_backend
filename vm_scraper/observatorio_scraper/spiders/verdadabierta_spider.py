import scrapy
from scrapy_redis.spiders import RedisSpider
from observatorio_scraper.spiders.diccionario import TERMINOS_ESTRATEGICOS

class VerdadAbiertaSpider(RedisSpider):
    name = "verdadabierta"
    allowed_domains = ["verdadabierta.com"]
    start_urls = ["https://verdadabierta.com/"]

    def parse(self, response):
        enlaces = response.css('h2.entry-title a::attr(href), h3.entry-title a::attr(href), .jeg_post_title a::attr(href)').getall()
        for enlace in enlaces:
            url_completa = response.urljoin(enlace)
            yield scrapy.Request(url_completa, callback=self.parse_noticia)

    def parse_noticia(self, response):
        titulo = response.css('h1.entry-title::text, h1.jeg_post_title::text, h1::text').get()
        
        parrafos = response.css('.entry-content p::text, .content-inner p::text').getall()
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
                'fuente': 'Verdad Abierta',
                'fecha_publicacion': response.css('meta[property="article:published_time"]::attr(content), time.entry-date::attr(datetime)').get()
            }

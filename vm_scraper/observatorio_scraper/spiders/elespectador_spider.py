# vm_scraper/observatorio_scraper/spiders/elespectador_spider.py

import scrapy
from datetime import datetime
from observatorio_scraper.spiders.diccionario import TERMINOS_ESTRATEGICOS

class ElEspectadorSpider(scrapy.Spider):
    name = "elespectador"
    allowed_domains = ["elespectador.com"]
    # Apuntamos a las secciones relevantes para V&M
    start_urls = [
        "https://www.elespectador.com/colombia-20/",
        "https://www.elespectador.com/judicial/"
    ]

    def parse(self, response):
        # El Espectador suele usar clases específicas para sus tarjetas de noticias
        enlaces = response.css('h2 a::attr(href), h3 a::attr(href), .Card-Title a::attr(href)').getall()
        for enlace in enlaces:
            url_completa = response.urljoin(enlace)
            yield scrapy.Request(url_completa, callback=self.parse_noticia)

    def parse_noticia(self, response):
        titulo = response.css('h1::text').get()
        
        # El Espectador guarda sus artículos en clases tipo Article-Content o font--secondary
        parrafos = response.css('.Article-Content p::text, .font--secondary p::text').getall()
        if not parrafos:
            parrafos = response.css('p::text').getall()
            
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
            item['fuente'] = 'El Espectador'
            # El Espectador suele usar meta tags para la fecha
            item['fecha_publicacion'] = response.css('meta[property="article:published_time"]::attr(content)').get()
            yield item
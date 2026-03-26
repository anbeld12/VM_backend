import scrapy

class NoticiaItem(scrapy.Item):
    # Definimos los campos que vamos a extraer de cada medio
    titulo = scrapy.Field()
    url = scrapy.Field()
    fecha_publicacion = scrapy.Field()
    fuente = scrapy.Field()
    contenido = scrapy.Field()
    terminos_encontrados = scrapy.Field() # Aquí guardaremos qué palabras clave hicieron match
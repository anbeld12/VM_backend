"""
Diccionario estratégico del Observatorio V&M.
"""

ESTRUCTURAS_E_INSTITUCIONES = [
    "Sistema Integral para la Paz", "SIP",
    "Sistema Integral de Verdad, Justicia, Reparación y No Repetición", "SIVJRNR",
    "Jurisdicción Especial para la Paz", "JEP",
    "Comisión para el Esclarecimiento de la Verdad, la Convivencia y la No Repetición", "CEV",
    "Unidad de Búsqueda de Personas dadas por Desaparecidas", "UBPD",
    "Agencia Nacional de Tierras", "ANT",
    "Sociedad de Activos Especiales", "SAE",
    "Agencia para la Reincorporación y la Normalización", "ARN",
    "OCAD Paz", "Órgano Colegiado de Administración y Decisión para la Paz"
]

TEMAS_Y_PROCESOS = [
    "Acuerdo de Paz", "Acuerdo de La Habana", "Posacuerdo",
    "Reforma Rural Integral", "Reincorporación", "Curules de Paz",
    "Reforma Agraria", "PDET", "Programas de Desarrollo con Enfoque Territorial",
    "ZOMAC", "Zonas Más Afectadas por el Conflicto",
    "Reconciliación", "Restauración", "Reparación",
    "Posconflicto", "Conflicto armado", "Justicia",
    "Justicia Transicional", "Justicia Restaurativa", "Justicia Reparadora",
    "Macrocasos", "Informe Final", "Exhumaciones",
    "Paz", "Verdad", "Memorias", "Territorio"
]

ACTORES_Y_SUJETOS = [
    "Partido Comunes", "partido FARC",
    "Firmantes de Paz", "Excombatientes", "Ex Farc",
    "Victimarios", "Víctimas",
    "Máximos responsables", "Familias buscadoras", "Desaparecidos"
]

TERMINOS_ESTIGMATIZANTES = [
    "Paramilitares", "Ex miembros de la fuerza pública", "Exmilitares",
    "Falsos Positivos", "Bajas en combate"
]

# Lista global unificada para el motor de matching en los spiders
TERMINOS_ESTRATEGICOS = (
    ESTRUCTURAS_E_INSTITUCIONES + 
    TEMAS_Y_PROCESOS + 
    ACTORES_Y_SUJETOS + 
    TERMINOS_ESTIGMATIZANTES
)
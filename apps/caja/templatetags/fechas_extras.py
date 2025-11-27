from django import template

register = template.Library()

MESES_ES = {
    1: "ene",
    2: "feb",
    3: "mar",
    4: "abr",
    5: "may",
    6: "jun",
    7: "jul",
    8: "ago",
    9: "sep",
    10: "oct",
    11: "nov",
    12: "dic",
}


@register.filter
def mes_es_abrev(value):
    try:
        return MESES_ES.get(value.month, "")
    except AttributeError:
        return ""

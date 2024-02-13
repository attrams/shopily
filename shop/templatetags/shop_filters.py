from django import template

register = template.Library()


@register.filter(name='first_paragraph')
def first_paragraph(value):
    """
    Returns the substring before the first double newline character.
    """
    paragraphs = value.split('\n', 1)

    if paragraphs:
        return paragraphs[0]

    return ''

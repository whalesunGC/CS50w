from django import template
import markdown

register = template.Library()

@register.filter(name="markdownify")
def markdownify(text):
    # safe_mode governs how the function handles raw HTML
    return markdown.markdown(text, safe_mode='escape') 
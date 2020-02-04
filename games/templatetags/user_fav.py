from django import template


register = template.Library()


@register.simple_tag
def is_favorite(profile, game_id):
    return profile.is_in_favorite(game_id)

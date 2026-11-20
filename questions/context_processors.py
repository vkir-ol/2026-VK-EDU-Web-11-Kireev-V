from .views import TAGS


def sidebar(request):
    return {
        "popular_tags": TAGS,
        "best_members": ["Mr. Oleg", "Mr. Mentalist", "Gogy"],
    }
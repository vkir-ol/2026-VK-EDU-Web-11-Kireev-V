from django.core.paginator import InvalidPage, Paginator
from django.http import Http404

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except InvalidPage as exc:
        raise Http404('Страница не найдена') from exc

    page.elided_range = paginator.get_elided_page_range(page.number)
    return page

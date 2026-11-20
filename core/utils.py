from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # если в page не число - показываем первую страницу
        page = paginator.page(1)
    except EmptyPage:
        # если такой страницы нет - показываем последнюю
        page = paginator.page(paginator.num_pages)

    return page
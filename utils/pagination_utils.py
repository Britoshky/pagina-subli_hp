def generate_pagination(page, total_pages):
    """
    Genera una lista de páginas para navegación.
    """
    visible_pages = []

    if page > 3:
        visible_pages.append(1)
        visible_pages.append('...')

    for p in range(max(1, page - 2), min(total_pages + 1, page + 3)):
        visible_pages.append(p)

    if page < total_pages - 2:
        visible_pages.append('...')
        visible_pages.append(total_pages)
    elif total_pages not in visible_pages:
        visible_pages.append(total_pages)

    return visible_pages

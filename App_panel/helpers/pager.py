def get_visible_page_numbers(paginator, page_obj, max_pages_around_current=1):
    visible_page_numbers = []

    if paginator.num_pages > 0:
        visible_page_numbers.append(1)

    if paginator.num_pages <= (max_pages_around_current * 2 + 1 + 2):
        for num in range(2, paginator.num_pages + 1):
            if num not in visible_page_numbers:
                visible_page_numbers.append(num)
    else:
        start_page = max(2, page_obj.number - max_pages_around_current)
        end_page = min(paginator.num_pages - 1, page_obj.number + max_pages_around_current)

        if page_obj.number <= max_pages_around_current + 1:
            end_page = min(paginator.num_pages - 1, max_pages_around_current * 2 + 1)
        if page_obj.number >= paginator.num_pages - max_pages_around_current:
            start_page = max(2, paginator.num_pages - (max_pages_around_current * 2))

        if start_page > 1 and len(visible_page_numbers) > 0 and start_page > visible_page_numbers[-1] + 1:
            visible_page_numbers.append('...')

        for num in range(start_page, end_page + 1):
            if num not in visible_page_numbers:
                visible_page_numbers.append(num)

        if paginator.num_pages > end_page and paginator.num_pages not in visible_page_numbers:
            if paginator.num_pages > end_page + 1:
                if '...' not in visible_page_numbers:
                    visible_page_numbers.append('...')
            if paginator.num_pages not in visible_page_numbers:
                visible_page_numbers.append(paginator.num_pages)

    final_visible_pages = []
    seen = set()
    for item in visible_page_numbers:
        if item not in seen:
            final_visible_pages.append(item)
            seen.add(item)

    return final_visible_pages

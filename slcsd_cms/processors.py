from django.urls import resolve
from django.urls.exceptions import Resolver404


def get_url_tree(path):
    paths = []
    split_path = path.split('/')
    while '' in split_path:
        split_path.remove('')
    while split_path:
        path = '/'.join(split_path)
        paths.append('/{0}/'.format(path))
        split_path.pop(-1)
    return paths


def admin_breadcrumbs(request):
    breadcrumbs = []
    url_tree = get_url_tree(request.path)
    url_tree.reverse()
    for path in url_tree:
        try:
            has_path = resolve(path)
            try:
                title = has_path.func.view_class.Meta.breadcrumb_title
            except AttributeError:
                title = has_path.url_name or path.split('/')[-2]
            try:
                icon = has_path.func.view_class.Meta.breadcrumb_icon
            except AttributeError:
                icon = None
            breadcrumbs.append({'path': path, 'title': title, 'icon': icon})
        except Resolver404:
            pass
    return {'admin_breadcrumbs': breadcrumbs}

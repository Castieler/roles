from django.template import Library
from django.conf import settings
from re import match

register = Library()


@register.inclusion_tag(filename='menu_1.html')
def menu_html(request):
    """ 生成渲染菜单的数据结构并返回该数据
    Args:
        request: 请求对象
    """

    current_url = request.path_info
    menu_list = request.session.get(settings.MENU_LIST)

    menu_dict = {}
    for item in menu_list:
        print('item:',item)
        menu_id = item['menu_id']
        menu_title = item['menu_title']
        title = item['feature']
        url = item['url']
        display = item['display']
        regex_url = f'^{item["url"]}$'
        if not display:
            continue
        if match(pattern=regex_url, string=current_url):
            item['active'] = True
        else:
            item['active'] = False

        active = item['active']
        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append({'feature': item['feature'], "title": title, "url": url, "active": active})
            if active:
                menu_dict[menu_id]['active'] = True
        else:
            menu_dict[menu_id] = {
                "menu_id": menu_id,
                "menu_title": menu_title,
                "active": active,
                "children": [
                    {'feature': item['feature'], "title": title, "url": url, "active": active}
                ]
            }
    print(menu_dict)
    return {'menu_dict': menu_dict}



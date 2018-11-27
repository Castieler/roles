def save_request_url(fun):
    def inner(request, *args, **kwargs):
        try:
            last_url = request.session['url']
        except:
            last_url= "/home/"
        request.session['url'] = request.path_info
        return fun(request, last_url, *args, **kwargs)
    return inner
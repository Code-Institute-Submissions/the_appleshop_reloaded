def get_active_app(request):
    app_path =  request.get_full_path()
    return {'app_path' : app_path}
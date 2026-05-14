def theme_processor(request):
    return {
        'dark_mode': request.session.get('dark_mode', False)
    }

from .models import ThemeSettings

def theme_settings(request):
    theme = ThemeSettings.objects.first()
    return {"theme": theme}
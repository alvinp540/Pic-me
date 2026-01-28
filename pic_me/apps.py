from django.apps import AppConfig


class PicMeConfig(AppConfig):
    name = 'pic_me'
    default_auto_field = 'django.db.models.BigAutoField'
    
    def ready(self):
        import pic_me.models  # This ensures signals are loaded


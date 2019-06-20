from django.apps import AppConfig, apps


class ReviewsConfig(AppConfig):
    name = 'reviews'

    def ready(self):
        #from django.contrib.auth.models import User
        from actstream import registry
        registry.register(apps.get_app_config('auth').get_model('User'))
        registry.register(self.get_model('Critic'))
        registry.register(self.get_model('Review'))
        registry.register(self.get_model('Comment'))
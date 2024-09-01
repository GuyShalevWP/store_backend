from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError

class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'


    # incase there's no db that will add caregories automatically.
    def ready(self):
        from .models import Category
        try:
            categories = [
                {"name": "Frozen Foods", "slug": "frozen-foods"},
                {"name": "Spices and Seasonings", "slug": "spices-and-seasonings"},
                {"name": "Canned and Jarred Goods", "slug": "canned-and-jarred-goods"},
                {"name": "Grains and Pasta", "slug": "grains-and-pasta"},
                {"name": "Beverages", "slug": "beverages"},
                {"name": "Snacks and Sweets", "slug": "snacks-and-sweets"},
                {"name": "Baked Goods", "slug": "baked-goods"},
                {"name": "Seafood", "slug": "seafood"},
                {"name": "Meat", "slug": "meat"},
                {"name": "Dairy and Eggs", "slug": "dairy-and-eggs"},
                {"name": "Vegetables", "slug": "vegetables"},
                {"name": "Fruits", "slug": "fruits"},
            ]

            for category_data in categories:
                Category.objects.get_or_create(name=category_data["name"], slug=category_data["slug"])

        except (OperationalError, ProgrammingError):
            pass

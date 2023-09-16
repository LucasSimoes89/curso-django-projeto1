from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('serving_unit', 65),
    ])
    def test_recipe_fields_max_lenght(self, field, max_lenght):
        # Seta o atributo de self.recipe com o field necessário para os testes
        setattr(self.recipe, field, 'A' * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # AQUI A VALIDAÇÃO DE CHARS OCORRE

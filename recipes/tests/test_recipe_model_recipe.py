from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default category'),
            author=self.make_author(username='newuser'),
            title='Recipe title',
            description='Recipe description',
            slug='recipe-slug',
            preparation_time=2,
            preparation_time_unit='horas',
            servings=5,
            servings_unit='pessoas',
            preparation_steps='steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_lenght(self, field, max_lenght):
        # Seta o atributo de self.recipe com o field necessário para os testes
        setattr(self.recipe, field, 'A' * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # AQUI A VALIDAÇÃO DE CHARS OCORRE

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_steps_is_html)

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation(self):
        needed = 'Testing Representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), needed,
                         msg=f'Recipe string representation must be '
                         f'"{needed}" but "{str(self.recipe)}" was received'
                         )

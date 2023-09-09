from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views
from recipes.models import Category, Recipe, User


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    # def test_recipe_home_view_returns_status_code_200_OK(self):
    #     response = self.client.get(reverse('recipes:home'))
    #     self.assertEqual(response.status_code, 200)

    # def test_recipe_home_view_load_correct_template(self):
    #     response = self.client.get(reverse('recipes:home'))
    #     self.assertTemplateUsed(response, 'recipes/pages/home.html')

    # def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
    #     response = self.client.get(reverse('recipes:home'))
    #     self.assertIn(
    #         'No recipes found here',
    #         response.content.decode('utf-8')
    #     )

    def teste_recipe_home_template_loads_recipes(self):
        category = Category.objects.create(name='Café da manhã')
        author = User.objects.create_user(
            first_name='lucas',
            last_name='simoes',
            username='lucas.simoes',
            password='123456',
            email='lucas@gmail.com',
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe title',
            description='Recipe description',
            slug='Recipe slug',
            preparation_time=2,
            preparation_time_unit='horas',
            servings=5,
            servings_unit='pessoas',
            preparation_steps='steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
        response = self.client.get(reverse('recipes:home'))
        response_context_recipes = response.context['recipes'][0]
        content = response.content.decode('utf-8')

        self.assertIn('Recipe title', content)
        self.assertIn('2 horas', content)
        self.assertIn('5 pessoas', content)
        self.assertEqual(len(response.context['recipes']), 1)
        self.assertEqual(response_context_recipes.is_published, True)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_viw_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_viw_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

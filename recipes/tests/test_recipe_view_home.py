from unittest import skip

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        #  Need a recipe for test
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_load_correct_template(self):
        #  Need a recipe for test
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    @skip('WIP')
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'Not Found',
            response.content.decode('utf-8')
        )

    def teste_recipe_home_template_loads_recipes(self):
        #  Need a recipe for test
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        response_context_recipes = response.context['recipes'][0]
        content = response.content.decode('utf-8')

        self.assertIn('Recipe title', content)
        self.assertEqual(len(response.context['recipes']), 1)
        self.assertEqual(response_context_recipes.is_published, True)

    def teste_recipe_home_template_dont_load_recipe_not_publisehd(self):
        #  Need a recipe for test
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            'Not Found',
            response.content.decode('utf-8')
        )

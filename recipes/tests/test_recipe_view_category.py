from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewsTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_viw_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def teste_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'

        #  Need a recipe for test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def teste_recipe_category_template_dont_load_recipe_not_publisehd(self):
        #  Need a recipe for test
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.category.id})
        )

        self.assertEqual(response.status_code, 404)

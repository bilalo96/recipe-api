"""Test for recipe API"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe , Tag

from recipe.serializers import(
     RecipeSerializer,
     RecipeDetailSerializer,
     )

RECIPES_URL=reverse('recipe:recipe-list') #we here define the url as a variable


def detail_url(recipe_id): #we here define the url as a function becauese we need pass in the recipe id to the url
    """Create and return a recipe detail URL"""
    return reverse('recipe:recipe-detail',args=[recipe_id])

def create_recipe(user,**params):
    """Create and return a sample recipe"""
    defaults = {
        'title':'sample recipe',
        'time_minutes':22,
        'price':Decimal('5.25'),
        'description':'Sample description',
        'link':'http://example.com/recipe.pdf',
    }
    defaults.update(params)

    recipe=Recipe.objects.create(user=user,**defaults)
    return recipe

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)



class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests"""
    def setUp(self):
       self.client=APIClient()
       self.user=create_user(email='user@example.com',password='test123')
       self.client.force_authenticate(self.user)

    def test_retrive_recipes(self):
        """Test retriving a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res=self.client.get(RECIPES_URL)

        recipes=Recipe.objects.all().order_by('-id')
        serializer=RecipeSerializer(recipes,many=True)#many:because serializer retrive item or list of item
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data) #data here is data dectionary of the objects passed through the serializer


    def test_recipe_list_limeted_to_user(self):# for the user logginin
        """Test list of recipe is limted to authenticated user"""
        other_user=create_user(
            email='other@example.com',
           password= 'test123',
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res=self.client.get(RECIPES_URL)

        recipes=Recipe.objects.filter(user=self.user)
        serializer=RecipeSerializer(recipes,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail"""
        recipe= create_recipe(user=self.user)

        url=detail_url(recipe.id)
        res=self.client.get(url)

        serializer=RecipeDetailSerializer(recipe)
        self.assertEqual(res.data,serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload={
            'title':'Sample recipe',
            'time_minutes':30,
            'price':Decimal('5.50')
        }
        res=self.client.post(RECIPES_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        recipe=Recipe.objects.get(id=res.data['id'])
        for i, j in payload.items():
            self.assertEqual(getattr(recipe,i),j)
        self.assertEqual(recipe.user,self.user)

    def test_partial_update(self):
        """Test partial update of a recipe"""
        original_link='https://example.com/recipe.pdf'
        recipe=create_recipe(
            user=self.user,
            title='Sample recie user',
            link=original_link,

        )
        payload={
            'title':'new recipe title'
        }
        url=detail_url(recipe.id)
        res=self.client.patch(url,payload)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title,payload['title'])
        self.assertEqual(recipe.link,original_link)
        self.assertEqual(recipe.user,self.user)

    def test_create_recipe_with_new_tag(self):
        """Test creating a recipe with new tag"""

        payload={
            'title':'Thai Prawn Curry',
            'time_minutes':30,
            'price':Decimal('3.50'),
            'tags':[{'name':'Thai'},{'name':'Dinner'}]
        }
        res=self.client.post(RECIPES_URL,payload,format='json')

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        recipes=Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(),1)
        recipe=recipes[0]
        self.assertEqual(recipe.tags.count(),2)
        for tag in payload['tags']:
            exists=recipe.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)


    def test_create_recipe_with_existing_tag(self):
        """Test creating a recipe with existing tag"""
        tag_indian=Tag.objects.create(user=self.user,name='Indian')
        payload={
            'title':'Pongal',
            'time_minuts':60,
            'description':'bssds',
            'link':'https://example.com/recipe1.pdf',
            'price':Decimal('3.50'),
            'tags':[{'name','Indian'},{'name':'Breakfast'}],
        }
        res=self.client.post(RECIPES_URL ,payload ,format='json')

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        recipes=Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(),1)
        recipe=recipes[0]
        self.assertEqual(recipe.tags.count(),2)
        self.assertIn(tag_indian,recipe.tags.all())
        for tag in payload['tags']:
            exists=recipe.tags.filter(
              name=tag['name'],
              user=self.user,
            ).exists()
            self.assertTrue(exists)





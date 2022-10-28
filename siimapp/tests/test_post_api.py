from django.urls import reverse, resolve
from django.test import SimpleTestCase
from siimapp.views import PostView, FavouritePostView
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from siimapp.models import Post, FavouritePost
from siimapp.serializers import PostSerializer
import json

class ApiUrlsTests(SimpleTestCase):

    def test_get_post_is_resolved(self):
        url = reverse("posts")
        self.assertEquals(resolve(url).func.view_class, PostView)


class PostAPIViewTests(APITestCase):
    posts_url = reverse('posts')
    
    def setUp(self):
        self.user = User.objects.create_user(
           email="adminuser@gmail.com", username='adminuser', password='adminuser@123'
        )
        self.token = Token.objects.create(user=self.user)
        # self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        Post.objects.create(user=self.user, title="POST CREATED", description="POST WAS CREATED")
        Post.objects.create(user=self.user, title="POST CREATED 2", description="POST WAS CREATED 2")
        Post.objects.create(user=self.user, title="POST CREATED 3", description="POST WAS CREATED 3")




    def test_get_posts_authenticated(self):
        # get API response 
        response = self.client.get(reverse('posts'))
        # get data from DB
        posts = Post.objects.all()
        # convert it to JSON
        serializer = PostSerializer(posts, many=True)
        # check the status 
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_get_posts_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.posts_url)
        self.assertEquals(response.status_code, 401)



class PostDetailAPIViewTests(APITestCase):
    posts_url = reverse('posts')
    
    def setUp(self):
        self.user = User.objects.create_user(
           email="adminuser@gmail.com", username='adminuser', password='adminuser@123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.first_post = Post.objects.create(user=self.user, title="POST CREATED", description="POST WAS CREATED")
        self.second_post = Post.objects.create(user=self.user, title="POST CREATED 2", description="POST WAS CREATED 2")

        self.valid_post = {
            "title" : "post changed",
            "content": "post changed"
        }
        self.invalid_post = {
            "title": "",
            "content": "post change"
        }
    def test_valid_update_post(self):
        '''
        Validated data case 
        '''
        response = self.client.put(
            reverse('post-by-id', kwargs={'pk': self.first_post.pk}),
            data = json.dumps(self.valid_post),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_post(self):
        '''
        Invalid data case 
        '''
        response = self.client.put(
            reverse('post-by-id', kwargs={'pk': self.second_post.pk}),
            data = json.dumps(self.invalid_post),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestLikeViews(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
           email="adminuser@gmail.com", username='adminuser', password='adminuser@123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.factory = APIRequestFactory()
        self.post = Post.objects.create(user=self.user, title="POST CREATED 2", description="POST WAS CREATED 2")
        self.fav = FavouritePost.objects.create(
            user=self.user, post=self.post)

    def test_like_put_user(self):
        request = self.factory.put('fav-post/', {'user': self.user.pk, 'post': self.post.pk}) 
        request.user = self.user
        response = FavouritePostView.as_view()(request, user=self.user.pk, post=self.post.pk)
        self.assertEqual(response.status_code, 201)
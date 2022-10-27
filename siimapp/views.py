from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from siimapp.backends import EmailBackend
from rest_framework import status
from siimapp.models import FavouritePost, Post, User
from siimapp.serializers import PostSerializer, UserSerializer


class Registration(APIView):

    def post(self, request):
        context = {}
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                context['data'] = serializer.data
                context['message'] = 'User register successfully.'
                context['status'] = True
                status_code = status.HTTP_201_CREATED
                return Response(data=context, status=status_code)
            else:
                context['message'] = serializer.errors
                context['status'] = False
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(data=context, status=status_code)
        except Exception as e:
            context['message'] = str(e)
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(data=context, status=status_code)


class LogIn(APIView):

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            content = [email, password]
            context = {}
            if all(content):
                user = User.objects.filter(email=email).first()
                if user is not None:
                    if user.is_active == True:
                        check = EmailBackend.authenticate(self, request, email=email, password=password)
                        if check is not None:
                            token, _ = Token.objects.get_or_create(user=user)
                            data = {}
                            data['token'] = token.key
                            context['data'] = data
                            context['message'] = 'Successfully login'
                            return Response(data=context, status=status.HTTP_200_OK)
                        else:
                            context['message'] = 'Incorrect password, enter right password'
                            context['status'] = False
                            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        context["message"] = 'You account is not active yet!'
                        context["status"] = False
                        return Response(data=context, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    context["message"] = 'This email not register, please enter register email!'
                    context["status"] = False
                    return Response(data=context, status=status.HTTP_404_NOT_FOUND)
            else:
                context["message"] = 'Please enter email and password!'
                context["status"] = False
                return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            context['message'] = str(e)
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(data=context, status=status_code)


class PostView(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        API  For Get All Posts 
        """
        try:
            context = {}
            status_code = status.HTTP_200_OK
            posts = Post.objects.all()
            if not posts:
                context['message'] = 'Not Found'
                context['status'] = False
                status_code = status.HTTP_404_NOT_FOUND
                return Response(data=context, status=status_code)
            serializer = self.serializer_class(posts, many=True)
            context['data'] = serializer.data
            context['status'] = True
            return Response(data=context, status=status_code)
        except Exception as e:
            context['message'] = str(e)
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(data=context, status=status_code)


    def post(self, request):
        """
        API  For Create Post
        """
        try:
            context = {}
            status_code = status.HTTP_200_OK
            serializer = self.serializer_class(data=request.data, context={'request': request.user})
            if serializer.is_valid():
                serializer.save()
                context['data'] = serializer.data
                context['message'] = 'Post Created Successfully'
                context['status'] = True
                status_code =status.HTTP_201_CREATED
                return Response(data=context, status=status_code)
            else:
                context['message'] = serializer.errors
                context['status'] = False
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(data=context, status=status_code)
        except Exception as e:
            context['message'] = str(e)
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(data=context, status=status_code)


class PostViewDetail(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        API For Get Post By id
        """
        try:
            context = {}
            status_code = status.HTTP_200_OK
            posts = Post.objects.get(id=pk)
            if not posts:
                context['message'] = 'Not Found'
                context['status'] = False
                status_code = status.HTTP_404_NOT_FOUND
                return Response(data=context, status=status_code)
            serializer = self.serializer_class(posts)
            context['data'] = serializer.data
            context['status'] = True
            return Response(data=context, status=status_code)
        except Exception as e:
            context['message'] = str(e)
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(data=context, status=status_code)

    def put(self, request, pk):
        """
        API For Update Post By id
        """
        try:
            context = {}
            status_code = status.HTTP_200_OK
            posts = Post.objects.filter(id=pk).first()
            if not posts:
                context['message'] = 'Not Found'
                context['status'] = False
                status_code = status.HTTP_404_NOT_FOUND
                return Response(data=context, status=status_code)
            serializer = self.serializer_class(posts, data=request.data)
            if serializer.is_valid():
                serializer.save()
                context['data'] = serializer.data
                context['message'] = 'Post Updated Successfully'
                context['status'] = True
                status_code = status.HTTP_200_OK
                return Response(data=context, status=status_code)
            else:
                context['message'] =  serializer.errors
                context['status'] = False
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(data=context, status=status_code)
        except Exception as e:
            context['message'] = str(e)
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(data=context, status=status_code)

    def delete(self, request, pk):
        """
        API For Delete Post By id 
        """
        try:
            context = {}
            status_code = status.HTTP_200_OK
            post = Post.objects.filter(id=pk).first()
            if not post:
                context['message'] = 'Not Found'
                context['status'] = False
                status_code = status.HTTP_404_NOT_FOUND
                return Response(data=context, status=status_code)
            post.delete()
            context['message'] = 'Post Deleted Successfully'
            context['status'] = True
            status_code = status.HTTP_204_NO_CONTENT
            return Response(data=context, status=status_code)
        except Exception as e:
            context['message'] = str(e)
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(data=context, status=status_code)


class FavouritePostView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, post_id):
        """
        API For Like and Unlike Post By id 
        """
        try:
            context = {}
            status_code = status.HTTP_200_OK
            user = request.user
            post = Post.objects.filter(pk=post_id).first()
            if not post:
                context['message'] = 'Not Found'
                context['status'] = False
                status_code = status.HTTP_404_NOT_FOUND
                return Response(context, status=status_code)
            like = FavouritePost.objects.filter(user=user, post=post)
            if like:
                like.delete()
                context['message'] = 'Unlike'
                context['status'] = True
                status_code =status.HTTP_200_OK
            else:
                FavouritePost.objects.create(user=user, post=post)
                context['message'] = 'like'
                context['status'] = True
                status_code =status.HTTP_200_OK
            return Response(context, status=status_code)
        except Exception as e:
            context['message'] = str(e)
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(data=context, status=status_code)
        
from api.models import Comment, Post, Profile, User
from api.utils import Utils
from datetime import timezone
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Prefetch
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from django.core.cache import cache


class UserSignupView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get("username")
            email = request.data.get("email")
            password = request.data.get("password")

            if not username or not email or not password:
                return Response(
                    {"message": "Missing required fields"}, status.HTTP_400_BAD_REQUEST
                )

            if User.objects.filter(username=username).exists():
                return Response(
                    {"message": "User already exists"}, status.HTTP_400_BAD_REQUEST
                )

            if User.objects.filter(email=email).exists():
                return Response(
                    {"message": "Email already exists"}, status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            profile = Profile.objects.create(user=user)

            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except:
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# @method_decorator(cache_page(60 * 15), name='dispatch')
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            cache_key = f"login__{username}__{password}"
            cached_data = cache.get(cache_key)

            if cached_data:
                return Response(cached_data, status=status.HTTP_200_OK)

            user = authenticate(request=request, username=username, password=password)
            if not user:
                return Response(
                    {"message": "Invalid username or password"},
                    status.HTTP_400_BAD_REQUEST,
                )
            token, created = Token.objects.get_or_create(user=user)
            response = {
                "username": user.username,
                "token": token.key,
            }
            cache.set(cache_key, response, timeout=60 * 15)
            return Response(
                data=response,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": f"Internal Server Error {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PostView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        post_slug = request.data.get("post_slug", None)
        if post_slug is None:
            try:
                page_number = request.GET.get("p_num", 1)
                page_size = request.GET.get("p_size", 10)

                cache_key = f"all_posts__{user_id}__{page_number}__{page_size}"
                cached_data = cache.get(cache_key)
                if cached_data:
                    return Response(cached_data, status=status.HTTP_200_OK)

                posts = (
                    Post.objects.filter(author_id=user_id)
                    .select_related("author")
                    .only(
                        "id",
                        "title",
                        "slug",
                        "content",
                        "created_at",
                        "updated_at",
                        "author__username",
                    )
                    .order_by("-updated_at")
                )

                Post.objects.raw("""
                    SELECT * FROM
            """)
                paginator = Paginator(posts, page_size)

                try:
                    page_posts = paginator.page(page_number)
                except PageNotAnInteger:
                    page_posts = paginator.page(1)
                except EmptyPage:
                    page_posts = paginator.page(paginator.num_pages)

                all_post = [
                    {
                        "id": post.id,
                        "title": post.title,
                        "slug": post.slug,
                        "content": post.content,
                        "created_at": post.created_at,
                        "updated_at": post.updated_at,
                        "author": post.author.username,
                        # "comments": [
                        #     {
                        #         "comment": comment.comment,
                        #         "user": comment.author.username,
                        #     }
                        #     for comment in list(
                        #         post.comments.select_related().all()[:5]
                        #     )
                        # ],
                    }
                    for post in page_posts
                ]

                response = {
                    "posts": all_post,
                    "page": page_posts.number,
                    "total_pages": paginator.num_pages,
                }
                cache.set(cache_key, response, timeout=60 * 15)

                return Response(
                    data=response,
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                print(e)
                return Response(
                    {
                        "error": "Internal Server Error",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        else:
            post = (
                Post.objects.filter(slug=post_slug)
                .select_related("author")
                .only(
                    "id",
                    "title",
                    "slug",
                    "content",
                    "created_at",
                    "updated_at",
                    "author__username",
                )
                .first()
            )
            if post is None:
                return Response(
                    {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
                )
            else:
                comments = list(
                    Comment.objects.select_related("author")
                    .filter(post=post)
                    .values("comment", "author__username")[:5]
                )
                return Response(
                    {
                        "id": post.id,
                        "title": post.title,
                        "slug": post.slug,
                        "content": post.content,
                        "created_at": post.created_at,
                        "updated_at": post.updated_at,
                        "author": post.author.username,
                        # "comments": [
                        #     {
                        #         "comment": comment.comment,
                        #         "user": comment.author.username,
                        #     }
                        #     for comment in list(post.comments.all())[:5]
                        # ],
                        "comments": comments,
                    },
                    status=status.HTTP_200_OK,
                )

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        data = request.data
        title = data.get("title")
        content = data.get("content")
        if title is None or content is None:
            return Response(
                {"error": "Title and content are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            try:
                slug = Utils.slugify(title)
                post = Post.objects.get(slug=slug)
                return Response(
                    {"error": "Blog with same title already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Post.DoesNotExist:
                post = Post.objects.create(
                    title=title,
                    content=content,
                    author_id=user_id,
                    slug=slug,
                )
                return Response(
                    {
                        "id": post.id,
                        "title": post.title,
                        "slug": post.slug,
                        "content": post.content,
                        "created_at": post.created_at,
                        "updated_at": post.updated_at,
                        "author": post.author.username,
                        "comments": [],
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                print(e)
                return Response(
                    {"error": "Can't create post"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    def patch(self, request, *args, **kwargs):
        user_id = request.user.id
        # post_slug = kwargs.get("post_slug")
        post_slug = request.data.get("post_slug", None)
        post = Post.objects.filter(author_id=user_id, slug=post_slug).first()
        if post is None:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if post_slug:
            data = request.data
            if data.get("comment", None) is None:
                title = data.get("title")
                content = data.get("content")
                if title is not None:
                    post.title = title
                if content is not None:
                    post.content = content
                post.save()
                return Response(
                    {
                        "id": post.id,
                        "title": post.title,
                        "slug": post.slug,
                        "content": post.content,
                        "created_at": post.created_at,
                        "updated_at": post.updated_at,
                        "author": post.author.username,
                        # "comments": [
                        #     {
                        #         "comment": comment.comment,
                        #         "user": comment.author.username,
                        #     }
                        #     for comment in list(post.comments.all())[:5]
                        # ],
                    },
                    status=status.HTTP_200_OK,
                )

            else:
                comment = data.get("comment", None)
                if comment:
                    comment_obj = Comment.objects.create(
                        post=post, author=request.user, comment=comment
                    )
                    print(comment_obj)
                    if comment_obj:
                        return Response(
                            {"message": "Comment added successfully"},
                            status=status.HTTP_201_CREATED,
                        )
                    return Response(
                        {"error": "Failed to add comment"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                return Response(
                    {"error": "Can not add empty comment"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

    def delete(self, request, *args, **kwargs):
        user_id = request.user.id
        post_slug = kwargs.get("post_slug")
        if post_slug:
            post = Post.objects.filter(author_id=user_id, slug=post_slug).first()
            if post is None:
                return Response(
                    {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
                )
            else:
                post.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"error": "Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

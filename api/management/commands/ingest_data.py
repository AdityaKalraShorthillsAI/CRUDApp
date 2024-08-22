from django.core.management import BaseCommand
import requests
from api.models import Comment, Post, User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Posts
        # random_words = requests.get('https://random-word-api.herokuapp.com/all')
        # user = User.objects.get(username="adityakalra1")
        # posts = []
        # for i in range(2, 9):
        #     for word in random_words.json():
        #         posts.append(Post(
        #             slug=f"{word}_{i}",
        #             title=f"{word}_{i}",
        #             content=f"{word}_{i}",
        #             author=user,
        #         ))
        #     Post.objects.bulk_create(posts, batch_size=200)
        #     posts = []
        #     print(i)

        # Comments

        random_words = requests.get('https://random-word-api.herokuapp.com/all')
        
        user = User.objects.get(username="adityakalra1")
        comments = []
        for i in range(2, 4):
            for word in random_words.json()[100:1000]:
                print(word)
                post = Post.objects.get(title=f"{word}_{i}")
                comments.append(Comment(
                    post=post,
                    author=user,
                    comment=f"This is a comment for {word}_{i}",
                ))
            
            Comment.objects.bulk_create(comments, batch_size=200)
            comments = []
            print(i)
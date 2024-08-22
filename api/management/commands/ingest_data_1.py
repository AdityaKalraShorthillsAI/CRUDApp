from api.models import Comment, Post, User
from api.utils import Utils
from django.core.management import BaseCommand
import os
import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), "blogtext.csv")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # user = User.objects.get(username="adityakalra")
        # df = pd.read_csv(file_path)
        # posts = []
        # count = 0
        # for i, row in df.iterrows():
        #     try:
        #         content = row['text'].strip()
        #         topic = Utils.slugify(content[:70])

        #         if '?' in topic:
        #             topic = topic.split('?')[0]
        #         slug = f"{topic}_{count}"
        #         count += 1

        #         posts.append(
        #             Post(
        #                 author=user,
        #                 title=topic,
        #                 slug=slug,
        #                 content=content,
        #             )
        #         )

        #         if len(posts) == 2000:
        #             Post.objects.bulk_create(posts, batch_size=500)
        #             print(f"{len(posts)} posts created")
        #             posts = []



        #         # try:
        #         #     post = Post.objects.get(author=user, title=topic, slug=slug)
        #         #     post.content = content
        #         # except Post.DoesNotExist:
        #         #     post = Post.objects.create(
        #         #         author=user,
        #         #         title=topic,
        #         #         slug=slug,
        #         #         content=content,
        #         #     )
        #         # post.save()
        #         # print(f"Created post: {topic}")

        #     except Exception as e:
        #         print(e)

       
    #    -----------------------------------------------------------------------------------------------------------------
        user = User.objects.get(username="adityakalra")
        posts = Post.objects.all()
        comments = []
        for post in posts:
            for i in range(0, 5):
                try:
                    comment_content = f"This is a comment for {post.title}_{i}"
                    comments.append(
                        Comment(
                            post=post,
                            author=user,
                            comment=comment_content,
                        )
                    )
                    if len(comments) == 5000:
                        Comment.objects.bulk_create(comments, batch_size=1000)
                        print(f"{len(comments)} comments created")
                        comments = []
                except:
                    pass

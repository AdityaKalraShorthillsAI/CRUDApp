from locust import HttpUser, TaskSet, task, between
from uuid import uuid4


class UserBehavior(TaskSet):
    @task
    def GetOrCreatePosts(self):
        login_data = self.client.post(
            "api/user/login/", {"username": "adityakalra", "password": "Aditya@1234"}
        )
        # token = f"{login_data.json()['token']}"
        token = "e84f96feccbe8ebb5cc1305cd732385d63fc4a6d"
        self.client.get(
            "api/posts/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {token}",
            },
        )
        post_slug = str(uuid4())
        self.client.post(
            "api/post/",
            data={
                "title": f"{post_slug}",
                "content": f"This is a sample post {post_slug}.",
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {token}",
            },
        )
        self.client.get(
            "api/post/",
            data={"post_slug": f"{post_slug}"},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {token}",
            },
        )
        comment_uuid = str(uuid4())
        self.client.patch(
            "api/post/",
            data={
                "post_slug": f"{post_slug}",
                "comment": f"This is a comment {comment_uuid}.",
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {token}",
            },
        )


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)

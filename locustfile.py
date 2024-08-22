from locust import HttpUser, TaskSet, task, between
from uuid import uuid4
import time

token = "e84f96feccbe8ebb5cc1305cd732385d63fc4a6d"
# token = "f819ab6be6fd12b48ef0ce0286d6d7de5a8aadc7"


class UserBehavior(TaskSet):
    @task
    def UserLogin(self):
        login_data = self.client.post(
            "api/user/login/", {"username": "adityakalra", "password": "adityakalra@1234"}
        )
        time.sleep(0.05)
        # token = f"{login_data.json()['token']}"

    @task
    def GetAllUserPosts(self):
        self.client.get(
            "api/posts/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {token}",
            },
        )
        time.sleep(0.05)

        # post_slug = str(uuid4())
        # self.client.post(
        #     "api/post/",
        #     data={
        #         "title": f"{post_slug}",
        #         "content": f"This is a sample post {post_slug}.",
        #     },
        #     headers={
        #         "Content-Type": "application/json",
        #         "Authorization": f"Token {token}",
        #     },
        # )
        # self.client.get(
        #     "api/post/",
        #     data={"post_slug": f"{post_slug}"},
        #     headers={
        #         "Content-Type": "application/json",
        #         "Authorization": f"Token {token}",
        #     },
        # )
        # comment_uuid = str(uuid4())
        # self.client.patch(
        #     "api/post/",
        #     data={
        #         "post_slug": f"{post_slug}",
        #         "comment": f"This is a comment {comment_uuid}.",
        #     },
        #     headers={
        #         "Content-Type": "application/json",
        #         "Authorization": f"Token {token}",
        #     },
        # )


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    # wait_time = between(1, 5)


# NRAK-WEQTXTQ66QKV4UZ4VN5KXPMJF84
# NRAK-WYBQIX4U9LYDG57GQ21YGYWTHPO
# 4212b2f5a592bff37a28efddf252ee18FFFFNRAL
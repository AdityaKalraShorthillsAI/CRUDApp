from locust import HttpUser, TaskSet, task, between
from uuid import uuid4
import time
from faker import Faker
from api.utils import Utils

token = "e84f96feccbe8ebb5cc1305cd732385d63fc4a6d" # Postgres
# token = "f819ab6be6fd12b48ef0ce0286d6d7de5a8aadc7" # MongoDB Atlas
# token = "f819ab6be6fd12b48ef0ce0286d6d7de5a8aadc7" 


class UserBehavior(TaskSet):
    @task(1)
    def UserLogin(self):
        login_data = self.client.post(
            # "api/user/login/", {"username": "adityakalra", "password": "adityakalra@1234"}
            "api/user/login/", {"username": "adityakalra", "password": "Aditya@1234"}
        )

    @task(1)
    def GetAllUserPosts(self):
        self.client.get(
            "api/posts/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {token}",
            },
        )

    @task(1)
    def createTask(self):
        faker = Faker()
        post_slug = faker.text(max_nb_chars=50)
        content = faker.text(max_nb_chars=1000)
        
        self.client.post(
            "api/post/",
            data={
                "title": post_slug,
                "content": content
            },
            headers={
                "Authorization": f"Token {token}",
            },
        )


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
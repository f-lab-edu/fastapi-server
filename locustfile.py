from locust import HttpUser, task


class APITestUser(HttpUser):

    # @task
    # def hello(self):
    #     self.client.get("/")

    # 게시물 가져오는 엔드포인트
    @task
    def get_post(self):
        self.client.get("/api/posts/?page=1")

    # def create_user(self):
    #     data = {
    #         "user_id": "testuser",
    #         "password": "A1234567890",
    #         "nickname": "testnick",
    #     }
    #     self.client.post("/api/users/", json=data)

    # def login_user(self):
    #     data = {"user_id": "testuser", "password": "A1234567890"}
    #     with self.client.post(
    #         "/api/users/login", json=data, catch_response=True
    #     ) as response:
    #         if response.status_code == 200:
    #             res_data = json.loads(response.text)
    #             self.token = res_data["access_token"]

    # @task
    # def get_user_posts(self):
    #     headers = {"Authorization": f"{self.token}"}
    #     self.client.get("/api/users/testuser/posts/?page=1", headers=headers)

    # @task
    # def get_user_comments(self):
    #     headers = {"Authorization": f"{self.token}"}
    #     self.client.get("/api/users/testuser/comments/?page=1", headers=headers)

    # @task
    # def delete_user(self):
    #     headers = {"Authorization": f"{self.token}"}
    #     self.client.delete("/api/users/testuser", headers=headers)

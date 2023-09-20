from rest_framework import status
from core.fixtures.user import user
from core.fixtures.post import post
class TestPostViewSet:
    endpoint = '/api/post/'

    #게시물 목록을 불러오는 테스트
    def test_list(self,client, user,post):
        #유저 권한 인증
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    #특정 게시물을 불러오는 테스트
    def test_retrieve(self,client, user, post):
        #유저의 권한 인증
        client.force_authenticate(user=user)
        response = client.get(self.endpoint+str(post.public_id)+"/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == post.public_id.hex
        assert response.data['body'] == post.body
        assert response.data['author']['id'] == post.author.public_id.hex
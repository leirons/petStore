from tests.test_app import client,test_db


def test_create_user(test_db):
    data = {
        "password": 'test3004',
        "login": "test1",
        "email": "test5@gmail.com",
        "phone": "3805029065612",
        "first_name": "ivan",
        "second_name": "grechka"
    }
    response = client.post("/api/v1/user",json=data)
    print(response.text)
    assert response.status_code == 400

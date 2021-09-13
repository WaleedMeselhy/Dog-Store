import json


def test_create_dog(test_client):

    response = test_client.post(
        "/dog/",
        json={
            "dog_id": "dog_2",
            "name": "dog 1",
            "age": 10,
            "breed": "breed 1",
            "price": 2,
            "available": True,
        },
    )
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data["dog_id"] == "dog_2"

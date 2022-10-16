from tests.sample_requests.sync_request import get_and_parse_user
import responses


@responses.activate
def test_get_and_parse_users_works_properly():
    base_url = "http://someurl.com"
    endpoint_prefix = "/users/"
    user_id = 0

    responses.add(
        responses.GET,
        f"{base_url}{endpoint_prefix}{user_id}",
        json={"user": user_id},
        status=200,
        headers={}
    )

    response = get_and_parse_user(base_url, endpoint_prefix, user_id)

    assert type(response) is dict
    assert response["user"] == user_id

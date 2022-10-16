def test_delete_user_success(testing_app, valid_user_id):
    response = testing_app.delete(f"/users/{valid_user_id}")
    assert response.status_code == 204


def test_double_delete_user_fail(testing_app, valid_user_id):
    response = testing_app.delete(f"/users/{valid_user_id}")
    assert response.status_code == 204

    user_not_found_response = testing_app.delete(f"/users/{valid_user_id}")
    assert user_not_found_response.status_code == 404
    assert user_not_found_response.json() == "User doesn't exist"


def test_delete_invalid_user_id_fails(testing_app, invalid_user_delete_id):
    response = testing_app.delete(f"/users/{invalid_user_delete_id}")
    assert response.status_code == 404
    assert response.json() == "User doesn't exist"


def test_put_user_returns_correct_results(testing_app, sample_full_user_profile):
    user_id = 1
    response = testing_app.put(f"/users/{user_id}", json=sample_full_user_profile.dict())
    assert response.status_code == 204


def test_put_user_twice_returns_correct_results(testing_app, sample_full_user_profile):
    user_id = 1
    response = testing_app.put(f"/users/{user_id}", json=sample_full_user_profile.dict())
    assert response.status_code == 204

    response = testing_app.put(f"/users/{user_id}", json=sample_full_user_profile.dict())
    assert response.status_code == 204


def test_get_valid_user_returns_correct_result(testing_app, valid_user_id):
    response = testing_app.get(f"/users/{valid_user_id}")
    assert response.status_code == 200
    assert response.json()["long_bio"] == "My bio long description"


def test_rate_limit_works(testing_app, testing_rate_limit, valid_user_id):
    for i in range(testing_rate_limit * 2):
        response = testing_app.get(f"/users/{valid_user_id}")
        if 'x-app-rate-limit' not in response.headers:
            assert response.status_code == 429

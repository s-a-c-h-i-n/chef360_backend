from services.preferenceService import getPreference
from app import app as app
from flask_jwt_extended import create_access_token
import pytest

def test_get_preference(mocker):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """

    with app.test_client() as client:
        with app.app_context():

            mock_result = {
            "code":200,
            "message":"Success",
            "data":{
                    "EMAIL":"testuser@gmail.com",
                    "COOKWARE":['Pan', 'Stove','Microwave'],
                    "ALLERGICS":['Dairy', 'Nuts']
                }
            }
            mocker.patch('services.preferenceService.getPreference', return_value= mock_result)
            access_token = create_access_token('testuser')
            headers = {
            'Authorization': 'Bearer {}'.format(access_token)
            }
            response = client.get('/getPreference', headers = headers)

            json_response = response.get_json()

            print(json_response)

            assert response.status_code == 200
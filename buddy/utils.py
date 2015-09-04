from accounts.serializers import UserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    '''
    Normally JWT returns only a token -
    Angular needs a user id to handle some AJAX requests.
    '''

    user_id = UserSerializer(user).data['id']
    username = UserSerializer(user).data['username']

    return {
        'token': token,
        'user_id': user_id,
        'username': username
    }

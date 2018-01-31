from orkut.service import AuthService
from orkut.model import UserModel

class SearchService(object):

    @staticmethod
    def search_users(pattern):
        if AuthService.get_current_user():
            return UserModel.find_users(pattern)

        return None

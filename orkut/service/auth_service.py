from orkut.model import UserModel


class AuthService(object):
    __CURRENT_USER = None

    @staticmethod
    def get_friends(user):
        return list(UserModel.find_friends(user.id))

    @staticmethod
    def get_current_user():
        if AuthService.__CURRENT_USER:
            AuthService.__CURRENT_USER = UserModel.find_by_email_and_password(AuthService.__CURRENT_USER.email,
                                                                              AuthService.__CURRENT_USER.password)
        return AuthService.__CURRENT_USER

    @staticmethod
    def login(email, password):
        u = UserModel.find_by_email_and_password(email, password)
        if u is not None:
            AuthService.__CURRENT_USER = u
            return True

        return False

    @staticmethod
    def signup(name, email, password, gender, birthdate):
        u = UserModel(email, name, birthdate, gender, password)
        u.save()
        AuthService.__CURRENT_USER = u

    @staticmethod
    def change_current_user_password(old, new):
        u = AuthService.get_current_user()
        if u:
            if old == u.password:
                u.password = new
                u.save()
                return True

        return False

    @staticmethod
    def make_friendship(friend1, friend2):
        if AuthService.get_current_user():
            return friend1.make_internal_friendship(friend2) and friend2.make_internal_friendship(friend1)

        return False

    @staticmethod
    def is_friend(user):
        if AuthService.get_current_user():
            if user.id == AuthService.get_current_user().id:
                return True
            for u in AuthService.get_current_user().friends:
                if u.id == user.id:
                    return True
        return False

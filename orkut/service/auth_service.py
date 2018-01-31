from orkut.model import UserModel


class AuthService(object):
    __CURRENT_USER = None


    @staticmethod
    def get_current_user():
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
        if AuthService.__CURRENT_USER:
            if old == AuthService.__CURRENT_USER.password:
                AuthService.__CURRENT_USER.password = new
                AuthService.__CURRENT_USER.save()
                return True

        return False


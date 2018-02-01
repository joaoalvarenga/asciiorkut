from orkut.model import PostModel
from orkut.service import AuthService
from datetime import datetime


class PostService(object):

    @staticmethod
    def get_posts_from_current_user():
        if AuthService.get_current_user():
            return PostModel.find_by_actor(AuthService.get_current_user().actor)
        return None

    @staticmethod
    def get_last_five_posts_from_actor(actor_id):
        return PostModel.find_last_posts_from_actor(actor_id, 5)

    @staticmethod
    def insert_post(content):
        if AuthService.get_current_user():
            PostModel(created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), content=content,
                      actor=AuthService.get_current_user().actor,
                      publishable=AuthService.get_current_user().publishable).save()
            return True
        return False
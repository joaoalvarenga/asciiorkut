from orkut.model.interaction_model import InteractionModel
from orkut.service import AuthService


class InteractionService(object):

    @staticmethod
    def like_post(post):
        if InteractionModel.find_by_actor_and_interactable(AuthService.get_current_user().actor, post.interactable) is None:
            InteractionModel(AuthService.get_current_user().actor, post.interactable, date="2018-02-01").save()
from orkut.config import Config


class InteractionModel(object):
    def __init__(self, actor, interactable, date):
        self.actor = actor
        self.interactable = interactable
        self.date = date

    def save(self):
        with Config().get_db_connection().cursor() as cursor:
            cursor.execute('INSERT INTO interacoes (codigo_ator, codigo_interativo, data)  '
                           'VALUES("{}", "{}", "{}")'
                           .format(self.actor, self.interactable, self.date))
        Config().get_db_connection().commit()

    @staticmethod
    def find_by_actor_and_interactable(actor, interactable):
        with Config().get_db_connection().cursor() as cursor:
            cursor.execute('SELECT codigo_ator, codigo_interativo, data '
                           'FROM interacoes '
                           'WHERE interacoes.codigo_ator = {} and interacoes.codigo_interativo = {}'.format(actor, interactable))
            u = cursor.fetchone()
            if u is not None:
                return InteractionModel(actor=u[0], interactable=u[1], date=u[2])
            return None
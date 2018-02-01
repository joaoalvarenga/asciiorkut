from orkut.config import Config


class PostModel(object):
    def __init__(self, created_at, content, actor, publishable=None, interactable=None, belong=None, id=None,
                 likes=None):
        self.id = id
        self.created_at = created_at
        self.content = content
        self.actor = actor
        self.publishable = publishable
        self.interactable = interactable
        self.belong = belong
        self.likes = likes

    def save(self):
        if self.id is None:
            with Config().get_db_connection().cursor() as cursor:
                cursor.execute('INSERT INTO interativos VALUES(NULL)')
                cursor.execute('SELECT LAST_INSERT_ID()')
                self.interactable = cursor.fetchone()[0]

                cursor.execute('INSERT INTO publicaveis VALUES(NULL)')
                cursor.execute('SELECT LAST_INSERT_ID()')
                self.publishable = cursor.fetchone()[0]

                self.belong = 'NULL' if self.belong is None else self.belong

                cursor.execute('INSERT INTO publicacoes (data_publicacao, conteudo, codigo_ator, codigo_publicavel, '
                               'codigo_interativo, codigo_pertence) '
                               'VALUES("{}", "{}", {}, {}, {}, {})'
                               .format(self.created_at, self.content, self.actor, self.publishable, self.interactable,
                                       self.belong))
                cursor.execute('SELECT LAST_INSERT_ID()')
                self.id = cursor.fetchone()[0]
            Config().get_db_connection().commit()
        return self.id

    def check_if_actor_liked(self, actor):
        with Config().get_db_connection().cursor() as cursor:
            cursor.execute('SELECT COUNT(codigo_interativo) FROM interacoes WHERE interacoes.codigo_interativo = {} and interacoes.codigo_ator = {}}'
                           .format(self.interactable, actor))
            return cursor.fetchone()[0] > 0

    @staticmethod
    def get_likes(pid):
        with Config().get_db_connection().cursor() as cursor:
            cursor.execute('SELECT COUNT(codigo_interativo) FROM interacoes WHERE interacoes.codigo_interativo = {}'
                           .format(pid))
            return cursor.fetchone()[0]

    @staticmethod
    def find_by_actor(uid):
        with Config().get_db_connection().cursor() as cursor:
            cursor.execute('SELECT codigo, data_publicacao, conteudo, codigo_ator, codigo_publicavel, '
                           'codigo_interativo, codigo_pertence '
                           'FROM publicacoes '
                           'WHERE publicacoes.codigo_ator = {} '
                           'ORDER BY data_publicacao DESC '
                           .format(uid))
            for p in cursor.fetchall():
                yield PostModel(id=p[0], created_at=p[1], content=p[2], actor=p[3], publishable=p[4], interactable=p[5],
                                belong=p[6], likes=PostModel.get_likes(p[5]))

    @staticmethod
    def find_last_posts_from_actor(uid, limit=5):
        with Config().get_db_connection().cursor() as cursor:
            cursor.execute('SELECT codigo, data_publicacao, conteudo, codigo_ator, codigo_publicavel, '
                           'codigo_interativo, codigo_pertence '
                           'FROM publicacoes '
                           'WHERE publicacoes.codigo_ator = {} '
                           'ORDER BY data_publicacao DESC '
                           'LIMIT {}'
                           .format(uid, limit))
            for p in cursor.fetchall():
                yield PostModel(id=p[0], created_at=p[1], content=p[2], actor=p[3], publishable=p[4], interactable=p[5],
                                belong=p[6], likes=PostModel.get_likes(p[5]))

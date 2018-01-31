from orkut.config import Config


class UserModel(object):
    def __init__(self, email, name, birthdate, gender, password, id=None, friends=[], actor=None, publishable=None):
        self.name = name
        self.email = email
        self.birthdate = birthdate
        self.gender = gender
        self.password = password
        self.id = id
        self.friends = friends
        self.actor = actor
        self.publishable = publishable

    def save(self):
        if self.id is None:
            with Config().get_db_connection().cursor() as cursor:
                cursor.execute('INSERT INTO atores VALUES(NULL)')
                cursor.execute('SELECT LAST_INSERT_ID();')
                self.actor = cursor.fetchone()[0]

                cursor.execute('INSERT INTO publicaveis VALUES(NULL)')
                cursor.execute('SELECT LAST_INSERT_ID()')
                self.publishable = cursor.fetchone()[0]

                cursor.execute('INSERT INTO usuarios (email, nome, data_nascimento, sexo, senha, codigo_ator, codigo_publicavel)'
                               'VALUES("{}", "{}", "{}", "{}", "{}", {}, {});'.format(self.email, self.name, self.birthdate, self.gender, self.password,
                                                                 self.actor, self.publishable))
                cursor.execute('SELECT LAST_INSERT_ID();')
                self.id = cursor.fetchone()[0]
            Config().get_db_connection().commit()
        return self.id

    @staticmethod
    def find_friends(uid):
        with Config().get_db_connection().cursor() as cursor:
            cursor.execute('SELECT codigo, email, nome, data_nascimento, sexo, senha, codigo_ator, codigo_publicavel '
                           'FROM usuarios, sao_amigos '
                           'WHERE sao_amigos.codigo_usuario_1 = {} AND usuarios.codigo = sao_amigos.codigo_usuario_2'
                           .format(uid))
            for u in cursor.fetchall():
                yield UserModel(id=u[0], email=u[1], name=u[2], birthdate=u[3], gender=u[4], password=u[5], actor=u[6],
                                publishable=u[7])

    @staticmethod
    def find_by_email_and_password(email, password):
        with Config().get_db_connection().cursor() as cursor:
            cursor.execute('SELECT codigo, email, nome, data_nascimento, sexo, senha, codigo_ator, codigo_publicavel '
                           'FROM usuarios '
                           'WHERE usuarios.email = \'{}\' AND usuarios.senha = \'{}\''.format(email, password))
            u = cursor.fetchone()
            if u is not None:
                return UserModel(id=u[0], email=u[1], name=u[2], birthdate=u[3], gender=u[4], password=u[5], actor=u[6],
                                 publishable=u[7], friends=list(UserModel.find_friends(u[0])))
            return None

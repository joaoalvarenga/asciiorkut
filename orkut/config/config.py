import json

import pymysql


class Config:
    class __Config:
        def __init__(self, filename):
            self.__filename = filename
            with open(filename) as f:
                self.__config = json.loads(f.read())
            if not self.validate():
                raise Exception()

            self.__connection = pymysql.connect(host=self.get_db_host(), user=self.get_db_user(),
                                                password=self.get_db_password(), db=self.get_db_database())

        def get_db_host(self):
            return self.__config['dbHost']

        def get_db_user(self):
            return self.__config['dbUser']

        def get_db_password(self):
            return self.__config['dbPassword']

        def get_db_database(self):
            return self.__config['dbDatabase']

        def get_db_connection(self):
            return self.__connection

        def validate(self):
            keys = {'dbHost', 'dbUser', 'dbPassword', 'dbDatabase'}
            return set(self.__config.keys()) == keys

    instance = None

    def __init__(self, filename='config.json'):
        if not Config.instance:
            Config.instance = Config.__Config(filename)

    def __getattr__(self, name):
        return getattr(self.instance, name)

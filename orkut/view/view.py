# -*- coding: utf-8 -*-

import os

from orkut.service import AuthService, PostService, SearchService
from orkut.utils.utils import is_valid_email, is_valid_gender, is_valid_birthdate, check_isdigit_interval


def print_header():
    with open('header.txt') as f:
        print(f.read())


def get_op(interval):
    print('Insira sua escolha [{}-{}]: '.format(interval[0], interval[1]))
    op = input()
    while not check_isdigit_interval(op, interval):
        print('Opção inválida.')
        print('Escolha entre [{}-{}]: '.format(interval[0], interval[1]))
        op = input()

    return int(op)


def signup():
    os.system('reset')
    print_header()
    print('------------------------------ CADASTRO ------------------------------')
    print('---------------------------------------------------------  [-1] VOLTAR')

    print('Digite seu nome: ')
    name = input()
    if name == '-1':
        os.system('reset')
        initial()
       	return

    print('Digite um email: ')
    email = input()
    if email == '-1':
        os.system('reset')
        initial()
       	return

    while not is_valid_email(email):
        print('Digite um email válido: ')
        email = input()
        if email == '-1':
        	os.system('reset')
        	initial()
       		return

    print('Digite uma senha: ')
    password = input()
    if password == '-1':
        os.system('reset')
        initial()
       	return

    print('Digite seu sexo (M ou F): ')
    gender = input()
    if gender == '-1':
        os.system('reset')
        initial()
       	return

    while not is_valid_gender(gender):
        print('Digite seu sexo válido (M ou F): ')
        gender = input()
        if gender == '-1':
        	os.system('reset')
        	initial()
       		return

    print('Digite sua data de nascimento (ANO-MES-DIA): ')
    birthdate = input()
    if birthdate == '-1':
        os.system('reset')
        initial()
       	return

    while not is_valid_birthdate(birthdate):
        print('Digite sua data de nascimento válida (ANO-MES-DIA): ')
        birthdate = input()
        if birthdate == '-1':
        	os.system('reset')
        	initial()
       		return
    print('-------------------------------------------------------------------')

    AuthService.signup(name, email, password, gender, birthdate)
    home()


def change_password():
    os.system('reset')
    print_header()
    print('------------------------------ MEU PERFIL ------------------------------')
    print('Digite sua senha antiga')
    old = input()
    print('Digite a nova senha')
    new = input()
    if not AuthService.change_current_user_password(old, new):
        print('Senha antiga incorreta')
        print('--------------------------------------------------------------------------------')
        print('1. Tentar novamente')
        print('2. Voltar')
        print('--------------------------------------------------------------------------------')
        op = get_op((1, 2))

        if op == 1:
            change_password()
            return

    my_profile()


def list_friends():
    os.system('reset')
    print_header()
    print('------------------------------ AMIGOS ------------------------------')
    friends = AuthService.get_current_user().friends
    output = '\n'.join(['{}. {}'.format(i, friend.name) for i, friend in enumerate(friends)])
    print(output)
    print(str(len(friends)) + '. Voltar')
    print('--------------------------------------------------------------------')
    print('Escolha um perfil para exibir')
    op = get_op((0,len(friends)))

    if op >= len(friends):
        my_profile()
        return
    else:
        # exibindo perfil
        os.system('reset')
        print_header()
        friend = friends[op]
        print(friend.name)
        print('Data de Nascimento: {}'.format(friend.birthdate))
        print('Sexo: {}'.format({'M': 'masculino', 'F': 'feminino'}[friend.gender]))
        print('Email: {}'.format(friend.email))
        print('\nUltimas publicacoes:\n')
        last_posts = PostService.get_last_five_posts_from_actor(friend.actor)
        output = '\n\n'.join(['Postado em: {}\nConteúdo: {}'.format(post.created_at, post.content) for post in last_posts])
        print(output + '\n')
        print('------------------------------------------------------------------------')
        print('1. Ver amigos')
        print('2. Voltar')
        print('--------------------------------------------------------------------------------')
        op = get_op((1, 2))

        if op == 1:
            list_friends()
            return
        else:
            my_profile()
            return


def my_profile():
    os.system('reset')
    print_header()
    print('------------------------------ MEU PERFIL ------------------------------')
    user = AuthService.get_current_user()
    print(user.name)
    print('Data de Nascimento: {}'.format(user.birthdate))
    print('Sexo: {}'.format({'M': 'masculino', 'F': 'feminino'}[user.gender]))
    print('Email: {}'.format(user.email))
    print('Quantidade de amigos: {}'.format(len(user.friends)))
    print('------------------------------------------------------------------------')
    print('1. Listar Amigos')
    print('2. Mudar senha')
    print('3. Voltar')
    print('--------------------------------------------------------------------------------')
    op = get_op((1, 3))

    if op == 1:
        list_friends()
        return

    elif op == 2:
        change_password()
        return

    elif op == 3:
        home()
        return


def my_posts():
    os.system('reset')
    print_header()
    print('---------------------- MINHAS PUBLICACOES -------------------------')
    output = '\n\n'.join(['Postado em: {}\nConteúdo: {}'.format(post.created_at, post.content) for post in
                          PostService.get_posts_from_current_user()])
    print(output)
    print('--------------------------------------------------------------------------------')
    print('1. Nova publicação')
    print('2. Voltar')
    print('--------------------------------------------------------------------------------')
    op = get_op((1, 2))

    if op == 1:
        new_post()
        return
    elif op == 2:
        home()
        return


def new_post():
    os.system('reset')
    print_header()
    print('------------------------------ NOVA PUBLICACOES ------------------------------')
    print('Insira o conteúdo da publicação: ')
    conteudo = input()
    if not PostService.insert_post(conteudo):
        print('Não foi possível inserir essa nova publicação :(')

    print('------------------------------------------------------------------------------')
    my_posts()
    return


def search_users():
    os.system('reset')
    print_header()
    print('------------------------------ PESQUISA ---------------------------')
    print('Digite o nome do usuario que deseja procurar (ou -1 pra voltar):')
    nome = input()
    if nome == '-1':
        home()
        return

    users = (SearchService.search_users(nome))
    output = '\n'.join(['{}. {}'.format(indice, tuple[1]) for indice, tuple in enumerate(users)])
    print(output)

    print(str(len(users)) + '. Voltar')
    print('--------------------------------------------------------------------------------')
    op = get_op((0, (len(users))))

    if op == str(len(users)):
        home()
        return

    elif 0 <= int(op) < len(users):
        if not AuthService.make_friendship(AuthService.get_current_user().id, users[op][0]):
            print('Amizade Incompativel')

    else:
        # invalid input
        home()
        return

def login():
    os.system('reset')
    print_header()
    print('------------------------------ LOGIN ---------------------------------')
    print('---------------------------------------------------------  [-1] VOLTAR')
    print('Digite seu email: ')
    email = input()
    if email == '-1':
        os.system('reset')
        initial()
        return
    print('Digite sua senha: ')
    senha = input()
    if senha == '-1':
        os.system('reset')
        initial()
        return
    print('-------------------------------------------------------------------')

    while not AuthService.login(email, senha):
        print('------------------------------ LOGIN ------------------------------')
        print('Email ou senha incorretos :S')
        print('Digite seu email: ')
        email = input()
        if email == '-1':
            initial()
            return
        print('Digite sua senha: ')
        senha = input()
        if senha == '-1':
        	os.system('reset')
        	initial()
        	return
        print('-------------------------------------------------------------------')

    home()


def home():
    os.system('reset')
    print_header()
    print('------------------------------ MENU ------------------------------')
    print('1. Meu perfil')
    print('2. Minhas publicações')
    print('3. Pesquisar usuarios')
    print('4. Sair')
    print('-------------------------------------------------------------------')
    op = get_op((1, 4))
    if op == 1:
        my_profile()
        return

    elif op == 2:
        my_posts()
        return

    elif op == 3:
        search_users()
        return


def initial():
    print_header()
    print('------------------------------ MENU ------------------------------')
    print('1. Login')
    print('2. Cadastrar')
    print('3. Sair')
    print('------------------------------------------------------------------')
    op = get_op((1, 3))
    if op == 1:
        login()
        return

    elif op == 2:
        signup()
        return

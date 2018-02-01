# -*- coding: utf-8 -*-

import os

from orkut.service import AuthService, PostService, SearchService, InteractionService
from orkut.utils.utils import is_valid_email, is_valid_gender, is_valid_birthdate, check_isdigit_interval

SYSTEM_CONST = 'clear'


def print_orkut():
    with open('orkut_img.txt') as f:
        print(f.read())


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
    os.system(SYSTEM_CONST)
    print_header()
    print('------------------------------ CADASTRO ------------------------------')
    print('---------------------------- Insira [-1] a qualquer momento para voltar.')

    print('Digite seu nome: ')
    name = input()
    if name == '-1':
        os.system(SYSTEM_CONST)
        initial()
        return

    print('Digite um email: ')
    email = input()
    if email == '-1':
        os.system(SYSTEM_CONST)
        initial()
        return

    while not is_valid_email(email):
        print('Digite um email válido: ')
        email = input()
        if email == '-1':
            os.system(SYSTEM_CONST)
            initial()
            return

    print('Digite uma senha: ')
    password = input()
    if password == '-1':
        os.system(SYSTEM_CONST)
        initial()
        return

    print('Digite seu sexo (M ou F): ')
    gender = input()
    if gender == '-1':
        os.system(SYSTEM_CONST)
        initial()
        return

    while not is_valid_gender(gender):
        print('Digite seu sexo válido (M ou F): ')
        gender = input()
        if gender == '-1':
            os.system(SYSTEM_CONST)
            initial()
            return

    print('Digite sua data de nascimento (ANO-MES-DIA): ')
    birthdate = input()
    if birthdate == '-1':
        os.system(SYSTEM_CONST)
        initial()
        return

    while not is_valid_birthdate(birthdate):
        print('Digite sua data de nascimento válida (ANO-MES-DIA): ')
        birthdate = input()
        if birthdate == '-1':
            os.system(SYSTEM_CONST)
            initial()
            return
    print('-------------------------------------------------------------------')

    AuthService.signup(name, email, password, gender, birthdate)
    home()


def change_password():
    os.system(SYSTEM_CONST)
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


def show_profile(user):
    user.friends = AuthService.get_friends(user)
    os.system(SYSTEM_CONST)
    print_header()
    print(user.name)
    print('Data de Nascimento: {}'.format(user.birthdate))
    print('Sexo: {}'.format({'M': 'masculino', 'F': 'feminino'}[user.gender]))
    print('Email: {}'.format(user.email))
    print('Quantidade de amigos: {}'.format(len(user.friends)))
    print('\nUltimas publicacoes:\n')
    last_posts = PostService.get_last_five_posts_from_actor(user.actor)
    output = '\n\n'.join(
        ['Postado em: {}\nConteúdo: {}\nCurtidas: {}'.format(post.created_at, post.content, post.likes) for post in last_posts])
    print(output + '\n')
    is_friend = AuthService.is_friend(user)
    print('------------------------------------------------------------------------')
    print('1. Ver amigos')
    if not is_friend:
        print('2. Tornar amigo')
        print('3. Voltar')
    else:
        print('2. Curtir publicação')
        print('3. Voltar')
    print('--------------------------------------------------------------------------------')
    op = get_op((1, 3))

    if op == 1:
        list_friends(user)
        return
    else:
        if not is_friend:
            if op == 2:
                AuthService.make_friendship(AuthService.get_current_user(), user)
                show_profile(user)
                return
        else:
            if op == 2:
                like_posts(user)
                return

        home()
        return


def list_friends(user):
    os.system(SYSTEM_CONST)
    print_header()
    print('------------------------------ AMIGOS ------------------------------')
    friends = user.friends
    output = '\n'.join(['{}. {}'.format(i, friend.name) for i, friend in enumerate(friends)])
    print(output)
    print(str(len(friends)) + '. Voltar')
    print('--------------------------------------------------------------------')
    print('Escolha um perfil para exibir')
    op = get_op((0, len(friends)))

    if op >= len(friends):
        show_profile(user)
        return
    else:
        friends[op].friends = AuthService.get_friends(friends[op])
        show_profile(friends[op])
        return


def like_posts(user):
    os.system(SYSTEM_CONST)
    print_header()
    print('------------------------------ PUBLICAÇÕES ------------------------------')
    posts = list(PostService.get_posts_from_user(user))
    output = '\n\n'.join(
        ['{}. Postado em: {}\nConteúdo: {}'.format(i, post.created_at, post.content) for i, post in enumerate(posts)])
    print(output)
    print('------------------------------------------------------------------------')
    print(str(len(posts)) + '. Voltar')
    print('Escolha uma publicação para curtir')
    op = get_op((0, len(posts)))

    if op >= len(posts):
        show_profile(user)
        return
    else:
        InteractionService.like_post(posts[op])
        like_posts(user)
        return


def my_profile():
    os.system(SYSTEM_CONST)
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
        list_friends(user)
        return

    elif op == 2:
        change_password()
        return

    elif op == 3:
        home()
        return


def my_posts():
    os.system(SYSTEM_CONST)
    print_header()
    print('---------------------- MINHAS PUBLICACOES -------------------------')
    output = '\n\n'.join(
        ['Postado em: {}\nConteúdo: {}\nCurtidas: {}'.format(post.created_at, post.content, post.likes) for post in
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
    os.system(SYSTEM_CONST)
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
    os.system(SYSTEM_CONST)
    print_header()
    print('------------------------------ PESQUISA ---------------------------')
    print('Digite o nome do usuario que deseja procurar (ou -1 pra voltar):')
    nome = input()
    if nome == '-1':
        home()
        return

    users = list(SearchService.search_users(nome))
    output = '\n'.join(['{}. {}'.format(i, user.name) for i, user in enumerate(users)])
    print(output)

    print(str(len(users)) + '. Voltar')
    print('--------------------------------------------------------------------------------')
    op = get_op((0, (len(users))))

    if op == str(len(users)):
        home()
        return

    elif 0 <= int(op) < len(users):
        show_profile(users[op])
        # if not AuthService.make_friendship(AuthService.get_current_user().id, users[op][0]):
        #     print('Amizade Incompativel')

    else:
        # invalid input
        home()
        return


def login():
    os.system(SYSTEM_CONST)
    print_header()
    print('------------------------------ LOGIN ---------------------------------')
    print('Digite seu email (ou -1 para voltar): ')
    email = input()
    if email == '-1':
        os.system(SYSTEM_CONST)
        initial()
        return
    print('Digite sua senha: ')
    senha = input()
    if senha == '-1':
        os.system(SYSTEM_CONST)
        initial()
        return
    print('-------------------------------------------------------------------')

    while not AuthService.login(email, senha):
        print('------------------------------ LOGIN ------------------------------')
        print('Email ou senha incorretos :S')
        print('Digite seu email (ou -1 para voltar): ')
        email = input()
        if email == '-1':
            initial()
            return
        print('Digite sua senha: ')
        senha = input()
        if senha == '-1':
            os.system(SYSTEM_CONST)
            initial()
            return
        print('-------------------------------------------------------------------')

    home()


def home():
    os.system(SYSTEM_CONST)
    print_header()
    print('------------------------------ MENU ------------------------------')
    print('1. Meu perfil')
    print('2. Minhas publicações')
    print('3. Pesquisar usuarios')
    print('4. Desconectar')
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

    elif op == 4:
        initial()
        return


def initial():
    os.system(SYSTEM_CONST)
    print_header()
    print_orkut()
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

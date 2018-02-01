import os

from orkut.service import AuthService, PostService
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


def my_posts():
    os.system('reset')
    print_header()
    print('---------------------- MINHAS PUBLICACOES -------------------------')
    output = '\n\n'.join(['Postado em: {}\nConteúdo: {}'.format(post.created_at, post.content) for post in
                          PostService.get_posts_from_current_user()])
    print('-------------------------------------------------------------------')
    print('1. Nova publicação')
    print('2. Voltar')
    print('-------------------------------------------------------------------')
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
    print('3. Sair')
    print('-------------------------------------------------------------------')
    op = get_op((1, 3))
    if op == 1:
        home()
        return

    elif op == 2:
        my_posts()
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

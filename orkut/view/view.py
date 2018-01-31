import os

from orkut.service import AuthService
from orkut.utils.utils import is_valid_email, is_valid_gender, is_valid_birthdate, check_isdigit_interval


def print_header():
    with open('header.txt') as f:
        print(f.read())


def signup():
    os.system('clear')
    print_header()
    print('------------------------------ LOGIN ------------------------------')
    print('Digite seu nome: ')
    name = input()

    print('Digite um email: ')
    email = input()
    while not is_valid_email(email):
        print('Digite um email válido: ')
        email = input()

    print('Digite uma senha: ')
    password = input()

    print('Digite seu sexo (M ou F): ')
    gender = input()
    while not is_valid_gender(gender):
        print('Digite seu sexo válido (M ou F): ')
        gender = input()

    print('Digite sua data de nascimento (ANO-MES-DIA): ')
    birthdate = input()
    while not is_valid_birthdate(birthdate):
        print('Digite sua data de nascimento válida (ANO-MES-DIA): ')
        birthdate = input()
    print('-------------------------------------------------------------------')

    AuthService.signup(name, email, password, gender, birthdate)


def login():
    os.system('reset')
    print_header()
    print('------------------------------ LOGIN ------------------------------')
    print('Digite seu email: ')
    email = input()
    print('Digite sua senha: ')
    senha = input()
    print('-------------------------------------------------------------------')

    while not AuthService.login(email, senha):
        print('------------------------------ LOGIN ------------------------------')
        print('Email ou senha incorretos :S')
        print('Digite seu email: ')
        email = input()
        print('Digite sua senha: ')
        senha = input()
        print('-------------------------------------------------------------------')

    print('Logou!')


def initial():
    print_header()
    print('------------------------------ MENU ------------------------------')
    print('1. Login')
    print('2. Cadastrar')
    print('3. Sair')
    print('-------------------------------------------------------------------')
    print('Insira sua escolha [1-3]: ')
    op = input()
    while not check_isdigit_interval(op, (1, 3)):
        print('Opção inválida.')
        print('Escolha entre [1-3]: ')
        op = input()
    op = int(op)
    if op == 1:
        login()

    elif op == 2:
        signup()

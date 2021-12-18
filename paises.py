import json
import sys

import requests

URL_ALL = "https://restcountries.com/v2/all"
URL_NAME = "https://restcountries.com/v2/name/"

def calloutAPI(url):
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta.text
    except:
        print('Erro ao fazer requisição em: ', url)


def parsing(resposta_texto):
    try:
        return json.loads(resposta_texto)
    except:
        print('Erro ao fazer parsing.')


def verificar_status(resposta):
    resposta_parsing = parsing(resposta)
    if 'status' in resposta_parsing:
        if resposta_parsing['status'] == 404:
            return False
    else:
        return True

def count_contries():
    resposta = calloutAPI(URL_ALL)
    if resposta:
        lista_de_paises = parsing(resposta)
        if lista_de_paises:
            print("Há {} países no mundo".format(len(lista_de_paises)))


def show_population(nome_pais):
    resposta = calloutAPI("{}/{}".format(URL_NAME, nome_pais))
    status = verificar_status(resposta)

    if status:
        lista_paises = parsing(resposta)
        if lista_paises:
            for pais in lista_paises:
                print("{}: {}".format(pais['name'], pais['population']))
    else:
        print('País não encontrado.')


def show_currencies(nome_pais):
    resposta = calloutAPI("{}/{}".format(URL_NAME, nome_pais))
    status = verificar_status(resposta)

    if status:
        lista_paises = parsing(resposta)
        if lista_paises:
            for pais in lista_paises:
                print('****Moeda(s) do(a): ', pais['name'] + '****')
                moedas = pais['currencies']
                for moeda in moedas:
                    print("{} - {}".format(moeda['name'], moeda['code']))
    else:
        print('País não encontrado.')


def ler_nome_do_pais():
    try:
        nome_do_pais = sys.argv[2]
        return nome_do_pais
    except:
        print("É necessário informar o nome do país")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("****Bem vindo ao sistema de países****")
        print("Uso: python paises.py <acao> <nome do país>")
        print("Ações disponíveis: contagem, moeda, populacao")

    else:
        argumento1 = sys.argv[1]
        if argumento1 == "contagem":
            count_contries()
            exit(0)
        elif argumento1 == "moeda":
            nome_do_pais = ler_nome_do_pais()
            if nome_do_pais:
                show_currencies(nome_do_pais)

        elif argumento1 == "populacao":
            nome_do_pais = ler_nome_do_pais()
            if nome_do_pais:
                show_population(nome_do_pais)

        else:
            print("Argumento inválido.")
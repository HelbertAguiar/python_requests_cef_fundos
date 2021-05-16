import requests
from bs4 import BeautifulSoup
import time


def printRequest(r, method, url_solicitada, form=None):
    print('\nURL Solicitada da requisicao: '.ljust(28, ' ') + url_solicitada)
    print('URL Efetiva da requisicao: '.ljust(30, ' ') + r.url)
    print('History redirect: '.ljust(30, ' ') + str(r.history))
    print('Status code: '.ljust(30, ' ') +
          str(r.status_code) + '\tReason: ' + str(r.reason))
    print('Elapsed: '.ljust(30, ' ') + str(r.elapsed) +
          '\tEnconding: ' + str(r.encoding))
    if form != None:
        printForm(form)
    print('\nOs headers da requisicao do ' + method + ' sao: ' + '\n')
    print("\n".join("{} {}".format(k.ljust(28, ' '), v.ljust(30, ' '))
                    for k, v in r.request.headers.items()))
    print('\nOs headers da resposta do ' + method + ' sao: ' + '\n')
    print("\n".join("{} {}".format(k.ljust(28, ' '), v.ljust(30, ' '))
                    for k, v in r.headers.items()))
    print('\n' + ''.ljust(158, '='))


def printForm(form):
    print('\nForm da requisicao:')
    print("\n".join("{} ".format(k) for k in form.items()))


def parse_and_print(req, data_inserir, classe):

    soup = BeautifulSoup(req.content, "html.parser")
    table = soup.findAll("table")[2].find('tbody')
    tags_tr = table.findChildren("tr", recursive=False)

    for tr in tags_tr:
        nome_fundo = (tr.td.a.text).strip().upper().replace('Õ', 'O').replace(
            'Ç', 'C').replace('Á', 'A').replace('É', 'E').replace('Ã', 'A').replace('Í', 'I')
        nome_fundo = nome_fundo.encode("ascii", errors="ignore").decode()
        taxa_adm = tr.findAll('td')[4].text

        try:
            perfil = tr.find(text='Risco:').findNext('td').text
        except:
            perfil = 'Unknown'

        cota = tr.findChildren("td", recursive=False)[3].text.strip()
        patrimonio = tr.findChildren("td", recursive=False)[8].text.strip()

        print('{};{};{};{};{};{};{}'.format(data_inserir,
                                         nome_fundo, taxa_adm, perfil, cota, patrimonio, classe))


def leitura_arquivo_data():

    lista_datas = []
    with open('input_datas', 'r') as reader:
        for line in reader.readlines():
            lista_datas.append(line.split())

    return lista_datas


with requests.Session() as session:

    session.headers.update(
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'})

    url_custom = 'http://www.fundos.caixa.gov.br/sipii/pages/public/listar-fundos-internet.jsf'
    r = session.get(url_custom)
    # printRequest(r, 'GET', url_custom)

    lista_classes_fundos = []
    lista_classes_fundos.append('RENDA FIXA SIMPLES')
    lista_classes_fundos.append('RENDA FIXA')
    lista_classes_fundos.append('RENDA FIXA REFERENCIADO')
    lista_classes_fundos.append('RENDA FIXA CURTO PRAZO')
    lista_classes_fundos.append('MULTIMERCADO')
    lista_classes_fundos.append('CAMBIAL')
    lista_classes_fundos.append('AÇÕES')
    lista_classes_fundos.append('FUNDO DE ÍNDICE')
    lista_classes_fundos.append('FUNDOS MÚTUOS DE PRIVATIZAÇÃO')

    lista_datas = leitura_arquivo_data()

    for data in lista_datas:

        data_inserir = str(data).replace(
            '\'', '').replace('[', '').replace(']', '')

        for classe in lista_classes_fundos:

            soup = BeautifulSoup(r.content, "html.parser")
            javaxFacesViewState = soup.find(id="javax.faces.ViewState").attrs['value']

            if classe == 'RENDA FIXA SIMPLES':
                index = 0
                ordemExibicao = 5
                codigoSegmentoSelecionado = 4
            elif classe == 'RENDA FIXA':
                index = 1
                ordemExibicao = 5
                codigoSegmentoSelecionado = 4
            elif classe == 'RENDA FIXA REFERENCIADO':
                index = 2
                ordemExibicao = 5
                codigoSegmentoSelecionado = 4
            elif classe == 'RENDA FIXA CURTO PRAZO':
                index = 3
                ordemExibicao = 5
                codigoSegmentoSelecionado = 4
            elif classe == 'MULTIMERCADO':
                index = 4
                ordemExibicao = 5
                codigoSegmentoSelecionado = 4
            elif classe == 'CAMBIAL':
                index = 5
                ordemExibicao = 5
                codigoSegmentoSelecionado = 4
            elif classe == 'AÇÕES':
                index = 6
                ordemExibicao = 5
                codigoSegmentoSelecionado = 4
            elif classe == 'FUNDO DE ÍNDICE':
                index = 7
                ordemExibicao = 5
                codigoSegmentoSelecionado = 4
            elif classe == 'FUNDOS MÚTUOS DE PRIVATIZAÇÃO':
                index = 8
                ordemExibicao = 1
                codigoSegmentoSelecionado = 1

            form = {'formPrincipal': 'formPrincipal',
                    'ordemExibicao': ordemExibicao,
                    'codSegmentoSelecionado': codigoSegmentoSelecionado,
                    'indexClasseFundo': index,
                    'dtBusca': data_inserir,
                    'pesquisar': '',
                    'j_idt88:2:gridPesquisar_length': '100',
                    'impt_pesquisa': '',
                    'tabAtiva': classe,
                    'javax.faces.ViewState': javaxFacesViewState,
                    'btn-consultar-1': 'btn-consultar-1'
                    }

            r = session.post(url_custom, data=form, allow_redirects=True)
            parse_and_print(r, data_inserir, classe)
            time.sleep(5)

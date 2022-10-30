import requests
import json
import os
import time
import pymysql



while(1):
    os.system("cls")
           
    dados = requests.get('https://resultados.tse.jus.br/oficial/ele2022/545/dados-simplificados/br/br-c0001-e000545-r.json')

    dadosEmJson = json.loads(dados.content)

    candidatos = []
    votos = []
    porcentagem = []
    porcentagemTotal = dadosEmJson['pesi']
    ultAtualizacao = dadosEmJson['dg'] + ' ' + dadosEmJson['hg']
    
    for informacoes in dadosEmJson['cand']:
        if informacoes['seq'] in ['1', '2']:
            candidatos.append(informacoes['nm'])
            votos.append(informacoes['vap'])
            porcentagem.append(informacoes['pvap'])

    for i in range(len(candidatos)):
        conexao = pymysql.connect(db='eleicoes', user='root', passwd='')
        cursor = conexao.cursor()
        cursor.execute('insert into candidatos(nome, votos, porcentagem, hora, porcentagemApurada) values ("'+candidatos[i]+'", "'+votos[i]+'", "'+porcentagem[i]+'", "'+ultAtualizacao+'", "'+porcentagemTotal+'")')
        conexao.commit()
        conexao.close()

    print("TOTAL APURADO: {}%".format(porcentagemTotal))
    print("")
    for i in range(len(candidatos)):
        print("CANDIDATO: {}".format(candidatos[i]))
        print("VOTOS: {}".format(votos[i]))
        print("PORCENTAGEM: {}%".format(porcentagem[i]))
        print("")

    print("ATUALIZADO EM {}".format(ultAtualizacao))
    print("")
    time.sleep(60)
    

    
#IMPORTANDO AS BIBLIOTECAS QUE VAMOS UTILIZAR 
from textwrap import dedent
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

#
#UTILIZANDO O PANDAS DATA READER PARA PEGAR DADOS DO YAHOO, REFERENTES AS AÇÕES DOS BANCOS E EXIBE O RESULTADO
#
dados_bancarios = pdr.get_data_yahoo(['ITUB4.SA', 'BBAS3.SA', 'SANB4.SA', 'BBDC4.SA', '^BVSP'], 
                                        start = "2010-01-01", end = "2022-10-01")['Adj Close']

#
#UTILIZANDO O PANDAS PARA LER DADOS DO ARQUIVO EXCEL, DANDO UMA COLUNA DE REFERÊNCIA E EXIBE RESULTADO
#
lucro_bancos = pd.read_excel('C:/Users/adria/Desktop/Estudos/Python MF/Minicurso_python_planilha_2022.xlsx', index_col = "data")

#
#ATRIBUINDO NOMES PARA FACILITAR MANIPULAÇÃO
#
itau = dados_bancarios['ITUB4.SA']
banco_brasil = dados_bancarios['BBAS3.SA']
santander = dados_bancarios['SANB4.SA']
bradesco = dados_bancarios['BBDC4.SA']
indice_ibovespa = dados_bancarios['^BVSP']

#
#CRIANDO FUNÇÃO QUE MOSTRA O RETORNO DAS AÇÕES (O VETOR -1 INDICA O VALOR DA ULTIMA POSIÇÃO)
#ESSE CALCULO É FEITO DA SEGUINTE FORMA: (VALOR FINAL / VALOR INICIAL) - 1
#
def retorno(item):
    retorno = (item[-1]/item[0]) - 1

    return retorno

#
#ATRIBUI A FUNÇÃO DE RETORNO A VARIAVEL, ESPECIFICA O ITEM E EXIBE RESULTADO
#
retorno_itau = retorno(item = itau)
retorno_banco_brasil = retorno(item = banco_brasil)
retorno_santander = retorno(item = santander)
retorno_bradesco = retorno(item = bradesco)

retorno_indice = retorno(item = indice_ibovespa)

#
#CRIANDO DATA FRAME (MATRIZ) PARA ORGANIZAR OS DADOS VIZUALMENTE
#
df_retornos = pd.DataFrame(data = {'retornos': [retorno_itau, retorno_banco_brasil, 
                                    retorno_santander, retorno_bradesco]}, 
                                    index = ["itau", "banco do brasil", "santander", "bradesco"])

#
#ORGANIZANDO OS VALORES, DEIXANDO EM VALORES DECIMAIS
#
df_retornos['retornos'] = df_retornos['retornos'] * 100

#
#EXIBINDO VALORES EM ORDEM DE RETORNO
#
df_retornos = df_retornos.sort_values(by = "retornos", ascending = False)

##################################################################################################

#
#CRIANDO O GRÁFICO DE RETORNO DAS AÇÕES A PARTIR DA BIBLIOTECA MATPLOTLIB
#
fig, ax = plt.subplots()
#DEFINDO EIXOS X E Y
ax.bar(df_retornos.index , df_retornos['retornos'])
#COLOCANDO EIXO Y EM %
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
#TROCANDO FONTE DO EIXO X
plt.xticks(fontsize = 10)
#EXIBIT GRÁFICO
plt.show()

#
#CRIANDO VARIÁVEL QUE EXIBE O DELTA DOS LUCROS ENTRE BANCOS, E ORGANIZA OS DADOS
#
delta_lucro = (lucro_bancos.iloc[-1] / lucro_bancos.iloc[0]) - 1
delta_lucro = delta_lucro * 100
delta_lucro = delta_lucro.sort_values(ascending = False)

#
#CRIANDO O GRÁFICO DE LUCRO A PARTIR DA BIBLIOTECA MATPLOTLIB
#
fig, ax = plt.subplots()
#DEFINDO EIXOS X E Y
ax.bar(delta_lucro.index , delta_lucro)
#COLOCANDO EIXO Y EM %
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
#TROCANDO FONTE DO EIXO X
plt.xticks(fontsize = 10)
#EXIBIT GRÁFICO
plt.show()

#
#CRIANDO UMA FUNÇÃÕ QUE RECEBE UMA AÇÃO E O PERÍODO A SER EXIBIDO, E RETORNA SÓ OS VALORES DO PERÍODO SELECIONADO
#
def resample_periodo(acao, periodo):

    #CRIA VARIAVEL E PEGA O PERIDO ESPECIFICADO "Y" "M"...
    acao_novo_periodo = acao.resample(f"{periodo}").last()
    #TROCA OS VALORES PARA PERCENTUAL
    acao_novo_periodo = acao_novo_periodo.pct_change()
    #RETIRA OS VALORES NULOS
    acao_novo_periodo = acao_novo_periodo.dropna()

    return acao_novo_periodo

#
#CRIANDO VAR QUE ARMAZENA OS RESULTADOS DO PERÍODO SELECIONADO
#
itau_ano_ano = resample_periodo(itau, "Y")
bb_ano_ano = resample_periodo(banco_brasil, "Y")
santander_ano_ano = resample_periodo(santander, "Y")
bradesco_ano_ano = resample_periodo(bradesco, "Y")

ibov_ano_ano = resample_periodo(indice_ibovespa, "Y")

#
#FUNÇÃO QUE FAZ A COMPARAÇÃO ENTRE AÇÕES/INDICE E EXIBE O GRÁFICO DESSA VARIAÇÃO
#
def compara_perform(long, short, periodo):

    delta_long = resample_periodo(long, periodo)
    delta_short = resample_periodo(short, periodo)

    resperform = delta_long - delta_short

    plt.plot(resperform)

#EXIBE
compara_perform(itau, indice_ibovespa, "Y")
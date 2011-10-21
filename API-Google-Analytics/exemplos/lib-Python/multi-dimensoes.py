#!/usr/bin/python
# -*- coding: utf-8 -*-

"""InterCon 2011 - Explorando a API do Google Analytics
Este script requer a biblioteca gdata - http://code.google.com/p/gdata-python-client/
"""

__author__ = 'vanessa@weureka.com (Vanessa Sabino)'


import sys
import auth
import gdata.analytics.client
import gdata.client
import datetime

APP_NAME = 'InterCon 2011'
TABLE_ID = 'ga:33702370' # id do perfil a ser usado por padrão 

def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(argv) > 1:
        TABLE_ID = argv[1]
        
    my_client = autenticar()
    exibir_dados(my_client)


def autenticar():
    u"""Gera um cliente com o token de autenticação"""

    my_client = gdata.analytics.client.AnalyticsClient(source=APP_NAME)
    my_auth_helper = auth.AuthRoutineUtil()

    my_auth = auth.OAuthRoutine(my_client, my_auth_helper)

    try:
        my_client.auth_token = my_auth.GetAuthToken()

    except auth.AuthError, error:
        print error.msg
        sys.exit(1)
        
    return my_client

def gerar_query():
    u"""Monta a query com os parâmetros definidos"""

    return gdata.analytics.client.DataFeedQuery({
            'ids': TABLE_ID,
            'start-date': (datetime.date.today() + datetime.timedelta(days=-30)).isoformat(),
            'end-date': datetime.date.today().isoformat(),
            'dimensions': 'ga:medium,ga:source,ga:campaign,ga:adContent',
            'metrics': 'ga:visits,ga:goalCompletionsAll',
            'max-results': '10000'})

def exibir_dados(my_client):
    u"""Executa a query e imprime na tela os dados"""

    try:
        data_query = gerar_query()
        feed = my_client.GetDataFeed(data_query)

        print '\t'.join(['Mídia'.ljust(25), 'Origem'.ljust(25), 'Campanha'.ljust(25), 'Versão'.ljust(25), 'Visitas', 'Metas'])

        for entry in feed.entry:
            line = []
            for dim in entry.dimension:
                try:
                    line.append(dim.value.encode('latin-1').ljust(25))
                except:
                    line.append('ERROR')
            for met in entry.metric:
                line.append(met.value)
            print '\t'.join(line)

    except gdata.client.Unauthorized, error:
        print '%s\nExcluindo token.' % error
        my_auth_helper.DeleteAuthToken()
        sys.exit(1)

if __name__ == '__main__':
    main()

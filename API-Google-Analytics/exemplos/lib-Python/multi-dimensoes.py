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
TABLE_ID = 'ga:33702370'

def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(argv) > 1:
        TABLE_ID = argv[1]

    # AuthSub
    my_client = gdata.analytics.client.AnalyticsClient(source=APP_NAME)
    my_auth_helper = auth.AuthRoutineUtil()

    my_auth = auth.OAuthRoutine(my_client, my_auth_helper)

    try:
        my_client.auth_token = my_auth.GetAuthToken()

    except auth.AuthError, error:
        print error.msg
        sys.exit(1)

    try:
        data_query = GetDataFeedQuery()
        feed = my_client.GetDataFeed(data_query)

        print '\t'.join(['Mídia', 'Origem', 'Campanha', 'Versão', 'Visitas', 'Metas'])

        for entry in feed.entry:
            line = []
            for dim in entry.dimension:
                try:
                    line.append(dim.value.encode('latin-1'))
                except:
                    line.append('ERROR')
            for met in entry.metric:
                line.append(met.value)
            print '\t'.join(line)

    except gdata.client.Unauthorized, error:
        print '%s\nDeleting token file.' % error
        my_auth_helper.DeleteAuthToken()
        sys.exit(1)

def GetDataFeedQuery():

    return gdata.analytics.client.DataFeedQuery({
            'ids': TABLE_ID,
            'start-date': (datetime.date.today() + datetime.timedelta(days=-30)).isoformat().replace('T00:00:00',''),
            'end-date': datetime.date.today().isoformat().replace('T00:00:00',''),
            'dimensions': 'ga:medium,ga:source,ga:campaign,ga:adContent',
            'metrics': 'ga:visits,ga:goalCompletionsAll',
            'max-results': '10000'})

if __name__ == '__main__':
    main()

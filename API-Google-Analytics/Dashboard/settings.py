#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


port = os.environ['SERVER_PORT']

if port and port != '80':
	HOST_NAME = '%s:%s' % (os.environ['SERVER_NAME'], port)
else:
	HOST_NAME = os.environ['SERVER_NAME']

DEBUG = True

# Dimensions dictionary
DIMENSIONS = {
	# D1. Visitor
	'ga:browser' : 'Navegador',
	'ga:browserVersion' : 'Versão do Navegador',
	'ga:city' : 'Cidade',
	'ga:connectionSpeed' : 'Velocidade de Conexão',
	'ga:continent' : 'Continente',
	# 'ga:countOfVisits' : 'Numero de Visitas', (deprecated)
	'ga:country' : 'País',
	'ga:date' : 'Data',
	'ga:day' : 'Dia',
	'ga:daysSinceLastVisit' : 'Dias desde a última visita',
	'ga:flashVersion' : 'Versão do flash',
	'ga:hostname' : 'Hostname',
	'ga:hour' : 'Hora',
	'ga:isMobile' : 'Mobile?',
	'ga:javaEnabled' : 'Java?',
	'ga:language' : 'Lingua',
	'ga:latitude' : 'Latitude',
	'ga:longitude' : 'Longitude',
	'ga:month' : 'Mês',
	'ga:networkDomain' : 'Domínio de Rede',
	'ga:networkLocation' : 'Local da Rede',
	'ga:operatingSystem' : 'Sistema Operacional',
	'ga:operatingSystemVersion' : 'Versão do SO',
	'ga:pageDepth' : 'Profundidade de Página',
	'ga:region' : 'Região',
	'ga:screenColors' : 'Cores da Tela',
	'ga:screenResolution' : 'Resolução da Tela',
	'ga:subContinent' : 'Sub-continente',
	'ga:userDefinedValue' : 'Valor Customizado',
	'ga:visitCount' : 'Contagem da Visitas',
	'ga:visitLength' : 'Duração da Visita',
	'ga:visitorType' : 'Tipo de Visitante',
	'ga:week' : 'Semana',
	'ga:year' : 'Ano',
	# D2. Campaign
	'ga:adContent' : 'Conteúdo do Anúncio',
	'ga:adGroup' : 'Grupo do Anúncio',
	'ga:adSlot' : 'Slot do Anúncio',
	'ga:adSlotPosition' : 'Posição do Anúncio',
	'ga:campaign' : 'Campanha',
	'ga:keyword' : 'Palavra Chave',
	'ga:medium' : 'Meio',
	'ga:referralPath' : 'Referral Path',
	'ga:source' : 'Origem',
	# D3. Content
	'ga:exitPagePath' : 'Página de Saída',
	'ga:landingPagePath' : 'Página de Entrada',
	'ga:nextPagePath' : 'Próxima Página',
	'ga:pagePath' : 'Página',
	'ga:pageTitle' : 'Título da Página',
	'ga:previousPagePath' : 'Página Anterior',
	'ga:secondPagePath' : 'Segunda Página',
	# D4. Ecommerce
	'ga:affiliation' : 'Afiliado',
	'ga:daysToTransaction' : 'Dias para Transação',
	'ga:productCategory' : 'Categoria de Produto',
	'ga:productName' : 'Nome do Produto',
	'ga:productSku' : 'Produto SKU',
	'ga:transactionId' : 'Id da Transação',
	'ga:visitsToTransaction' : 'Visitas para Transação',
	# D5. Internal Search
	'ga:searchCategory' : 'Categoria de Busca',
	'ga:searchDestinationPage' : 'Página de destino da Busca',
	'ga:searchKeyword' : 'Palavra buscada',
	'ga:searchKeywordRefinement' : 'Refinamento de Busca',
	'ga:searchStartPage' : 'Página de Busca',
	'ga:searchUsed' : 'Busca Usada',
	# D6. Custom Variables
	'ga:customVarName(n)' : 'Nome da Variável',
	'ga:customVarValue(n)' : 'Valor da Vaiável',
	# D7. Events
	'ga:eventCategory' : 'Categoria do Evento',
	'ga:eventAction' : 'Ação do Evento',
	'ga:eventLabel' : 'Label do Evento',
}

# Metrics Dictionary
METRICS = {
	# M1. Visitor
	'ga:bounces' : 'Bounces',
	'ga:entrances' : 'Entradas',
	'ga:exits' : 'Saídas',
	'ga:newVisits' : 'Novas Visitas',
	'ga:pageviews' : 'Pageviews',
	'ga:timeOnPage' : 'Tempo na página',
	'ga:timeOnSite' : 'Tempo no site',
	'ga:visitors' : 'Visitantes',
	'ga:visits' : 'Visitas',
	# M2. Campaign
	'ga:adCost' : 'adCost',
	'ga:adClicks' : 'adClicks',
	'ga:CPC' : 'CPC',
	'ga:CPM' : 'CPM',
	'ga:CTR' : 'CTR',
	'ga:impressions' : 'Impressões',
	# M3. Content
	'ga:uniquePageviews' : 'Pageviews Únicos',
	# M4. Ecommerce
	'ga:itemQuantity' : 'Quantidade',
	'ga:itemRevenue' : 'Revenue',
	'ga:transactions' : 'Transações',
	'ga:transactionRevenue' : 'Faturamento',
	'ga:transactionShipping' : 'Custo de Entrega',
	'ga:transactionTax' : 'Taxas',
	'ga:uniquePurchases' : 'Compras Únicas',
	# M5. Internal Search
	'ga:searchDepth' : 'Profundidade de Busca',
	'ga:searchDuration' : 'Duração da Busca',
	'ga:searchExits' : 'Saídas de Busca',
	'ga:searchRefinements' : 'Refinamentos de Busca',
	'ga:searchUniques' : 'Buscas Únicas',
	'ga:searchVisits' : 'Visitas com Busca',
	# M6. Goals
	'ga:goal(n)Completions' : 'Meta %d Completa',
	'ga:goalCompletionsAll' : 'Metas Completadas',
	'ga:goal(n)Starts' : 'Início da Meta %d',
	'ga:goalStartsAll' : 'Início das Metas',
	'ga:goal(n)Value' : 'Valor da Meta %d',
	'ga:goalValueAll' : 'Valores das Metas',
	# M7. Events
	'ga:totalEvents' : 'Eventos',
	'ga:uniqueEvents' : 'Eventos Únicos',
	'ga:eventValue' : 'Valor de Eventos',
}

CALCULATED_METRICS = {
	'dpc:bounceRate' : 'ga:bounces/ga:entrances',
	'dpc:returningVisits' : 'ga:visits - ga:newVisits',
}


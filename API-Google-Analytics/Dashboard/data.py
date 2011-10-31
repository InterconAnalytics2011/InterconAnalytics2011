#!/usr/bin/env python
# -*- coding: utf-8 -*-

# solve integer division issue
from __future__ import division

def splitThousands( s, tSep=',', dSep='.'):
    '''Splits a general float on thousands. GIGO on general input'''
    if s == None:
        return 0
    if not isinstance( s, str ):
        s = str( s )

    cnt=0
    numChars=dSep+'0123456789'
    ls=len(s)
    while cnt < ls and s[cnt] not in numChars: cnt += 1

    lhs = s[ 0:cnt ]
    s = s[ cnt: ]
    if dSep == '':
        cnt = -1
    else:
        cnt = s.rfind( dSep )
    if cnt > 0:
        rhs = dSep + s[ cnt+1: ]
        s = s[ :cnt ]
    else:
        rhs = ''

    splt=''
    while s != '':
        splt= s[ -3: ] + tSep + splt
        s = s[ :-3 ]

    return lhs + splt[ :-1 ] + rhs

import os
import logging
import datetime
import math

import settings
import gviz_api
import gdata.analytics.client
import gdata.alt.appengine
import gdata.gauth

from urllib import unquote

from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from gdata.client import RequestError
from google.appengine.api.urlfetch import DownloadError
from google.appengine.api import memcache

# Last Year Visits
class LastYearVisits(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()

		# GA API Base parameters
		kwargs = {
			'ids' : 'ga:9060294', # comma-separated string of analytics accounts.
			'start-index' : '1', # used in combination with max-results to pull more than 1000 entries, defaults to 1
			}
		
		# populate GA API parameters 
		kwargs['max-results'] = self.request.get('max-results','1000')
		kwargs['dimensions'] = self.request.get('dimensions','')
		kwargs['metrics'] = self.request.get('metrics','ga:visits')
		kwargs['sort'] = self.request.get('sort','')
		kwargs['filters'] = self.request.get('filters','')
		
		if self.request.get('segment',''):
			kwargs['segment'] = self.request.get('segment','')
			
		# last year
		d = datetime.date.today()
		last_year = d.year - 1
		
		kwargs['end-date'] = self.request.get('end-date', str(datetime.date(last_year, 12, 31)))
		kwargs['start-date'] = self.request.get('start-date', str(datetime.date(last_year, 1, 1)))

		# Search cache
		cache_key = user.user_id() + str(kwargs)
		total = memcache.get(cache_key)
		
		if total is not None:
			self.response.out.write('%.2f' % total)
			return
		
		logging.info('Cache Miss')

		# Initialize a client to talk to Google Data API services.
		auth_token = gdata.gauth.ae_load(user.user_id())
		client = gdata.analytics.client.AnalyticsClient()
		
	
		# Query GA API
		try:
			logging.debug(str(kwargs))
			query = gdata.analytics.client.DataFeedQuery(kwargs)
			feed = client.get_data_feed(query, auth_token)
		except RequestError:
			logging.error('RequestError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='invalid_request',
				message='Request Error',
				tqx=self.request.get('tqx','out:json')))
			return
		except DownloadError:
			# usually triggers for GA API timeouts
			logging.error('DownloadError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='internal_error',
				message='API Timeout',
				tqx=self.request.get('tqx','out:json')))
			return

		last_year_total = ''

		if feed.entry:
			# dispense title
			for entry in feed.entry:
				if entry.dimension:
					for dimension in entry.dimension:
						pass
				for metric in entry.metric:
					pass
				break
			
			# get visits
			for entry in feed.entry:
				if entry.dimension:
					for dimension in entry.dimension:
						pass
				for metric in entry.metric:
					last_year_total = int(metric.value)
		
		in_million = last_year_total / 1000000
		
		# Cache response
		memcache.set(cache_key, in_million, 60*60*12)
		# Write
		self.response.out.write('%.2f' % in_million)

	
# Current Year Visits
class CurrentYearVisits(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()

		# GA API Base parameters
		kwargs = {
			'ids' : 'ga:9060294', # comma-separated string of analytics accounts.
			'start-index' : '1', # used in combination with max-results to pull more than 1000 entries, defaults to 1
			}
		
		# populate GA API parameters 
		kwargs['max-results'] = self.request.get('max-results','1000')
		kwargs['dimensions'] = self.request.get('dimensions','')
		kwargs['metrics'] = self.request.get('metrics','ga:visits')
		kwargs['sort'] = self.request.get('sort','')
		kwargs['filters'] = self.request.get('filters','')
		
		if self.request.get('segment',''):
			kwargs['segment'] = self.request.get('segment','')
			
		# current year
		d = datetime.date.today()
		
		kwargs['end-date'] = self.request.get('end-date', str(d))
		kwargs['start-date'] = self.request.get('start-date', str(datetime.date(d.year, 1, 1)))

		# Search cache
		cache_key = user.user_id() + str(kwargs)
		total = memcache.get(cache_key)
		
		if total is not None:
			self.response.out.write('%.2f' % total)
			return
		
		logging.info('Cache Miss')

		# Initialize a client to talk to Google Data API services.
		auth_token = gdata.gauth.ae_load(user.user_id())
		client = gdata.analytics.client.AnalyticsClient()
		
	
		# Query GA API
		try:
			logging.debug(str(kwargs))
			query = gdata.analytics.client.DataFeedQuery(kwargs)
			feed = client.get_data_feed(query, auth_token)
		except RequestError:
			logging.error('RequestError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='invalid_request',
				message='Request Error',
				tqx=self.request.get('tqx','out:json')))
			return
		except DownloadError:
			# usually triggers for GA API timeouts
			logging.error('DownloadError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='internal_error',
				message='API Timeout',
				tqx=self.request.get('tqx','out:json')))
			return

		current_year_total = ''

		if feed.entry:
			# dispense title
			for entry in feed.entry:
				if entry.dimension:
					for dimension in entry.dimension:
						pass
				for metric in entry.metric:
					pass
				break
			
			# get visits
			for entry in feed.entry:
				if entry.dimension:
					for dimension in entry.dimension:
						pass
				for metric in entry.metric:
					current_year_total = int(metric.value)
		
		in_million = current_year_total / 1000000
		
		# Cache response
		memcache.set(cache_key, in_million, 60*60*12)
		# Write
		self.response.out.write('%.2f' % in_million)


# Last Month New / Returning
class LastMonthNewReturning(webapp.RequestHandler):
	def get(self):

		self.response.headers['Content-Type'] = 'application/json'

		user = users.get_current_user()

		# GA API Base parameters
		kwargs = {
			'ids' : 'ga:9060294', # comma-separated string of analytics accounts.
			'start-index' : '1', # used in combination with max-results to pull more than 1000 entries, defaults to 1
			}
		
		# populate GA API parameters 
		kwargs['max-results'] = self.request.get('max-results','1000')
		kwargs['dimensions'] = self.request.get('dimensions','')
		kwargs['metrics'] = self.request.get('metrics','ga:visits,ga:newVisits')
		kwargs['sort'] = self.request.get('sort','')
		kwargs['filters'] = self.request.get('filters','')
		
		if self.request.get('segment',''):
			kwargs['segment'] = self.request.get('segment','')
			
		# last month
		default_end_date = datetime.date.today()
		default_end_date = datetime.date.fromordinal(default_end_date.toordinal() - default_end_date.day)
		kwargs['end-date'] = self.request.get('end-date', str(default_end_date))
		
		default_start_date = datetime.date.fromordinal((default_end_date.toordinal() - default_end_date.day) + 1)
		kwargs['start-date'] = self.request.get('start-date', str(default_start_date))

		# Search cache
		cache_key = user.user_id() + str(kwargs)
		data_table = memcache.get(cache_key)
		
		if data_table is not None:
			self.response.out.write(data_table.ToResponse(tqx=self.request.get('tqx','out:json')))
			return
		
		logging.info('Cache Miss')

		# Initialize a client to talk to Google Data API services.
		auth_token = gdata.gauth.ae_load(user.user_id())
		client = gdata.analytics.client.AnalyticsClient()

		# Query GA API
		try:
			logging.debug(str(kwargs))
			query = gdata.analytics.client.DataFeedQuery(kwargs)
			feed = client.get_data_feed(query, auth_token)
		except RequestError:
			logging.error('RequestError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='invalid_request',
				message='Request Error',
				tqx=self.request.get('tqx','out:json')))
			return
		except DownloadError:
			# usually triggers for GA API timeouts
			logging.error('DownloadError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='internal_error',
				message='API Timeout',
				tqx=self.request.get('tqx','out:json')))
			return

		description = []
		data = []
		
		description.append(tuple(['Visitor','string']))
		description.append(tuple(['Total','number']))

		if feed.entry:
			# dispense title
			for entry in feed.entry:
				if entry.dimension:
					for dimension in entry.dimension:
						pass
				for metric in entry.metric:
					pass
				break
			# populate data_table
			for entry in feed.entry:
				r = []
				n = []
				for metric in entry.metric:
					if metric.name == 'ga:visits':
						visits = metric.value
					else:
						r.append(unicode(unquote('Visitas retornantes'), 'utf-8'))
						r.append(tuple([int(visits) - int(metric.value), splitThousands(int(visits) - int(metric.value))]))
						n.append(unicode(unquote('Novas visistas'), 'utf-8'))
						n.append(tuple([int(metric.value), splitThousands(metric.value)]))
						
						data.append(r)
						data.append(n)

		# Init Viz
		data_table = gviz_api.DataTable(description)
		# Load data into viz
		data_table.LoadData(data)
		# Cache response
		memcache.set(cache_key, data_table, 60*60*12)
		# Write JSON
		self.response.out.write(data_table.ToResponse(tqx=self.request.get('tqx','out:json')))
		
# Current Month New / Returning
class CurrentMonthNewReturning(webapp.RequestHandler):
	def get(self):

		self.response.headers['Content-Type'] = 'application/json'

		user = users.get_current_user()

		# GA API Base parameters
		kwargs = {
			'ids' : 'ga:9060294', # comma-separated string of analytics accounts.
			'start-index' : '1', # used in combination with max-results to pull more than 1000 entries, defaults to 1
			}
		
		# populate GA API parameters 
		kwargs['max-results'] = self.request.get('max-results','1000')
		kwargs['dimensions'] = self.request.get('dimensions','')
		kwargs['metrics'] = self.request.get('metrics','ga:visits,ga:newVisits')
		kwargs['sort'] = self.request.get('sort','')
		kwargs['filters'] = self.request.get('filters','')
		
		if self.request.get('segment',''):
			kwargs['segment'] = self.request.get('segment','')
			
		# current month
		default_end_date = datetime.date.today()
		default_end_date = datetime.date.fromordinal(default_end_date.toordinal())
		kwargs['end-date'] = self.request.get('end-date', str(default_end_date))
		
		default_start_date = datetime.date.fromordinal((default_end_date.toordinal() - default_end_date.day) + 1)
		kwargs['start-date'] = self.request.get('start-date', str(default_start_date))

		# Search cache
		cache_key = user.user_id() + str(kwargs)
		data_table = memcache.get(cache_key)
		
		if data_table is not None:
			self.response.out.write(data_table.ToResponse(tqx=self.request.get('tqx','out:json')))
			return
		
		logging.info('Cache Miss')

		# Initialize a client to talk to Google Data API services.
		auth_token = gdata.gauth.ae_load(user.user_id())
		client = gdata.analytics.client.AnalyticsClient()

		# Query GA API
		try:
			logging.debug(str(kwargs))
			query = gdata.analytics.client.DataFeedQuery(kwargs)
			feed = client.get_data_feed(query, auth_token)
		except RequestError:
			logging.error('RequestError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='invalid_request',
				message='Request Error',
				tqx=self.request.get('tqx','out:json')))
			return
		except DownloadError:
			# usually triggers for GA API timeouts
			logging.error('DownloadError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='internal_error',
				message='API Timeout',
				tqx=self.request.get('tqx','out:json')))
			return

		description = []
		data = []
		
		description.append(tuple(['Visitor','string']))
		description.append(tuple(['Total','number']))

		if feed.entry:
			# dispense title
			for entry in feed.entry:
				if entry.dimension:
					for dimension in entry.dimension:
						pass
				for metric in entry.metric:
					pass
				break
			# populate data_table
			for entry in feed.entry:
				r = []
				n = []
				for metric in entry.metric:
					if metric.name == 'ga:visits':
						visits = metric.value
					else:
						r.append(unicode(unquote('Visitas retornantes'), 'utf-8'))
						r.append(tuple([int(visits) - int(metric.value), splitThousands(int(visits) - int(metric.value))]))
						n.append(unicode(unquote('Novas visistas'), 'utf-8'))
						n.append(tuple([int(metric.value), splitThousands(metric.value)]))
						
						data.append(r)
						data.append(n)

		# Init Viz
		data_table = gviz_api.DataTable(description)
		# Load data into viz
		data_table.LoadData(data)
		# Cache response
		memcache.set(cache_key, data_table, 60*60*12)
		# Write JSON
		self.response.out.write(data_table.ToResponse(tqx=self.request.get('tqx','out:json')))

		
# Visits
class Visits(webapp.RequestHandler):
	def get(self):

		self.response.headers['Content-Type'] = 'application/json'

		user = users.get_current_user()

		# GA API Base parameters
		kwargs = {
			'ids' : 'ga:9060294', # comma-separated string of analytics accounts.
			'start-index' : '1', # used in combination with max-results to pull more than 1000 entries, defaults to 1
			}
		
		# populate GA API parameters 
		kwargs['max-results'] = self.request.get('max-results','1000')
		kwargs['dimensions'] = self.request.get('dimensions','ga:date')
		kwargs['metrics'] = self.request.get('metrics','ga:visits')
		kwargs['sort'] = self.request.get('sort','')
		kwargs['filters'] = self.request.get('filters','')
		
		if self.request.get('segment',''):
			kwargs['segment'] = self.request.get('segment','')
			
		# current month
		default_end_date = datetime.date.today()
		kwargs['end-date'] = self.request.get('end-date', str(default_end_date))
		
		default_start_date = datetime.date.fromordinal((default_end_date.toordinal() - default_end_date.day) + 1)
		kwargs['start-date'] = self.request.get('start-date', str(default_start_date))

		# Search cache
		cache_key = user.user_id() + str(kwargs)
		data_table = memcache.get(cache_key)
		
		if data_table is not None:
			self.response.out.write(data_table.ToResponse(tqx=self.request.get('tqx','out:json')))
			return
		
		logging.info('Cache Miss')

		# Initialize a client to talk to Google Data API services.
		auth_token = gdata.gauth.ae_load(user.user_id())
		client = gdata.analytics.client.AnalyticsClient()

		# Query GA API
		try:
			logging.debug(str(kwargs))
			query = gdata.analytics.client.DataFeedQuery(kwargs)
			feed = client.get_data_feed(query, auth_token)
		except RequestError:
			logging.error('RequestError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='invalid_request',
				message='Request Error',
				tqx=self.request.get('tqx','out:json')))
			return
		except DownloadError:
			# usually triggers for GA API timeouts
			logging.error('DownloadError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='internal_error',
				message='API Timeout',
				tqx=self.request.get('tqx','out:json')))
			return
		
		vcm = []
		
		if feed.entry:
			# dispense title
			for entry in feed.entry:
				if entry.dimension:
					for dimension in entry.dimension:
						pass
				for metric in entry.metric:
					pass
				break
			# populate data_table
			for entry in feed.entry:
				for metric in entry.metric:
					vcm.append(int(metric.value))					
	
		# last month
		default_end_date = datetime.date.today()
		default_end_date = datetime.date.fromordinal(default_end_date.toordinal() - default_end_date.day)
		kwargs['end-date'] = self.request.get('end-date', str(default_end_date))
		
		default_start_date = datetime.date.fromordinal((default_end_date.toordinal() - default_end_date.day) + 1)
		kwargs['start-date'] = self.request.get('start-date', str(default_start_date))
		
		# Query GA API
		try:
			logging.debug(str(kwargs))
			query = gdata.analytics.client.DataFeedQuery(kwargs)
			feed = client.get_data_feed(query, auth_token)
		except RequestError:
			logging.error('RequestError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='invalid_request',
				message='Request Error',
				tqx=self.request.get('tqx','out:json')))
			return
		except DownloadError:
			# usually triggers for GA API timeouts
			logging.error('DownloadError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='internal_error',
				message='API Timeout',
				tqx=self.request.get('tqx','out:json')))
			return
		
		description = []
		data = []
		i = 0
		
		description.append(tuple(['Dia','date']))
		description.append(tuple([unicode(unquote('Visitas mês atual'), 'utf-8'),'number']))
		description.append(tuple([unicode(unquote('Visitas mês anterior'), 'utf-8'),'number']))

		if feed.entry:
			# dispense title
			for entry in feed.entry:
				if entry.dimension:
					for dimension in entry.dimension:
						pass
				for metric in entry.metric:
					pass
				break
			# populate data_table
			for entry in feed.entry:
				ga_entry = []
				if entry.dimension:
					for dimension in entry.dimension:
						if dimension.name == 'ga:date':
							ga_entry.append(tuple([
								datetime.datetime.strptime(dimension.value,'%Y%m%d'),
								datetime.datetime.strptime(dimension.value,'%Y%m%d').strftime('%d')
							]))
						else:
							ga_entry.append(dimension.value)
				for metric in entry.metric:
					try:
						ga_entry.append(tuple([int(vcm[i]), splitThousands(vcm[i])]))
					except:
						ga_entry.append(0)
					
					ga_entry.append(tuple([int(metric.value), splitThousands(metric.value)]))
				
				i = i + 1
				data.append(ga_entry)

		# Init Viz
		data_table = gviz_api.DataTable(description)
		# Load data into viz
		data_table.LoadData(data)
		# Cache response
		memcache.set(cache_key, data_table, 60*60*12)
		# Write JSON
		self.response.out.write(data_table.ToResponse(tqx=self.request.get('tqx','out:json')))
		
# Keywords
class Keywords(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		
		user = users.get_current_user()

		# GA API Base parameters
		kwargs = {
			'ids' : 'ga:9060294', # comma-separated string of analytics accounts.
			'start-index' : '1', # used in combination with max-results to pull more than 1000 entries, defaults to 1
			}
		
		# populate GA API parameters 
		kwargs['max-results'] = self.request.get('max-results','50')
		kwargs['dimensions'] = self.request.get('dimensions','ga:keyword')
		kwargs['metrics'] = self.request.get('metrics','ga:visits')
		kwargs['sort'] = self.request.get('sort','-ga:visits')
		kwargs['filters'] = self.request.get('filters','ga:keyword!~(not set)')
		
		if self.request.get('segment',''):
			kwargs['segment'] = self.request.get('segment','')
			
		# last year
		default_end_date = datetime.date.today()
		kwargs['end-date'] = self.request.get('end-date', str(default_end_date))
		
		default_start_date = datetime.date.fromordinal((default_end_date.toordinal() - default_end_date.day) + 1)
		kwargs['start-date'] = self.request.get('start-date', str(default_start_date))

		# Search cache
		cache_key = user.user_id() + str(kwargs)
		keywords = memcache.get(cache_key)
		
		if keywords is not None:
			self.response.out.write(simplejson.dumps(keywords))
			return
		
		logging.info('Cache Miss')

		# Initialize a client to talk to Google Data API services.
		auth_token = gdata.gauth.ae_load(user.user_id())
		client = gdata.analytics.client.AnalyticsClient()
		
	
		# Query GA API
		try:
			logging.debug(str(kwargs))
			query = gdata.analytics.client.DataFeedQuery(kwargs)
			feed = client.get_data_feed(query, auth_token)
		except RequestError:
			logging.error('RequestError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='invalid_request',
				message='Request Error',
				tqx=self.request.get('tqx','out:json')))
			return
		except DownloadError:
			# usually triggers for GA API timeouts
			logging.error('DownloadError:' + str(kwargs))
			self.response.out.write(gviz_api.Error(reason='internal_error',
				message='API Timeout',
				tqx=self.request.get('tqx','out:json')))
			return
		
		tag_cloud = []

		if feed.entry:
			# dispense title
			for entry in feed.entry:
				if entry.dimension:
					for dimension in entry.dimension:
						pass
				for metric in entry.metric:
					pass
				break
			
			# get visits
			for entry in feed.entry:
				row = {}
				if entry.dimension:
					for dimension in entry.dimension:
						row['keyword'] = (dimension.value)
				for metric in entry.metric:
					row['visits'] = (metric.value)
				
				tag_cloud.append(row)	
		
		ks = {}		
		ks['feed'] = tag_cloud
		
		# Cache response
		memcache.set(cache_key, ks, 60*60*12)
		# Write
		self.response.out.write(simplejson.dumps(ks))
		
def main():
	if settings.DEBUG:
		logging.getLogger().setLevel(logging.DEBUG)
	else:
		logging.getLogger().setLevel(logging.WARN)
		
	application = webapp.WSGIApplication([
		('/data/last-year-visits', LastYearVisits),
		('/data/current-year-visits', CurrentYearVisits),
		('/data/last-month-new-returning', LastMonthNewReturning),
		('/data/current-month-new-returning', CurrentMonthNewReturning),
		('/data/visits', Visits),
		('/data/keywords', Keywords),
	], debug = settings.DEBUG)
	run_wsgi_app(application)
	
if __name__ == '__main__':
	main()


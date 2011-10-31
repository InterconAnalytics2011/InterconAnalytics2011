#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

import settings
import atom.http_core
import gdata.analytics.client
import gdata.gauth

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.api import memcache

class ClearCache(webapp.RequestHandler):
	def get(self):
		if users.is_current_user_admin():
			self.response.out.write(str(memcache.get_stats()))
		else: 
			self.error(403)
			self.response.out.write("403: Forbidden")
			return
		if memcache.flush_all():
			self.response.out.write("'\nOK: Cache Cleared")
		else: 
			self.response.out.write("\nError: Cache couldn't be cleared")
			

class Login(webapp.RequestHandler):

	def get(self):
		debug = ''
		# Write our pages title
		next_url = atom.http_core.Uri('http', settings.HOST_NAME , path='/login')
		user = users.get_current_user()
		# Allow the user to sign in or sign out
		if user:
			sign = '<a href="%s">Logout %s</a><br />' % (
			users.create_logout_url(str(next_url)),user.email())
		else:
			sign = '<a href="%s">Login usando sua Google Account</a><br />' % (users.create_login_url(str(next_url)))

		# Initialize a client to talk to Google Data API services.
		client = gdata.analytics.client.AnalyticsClient()

		# Find the AuthSub token and upgrade it to a session token.
		session_token = None
		auth_token, scopes = gdata.gauth.auth_sub_string_from_url(self.request.uri)
		if auth_token:
			# Upgrade the single-use AuthSub token to a multi-use session token.
			session_token = client.upgrade_token(gdata.gauth.AuthSubToken(auth_token, scopes))
		if session_token and user:
			# If there is a current user, store the token in the datastore and
			# associate it with the current user. Since we told the client to
			# run_on_appengine, the add_token call will automatically store the
			# session token if there is a current_user.
			gdata.gauth.ae_save(session_token, user.user_id())

		authsub_url = None
		if user:
			# Check if has token
			logging.debug('Get Token')
			auth_token = gdata.gauth.ae_load(user.user_id())
			logging.debug('Found Token: ' + str(auth_token))
			# No token yet
			if user and auth_token:
				logging.warn('Found Token: ' + str(auth_token))
			else:
				logging.warn('No Token: user->' + str(user))
				authsub_url = gdata.gauth.generate_auth_sub_url(next_url,
					gdata.gauth.AUTH_SCOPES['analytics'],
					secure=False, session=True)
				logging.warn('AuthSubUrl' + str(authsub_url))

		template_values = {
			'authsub_url': authsub_url,
			'user': user,
			'sign': sign,
			}

		path = os.path.join(os.path.dirname(__file__), 'templates/login.html')
		self.response.out.write(template.render(path, template_values))
		
def main():
	application = webapp.WSGIApplication([
		('/clear-cache', ClearCache),
		('/.*', Login),
	], debug = settings.DEBUG)
	run_wsgi_app(application)


if __name__ == '__main__':
	main()


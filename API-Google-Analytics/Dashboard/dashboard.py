#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

import settings
import atom.http_core
import gdata.analytics.client
import gdata.gauth

import gdata.service
import gdata.analytics.service
import gdata.alt.appengine

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.api import memcache

class DashBoard(webapp.RequestHandler):

	def get(self):
		user = users.get_current_user()
		# Allow the user to sign in or sign out
		next_url = atom.http_core.Uri('http', settings.HOST_NAME , path='/login')
		if user:
			sign = '<a href="%s">Logout %s</a><br />' % (
			users.create_logout_url(str(next_url)),user.email())
		else:
			sign = '<a href="%s">Login using your Google Account</a><br />' % (
			users.create_login_url(str(next_url)))

		template_values = {
			'sign': sign,
			}
		
		path = os.path.join(os.path.dirname(__file__), 'templates/dashboard.html')
		self.response.out.write(template.render(path, template_values))
		
def main():
	application = webapp.WSGIApplication([
		('/.*', DashBoard),
	], debug = settings.DEBUG)
	run_wsgi_app(application)

if __name__ == '__main__':
	main()


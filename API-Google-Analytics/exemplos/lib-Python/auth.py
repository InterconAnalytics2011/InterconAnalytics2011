#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provides classes to simplify authorization to The Google Analytics API.

  This is specifically designed for installed applications. The
  OAuthRoutine and ClientLoginRoutine classs will retrieve new auth tokens
  and set them in a gdata.analytics.client object. Developers can use the
  authorized client object to make requests to the Google Analytics API.
  Beyond getting new tokens, these classes will try to reuse old tokens
  by saving and loading them to disk.

  AuthRoutine: Base class to handle saving, loading and deleting auth tokens.
  OAuthRoutine: Extends AuthRoutine to retrieve an OAuth for Installed
      Applications token. Most people should use this class.
  ClientLoginRoutine: Extends AuthRoutine to get a ClientLogin token.
  AppError: Base class for exceptions.
  AuthError: Raised if there is an authorization error.
"""

__author__ = 'api.nickm@google.com (Nick Mihailovski)'


import cPickle
import getpass
import os
import webbrowser

import gdata
import gdata.analytics.client


class AuthRoutine(object):
  """Base class to retrieve a Google Analytics API Authorization Token.

  This class should be subclassed to implement the logic to retrieve
  a particular type of token. See OAuthRoutine and ClientLoginRoutine
  as implementations.

  Attributes:
    auth_token: An authorization token.
    auth_routine_util: AuthRoutineUtil Utility to save, load and delete from
        the local file system.
    token_obj_name: string The name of the token object for this authorization
        routine. This is used to differentiate tokens from different
        auhtorization routines.
  """

  def __init__(self, auth_routine_util, token_obj_name):
    """Initializes this class.

    Args:
      auth_routine_util: AuthRoutineUtil Utility to save, load and delete from
          the local file system.
      token_obj_name: string The name of the token object.
    """
    self.auth_token = None
    self.auth_routine_util = auth_routine_util
    self.token_obj_name = token_obj_name

  def RequestAuthToken(self):
    """Should be overridden by a subclass."""
    pass

  def GetAuthToken(self):
    """Returns an Authorization token in the my_client parameter.

    We try to see if an authorization token has previously been saved
    to disk. If a token is found, a check is made to ensure that the
    type of token is from the current authorization method. Each subclass
    of this AuthRoutine should define the class name for the token.
    If the token is of the correct type, it is returned. Otherwise, we go
    and fetch a new token and save it to disk for futher use.

    Returns:
      An authorization token to be used with the Google Analytics API.

    Raises:
      AuthError: If there was an error trying to get a token.
    """
    if self.auth_token:
      return self.auth_token

    self.auth_token = self.auth_routine_util.LoadAuthToken(self.token_obj_name)

    if not self.auth_token:
      self.auth_token = self.RequestAuthToken()
      self.auth_routine_util.SaveAuthToken(self.auth_token)

    return self.auth_token


class OAuthRoutine(AuthRoutine):
  """AuthRoutine Implementation using the OAuth For Installed Apps Routine."""

  OAUTH_SCOPES = ['https://www.google.com/analytics/feeds']

  def __init__(self, my_client, auth_routine_util):
    """Initializes the object.

    Args:
      my_client: gdata.analytics.client The Google Analytics client object
          which makes requests to the API.
      auth_routine_util: AuthRoutineUtil Utility to save, load and delete from
          the local file system.
    """
    self.my_client = my_client
    AuthRoutine.__init__(self, auth_routine_util, 'OAuthHmacToken')

  def RequestAuthToken(self):
    """Handles all the logic to get a new OAuth HMAC token.

    This prompts the user to go to a URL and tries to open the URL in a
    running browser. The page on the URL prompts the user to login to
    their Google Account and grant access to this script. Next the user
    is given a verification code which the must paste back into the script.
    The script then retrieves a long lived authorization token.

    See the docs for more magic about OAuth for installed apps:
    http://code.google.com/apis/accounts/docs/OAuthForInstalledApps.html

    Returns:
      gdata.gauth.OAuthHmacToken The OAuth HMAC token.

    Raises:
      AuthError: If there was an error trying to get the OAuth token.
    """
    url = ('%s?xoauth_displayname=%s' % (gdata.gauth.REQUEST_TOKEN_URL,
                                         self.my_client.source))

    request_token = self.my_client.GetOAuthToken(
        OAuthRoutine.OAUTH_SCOPES,
        next='oob',
        consumer_key='anonymous',
        consumer_secret='anonymous',
        url=url)

    verify_url = request_token.generate_authorization_url(
        google_apps_domain='default')

    print 'Please log in and/or grant access at: %s\n' % verify_url
    webbrowser.open(str(verify_url))
    request_token.verifier = raw_input(
        'Please enter the verification code on the success page: ')
    try:
      return self.my_client.GetAccessToken(request_token)

    except gdata.client.RequestError, err:
      raise AuthError(msg='Error upgrading token: %s' % err)


class ClientLoginRoutine(AuthRoutine):
  """AuthRoutine Implementation using the Client Login Routine."""

  def __init__(self, my_client, auth_routine_util):
    """Initializes this object.

    Args:
      my_client: gdata.analytics.client The Google Analytics client object
          which makes requests to the API.
      auth_routine_util: AuthRoutineUtil Utility to save, load and delete from
          the local file system.
    """
    self.my_client = my_client
    AuthRoutine.__init__(self, auth_routine_util, 'ClientLoginToken')

  def RequestAuthToken(self):
    """Handles all the logic to get and set a new ClientLogin token.

    Prompts the user for their user name and password. Then tries to authorize
    the user with the ClientLogin reoutine. If sucessful, the token is returned.
    Otherwise, an AuthError exception is raised.

    Returns:
      gdata.gauth.ClientLoginToken The ClientLogin token.

    Raises:
      AuthError: If there was an error trying to get the Client Login token.
    """
    username = raw_input('Input your username: ')
    password = getpass.getpass('Input your password: ')
    try:
      return self.my_client.RequestClientLoginToken(
          username,
          password,
          self.my_client.source,
          service='analytics')

    except gdata.client.RequestError, err:
      raise AuthError(msg='There was an authorization error: %s' % err)


class AuthRoutineUtil(object):
  """Handles saving, loading and deleting of Auth tokens.

  Attributes:
    TOKEN_FILE_NAME: The name of the file to save tokens.
  """

  TOKEN_FILE_NAME = 'auth_token.tok'

  def SaveAuthToken(self, auth_token):
    """Saves the authorization token into a file to be used later.

    This saves the entire authorization token as a cPickle object.

    Args:
      auth_token: object The Authorization token to be saved.
    """
    try:
      my_file = open(AuthRoutineUtil.TOKEN_FILE_NAME, 'wb')
      cPickle.dump(auth_token, my_file)
    except (IOError, EOFError):
      print 'Problems writing access token to file, try again.'
    finally:
      my_file.close()

  def LoadAuthToken(self, token_obj_name):
    """Tries to load an authorization token of type token_obj_name from disk.

    To differentiate between different types of token, a check is made to
    ensure the right type of token was loaded.

    Args:
      token_obj_name: string The name of the authorization object to
      try and load.

    Returns:
      The object saved in AuthRoutine.TOKEN_FILE_NAME. None if an error
      occurs or if the incorrect token type was found.
    """
    try:
      my_file = open(AuthRoutineUtil.TOKEN_FILE_NAME, 'rb')
      access_token = cPickle.load(my_file)
    except (IOError, EOFError):
      return None

    if access_token.__class__.__name__ != token_obj_name:
      return None
    return access_token

  def DeleteAuthToken(self):
    """Deletes the authorization token file if it exists."""
    if os.path.exists(AuthRoutineUtil.TOKEN_FILE_NAME):
      os.remove(AuthRoutineUtil.TOKEN_FILE_NAME)


class AppError(Exception):
  """Generic Error for this application."""

  def __init__(self, msg=''):
    self.msg = msg
    Exception.__init__(self)


class AuthError(AppError):
  """If there is an authorization error."""
  pass


#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This is a modified version of 'service.py' (version 1.1.1), part of the 'atom' module
#  from the gdata-python-client project (http://code.google.com/p/gdata-python-client/) by Google Inc.
# Copyright (C) 2006, 2007, 2008 Google Inc.
#
# It has been modified to support json formatted data instead of atom.
# Copyright (C) 2012 rambla.eu
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
__author__ = 'api.jscudder (Jeffrey Scudder)'

"""RawsService provides CRUD ops. in line with the Atom Publishing Protocol.

  RawsService: Encapsulates the ability to perform insert, update and delete
               operations with the Atom Publishing Protocol and json formatted data.
               An instance can perform query, insertion, deletion, and
               update.
"""
import re
import httplib
import urllib
import raws_json
import json

# Module level variable specifies which module should be used by RawsService
# objects to make HttpRequests. This setting can be overridden on each
# instance of RawsService.
http_request_handler = raws_json


class Error(Exception):
  pass

class BadAuthentication(Error):
  pass


class NotAuthenticated(Error):
  pass


class NonAuthSubToken(Error):
  pass


class RequestError(Error):
  pass


class UnexpectedReturnType(Error):
  pass

class BadAuthenticationServiceURL(Error):
  pass


class Feed(object):

    def __init__(self, feed = None):
        self.entries = []
        if "entry" in feed["feed"]:
            for e in feed["feed"]["entry"]:
                self.entries.append({"entry":e,})


class RawsService(raws_json.JsonService):
    """Contains elements needed for Raws login and CRUD request headers.
    
    Maintains additional headers (tokens for example) needed for the Raws
    services to allow a user to perform inserts, updates, and deletes.
    """
    
    def __init__(self, username=None, password=None, source=None, server=None, port = None,
               additional_headers=None, handler=None, ssl = False):
        """Creates an object of type RawsService.
        
        Args:
          username: string (optional) The username for authentication.
          password: string (optional) The user's password.
          source: string (optional) The name of the user's application.
          server: string (optional) The name of the server to which a connection will be opened. (eg 'rass.cdn01.rambla.be').
          additional_headers: dictionary (optional) Any additional headers which should be included with CRUD operations.
          handler: module (optional) The module whose HttpRequest function should be used when making requests to the server. The default value is atom.service.
          ssl: bool (optional) Use SSL encryption.
        """
        self.username = username
        self.password = password
        self.server = server
        self.additional_headers = additional_headers or {}
        self.handler = handler or http_request_handler
        self.ssl = ssl
        if port:
            self.port = port
        elif ssl:
            self.port = 443
        else:
            self.port = 80 # default
        self.__SetSource(source)
        # Authentication operations
        if self.username and self.password:
            self.UseBasicAuth(self.username, self.password)
    
    def set_credentials(self, username, password, server = None, port = None):
        """ Sets the authentication credentials and server name on the object. """
        self.username = username
        self.password = password
        if server:
            self.server = server
        if port:
            self.port = port
        # Authentication operations
        if self.username and self.password:
            self.UseBasicAuth(self.username, self.password)

    def get_service_uri(self):
        base_uri = "http://" + self.server
        if self.port:
            base_uri += ":" + self.port
        return base_uri

    # Private methods to create the source property.
    def __GetSource(self):
        return self.__source

    def __SetSource(self, new_source):
        self.__source = new_source
        # Update the UserAgent header to include the new application name.
        self.additional_headers['User-Agent'] = '%s Raws-Python/1.1.1' % (self.__source)

    source = property(__GetSource, __SetSource, doc="""The source is the name of the application making the request. It should be in the form company_id-app_name-app_version""")
  
  
    # CRUD operations
    def Get(self, uri, extra_headers=None, redirects_remaining=4, encoding='UTF-8', converter=None):
        """Query the Raws API with the given URI

        The uri is the portion of the URI after the server value

        To perform a query against RAMS, set the server to
        'rams.mon01.rambla.be' and set the uri to '/traffic/...', where ... is
        your query. For example, to get recursive file traffic: '/traffic/?kind=recursive'

        Args:
          uri: string The query in the form of a URI. Example:
               '/traffic/?kind=recursive'.
          extra_headers: dictionary (optional) Extra HTTP headers to be included
                         in the GET request. These headers are in addition to
                         those stored in the client's additional_headers property.
                         The client automatically sets the Content-Type and
                         Authorization headers.
          redirects_remaining: int (optional) Tracks the number of additional
              redirects this method will allow. If the service object receives
              a redirect and remaining is 0, it will not follow the redirect.
              This was added to avoid infinite redirect loops.
          encoding: string (optional) The character encoding for the server's
              response. Default is UTF-8
          converter: func (optional) A function which will transform
              the server's results before it is returned. Example: use
              RawsFeedFromString to parse the server response as if it
              were a RawsFeed.

        Returns:
          If there is no ResultsTransformer specified in the call, a RawsFeed
          or RawsEntry depending on which is sent from the server. If the
          response is niether a feed or entry and there is no ResultsTransformer,
          return a string. If there is a ResultsTransformer, the returned value
          will be that of the ResultsTransformer function.
        """
        if extra_headers is None:
            extra_headers = {"Accept":"application/json"}
        else:
            extra_headers.update({"Accept":"application/json"})

        server_response = self.handler.HttpRequest(self, 'GET', None, uri, extra_headers=extra_headers)
        result_body = server_response.read()

        if server_response.status == 200:
            return json.loads(s = result_body, parse_int = True, parse_float = True)
        else:
          raise RequestError, {'status': server_response.status,
              'reason': server_response.reason, 'body': result_body}
  
    # def GetMedia(self, uri, extra_headers=None, file_path = None):
    #     """Returns a MediaSource containing media and its metadata from the given
    #     URI string, storing it into the local file_path.
    #     """
    #     response_handle = self.handler.HttpRequest(self, 'GET', None, uri, extra_headers=extra_headers)
    #     if not response_handle:
    #         raise rawsc.RawscException('Failed to retrieve response handle from URI = %s.' % str(uri))
    #     media_source = rawsc.MediaSource(file_handle = response_handle, content_type = response_handle.getheader('Content-Type'), content_length = response_handle.getheader('Content-Length'))
    #     if not media_source:
    #         raise rawsc.RawscException('Failed to create media_source object after retrieving URI = %s.' % str(uri))
    #     if file_path is not None:
    #         if not media_source.writeFile(file_path):
    #             raise rawsc.RawscException('Failed writing response (URI = %s) to path = %s.' % (str(uri), str(file_path)))
    #     return media_source
    #     
    # 
    # def GetEntry(self, uri, extra_headers=None):
    #     """Query the Raws API with the given URI and receive an Entry.
    # 
    #     See also documentation for rawsc.service.Get
    # 
    #     Args:
    #       uri: string The query in the form of a URI. Example:
    #            '/item/mysubdir/myfile.mp4'.
    #       extra_headers: dictionary (optional) Extra HTTP headers to be included
    #                      in the GET request. These headers are in addition to
    #                      those stored in the client's additional_headers property.
    #                      The client automatically sets the Content-Type and
    #                      Authorization headers.
    # 
    #     Returns:
    #       A RawsEntry built from the XML in the server's response.
    #     """
    # 
    #     result = self.Get(uri, extra_headers, converter=atom.EntryFromString)
    #     if isinstance(result, atom.Entry):
    #         return result
    #     else:
    #         raise UnexpectedReturnType, 'Server did not send an entry'
    #   
    # def GetFeed(self, uri, extra_headers=None,
    #           converter=rawsc.RawsFeedFromString):
    #     """Query the Raws API with the given URI and receive a Feed.
    # 
    #     See also documentation for rawsc.service.Get
    # 
    #     Args:
    #       uri: string The query in the form of a URI. Example:
    #            '/dir/mysubdir/?kind=file'.
    #       extra_headers: dictionary (optional) Extra HTTP headers to be included
    #                      in the GET request. These headers are in addition to
    #                      those stored in the client's additional_headers property.
    #                      The client automatically sets the Content-Type and
    #                      Authorization headers.
    # 
    #     Returns:
    #       A RawsFeed built from the XML in the server's response.
    #     """
    # 
    #     result = self.Get(uri, extra_headers, converter=converter)
    #     if isinstance(result, atom.Feed):
    #         return result
    #     else:
    #         raise UnexpectedReturnType, 'Server did not send a feed'
    #   
    # def GetNext(self, feed):
    #     """Requests the next 'page' of results in the feed.
    # 
    #     This method uses the feed's next link to request an additional feed
    #     and uses the class of the feed to convert the results of the GET request.
    # 
    #     Args:
    #       feed: atom.Feed or a subclass. The feed should contain a next link and
    #           the type of the feed will be applied to the results from the
    #           server. The new feed which is returned will be of the same class
    #           as this feed which was passed in.
    # 
    #     Returns:
    #       A new feed representing the next set of results in the server's feed.
    #       The type of this feed will match that of the feed argument.
    #     """
    #     next_link = feed.GetNextLink()
    #     # Create a closure which will convert an XML string to the class of
    #     # the feed object passed in.
    #     def ConvertToFeedClass(xml_string):
    #         return atom.CreateClassFromXMLString(feed.__class__, xml_string)
    #     # Make a GET request on the next link and use the above closure for the
    #     # converted which processes the XML string from the server.
    #     if next_link and next_link.href:
    #         return self.Get(next_link.href, converter=ConvertToFeedClass)
    #     else:
    #         return None
    # 
    def Post(self, data, uri, extra_headers=None, url_params=None,
           escape_params=True, redirects_remaining=4, media_source=None,
           converter=None):
        """Insert or update  data into a Raws service at the given URI.
    
        Args:
          data: string, ElementTree._Element, atom.Entry, or rawsc.RawsEntry The
                XML to be sent to the uri.
          uri: string The location (feed) to which the data should be inserted.
               Example: '/job/'.
          extra_headers: dict (optional) HTTP headers which are to be included.
                         The client automatically sets the Content-Type,
                         Authorization, and Content-Length headers.
          url_params: dict (optional) Additional URL parameters to be included
                      in the URI. These are translated into query arguments
                      in the form '&dict_key=value&...'.
                      Example: {'paginate_by': '50'} becomes &paginate_by=50
          escape_params: boolean (optional) If false, the calling code has already
                         ensured that the query will form a valid URL (all
                         reserved characters have been escaped). If true, this
                         method will escape the query and any URL parameters
                         provided.
          media_source: MediaSource (optional) Container for the media to be sent
              along with the entry, if provided.
          converter: func (optional) A function which will be executed on the
              server's response. Often this is a function like
              RawsEntryFromString which will parse the body of the server's
              response and return a RawsEntry.
    
        Returns:
          If the post succeeded, this method will return a RawsFeed, RawsEntry,
          or the results of running converter on the server's result body (if
          converter was specified).
        """
        return self.PostOrPut('POST', data, uri, extra_headers=extra_headers,
            url_params=url_params, escape_params=escape_params,
            redirects_remaining=redirects_remaining,
            media_source=media_source, converter=converter)
      
    def PostOrPut(self, verb, data, uri, extra_headers=None, url_params=None,
           escape_params=True, redirects_remaining=4, media_source=None,
           converter=None):
        """Insert data into a Raws service at the given URI.
    
        Args:
          verb: string, either 'POST' or 'PUT'
          data: string, ElementTree._Element, atom.Entry, or rawsc.RawsEntry The
                XML to be sent to the uri.
          uri: string The location (feed) to which the data should be inserted.
               Example: '/job/'.
          extra_headers: dict (optional) HTTP headers which are to be included.
                         The client automatically sets the Content-Type,
                         Authorization, and Content-Length headers.
          url_params: dict (optional) Additional URL parameters to be included
                      in the URI. These are translated into query arguments
                      in the form '&paginate_by=50&...'.
                      Example: {'paginate_by': '50'} becomes &paginate_by=50
          escape_params: boolean (optional) If false, the calling code has already
                         ensured that the query will form a valid URL (all
                         reserved characters have been escaped). If true, this
                         method will escape the query and any URL parameters
                         provided.
          media_source: MediaSource (optional) Container for the media to be sent
              along with the entry, if provided.
          converter: func (optional) A function which will be executed on the
              server's response. Often this is a function like
              RawsEntryFromString which will parse the body of the server's
              response and return a RawsEntry.
    
        Returns:
          If the post succeeded, this method will return a RawsFeed, RawsEntry,
          or the results of running converter on the server's result body (if
          converter was specified).
        """
        if extra_headers is None:
            extra_headers = {"Accept":"application/json"}
        else:
            extra_headers.update({"Accept":"application/json"})
    
        if data and media_source:
            if ElementTree.iselement(data):
                data_str = ElementTree.tostring(data)
            else:
                data_str = str(data)
    
            multipart = []
            multipart.append('Media multipart posting\r\n--END_OF_PART\r\n' + \
              'Content-Type: application/atom+xml\r\n\r\n')
            multipart.append('\r\n--END_OF_PART\r\nContent-Type: ' + \
              media_source.content_type+'\r\n\r\n')
            multipart.append('\r\n--END_OF_PART--\r\n')
    
            extra_headers['MIME-version'] = '1.0'
            extra_headers['Content-Length'] = str(len(multipart[0]) +
              len(multipart[1]) + len(multipart[2]) +
              len(data_str) + media_source.content_length)
    
            server_response = self.handler.HttpRequest(self, verb,
              [multipart[0], data_str, multipart[1], media_source.file_handle,
                  multipart[2]], uri,
              extra_headers=extra_headers, url_params=url_params,
              escape_params=escape_params,
              content_type='multipart/related; boundary=END_OF_PART')
            result_body = server_response.read()
    
        elif media_source or isinstance(data, raws_json.MediaSource):
            if isinstance(data, raws_json.MediaSource):
                media_source = data
            extra_headers['Content-Length'] = str(media_source.content_length)
            extra_headers['Slug'] = str(media_source.svr_filename)
            server_response = self.handler.HttpRequest(self, verb,
              media_source.file_handle, uri, extra_headers=extra_headers,
              url_params=url_params, escape_params=escape_params,
              content_type=media_source.content_type)
            result_body = server_response.read()
    
        else:
            http_data = json.dumps(data)
            content_type = 'application/json'
            server_response = self.handler.HttpRequest(self, verb,
              http_data, uri, extra_headers=extra_headers,
              url_params=url_params, escape_params=escape_params,
              content_type=content_type)
            result_body = server_response.read()
    
        # Server returns 201 for most post requests, but when performing a batch
        # request the server responds with a 200 on success.
        if server_response.status == 201 or server_response.status == 200:
            return json.loads(result_body)
        else:
            raise RequestError, {'status': server_response.status, 'reason': server_response.reason, 'body': result_body}
      
    def Put(self, data, uri, extra_headers=None, url_params=None,
          escape_params=True, redirects_remaining=3, media_source=None,
          converter=None):
        """Updates an entry at the given URI.
    
        Args:
          data: string, ElementTree._Element, or xml_wrapper.ElementWrapper The
                XML containing the updated data.
          uri: string A URI indicating entry to which the update will be applied.
               Example: '/dir/my_new_subdir/'
          extra_headers: dict (optional) HTTP headers which are to be included.
                         The client automatically sets the Content-Type,
                         Authorization, and Content-Length headers.
          url_params: dict (optional) Additional URL parameters to be included
                         in the URI. These are translated into query arguments
                         in the form '&paginate_by=50&...'.
                         Example: {'paginate_by': '50'} becomes &paginate_by=50
          escape_params: boolean (optional) If false, the calling code has already
                         ensured that the query will form a valid URL (all
                         reserved characters have been escaped). If true, this
                         method will escape the query and any URL parameters
                         provided.
          converter: func (optional) A function which will be executed on the
              server's response. Often this is a function like
              RawsEntryFromString which will parse the body of the server's
              response and return a RawsEntry.
    
        Returns:
          If the put succeeded, this method will return a RawsFeed, RawsEntry,
          or the results of running converter on the server's result body (if
          converter was specified).
        """
        return self.PostOrPut('PUT', data, uri, extra_headers=extra_headers,
            url_params=url_params, escape_params=escape_params,
            redirects_remaining=redirects_remaining,
            media_source=media_source, converter=converter)
      
    def Delete(self, uri, extra_headers=None, url_params=None, escape_params=True, redirects_remaining=4):
        """Deletes the entry at the given URI.
    
        Args:
          uri: string The URI of the entry to be deleted. Example:
               '/item/mysubdir/myfile.mp4'
          extra_headers: dict (optional) HTTP headers which are to be included.
                         The client automatically sets the Content-Type and
                         Authorization headers.
          url_params: dict (optional) Additional URL parameters to be included
                     in the URI. These are translated into query arguments
                     in the form '&paginate_by=50&...'.
                     Example: {'paginate_by': '50'} becomes &paginate_by=50
          escape_params: boolean (optional) If false, the calling code has already
                         ensured that the query will form a valid URL (all
                         reserved characters have been escaped). If true, this
                         method will escape the query and any URL parameters
                         provided.
    
        Returns:
          True if the entry was deleted.
        """
        if extra_headers is None:
          extra_headers = {}
    
        server_response = self.handler.HttpRequest(self, 'DELETE', None, uri,
            extra_headers=extra_headers, url_params=url_params,
            escape_params=escape_params)
        result_body = server_response.read()
    
        if server_response.status == 204:
            return True
        else:
          raise RequestError, {'status': server_response.status,
              'reason': server_response.reason, 'body': result_body}


class Query(dict):
  """Constructs a query URL to be used in GET requests

  Url parameters are created by adding key-value pairs to this object as a
  dict. For example, to add &paginate_by=50 to the URL do
  my_query['paginate_by'] = 50

  Category queries are created by adding category strings to the categories
  member. All items in the categories list will be concatenated with the /
  symbol (symbolizing a category x AND y restriction). If you would like to OR
  2 categories, append them as one string with a | between the categories.
  For example, do query.categories.append('Fritz|Laurie') to create a query
  like this feed/-/Fritz%7CLaurie . This query will look for results in both
  categories.
  """

  def __init__(self, feed=None, text_query=None, params=None,
    categories=None):
      """Constructor for Query

      Args:
        feed: str (optional) The path for the feed (Examples:
            '/dir/mysubdir/' or 'customer/used/'
        text_query: str (optional) The contents of the q query parameter. The
            contents of the text_query are URL escaped upon conversion to a URI.
        params: dict (optional) Parameter value string pairs which become URL
            params when translated to a URI. These parameters are added to the
            query's items (key-value pairs).
        categories: list (optional) List of category strings which should be
            included as query categories. Currently not supported by RAWS.
            If you want to get results from category A or B (both
            categories), specify a single list item 'A|B'.
      """

      self.feed = feed
      self.categories = []
      if text_query:
          self.text_query = text_query
      if isinstance(params, dict):
          for param in params:
            self[param] = params[param]
      if isinstance(categories, list):
          for category in categories:
            self.categories.append(category)

  def ToUri(self):
      q_feed = self.feed or ''
      category_string = '/'.join([urllib.quote_plus(c) for c in self.categories])
      # Add categories to the feed if there are any.
      if len(self.categories) > 0:
          q_feed = q_feed + '/-/' + category_string
      return raws_json.BuildUri(q_feed, self)

  def __str__(self):
      return self.ToUri()


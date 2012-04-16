#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
# limitations under the License.import os
import json
import raws_json
from raws_json.raws_service import RawsService

class MetaService(RawsService):

    def __init__(self, username=None, password=None, server=None, ssl = False):
        self.username = username
        super(MetaService, self).__init__(username = username, password = password, server = server, ssl = ssl)

    def delete(self, uri):
        """ Deletes any resource, given the uri. 
        
            @param string URI to an instance to be deleted from META.
        """
        return self.Delete(uri = uri)

    # Content Methods
    # ---------------

    def createContent(self, entry):
        """ Tries to POST a new content entry to META, in order to create a new instance.

            @param dict Content entry dict, containing at least a params object + a single file object.
            @return Content entry dict
        """
        uri = "/content/" + self.username + "/"
        return self.Post(entry, uri= uri)

    def updateContent(self, entry, query = None):
        """ Tries to POST a new content resource to META, in order to update the entry that was passed as argument.

            @param dict The (modified) content entry dict, that will be posted to META.
            @return Content entry dict
        """
        name = entry["entry"]["content"]["params"]["name"]
        uri = "/content/" + self.username + "/" + name + "/"
        if query:
            query.feed = uri
            uri = query.ToUri()
        return self.Post(entry, uri= uri)

    def deleteContent(self, entry):
        """ Deletes the content instance that was passed as argument.

            @param dict The content entry dict that should be deleted from META.
        """
        name = entry["entry"]["content"]["params"]["name"]
        uri = "/content/" + self.username + "/" + name + "/"
        return self.Delete(uri = uri)

    def getContentList(self, query = None):
        """ Retrieves a content list. 

            @param query raws_json.Query object that contains queryset args.
            @return List of content dicts.
        """
        uri = "/content/" + self.username + "/"
        if query:
            query.feed = uri
            uri = query.ToUri()
        return self.Get(uri = uri)
        
    def getContentInstance(self, name, query = None):
        """ Retrieves a content entry with name passed in the argument. 

            @param string Name of the content instance to be retrieved.
            @param query raws_json.Query object that contains queryset args.
            @return Content entry dict
        """
        uri = "/content/" + self.username + "/" + name + "/"
        if query:
            query.feed = uri
            uri = query.ToUri()
        return self.Get(uri = uri)
        
    # GET Contentdir
    # -------------

    def getContentDirList(self, dirpath = None, query = None):
        """ Retrieves a contentdir list. 

            @param string Relative path to the directory from which to retrieve file info (None = root-dir).
            @param query raws_json.Query object that contains queryset args.
            @return List of content dicts (virtual or real).
        """
        path = "/"
        if dirpath:
            path = "/" + dirpath.lstrip("/")
        uri = "/contentdir/" + self.username + path
        if query:
            query.feed = uri
            uri = query.ToUri()
        return self.Get(uri = uri)

    
    # Vocab Methods
    # -------------
    
    def createVocab(self, entry):
        """ Tries to POST a new vocab entry to META, in order to create a new instance.

            @param dict Vocab entry dict, containing at least a params object with 'name' and 'xml_namespace' set.
            @return Vocab entry dict
        """
        uri = "/vocab/" + self.username + "/"
        return self.Post(entry, uri= uri)

    def updateVocab(self, entry):
        """ Tries to POST a new vocab resource to META, in order to update the entry that was passed as argument.

            @param dict The (modified) vocab entry dict, that will be posted to META.
            @return Vocab entry dict
        """
        name = entry["entry"]["content"]["params"]["name"]
        uri = "/vocab/" + self.username + "/" + name + "/"
        return self.Post(entry, uri= uri)

    def deleteVocab(self, entry):
        """ Deletes the vocab instance that was passed as argument.

            @param dict The content vocab dict that should be deleted from META.
        """
        name = entry["entry"]["content"]["params"]["name"]
        uri = "/vocab/" + self.username + "/" + name + "/"
        return self.Delete(uri = uri)

    def getVocabList(self, query = None):
        """ Retrieves a vocab list. 

            @param query raws_json.Query object that contains queryset args.
            @return List of vocab dicts.
        """
        uri = "/vocab/" + self.username + "/"
        if query:
            query.feed = uri
            uri = query.ToUri()
        return self.Get(uri = uri)

    def getVocabInstance(self, name):
        """ Retrieves a vocab entry with name passed in the argument. 

            @param string Name of the vocab instance to be retrieved.
            @return Vocab entry dict
        """
        uri = "/vocab/" + self.username + "/" + name + "/"
        return self.Get(uri = uri)

    def updateVocabName(self, entry, name):
        """ Tries to POST a new vocab resource to META, in order to update the entry that was passed as argument.

            @param dict The (modified) vocab entry dict, that will be posted to META.
            @return Vocab entry dict
        """
        uri = "/vocab/" + self.username + "/" + name + "/"
        return self.Post(entry, uri= uri)

    # GET Ext
    # -------------

    def getExtJson(self, query = None):
        """ Retrieves a ext list in json. 

            @param query raws_json.Query object that contains queryset args.
            @return List of content dicts (virtual or real).
        """
        uri = "/ext/json/" + self.username + "/"
        if query:
            query.feed = uri
            uri = query.ToUri()
        return self.Get(uri = uri)
        
    def getExtAtom(self, query = None):
        """ Retrieves a ext list in atom. 

            @param query raws_json.Query object that contains queryset args.
            @return List of content dicts (virtual or real).
        """
        uri = "/ext/atom/" + self.username + "/"
        if query:
            query.feed = uri
            uri = query.ToUri()

        server_response = self.handler.HttpRequest(self, 'GET', None, uri, extra_headers= {"Accept":"application/atom"})
        result_body = server_response.read()

        if server_response.status == 200:
            return result_body
        else:
            raise RequestError, {'status': server_response.status,
              'reason': server_response.reason, 'body': result_body}
        
    def getExtMrss(self, rtmp = False, query = None):
        """ Retrieves a ext list in json. 

            @param query raws_json.Query object that contains queryset args.
            @return List of content dicts (virtual or real).
        """
        uri = "/ext/mrss/" + self.username + "/"
        if rtmp:
            uri = "/ext/mrss-jw-rtmp/" + self.username + "/"
        if query:
            query.feed = uri
            uri = query.ToUri()

        server_response = self.handler.HttpRequest(self, 'GET', None, uri, extra_headers= {"Accept":"application/xml"})
        result_body = server_response.read()

        if server_response.status == 200:
            return result_body
        else:
            raise RequestError, {'status': server_response.status,
              'reason': server_response.reason, 'body': result_body}

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
import json, os
import raws_json
from raws_json.raws_service import RawsService, Feed, Query, RequestError

class RassService(RawsService):

    def __init__(self, username=None, password=None, server=None, ssl = False):
        self.username = username
        super(RassService, self).__init__(username = username, password = password, server = server, ssl = ssl)

    def delete(self, uri):
        """ Deletes any resource, given the uri. """
        return self.Delete(uri = uri)

    def getItemHeader(self, uri):
        """ Does a HTTP HEAD request to RASS for the given URI and returns the status code.

            @param string: URL of the item
            @return int : status code (200 or 404)
        """
        http_resp = self.Head(uri = uri)
        return http_resp.status

    def getItemHeaderFromPath(self, path):
        """ Does a HTTP HEAD request to RASS for the given item path and returns the status code.

            @param string: relative path to the file on the CDN
            @return int : status code (200 or 404)
        """
        return self.getItemHeader(uri = "/item/" + path.lstrip("/"))

    # ITEM METHODS
    # -----------

    def createItem(self, dirpath, filename, local_path, force_create = True):
        """ Creates a new RASS item resource by uploading a file (= a file on the CDN). 

            @param string dirpath : path to the directory (on the rambla CDN) in which the item needs to be created.
            @param string filename : proposed filename to be used when storing the file (RASS will append a suffix if file already exists on CDN and force_create == True).
            @param string local_path : location of the file to be uploaded on the local machine
            @param bool force_create : If True, append suffix to filename if file already exists. If False, return HTTP error if already exists.
            @return item object (= result of json.decode(response_body))
        """
        uri = "/item/" + dirpath.lstrip("/")
        media_source = raws_json.MediaSource(file_path = local_path, svr_filename = filename)
        if force_create: # do POST
            media_entry = self.Post(data = None, uri = uri, media_source = media_source)
        else:
            uri = uri.rstrip("/") + "/" + filename # PUT requires filename to be part of the URL path
            media_entry = self.Put(data = None, uri = uri, media_source = media_source)
        return media_entry

    def itemExists(self, path):
        """ Checks if a RASS item (= file on the CDN) exists?

            @param string: relative path to the file on the CDN
            @return bool : True if exists
        """
        return self.itemUrlExists(uri = "/item/" + path.lstrip("/"))

    def itemUrlExists(self, uri):
        """ Checks if a RASS item (= file on the CDN) exists?

            @param string: URL of the item
            @return bool : True if exists
        """
        exists = False
        http_resp = self.Head(uri = uri)
        if http_resp.status == 200:
            exists = True
        return exists
        
    def deleteItem(self, path):
        """ Deletes a RASS item (file on the CDN + RASS resource attached to it)
        
            @param string: relative path to the file on the cdn
        """
        uri = "/item/" + path.lstrip("/")
        return self.delete(uri)

    # DIR METHODS
    # -----------
        
    def createDir(self, path, force_create = False):
        """ Creates a new RASS dir resource (= a directory on the CDN). 
    
            @param string path : path to the directory (on the rambla CDN) that needs to be created.
            @param bool force_create : If True, append suffix to directory name if the directory already exists. If False, return HTTP error if already exists.
            @return dir object (= result of json.decode(response_body))
        """
        uri = "/dir/" + path.lstrip("/")
        if force_create:
            return self.Post(data = None, uri = uri)
        else:
            return self.Put(data = None, uri = uri)
            
    def dirExists(self, path):
        """ Checks if a RASS dir exists at the given path.

            @param string : relative path to the directory of which the existence needs to be checked
            @return book True if dir exists.
        """
        exists = False
        qry = Query()
        qry["kind"] = "root"
        try:
            feed = self.getDirList(path, qry)
            exists = True
        except RequestError, e:
            pass
        return exists
        
    def getDirList(self, path, query = None):
        """ Retrieve the content of a directory.

            @param string : relative path to the directory to be retrieved
            @param query raws_json.Query object that contains queryset args.
            @return dir feed (= result of json.decode(response_body))
        """
        uri = "/dir/" + path.lstrip("/")
        if query:
            query.feed = uri
            uri = query.ToUri()
        return self.Get(uri = uri)

    def deleteDir(self, path, recursive = False):
        """ Deletes a RASS item (file on the CDN + RASS resource attached to it)

            @param string: relative path to the file on the cdn
        """
        uri = "/dir/" + path.lstrip("/")
        if recursive:
            query = Query()
            query["recursive"] = "1"
            query.feed = uri
            uri = query.ToUri()
        return self.delete(uri)
        
    # META METHODS
    # -----------

    def get_meta_info(self, path, query = None):
        """ Sends a GET meta request with the given path.
        
            @param string Relative path to a file or directory (pass "/" for root-directory) on the CDN
            @return single meta object
        """
        uri = "/meta/" + self.username + "/" + path.lstrip("/")
        if query:
            query.feed = uri
            uri = query.ToUri()
        return self.Get(uri = uri)
    
    def get_file_info(self, path, query = None):
        """ Sends a GET meta request for the file identified on the CDN by path.
        
            @param string Relative path to the file on the CDN
            @return single meta object
        """
        return self.get_meta_info(path, query)

    def get_dir_info(self, path, query = None):
        """ Sends a GET meta request for the directory identified on the CDN by path.

            @param string Relative path to the directory on the CDN
            @return a list (feed) of meta objects
        """
        return self.get_meta_info(path, query)
        


        


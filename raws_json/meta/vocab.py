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

class Vocab(object):
    
    def __init__(self, name = None, description = None, xml_namespace = None, entry = None):
        self.clear()
        # if the entry is passed instead of params, use that to populate datamembers
        if entry is not None:
            self.from_entry(entry)
        else:
            if name:
                self.name = name
            if description:
                self.description = description
            if xml_namespace:
                self.xml_namespace = xml_namespace
        
    def clear(self):
        self.name = ""
        self.description = ""
        self.xml_namespace = ""
            
    def from_entry(self, entry):
        """ Set datamembers from entry. """
        self.clear()
        if "name" in entry["entry"]["content"]["params"]:
            self.name = entry["entry"]["content"]["params"]["name"]
        if "description" in entry["entry"]["content"]["params"]:
            self.description = entry["entry"]["content"]["params"]["description"]
        if "xml_namespace" in entry["entry"]["content"]["params"]:
            self.xml_namespace = entry["entry"]["content"]["params"]["xml_namespace"]
    
    def to_entry(self):
        entry = {"entry":{"content":{"params":{"name": self.name, "description": self.description, "xml_namespace": self.xml_namespace,},},},}
        return entry

    def __eq__(self, other):
        if isinstance(other, Vocab):
            if unicode(self.name) != unicode(other.name):
                return False
            if unicode(self.description) != unicode(other.description):
                return False
            if unicode(self.xml_namespace) != unicode(other.xml_namespace):
                return False
            return True
        else:
            return NotImplemented
        return False

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

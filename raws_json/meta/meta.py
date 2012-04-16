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

class MetaObj(object):

    def __init__(self, meta_name = None, vocab = None, text = None, lang = None, attrs = None, meta_dict = None):
        self.clear()
        # if the meta_dict is passed instead of params, use that to populate datamembers
        if meta_dict:
            self.from_dict(meta_dict)
        else:
            if vocab:
                self.vocab = vocab
            if meta_name:
                self.meta_name = meta_name
            if text:
                self.text = text
            if lang:
                self.lang = lang
            if attrs:
                self.attrs = attrs
        
    def clear(self):
        self.vocab = ""
        self.meta_name = ""
        self.text = ""
        self.lang = ""
        self.attrs = {}
        
    def from_dict(self, dict_data):
        for k,v in dict_data.items():
            if "vocab" == k:
                self.vocab = v
            elif "meta_name" == k:
                self.meta_name = v
            elif "text" == k:
                self.text = v
            elif "lang" == k:
                self.lang = v
            else:
                self.attrs[k] = v

    def to_dict(self):
        meta_dict = {"vocab":self.vocab, "meta_name":self.meta_name, "text":self.text, "lang":self.lang,}
        for k,v in self.attrs:
            meta_dict[k] = v
        return meta_dict
    
    def __eq__(self, other):
        if isinstance(other, MetaObj):
            if unicode(self.vocab) != unicode(other.vocab):
                return False
            if self.meta_name != other.meta_name:
                return False
            if unicode(self.text) != unicode(other.text):
                return False
            if unicode(self.lang) != unicode(other.lang):
                return False
            if self.attrs != other.attrs:
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
        
class FileObj(object):

    def __init__(self, path = None, media_type = None, size = None, duration = None, container = None, bitrate = None, width = None, height = None, 
                    frames = None, framerate = None, samplerate = None, file_dict = None):
        self.clear()
        # if the file_dict is passed instead of params, use that to populate datamembers
        if file_dict:
            self.from_dict(file_dict)
        else:
            if path:
                self.set_path(path)
            if media_type:
                self.media_type = media_type
            if duration:
                self.duration = duration
            if size:
                self.size = size
            if container:
                self.container = container
            if bitrate:
                self.bitrate = bitrate
            if width:
                self.width = width
            if height:
                self.height = height
            if frames:
                self.frames = frames
            if framerate:
                self.framerate = framerate
            if samplerate:
                self.samplerate = samplerate

    def clear(self):
        self.path = ""
        self.filename = ""
        self.extension = ""
        self.media_type = ""
        self.duration = ""
        self.size = ""
        self.container = ""
        self.bitrate = ""
        self.width = ""
        self.height = ""
        self.frames = ""
        self.framerate = ""
        self.samplerate = ""

    def from_dict(self, dict_data):
        if "path" in dict_data:
            self.path = dict_data["path"]
        if "filename" in dict_data:
            self.filename = dict_data["filename"]
        if "extension" in dict_data:
            self.extension = dict_data["extension"]
        if "media_type" in dict_data:
            self.media_type = dict_data["media_type"]
        if "duration" in dict_data:
            self.duration = dict_data["duration"]
        if "size" in dict_data:
            self.size = dict_data["size"]
        if "container" in dict_data:
            self.container = dict_data["container"]
        if "bitrate" in dict_data:
            self.bitrate = dict_data["bitrate"]
        if "width" in dict_data:
            self.width = dict_data["width"]
        if "height" in dict_data:
            self.height = dict_data["height"]
        if "frames" in dict_data:
            self.frames = dict_data["frames"]
        if "framerate" in dict_data:
            self.framerate = dict_data["framerate"]
        if "samplerate" in dict_data:
            self.samplerate = dict_data["samplerate"]
        
    def to_dict(self):
        return {"path":self.path, "media_type":self.media_type, "duration":self.duration, "size":self.size, "container":self.container, "bitrate":self.bitrate,
                "width":self.width, "height":self.height, "frames":self.frames, "framerate":self.framerate, "samplerate":self.samplerate}

    def set_path(self, path):
        self.path = u"/" + path.lstrip('/').rstrip('/')
        
    def __eq__(self, other):
        if isinstance(other, FileObj):
            if unicode(self.path) != unicode(other.path):
                print "file.path not equal"
                return False
            if self.media_type:
                if unicode(self.media_type) != unicode(other.media_type):
                    print "file.media_type not equal"
                    return False
            if self.duration:
                if not other.duration:
                    return False
                if int(self.duration) != int(other.duration):
                    print "file.duration not equal"
                    return False
            if self.size and other.size: # size is set by the META service, so only compare if both objects have a size
                if int(self.size) != int(other.size):
                    print "file.size not equal"
                    return False
            if unicode(self.container) != unicode(other.container):
                print "file.container not equal"
                return False
            if self.bitrate:
                if not other.bitrate:
                    return False
                if int(self.bitrate) != int(other.bitrate):
                    print "file.bitrate not equal"
                    return False
            if self.width:
                if not other.width:
                    return False
                if int(self.width) != int(other.width):
                    print "file.width not equal"
                    return False
            if self.height:
                if not other.height:
                    return False
                if int(self.height) != int(other.height):
                    print "file.height not equal"
                    return False
            if self.frames:
                if not other.frames:
                    return False
                if int(self.frames) != int(other.frames):
                    print "file.frames not equal"
                    return False
            if self.framerate:
                if not other.framerate:
                    return False
                if int(self.framerate) != int(other.framerate):
                    print "file.framerate not equal"
                    return False
            if self.samplerate:
                if not other.samplerate:
                    return False
                if int(self.samplerate) != int(other.samplerate):
                    print "file.samplerate not equal"
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

    

class MetaContent(object):
    
    def __init__(self, name = None, file_objs = None, tags = None, meta_objs = None, thumb_used = None, update_files = None, yt_id = None, entry = None):
        self.clear()
        # if the entry is passed instead of params, use that to populate datamembers
        if entry is not None:
            self.from_entry(entry)
        else:
            if name:
                self.name = name
            if file_objs:
                self.file_objs = file_objs
            if tags:
                self.tags = tags
            if meta_objs:
                self.meta_objs = meta_objs
            if thumb_used:
                self.set_thumb_used(thumb_used)
            if update_files:
                self.update_files = update_files
            if yt_id:
                self.yt_id = yt_id
        
    def clear(self):
        # files
        self.file_objs = [] # list of file objects
        # params
        self.name = None
        self.meta_updated = None
        self.yt_id = None
        self.tags = [] # list of tag strings
        self.meta_objs = [] # list of meta objects
        # file_params
        self.thumb_used = ""
        self.update_files = 0
            
    def from_entry(self, entry):
        """ Set datamembers from entry. """
        self.clear()
        self.name = entry["entry"]["content"]["params"]["name"]
        self.meta_updated = entry["entry"]["content"]["params"]["meta_updated"]
        self.yt_id = entry["entry"]["content"]["params"]["yt_id"]
        self.thumb_used = entry["entry"]["content"]["file_params"]["thumb_used"]
        self.update_files = entry["entry"]["content"]["file_params"]["update_files"]
        # set tags
        if "tag" in entry["entry"]["content"]["params"]:
            for t in entry["entry"]["content"]["params"]["tag"]:
                self.tags.append(t)
        # set meta objs
        if "meta" in entry["entry"]["content"]["params"]:
            for m_dict in entry["entry"]["content"]["params"]["meta"]:
                self.meta_objs.append(MetaObj(meta_dict = m_dict))
        # set files
        for f_dict in entry["entry"]["content"]["file"]:
            self.file_objs.append(FileObj(file_dict = f_dict))
    
    def to_entry(self):
        entry = {"entry":{"content":{},},}
        # set file array
        entry["entry"]["content"]["file"] = []
        for f in self.file_objs:
            entry["entry"]["content"]["file"].append(f.to_dict())
        # set params dict
        entry["entry"]["content"]["params"] = {"name":self.name,}
        if self.yt_id:
            entry["entry"]["content"]["params"]["yt_id"] = self.yt_id
        if self.tags:
            entry["entry"]["content"]["params"]["tag"] = self.tags
        if self.meta_objs:
            entry["entry"]["content"]["params"]["meta"] = []
            for m in self.meta_objs:
                entry["entry"]["content"]["params"]["meta"].append(m.to_dict())
        # set file_params dict
        entry["entry"]["content"]["file_params"] = {"thumb_used":self.thumb_used,"update_files":self.update_files}
        
        return entry
        
    def set_thumb_used(self, thumb_used):
        self.thumb_used = u"/" + thumb_used.lstrip('/').rstrip('/')
        
    def compare_file_objs(self, file_objs):
        """ Compares the file_objs param to self.file_objs. 
        
            True if file_objs are the same.
        """
        if len(self.file_objs) != len(file_objs):
            print "len fault"
            return False
        for f in self.file_objs:
            found_equal_path = False
            for f2 in file_objs:
                print "comparing %s path to %s path" % (f.path, f2.path)
                if unicode(f.path) == unicode(f2.path):
                    found_equal_path = True
                    if f != f2:
                        print "file objects with same path are not equal"
                        return False
                    else:
                        break
            if not found_equal_path:
                print "%s path not found in param obj" % f.path
                return False
        return True      

    def compare_meta_objs(self, meta_objs):
        """ Compares the meta_objs param to self.meta_objs. 

            True if meta_objs are the same.
        """
        if len(self.meta_objs) != len(meta_objs):
            print "len fault"
            return False
        for m in self.meta_objs:
            found_equal_meta = False
            for m2 in meta_objs:
#                print "comparing %s:%s:%s to %s:%s:%s" % (m.vocab, m.meta_name, m.lang, m2.vocab, m2.meta_name, m.lang)
                # # print m.meta_name.type
                # # print m2.meta_name.type
                if unicode(m.meta_name) == unicode(m2.meta_name) and ("%s:%s" % (m.vocab, m.lang) == "%s:%s" % (m2.vocab, m2.lang)):
                    found_equal_meta = True
                    if m != m2:
                        print "%s not equal to %s" % (str(m), str(m2)) 
                        return False
                    else:
                        break
            if not found_equal_meta:
                print "%s:%s not found in param" % (m.vocab, m.meta_name)
                return False
        return True      
                    
    def __eq__(self, other):
        """ == operator overload """
        if isinstance(other, MetaContent):
            if unicode(self.name) != unicode(other.name):
                print "self.name " + self.name + " doesn't compare to other.name " + other.name
                return False
            if self.tags != other.tags:
                print "self.tags " + str(self.tags) + " don't compare to other.tags " + str(other.tags)
                return False
            if not self.compare_file_objs(other.file_objs):
                print "compare_file_objs failed"
                return False
            if not self.compare_meta_objs(other.meta_objs):
                print "compare_meta_objs failed"
                return False
            return True
        else:
            return NotImplemented
        return False

    def __ne__(self, other):
        """ != operator overload """
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

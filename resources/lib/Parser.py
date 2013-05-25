# -*- coding=utf8 -*-
#******************************************************************************
# Parser.py
#------------------------------------------------------------------------------
#
# Copyright (c) 2013 LivingOn <LivingOn@xmail.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#******************************************************************************
import re
import xml.sax as sax

from resources.lib.RssHandler import RssHandler

class Parser(object):
    
    _url         = None
    _reobj_folge = None
    _reobj_thema = None
    
    def __init__(self, url, regex_folge, regex_thema):
        self._url = url
        self._reobj_folge = re.compile(regex_folge)
        self._reobj_thema = re.compile(regex_thema)
        
    def get_data(self):
        handler = RssHandler()
        try: 
            parser = sax.make_parser() 
            parser.setContentHandler(handler)
            parser.parse(self._url) 
            result = []
            for (title, dummy_date, desc, url) in handler.result:
                result.append((
                    self._get_folge(title), 
                    self._get_thema(desc), 
                    url
                ))
        except Exception:
            result = None
        return result
    
    def _get_folge(self, title):
        return self._filter_text(self._reobj_folge, title)
    
    def _get_thema(self, desc):
        return self._filter_text(self._reobj_thema, desc)
    
    def _filter_text(self, reobj, text):
        try:
            result = reobj.search(text).group(1)
        except: 
            result = text
        return result 

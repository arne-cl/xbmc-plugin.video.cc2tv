# -*- coding=utf8 -*-
#******************************************************************************
# RssHandler.py
#------------------------------------------------------------------------------
#
# Copyright (c) 2009, 2013 LivingOn <LivingOn@xmail.net>
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
import xml.sax as sax

class RssHandler(sax.handler.ContentHandler):

    result       = None
    _aktiv       = None
    _title       = None
    _pubDate     = None
    _description = None
    _enclosure   = None

    def __init__(self): 
        self.result = []
        self._aktiv = None 
        self._resetVariables()
    
    def startElement(self, name, attrs): 
        if name == "item": 
            self._resetVariables()
        elif name == "title" or name == "pubDate" or name == "description": 
            self._aktiv = name
        elif name == "enclosure":
            self._enclosure = attrs["url"]

    def endElement(self, name):
        if name == "item": 
            self.result.append( 
               (self._title, self._pubDate, self._description, self._enclosure))
        elif name == "title" or name == "pubDate" or \
                                name == "description" or name == "enclosure": 
            self._aktiv = None

    def characters(self, content): 
        if self._aktiv == "title": 
            self._title += content 
        elif self._aktiv == "pubDate": 
            self._pubDate += content
        elif self._aktiv == "description": 
            if self._description == "":
                self._description += content

    def _resetVariables(self):
        self._title = "" 
        self._pubDate = ""
        self._description = ""
        self._enclosure = ""

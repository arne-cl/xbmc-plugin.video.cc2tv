# -*- coding=utf8 -*-
#******************************************************************************
# addon.py
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
import sys
import xbmcgui
import xbmcaddon
import xbmcplugin

from resources.lib.Parser import Parser

class CCZwei(object):
    
    PLUGIN_NAME = "plugin.video.cczwei"
    
    _plugin_id   = None
    _addon       = None
    _rss_feed    = None
    _regex_folge = None
    _regex_thema = None
    
    def __init__(self):
        self._register_addon()
        self._load_settings()
        self._add_directory_items()
        
    def _register_addon(self):
        self._plugin_id = int(sys.argv[1])
        self._addon = xbmcaddon.Addon(id = self.PLUGIN_NAME)

    def _load_settings(self):
        self._rss_feed = xbmcplugin.getSetting(self._plugin_id, "rss_feed")
        self._regex_folge = r"%s" % xbmcplugin.getSetting(self._plugin_id, "regex_folge")
        self._regex_thema = r"%s" % xbmcplugin.getSetting(self._plugin_id, "regex_thema")

    def _add_directory_items(self):
        feed_data = Parser(self._rss_feed, self._regex_folge, self._regex_thema).get_data()
        if feed_data:
            for (folge, thema, stream_url) in feed_data:
                item = xbmcgui.ListItem("%s - %s" % (folge, thema))
                xbmcplugin.addDirectoryItem(self._plugin_id, stream_url, item)
            xbmcplugin.endOfDirectory(self._plugin_id)
        else:
            title = self._addon.getLocalizedString(30110)
            msg = self._addon.getLocalizedString(30120)
            xbmcgui.Dialog().ok(title, msg)
            
if __name__ == "__main__":
    CCZwei()

                
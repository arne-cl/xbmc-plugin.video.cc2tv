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
import urllib
import xbmcgui
import xbmcaddon
import xbmcplugin

from resources.lib.Parser import Parser

class CCZwei(object):
    
    PLUGIN_NAME = "plugin.video.cczwei"
    
    _plugin_id      = None
    _addon          = None
    _rss_video_feed = None
    _rss_audio_feed = None
    _regex_folge    = None
    _regex_thema    = None
    
    def __init__(self):
        self._register_addon()
        self._load_settings()
        self._add_directory_items()
        
    def _register_addon(self):
        self._plugin_id = int(sys.argv[1])
        self._addon = xbmcaddon.Addon(id = self.PLUGIN_NAME)

    def _load_settings(self):
        self._rss_video_feed = xbmcplugin.getSetting(self._plugin_id, "rss_video_feed")
        self._rss_audio_feed = xbmcplugin.getSetting(self._plugin_id, "rss_audio_feed")
        self._regex_folge = r"%s" % xbmcplugin.getSetting(self._plugin_id, "regex_folge")
        self._regex_thema = r"%s" % xbmcplugin.getSetting(self._plugin_id, "regex_thema")

    def _add_directory_items(self):
        if not sys.argv[2]:
            self._create_submenues()
        else:
            self._read_feed_data_into_directory(sys.argv[2])

    def _create_submenues(self):
        self._add_item_to_directory("Videopodcast", None, True)
        self._add_item_to_directory("Audiopodcast", None, True)
        xbmcplugin.endOfDirectory(self._plugin_id)

    def _read_feed_data_into_directory(self, mode):
        if mode == "?mode=Videopodcast":
            rss_feed = self._rss_video_feed
        else:
            rss_feed = self._rss_audio_feed
        feed_data = Parser(rss_feed, self._regex_folge, self._regex_thema).get_data()
        if feed_data:
            for (folge, thema, stream_url) in feed_data:
                self._add_item_to_directory("%s - %s" % (folge, thema), stream_url)
            xbmcplugin.endOfDirectory(self._plugin_id)
        else:
            title = self._addon.getLocalizedString(30110)
            msg = self._addon.getLocalizedString(30120)
            xbmcgui.Dialog().ok(title, msg)

    def _add_item_to_directory(self, title, url, isfolder=False):
        if isfolder:
            url = sys.argv[0] + "?" + urllib.urlencode({'mode' : title})
        item = xbmcgui.ListItem(title)
        xbmcplugin.addDirectoryItem(self._plugin_id, url, item, isfolder)
            
if __name__ == "__main__":
    CCZwei()
                
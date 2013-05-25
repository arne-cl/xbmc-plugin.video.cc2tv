# *-* coding=utf8 *-*
from resources.lib.Parser import Parser

class Test_Parser(object):
    
    def test__init__(self):
        parser = _get_parser_for_test_feed()
        # prüfe ob korrekt initialisiert wurde
        assert parser._url == _get_feed()
        assert parser._reobj_folge.pattern == _get_folge_pattern()
        assert parser._reobj_thema.pattern == _get_thema_pattern()
        
    def test_get_data(self):
        parser = _get_parser_for_test_feed()
        #prüfe ob die daten korrekt ermittelt wurden
        feed_data = parser.get_data()
        assert feed_data[0][0] == u"108. Folge"
        assert feed_data[0][1] == u"Raspberry PI \x96 ein erster Eindruck. "
        assert feed_data[0][2] == u"http://cczwei.mirror.speedpartner.de/cc2tv/CC2_108.mp4"
        
    def test__get_folge(self):
        parser = _get_parser_for_test_feed()
        assert parser._get_folge(u"CC2-NRWTV - 108. Folge") == "108. Folge"
        
    def test__get_thema(self):
        parser = _get_parser_for_test_feed()
        desc = u"Heute: CC2: Raspberry PI  ein erster Eindruck. "
        assert parser._get_thema(desc) == u"Raspberry PI \x96 ein erster Eindruck. "
        
def _get_parser_for_test_feed():
    return Parser(_get_feed(), _get_folge_pattern(), _get_thema_pattern() )

def _get_feed():
    return "data/feed.xhtml"

def _get_folge_pattern():
    return "- (\d+. Folge)"

def _get_thema_pattern():
    return "Heute: CC2: (.*)"
    
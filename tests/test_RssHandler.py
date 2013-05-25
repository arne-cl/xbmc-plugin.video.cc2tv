# *-* coding=utf8 *-*
from resources.lib.RssHandler import RssHandler

class Test_RssHandler(object):

    def test__init__(self):
        rsshandler = RssHandler()
        assert ["","","",""] == _get_datafields(rsshandler)
    
    def test_startElement(self):
        # prüfe ob RssHandler korrekt mit Daten gefüllt werden kann
        rsshandler = _get_rsshandler_with_data()
        assert _get_datafields(rsshandler) == ["a","b","c","d"]

        # prüfe ob diese Schlüsselworte kein Reset ausführen
        for key in ("title","pubDate","description","enclosure"):
            rsshandler = _get_rsshandler_with_data()
            rsshandler.startElement(key, {"url":"d"})
            assert _get_datafields(rsshandler) == ["a","b","c","d"]

        # prüfe ob "item" ein Reset durchführt
        rsshandler = _get_rsshandler_with_data()
        rsshandler.startElement("item", {"url":"d"})
        assert _get_datafields(rsshandler) == ["","","",""]

        # prüfe ob die folgende Schlüsselworte das Feld "_aktiv" ändern
        for key in ("title","pubDate","description"):
            rsshandler = _get_rsshandler_with_data()
            rsshandler.startElement(key, {"url":"d"})
            assert rsshandler._aktiv == key

        # prüfe ob die folgenden Schlüsselworte das Feld "_aktiv" nicht ändern
        for key in ("item","enclosure"):
            rsshandler = _get_rsshandler_with_data()
            rsshandler.startElement(key, {"url":"d"})
            assert rsshandler._aktiv != key
            
        # prüfe ob "enclosure" korrekt gesetzt wird
        rsshandler = _get_rsshandler_with_data()
        rsshandler.startElement("enclosure", {"url":"/path/to/nowhere"})
        assert rsshandler._enclosure == "/path/to/nowhere"
        
    def test_endElement(self):
        # prüfe ob Feld "result" vorm Start leer ist
        rsshandler = _get_rsshandler_with_data()
        assert rsshandler.result == []
        
        # prüfe ob bei "item" alle Datenfelder in "result" übernommen werden
        rsshandler.endElement("item")
        assert rsshandler.result == [("a","b","c","d")]
        
        # prüfe ob die folgenden Schlüsselwörter das Feld "_aktiv" zurücksetzen
        for key in ("title","pubDate","description","enclosure"):
            rsshandler = _get_rsshandler_with_data()
            rsshandler._aktiv = key
            rsshandler.endElement(key)
            assert rsshandler._aktiv == None
            
        # prüfe ob "item" das Feld "_aktiv" nicht zurücksetzt
        rsshandler = _get_rsshandler_with_data()
        feldinhalt = "bleibt unangetastet!"
        rsshandler._aktiv = feldinhalt
        rsshandler.endElement("item")
        assert rsshandler._aktiv == feldinhalt

    def test_characters(self):
        # prüfe ob Daten richtig zugeordnet werden
        rsshandler = RssHandler()
        rsshandler._aktiv = "title"
        rsshandler.characters("testdaten title")
        assert rsshandler._title == "testdaten title"
        
        rsshandler._aktiv = "pubDate"
        rsshandler.characters("testdaten pubDate")
        assert rsshandler._pubDate == "testdaten pubDate"
        
        rsshandler._aktiv = "description"
        rsshandler.characters("testdaten description")
        assert rsshandler._description == "testdaten description"
        

def _get_rsshandler_with_data():
    rsshandler = RssHandler()
    rsshandler._title = "a"
    rsshandler._pubDate = "b"
    rsshandler._description = "c"
    rsshandler._enclosure = "d"
    return rsshandler
    
def _get_datafields(rsshandler):
    return [
        rsshandler._title,
        rsshandler._pubDate,
        rsshandler._description,
        rsshandler._enclosure
    ]    
   

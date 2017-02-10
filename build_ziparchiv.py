#!/usr/bin/env python
from zipfile import ZipFile, ZIP_DEFLATED

class Build(object):
    
    NAME = "plugin.video.cc2tv"
    FILES = [
        "addon.py",
        "addon.xml",
        "changelog.txt",
        "icon.png",
        "LICENSE.TXT",
        "resources/__init__.py",
        "resources/settings.xml",
        "resources/language/English/strings.xml",
        "resources/language/German/strings.xml",
        "resources/lib/__init__.py",
        "resources/lib/Parser.py",
        "resources/lib/RssHandler.py"
    ]
    
    def create_ziparchiv(self, path):
        print("create ziparchiv %s" % path)
        ziparchiv = ZipFile(path, "w")
        count = 0
        for f in self.FILES:
            print("   add %s" % f)
            count += 1
            ziparchiv.write(f, "%s/%s" % (self.NAME,f), ZIP_DEFLATED)
        ziparchiv.close()
        print("%d files added" % count)
            
    
if __name__ == "__main__":
    build = Build()
    build.create_ziparchiv("%s.zip" % build.NAME)    
        

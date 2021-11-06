import os
import pkg_resources
from pysword.modules import SwordModules

DATA_DIR = pkg_resources.resource_filename(__name__, "resources/sword")

BIBLE_VERSION = {
    'AKJV': {'file':'AKJV.zip',
             'description': "American King James Version.  \r"
                            "Produced by Stone Engelbrite.  \r"
                            "For more details see: http://www.crosswire.org/sword/modules/ModInfo.jsp?modName=AKJV"
             },
    'ASV': {'file':'ASV.zip',
             'description': "American Standard Version (1901). \r"
                            "For more details see: http://www.crosswire.org/sword/modules/ModInfo.jsp?modName=ASV"
             },

}

def HelloSword():
    print("Hello from biblearn.sword.  DATA_DIR: {}".format(DATA_DIR))


def loadData(version="AKJV"):
    version = version.upper()
    if version not in BIBLE_VERSION.keys():
        raise Exception("Invalid SWORD Bible Version: {}.  Must be one of: {}".format(version, BIBLE_VERSION.keys()))

    modules = SwordModules(os.path.join(DATA_DIR,BIBLE_VERSION[version]['file']))
    found_modules = modules.parse_modules()
    bible = modules.get_bible_from_module(u'AKJV')
    # Get John chapter 3 verse 16
    output = bible.get(books=[u'john'], chapters=[3], verses=[16])
    return output
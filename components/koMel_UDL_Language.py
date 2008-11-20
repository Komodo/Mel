# Komodo Mel language service.

import logging
from koUDLLanguageBase import KoUDLLanguage


log = logging.getLogger("koMelLanguage")
#log.setLevel(logging.DEBUG)


def registerLanguage(registry):
    log.debug("Registering language Mel")
    registry.registerLanguage(KoMelLanguage())


class KoMelLanguage(KoUDLLanguage):
    name = "Mel"
    lexresLangName = "Mel"
    _reg_desc_ = "%s Language" % name
    _reg_contractid_ = "@activestate.com/koLanguage?language=%s;1" % name
    _reg_clsid_ = "78c36838-be2a-4193-b154-81d7026458c4"
    defaultExtension = '.mel'

    lang_from_udl_family = {
        'SSL': 'Mel'
    }

    commentDelimiterInfo = {
        "line": [ "//", ],
    }

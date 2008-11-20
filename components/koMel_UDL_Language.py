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

    variableIndicators = '$'
    _dedenting_statements = [u'return', u'break', u'continue']
    _indenting_statements = [u'case']
    supportsSmartIndent = "brace"

    sample = """// animated duplicate/instance script
proc animatedDuplication(int $rangeStart, int $rangeEnd,
                         int $numOfDuplicates, int $duplicateOrInstance) {
    int $range_start = $rangeStart;
    int $range_end = $rangeEnd;
    int $num_of_duplicates = $numOfDuplicates;
    int $step_size = ($range_end - $range_start) / $num_of_duplicates;
    int $i = 0;
    int $temp;
  
    currentTime $range_start;     // set to range start
  
    string $selectedObjects[];    // to store selected objects
    $selectedObjects = `ls -sl`;  // store selected objects
    select $selectedObjects;
  
    while ($i <= $num_of_duplicates) {
        $temp = $range_start + ($step_size * $i);
        currentTime ($temp);
        // seleced the objects to duplicate or instance
        select $selectedObjects;
        if ($duplicateOrInstance == 0) {
            duplicate;
        } else {
            instance;
        }
        $i++;
    }
}
"""

    # Overriding these base methods to work around bug 81066.
    def get_linter(self):
        return None
    def get_interpreter(self):
        None

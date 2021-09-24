import polib
import json
from polib import MOFile, MOEntry

if __name__ == '__main__':
    mo_strings: MOFile = polib.mofile("global.mo")

    with open('en.json', "w") as f:
        dict_strings = {}
        for mo_string in mo_strings:
            mo_string: MOEntry
            dict_strings[mo_string.msgid] = mo_string.msgstr
        json.dump(dict_strings, f)


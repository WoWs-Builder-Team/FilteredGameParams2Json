import polib
from polib import MOFile, MOEntry

if __name__ == '__main__':
    mo_strings: MOFile = polib.mofile("global.mo")

    with open('en.csv', "w") as f:

        for mo_string in mo_strings:
            mo_string: MOEntry
            msgstr = f'"{mo_string.msgstr}"' if "," in mo_string.msgstr else mo_string.msgstr
            f.write(f'{mo_string.msgid},{msgstr}\n')


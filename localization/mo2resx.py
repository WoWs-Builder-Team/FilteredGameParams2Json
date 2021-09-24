import polib
from lxml import etree
from polib import MOFile, MOEntry

if __name__ == '__main__':
    mo_strings: MOFile = polib.mofile("global.mo")
    dict_strings = {}

    root = etree.Element('root')

    for mo_string in mo_strings:
        mo_string: MOEntry
        dict_strings[mo_string.msgid] = mo_string.msgstr

        data = etree.Element("data", attrib={"name": mo_string.msgid})
        data.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")

        value = etree.Element("value")
        value.text = mo_string.msgstr

        data.append(value)

        root.append(data)

    root.getroottree().write('en.resx', pretty_print=True, xml_declaration=True, encoding='UTF-8')
    # with open("output.xml", "w") as f:


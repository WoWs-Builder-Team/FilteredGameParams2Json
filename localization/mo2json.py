import polib
import json
import argparse
import csv
from os import path
from polib import MOFile

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", help="Filter. A csv file.", type=str, required=True)
    parser.add_argument("--mofile", help="WoWS localization file.", type=str, required=True)
    parser.add_argument("--out", help="Output json file.", type=str, required=False, default="strings.json")
    parsed = parser.parse_args()

    if not all([path.exists(i) and path.isfile(i) for i in [parsed.filter, parsed.mofile]]):
        raise RuntimeError

    mo_strings: MOFile = polib.mofile(parsed.mofile)
    game_strings = {mo_string.msgid: mo_string.msgstr for mo_string in mo_strings}
    with open(parsed.filter, 'r') as f:
        filter_strings = [i[0] for i in csv.reader(f)]

    filtered_strings = {}

    # this uses the whole index, ex `PCY009`
    # Super slow. aleast for my laptop.

    # for filter_string in filter_strings:
    #     for game_string, value in game_strings.items():
    #         split = game_string.split('_')
    #         index = filter_string.split('_')[0]
    #
    #         if index in split:
    #             if filter_string not in filtered_strings:
    #                 filtered_strings[filter_string] = {"_".join(split[2:]): value}
    #             else:
    #                 filtered_strings[filter_string].update({"_".join(split[2:]): value})

    # this uses the whole thing in the csv file. ex `PCY009_CrashCrewPremium`

    for filter_string in filter_strings:
        for game_string, value in game_strings.items():
            if filter_string in game_string:
                if filter_string not in filtered_strings:
                    filtered_strings[filter_string] = value
                else:
                    filtered_strings[filter_string] = value

    with open(parsed.out, 'w', encoding='utf8') as f:
        json.dump(filtered_strings, f, indent=1, ensure_ascii=False)


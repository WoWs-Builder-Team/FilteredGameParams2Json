import polib
import json
import argparse
import csv
import os
import logging
from os import path
from polib import MOFile
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_single_mo(lang_name: str, mo_file_path: str, output_path: str, filter_file: str, missing=False):
    logger.info(f"Processing language: {lang_name}")

    mo_strings: MOFile = polib.mofile(mo_file_path)
    game_strings = {mo_string.msgid: mo_string.msgstr for mo_string in mo_strings}
    with open(filter_file, 'r') as f:
        filter_strings = [i[0] for i in csv.reader(f)]

    filtered_strings = {}

    for filter_string in filter_strings:
        for game_string, value in game_strings.items():
            if filter_string.lower() in game_string.lower():
                if game_string.lower().startswith('ids_'):
                    filtered_strings[game_string[4:]] = value
                else:
                    filtered_strings[game_string] = value

    if missing:
        missing_file = os.path.join(output_path, f"missing_{lang_name}.txt")

        with open(missing_file, "w") as f:
            for i in set(filter_strings).difference(filtered_strings):
                f.write(f"{i}\n")

    output_file = os.path.join(output_path, f"{lang_name}.json")

    with open(output_file, 'w', encoding='utf8') as f:
        json.dump(filtered_strings, f, indent=1, ensure_ascii=False)

    logger.info(f"Processing language: {lang_name}, Done.")


def process_multiple_mo(dir_path: str, filter_path: str, missing=False, serial=True):
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    paths = []

    for d in os.listdir(dir_path):
        fp = os.path.join(dir_path, d)
        if path.isdir(fp):
            lang_name = os.path.basename(fp)
            mo_path = os.path.join(fp, 'LC_MESSAGES', 'global.mo')
            paths.append((lang_name, mo_path, output_dir, filter_path, missing))

    # process_single_mo(*paths[0])

    with ThreadPoolExecutor(max_workers=4) as tpe:
        list(tpe.map(process_single_mo, *zip(*paths)))

    if serial:
        for params in paths:
            process_single_mo(*params)
    else:
        with ThreadPoolExecutor() as tpe:
            list(tpe.map(process_single_mo, *zip(*paths)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--localizations", help="Localization folder path.", type=str, required=False)
    parser.add_argument("--filter", help="Filter. A csv file.", type=str, required=True)
    parser.add_argument("--missing", help="Not found indexes.", action="store_true", required=False)
    parser.add_argument("--serial", help="Run serially.", action="store_true", required=False)
    parsed = parser.parse_args()

    if not all([path.exists(i) and (path.isfile(i) or path.isdir(i)) for i in [parsed.filter, parsed.localizations]]):
        raise RuntimeError

    process_multiple_mo(parsed.localizations, parsed.filter, parsed.missing, parsed.serial)

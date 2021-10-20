import os
import struct
import zlib
import pickle
import json
import copy
import argparse
from filters import *
from concurrent.futures import ThreadPoolExecutor
from os import path

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

entities_dir = os.path.join(__location__, "entities")


class GPEncode(json.JSONEncoder):
    def default(self, o: object):
        try:
            for e in ['Cameras', 'DockCamera', 'damageDistribution']:
                o.__dict__.pop(e, o.__dict__)
            for k, v in o.__dict__.items():
                if k in ['A_Torpedoes', 'B_Torpedoes', 'C_Torpedoes', 'D_Torpedoes']:
                    try:
                        salvo_params = o.__dict__[k].__dict__["salvoParams"]
                        salvo_params = {str(k): v for k, v in salvo_params.items()}
                        o.__dict__[k].__dict__['salvoParams'] = salvo_params
                    except Exception:
                        pass
            return o.__dict__
        except AttributeError:
            return {}
        except TypeError:
            return {}
        except Exception:
            return {}


def write_entities(data):
    _key, _value, do_filter, is_pt = data

    if is_pt:
        _ent_dir = os.path.join(__location__, "pts", "entities", _key)
    else:
        _ent_dir = os.path.join(__location__, "live", "entities", _key)

    if not os.path.exists(_ent_dir):
        try:
            os.makedirs(_ent_dir)
        except OSError:
            print("Error at creating directories for the entities.")
            exit()

    data = {}
    data_filtered = {}

    for idx, item in enumerate(_value):
        try:
            group_by = item.typeinfo.nation if item.typeinfo.nation else "no_nation"
        except AttributeError:
            group_by = item.typeinfo.species if item.typeinfo.species else _key

        if group_by not in data:
            data[group_by] = [item]
        else:
            data[group_by].append(item)

        if not do_filter:
            continue

        filtered_item = get_filtered(copy.deepcopy(item))

        if filtered_item:
            if group_by not in data_filtered:
                data_filtered[group_by] = [filtered_item]
            else:
                data_filtered[group_by].append(filtered_item)

    for k, v in data.items():
        with open(os.path.join(_ent_dir, f"{k}.json"), "w") as ff:
            json.dump(v, ff, indent=1, cls=GPEncode, sort_keys=True)

    if do_filter:
        for k, v in data_filtered.items():
            if not any(v):
                continue

            with open(os.path.join(_ent_dir, f"filtered_{k}.json"), "w") as ff:
                json.dump(v, ff, indent=1, cls=GPEncode, sort_keys=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help="GameParams.data file path.", required=True)
    parser.add_argument("--filter", help="Filter the data. (WoWs ShipBuilder)", action="store_true", required=False)
    parser.add_argument("--pts", help="Extracts the entities and put it in a folder named `pts`.", action="store_true",
                        required=False)

    args = parser.parse_args()

    if not path.isfile(args.path):
        print("Invalid GameParams.data file path.")
        exit(-1)

    with open(args.path, "rb") as f:
        gp_data: bytes = f.read()
    gp_data: bytes = struct.pack('B' * len(gp_data), *gp_data[::-1])
    gp_data: bytes = zlib.decompress(gp_data)
    gp_data: tuple = pickle.loads(gp_data, encoding='windows-1251')

    entity_types = {}

    for index, value in gp_data[0].items():
        data_type = value.typeinfo.type

        try:
            entity_types[data_type].append(value)
        except KeyError:
            entity_types[data_type] = [value]

    with ThreadPoolExecutor() as tpe:
        list(tpe.map(write_entities, [(k, v, args.filter, args.pts) for k, v in entity_types.items()]))

    print("Done.")

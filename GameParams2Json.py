import os
import struct
import zlib
import pickle
import json
import copy
from filters import *
from concurrent.futures import ThreadPoolExecutor

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
    _key, _value = data

    _ent_dir = os.path.join(entities_dir, _key)

    if not os.path.exists(_ent_dir):
        try:
            os.makedirs(_ent_dir)
        except OSError:
            pass

    data = {}
    data_filtered = {}

    for idx, item in enumerate(_value):
        try:
            group_by = item.typeinfo.nation if item.typeinfo.nation else "no_nation"
        except AttributeError:
            group_by = item.typeinfo.species if item.typeinfo.species else _key

        filtered_item = get_filtered(copy.copy(item))

        if group_by not in data:
            data[group_by] = [item]
        else:
            data[group_by].append(item)

        if group_by not in data_filtered:
            data_filtered[group_by] = [filtered_item]
        else:
            data_filtered[group_by].append(filtered_item)

    for k, v in data.items():
        with open(os.path.join(_ent_dir, f"{k}.json"), "w") as ff:
            json.dump(v, ff, indent=1, cls=GPEncode, sort_keys=True)

    for k, v in data_filtered.items():
        if not any(v):
            continue

        with open(os.path.join(_ent_dir, f"filtered_{k}.json"), "w") as ff:
            json.dump(v, ff, indent=1, cls=GPEncode, sort_keys=True)


if __name__ == '__main__':
    gp_file_path = os.path.join(__location__, 'GameParams.data')
    with open(gp_file_path, "rb") as f:
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
        list(tpe.map(write_entities, [(k, v) for k, v in entity_types.items()]))

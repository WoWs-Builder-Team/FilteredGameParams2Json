MODERNIZATION_KEYS = ["modifiers", "nation", "shiplevel", "ships", "shiptype", "slot", "excludes"]
COMMON_KEYS = ['id', 'typeinfo', 'name', 'index']


class Modernization:
    def __init__(self, data: object):
        self._data = data

    def get_filtered(self):
        self._delete_attributes(self._data, COMMON_KEYS + MODERNIZATION_KEYS)
        return self._data

    @staticmethod
    def _delete_attributes(obj: object, keys_to_keep: list):
        for _k in list(obj.__dict__.keys()):
            if _k not in keys_to_keep:
                obj.__delattr__(_k)

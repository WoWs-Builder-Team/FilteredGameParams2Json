KEYS = ["personName", "Skills", "UniqueSkills"]
COMMON_KEYS = ['id', 'typeinfo', 'name', 'index']


class Crew:
    def __init__(self, data: object):
        self._data = data

    def _get_type(self) -> str:
        return self._data.__getattribute__("typeinfo").__getattribute__("type")

    def _get_species(self) -> str:
        return self._data.__getattribute__("typeinfo").__getattribute__("species")

    def get_filtered(self):
        self._delete_attributes(self._data, COMMON_KEYS + KEYS)
        return self._data

    @staticmethod
    def _delete_attributes(obj: object, keys_to_keep: list):
        for _k in list(obj.__dict__.keys()):
            if _k not in keys_to_keep:
                obj.__delattr__(_k)

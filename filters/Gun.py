TORPEDO_KEYS = ["ammoList", "barrelDiameter", "numBarrels", "rotationSpeed", "shotDelay", "torpedoAngles"]
DCHARGE_KEYS = ["ammoList", "horizSector", "numBombs", "rotationSpeed"]
SECONDARY_KEYS = ["ammoList", "antiAirAuraDistance", "antiAirAuraStrength", "barrelDiameter", "delim", "idealDistance",
                  "idealRadius", "minRadius", "radiusOnDelim", "radiusOnMax", "radiusOnZero", "rotationSpeed",
                  "shotDelay", "smokePenalty", "vertSector"]
AAIRCRAFT_KEYS = ["antiAirAuraDistance", "antiAirAuraStrength", "numBarrels", "shotDelay"]
MAIN_KEYS = ['deadZone']
COMMON_KEYS = ['id', 'typeinfo', 'name', 'index']


class Gun:
    def __init__(self, data: object):
        self._data = data

    def _get_species(self) -> str:
        return self._data.__getattribute__("typeinfo").__getattribute__("species")

    def get_filtered(self):
        # Main, DCharge, AAircraft, Torpedo, Secondary
        species = self._get_species()
        if species == "DCharge":
            self._delete_attributes(self._data, COMMON_KEYS + DCHARGE_KEYS)
        elif species == "AAircraft":
            self._delete_attributes(self._data, COMMON_KEYS + AAIRCRAFT_KEYS)
        elif species == "Torpedo":
            self._delete_attributes(self._data, COMMON_KEYS + TORPEDO_KEYS)
        elif species == "Secondary":
            self._delete_attributes(self._data, COMMON_KEYS + SECONDARY_KEYS)
        else:
            self._delete_attributes(self._data, COMMON_KEYS + MAIN_KEYS)
        return self._data

    @staticmethod
    def _delete_attributes(obj: object, keys_to_keep: list):
        for _k in list(obj.__dict__.keys()):
            if _k not in keys_to_keep:
                obj.__delattr__(_k)

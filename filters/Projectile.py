ARTILLERY_KEYS = ["affectedByPTZ", "alphaDamage", "alphaPiercingCS", "alphaPiercingHE", "ammoType", "applyPTZCoeff",
                  "bulletAirDrag", "bulletAlwayRiccochetAt", "bulletDetonator", "bulletDetonatorThreshold",
                  "bulletDiametr", "bulletKrupp", "bulletMass", "bulletRicochetAt", "bulletSpeed", "burnProb",
                  "distTile", "ignoreClasses", "isBomb"]
TORPEDO_KEYS = ["alertDist", "alphaDamage", "ammoType", "bulletDiametr", "maxDist", "ignoreClasses",
                "speed", "armingTime", "uwCritical", "visibilityFactor", "damage"]
DEPTHCHARGE_KEYS = ["alertDist", "alphaDamage", "ammoType", "burnProb", "uwCritical", "timer", "splashCubeSize",
                    "speed"]
COMMON_KEYS = ['id', 'typeinfo', 'name', 'index']


class Projectile:
    def __init__(self, data: object):
        self._data = data

    def _get_type(self) -> str:
        return self._data.__getattribute__("typeinfo").__getattribute__("type")

    def _get_species(self) -> str:
        return self._data.__getattribute__("typeinfo").__getattribute__("species")

    def get_filtered(self):
        # Artillery, Bomb, Rocket
        # Torpedo, DepthCharge
        species = self._get_species()
        if species in ["Artillery", "Bomb", "Rocket", "SkipBomb"]:
            self._delete_attributes(self._data, COMMON_KEYS + ARTILLERY_KEYS)
        elif species == "Torpedo":
            self._delete_attributes(self._data, COMMON_KEYS + TORPEDO_KEYS)
        elif species == "DepthCharge":
            self._delete_attributes(self._data, COMMON_KEYS + DEPTHCHARGE_KEYS)
        else:
            self._delete_attributes(self._data, COMMON_KEYS)

        return self._data

    @staticmethod
    def _delete_attributes(obj: object, keys_to_keep: list):
        for _k in list(obj.__dict__.keys()):
            if _k not in keys_to_keep:
                obj.__delattr__(_k)

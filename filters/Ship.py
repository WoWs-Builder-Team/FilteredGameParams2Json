import pickle

ARTILLERY_KEYS = ["maxDist", "normalDistribution", "sigmaCount", "AuraFar", "AuraFar_Bubbles"]
ARTILLERY_GUN_KEYS = ["ammoList", "barrelDiameter", "horizSector", "id", "index", "numBarrels", "position",
                      "rotationSpeed", "shotDelay", "smokePenalty", "typeinfo"]
AIRDEFENCE_KEYS = []
AIRDEFENCE_SUBKEYS = ["areaDamage", "areaDamagePeriod", "bubbleDamage", "hitChance", "innerBubbleCount", "maxDistance",
                      "minDistance", "type"]
AIRARMAMENT_KEYS = ["deckPlaceCount", "planesReserveCapacity"]
ATBA_KEYS = ["AuraFar", "AuraFar_Bubbles", "AuraMedium", "AuraMedium_Bubbles", "maxDist", "sigmaCount"]
ATBA_SUBKEYS = ["maxDist", "sigmaCount", "ammoList", "id", "index", "name", "numBarrels", "rotationSpeed", "shotDelay",
                "smallGun", "typeinfo"]
AA_KEYS = ["AuraFar", "AuraFar_Bubbles", "AuraMedium", "AuraMedium_Bubbles", "AuraNear", "AuraNear_Bubbles"]
DEPTHCHARGE_KEYS = ["reloadTime", "maxPacks"]
DEPTHCHARGE_SUBKEYS = ["ammoList", "horizSector", "id", "index", "name", "numBombs", "rotationSpeed", "typeinfo"]
TORPEDO_KEYS = []
TORPEDO_SUBKEYS = ["ammoList", "barrelDiameter", "id", "index", "name", "numBarrels", "rotationSpeed", "shotDelay",
                   "torpedoAngles", "typeinfo"]
HULL_SUBKEYS = ["health", "maxSpeed", "rudderTime", "speedCoef", "visibilityCoefGKInSmoke", "visibilityFactor",
                "visibilityFactorByPlane"]
ENGINE_KEYS = ["forwardEngineUpTime", "backwardEngineUpTime", "speedCoef"]
PINGERGUN_KEYS = ["rotationSpeed", "sectorParams", "waveDistance", "waveHitAlertTime", "waveHitLifeTime", "waveParams",
                  "waveReloadTime"]
ROOT_KEYS = ["id", "index", "level", "name", "typeinfo", "ShipUpgradeInfo", "ShipAbilities"]


class Ship:
    def __init__(self, data):
        self._data: object = data

    def _get_components(self, filters: tuple) -> list[str]:
        uc_type, component = filters
        try:
            keys = []
            for k, v in self._data.__dict__["ShipUpgradeInfo"].__dict__.items():
                try:
                    if v.ucType == uc_type:
                        keys.extend(v.components[component])
                except AttributeError:
                    pass
            return keys
        except KeyError:
            return []

    def _apply_gun_filters(self, uc_component: tuple, parent, children, delete_guns=False):
        try:
            keys = self._get_components(uc_component)
            for key in keys:
                gp_object: object = self._data.__getattribute__(key)

                gun_keys = []

                for k, v in gp_object.__dict__.items():
                    try:
                        if v.typeinfo.type == "Gun":
                            gun_keys.append(k)
                            self._delete_attributes(v, children)
                    except AttributeError:
                        pass

                for _k in AA_KEYS:
                    try:
                        if obj := gp_object.__getattribute__(_k):
                            self._delete_attributes(obj, AIRDEFENCE_SUBKEYS)
                    except AttributeError:
                        pass

                gun_keys = gun_keys if not delete_guns else []
                self._delete_attributes(gp_object, parent + gun_keys + AA_KEYS)
        except KeyError:
            pass

    def _filter_common(self, uc_component: tuple, children):
        try:
            keys = self._get_components(uc_component)
            for key in keys:
                gp_object: object = self._data.__getattribute__(key)
                self._delete_attributes(gp_object, children)
        except KeyError:
            pass

    def _filter_upgrade_info(self):
        u_info: object = self._data.__getattribute__("ShipUpgradeInfo")
        try:
            u_info.__delattr__("lockedConfig")
        except AttributeError:
            pass

    def _apply_root_filter(self):
        # COMMON
        fire_control_keys = self._get_components(("_Suo", "fireControl"))
        artillery_keys = self._get_components(("_Artillery", "artillery"))
        atba_keys = self._get_components(("_Hull", "atba"))
        depthcharge_keys = self._get_components(("_Hull", "depthCharges"))
        torpedo_keys = self._get_components(("_Hull", "torpedoes"))
        airdefence_keys = self._get_components(("_Hull", "airDefense"))
        hull_keys = self._get_components(("_Hull", "hull"))
        engine_keys = self._get_components(("_Engine", "engine"))
        # CV RELATED
        tbomber_keys = self._get_components(("_TorpedoBomber", "torpedoBomber"))
        dbomber_keys = self._get_components(("_DiveBomber", "diveBomber"))
        fighter_keys = self._get_components(("_Fighter", "fighter"))
        sbomber_keys = self._get_components(("_SkipBomber", "skipBomber"))
        fcontrol_keys = self._get_components(("_FlightControl", "flightControl"))
        airarmament_keys = self._get_components(("_Hull", "airArmament"))
        # SUB RELATED
        pingergun_keys = self._get_components(("_Hull", "pinger"))

        all_components = fire_control_keys + artillery_keys + atba_keys + depthcharge_keys + torpedo_keys
        all_components = all_components + airdefence_keys + hull_keys + engine_keys
        all_components = all_components + tbomber_keys + dbomber_keys + fighter_keys + sbomber_keys + fcontrol_keys
        all_components = all_components + airarmament_keys + pingergun_keys

        modules_armaments = {comp: self._data.__getattribute__(comp) for comp in all_components}

        self._data.__setattr__("ModulesArmaments", modules_armaments)

        all_root_keys = ROOT_KEYS + ["ModulesArmaments"]
        self._delete_attributes(self._data, all_root_keys)

    @staticmethod
    def _delete_attributes(obj: object, keys_to_keep: list):
        for _k in list(obj.__dict__.keys()):
            if _k not in keys_to_keep:
                obj.__delattr__(_k)

    def get_filtered(self):
        self._apply_gun_filters(("_Artillery", "artillery"), ARTILLERY_KEYS, ARTILLERY_GUN_KEYS)
        self._apply_gun_filters(("_Hull", "atba"), ATBA_KEYS, ATBA_SUBKEYS)
        self._apply_gun_filters(("_Hull", "depthCharges"), DEPTHCHARGE_KEYS, DEPTHCHARGE_SUBKEYS)
        self._apply_gun_filters(("_Hull", "torpedoes"), TORPEDO_KEYS, TORPEDO_SUBKEYS)
        self._apply_gun_filters(("_Hull", "airDefense"), AIRDEFENCE_KEYS, AIRDEFENCE_SUBKEYS, delete_guns=True)
        self._filter_common(("_Hull", "hull"), HULL_SUBKEYS)
        self._filter_common(("_Engine", "engine"), ENGINE_KEYS)
        self._filter_common(("_Hull", "airArmament"), AIRARMAMENT_KEYS)
        self._filter_common(("_Hull", "pinger"), PINGERGUN_KEYS)
        self._filter_upgrade_info()
        self._apply_root_filter()
        return self._data


# if __name__ == '__main__':
#     with open("sample/PASB509_Missouri.dat", "rb") as f:
#         sample_data = pickle.load(f)
#
#     s = Ship(sample_data)
#     s.get_filtered_ship()

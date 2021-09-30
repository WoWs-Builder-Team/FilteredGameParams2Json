ARTILLERY_KEYS = ["maxDist", "normalDistribution", "sigmaCount", "AuraFar", "AuraFar_Bubbles", "taperDistance",
                  "taperDist"]
ARTILLERY_GUN_KEYS = ["ammoList", "barrelDiameter", "horizSector", "id", "index", "numBarrels", "position",
                      "rotationSpeed", "shotDelay", "smokePenalty", "typeinfo", "name", "idealRadius", "minRadius",
                      "idealDistance", "radiusOnZero", "delim", "radiusOnMax", "radiusOnDelim"]
AIRDEFENCE_KEYS = []
AIRDEFENCE_SUBKEYS = ["areaDamage", "areaDamagePeriod", "bubbleDamage", "hitChance", "innerBubbleCount", "maxDistance",
                      "minDistance", "type"]
AIRARMAMENT_KEYS = ["deckPlaceCount", "planesReserveCapacity"]
AIRSUPPORT_KEYS = ["chargesNum", "flyAwayTime", "maxDist", "maxPlaneFlightDist", "minDist", "planeName", "reloadTime",
                   "timeBetweenShots", "timeFromHeaven"]
ATBA_KEYS = ["AuraFar", "AuraFar_Bubbles", "AuraMedium", "AuraMedium_Bubbles", "maxDist", "sigmaCount"]
ATBA_SUBKEYS = ["maxDist", "sigmaCount", "ammoList", "id", "index", "name", "numBarrels", "rotationSpeed", "shotDelay",
                "smallGun", "typeinfo", "barrelDiameter"]
AA_KEYS = ["AuraFar", "AuraFar_Bubbles", "AuraMedium", "AuraMedium_Bubbles", "AuraNear", "AuraNear_Bubbles"]
DEPTHCHARGE_KEYS = ["reloadTime", "maxPacks"]
DEPTHCHARGE_SUBKEYS = ["ammoList", "horizSector", "id", "index", "name", "numBombs", "rotationSpeed", "typeinfo"]
TORPEDO_KEYS = []
TORPEDO_SUBKEYS = ["ammoList", "barrelDiameter", "id", "index", "name", "numBarrels", "rotationSpeed", "shotDelay",
                   "torpedoAngles", "typeinfo", "deadZone", "horizSector", "canRotate", "useGroups", "useOneShot",
                   "groups", "torpAngles"]
HULL_SUBKEYS = ["health", "maxSpeed", "rudderTime", "speedCoef", "visibilityCoefGKInSmoke", "visibilityFactor",
                "visibilityFactorByPlane"]
ENGINE_KEYS = ["forwardEngineUpTime", "backwardEngineUpTime", "speedCoef"]
PINGERGUN_KEYS = ["rotationSpeed", "sectorParams", "waveDistance", "waveHitAlertTime", "waveHitLifeTime", "waveParams",
                  "waveReloadTime"]
FLIGHTCONTROL_KEYS = ["squadrons"]
ROOT_KEYS = ["id", "index", "level", "name", "typeinfo", "ShipUpgradeInfo", "ShipAbilities", "group"]


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

                # species: Main, Torpedo, Secondary, DCharge
                # Main: guns
                # Torpedo: torpedoArray
                # Secondary: antiAirAndSecondaries
                # DCharge: depthCharges

                main, torpedo, secondary, dcharge = {}, {}, {}, {}
                species_map = {"Main": ("guns", main), "Torpedo": ("torpedoArray", torpedo),
                               "Secondary": ("antiAirAndSecondaries", secondary), "DCharge": ("depthCharges", dcharge)}

                for k, v in gp_object.__dict__.items():
                    try:
                        if v.typeinfo.type == "Gun":
                            self._delete_attributes(v, children)
                            try:
                                species_map[v.typeinfo.species][1].update({k: gp_object.__getattribute__(k)})
                            except KeyError:
                                pass
                    except AttributeError:
                        pass

                for k, v in species_map.items():
                    if v[1]:
                        gp_object.__setattr__(*v)

                aa_subkeys = []

                for subkey, subvalue in gp_object.__dict__.items():
                    subkey_lower = subkey.lower()
                    for search_str in ["far", "medium", "med", "near"]:
                        if search_str in subkey_lower:
                            aa_subkeys.append(subkey)
                            self._delete_attributes(subvalue, AIRDEFENCE_SUBKEYS)

                self._delete_attributes(gp_object, parent + AA_KEYS + aa_subkeys + [v[0] for v in species_map.values()])
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

    def _add_new_key(self, uc_component: tuple, data: dict):
        for key in self._get_components(uc_component):
            try:
                obj: object = self._data.__getattribute__(key)
                for k, v in data.items():
                    obj.__setattr__(k, v)
            except Exception as e:
                print(e)

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
        # airarmament_keys = self._get_components(("_Hull", "airArmament"))
        # SUB RELATED
        pingergun_keys = self._get_components(("_Hull", "pinger"))
        # NL RELATED
        airsupport_keys = self._get_components(("_Hull", "airSupport"))

        all_components = fire_control_keys + artillery_keys + atba_keys + depthcharge_keys + torpedo_keys
        all_components = all_components + airdefence_keys + hull_keys + engine_keys
        all_components = all_components + tbomber_keys + dbomber_keys + fighter_keys + sbomber_keys + fcontrol_keys
        all_components = all_components + pingergun_keys + airsupport_keys

        modules_armaments = {comp: self._data.__getattribute__(comp) for comp in all_components}

        self._data.__setattr__("ModulesArmaments", modules_armaments)

        all_root_keys = ROOT_KEYS + ["ModulesArmaments"]
        self._add_new_key(("_Hull", "airDefense"), {"isAA": True})
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
        self._filter_common(("_Hull", "airSupport"), AIRSUPPORT_KEYS)
        self._filter_common(("_Hull", "hull"), HULL_SUBKEYS)
        self._filter_common(("_Engine", "engine"), ENGINE_KEYS)
        self._filter_common(("_Hull", "airArmament"), AIRARMAMENT_KEYS)
        self._filter_common(("_Hull", "pinger"), PINGERGUN_KEYS)
        self._filter_common(("_FlightControl", "flightControl"), FLIGHTCONTROL_KEYS)
        self._filter_upgrade_info()
        self._apply_root_filter()
        return self._data

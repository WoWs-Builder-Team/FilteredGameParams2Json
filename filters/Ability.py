# {'onWaterEffect', 'radarEffectForPlayer', 'weaponTypes', 'absoluteBuff', 'livePointEffect', 'radarEffect',
#  'acousticWaveSpeed', 'spawnPointEffect', 'zoneLifetime', 'fightersName', 'titleIDs', 'timeToTryingCatch',
#  'activationDelay', 'regenerationHPSpeedUnits', 'climbAngle', 'source', 'zoneRadius', 'ammo', 'affectedClasses',
#  'dogFightTime', 'targetEffect', 'flyAwayTime', 'buoyancyState', 'waveParams', 'target', 'consumableType',
#  'distanceToKill', 'waveEffect', 'bubbleDamageMultiplier', 'waterEffect', 'enemyAuraBuff', 'conditionalBuff',
#  'spawnBackwardShift', 'SpecialSoundID', 'startDelayTime', 'logic', 'selfAuraBuff', 'timeFromHeaven',
#  'torpedoReloadTime', 'targetBuff', 'canUseOnEmpty', 'startDistance', 'waveDistance', 'effectOnEndLongivity', 'height',
#  'spawnEffect', 'acousticWaveLifetime', 'allyAuraBuff', 'reloadBoostCoeff', 'condition'}

CONSUMABLE_KEYS = ["artilleryDistCoeff", "regenerationHPSpeed", "regenerationRate", "visionDistance", "updateFrequency",
                   "areaDamageMultiplier", "bubbleDamageMultiplier" "dogFightTime", "fightersNum", "radius",
                   "timeDelayAttack", "timeWaitDelayAttack", "distShip", "backwardEngineForsag", "forwardEngineForsag",
                   "forwardEngineForsagMaxSpeed", "backwardEngineForsagMaxSpeed", "lifeTime", "radius", "speedLimit",
                   "workTime", "distTorpedo", "boostCoeff", "buoyancyRudderResetTimeCoeff", "buoyancyRudderTimeCoeff",
                   "maxBuoyancySpeedCoeff", "underwaterMaxRudderAngleCoeff", "numConsumables", "reloadTime", "workTime",
                   "iconIDs", "descIDs", "group"]
COMMON_KEYS = ['id', 'typeinfo', 'name', 'index']


class Ability:
    def __init__(self, data: object):
        self._data = data

    def _get_consumables(self):
        consumable_keys = []
        for k, v in self._data.__dict__.items():
            v: object
            try:
                v.__getattribute__("consumableType")
                consumable_keys.append(k)
            except AttributeError:
                pass
        return consumable_keys

    def _filter_consumables(self, keys: list):
        for key in keys:
            consumable_obj: object = self._data.__getattribute__(key)
            self._delete_attributes(consumable_obj, CONSUMABLE_KEYS)

    def get_filtered(self):
        consumable_keys = self._get_consumables()
        self._filter_consumables(consumable_keys)
        variants = {comp: self._data.__getattribute__(comp) for comp in consumable_keys}
        self._data.__setattr__("variants", variants)
        self._delete_attributes(self._data, COMMON_KEYS + ["variants"])
        return self._data

    @staticmethod
    def _delete_attributes(obj: object, keys_to_keep: list):
        obj_keys = set(obj.__dict__.keys())
        keep_keys = set(keys_to_keep)

        for _k in obj_keys.difference(keep_keys):
            obj.__delattr__(_k)

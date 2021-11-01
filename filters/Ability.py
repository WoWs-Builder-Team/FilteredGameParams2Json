CONSUMABLE_KEYS = ["artilleryDistCoeff", "regenerationHPSpeed", "regenerationRate", "visionDistance", "updateFrequency", "areaDamageMultiplier", "bubbleDamageMultiplier" "dogFightTime", "fightersNum", "radius", "timeDelayAttack", "timeWaitDelayAttack", "distShip", "backwardEngineForsag", "forwardEngineForsag", "forwardEngineForsagMaxSpeed" "backwardEngineForsagMaxSpeed", "lifeTime", "radius", "speedLimit", "workTime", "distTorpedo", "boostCoeff", "buoyancyRudderResetTimeCoeff", "buoyancyRudderTimeCoeff", "maxBuoyancySpeedCoeff", "underwaterMaxRudderAngleCoeff",  "numConsumables", "reloadTime", "workTime", "iconIDs", "descIDs", "group"]
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
        variants = {comp: self._data.__getattribute__(comp) for comp in consumable_keys}
        self._data.__setattr__("variants", variants)
        self._filter_consumables(consumable_keys)
        self._delete_attributes(self._data, COMMON_KEYS + ["variants"])
        return self._data

    @staticmethod
    def _delete_attributes(obj: object, keys_to_keep: list):
        for _k in list(obj.__dict__.keys()):
            if _k not in keys_to_keep:
                obj.__delattr__(_k)

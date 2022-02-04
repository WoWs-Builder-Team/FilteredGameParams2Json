import logging

AIRCRAFT_KEYS = ["hangarSettings", "maxHealth", "naturalAcceleration", "naturalDeceleration", "numPlanesInSquadron",
                 "returnHeight", "speedMax", "speedMin", "bombName", "attackCooldown", "attackInterval",
                 "attackerDamageTakenMultiplier", "attackSpeedMultiplier", "attackSpeedMultiplierApplyTime",
                 "attackerSize", "bombFallingTime", "flightHeight", "flightRadius", "projectilesPerAttack",
                 "innerBombsPercentage", "innerSalvoSize", "isAirSupportPlane", "isConsumablePlane",
                 "isJatoBoosterDetachable", "jatoDuration", "jatoSpeedMultiplier", "speedMoveWithBomb", "PlaneAbilities",
                 "aimingAccuracyDecreaseRate", "aimingAccuracyIncreaseRate", "aimingTime", "postAttackInvulnerabilityDuration", 
                 "preparationAccuracyDecreaseRate", "preparationAccuracyIncreaseRate", "preparationTime", "planeSubtype"]
COMMON_KEYS = ['id', 'typeinfo', 'name', 'index']


class Aircraft:
    logger = logging.getLogger(__name__)

    def __init__(self, data: object):
        self._data = data

    def get_filtered(self):
        self._delete_attributes(self._data, COMMON_KEYS + AIRCRAFT_KEYS)
        return self._data

    @staticmethod
    def _delete_attributes(obj: object, keys_to_keep: list):
        for _k in list(obj.__dict__.keys()):
            if _k not in keys_to_keep:
                obj.__delattr__(_k)

        if isinstance(obj.__getattribute__("planeSubtype"), int):
            Aircraft.logger.warning("Replacing planeSubtype for plane " + obj.__getattribute__("index") + " due to it having the wrong type.")
            if obj.__getattribute__("planeSubtype") == 1:
                obj.__setattr__("planeSubtype", ["consumable"])
            else:
                obj.__setattr__("planeSubtype", [])

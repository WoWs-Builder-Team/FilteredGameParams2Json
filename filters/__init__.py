from .Ship import Ship
from .Gun import Gun
from .Projectile import Projectile
from .Crew import Crew
from .Ability import Ability
from .Aircraft import Aircraft
from .Exterior import Exterior
from .Modernization import Modernization
from .Unit import Unit

FILTER_MAP = {obj_filter.__name__: obj_filter for obj_filter in [Ship, Gun, Projectile, Crew, Ability, Aircraft,
                                                                 Exterior, Modernization, Unit]}


def get_filtered(obj: object):
    object_type = obj.__getattribute__("typeinfo").__getattribute__("type")

    try:
        return FILTER_MAP[object_type](obj).get_filtered()
    except KeyError:
        return None

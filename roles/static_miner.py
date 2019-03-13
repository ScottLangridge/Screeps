from consts import STATIC_MINER_SPOTS
from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run(me):
    if me.memory.station is undefined:
        me.memory['station'] = get_station(me)
        station = me.room.getPositionAt(me.memory.station[0], me.memory.station[1])
        me.memory.target = station.findClosestByRange(FIND_SOURCES).id
    else:
        station = me.room.getPositionAt(me.memory.station[0], me.memory.station[1])
        code = me.harvest(Game.getObjectById(me.memory.target))
        if code == ERR_NOT_IN_RANGE:
            me.moveTo(station)


def get_station(me):
    stations = STATIC_MINER_SPOTS[:]

    harvesters = []
    for creep_name in Object.keys(Game.creeps):
        creep = Game.creeps[creep_name]
        if creep.memory.role == 'static_miner' and creep.name != me.name:
            harvesters.append(creep)

    for harvester in harvesters:
        for station in stations:
            if str(harvester.memory.station) == str(station):
                stations.remove(station)

    return stations[0]

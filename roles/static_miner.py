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
    if me.memory.station is None:
        me.memory.station = get_station(me)
        me.memory.target = me.memory.station.findClosestByRange(FIND_SOURCES)
    else:
        if me.harvest(me.memory.target) == ERR_NOT_IN_RANGE:
            me.moveTo(me.memory.target)


def get_station(me):
    stations = STATIC_MINER_SPOTS[:]
    for i in range(len(stations)):
        stations[i] = me.room.getPositionAt(stations[i][0], stations[i][1])

    harvesters = []
    for creep_name in Object.keys(Game.creeps):
        creep = Game.creeps[creep_name]
        if creep.memory.role == 'static_harvester':
            harvesters.append(creep)

    for harvester in harvesters:
        stations.remove(harvester.memory.station)

    return stations[0]

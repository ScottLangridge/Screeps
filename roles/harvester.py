from defs import *
from consts import HARVESTER_CONTAINER_FILL_ORDER

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run(me):
    decide_task(me)

    if me.memory.depositing:
        deposit(me)
    else:
        collect(me)


def decide_task(me):
    if me.carry.energy == 0:
        if me.memory.depositing:
            me.say('Mining')
        me.memory.depositing = False
    elif me.carry.energy == me.carryCapacity:
        if not me.memory.depositing:
            me.say('Dropping')
        me.memory.depositing = True


def deposit(me):
    target = get_target(me)
    code = me.transfer(target, RESOURCE_ENERGY)
    if code == OK:
        me.memory.target = False
    elif code == ERR_NOT_IN_RANGE:
        me.moveTo(target)


def collect(me):
    target = me.pos.findClosestByPath(FIND_SOURCES_ACTIVE)
    code = me.harvest(target)
    if code == OK:
        pass
    elif code == ERR_NOT_IN_RANGE:
        me.moveTo(target)


def get_target(me):
    spawn = Game.spawns['Spawn1']
    filter_non_full_extensions = {'filter': lambda s: s.structureType == STRUCTURE_EXTENSION
                                                      and s.energy < s.energyCapacity}
    extension = me.pos.findClosestByPath(FIND_STRUCTURES, filter_non_full_extensions)

    # Containers (in order of importance)
    for container in HARVESTER_CONTAINER_FILL_ORDER:
        cont = Game.getObjectById(container)
        if cont.store[RESOURCE_ENERGY] < cont.storeCapacity:
            return cont

    # Spawn
    if spawn.energy < spawn.energyCapacity:
        return spawn

    # Extensions
    if extension is not None:
        return extension

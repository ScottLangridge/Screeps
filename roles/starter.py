from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

BODY_0 = [MOVE, WORK, WORK, CARRY]
BODY_1 = [MOVE, WORK, WORK, WORK, CARRY, CARRY]


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

    # If construction
    # TODO This is a little dodgy. Maybe find a better way of differentiating type of structure.
    if str(target)[1:18] == 'construction site':
        code = me.build(target)
        if code == OK:
            me.memory.target = False
        elif code == ERR_NOT_IN_RANGE:
            me.moveTo(target)

    # If spawn or Extension
    elif target.structureType == STRUCTURE_SPAWN or target.structureType == STRUCTURE_EXTENSION:
        code = me.transfer(target, RESOURCE_ENERGY)
        if code == OK:
            me.memory.target = False
        elif code == ERR_NOT_IN_RANGE:
            me.moveTo(target)

    # If controller
    elif target.structureType == STRUCTURE_CONTROLLER:
        code = me.upgradeController(target)
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
    controller = me.room.controller
    filter_non_full_extensions = {'filter': lambda s: s.structureType == STRUCTURE_EXTENSION
                                                      and s.energy < s.energyCapacity}
    extension = me.pos.findClosestByPath(FIND_STRUCTURES, filter_non_full_extensions)

    if spawn.energy < spawn.energyCapacity:
        return spawn
    elif extension is not None:
        return extension
    elif len(Game.constructionSites) > 0:
        return me.pos.findClosestByPath(FIND_CONSTRUCTION_SITES)
    else:
        return controller

from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


BODY_0 = [MOVE, WORK, CARRY]
BODY_1 = [MOVE, WORK, WORK, CARRY]


def run(me):
    # Switch task if necessary:
    if me.carry.energy == 0:
        if me.memory.depositing:
            me.say('Mining')
        me.memory.depositing = False
    elif me.carry.energy == me.carryCapacity:
        if not me.memory.depositing:
            me.say('Dropping')
        me.memory.depositing = True

    # If depositing
    if me.memory.depositing:
        target = get_target(me)
        code = me.transfer(target, RESOURCE_ENERGY)
        if code == OK:
            me.memory.target = False
        if me.transfer(target, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE:
            me.moveTo(target)

    # If collecting
    else:
        target = me.pos.findClosestByPath(FIND_SOURCES_ACTIVE)
        code = me.harvest(target)
        if code == OK:
            pass
        elif code == ERR_NOT_IN_RANGE:
            me.moveTo(target)


def get_target(me):
    drop_points = []
    drop_points.extend(me.room.find(FIND_STRUCTURES,
                                    {'filter': lambda s: s.structureType == STRUCTURE_EXTENSION}))

    # For each structure
    for pointName in Object.keys(Game.structures):
        point = Game.structures[pointName]
        point_targeted = False

        # If it is an extension with empty space
        if (point.structureType == STRUCTURE_EXTENSION
                and point.energy < point.energyCapacity):

            # If no creep targets it
            for creepName in Object.keys(Game.creeps):
                creep = Game.creeps[creepName]

                if creep.memory.target == point:
                    point_targeted = True

            # Target it
            if not point_targeted:
                me.memory.target = point
                return point

    # Else take energy to spawn
    if Game.spawns['Spawn1'].energy < Game.spawns['Spawn1'].energyCapacity:
        me.memory.target = Game.spawns['Spawn1']
        return Game.spawns['Spawn1']

    # If spawn is full, queue at an extension
    for pointName in Object.keys(Game.structures):
        point = Game.structures[pointName]
        point_targeted = False

        # If it is an extension with empty space
        if point.structureType == STRUCTURE_EXTENSION:

            # If no creep targets it
            for creepName in Object.keys(Game.creeps):
                creep = Game.creeps[creepName]

                if creep.memory.target == point:
                    point_targeted = True

            # Target it
            if not point_targeted:
                me.memory.target = point
                return point

    # If there is no suitable extension to queue at, queue at spawn.
    me.memory.target = Game.spawns['Spawn1']
    return Game.spawns['Spawn1']
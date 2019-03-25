from consts import TARGET_WALL_HEALTH, BUILDERS_REPAIR_DEFENCES
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
    decide_task(me)

    if me.memory.task == 'building':
        build(me)
    elif me.memory.task == 'repairing':
        repair(me)
    else:
        collect(me)


def decide_task(me):
    if me.carry.energy == 0:
        if me.memory.task != 'collect':
            me.say('Collecting')
            me.memory.task = 'collect'
    elif me.carry.energy == me.carryCapacity and me.memory.task == 'collect':
            me.say('Working')
            if me.pos.findClosestByRange(FIND_CONSTRUCTION_SITES) is not None:
                me.memory.task = 'building'
            else:
                me.memory.task = 'repairing'
    else:
        if me.pos.findClosestByRange(FIND_CONSTRUCTION_SITES) is not None:
            me.memory.task = 'building'
        else:
            me.memory.task = 'repairing'


def build(me):
    target = me.pos.findClosestByRange(FIND_CONSTRUCTION_SITES)

    code = me.build(target)
    if code == OK:
        return
    elif code == ERR_NOT_IN_RANGE:
        me.moveTo(target)


def repair(me):
    filter_damaged = {'filter': lambda s: s.hits < s.hitsMax and s.structureType != STRUCTURE_WALL
                                          and s.structureType != STRUCTURE_RAMPART}
    target = me.pos.findClosestByRange(FIND_STRUCTURES, filter_damaged)

    code = me.repair(target)
    if code == OK:
        return
    elif code == ERR_NOT_IN_RANGE:
        me.moveTo(target)

    # Repair defences
    if BUILDERS_REPAIR_DEFENCES:
        filter_defences = {'filter': lambda s: s.structureType == STRUCTURE_WALL or s.structureType == STRUCTURE_RAMPART
                           and s.hits < s.hitsMax}
        target = None
        for defence in me.room.find(FIND_STRUCTURES, filter_defences):
            if target is None or defence.hits < target.hits:
                target = defence
        if target is not None and target.hits < TARGET_WALL_HEALTH:
            code = me.repair(target)
            if code == OK:
                return
            elif code == ERR_NOT_IN_RANGE:
                me.moveTo(target)
            return


def collect(me):
    if Memory.energy_save:
        return

    # Take from containers or store
    filter_containers = {'filter': lambda s: (s.structureType == STRUCTURE_CONTAINER
                         or s.structureType == STRUCTURE_STORAGE)
                         and s.store[RESOURCE_ENERGY] > me.carryCapacity}
    target = me.pos.findClosestByRange(FIND_STRUCTURES, filter_containers)
    if target is not None:
        code = me.withdraw(target, RESOURCE_ENERGY)
        if code == OK:
            pass
        elif code == ERR_NOT_IN_RANGE:
            me.moveTo(target)
        else:
            me.say('ERR1: ' + str(code))
        return

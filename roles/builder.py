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
    elif me.carry.energy == me.carryCapacity:
        if me.memory.task != 'building' or me.memory.task != 'repairing':
            me.say('Working')
            if me.pos.findClosestByRange(FIND_MY_CONSTRUCTION_SITES) is not None:
                me.memory.task = 'building'
            else:
                me.memory.task = 'repairing'


def build(me):
    target = me.pos.findClosestByRange(FIND_MY_CONSTRUCTION_SITES)

    code = me.build(target)
    if code == OK:
        return
    elif code == ERR_NOT_IN_RANGE:
        me.moveTo(target)


def repair(me):
    filter_damaged = {'filter': lambda s: s.hits < s.hitsMax}
    target = me.pos.findClosestByRange(FIND_MY_STRUCTURES, filter_damaged)

    code = me.repair(target)
    if code == OK:
        return
    elif code == ERR_NOT_IN_RANGE:
        me.moveTo(target)


def collect(me):
    filter_containers = {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and
                         s.store[RESOURCE_ENERGY] > me.carryCapacity}
    target = me.pos.findClosestByRange(FIND_MY_STRUCTURES, filter_containers)

    code = me.withdraw(target)
    if code == OK:
        return
    elif code == ERR_NOT_IN_RANGE:
        me.moveTo(target)

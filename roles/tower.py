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
    if me.pos.findClosestByRange(FIND_HOSTILE_CREEPS) is not None:
        attack(me)
    else:
        repair(me)


def attack(me):
    target = me.pos.findClosestByRange(FIND_HOSTILE_CREEPS)
    if target is not None:
        me.attack(target)


def repair(me):
    filter_damaged = {'filter': lambda s: s.hits < s.hitsMax}
    target = me.pos.findClosestByRange(FIND_STRUCTURES, filter_damaged)
    me.repair(target)

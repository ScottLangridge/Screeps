from consts import TARGET_WALL_HEALTH
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
    # Regular repairs
    filter_damaged = {'filter': lambda s: s.hits < s.hitsMax and s.structureType != STRUCTURE_WALL
                      and s.structureType != STRUCTURE_RAMPART}
    target = me.pos.findClosestByRange(FIND_STRUCTURES, filter_damaged)
    if target is not None:
        me.repair(target)
        return

    # Repair defences
    filter_defences = {'filter': lambda s: s.structureType == STRUCTURE_WALL or s.structureType == STRUCTURE_RAMPART
                       and s.hits < s.hitsMax}
    target = None
    for defence in me.room.find(FIND_STRUCTURES, filter_defences):
        if target is None or defence.hits < target.hits:
            target = defence
    if target is not None and target.hits < TARGET_WALL_HEALTH:
        me.repair(target)
        return

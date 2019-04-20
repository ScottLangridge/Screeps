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
    enemies = me.room.find(FIND_HOSTILE_CREEPS)
    # Target Healers
    for i in enemies:
        for j in i.body:
            if j.type == 'heal':
                target = i

    # Target Any
    if target == undefined:
        target = me.pos.findClosestByRange(FIND_HOSTILE_CREEPS)

    # Attack
    if target != undefined:
        me.attack(target)


def repair(me):
    # Regular repairs
    filter_damaged = {'filter': lambda s: s.hits < s.hitsMax and s.structureType != STRUCTURE_WALL
                                          and s.structureType != STRUCTURE_RAMPART}
    target = me.pos.findClosestByRange(FIND_STRUCTURES, filter_damaged)
    if target is not None:
        me.repair(target)
        return

    if not Memory.energy_save:
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

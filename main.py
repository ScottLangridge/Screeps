# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.

from defs import *

# These are currently required for Transcrypt in order to use the following names in JavaScript.
# Without the 'noalias' pragma, each of the following would be translated into something like 'py_Infinity' or
#  'py_keys' in the output file.
__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

###############################################################################
# MY CODE
###############################################################################

import consts
from roles import tower, starter, harvester, builder, hauler, upgrader, static_miner, mine_hauler


# Run each tick.
def main():
    memory_cleanup()
    creep_counts = creep_control()
    spawn_control(creep_counts)
    tower_control()


# Controls all creeps
def creep_control():
    creep_counts = {'starter': 0, 'harvester': 0, 'builder': 0, 'hauler': 0, 'upgrader': 0, 'static_miner': 0,
                    'mine_hauler': 0}
    for creepName in Object.keys(Game.creeps):
        creep = Game.creeps[creepName]
        if creep.memory.role == 'harvester':
            harvester.run(creep)
            creep_counts['harvester'] += 1
        elif creep.memory.role == 'starter':
            starter.run(creep)
            creep_counts['starter'] += 1
        elif creep.memory.role == 'builder':
            builder.run(creep)
            creep_counts['builder'] += 1
        elif creep.memory.role == 'hauler':
            hauler.run(creep)
            creep_counts['hauler'] += 1
        elif creep.memory.role == 'upgrader':
            upgrader.run(creep)
            creep_counts['upgrader'] += 1
        elif creep.memory.role == 'static_miner':
            static_miner.run(creep)
            creep_counts['static_miner'] += 1
        elif creep.memory.role == 'mine_hauler':
            mine_hauler.run(creep)
            creep_counts['mine_hauler'] += 1
    return creep_counts


# Controls all spawners
def spawn_control(creep_counts):
    for spawnName in Object.keys(Game.spawns):
        spawn = Game.spawns[spawnName]

        # If already spawning, skip.
        if spawn.spawning is not None:
            continue

        # If there are not enough of a certain class, spawn it
        if creep_counts['starter'] < consts.TARGET_STARTERS:
            spawn.spawnCreep(consts.STARTER_BODY, name_creep('starter'), {'memory': {'role': 'starter'}})
            continue
        if creep_counts['harvester'] < consts.TARGET_HARVESTERS:
            spawn.spawnCreep(consts.HARVESTER_BODY, name_creep('harvester'), {'memory': {'role': 'harvester'}})
            continue
        if creep_counts['builder'] < consts.TARGET_BUILDERS:
            spawn.spawnCreep(consts.BUILDER_BODY, name_creep('builder'), {'memory': {'role': 'builder'}})
            continue
        if creep_counts['hauler'] < consts.TARGET_HAULERS:
            spawn.spawnCreep(consts.HAULER_BODY, name_creep('hauler'), {'memory': {'role': 'hauler'}})
            continue
        if creep_counts['upgrader'] < consts.TARGET_UPGRADERS:
            spawn.spawnCreep(consts.UPGRADER_BODY, name_creep('upgrader'), {'memory': {'role': 'upgrader'}})
            continue
        if creep_counts['static_miner'] < consts.TARGET_STATIC_MINERS:
            spawn.spawnCreep(consts.STATIC_MINER_BODY, name_creep('static'), {'memory': {'role': 'static_miner'}})
            continue
        if creep_counts['mine_hauler'] < consts.TARGET_MINE_HAULERS:
            spawn.spawnCreep(consts.MINE_HAULER_BODY, name_creep('m_hauler'), {'memory': {'role': 'mine_hauler'}})
            continue


# Controls towers
def tower_control():
    tower_filter = {'filter': lambda s: s.structureType == STRUCTURE_TOWER}
    for key, room in _.pairs(Game.rooms):
        for key2, this_tower in _.pairs(room.find(FIND_STRUCTURES, tower_filter)):
            tower.run(this_tower)


# Generates names for new creeps
def name_creep(role):
    pre = role[0].upper() + role[1:] + ' '

    i = 0
    while True:
        i += 1
        name = str(pre + str(i))
        if name in Game.creeps:
            continue
        else:
            return name


# Removes memory for dead creeps
def memory_cleanup():
    for name, creep in _.pairs(Memory.creeps):
        if not (name in Game.creeps):
            del Memory.creeps[name]


module.exports.loop = main

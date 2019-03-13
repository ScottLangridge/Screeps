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
from roles import starter, harvester, builder


# Run each tick.
def main():
    memory_cleanup()
    creep_counts = creep_control()
    spawn_control(creep_counts)


# Controls all creeps
def creep_control():
    creep_counts = {'starter': 0, 'harvester': 0, 'builder': 0}
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
            spawn.spawnCreep(consts.HARVESTER_BODY, name_creep('builder'), {'memory': {'role': 'builder'}})


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

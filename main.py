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

###############################################################################################################################
#    MY CODE
###############################################################################################################################

import consts
import starter
import harvester


# Run each tick.
def main():
    starters = 0
    harvesters = 0

    # MEMORY CONTROL
    # Cleanup
    for name, creep in _.pairs(Memory.creeps):
        if not (name in Game.creeps):
            del Memory.creeps[name]

    # CREEP CONTROL
    for creepName in Object.keys(Game.creeps):
        creep = Game.creeps[creepName]

        if creep.memory.role == 'harvester':
            harvester.run(creep)
            harvesters += 1
        elif creep.memory.role == 'starter':
            starter.run(creep)
            starters += 1

    # SPAWN CONTROL
    for spawnName in Object.keys(Game.spawns):
        spawn = Game.spawns[spawnName]

        # If already spawning, skip.
        if spawn.spawning is not None:
            continue

        # If there are not enough of a certain class, spawn it
        if harvesters < consts.TARGET_HARVESTERS:
            spawn.spawnCreep(harvester.BODY_1, name_creep('harvester'), {'memory': {'role': 'harvester'}})
            continue
        if starters < consts.TARGET_STARTERS:
            spawn.spawnCreep(starter.BODY_0, name_creep('starter'), {'memory': {'role': 'starter'}})
            continue


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


module.exports.loop = main

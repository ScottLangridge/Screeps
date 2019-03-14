from defs import *
from consts import STATIC_MINER_SPOTS, HARVESTER_CONTAINER_FILL_ORDER

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

    if me.memory.depositing:
        deposit(me)
    else:
        collect(me)


def decide_task(me):
    if me.carry.energy == 0:
        if me.memory.depositing:
            me.say('Collecting')
        me.memory.depositing = False
    elif me.carry.energy == me.carryCapacity:
        if not me.memory.depositing:
            me.say('Dropping')
        me.memory.depositing = True
    else:
        me.memory.depositing = True


def deposit(me):
    # Fill containers (in order of importance)
    for container in HARVESTER_CONTAINER_FILL_ORDER:
        target = Game.getObjectById(container)
        if target.store[RESOURCE_ENERGY] < target.storeCapacity:
            code = me.transfer(target, RESOURCE_ENERGY)
            if code == OK:
                me.memory.target = False
            elif code == ERR_NOT_IN_RANGE:
                me.moveTo(target)
            else:
                me.say('ERR1: ' + code)
            return

    # Fill storage
    filter_storage = {'filter': lambda s: s.structureType == STRUCTURE_STORAGE
                                          and s.storeCapacity - s.store[RESOURCE_ENERGY] > me.carry[RESOURCE_ENERGY]}
    target = me.pos.findClosestByRange(FIND_STRUCTURES, filter_storage)
    if target is not None:
        code = me.transfer(target, RESOURCE_ENERGY)
        if code == OK:
            pass
        elif code == ERR_NOT_IN_RANGE:
            me.moveTo(target)
        return

    # Fill extensions
    filter_extension = {'filter': lambda s: s.structureType == STRUCTURE_EXTENSION and s.energy < s.energyCapacity}
    target = me.pos.findClosestByRange(FIND_STRUCTURES, filter_extension)
    if target is not None:
        code = me.transfer(target, RESOURCE_ENERGY)
        if code == OK:
            pass
        elif code == ERR_NOT_IN_RANGE:
            me.moveTo(target)
        return

    # Fill spawns
    for spawn_name in Object.keys(Game.spawns):
        spawn = Game.spawns[spawn_name]
        if spawn.energy < spawn.energyCapacity:
            target = spawn
            code = me.transfer(target, RESOURCE_ENERGY)
            if code == OK:
                pass
            elif code == ERR_NOT_IN_RANGE:
                me.moveTo(spawn)
            return

    # Fill towers
    filter_tower = {'filter': lambda s: s.structureType == STRUCTURE_TOWER
                    and s.energyCapacity - s.energy > me.carry[RESOURCE_ENERGY]}
    target = me.pos.findClosestByRange(FIND_STRUCTURES, filter_tower)
    if target is not None:
        code = me.transfer(target, RESOURCE_ENERGY)
        if code == OK:
            pass
        elif code == ERR_NOT_IN_RANGE:
            me.moveTo(target)
        return


def collect(me):
    # Take from full mine containers
    for mine in STATIC_MINER_SPOTS:
        container = get_container_at(me, mine[0], mine[1])
        if container is not None and container.store[RESOURCE_ENERGY] >= me.carryCapacity:
            code = me.withdraw(container, RESOURCE_ENERGY)
            if code == OK:
                return
            elif code == ERR_NOT_IN_RANGE:
                me.moveTo(container)
            else:
                me.say('ERR3:' + str(code))
            return

    # Take from floor
    filter_floor_energy = {'filter': lambda s: s.resourceType == RESOURCE_ENERGY and s.amount > 100}
    target = me.pos.findClosestByRange(FIND_DROPPED_RESOURCES, filter_floor_energy)
    if target is not None:
        code = me.pickup(target)
        if code == OK:
            return
        elif code == ERR_NOT_IN_RANGE:
            me.moveTo(target)
        else:
            me.say('ERR1:' + str(code))
        return

    # Move to next mine container
    most_full = get_container_at(me, STATIC_MINER_SPOTS[0][0], STATIC_MINER_SPOTS[0][1])
    for mine in STATIC_MINER_SPOTS[1:]:
        container = get_container_at(me, mine[0], mine[1])
        if container.store[RESOURCE_ENERGY] > most_full.store[RESOURCE_ENERGY]:
            most_full = container
    if most_full is not None:
        me.moveTo(most_full)


def get_container_at(me, x, y):
    pos = me.room.getPositionAt(x, y)
    structures = pos.lookFor(LOOK_STRUCTURES)
    for s in structures:
        if s.structureType == STRUCTURE_CONTAINER:
            return s
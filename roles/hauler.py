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

    # Take from container
    filter_containers = {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER
                                             and s.store[RESOURCE_ENERGY] >= me.carryCapacity}
    target = me.pos.findClosestByRange(FIND_STRUCTURES, filter_containers)
    if target is not None:
        code = me.withdraw(target, RESOURCE_ENERGY)
        if code == OK:
            return
        elif code == ERR_NOT_IN_RANGE:
            me.moveTo(target)
        else:
            me.say('ERR2:' + str(code))
        return

    # Take from storage
    filter_storage = {'filter': lambda s: s.structureType == STRUCTURE_STORAGE
                      and s.store[RESOURCE_ENERGY] >= me.carryCapacity}
    target = me.pos.findClosestByRange(FIND_STRUCTURES, filter_storage)
    if target is not None:
        code = me.withdraw(target, RESOURCE_ENERGY)
        if code == OK:
            return
        elif code == ERR_NOT_IN_RANGE:
            me.moveTo(target)
        else:
            me.say('ERR3:' + str(code))
        return

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
            me.say('Upgrading')
        me.memory.depositing = True
    else:
        me.memory.depositing = True


def deposit(me):
    filter_controller = {'filter': lambda s: s.structureType == STRUCTURE_CONTROLLER}
    target = me.pos.findClosestByRange(FIND_STRUCTURES, filter_controller)
    code = me.upgradeController(target)
    if code == OK:
        return
    elif code == ERR_NOT_IN_RANGE:
        me.moveTo(target)
    else:
        me.say('ERR1: ' + code)


def collect(me):
    # Take from container
    filter_containers = {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER
                         and s.store[RESOURCE_ENERGY] >= me.carryCapacity}
    target = me.pos.findClosestByRange(FIND_STRUCTURES, filter_containers)
    code = me.withdraw(target, RESOURCE_ENERGY)
    if target is not None:
        if code == OK:
            return
        elif code == ERR_NOT_IN_RANGE:
            me.moveTo(target)
        else:
            me.say('ERR2:' + str(code))

from defs import *

TARGET_STARTERS = 5
TARGET_HARVESTERS = 1

# TODO Find a better solution for where to put bodies.
STARTER_BODY_0 = [MOVE, WORK, WORK, CARRY]
STARTER_BODY_1 = [MOVE, WORK, WORK, WORK, CARRY, CARRY]
STARTER_BODY_2 = [MOVE, MOVE, WORK, WORK, WORK, CARRY, CARRY]
HARVESTER_BODY_0 = [MOVE, WORK, WORK, CARRY]
HARVESTER_BODY_1 = [MOVE, WORK, WORK, WORK, CARRY, CARRY]
HARVESTER_BODY_2 = [MOVE, MOVE, WORK, WORK, WORK, CARRY, CARRY]

STARTER_BODY = STARTER_BODY_2
HARVESTER_BODY = HARVESTER_BODY_0

CONTAINER_FILL_ORDER = []

DEBUG_MESSAGES = False

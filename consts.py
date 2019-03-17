from roles.creep_bodies import BODIES

TARGET_STARTERS = 0
TARGET_HARVESTERS = 0
TARGET_BUILDERS = 0
TARGET_HAULERS = 2
TARGET_UPGRADERS = 1
TARGET_STATIC_MINERS = 2
TARGET_MINE_HAULERS = 1

STARTER_BODY = BODIES['starter'][2]
HARVESTER_BODY = BODIES['harvester'][2]
BUILDER_BODY = BODIES['builder'][4]
HAULER_BODY = BODIES['hauler'][0]
UPGRADER_BODY = BODIES['upgrader'][1]
STATIC_MINER_BODY = BODIES['static_miner'][0]
MINE_HAULER_BODY = BODIES['mine_hauler'][0]

HARVESTER_CONTAINER_FILL_ORDER = ['5c8837ab0feddb5f7827ba2c',
                                  '5c88e870946eb05f77944ad6',
                                  '5c884a25311fe41e87188549',
                                  '5c8a579903c0d05f629a5f0a']

STATIC_MINER_SPOTS = [[23, 18], [30, 20]]

DEBUG_MESSAGES = False

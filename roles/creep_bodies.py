from defs import *

BODIES = {'starter': [[MOVE, WORK, WORK, CARRY],
                      [MOVE, WORK, WORK, WORK, CARRY, CARRY],
                      [MOVE, MOVE, WORK, WORK, WORK, CARRY, CARRY]],

          'harvester': [[MOVE, WORK, WORK, CARRY],
                        [MOVE, WORK, WORK, WORK, CARRY, CARRY],
                        [MOVE, MOVE, WORK, WORK, WORK, CARRY, CARRY]],

          'builder': [[MOVE, WORK, WORK, CARRY],
                      [MOVE, WORK, WORK, WORK, CARRY, CARRY],
                      [MOVE, MOVE, MOVE, WORK, WORK, WORK, CARRY, CARRY, CARRY]],

          'hauler': [[MOVE, MOVE, MOVE, MOVE, MOVE, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY]]
          }

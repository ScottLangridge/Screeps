from defs import *

BODIES = {'starter': [[MOVE, WORK, WORK, CARRY],
                      [MOVE, WORK, WORK, WORK, CARRY, CARRY],
                      [MOVE, MOVE, WORK, WORK, WORK, CARRY, CARRY]],

          'harvester': [[MOVE, WORK, WORK, CARRY],
                        [MOVE, WORK, WORK, WORK, CARRY, CARRY],
                        [MOVE, MOVE, WORK, WORK, WORK, CARRY, CARRY]],

          'builder': [[MOVE, WORK, WORK, CARRY],
                      [MOVE, WORK, WORK, WORK, CARRY, CARRY],
                      [MOVE, MOVE, WORK, WORK, CARRY, CARRY, CARRY],
                      [MOVE, MOVE, MOVE, WORK, WORK, WORK, CARRY, CARRY, CARRY],
                      [MOVE, MOVE, MOVE, MOVE, WORK, WORK, WORK, WORK, CARRY, CARRY, CARRY, CARRY]],

          'hauler': [[MOVE, MOVE, MOVE, MOVE, MOVE, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY]],

          'upgrader': [[MOVE, CARRY, WORK],
                       [MOVE, MOVE, MOVE, WORK, WORK, WORK, WORK, CARRY, CARRY, CARRY, CARRY, CARRY]],

          'static_miner': [[MOVE, MOVE, MOVE, WORK, WORK, WORK, WORK, WORK]],

          'mine_hauler': [
              [MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY]],
          }

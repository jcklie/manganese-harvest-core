import numpy as np
import itertools

import fharvest.logic as fhl

from harvest.place_robots import place_robots
from harvest.geometry.taxicab_circle import TaxicabCircle
from harvest.geometry.minidisk import minidisk

from harvest.visualize import *

import harvest.io as io

from harvest.distance import *
from harvest.constants import MAX_DISTANCE



def goal_was_reached(data, goal):
	for robot in data[-1]:
		if not np.array_equal(robot, GOAL):
			return False
	return True

if __name__ == '__main__':
	AGENT = "heuristic"
	from_file = False
	write_file = False
	double = True
	if from_file:
		ROBO_COUNT, robots = io.positions_from_file('tests/robots_100.txt')
	else:
		ROBO_COUNT = 100
		robots = place_robots(ROBO_COUNT)

	if write_file:
		io.positions_to_file("tests/robots_{}.txt".format(ROBO_COUNT), robots)

	assert distance_constraint_holds(robots)

	GOAL, MISSION_TIME = calc_battle_plan(robots)
	assert all_can_reach_goal(robots, GOAL, MISSION_TIME)

	if double:
		MISSION_TIME *= 2

	STEPS = MISSION_TIME + 1	
	GOAL_X, GOAL_Y = GOAL

	
	data = np.zeros([STEPS, ROBO_COUNT, 2], dtype=np.int32)
	data[0] = robots

	traveled, collected = fhl.harvest(data, AGENT, GOAL_X, GOAL_Y, STEPS, ROBO_COUNT)
	#assert goal_was_reached(data, GOAL)

	print "Double: ", double
	print "Robots: ", ROBO_COUNT
	print "Mission time: ", MISSION_TIME 
	print "Goal: ", GOAL
	print "Traveled: ", traveled
	print "Collected: ", collected
	print "% harvested: ", collected / float(MISSION_TIME * ROBO_COUNT)

	animated(data,GOAL,interval=100)
	FILENAME = "test_{}_{}".format(ROBO_COUNT, AGENT)
	if double: FILENAME += "_double"
	#svg(data, FILENAME + ".svg")
	#png(data, FILENAME + ".png")
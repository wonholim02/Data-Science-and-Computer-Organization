import time

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import os

from robot_planning.environment.robots.simulated_robot import SimulatedRobot
from robot_planning.factory.factories import robot_factory_base
from robot_planning.factory.factories import renderer_factory_base
from robot_planning.factory.factories import logger_factory_base
from robot_planning.factory.factory_from_config import factory_from_config
from robot_planning.factory.factories import goal_checker_factory_base
import numpy as np
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def main():
    try:
        config_path = "configs/run_Autorally_MPPI.cfg"
        config_data = ConfigParser.ConfigParser()
        config_data.read(config_path)
        agent1 = factory_from_config(robot_factory_base, config_data, 'agent1')
        agent2 = factory_from_config(robot_factory_base, config_data, 'agent2')
        renderer1 = factory_from_config(renderer_factory_base, config_data, 'renderer1')
        logger = factory_from_config(logger_factory_base, config_data, 'logger')
        logger2 = factory_from_config(logger_factory_base, config_data, 'logger')

        agent1.set_renderer(renderer=renderer1)
        agent2.set_renderer(renderer=renderer1)

        logger.set_agent(agent=agent1)
        logger2.set_agent(agent=agent2)
        goal_checker_for_checking_vehicle_position = factory_from_config(goal_checker_factory_base, config_data, 'my_goal_checker_for_checking_vehicle_position')

        while True:
            try:
                state_next, cost = agent1.take_action_with_controller()
            except FileNotFoundError:
                logger.add_number_of_failure()
                agent1.reset_state()
                agent1.reset_time()
            logger.calculate_number_of_laps(state_next, dynamics=agent1.dynamics, goal_checker=agent1.cost_evaluator.goal_checker)
            logger.calculate_number_of_collisions(state_next, dynamics=agent1.dynamics, collision_checker=agent1.cost_evaluator.collision_checker)
            logger2.calculate_number_of_laps(state_next, dynamics=agent2.dynamics, goal_checker=agent2.cost_evaluator.goal_checker)
            logger2.calculate_number_of_collisions(state_next, dynamics=agent2.dynamics, collision_checker=agent2.cost_evaluator.collision_checker)
            renderer1.render_goal(goal_checker_for_checking_vehicle_position.get_goal())
            logger.log()
            if logger.crash == 1:
                break
            print(state_next, "    ", cost)
    finally:
        logger.shutdown()


if __name__ == '__main__':
    main()


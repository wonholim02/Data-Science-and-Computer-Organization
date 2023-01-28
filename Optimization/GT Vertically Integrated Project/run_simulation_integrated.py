try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import os
import ast
from robot_planning.scripts.generate_batch_configs import generate_batch_configs
import os
from robot_planning.factory.factories import robot_factory_base
from robot_planning.factory.factories import renderer_factory_base
from robot_planning.factory.factories import logger_factory_base
from robot_planning.factory.factory_from_config import factory_from_config
from robot_planning.factory.factories import goal_checker_factory_base
import numpy as np
from robot_planning.factory.factories import configs_generator_factory_base
from robot_planning.factory.factory_from_config import factory_from_config
import configparser as ConfigParser
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# streamlined batch experiment running process
def main():
    # use try and except to prevent unexpected crash
    print("")
    print("------------------- SECTION STARTED -------------------")
    print("")
    selection = int(input("Single experiment - \"1\" / Batch of experiments - \"2\" : "))
    print("")
    try:
        if selection == 1:
            print("---------- SET UP ----------")
            print("")
            choice = int(input("Select script for the experiment: \n (1) run_CSSMPC \n (2) run_CCMPPI \n (3) run_MPPI \n (4) run_MPPICS \n (5) run_MPPICS_SMPC \n (6) run_Autorally_CSSMPC \n (7) run_Autorally_MPPI \n (8) Manual \n Option:"))
            print("")
            # get path of the config and template config to be used for generating batch configs from the user
            if choice == 1:
                config_path = "configs/run_CSSMPC.cfg"
            elif choice == 2:
                config_path = "configs/run_CCMPPI.cfg"
            elif choice == 3:
                config_path = "configs/run_MPPI.cfg"
            elif choice == 4:
                config_path = "configs/run_MPPICS.cfg"
            elif choice == 5:
                config_path = "configs/run_MPPICS_SMPC.cfg"
            elif choice == 6:
                config_path = "configs/run_Autorally_MPPI.cfg"
            elif choice == 7:
                config_path = "configs/run_Autorally_CSSMPC.cfg"
            else :
                config_path = input("Enter config_path to be used: ")
            print("")
            # check if the path is invalid before executing
            try:
                config_data = ConfigParser.ConfigParser()
                config_data.read(config_path)
            except FileNotFoundError:
                # retry getting data
                config_path = input("[ERROR - PATH INVALID] Enter new config_path to be used:")
                print("")
                config_data = ConfigParser.ConfigParser()
                config_data.read(config_path)
            agent1 = factory_from_config(robot_factory_base, config_data, 'agent1')
            renderer1 = factory_from_config(renderer_factory_base, config_data, 'renderer1')
            logger = factory_from_config(logger_factory_base, config_data, 'logger')
            logger.set_agent(agent=agent1)
            agent1.set_renderer(renderer=renderer1)
            goal_checker_for_checking_vehicle_position = factory_from_config(goal_checker_factory_base, config_data,
                                                                             'my_goal_checker_for_checking_vehicle_position')
            collison = int(input("Number of crashes allowed: "))
            numCol = 0;
            print("")
            print("-----EXPERIMENT STARTED-----")
            print("")
            while True:
                try:
                    state_next, cost = agent1.take_action_with_controller()
                except FileNotFoundError:
                    logger.add_number_of_failure()
                    agent1.reset_state()
                    agent1.reset_time()
                logger.calculate_number_of_laps(state_next, dynamics=agent1.dynamics,
                                                goal_checker=agent1.cost_evaluator.goal_checker)
                logger.calculate_number_of_collisions(state_next, dynamics=agent1.dynamics,
                                                      collision_checker=agent1.cost_evaluator.collision_checker)
                renderer1.render_goal(goal_checker_for_checking_vehicle_position.get_goal())
                logger.log()
                if logger.crash == 1:
                    numCol = numCol + 1
                if numCol >= collison + 2:
                    break
                print(state_next, "    ", cost)
                agent1.dynamics.shutdown()
            print("")
            print("------EXPERIMENT ENDED------")
        elif selection == 2:
            print("")
            print("---------- SET UP ----------")
            print("")
            option = 0
            # get path of the config and template config to be used for generating batch configs from the user

            option = int(input("Select Batch Type \n (1) CSSMPC Batch \n (2) MPPI Batch \n (3) Others \n Option:"))
            print("")

            if option == 1:
                generate_batch_config_path = "configs/Autorally_CSSMPC_generate_batch_configs.cfg"
                template_config_path = "configs/run_Autorally_CSSMPC.cfg"
                run_batch_Autorally_config_path = "configs/run_batch_Autorally_CSSMPC.cfg"
                generate_batch_configs(generate_batch_config_path, template_config_path)
            elif option == 2:
                generate_batch_config_path = "configs/Autorally_MPPI_generate_batch_configs.cfg"
                template_config_path = "configs/run_Autorally_MPPI.cfg"
                run_batch_Autorally_config_path = "configs/run_batch_Autorally_MPPI.cfg"
                generate_batch_configs(generate_batch_config_path, template_config_path)
            else :
                generate_batch_config_path = input("Type generate_batch_config_path: ")
                template_config_path = input("Type template_config_path: ")
                run_batch_Autorally_config_path = input("Enter run_batch_Autorally_config_path to be used: ")
                generate_batch_configs(generate_batch_config_path, template_config_path)

            # get path of the batch config files to be executed from the user
            print("")
            batch_config_folder_path = "configs/batch_configs"
            print("")
            # check if the path is invalid
            try:
                config_data = ConfigParser.ConfigParser()
                config_data.read(run_batch_Autorally_config_path)
            except FileNotFoundError:
                # retry getting data
                run_batch_Autorally_config_path = input("[ERROR - PATH INVALID] Enter run_batch_Autorally_config_path to be used: ")
                print("")
                config_data = ConfigParser.ConfigParser()
                config_data.read(run_batch_Autorally_config_path)

            if option == 1:
                experiment_names = ast.literal_eval(config_data.get('run_batch_Autorally_CSSMPC', 'experiment_names'))
            elif option == 2:
                experiment_names = ast.literal_eval(config_data.get('run_batch_Autorally_MPPI', 'experiment_names'))
            else :
                experiment_naming = input("Enter experiment_name to be used: ")
                experiment_names = ast.literal_eval(config_data.get(experiment_naming, 'experiment_names'))

            # set up experiment based on user input

            print("-----EXPERIMENT STARTED-----")
            print("")
            # run each experiment assigned
            for experiment_name in experiment_names:
                print("Running " + experiment_name)
                single_experiment_config_path = batch_config_folder_path + '/' + experiment_name + '.cfg'
                single_experiment_config_data = ConfigParser.ConfigParser()
                single_experiment_config_data.read(single_experiment_config_path)
                run_single_Autorally(config_data=single_experiment_config_data, experiment_name=experiment_name)
            print("------EXPERIMENT ENDED------")
            print("")
        agent1.dynamics.shutdown()
    finally:
        print("------------------- SECTION ENDED -------------------")

def run_single_Autorally(config_data, experiment_name):
    # renderer and compile_batch_data visualize the entire experiment
    agent1 = factory_from_config(robot_factory_base, config_data, 'agent1')
    renderer1 = factory_from_config(renderer_factory_base, config_data, 'renderer1')
    logger = factory_from_config(logger_factory_base, config_data, 'logger')
    logger.set_agent(agent=agent1)
    agent1.set_renderer(renderer=renderer1)
    logger.set_experiment_name(experiment_name)
    goal_checker_for_checking_vehicle_position = factory_from_config(goal_checker_factory_base, config_data,
                                                                     'my_goal_checker_for_checking_vehicle_position')
    # try except to avoid abnormal crash
    try:
        # decide how many laps will be completed based on user input
        lapNum = input("Enter number of laps: ")
        while logger.get_num_of_laps() < int(lapNum):
            try:
                state_next, cost = agent1.take_action_with_controller()
            except:
                logger.add_number_of_failure()
                agent1.reset_state()
                agent1.reset_time()
                break
            finally:
                logger.calculate_number_of_laps(state_next, agent1.dynamics, goal_checker_for_checking_vehicle_position)
                logger.calculate_number_of_collisions(state_next, agent1.dynamics, agent1.cost_evaluator.collision_checker)
                # renderer1.render_goal(goal_checker_for_checking_vehicle_position.get_goal())
                logger.log()
                if logger.crash:
                    break
                # renderer1.show()
                # renderer1.clear()

                # streamlined output release process
                print("state: ", state_next, "cost: ", cost, "lap number: ", logger.get_num_of_laps())
                print("number of laps: ", logger.get_num_of_laps(), "number of collisions: ",
                      logger.get_num_of_collisions(), "number of controller failures: ", logger.get_num_of_failures())
        logger.shutdown()
    finally:
        # shutdown agent
        agent1.dynamics.shutdown()

if __name__ == '__main__':
    main()
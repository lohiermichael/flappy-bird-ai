import pickle

import pygame

from views.view_management.view_template import View
from views.play import PlayView
from views.train_ai import TrainAIView, NeatManagement, FinalTrainAIView
from views.test_ai import TestAIView

from config.neat.neat_config import GENERATIONS_NUMBER, BEST_NETWORK_LOCATION


def run_play():
    replay = True
    while replay:
        play_view = PlayView()
        play_view.start_main_loop()
        replay = play_view.replay


def run_train_ai():

    # Make the train view
    train_view = TrainAIView()

    # Run the genetic algorithm on the eval genome method of the train view
    neat_management = NeatManagement(generations_number=GENERATIONS_NUMBER)
    neat_management.run(eval_func=train_view.neat_eval_genome)

    # Save the best net
    best_network = train_view.best_network
    with open(BEST_NETWORK_LOCATION, 'wb') as f:
        pickle.dump(best_network, f)

        # Make the final view
    game = train_view.game
    final_train_ai_view = FinalTrainAIView(game=game)
    final_train_ai_view.start_main_loop()


def run_test_ai():

    with open(BEST_NETWORK_LOCATION, 'rb') as f:
        best_network = pickle.load(f)

    replay = True
    while replay:
        test_ai_view = TestAIView(best_network=best_network)
        test_ai_view.start_main_loop()
        replay = test_ai_view.replay


if __name__ == "__main__":
    pygame.init()

    run_train_ai()

    run_test_ai()

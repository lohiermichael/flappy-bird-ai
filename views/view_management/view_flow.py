import pickle

import pygame

from ..start import StartView
from ..play import PlayView
from ..train_ai import TrainAIView, NeatManagement, FinalTrainAIView
from ..test_ai import TestAIView
from ..play_against_ai import PlayAgaintAI

from config.neat.neat_config import GENERATIONS_NUMBER, BEST_NETWORK_LOCATION


class ViewFlow:
    def __init__(self):
        self.current_view = None

    def run(self):

        while self.current_view is None or self.current_view.return_start_view:

            self.run_start()

            if self.current_view.selected_game_type == 'Play Normal Game':
                self.run_play()
            elif self.current_view.selected_game_type == 'Train AI':
                self.run_train_ai()
            elif self.current_view.selected_game_type == 'Test AI':
                self.run_test_ai()
            elif self.current_view.selected_game_type == 'Play Against AI':
                self.run_play_against_ai()

    def run_start(self):
        self.current_view = StartView()
        self.current_view.run_main_loop()

    def run_play(self):
        replay = True
        while replay:
            self.current_view = PlayView()
            self.current_view.run_main_loop()
            replay = self.current_view.replay

    def run_train_ai(self):

        # Make the train view
        self.current_view = TrainAIView()

        # Run the genetic algorithm on the eval genome method of the train view
        neat_management = NeatManagement(generations_number=GENERATIONS_NUMBER)
        neat_management.run(eval_func=self.current_view.neat_eval_genome)

        # Save the best net
        best_network = self.current_view.best_network
        with open(BEST_NETWORK_LOCATION, 'wb') as f:
            pickle.dump(best_network, f)

            # Make the final view
        game = self.current_view.game
        self.current_view = FinalTrainAIView(game=game)
        self.current_view.run_main_loop()

    def run_test_ai(self):

        with open(BEST_NETWORK_LOCATION, 'rb') as f:
            best_network = pickle.load(f)

        replay = True
        while replay:
            self.current_view = TestAIView(best_network=best_network)
            self.current_view.run_main_loop()
            replay = self.current_view.replay

    def run_play_against_ai(self):

        with open(BEST_NETWORK_LOCATION, 'rb') as f:
            best_network = pickle.load(f)

        replay = True
        while replay:
            self.current_view = PlayAgaintAI(best_network=best_network)
            self.current_view.run_main_loop()
            replay = self.current_view.replay

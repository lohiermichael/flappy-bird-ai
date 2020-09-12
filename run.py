import pygame

from views.play import PlayView
from views.train_ai import TrainView, NeatManagement
from views.view_management.view_template import View

from config.neat.neat_config import GENERATIONS_NUMBER


def run_play():
    replay = True
    while replay:
        play_view = PlayView()
        play_view.start_main_loop()
        replay = play_view.replay


def run_train_ai():

    eval_func = TrainView().neat_eval_genome

    neat_management = NeatManagement(generations_number=GENERATIONS_NUMBER)
    neat_management.run(eval_func=eval_func)


if __name__ == "__main__":
    pygame.init()
    # run_play()
    run_train_ai()

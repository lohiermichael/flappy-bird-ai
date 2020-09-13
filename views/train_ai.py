import pygame
import neat

from .view_management.view_template import View

from objects.visual_objects import Bird, Pipe, Base
from objects.game_objects import GameTrainAI

from config.config import *
from config.neat.neat_config import NETWORK_CONFIG_FILE, FITNESS_DECREASE_DIE, FITNESS_INCREASE_PASS_PIE, FITNESS_INCREASE_ON_MOVE


class TrainAIView(View):

    def __init__(self):
        super().__init__()

        self.name = 'train_ai'
        self.game = GameTrainAI()
        self.best_network = None

    def neat_eval_genome(self, genomes, config):
        """Runs the simulation of the current population of birds
        and sets their fitness based on the distance they reach in the
        game

        Args:
            genome: Neat genome object
            config: Neat config object
        """

        self.neat_genomes = genomes
        self.neat_config = config

        self._initialize_objects()

        self.run_main_loop()

    def _initialize_objects(self):

        self.pipes = [Pipe(x=INITIAL_PIPE_X)]

        self.base = Base(y=INITIAL_BASE_Y)

        self.game.score = 0
        self.game.generation += 1
        self.game.total_birds = len(self.neat_genomes)
        self.game.living_birds = len(self.neat_genomes)

        self.active = True

        # The three following lists map on their index
        # Create lists for holding the genome (collection of birds)
        self.genomes = []
        # Create a list for holding theire neural networks
        self.nets = []
        # Create a list for holding th birds
        self.birds = []

        for _, genome in self.neat_genomes:
            # Initialize the fitness
            genome.fitness = 0
            # Initialize the neural network
            net = neat.nn.FeedForwardNetwork.create(
                genome, self.neat_config)

            # Initialize the NeatManager objects
            self.nets.append(net)
            # Make all the birds at the same starting position
            self.birds.append(
                Bird(x=INITIAL_BIRD_X, y=INITIAL_BIRD_Y, bird_type='ai'))
            self.genomes.append(genome)

    def _main_loop(self):

        self._manage_events()

        self._make_ai_choose_jump()

        self._manage_collisions()

        self._manage_pipes()

        self._move_objects()

        self._pass_pipe()

        self._redraw_window()

        self._update_best_net()

        self._check_terminal_condition()

    def _manage_events(self):

        for event in pygame.event.get():
            # Quite the window
            if event.type == pygame.QUIT:
                self._quit_window()

    def _make_ai_choose_jump(self):

        # Determine which pipe we must focus on (first or second)
        pipe_index = 0
        if len(self.birds) > 0:
            if len(self.pipes) > 1 and self.birds[0].x > self.pipes[0].x + self.pipes[0].WIDTH:
                pipe_index = 1

        # If no birds left, quit the game
        else:
            self._quit_window()

        for i_bird, bird in enumerate(self.birds):

            # Send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output_network = self.nets[i_bird].activate((bird.y, abs(
                bird.y - self.pipes[pipe_index].y_top), abs(bird.y - self.pipes[pipe_index].y_bottom)))

            # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
            if output_network[0] > 0.5:
                bird.jump()

    def _manage_collisions(self):
        """"Remove fitness on collision and make the bird dies"""

        indices_birds_to_remove = set()

        for bird_index, bird in enumerate(self.birds):

            if bird.collide_base(self.base):
                indices_birds_to_remove.add(bird_index)

            elif bird.collide_top_window():
                indices_birds_to_remove.add(bird_index)

            for pipe in self.pipes:
                if bird.collide_pipe(pipe):
                    indices_birds_to_remove.add(bird_index)

        self._remove_bird_on_indices(indices_birds_to_remove)

    def _manage_pipes(self):

        # Pipes to remove
        pipes_to_remove = []

        for pipe in self.pipes:
            # If it gets off the screen add it to the list to remove
            if pipe.x + pipe.WIDTH < 0:
                pipes_to_remove.append(pipe)

        for pipe_to_remove in pipes_to_remove:
            self.pipes.remove(pipe_to_remove)

    def _move_objects(self):

        # Base
        self.base.move()
        # Pipes
        for pipe in self.pipes:
            pipe.move()

        # Grant each bird fitness on movement
        for i_bird, bird in enumerate(self.birds):
            self.genomes[i_bird].fitness += FITNESS_INCREASE_ON_MOVE
            bird.move()

    def _pass_pipe(self):
        """Update the score of the birds that go through a pipe
        as well as increasing their fitness level"""

        for pipe in self.pipes:

            # If the pipe is passed create a new one
            if self.birds and (not pipe.passed and pipe.x < self.birds[0].x):
                # Update score
                self.game.score += 1
                pipe.passed = True
                self.pipes.append(Pipe(x=INITIAL_PIPE_X))

            # Increase the fitness score of the genome (bird) still alive
            for genome in self.genomes:
                genome.fitness += FITNESS_INCREASE_PASS_PIE

    def _remove_bird_on_indices(self, indices_birds_to_remove):

        for bird_index in indices_birds_to_remove:
            # Decrease fitness
            self.genomes[bird_index].fitness -= FITNESS_DECREASE_DIE

            self.game.living_birds -= 1

        self.birds = [bird for i_bird, bird in enumerate(
            self.birds) if i_bird not in indices_birds_to_remove]
        self.genomes = [genome for i_bird, genome in enumerate(
            self.genomes) if i_bird not in indices_birds_to_remove]
        self.nets = [net for i_bird, net in enumerate(
            self.nets) if i_bird not in indices_birds_to_remove]

    def _redraw_window(self):
        self.clock.tick(FPS)
        self.window.blit(BACKGROUND_IMAGE,
                         (INITIAL_BACKGROUND_X, INITIAL_BACKGROUND_Y))

        for bird in self.birds:
            bird.draw(window=self.window)

        # Draw the pipe first and then the base
        for pipe in self.pipes:
            pipe.draw(window=self.window)

        self.base.draw(window=self.window)

        self.game.draw_score(window=self.window)
        self.game.draw_generation(window=self.window)
        self.game.draw_birds_count(window=self.window)

        pygame.display.update()

    def _update_best_net(self):
        if len(self.nets) == 1 and self.game.score > self.game.best_score:
            self.best_network = self.nets[0]

    def _check_terminal_condition(self):
        # If no bird living, leave the main loop
        if not self.birds:
            self.active = False
            # Update best score
            self.game.best_score = max(self.game.score, self.game.best_score)


class FinalTrainAIView(View):
    def __init__(self, game: GameTrainAI):
        super().__init__()

        self.game = game

        self.name = 'final_train_ai'

        self.base = Base(y=INITIAL_BASE_Y)

    def _main_loop(self):

        self._manage_events()

        self._redraw_window()

    def _manage_events(self):

        for event in pygame.event.get():
            # Quite the window
            if event.type == pygame.QUIT:
                self._quit_window()

    def _redraw_window(self):
        self.clock.tick(FPS)
        self.window.blit(BACKGROUND_IMAGE,
                         (INITIAL_BACKGROUND_X, INITIAL_BACKGROUND_Y))

        self.base.draw(window=self.window)

        self.game.draw_best_score(window=self.window)

        pygame.display.update()


class NeatManagement:
    def __init__(self, generations_number: int, config_file=None):
        """Initialize the object in which we will make the AI

        Args:
            generation_number (int): Maximal number of generations we want to run the algorithm
            config_file (txt, optional): neat configuration file. Defaults to None.
        """

        self.generations_number = generations_number

        self.config_file = config_file if config_file else NETWORK_CONFIG_FILE
        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                         self.config_file)

        self._create_population()
        self._add_reporter()

    def _create_population(self):
        """This is the top level of a NEAT run"""

        self.population = neat.Population(self.config)

    def _add_reporter(self):
        """Show the progress in the terminal"""

        self.population.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.population.add_reporter(self.stats)

    def run(self, eval_func):
        """Run the genetic algorithm

        Args:
            func : function on which we should evaluate the algorithm
        """
        # Make the winner
        self.winner = self.population.run(eval_func, self.generations_number)

        # Show final stats
        print(f'\nBest genome:\n{self.winner}')

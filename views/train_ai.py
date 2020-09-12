import pygame
import neat

from .view_management.view_template import View

from objects.visual_objects import Bird, Pipe, Base
from objects.game_objects import Game, RectangularButton

from config.config import *
from config.neat.neat_config import NETWORK_CONFIG_FILE, FITNESS_DECREASE_DIE, FITNESS_INCREASE_PASS_PIE


class TrainView(View):

    def __init__(self):
        super().__init__()

        self.name = 'train'

        self.generation = 0

        self.pipes = [Pipe(x=INITIAL_PIPE_X)]

        self.base = Base(y=INITIAL_BASE_Y)

        self.score = 0

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

        self._initialize_genome_objects()

        self.start_main_loop()

    def _initialize_genome_objects(self):

        self.generation += 1

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
            self.birds.append(Bird(INITIAL_BIRD_X, INITIAL_BACKGROUND_Y))
            self.genomes.append(genome)

    def _main_loop(self):

        self._manage_events()

        self._make_ai_choose_jump()

        self._manage_collisions()

        self._manage_pipes()

        self._move_objects()

        self._pass_pipe()

        self._redraw_window()

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

        for bird in self.birds:

            # Send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output_network = self.nets[self.birds.index(bird)].activate((bird.y, abs(
                bird.y - self.pipes[pipe_index].y_top), abs(bird.y - self.pipes[pipe_index].y_bottom)))

            # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
            if output_network[0] > 0.5:
                bird.jump()

    def _manage_collisions(self):
        """"Remove fitness on collision and make the bird dies"""

        for bird_index, bird in enumerate(self.birds):

            if bird.collide_base(self.base):
                self.genomes[bird_index].fitness -= FITNESS_DECREASE_DIE
                self._remove_bird_on_index(bird_index)

            elif bird.collide_top_window():
                self.genomes[bird_index].fitness -= FITNESS_DECREASE_DIE
                self._remove_bird_on_index(bird_index)

            for pipe in self.pipes:
                if bird.collide_pipe(pipe):
                    self.genomes[bird_index].fitness -= FITNESS_DECREASE_DIE
                    self._remove_bird_on_index(bird_index)

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
        for x, bird in enumerate(self.birds):
            self.genomes[x].fitness += 0.1
            bird.move()

    def _pass_pipe(self):
        """Update the score of the birds that go through a pipe
        as well as increasing their fitness level"""

        for pipe in self.pipes:
            # Update score
            self.score += 1

            # If the pipe is passed create a new one
            if not self.birds or (not pipe.passed and pipe.x < self.birds[0].x):
                pipe.passed = True
                self.pipes.append(Pipe(x=INITIAL_PIPE_X))

            # Increase the fitness score of the genome (bird) still alive
            for genome in self.genomes:
                genome.fitness += FITNESS_INCREASE_PASS_PIE

    def _remove_bird_on_index(self, bird_index):
        self.birds.pop(bird_index)
        self.nets.pop(bird_index)
        self.genomes.pop(bird_index)

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

        # self.game.draw_score(window=self.window)

        pygame.display.update()

    def _check_terminal_condition(self):
        # If no bird living, leave the main loop
        print(len(self.birds))
        if not self.birds:
            self.active = False


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

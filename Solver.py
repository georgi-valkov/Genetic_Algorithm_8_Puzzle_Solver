from Population import Population
import threading, os
import time
# Importing kivy components
from kivy.clock import mainthread
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.splitter import Splitter


class MyApp(App):
    """
    Handles the proper exit of the app
    Stops all threads
    """
    def on_stop(self):
        os._exit(1)
    # Global variables
    board_layout = GridLayout()
    initial_state_ti = None
    goal_state_ti = None
    shape_ti = TextInput(multiline=False, size_hint=(None, None),
                         width=125, height=30, hint_text='Shape 3x3', text='3x3', readonly=True)
    initial_population_ti = None
    mutation_rate_ti = None
    valid_moves = None
    previous_move = ''
    generation = Label(size_hint=(None,None), height=30)
    avg_fitness = Label(size_hint=(None,None), height=30)
    population_to = TextInput(readonly=True)
    current_state = ''

# Building all of the controls
    def build(self):
        # Set title of the window
        self.title = 'Solver'
        # Set layouts
        root_layout = BoxLayout(orientation='horizontal')
        column_1 = GridLayout(rows=2, padding=[5, 5, 5, 5])
        column_2 = GridLayout(rows=18, padding=[0, 5, 0, 5])
        column_3 = GridLayout(rows=1, padding=[5, 5, 5, 5])

        # Add elements to columns
        # Column 1 Controls
        self.valid_moves = TextInput(readonly=True)
        column_1.add_widget(self.board_layout)
        column_1.add_widget(self.valid_moves)

        # Column 2 Controls
        column_2.add_widget(Label(text='Initial State', size_hint=(None,None), width=80, height=30))
        self.initial_state_ti = TextInput(multiline=False, size_hint=(None,None),
                                          width=200, height=30, hint_text='Initial State 1234...', text='283164705')
        self.initial_state_ti.bind(focus=self.on_focus)
        column_2.add_widget(self.initial_state_ti)
        column_2.add_widget(Label(text='Goal State', size_hint=(None,None), width=75, height=30))
        self.goal_state_ti = TextInput(multiline=False, size_hint=(None,None),
                                       width=200, height=30, hint_text='Goal State 1234...', text='123804765')
        column_2.add_widget(self.goal_state_ti)
        column_2.add_widget(Label(text='Shape', size_hint=(None,None), width=45, height=30))
        column_2.add_widget(self.shape_ti)
        column_2.add_widget(Label(text='Initial Population', size_hint=(None,None), width=115, height=30))
        self.initial_population_ti = TextInput(multiline=False, size_hint=(None,None),
                                               width=125, height=30, hint_text='Ex.50', text='50')
        column_2.add_widget(self.initial_population_ti)
        column_2.add_widget(Label(text='Mutation Rate', size_hint=(None,None), width=95, height=30))
        self.mutation_rate_ti = TextInput(multiline=False, size_hint=(None,None),
                                          width=125, height=30, hint_text='Ex. 0.01', text='0.01')
        column_2.add_widget(self.mutation_rate_ti)
        column_2.add_widget(Splitter(size_hint_y=None, height=5))
        column_2.add_widget(Button(text='Solve',
                                   size_hint_y=None, on_press=lambda a:self.start_second_thread(self.main_function)))
        column_2.add_widget(Splitter(size_hint_y=None, height=150))
        grid = GridLayout(rows=2, cols=2)
        grid.add_widget(Label(text='Generation', size_hint=(None,None), height=10))
        grid.add_widget(Label(text='Avg. Fitness', size_hint=(None,None), height=10))
        grid.add_widget(self.generation)
        grid.add_widget(self.avg_fitness)
        column_2.add_widget(grid)

        # Column 3 Controls
        column_3.add_widget(self.population_to)

        # Add elements to the root layout
        root_layout.add_widget(column_1)
        root_layout.add_widget(column_2)
        root_layout.add_widget(column_3)

        return root_layout

    # It is used to create the board when initial state text input box is de focused
    def on_focus(self, instance, value):
        if not value:
            self.set_up_board(shape=self.shape_ti.text, state=self.initial_state_ti.text)

    # Sets up the board with buttons
    def set_up_board(self, shape, state):
        # Remove all buttons of the layout first
        self.board_layout.clear_widgets()
        # Create buttons and put them in the layout
        if shape is not '' and state is not '':
            shape = int(shape.split('x')[0])
            self.board_layout.cols = int(shape)
            self.board_layout.rows = int(shape)
            for i in range(int(shape) * int(shape)):
                if state[i] == '0':
                    self.board_layout.add_widget(Button(text='', border=(1, 1, 1, 1)))
                else:
                    self.board_layout.add_widget(Button(text=state[i], border=(1, 1, 1, 1)))
    # Starts a second thread to run the computation heavy main logic of the solver
    def start_second_thread(self, function):

        threading.Thread(target=function, args=(self.initial_state_ti.text,
                                                self.goal_state_ti.text,
                                                self.initial_population_ti.text,
                                                self.mutation_rate_ti.text,
                                                self.shape_ti.text)).start()
    # Use main thread only to update valid moves on the board and in the valid moves text box output
    @mainthread
    def update_valid_moves(self, valid_move):

        if valid_move is not None:
            move = valid_move.split('-')[1]
            move = move.replace(' ', '')
            gen = valid_move.split('-')[2]
            # Determine moving position
            if self.current_state.index('0') - move.index('0') == -1:
                direction = 'Left'
            elif self.current_state.index('0') - move.index('0') == 1:
                direction = 'Right'
            elif self.current_state.index('0') - move.index('0') == 3:
                direction = 'Down'
            elif self.current_state.index('0') - move.index('0') == -3:
                direction = 'UP'
            # Append valid moves to the output box
            self.valid_moves.text = self.valid_moves.text + 'Move tile ' + \
                                    self.current_state[move.index('0')] + ' to the ' + \
                                    direction + ' - gen ' + gen + '\n'
            # Replace current state with the valid move
            self.current_state = move
            # Make changes to the board to reflect valid move
            self.board_layout.clear_widgets()
            self.set_up_board(shape=self.shape_ti.text, state=move)

    # Use main thread to write time taken to find solution
    @mainthread
    def update_time(self, time):
        # Append processing time to the valid_move box
        self.valid_moves.text = self.valid_moves.text + '\n\n Took %.2f sec to finish\n\n' % round(time,2)

    # Update current generation, average fitness and show all members in the population
    def update_gen_fit_pop(self, generation, avg_fitness, population):
        self.generation.text = str(generation)
        self.avg_fitness.text = str(avg_fitness)
        self.population_to.text = population

    #============================
    # MAIN LOGIC
    #============================
    def main_function(self, _initial_state, _goal_state, _initial_population, _mutation_rate, _shape):
        # Check if all required field were filed
        if _initial_state is not '' and _goal_state is not '' and _initial_population is not '' and _mutation_rate is not '' and _shape is not '':
            shape = int(_shape.split('x')[0])
            initial_state = [None] * (shape**2)
            goal_state = [None] * (shape**2)
            for i in range(shape**2):
                initial_state[i] = int(_initial_state[i])
                goal_state[i] = int(_goal_state[i])
            self.current_state = self.initial_state_ti.text

            # Start timer
            start_time = time.time()
            #=============
            # Solve puzzle
            #=============
            # Creating initial population with following parameters
            po = Population(initial_state=initial_state,
                            goal_state=goal_state,
                            initial_population=int(_initial_population),
                            mutation_rate=float(_mutation_rate),
                            shape=shape)
            # Calculate fitness
            po.calculate_fitness()
            # While a solution is found do:
            # 1. Generate new generation
            # 2. Calculate fitness
            # 3. Check for a valid move
            #   3.1 Show valid move
            #   3.2 Check if valid move has reached the goal
            while True:
                po.produce_new_generation()
                po.calculate_fitness()
                valid_move = po.evaluate()
                population_str = ''
                for member in po.members:
                    population_str =''.join(str(e) for e in member.state) + '\t' + population_str
                self.update_valid_moves(valid_move)
                self.update_gen_fit_pop(po.generation, po.avg_fitness, population_str)
                if po.elite_chromosome.state == goal_state:
                    break
            # Stop timer
            stop_time = time.time()
            # Update time in GUI
            self.update_time(stop_time - start_time)



if __name__ == '__main__':
    MyApp().run()
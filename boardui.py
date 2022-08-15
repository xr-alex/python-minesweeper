import tkinter as tkinter
from tkinter import *
import soundmanager
import board
import sys


class BoardUI:

    #    Construtor onde são atribuidas as dimensoes para a board ui e os icones utilizados
    def __init__(self, game_board):
        self._board = game_board
        self.sound_manager = soundmanager.SoundManager
        # UI Settings
        self.window = tkinter.Tk()
        self.window.title("Minesweeper")
        self.rows = game_board.get_size()
        self.cols = game_board.get_size()
        self.buttons = []
        self.popup = None
        self.information_layer = None
        self.information_layer_flag = None

        # Load icons
        self._load_icons()

    # Função que inicializa os icons usados no jogo.
    def _load_icons(self):
        self.flag_image = PhotoImage(file=r"Icons\flag.png")
        self.question_mark_image = PhotoImage(file=r"Icons\question.png")
        self.down_image = PhotoImage(file=r"Icons\tilebase.png")
        self.mine_image = PhotoImage(file=r"Icons\mine.png")
        self.bomb_image = PhotoImage(file=r"Icons\hit.png")

        self.bomb_count_image = []
        self.bomb_count_image.append(self.down_image)
        for i in range(8):
            self.bomb_count_image.append(PhotoImage(file=r"Icons\mine" + str(i + 1) + ".png"))

        self.col_row_image = []
        for i in range(10):
            self.col_row_image.append(PhotoImage(file=r"Icons\coord" + str(i) + ".png"))

    """
        Função que chama todas as funções resposaveis pela criação dos componentes da UI
    """

    def create_gui(self):
        self.create_top_restart_button()
        self.create_side_numbers()
        self.crete_button_board()
        self.create_information_row()
        self.window.resizable(0, 0)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    """
    Função que cria um botão de restart no topo da UI
    """

    def create_top_restart_button(self):
        tkinter.Button(self.window, text="Restart", command=self.restart_game).grid(row=0, column=1,
                                                                                    columnspan=self.cols,
                                                                                    sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)

    """
    Função que cria os numeros laterais indicadores das posiçoes da board
    """

    def create_side_numbers(self):
        for i in range(1, self.cols + 1):
            tkinter.Label(self.window, image=self.col_row_image[i - 1]).grid(row=1, column=i,
                                                                             sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        for j in range(2, self.rows + 2):
            tkinter.Label(self.window, image=self.col_row_image[j - 2]).grid(row=j, column=0,
                                                                             sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)

    """
    Função que cria a UI da grelha de jogo composta por botões, que
    chamam funções distintas se feito um right ou left click no rato.
    """

    def crete_button_board(self):
        self.buttons.clear()
        for x in range(0, self.cols):
            self.buttons.append([])
            for y in range(0, self.rows):
                b = tkinter.Button(self.window, text=" ", image=self.question_mark_image,
                                   command=lambda x=x, y=y: self.on_click(x, y))
                b.bind("<Button-3>", lambda e, x=x, y=y: self.on_right_click(x, y))
                b.grid(row=y + 2, column=x + 1, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
                self.buttons[x].append(b)

    # Função que cria a zona da UI onde irá ser feito o display do numero de bandeiras
    def create_information_row(self):
        self.information_layer_flag = tkinter.Label(self.window, image=self.flag_image).grid(row=self.rows + 2,
                                                                                             column=int(self.cols / 2),
                                                                                             sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        self.information_layer = tkinter.Label(self.window, text=str(self._board.get_flag_count()))
        self.information_layer.grid(row=self.rows + 2, column=int(self.cols / 2 + 1),
                                    sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)

    """
        Função que faz restart da Board Ui criando uma nova board e de seguida 
        um novo campo de jogo e faz update do numero de flags disponiveis  
    """

    def restart_game(self):
        self._board = board.Board(self._board.get_size(), self._board.get_ratio())
        self.crete_button_board()
        self.update_flag_count()
        if self.popup is not None:
            self.popup.destroy()

    """
        Função responsável por tratar os left clicks nos botões (descobre uma casa)
        Esta função irá chamar duas funções da class board que iram tratar este click dada a posição do botão
    """

    def on_click(self, x, y):
        if not self._board.is_game_over():
            self.sound_manager.play_click_sound()
            self._board.test_position(x, y, self)
            self._board.check_winning_condition(self)

    """
        Função responsável por tratar os right clicks nos botões (marca uma casa com uma bandeira)
        Esta função irá chamar duas funções da class board que iram tratar este click
    """

    def on_right_click(self, x, y):
        if not self._board.is_game_over():
            self._board.flag_position(x, y, self)
            self._board.check_winning_condition(self)

    # Função chamada quando o utilizador clica no botão "Tentar Novamente".
    def new_game(self):
        self.window.destroy()

    # Função chamada no evento de o utilizador clicar no botão de sair do SO.
    def on_closing(self):
        sys.exit()

    """
        Função que cria um popup de end_game com a mensagem uma dada mensagem, este popup tem 
        dois botões um para fazer restart no jogo e outro para sair deste
    """

    def end_game_popup(self, text):
        # Create pop-up window object
        self.popup = tkinter.Toplevel()
        self.popup.title(text)
        self.popup.grab_set()
        self.popup.resizable(0, 0)

        # Create frame
        my_frame = Frame(self.popup, width=300, height=300)
        my_frame.pack(expand=True)

        # Create button objects
        new_game_btn = tkinter.Button(my_frame, text="Novo Tabuleiro", command=self.new_game)
        restart_btn = tkinter.Button(my_frame, text="Tentar Novamente", command=self.restart_game)
        quit_btn = tkinter.Button(my_frame, text="Sair", command=self.quit_game)

        # Place them on the frame
        new_game_btn.pack(side=LEFT)
        restart_btn.pack(side=LEFT)
        quit_btn.pack(side=LEFT)

        # Define pop-up window geometry
        x = self.window.winfo_x()
        y = self.window.winfo_y()
        w = self.window.winfo_reqwidth()
        h = 35
        self.popup.geometry("%dx%d+%d+%d" % (w, h, x, y + self.window.winfo_reqheight() / 2 - h / 2))
        self.popup.protocol("WM_DELETE_WINDOW", self.on_closing)

    """
        Função responsavél pela saida do jogo 
    """

    def quit_game(self):
        sys.exit()

    """
        Função que chama um popup de end_game com a mensagem "You win!"
    """

    def win_game(self):
        print('Vitória!')
        self.end_game_popup('Vitória!')

    def reveal_board(self):
        pass

    """
        Função que recebe coordenadas x e y para trocar a imagem do botão 
        nessa posição para a imagem de uma bomba e chama um popup de end_game com a mensagem "Game over"
    """

    def display_bomb(self, x, y):
        self.buttons[x][y].config(image=self.bomb_image)
        self.sound_manager.play_bomb_exploding_sound()
        self.end_game_popup('Game Over')

    """
     Função que recebe coordenadas x e y para trocar a imagem do botão 
     nessa posição com a imagem de uma bomba que não foi explodida
     """

    def display_mine(self, x, y):
        self.buttons[x][y].config(image=self.mine_image)

    """
         Função que faz o update do numero de bandeiras 
    """

    def update_flag_count(self):
        self.information_layer['text'] = str(self._board.get_flag_count())

    """
        Função que recebe coordenadas x e y para trocar a imagem do botão 
        nessa posição para a imagem de uma bandeira
    """

    def display_flag(self, x, y):
        self.sound_manager.play_place_flag_sound()
        self.update_flag_count()
        self.buttons[x][y].config(image=self.flag_image)

    """
        Função que recebe coordenadas x e y para trocar a imagem do botão 
        nessa posição de uma bandeira para o ponte de interrogação
    """

    def remove_flag(self, x, y):
        self.sound_manager.play_unflag_sound()
        self.update_flag_count()
        self.buttons[x][y].config(image=self.question_mark_image)

    """
        Função que recebe coordenadas x e y assim como o numero de bombas na vizinhança dessa casa 
        e com isso irá mudar a imagem do botão para uma imagem do numero dado
    """

    def display_number_of_bombs(self, x, y, bomb_counter):
        self.buttons[x][y].config(image=self.bomb_count_image[bomb_counter])

import random
import math


class Board:

    # Função que devolve uma lista de bombas dado um tamanho de um tabuleiro e o numero de bombas desejadas.
    @staticmethod
    def init_bombs(size, number_of_bombs):
        bomb_list = []
        bombs_placed = 0
        while bombs_placed < number_of_bombs:
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            bomb = Bomb(x, y)
            if bomb not in bomb_list:
                bomb_list.append(bomb)
                bombs_placed += 1
        return bomb_list

    # Construtor de uma Board
    def __init__(self, size, ratio, cheat_mode=False):
        self._game_over = False
        self._size = size
        self._ratio = ratio
        self._init_lists(size, ratio)
        print("Este tabuleiro tem {0} bombas.".format(self._number_of_bombs))
        self._handle_cheat(cheat_mode)

    # Calcula o numero de bombas (number_of_bombs) dado o racio, e inicializa a matriz do tabuleiro (tiles),
    # a lista de bombas (bomb_list) e a lista de bandeiras (flag_list)
    def _init_lists(self, size, ratio):
        self._tiles = [['?' for y in range(self._size)] for x in range(self._size)]
        self._number_of_bombs = math.ceil(
            min(max(int(self._size * self._size * ratio), 1), self._size * self._size - 1))
        self._bomb_list = self.init_bombs(size, self._number_of_bombs)
        self._flag_count = self._number_of_bombs
        self._flag_list = []

    # Imprime para a consola a localização de cada bomba no tabuleiro
    def _handle_cheat(self, cheat_mode):
        if cheat_mode:
            for bomb in self._bomb_list:
                print("Bomba na posição: ({0},{1})".format(str(bomb.x), str(bomb.y)))

    # Função que testa uma posição no tabuleiro
    def test_position(self, x, y, board_ui):
        if self._tiles[x][y] == '?':
            if any(bomb.x == int(x) and bomb.y == int(y) for bomb in self._bomb_list):
                self._display_bombs(x, y, board_ui)
                self._game_over = True
            else:
                self._recursive_test(x, y, board_ui)
            #  Local onde seria chamada a função para limpar bandeiras desnecessárias
            #   self._clear_flags(board_ui)

    # Função responsável por fazer display da bomba testada e de revelar as bombas escondidas
    def _display_bombs(self, x, y, board_ui):
        board_ui.display_bomb(x, y)
        for i, bomb in enumerate(self._bomb_list):
            if bomb.x == x and bomb.y == y:
                del self._bomb_list[i]
        for bomb in self._bomb_list:
            board_ui.display_mine(bomb.x, bomb.y)

    # Dadas as coordenadas de uma posição na grelha de jogo, devolve o numéro de bombas nas casas vizinhas. (0 a 8)
    def count_neighbour_bombs(self, x, y):
        bomb_counter = 0
        for i in range(max(0, x - 1), min(x + 2, self._size)):
            for j in range(max(0, y - 1), min(y + 2, self._size)):
                if not (i == x and j == y) and any(bomb.x == i and bomb.y == j for bomb in self._bomb_list):
                    # if not (i == x and j == y) and any(Bomb(i, j) == bomb for bomb in self._bomb_list):
                    bomb_counter += 1
        return bomb_counter

    # Função recursiva que progressivamente limpa o tabuleiro
    def _recursive_test(self, x, y, board_ui):
        self._tiles[x][y] = str(self.count_neighbour_bombs(int(x), int(y)))
        board_ui.display_number_of_bombs(x, y, int(self._tiles[x][y]))
        if self._tiles[x][y] == '0':
            for i in range(max(0, x - 1), min(x + 2, self._size)):
                for j in range(max(0, y - 1), min(y + 2, self._size)):
                    if self._tiles[i][j] == '?':
                        self._recursive_test(i, j, board_ui)

    # Função que coloca uma bandeira/marcador numa posição da grelha do jogo
    def flag_position(self, x, y, board_ui):
        if self._tiles[x][y] == '?':
            self._flag_list.append(Flag(x, y))
            self._tiles[x][y] = '*'
            self._flag_count -= 1
            board_ui.display_flag(x, y)

        elif self._tiles[x][y] == '*':
            for i, flag in enumerate(self._flag_list):
                if flag.x == x and flag.y == y:
                    del self._flag_list[i]
            self._tiles[x][y] = '?'
            self._flag_count += 1
            board_ui.remove_flag(x, y)

        else:
            print('Não pode colocar bandeiras nesta posição.')

    # Função que verifica se o estado atual do tabuleiro reune as condições para vitória.
    def check_winning_condition(self, board_ui):
        if self._flag_count == 0 and not any('?' in sub_list for sub_list in self._tiles):
            self._game_over = True
            board_ui.win_game()

    # Getter para o valor do tamanho do lado do tabuleiro. (_size)
    def get_size(self):
        return self._size

    # Getter para o valor do rácio das minas. (_ratio)
    def get_ratio(self):
        return self._ratio

    # Getter que devolve o numero de bandeiras restantes
    def get_flag_count(self):
        return self._flag_count

    # Getter para o valor booleano que representa se o jogo está a decorrer ou já terminou. (_game_over)
    def is_game_over(self):
        return self._game_over

    """ 
    Função que limpa bandeiras do tabuleiro que são desnecessárias, iterando por todas as bandeiras existentes
    e verificando se algum tile vizinho está exposto com um valor de '0' (significando que não há bombas na vizinhança
    """

    def _clear_flags(self, board_ui):
        changes_occurred = True
        while changes_occurred:
            changes_occurred = False
            flags_cleared = []
            for flag in self._flag_list:
                clear_flag = False
                for i in range(max(0, flag.x - 1), min(flag.x + 2, self._size)):
                    if clear_flag:
                        break
                    for j in range(max(0, flag.y - 1), min(flag.y + 2, self._size)):
                        if clear_flag:
                            break
                        if not (i == flag.x and j == flag.y) and self._tiles[i][j] == '0':
                            changes_occurred = True
                            clear_flag = True
                if clear_flag:
                    flags_cleared.append(flag)
                    self._tiles[flag.x][flag.y] = str(self.count_neighbour_bombs(flag.x, flag.y))
                    board_ui.display_number_of_bombs(flag.x, flag.y, self.count_neighbour_bombs(flag.x, flag.y))
            self._flag_list = [flag for flag in self._flag_list if flag not in flags_cleared]


"""
 Super classe que representa objectos que tenham uma posição na grelha do jogo
 Atributos:
   x - posição horizontal na grelha
   y - posição vertical na grelha
"""


class BoardObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.x == other.x and self.y == other.y


# Classe que representa bandeiras/marcadores (Sub-classe de BoardObject)
class Flag(BoardObject):
    def __init__(self, x, y):
        super(Flag, self).__init__(x, y)


# Classe que representa bombas (Sub-classe de BoardObject)
class Bomb(BoardObject):
    def __init__(self, x, y):
        super(Bomb, self).__init__(x, y)

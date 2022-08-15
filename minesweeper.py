import board
import boardui


def check_input_validity(board_size, bomb_ratio):
    return 11 > board_size > 0 and 1 > bomb_ratio > 0


if __name__ == "__main__":
    while True:
        print('Bem vindo ao Limpa-Minas!')
        size, ratio = input('Insira o tamanho do tabuleiro e o rácio de bombas. Ex.: \'9 0.12\'\n').split()
        valid = check_input_validity(int(size), float(ratio))
        while not valid:
            print(
                'Configuração de tabuleiro inválida. Tente criar um tabuleiro com tamanho entre \'1\' e \'10\' e '
                'rácio entre 0 e 1.')
            size, ratio = input('Insira o tamanho do tabuleiro e o rácio de bombas. Ex.: \'9 0.12\'\n').split()
            valid = check_input_validity(int(size), float(ratio))
        print("Criou um tabuleiro de {0}x{0} com um rácio de bombas de {1}.".format(size, ratio))
        game_board = board.Board(int(size), float(ratio))
        board_ui = boardui.BoardUI(game_board)
        board_ui.create_gui()
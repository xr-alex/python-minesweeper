import time
import winsound


class SoundManager:
    click_sound = 'Sounds\\click.wav'
    bomb_exploding_sound = 'Sounds\\wrong.wav'
    place_flag_sound = 'Sounds\\flag.wav'
    unflag_sound = 'Sounds\\unflag.wav'

    @staticmethod
    def play_click_sound():
        winsound.PlaySound(SoundManager.click_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)

    @staticmethod
    def play_bomb_exploding_sound():
        winsound.PlaySound(SoundManager.bomb_exploding_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)

    @staticmethod
    def play_place_flag_sound():
        winsound.PlaySound(SoundManager.place_flag_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)

    @staticmethod
    def play_unflag_sound():
        winsound.PlaySound(SoundManager.unflag_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)

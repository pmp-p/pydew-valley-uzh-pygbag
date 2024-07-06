import sys
#import pygbag.aio as asyncio

# /// script
# dependencies = [
#  "pygame-ce",
#  "pytmx",
# ]
# ///


try:
    import pygame
    pygame.init()
    pygame.font.init()
except:
    pygame = None

from src import settings
from src import support
from src import level
from src import main_menu

from gamestates import GameState, Loop, asyncio


class Game(GameState):
    def __init__(self):
        self.character_frames: dict[str, settings.AniFrames] | None = None
        self.level_frames: dict | None = None
        self.tmx_maps: settings.MapDict | None = None
        self.overlay_frames: dict[str, pygame.Surface] | None = None
        self.font: pygame.font.Font | None = None
        self.sounds: settings.SoundDict | None = None
        pygame.init()
        self.screen = pygame.display.set_mode((
            settings.SCREEN_WIDTH,
            settings.SCREEN_HEIGHT,
        ))
        pygame.display.set_caption('PyDew')
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_assets()
        self.running = True
        self.level = level.Level(
            self.tmx_maps,
            self.character_frames,
            self.level_frames,
            self.overlay_frames,
            self.font,
            self.sounds)

    def load_assets(self):
        self.tmx_maps = support.tmx_importer('data/maps')
        self.level_frames = {
            'animations': support.animation_importer('images', 'animations'),
            'soil': support.import_folder_dict('images/soil'),
            'soil water': support.import_folder_dict('images/soil water'),
            'tomato': support.import_folder('images/plants/tomato'),
            'corn': support.import_folder('images/plants/corn'),
            'rain drops': support.import_folder('images/rain/drops'),
            'rain floor': support.import_folder('images/rain/floor'),
            'objects': support.import_folder_dict('images/objects')
        }
        self.overlay_frames = support.import_folder_dict('images/overlay')
        self.character_frames = support.character_importer('images/characters')

        # sounds
        self.sounds = support.sound_importer('audio', default_volume=0.25)

        self.font = support.import_font(30, 'font/LycheeSoda.ttf')


    def draw(self, events):
        dt = self.clock.tick() / 1000
        for event in events:
            keys = pygame.key.get_just_pressed()
            self.screen.fill('gray')
            self.level.update(dt)
            if self.level.entities["Player"].paused:
                pause_menu = self.level.entities["Player"].pause_menu
                self.settings_menu = False
                if pause_menu.pressed_play:
                    self.level.entities["Player"].paused = (
                        not self.level.entities["Player"].paused
                    )
                    pause_menu.pressed_play = False
                elif pause_menu.pressed_quit:
                    pause_menu.pressed_quit = False
                    self.running = False
                    self.main_menu.menu = True
                    self.level.entities["Player"].paused = False
                    self.main_menu.run()
                elif pause_menu.pressed_settings:
                    self.settings_menu = (
                        self.level.entities["Player"].settings_menu
                    )
                if self.settings_menu and self.settings_menu.go_back:
                    self.settings_menu.go_back = False
                    self.settings_menu = False
                    pause_menu.pressed_settings = False
                if not self.settings_menu:
                    pause_menu.update()
                if self.settings_menu:
                    self.settings_menu.update()
            if self.settings_menu:
                if keys[pygame.K_ESCAPE]:
                    self.settings_menu = False
                    pause_menu.pressed_settings = False




class MainMenu_view(GameState):
    if pygame:
        pygame.init()

        font = support.import_font(30, 'font/LycheeSoda.ttf')
        pygame.display.set_caption('PyDew')
        clock = pygame.time.Clock()
        sounds = support.sound_importer('audio', default_volume=0.25)
        main_menu = main_menu.main_menu(font, sounds["music"])
        background = pygame.image.load("images/menu_background/bg.png")

        #pygame.mixer.music.load("music/Pytheme_Has_Feelings_Too.ogg")
        #pygame.mixer.music.play()


        pygame.display.init()

        GameState.screen = pygame.display.set_mode([1024,600])


        def __init__(self):
            self.background = pygame.transform.scale(
                self.background, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
            )
            self.main_menu.display_surface = self.screen

        def draw(self, events):
            dt = self.clock.tick() / 1000  # noqa: F841

            self.screen.blit(self.background, (0, 0))

            self.main_menu.update()

            if self.main_menu.pressed_play:
                self.sounds["music"].stop()
                self.main_menu.pressed_play = False
                Loop.instance.set_state(Game)

            elif self.main_menu.pressed_quit:
                Loop.instance.set_state(state_quit)

# logic
class MainMenu(MainMenu_view):
    pass

# special handler to call directly if not handled by a state.

async def async_quit():
    print("ASYNC QUIT")
    pygame.mixer.music.stop()


def state_quit(events):
    Loop.close()


def events_generator(*any):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            self.set_state(state_quit)
            return

    pygame.display.update()
    return events


if __name__ == '__main__':
    asyncio.run(Loop.start(MainMenu, events_generator, async_quit))


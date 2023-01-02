"""
David Cao
"""
# ============================
# MINI-PROJECT 3 - MEMORY GAME
# ============================
# The player tries to find two matching tiles by selecting tiles from
# a rectangular grid. A score will continously count up once per second
# until the player finds all the matching tiles. The player can only see
# two tiles per time, in which the tiles will flip back to hidden if
# the tiles are not matching. If the tiles are matching, the tiles will
# stay exposed.
#
# Challenges:
# - Figure out a way to have the score count up without lagging (used FPS)
# - Figure out how to stop delay once two tiles match
#
# Learned:
# - I learned more about the nested loops as well as the pygame module

import random  # used to shuffle images

import pygame


def main():
    """
    Runs the main program of the game.

    Initializes all pygame modules, sets the display window size, caption,
    creates the game object, plays the game, and quits pygame once we are
    done with it.
    """
    pygame.init()

    pygame.display.set_mode((520, 420))
    pygame.display.set_caption("Memory")

    w_surface = pygame.display.get_surface()
    game = Game(w_surface)
    game.play()

    pygame.quit()


class Game:
    """
    An object in this class represents a complete game.
    """

    def __init__(self, surface):
        """
        Initialize a game.

        Args:
        - self is the Game to initialize
        - surface is the display window surface object
        """
        # === general variables
        self.surface = surface
        self.bg_color = pygame.Color("black")
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects
        self.score = 0

        # interacting with the tiles
        self.clicked_tile = []
        self.flip_time = 0

        # board dimensions
        self.board_width = 5
        self.board_height = 4
        self.board_size = (self.board_width - 1) * self.board_height

        # save images to list
        self.hidden_image = "image0.bmp"
        self.images = []
        self.get_images()

        # create a nested list of tiles
        self.board = []
        self.create_board()

    def get_images(self):
        """
        Append the strings of images into a list --> self.images.
        """
        # a board size of 16 means that we need 8 images
        number_of_images = self.board_size // 2
        for i in range(1, number_of_images + 1):
            self.images.append("image" + str(i) + ".bmp")
        # get pairs of each image
        self.images += self.images
        random.shuffle(self.images)

    def create_board(self):
        """
        Create the board of tiles as a nested list.

        The board will not create a tile at the last column to display
        the score.
        """
        width = self.surface.get_width() // self.board_width
        height = self.surface.get_height() // self.board_height
        for row_index in range(0, self.board_height):
            row = []
            for col_index in range(0, self.board_width):
                # tile offsets
                x = col_index * width
                y = row_index * height

                # leave a blank column at last column
                if col_index != self.board_width - 1:
                    tile = Tile(
                        x,
                        y,
                        width,
                        height,
                        self.surface,
                        self.hidden_image,
                        # equation goes from 0 - 16
                        self.images[col_index + (row_index * (self.board_width - 1))],
                    )
                    row.append(tile)
            self.board.append(row)

    def play(self):
        """
        Play the game until the player presses the close box.

        Run the memory game, while handling all events, drawing shapes onto
        the pygame surface, updating the game, and deciding if you've won
        the game. The game will run at 60 frames per second.
        """
        while not self.close_clicked:
            # play frame
            self.handle_events()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second

    def handle_events(self):
        """
        Handle each user event by changing the game state appropriately.

        Args:
        - self is the Game whose events will be handled
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.MOUSEBUTTONUP and self.continue_game:
                self.handle_mouse_up(event.pos)

    def handle_mouse_up(self, position):
        """
        Handle when a user releases a mouse click.

        Goes through every tile and flips it to the exposed side if clicked
        and you've only clicked two tiles so far. This method prevents you
        from clicking and showing more than two tiles at a time.

        Args:
        - self is the Game to handle the mouse up event
        - position(tuple): the position of the mouse click up event
        """
        for row in self.board:
            for tile in row:
                # click at most 2 tiles at a time
                if tile.select(position) and (len(self.clicked_tile) < 2):
                    tile.flip_card()
                    self.add_tile(tile)

    def add_tile(self, tile):
        """
        Appends a tile to a list.

        When a tile is clicked, append that tile to a list. It also makes
        sure that the same tile is not appended twice (fixes bug which
        appends tile twice when last column is clicked)
        """
        if tile not in self.clicked_tile:
            self.clicked_tile.append(tile)

    def draw(self):
        """
        Draw all game objects.

        Draws the tiles, the scoreboard, and the end game title when
        the game ends.

        Args:
        - self is the Game to draw
        """
        # clear the display surface first
        self.surface.fill(self.bg_color)

        # draw the board
        for row in self.board:
            for tile in row:
                tile.draw()

        self.draw_score()
        if not self.continue_game:
            self.draw_end_title()

        # make the updates surface appear on the display
        pygame.display.update()

    def draw_score(self):
        """
        Draw the score of the memory game at the top right of the screen.
        - self is the Game
        """
        score_string = str(self.score)
        fg_color = pygame.Color("white")
        bg_color = pygame.Color("black")

        font = pygame.font.SysFont("", 80)
        text_box = font.render(score_string, True, fg_color, bg_color)

        x = self.surface.get_width() - text_box.get_width()
        location = (x, 0)
        self.surface.blit(text_box, location)

    def draw_end_title(self):
        """
        Draw the end title when you've completed the game.
        - self is the Game
        """
        end_string = "Success!"
        fg_color = pygame.Color("darkgreen")
        bg_color = pygame.Color("white")

        font = pygame.font.SysFont("", 100)
        text_box = font.render(end_string, True, fg_color, bg_color)

        # centers the end game title
        center_x = self.surface.get_width() // 2 - text_box.get_width() // 2
        center_y = self.surface.get_height() // 2 - text_box.get_height() // 2
        location = (center_x, center_y)
        self.surface.blit(text_box, location)

    def update(self):
        """
        Update the game objects for the next frame.
        - self is the Game to update
        """
        self.update_score()
        self.update_tiles()

    def update_score(self):
        """
        Increment score every second.
        - self is the Game
        """
        self.score = pygame.time.get_ticks() // 1000

    def update_tiles(self):
        """
        Checks to see if tiles match, and if not, flips the tile back
        to hidden.

        Args:
        - self is the Game
        """
        if len(self.clicked_tile) >= 2:
            # start check once you've clicked two tiles
            tile1 = self.clicked_tile[0]
            tile2 = self.clicked_tile[1]
            equal_tile = tile1.get_exposed_tile() == tile2.get_exposed_tile()

            # utilizing FPS
            self.flip_time += 1
            second = 60

            if equal_tile:
                # Makes sure that if you got the correct tiles, you don't
                # have to wait 0.5 seconds to find the next pair of tiles
                self.reset_tile_check()
            elif self.flip_time >= second / 2:
                # if the tile is not correct, flip back to hidden after
                # 0.5 seconds
                for tile in self.clicked_tile:
                    tile.flip_card()
                self.reset_tile_check()

    def reset_tile_check(self):
        """
        Reset the list with your clicked tiles and the exposed tile delay time.

        This function is specifically used in the update_tiles(self) method
        to reset the tile checking frames and list.
        """
        self.flip_time = 0
        self.clicked_tile.clear()

    def decide_continue(self):
        """
        Checks if every tile is exposed, and if so, ends the game.
        - self is the Game to check
        """
        end_count = 0
        for row in self.board:
            for tile in row:
                if tile.get_exposed_tile() == tile.get_tile_content():
                    end_count += 1
        if end_count == len(self.board) * len(self.board[0]):
            self.continue_game = False


class Tile:
    """
    An object in this class represents a single tile in the game.
    """

    def __init__(self, x, y, width, height, surface, hidden_tile, exposed_tile):
        """
        Initialize a game.

        Args:
        - self is the Tile to initialize
        - x(int): the left-most coordinate of the tile
        - y(int): the top-most coordinate of the tile
        - width(int): the width of the tile
        - height(int): the height of the tile
        - surface(pygame.Surface): the windows pygame.Surface object
        - hidden_tile(str): the name of the hidden tile image
        - exposed_tile(str): the name of the exposed tile image
        """
        # tile dimensions
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color("black")
        self.q_color = pygame.Color("red")
        self.border_width = 3
        self.surface = surface

        # tile content
        self.exposed_tile = exposed_tile
        self.hidden_tile = hidden_tile
        self.content = self.hidden_tile

    def select(self, position):
        """
        Determine if a position has collided with the tile or not.

        Args:
        - self is the Tile to select
        - position(tuple): the x and y coordinates of a click

        Return:
        - True if a tile is clicked and hidden
        - False if a tile is clicked and exposed
        """
        selected = False
        if self.rect.collidepoint(position):
            if self.content == self.hidden_tile:
                selected = True
        return selected

    def get_exposed_tile(self):
        """
        Get the exposed tile string name.
        - self is the Tile to get
        """
        return self.exposed_tile

    def get_tile_content(self):
        """
        Get the string of the current displayed tile image.
        - self is the Tile to get
        """
        return self.content

    def flip_card(self):
        """
        Flips the tile from exposed to hidden, or if already hidden, from
        hidden to exposed.
        - self is the Tile to flip
        """
        # flips card from exposed to hidden or vice versa
        if self.content == self.exposed_tile:
            self.content = self.hidden_tile
        else:
            self.content = self.exposed_tile

    def draw(self):
        """
        Draw the tile and it's contents onto the display surface.
        - self is the Tile to draw
        """
        pygame.draw.rect(self.surface, self.color, self.rect, self.border_width)
        self.draw_content()

    def draw_content(self):
        """
        Center and draw the tile picture onto the display surface.
        - self is the Tile to draw
        """
        # draws tile pictures onto surface
        image = pygame.image.load(self.content)

        # sets center of image to center of tile
        rect1 = image.get_rect()
        rect1.center = self.rect.center
        location = (rect1.x, rect1.y)

        self.surface.blit(image, location)


main()

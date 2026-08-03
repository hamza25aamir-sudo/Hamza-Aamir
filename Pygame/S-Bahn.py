import random  # used to pick a random arrival delay for each train
import sys  # used to cleanly exit the program (sys.exit())
import pygame  # the game engine: graphics, input, timing, etc.

pygame.init(
)  # initializes all pygame modules (must be called before using pygame)
WIDTH, HEIGHT = 922, 648  # the actual size of the game window, in pixels
screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)  # creates the game window/surface at that size
pygame.display.set_caption(
    "Catch the S-Bahn!"
)  # sets the text shown in the window's title bar
clock = (
    pygame.time.Clock()
)  # a clock object used to lock the game to a fixed frame rate
BASE_WIDTH, BASE_HEIGHT = (
    922,
    648,
)  # the "design" resolution all original pixel values were based on
SCALE_X = (
    WIDTH / BASE_WIDTH
)  # horizontal scale factor (1.0 here, since WIDTH == BASE_WIDTH)
SCALE_Y = (
    HEIGHT / BASE_HEIGHT
)  # vertical scale factor (1.0 here, since HEIGHT == BASE_HEIGHT)
PLATFORM_Y = (
    HEIGHT - int(150 * SCALE_Y)
)  # y-coordinate of the platform line, scaled from the base value
STOP_X = (
    WIDTH - int(725 * SCALE_X)
)  # x-coordinate where the train comes to a stop
PLAYER_X = int(350 * SCALE_X)  # fixed x-coordinate of the player on screen
SPEED = int(22 * SCALE_X)  # how many pixels the train moves per frame
TRAIN_WIDTH = int(
    1400 * SCALE_X
)  # width to which the train image will be scaled
TRAIN_HEIGHT = int(
    1000 * SCALE_Y
)  # height to which the train image will be scaled
TRAIN_Y_OFFSET = int(
    340 * SCALE_Y
)  # vertical offset used to position the train image correctly
PLAYER_WIDTH = int(
    450 * SCALE_X
)  # width to which the player image will be scaled
PLAYER_HEIGHT = int(
    320 * SCALE_Y
)  # height to which the player image will be scaled
PLAYER_Y_OFFSET = int(
    100 * SCALE_Y
)  # vertical offset used to position the player image correctly
PLAYER_Y = (
    PLATFORM_Y - PLAYER_HEIGHT + PLAYER_Y_OFFSET
)  # final y-coordinate where the player is drawn
TRAIN_Y = (
    PLATFORM_Y - TRAIN_HEIGHT + TRAIN_Y_OFFSET
)  # final y-coordinate where the train is drawn
bg_img = pygame.transform.scale(  # load and resize the background image...
    pygame.image.load("background.png").convert(),
    (WIDTH, HEIGHT),  # to exactly fill the window
)
player_img = pygame.transform.scale(  # load and resize the player sprite...
    pygame.image.load("human.png").convert_alpha(),  # ...convert_alpha() keeps transparency
    (PLAYER_WIDTH, PLAYER_HEIGHT),  # to the computed player dimensions
)
train_closed_img = pygame.transform.scale(  # load and resize the train-with-closed-doors sprite...
    pygame.image.load("sbahn.png").convert_alpha(),
    (TRAIN_WIDTH, TRAIN_HEIGHT),  # to the computed train dimensions
)
train_open_img = pygame.transform.scale(  # load and resize the train-with-open-doors sprite...
    pygame.image.load("sbahn_open.png").convert_alpha(),
    (TRAIN_WIDTH, TRAIN_HEIGHT),  # to the same computed train dimensions
)


class Player:  # represents the player character and its jump animation

  def __init__(self):
    self.jump_frames = (
        0  # counts down the remaining frames of an in-progress jump
    )

  def jump(self):
    self.jump_frames = 15  # starts a new jump lasting 15 frames

  def update(self):
    self.jump_frames = max(
        0, self.jump_frames - 1
    )  # decreases the jump counter each frame, never below 0

  def draw(self):
    screen.blit(
        player_img, (PLAYER_X, PLAYER_Y - self.jump_frames // 2)
    )  # draws player, moved up while jumping


class Timer:  # a simple reusable frame-based countdown timer

  def __init__(self, duration):
    self.reset(
        duration
    )  # initializes the timer by calling reset with the starting duration

  def reset(self, duration):
    self.frames_left = (
        duration  # sets (or resets) how many frames remain on the timer
    )

  def tick(self):
    if self.frames_left > 0:  # only count down if time remains
      self.frames_left -= 1  # decrease the remaining frames by one

  def is_done(self):
    return (
        self.frames_left <= 0
    )  # returns True once the countdown has reached zero

  def seconds_left(self):
    return (
        self.frames_left + 29
    ) // 30  # converts remaining frames to whole seconds, rounding up


class Train:  # represents the S-Bahn train and its arrival/boarding/departure logic

  def __init__(self, open_time):
    self.wait_timer = Timer(
        90
    )  # creates a timer (arrival countdown), placeholder duration of 90 frames
    self.reset(
        open_time
    )  # immediately configures the train for its first arrival cycle

  def reset(self, open_time, wait_time=None):
    if wait_time is None:  # if no wait_time was explicitly given
      wait_time = (
          random.randint(1, 8) * 30
      )  # pick a random arrival delay between 1-8 seconds (30 FPS)
    self.x = WIDTH + 50  # positions the train just off-screen to the right
    self.stopped = (
        False  # marks that the train has not yet come to a stop at the platform
    )
    self.door_timer = (
        open_time  # how many frames the doors stay open once stopped
    )
    self.wait_timer.reset(
        wait_time
    )  # resets the arrival countdown to the new wait_time

  def update(self):
    if not self.wait_timer.is_done():  # while still waiting to arrive...
      self.wait_timer.tick()  # count down the arrival timer
    elif not self.stopped:  # once the wait is over, but train hasn't stopped yet...
      self.x = max(
          STOP_X, self.x - SPEED
      )  # ...move it left toward the stop position, without overshooting
      self.stopped = (
          self.x == STOP_X
      )  # mark as stopped once it has reached the stop position exactly
    else:  # once stopped at the platform
      self.door_timer -= 1  # count down the time the doors remain open
      if self.door_timer <= 0:  # once the door timer expires...
        self.x -= SPEED  # ...the train starts moving left again (departing)

  def is_boardable(self):
    return (
        self.stopped and self.door_timer > 0
    )  # train can be boarded only while stopped with doors still open

  def seconds_until_arrival(self):
    return (
        self.wait_timer.seconds_left()
    )  # returns how many whole seconds remain until the train arrives

  def draw(self):
    current_img = (
        train_open_img if self.is_boardable() else train_closed_img
    )  # pick sprite based on door state
    screen.blit(
        current_img, (self.x, TRAIN_Y)
    )  # draw the chosen train image at its current position


class ScoreKeeper:  # tracks the player's score and whether the game has ended

  def __init__(self):
    self.caught = (
        0  # number of trains successfully boarded so far
    )
    self.game_over = (
        False  # flag indicating whether the game has ended
    )

  def add_catch(self):
    self.caught += 1  # increments the score by one successful catch

  def trigger_game_over(self):
    self.game_over = True  # marks the game as over


class GameManager:  # orchestrates the overall game input, updates, drawing, and the main loop

  def __init__(self):
    self.player = Player()  # creates the player object
    self.score = ScoreKeeper()  # creates the score/game-over tracker
    self.train = Train(
        open_time=60
    )  # creates the train, with doors initially staying open for 60 frames
    self.font = pygame.font.SysFont(
        "Arial", int(40 * SCALE_Y)
    )  # font used for the big score/game-over text
    self.timer_font = pygame.font.SysFont(
        "Arial", int(18 * SCALE_Y)
    )  # smaller font used for the arrival countdown

  def update(self, space_pressed):
    self.player.update()  # advances the player's jump animation by one frame
    self.train.update()  # advances the train's arrival/stop/departure state by one frame

    if (
        space_pressed and self.train.is_boardable()
    ):  # if the player pressed space while doors were open
      self.score.add_catch()  # award a point
      self.player.jump()  # trigger the jump animation
      self.train.reset(
          max(20, 60 - self.score.caught * 5)
      )  # and reset the train with a shorter open time (min 20)
    elif (
        self.train.x < -TRAIN_WIDTH
    ):  # otherwise, if the train has fully left the screen unboarded
      self.score.trigger_game_over()  #end the game

  def draw_hud(self):
    text = self.font.render(
        f"Caught: {self.score.caught}", True, (255, 255, 255)
    )  # render the "Caught N" score text in white
    screen.blit(
        text, (WIDTH - text.get_width() - 675, 550)
    )  # draw the score text at a fixed screen position

    seconds_left = (
        self.train.seconds_until_arrival()
    )  # get the whole seconds remaining until the train arrives
    if seconds_left > 0:  # only show the countdown while time remains
      timer_text = self.timer_font.render(
          str(seconds_left), True, (255, 255, 255)
      )  # render the countdown number... in white
      sign_center_x = int(
          130 * SCALE_X
      )  # x-coordinate of the center of the station sign
      sign_center_y = int(
          170 * SCALE_Y
      )  # y-coordinate of the center of the station sign
      screen.blit(
          timer_text,
          (
              sign_center_x
              - timer_text.get_width() // 2,  # center the text horizontally on the sign
              sign_center_y
              - timer_text.get_height() // 2,  # center the text vertically on the sign
          ),
      )

  def run(self):
    while not self.score.game_over:  # main game loop, runs until the game ends
      clock.tick(30)  # cap the loop at 30 frames per second
      space_pressed = (
          False  # reset the "space was pressed this frame" flag
      )
      for event in pygame.event.get():  # process all pending input/window events
        if event.type == pygame.QUIT:  # if the player closes the window...
          pygame.quit()  # shut down pygame
          sys.exit()  # and exit the program
        elif (
            event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
        ):  # if the spacebar was pressed
          space_pressed = (
              True  # remember that for this frame's update
          )

      self.update(space_pressed)  # update all game logic for this frame
      screen.blit(bg_img, (0, 0))  # draw the background first, filling the screen
      self.train.draw()  # draw the train on top of the background
      self.player.draw()  # draw the player on top of the background
      self.draw_hud()  # draw the score and countdown text on top of everything
      pygame.display.flip()  # push the newly drawn frame to the actual display

    screen.fill((0, 0, 0))  # once the game is over, clear the screen to black
    text = self.font.render(  # render the game-over message with the final score
        f"GAME OVER - Trains Caught: {self.score.caught}",
        True,
        (255, 255, 255),  # in white
    )
    screen.blit(
        text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2)
    )  # center the message on screen
    pygame.display.flip()  # display the game-over screen
    pygame.time.wait(
        2500
    )  # pause for 2.5 seconds so the player can read the message
    pygame.quit()  # shut down pygame
    sys.exit()  # exit the program


if __name__ == "__main__":  # only run the game if this file is executed directly (not imported)
  GameManager().run()  # create a GameManager and start the main game loop
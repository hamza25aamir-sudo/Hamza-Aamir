import random
import sys
import pygame

pygame.init()
WIDTH, HEIGHT = 922, 648
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the S-Bahn!")
clock = pygame.time.Clock()

BASE_WIDTH, BASE_HEIGHT = 922, 648
SCALE_X = WIDTH / BASE_WIDTH
SCALE_Y = HEIGHT / BASE_HEIGHT

PLATFORM_Y = HEIGHT - int(150 * SCALE_Y)
STOP_X = WIDTH - int(725 * SCALE_X)
PLAYER_X = int(350 * SCALE_X)
SPEED = int(22 * SCALE_X)

TRAIN_WIDTH = int(1400 * SCALE_X)
TRAIN_HEIGHT = int(1000 * SCALE_Y)
TRAIN_Y_OFFSET = int(340 * SCALE_Y)

PLAYER_WIDTH = int(450 * SCALE_X)
PLAYER_HEIGHT = int(320 * SCALE_Y)
PLAYER_Y_OFFSET = int(100 * SCALE_Y)

PLAYER_Y = PLATFORM_Y - PLAYER_HEIGHT + PLAYER_Y_OFFSET
TRAIN_Y = PLATFORM_Y - TRAIN_HEIGHT + TRAIN_Y_OFFSET

bg_img = pygame.transform.scale(
    pygame.image.load("background.png").convert(), (WIDTH, HEIGHT)
)
player_img = pygame.transform.scale(
    pygame.image.load("human.png").convert_alpha(),
    (PLAYER_WIDTH, PLAYER_HEIGHT),
)
train_closed_img = pygame.transform.scale(
    pygame.image.load("sbahn.png").convert_alpha(),
    (TRAIN_WIDTH, TRAIN_HEIGHT),
)
train_open_img = pygame.transform.scale(
    pygame.image.load("sbahn_open.png").convert_alpha(),
    (TRAIN_WIDTH, TRAIN_HEIGHT),
)


class Player:

  def __init__(self):
    self.jump_frames = 0

  def jump(self):
    self.jump_frames = 15

  def update(self):
    self.jump_frames = max(0, self.jump_frames - 1)

  def draw(self):
    screen.blit(player_img, (PLAYER_X, PLAYER_Y - self.jump_frames // 2))


class Timer:

  def __init__(self, duration):
    self.reset(duration)

  def reset(self, duration):
    self.frames_left = duration

  def tick(self):
    if self.frames_left > 0:
      self.frames_left -= 1

  def is_done(self):
    return self.frames_left <= 0

  def seconds_left(self):
    return (self.frames_left + 29) // 30


class Train:

  def __init__(self, open_time):
    self.wait_timer = Timer(90)
    self.reset(open_time)

  def reset(self, open_time, wait_time=None):
    if wait_time is None:
      wait_time = random.randint(1, 8) * 30
    self.x = WIDTH + 50
    self.stopped = False
    self.door_timer = open_time
    self.wait_timer.reset(wait_time)

  def update(self):
    if not self.wait_timer.is_done():
      self.wait_timer.tick()
    elif not self.stopped:
      self.x = max(STOP_X, self.x - SPEED)
      self.stopped = self.x == STOP_X
    else:
      self.door_timer -= 1
      if self.door_timer <= 0:
        self.x -= SPEED

  def is_boardable(self):
    return self.stopped and self.door_timer > 0

  def seconds_until_arrival(self):
    return self.wait_timer.seconds_left()

  def draw(self):
    current_img = train_open_img if self.is_boardable() else train_closed_img
    screen.blit(current_img, (self.x, TRAIN_Y))


class ScoreKeeper:

  def __init__(self):
    self.caught = 0
    self.game_over = False

  def add_catch(self):
    self.caught += 1

  def trigger_game_over(self):
    self.game_over = True


class GameManager:

  def __init__(self):
    self.player = Player()
    self.score = ScoreKeeper()
    self.train = Train(open_time=60)
    self.font = pygame.font.SysFont("Arial", int(40 * SCALE_Y))
    self.timer_font = pygame.font.SysFont("Arial", int(18 * SCALE_Y))

  def update(self, space_pressed):
    self.player.update()
    self.train.update()

    if space_pressed and self.train.is_boardable():
      self.score.add_catch()
      self.player.jump()
      self.train.reset(max(20, 60 - self.score.caught * 5))
    elif self.train.x < -TRAIN_WIDTH:
      self.score.trigger_game_over()

  def draw_hud(self):
    text = self.font.render(
        f"Caught: {self.score.caught}", True, (255, 255, 255)
    )
    screen.blit(text, (WIDTH - text.get_width() - 675, 550))

    seconds_left = self.train.seconds_until_arrival()
    if seconds_left > 0:
      timer_text = self.timer_font.render(
          str(seconds_left), True, (255, 255, 255)
      )
      sign_center_x = int(130 * SCALE_X)
      sign_center_y = int(170 * SCALE_Y)
      screen.blit(
          timer_text,
          (
              sign_center_x - timer_text.get_width() // 2,
              sign_center_y - timer_text.get_height() // 2,
          ),
      )

  def run(self):
    while not self.score.game_over:
      clock.tick(30)
      space_pressed = False
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
          space_pressed = True

      self.update(space_pressed)
      screen.blit(bg_img, (0, 0))
      self.train.draw()
      self.player.draw()
      self.draw_hud()
      pygame.display.flip()

    screen.fill((0, 0, 0))
    text = self.font.render(
        f"GAME OVER - Trains Caught: {self.score.caught}",
        True,
        (255, 255, 255),
    )
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2500)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
  GameManager().run()
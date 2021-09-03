from pygame import (
    init,
    sprite,
    image,
    display,
    event,
    time,
    transform,
    key,
    USEREVENT,
    mouse,
    mixer,
    font,
    K_SPACE,
    QUIT,
)
from random import randint

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 400
GRAVITY = 1
GRAVITY_INCREMENT = 0.4
OBSTACLE_RANGE = ...
ANGLE = 0
COLOR = (0, 0, 0)
obstacle_list = []


def collision_sprite() -> bool:
    if sprite.spritecollide(bird.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


class Bird(sprite.Sprite):
    def __init__(self, *groups: sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        img1 = image.load("assets/yellowbird-upflap.png").convert_alpha()
        img2 = image.load("assets/yellowbird-midflap.png").convert_alpha()
        img3 = image.load("assets/yellowbird-downflap.png").convert_alpha()
        self.images = [img1, img2, img3]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(100, 260))
        self.angle = ANGLE
        self.gravity = GRAVITY
        self.angle = 0

    def animate(self) -> None:
        self.index += 0.2
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[int(self.index)]

    def rotate(self) -> None:
        self.image = transform.rotate(self.image, self.angle)

    def apply_gravity(self) -> None:
        self.rect.y += self.gravity

    def player_input(self) -> None:
        keys = key.get_pressed()
        if keys[K_SPACE]:
            self.angle += 2
            self.gravity -= GRAVITY_INCREMENT
        else:
            self.angle -= 2
            self.gravity += GRAVITY_INCREMENT

    def check_pos(self) -> bool:
        if self.rect.y < -40:
            return False
        if self.rect.y > 550 + 5:
            return False
        return True

    def update(self) -> None:
        self.apply_gravity()
        self.player_input()
        self.animate()
        self.rotate()

class Obstacle(sprite.Sprite):
    def __init__(self, type, number, *groups: sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        pipe1 = image.load("assets/pipe-green.png").convert_alpha()
        pipe2 = transform.rotate(pipe1, 180)
        self.distance = 400
        self.pipe = [pipe1, pipe2]
        self.height = 0
        if type == "upper":
            self.height = number
            self.image = self.pipe[1]
            self.rect = self.image.get_rect(center=(self.distance, self.height))
            screen.blit(self.image, self.rect)
        if type == "lower":
            self.image = self.pipe[0]
            self.height = number
            self.rect = self.image.get_rect(center=(self.distance, self.height))

    def destroy(self) -> None:
        if self.rect.x <= -50:
            self.kill()

    def update(self) -> None:
        self.rect.x -= 6
        self.destroy()


class GameStuff:
    def __init__(self) -> None:
        self.background_image = image.load("assets/background-day.png").convert_alpha()
        self.background = transform.scale(
            self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.background_rect = self.background.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        )
        self.score = 0
        self.initial_state = True
        self.collide_music = mixer.Sound("audio/sfx_hit.wav")
        self.fall_music = mixer.Sound("audio/sfx_swooshing.wav")
        self.dead_music = mixer.Sound("audio/sfx_die.wav")
        self.score_music = mixer.Sound("audio/sfx_point.wav")
        self.initial_image = image.load("assets/message.png").convert_alpha()
        self.initial_image = transform.scale(
            self.initial_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.initial_image_rect = self.initial_image.get_rect(
            center=(SCREEN_WIDTH / 2, 100)
        )
        self.foreground_image = image.load("assets/base.png").convert_alpha()
        self.foreground_image = transform.scale(
            self.foreground_image, (SCREEN_WIDTH, 150)
        )
        self.foreground_image_rect = self.foreground_image.get_rect(
            midtop=(SCREEN_WIDTH / 2, 550)
        )
        self.game_over_image = image.load("assets/gameover.png").convert_alpha()
        self.game_over_rect = self.game_over_image.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        )

    def check_game(self) -> None:
        for game_event in event.get():
            if game_event.type == QUIT:
                quit()
                exit()

    def initial_game(self) -> None:
        while True:
            self.check_game()
            screen.blit(self.background, self.background_rect)
            screen.blit(self.initial_image, self.initial_image_rect)
            display.update()
            if mouse.get_pressed()[0]:
                break

    def post_game(self) -> None:
        while True:
            self.check_game()
            display.update()

    def show(self) -> None:
        screen.blit(self.background, self.background_rect)

    def display_score(self) -> None:
        font_surf = score_font.render(str(self.score), True, (255, 255, 255))
        score_rect = font_surf.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(font_surf, score_rect)

    def display_foreground(self) -> None:
        screen.blit(self.foreground_image, self.foreground_image_rect)

    def check_score(self) -> None:
        with open("score.txt", "r") as f:
            self.high_score = f.readline()
            if self.score > int(self.high_score):
                self.high_score = self.score
                self.write_score()

    def write_score(self) -> None:
        with open("score.txt", "w") as f:
            f.write(str(self.score))

    def post_game(self) -> None:
        print("post game phase")
        high_score_font = score_font.render("High Score", True, COLOR)
        high_score_rect = high_score_font.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 200)
        )
        high_font_surf = score_font.render(str(self.high_score), True, COLOR)
        high_font_rect = high_font_surf.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150)
        )

        current_score_font = score_font.render("Current Score", True, COLOR)
        current_score_font_rect = current_score_font.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100)
        )
        current_score_surf = score_font.render(str(self.score), True, COLOR)
        current_score_rect = current_score_surf.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
        )
        while True:
            self.check_game()
            screen.blit(self.game_over_image, self.game_over_rect)
            screen.blit(high_score_font, high_score_rect)
            screen.blit(high_font_surf, high_font_rect)
            screen.blit(current_score_surf, current_score_rect)
            screen.blit(current_score_font, current_score_font_rect)
            self.score = 0
            display.update()

    def start_game(self) -> None:
        self.initial_game()
        while True:
            for game_event in event.get():
                if game_event.type == QUIT:
                    quit()
                    exit()

                if game_event.type == obstacle_timer:
                    pipe_pos = randint(-100, 100)
                    obstacle_group.add(Obstacle("upper", pipe_pos))
                    obstacle_group.add(Obstacle("lower", pipe_pos + 500))
                    print(self.score)
                    self.score += 1

            flappy_bird.show()
            if collision_sprite():
                if bird_sprite.check_pos():

                    bird.draw(screen)
                    bird.update()

                    obstacle_group.draw(screen)
                    obstacle_group.update()
                else:
                    self.fall_music.play()
                    self.check_score()
                    self.post_game()
            else:
                self.collide_music.play()
                self.check_score()
                self.post_game()

            self.display_score()
            self.display_foreground()

            display.update()
            clock.tick(60)


init()
screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = time.Clock()
display.set_caption("Flappy Bird")
score_font = font.Font("fonts/04B_19.TTF", 40)

flappy_bird = GameStuff()

bird_sprite = Bird()
bird = sprite.GroupSingle()

bird.add(bird_sprite)

obstacle_group = sprite.Group()

obstacle_timer = USEREVENT + 1
time.set_timer(obstacle_timer, 1000)

flappy_bird.start_game()

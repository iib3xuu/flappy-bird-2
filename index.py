import pygame
import random
import os

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 68
BIRD_HEIGHT = 48
PIPE_WIDTH = 52
PIPE_GAP = 150
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = 3
FLAP_COOLDOWN = 200

bird_image = pygame.image.load('bird.png')  
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
pipe_image = pygame.image.load('pipe.jpg')  
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, SCREEN_HEIGHT))
background_image = pygame.image.load('background.jpg')  
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

flap_sound = pygame.mixer.Sound('flap.mp3')  
score_sound = pygame.mixer.Sound('score.mp3')  
game_over_sound = pygame.mixer.Sound('game_over.mp3')  
pygame.mixer.music.load('background_music.mp3')  
pygame.mixer.music.play(-1)  

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.last_flap_time = 0
        self.flap_count = 0

    def flap(self, current_time):
        if current_time - self.last_flap_time > FLAP_COOLDOWN:
            self.velocity = FLAP_STRENGTH
            self.last_flap_time = current_time
            flap_sound.play()  
            self.flap_count += 1

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, screen):

        if self.flap_count % 2 == 0:
            screen.blit(bird_image, (self.x, self.y))
        else:
            screen.blit(pygame.transform.flip(bird_image, False, True), (self.x, self.y))

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 400)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):

        screen.blit(pipe_image, (self.x, self.height - pipe_image.get_height()))

        screen.blit(pipe_image, (self.x, self.height + PIPE_GAP))

def display_game_over(screen, score, high_score):
    font = pygame.font.Font(None, 48)
    game_over_text = font.render('Game Over!', True, (255, 0, 0))
    play_again_text = font.render('Press SPACE to Play Again', True, (255, 255, 255))
    score_text = font.render(f'Your Score: {score}', True, (255, 255, 255))
    high_score_text = font.render(f'High Score: {high_score}', True, (255, 255, 0))

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 +  100))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    running = True
    high_score = 0

    while running:
        player_bird = Bird()
        pipes = [Pipe()]
        score = 0
        game_over = False

        while not game_over:
            screen.blit(background_image, (0, 0))  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player_bird.flap(pygame.time.get_ticks())

            player_bird.update()

            if pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe())

            for pipe in pipes:
                pipe.update()
                pipe.draw(screen)

                if (player_bird.x + BIRD_WIDTH > pipe.x and player_bird.x < pipe.x + PIPE_WIDTH):
                    if (player_bird.y < pipe.height or player_bird.y + BIRD_HEIGHT > pipe.height + PIPE_GAP):
                        game_over_sound.play()  
                        game_over = True

                if not pipe.passed and pipe.x < player_bird.x:
                    pipe.passed = True
                    score += 1
                    score_sound.play()  

            player_bird.draw(screen)

            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {score}', True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)

        if score > high_score:
            high_score = score

        while game_over:
            screen.blit(background_image, (0, 0))  
            display_game_over(screen, score, high_score)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_over = False  

    pygame.quit()

if __name__ == "__main__":
    main()
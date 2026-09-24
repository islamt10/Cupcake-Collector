import pygame
import asyncio

pygame.init()


WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cupcake Collector")
clock = pygame.time.Clock()
score_font = pygame.font.Font(None, 35)


player_x = 50
player_y = 300
player_rect = pygame.Rect(50, 300, 50, 50)
player_dy = 0
player_dx = 0
player_speed = 6
gravity = 0.5
jump_speed = -10
on_ground = True

score = 0

platforms = [
    pygame.Rect(0, 350, 600, 50),
    pygame.Rect(100, 270, 150, 20),
    pygame.Rect(350, 220, 150, 20),
    pygame.Rect(0, 720-50, 1920, 50),
    pygame.Rect(600, 150, 190, 30),
    pygame.Rect(1100, 580, 150, 20),
]

obstacles = [
    pygame.Rect(200, 650, 60, 20),
    pygame.Rect(400, 650, 60, 20),
    pygame.Rect(1150, 560, 60, 20)
]

cupcakes = [
    pygame.Rect(150, 230, 30, 30),
    pygame.Rect(400, 180, 30, 30),
    pygame.Rect(520, 310, 30, 30),
    pygame.Rect(670, 30, 30, 30),
    pygame.Rect(30, 620, 30,30),
    pygame.Rect(1170, 620, 30,30),
    pygame.Rect(1170, 500, 30,30)
]

async def main():
    global player_dy, on_ground, score

    player_image = pygame.image.load("assets/player.png").convert_alpha()
    player_image = pygame.transform.scale(player_image, (50, 50))
    carrot_image = pygame.image.load("assets/carrot.png").convert_alpha()
    cupcake_image = pygame.transform.scale(carrot_image, (30, 30))
    background_image = pygame.image.load("assets/background.png").convert_alpha()
    background_image = pygame.transform.scale(background_image, (1280, 720))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background_image, (0,0))
        keys = pygame.key.get_pressed()

        player_dx = 0

        if keys[pygame.K_LEFT]:
            player_dx = -player_speed

        if keys[pygame.K_RIGHT]:
            player_dx = player_speed

        previous_left = player_rect.left
        previous_right = player_rect.right
        player_rect.x += player_dx
        if player_rect.left < 0: player_rect.left = 0
        if player_rect.right > WIDTH: player_rect.right = WIDTH

        if keys[pygame.K_UP] and on_ground:
            player_dy = jump_speed
            on_ground = False

        player_dy += gravity
        previous_top = player_rect.top
        previous_bottom = player_rect.bottom
        player_rect.y += player_dy

        if player_rect.bottom >= HEIGHT:
            player_rect.bottom = HEIGHT
            player_dy = 0
            on_ground = True

        for platform in platforms:
            pygame.draw.rect(screen, (95, 145, 105), platform)

        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_dx > 0 and previous_right <= platform.left:
                    player_rect.right = platform.left
                elif player_dx < 0 and previous_left >= platform.right:
                    player_rect.left = platform.right
                elif player_dy > 0 and previous_bottom <= platform.top:  # Falling down
                    player_rect.bottom = platform.top
                    player_dy = 0
                    on_ground = True
                elif player_dy < 0 and previous_top >= platform.bottom:  # Jumping up
                    player_rect.top = platform.bottom
                    player_dy = 0

        for obstacle in obstacles:
            pygame.draw.rect(screen, (170, 65, 65), obstacle)
            if player_rect.colliderect(obstacle):
                player_rect.topleft = (player_x, player_y)
                player_dx = 0
                player_dy = 0
                on_ground = True

        for cupcake in cupcakes[:]:
            if player_rect.colliderect(cupcake):
                cupcakes.remove(cupcake)
                score += 1

        for cupcake in cupcakes:
            screen.blit(
                cupcake_image,
                (cupcake.x, cupcake.y)
            )

        screen.blit(player_image, player_rect)

        score_surface = score_font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_surface, (10, 10))
        pygame.display.flip()
        await asyncio.sleep(0)
    
    pygame.quit()

asyncio.run(main())
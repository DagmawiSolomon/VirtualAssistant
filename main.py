import pygame

# Initialize Pygame
pygame.init()


BLUE = (0, 120, 225)
LIGHT_BLUE = (13, 67, 95)
BACKGROUND = (23, 23, 23)

radius1 = 150
min_radius1 = 130
max_radius1 = 170

radius2 = 80
min_radius2 = 30
max_radius2 = 100

animation_speed = 2
fade_speed = 5

window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
pygame.display.set_caption("Simple Pygame Window")

def draw_circle(radius, color):
    window.fill(BACKGROUND)

    pygame.draw.circle(window, color,[window_width//2, window_height//2], radius1, 0)
    pygame.display.update()


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for radius1 in range(min_radius1, max_radius1, 1):
        if radius1 == max_radius1 - 1:
            draw_circle(radius1, LIGHT_BLUE)
            pygame.time.delay(60)
        else:
            draw_circle(radius1, LIGHT_BLUE)
            pygame.time.delay(60)

    window.fill(BACKGROUND)

    #pygame.draw.circle(window, LIGHT_BLUE,[window_width//2, window_height//2], 145, 0)
    #pygame.draw.circle(window, BLUE,[window_width//2, window_height//2], 100, 0)
    #pygame.draw.circle(window, BACKGROUND,[window_width//2, window_height//2], 75, 0)
    
    
    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()

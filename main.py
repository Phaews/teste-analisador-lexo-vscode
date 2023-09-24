import pygame
import sys

# Inicializar o pygame
pygame.init()

# Configurações da tela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Exercício Python")

# Definir cores
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
green = (0, 255, 0)
green_fill = (0, 128, 0)  # Verde para o fundo do círculo
pink = (255, 105, 180)
black = (0, 0, 0)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpar a tela
    screen.fill((255, 255, 255))

    # Criar um retângulo vermelho
    pygame.draw.rect(screen, red, pygame.Rect(100, 100, 300, 200), 2)

    # Criar um quadrado azul
    pygame.draw.rect(screen, blue, pygame.Rect(100, 500, 80, 80))

    # Criar um círculo com borda amarela e fundo verde
    pygame.draw.circle(screen, green_fill, (545, 95), 45, 0)
    pygame.draw.circle(screen, yellow, (545, 95), 45, 2)  


    # Desenhar texto em rosa
    font = pygame.font.Font(None, 36)
    text = font.render("Nova UniPinhal, Como você sempre quis!", True, pink)
    screen.blit(text, (150, 150))

    # Criar uma linha horizontal preta
    pygame.draw.line(screen, black, (20, 20), (220, 20), 2)

    # Atualizar a tela
    pygame.display.flip()

# Encerrar o pygame
pygame.quit()
sys.exit()

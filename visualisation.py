import pygame
from environment import Env
from behavior import Animal

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyForager")

# Kolory
white = (255, 255, 255)
black = (0, 0, 0)

# Wczytanie obrazów
animal_image = pygame.image.load('deer.png')
food_image = pygame.image.load('food.png')
food_image = pygame.transform.scale(food_image, (50, 50))

# Pozycje stref
zone_positions = {
    'A1': (100, 100),
    'A2': (300, 100),
    'A3': (500, 100),
    'B1': (100, 300),
    'B2': (300, 300),
    'B3': (500, 300)
}

# Inicjalizacja środowiska i zwierzęcia
env = Env()
animal = Animal(env)

# Ustaw początkową strefę zwierzęcia, jeśli jest niezdefiniowana
if animal.current_zone is None:
    animal.current_zone = 'A1'  # Możesz ustawić domyślną strefę na dowolną z dostępnych

# Ustawienia animacji
animal_x, animal_y = zone_positions[animal.current_zone]
speed = 7  # Prędkość przemieszczania się zwierzęcia

def move_towards(current_pos, target_pos, speed):
    current_x, current_y = current_pos
    target_x, target_y = target_pos
    
    direction_x = target_x - current_x
    direction_y = target_y - current_y
    
    distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
    
    if distance != 0:
        direction_x /= distance
        direction_y /= distance
    
    new_x = current_x + direction_x * speed
    new_y = current_y + direction_y * speed
    
    if abs(new_x - target_x) < speed:
        new_x = target_x
    if abs(new_y - target_y) < speed:
        new_y = target_y
    
    return new_x, new_y

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Wygeneruj jedzenie w strefach
    env.generate_food()

    # Zapisz pozycję docelową przed ruchem zwierzęcia
    target_position = zone_positions[animal.current_zone]
    
    # Porusz zwierzę
    animal.move()
    animal.learn()

    # Ustaw nową pozycję docelową po ruchu zwierzęcia
    new_target_position = zone_positions[animal.current_zone]

    # Płynne przemieszczanie zwierzęcia do nowej pozycji
    while (animal_x, animal_y) != new_target_position:
        animal_x, animal_y = move_towards((animal_x, animal_y), new_target_position, speed)

        # Rysowanie tła
        screen.fill(white)

        # Rysowanie stref i jedzenia
        for zone_id, position in zone_positions.items():
            zone = next(z for z in env.get_zones() if z['id'] == zone_id)
            if zone['food'] > 0:
                screen.blit(food_image, position)

        # Rysowanie zwierzęcia
        screen.blit(animal_image, (animal_x, animal_y))

        # Wyświetlanie współczynnika eksploracji na ekranie
        font = pygame.font.SysFont(None, 26)
        exploration_text = font.render(f'Exploration Rate: {animal.exploration_rate:.3f}', True, black)
        screen.blit(exploration_text, (10, 10))
        
        current_zone_text = font.render(f'Current Zone: {animal.current_zone}', True, black)
        screen.blit(current_zone_text, (10, 40))
        

        # Wyświetlanie na ekranie
        pygame.display.update()

        # Dodanie opóźnienia do symulacji
        pygame.time.delay(20)

    # Zwiększenie liczby iteracji
    animal.iteration += 1

# Zakończenie Pygame
pygame.quit()

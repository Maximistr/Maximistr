"""Raycasting 3D Game Engine - pygame"""
import pygame, math, sys, random
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
FPS = 60
FOV = math.pi / 3
NUM_RAYS = 120
MAX_RAY_DISTANCE = 30

# Map (10x10)
GAME_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

MAP_WIDTH = len(GAME_MAP[0])
MAP_HEIGHT = len(GAME_MAP)
player = {'x': 4.5, 'y': 4.5, 'angle': 0, 'speed': 0.1, 'rotSpeed': 0.05}

def generate_coins(num_coins=5):
    """Generate random coin positions that don't spawn in walls"""
    new_coins = []
    attempts = 0
    max_attempts = 1000
    
    while len(new_coins) < num_coins and attempts < max_attempts:
        x = random.uniform(1.5, MAP_WIDTH - 1.5)
        y = random.uniform(1.5, MAP_HEIGHT - 1.5)
        
        # Check if position is walkable
        r = 0.3
        walkable = True
        for dx in [-r, 0, r]:
            for dy in [-r, 0, r]:
                if GAME_MAP[int(y + dy)][int(x + dx)] == 1:
                    walkable = False
                    break
            if not walkable:
                break
        
        if walkable:
            new_coins.append((x, y))
        
        attempts += 1
    
    return new_coins

# Coins and score
coins = generate_coins(5)
score = 0


def cast_ray(x, y, angle):
    """Cast a ray and return distance and wall type"""
    sin_a, cos_a = math.sin(angle), math.cos(angle)
    distance = 0.01
    
    while distance < MAX_RAY_DISTANCE:
        check_x = x + distance * cos_a
        check_y = y + distance * sin_a
        grid_x, grid_y = int(check_x), int(check_y)
        
        if grid_x < 0 or grid_x >= MAP_WIDTH or grid_y < 0 or grid_y >= MAP_HEIGHT:
            break
        if GAME_MAP[grid_y][grid_x] == 1:
            wall_type = 'v' if (check_x - grid_x) < 0.5 else 'h'
            return (distance, wall_type)
        distance += 0.01
    
    return (MAX_RAY_DISTANCE, 'v')


def is_walkable(x, y):
    """Check if position is walkable"""
    r = 0.15
    if x - r < 0 or x + r >= MAP_WIDTH or y - r < 0 or y + r >= MAP_HEIGHT:
        return False
    for dx in [-r, 0, r]:
        for dy in [-r, 0, r]:
            if GAME_MAP[int(y + dy)][int(x + dx)] == 1:
                return False
    return True


def update_player(keys):
    """Update player position and rotation"""
    global score
    new_x, new_y = player['x'], player['y']
    
    if keys[pygame.K_w]:
        new_x += math.cos(player['angle']) * player['speed']
        new_y += math.sin(player['angle']) * player['speed']
    if keys[pygame.K_s]:
        new_x -= math.cos(player['angle']) * player['speed']
        new_y -= math.sin(player['angle']) * player['speed']
    if keys[pygame.K_a]:
        new_x += math.cos(player['angle'] - math.pi/2) * player['speed']
        new_y += math.sin(player['angle'] - math.pi/2) * player['speed']
    if keys[pygame.K_d]:
        new_x += math.cos(player['angle'] + math.pi/2) * player['speed']
        new_y += math.sin(player['angle'] + math.pi/2) * player['speed']
    
    if is_walkable(new_x, new_y):
        player['x'], player['y'] = new_x, new_y
    else:
        if is_walkable(new_x, player['y']):
            player['x'] = new_x
        if is_walkable(player['x'], new_y):
            player['y'] = new_y
    
    # Check for coin collection
    coins_to_remove = []
    for i, (cx, cy) in enumerate(coins):
        if math.sqrt((player['x'] - cx)**2 + (player['y'] - cy)**2) < 0.3:
            coins_to_remove.append(i)
            score += 10
    
    for i in reversed(coins_to_remove):
        coins.pop(i)
    
    if keys[pygame.K_LEFT]:
        player['angle'] -= player['rotSpeed']
    if keys[pygame.K_RIGHT]:
        player['angle'] += player['rotSpeed']


def render(screen):
    """Render 3D view and minimap"""
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (30, 30, 30), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    pygame.draw.rect(screen, (50, 50, 50), (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    
    ray_width = SCREEN_WIDTH / NUM_RAYS
    for i in range(NUM_RAYS):
        angle = player['angle'] - FOV/2 + (i/NUM_RAYS) * FOV
        dist, wtype = cast_ray(player['x'], player['y'], angle)
        dist *= math.cos(angle - player['angle'])
        
        height = (SCREEN_HEIGHT / 2) / (dist / 5) if dist > 0 else SCREEN_HEIGHT
        darkness = max(0.2, 1 - dist / MAX_RAY_DISTANCE)
        color = tuple(int(c * darkness) for c in ((100, 100, 200) if wtype == 'v' else (80, 80, 180)))
        
        y = (SCREEN_HEIGHT - height) / 2
        pygame.draw.rect(screen, color, (i * ray_width, y, ray_width + 1, height))
    
    # Draw coins in 3D view
    for cx, cy in coins:
        dx = cx - player['x']
        dy = cy - player['y']
        dist = math.sqrt(dx**2 + dy**2)
        angle_to_coin = math.atan2(dy, dx)
        
        # Check line of sight to coin
        wall_dist, _ = cast_ray(player['x'], player['y'], angle_to_coin)
        wall_dist *= math.cos(angle_to_coin - player['angle'])
        
        # Only draw if coin is visible (no wall blocking)
        if wall_dist > dist:
            angle_diff = angle_to_coin - player['angle']
            
            # Normalize angle difference to -pi to pi
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            
            # Check if coin is in FOV
            if abs(angle_diff) < FOV / 2 and dist < MAX_RAY_DISTANCE:
                screen_x = SCREEN_WIDTH / 2 + (angle_diff / (FOV / 2)) * (SCREEN_WIDTH / 2)
                coin_height = (SCREEN_HEIGHT / 2) / (dist / 5)
                coin_size = max(2, int(coin_height / 4))
                coin_y = (SCREEN_HEIGHT - coin_height) / 2 + coin_height / 2
                
                brightness = max(0.3, 1 - dist / MAX_RAY_DISTANCE)
                coin_color = tuple(int(c * brightness) for c in (255, 215, 0))
                
                pygame.draw.circle(screen, coin_color, (int(screen_x), int(coin_y)), coin_size)
    
    # Minimap
    mm_scale = 15
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            color = (100, 100, 100) if GAME_MAP[y][x] == 1 else (50, 50, 50)
            pygame.draw.rect(screen, color, (x * mm_scale, y * mm_scale, mm_scale, mm_scale))
    
    # Draw coins on minimap
    for cx, cy in coins:
        pygame.draw.circle(screen, (255, 215, 0), (int(cx * mm_scale), int(cy * mm_scale)), 4)
    
    pmx, pmy = player['x'] * mm_scale, player['y'] * mm_scale
    pygame.draw.circle(screen, (255, 0, 0), (int(pmx), int(pmy)), 3)
    pygame.draw.line(screen, (255, 0, 0), (pmx, pmy), 
                     (pmx + math.cos(player['angle'])*10, pmy + math.sin(player['angle'])*10), 2)
    
    # Info
    font = pygame.font.Font(None, 20)
    screen.blit(font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255)), (5, SCREEN_HEIGHT - 25))
    screen.blit(font.render(f"Score: {score} | Coins: {len(coins)}", True, (255, 215, 0)), (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 25))


def main():
    global clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Raycasting 3D Game")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        
        update_player(pygame.key.get_pressed())
        render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

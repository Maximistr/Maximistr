"""Raycasting 3D Game Engine - pygame"""
import pygame, math, sys, random
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
FPS = 60
FOV = math.pi / 3
NUM_RAYS = 120
MAX_RAY_DISTANCE = 30
MAP_WIDTH, MAP_HEIGHT = 25, 25

def generate_map(width, height):
    """Generate connected dungeon map with corridors"""
    game_map = [[1 for _ in range(width)] for _ in range(height)]
    
    # Carve out rooms and store their centers
    rooms = []
    for _ in range(15):
        x = random.randint(3, width - 7)
        y = random.randint(3, height - 7)
        w = random.randint(4, 8)
        h = random.randint(4, 8)
        
        # Carve room
        for dy in range(h):
            for dx in range(w):
                if y + dy < height and x + dx < width:
                    game_map[y + dy][x + dx] = 0
        
        rooms.append((x + w // 2, y + h // 2))
    
    # Connect rooms with corridors
    for i in range(len(rooms) - 1):
        x1, y1 = rooms[i]
        x2, y2 = rooms[i + 1]
        
        # Horizontal corridor
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if y1 < height and x < width:
                game_map[int(y1)][int(x)] = 0
        
        # Vertical corridor
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if x2 < width and y < height:
                game_map[int(y)][int(x2)] = 0
    
    return game_map

GAME_MAP = generate_map(MAP_WIDTH, MAP_HEIGHT)

# Find a safe spawn point
def find_safe_spawn():
    attempts = 0
    while attempts < 1000:
        x = random.uniform(2, MAP_WIDTH - 2)
        y = random.uniform(2, MAP_HEIGHT - 2)
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
            return x, y
        attempts += 1
    return 12.5, 12.5

px, py = find_safe_spawn()
player = {'x': px, 'y': py, 'angle': 0, 'speed': 0.1, 'rotSpeed': 0.05, 'health': 100}

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

def generate_enemies(num_enemies=5):
    """Generate random enemy positions"""
    enemies = []
    attempts = 0
    while len(enemies) < num_enemies and attempts < 1000:
        x = random.uniform(2, MAP_WIDTH - 2)
        y = random.uniform(2, MAP_HEIGHT - 2)
        r = 0.3
        walkable = True
        for dx in [-r, 0, r]:
            for dy in [-r, 0, r]:
                if GAME_MAP[int(y + dy)][int(x + dx)] == 1:
                    walkable = False
                    break
            if not walkable:
                break
        
        # Don't spawn too close to player
        if walkable and math.sqrt((px - x)**2 + (py - y)**2) > 4:
            enemies.append({'x': x, 'y': y, 'health': 20, 'speed': 0.05})
        
        attempts += 1
    return enemies

enemies = generate_enemies(5)


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
    
    # Check enemy collision (take damage)
    for enemy in enemies:
        dist = math.sqrt((player['x'] - enemy['x'])**2 + (player['y'] - enemy['y'])**2)
        if dist < 0.5:
            player['health'] -= 0.1

def update_enemies():
    """Update enemy AI - move toward player"""
    for enemy in enemies:
        dx = player['x'] - enemy['x']
        dy = player['y'] - enemy['y']
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0.1:
            # Move toward player
            enemy['x'] += (dx / dist) * enemy['speed']
            enemy['y'] += (dy / dist) * enemy['speed']
            
            # Simple wall collision
            r = 0.2
            for dx_check in [-r, 0, r]:
                for dy_check in [-r, 0, r]:
                    if GAME_MAP[int(enemy['y'] + dy_check)][int(enemy['x'] + dx_check)] == 1:
                        enemy['x'] -= (dx / dist) * enemy['speed']
                        enemy['y'] -= (dy / dist) * enemy['speed']
                        break

def shoot():
    """Shoot in the direction the player is looking"""
    global score
    shot_dist = 30
    enemies_to_remove = []
    
    for i, enemy in enumerate(enemies):
        dx = enemy['x'] - player['x']
        dy = enemy['y'] - player['y']
        dist = math.sqrt(dx**2 + dy**2)
        angle_to_enemy = math.atan2(dy, dx)
        angle_diff = angle_to_enemy - player['angle']
        
        # Normalize angle
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi
        
        # Hit if in center of screen and close enough
        if abs(angle_diff) < 0.1 and dist < shot_dist:
            enemy['health'] -= 50
            if enemy['health'] <= 0:
                enemies_to_remove.append(i)
                score += 50
    
    for i in reversed(enemies_to_remove):
        enemies.pop(i)


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
    
    # Draw enemies in 3D view
    for enemy in enemies:
        dx = enemy['x'] - player['x']
        dy = enemy['y'] - player['y']
        dist = math.sqrt(dx**2 + dy**2)
        angle_to_enemy = math.atan2(dy, dx)
        
        # Check line of sight
        wall_dist, _ = cast_ray(player['x'], player['y'], angle_to_enemy)
        wall_dist *= math.cos(angle_to_enemy - player['angle'])
        
        if wall_dist > dist and dist > 0.1:
            angle_diff = angle_to_enemy - player['angle']
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            
            if abs(angle_diff) < FOV / 2 and dist < MAX_RAY_DISTANCE:
                screen_x = SCREEN_WIDTH / 2 + (angle_diff / (FOV / 2)) * (SCREEN_WIDTH / 2)
                enemy_height = (SCREEN_HEIGHT / 2) / (dist / 5)
                enemy_size = max(5, int(enemy_height / 3))
                enemy_y = (SCREEN_HEIGHT - enemy_height) / 2 + enemy_height / 2
                
                # Enemy color based on health
                health_ratio = enemy['health'] / 20.0
                enemy_color = (int(200 * (1 - health_ratio)), int(50 + 150 * health_ratio), 50)
                
                pygame.draw.rect(screen, enemy_color, (int(screen_x) - enemy_size // 2, 
                                                      int(enemy_y) - enemy_size, 
                                                      enemy_size, enemy_size * 2))
    
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
    screen.blit(font.render(f"Score: {score} | Coins: {len(coins)} | Enemies: {len(enemies)}", True, (255, 215, 0)), (SCREEN_WIDTH - 350, SCREEN_HEIGHT - 25))
    
    # Health bar
    bar_width = 200
    bar_height = 20
    bar_x = 10
    bar_y = SCREEN_HEIGHT - 55
    health_ratio = max(0, player['health'] / 100)
    pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (255 - int(health_ratio * 200), int(health_ratio * 200), 50), 
                     (bar_x, bar_y, int(bar_width * health_ratio), bar_height))
    screen.blit(font.render(f"Health: {int(player['health'])}", True, (255, 255, 255)), (bar_x, bar_y - 25))
    
    # Crosshair
    cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4
    pygame.draw.line(screen, (100, 200, 100), (cx - 10, cy), (cx + 10, cy), 1)
    pygame.draw.line(screen, (100, 200, 100), (cx, cy - 10), (cx, cy + 10), 1)


def main():
    global clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Raycasting 3D Game - WASD move, SPACE/Click shoot, Mouse rotate")
    clock = pygame.time.Clock()
    
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    center_x = SCREEN_WIDTH // 2
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                shoot()
        
        if player['health'] <= 0:
            running = False
        
        # Mouse rotation (like classic FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_delta = mouse_x - center_x
        player['angle'] += mouse_delta * 0.005
        pygame.mouse.set_pos(center_x, mouse_y)
        
        update_player(pygame.key.get_pressed())
        update_enemies()
        render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

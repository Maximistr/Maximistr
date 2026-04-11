"""Raycasting 3D Game Engine - pygame"""
import pygame, math, sys, random,os 
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
FPS = 60
FOV = math.pi / 3
NUM_RAYS = 80
MAX_RAY_DISTANCE = 20
RAY_STEP = 0.05
MAP_WIDTH, MAP_HEIGHT = 25, 25

# Animation constants
ANIMATION_INTERVAL = 300  # ms

# Global game state
current_level = 1
total_score = 0

# Game state variables (will be initialized per level)
player = {}
coins = []
enemies = []
fireballs = []
GAME_MAP = []
score = 0
enemy_sprite_img = None
clock = None

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
    
    # Ensure perimeter walls
    for x in range(width):
        game_map[0][x] = 1
        game_map[height - 1][x] = 1
    for y in range(height):
        game_map[y][0] = 1
        game_map[y][width - 1] = 1
    
    return game_map


def find_safe_spawn():
    """Find a safe spawn point not in walls"""
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


def cast_ray(x, y, angle):
    """Cast a ray using DDA algorithm for high precision"""
    dir_x = math.cos(angle)
    dir_y = math.sin(angle)
    
    map_x = int(x)
    map_y = int(y)
    
    # Length of ray from one x or y-side to next x or y-side
    delta_dist_x = abs(1 / dir_x) if dir_x != 0 else 1e30
    delta_dist_y = abs(1 / dir_y) if dir_y != 0 else 1e30
    
    # Calculate step and initial sideDist
    if dir_x < 0:
        step_x = -1
        side_dist_x = (x - map_x) * delta_dist_x
    else:
        step_x = 1
        side_dist_x = (map_x + 1.0 - x) * delta_dist_x
        
    if dir_y < 0:
        step_y = -1
        side_dist_y = (y - map_y) * delta_dist_y
    else:
        step_y = 1
        side_dist_y = (map_y + 1.0 - y) * delta_dist_y
    
    # DDA
    hit = False
    side = 0 # 0 for NS, 1 for EW
    dist = 0
    
    while not hit and dist < MAX_RAY_DISTANCE:
        if side_dist_x < side_dist_y:
            side_dist_x += delta_dist_x
            map_x += step_x
            side = 0
        else:
            side_dist_y += delta_dist_y
            map_y += step_y
            side = 1
            
        if 0 <= map_x < MAP_WIDTH and 0 <= map_y < MAP_HEIGHT:
            if GAME_MAP[map_y][map_x] == 1:
                hit = True
        else:
            break
            
    if hit:
        if side == 0:
            dist = (side_dist_x - delta_dist_x)
            hit_pos = y + dist * dir_y
        else:
            dist = (side_dist_y - delta_dist_y)
            hit_pos = x + dist * dir_x
        
        hit_pos -= math.floor(hit_pos)
        return (dist, 'v' if side == 0 else 'h', hit_pos)
    
    return (MAX_RAY_DISTANCE, 'v', 0)


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
    current_time = pygame.time.get_ticks()
    
    # Handle ammo reload (1.5 seconds per ammo)
    if player['ammo'] < player['max_ammo']:
        if player['reload_start_time'] is None:
            player['reload_start_time'] = current_time
        elif current_time - player['reload_start_time'] >= 1500:
            player['ammo'] += 1
            player['reload_start_time'] = current_time
    
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
        if math.sqrt((player['x'] - cx)**2 + (player['y'] - cy)**2) < 0.6:
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
    """Update enemy AI - move toward player with sliding"""
    for enemy in enemies:
        dx = player['x'] - enemy['x']
        dy = player['y'] - enemy['y']
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0.1:
            # Move toward player
            vx = (dx / dist) * enemy['speed']
            vy = (dy / dist) * enemy['speed']
            
            # Try moving X
            new_x = enemy['x'] + vx
            if is_walkable(new_x, enemy['y']):
                enemy['x'] = new_x
                
            # Try moving Y
            new_y = enemy['y'] + vy
            if is_walkable(enemy['x'], new_y):
                enemy['y'] = new_y

def update_fireballs():
    """Update fireball movement and collisions"""
    global score
    fireballs_to_remove = []
    
    for i, fb in enumerate(fireballs):
        fb['x'] += math.cos(fb['angle']) * fb['speed']
        fb['y'] += math.sin(fb['angle']) * fb['speed']
        fb['distance'] += fb['speed']
        
        # Check for wall collision
        if fb['x'] < 0 or fb['x'] >= MAP_WIDTH or fb['y'] < 0 or fb['y'] >= MAP_HEIGHT or \
           GAME_MAP[int(fb['y'])][int(fb['x'])] == 1:
            fireballs_to_remove.append(i)
            continue
            
        # Check for enemy collision
        for j, enemy in enumerate(enemies):
            dist = math.sqrt((fb['x'] - enemy['x'])**2 + (fb['y'] - enemy['y'])**2)
            if dist < 1.0:
                enemy['health'] -= 20
                fireballs_to_remove.append(i)
                if enemy['health'] <= 0:
                    enemies.pop(j)
                    score += 50
                break
        
        # Max distance
        if fb['distance'] > MAX_RAY_DISTANCE:
            fireballs_to_remove.append(i)
            
    for i in reversed(sorted(list(set(fireballs_to_remove)))):
        if 0 <= i < len(fireballs):
            fireballs.pop(i)

def shoot():
    """Spawn a fireball in the direction the player is looking"""
    # Check if player has ammo
    if player['ammo'] <= 0:
        return
    
    fireballs.append({
        'x': player['x'],
        'y': player['y'],
        'angle': player['angle'],
        'speed': 0.3,
        'distance': 0
    })
    
    # Decrement ammo
    player['ammo'] -= 1


def render(screen):
    """Render 3D view and minimap"""
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (100, 50, 20), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    pygame.draw.rect(screen, (139, 69, 19), (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    
    ray_width = SCREEN_WIDTH / NUM_RAYS
    
    # Shading cache surface
    shade_cache = pygame.Surface((int(ray_width) + 2, SCREEN_HEIGHT))
    
    for i in range(NUM_RAYS):
        angle = player['angle'] - FOV/2 + (i/NUM_RAYS) * FOV
        dist, wtype, hit_pos = cast_ray(player['x'], player['y'], angle)
        
        # Fish-eye correction
        dist *= math.cos(angle - player['angle'])
        
        height = (SCREEN_HEIGHT / 2) / (dist / 5) if dist > 0.01 else SCREEN_HEIGHT
        
        # Clamp height and determine vertical offset
        draw_height = min(int(height), SCREEN_HEIGHT)
        y = (SCREEN_HEIGHT - draw_height) / 2
        
        # Draw walls as solid blocks (with shading)
        darkness = max(0.2, 1 - dist / MAX_RAY_DISTANCE)
        # Use different shades of orange for vertical vs horizontal hits
        color = tuple(int(c * darkness) for c in ((255, 140, 0) if wtype == 'v' else (255, 165, 0)))
        
        pygame.draw.rect(screen, color, (i * ray_width, y, ray_width + 1, draw_height))
    
    # Draw coins in 3D view
    for cx, cy in coins:
        dx = cx - player['x']
        dy = cy - player['y']
        dist = math.sqrt(dx**2 + dy**2)
        angle_to_coin = math.atan2(dy, dx)
        
        # Check line of sight to coin
        wall_dist, _, _ = cast_ray(player['x'], player['y'], angle_to_coin)
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
        wall_dist, _, _ = cast_ray(player['x'], player['y'], angle_to_enemy)
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
                
                # Draw enemy as sprite
                health_ratio = min(1.0, enemy['health'] / 50.0)
                
                # Scale sprite based on distance
                s_width = int(enemy_height)
                s_height = int(enemy_height)
                
                # Center the sprite on the screen position
                sprite_rect = pygame.Rect(0, 0, s_width, s_height)
                sprite_rect.center = (int(screen_x), int(enemy_y))
                
                scaled_sprite = pygame.transform.scale(enemy_sprite_img, (s_width, s_height))
                
                # Simple flipping animation
                current_time = pygame.time.get_ticks()
                if ((current_time + enemy.get('anim_offset', 0)) // ANIMATION_INTERVAL) % 2 == 1:
                    scaled_sprite = pygame.transform.flip(scaled_sprite, True, False)

                # Apply depth shading while preserving alpha
                darkness = max(0.3, 1 - dist / MAX_RAY_DISTANCE)
                shade = int(255 * darkness)
                
                # Create a shading surface
                shade_surf = pygame.Surface((s_width, s_height))
                shade_surf.fill((shade, shade, shade))
                
                # Blend with MULTIPLY to darken while keeping transparent parts transparent
                scaled_sprite.blit(shade_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
                screen.blit(scaled_sprite, sprite_rect)
                
                # Draw health bar above enemy
                bar_width = int(enemy_height / 2)
                bar_height = 4
                pygame.draw.rect(screen, (100, 100, 100), (int(screen_x - bar_width // 2), int(sprite_rect.top - 10), bar_width, bar_height))
                pygame.draw.rect(screen, (0, 255, 0), (int(screen_x - bar_width // 2), int(sprite_rect.top - 10), int(bar_width * health_ratio), bar_height))

    # Draw fireballs in 3D view
    for fb in fireballs:
        dx = fb['x'] - player['x']
        dy = fb['y'] - player['y']
        dist = math.sqrt(dx**2 + dy**2)
        angle_to_fb = math.atan2(dy, dx)
        
        # Check line of sight
        wall_dist, _, _ = cast_ray(player['x'], player['y'], angle_to_fb)
        wall_dist *= math.cos(angle_to_fb - player['angle'])
        
        if wall_dist > dist:
            angle_diff = angle_to_fb - player['angle']
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            
            if abs(angle_diff) < FOV / 2 and dist < MAX_RAY_DISTANCE and dist > 0.1:
                screen_x = SCREEN_WIDTH / 2 + (angle_diff / (FOV / 2)) * (SCREEN_WIDTH / 2)
                fb_height = (SCREEN_HEIGHT / 2) / (dist / 5)
                fb_size = max(4, int(fb_height / 6))
                fb_y = (SCREEN_HEIGHT - fb_height) / 2 + fb_height / 2
                
                # Glowing fireball effect
                pygame.draw.circle(screen, (255, 200, 0), (int(screen_x), int(fb_y)), fb_size + 2)
                pygame.draw.circle(screen, (255, 100, 0), (int(screen_x), int(fb_y)), fb_size)
                pygame.draw.circle(screen, (255, 255, 200), (int(screen_x), int(fb_y)), fb_size // 2)

    # Minimap
    mm_scale = 10
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
    screen.blit(font.render(f"Level: {current_level} | Score: {score} | Coins: {len(coins)} | Enemies: {len(enemies)}", True, (255, 215, 0)), (SCREEN_WIDTH - 500, SCREEN_HEIGHT - 25))
    
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
    
    # Ammo display
    ammo_x = SCREEN_WIDTH - 200
    ammo_y = SCREEN_HEIGHT - 55
    ammo_text = font.render(f"Ammo: {player['ammo']}/{player['max_ammo']}", True, (255, 165, 0))
    screen.blit(ammo_text, (ammo_x, ammo_y - 25))
    
    # Ammo bar
    ammo_bar_width = 150
    ammo_bar_height = 20
    ammo_ratio = player['ammo'] / player['max_ammo']
    ammo_color = (255, 165, 0) if player['ammo'] > 0 else (100, 100, 100)
    pygame.draw.rect(screen, (50, 50, 50), (ammo_x, ammo_y, ammo_bar_width, ammo_bar_height))
    pygame.draw.rect(screen, ammo_color, (ammo_x, ammo_y, int(ammo_bar_width * ammo_ratio), ammo_bar_height))
    
    # Reload status
    if player['ammo'] < player['max_ammo'] and player['reload_start_time'] is not None:
        current_time = pygame.time.get_ticks()
        time_reloading = current_time - player['reload_start_time']
        reload_time = 1500
        reload_progress = min(1.0, time_reloading / reload_time)
        reload_text = font.render(f"Reload: {int(reload_progress * 100)}%", True, (255, 100, 100))
        screen.blit(reload_text, (ammo_x, ammo_y + 25))
    
    # Crosshair (center of screen)
    cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    pygame.draw.line(screen, (100, 200, 100), (cx - 10, cy), (cx + 10, cy), 1)
    pygame.draw.line(screen, (100, 200, 100), (cx, cy - 10), (cx, cy + 10), 1)


def initialize_level(level):
    """Initialize a new level with difficulty scaling"""
    global GAME_MAP, player, coins, enemies, fireballs, px, py, score
    
    score = 0
    fireballs = []
    
    # Generate new map
    GAME_MAP = generate_map(MAP_WIDTH, MAP_HEIGHT)
    px, py = find_safe_spawn()
    
    # Scale difficulty with level
    health_scaling = 1.0 + (level - 1) * 0.2  # Slightly reduced for better playability
    enemy_count = 3 + (level - 1) * 2
    coin_count = 5 + (level - 1)
    enemy_speed_scaling = 1.0 + (level - 1) * 0.15
    
    # Reset player
    player = {
        'x': px, 
        'y': py, 
        'angle': 0, 
        'speed': 0.1, 
        'rotSpeed': 0.05, 
        'health': 100 * health_scaling,
        'ammo': 3,
        'max_ammo': 3,
        'reload_start_time': None
    }
    
    # Generate level-specific enemies with difficulty scaling
    enemies = []
    attempts = 0
    while len(enemies) < enemy_count and attempts < 1000:
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
        
        if walkable and math.sqrt((player['x'] - x)**2 + (player['y'] - y)**2) > 4:
            enemies.append({
                'x': x, 
                'y': y, 
                'health': 50 * (1.0 + (level - 1) * 0.3), 
                'speed': 0.05 * enemy_speed_scaling, 
                'anim_offset': random.randint(0, 1000)
            })
        attempts += 1
    
    # Generate coins
    coins = generate_coins(coin_count)


def show_level_menu(screen, font_large, font_small):
    """Display level selection menu"""
    selecting = True
    selected_level = 1
    
    while selecting:
        screen.fill((10, 10, 10))
        
        title = font_large.render("SELECT LEVEL", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        y_pos = 150
        for level_num in range(1, 6):
            color = (255, 255, 0) if level_num == selected_level else (150, 150, 150)
            indicator = ">>> " if level_num == selected_level else "    "
            level_text = font_small.render(f"{indicator}Level {level_num}", True, color)
            screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, y_pos))
            y_pos += 50
        
        instructions = font_small.render("UP/DOWN: Select | ENTER/SPACE: Play | ESC: Quit", True, (200, 200, 200))
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 100))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_level = max(1, selected_level - 1)
                elif event.key == pygame.K_DOWN:
                    selected_level = min(5, selected_level + 1)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return selected_level
                elif event.key == pygame.K_ESCAPE:
                    return None
    
    return selected_level


def show_level_complete_menu(screen, font_large, font_small, level, level_score):
    """Display level complete screen with options"""
    waiting = True
    
    while waiting:
        screen.fill((10, 10, 10))
        
        title = font_large.render(f"LEVEL {level} COMPLETE!", True, (0, 255, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        
        score_text = font_small.render(f"Level Score: {int(level_score)}", True, (255, 215, 0))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 180))
        
        total_text = font_small.render(f"Total Score: {int(total_score)}", True, (255, 215, 0))
        screen.blit(total_text, (SCREEN_WIDTH // 2 - total_text.get_width() // 2, 230))
        
        next_level_text = font_small.render("SPACE: Next Level", True, (150, 200, 255))
        screen.blit(next_level_text, (SCREEN_WIDTH // 2 - next_level_text.get_width() // 2, 330))
        
        level_select_text = font_small.render("M: Select Level", True, (200, 150, 200))
        screen.blit(level_select_text, (SCREEN_WIDTH // 2 - level_select_text.get_width() // 2, 380))
        
        quit_text = font_small.render("ESC: Quit", True, (200, 100, 100))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 430))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 'next'
                elif event.key == pygame.K_m:
                    return 'menu'
                elif event.key == pygame.K_ESCAPE:
                    return None
    
    return 'next'


def show_game_over_menu(screen, font_large, font_small, game_over_reason):
    """Display game over screen"""
    waiting = True
    
    while waiting:
        screen.fill((10, 10, 10))
        
        title = font_large.render("GAME OVER", True, (255, 0, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        reason = font_small.render(game_over_reason, True, (255, 100, 100))
        screen.blit(reason, (SCREEN_WIDTH // 2 - reason.get_width() // 2, 200))
        
        total_text = font_small.render(f"Total Score: {int(total_score)}", True, (255, 215, 0))
        screen.blit(total_text, (SCREEN_WIDTH // 2 - total_text.get_width() // 2, 280))
        
        retry_text = font_small.render("SPACE: Try Again", True, (150, 200, 255))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, 360))
        
        level_select_text = font_small.render("M: Select Level", True, (200, 150, 200))
        screen.blit(level_select_text, (SCREEN_WIDTH // 2 - level_select_text.get_width() // 2, 410))
        
        quit_text = font_small.render("ESC: Quit", True, (200, 100, 100))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 460))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 'retry'
                elif event.key == pygame.K_m:
                    return 'menu'
                elif event.key == pygame.K_ESCAPE:
                    return None
    
    return 'menu'


def main():
    global clock, current_level, total_score, player, coins, enemies, fireballs, GAME_MAP, score
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Raycasting 3D Game - WASD move, SPACE/Click shoot, Mouse rotate, M: Menu")
    
    # Load Assets (must be after set_mode for convert_alpha)
    global enemy_sprite_img
    script_dir = os.path.dirname(__file__)
    
    try:
        sprite_path = os.path.join(script_dir, "enemy_sprite.png")
        temp_img = pygame.image.load(sprite_path).convert()
        # Use top-left pixel as colorkey
        colorkey = temp_img.get_at((0, 0))
        temp_img.set_colorkey(colorkey)
        
        # Bake the colorkey into a true alpha channel
        enemy_sprite_img = pygame.Surface(temp_img.get_size(), pygame.SRCALPHA)
        enemy_sprite_img.blit(temp_img, (0, 0))
    except Exception as e:
        print(f"Error loading sprite: {e}")
        enemy_sprite_img = pygame.Surface((64, 64))
        enemy_sprite_img.fill((255, 0, 0))

    clock = pygame.time.Clock()
    
    # Fonts for menus
    font_large = pygame.font.Font(None, 50)
    font_small = pygame.font.Font(None, 30)
    
    # Show initial level menu
    level_to_play = show_level_menu(screen, font_large, font_small)
    if level_to_play is None:
        pygame.quit()
        return
    
    current_level = level_to_play
    total_score = 0
    
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    center_x = SCREEN_WIDTH // 2
    
    # Main game loop
    running = True
    in_level = True
    
    while running:
        if in_level:
            # Initialize the current level
            initialize_level(current_level)
            level_complete = False
            
            # Level gameplay loop
            while in_level and not level_complete:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        in_level = False
                        break
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            in_level = False
                            break
                        if event.key == pygame.K_m:
                            # Return to menu
                            in_level = False
                            break
                        if event.type == pygame.MOUSEBUTTONDOWN or event.key == pygame.K_SPACE:
                            shoot()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        shoot()
                
                if not in_level:
                    break
                
                if player['health'] <= 0:
                    # Game over
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
                    action = show_game_over_menu(screen, font_large, font_small, "You died!")
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    
                    if action == 'retry':
                        break
                    elif action == 'menu':
                        in_level = False
                        break
                    else:
                        running = False
                        in_level = False
                        break
                
                # Check if level is complete (all enemies defeated AND all coins collected)
                if len(enemies) == 0 and len(coins) == 0:
                    level_complete = True
                    total_score += score
                    break
                
                # Mouse rotation (like classic FPS)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_delta = mouse_x - center_x
                player['angle'] += mouse_delta * 0.005
                pygame.mouse.set_pos(center_x, mouse_y)
                
                update_player(pygame.key.get_pressed())
                update_enemies()
                update_fireballs()
                render(screen)
                pygame.display.flip()
                clock.tick(FPS)
            
            # Level complete menu
            if level_complete and in_level:
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
                action = show_level_complete_menu(screen, font_large, font_small, current_level, score)
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)
                
                if action == 'next':
                    current_level += 1
                    in_level = True
                elif action == 'menu':
                    in_level = False
                    level_to_play = show_level_menu(screen, font_large, font_small)
                    if level_to_play is None:
                        running = False
                    else:
                        current_level = level_to_play
                        in_level = True
                else:
                    running = False
                    in_level = False
            
            # If player died
            elif not level_complete and not in_level:
                # Return to menu
                level_to_play = show_level_menu(screen, font_large, font_small)
                if level_to_play is None:
                    running = False
                else:
                    current_level = level_to_play
                    total_score = 0
                    in_level = True
    
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

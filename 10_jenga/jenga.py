import pygame
import math

WIDTH, HEIGHT = 800, 600
BACKGROUND = (30, 30, 40)

# Barvy pro jednotlivé strany krychle
COLOR_TOP = (200, 200, 200)
COLOR_LEFT = (150, 150, 150)
COLOR_RIGHT = (100, 100, 100)

# Velikost hrany krychle
SIZE = 150

# Nastavení izometrické projekce
ISO_COS = 0.866
ISO_SIN = 0.5

def project(x, y, z):
    """Převede 3D souřadnice na 2D souřadnice obrazovky."""
    screen_x = WIDTH // 2 + (x - y) * ISO_COS
    # Použijeme střed obrazovky jako výchozí bod (0,0,0)
    screen_y = HEIGHT // 2 + (x + y) * ISO_SIN - z
    return int(screen_x), int(screen_y)

def rotate_point(x, y, z, ax=0, ay=0, az=0):
    """Otočí 3D bod kolem os X, Y a Z."""
    # Rotate around X
    cosa, sina = math.cos(ax), math.sin(ax)
    y, z = y * cosa - z * sina, y * sina + z * cosa

    # Rotate around Y
    cosb, sinb = math.cos(ay), math.sin(ay)
    x, z = x * cosb + z * sinb, -x * sinb + z * cosb

    # Rotate around Z
    cosc, sinc = math.cos(az), math.sin(az)
    x, y = x * cosc - y * sinc, x * sinc + y * cosc

    return x, y, z

def draw_cube(surface, angle_x=0, angle_y=0, angle_z=0):
    """Vykreslí izometrickou krychli."""
    s = SIZE / 2
    # 8 rohů krychle ve 3D prostoru (x, y, z)
    corners_3d = [
        (-s, -s, -s), (s, -s, -s), (s, s, -s), (-s, s, -s), # Spodní rohy
        (-s, -s, s),  (s, -s, s),  (s, s, s),  (-s, s, s)   # Horní rohy
    ]
    
    # Převedení všech rohů do 2D obrazovky
    rotated = [rotate_point(x, y, z, angle_x, angle_y, angle_z) for x, y, z in corners_3d]
    c = [project(x, y, z) for x, y, z in rotated]
    
    # Definice 6 stěn (pomocí indexů rohů) a jejich barvy
    faces = [
        ([4, 5, 6, 7], COLOR_TOP),   # Horní stěna (+z)
        ([5, 1, 2, 6], COLOR_RIGHT), # Pravá stěna (+x)
        ([6, 2, 3, 7], COLOR_LEFT),  # Levá stěna (+y)
        ([7, 3, 0, 4], COLOR_RIGHT), # Zadní pravá (-x)
        ([4, 0, 1, 5], COLOR_LEFT),  # Zadní levá (-y)
        ([1, 0, 3, 2], COLOR_TOP),   # Spodní stěna (-z)
    ]
    
    for idxs, color in faces:
        face = [c[i] for i in idxs]
        
        # Algoritmus Backface culling: zjistí, zda je stěna natočená k nám
        area = 0
        for i in range(len(face)):
            p1 = face[i]
            p2 = face[(i+1) % len(face)]
            area += (p1[0] * p2[1] - p2[0] * p1[1])
            
        # Vykreslí stěnu pouze pokud je viditelná (obsah > 0)
        if area > 0:
            pygame.draw.polygon(surface, color, face)       # Vyplnění barvou
            pygame.draw.polygon(surface, (0, 0, 0), face, 2) # Černý obrys

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Izometrická krychle")
    clock = pygame.time.Clock()

    angle_x = 0.0
    angle_y = 0.0
    angle_z = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    angle_y -= 0.05
                elif event.key == pygame.K_RIGHT:
                    angle_y += 0.05
                elif event.key == pygame.K_UP:
                    angle_x -= 0.05
                elif event.key == pygame.K_DOWN:
                    angle_x += 0.05
                elif event.key == pygame.K_a:
                    angle_z -= 0.05
                elif event.key == pygame.K_d:
                    angle_z += 0.05

        # Continuous automatic rotation


        screen.fill(BACKGROUND)
        draw_cube(screen, angle_x, angle_y, angle_z)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
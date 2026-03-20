"""
Interaktivní Systém Částic s Fyzikou
- Reálná fyzikální simulace s gravitací, třením a elastickými srážkami
- Interaktivní ovládání částic pomocí myši a klávesnice
"""

import pygame
import math
import random
import sys

pygame.init()

# Konstanty
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
FPS = 60
GRAVITY = 9.81
PARTICLE_RADIUS = 5
FRICTION = 0.99  # Odpor vzduchu (0.99 = 1% ztráta energie za frame)
ELASTICITY = 0.85  # Pružnost srážek (0.85 = 15% ztráta energie)
PARTICLE_MASS = 1.0

# Barvy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WALL_COLOR = (100, 100, 100)


class Particle:
    """Třída reprezentující jednu částici s fyzikou"""
    
    def __init__(self, x, y, velocity_x=0, velocity_y=0):
        """Inicializace částice
        
        Args:
            x, y: Počáteční pozice
            velocity_x, velocity_y: Počáteční rychlost
        """
        self.x = x
        self.y = y
        self.vx = velocity_x
        self.vy = velocity_y
        self.ax = 0  # Akcelerace
        self.ay = GRAVITY
        self.mass = PARTICLE_MASS
        self.radius = PARTICLE_RADIUS
        self.color = (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255))
        self.life = 1.0  # Průhlednost (1.0 = plná viditelnost)
    
    def apply_force(self, fx, fy):
        """Aplikuj sílu na částici (F = ma)"""
        self.ax += fx / self.mass
        self.ay += fy / self.mass
    
    def update(self, dt=1/60):
        """Aktualizuj pozici a rychlost částice (Eulerova integrátor)"""
        # Aktualizuj rychlost: v = v + a*dt
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        
        # Aplikuj odpor vzduchu
        self.vx *= FRICTION
        self.vy *= FRICTION
        
        # Aktualizuj pozici: x = x + v*dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Resetuj akceleraci pro příští krok
        self.ax = 0
        self.ay = GRAVITY
    
    def check_wall_collision(self):
        """Detekuj srážky se zeďmi a vrátí elastickou srážku"""
        # Dolní stěna
        if self.y + self.radius > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius
            self.vy *= -ELASTICITY
        
        # Horní stěna
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -ELASTICITY
        
        # Pravá stěna
        if self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.vx *= -ELASTICITY
        
        # Levá stěna
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -ELASTICITY
    
    def distance_to(self, other):
        """Vypočítej vzdálenost od jiné částice"""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx + dy*dy)
    
    def check_particle_collision(self, other):
        """Detekuj a zpracuj elastickou srážku s jinou částicí"""
        dist = self.distance_to(other)
        min_dist = self.radius + other.radius
        
        if dist < min_dist:
            # Normalizovaný vektor srážky
            nx = (other.x - self.x) / dist
            ny = (other.y - self.y) / dist
            
            # Relativní rychlost
            dvx = other.vx - self.vx
            dvy = other.vy - self.vy
            
            # Relativní rychlost podél normály srážky
            dvn = dvx * nx + dvy * ny
            
            # Ignoruj pokud se částice vzdalují
            if dvn < 0:
                return
            
            # Elastická srážka (zakončení hybnosti a energie)
            # Pro rovné hmoty: v1' = v1 + (v2-v1)*n*n
            impulse = (1 + ELASTICITY) * dvn / 2
            
            self.vx += impulse * nx
            self.vy += impulse * ny
            other.vx -= impulse * nx
            other.vy -= impulse * ny
            
            # Oddělení částic aby se nelepily
            overlap = min_dist - dist
            separate_x = (overlap / 2 + 0.01) * nx
            separate_y = (overlap / 2 + 0.01) * ny
            
            self.x -= separate_x
            self.y -= separate_y
            other.x += separate_x
            other.y += separate_y
    
    def draw(self, surface):
        """Nakresli částici na povrch"""
        # Barva s fade efektem
        r = int(self.color[0] * self.life)
        g = int(self.color[1] * self.life)
        b = int(self.color[2] * self.life)
        
        pygame.draw.circle(surface, (r, g, b), (int(self.x), int(self.y)), self.radius)
        
        # Malý okraj pro lepší viditelnost
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 1)


class ParticleSystem:
    """Správce systému částic"""
    
    def __init__(self):
        self.particles = []
    
    def add_particle(self, x, y, vx=None, vy=None):
        """Přidej novou částici"""
        if vx is None and vy is None:
            # Náhodná počáteční rychlost
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
        
        self.particles.append(Particle(x, y, vx, vy))
    
    def apply_force_field(self, center_x, center_y, force_strength, radius):
        """Aplikuj kruhové silové pole (přitažlivost/odpor)"""
        for particle in self.particles:
            dx = center_x - particle.x
            dy = center_y - particle.y
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < radius and dist > 0.1:
                # Normalizuj směr
                nx = dx / dist
                ny = dy / dist
                
                # Síla slábne s vzdáleností
                force = force_strength * (1 - dist / radius)
                particle.apply_force(nx * force, ny * force)
    
    def explode_all(self):
        """Vybuchni všechny částice od středu"""
        center_x = SCREEN_WIDTH / 2
        center_y = SCREEN_HEIGHT / 2
        
        for particle in self.particles:
            dx = particle.x - center_x
            dy = particle.y - center_y
            dist = math.sqrt(dx*dx + dy*dy) + 0.1
            
            # Rozptyl od středu
            explosion_force = 15
            particle.vx += (dx / dist) * explosion_force
            particle.vy += (dy / dist) * explosion_force
    
    def update(self):
        """Aktualizuj všechny částice"""
        # Aktualizuj fyziku
        for particle in self.particles:
            particle.update()
            particle.check_wall_collision()
        
        # Detekuj srážky mezi částicemi (O(n²) algoritmus - jednoduché řešení)
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                self.particles[i].check_particle_collision(self.particles[j])
    
    def draw(self, surface):
        """Nakresli všechny částice"""
        for particle in self.particles:
            particle.draw(surface)
    
    def clear(self):
        """Vymaž všechny částice"""
        self.particles.clear()
    
    def get_count(self):
        """Vrátí počet aktivních částic"""
        return len(self.particles)


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Interaktivní Systém Částic - LMB: Částice | RMB: Přitažlivost | SPACE: Výbuch | C: Vyčistit")
    clock = pygame.time.Clock()
    
    particle_system = ParticleSystem()
    font = pygame.font.Font(None, 24)
    
    # Interaktivní proměnné
    mouse_force_active = False
    spawn_particles_on_click = True
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time v sekundách
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Vybuchni všechny částice
                    particle_system.explode_all()
                elif event.key == pygame.K_c:
                    # Vyčisti všechny částice
                    particle_system.clear()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Levé kliknutí
                    # Spusť několik částic v místě kliknutí
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for _ in range(3):
                        particle_system.add_particle(mouse_x, mouse_y)
                
                elif event.button == 3:  # Pravé kliknutí
                    mouse_force_active = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    mouse_force_active = False
        
        # Aplikuj přitažlivé silové pole při RMB
        if mouse_force_active:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Přitažlivá síla s poloměrem 150 pixelů
            particle_system.apply_force_field(mouse_x, mouse_y, force_strength=50, radius=150)
        
        # Aktualizuj fyziku
        particle_system.update()
        
        # Vykreslování
        screen.fill(BLACK)
        
        # Nakresli stěny (náznaky)
        pygame.draw.rect(screen, WALL_COLOR, (0, 0, SCREEN_WIDTH, 3))
        pygame.draw.rect(screen, WALL_COLOR, (0, SCREEN_HEIGHT - 3, SCREEN_WIDTH, 3))
        pygame.draw.rect(screen, WALL_COLOR, (0, 0, 3, SCREEN_HEIGHT))
        pygame.draw.rect(screen, WALL_COLOR, (SCREEN_WIDTH - 3, 0, 3, SCREEN_HEIGHT))
        
        # Nakresli částice
        particle_system.draw(screen)
        
        # Nakresli UI
        particle_count = particle_system.get_count()
        info_text = f"Částice: {particle_count} | LMB: Spusť | RMB: Přitažlivost | SPACE: Výbuch | C: Vyčistit"
        text_surface = font.render(info_text, True, WHITE)
        screen.blit(text_surface, (10, 10))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

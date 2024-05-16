import pygame
import numpy as np
import random
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tank Shell Impact Simulation")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
grey = (169, 169, 169)
yellow = (255, 255, 0)

# Define material properties and initial conditions
shell_velocity = 1000  # m/s
shell_mass = 10  # kg
steel_density = 7850  # kg/m^3
steel_yield_strength = 250e6  # Pa
steel_thickness = 0.05  # m
impact_radius = 0.01  # m

# Angle of incidence (in degrees)
angles_of_incidence = np.linspace(0, 90, 10)

# Function to calculate deformation and penetration
def calculate_penetration(angle):
    angle_rad = np.radians(angle)
    v_normal = shell_velocity * np.cos(angle_rad)
    kinetic_energy = 0.5 * shell_mass * v_normal**2

    area_of_impact = np.pi * (impact_radius**2)
    volume_of_steel = area_of_impact * steel_thickness
    mass_of_steel = volume_of_steel * steel_density
    energy_to_deform = mass_of_steel * steel_yield_strength

    penetration_depth = kinetic_energy / energy_to_deform

    return penetration_depth

# Calculate penetration for each angle
penetration_depths = [calculate_penetration(angle) for angle in angles_of_incidence]

# Simulation loop
running = True
clock = pygame.time.Clock()

# Drawing constants
plate_width = 700
plate_height = 50
plate_x = (screen_width - plate_width) / 2
plate_y = (screen_height - plate_height) / 2

def draw_plate():
    pygame.draw.rect(screen, blue, (plate_x, plate_y, plate_width, plate_height))

def draw_shell(angle, penetration, deformation_factor):
    shell_x = screen_width / 2
    shell_y = plate_y - 100
    angle_rad = np.radians(angle)
    end_x = shell_x + 100 * np.cos(angle_rad)
    end_y = shell_y + 100 * np.sin(angle_rad)

    pygame.draw.line(screen, red, (shell_x, shell_y), (end_x, end_y), 5)
    pygame.draw.circle(screen, red, (int(shell_x), int(shell_y)), 10)

    deformation_length = 30 * deformation_factor
    deformation_start_x = end_x
    deformation_start_y = end_y
    deformation_end_x = deformation_start_x + deformation_length * np.cos(angle_rad)
    deformation_end_y = deformation_start_y + deformation_length * np.sin(angle_rad)
    pygame.draw.line(screen, grey, (deformation_start_x, deformation_start_y), (deformation_end_x, deformation_end_y), 3)

    penetration_effect_x = plate_x + plate_width / 2
    penetration_effect_y = plate_y + plate_height / 2 + penetration * 100
    pygame.draw.circle(screen, black, (int(penetration_effect_x), int(penetration_effect_y)), 5)

def draw_fragments(angle, penetration):
    shell_x = screen_width / 2
    shell_y = plate_y - 100
    angle_rad = np.radians(angle)
    end_x = shell_x + 100 * np.cos(angle_rad)
    end_y = shell_y + 100 * np.sin(angle_rad)

    fragments = []
    for _ in range(10):
        fragment_angle = random.uniform(0, 2 * np.pi)
        fragment_speed = random.uniform(50, 150)
        fragments.append([end_x, end_y, fragment_angle, fragment_speed])

    return fragments

def update_fragments(fragments):
    for fragment in fragments:
        fragment[0] += fragment[3] * np.cos(fragment[2])
        fragment[1] += fragment[3] * np.sin(fragment[2])
        pygame.draw.circle(screen, yellow, (int(fragment[0]), int(fragment[1])), 3)

angle_index = 0
deformation_factors = np.linspace(0, 1, len(angles_of_incidence))
fragments = []

while running:
    screen.fill(white)
    draw_plate()

    angle = angles_of_incidence[angle_index]
    penetration = penetration_depths[angle_index]
    deformation_factor = deformation_factors[angle_index]
    draw_shell(angle, penetration, deformation_factor)

    if not fragments:
        fragments = draw_fragments(angle, penetration)
    update_fragments(fragments)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(10)

    angle_index = (angle_index + 1) % len(angles_of_incidence)
    fragments = []

pygame.quit()

# Plot the penetration depth vs angle
plt.figure(figsize=(10, 6))
plt.plot(angles_of_incidence, penetration_depths, marker='o')
plt.title('Impact of Tank Shell on Steel Plate at Various Angles of Incidence')
plt.xlabel('Angle of Incidence (degrees)')
plt.ylabel('Penetration Depth (m)')
plt.grid(True)
plt.show()

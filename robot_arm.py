"""Robot Arm - Animated articulated robot arm with PyGame."""

import math
import pygame
import sys

# Screen dimensions
SCREEN_WIDTH: int = 1024
SCREEN_HEIGHT: int = 768

# Colors
WHITE: tuple[int, int, int] = (255, 255, 255)
BROWN: tuple[int, int, int] = (139, 90, 43)
BLACK: tuple[int, int, int] = (0, 0, 0)

# Metallic palette - primary colors
DARK_STEEL: tuple[int, int, int] = (70, 75, 85)
SILVER: tuple[int, int, int] = (180, 185, 195)
CYAN_BLUE: tuple[int, int, int] = (60, 170, 210)
METALLIC_DARK: tuple[int, int, int] = (40, 42, 48)

# Metallic palette - highlight variants (lighter)
DARK_STEEL_HIGHLIGHT: tuple[int, int, int] = (100, 105, 115)
SILVER_HIGHLIGHT: tuple[int, int, int] = (210, 215, 225)
CYAN_BLUE_HIGHLIGHT: tuple[int, int, int] = (100, 200, 235)

# Metallic palette - shadow variants (darker)
DARK_STEEL_SHADOW: tuple[int, int, int] = (45, 50, 60)
SILVER_SHADOW: tuple[int, int, int] = (140, 145, 155)
CYAN_BLUE_SHADOW: tuple[int, int, int] = (35, 130, 170)

# Ground
GROUND_HEIGHT: int = 100
GROUND_Y: int = SCREEN_HEIGHT - GROUND_HEIGHT

# Base position (where the robot arm sits on the ground)
BASE_X: int = SCREEN_WIDTH // 2
BASE_Y: int = GROUND_Y

# Base dimensions
BASE_WIDTH: int = 120
BASE_HEIGHT: int = 50
BASE_SPEED: int = 5

# Arm segment 1
ARM1_LENGTH: int = 120
ARM1_WIDTH: int = 20
ARM1_ROTATION_SPEED: float = 0.03
JOINT_RADIUS: int = 8

# Arm segment 2
ARM2_LENGTH: int = 100
ARM2_WIDTH: int = 16
ARM2_ROTATION_SPEED: float = 0.03


def draw_ground(screen: pygame.Surface) -> None:
    """Draw the brown ground rectangle at the bottom of the screen."""
    pygame.draw.rect(screen, BROWN, (0, GROUND_Y, SCREEN_WIDTH, GROUND_HEIGHT))


def draw_base(screen: pygame.Surface, base_x: int) -> None:
    """Draw an industrial pedestal base with stepped shape and tread details."""
    # Bottom platform (wider)
    platform_w = BASE_WIDTH
    platform_h = 18
    platform_x = base_x - platform_w // 2
    platform_y = GROUND_Y - platform_h

    # Shadow/outline for 3D feel (offset darker shape behind)
    shadow_offset = 3
    pygame.draw.rect(
        screen,
        DARK_STEEL_SHADOW,
        (platform_x + shadow_offset, platform_y + shadow_offset, platform_w, platform_h),
    )
    pygame.draw.rect(screen, DARK_STEEL, (platform_x, platform_y, platform_w, platform_h))

    # Top pedestal (narrower, trapezoidal effect via stepped shape)
    pedestal_w = BASE_WIDTH - 30
    pedestal_h = BASE_HEIGHT - platform_h
    pedestal_x = base_x - pedestal_w // 2
    pedestal_y = platform_y - pedestal_h

    # Shadow for top pedestal
    pygame.draw.rect(
        screen,
        DARK_STEEL_SHADOW,
        (pedestal_x + shadow_offset, pedestal_y + shadow_offset, pedestal_w, pedestal_h),
    )
    pygame.draw.rect(screen, DARK_STEEL, (pedestal_x, pedestal_y, pedestal_w, pedestal_h))

    # Tread grooves on the bottom platform (horizontal lines)
    groove_color = DARK_STEEL_SHADOW
    for i in range(3):
        groove_y = platform_y + 4 + i * 5
        pygame.draw.line(
            screen, groove_color, (platform_x + 4, groove_y), (platform_x + platform_w - 4, groove_y), 1
        )

    # Bolt circles on the platform sides
    bolt_color = METALLIC_DARK
    bolt_r = 3
    bolt_y_pos = platform_y + platform_h // 2
    pygame.draw.circle(screen, bolt_color, (platform_x + 10, bolt_y_pos), bolt_r)
    pygame.draw.circle(screen, bolt_color, (platform_x + platform_w - 10, bolt_y_pos), bolt_r)

    # Outline for pedestal sections
    pygame.draw.rect(screen, BLACK, (platform_x, platform_y, platform_w, platform_h), 1)
    pygame.draw.rect(screen, BLACK, (pedestal_x, pedestal_y, pedestal_w, pedestal_h), 1)


def draw_arm1(
    screen: pygame.Surface, base_x: int, arm1_angle: float
) -> tuple[float, float]:
    """Draw arm segment 1 connected to the top of the base.

    Returns the end point (tip) of arm 1 for chaining arm 2.
    """
    # Pivot point: top-center of the base
    pivot_x = float(base_x)
    pivot_y = float(GROUND_Y - BASE_HEIGHT)

    # Calculate the four corners of the arm rectangle, rotated around pivot
    # Arm extends upward (negative Y) from pivot by default (angle=0 means straight up)
    half_w = ARM1_WIDTH / 2.0
    # Corners relative to pivot (unrotated: arm points up)
    corners = [
        (-half_w, 0.0),
        (half_w, 0.0),
        (half_w, -ARM1_LENGTH),
        (-half_w, -ARM1_LENGTH),
    ]
    cos_a = math.cos(arm1_angle)
    sin_a = math.sin(arm1_angle)
    rotated = [
        (pivot_x + cx * cos_a - cy * sin_a, pivot_y + cx * sin_a + cy * cos_a)
        for cx, cy in corners
    ]
    pygame.draw.polygon(screen, SILVER, rotated)
    pygame.draw.polygon(screen, BLACK, rotated, 2)

    # Draw dark circle at pivot joint
    pygame.draw.circle(screen, METALLIC_DARK, (int(pivot_x), int(pivot_y)), JOINT_RADIUS)

    # End point of arm 1
    end_x = pivot_x + 0.0 * cos_a - (-ARM1_LENGTH) * sin_a
    end_y = pivot_y + 0.0 * sin_a + (-ARM1_LENGTH) * cos_a
    return (end_x, end_y)


def draw_arm2(
    screen: pygame.Surface,
    arm1_end: tuple[float, float],
    arm1_angle: float,
    arm2_angle: float,
) -> None:
    """Draw arm segment 2 connected to the end of arm 1.

    arm2_angle is relative to arm 1's orientation.
    """
    pivot_x, pivot_y = arm1_end
    # Total angle in world space
    total_angle = arm1_angle + arm2_angle

    half_w = ARM2_WIDTH / 2.0
    corners = [
        (-half_w, 0.0),
        (half_w, 0.0),
        (half_w, -ARM2_LENGTH),
        (-half_w, -ARM2_LENGTH),
    ]
    cos_a = math.cos(total_angle)
    sin_a = math.sin(total_angle)
    rotated = [
        (pivot_x + cx * cos_a - cy * sin_a, pivot_y + cx * sin_a + cy * cos_a)
        for cx, cy in corners
    ]
    pygame.draw.polygon(screen, CYAN_BLUE, rotated)
    pygame.draw.polygon(screen, BLACK, rotated, 2)

    # Draw metallic dark circle at pivot joint (arm1-arm2 joint)
    pygame.draw.circle(screen, METALLIC_DARK, (int(pivot_x), int(pivot_y)), JOINT_RADIUS)


def draw_axes(screen: pygame.Surface, font: pygame.font.Font) -> None:
    """Draw X and Y coordinate axes at the base position."""
    # X axis - horizontal along ground surface
    pygame.draw.line(screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)
    x_label = font.render("X", True, BLACK)
    screen.blit(x_label, (SCREEN_WIDTH - 20, GROUND_Y + 5))

    # Y axis - vertical from base position
    pygame.draw.line(screen, BLACK, (BASE_X, 0), (BASE_X, GROUND_Y), 2)
    y_label = font.render("Y", True, BLACK)
    screen.blit(y_label, (BASE_X + 5, 5))


def main() -> None:
    """Main entry point for the robot arm application."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Robot Arm")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    base_x: int = BASE_X
    arm1_angle: float = 0.0  # radians, 0 = straight up
    arm2_angle: float = 0.0  # radians, relative to arm 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle continuous key presses for base movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            base_x -= BASE_SPEED
        if keys[pygame.K_RIGHT]:
            base_x += BASE_SPEED
        if keys[pygame.K_q]:
            arm1_angle -= ARM1_ROTATION_SPEED
        if keys[pygame.K_w]:
            arm1_angle += ARM1_ROTATION_SPEED
        if keys[pygame.K_a]:
            arm2_angle -= ARM2_ROTATION_SPEED
        if keys[pygame.K_s]:
            arm2_angle += ARM2_ROTATION_SPEED

        # Clamp base position to screen boundaries
        min_x = BASE_WIDTH // 2
        max_x = SCREEN_WIDTH - BASE_WIDTH // 2
        base_x = max(min_x, min(base_x, max_x))

        screen.fill(WHITE)
        draw_ground(screen)
        draw_axes(screen, font)
        draw_base(screen, base_x)
        arm1_end = draw_arm1(screen, base_x, arm1_angle)
        draw_arm2(screen, arm1_end, arm1_angle, arm2_angle)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

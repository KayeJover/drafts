import pygame
import sys
import random

# =========================================================
# INITIALISE PYGAME
# =========================================================

pygame.init()
pygame.mixer.init()

# =========================================================
# WINDOW
# =========================================================

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

# =========================================================
# COLOURS
# =========================================================

SKY_BLUE = (135, 206, 235)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 180, 70)
DARK_GREEN = (30, 130, 50)

# =========================================================
# MUSIC
# =========================================================

music_file = "miss_miss.mp3"

# Music starts at 1:00
MUSIC_START = 60.0

# Music stops at 1:44
MUSIC_END = 104.0

music_started = False

# =========================================================
# LYRICS
# =========================================================

# Time is measured from the moment the music starts at 1:00.
lyrics = [
    (0.0, "Oh"),
    (1.0, "nasa'n"),
    (2.0, "ka ba"),
    (3.0, "mahal"),

    (4.1, "Hinahanap"),
    (5.3, "ka na"),
    (6.5, "ng puso"),
    (7.7, "ko....."),

    (9.6, "Baby"),
    (10.3, "ikaw lang"),
    (10.8, "talaga"),

    (13.8, "Ang nami-miss"),
    (15.0, "ko sa"),
    (16.0, "tuwi-tuwina"),

    (20.2, "Sa"),
    (21.0, "tuwi-tuwina...."),

    (25.2, "At baby"),
    (26.5, "ako'y"),
    (26.9, "mag-aabang"),

    (28.9, "At dadalhin"),
    (31.2, "ka sa"),
    (31.9, "nakaraan...."),

    (35.0, "Sa"),
    (35.9, "nakaraan...")
]

# =========================================================
# GAME STATE
# =========================================================

game_over = False
lyrics_page = False

# =========================================================
# BIRD
# =========================================================

bird_x = 200
bird_y = 300
bird_radius = 20

gravity = 0.5
bird_velocity = 0

# =========================================================
# PIPES
# =========================================================

pipe_width = 80
pipe_gap = 180
pipe_speed = 4

pipes = []


def create_pipe(x):

    # Keep the first pipe centred and easier
    if x == 600:
        gap_y = 300
    else:
        gap_y = random.randint(150, 400)

    top_pipe = pygame.Rect(
        x,
        0,
        pipe_width,
        gap_y - pipe_gap // 2
    )

    bottom_pipe = pygame.Rect(
        x,
        gap_y + pipe_gap // 2,
        pipe_width,
        HEIGHT
    )

    return {
        "top": top_pipe,
        "bottom": bottom_pipe,
        "passed": False
    }


# First pipe
pipes.append(create_pipe(600))

# =========================================================
# LYRIC FONT FUNCTION
# =========================================================

def create_lyric_font(text):

    font_size = 100
    max_width = WIDTH - 80

    while font_size > 40:

        font = pygame.font.Font(
            None,
            font_size
        )

        if font.size(text)[0] <= max_width:
            return font

        font_size -= 2

    return pygame.font.Font(None, 40)


# =========================================================
# GAME LOOP
# =========================================================

running = True

while running:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # SPACE makes the bird jump
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                if not game_over:
                    bird_velocity = -8

    # =====================================================
    # NORMAL GAME
    # =====================================================

    if not game_over:

        # -------------------------------------------------
        # BIRD PHYSICS
        # -------------------------------------------------

        bird_velocity += gravity
        bird_y += bird_velocity

        # -------------------------------------------------
        # MOVE PIPES
        # -------------------------------------------------

        for pipe in pipes:

            pipe["top"].x -= pipe_speed
            pipe["bottom"].x -= pipe_speed

        # -------------------------------------------------
        # ADD NEW PIPE
        # -------------------------------------------------

        if pipes[-1]["top"].x < 400:

            pipes.append(
                create_pipe(WIDTH)
            )

        # -------------------------------------------------
        # REMOVE OLD PIPES
        # -------------------------------------------------

        pipes = [
            pipe
            for pipe in pipes
            if pipe["top"].right > 0
        ]

        # -------------------------------------------------
        # BIRD COLLISION RECTANGLE
        # -------------------------------------------------

        bird_rect = pygame.Rect(
            int(bird_x - bird_radius),
            int(bird_y - bird_radius),
            bird_radius * 2,
            bird_radius * 2
        )

        # -------------------------------------------------
        # PIPE COLLISION
        # -------------------------------------------------

        for pipe in pipes:

            if bird_rect.colliderect(
                pipe["top"]
            ):

                game_over = True

            if bird_rect.colliderect(
                pipe["bottom"]
            ):

                game_over = True

        # -------------------------------------------------
        # CEILING COLLISION
        # -------------------------------------------------

        if bird_y - bird_radius <= 0:

            game_over = True

        # -------------------------------------------------
        # GROUND COLLISION
        # -------------------------------------------------

        if bird_y + bird_radius >= HEIGHT:

            game_over = True

        # -------------------------------------------------
        # GAME OVER
        # -------------------------------------------------

        if game_over:

            # Start the song at exactly 1:00
            pygame.mixer.music.load(
                music_file
            )

            pygame.mixer.music.play(
                0,
                MUSIC_START
            )

            music_started = True

            # Immediately switch to lyric page
            lyrics_page = True

    # =====================================================
    # GAME SCREEN
    # =====================================================

    if not lyrics_page:

        # -------------------------------------------------
        # BACKGROUND
        # -------------------------------------------------

        screen.fill(SKY_BLUE)

        # -------------------------------------------------
        # DRAW PIPES
        # -------------------------------------------------

        for pipe in pipes:

            # Top pipe
            pygame.draw.rect(
                screen,
                GREEN,
                pipe["top"]
            )

            # Bottom pipe
            pygame.draw.rect(
                screen,
                GREEN,
                pipe["bottom"]
            )

            # Top cap
            top_cap = pygame.Rect(
                pipe["top"].x - 5,
                pipe["top"].bottom - 20,
                pipe_width + 10,
                20
            )

            # Bottom cap
            bottom_cap = pygame.Rect(
                pipe["bottom"].x - 5,
                pipe["bottom"].top,
                pipe_width + 10,
                20
            )

            pygame.draw.rect(
                screen,
                DARK_GREEN,
                top_cap
            )

            pygame.draw.rect(
                screen,
                DARK_GREEN,
                bottom_cap
            )

        # -------------------------------------------------
        # DRAW BIRD
        # -------------------------------------------------

        pygame.draw.circle(
            screen,
            YELLOW,
            (
                int(bird_x),
                int(bird_y)
            ),
            bird_radius
        )

        # -------------------------------------------------
        # BIRD EYE
        # -------------------------------------------------

        pygame.draw.circle(
            screen,
            WHITE,
            (
                int(bird_x + 7),
                int(bird_y - 7)
            ),
            6
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (
                int(bird_x + 9),
                int(bird_y - 7)
            ),
            3
        )

        # -------------------------------------------------
        # BIRD BEAK
        # -------------------------------------------------

        pygame.draw.polygon(
            screen,
            ORANGE,
            [
                (
                    bird_x + 18,
                    bird_y
                ),
                (
                    bird_x + 32,
                    bird_y + 5
                ),
                (
                    bird_x + 18,
                    bird_y + 10
                )
            ]
        )

    # =====================================================
    # LYRIC PAGE
    # =====================================================

    if lyrics_page:

        # -------------------------------------------------
        # WHITE BACKGROUND
        # -------------------------------------------------
        screen.fill(WHITE)

        # -------------------------------------------------
        # GET MUSIC POSITION
        # -------------------------------------------------

        music_position = (
            pygame.mixer.music.get_pos()
            / 1000.0
        )

        # -------------------------------------------------
        # STOP MUSIC AT 1:44
        # -------------------------------------------------

        if music_position >= (
            MUSIC_END - MUSIC_START
        ):

            pygame.mixer.music.stop()

        # -------------------------------------------------
        # FIND CURRENT LYRIC PHRASE
        # -------------------------------------------------

        current_lyric = ""

        for timestamp, text in lyrics:

            if music_position >= timestamp:
                current_lyric = text

        # -------------------------------------------------
        # DISPLAY CURRENT PHRASE
        # -------------------------------------------------

        if current_lyric:

            lyric_font = create_lyric_font(
                current_lyric
            )

            lyric_text = lyric_font.render(
                current_lyric,
                True,
                BLACK
            )

            lyric_rect = lyric_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2
                )
            )

            screen.blit(
                lyric_text,
                lyric_rect
            )

    # =====================================================
    # UPDATE DISPLAY
    # =====================================================

    pygame.display.flip()

    clock.tick(60)

# =========================================================
# EXIT
# =========================================================

pygame.mixer.music.stop()

pygame.quit()

sys.exit()
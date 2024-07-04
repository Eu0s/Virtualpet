import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Virtual Pet Game")

# Load images for the original cat pet
background_img = pygame.image.load("background.jpg")
cat_happy_img = pygame.image.load("happycat.png")
cat_sad_img = pygame.image.load("cat_sad.png")
cat_normal_img = pygame.image.load("cat_normal.png")
cat_sitting_img = pygame.image.load("cat_sleep.png")
cat_feeding_img = pygame.image.load("cat_feeding.png")

# Load images for the new pets (dog and bird)
dog_happy_img = pygame.image.load("dog_happy.png")
dog_normal_img = pygame.image.load("dog_normal.png")
dog_sitting_img = pygame.image.load("dog_sleep.png")
dog_feeding_img = pygame.image.load("dog_feeding.png")

cat2_happy_img = pygame.image.load("cat2_normal.png")
cat2_normal_img = pygame.image.load("cat2_normal.png")
cat2_sitting_img = pygame.image.load("cat2_sleep.png")
cat2_feeding_img = pygame.image.load("cat2_feeding.png")

# Scale images for all pets
image_size = (150, 150)
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

cat_happy_img = pygame.transform.scale(cat_happy_img, image_size)
cat_sad_img = pygame.transform.scale(cat_sad_img, image_size)
cat_normal_img = pygame.transform.scale(cat_normal_img, image_size)
cat_sitting_img = pygame.transform.scale(cat_sitting_img, image_size)
cat_feeding_img = pygame.transform.scale(cat_feeding_img, image_size)

dog_happy_img = pygame.transform.scale(dog_happy_img, image_size)
dog_normal_img = pygame.transform.scale(dog_normal_img, image_size)
dog_sitting_img = pygame.transform.scale(dog_sitting_img, image_size)
dog_feeding_img = pygame.transform.scale(dog_feeding_img, image_size)

cat2_happy_img = pygame.transform.scale(cat2_happy_img, image_size)
cat2_normal_img = pygame.transform.scale(cat2_normal_img, image_size)
cat2_sitting_img = pygame.transform.scale(cat2_sitting_img, image_size)
cat2_feeding_img = pygame.transform.scale(cat2_feeding_img, image_size)

# Set positions
image_spacing = 20
image_bottom_margin = 20
cat_x = screen_width // 2 - (image_size[0] + image_spacing) // 2

# Define colors
cream = (245, 245, 220)
hover_color = (230, 230, 210)
text_color = black = (0, 0, 0)
border_color = (150, 75, 0)

# Set font
font = pygame.font.Font(None, 36)
# Button positions and sizes
button_width = 140
button_height = 60
button_spacing = 20
button_x = 20
button_y = screen_height - button_height - 20

feed_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
sit_button_rect = pygame.Rect(button_x, button_y - (button_height + button_spacing), button_width, button_height)
pet_button_rect = pygame.Rect(button_x, button_y - 2 * (button_height + button_spacing), button_width, button_height)
switch_pet_button_rect = pygame.Rect(screen_width - button_x - button_width, screen_height - button_y - button_height, button_width, button_height)

# Function to draw rounded rectangle
def draw_rounded_rect(surface, color, rect, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

# Function to draw a button with hover effect
def draw_button(surface, rect, text, base_color, hover_color, text_color, border_color, corner_radius=10):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        color = hover_color
    else:
        color = base_color

    draw_rounded_rect(surface, color, rect, corner_radius)
    pygame.draw.rect(surface, border_color, rect, 2, border_radius=corner_radius)

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

# Function to draw text inside a box with a border
def draw_text_box(surface, text, pos, box_color, text_color, border_color, padding=10, corner_radius=10):
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(topleft=pos)
    box_rect = pygame.Rect(text_rect.left - padding, text_rect.top - padding, text_rect.width + 2 * padding,
                           text_rect.height + 2 * padding)

    draw_rounded_rect(surface, box_color, box_rect, corner_radius)
    pygame.draw.rect(surface, border_color, box_rect, 2, border_radius=corner_radius)

    surface.blit(text_surface, text_rect.topleft)
# Class for the pet
class Pet:
    def __init__(self, happy_img, normal_img, sit_img, feed_img):
            self.energy = 100
            self.happiness = 100
            self.hunger = 0
            self.is_happy = False
            self.is_sitting = False
            self.happy_timer = 0
            self.feed_timer = 0
            self.images = {
                'happy': happy_img,
                'normal': normal_img,
                'sitting': sit_img,
                'feeding': feed_img
            }
            self.current_image = normal_img

    def feed(self):
        self.hunger = max(self.hunger - random.randint(1, 4), 0)
        self.feed_timer = 120
        self.current_image = self.images['feeding']

    def sit(self):
        self.is_sitting = not self.is_sitting
        if self.is_sitting:
            self.energy = min(self.energy + 20, 100)
            self.current_image = self.images['sitting']
        else:
            self.current_image = self.images['normal']

    def pet(self):
        self.is_happy = True
        self.happy_timer = random.randint(120, 180)
        self.happiness = min(self.happiness + random.randint(1, 4), 100)
        self.current_image = self.images['happy']

    def update(self):
        if self.is_happy:
            self.happy_timer -= 1
            if self.happy_timer <= 0:
                self.is_happy = False
                self.current_image = self.images['normal'] if not self.is_sitting else self.images['sitting']
        if self.feed_timer > 0:  # Fixed indentation here
            self.feed_timer -= 1
            if self.feed_timer <= 0:
                self.current_image = self.images['normal'] if not self.is_sitting else self.images['sitting']
        if not self.is_sitting and self.feed_timer == 0:
            self.energy = max(self.energy - 0.01, 0)
            self.happiness = max(self.happiness - 0.01, 0)
            self.hunger = min(self.hunger + 0.01, 100)
# Class for the Button
class Button:
    def __init__(self, rect, text, action):
        self.rect = rect
        self.text = text
        self.action = action

    def draw(self, surface, base_color, hover_color, text_color, border_color, font):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = hover_color
        else:
            color = base_color

        draw_rounded_rect(surface, color, self.rect, 10)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=10)

        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()

# Initialize the original cat pet
pet = Pet(cat_happy_img, cat_normal_img, cat_sitting_img, cat_feeding_img)

# Initialize two more pets (dog and bird)
dog = Pet(dog_happy_img, dog_normal_img, dog_sitting_img, dog_feeding_img)
cat2 = Pet(cat2_happy_img, cat2_normal_img, cat2_sitting_img, cat2_feeding_img)

# List of all pets
pets = [pet, dog, cat2]
current_pet_index = 0
current_pet = pets[current_pet_index]

# Create buttons for the actions (Feed, Sit, Pet)
buttons = [
    Button(feed_button_rect, "Feed",  current_pet.feed),
    Button(sit_button_rect, "Sit",  current_pet.sit),
    Button(pet_button_rect, "Pet",  current_pet.pet)
]

# Create a button for switching pets
switch_pet_button = Button(switch_pet_button_rect, "Switch Pet", lambda: switch_pet())

# Function to switch between pets
# Function to switch between pets
# Function to switch between pets
def switch_pet():
    global current_pet_index, current_pet
    current_pet_index = (current_pet_index + 1) % len(pets)
    current_pet = pets[current_pet_index]
    update_button_actions()  # Update button actions after switching pets



# Function to update button actions after switching pets
def update_button_actions():
    for button in buttons:
        if button.text == "Feed":
            button.action = current_pet.feed
        elif button.text == "Sit":
            button.action = current_pet.sit
        elif button.text == "Pet":
            button.action = current_pet.pet

# Add the switch pet button to the list of buttons
buttons.append(switch_pet_button)

# Main game loop
running = True
clock = pygame.time.Clock()
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif not game_over:
            for button in buttons:
                button.handle_event(event)

    # Check for game over conditions
    if current_pet.hunger >= 100 or current_pet.energy <= 0 or current_pet.happiness <= 0:
        game_over = True

    if not game_over:
        current_pet.update()

    # Draw everything
    screen.blit(background_img, (0, 0))
    screen.blit(current_pet.current_image, (cat_x, screen_height - image_size[1] - image_bottom_margin))

    # Draw buttons
    if not game_over:
        for button in buttons:
            button.draw(screen, cream, hover_color, text_color, border_color, font)

    # Draw statistics
    draw_text_box(screen, f"Energy: {current_pet.energy:.0f}", (button_x, 20), cream, text_color, border_color)
    draw_text_box(screen, f"Hunger: {current_pet.hunger:.0f}", (button_x, 20 + font.get_linesize() + 20), cream,
                  text_color, border_color)
    draw_text_box(screen, f"Happiness: {current_pet.happiness:.0f}",
                  (button_x, 20 + 2 * (font.get_linesize() + 20)), cream, text_color, border_color)

    if game_over:
        game_over_text = font.render("Game Over", True, text_color)
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(game_over_text, game_over_rect)

    # Update the display
    pygame.display.flip()
    # Cap the frame rate
    clock.tick(60)
# Quit Pygame
pygame.quit()
sys.exit()

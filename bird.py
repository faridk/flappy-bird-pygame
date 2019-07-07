import sys, pygame, random

pygame.init()
pygame.font.init()

score_font = pygame.font.Font('fonts/04b_19/04B_19__.TTF', 100)

SIZE = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(SIZE)

class Game:
	def __init__(self):
		self.score = 0
		self.pipes = []
		self.generate_pipes(10)
		self.bird = Bird()
		self.background = pygame.image.load("background.png")
		self.background = pygame.transform.scale(self.background, (HEIGHT, HEIGHT))
		self.background_x = 0
		self.speed = 5
		self.game_over = False

	def generate_pipes(self, count):
		if (len(self.pipes) == 0):
			x = 0
		else:
			x = self.pipes[-1].x
		for i in range(count):
			x_gap = 360
			x += x_gap + i
			y_gap = 200
			random_variation = 200 # Must be less than y_gap
			random_y_offset = random.randint(0, random_variation)
			y_bottom = HEIGHT - Pipe.height + random_y_offset + y_gap
			self.pipes.append(Pipe(x, y_bottom, False))
			y_top = 0 + random_y_offset - y_gap
			self.pipes.append(Pipe(x, y_top, True))

	def dispose_pipes(self):
		for pipe in self.pipes:
			if pipe.x < 0:
				self.pipes.remove(pipe)

	# Move and generate pipes
	def move_pipes(self):
		if (len(self.pipes) > 10):
			self.dispose_pipes()
		else:
			self.generate_pipes(2)
		for pipe in self.pipes:
			pipe.x -= self.speed

	def move_background(self):
			# Draw the background
			if (self.background_x > HEIGHT):
				self.background_x = 0
			screen.blit(self.background, (self.background_x - HEIGHT, 0))
			screen.blit(self.background, (self.background_x, 0))
			screen.blit(self.background, (HEIGHT + self.background_x, 0))
			self.background_x += self.speed

	# Check if the bird is past the pipe (add 1 to the score)
	def pipe_passed(self, pipe):
		# Substract 50 to compensate for non-pixel-by-pixel movement
		if not self.game_over and pipe.x + pipe.width - 50 < self.bird.x:
			self.score += 1
		
	def draw(self):
			self.move_background()
			self.move_pipes()
			self.bird.draw()
			self.bird.fall()
			
			for pipe in self.pipes:
				pipe.draw()
				self.pipe_passed(pipe)
				if self.bird.rect.colliderect(pipe.rect):
					self.game_over = True
			
			# Handle bar movement using keys
			pressed = pygame.key.get_pressed()
			if pressed[pygame.K_SPACE] and self.bird.y > 0:
				self.bird.jump()
			
			# Draw score
			score_label = score_font.render(str(self.score), False, (255, 255, 255))
			screen.blit(score_label,(WIDTH // 2, HEIGHT // 15))
			
			# Show game over message
			game_over_label = score_font.render("Game Over", False, (255, 255, 255))
			if self.game_over:
				screen.blit(game_over_label, (WIDTH // 2 - 250, HEIGHT // 2))


class Bird:
	scale = 5
	width = 18 * scale
	height = 11 * scale
	def __init__(self):
		self.x = 50
		self.y = (HEIGHT - self.height) // 2
		self.x_velocity = 0
		self.y_velocity = 0
		self.x_acceleration = 0
		self.y_acceleration = 9.8
		self.image = pygame.image.load("bird.png")
		self.image = pygame.transform.scale(self.image, (self.width, self.height))
		# Update rect's coordinates for collision detection
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
	
	def fall(self):
		if (self.y < HEIGHT - self.height):
			self.y += 5

	def jump(self):
		self.y -= 15

	def draw(self):
			# Update rect's coordinates for collision detection
			self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
			# Draw a bird
			screen.blit(self.image, (self.x, self.y))
			# pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))


class Pipe:
	scale = 7
	width = 15 * scale
	height = 64 * scale
	def __init__(self, x, y, flipped):
		self.x = x
		self.y = y
		self.image = pygame.image.load("long_pipe.png")
		self.image = pygame.transform.scale(self.image, (self.width, self.height))
		if flipped:
			self.image = pygame.transform.flip(self.image, False, True)
		# Update rect's coordinates for collision detection
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
	
	def draw(self):
		# Update rect's coordinates for collision detection
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		# Draw a pipe
		screen.blit(self.image, (self.x, self.y))


black = (0, 0, 0)
white = (255, 255, 255)
# Colors
background_color = black

game = Game()

while True:
	for event in pygame.event.get():
		# Handle exit
		if event.type == pygame.QUIT:
			pygame.quit() # Close the window
			sys.exit()

	game.draw()

	pygame.display.flip() # Updates the display
	screen.fill(background_color) # Clear the screen, leave no smudges

from __future__ import division
import pygame
import random
import time
import sys
import array
pygame.init()

sw = 700
sh = 512

started = False
score = 0
nSeconds = 30
eCount = 0
oCount = 0
nCount = 0
soundOn = True
soundEffectsOn = True
timer = 0
version = random.randint(0, 18)
gameover = False
dropping = False

win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("athus")

walkRight = [pygame.image.load('athusr-1.png'), pygame.image.load('athusr-2.png'), pygame.image.load('athusr-3.png'), pygame.image.load('athusr-4.png'), pygame.image.load('athusr-5.png'), pygame.image.load('athusr-6.png'), pygame.image.load('athusr-7.png'), pygame.image.load('athusr-8.png')]
walkLeft = [pygame.image.load('athusl-1.png'), pygame.image.load('athusl-2.png'), pygame.image.load('athusl-3.png'), pygame.image.load('athusl-4.png'), pygame.image.load('athusl-5.png'), pygame.image.load('athusl-6.png'), pygame.image.load('athusl-7.png'), pygame.image.load('athusl-8.png')]
bg = [pygame.image.load('bgp-1.jpg'), pygame.image.load('bgp-2.jpg'), pygame.image.load('bgp-3.jpg'), pygame.image.load('bgp-4.jpg'), pygame.image.load('bgp-5.jpg'), pygame.image.load('bgp-6.jpg'), pygame.image.load('bgp-7.jpg'), pygame.image.load('bgp-8.jpg'), pygame.image.load('bgp-9.jpg'), pygame.image.load('bgp-10.jpg'), pygame.image.load('bgp-11.jpg'), pygame.image.load('bgp-12.jpg'), pygame.image.load('bgp-13.jpg'), pygame.image.load('bgp-14.jpg'), pygame.image.load('bgp-15.jpg'), pygame.image.load('bgp-16.jpg'), pygame.image.load('bgp-17.jpg'), pygame.image.load('bgp-18.jpg'), pygame.image.load('bgp-19.jpg')]
charRight = pygame.image.load('athus_stand-r.png')
charLeft = pygame.image.load('athus_stand-l.png')
lShoot = pygame.image.load('athus_shoot-l.png')
rShoot = pygame.image.load('athus_shoot-r.png')
athus_big = pygame.image.load('athus_big.png')
oleste_big = pygame.image.load('oleste_big.png')
etro_big = [pygame.image.load('etro_big_def.png'), pygame.image.load('etro_big_atk.png')]


athusLaserSound = pygame.mixer.Sound('athus_laser.wav')
etroLaserSound = pygame.mixer.Sound('etro_laser.wav')
athusHitSound = pygame.mixer.Sound('athus_hit.wav')
athusDeadSound = pygame.mixer.Sound('athus_dead.wav')
olesteHitSound = pygame.mixer.Sound('oleste_hit.wav')
olesteDeadSound = pygame.mixer.Sound('oleste_dead.wav')
etroHitSound = pygame.mixer.Sound('etro_hit.wav')
etroDeadSound = pygame.mixer.Sound('etro_dead.wav')
jungleMusic = pygame.mixer.music.load('blue_jungle.mp3')

pygame.mixer.music.play(-1)

pygame.mixer.music.set_volume(.7)
athusLaserSound.set_volume(.5)
etroLaserSound.set_volume(.5)
athusHitSound.set_volume(.5)
athusDeadSound.set_volume(.5)
olesteHitSound.set_volume(.5)
olesteDeadSound.set_volume(.5)
etroHitSound.set_volume(.5)

# pygame.mixer.music.set_volume(0)
# athusLaserSound.set_volume(0)
# etroLaserSound.set_volume(0)
# athusHitSound.set_volume(0)
# athusDeadSound.set_volume(0)
# olesteHitSound.set_volume(0)
# olesteDeadSound.set_volume(0)
# etroHitSound.set_volume(0)

clock = pygame.time.Clock()

class player(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = 5
		self.isJump = False
		self.jumpCount = 10
		self.left = True
		self.right = False
		self.walkCount = 0
		self.timeSinceHit = 0
		self.standing = True
		self.isShooting = False
		self.healthboxColor = (0, 250, 0)
		self.isInvincible = False
		self.visible = True
		self.hitbox = (self.x + 16, self.y + 10, 28, 50)
		self.healthbox = (sw/2 - 128, 20, 256, 8)
		self.health = 16

	def draw(self,win):
		if self.walkCount + 1 >= 24:	# 27 fps because there are 9 frames
			self.walkCount = 0

		if not (self.standing):			# if athus is not standing, then athus is
			if self.left:				# moving left, or
				win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
				self.walkCount += 1
			elif self.right:			# moving right, or
				win.blit(walkRight[self.walkCount//3], (self.x,self.y))
				self.walkCount += 1
		elif (self.isShooting):			# shooting
			if self.left:
				win.blit(lShoot, (self.x, self.y))
			else:
				win.blit(rShoot, (self.x, self.y))
			self.isShooting = False
		else:							# else, athus is standing
			if self.right:
				win.blit(charRight, (self.x,self.y))
			elif self.left:
				win.blit(charLeft, (self.x,self.y))

		self.hitbox = (self.x + 16, self.y + 10, 28, 50)
		pygame.draw.rect(win, (255,255,255), (sw/2 - 131, 18, 261, 12), 10)
		pygame.draw.rect(win, (255,0,0), self.healthbox, 8)
		pygame.draw.rect(win, self.healthboxColor, (222, 20, (self.health * 16), 8), 8)
		# pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

	def hit(self):
		global gameover
		self.timeSinceHit = pygame.time.get_ticks()
		if self.health > 0:
			if self.health <= 9 and self.health > 5:
				self.healthboxColor = (255, 204, 0)
			elif self.health <= 5 and self.health > 0:
				self.healthboxColor = (247, 137, 46)
			else:
				self.healthboxColor = (0, 250, 0)

			if not self.isInvincible:
				print("i got hit :(")
				self.health = self.health -1
				athusHitSound.play()
				
		
		elif self.health == 0:
			self.healthboxColor = (255, 0, 0)
			athusDeadSound.play()
			athus.isInvincible = True
			timedead = timer
			gameover = True

class projectile(object):
	def __init__(self, x, y, radius, length, color, facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.length = length
		self.color = color
		self.facing = facing
		self.i = 1
		self.vel = 8 * facing

	def draw(self, win):
		
		pygame.draw.circle(win, (255, 255, 0), (round(self.x), round(self.y)), self.radius)

class projectile2(object):
	def __init__(self, x, y, radius, length, color, facing):
		self.x = x 
		self.y = y
		self.radius = radius
		self.length = length
		self.color = color
		self.facing = facing
		self.vel = 6 * facing
		self.i = 1

	def draw(self, win):
		
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy1(object):
	walkRight = [pygame.image.load('olester-1.png'), pygame.image.load('olester-2.png'), pygame.image.load('olester-3.png'), pygame.image.load('olester-4.png'), pygame.image.load('olester-5.png'), pygame.image.load('olester-6.png'), pygame.image.load('olester-7.png'), pygame.image.load('olester-8.png'), pygame.image.load('olester-9.png'), pygame.image.load('olester-10.png')]
	walkLeft = [pygame.image.load('olestel-1.png'), pygame.image.load('olestel-2.png'), pygame.image.load('olestel-3.png'), pygame.image.load('olestel-4.png'), pygame.image.load('olestel-5.png'), pygame.image.load('olestel-6.png'), pygame.image.load('olestel-7.png'), pygame.image.load('olestel-8.png'), pygame.image.load('olestel-9.png'), pygame.image.load('olestel-10.png')]
	ocharRight = pygame.image.load('olest_stand-r.png')
	# ocharLeft = pygame.image.load('olest_stand-l.png')
	
	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.onScreen = False
		self.width = width
		self.height = height
		self.end = end
		self.path = [self.x, end]
		self.walkCount = 0
		self.vel = 3
		self.hitbox = (self.x + 12, self.y + 10, 34, 50)
		self.health = 10
		self.visible = True

	def draw(self, win):
		self.move()
		if self.visible:
			if self.walkCount +1 >= 30:	# 30 fps because there are 10 frames
				self.walkCount = 0

			if self.vel > 0:			# walking to the right
				win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
			else:						# walking to the left
				win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1

			self.hitbox = (self.x + 12, self.y + 10, 34, 50)
			pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 5))
			pygame.draw.rect(win, (0,250,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50//10) * (10 - self.health)), 5))
			# pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
			# pygame.draw.rect(win, (0,0,0), (109, 390, 34, 50), 2)

	def move(self):
		if not self.onScreen and not self.x < 0:
			self.onScreen = True
			self.path = [0, self.end]

		if self.vel > 0:
			if self.x < self.path[1] + self.vel:
				self.x += self.vel
			else:
				self.vel = self.vel * -1
				self.x += self.vel
				self.walkCount = 0
		else:
			if self.x > self.path[0] - self.vel:
				self.x += self.vel
			else:
				self.vel = self.vel * -1
				self.x += self.vel
				self.walkCount = 0

	def hit(self):
		global oCount
		global olesteOn
		global score
		if self.health > 1:
			self.health -= 1
			olesteHitSound.play()
		else:
			olesteDeadSound.play()
			self.visible = False
			olesteOn = False
			oCount -= 1
			score += 10
		print('hit!')

class enemy2(object):
	walkRight = [pygame.image.load('etror-1.png'), pygame.image.load('etror-2.png'), pygame.image.load('etror-3.png'), pygame.image.load('etror-4.png'), pygame.image.load('etror-5.png'), pygame.image.load('etror-6.png'), pygame.image.load('etror-7.png'), pygame.image.load('etror-8.png'), pygame.image.load('etror-9.png'), pygame.image.load('etror-10.png'), pygame.image.load('etror-11.png'), pygame.image.load('etror-12.png'), pygame.image.load('etror-13.png'), pygame.image.load('etror-14.png'), pygame.image.load('etror-15.png'), pygame.image.load('etror-16.png'), pygame.image.load('etror-17.png'), pygame.image.load('etror-18.png'), pygame.image.load('etror-19.png')]
	walkLeft = [pygame.image.load('etrol-1.png'), pygame.image.load('etrol-2.png'), pygame.image.load('etrol-3.png'), pygame.image.load('etrol-4.png'), pygame.image.load('etrol-5.png'), pygame.image.load('etrol-6.png'), pygame.image.load('etrol-7.png'), pygame.image.load('etrol-8.png'), pygame.image.load('etrol-9.png'), pygame.image.load('etrol-10.png'), pygame.image.load('etrol-11.png'), pygame.image.load('etrol-12.png'), pygame.image.load('etrol-13.png'), pygame.image.load('etrol-14.png'), pygame.image.load('etrol-15.png'), pygame.image.load('etrol-16.png'), pygame.image.load('etrol-17.png'), pygame.image.load('etrol-18.png'), pygame.image.load('etrol-19.png')]
	
	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.onScreen = False
		self.left = False
		self.right = True
		self.facing = 1
		self.width = width
		self.height = height
		self.end = end
		self.path = [self.x, end]
		self.walkCount = 0
		self.vel = 1
		self.hitbox = (self.x + 16, self.y + 18, 36, 44)
		self.health = 20
		self.visible = True

	def draw(self, win):
		self.move()
		if self.visible:
			if self.walkCount +1 >= 57:
				self.walkCount = 0

			if self.vel > 0:		# walking to the right
				win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
				self.right = True
				self.left = False
				self.facing = 1
			else:					# walking to the left
				win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
				self.left = True
				self.right = False
				self.facing = -1

			self.hitbox = (self.x + 16, self.y + 18, 36, 44)
			pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 5))
			pygame.draw.rect(win, (0,250,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50/20) * (20 - self.health)), 5))
			# pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

	def move(self):
		if not self.onScreen and not self.x < 0:	# once the dino is fully on the screen, this 
			self.onScreen = True					# prevents it from going off again
			self.path = [0, self.end]

		if (self.walkCount//3) >= 9 and (self.walkCount//3) <= 13:	# when etro gets to the 'fire' frames of
			if (self.walkCount//3) == 12:							# his animation sequence, he stays still
				pass
		else:
			if self.vel > 0:							# when velocity is positive, etro is moving right
				if self.x < self.path[1] + self.vel:
					self.x += self.vel
				else:
					self.vel = self.vel * -1
					self.x += self.vel
					self.walkCount = 0
			else:										# when velocity is negative, etro is moving left
				if self.x > self.path[0] - self.vel:
					self.x += self.vel
				else:
					self.vel = self.vel * -1
					self.x += self.vel
					self.walkCount = 0

	def hit(self):
		global eCount
		global etroOn
		global score
		if self.health > 1:
			self.health -= 1
			etroHitSound.play()

		else:
			etroDeadSound.play()
			self.visible = False
			etroOn = False
			eCount -= 1
			score += 20
			

		print('hit!')

class friend(object):
	fly = [pygame.image.load('nodon-1.png'), pygame.image.load('nodon-2.png'), pygame.image.load('nodon-3.png'), pygame.image.load('nodon-4.png'), pygame.image.load('nodon-5.png'), pygame.image.load('nodon-6.png'), pygame.image.load('nodon-7.png')]

	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.onScreen = False
		self.visible = True
		self.left = False
		self.right = True
		self.width = width
		self.height = height
		self.end = end
		self.path = [self.x, end]
		self.walkCount = 0
		self.vel = -4
		self.dropcoord = 0

	def draw(self, win):
		self.move()
		if self.visible:
			if self.walkCount + 1 >= 21:	# 21 fps because there are 7 frames
				self.walkCount = 0
			if self.vel < 0:			# walking to the left
				win.blit(self.fly[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
			
	def move(self):
		global dropping
		global nodonOn
		global nCount
		if not self.onScreen:	# once the dino is fully on the screen, this 
			self.onScreen = True					# prevents it from going off again
			self.path = [self.x, self.end]

		if self.x <= self.dropcoord - self.vel and self.x >= self.dropcoord + self.vel:
			dropping = True
		if self.vel < 0:
			self.x += self.vel
		if self.x < -32:
			dropping = False
		if self.x + self.width <= 1:
			nodonOn = False
			self.visible = False
			nCount -= 1

class heart(object):
	heartimg = pygame.image.load('heart.png')

	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.land = 410
		self.yvel = 6
		self.xvel = -4
		self.dropped = False
		self.hitbox = (self.x + 8, self.y + 8, 32, 32)

	def draw(self, win):
		self.move()
		win.blit(self.heartimg, (self.x, self.y))
		pygame.draw.rect(win, (255, 255, 255), self.hitbox, 2)

	def move(self):
		if dropping:
			self.dropped = True

		if not self.dropped:
			self.x += self.xvel
		elif self.dropped and self.y < self.land:
			self.y += self.yvel


def redrawWindow():
	global score
	global started
	global version
	win.blit(bg[version], (0,0))
	if score < 0:
		score = 0
	text = font.render(str(score), 1, (255, 255, 255))
	win.blit(text, (sw - 100, 15))
	athus.draw(win)
	oleste.draw(win)
	etro.draw(win)
	if timer > 20 and started:
		# nodon.draw(win)
		# heart_health.draw(win)
		pass
	for bullet in bullets:
		bullet.draw(win)
	for laser in lasers:
		laser.draw(win)
	pygame.display.update()
	started = True

def show_go_screen():
	global timer
	global score
	draw_text(win, "ATHUS", 100, sw / 2, sh / 3)
	draw_text(win, "Press [ENTER] to begin", 18, sw / 2, sh * 2 / 3 + 20)
	draw_text(win, "Press [I] for Instructions", 18, sw / 2, sh * 2 / 3 - 20)
	draw_text(win, "Press [A] for About", 18, sw / 2, sh * 2 / 3 + 60)
	draw_text(win, "Press [T] for Top Scores", 18, sw / 2, sh * 2 / 3 + 100)


	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
				timer = 0
				score = 0
				waiting = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
				instructionScreen()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
				aboutScreen(0)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
				show_top_scores()

def aboutScreen(page):
	global timer
	global score
	global waiting
	i = 0
	start_time = pygame.time.get_ticks()

	win.fill((0,0,0))
	draw_text(win, "About this Game", 70, sw / 2, sh / 16)

	if page == 0:
		win.blit(athus_big, (40, 150))
		text_line(win, "Athus, the creature after which this game", 20, 180, sh / 16 * 6)
		text_line(win, "is named, is a light-footed Compsagnathus", 20, 180, sh / 16 * 7)
		text_line(win, "with a quick-fire laser and a mighty need", 20, 180, sh / 16 * 8)
		text_line(win, "to do some damage. And though he is only 6lbs, do not", 20, 37, sh / 16 * 9)
		text_line(win, "underestimate his grit. He survived the Cretaceous - ", 20, 37, sh / 16 * 10)
		text_line(win, "Paleogene extinction event and knows no fear.", 20, 37, sh / 16 * 11)

		draw_text(win, "PRESS [2] FOR PAGE 2", 15, sw / 2, sh /16 * 14)

	elif page == 1:
		win.blit(oleste_big, (520, 280))
		text_line(win, "Oleste is a voracious theropod from the late Jurassic", 20, 37, sh / 16 * 5)
		text_line(win, "period. He is something of an enigma; to date, Ornit-", 20, 37, sh / 16 * 6)
		text_line(win, "holestes is known only from a single partial skeleton", 20, 37, sh / 16 * 7)
		text_line(win, "with a badly crushed skull that was unearthed in Wyo-", 20, 37, sh / 16 * 8)
		text_line(win, "ming, 1900. That being said, it doesn't", 20, 37, sh / 16 * 9)
		text_line(win, "take a paleontologist to see that those", 20, 37, sh / 16 * 10)
		text_line(win, "teeth are for bitin'. Keep an eye on him.", 20, 37, sh / 16 * 11)
		
		draw_text(win, "PRESS [3] FOR PAGE 3", 15, sw / 2, sh /16 * 14)
		draw_text(win, "PRESS [B] TO GO BACK", 15, sw / 2, sh /16 * 13)

	elif page == 2:

		# while pygame.time.get_ticks() - start_time > .5:
		# 	print("entered while")
		# 	win.blit(etro_big[i % 2], (40, 200))
		# 	i += 1
		# 	start_time = pygame.time.get_ticks()

		win.blit(etro_big[0], (40, 200))
		text_line(win, "Etro never ceases to amaze. As a dimetrodon, the very", 20, 37, sh / 15 * 5)
		text_line(win, "first synapsid creature ever discovered, he harbors a", 20, 37, sh / 15 * 6)
		text_line(win, "vast amount of energy. His ability to harness the po-", 20, 37, sh / 15 * 7)
		text_line(win, "wer of the sun through his sail", 20, 310, sh / 15 * 8)
		text_line(win, "makes him quite the formidable", 20, 310, sh / 15 * 9)
		text_line(win, "adversary. Don't turn your back", 20, 310, sh / 15 * 10)
		text_line(win, "towards this Cisuralian relic.", 20, 310, sh / 15 * 11)

		draw_text(win, "PRESS [B] TO GO BACK", 15, sw / 2, sh /16 * 14)


	draw_text(win, "PRESS [ENTER] TO PLAY", 15, sw / 2, sh /16 * 15)

	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				timer = 0
				score = 0
				waiting = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
				aboutScreen(0)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
				aboutScreen(1)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
				aboutScreen(2)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_b and page >= 1:
				aboutScreen(page - 1)

def animateEtro():
	i = 0
	start_time = pygame.time.get_ticks()

	while start_time - pygame.time.get_ticks() > 2000:
			win.blit(etro_big[i % 2], (40, 300))
			i += 1
			start_time = pygame.time.get_ticks()

def instructionScreen():
	global timer
	global score
	win.fill((0,0,0))
	draw_text(win, "KEYS", 100, sw / 2, sh / 5 - 20)
	draw_text(win, "[^]", 30, 225, sh / 5 * 2)	
	draw_text(win, "jump", 30, 475, sh / 5 * 2)	
	draw_text(win, "[<]  [>]", 30, 225, sh / 5 * 2 + 30)
	draw_text(win, "move", 30, 475, sh / 5 * 2 + 30)
	draw_text(win, "[SPACE]", 30, 225, sh / 5 * 2 + 60)
	draw_text(win, "shoot", 30, 475, sh / 5 * 2 + 60)
	draw_text(win, "[P]", 30, 225, sh / 5 * 2 + 90)
	draw_text(win, "pause", 30, 475, sh / 5 * 2 + 90)
	draw_text(win, "[M]", 30, 225, sh / 5 * 2 + 120)
	draw_text(win, "mute music", 30, 475, sh / 5 * 2 + 120)
	draw_text(win, "[N]", 30, 225, sh / 5 * 2 + 150)
	draw_text(win, "mute sound effects", 30, 475, sh / 5 * 2 + 150)
	draw_text(win, "Press [ENTER] to begin", 30, sw / 2, sh / 5 * 2 + 200)

	pygame.display.flip()

	for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                timer = 0
                score = 0
                waiting = False

def show_top_scores():
	global version
	win.blit(bg[version], (0,0))
	win.fill((0,0,0,128))
	draw_text(win, "TOP SCORES", 100, sw / 2, sh / 5 - 30)
	topscores = set(open('topscores.txt').read().split())
	print(topscores)
	scorelist = []

	for singlescore in topscores:
		singlescore_int = int(singlescore)
		array = singlescore_int
		scorelist.append(singlescore_int)

		print(singlescore)
	print(array)

	max_val = max(scorelist)
	min_val = min(scorelist)
	med_val = 0

	for item in scorelist:
		if (item != max_val and item != min_val):
			med_val = item

	print("max: " + str(max_val))
	print("min: " + str(min_val))
	print("med: " + str(med_val))

	draw_text(win, "1. ", 40, 275, sh / 5 * 2)
	draw_text(win, str(max_val), 40, 450, sh / 5 * 2)
	draw_text(win, "2. ", 40, 275, sh / 5 * 2.5)
	draw_text(win,str(med_val), 40, 450, sh / 5 * 2.5)
	draw_text(win, "3. ", 40, 275, sh / 5 * 3)
	draw_text(win, str(min_val), 40, 450, sh / 5 * 3)
	draw_text(win, "PRESS [ENTER] TO RESTART", 30, sw / 2, sh / 5 * 4)

	pygame.display.flip()




def show_gameover_screen():
	
	global score
	global timer
	global started
	
	#------------------------------------------------
	topscores = set(open('topscores.txt').read().split())
	print(topscores)
	scorelist = []

	for singlescore in topscores:
		singlescore_int = int(singlescore)
		array = singlescore_int
		scorelist.append(singlescore_int)

		print(singlescore)
	print(array)

	max_val = max(scorelist)
	min_val = min(scorelist)
	med_val = 0

	for item in scorelist:
		if (item != max_val and item != min_val):
			med_val = item

	print("max: " + str(max_val))
	print("min: " + str(min_val))
	print("med: " + str(med_val))

	if score > min_val:
		scorelist.append(score)
		scorelist.remove(min_val)

	print(scorelist)

	file = open("topscores.txt", "r+")
	file.truncate(0)
	for item in scorelist:
		file.write(str(item) + "\n")
	file.close()
#------------------------------------------------
	global version
	started = False
	draw_text(win, "GAME OVER", 125, sw / 2, sh / 2 - 125)
	if score > min_val:
		draw_text(win, "NEW HIGH SCORE: " + str(score), 50, sw / 2, sh / 2)

	draw_text(win, "PRESS [T] TO SEE TOP SCORES", 30, sw / 2, sh / 3 * 2 - 20)
	draw_text(win, "PRESS [ENTER] TO PLAY", 30, sw / 2, sh / 3 * 2 + 20)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				version = random.randint(0, 18)
				started = True
				etro.x = -120
				oleste.x = -120
				#nodon.x = 828
				athus.health = 16
				score = -100
				waiting = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
				show_top_scores()

def paused():
	global pause
	global keys
	draw_text(win, "PAUSED", 125, sw / 2, sh / 2 - 125)
	draw_text(win, "PRESS [P] TO UNPAUSE", 50, sw / 2, sh / 2 + 20)
	pygame.display.flip()

	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
				pause = False

		pygame.display.update()
		clock.tick(15)  

font_name = pygame.font.match_font('couriernewttf')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def text_line(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surf.blit(text_surface, text_rect)



athus = player(600, 380, 64, 64)
olesteOn = False
nodonOn = False
etroOn = False
display_damage = False
addscore = 0
timescore = 0
time_since_hit = 0
shootLoop = 0
laserLoop = 0
bullets = []
lasers = []
pause = False

dto = 0
dte = 0
dtn = 0
show_go_screen()

#mainloop

font = pygame.font.SysFont('couriernewttf', 30)
run = True
while run:

	t0e = time.clock()
	t0n = time.clock()
	t0o = time.clock()
	

	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

	clock.tick(36)

	if gameover:
		show_gameover_screen()
		gameover = False
		score = -100
		athus.health = 16
		etro.health = 20
		oleste.health = 10
		athus.hit()
		athus.draw(win)
		pygame.display.update()
		#input()

	if not etroOn:
		if dte < nSeconds and eCount > 1:
			t1 = time.clock()
			dte = t1 - t0e
		else:
			etro = enemy2(-80, 384, 64, 64, sw - 74)
			etroOn = True
			etro.visible = True
			eCount += 1

	if not olesteOn:
		if dto < nSeconds and oCount > 1:
			t1 = time.clock()
			dto = t1 - t0o
		else:
			oleste = enemy1(-80, 380, 64, 64, sw - 74)
			olesteOn = True
			oleste.visible = True
			oCount += 1

	if not nodonOn:
		if timer < 20 or nCount > 1:
			pass
		else:
			# nodon = friend(828, 80, 128, 96, -128)
			# nodon.dropcoord = random.randint(nodon.width, sw - nodon.width)
			# print('drop coordinate: ', nodon.dropcoord)
			# heart_health = heart(nodon.x + 18, nodon.y + 48, 32, 32)
			nodonOn = True
			#nodon.visible = True
			nCount += 1
			timer = 0


	timealive = round(pygame.time.get_ticks() / 1000) - 4
	# print(timealive)

	if athus.health > 0:
		if addscore < timealive:
			adding = timealive - addscore
			addscore = timealive
			timescore = timescore + adding
			if started:
				score += adding
				timer += adding	
			elif not started:
				score = 0
				timer = 0		
	

		

	if pygame.time.get_ticks() - athus.timeSinceHit > 500:
		athus.isInvincible = False

	if etro.visible:
		if athus.hitbox[1] < etro.hitbox[1] + etro.hitbox[3] and athus.hitbox[1] + athus.hitbox[3] > etro.hitbox[1]:
			if athus.hitbox[0] + athus.hitbox[2] > etro.hitbox[0] and athus.hitbox[0] < etro.hitbox[0] + etro.hitbox[2]:
				display_damage = True
				athus.hit()
				time_since_hit = pygame.time.get_ticks()
				athus.isInvincible = True

	if oleste.visible:
		if athus.hitbox[1] < oleste.hitbox[1] + oleste.hitbox[3] and athus.hitbox[1] + athus.hitbox[3] > oleste.hitbox[1]:
			if athus.hitbox[0] + athus.hitbox[2] > oleste.hitbox[0] and athus.hitbox[0] < oleste.hitbox[0] + oleste.hitbox[2]:
				display_damage = True
				athus.hit()
				time_since_hit = pygame.time.get_ticks()
				athus.isInvincible = True

	if shootLoop > 0:
		shootLoop += 1
	if shootLoop > 10:
		shootLoop = 0

	if laserLoop > 0:
		laserLoop += 1
	if laserLoop > 5:
		laserLoop = 0

	for bullet in bullets:
		if etroOn:
			if etro.visible:
				if bullet.y - bullet.radius < etro.hitbox[1] + etro.hitbox[3] and bullet.y + bullet.radius > etro.hitbox[1]:
					if bullet.x + bullet.radius > etro.hitbox[0] and bullet.x - bullet.radius  < etro.hitbox[0] + etro.hitbox[2]:
						etro.hit()
						score += 1
						if len(bullets) > 0:
							bullets.pop(bullets.index(bullet))

		if olesteOn:
			if oleste.visible:
				if bullet.y - bullet.radius < oleste.hitbox[1] + oleste.hitbox[3] and bullet.y + bullet.radius > oleste.hitbox[1]:
					if bullet.x + bullet.radius > oleste.hitbox[0] and bullet.x - bullet.radius  < oleste.hitbox[0] + oleste.hitbox[2]:
						oleste.hit()
						score += 1
						if len(bullets) > 0:
							try:
								bullets.pop(bullets.index(bullet))
							except(ValueError):
								print('empty list error: ')
								# print('bullet index:')
								# print(bullets.index(bullet))
								print('bullet.x, bullet.y')
								print(bullet.x, bullet.y)
								print('oleste.hitbox: ( x, y, width, height): ')
								print(oleste.hitbox[0])
								print(oleste.hitbox[1])
								print(oleste.hitbox[2])
								print(oleste.hitbox[3])
								print('oleste.health')
								print(oleste.health)			

		if bullet.x < sw and bullet.x > 0:
			bullet.x += bullet.vel
		else:
			if len(bullets) > 0:
				try:
					bullets.pop(bullets.index(bullet))
				except(ValueError):
					print('empty list error: ')
					# print('bullet index:')
					# print(bullets.index(bullet))
					print('bullet.x, bullet.y')
					print(bullet.x, bullet.y)
					print('oleste.hitbox: ( x, y, width, height): ')
					print(oleste.hitbox[0])
					print(oleste.hitbox[1])
					print(oleste.hitbox[2])
					print(oleste.hitbox[3])
					print('oleste.health')
					print(oleste.health)			

	for laser in lasers:
		if athus.hitbox[1] < laser.y + laser.radius and athus.hitbox[1] + athus.hitbox[3] > laser.y:
			if athus.hitbox[0] + athus.hitbox[2] > laser.x + laser.radius and athus.hitbox[0] < laser.x + laser.radius:
				display_damage = True
				athus.hit()
				athus.isInvincible = True
				if len(lasers) > 0:
					lasers.pop(lasers.index(laser))
				

		if laser.x < sw and laser.x > 0:
			laser.x += laser.vel
		else:
			lasers.pop(lasers.index(laser))

	keys = pygame.key.get_pressed()

	if (etro.walkCount//3) == 12 and laserLoop ==0:
		i = 0
		if etro.left:
			efacing = -1
			i = 2
		else:
			efacing = 1
			i = 60
		if len(lasers) < 3:
			lasers.append(projectile2(etro.x + i, etro.y + 52, 3, 1, (179,255,255), efacing))
			laserLoop = 1
			etroLaserSound.play()

	if keys[pygame.K_SPACE] and shootLoop == 0:
		i = 0
		athus.isShooting = True
		if athus.left:
			facing = -1
			i = 2
		else:
			i = 62
			facing = 1

		if len(bullets) < 3:
			athusLaserSound.play()
			bullets.append(projectile(athus.x + i, athus.y + 30, 2, 200, (255,0,0), facing))
			shootLoop = 1

	if keys[pygame.K_m]:
		if soundOn:
			pygame.mixer.music.set_volume(0)
			# athusLaserSound.set_volume(0)
			# etroLaserSound.set_volume(0)
			# athusHitSound.set_volume(0)
			# athusDeadSound.set_volume(0)
			# olesteHitSound.set_volume(0)
			# olesteDeadSound.set_volume(0)
			# etroHitSound.set_volume(0)
			# etroDeadSound.set_volume(0)
			soundOn = False

		elif not soundOn:
			pygame.mixer.music.set_volume(.7)
			# athusLaserSound.set_volume(.5)
			# etroLaserSound.set_volume(.5)
			# athusHitSound.set_volume(.5)
			# athusDeadSound.set_volume(.5)
			# olesteHitSound.set_volume(.5)
			# olesteDeadSound.set_volume(.5)
			# etroHitSound.set_volume(.5)
			soundOn = True

	if keys[pygame.K_n]:
		if soundEffectsOn:
			athusLaserSound.set_volume(0)
			etroLaserSound.set_volume(0)
			athusHitSound.set_volume(0)
			athusDeadSound.set_volume(0)
			olesteHitSound.set_volume(0)
			olesteDeadSound.set_volume(0)
			etroHitSound.set_volume(0)
			etroDeadSound.set_volume(0)
			soundEffectsOn = False

		elif not soundEffectsOn:
			athusLaserSound.set_volume(.5)
			etroLaserSound.set_volume(.5)
			athusHitSound.set_volume(.5)
			athusDeadSound.set_volume(.5)
			olesteHitSound.set_volume(.5)
			olesteDeadSound.set_volume(.5)
			etroHitSound.set_volume(.5)
			soundEffectsOn = True

	if keys[pygame.K_p]:
		pause = True
		paused()
		
	# while pause:
	# 	for event in pygame.event.get():
	# 		if event.type == KEYUP:
	# 			if event.key == K_p:
	# 				pause = False



	if keys[pygame.K_LEFT] and athus.x > athus.vel:
		athus.x -= athus.vel
		athus.left = True
		athus.right = False
		athus.standing = False

	elif keys[pygame.K_RIGHT] and athus.x < sw - athus.width - athus.vel:
		athus.x += athus.vel
		athus.right = True
		athus.left = False
		athus.standing = False

	else:
		athus.standing = True
		athus.walkCount = 0

	if not (athus.isJump):
		if keys[pygame.K_UP]:
			athus.isJump = True
			
	else:
		if athus.jumpCount >= -10:
			neg = 1
			if athus.jumpCount < 0:
				neg = -1
			athus.y -= (athus.jumpCount ** 2) * 0.5 * neg
			athus.jumpCount -= 1

		else:
			athus.isJump = False
			athus.jumpCount = 10

	redrawWindow()

pygame.quit()
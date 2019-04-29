import pygame
import random
import time
pygame.init()

#TO DO
#figure out why enemies disappear at certain time
#add sound to etro's laser
#create quetzlcoatlus sprite
#create something for healing
#collision for healing
#game start screen
#music mute button
#what happens when you die?

sw = 700
sh = 512

# nSeconds = 30
# t0e = time.clock()
# dto = 0
# t0o = time.clock()
# dte = 0
# eCount = 0
# oCount = 0

win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("athus")

walkRight = [pygame.image.load('athusr-1.png'), pygame.image.load('athusr-2.png'), pygame.image.load('athusr-3.png'), pygame.image.load('athusr-4.png'), pygame.image.load('athusr-5.png'), pygame.image.load('athusr-6.png'), pygame.image.load('athusr-7.png'), pygame.image.load('athusr-8.png'), pygame.image.load('athusr-9.png')]
walkLeft = [pygame.image.load('athusl-1.png'), pygame.image.load('athusl-2.png'), pygame.image.load('athusl-3.png'), pygame.image.load('athusl-4.png'), pygame.image.load('athusl-5.png'), pygame.image.load('athusl-6.png'), pygame.image.load('athusl-7.png'), pygame.image.load('athusl-8.png'), pygame.image.load('athusl-9.png')]
bg = pygame.image.load('bgp.jpg')
charRight = pygame.image.load('athus_stand-r.png')
charLeft = pygame.image.load('athus_stand-l.png')
lShoot = pygame.image.load('athus_shoot-l.png')
rShoot = pygame.image.load('athus_shoot-r.png')

athusLaserSound = pygame.mixer.Sound('athus_laser.wav')
etroLaserSound = pygame.mixer.Sound('etro_laser.wav')
athusHitSound = pygame.mixer.Sound('athus_hit.wav')
olesteHitSound = pygame.mixer.Sound('oleste_hit.wav')
olesteDeadSound = pygame.mixer.Sound('oleste_dead.wav')
etroHitSound = pygame.mixer.Sound('etro_hit.wav')
etroDeadSound = pygame.mixer.Sound('etro_dead.wav')
jungleMusic = pygame.mixer.music.load('blue_jungle.mp3')
#dinoHerd = pygame.mixer.music.load('dino_herd.mp3')
# pygame.mixer.Channel(0).play(pygame.mixer.Sound('blue_jungle.mp3'))
# pygame.mixer.Channel(1).play(pygame.mixer.Sound('dino_herd.mp3'))

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.1)

clock = pygame.time.Clock()

score = 0

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
		self.isInvincible = False
		self.visible = True
		self.hitbox = (self.x + 16, self.y + 10, 28, 50)
		self.healthbox = (sw/2 - 128, 20, 256, 8)
		self.health = 16

	def draw(self,win):
		if self.walkCount + 1 >= 27:	# 27 fps because there are 9 frames
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
		pygame.draw.rect(win, (255,0,0), self.healthbox, 8)
		pygame.draw.rect(win, (0,250,0), (222, 20, (self.health * 16), 8), 8)
		pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

	def hit(self):
		self.timeSinceHit = pygame.time.get_ticks()
		if self.health > 1:
			if not self.isInvincible:
				print("i got hit :(")
				self.health = self.health -1
				athusHitSound.play()
				damageRead = pygame.font.SysFont('couriernewttf', 80)
				text = damageRead.render('-5', 1, (255, 0, 0))
				win.blit(text, ((sw/2) - (text.get_width()/2), sh/2))
				pygame.display.update()
	

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
		
		pygame.draw.circle(win, self.color, (round(self.x), round(self.y)), self.radius)

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
	ocharLeft = pygame.image.load('olest_stand-l.png')
	
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
			pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

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
		if self.health > 1:
			self.health -= 1
			olesteHitSound.play()
		else:
			olesteDeadSound.play()
			self.visible = False
			olesteOn = False
			oCount -= 1
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
			pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

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
		if self.health > 1:
			self.health -= 1
			etroHitSound.play()

		else:
			etroDeadSound.play()
			self.visible = False
			etroOn = False
			eCount -= 1
		print('hit!')

def redrawWindow():
	win.blit(bg, (0,0))
	text = font.render(str(score), 1, (255, 255, 255))
	win.blit(text, (sw - 100, 15))
	athus.draw(win)
	oleste.draw(win)
	etro.draw(win)
	for bullet in bullets:
		bullet.draw(win)
	for laser in lasers:
		laser.draw(win)
	pygame.display.update()

athus = player(600, 380, 64, 64)
oleste = enemy1(-80, 380, 64, 64, sw - 74)
olesteOn = False
# oCount += 1
etro = enemy2(-80, 384, 64, 64, sw - 74)
etroOn = False
# eCount += 1
shootLoop = 0
laserLoop = 0
bullets = []
lasers = []

#mainloop

font = pygame.font.SysFont('couriernewttf', 30)
run = True
while run:
	clock.tick(36)

	# if dte < nSeconds and eCount > 1:
	# 	t1 = time.clock()
	# 	dte = t1 - t0e
	# else:

	# 	etro = enemy2(-80, 384, 64, 64, sw - 74)
	# 	etroOn = True
	# 	etro.visible = True
	# 	eCount += 1

	# if dto < nSeconds and oCount > 1:
	# 	t1 = time.clock()
	# 	dto = t1 - t0o
	# else:
	# 	oleste = enemy1(-80, 380, 64, 64, sw - 74)
	# 	olesteOn = True
	# 	oleste.visible = True
	# 	oCount += 1
		

	if pygame.time.get_ticks() - athus.timeSinceHit > 500:
		athus.isInvincible = False

	if etro.visible:
		if athus.hitbox[1] < etro.hitbox[1] + etro.hitbox[3] and athus.hitbox[1] + athus.hitbox[3] > etro.hitbox[1]:
			if athus.hitbox[0] + athus.hitbox[2] > etro.hitbox[0] and athus.hitbox[0] < etro.hitbox[0] + etro.hitbox[2]:
				athus.hit()
				athus.isInvincible = True

	if oleste.visible:
		if athus.hitbox[1] < oleste.hitbox[1] + oleste.hitbox[3] and athus.hitbox[1] + athus.hitbox[3] > oleste.hitbox[1]:
			if athus.hitbox[0] + athus.hitbox[2] > oleste.hitbox[0] and athus.hitbox[0] < oleste.hitbox[0] + oleste.hitbox[2]:
				athus.hit()
				athus.isInvincible = True

	if shootLoop > 0:
		shootLoop += 1
	if shootLoop > 10:
		shootLoop = 0

	if laserLoop > 0:
		laserLoop += 1
	if laserLoop > 3:
		laserLoop = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False


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
						print(len(bullets))
						if len(bullets) > 1:
							bullets.pop(bullets.index(bullet))

		if bullet.x < sw and bullet.x > 0:
			bullet.x += bullet.vel
		else:
			if len(bullets) > 0:
				bullets.pop(bullets.index(bullet))

	for laser in lasers:
		if athus.hitbox[1] < laser.y + laser.radius and athus.hitbox[1] + athus.hitbox[3] > laser.y:
			if athus.hitbox[0] + athus.hitbox[2] > laser.x + laser.radius and athus.hitbox[0] < laser.x + laser.radius:
				athus.hit()
				if len(lasers) > 0:
					lasers.pop(lasers.index(laser))
				athus.isInvincible = True

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
		if len(lasers) < 1:
			lasers.append(projectile2(etro.x + i, etro.y + 52, 3, 1, (179,255,255), efacing))
			laserLoop = 1
			etroLaserSound.play()


	if keys[pygame.K_SPACE] and shootLoop == 0:
		i = 0
		athusLaserSound.play()
		athus.isShooting = True
		if athus.left:
			facing = -1
			i = 2
		else:
			i = 62
			facing = 1

		if len(bullets) < 3:
			bullets.append(projectile(athus.x + i, athus.y + 30, 2, 200, (255,0,0), facing))
		shootLoop = 1

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
import pygame
import random
import time
import sys

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
			if self.walkCount + 1 >= 21:	# 30 fps because there are 10 frames
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
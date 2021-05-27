import random
import pygame
import time

pygame.init()

frame = pygame.display.set_mode((650, 400))
pygame.display.set_caption("Space Invaders")

player_x = 285
player_y = 365
player_move_x = 0

score_font = pygame.font.Font('freesansbold.ttf', 32)
gameOver_font = pygame.font.Font('freesansbold.ttf', 64)
score = 0

bullet_x = 0
bullet_y = 496
bullet_move_y = 3
bullet_ready = True

enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
aantal_vijanden = 6

enemyBulletX = []
enemyBulletY = []
enemyBulletY_change = []
enemyBullet_ready = []

for _ in range(aantal_vijanden):
  enemyX.append(random.randint(0, 586))
  enemyY.append(random.randint(50, 150))
  enemyX_change.append(2)
  enemyY_change.append(40)

for _ in range(aantal_vijanden):
  enemyBulletX.append(0)
  enemyBulletY.append(496)
  enemyBulletY_change.append(3)
  enemyBullet_ready.append(True)


def isHetRaak(enemyX, enemyY, bulletX, bulletY):
  if enemyX <= bulletX and enemyX + 50 >= bulletX:
    if enemyY <= bulletY and enemyY + 23 >= bulletY:
      return True
  return False

def isHetRaakEnemy(playerX, playerY, bulletX, bulletY):
  if playerX <= bulletX and playerX + 60 >= bulletX:
    if playerY <= bulletY and playerY + 18 >= bulletY:
      return True
  return False

def showScore():
  scoreText = score_font.render("Score: " + str(score), True, (255, 255, 255))
  frame.blit(scoreText, (10, 10))

def gameOver():
  global running

  gameOverText = gameOver_font.render("Game Over", True, (255, 255, 255))
  frame.blit(gameOverText, (325 - 128, 200 - 32))

  running = False

running = True
clock = pygame.time.Clock()
start_time = time.time()

while running:
  frame.fill((0, 0, 0))
  showScore()

  for _ in range(aantal_vijanden):
    enemyX[_] += enemyX_change[_]
    if enemyX[_] <= 0:
      enemyX_change[_] = 2
      enemyY[_] += enemyY_change[_]
    elif enemyX[_] >= 586:
      enemyX_change[_] = -2
      enemyY[_] += enemyY_change[_]
    if enemyY[_] > 400:
      gameOver()
    pygame.draw.rect(frame, (255, 255, 255), (enemyX[_], enemyY[_], 50, 23))

    if random.randint(0, 400) == 1 and enemyBullet_ready[_] and time.time() - start_time >= 2:
      enemyBullet_ready[_] = False
      enemyBulletX[_] = enemyX[_] + 27
      enemyBulletY[_] = enemyY[_] + 5

    if not enemyBullet_ready[_]:
      pygame.draw.circle(frame, (255, 255, 255), (enemyBulletX[_], enemyBulletY[_] - enemyBulletY_change[_]), 7)
      enemyBulletY[_] += enemyBulletY_change[_]

      if enemyBulletY[_] >= 407:
        enemyBulletY[_] = 0
        enemyBullet_ready[_] = True

    if isHetRaak(enemyX[_], enemyY[_], bullet_x, bullet_y):
      bullet_y = 480
      bullet_ready = True
      enemyX[_] = random.randint(0, 586)
      enemyY[_] = random.randint(50, 150)
      score += 1

      if score >= 10 and score % 10 == 0:
        aantal_vijanden += 1
        enemyX.append(random.randint(0, 586))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(2)
        enemyY_change.append(40)

        enemyBulletX.append(0)
        enemyBulletY.append(496)
        enemyBulletY_change.append(3)
        enemyBullet_ready.append(True)

    if isHetRaakEnemy(player_x, player_y, enemyBulletX[_], enemyBulletY[_]):
      gameOver()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.display.quit()
      running = False
      
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        player_move_x = -2
      elif event.key == pygame.K_RIGHT:
        player_move_x = 2
      elif event.key == pygame.K_SPACE and bullet_ready and time.time() - start_time >= 2:
        bullet_ready = False
        bullet_x = player_x + 25
        bullet_y = player_y + 5

    elif event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        player_move_x = 0

  player_x += player_move_x
  if player_x < 0:
    player_x = 1
  elif player_x > 590:
    player_x = 589

  if not bullet_ready:
    bullet = pygame.draw.circle(frame, (255, 255, 255), (bullet_x, bullet_y - bullet_move_y), 7)
    bullet_y -= bullet_move_y
  if bullet_y < 0:
    bullet_y = 0
    bullet_ready = True

  player = pygame.draw.rect(frame, (255, 255, 255), (player_x, player_y, 60, 18))

  pygame.display.update()
  clock.tick(100)

time.sleep(3)
pygame.display.quit()

import cv2
import mediapipe as mp
import pygame
import random
import sys

# === Initialize Pygame ===
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Catch with Hand")
clock = pygame.time.Clock()

# === Score and Font ===
score = 0
font = pygame.font.SysFont("Arial", 30)

# === Paddle (Your Hand Control) ===
paddle = pygame.Rect(300, 440, 100, 20)

# === Ball ===
ball = pygame.Rect(random.randint(0, 600), 0, 20, 20)
ball_speed = 5

# === Mediapipe for Hand ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0)

# === Game Loop ===
while True:
    screen.fill((200, 255, 255))  # Background

    # Handle quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()

    # Webcam frame
    ret, frame = cap.read()
    if not ret:
        continue
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Hand tracking to move paddle
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_x = hand_landmarks.landmark[8].x  # Index finger tip
            paddle.centerx = int(index_x * WIDTH)

    # Ball falling
    ball.y += ball_speed
    if ball.y > HEIGHT:
        ball.x = random.randint(0, WIDTH - 20)
        ball.y = 0

    # Collision
    if paddle.colliderect(ball):
        score += 1
        ball.x = random.randint(0, WIDTH - 20)
        ball.y = 0

    # Draw
    pygame.draw.rect(screen, (0, 0, 255), paddle)  # Paddle blue
    pygame.draw.ellipse(screen, (255, 0, 0), ball)  # Ball red
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)
p
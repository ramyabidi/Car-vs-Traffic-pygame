import pygame
import tkinter as tk
from tkinter import messagebox
import random
from sys import exit

pygame.init()

screen_width = 600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Car vs Traffic')

clock = pygame.time.Clock()

font = pygame.font.Font(None, 50)

music_files = ["music.mp3", "crash.mp3"]
pygame.mixer.music.load(music_files[0])
pygame.mixer.music.play()

road_img = pygame.image.load("road.png").convert_alpha()
road_img = pygame.transform.scale(road_img, (screen_width, screen_height))

car_width, car_height = 100, 200
my_car_img = pygame.image.load("car.png").convert_alpha()
my_car_img = pygame.transform.scale(my_car_img, (car_width, car_height))
enemy_car_img = pygame.image.load("enemy_car.png").convert_alpha()
enemy_car_img = pygame.transform.scale(enemy_car_img, (car_width, car_height))

def respawn_enemy_car():
    global enemy_car_x, enemy_car_y, enemy_car_speed
    enemy_car_x = random.choice([125, 375])
    enemy_car_y = random.randint(-screen_height, -200)
    enemy_car_speed += 1

def get_top_scores():
    try:
        with open("high_scores.txt", "r") as file:
            top_scores = [int(line.strip()) for line in file.readlines()]
            return sorted(top_scores, reverse=True)[:5]
    except FileNotFoundError:
        return []

def save_top_scores(top_scores):
    with open("high_scores.txt", "w") as file:
        for score in top_scores:
            file.write(str(score) + "\n")

def show_game_over_message():
    root = tk.Tk()
    root.withdraw()

    message = f"Game Over! Your Score: {score}"
    top_scores = get_top_scores()

    if score > 0 and (len(top_scores) < 5 or score > min(top_scores)):
        top_scores.append(score)
        top_scores = sorted(top_scores, reverse=True)[:5]
        save_top_scores(top_scores)
        if score == top_scores[0]:
            message += "\n    NEW HIGH SCORE!\n"

    top_scores_text = "\nTop Scores:\n"
    for i, top_score in enumerate(top_scores, start=1):
        top_scores_text += f"{i}. {top_score}\n"
    message += top_scores_text

    messagebox.showinfo("Car vs Traffic", message)

    if messagebox.askyesno("Car vs Traffic", "Try Again?"):
        reset_game()
    else:
        pygame.quit()
        exit()

def reset_game():
    global score, car_x, car_y, enemy_car_speed
    pygame.mixer.music.load(music_files[0])
    pygame.mixer.music.play()
    score = 0
    car_x, car_y = 125, 650
    enemy_car_speed = 5
    respawn_enemy_car()

enemy_car_x, enemy_car_y = random.choice([125, 375]), -200
enemy_car_speed = 5

car_x, car_y = 125, 650

road_y1 = 0
road_y2 = -screen_height

score = 0
time_elapsed = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x = 125
    if keys[pygame.K_RIGHT]:
        car_x = 375

    enemy_car_y += enemy_car_speed
    if enemy_car_y > screen_height:
        respawn_enemy_car()

    road_y1 += 5
    road_y2 += 5

    if road_y1 > screen_height:
        road_y1 = road_y2 - screen_height
    if road_y2 > screen_height:
        road_y2 = road_y1 - screen_height

    screen.blit(road_img, (0, road_y1))
    screen.blit(road_img, (0, road_y2))

    score_display = font.render(f"Score: {score}", False, 'black')
    screen.blit(score_display, (10, 10))

    screen.blit(my_car_img, (car_x, 650))
    screen.blit(enemy_car_img, (enemy_car_x, enemy_car_y))

    my_car_rect = pygame.Rect(car_x, 650, car_width, car_height)
    enemy_car_rect = pygame.Rect(enemy_car_x, enemy_car_y, car_width, car_height)

    if my_car_rect.colliderect(enemy_car_rect):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_files[1])
        pygame.mixer.music.play()
        show_game_over_message()
    else:
        score += 1

    time_elapsed += clock.get_time()
    if time_elapsed >= 7000:
        enemy_car_speed += 1
        time_elapsed = 0

    pygame.display.update()
    clock.tick(60)

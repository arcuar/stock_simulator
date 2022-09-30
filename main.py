import os
import pygame
import random

pygame.init()  # 초기화

# 게임 버전
ver = "1.0.1"

screen_size = [1720, 950]  # 게임 창 크기
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption("주식시뮬레이터")  # 창 타이틀

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

current_path = os.path.dirname(__file__)
font_D2 = os.path.join(current_path, "assets\\D2Coding-Ver1.3.2-20180524.ttc")


class Stock:
    def __init__(self, name: str, background_color: tuple, price: int, position: tuple):
        self.name = name
        self.price = price
        self.position = position
        self.background_color = background_color
        self.change = None
        self.item_color = None
        self.arrow = None
        self.evaluation = 0

        self.item = 0

        self.past_1 = [0]
        self.past_2 = [0, 0]
        self.past_3 = [0, 0, 0]
        self.past_4 = [0, 0, 0, 0]
        self.past_5 = [0, 0, 0, 0, 0]

        font = pygame.font.Font(font_D2, 60)
        self.past_1_text = font.render("", False, BLACK)
        self.past_2_text = font.render("", False, BLACK)
        self.past_3_text = font.render("", False, BLACK)
        self.past_4_text = font.render("", False, BLACK)
        self.past_5_text = font.render("", False, BLACK)

    def change_price(self, fluctuation: tuple):
        self.change = random.randrange(fluctuation[0], fluctuation[1]) * random.choice((-1, 1))
        self.price = round(self.price + self.price * self.change * 0.01)

        if self.change > 0:
            self.item_color = RED
            self.arrow = "▲"
        elif self.change < 0:
            self.item_color = BLUE
            self.arrow = "▼"
        else:
            self.item_color = WHITE
            self.arrow = " "

        self.past_1.extend([self.price, self.arrow, self.item_color])
        self.past_2.extend([self.price, self.arrow, self.item_color])
        self.past_3.extend([self.price, self.arrow, self.item_color])
        self.past_4.extend([self.price, self.arrow, self.item_color])
        self.past_5.extend([self.price, self.arrow, self.item_color])

        font = pygame.font.Font(font_D2, 60)

        if self.past_1[0] == 0:
            del self.past_1[0]
        else:
            self.past_1_text = font.render(f"{self.past_1[1]}{self.past_1[0]}", True, self.past_1[2])
            del self.past_1[:3]

        if self.past_2[0] == 0:
            del self.past_2[0]
        else:
            self.past_2_text = font.render(f"{self.past_2[1]}{self.past_2[0]}", True, self.past_2[2])
            del self.past_2[:3]

        if self.past_3[0] == 0:
            del self.past_3[0]
        else:
            self.past_3_text = font.render(f"{self.past_3[1]}{self.past_3[0]}", True, self.past_3[2])
            del self.past_3[:3]

        if self.past_4[0] == 0:
            del self.past_4[0]
        else:
            self.past_4_text = font.render(f"{self.past_4[1]}{self.past_4[0]}", True, self.past_4[2])
            del self.past_4[:3]

        if self.past_5[0] == 0:
            del self.past_5[0]
        else:
            self.past_5_text = font.render(f"{self.past_5[1]}{self.past_5[0]}", True, self.past_5[2])
            del self.past_5[:3]

    def purchase(self, mouse_pos, money):
        if self.position[0] < mouse_pos[0] < self.position[0] + 130 and \
                self.position[1] + 130 < mouse_pos[1] < self.position[1] + 200:
            if money >= self.price:
                self.item += 1
                money -= self.price
        elif self.position[0] + 135 < mouse_pos[0] < self.position[0] + 190 and \
                self.position[1] + 130 < mouse_pos[1] < self.position[1] + 200:
            if money >= self.price * 10:
                self.item += 10
                money -= self.price * 10
            elif self.price * 10 > money >= self.price:
                self.item += money // self.price
                money -= self.price * (money // self.price)
        elif self.position[0] + 195 < mouse_pos[0] < self.position[0] + 325 and \
                self.position[1] + 130 < mouse_pos[1] < self.position[1] + 200:
            if self.item >= 1:
                self.item -= 1
                money += self.price
        elif self.position[0] + 330 < mouse_pos[0] < self.position[0] + 385 and \
                self.position[1] + 130 < mouse_pos[1] < self.position[1] + 200:
            if self.item >= 10:
                self.item -= 10
                money += self.price * 10
            elif 10 > self.item > 0:
                money += self.price * self.item
                self.item -= self.item

        return money

    def screen_blit(self):
        font = pygame.font.Font(font_D2, 110)
        text = font.render(self.name, True, WHITE, self.background_color)
        screen.blit(text, self.position)
        text = font.render(f"{self.arrow}{self.price}", True, self.item_color)
        screen.blit(text, (int(self.position[0]) + 10, int(self.position[1]) - 100))
        font = pygame.font.Font(font_D2, 75)
        text = font.render(f"{self.change}%", True, WHITE)
        screen.blit(text, (int(self.position[0]) + 400, int(self.position[1]) + 10))
        font = pygame.font.Font(font_D2, 40)
        text = font.render(f"수량: {self.item}", True, WHITE)
        screen.blit(text, (int(self.position[0]), int(self.position[1]) + 200))
        text = font.render(f"평가: {self.item * self.price}", True, WHITE)
        screen.blit(text, (int(self.position[0]), int(self.position[1]) + 250))
        screen.blit(self.past_1_text, (int(self.position[0]) + 80, int(self.position[1]) - 170))
        screen.blit(self.past_2_text, (int(self.position[0]) + 80, int(self.position[1]) - 240))
        screen.blit(self.past_3_text, (int(self.position[0]) + 80, int(self.position[1]) - 310))
        screen.blit(self.past_4_text, (int(self.position[0]) + 80, int(self.position[1]) - 380))
        screen.blit(self.past_4_text, (int(self.position[0]) + 80, int(self.position[1]) - 450))
        font = pygame.font.Font(font_D2, 35)
        pygame.draw.rect(screen, RED, [self.position[0], self.position[1] + 130, 130, 70])
        text = font.render("매수", True, WHITE)
        screen.blit(text, (int(self.position[0]) + 30, int(self.position[1]) + 145))
        pygame.draw.rect(screen, RED, [self.position[0] + 135, self.position[1] + 130, 55, 70])
        text = font.render("+10", True, WHITE)
        screen.blit(text, (int(self.position[0]) + 135, int(self.position[1]) + 145))
        pygame.draw.rect(screen, BLUE, [self.position[0] + 195, self.position[1] + 130, 130, 70])
        text = font.render("매도", True, WHITE)
        screen.blit(text, (int(self.position[0]) + 225, int(self.position[1]) + 145))
        pygame.draw.rect(screen, BLUE, [self.position[0] + 330, self.position[1] + 130, 55, 70])
        text = font.render("-10", True, WHITE)
        screen.blit(text, (int(self.position[0]) + 330, int(self.position[1]) + 145))


money = 500000

satsung = Stock("SATSUNG", (0, 0, 50), 50000, (50, 450)) # 샀엉
makao = Stock(" MAKAO ", (50, 50, 0), 100000, (610, 450)) # 마카오
hyunbai = Stock("HYUNBAI", (50, 50, 50), 150000, (1170, 450)) # 현배
i = 120
isRun = True
while isRun:
    clock.tick(60)
    screen.fill(BLACK)

    font = pygame.font.Font(font_D2, 15)
    text = font.render(f"{ver}", True, WHITE)
    screen.blit(text, (1670, 20))
    text = font.render("Developed by Nunnaerim", True, WHITE)
    screen.blit(text, (1535, 5))
    font = pygame.font.Font(font_D2, 50)
    text = font.render(f"보유자금: {format(money, ',')}", True, WHITE)
    screen.blit(text, (1250, 850))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            money = satsung.purchase(pygame.mouse.get_pos(), money)
            money = makao.purchase(pygame.mouse.get_pos(), money)
            money = hyunbai.purchase(pygame.mouse.get_pos(), money)
    if i == 120:
        satsung.change_price((00, 12))
        makao.change_price((00, 14))
        hyunbai.change_price((00, 16))
        i = 0
    i += 1
    satsung.screen_blit()
    makao.screen_blit()
    hyunbai.screen_blit()
    pygame.display.flip()

# 사실상 주식 시뮬레이터가 아니라 투기 시뮬레이터인건 비밀

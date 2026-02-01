import pygame
import sys
import random
import os
from tkinter import messagebox
import tkinter as tk
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# tkinterのメインウィンドウを隠す（パス通知メッセージ用）
root = tk.Tk()
root.withdraw()

# --- 設定 ---
SCREEN_SIZE = 750
GRID_SIZE = 10
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
FPS = 60

# 色の定義
GREEN = (34, 139, 34)
DARK_GREEN = (20, 100, 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
HINT_COLOR = (200, 200, 0)
YELLOW = (255, 255, 0)

class Othello:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("10x10 リバーシ")
        
        font_list = ["msgothic", "msqothic", "hiraginosans", "yugothic", "arial"]
        self.font = pygame.font.SysFont(font_list, 42)
        self.title_font = pygame.font.SysFont(font_list, 100, bold=True)
        
        self.clock = pygame.time.Clock()
        self.state = "TITLE"
        self.player_color = 1 
        
        # 音声読み込み
# --- 音声ファイルの読み込み ---
# --- 音声ファイルの読み込み ---
# --- 音声読み込み (resource_path で囲むのがポイント！) ---
        try:
            # BGMの読み込み
            pygame.mixer.music.load(resource_path("bgm.mp3"))
            pygame.mixer.music.set_volume(0.15)
            
            # 効果音の読み込み
            # ※ファイル名が put.mp3 か put.wav か、左側のエクスプローラーと一致させてください
            self.sound_put = pygame.mixer.Sound(resource_path("put.mp3"))
            self.sound_put.set_volume(0.7)
        except Exception as e:
            print(f"音声ファイルが見つかりません: {e}")
            self.sound_put = None

    def reset_game(self):
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.board[4][4], self.board[5][5] = -1, -1
        self.board[4][5], self.board[5][4] = 1, 1
        self.turn = 1 
        if not pygame.mixer.music.get_busy():
            try: pygame.mixer.music.play(-1)
            except: pass

    def draw_text(self, text, y, font, color=WHITE):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(SCREEN_SIZE // 2, y))
        self.screen.blit(img, rect)

    def get_flippable(self, r, c, player):
        if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE) or self.board[r][c] != 0:
            return []
        flippable = []
        directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
        for dr, dc in directions:
            temp = []
            nr, nc = r + dr, c + dc
            while 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and self.board[nr][nc] == -player:
                temp.append((nr, nc))
                nr += dr
                nc += dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and self.board[nr][nc] == player:
                    flippable.extend(temp)
                    break
        return flippable

    def get_valid_moves(self, player):
        moves = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.get_flippable(r, c, player):
                    moves.append((r, c))
        return moves

    def handle_title(self):
        self.screen.fill(DARK_GREEN)
        self.draw_text("10x10 リバーシ", SCREEN_SIZE // 4, self.title_font)
        self.draw_text("1キー：黒（先攻）", SCREEN_SIZE // 2, self.font)
        self.draw_text("2キー：白（後攻）", SCREEN_SIZE // 2 + 80, self.font)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.player_color = 1
                    self.reset_game()
                    self.state = "PLAYING"
                elif event.key == pygame.K_2:
                    self.player_color = -1
                    self.reset_game()
                    self.state = "PLAYING"

    def handle_playing(self):
        if self.turn != self.player_color:
            pygame.time.delay(600)
            moves = self.get_valid_moves(self.turn)
            if moves:
                r, c = random.choice(moves)
                self.execute_move(r, c)
            else:
                self.pass_turn()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                r, c = y // CELL_SIZE, x // CELL_SIZE
                self.execute_move(r, c)

    def execute_move(self, r, c):
        flippable = self.get_flippable(r, c, self.turn)
        if flippable:
            if self.sound_put:
                self.sound_put.play()
            
            self.board[r][c] = self.turn
            for fr, fc in flippable:
                self.board[fr][fc] = self.turn
            self.pass_turn()
            return True
        return False

    def pass_turn(self):
        self.turn *= -1
        if not self.get_valid_moves(self.turn):
            self.draw_playing()
            pygame.display.flip()
            
            if not self.get_valid_moves(-self.turn):
                self.state = "GAMEOVER"
                pygame.mixer.music.fadeout(2000)
            else:
                p_name = "黒" if self.turn == 1 else "白"
                messagebox.showinfo("パス", f"{p_name}の置ける場所がないため、順番をパスします")
                self.turn *= -1

    def draw_playing(self):
        self.screen.fill(GREEN)
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * CELL_SIZE), (SCREEN_SIZE, i * CELL_SIZE), 2)
            pygame.draw.line(self.screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_SIZE), 2)
        
        if self.turn == self.player_color:
            for r, c in self.get_valid_moves(self.turn):
                center = (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2)
                pygame.draw.circle(self.screen, HINT_COLOR, center, 8)

        black_cnt = 0 
        white_cnt = 0
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c] != 0:
                    color = BLACK if self.board[r][c] == 1 else WHITE
                    pos = (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2)
                    pygame.draw.circle(self.screen, color, pos, CELL_SIZE // 2 - 5)
                    if self.board[r][c] == 1: black_cnt += 1
                    else: white_cnt += 1

        msg = "あなたの番" if self.turn == self.player_color else "CPU思考中..."
        pygame.display.set_caption(f"黒: {black_cnt} 白: {white_cnt} | {msg}")

    def handle_gameover(self):
        b_cnt = sum(row.count(1) for row in self.board)
        w_cnt = sum(row.count(-1) for row in self.board)
        self.screen.fill(DARK_GREEN)
        self.draw_text("終局", SCREEN_SIZE // 4, self.title_font)
        self.draw_text(f"黒: {b_cnt}枚 － 白: {w_cnt}枚", SCREEN_SIZE // 2, self.font)
        
        winner_msg = "引き分け！"
        if b_cnt > w_cnt: winner_msg = "黒の勝ち！"
        elif w_cnt > b_cnt: winner_msg = "白の勝ち！"
            
        self.draw_text(winner_msg, SCREEN_SIZE // 2 + 80, self.font, YELLOW)
        self.draw_text("Rキー：タイトルへ戻る", SCREEN_SIZE - 100, self.font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.state = "TITLE"

    def run(self):
        while True:
            if self.state == "TITLE": self.handle_title()
            elif self.state == "PLAYING":
                self.handle_playing()
                self.draw_playing()
            elif self.state == "GAMEOVER": self.handle_gameover()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Othello().run()
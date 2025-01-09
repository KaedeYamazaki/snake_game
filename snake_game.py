import pyxel
import random
import math

class SnakeGame:
    def __init__(self):
        pyxel.init(160, 120, title="snake")
        self.create_sound()
        self.reset_game()
        pyxel.run(self.update, self.draw)


    def create_sound(self):
        # 花火の爆発音を作成
        pyxel.sounds[3].set("a3a2c1a1", "p", "7", "s", 5)

    # 残りのコードは同じなので省略せずにそのまま記述
    def reset_game(self):
        self.snake_pos = [(80, 60)]
        self.direction = (1, 0)
        self.score = 0
        
        self.time_limit = 60 * 30
        self.remaining_time = self.time_limit
        
        self.food = self.spawn_food()
        self.fireworks = []
        
        self.game_over = False
        self.game_started = False

    def spawn_food(self):
        while True:
            x = random.randint(0, 52) * 3
            y = random.randint(0, 38) * 3
            if (x, y) not in self.snake_pos:
                return (x, y)

    def spawn_firework(self):
        x = random.randint(20, 140)
        y = random.randint(20, 100)
        particles = []
        
        # 花火の爆発音を再生
        pyxel.play(0, 3)
        
        num_particles = 20
        for _ in range(num_particles):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(0.5, 2.0)
            color = random.choice([8, 9, 10, 11, 12])
            particles.append({
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'x': 0,
                'y': 0,
                'life': 30,
                'color': color
            })
        
        self.fireworks.append({
            'x': x,
            'y': y,
            'particles': particles,
            'timer': 30
        })

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.game_started = True
            if self.game_over:
                self.reset_game()
                
        if not self.game_started or self.game_over:
            return

        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.game_over = True
            return

        if pyxel.btn(pyxel.KEY_LEFT) and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif pyxel.btn(pyxel.KEY_RIGHT) and self.direction != (-1, 0):
            self.direction = (1, 0)
        elif pyxel.btn(pyxel.KEY_UP) and self.direction != (0, 1):
            self.direction = (0, -1)
        elif pyxel.btn(pyxel.KEY_DOWN) and self.direction != (0, -1):
            self.direction = (0, 1)

        head_x = (self.snake_pos[0][0] + self.direction[0] * 3) % 160
        head_y = (self.snake_pos[0][1] + self.direction[1] * 3) % 120
        new_head = (head_x, head_y)

        if new_head in self.snake_pos:
            self.game_over = True
            return

        self.snake_pos.insert(0, new_head)

        if abs(head_x - self.food[0]) < 3 and abs(head_y - self.food[1]) < 3:
            self.score += 1
            self.food = self.spawn_food()
            for _ in range(3):
                self.spawn_firework()
        else:
            self.snake_pos.pop()

        for firework in self.fireworks[:]:
            firework['timer'] -= 1
            
            for particle in firework['particles']:
                particle['x'] += particle['dx']
                particle['y'] += particle['dy']
                particle['life'] -= 1
                particle['dy'] += 0.1
            
            if firework['timer'] <= 0:
                self.fireworks.remove(firework)

    def draw_snake_head(self, x, y):
        GREEN = 11
        BROWN = 4
        
        pyxel.pset(x, y, GREEN)
        pyxel.pset(x+1, y, GREEN)
        pyxel.pset(x+2, y, GREEN)
        pyxel.pset(x, y+2, GREEN)
        pyxel.pset(x+1, y+2, GREEN)
        pyxel.pset(x+2, y+2, GREEN)
        
        pyxel.pset(x, y+1, BROWN)
        pyxel.pset(x+1, y+1, GREEN)
        pyxel.pset(x+2, y+1, BROWN)

    def draw(self):
        pyxel.cls(0)

        if not self.game_started:
            pyxel.text(55, 50, "Happy New Year!", pyxel.frame_count % 16)
            pyxel.text(45, 70, "Press SPACE to Start", 7)
            return

        if self.game_over:
            pyxel.text(60, 50, "GAME OVER", 8)
            pyxel.text(45, 70, "Press SPACE to Restart", 7)
            pyxel.text(50, 85, f"Final Score: {self.score}", 7)
            return

        remaining_seconds = self.remaining_time // 30
        pyxel.text(5, 5, f"Time: {remaining_seconds}", 7)
        pyxel.text(60, 5, f"Score: {self.score}", 7)

        for i, pos in enumerate(self.snake_pos):
            if i == 0:
                self.draw_snake_head(pos[0], pos[1])
            else:
                pyxel.rect(pos[0], pos[1], 3, 3, 3)

        x, y = self.food
        pyxel.rect(x, y, 3, 3, 8)
        pyxel.pset(x + 1, y + 1, 7)

        for firework in self.fireworks:
            for particle in firework['particles']:
                if particle['life'] > 0:
                    x = firework['x'] + particle['x']
                    y = firework['y'] + particle['y']
                    if 0 <= x < 160 and 0 <= y < 120:
                        pyxel.pset(x, y, particle['color'])

        if remaining_seconds <= 10:
            if pyxel.frame_count % 30 < 15:
                pyxel.text(60, 20, "Time Running Out!", 8)

SnakeGame()
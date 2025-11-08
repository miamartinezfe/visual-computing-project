import cv2
import numpy as np
import random
import time

class SnakeGame:
    def __init__(self, width=800, height=600, cell_size=30):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.game_speed = 0.25
        self.last_update_time = 0
        self.reset()
        
    def reset(self):
        """Reinicia el juego"""
        # Asegurar que la posición inicial esté alineada con la grid
        start_x = (self.width // (2 * self.cell_size)) * self.cell_size
        start_y = (self.height // (2 * self.cell_size)) * self.cell_size
        self.snake = [(start_x, start_y)]
        self.direction = (1, 0)  # Derecha
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.game_started = False
        self.last_update_time = time.time()
        self.grow_pending = False  # Nueva bandera para crecimiento
        
    def generate_food(self):
        """Genera comida en posición aleatoria que coincida con la grid"""
        max_x = (self.width - self.cell_size) // self.cell_size
        max_y = (self.height - self.cell_size) // self.cell_size
        
        while True:
            food_x = random.randint(0, max_x) * self.cell_size
            food_y = random.randint(0, max_y) * self.cell_size
            food_pos = (food_x, food_y)
            
            # Asegurar que la comida no aparezca en la serpiente
            if food_pos not in self.snake:
                return food_pos
    
    def update(self, gesture):
        """Actualiza el estado del juego basado en el gesto"""
        current_time = time.time()
        
        # Control de velocidad - solo actualizar si ha pasado el tiempo suficiente
        if current_time - self.last_update_time < self.game_speed:
            return
            
        self.last_update_time = current_time
        
        if not self.game_started:
            if gesture == "START":
                self.game_started = True
            return
            
        if self.game_over:
            if gesture == "START":
                self.reset()
                self.game_started = True
            return
        
        # Cambiar dirección basado en gestos
        if gesture == "UP" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif gesture == "DOWN" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif gesture == "LEFT" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif gesture == "RIGHT" and self.direction != (-1, 0):
            self.direction = (1, 0)
        elif gesture == "STOP":
            return  # Pausa el juego
        
        # Mover serpiente
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0] * self.cell_size, 
                   head_y + self.direction[1] * self.cell_size)
        
        # Verificar colisiones con bordes
        if (new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height or
            new_head in self.snake):
            self.game_over = True
            return
        
        # Mover serpiente - insertar nueva cabeza
        self.snake.insert(0, new_head)
        
        # Verificar si comió comida
        if new_head == self.food:
            self.score += 1
            print(f"¡Punto! Puntuación: {self.score}")  # Debug
            self.food = self.generate_food()
            # NO remover la cola - esto hace que la serpiente crezca
        else:
            # Solo remover la cola si no comió
            self.snake.pop()
    
    def draw(self, canvas, x_offset=0, y_offset=0):
        """Dibuja el juego en el canvas"""
        # Fondo
        cv2.rectangle(canvas, (x_offset, y_offset), 
                     (x_offset + self.width, y_offset + self.height), (50, 50, 50), -1)
        
        # Dibujar grid
        for i in range(0, self.width, self.cell_size):
            cv2.line(canvas, (x_offset + i, y_offset), (x_offset + i, y_offset + self.height), (70, 70, 70), 1)
        for i in range(0, self.height, self.cell_size):
            cv2.line(canvas, (x_offset, y_offset + i), (x_offset + self.width, y_offset + i), (70, 70, 70), 1)
        
        if not self.game_started:
            # Pantalla de inicio
            text = "Mano ABIERTA para comenzar"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            text_x = x_offset + (self.width - text_size[0]) // 2
            text_y = y_offset + self.height // 2
            cv2.putText(canvas, text, (text_x, text_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Instrucciones
            instructions = [
                "Controles:",
                "1 dedo - Arriba",
                "2 dedos - Derecha", 
                "3 dedos - Abajo",
                "4 dedos - Izquierda",
                "Puño - Pausa",
                "Mano abierta - Start/Reset",
                "Puño 3 segundos - Salir"
            ]
            
            for i, instruction in enumerate(instructions):
                cv2.putText(canvas, instruction, (x_offset + 20, y_offset + 100 + i * 25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            return
        
        # Dibujar serpiente
        for i, segment in enumerate(self.snake):
            # Cabeza en color diferente
            if i == 0:
                color = (0, 255, 0)  # Verde brillante para la cabeza
            else:
                color = (0, 200, 100)  # Verde más oscuro para el cuerpo
            
            cv2.rectangle(canvas, 
                         (segment[0] + x_offset, segment[1] + y_offset),
                         (segment[0] + x_offset + self.cell_size - 1, 
                          segment[1] + y_offset + self.cell_size - 1),
                         color, -1)
            
            # Bordes de los segmentos
            cv2.rectangle(canvas, 
                         (segment[0] + x_offset, segment[1] + y_offset),
                         (segment[0] + x_offset + self.cell_size - 1, 
                          segment[1] + y_offset + self.cell_size - 1),
                         (0, 150, 0), 1)
        
        # Dibujar comida
        cv2.rectangle(canvas, 
                     (self.food[0] + x_offset, self.food[1] + y_offset),
                     (self.food[0] + x_offset + self.cell_size - 1, 
                      self.food[1] + y_offset + self.cell_size - 1),
                     (0, 0, 255), -1)
        
        # Dibujar puntuación con fondo para mejor visibilidad
        score_text = f'Puntuacion: {self.score}'
        text_size = cv2.getTextSize(score_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        cv2.rectangle(canvas, 
                     (x_offset + 5, y_offset + 5),
                     (x_offset + text_size[0] + 15, y_offset + text_size[1] + 15),
                     (40, 40, 40), -1)
        cv2.putText(canvas, score_text, 
                   (x_offset + 10, y_offset + 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if self.game_over:
            # Pantalla de game over
            overlay = canvas.copy()
            cv2.rectangle(overlay, (x_offset, y_offset), 
                         (x_offset + self.width, y_offset + self.height), 
                         (0, 0, 0), -1)
            alpha = 0.7
            cv2.addWeighted(overlay, alpha, canvas, 1 - alpha, 0, canvas)
            
            text = "GAME OVER"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = x_offset + (self.width - text_size[0]) // 2
            text_y = y_offset + self.height // 2 - 20
            cv2.putText(canvas, text, (text_x, text_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            text = f"Puntuacion final: {self.score}"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            text_x = x_offset + (self.width - text_size[0]) // 2
            text_y = y_offset + self.height // 2 + 20
            cv2.putText(canvas, text, (text_x, text_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            text = "Mano ABIERTA para reiniciar"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            text_x = x_offset + (self.width - text_size[0]) // 2
            text_y = y_offset + self.height // 2 + 60
            cv2.putText(canvas, text, (text_x, text_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
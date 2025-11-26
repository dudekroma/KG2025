import tkinter as tk
from tkinter import ttk, messagebox
import time
import math


class RasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная №3: Базовые растровые алгоритмы")
        self.root.geometry("1100x750")  # Немного увеличил окно

        # --- Настройки сетки ---
        self.cell_size = 20  # Размер одной клетки (пикселя) в пикселях экрана
        self.grid_width = 40  # Количество клеток по ширине
        self.grid_height = 30  # Количество клеток по высоте

        # Смещение центра координат (в клетках)
        self.center_x = self.grid_width // 2
        self.center_y = self.grid_height // 2

        # --- Интерфейс ---
        control_frame = tk.Frame(root, padx=10, pady=10)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # === БЛОК ДЛЯ ЛИНИЙ ===
        line_frame = tk.LabelFrame(control_frame, text="Построение ЛИНИЙ", padx=5, pady=5)
        line_frame.pack(fill="x", pady=10)

        tk.Label(line_frame, text="Начало (x1, y1):").pack()
        frame_p1 = tk.Frame(line_frame)
        frame_p1.pack()
        self.entry_x1 = tk.Entry(frame_p1, width=5);
        self.entry_x1.pack(side=tk.LEFT)
        self.entry_y1 = tk.Entry(frame_p1, width=5);
        self.entry_y1.pack(side=tk.LEFT)

        tk.Label(line_frame, text="Конец (x2, y2):").pack()
        frame_p2 = tk.Frame(line_frame)
        frame_p2.pack()
        self.entry_x2 = tk.Entry(frame_p2, width=5);
        self.entry_x2.pack(side=tk.LEFT)
        self.entry_y2 = tk.Entry(frame_p2, width=5);
        self.entry_y2.pack(side=tk.LEFT)

        # Выбор алгоритма ЛИНИИ
        tk.Label(line_frame, text="Алгоритм линии:").pack(pady=5)
        self.line_algo_var = tk.StringVar(value="step")
        self.algos = [
            ("Пошаговый", "step"),
            ("ЦДА (DDA)", "dda"),
            ("Брезенхем", "bres_line")
        ]
        for text, val in self.algos:
            tk.Radiobutton(line_frame, text=text, variable=self.line_algo_var, value=val).pack(anchor=tk.W)

        tk.Button(line_frame, text="Построить ЛИНИЮ", command=self.draw_line, bg="lightblue").pack(pady=10, fill="x")

        # === БЛОК ДЛЯ ОКРУЖНОСТИ ===
        circle_frame = tk.LabelFrame(control_frame, text="Построение ОКРУЖНОСТИ", padx=5, pady=5)
        circle_frame.pack(fill="x", pady=10)

        tk.Label(circle_frame, text="Центр (Xc, Yc):").pack()
        frame_c = tk.Frame(circle_frame)
        frame_c.pack()
        self.entry_xc = tk.Entry(frame_c, width=5);
        self.entry_xc.pack(side=tk.LEFT)
        self.entry_yc = tk.Entry(frame_c, width=5);
        self.entry_yc.pack(side=tk.LEFT)

        tk.Label(circle_frame, text="Радиус (R):").pack()
        self.entry_r = tk.Entry(circle_frame, width=5);
        self.entry_r.pack()

        tk.Button(circle_frame, text="Построить КРУГ\n(Брезенхем)", command=self.draw_circle, bg="lightgreen").pack(
            pady=10, fill="x")

        # === БЛОК ДЛЯ ДОПОЛНИТЕЛЬНЫХ АЛГОРИТМОВ ===
        advanced_frame = tk.LabelFrame(control_frame, text="Дополнительные алгоритмы", padx=5, pady=5)
        advanced_frame.pack(fill="x", pady=10)

        # Кнопка для алгоритма Ву (сглаживание)
        tk.Button(advanced_frame, text="Сглаженная линия\n(Алгоритм Ву)",
                  command=self.draw_wu_line, bg="#ffcc99").pack(pady=5, fill="x")

        # Кнопка для алгоритма Кастла-Питвея
        tk.Button(advanced_frame, text="Линия Кастла-Питвея",
                  command=self.draw_castle_pitway_line, bg="#cc99ff").pack(pady=5, fill="x")

        # === ОБЩИЕ КНОПКИ ===
        tk.Button(control_frame, text="Очистить всё", command=self.clear_canvas, bg="#ffcccc").pack(pady=20, fill="x")

        # Вывод времени
        self.time_label = tk.Label(control_frame, text="Время: 0.00 мкс", fg="red", font=("Arial", 10, "bold"))
        self.time_label.pack(pady=10)

        # Информация
        info = tk.Label(control_frame, text="Масштаб: 1 клетка = 1 ед.\nОсь Y направлена вверх", justify=tk.LEFT,
                        fg="gray")
        info.pack(side=tk.BOTTOM)

        # Отрисовка начальной сетки
        self.draw_grid()

    def to_screen(self, logical_x, logical_y):
        """Перевод логических координат в экранные (с учетом центра и инверсии Y)"""
        screen_x = (self.center_x + logical_x) * self.cell_size
        # screen_y инвертирован, так как в Tkinter (0,0) сверху слева, а нам нужен декартов (снизу)
        screen_y = (self.center_y - logical_y) * self.cell_size
        return screen_x, screen_y

    def draw_pixel(self, x, y, color="black"):
        """Закрашивает логическую клетку (x, y)"""
        sx, sy = self.to_screen(x, y)
        # Рисуем квадрат, имитирующий пиксель
        self.canvas.create_rectangle(sx, sy, sx + self.cell_size, sy - self.cell_size,
                                     fill=color, outline="gray")

    def draw_pixel_alpha(self, x, y, alpha, color="black"):
        """Закрашивает пиксель с прозрачностью (alpha от 0 до 1)"""
        sx, sy = self.to_screen(x, y)
        # Создаем цвет с альфа-каналом (для простоты используем оттенки серого)
        intensity = int(255 * alpha)
        hex_color = f'#{intensity:02x}{intensity:02x}{intensity:02x}'
        self.canvas.create_rectangle(sx, sy, sx + self.cell_size, sy - self.cell_size,
                                     fill=hex_color, outline="")

    def draw_grid(self):
        self.canvas.delete("all")
        w = self.grid_width * self.cell_size
        h = self.grid_height * self.cell_size

        # Сетка
        for i in range(0, w + 1, self.cell_size):
            self.canvas.create_line(i, 0, i, h, fill="#eee")
        for i in range(0, h + 1, self.cell_size):
            self.canvas.create_line(0, i, w, i, fill="#eee")

        # Оси
        cx, cy = self.to_screen(0, 0)
        # Ось X
        self.canvas.create_line(0, cy, w, cy, width=2, arrow=tk.LAST)
        self.canvas.create_text(w - 10, cy + 15, text="X")
        # Ось Y
        self.canvas.create_line(cx, h, cx, 0, width=2, arrow=tk.LAST)
        self.canvas.create_text(cx + 15, 10, text="Y")

        # Подписи координат (каждые 5 клеток)
        for i in range(-self.center_x, self.grid_width - self.center_x + 1, 5):
            sx, sy = self.to_screen(i, 0)
            if i != 0: self.canvas.create_text(sx, sy + 10, text=str(i), font=("Arial", 8))

        for i in range(-self.center_y, self.grid_height - self.center_y + 1, 5):
            sx, sy = self.to_screen(0, i)
            if i != 0: self.canvas.create_text(sx + 15, sy, text=str(i), font=("Arial", 8))

    def clear_canvas(self):
        self.draw_grid()
        self.time_label.config(text="Время: 0.00 мкс")

    # --- АЛГОРИТМЫ ---

    def step_by_step(self, x1, y1, x2, y2):
        points = []
        if x1 == x2 and y1 == y2:
            points.append((x1, y1))
            return points

        dx = x2 - x1
        dy = y2 - y1

        steps = max(abs(dx), abs(dy))

        if steps == 0:
            return [(x1, y1)]

        # Здесь используем классический подход y = mx + b,
        # но адаптированный для всех октантов (итерация по большей дельте)
        if abs(dx) >= abs(dy):
            # Идем по X
            if x1 > x2: x1, x2, y1, y2 = x2, x1, y2, y1  # swap
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            for x in range(x1, x2 + 1):
                y = m * x + b
                points.append((x, round(y)))
        else:
            # Идем по Y (если наклон крутой)
            if y1 > y2: x1, x2, y1, y2 = x2, x1, y2, y1  # swap
            if (y2 - y1) == 0:
                m_inv = 0
            else:
                m_inv = (x2 - x1) / (y2 - y1)
            b_inv = x1 - m_inv * y1
            for y in range(y1, y2 + 1):
                x = m_inv * y + b_inv
                points.append((round(x), y))

        return points

    def dda(self, x1, y1, x2, y2):
        points = []
        dx = x2 - x1
        dy = y2 - y1

        steps = max(abs(dx), abs(dy))
        if steps == 0: return [(x1, y1)]

        x_inc = dx / steps
        y_inc = dy / steps

        x = x1
        y = y1

        for _ in range(steps + 1):
            points.append((round(x), round(y)))
            x += x_inc
            y += y_inc

        return points

    def bresenham_line(self, x1, y1, x2, y2):
        points = []

        # Определяем приращения
        dx = x2 - x1
        dy = y2 - y1

        # Определяем направление
        sx = 1 if dx > 0 else -1
        sy = 1 if dy > 0 else -1

        # Берем абсолютные значения
        dx = abs(dx)
        dy = abs(dy)

        # Определяем ведущую координату (большее приращение)
        if dx > dy:
            # X - ведущая координата
            leading_steps = dx
            k = dy / dx if dx != 0 else 0  # угловой коэффициент

            # Инициализация как на слайде
            x, y = x1, y1
            error = -0.5  # первоначальное значение ошибки = -1/2

            for i in range(leading_steps + 1):
                points.append((x, y))

                if i < leading_steps:  # чтобы не выйти за пределы
                    x += sx  # ведущая координата всегда увеличивается
                    error += k  # к ошибке прибавляется угловой коэффициент

                    if error > 0:
                        y += sy
                        error -= 1  # вычитаем 1, как в алгоритме на слайде
        else:
            # Y - ведущая координата
            leading_steps = dy
            k = dx / dy if dy != 0 else 0  # обратный угловой коэффициент

            # Инициализация
            x, y = x1, y1
            error = -0.5

            for i in range(leading_steps + 1):
                points.append((x, y))

                if i < leading_steps:
                    y += sy  # ведущая координата всегда увеличивается
                    error += k

                    if error > 0:
                        x += sx
                        error -= 1

        return points

    def bresenham_circle(self, xc, yc, r):
        points = []
        x = 0
        y = r
        d = 3 - 2 * r

        def add_points(xc, yc, x, y):
            # Симметрия (8 точек)
            pts = [
                (xc + x, yc + y), (xc - x, yc + y),
                (xc + x, yc - y), (xc - x, yc - y),
                (xc + y, yc + x), (xc - y, yc + x),
                (xc + y, yc - x), (xc - y, yc - x)
            ]
            return pts

        while y >= x:
            points.extend(add_points(xc, yc, x, y))
            x += 1
            if d > 0:
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
        return points

    # --- АЛГОРИТМ ВУ (СГЛАЖИВАНИЕ) ---
    def wu_line(self, x1, y1, x2, y2):
        """Алгоритм Ву для сглаженных линий"""
        points = []  # возвращаем список кортежей (x, y, alpha)

        # Проверка вырожденного случая
        if x1 == x2 and y1 == y2:
            return [(x1, y1, 1.0)]

        steep = abs(y2 - y1) > abs(x2 - x1)

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = y2 - y1

        if dx == 0:
            gradient = 1.0
        else:
            gradient = dy / dx

        # Первая конечная точка
        xend = round(x1)
        yend = y1 + gradient * (xend - x1)
        xgap = 1 - (x1 + 0.5) % 1
        xpxl1 = xend
        ypxl1 = math.floor(yend)

        if steep:
            points.append((ypxl1, xpxl1, (1 - (yend % 1)) * xgap))
            points.append((ypxl1 + 1, xpxl1, (yend % 1) * xgap))
        else:
            points.append((xpxl1, ypxl1, (1 - (yend % 1)) * xgap))
            points.append((xpxl1, ypxl1 + 1, (yend % 1) * xgap))

        intery = yend + gradient

        # Вторая конечная точка
        xend = round(x2)
        yend = y2 + gradient * (xend - x2)
        xgap = (x2 + 0.5) % 1
        xpxl2 = xend
        ypxl2 = math.floor(yend)

        if steep:
            points.append((ypxl2, xpxl2, (1 - (yend % 1)) * xgap))
            points.append((ypxl2 + 1, xpxl2, (yend % 1) * xgap))
        else:
            points.append((xpxl2, ypxl2, (1 - (yend % 1)) * xgap))
            points.append((xpxl2, ypxl2 + 1, (yend % 1) * xgap))

        # Основной цикл
        if steep:
            for x in range(int(xpxl1) + 1, int(xpxl2)):
                points.append((math.floor(intery), x, 1 - (intery % 1)))
                points.append((math.floor(intery) + 1, x, intery % 1))
                intery += gradient
        else:
            for x in range(int(xpxl1) + 1, int(xpxl2)):
                points.append((x, math.floor(intery), 1 - (intery % 1)))
                points.append((x, math.floor(intery) + 1, intery % 1))
                intery += gradient

        return points

    # --- АЛГОРИТМ КАСТЛА-ПИТВЕЯ ---
    def castle_pitway_line(self, x1, y1, x2, y2):
        points = []

        a = abs(x2 - x1)
        b = abs(y2 - y1)

        # Определяем направления
        sx = 1 if x2 >= x1 else -1
        sy = 1 if y2 >= y1 else -1

        y_val = b
        x_val = a - b

        m1 = "s"  # горизонтальный шаг
        m2 = "d"  # диагональный шаг

        # Алгоритм Евклида для строк
        while x_val != y_val:
            if x_val > y_val:
                x_val = x_val - y_val
                m2 = m1 + m2  # конкатенация строк
            else:
                y_val = y_val - x_val
                m1 = m2 + m1  # конкатенация строк

        # Финальная последовательность
        sequence = m2 + m1

        x, y = 0, 0
        points.append((x1, y1))

        for move in sequence:
            if move == 's':
                # Горизонтальный шаг
                x += sx
            elif move == 'd':
                # Диагональный шаг
                x += sx
                y += sy

            points.append((x1 + x, y1 + y))

        return points

    # --- ОБРАБОТЧИКИ СОБЫТИЙ ---
    def draw_line(self):
        try:
            x1 = int(self.entry_x1.get())
            y1 = int(self.entry_y1.get())
            x2 = int(self.entry_x2.get())
            y2 = int(self.entry_y2.get())

            algo = self.line_algo_var.get()

            start_time = time.perf_counter()

            if algo == "step":
                points = self.step_by_step(x1, y1, x2, y2)
                color = "blue"
            elif algo == "dda":
                points = self.dda(x1, y1, x2, y2)
                color = "green"
            elif algo == "bres_line":
                points = self.bresenham_line(x1, y1, x2, y2)
                color = "red"

            end_time = time.perf_counter()

            elapsed_us = (end_time - start_time) * 1_000_000
            self.time_label.config(text=f"Время (Линия): {elapsed_us:.2f} мкс")

            for px, py in points:
                self.draw_pixel(px, py, color=color)

        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа для координат линии (x1, y1, x2, y2)")

    def draw_circle(self):
        try:
            xc = int(self.entry_xc.get())
            yc = int(self.entry_yc.get())
            r = int(self.entry_r.get())

            if r <= 0:
                messagebox.showerror("Ошибка", "Радиус должен быть > 0")
                return

            start_time = time.perf_counter()
            points = self.bresenham_circle(xc, yc, r)
            end_time = time.perf_counter()

            elapsed_us = (end_time - start_time) * 1_000_000
            self.time_label.config(text=f"Время (Круг): {elapsed_us:.2f} мкс")

            for px, py in points:
                self.draw_pixel(px, py, color="magenta")

        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа для центра и радиуса (Xc, Yc, R)")

    def draw_wu_line(self):
        """Обработчик для рисования сглаженной линии алгоритмом Ву"""
        try:
            x1 = int(self.entry_x1.get())
            y1 = int(self.entry_y1.get())
            x2 = int(self.entry_x2.get())
            y2 = int(self.entry_y2.get())

            start_time = time.perf_counter()
            points = self.wu_line(x1, y1, x2, y2)
            end_time = time.perf_counter()

            elapsed_us = (end_time - start_time) * 1_000_000
            self.time_label.config(text=f"Время (Ву): {elapsed_us:.2f} мкс")

            # Рисуем точки с прозрачностью
            for px, py, alpha in points:
                self.draw_pixel_alpha(px, py, alpha, color="orange")

        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа для координат линии (x1, y1, x2, y2)")

    def draw_castle_pitway_line(self):
        """Обработчик для рисования линии алгоритмом Кастла-Питвея"""
        try:
            x1 = int(self.entry_x1.get())
            y1 = int(self.entry_y1.get())
            x2 = int(self.entry_x2.get())
            y2 = int(self.entry_y2.get())

            start_time = time.perf_counter()
            points = self.castle_pitway_line(x1, y1, x2, y2)
            end_time = time.perf_counter()

            elapsed_us = (end_time - start_time) * 1_000_000
            self.time_label.config(text=f"Время (Кастла-Питвея): {elapsed_us:.2f} мкс")

            for px, py in points:
                self.draw_pixel(px, py, color="purple")

        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа для координат линии (x1, y1, x2, y2)")


if __name__ == "__main__":
    root = tk.Tk()
    app = RasterApp(root)
    root.mainloop()
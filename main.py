import tkinter as tk
from tkinter import ttk, font
import time
import math

class RasterAlgorithmsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Растровые алгоритмы")
        self.geometry("1000x700")
        self.configure(bg="#f0f0f0")
        self.scale = 1
        self.point_size = 3
        self.create_fonts()
        self.create_widgets()
        self.setup_canvas()

    def create_fonts(self):
        self.label_font = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=14, weight="bold")

    def create_widgets(self):
        # Панель управления слева
        control_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=20)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        header_label = tk.Label(control_frame, text="Растровые алгоритмы", font=("Arial", 16, "bold"), bg="#f0f0f0")
        header_label.grid(row=0, column=0, columnspan=2, pady=10)

        algorithm_label = tk.Label(control_frame, text="Выберите алгоритм:", bg="#f0f0f0", font=self.label_font)
        algorithm_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        # Список алгоритмов
        self.algorithm = tk.StringVar(value="DDA")
        algorithms = [
            ("Пошаговый алгоритм", "step"),
            ("Алгоритм ЦДА", "DDA"),
            ("Алгоритм Брезенхема (отрезок)", "bresenham_line"),
            ("Алгоритм Брезенхема (окружность)", "bresenham_circle")
        ]
        for i, (text, mode) in enumerate(algorithms):
            rb = tk.Radiobutton(control_frame, text=text, variable=self.algorithm, value=mode, bg="#f0f0f0", font=self.label_font)
            rb.grid(row=2+i, column=0, sticky=tk.W, pady=3)

        # Ввод координат начальной и конечной точки
        tk.Label(control_frame, text="Начальная точка (x0, y0):", bg="#f0f0f0", font=self.label_font).grid(row=6, column=0, sticky=tk.W, pady=5)
        self.x0_entry = self.create_entry(control_frame, row=6, column=1)
        self.y0_entry = self.create_entry(control_frame, row=7, column=1)

        tk.Label(control_frame, text="Конечная точка (x1, y1):", bg="#f0f0f0", font=self.label_font).grid(row=8, column=0, sticky=tk.W, pady=5)
        self.x1_entry = self.create_entry(control_frame, row=8, column=1)
        self.y1_entry = self.create_entry(control_frame, row=9, column=1)

        # Ввод для окружности
        tk.Label(control_frame, text="Центр окружности (xc, yc):", bg="#f0f0f0", font=self.label_font).grid(row=10, column=0, sticky=tk.W, pady=5)
        self.xc_entry = self.create_entry(control_frame, row=10, column=1)
        self.yc_entry = self.create_entry(control_frame, row=11, column=1)

        tk.Label(control_frame, text="Радиус (r):", bg="#f0f0f0", font=self.label_font).grid(row=12, column=0, sticky=tk.W, pady=5)
        self.r_entry = self.create_entry(control_frame, row=12, column=1)

        # Кнопки
        self.create_buttons(control_frame)

        # Метка времени выполнения
        self.time_label = tk.Label(control_frame, text="Время выполнения: N/A", bg="#f0f0f0", font=self.label_font)
        self.time_label.grid(row=13, column=0, columnspan=2, pady=10)

    def create_entry(self, parent, row, column):
        entry = tk.Entry(parent, font=self.label_font, width=12)
        entry.grid(row=row, column=column, sticky=tk.W, padx=5, pady=3)
        return entry

    def create_buttons(self, parent):
        button_frame = tk.Frame(parent, bg="#f0f0f0")
        button_frame.grid(row=14, column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="Отрисовать", command=self.draw, font=self.button_font, bg="#4CAF50", fg="white", relief="solid", width=20).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Очистить", command=self.clear_canvas, font=self.button_font, bg="#f44336", fg="white", relief="solid", width=20).grid(row=0, column=1, padx=5, pady=5)

        zoom_frame = tk.Frame(parent, bg="#f0f0f0")
        zoom_frame.grid(row=15, column=0, columnspan=2, pady=10)

        tk.Button(zoom_frame, text="Увеличить масштаб", command=self.zoom_in, font=self.button_font, bg="#FF9800", fg="white", relief="solid", width=20).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(zoom_frame, text="Уменьшить масштаб", command=self.zoom_out, font=self.button_font, bg="#FF9800", fg="white", relief="solid", width=20).grid(row=0, column=1, padx=5, pady=5)

    def setup_canvas(self):
        self.canvas = tk.Canvas(self, bg="white", bd=0)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda event: self.draw_grid())
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("grid")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        ox = width // 2
        oy = height // 2
        base_grid_step = 20
        grid_step = base_grid_step * self.scale

        if grid_step == 0:
            grid_step = 1

        min_label_spacing = 50
        label_step = max(1, math.ceil(min_label_spacing / grid_step))

        new_font_size = max(8, min(int(20 / self.scale), 20))
        self.label_font.configure(size=new_font_size)

        for i in range(int(-ox / grid_step), int(ox / grid_step) + 1):
            x = ox + i * grid_step
            self.canvas.create_line(x, 0, x, height, fill="lightgrey", tag="grid")
            if i != 0 and i % label_step == 0:
                self.canvas.create_text(x, oy + 15, text=str(i), fill="black", font=self.label_font, tag="grid_text")

        for i in range(int(-oy / grid_step), int(oy / grid_step) + 1):
            y = oy + i * grid_step
            self.canvas.create_line(0, y, width, y, fill="lightgrey", tag="grid")
            if i != 0 and i % label_step == 0:
                self.canvas.create_text(ox + 15, y, text=str(-i), fill="black", font=self.label_font, tag="grid_text")

        self.canvas.create_line(ox, 0, ox, height, fill="black", arrow=tk.LAST, tag="grid")
        self.canvas.create_line(0, oy, width, oy, fill="black", arrow=tk.LAST, tag="grid")
        self.canvas.create_text(ox - 10, oy + 10, text="0", fill="black", font=self.label_font, tag="grid_text")
        self.canvas.create_text(width - 10, oy + 10, text="X", fill="black", font=self.label_font, tag="grid_text")
        self.canvas.create_text(ox + 10, 10, text="Y", fill="black", font=self.label_font, tag="grid_text")

        self.canvas.tag_raise("grid_text")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.time_label.config(text="Время выполнения: N/A")

    def draw(self):
        self.clear_canvas()
        alg = self.algorithm.get()
        start_time = time.time()
        if alg == "step":
            self.step_by_step()
        elif alg == "DDA":
            self.dda_algorithm()
        elif alg == "bresenham_line":
            self.bresenham_line()
        elif alg == "bresenham_circle":
            self.bresenham_circle()
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000  # Время в миллисекундах
        self.time_label.config(text=f"Время выполнения: {elapsed_time:.3f} мс")

    def put_pixel(self, x, y):
        self.canvas.create_rectangle(x * self.scale + self.canvas.winfo_width() // 2,
                                      -y * self.scale + self.canvas.winfo_height() // 2,
                                      x * self.scale + self.canvas.winfo_width() // 2 + self.point_size,
                                      -y * self.scale + self.canvas.winfo_height() // 2 + self.point_size,
                                      fill="black", outline="black")

    def step_by_step(self):
        x0 = int(self.x0_entry.get())
        y0 = int(self.y0_entry.get())
        x1 = int(self.x1_entry.get())
        y1 = int(self.y1_entry.get())
        self.put_pixel(x0, y0)
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy))
        x_inc = dx / steps
        y_inc = dy / steps
        x = x0
        y = y0
        for i in range(steps):
            self.put_pixel(round(x), round(y))
            x += x_inc
            y += y_inc
            time.sleep(0.01)

    def dda_algorithm(self):
        x0 = int(self.x0_entry.get())
        y0 = int(self.y0_entry.get())
        x1 = int(self.x1_entry.get())
        y1 = int(self.y1_entry.get())
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy))
        x_inc = dx / steps
        y_inc = dy / steps
        x = x0
        y = y0
        self.put_pixel(x, y)
        for i in range(steps):
            x += x_inc
            y += y_inc
            self.put_pixel(round(x), round(y))

    def bresenham_line(self):
        x0 = int(self.x0_entry.get())
        y0 = int(self.y0_entry.get())
        x1 = int(self.x1_entry.get())
        y1 = int(self.y1_entry.get())

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            self.put_pixel(x0, y0)
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def bresenham_circle(self):
        xc = int(self.xc_entry.get())
        yc = int(self.yc_entry.get())
        r = int(self.r_entry.get())
        x = 0
        y = r
        p = 3 - 2 * r
        self.put_pixel(xc + x, yc - y)
        self.put_pixel(xc - x, yc - y)
        self.put_pixel(xc + x, yc + y)
        self.put_pixel(xc - x, yc + y)
        self.put_pixel(xc + y, yc - x)
        self.put_pixel(xc - y, yc - x)
        self.put_pixel(xc + y, yc + x)
        self.put_pixel(xc - y, yc + x)

        while x < y:
            x += 1
            if p < 0:
                p += 4 * x + 6
            else:
                y -= 1
                p += 4 * (x - y) + 10
            self.put_pixel(xc + x, yc - y)
            self.put_pixel(xc - x, yc - y)
            self.put_pixel(xc + x, yc + y)
            self.put_pixel(xc - x, yc + y)
            self.put_pixel(xc + y, yc - x)
            self.put_pixel(xc - y, yc - x)
            self.put_pixel(xc + y, yc + x)
            self.put_pixel(xc - y, yc + x)

    def zoom_in(self):
        self.scale *= 1.1
        self.draw_grid()

    def zoom_out(self):
        self.scale /= 1.1
        self.draw_grid()

if __name__ == "__main__":
    app = RasterAlgorithmsApp()
    app.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter import messagebox


class ColorConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Models Converter")
        self.root.geometry("800x500")

        self.r_var = tk.IntVar(value=128)
        self.g_var = tk.IntVar(value=128)
        self.b_var = tk.IntVar(value=128)

        self.c_var = tk.DoubleVar(value=0.0)
        self.m_var = tk.DoubleVar(value=0.0)
        self.y_var = tk.DoubleVar(value=0.0)
        self.k_var = tk.DoubleVar(value=0.0)

        self.h_var = tk.DoubleVar(value=0.0)
        self.s_var = tk.DoubleVar(value=0.0)
        self.v_var = tk.DoubleVar(value=0.5)

        self.create_widgets()
        self.update_all_models()

    def validate_input(self, value, min_val, max_val):
        try:
            num = float(value)
            return min_val <= num <= max_val
        except ValueError:
            return False

    def validate_rgb_input(self):
        corrections = []

        if not self.validate_input(self.r_var.get(), 0, 255):
            old_val = self.r_var.get()
            new_val = max(0, min(255, self.r_var.get()))
            self.r_var.set(new_val)
            corrections.append(f"Red: {old_val} → {new_val}")

        if not self.validate_input(self.g_var.get(), 0, 255):
            old_val = self.g_var.get()
            new_val = max(0, min(255, self.g_var.get()))
            self.g_var.set(new_val)
            corrections.append(f"Green: {old_val} → {new_val}")

        if not self.validate_input(self.b_var.get(), 0, 255):
            old_val = self.b_var.get()
            new_val = max(0, min(255, self.b_var.get()))
            self.b_var.set(new_val)
            corrections.append(f"Blue: {old_val} → {new_val}")

        return corrections

    def validate_cmyk_input(self):
        corrections = []

        if not self.validate_input(self.c_var.get(), 0, 1):
            old_val = self.c_var.get()
            new_val = max(0.0, min(1.0, self.c_var.get()))
            self.c_var.set(round(new_val, 3))
            corrections.append(f"Cyan: {old_val:.3f} → {new_val:.3f}")

        if not self.validate_input(self.m_var.get(), 0, 1):
            old_val = self.m_var.get()
            new_val = max(0.0, min(1.0, self.m_var.get()))
            self.m_var.set(round(new_val, 3))
            corrections.append(f"Magenta: {old_val:.3f} → {new_val:.3f}")

        if not self.validate_input(self.y_var.get(), 0, 1):
            old_val = self.y_var.get()
            new_val = max(0.0, min(1.0, self.y_var.get()))
            self.y_var.set(round(new_val, 3))
            corrections.append(f"Yellow: {old_val:.3f} → {new_val:.3f}")

        if not self.validate_input(self.k_var.get(), 0, 1):
            old_val = self.k_var.get()
            new_val = max(0.0, min(1.0, self.k_var.get()))
            self.k_var.set(round(new_val, 3))
            corrections.append(f"Black: {old_val:.3f} → {new_val:.3f}")

        return corrections

    def validate_hsv_input(self):
        corrections = []

        if not self.validate_input(self.h_var.get(), 0, 360):
            old_val = self.h_var.get()
            new_val = max(0.0, min(360.0, self.h_var.get()))
            self.h_var.set(round(new_val, 1))
            corrections.append(f"Hue: {old_val:.1f} → {new_val:.1f}")

        if not self.validate_input(self.s_var.get(), 0, 1):
            old_val = self.s_var.get()
            new_val = max(0.0, min(1.0, self.s_var.get()))
            self.s_var.set(round(new_val, 3))
            corrections.append(f"Saturation: {old_val:.3f} → {new_val:.3f}")

        if not self.validate_input(self.v_var.get(), 0, 1):
            old_val = self.v_var.get()
            new_val = max(0.0, min(1.0, self.v_var.get()))
            self.v_var.set(round(new_val, 3))
            corrections.append(f"Value: {old_val:.3f} → {new_val:.3f}")

        return corrections

    def show_correction_message(self, corrections, model_name):
        if corrections:
            message = f"В модели {model_name} значения выходят за допустимые диапазоны:\n\n"
            message += "\n".join(corrections)
            message += "\n\nЗначения были автоматически скорректированы."
            messagebox.showwarning("Корректировка значений", message)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.color_display = tk.Canvas(main_frame, width=200, height=100, bg='#808080')
        self.color_display.grid(row=0, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        self.color_display.bind("<Button-1>", self.choose_color_from_palette)

        rgb_frame = ttk.LabelFrame(main_frame, text="RGB", padding="5")
        rgb_frame.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.create_rgb_controls(rgb_frame)

        cmyk_frame = ttk.LabelFrame(main_frame, text="CMYK", padding="5")
        cmyk_frame.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.create_cmyk_controls(cmyk_frame)

        hsv_frame = ttk.LabelFrame(main_frame, text="HSV", padding="5")
        hsv_frame.grid(row=1, column=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.create_hsv_controls(hsv_frame)

    def create_rgb_controls(self, parent):
        ttk.Label(parent, text="Red (0-255):").grid(row=0, column=0, sticky=tk.W)
        red_scale = ttk.Scale(parent, from_=0, to=255, variable=self.r_var,
                              command=self.update_from_rgb, orient=tk.HORIZONTAL)
        red_scale.grid(row=0, column=1, sticky=(tk.W, tk.E))
        red_entry = ttk.Entry(parent, textvariable=self.r_var, width=5)
        red_entry.grid(row=0, column=2, padx=5)
        red_entry.bind('<Return>', self.update_from_rgb_entry)

        ttk.Label(parent, text="Green (0-255):").grid(row=1, column=0, sticky=tk.W)
        green_scale = ttk.Scale(parent, from_=0, to=255, variable=self.g_var,
                                command=self.update_from_rgb, orient=tk.HORIZONTAL)
        green_scale.grid(row=1, column=1, sticky=(tk.W, tk.E))
        green_entry = ttk.Entry(parent, textvariable=self.g_var, width=5)
        green_entry.grid(row=1, column=2, padx=5)
        green_entry.bind('<Return>', self.update_from_rgb_entry)

        ttk.Label(parent, text="Blue (0-255):").grid(row=2, column=0, sticky=tk.W)
        blue_scale = ttk.Scale(parent, from_=0, to=255, variable=self.b_var,
                               command=self.update_from_rgb, orient=tk.HORIZONTAL)
        blue_scale.grid(row=2, column=1, sticky=(tk.W, tk.E))
        blue_entry = ttk.Entry(parent, textvariable=self.b_var, width=5)
        blue_entry.grid(row=2, column=2, padx=5)
        blue_entry.bind('<Return>', self.update_from_rgb_entry)

    def create_cmyk_controls(self, parent):
        ttk.Label(parent, text="Cyan (0-1):").grid(row=0, column=0, sticky=tk.W)
        cyan_scale = ttk.Scale(parent, from_=0, to=1, variable=self.c_var,
                               command=self.update_from_cmyk, orient=tk.HORIZONTAL)
        cyan_scale.grid(row=0, column=1, sticky=(tk.W, tk.E))
        cyan_entry = ttk.Entry(parent, textvariable=self.c_var, width=5)
        cyan_entry.grid(row=0, column=2, padx=5)
        cyan_entry.bind('<Return>', self.update_from_cmyk_entry)

        ttk.Label(parent, text="Magenta (0-1):").grid(row=1, column=0, sticky=tk.W)
        magenta_scale = ttk.Scale(parent, from_=0, to=1, variable=self.m_var,
                                  command=self.update_from_cmyk, orient=tk.HORIZONTAL)
        magenta_scale.grid(row=1, column=1, sticky=(tk.W, tk.E))
        magenta_entry = ttk.Entry(parent, textvariable=self.m_var, width=5)
        magenta_entry.grid(row=1, column=2, padx=5)
        magenta_entry.bind('<Return>', self.update_from_cmyk_entry)

        ttk.Label(parent, text="Yellow (0-1):").grid(row=2, column=0, sticky=tk.W)
        yellow_scale = ttk.Scale(parent, from_=0, to=1, variable=self.y_var,
                                 command=self.update_from_cmyk, orient=tk.HORIZONTAL)
        yellow_scale.grid(row=2, column=1, sticky=(tk.W, tk.E))
        yellow_entry = ttk.Entry(parent, textvariable=self.y_var, width=5)
        yellow_entry.grid(row=2, column=2, padx=5)
        yellow_entry.bind('<Return>', self.update_from_cmyk_entry)

        ttk.Label(parent, text="Black (0-1):").grid(row=3, column=0, sticky=tk.W)
        black_scale = ttk.Scale(parent, from_=0, to=1, variable=self.k_var,
                                command=self.update_from_cmyk, orient=tk.HORIZONTAL)
        black_scale.grid(row=3, column=1, sticky=(tk.W, tk.E))
        black_entry = ttk.Entry(parent, textvariable=self.k_var, width=5)
        black_entry.grid(row=3, column=2, padx=5)
        black_entry.bind('<Return>', self.update_from_cmyk_entry)

    def create_hsv_controls(self, parent):
        ttk.Label(parent, text="Hue (0-360):").grid(row=0, column=0, sticky=tk.W)
        hue_scale = ttk.Scale(parent, from_=0, to=360, variable=self.h_var,
                              command=self.update_from_hsv, orient=tk.HORIZONTAL)
        hue_scale.grid(row=0, column=1, sticky=(tk.W, tk.E))
        hue_entry = ttk.Entry(parent, textvariable=self.h_var, width=5)
        hue_entry.grid(row=0, column=2, padx=5)
        hue_entry.bind('<Return>', self.update_from_hsv_entry)

        ttk.Label(parent, text="Saturation (0-1):").grid(row=1, column=0, sticky=tk.W)
        saturation_scale = ttk.Scale(parent, from_=0, to=1, variable=self.s_var,
                                     command=self.update_from_hsv, orient=tk.HORIZONTAL)
        saturation_scale.grid(row=1, column=1, sticky=(tk.W, tk.E))
        saturation_entry = ttk.Entry(parent, textvariable=self.s_var, width=5)
        saturation_entry.grid(row=1, column=2, padx=5)
        saturation_entry.bind('<Return>', self.update_from_hsv_entry)

        ttk.Label(parent, text="Value (0-1):").grid(row=2, column=0, sticky=tk.W)
        value_scale = ttk.Scale(parent, from_=0, to=1, variable=self.v_var,
                                command=self.update_from_hsv, orient=tk.HORIZONTAL)
        value_scale.grid(row=2, column=1, sticky=(tk.W, tk.E))
        value_entry = ttk.Entry(parent, textvariable=self.v_var, width=5)
        value_entry.grid(row=2, column=2, padx=5)
        value_entry.bind('<Return>', self.update_from_hsv_entry)

    def choose_color_from_palette(self, event):
        color = askcolor(initialcolor=self.get_hex_color())[1]
        if color:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            self.update_from_rgb_values(r, g, b)

    def get_hex_color(self):
        return f"#{self.r_var.get():02x}{self.g_var.get():02x}{self.b_var.get():02x}"

    def update_color_display(self):
        self.color_display.configure(bg=self.get_hex_color())

    def update_from_rgb(self, *args):
        r, g, b = self.r_var.get(), self.g_var.get(), self.b_var.get()
        self.rgb_to_cmyk(r, g, b)
        self.rgb_to_hsv(r, g, b)
        self.update_color_display()

    def update_from_rgb_entry(self, event):
        corrections = self.validate_rgb_input()
        if corrections:
            self.show_correction_message(corrections, "RGB")
        self.update_from_rgb()

    def update_from_cmyk(self, *args):
        c, m, y, k = self.c_var.get(), self.m_var.get(), self.y_var.get(), self.k_var.get()
        r, g, b = self.cmyk_to_rgb(c, m, y, k)
        self.r_var.set(int(r))
        self.g_var.set(int(g))
        self.b_var.set(int(b))
        self.rgb_to_hsv(r, g, b)
        self.update_color_display()

    def update_from_cmyk_entry(self, event):
        corrections = self.validate_cmyk_input()
        if corrections:
            self.show_correction_message(corrections, "CMYK")
        self.update_from_cmyk()

    def update_from_hsv(self, *args):
        h, s, v = self.h_var.get(), self.s_var.get(), self.v_var.get()
        r, g, b = self.hsv_to_rgb(h, s, v)
        self.r_var.set(int(r))
        self.g_var.set(int(g))
        self.b_var.set(int(b))
        self.rgb_to_cmyk(r, g, b)
        self.update_color_display()

    def update_from_hsv_entry(self, event):
        corrections = self.validate_hsv_input()
        if corrections:
            self.show_correction_message(corrections, "HSV")
        self.update_from_hsv()

    def update_from_rgb_values(self, r, g, b):
        self.r_var.set(r)
        self.g_var.set(g)
        self.b_var.set(b)
        self.update_from_rgb()

    def update_all_models(self):
        self.update_from_rgb()

    def rgb_to_cmyk(self, r, g, b):
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0

        k = 1 - max(r_norm, g_norm, b_norm)

        if k == 1:
            c = m = y = 0
        else:
            c = (1 - r_norm - k) / (1 - k)
            m = (1 - g_norm - k) / (1 - k)
            y = (1 - b_norm - k) / (1 - k)

        self.c_var.set(round(c, 3))
        self.m_var.set(round(m, 3))
        self.y_var.set(round(y, 3))
        self.k_var.set(round(k, 3))

    def cmyk_to_rgb(self, c, m, y, k):
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)

        return r, g, b

    def rgb_to_hsv(self, r, g, b):
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0

        max_val = max(r_norm, g_norm, b_norm)
        min_val = min(r_norm, g_norm, b_norm)
        diff = max_val - min_val

        v = max_val

        if max_val == 0:
            s = 0
        else:
            s = diff / max_val

        if diff == 0:
            h = 0
        else:
            if max_val == r_norm:
                h = (g_norm - b_norm) / diff
                if h < 0:
                    h += 6
            elif max_val == g_norm:
                h = 2 + (b_norm - r_norm) / diff
            else:
                h = 4 + (r_norm - g_norm) / diff

            h *= 60

        self.h_var.set(round(h, 1))
        self.s_var.set(round(s, 3))
        self.v_var.set(round(v, 3))

    def hsv_to_rgb(self, h, s, v):
        h = h % 360
        if h < 0:
            h += 360

        h_normalized = h / 60.0
        sector = int(h_normalized)
        fractional = h_normalized - sector

        p = v * (1 - s)
        q = v * (1 - s * fractional)
        t = v * (1 - s * (1 - fractional))

        if sector == 0:
            r, g, b = v, t, p
        elif sector == 1:
            r, g, b = q, v, p
        elif sector == 2:
            r, g, b = p, v, t
        elif sector == 3:
            r, g, b = p, q, v
        elif sector == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q

        return r * 255, g * 255, b * 255


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorConverterApp(root)
    root.mainloop()

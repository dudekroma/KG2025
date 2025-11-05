import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка изображений - Вариант 3")
        self.root.geometry("1000x700")

        self.original_image = None
        self.processed_image = None

        self.create_widgets()

    def create_widgets(self):
        # Верхняя панель - загрузка/сохранение
        top_frame = Frame(self.root)
        top_frame.pack(fill=X, padx=10, pady=5)

        Button(top_frame, text="Загрузить изображение", command=self.load_image).pack(side=LEFT, padx=5)
        Button(top_frame, text="Сохранить результат", command=self.save_image).pack(side=LEFT, padx=5)

        # Основной контейнер
        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Левая панель - управление
        left_frame = Frame(main_frame)
        left_frame.pack(side=LEFT, fill=Y, padx=5)

        # Правая панель - изображения
        right_frame = Frame(main_frame)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)

        # === ГИСТОГРАММА И КОНТРАСТИРОВАНИЕ ===
        hist_frame = LabelFrame(left_frame, text="Гистограмма и контрастирование", pady=10)
        hist_frame.pack(fill=X, pady=5)

        Button(hist_frame, text="Лин контрастирование",
               command=self.linear_contrast, width=20).pack(pady=2)
        Button(hist_frame, text="Эквализация RGB",
               command=self.histogram_equalization_rgb, width=20).pack(pady=2)
        Button(hist_frame, text="Эквализация HSV",
               command=self.histogram_equalization_hsv, width=20).pack(pady=2)
        Button(hist_frame, text="Показать гистограммы",
               command=self.show_histograms, width=20).pack(pady=2)

        # === УВЕЛИЧЕНИЕ РЕЗКОСТИ ===
        sharp_frame = LabelFrame(left_frame, text="Увеличение резкости", pady=10)
        sharp_frame.pack(fill=X, pady=5)

        Button(sharp_frame, text="Фильтр Лапласиана",
               command=self.laplacian_sharpen, width=20).pack(pady=2)
        Button(sharp_frame, text="Фильтр Собеля",
               command=self.sobel_sharpen, width=20).pack(pady=2)
        Button(sharp_frame, text="Unsharp Masking",
               command=self.unsharp_masking, width=20).pack(pady=2)

        # Параметр силы резкости
        Label(sharp_frame, text="Сила резкости:").pack(pady=5)
        self.sharp_strength = Scale(sharp_frame, from_=0.1, to=3.0,
                                    resolution=0.1, orient=HORIZONTAL, length=150)
        self.sharp_strength.set(1.0)
        self.sharp_strength.pack(pady=5)

        # Информационная панель
        info_frame = LabelFrame(left_frame, text="Информация", pady=10)
        info_frame.pack(fill=X, pady=5)

        self.info_text = Text(info_frame, height=8, width=25)
        self.info_text.pack(fill=BOTH, padx=5, pady=5)

        # === ОБЛАСТЬ ИЗОБРАЖЕНИЙ ===
        # Оригинальное изображение
        orig_frame = LabelFrame(right_frame, text="Оригинальное изображение")
        orig_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

        self.original_canvas = Canvas(orig_frame, width=350, height=350, bg="gray")
        self.original_canvas.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Обработанное изображение
        proc_frame = LabelFrame(right_frame, text="Обработанное изображение")
        proc_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)

        self.processed_canvas = Canvas(proc_frame, width=350, height=350, bg="gray")
        self.processed_canvas.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Фрейм для гистограмм
        self.hist_frame = Frame(self.root)
        self.hist_frame.pack(fill=X, padx=10, pady=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.original_image = cv2.imread(file_path)
            if self.original_image is not None:
                self.processed_image = self.original_image.copy()
                self.display_images()
                self.add_info("Изображение загружено")
                self.show_histograms()

    def display_images(self):
        if self.original_image is not None:
            display_original = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            display_original = self.resize_image(display_original, 350)
            self.original_photo = ImageTk.PhotoImage(Image.fromarray(display_original))
            self.original_canvas.create_image(175, 175, anchor=CENTER, image=self.original_photo)

        if self.processed_image is not None:
            display_processed = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
            display_processed = self.resize_image(display_processed, 350)
            self.processed_photo = ImageTk.PhotoImage(Image.fromarray(display_processed))
            self.processed_canvas.create_image(175, 175, anchor=CENTER, image=self.processed_photo)

    def resize_image(self, image, max_size):
        h, w = image.shape[:2]
        if h > w:
            new_h = max_size
            new_w = int(w * max_size / h)
        else:
            new_w = max_size
            new_h = int(h * max_size / w)
        return cv2.resize(image, (new_w, new_h))

    def add_info(self, message):
        self.info_text.insert(END, message + "\n")
        self.info_text.see(END)

    # === МЕТОДЫ ГИСТОГРАММЫ И КОНТРАСТИРОВАНИЯ ===
    def linear_contrast(self):
        if self.original_image is None: return

        img = self.original_image.copy()
        result = np.zeros_like(img)

        for i in range(3):
            channel = img[:, :, i]
            min_val, max_val = np.min(channel), np.max(channel)
            if max_val > min_val:
                result[:, :, i] = ((channel - min_val) * (255.0 / (max_val - min_val))).astype(np.uint8)
            else:
                result[:, :, i] = channel

        self.processed_image = result
        self.display_images()
        self.add_info("Линейное контрастирование")
        self.show_histograms()

    def histogram_equalization_rgb(self):
        if self.original_image is None: return

        img = self.original_image.copy()
        channels = cv2.split(img)
        eq_channels = [cv2.equalizeHist(ch) for ch in channels]
        result = cv2.merge(eq_channels)

        self.processed_image = result
        self.display_images()
        self.add_info("Эквализация RGB")
        self.show_histograms()

    def histogram_equalization_hsv(self):
        if self.original_image is None: return

        img = self.original_image.copy()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        self.processed_image = result
        self.display_images()
        self.add_info("Эквализация HSV")
        self.show_histograms()

    # === МЕТОДЫ УВЕЛИЧЕНИЯ РЕЗКОСТИ ===
    def laplacian_sharpen(self):
        if self.original_image is None: return

        img = self.original_image.copy()
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        strength = self.sharp_strength.get()
        result = img - strength * laplacian
        result = np.clip(result, 0, 255).astype(np.uint8)

        self.processed_image = result
        self.display_images()
        self.add_info(f"Лапласиан (сила: {strength})")

    def sobel_sharpen(self):
        if self.original_image is None: return

        img = self.original_image.copy()
        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        sobel_combined = np.sqrt(sobelx ** 2 + sobely ** 2)
        strength = self.sharp_strength.get()
        result = img + strength * sobel_combined
        result = np.clip(result, 0, 255).astype(np.uint8)

        self.processed_image = result
        self.display_images()
        self.add_info(f"Собель (сила: {strength})")

    def unsharp_masking(self):
        if self.original_image is None: return

        img = self.original_image.copy()
        blurred = cv2.GaussianBlur(img, (0, 0), 3.0)
        high_freq = img - blurred
        strength = self.sharp_strength.get()
        result = img + strength * high_freq
        result = np.clip(result, 0, 255).astype(np.uint8)

        self.processed_image = result
        self.display_images()
        self.add_info(f"Unsharp Masking (сила: {strength})")

    def show_histograms(self):
        if self.original_image is None: return

        for widget in self.hist_frame.winfo_children():
            widget.destroy()

        orig_gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        proc_gray = cv2.cvtColor(self.processed_image,
                                 cv2.COLOR_BGR2GRAY) if self.processed_image is not None else orig_gray

        plt.figure(figsize=(10, 3))

        plt.subplot(1, 2, 1)
        plt.hist(orig_gray.ravel(), 256, [0, 256], color='blue', alpha=0.7)
        plt.title('Оригинал')
        plt.xlabel('Яркость')
        plt.ylabel('Частота')

        plt.subplot(1, 2, 2)
        plt.hist(proc_gray.ravel(), 256, [0, 256], color='red', alpha=0.7)
        plt.title('Обработанный')
        plt.xlabel('Яркость')
        plt.ylabel('Частота')

        plt.tight_layout()
        plt.savefig('temp_hist.png', dpi=100, bbox_inches='tight')
        plt.close()

        hist_img = Image.open('temp_hist.png')
        hist_img = hist_img.resize((600, 200), Image.Resampling.LANCZOS)
        hist_photo = ImageTk.PhotoImage(hist_img)

        hist_label = Label(self.hist_frame, image=hist_photo)
        hist_label.image = hist_photo
        hist_label.pack()

    def save_image(self):
        if self.processed_image is None: return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
        )
        if file_path:
            cv2.imwrite(file_path, self.processed_image)
            self.add_info(f"Сохранено: {file_path}")


if __name__ == "__main__":
    root = Tk()
    app = ImageProcessor(root)
    root.mainloop()
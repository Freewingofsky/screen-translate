from tkinter import Tk, Canvas, Frame, Button
from PIL import ImageGrab
import pytesseract
from translator import Translator
from dummy_translation_service import GoogleTranslationService
import time

class ScreenTranslatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Screen Translator")
        self.canvas = Canvas(master, cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.translator = Translator(GoogleTranslationService())

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.translate_button = Button(master, text="Translate", command=self.translate_area)
        self.translate_button.pack()

        self.is_translating = False
        self.interval_ms = 1500  # 每1.5秒翻譯一次
        self.start_live_button = Button(master, text="開始即時翻譯", command=self.start_live_translate)
        self.start_live_button.pack()
        self.stop_live_button = Button(master, text="停止即時翻譯", command=self.stop_live_translate)
        self.stop_live_button.pack()

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def translate_area(self):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        text = pytesseract.image_to_string(img, lang='jpn')
        translation = self.translator.translate_text(text)
        print("Translated Text:", translation)

    def start_live_translate(self):
        self.is_translating = True
        self.live_translate()

    def stop_live_translate(self):
        self.is_translating = False

    def live_translate(self):
        if self.is_translating and self.rect is not None:
            try:
                x1, y1, x2, y2 = self.canvas.coords(self.rect)
                img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                text = pytesseract.image_to_string(img, lang='jpn')
                translation = self.translator.translate_text(text)
                print("[即時翻譯]", translation)
            except Exception as e:
                print("翻譯失敗:", e)
            self.master.after(self.interval_ms, self.live_translate)

if __name__ == "__main__":
    root = Tk()
    app = ScreenTranslatorApp(root)
    root.mainloop()
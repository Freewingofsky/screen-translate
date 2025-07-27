from tkinter import Tk, Canvas, Frame, Button
from PIL import ImageGrab
import pytesseract
from translator import Translator
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
        self.translator = Translator()

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.translate_button = Button(master, text="Translate", command=self.translate_area)
        self.translate_button.pack()

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

if __name__ == "__main__":
    root = Tk()
    app = ScreenTranslatorApp(root)
    root.mainloop()
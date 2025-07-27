import tkinter as tk
from PIL import ImageGrab
import pytesseract
import os
from dummy_translation_service import GoogleTranslationService
from translator import Translator

# Tesseract 設定
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

class SnippingTool:
    def __init__(self, on_finish_callback=None, mode="auto", target_lang="zh-TW"):
        self.on_finish_callback = on_finish_callback
        self.mode = mode
        self.target_lang = target_lang
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.configure(bg='black')
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.translator = Translator(GoogleTranslationService())
        self.results = []
    def on_close(self):
        # 關閉視窗時確保所有執行緒停止
        self.is_translating = False
        try:
            if hasattr(self, '_timer'):
                self._timer.cancel()
        except Exception:
            pass
        self.root.destroy()

    def on_button_press(self, event):
        self.start_x = self.canvas.winfo_pointerx()
        self.start_y = self.canvas.winfo_pointery()
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        cur_x = self.canvas.winfo_pointerx()
        cur_y = self.canvas.winfo_pointery()
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        self.end_x = self.canvas.winfo_pointerx()
        self.end_y = self.canvas.winfo_pointery()
        self.is_translating = True
        self.interval_ms = 1500  # 每1.5秒翻譯一次
        if self.mode == "auto" and self.is_translating:
            self.live_translate()
        self.root.destroy()
    def manual_translate(self):
        self.snip_and_translate()

    def live_translate(self):
        if not self.is_translating:
            return
        self.snip_and_translate()
        import threading
        self._timer = threading.Timer(self.interval_ms / 1000.0, self.live_translate)
        self._timer.start()

    def stop_translate(self):
        self.is_translating = False
        try:
            self._timer.cancel()
        except Exception:
            pass
        if self.on_finish_callback:
            self.on_finish_callback(self.results)

    def snip_and_translate(self):
        try:
            x1, y1, x2, y2 = self.start_x, self.start_y, self.end_x, self.end_y
            if x2 <= x1 or y2 <= y1:
                print("選取區域無效，請重新選取。")
                self.is_translating = False
                try:
                    self._timer.cancel()
                except Exception:
                    pass
                # 重新啟動選取流程
                if self.on_finish_callback:
                    self.on_finish_callback('RETRY_SNIP')
                return
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            text = pytesseract.image_to_string(img, lang='jpn')
            translation = self.translator.translation_service.translate(text, target_language=self.target_lang)
            self.results = [(text, translation)]  # 每次只保留最新一次結果
            # 自動模式下即時回傳結果
            if self.on_finish_callback:
                self.on_finish_callback(self.results)
        except Exception as e:
            print(f"擷取或翻譯失敗: {e}")


class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("螢幕翻譯工具")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # 模式選擇
        self.mode = tk.StringVar(value="auto")
        self.target_lang = tk.StringVar(value="zh-TW")
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=10)
        tk.Label(mode_frame, text="翻譯模式:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(mode_frame, text="自動", variable=self.mode, value="auto", command=self.update_mode, font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(mode_frame, text="手動", variable=self.mode, value="manual", command=self.update_mode, font=("Arial", 11)).pack(side=tk.LEFT, padx=5)

        lang_frame = tk.Frame(self.root)
        lang_frame.pack(pady=5)
        tk.Label(lang_frame, text="翻譯語言:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(lang_frame, text="繁體中文", variable=self.target_lang, value="zh-TW", font=("Arial", 11), command=self.on_lang_change).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(lang_frame, text="英文", variable=self.target_lang, value="en", font=("Arial", 11), command=self.on_lang_change).pack(side=tk.LEFT, padx=5)

        # 按鈕區
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        self.start_button = tk.Button(button_frame, text="開始選取區域", command=self.start_snip, font=("Arial", 12), width=18)
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.stop_button = tk.Button(button_frame, text="停止翻譯", command=self.stop_translate, state=tk.DISABLED, font=("Arial", 12), width=18)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        self.manual_button = tk.Button(button_frame, text="手動翻譯", command=self.manual_translate, state=tk.DISABLED, font=("Arial", 12), width=18)
        self.manual_button.pack(side=tk.LEFT, padx=10)

        # 結果顯示區
        self.snip_tool = None
        result_frame = tk.Frame(self.root)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        left_frame = tk.Frame(result_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_frame = tk.Frame(result_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(left_frame, text="原文", font=("Arial", 12)).pack(anchor=tk.W)
        self.text_widget_src = tk.Text(left_frame, wrap=tk.WORD, width=40, height=25, font=("Consolas", 11))
        self.text_widget_src.pack(fill=tk.BOTH, expand=True)

        tk.Label(right_frame, text="翻譯", font=("Arial", 12)).pack(anchor=tk.W)
        self.text_widget_trans = tk.Text(right_frame, wrap=tk.WORD, width=40, height=25, font=("Consolas", 11))
        self.text_widget_trans.pack(fill=tk.BOTH, expand=True)

    def on_lang_change(self):
        # 語言切換時自動停止翻譯並重製狀態
        if self.snip_tool and self.snip_tool.is_translating:
            self.snip_tool.stop_translate()
            self.stop_button.config(state=tk.DISABLED)
            self.start_button.config(state=tk.NORMAL)
        self.reset_snip_tool()
    def update_mode(self):
        mode = self.mode.get()
        # 如果原本是自動翻譯且有 snip_tool，需停止翻譯並重製按鈕
        if self.snip_tool and self.snip_tool.is_translating:
            self.snip_tool.stop_translate()
            self.stop_button.config(state=tk.DISABLED)
            self.start_button.config(state=tk.NORMAL)
        if mode == "auto":
            self.manual_button.config(state=tk.DISABLED)
        else:
            self.manual_button.config(state=tk.NORMAL)
        # 切換模式時重製選取框
        self.reset_snip_tool()

    def start_snip(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        mode = self.mode.get()
        target_lang = self.target_lang.get()
        self.snip_tool = SnippingTool(on_finish_callback=self.update_results, mode=mode, target_lang=target_lang)
        self.snip_tool.root.mainloop()
        self.update_mode()
    def manual_translate(self):
        if self.snip_tool:
            self.snip_tool.manual_translate()

    def stop_translate(self):
        if self.snip_tool:
            self.snip_tool.stop_translate()
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        # 停止翻譯時重製選取框
        self.reset_snip_tool()
    def reset_snip_tool(self):
        # 釋放選取工具，需重新選取
        self.snip_tool = None

    def update_results(self, results):
        if results == 'RETRY_SNIP':
            # 只在主動選取時顯示一次提示
            if self.mode.get() == "manual":
                import tkinter.messagebox as msg
                msg.showinfo("提示", "選取區域無效，請重新選取！")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.reset_snip_tool()
            return
        self.text_widget_src.config(state=tk.NORMAL)
        self.text_widget_src.delete(1.0, tk.END)
        self.text_widget_trans.config(state=tk.NORMAL)
        self.text_widget_trans.delete(1.0, tk.END)
        for src, trans in results:
            self.text_widget_src.insert(tk.END, f"{src.strip()}\n{'-'*40}\n")
            self.text_widget_trans.insert(tk.END, f"{trans.strip()}\n{'-'*40}\n")
        self.text_widget_src.config(state=tk.DISABLED)
        self.text_widget_trans.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = MainApp()
    app.root.mainloop()

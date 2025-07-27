from deep_translator import GoogleTranslator

class GoogleTranslationService:
    def __init__(self):
        pass

    def translate(self, text, target_language='en'):
        try:
            # deep-translator 會自動偵測語言
            result = GoogleTranslator(source='auto', target=target_language).translate(text)
            return result
        except Exception as e:
            print(f"翻譯失敗: {e}")
            return "[翻譯失敗]"

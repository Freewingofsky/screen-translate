class Translator:
    def __init__(self, translation_service):
        self.translation_service = translation_service

    def translate_text(self, text):
        # Here you would implement the logic to call the translation service
        # For example, using an API to translate the text
        translated_text = self.translation_service.translate(text, target_language='en')
        return translated_text
# Screen Translate App

# Screen Translate App


螢幕翻譯工具，使用者可選取螢幕區域，程式會即時擷取區域內的日文並翻譯為繁體中文或英文。支援自動/手動翻譯、語言切換、原文/翻譯分區顯示。


## 專案結構

```
screen-translate-app
├── src
│   ├── screen_translate.py      # 主程式，整合選取、翻譯、UI
│   ├── dummy_translation_service.py # Google翻譯服務包裝
│   ├── translator.py            # 翻譯服務包裝器
│   ├── screenshot.py            # 擷取螢幕區域（如有）
│   ├── utils.py                 # 影像處理/文字工具（如有）
│   └── main.py                  # 入口（如有）
├── requirements.txt             # 依賴套件
└── README.md                    # 專案說明
```


## 安裝與使用

1. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```

2. 執行主程式：
   ```bash
   python src/screen_translate.py
   ```

3. 依照畫面指示選取螢幕區域，程式會自動擷取並翻譯日文。


## 功能說明

- 螢幕區域選取：可自由框選螢幕區域
- 即時/手動翻譯：自動持續翻譯或手動觸發
- 語言切換：可選繁體中文或英文
- 原文/翻譯分區顯示
- 錯誤處理與資源釋放


## 貢獻

歡迎提出建議或回報問題。

## 授權

MIT License
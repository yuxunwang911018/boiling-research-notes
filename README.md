# 沸騰流場與神經網路研究筆記

以繁體中文介紹 CFD 資料與神經網路場重建，使用可重複的內容格式與 AGENTS.md，讓 AI 可以持續新增研究案例。
## 專案結構

```text
boiling-research-notes/
├── AGENTS.md                 # AI 協作、風格、研究表述與新增規則
├── content/
│   ├── pages/                # 首頁與方法文案
│   └── cases/                # T50、T65 的結構化內容
├── templates/                # 共用 HTML 模板
├── assets/
│   ├── images/               # 5 張選定的研究靜態圖
│   └── animations/           # 4 份選定的研究動畫
├── styles/main.css
├── scripts/main.js
├── tools/                    # 建置及檢查工具，Python 3 標準函式庫
├── docs/                     # 內容格式、素材來源、擴充與驗證紀錄
├── dist/                     # 產生的五頁網站；不要直接編輯
└── review-materials/          # 先前候選副本，不追蹤、不放入網站成品
```

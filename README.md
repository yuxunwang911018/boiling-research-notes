# 沸騰流場與神經網路研究筆記

以繁體中文介紹 CFD 資料與神經網路場重建，使用可重複的內容格式與 AGENTS.md，讓 AI 可以持續新增研究案例。

## 目前成果

2026-11-11：完成作業流程第 3–7 步。網站已有首頁、研究方法、T50 案例、T65 案例與協作規則共五頁；兩個案例共用同一模板，包含六個固定段落、比較表、可切換及停止的動畫、來源與限制。新增 T65 時只增加案例內容檔，首頁與導覽自動產生。

2026-11-16：使用者已確認將本專案原始檔、規則文件、選定圖像及研究數值上傳至指定的公開儲存庫。網站尚未發布，GitHub Pages 設定與作業繳交由使用者接續完成。

原始碼儲存庫：[yuxunwang911018/boiling-research-notes](https://github.com/yuxunwang911018/boiling-research-notes)。

`dist/` 是由原始檔產生的網站成品，依 .gitignore 不上傳；後續部署時先執行下方建置指令，再發布 `dist/`。

## 如何瀏覽

可直接用瀏覽器開啟 `dist/index.html`。此網站不需要後端、帳號、外部字型或網路套件；相對路徑設計也適用 GitHub Pages 的儲存庫子路徑。

重新產生與檢查：

```sh
python3 tools/build_site.py
python3 tools/check_site.py
```

需要本機 HTTP 預覽時：

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```

然後以瀏覽器開啟 `http://127.0.0.1:8765/`。本機服務只作預覽，不會公開至網際網路。

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

## 新增內容

先讀 `AGENTS.md` 與 `docs/content-format.md`。依現有案例建立新的 `content/cases/<slug>.json`，放入素材並記錄來源，重新產生網站即可更新首頁、導覽與案例頁，不需要複製 HTML。T65 的實際擴充紀錄在 `docs/extension-log.md`。

## 資料來源與驗證

研究來源為本機 `case` 專案；其原始資料與研究程式未修改。此網站只整理文字與複製九份圖像；未帶入 CSV、NPZ、模型權重、PDF 或 PPT。四份 GIF 完整解碼，共 50 幀，保留原色階、比例及播放設定。

內容範圍見 `docs/content-scope.md`；圖像來源與 SHA-256 見 `docs/asset-manifest.json`；表格與原報告數值核對見 `docs/source-verification.json`；完整網站檢查見 `docs/verification.md`。

目前研究結果限同工況時間內插，不宣稱完整 PINN、未來預測、新工況泛化或模型全面優於時間插值。

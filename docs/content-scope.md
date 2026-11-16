# 內容與公開範圍

更新日期：2026-11-16。網站名稱為「沸騰流場與神經網路研究筆記」。

## 本次完成範圍

依使用者指示完成至第七步：建立 AGENTS.md、共同內容格式、第一版網站、新增 T65 驗證擴充方式，以及檢查網站與研究敘述。2026-11-16 使用者另行授權將此專案上傳至既有公開儲存庫 wyhen14/boiling-research-notes；本次不啟用網站發布。

## 網站內容

| 頁面 | 內容來源 | 現況 |
| --- | --- | --- |
| 首頁 | `content/pages/home.json` | 研究問題、場重建說明與自動產生的案例清單 |
| 研究方法 | `content/pages/methods.json` | 六個研究步驟、術語展開與研究範圍 |
| T50 案例 | `content/cases/t50.json` | V11 方法、完整 validation 指標、T50 比較動畫、限制與來源 |
| T65 案例 | `content/cases/t65.json` | v1 獨立重現、完整 validation 指標、比較動畫、限制與來源 |
| 協作規則 | `templates/rules.html`、`AGENTS.md` | 內容規則說明、規則文件及案例格式下載 |

讀者以對 CFD 與 AI 感興趣的同學為主。文章使用「研究問題、資料條件、方法、結果、限制、圖表與文字來源」六段結構。

## 素材

網站本機預覽使用九份未修改的研究圖像：T50 三張靜態圖、兩份動畫；T65 兩張靜態圖、兩份動畫。原路徑、檔案大小、SHA-256、尺寸、幀數與播放時間記錄於 `asset-manifest.json`，狀態均為 `repository_upload_authorized`。

T50 動畫為 CFD／V10／V11，T65 動畫為 CFD／MLP／時間線性插值。兩者對照組不同，圖說分別交代，不作同一對照組的跨工況比較。動畫僅由已有 validation 快照組成，不增加中間影格；靜態海報時間與動畫時間範圍均有標記。

## 研究結果與來源

主要來源文件（相對原研究 `case` 根目錄）：

- `README.md`、`SESSION.md`：研究範圍與進度。
- `docs/DATA_CONTRACT.md`：資料核對、座標對齊與切分。
- `docs/T50_RECONSTRUCTION_PLAN.md`、`docs/T50_V11_PLAN.md`：研究流程及 V11 方法。
- `outputs/T50-MLP-v11-interface05-30000/REPORT.md`：T50 結果與限制。
- `outputs/T50-visual-comparison-v1/animation_report.json`：T50 比較動畫。
- `docs/T65_RECONSTRUCTION_PLAN.md`、`outputs/T65-MLP-v1-independent-30000/REPORT.md`：T65 設計、結果與限制。
- `docs/RECONSTRUCTION_STAGE_ACCEPTANCE.md`：人工階段接受，與原自動門檻分開記錄。

T50 與 T65 各六項指標均呈現模型及時間插值數值，保留基準表現較好的項目；來源核對見 `source-verification.json`。界面距離由 m 換為 mm，表格顯示至小數第六位。未重新訓練或重算模型評分。

敘述限定為監督式同工況時間內插，不宣稱完整 PINN、未來預測、新工況泛化、物理守恆或模型全面勝出。不把目前案例等同計畫 PDF 的微流管案例；底部 cell center 不當作物理壁面，氣相連通區不直接當作物理氣泡數。目前 CAS／DAT 缺少，未宣稱重新完成原生驗證。

## 公開狀態

本網站已包含兩個案例的工況標記、實際數值及選定圖像。使用者在檢查檔案、瀏覽網站並收到公開 Repository 操作說明後，於 2026-11-16 指定 wyhen14/boiling-research-notes 並要求代為上傳；本次授權涵蓋上述現有網站內容、原始檔與文件。GitHub Pages 發布及作業繳交仍由使用者接續。未匯入原始 CSV、CAS／DAT、NPZ、模型權重、PDF、PPT、完整研究程式或整個實驗目錄。

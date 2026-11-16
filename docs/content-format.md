# 案例內容格式

每篇案例以 UTF-8 JSON 儲存於 `content/cases/<slug>.json`。以 `t50.json` 為實際範本；不要複製或編輯 `dist/` 內 HTML。

| 欄位 | 格式與意義 |
| --- | --- |
| `slug` | 小寫英文、數字、連字號；與檔名一致，產生 `<slug>.html` |
| `order` | 正整數，決定導覽與首頁顯示順序 |
| `label`、`title`、`summary` | 案例短名、標題與摘要 |
| `version`、`updated` | 研究版本與內容更新日期 |
| `question` | 本案例的研究問題 |
| `conditions` | `{label, value}` 陣列，記錄範圍、網格、切分等 |
| `methods` | 方法步驟字串陣列 |
| `metrics` | `{label, model, baseline, unit, aggregation}` 陣列，數字為 JSON number；目前基準為時間插值 |
| `interpretation` | 對指標的解讀，不把不同指標合成單一成功敘述 |
| `acceptance` | `{automatic, stage}`，區分自動檢查與人工階段接受 |
| `limitations` | 限制字串陣列 |
| `media` | `{label, poster, animation, alt, caption, source_id}` 陣列；路徑相對網站根目錄，海報與動畫分開 |
| `sources` | `{id, title, path}` 陣列；原研究檔案相對 `case` 的路徑，來源只顯示文字，不做失效的站外連結 |

必備六段依序為「研究問題、資料條件、方法、結果、限制、圖表與文字來源」，由共用模板產生。指標表統一顯示模型與時間插值，欄位寫清楚單位及彙整方式。

`content/pages/home.json` 管理首頁文案，`content/pages/methods.json` 管理研究方法與術語。所有案例均自動進入首頁與導覽。

素材清單 `docs/asset-manifest.json` 每筆紀錄至少含 `id`、`source_relative_to_case`、`local_path`、`sha256`、`publication_status`。動畫另記幀數與每輪播放長度；這是播放設定，不等於物理時間。公開狀態目前為 `local_preview_only`。

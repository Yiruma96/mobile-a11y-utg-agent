# 本地样本存放目录（`samples/`，与 418 份报告及动态 UTG 一一对应）

本目录用于在**本地研究环境**按与 `results/per_app_reports/` 完全一致的文件名存放全部 418 款 APKAudit 审计样本：

- `samples/malicious/<report_stem>.apk`（348 个，覆盖 82/82 恶意家族）
- `samples/benign/<report_stem>.apk`（70 个，覆盖 11/11 良性品类）

完整的一一对应映射关系（`report_stem` ↔ `app_id` ↔ `SHA-256` ↔ 静态报告 ↔ 本地 APK ↔ 动态 UTG 目录）见：
[`../results/per_app_reports/REPORT_APK_UTG_MANIFEST.csv`](../results/per_app_reports/REPORT_APK_UTG_MANIFEST.csv)。

> **仓库安全说明**：`.gitignore` 已严格屏蔽 `samples/**/*.apk` 与 `*.apk` 二进制文件，执行 `git push` 时**绝不会上传任何恶意 APK 样本**至公开 GitHub 仓库；外部研究者可依据 `dataset_provenance_1769.csv` 中的公开 SHA-256 从 MalwareBazaar / MalRadar / F-Droid 自行下载复现并放入本目录。

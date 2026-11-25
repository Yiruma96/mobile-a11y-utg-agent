# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:36:32
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.riverfront8`（静态标签：`malicious` / `Octo` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `3` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.riverfront8/com.riverfront8.p084k` | hooks=`[]` | overlays=`0` | texts=`Chrome / MH1LDiZuzhiYqAAAAAElFTkSuQmCC / Accessibility Service / DOWNLOADED SERVICES / Switch Access`
- **Back 后 +5.5s**：`com.riverfront8/com.riverfront8.p084k` | hooks=`[]` | overlays=`0` | texts=`Chrome / MH1LDiZuzhiYqAAAAAElFTkSuQmCC / Accessibility Service / DOWNLOADED SERVICES / Switch Access`
- **Back 后 +10.5s**：`com.riverfront8/com.riverfront8.p084k` | hooks=`[]` | overlays=`0` | texts=`Chrome / MH1LDiZuzhiYqAAAAAElFTkSuQmCC / Accessibility Service / DOWNLOADED SERVICES / Switch Access`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.riverfront8` / `p084k` | `-` | 13 | 118 / 否 | `click` → [13] Button text="Open Settings" id=t_openSettings (cli | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.riverfront8/p084k`)**: `Chrome` | `MH1LDiZuzhiYqAAAAAElFTkSuQmCC` | `Accessibility Service` | `DOWNLOADED SERVICES` | `Switch Access` | `OFF` | `TalkBack` | `svg%3E` | `Open Settings`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Chrome` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先以“Accessibility Service/Open Settings”引导用户开启无障碍，并持续弹出“Enable service/Chrome”通知；进入系统无障碍列表与服务详情后展示“保护设备”话术，拒权返回仍被困在诱导页，未出现正常退出路径。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> “Accessibility Service”：无障碍服务（应用引导页 step_01）
- English -> “Open Settings”：打开设置（应用引导页 step_01）
- English -> “Enable service”/“Chrome”：启用服务/Chrome（通知横幅，贯穿多页）
- English -> “DOWNLOADED SERVICES”：已下载服务（应用引导页 step_01）
- English -> “Enable this service to protect your device.”：启用此服务以保护你的设备（服务详情页 detail_1）
- English -> “Use Chrome”：使用 Chrome（服务详情页 detail_1）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: p084k** | 应用内无障碍引导页，英文“Open Settings”即打开设置；点击后跳系统设置，通知横幅“启用服务/Chrome”常驻，遮罩0。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | [无障碍列表页] 系统无障碍设置，列出DOWNLOADED APPS中Chrome为Off；本步命中HOOK_A11Y_SETTINGS并自动终止，通知横幅仍在，遮罩0。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍在系统无障碍设置页，界面文本为空；通知横幅“启用服务/Chrome”仍在，遮罩0，无新弹窗。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍停留系统无障碍设置页，无新界面文本；通知横幅持续，遮罩0，未见系统警告或浮层。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页，英文“Use Chrome/Chrome shortcut”等选项，并称“启用此服务以保护设备”；本步仅检查详情与警告，通知横幅在，遮罩0。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 标题为系统警告弹窗(点Deny)，实际快照回应用p084k同一引导页，“Open Settings”仍诱导；本步检查未见浮层，遮罩0，通知横幅暂缺。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回后2.0秒仍困在应用引导页，仍显示“Open Settings”与无障碍说明；通知横幅恢复，遮罩0，结果TRAPPED_ON_LURE_SCREEN。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权返回后10.5秒仍无退出路径，停留同一诱导页，“Open Settings”继续引导开启无障碍；通知横幅常驻，遮罩0，仍TRAPPED_ON_LURE_SCREEN。 | `step_02_refusal_10500ms_screen.png` |

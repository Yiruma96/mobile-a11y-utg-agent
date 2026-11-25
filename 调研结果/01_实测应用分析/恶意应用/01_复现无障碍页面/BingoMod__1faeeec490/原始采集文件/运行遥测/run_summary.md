# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:09:36
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`p50f9cd20.pe806e63b.pe1a3069b`（静态标签：`malicious` / `BingoMod` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`p50f9cd20.pe806e63b.pe1a3069b/p50f9cd20.pe806e63b.pe1a3069b.peb3e8c60` | hooks=`[]` | overlays=`0` | texts=`AnroidRAA / Image 2 / Per abilitare correttamente l'app è necessario consentire tutti i permessi. Clicca sul pulsante "Prosegui" in basso per continuare. / Prosegui`
- **Back 后 +5.5s**：`p50f9cd20.pe806e63b.pe1a3069b/p50f9cd20.pe806e63b.pe1a3069b.peb3e8c60` | hooks=`[]` | overlays=`0` | texts=`AnroidRAA / Image 2 / Per abilitare correttamente l'app è necessario consentire tutti i permessi. Clicca sul pulsante "Prosegui" in basso per continuare. / Prosegui`
- **Back 后 +10.5s**：`p50f9cd20.pe806e63b.pe1a3069b/p50f9cd20.pe806e63b.pe1a3069b.peb3e8c60` | hooks=`[]` | overlays=`0` | texts=`AnroidRAA / Image 2 / Per abilitare correttamente l'app è necessario consentire tutti i permessi. Clicca sul pulsante "Prosegui" in basso per continuare. / Prosegui`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `p50f9cd20.pe806e63b.pe1a3069b` / `peb3e8c60` | `-` | 1 | 0 / 是 | `click` → [540, 1697] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `p50f9cd20.pe806e63b.pe1a3069b` / `peb3e8c60` | `-` | 4 | 155 / 否 | `click` → [4] Button text="Prosegui" (click) center=(540,2018) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 220 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`p50f9cd20.pe806e63b.pe1a3069b/peb3e8c60`)**: (空文本)
- **Step 2 (`p50f9cd20.pe806e63b.pe1a3069b/peb3e8c60`)**: `AnroidRAA` | `Image 2` | `Per abilitare correttamente l'app è necessario consenti` | `Prosegui`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Sicurezza Dispositivo` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：入口WebView以意大利语“必须授予全部权限”诱导点击Prosegui，跳转系统无障碍设置开启“Sicurezza Dispositivo”，触发全控权限警告；拒权后仍被弹回同一诱导页，形成TRAPPED_ON_LURE_SCREEN。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 意大利语 -> “要正确启用本应用，必须允许全部权限；请点击下方‘Prosegui’按钮继续。”（step_02及拒权返回页）
- 英语系统警告 -> “允许Sicurezza Dispositivo完全控制您的设备？可查看并控制屏幕、读取屏幕全部内容并叠加显示、跟踪交互并代您操作应用。”（detail_2系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: peb3e8c60** | 入口WebView空白页，仅见可点击区域；按坐标点按“Prosegui”继续，尚无可见文本、通知或遮罩，属于引导前置页。 | `step_01_action.png` |
| 2 | **Step 2: peb3e8c60** | WebView诱导页显示“AnroidRAA/Image 2”，意大利语称必须允许全部权限并点下方“Prosegui”；本步点击该按钮，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 跳转系统无障碍设置，已下载应用“Sicurezza Dispositivo”呈Off；探针捕获A11Y设置Hook后自动终止，无通知/遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒停留无障碍设置页，界面文本未采到；等待探针显示遮罩数为0，无通知横幅，未见额外弹窗。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒仍在无障碍设置页等待，未出现新文本；遮罩计数为0，无通知或浮层，说明未发生二次覆盖诱导。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 进入“Sicurezza Dispositivo”服务详情，显示Use开关Off、Shortcut settings及“No description provided.”；本步仅查看详情，无通知/遮罩。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统警告弹窗询问是否允许“Sicurezza Dispositivo”完全控制设备，列明读屏、叠加与代操作；含Allow/Deny，本步仅查看，无遮罩。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 点Deny拒权后2秒被弹回同一WebView诱导页，仍要求点“Prosegui”授予全部权限；无通知/遮罩，状态为TRAPPED_ON_LURE_SCREEN。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权后10.5秒仍停留在同一诱导页，反复要求“Prosegui”授权；无通知/遮罩，确认被锁在TRAPPED_ON_LURE_SCREEN。 | `step_03_refusal_10500ms_screen.png` |

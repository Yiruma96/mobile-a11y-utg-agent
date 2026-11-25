# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:40:59
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`io.github.jqssun.displayextend`（静态标签：`benign` / `显示调节、截屏与分屏效率` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`io.github.jqssun.displayextend/io.github.jqssun.displayextend.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Overview / Missing permissions / Certain features will not work / Permissions / Shizuku`
- **Back 后 +5.5s**：`io.github.jqssun.displayextend/io.github.jqssun.displayextend.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Overview / Missing permissions / Certain features will not work / Permissions / Shizuku`
- **Back 后 +10.5s**：`io.github.jqssun.displayextend/io.github.jqssun.displayextend.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Overview / Missing permissions / Certain features will not work / Permissions / Shizuku`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `io.github.jqssun.displayextend` / `MainActivity` | `-` | 24 | 399 / 否 | `click` → [9] Button text="Enable" id=accessibility_permission_bt | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `io.github.jqssun.displayextend` / `AccessibilityConsentActivity` | `-` | 4 | 448 / 否 | `click` → [4] Button text="Enable" id=button1 (click) center=(827 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`io.github.jqssun.displayextend/MainActivity`)**: `Overview` | `Missing permissions` | `Certain features will not work` | `Permissions` | `Shizuku` | `Not started` | `Accessibility` | `Optional; only needed for popup and system surfaces on ` | `Enable` | `Displays`
- **Step 2 (`io.github.jqssun.displayextend/AccessibilityConsentActivity`)**: `Enable accessibility access` | `Extend uses the Accessibility Service to operate your e` | `Not now` | `Enable`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Extend` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用从主界面以“缺少权限/部分功能不可用”提示引导点击无障碍Enable，经应用内同意页跳转系统无障碍列表与Extend详情，最终弹出系统完全控制警告；拒权后回到主界面仍停留在权限引导页，呈现TRAPPED_ON_LURE_SCREEN，通知与遮罩均为0。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “缺少权限/部分功能将无法使用”（主界面Step 1）
- 英文 -> “可选；仅外接显示器的弹窗与系统界面需要”（主界面无障碍说明）
- 英文 -> “启用无障碍访问……是否启用无障碍服务？”（应用内同意页Step 2）
- 英文 -> “暂不/启用”（应用内同意页按钮）
- 英文 -> “使用Extend/Extend快捷方式关闭/用于模拟副屏触摸事件的无障碍服务”（系统服务详情页）
- 英文 -> “允许Extend完全控制你的设备？可查看并控制屏幕、查看并代为执行操作”（系统警告弹窗）
- 英文 -> “允许/拒绝”（系统警告弹窗按钮）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面概览：提示缺少权限、部分功能不可用，无障碍显示未启动；点击无障碍Enable，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: AccessibilityConsentActivi** | 应用内无障碍同意页：英文说明仅本机使用、不收集共享，询问是否启用；点击Enable进入系统设置，未直接开权限。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表：下载应用下Extend显示Off；探针捕获设置钩子后自动终止，页面无通知与遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留系统无障碍列表，UI文本为空，遮罩数0，无通知横幅。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍在系统无障碍列表，文本为空，遮罩数0，无通知，未见弹窗。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 系统Extend服务详情：显示Use Extend、快捷方式Off及模拟副屏触摸说明；仅查看详情未授权，无遮罩。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统警告弹窗：英文称允许Extend完全控制设备，可查看屏幕并代操作；有Allow/Deny，本步检查警告，遮罩0。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权后2秒回到主界面：仍显示缺少权限、无障碍Enable；未退出或跳转，状态为TRAPPED_ON_LURE_SCREEN，无通知/遮罩。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权后10.5秒仍困在主界面权限引导页，无障碍Enable持续存在，未放行；无通知/遮罩，判为TRAPPED_ON_LURE_SCREEN。 | `step_03_refusal_10500ms_screen.png` |

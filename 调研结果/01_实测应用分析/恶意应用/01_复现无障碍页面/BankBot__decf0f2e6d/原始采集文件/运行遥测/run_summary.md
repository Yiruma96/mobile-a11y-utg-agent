# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:20:00
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.starryheaded.defrauds`（静态标签：`malicious` / `BankBot` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `3` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.starryheaded.defrauds/com.starryheaded.defrauds.craniate` | hooks=`[]` | overlays=`0` | texts=`e / Müzik indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz. / İzin Ver`
- **Back 后 +5.5s**：`com.starryheaded.defrauds/com.starryheaded.defrauds.craniate` | hooks=`[]` | overlays=`0` | texts=`e / Müzik indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz. / İzin Ver`
- **Back 后 +10.5s**：`com.starryheaded.defrauds/com.starryheaded.defrauds.craniate` | hooks=`[]` | overlays=`0` | texts=`e / Müzik indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz. / İzin Ver`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.starryheaded.defrauds` / `craniate` | `-` | 4 | 88 / 否 | `click` → [3] FrameLayout id=button (click) center=(540,2024) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 208 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.starryheaded.defrauds/craniate`)**: `e` | `Müzik indirme işleminin aktif olabilmesi için yukarıda ` | `İzin Ver`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `M​ü​z​i​k` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先以土耳其语音乐下载为幌子，诱导点击“İzin Ver”跳转系统无障碍设置并授予 Müzik 服务；通知横幅反复催促授权。若拒绝或返回，则反复落回同一诱导页（TRAPPED_ON_LURE_SCREEN），无正常退出路径。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语 -> “为使音乐下载功能生效，请授予上方显示的权限”（入口诱导页）
- 土耳其语 -> “允许”（入口诱导页授权按钮“İzin Ver”）
- 土耳其语 -> “为能下载音乐，请授予无障碍权限”（通知横幅，原文含占位符 String）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: craniate** | 土耳其语音乐下载诱导页：称须授予上方权限才能启用下载；点击“İzin Ver(允许)”后跳系统无障碍设置，通知横幅同步催促授权。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 跳转至系统无障碍列表：下载应用显示为“Müzik”，状态“Off(关闭)”；此为授权关键入口，探针因捕获无障碍设置钩子而终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍停留在无障碍设置页，无遮罩；仅见恶意包占位通知，页面文本暂空，未完成授权。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒探针：仍在无障碍设置页且无遮罩；通知横幅恢复为土耳其语“为下载音乐请授予无障碍权限”，持续施压。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 无障碍服务详情页：显示“Müzik”“Use Müzik(使用)”及快捷键选项；无描述，通知横幅仍催促授权，用于核验服务角色。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统警告弹窗场景：仍见服务详情与“Use Müzik”“Off”等控件，遮罩数为0；记录点Deny/拒绝时的系统提示与页面状态。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回2.0秒：回到土耳其语音乐下载诱导页，仍显示授权说明与“İzin Ver”；无取消出口，状态为困在诱导页。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权返回10.5秒：页面仍停在同一诱导页，授权说明和“İzin Ver”按钮未消失；确认拒绝后无法绕过，持续困在诱导页。 | `step_02_refusal_10500ms_screen.png` |

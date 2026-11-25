# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:55:04
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.quadrigeminate.hydrocatalysis`（静态标签：`malicious` / `BankBot` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.quadrigeminate.hydrocatalysis/com.quadrigeminate.hydrocatalysis.directorial` | hooks=`[]` | overlays=`0` | texts=`e / Müzik indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz. / İzin Ver`
- **Back 后 +5.5s**：`com.quadrigeminate.hydrocatalysis/com.quadrigeminate.hydrocatalysis.directorial` | hooks=`[]` | overlays=`0` | texts=`e / Müzik indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz. / İzin Ver`
- **Back 后 +10.5s**：`com.quadrigeminate.hydrocatalysis/com.quadrigeminate.hydrocatalysis.directorial` | hooks=`[]` | overlays=`0` | texts=`e / Müzik indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz. / İzin Ver`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.quadrigeminate.hydrocatalysis` / `directorial` | `-` | 4 | 88 / 否 | `click` → [3] FrameLayout id=button (click) center=(540,2024) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 208 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.quadrigeminate.hydrocatalysis/directorial`)**: `e` | `Müzik indirme işleminin aktif olabilmesi için yukarıda ` | `İzin Ver`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `M​ü​z​i​k` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以“音乐下载需授权”为名，从土耳其语诱导页跳转系统无障碍设置，并通过通知反复催促开启“Müzik”无障碍服务；用户拒绝高风险“完全控制设备”授权后仍被退回同一诱导页，无法绕过。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语 -> “为使音乐下载功能启用，请授予上方所示权限。”（step_01/拒权返回页）
- 土耳其语 -> “允许/授予权限”（step_01/拒权返回页按钮）
- 土耳其语通知 -> “音乐：请授予无障碍权限以便下载音乐。”（step_01通知横幅）
- 土耳其语通知 -> “请授予无障碍权限以便下载音乐。”（post_jump_0.8s通知横幅）
- 英语系统警告 -> “允许 Müzik 完全控制设备吗？可查看并控制屏幕、读取屏幕内容、跟踪交互并代你操作应用。”（detail_2系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: directorial** | 土耳其语诱导页称音乐下载需授权，按钮意为“允许”；点击后跳转无障碍设置，通知横幅同步催促开启无障碍。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍设置列表，已下载应用“Müzik”显示关闭；通知横幅仍要求为下载音乐授予无障碍。探针在此捕获设置钩子后自动终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒仍停留在无障碍列表，界面无文字；音乐通知横幅继续显示“下载音乐需授予无障碍”，等待探针未见遮罩。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒无障碍列表仍无界面文字，通知已变为空；等待探针显示遮罩数为0，未出现进一步诱导弹窗。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | “Müzik”无障碍服务详情页，含“Use Müzik”、快捷键关闭及“未提供描述”；仅检查详情，未开启服务。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统高风险授权警告：询问是否允许“Müzik”完全控制设备，列明可读屏、代操作等；检查后点击“Deny”拒绝。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝后2秒被退回同一土耳其语诱导页，仍称音乐下载需授权并提供“允许”按钮；通知横幅仍在，流程被卡在诱导页。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒绝后10.5秒仍停在原诱导页，文案和“允许”按钮不变；通知已空，未见退出或替代路径，持续困在诱导屏。 | `step_02_refusal_10500ms_screen.png` |

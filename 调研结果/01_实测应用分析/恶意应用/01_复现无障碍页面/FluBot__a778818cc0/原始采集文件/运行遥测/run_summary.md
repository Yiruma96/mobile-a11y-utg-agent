# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:18:01
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.sina.weibo`（静态标签：`malicious` / `FluBot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.sina.weibo/com.sina.weibo.p9c215b6d` | hooks=`[]` | overlays=`0` | texts=`Action Required / To install you must turn on the accessibility service for "Voicemail".

Click "OK" to go to the settings and then scroll until you find "Voicemail" and click to turn on the accessibility service. 

If you do not find it click on "Downloaded / Installed services" and then click on "Voicemail". / OK`
- **Back 后 +5.5s**：`com.sina.weibo/com.sina.weibo.p9c215b6d` | hooks=`[]` | overlays=`0` | texts=`Action Required / To install you must turn on the accessibility service for "Voicemail".

Click "OK" to go to the settings and then scroll until you find "Voicemail" and click to turn on the accessibility service. 

If you do not find it click on "Downloaded / Installed services" and then click on "Voicemail". / OK`
- **Back 后 +10.5s**：`com.sina.weibo/com.sina.weibo.p9c215b6d` | hooks=`[]` | overlays=`0` | texts=`Action Required / To install you must turn on the accessibility service for "Voicemail".

Click "OK" to go to the settings and then scroll until you find "Voicemail" and click to turn on the accessibility service. 

If you do not find it click on "Downloaded / Installed services" and then click on "Voicemail". / OK`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.sina.weibo` / `p9c215b6d` | `-` | 3 | 310 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,145 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 208 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.sina.weibo/p9c215b6d`)**: `Action Required` | `To install you must turn on the accessibility service f` | `OK`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Voicemail` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以 com.sina.weibo 包名承载 p9c215b6d 页面，先用英文“Action Required”诱导用户为“Voicemail”开启无障碍服务并跳转系统设置；用户拒绝授权后，应用反复重新拉起同一诱导弹窗，并伴随“Action Required”通知横幅。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “必须为 Voicemail 开启无障碍服务才能安装；点 OK 去设置，滚动找到 Voicemail 并开启；找不到就点 Downloaded / Installed services 再点 Voicemail”（入口诱导页及拒权后重复页）
- 英文 -> “允许 Voicemail 完全控制你的设备？可查看并控制屏幕、读取屏幕内容、查看并执行操作等；Allow / Deny”（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: p9c215b6d** | 英文诱导页“Action Required”，要求为“Voicemail”开启无障碍服务才能安装；点击OK跳系统设置，有空白通知，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表页，DOWNLOADED APPS下“Voicemail”为Off；采集到无障碍设置钩子与探针后自动终止，有空白通知，无遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停留在无障碍列表页；无界面文本采集，通知栏有微博包空白通知，遮罩数为0。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒探针，页面仍为无障碍列表页；无界面文本采集，通知栏有微博包空白通知，遮罩数为0。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | Voicemail服务详情页，含“Use Voicemail”、音量键快捷键等选项；本步仅检查详情/警告未授权，有空白通知，无遮罩。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统高危警告弹窗：询问是否允许Voicemail完全控制设备，并列读屏、查看/执行操作等能力；含Allow/Deny，本步按Deny拒绝，无遮罩。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝授权返回后2秒，应用重新弹出同一英文“Action Required”诱导页；通知横幅显示String (Action Required)，无遮罩，OK仍可再拉起设置。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒绝授权返回后10.5秒，仍被重新拉起同一“Action Required”诱导页；通知横幅显示String (Action Required)，无遮罩，形成循环催权。 | `step_02_refusal_10500ms_screen.png` |

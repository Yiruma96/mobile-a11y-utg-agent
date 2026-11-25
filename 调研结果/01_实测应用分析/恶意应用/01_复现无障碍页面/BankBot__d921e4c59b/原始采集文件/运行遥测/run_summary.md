# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:48:27
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.tumuluses.gastrocnemius`（静态标签：`malicious` / `BankBot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.tumuluses.gastrocnemius/com.tumuluses.gastrocnemius.precordial` | hooks=`[]` | overlays=`0` | texts=`e / Please grant the permission shown above for the application to run. / ALLOW`
- **Back 后 +5.5s**：`com.tumuluses.gastrocnemius/com.tumuluses.gastrocnemius.precordial` | hooks=`[]` | overlays=`0` | texts=`e / Please grant the permission shown above for the application to run. / ALLOW`
- **Back 后 +10.5s**：`com.tumuluses.gastrocnemius/com.tumuluses.gastrocnemius.precordial` | hooks=`[]` | overlays=`0` | texts=`e / Please grant the permission shown above for the application to run. / ALLOW`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.tumuluses.gastrocnemius` / `precordial` | `-` | 3 | 73 / 否 | `click` → [3] Button text="ALLOW" id=button (click) center=(540,2 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 215 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.tumuluses.gastrocnemius/precordial`)**: `e` | `Please grant the permission shown above for the applica` | `ALLOW`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Music Downloader` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用冒充“音乐下载器”，先在自有页以“请授予上方权限”诱导点ALLOW，再跳系统无障碍列表/详情与完全控制警告；拒权后仍自动重弹同一诱导页（RELAUNCHED_LURE_DIALOG），持续施压获取无障碍权限。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Please grant the permission shown above for the application to run. -> “请授予上方所示权限，应用才能运行”（precordial权限诱导页，拒权后重复出现）
- ALLOW -> “允许”（诱导页唯一主按钮）
- Please grant accessibility permission to use the application. -> “请授予无障碍权限以使用该应用”（Music Downloader通知横幅，多次催授）
- Music Downloader -> “音乐下载器”（伪装应用名，用于降低戒心）
- Play Store -> “应用商店”（伪装商店通知标题，正文为空）
- Use Music Downloader -> “使用音乐下载器”（无障碍服务详情页开关/入口）
- No description provided. -> “未提供描述”（无障碍服务详情页，弱化风险说明）
- Allow Music Downloader to have full control of your device? -> “允许音乐下载器完全控制您的设备？”（系统无障碍警告）
- Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> “完全控制仅适合辅助无障碍需求的应用，不适用于多数应用”（系统警告说明）
- View and control screen -> “查看并控制屏幕”（系统警告权限说明）
- It can read all content on the screen and display content over other apps. -> “可读取屏幕全部内容并叠加显示在其他应用上”（系统警告说明）
- View and perform actions -> “查看并执行操作”（系统警告权限说明）
- It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf. -> “可跟踪与应用的交互或硬件传感器，并代表您操作应用”（系统警告说明）
- Allow -> “允许”（系统警告高危授权按钮）
- Deny -> “拒绝”（系统警告拒绝按钮，被测用于观察拒权后行为）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: precordial** | 自有权限诱导页：英文提示“请授予上方权限”，仅有ALLOW按钮；点击后，通知栏以Music Downloader横幅催授无障碍。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表页：DOWNLOADED APPS下Music Downloader为Off；探针在此捕获无障碍设置Hook，自动终止并记录探针。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后0.8秒探针：无障碍设置页UI为空，无遮罩；通知仍保留Music Downloader催授无障碍与Play Store空正文通知。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒探针：仍无UI与遮罩；无障碍催权通知消失，仅剩Play Store空通知及系统备份提醒，未见新动作。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 无障碍服务详情页：显示Music Downloader、Use Music Downloader与快捷方式Off，并称No description provided；本步仅检查详情，未授权。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统完全控制警告弹窗：详列查看/控制屏幕、读取屏幕内容并叠加、跟踪交互代操作；有Allow与Deny，本步仅检查未点选。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 点Deny拒权后2秒返回自有页：再次显示“请授予上方权限”和ALLOW，判定RELAUNCHED_LURE_DIALOG，并继续推送Music Downloader催权通知。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权后10.5秒仍停留自有诱导页：同一英文提示与ALLOW保留，页面被重复拉起为RELAUNCHED_LURE_DIALOG；Music Downloader通知已消失。 | `step_02_refusal_10500ms_screen.png` |

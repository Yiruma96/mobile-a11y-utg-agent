# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:17:48
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.github.cvzi.screenshottile`（静态标签：`benign` / `显示调节、截屏与分屏效率` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.github.cvzi.screenshottile/com.github.cvzi.screenshottile.activities.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Screenshot Tile / More Settings / Before you can use this app, you need to add the tile/button to the quick settings. If you don't know how to do this, take a look at the Tutorial.

This app supports two different methods to take screenshots: / Legacy Method / The legacy method to take screenshots uses the screen recording features of Android.
When you take a screenshot, no sound is played. A silent notification is shown to open, share or edit the screenshot. The notification can be disabled in the app settings.
Before you can take a screenshot you need to add the tile to the quick settings, accept the permission to record the screen and the permission to access the internal storage to save the image file.
See the tutorial on how to do it.

On some phones this method does not work, especially on newer Androids (9.0+) it is unstable and it may ask for permission on every single screenshot. If that happens you should use the native method below.`
- **Back 后 +5.5s**：`com.github.cvzi.screenshottile/com.github.cvzi.screenshottile.activities.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Screenshot Tile / More Settings / Before you can use this app, you need to add the tile/button to the quick settings. If you don't know how to do this, take a look at the Tutorial.

This app supports two different methods to take screenshots: / Legacy Method / The legacy method to take screenshots uses the screen recording features of Android.
When you take a screenshot, no sound is played. A silent notification is shown to open, share or edit the screenshot. The notification can be disabled in the app settings.
Before you can take a screenshot you need to add the tile to the quick settings, accept the permission to record the screen and the permission to access the internal storage to save the image file.
See the tutorial on how to do it.

On some phones this method does not work, especially on newer Androids (9.0+) it is unstable and it may ask for permission on every single screenshot. If that happens you should use the native method below.`
- **Back 后 +10.5s**：`com.github.cvzi.screenshottile/com.github.cvzi.screenshottile.activities.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Screenshot Tile / More Settings / Before you can use this app, you need to add the tile/button to the quick settings. If you don't know how to do this, take a look at the Tutorial.

This app supports two different methods to take screenshots: / Legacy Method / The legacy method to take screenshots uses the screen recording features of Android.
When you take a screenshot, no sound is played. A silent notification is shown to open, share or edit the screenshot. The notification can be disabled in the app settings.
Before you can take a screenshot you need to add the tile to the quick settings, accept the permission to record the screen and the permission to access the internal storage to save the image file.
See the tutorial on how to do it.

On some phones this method does not work, especially on newer Androids (9.0+) it is unstable and it may ask for permission on every single screenshot. If that happens you should use the native method below.`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.github.cvzi.screenshottile` / `MainActivity` | `-` | 11 | 1536 / 否 | `click` → [9] Switch text="Native Method" id=switchNative (click, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.github.cvzi.screenshottile` / `MainActivity` | `-` | 4 | 1109 / 否 | `click` → [4] Button text="I AGREE" id=button1 (click) center=(87 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 214 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.github.cvzi.screenshottile/MainActivity`)**: `Screenshot Tile` | `More Settings` | `Before you can use this app, you need to add the tile/b` | `Legacy Method` | `The legacy method to take screenshots uses the screen r` | `Tutorial` | `Native Method` | `The native method to take screenshots simulates a press`
- **Step 2 (`com.github.cvzi.screenshottile/MainActivity`)**: `Google Play Prominent Disclosure & Consent Requirement` | `Google Play requires prominent disclosure of the Access` | `I REFUSE` | `I AGREE`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Screenshot Tile` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用主界面把截图功能包装成「传统(录屏)／原生(无障碍模拟电源+Home键)」两种选择，用户开启原生方式后立刻弹出 Google Play 醒目披露弹窗，以「仅用于截图、不收集不共享」话术索取无障碍 API；同意后被引导到系统无障碍设置与服务详情页，再触发「完全控制设备」系统警告，拒绝则回到主界面并永久挂着「无障碍服务已禁用」提示，被困在诱饵页。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 「使用前需先把磁贴/按钮加入快捷设置，不会操作请看教程」（主界面 step_01）
- 英文 -> 「原生方式模拟按下 Home+电源键，调用设备自带截图；需先在系统设置中启用无障碍服务，点击下方按钮打开」（主界面 step_01）
- 英文 -> 「本应用非无障碍工具，但需访问无障碍服务 API，才能在应用未使用时截图；录屏仅用于生成截图，数据既不收集也不共享」（醒目披露弹窗 step_02）
- 英文 -> 按钮「I REFUSE 我拒绝」「I AGREE 我同意」，把同意设为唯一前进路径（step_02）
- 英文 -> 「启用此服务后，应用可模拟电源+Home 键截图，某些设备上比默认方式更稳更快；在系统里启用后还需在应用设置中打开原生方式」（服务详情页）
- 英文 -> 「允许 Screenshot Tile 完全控制你的设备？完全控制只适合辅助无障碍需求的应用，大多数应用不适用」，并列出可读取屏幕全部内容、可在其他应用上显示内容、可代替你操作应用（系统警告弹窗）
- 英文 -> 主界面常驻警告「⚠️ Accessibility service is disabled 无障碍服务已被禁用」，作为拒权后仍留在此页的提示（refusal_2.0s/10.5s）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面：列出「传统」(录屏静音截图)与「原生」(模拟电源+Home键)两种方式。本步打开原生开关，触发披露流程。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | Google Play 醒目披露弹窗：称需无障碍 API 才能离屏截图、数据不收集不共享，问是否授权。本步点「I AGREE」。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍设置列表：下载应用区显示 Screenshot Tile 状态为 Off 关闭。采集到无障碍设置钩子后自动终止。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停在无障碍设置页，界面文本为空，无通知横幅、无遮罩，页面状态平稳。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：无障碍设置页无变化，未见浮层或通知，应用也未再弹出补充说明话术。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 服务详情页：「Use Screenshot Tile」开关默认关，说明启用后可模拟电源+Home键截图，但还须在应用内开启原生方式。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统授权警告弹窗：称授予后可完全控制设备、读取屏幕内容并代你操作，提供「Allow 允许」与「Deny 拒绝」。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 点 Deny 返回主界面 2 秒：页面内容基本未变，仅底部新增「⚠️ 无障碍服务已禁用」提示，无其他出口。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权后 10.5 秒：仍停在主界面诱饵页，无障碍禁用警告不变，无跳转或绕过路径，判定被困。 | `step_03_refusal_10500ms_screen.png` |

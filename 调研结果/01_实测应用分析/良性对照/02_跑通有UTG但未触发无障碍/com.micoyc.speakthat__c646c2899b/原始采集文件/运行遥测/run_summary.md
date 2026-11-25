# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:07:05
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.micoyc.speakthat`（静态标签：`benign` / `残障辅助与无障碍支持` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.micoyc.speakthat` / `OnboardingActivity` | `-` | 15 | 261 / 否 | `click` → [15] ImageButton desc="Next" id=buttonNext (click) cent | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.micoyc.speakthat` / `OnboardingActivity` | `-` | 11 | 328 / 否 | `click` → [11] ImageButton desc="Next" id=buttonNext (click) cent | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.micoyc.speakthat` / `OnboardingActivity` | `-` | 17 | 444 / 否 | `click` → [17] ImageButton desc="Next" id=buttonNext (click) cent | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.micoyc.speakthat` / `OnboardingActivity` | `-` | 14 | 398 / 否 | `click` → [10] Button text="Open Settings" id=buttonOpenSettings  | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings$NotificationAccessSettingsActivity` | `-` | 12 | 92 / 否 | `system_button` → Back | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.micoyc.speakthat` / `OnboardingActivity` | `-` | 14 | 398 / 否 | `click` → [14] ImageButton desc="Next" id=buttonNext (click) cent | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.micoyc.speakthat` / `OnboardingActivity` | `-` | 14 | 398 / 否 | `swipe` → [900, 1000] | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.micoyc.speakthat` / `OnboardingActivity` | `-` | 14 | 398 / 否 | `click` → [14] ImageButton desc="Next" id=buttonNext (click) cent | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.micoyc.speakthat/OnboardingActivity`)**: `SpeakThat!` | `Language icon` | `Language` | `Choose which language you would like SpeakThat to use!` | `Tap the box below to pick which language SpeakThat shou` | `English (United States)` | `Information icon` | `Is your language not complete?` | `Back` | `Mute`
- **Step 2 (`com.micoyc.speakthat/OnboardingActivity`)**: `SpeakThat!` | `SpeakThat icon` | `Welcome to SpeakThat!` | `Stay connected without staring at your screen!` | `How does SpeakThat work?` | `When you receive a notification, SpeakThat will read it` | `Back` | `Mute` | `Skip` | `Next`
- **Step 3 (`com.micoyc.speakthat/OnboardingActivity`)**: `SpeakThat!` | `Privacy shield icon` | `Privacy-First` | `Your privacy is SpeakThat's priority. Learn how it ensu` | `Will it read sensitive notifications?` | `SpeakThat gives you complete control over what gets rea` | `• notifications from specific apps` | `• notifications containing specific words` | `• in certain places` | `• between certain times`
- **Step 4 (`com.micoyc.speakthat/OnboardingActivity`)**: `SpeakThat!` | `Notification bell icon` | `Permission Required` | `SpeakThat requires notifications access to read aloud i` | `Grant SpeakThat access to your notifications` | `SpeakThat can't read your notifications if it can't see` | `Tip: In the list, tap 'SpeakThat' to enable` | `Open Settings` | `Back` | `Mute`
- **Step 5 (`com.android.settings/Settings$NotificationAccessSettingsActivity`)**: `Back` | `Notification access` | `Search settings` | `Android Auto` | `Not allowed` | `Pixel Launcher` | `Allowed` | `SpeakThat!`
- **Step 6 (`com.micoyc.speakthat/OnboardingActivity`)**: `SpeakThat!` | `Notification bell icon` | `Permission Required` | `SpeakThat requires notifications access to read aloud i` | `Grant SpeakThat access to your notifications` | `SpeakThat can't read your notifications if it can't see` | `Tip: In the list, tap 'SpeakThat' to enable` | `Open Settings` | `Back` | `Mute`
- **Step 7 (`com.micoyc.speakthat/OnboardingActivity`)**: `SpeakThat!` | `Notification bell icon` | `Permission Required` | `SpeakThat requires notifications access to read aloud i` | `Grant SpeakThat access to your notifications` | `SpeakThat can't read your notifications if it can't see` | `Tip: In the list, tap 'SpeakThat' to enable` | `Open Settings` | `Back` | `Mute`
- **Step 8 (`com.micoyc.speakthat/OnboardingActivity`)**: `SpeakThat!` | `Notification bell icon` | `Permission Required` | `SpeakThat requires notifications access to read aloud i` | `Grant SpeakThat access to your notifications` | `SpeakThat can't read your notifications if it can't see` | `Tip: In the list, tap 'SpeakThat' to enable` | `Open Settings` | `Back` | `Mute`

## 中文逐页引导链路解读

> **全链路总结**：该应用从语言选择、欢迎与隐私说明页进入通知访问权限引导，点击“Open Settings”跳到系统通知访问列表后返回，仍停留权限页并反复点击或滑动 Next 尝试推进。整体以功能说明、本地处理和过滤控制为主，未见通知横幅或遮罩，授权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 不必盯着屏幕也能保持连接（第2页欢迎页）
- English -> 所有处理完全在设备本地完成，用户可控制朗读内容（第2页欢迎页）
- English -> 可创建过滤器阻止朗读特定应用、特定词语、特定地点、特定时间或未连接指定蓝牙设备时的通知（第3页隐私页）
- English -> SpeakThat 需要通知访问权限才能朗读收到的通知（第4/6/7/8页权限页）
- English -> 授予 SpeakThat 通知访问权限（第4/6/7/8页权限页）
- English -> 若无法查看通知就无法朗读，需要到系统设置允许访问（第4/6/7/8页权限页）
- English -> 提示：在列表中点击“SpeakThat”以启用（第4/6/7/8页权限页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: OnboardingActivity** | 语言选择引导页，显示英文（美国）及语言不完整说明；点击底部Next进入下一页。 | `step_01_action.png` |
| 2 | **Step 2: OnboardingActivity** | 欢迎说明页，称无需盯屏即可朗读通知且本地处理；点击Next继续。 | `step_02_action.png` |
| 3 | **Step 3: OnboardingActivity** | 隐私优先说明页，列出按应用、词语、地点、时间、蓝牙过滤朗读；点击Next继续。 | `step_03_action.png` |
| 4 | **Step 4: OnboardingActivity** | 通知访问权限页，要求到系统设置允许读取通知；本步点击Open Settings跳转系统设置。 | `step_04_action.png` |
| 5 | **Step 5: Settings$NotificationAcces** | 系统“通知访问”列表，见Android Auto未允许、Pixel Launcher已允许及SpeakThat；按返回键退出。 | `step_05_action.png` |
| 6 | **Step 6: OnboardingActivity** | 返回应用同一通知权限页，文案未变；再次点击Next尝试推进到无障碍权限。 | `step_06_action.png` |
| 7 | **Step 7: OnboardingActivity** | 停留通知权限页，因Next未响应改为左滑翻页；界面与权限要求未变化。 | `step_07_action.png` |
| 8 | **Step 8: OnboardingActivity** | 仍为通知权限页，按元素ID再次点击Next尝试推进；无遮罩或通知横幅。 | `step_08_action.png` |

# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:59:50
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`app.plugbrain.android`（静态标签：`benign` / `专注自律与防沉迷管控` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 4 步，UTG 唯一节点 `6` 个，有向边 `8` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 4 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_04_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`app.plugbrain.android/app.plugbrain.android.ui.onboarding.OnboardingActivity` | hooks=`[]` | overlays=`0` | texts=`Let's get set up / PlugBrain needs the following permissions to work correctly. / App usage access / Lets PlugBrain track app usage so it can block distracting apps at the right time. / Display over other apps`
- **Back 后 +5.5s**：`app.plugbrain.android/app.plugbrain.android.ui.onboarding.OnboardingActivity` | hooks=`[]` | overlays=`0` | texts=`Let's get set up / PlugBrain needs the following permissions to work correctly. / App usage access / Lets PlugBrain track app usage so it can block distracting apps at the right time. / Display over other apps`
- **Back 后 +10.5s**：`app.plugbrain.android/app.plugbrain.android.ui.onboarding.OnboardingActivity` | hooks=`[]` | overlays=`0` | texts=`Let's get set up / PlugBrain needs the following permissions to work correctly. / App usage access / Lets PlugBrain track app usage so it can block distracting apps at the right time. / Display over other apps`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `app.plugbrain.android` / `OnboardingActivity` | `-` | 9 | 266 / 否 | `click` → [8] View (click) center=(540,2035) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `app.plugbrain.android` / `OnboardingActivity` | `-` | 17 | 509 / 否 | `click` → [9] View (click,unchecked) center=(540,1169) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `app.plugbrain.android` / `OnboardingActivity` | `-` | 10 | 440 / 否 | `click` → [8] TextView text="Agree and continue" center=(540,1809 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 210 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_04_layout.xml` + `step_04_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`app.plugbrain.android/OnboardingActivity`)**: `Plug your brain back in.` | `Focus your attention` | `Spend less time on apps that distract you.` | `Unlock with a challenge` | `Solve a quick math challenge to keep using the app.` | `Gets harder the longer you stay` | `Challenges increase in difficulty the longer you keep s` | `Get started`
- **Step 2 (`app.plugbrain.android/OnboardingActivity`)**: `Let's get set up` | `PlugBrain needs the following permissions to work corre` | `App usage access` | `Lets PlugBrain track app usage so it can block distract` | `Display over other apps` | `Allows PlugBrain to display a challenge while you use a` | `Accessibility permission` | `Allows PlugBrain to detect when apps are open.` | `Battery optimization (optional)` | `Ensures that PlugBrain keeps running reliably even when`
- **Step 3 (`app.plugbrain.android/OnboardingActivity`)**: `Close sheet` | `Drag handle` | `Turn the accessibility service on` | `PlugBrain uses the Accessibility service to see which a` | `Find PlugBrain, then turn on the switch and confirm.` | `Agree and continue` | `Not now`
- **Step 4 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `PlugBrain 🧠` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: OnboardingActivity** | Step 1: OnboardingActivity（OnboardingActivity）：Plug your brain back in. / Focus your at；动作 click | `step_01_action.png` |
| 2 | **Step 2: OnboardingActivity** | Step 2: OnboardingActivity（OnboardingActivity）：Let's get set up / PlugBrain needs the f；动作 click | `step_02_action.png` |
| 3 | **Step 3: OnboardingActivity** | Step 3: OnboardingActivity（OnboardingActivity）：Close sheet / Drag handle / Turn the acc；动作 click | `step_03_action.png` |
| 4 | **Step 4: [无障碍列表页]** | Step 4: [无障碍列表页]（Settings$AccessibilitySettingsActivity）：Back / Accessibility / Search settings；动作 terminate | `step_04_screen.png` |
| 5 | **跳后探针 +0.8s** | 跳后探针 +0.8s（Settings$AccessibilitySettingsActivity）：无文本；动作 wait(0.8s) | `step_04_probe_800ms_screen.png` |
| 6 | **跳后探针 +2.0s** | 跳后探针 +2.0s（Settings$AccessibilitySettingsActivity）：无文本；动作 wait(2.0s) | `step_04_probe_2000ms_screen.png` |
| 7 | **服务详情页** | 服务详情页（SubSettings）：Back / PlugBrain 🧠 / Use PlugBrain 🧠；动作 inspect_detail_or_warning | `step_04_service_detail_screen.png` |
| 8 | **系统警告弹窗(点Deny)** | 系统警告弹窗(点Deny)（SubSettings）：Allow PlugBrain 🧠 to have full control o；动作 inspect_detail_or_warning | `step_04_system_warning_screen.png` |
| 9 | **拒权返回 +2.0s** | 拒权返回 +2.0s（OnboardingActivity）：Let's get set up / PlugBrain needs the f；动作 Back_refuse -> TRAPPED_ON_LURE_SCREEN | `step_04_refusal_2000ms_screen.png` |
| 10 | **拒权返回 +10.5s** | 拒权返回 +10.5s（OnboardingActivity）：Let's get set up / PlugBrain needs the f；动作 Back_refuse -> TRAPPED_ON_LURE_SCREEN | `step_04_refusal_10500ms_screen.png` |

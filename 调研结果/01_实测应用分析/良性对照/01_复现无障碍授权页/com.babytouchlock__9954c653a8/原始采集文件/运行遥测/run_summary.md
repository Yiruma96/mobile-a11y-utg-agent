# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:21:22
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.babytouchlock`（静态标签：`benign` / `残障辅助与无障碍支持` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.babytouchlock/com.babytouchlock.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Baby Touch Lock / Screen and buttons lock for kids / Activation Required / Enable the Accessibility Service to intercept touches and buttons. / Enable Service`
- **Back 后 +5.5s**：`com.babytouchlock/com.babytouchlock.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Baby Touch Lock / Screen and buttons lock for kids / Activation Required / Enable the Accessibility Service to intercept touches and buttons. / Enable Service`
- **Back 后 +10.5s**：`com.babytouchlock/com.babytouchlock.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Baby Touch Lock / Screen and buttons lock for kids / Activation Required / Enable the Accessibility Service to intercept touches and buttons. / Enable Service`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.babytouchlock` / `MainActivity` | `-` | 22 | 491 / 否 | `click` → [6] Button text="Enable Service" id=btn_grant_accessibi | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.babytouchlock` / `MainActivity` | `-` | 4 | 347 / 否 | `click` → [4] Button text="Accept & Continue" id=button1 (click)  | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 222 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.babytouchlock/MainActivity`)**: `Baby Touch Lock` | `Screen and buttons lock for kids` | `Activation Required` | `Enable the Accessibility Service to intercept touches a` | `Enable Service` | `Privacy Policy and Accessibility Disclosure` | `SETTINGS` | `Lock Volume Keys` | `Prevents adjusting the volume while locked` | `Wake Screen on Power`
- **Step 2 (`com.babytouchlock/MainActivity`)**: `Accessibility Service Disclosure` | `Baby Touch Lock uses Android's AccessibilityService API` | `Cancel` | `Accept & Continue`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Baby Touch Lock Service` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以儿童触控锁为名，入口页强调必须激活并引导开启无障碍服务；接受应用内披露后进入系统无障碍列表与详情，弹出完全控制警告，拒绝后仍反复回到激活页形成卡点。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English: “Activation Required / Enable the Accessibility Service to intercept touches and buttons.” -> 中文：要求启用无障碍服务以拦截触摸和按键（主界面 step_01）
- English: “Baby Touch Lock uses Android's AccessibilityService API solely to block accidental screen taps...” -> 中文：声称仅用于拦截误触且100%本地隐私，不读取、存储或传输屏幕/按键/个人数据（披露弹窗 step_02）
- English: “Prevents accidental touches, navigation gestures, notification shade expansion, and volume key presses...” -> 中文：宣称可防止误触、导航手势、通知栏展开和音量键，以保护媒体播放（服务详情 detail_1）
- English: “Allow Baby Touch Lock Service to have full control of your device?” -> 中文：系统警告询问是否允许该服务完全控制设备，并称可查看控制屏幕、跟踪交互并代为操作（系统警告 detail_2）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面显示“Baby Touch Lock”和“需要激活”，提示启用无障碍服务拦截触摸与按键；本步点击“Enable Service”进入同意流程，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 应用内无障碍披露弹窗，英文称仅用于拦截误触、全本地隐私且不读取屏幕/按键/个人数据；本步点击“Accept & Continue”准备跳转系统设置。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表页，“Baby Touch Lock Service”显示关闭；采集到无障碍设置钩子后自动终止，无通知横幅或遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针仍停留在系统无障碍列表，界面文本为空，无活动通知与遮罩；仅等待观察，未发生点击。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针仍处于系统无障碍列表，文本为空、通知与遮罩均为0；继续等待，未见自动跳转或覆盖层。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 服务详情页显示“Use Baby Touch Lock Service”及快捷键关闭；说明称防误触、导航手势、通知栏与音量键，本步仅查看。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统“完全控制设备”警告弹窗，列明可查看控制屏幕、跟踪交互并代操作；含允许/拒绝，本步仅检查警告未授权。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回2秒后仍回到主界面“需要激活”页，继续提示启用无障碍服务；未退出也未提供可用替代，形成卡点。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回10.5秒后仍停留在同一激活引导页，重复显示“Enable Service”；无通知或遮罩，应用未放行。 | `step_03_refusal_10500ms_screen.png` |

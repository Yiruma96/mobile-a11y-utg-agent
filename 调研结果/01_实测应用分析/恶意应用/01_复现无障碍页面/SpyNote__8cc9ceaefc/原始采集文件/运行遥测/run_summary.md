# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:13:18
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`cmf0.c3b5bm90zq.patch`（静态标签：`malicious` / `SpyNote` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `3` 个，有向边 `2` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / System Android`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 342 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 3 | 145 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow System Android to access` | `Camera` | `take pictures and record video` | `Files and media` | `access photos, media, and files on your device` | `Call logs` | `read and write phone call log` | `Contacts` | `access your contacts` | `Microphone`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `System Android` | `This app was built for an older version of Android and ` | `OK`

## 中文逐页引导链路解读

> **全链路总结**：该应用伪装成“System Android”，先进入系统权限审查页，集中索取相机、文件、通话记录、联系人、麦克风、短信和电话等敏感权限，随后跳转无障碍设置并触发 Hook；拒权返回后仍自动重拉起无障碍设置，维持“System Android”关闭项与“Phone”通知。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> 选择允许“System Android”访问哪些内容（权限审查页）
- 英语 -> 该应用针对旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者（无障碍设置页）
- 英语 -> 你的数据未备份 / 现在添加备份账户（系统通知横幅，贯穿各页）
- 英语 -> “System Android”/“Phone”作为应用名和通知标题，用于伪装系统组件（权限页、无障碍页、通知栏）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 权限审查页：伪装“System Android”请求相机、文件、通话记录、联系人、麦克风、短信及电话权限，点 Continue；有“数据未备份”通知。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 无障碍设置页：警告“System Android”为旧版构建、可能异常，建议更新或联系开发者；出现 OK，捕获无障碍 Hook 后终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍停在无障碍设置页，界面无文本、无遮罩、无浮层，仅保留“数据未备份”和“Phone”通知。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒探针：无障碍设置页仍无文本，overlays=0、无遮罩；通知栏继续显示“数据未备份”和“Phone”。 | `step_02_probe_2000ms_screen.png` |
| 5 | **拒权返回 +2.0s** | 拒权返回2秒：无障碍列表显示“System Android”为 Off，含 Back、Accessibility 等；拒权后仍自动重拉起无障碍设置，通知保留。 | `step_02_refusal_2000ms_screen.png` |

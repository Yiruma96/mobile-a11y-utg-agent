# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:59:45
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.eset.ems2.gp`（静态标签：`malicious` / `SpyNote` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `3` 个，有向边 `2` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / Any Number`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 338 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 3 | 141 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Any Number to access` | `Camera` | `take pictures and record video` | `Files and media` | `access photos, media, and files on your device` | `Call logs` | `read and write phone call log` | `SMS` | `send and view SMS messages` | `Contacts`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Any Number` | `This app was built for an older version of Android and ` | `OK`

## 中文逐页引导链路解读

> **全链路总结**：该应用以“Any Number”名义先经系统权限审核页批量索取相机、媒体、通话记录、短信、联系人、麦克风与电话权限，随后跳转无障碍设置页；拒权返回后仍重拉起无障碍设置，呈现明显诱导授权与持久化控制特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Choose what to allow Any Number to access -> 选择允许“Any Number”访问的内容（系统权限审核页）
- This app was built for an older version of Android and may not work properly. Try checking for updates, or contact the developer. -> 该应用为旧版 Android 构建、可能无法正常运行，请检查更新或联系开发者（无障碍列表页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审核页：为“Any Number”批量列出相机、媒体、通话记录、短信、联系人、麦克风、电话权限；点“Continue”继续，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 无障碍列表页：显示“Any Number”和“旧版Android可能无法正常运行”警告及“OK”；已捕获无障碍设置钩子后终止，无遮罩，通知栏有该应用通知。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停在无障碍设置页且未读到文字；无悬浮遮罩，通知栏保留谷歌备份和“Any Number”通知，持续等待。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒探针：无障碍设置页仍无可见文字，未出现遮罩；通知栏持续显示谷歌备份与“Any Number”通知，继续等待。 | `step_02_probe_2000ms_screen.png` |
| 5 | **拒权返回 +2.0s** | 拒权返回2.0秒：无障碍页“DOWNLOADED APPS”下“Any Number”为“Off”；返回拒权后应用又重拉起无障碍设置，无遮罩，通知仍在。 | `step_02_refusal_2000ms_screen.png` |

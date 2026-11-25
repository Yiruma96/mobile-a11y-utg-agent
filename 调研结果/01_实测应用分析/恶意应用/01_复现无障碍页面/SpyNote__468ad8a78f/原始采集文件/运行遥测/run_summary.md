# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:04:54
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.android.tester`（静态标签：`malicious` / `SpyNote` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `3` 个，有向边 `2` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / OfficeSuite`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 339 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 3 | 142 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow OfficeSuite to access` | `Camera` | `take pictures and record video` | `Files and media` | `access photos, media, and files on your device` | `Call logs` | `read and write phone call log` | `Contacts` | `access your contacts` | `Microphone`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `OfficeSuite` | `This app was built for an older version of Android and ` | `OK`

## 中文逐页引导链路解读

> **全链路总结**：该应用以 OfficeSuite 名义先弹出 Android 运行时权限审查页，诱导继续授权相机、文件、通话记录、联系人、麦克风、短信与电话；随后跳转无障碍设置页并触发 Hook，拒权返回后仍反复拉起无障碍设置。核心特征为借用系统权限/无障碍界面伪装与持续重定向。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许 OfficeSuite 访问哪些内容”（Step 1 权限审查页标题）
- 英文 -> “此应用针对旧版 Android 构建，可能无法正常工作；请检查更新或联系开发者”（Step 2 无障碍设置页旧版兼容提示）
- 英文 -> “你的数据未备份 / 立即添加备份账户”（权限页及后续页的 GMS 通知横幅）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | Android 权限审查页：以 OfficeSuite 名义请求相机、文件、通话记录、联系人、麦克风、短信与电话，点击 Continue 继续；有未备份通知，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 无障碍设置页：列表出现 OfficeSuite，并弹旧版 Android 可能无法正常工作的提示与 OK；已捕获无障碍设置 Hook/探针后自动终止，通知含 tester/Chrome。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停在无障碍设置页，界面文本为空、遮罩为 0；仅保留 GMS 未备份与 tester/Chrome 通知，无新增交互。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：仍为无障碍设置页，界面文本为空、遮罩为 0；通知栏延续 GMS 未备份及 tester/Chrome 通知，无新增动作。 | `step_02_probe_2000ms_screen.png` |
| 5 | **拒权返回 +2.0s** | 拒权返回 2 秒：无障碍设置页显示 OfficeSuite 为 Off，仍列屏幕阅读器/显示项；执行返回拒绝后触发 RELAUNCHED_A11Y_SETTINGS，通知不变、无遮罩。 | `step_02_refusal_2000ms_screen.png` |

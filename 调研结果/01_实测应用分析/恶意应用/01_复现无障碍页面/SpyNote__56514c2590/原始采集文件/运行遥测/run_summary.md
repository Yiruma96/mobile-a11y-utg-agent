# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:02:00
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

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / Security Checker`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 344 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 3 | 147 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Security Checker to access` | `Camera` | `take pictures and record video` | `Files and media` | `access photos, media, and files on your device` | `Call logs` | `read and write phone call log` | `Contacts` | `access your contacts` | `Microphone`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Security Checker` | `This app was built for an older version of Android and ` | `OK`

## 中文逐页引导链路解读

> **全链路总结**：应用冒充“Security Checker”先拉起系统批量敏感权限页并点击继续，随后跳转无障碍设置出现旧版兼容警告；捕获 A11Y 设置钩子后终止，拒权返回又自动重拉无障碍设置，符合 SpyNote 诱导授权特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Choose what to allow Security Checker to access -> 选择允许“Security Checker”访问哪些内容（系统批量权限页）
- Camera / take pictures and record video -> 相机/拍照和录制视频（系统权限页）
- Files and media / access photos, media, and files on your device -> 文件与媒体/访问设备上的照片、媒体和文件（系统权限页）
- Call logs / read and write phone call log -> 通话记录/读写手机通话记录（系统权限页）
- Contacts / access your contacts -> 联系人/访问联系人（系统权限页）
- Microphone / record audio -> 麦克风/录制音频（系统权限页）
- SMS / send and view SMS messages -> 短信/发送和查看短信（系统权限页）
- Phone -> 电话（系统权限页）
- Security Checker -> “安全检测器”伪装应用名（权限页/无障碍页）
- This app was built for an older version of Android and may not work properly. Try checking for updates, or contact the developer. -> 该应用为旧版 Android 构建，可能无法正常工作；请检查更新或联系开发者（无障碍设置页）
- OK -> 确定（无障碍兼容警告）
- Off -> 关闭（无障碍页，Security Checker 当前未启用）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统批量授权页：伪装 Security Checker 索要相机、文件、通话记录、联系人、麦克风、短信和电话；点 Continue 继续，顶部有未备份通知。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 无障碍设置页：显示“Security Checker”及“旧版 Android 可能无法正常工作”的兼容警告和 OK；本步终止并捕获无障碍设置钩子探针。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍在无障碍设置页，界面无文本，仅见未备份与 Clock 通知横幅；等待0.8秒，无遮罩。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒探针：页面仍未变化，界面文本为空，保留未备份与 Clock 通知横幅；等待2秒，无遮罩覆盖。 | `step_02_probe_2000ms_screen.png` |
| 5 | **拒权返回 +2.0s** | 拒权返回后2秒：无障碍页显示“Security Checker”为 Off，仍列出屏幕阅读器与显示项；返回拒权后自动重拉无障碍设置，通知仍在。 | `step_02_refusal_2000ms_screen.png` |

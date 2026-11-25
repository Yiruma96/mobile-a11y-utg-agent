# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:57:35
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`spymax.stub7.suffix`（静态标签：`malicious` / `SpyMax` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 36 | 348 / 否 | `click` → [36] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 151 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `swipe` → [540, 1800] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 163 / 否 | `click` → [19] TextView text="[SPY_MAX_NAME_PATCH]" id=icon (clic | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 163 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 163 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 163 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow [SPY_MAX_NAME_PATCH] to access` | `SMS` | `send and view SMS messages` | `Call logs` | `read and write phone call log` | `Contacts` | `access your contacts` | `Files and media` | `access photos, media, and files on your device` | `Camera`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `[SPY_MAX_NAME_PATCH]` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`

## 中文逐页引导链路解读

> **全链路总结**：应用链路起于系统权限审查页，集中展示短信、通话记录、联系人、文件媒体、相机、麦克风、位置等高风险权限并以Continue推进；随后经旧版Android警告、桌面与应用抽屉点击目标图标，最后仅发生静态Activity跳转至spymax.stub7.ClassGen9/14/1，未捕获应用自身UI，亦无通知或遮罩，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文“Choose what to allow [SPY_MAX_NAME_PATCH] to access” -> 选择允许[SPY_MAX_NAME_PATCH]访问的内容（Step1权限审查页）
- 英文“send and view SMS messages” -> 发送和查看短信（Step1权限审查页）
- 英文“read and write phone call log” -> 读取和写入通话记录（Step1权限审查页）
- 英文“access your contacts” -> 访问联系人（Step1权限审查页）
- 英文“access photos, media, and files on your device” -> 访问设备上的照片、媒体和文件（Step1权限审查页）
- 英文“take pictures and record video” -> 拍照和录制视频（Step1权限审查页）
- 英文“record audio” -> 录制音频（Step1权限审查页）
- 英文“This app was built for an older version of Android and may not work properly. Try checking for updates, or contact the developer.” -> 此应用为旧版Android构建，可能无法正常运行；请检查更新或联系开发者（Step2旧版警告）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审查页，列短信、通话记录、联系人、文件媒体、相机、麦克风、位置，文案称选择允许[SPY_MAX_NAME_PATCH]访问；仅见Continue并点击。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面弹出旧版Android警告，称[SPY_MAX_NAME_PATCH]可能无法正常运行，建议检查更新或联系开发者；仅OK，点击关闭。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面首页含Apps list、天气与日期；点击“Apps list”打开应用列表，界面无通知横幅或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍为桌面首页/应用列表入口，日期天气可见；上滑以打开应用抽屉寻找目标应用，未出现应用自身界面。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 应用抽屉列出日历、相机、Chrome等系统应用；点击目标图标[SPY_MAX_NAME_PATCH]尝试启动恶意应用。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 界面仍停留应用抽屉，静态引导跳转至spymax.stub7.ClassGen9；未见应用新页面，也无通知或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 仍为应用抽屉画面，静态引导再跳转spymax.stub7.ClassGen14；无可见应用UI、通知横幅或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 仍为应用抽屉画面，静态引导跳转spymax.stub7.ClassGen1；无可见应用页面，通知与遮罩均为零。 | `step_08_screen.png` |

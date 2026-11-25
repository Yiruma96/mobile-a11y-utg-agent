# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:11:53
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`cmf0.c3b5bm90zq.patch`（静态标签：`malicious` / `SpyNote` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 340 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 143 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1800] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 155 / 否 | `click` → [12] TextView text="media player" id=icon (click) cente | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 155 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 155 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 155 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow media player to access` | `Camera` | `take pictures and record video` | `Files and media` | `access photos, media, and files on your device` | `Call logs` | `read and write phone call log` | `Contacts` | `access your contacts` | `Microphone`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `media player` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`

## 中文逐页引导链路解读

> **全链路总结**：该样本伪装为“media player”，入口先进入系统权限审查并请求相机、文件媒体、通话记录、联系人、麦克风、短信、电话等敏感权限；点击Continue后因旧版Android警告退回桌面，后续多次重launch和静态跳转.C7/.C3/.C8均未出现可见业务页，未观察到拒权结果。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Choose what to allow media player to access -> 选择允许“媒体播放器”访问哪些内容（Step 1 权限审查页）
- Camera / take pictures and record video -> 相机/拍照和录像（Step 1 权限审查页）
- Files and media / access photos, media, and files on your device -> 文件与媒体/访问设备上的照片、媒体和文件（Step 1 权限审查页）
- Call logs / read and write phone call log -> 通话记录/读写通话记录（Step 1 权限审查页）
- Contacts / access your contacts -> 联系人/访问联系人（Step 1 权限审查页）
- Microphone / record audio -> 麦克风/录制音频（Step 1 权限审查页）
- SMS / send and view SMS messages -> 短信/发送和查看短信（Step 1 权限审查页）
- Phone -> 电话（Step 1 权限审查页）
- media player -> 媒体播放器（Step 2 与 Step 5 桌面/应用抽屉，应用显示名伪装）
- This app was built for an older version of Android and may not work properly. Try checking for updates, or contact the developer. -> 此应用针对旧版Android构建，可能无法正常运行，请检查更新或联系开发者（Step 2 兼容性警告）
- String (Files) / String (com.google.android.documentsui) -> 字符串(文件)/字符串(com.google.android.documentsui)（Step 2-8 目标应用通知横幅，疑似调试或伪装文本）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 权限审查页以“media player”名义请求相机、文件媒体、通话记录、联系人、麦克风、短信、电话；无横幅/遮罩，点击Continue。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面弹出旧版Android兼容性警告，称应用可能无法正常运行；无遮罩，点击OK关闭，目标应用通知横幅仍在。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面首页含Apps list、Messages、Chrome、Search等；目标应用通知横幅仍在。点击Apps list但未打开抽屉。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍在桌面首页；上滑尝试打开应用抽屉，界面文本未变化，目标应用通知横幅持续显示。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 应用抽屉展开，含Calendar、Camera、Chrome等及“media player”图标；本步点击该图标重launch目标应用。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 应用抽屉界面不变，未见目标业务页；执行静态Activity跳转至.C7，目标应用通知横幅仍显示。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 应用抽屉界面维持不变；执行静态Activity跳转至.C3，仍未出现可见业务界面，通知横幅持续。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 应用抽屉界面维持原样；执行静态Activity跳转至.C8，页面无可见变化，通知横幅仍在。 | `step_08_screen.png` |

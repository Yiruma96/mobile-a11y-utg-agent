# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:55:33
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.example.eventbot`（静态标签：`malicious` / `EventBot` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 11 | 149 / 否 | `click` → [10] Button text="Cancel" id=cancel_button (click) cent | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `wait` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 11 | 149 / 否 | `click` → [10] Button text="Cancel" id=cancel_button (click) cent | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 11 | 149 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Microsoft Word to access` | `Files and media` | `access photos, media, and files on your device` | `SMS` | `send and view SMS messages` | `Cancel` | `Continue`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Microsoft Word to access` | `Files and media` | `access photos, media, and files on your device` | `SMS` | `send and view SMS messages` | `Cancel` | `Continue`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Microsoft Word to access` | `Files and media` | `access photos, media, and files on your device` | `SMS` | `send and view SMS messages` | `Cancel` | `Continue`

## 中文逐页引导链路解读

> **全链路总结**：该应用先以 Microsoft Word 名义弹出文件/媒体与短信权限页，反复点“取消”后回到桌面，再通过静态活动跳转尝试触发 doActivity、sendShortMsg、recvPushMsg 等后台/SMS 相关动作，呈现伪装授权与规避式诱导特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许 Microsoft Word 访问的内容”（Step 1/4/8 权限页）
- 英文 -> “文件与媒体：访问设备上的照片、媒体和文件”（Step 1/4/8 权限页）
- 英文 -> “短信：发送和查看短信”（Step 1/4/8 权限页）
- 英文 -> “取消 / 继续”按钮（Step 1/4/8 权限页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 权限控制器显示“允许 Microsoft Word 访问”页，含文件媒体与短信两项；点“取消”关闭授权，未出现通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 回到桌面启动器，显示应用列表、日期、天气及 Messages/Chrome/搜索；本步仅等待，无通知横幅或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 仍在桌面启动器，界面同上；本步按包名重新打开 EventBot，试图重启后台权限线程，无通知与遮罩。 | `step_03_action.png` |
| 4 | **Step 4: ReviewPermissionsActivity** | 再次弹出“允许 Microsoft Word 访问”权限页，索要文件媒体与短信；点“取消”拒绝，通知与遮罩均为零。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面启动器等待页，保留应用列表、日期、Messages/Chrome/搜索；等待后台权限线程浮层，未观察到通知或遮罩。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面启动器上执行静态活动跳转，界面仍为应用列表等；探针拟跳转 func.doActivity，无通知、无遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 仍在桌面启动器，显示应用列表、日期、Messages/Chrome/搜索；静态跳转指向 .sendShortMsg，无通知横幅与遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: ReviewPermissionsActivity** | 静态跳转触发权限控制器“允许 Microsoft Word 访问”页，索要文件媒体与短信；指向 .recvPushMsg，无通知/遮罩。 | `step_08_screen.png` |

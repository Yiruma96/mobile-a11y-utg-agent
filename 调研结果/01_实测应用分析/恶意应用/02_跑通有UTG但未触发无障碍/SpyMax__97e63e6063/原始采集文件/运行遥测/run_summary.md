# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:18:31
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.flayvr.flayvr`（静态标签：`malicious` / `SpyMax` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 334 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.flayvr.flayvr` / `iozrkbwinawtxxtfsusguypnjty1912` | `-` | 3 | 137 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.flayvr.flayvr` / `iozrkbwinawtxxtfsusguypnjty1912` | `-` | 2 | 30 / 否 | `system_button` → Back | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.flayvr.flayvr` / `iozrkbwinawtxxtfsusguypnjty1912` | `-` | 2 | 30 / 否 | `system_button` → Home | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [7] FrameLayout desc="Search" id=search_container_all_a | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.flayvr.flayvr` / `iozrkbwinawtxxtfsusguypnjty1912` | `-` | 2 | 30 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.flayvr.flayvr` / `iozrkbwinawtxxtfsusguypnjty1912` | `-` | 2 | 30 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Images to access` | `SMS` | `send and view SMS messages` | `Call logs` | `read and write phone call log` | `Contacts` | `access your contacts` | `Files and media` | `access photos, media, and files on your device` | `Camera`
- **Step 2 (`com.flayvr.flayvr/iozrkbwinawtxxtfsusguypnjty1912`)**: `Images` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.flayvr.flayvr/iozrkbwinawtxxtfsusguypnjty1912`)**: `net::ERR_INTERNET_DISCONNECTED`
- **Step 4 (`com.flayvr.flayvr/iozrkbwinawtxxtfsusguypnjty1912`)**: `net::ERR_INTERNET_DISCONNECTED`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`
- **Step 7 (`com.flayvr.flayvr/iozrkbwinawtxxtfsusguypnjty1912`)**: `net::ERR_INTERNET_DISCONNECTED`
- **Step 8 (`com.flayvr.flayvr/iozrkbwinawtxxtfsusguypnjty1912`)**: `net::ERR_INTERNET_DISCONNECTED`

## 中文逐页引导链路解读

> **全链路总结**：该应用入口先以“Images”名义触发系统权限复核，集中索要短信、通话记录、联系人、文件媒体、相机、麦克风和位置；随后进入混淆Activity的WebView仅显示网络断开，兼容性弹窗与空通知伴随，多次静态跳转未展示实际业务，授权/拒权结果未测。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文“Choose what to allow Images to access” -> “选择允许Images访问什么”（Step 1 权限复核页）
- 英文“SMS / send and view SMS messages” -> “短信：发送和查看短信”（Step 1 权限复核页）
- 英文“Call logs / read and write phone call log” -> “通话记录：读取和写入通话记录”（Step 1 权限复核页）
- 英文“Contacts / access your contacts” -> “联系人：访问你的联系人”（Step 1 权限复核页）
- 英文“Files and media / access photos, media, and files on your device” -> “文件与媒体：访问设备上的照片、媒体和文件”（Step 1 权限复核页）
- 英文“Camera / take pictures and record video” -> “相机：拍照和录制视频”（Step 1 权限复核页）
- 英文“Microphone / record audio” -> “麦克风：录制音频”（Step 1 权限复核页）
- 英文“Location” -> “位置”（Step 1 权限复核页）
- 英文“This app was built for an older version of Android and may not work properly. Try checking for updates, or contact the developer.” -> “此应用针对旧版Android构建，可能无法正常工作；请检查更新或联系开发者”（Step 2 兼容性警告）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限页：“Images”索要短信、通话记录、联系人、文件媒体、相机、麦克风、位置；点“Continue”继续，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: iozrkbwinawtxxtfsusguypnjt** | 兼容性警告弹窗：称应用为旧版Android构建、可能异常；点“OK”关闭；应用空通知在，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: iozrkbwinawtxxtfsusguypnjt** | 应用WebView错误页：显示“net::ERR_INTERNET_DISCONNECTED”（网络未连接）；按返回无效，空通知在，无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: iozrkbwinawtxxtfsusguypnjt** | 同一网络错误页：返回无效后按Home离开应用，转桌面/设置继续；应用空通知仍在，无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面启动器页：显示应用列表、日期、Messages、Chrome与搜索；点搜索容器查找设置；空通知在，无遮罩。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面全局搜索页：显示前往Discover、搜索应用/网页及语音搜索；本步静态跳回应用WebView，空通知在，无遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: iozrkbwinawtxxtfsusguypnjt** | 回到应用WebView网络错误页；本步静态跳转至另一混淆Activity（…19054），空通知在，无遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: iozrkbwinawtxxtfsusguypnjt** | 仍为网络错误页；静态跳转目标改为混淆Activity（…1905），未见实际业务或授权弹窗，空通知在，无遮罩。 | `step_08_screen.png` |

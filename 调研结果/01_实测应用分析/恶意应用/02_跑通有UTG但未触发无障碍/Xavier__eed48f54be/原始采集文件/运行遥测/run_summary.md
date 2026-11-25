# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:26:04
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.minfivezz.launcher`（静态标签：`malicious` / `Xavier` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 31 | 323 / 否 | `click` → [31] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.minfivezz.launcher` / `Launcher` | `-` | 3 | 148 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.minfivezz.launcher` / `Launcher` | `-` | 21 | 191 / 否 | `click` → [15] TextView text="Lollipop Setting" (click) center=(4 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.minfivezz.launcher` / `LauncherSetting` | `-` | 15 | 102 / 否 | `click` → [4] TextView text="Common" id=title center=(282,302) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.minfivezz.launcher` / `LauncherSetting` | `-` | 11 | 159 / 否 | `click` → [6] TextView text="Notification Toolbar" id=title cente | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.minfivezz.launcher` / `LauncherSetting` | `-` | 11 | 159 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.minfivezz.launcher` / `CommonPrefActivity` | `-` | 11 | 140 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.minfivezz.launcher` / `CommonPrefActivity` | `-` | 11 | 140 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Lollipop Launcher to access` | `Phone` | `make and manage phone calls` | `Contacts` | `access your contacts` | `Files and media` | `access photos, media, and files on your device` | `SMS` | `send and view SMS messages` | `Call logs`
- **Step 2 (`com.minfivezz.launcher/Launcher`)**: `Lollipop Launcher` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.minfivezz.launcher/Launcher`)**: `Search` | `Voice Search` | `Import from others` | `User guide` | `Lollipop Tool Box` | `Lollipop Boost` | `Theme` | `Folder: Lollipop Apps` | `Lollipop Apps` | `Lollipop Setting`
- **Step 4 (`com.minfivezz.launcher/LauncherSetting`)**: `Lollipop Launcher` | `Common` | `Desktop` | `Drawer` | `Dock` | `Sidebar` | `Folder` | `Theme & UI` | `Unread Counts` | `Gestures & Buttons`
- **Step 5 (`com.minfivezz.launcher/LauncherSetting`)**: `Common, Navigate up` | `Common` | `Set Default Launcher` | `No default selected` | `Notification Toolbar` | `Launcher style` | `Android L style` | `Security & Privacy` | `protect hidden app, lock app`
- **Step 6 (`com.minfivezz.launcher/LauncherSetting`)**: `Common, Navigate up` | `Common` | `Set Default Launcher` | `No default selected` | `Notification Toolbar` | `Launcher style` | `Android L style` | `Security & Privacy` | `protect hidden app, lock app`
- **Step 7 (`com.minfivezz.launcher/CommonPrefActivity`)**: `Common` | `Set Default Launcher` | `No default selected` | `Notification Toolbar` | `Launcher style` | `Android L style` | `Security & Privacy` | `protect hidden app, lock app`
- **Step 8 (`com.minfivezz.launcher/CommonPrefActivity`)**: `Common` | `Set Default Launcher` | `No default selected` | `Notification Toolbar` | `Launcher style` | `Android L style` | `Security & Privacy` | `protect hidden app, lock app`

## 中文逐页引导链路解读

> **全链路总结**：应用以“Lollipop Launcher”启动器为外壳，先经系统权限复核页集中索取电话、联系人、文件媒体、短信、通话记录、定位、相机等权限，再以旧版兼容提示和启动器设置/通知工具栏引导进入设置及静态跳转页面；全程无遮罩，通知横幅短暂出现，未测试拒绝分支。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许 Lollipop Launcher 访问什么”（Step 1 ReviewPermissionsActivity）
- 英文 -> “电话/拨打和管理电话”“联系人/访问联系人”“文件与媒体/访问设备上的照片、媒体和文件”“短信/发送和查看短信”“通话记录/读写通话记录”“位置/访问本机位置”“相机”（Step 1 ReviewPermissionsActivity）
- 英文 -> “此应用为旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者”（Step 2 Launcher 兼容警告）
- 英文 -> “Lollipop 设置”（Step 3 启动器主屏入口）
- 英文 -> “通知工具栏”“设置默认启动器/未选择默认”“安全与隐私/保护隐藏应用、锁定应用”（Step 5-8 设置页）
- 英文 -> 占位通知“String (Notification) / String (Hello)”（Step 2-5 顶部通知横幅）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统英文权限复核页，集中展示电话、联系人、文件媒体、短信、通话记录、定位、相机等权限说明；点击“Continue”继续。 | `step_01_action.png` |
| 2 | **Step 2: Launcher** | 旧版兼容警告页，英文提示应用为旧 Android 构建或异常；点“OK”关闭，通知横幅“String (Hello)”仍在。 | `step_02_action.png` |
| 3 | **Step 3: Launcher** | 启动器主屏，含搜索、语音搜索、工具箱/加速、主题、Lollipop 设置等入口；点击“Lollipop Setting”进入设置，通知横幅仍在。 | `step_03_action.png` |
| 4 | **Step 4: LauncherSetting** | 设置总览页，含常用、桌面、抽屉、Dock、侧栏、文件夹、主题界面、未读计数、手势按键、高级；点击“Common”进入常用设置。 | `step_04_action.png` |
| 5 | **Step 5: LauncherSetting** | 常用设置页，显示未选默认启动器、通知工具栏、Android L 风格、安全与隐私；点击“Notification Toolbar”触发通知访问说明。 | `step_05_action.png` |
| 6 | **Step 6: LauncherSetting** | 仍为常用设置页，界面同上；本步通过静态引导跳转至 CommonPrefActivity，未见可见点击或新弹窗，通知横幅已消失。 | `step_06_screen.png` |
| 7 | **Step 7: CommonPrefActivity** | 静态跳转后的 CommonPrefActivity，重复展示常用设置项；随后引导跳至 HibernateActivity，未见新界面内容或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: CommonPrefActivity** | 仍停留 CommonPrefActivity 的设置项，最后静态引导跳向 WallpaperCropActivity 壁纸裁剪页；无可见弹窗、遮罩或通知横幅。 | `step_08_screen.png` |

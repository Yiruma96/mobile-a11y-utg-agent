# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:49:11
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.coramobile.powerbattery.batterysaver`（静态标签：`malicious` / `Xavier` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 15 | 179 / 否 | `click` → [15] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.coramobile.powerbattery.batterysaver` / `SplashActivity` | `-` | 3 | 144 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.coramobile.powerbattery.batterysaver` / `SplashActivity` | `-` | 2 | 48 / 否 | `click` → [1] Button text="START" id=btn_start (click) center=(54 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.coramobile.powerbattery.batterysaver` / `UserTipActivity` | `-` | 4 | 77 / 否 | `click` → [4] TextView text="Skip" id=skip (click) center=(80,195 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.coramobile.powerbattery.batterysaver` / `MainActivity` | `-` | 3 | 77 / 否 | `click` → [3] TextView text="ALLOW" id=button_accept (click) cent | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.coramobile.powerbattery.batterysaver` / `MainActivity` | `-` | 3 | 77 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.coramobile.powerbattery.batterysaver` / `MainActivity` | `-` | 3 | 77 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.coramobile.powerbattery.batterysaver` / `MainActivity` | `-` | 3 | 77 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Battery Saver to access` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Phone` | `make and manage phone calls` | `Cancel` | `Continue`
- **Step 2 (`com.coramobile.powerbattery.batterysaver/SplashActivity`)**: `Battery Saver` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.coramobile.powerbattery.batterysaver/SplashActivity`)**: `START` | `By proceeding you agree with Privacy Policy`
- **Step 4 (`com.coramobile.powerbattery.batterysaver/UserTipActivity`)**: `Thank you for choosing Battery Saver` | `Swipe left or right to see more tips.` | `Skip`
- **Step 5 (`com.coramobile.powerbattery.batterysaver/MainActivity`)**: `Allow application to access photos, media, and files on` | `DENY` | `ALLOW`
- **Step 6 (`com.coramobile.powerbattery.batterysaver/MainActivity`)**: `Allow application to access photos, media, and files on` | `DENY` | `ALLOW`
- **Step 7 (`com.coramobile.powerbattery.batterysaver/MainActivity`)**: `Allow application to access photos, media, and files on` | `DENY` | `ALLOW`
- **Step 8 (`com.coramobile.powerbattery.batterysaver/MainActivity`)**: `Allow application to access photos, media, and files on` | `DENY` | `ALLOW`

## 中文逐页引导链路解读

> **全链路总结**：应用先经系统权限复核与旧版警告，以“Battery Saver”和隐私政策同意进入，教程可跳过；主界面反复弹出存储授权框，点ALLOW后仍以静态跳转探针前往Force、Splash、Shortcut页面。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> “选择允许Battery Saver访问哪些内容”（Step 1 系统权限复核页）
- English -> “访问设备上的照片、媒体和文件/联系人/拨打电话”（Step 1 权限清单）
- English -> “此应用为旧版Android构建，可能无法正常工作，请检查更新或联系开发者”（Step 2 旧版警告）
- English -> “继续即表示同意隐私政策”（Step 3 启动页）
- English -> “感谢选择Battery Saver；左右滑动查看更多提示”（Step 4 教程页）
- English -> “允许应用访问设备上的照片、媒体和文件吗？”（Step 5-8 存储授权弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限复核页：要求选择Battery Saver可访问的文件媒体、联系人、电话；有取消/继续，本步点“继续”放行权限复核。 | `step_01_action.png` |
| 2 | **Step 2: SplashActivity** | 旧版Android警告页：提示应用为旧版构建、可能异常，建议更新或联系开发者；本步点OK关闭警告继续。 | `step_02_action.png` |
| 3 | **Step 3: SplashActivity** | 应用启动页：显示START及“继续即同意隐私政策”，以隐私政策捆绑同意；本步点START进入主流程。 | `step_03_action.png` |
| 4 | **Step 4: UserTipActivity** | 新手提示页：称“感谢选择Battery Saver”并提示左右滑动看更多；提供Skip，本步点Skip跳过教程。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 主界面弹出存储授权框：请求照片、媒体和文件访问，提供DENY/ALLOW；有标题正文均为null的通知，本步点ALLOW。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 仍为存储授权弹窗，未做点击；保留空通知横幅，并静态探针跳转ForceActivity，授权框未消失。 | `step_06_screen.png` |
| 7 | **Step 7: MainActivity** | 存储授权弹窗重复显示，界面无变化；空通知横幅仍在，静态探针改跳SplashActivity，授权仍未处理。 | `step_07_screen.png` |
| 8 | **Step 8: MainActivity** | 存储授权弹窗仍停留，空通知横幅持续；静态探针跳转ShortcutActivity，显示应用反复引导授权与快捷入口。 | `step_08_screen.png` |

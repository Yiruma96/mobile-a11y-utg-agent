# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:07:07
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.update.system.important`（静态标签：`malicious` / `boogr` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 37 | 341 / 否 | `click` → [37] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 37 | 341 / 否 | `click` → [37] Button text="Continue" id=continue_button (click)  | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 37 | 341 / 否 | `click` → [895, 1390] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 4 | 187 / 否 | `click` → [4] Button text="Allow" id=button1 (click) center=(887, | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 4 | 187 / 否 | `click` → [4] Button text="Allow" id=button1 (click) center=(887, | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow System Update to access` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location` | `access this device's location` | `Microphone` | `record audio` | `Phone`
- **Step 2 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Choose what to allow System Update to access` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location` | `access this device's location` | `Microphone` | `record audio` | `Phone`
- **Step 3 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Choose what to allow System Update to access` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location` | `access this device's location` | `Microphone` | `record audio` | `Phone`
- **Step 4 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Let app always run in background?` | `Allowing System Update to always run in the background ` | `Deny` | `Allow`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Let app always run in background?` | `Allowing System Update to always run in the background ` | `Deny` | `Allow`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：该应用伪装为“System Update/系统更新”，先请求通讯录、相机、位置、麦克风、电话、通话记录、短信等高风险权限，再诱导允许忽略电池优化以常驻后台；允许后迅速回落桌面，后续仅发生静态跳转回退，未进入实际功能界面。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 选择允许“系统更新”访问什么（权限总览页）
- 英文 -> 通讯录；访问你的通讯录（权限总览页）
- 英文 -> 相机；拍照和录像（权限总览页）
- 英文 -> 位置；访问本设备位置（权限总览页）
- 英文 -> 麦克风；录音（权限总览页）
- 英文 -> 电话；拨打和管理电话（权限总览页）
- 英文 -> 通话记录；读写通话记录（权限总览页）
- 英文 -> 短信（权限总览页）
- 英文 -> 让应用始终在后台运行？（电池优化弹窗）
- 英文 -> 允许系统更新始终后台运行可能缩短续航，可稍后在设置中更改（电池优化弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 权限总览页以“系统更新”名义请求通讯录、相机、位置、麦克风、电话、通话记录和短信权限；点击“继续”进入下一步。 | `step_01_action.png` |
| 2 | **Step 2: RequestIgnoreBatteryOptimi** | 电池优化请求活动仍显示权限总览文本，列出通讯录、相机、位置、麦克风等高风险权限；点击“继续”推进。 | `step_02_action.png` |
| 3 | **Step 3: RequestIgnoreBatteryOptimi** | 仍为电池优化请求活动且无通知/遮罩，界面沿用权限总览文本；按坐标点击屏幕中部尝试推进流程。 | `step_03_action.png` |
| 4 | **Step 4: RequestIgnoreBatteryOptimi** | 系统弹窗询问“让应用始终在后台运行？”，称可能缩短续航、可稍后更改，提供“拒绝/允许”；点击“允许”授予后台常驻。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 已回到桌面但仍残留后台运行授权弹窗，含“拒绝/允许”按钮；再次点击“允许”以消除弹窗并推进。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 回到桌面应用列表，显示日期、信息、Chrome、搜索等；执行静态活动跳转回退（Utility.displayActivity），未进入业务页。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 仍在桌面应用列表，无通知或遮罩；静态跳转回退到“.LeanbackLauncherActivity”，应用流程未呈现。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 仍在桌面应用列表，无业务界面；静态跳转回退到“.PackageReceiver”，未观察到进一步诱导或权限操作。 | `step_08_screen.png` |

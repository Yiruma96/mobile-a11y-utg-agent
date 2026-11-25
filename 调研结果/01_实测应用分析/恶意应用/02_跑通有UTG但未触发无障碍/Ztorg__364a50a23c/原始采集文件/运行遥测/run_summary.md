# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:10:40
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.countrys.converter.currency`（静态标签：`malicious` / `Ztorg` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 19 | 217 / 否 | `click` → [19] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.countrys.converter.currency` / `MainActivity` | `-` | 3 | 146 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.countrys.converter.currency` / `MainActivity` | `-` | 13 | 82 / 否 | `click` → [4] TextView desc="Setting" id=menu_setting (click) cen | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.countrys.converter.currency` / `SettingActivity` | `-` | 6 | 196 / 否 | `system_button` → Home | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.countrys.converter.currency` / `UponGuideActivity` | `-` | 1 | 142 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.countrys.converter.currency` / `UponGuideActivity` | `-` | 1 | 142 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Money Converter to access` | `Contacts` | `access your contacts` | `Files and media` | `access photos, media, and files on your device` | `Camera` | `take pictures and record video` | `Phone` | `make and manage phone calls` | `Cancel`
- **Step 2 (`com.countrys.converter.currency/MainActivity`)**: `Money Converter` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.countrys.converter.currency/MainActivity`)**: `Currency` | `Wall` | `Setting` | `1` | `Euro Member Countries (EUR)` | `Click Calculate for Result` | `Calculate`
- **Step 4 (`com.countrys.converter.currency/SettingActivity`)**: `Setting` | `Theme` | `Change the theme for this app` | `Disclaimer` | `Neither Currency Converter nor GoodView Studio is liabl`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.countrys.converter.currency/UponGuideActivity`)**: `Please open the Acccessibility on, protect your informa`
- **Step 8 (`com.countrys.converter.currency/UponGuideActivity`)**: `Please open the Acccessibility on, protect your informa`

## 中文逐页引导链路解读

> **全链路总结**：应用先通过系统权限审查索要联系人、文件媒体、相机和电话权限，关闭旧版 Android 警告后进入伪装货币转换器；在设置页停留后返回桌面/应用列表，最终由 UponGuideActivity 以“保护隐私”恐吓话术诱导开启无障碍，并指向广播接收器链路。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许 Money Converter 访问哪些内容”（系统权限审查页，列出联系人、文件媒体、相机、电话）
- 英文 -> “此应用针对旧版 Android 构建，可能无法正常运行，请检查更新或联系开发者”（旧版兼容警告）
- 英文 -> “请开启无障碍，保护你的信息不被泄露、不被窃取，防止他人窥探你的隐私”（UponGuideActivity，恐吓式诱导开启无障碍）
- 英文 -> “Currency Converter 与 GoodView Studio 均不对汇率数据错误/延迟或据此采取的行动负责”（设置页免责声明）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审查页：英文要求选择允许 Money Converter 访问联系人、文件媒体、相机和电话；点击 Continue 继续。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 主界面弹出旧版 Android 兼容警告，称应用可能无法正常运行；点击 OK 关闭，通知栏出现异常“String (  )”通知。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 伪装货币转换器主页，含 Currency、Wall、Setting 与 EUR 换算入口；点击右上角 Setting 齿轮进入设置页。 | `step_03_action.png` |
| 4 | **Step 4: SettingActivity** | 设置页含 Theme 与免责声明，称 Currency Converter/GoodView Studio 不担责；随后按 Home 退到后台等待广播。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 系统桌面显示 Apps list、日期和常用图标；点击“Apps list”打开应用列表，准备重新启动目标应用。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 仍在系统桌面/应用列表，未见可点目标；探针以静态跳转回退进入 UponGuideActivity。 | `step_06_screen.png` |
| 7 | **Step 7: UponGuideActivity** | UponGuideActivity 用英文恐吓话术要求开启无障碍，称可防信息泄露、窃取和隐私窥探；本步静态跳转。 | `step_07_screen.png` |
| 8 | **Step 8: UponGuideActivity** | 同一无障碍诱导页继续停留，话术不变；探针再次静态跳转至 OpenAccessReceiver，疑似广播触发链路。 | `step_08_screen.png` |

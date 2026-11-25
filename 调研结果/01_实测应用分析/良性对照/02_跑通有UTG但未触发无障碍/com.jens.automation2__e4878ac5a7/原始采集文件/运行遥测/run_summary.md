# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:02:30
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.jens.automation2`（静态标签：`benign` / `系统效率与通用辅助` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.jens.automation2` / `ActivityPermissions` | `-` | 7 | 547 / 否 | `click` → [7] Button text="continue" id=bRequestPermissions (clic | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 4 | 184 / 否 | `click` → [4] Button text="Allow" id=button1 (click) center=(887, | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.jens.automation2` / `ActivityMainScreen` | `-` | 3 | 233 / 否 | `click` → [3] Button text="No" id=button2 (click) center=(764,135 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.jens.automation2` / `ActivityMainTabLayout` | `-` | 25 | 231 / 否 | `click` → [13] ToggleButton text="OFF" id=tbArmMastListener (clic | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.jens.automation2` / `ActivityMainTabLayout` | `-` | 25 | 231 / 否 | `click` → [25] Button text="Control center" id=bControlCenter (cl | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.jens.automation2` / `ActivityControlCenter` | `-` | 12 | 513 / 否 | `click` → [4] Button text="Settings" id=bMoreSettings (click) cen | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.jens.automation2` / `ActivitySettings` | `-` | 27 | 688 / 否 | `swipe` → [540, 1900] | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.jens.automation2` / `ActivitySettings` | `-` | 29 | 692 / 否 | `system_button` → Back | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.jens.automation2/ActivityPermissions`)**: `Automation` | `Required permissions` | `The app is current running in limited mode and has deac` | `These are the permissions required:` | `Exclude from battery optimization Recommended for bette` | `Cancel` | `continue`
- **Step 2 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Let app always run in background?` | `Allowing Automation to always run in the background may` | `Deny` | `Allow`
- **Step 3 (`com.jens.automation2/ActivityMainScreen`)**: `Would you like to receive (only important) news about t` | `Yes` | `No`
- **Step 4 (`com.jens.automation2/ActivityMainTabLayout`)**: `Automation` | `Overview` | `Locations` | `Rules` | `Profiles` | `Status` | `Service:` | `OFF` | `Active location:` | `Service is not running.`
- **Step 5 (`com.jens.automation2/ActivityMainTabLayout`)**: `Automation` | `Overview` | `Locations` | `Rules` | `Profiles` | `Status` | `Service:` | `OFF` | `Active location:` | `Service is not running.`
- **Step 6 (`com.jens.automation2/ActivityControlCenter`)**: `Automation` | `Control center` | `Settings` | `When clicking import or export you select the directory` | `Import configuration` | `Export configuration` | `Volume calibration` | `Default settings` | `If you have a problem, suggestions or question, please ` | `Attach config and log files.`
- **Step 7 (`com.jens.automation2/ActivitySettings`)**: `Automation` | `General settings` | `Start at system boot` | `On/Off` | `Start service after update` | `Start service automatically after app update if it has ` | `Show icon` | `Show icon when service is running (hiding it only works` | `Log to console (logcat)` | `Write log file`
- **Step 8 (`com.jens.automation2/ActivitySettings`)**: `Automation` | `Maximum log file size in Megabyte. Will be rotated if b` | `UI theme` | `The theme of the graphical user interface. Application ` | `Start screen` | `Select the screen the applications opens with at start.` | `Position of tab bar` | `Choose where the tabs bar should be placed.` | `Display language` | `Set a custom language for the application`

## 中文逐页引导链路解读

> **全链路总结**：链路自权限说明页开始，经系统电池优化豁免、新闻订阅拒绝，进入概览页尝试开启服务，再进入控制中心与通用设置查找权限/无障碍入口，最终返回。整体为系统自动化工具的正常授权引导，文案透明并给出取消/拒绝/否选项，全程未见通知横幅或遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> “应用当前处于受限模式并停用了部分功能，如需完整功能须在后续权限对话框授予权限；准备好后点击继续。”（Step 1 权限说明页）
- English -> “允许 Automation 始终在后台运行可能缩短电池续航，之后可在设置中更改。”（Step 2 系统电池优化弹窗）
- English -> “是否接收有关本应用的重要资讯？内容来自开发者网站，仅主屏文字，不会 intrusive notification。”（Step 3 新闻提示弹窗）
- English -> “导入或导出时需选择目录，导出可能覆盖现有文件；有问题请写邮件说明，不要只发送默认邮件和文件。”（Step 6 控制中心说明）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ActivityPermissions** | 权限说明页：称应用受限并列出需电池优化豁免等权限，可取消；点击 continue 进入系统授权。 | `step_01_action.png` |
| 2 | **Step 2: RequestIgnoreBatteryOptimi** | 系统电池优化弹窗：询问是否允许 Automation 始终后台运行并提示耗电，提供 Deny/Allow；点击 Allow。 | `step_02_action.png` |
| 3 | **Step 3: ActivityMainScreen** | 主界面新闻弹窗：询问是否接收开发者网站重要资讯，称仅主屏文字、不打扰；点击 No 拒绝。 | `step_03_action.png` |
| 4 | **Step 4: ActivityMainTabLayout** | 主界面概览标签：显示 Service OFF、服务未运行、位置与规则历史；点击 OFF 开关尝试启用服务。 | `step_04_action.png` |
| 5 | **Step 5: ActivityMainTabLayout** | 主界面概览仍显示 Service OFF；点击 Control center 进入控制中心，准备查找服务与权限控制。 | `step_05_action.png` |
| 6 | **Step 6: ActivityControlCenter** | 控制中心：含设置、配置导入/导出、音量校准和联系开发者说明；点击 Settings 查找权限入口。 | `step_06_action.png` |
| 7 | **Step 7: ActivitySettings** | 通用设置页：含开机启动、更新后启动、显示图标和日志等开关；向下滑动查找权限/无障碍入口。 | `step_07_action.png` |
| 8 | **Step 8: ActivitySettings** | 通用设置下半部：含主题、起始页、标签栏、语言、更新和主屏新闻；按 Back 返回，未发现无障碍项。 | `step_08_action.png` |

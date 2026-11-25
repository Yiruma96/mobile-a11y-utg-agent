# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:58:26
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`store.pandaac.task9d`（静态标签：`malicious` / `Unattributed` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `store.pandaac.task9d` / `UpgradeActivity` | `-` | 22 | 486 / 否 | `click` → [6] View (click) center=(540,817) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `store.pandaac.task9d` / `UpgradeActivity` | `-` | 1 | 0 / 是 | `system_button` → Back | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `store.pandaac.task9d` / `UpgradeActivity` | `-` | 20 | 465 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `store.pandaac.task9d` / `UpgradeActivity` | `-` | 20 | 465 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`store.pandaac.task9d/UpgradeActivity`)**: `Setup needed` | `3 steps left` | `Accessibility disclosure` | `Accessibility service` | `Turn it on in Accessibility settings so the button can ` | `What the button opens` | `Choose the app or shortcut the button opens.` | `Unrestricted battery` | `Stops your phone from putting the service to sleep.` | `Button action`
- **Step 2 (`store.pandaac.task9d/UpgradeActivity`)**: (空文本)
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-2°C` | `Cloudy, -2°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-2°C` | `Cloudy, -2°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-2°C` | `Cloudy, -2°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-2°C` | `Cloudy, -2°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`store.pandaac.task9d/UpgradeActivity`)**: `Google Play` | `Update Available` | `To use this app, download the latest version.` | `TikTok18+` | `E` | `Everyone` | `What's new` | `Last updated` | `We are always making changes and improvements to this a` | `More info`
- **Step 8 (`store.pandaac.task9d/UpgradeActivity`)**: `Google Play` | `Update Available` | `To use this app, download the latest version.` | `TikTok18+` | `E` | `Everyone` | `What's new` | `Last updated` | `We are always making changes and improvements to this a` | `More info`

## 中文逐页引导链路解读

> **全链路总结**：应用入口以“还剩3步”的设置向导诱导开启无障碍服务与无限制电池，并配置无障碍按钮启动器；中途出现可返回关闭的伪造更新遮罩，随后切至桌面并通过静态跳转探针进入未知来源权限、启动路由、调试安装及视频流/交易模块。本次轨迹未实际完成授权或拒权，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 需要设置；还剩3步（Step 1）
- 英文 -> 在无障碍设置中开启它，按钮才能工作（Step 1）
- 英文 -> 防止手机让服务休眠（Step 1）
- 英文 -> 选择按下无障碍按钮时打开的应用或快捷方式（Step 1）
- 英文 -> 有可用更新；要使用此应用，请下载最新版本（Step 7/8）
- 英文 -> 关键安全漏洞补丁（Step 7/8）
- 英文 -> 冒充“TikTok18+”“Google Play”品牌与“更新”按钮（Step 7/8）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: UpgradeActivity** | 伪装设置引导页：称需设置、余3步，诱导开启无障碍与无限制电池；本步点“无障碍服务”继续；系统未备份通知常驻，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: UpgradeActivity** | 页面无文本，疑为伪造“Update Available”网页遮罩；按返回键关闭并退回；系统未备份通知常驻，无取消提示。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 已切到系统桌面，显示应用列表、天气与搜索；未见本应用界面，需重新启动继续；系统未备份通知常驻。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍在系统桌面；本步点“应用列表”试图查找并重启目标应用；未出现授权页；系统未备份通知常驻。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 仍为系统桌面；探针静态跳转“未知来源安装权限”页但界面未变；无授权弹窗；系统未备份通知常驻。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 仍为系统桌面；探针静态跳转启动路由页但界面未变；未见诱导或授权弹窗；系统未备份通知常驻。 | `step_06_screen.png` |
| 7 | **Step 7: UpgradeActivity** | 伪造Google Play更新页：标“TikTok18+”“有可用更新”，称须下最新版并补安全漏洞；本步跳调试安装页；有系统未备份通知。 | `step_07_screen.png` |
| 8 | **Step 8: UpgradeActivity** | 仍为伪造Google Play更新页，以TikTok18+和安全补丁催促更新；本步静态跳视频流/交易模块；系统未备份通知，无遮罩。 | `step_08_screen.png` |

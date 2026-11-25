# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:03:42
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`video.lotus19.ridenovel31`（静态标签：`malicious` / `Unattributed` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `video.lotus19.ridenovel31` / `UpgradeActivity` | `-` | 1 | 0 / 是 | `click` → [888, 1063] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `video.lotus19.ridenovel31` / `UpgradeActivity` | `-` | 20 | 465 / 否 | `click` → [13] Button text="Update" id=installBtn (click) center= | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.vpndialogs` / `ConfirmDialog` | `-` | 4 | 219 / 否 | `click` → [4] Button text="OK" id=button1 (click) center=(887,141 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$ManageAppExternalSourcesActivity` | `-` | 10 | 318 / 否 | `click` → [9] Switch id=switch_widget (unchecked) center=(972,707 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings$ManageAppExternalSourcesActivity` | `-` | 10 | 318 / 否 | `system_button` → Back | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `Settings$ManageAppExternalSourcesActivity` | `-` | 10 | 318 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.settings` / `Settings$ManageAppExternalSourcesActivity` | `-` | 10 | 318 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.settings` / `Settings$ManageAppExternalSourcesActivity` | `-` | 10 | 318 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`video.lotus19.ridenovel31/UpgradeActivity`)**: (空文本)
- **Step 2 (`video.lotus19.ridenovel31/UpgradeActivity`)**: `Google Play` | `Update Available` | `To use this app, download the latest version.` | `Dixmax Tv` | `E` | `Everyone` | `What's new` | `Last updated` | `We are always making changes and improvements to this a` | `More info`
- **Step 3 (`com.android.vpndialogs/ConfirmDialog`)**: `Connection request` | `D​i⁠‌‍x​m⁠⁠a‍⁠x ‌T‍‌⁠v wants to set up a VPN connection` | `Cancel` | `OK`
- **Step 4 (`com.android.settings/Settings$ManageAppExternalSourcesActivity`)**: `Back` | `Install unknown apps` | `Search settings` | `D​i⁠‌‍x​m⁠⁠a‍⁠x ‌T‍‌⁠v` | `1.91.37.237` | `Allow from this source` | `Your phone and personal data are more vulnerable to att`
- **Step 5 (`com.android.settings/Settings$ManageAppExternalSourcesActivity`)**: `Back` | `Install unknown apps` | `Search settings` | `D​i⁠‌‍x​m⁠⁠a‍⁠x ‌T‍‌⁠v` | `1.91.37.237` | `Allow from this source` | `Your phone and personal data are more vulnerable to att`
- **Step 6 (`com.android.settings/Settings$ManageAppExternalSourcesActivity`)**: `Back` | `Install unknown apps` | `Search settings` | `D​i⁠‌‍x​m⁠⁠a‍⁠x ‌T‍‌⁠v` | `1.91.37.237` | `Allow from this source` | `Your phone and personal data are more vulnerable to att`
- **Step 7 (`com.android.settings/Settings$ManageAppExternalSourcesActivity`)**: `Back` | `Install unknown apps` | `Search settings` | `D​i⁠‌‍x​m⁠⁠a‍⁠x ‌T‍‌⁠v` | `1.91.37.237` | `Allow from this source` | `Your phone and personal data are more vulnerable to att`
- **Step 8 (`com.android.settings/Settings$ManageAppExternalSourcesActivity`)**: `Back` | `Install unknown apps` | `Search settings` | `D​i⁠‌‍x​m⁠⁠a‍⁠x ‌T‍‌⁠v` | `1.91.37.237` | `Allow from this source` | `Your phone and personal data are more vulnerable to att`

## 中文逐页引导链路解读

> **全链路总结**：应用入口伪装成 Google Play 的“有可用更新”页，诱导点击 Update 后依次请求 VPN 授权和“安装未知应用”权限，随后静态跳转至安装/启动路由模板。核心特征是假更新页加系统权限诱导，观测中未见拒绝分支。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> Google Play/有可用更新/需下载最新版本才能使用本应用（Step2 伪Google Play更新页）
- English -> 以“持续改进”和“关键安全漏洞补丁”为由催促更新（Step2 伪更新页）
- English -> Dixmax Tv 请求建立可监控网络流量的 VPN 连接，仅信任来源时才应接受（Step3 VPN授权弹窗）
- English -> 系统警告：从未知来源安装应用会使手机和个人数据更易受攻击（Step4-8 未知来源设置页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: UpgradeActivity** | UpgradeActivity无可见文案，已伪装Google Play更新入口；顶部有“数据未备份”通知，本步点击坐标继续。 | `step_01_action.png` |
| 2 | **Step 2: UpgradeActivity** | 伪Google Play更新页显示“有可用更新”、Dixmax Tv及安全补丁说明；点击Update继续，通知横幅仍在。 | `step_02_action.png` |
| 3 | **Step 3: ConfirmDialog** | 系统VPN连接请求弹窗称Dixmax Tv将监控网络流量；保留Cancel/OK，本步点击OK授予VPN权限。 | `step_03_action.png` |
| 4 | **Step 4: Settings$ManageAppExternal** | 系统“安装未知应用”设置页，显示Dixmax Tv与IP 1.91.37.237；本步打开“允许来自此来源”开关。 | `step_04_action.png` |
| 5 | **Step 5: Settings$ManageAppExternal** | 同一未知来源设置页，开关已开启；本步按返回键，准备回到应用继续安装流程。 | `step_05_action.png` |
| 6 | **Step 6: Settings$ManageAppExternal** | 仍显示未知来源授权页且已允许；探针静态跳转至UnknownSourcesPermissionActivity，无用户点击。 | `step_06_screen.png` |
| 7 | **Step 7: Settings$ManageAppExternal** | 未知来源页维持已授权状态；探针再次静态跳转至LaunchRouterActivity，继续路由流程。 | `step_07_screen.png` |
| 8 | **Step 8: Settings$ManageAppExternal** | 未知来源页保持不变；探针触发LaunchRouterActivity.startActivity，进入安装/启动路由。 | `step_08_screen.png` |

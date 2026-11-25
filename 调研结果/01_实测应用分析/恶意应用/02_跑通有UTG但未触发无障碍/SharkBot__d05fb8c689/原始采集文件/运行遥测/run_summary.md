# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T16:08:03
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.pagnotto28.sellsourcecode.supercleaner`（静态标签：`malicious` / `SharkBot` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.pagnotto28.sellsourcecode.supercleaner` / `MainActivity` | `-` | 26 | 114 / 否 | `click` → [15] LinearLayout (click) center=(180,1204) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.pagnotto28.sellsourcecode.supercleaner` / `MainActivity` | `-` | 3 | 83 / 否 | `click` → [3] TextView text="Grant Now" id=tv_action_1 (click) ce | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 85 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.pagnotto28.sellsourcecode.supercleaner` / `ResultAcitvity` | `-` | 16 | 258 / 否 | `click` → [16] TextView text="RESOLVE ALL" id=tv_resolve_all (cli | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.pagnotto28.sellsourcecode.supercleaner` / `MainActivity` | `-` | 3 | 90 / 否 | `click` → [3] TextView text="Grant Now" id=tv_action_1 (click) ce | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.pagnotto28.sellsourcecode.supercleaner` / `GuildPermissionActivity` | `-` | 5 | 93 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.pagnotto28.sellsourcecode.supercleaner` / `GuildPermissionActivity` | `-` | 5 | 93 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.pagnotto28.sellsourcecode.supercleaner` / `GuildPermissionActivity` | `-` | 5 | 93 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.pagnotto28.sellsourcecode.supercleaner/MainActivity`)**: `HOME` | `48` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 2 (`com.pagnotto28.sellsourcecode.supercleaner/MainActivity`)**: `Permission Needed` | `Grant access to the external storage memory in the devi` | `Grant Now`
- **Step 3 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Powerful Cleaner, Antivirus to access photos and ` | `Allow` | `Deny`
- **Step 4 (`com.pagnotto28.sellsourcecode.supercleaner/ResultAcitvity`)**: `89` | `%` | `Safety Scanning` | `com.google.android.googlequicksearchbox` | `SECURITY` | `In Danger` | `virus app` | `The app could cause multiple issues like files and syst` | `CHECK` | `dangerous app`
- **Step 5 (`com.pagnotto28.sellsourcecode.supercleaner/MainActivity`)**: `Permission Needed` | `Grant App Usage Permission for a comprehensive phone sc` | `Grant Now`
- **Step 6 (`com.pagnotto28.sellsourcecode.supercleaner/GuildPermissionActivity`)**: `Find Powerful Cleaner, Antivirus and grant usage Access` | `Powerful Cleaner, Antivirus`
- **Step 7 (`com.pagnotto28.sellsourcecode.supercleaner/GuildPermissionActivity`)**: `Find Powerful Cleaner, Antivirus and grant usage Access` | `Powerful Cleaner, Antivirus`
- **Step 8 (`com.pagnotto28.sellsourcecode.supercleaner/GuildPermissionActivity`)**: `Find Powerful Cleaner, Antivirus and grant usage Access` | `Powerful Cleaner, Antivirus`

## 中文逐页引导链路解读

> **全链路总结**：从清理加速首页诱导点击Antivirus后，应用以“Permission Needed/Grant Now”连续索要存储、照片媒体、App Usage与Usage Access权限，并穿插伪造安全扫描“In Danger/RESOLVE ALL”制造恐慌；全程以Allow/Grant Now推进，未见拒权分支，末段停留在引导授权页并静态跳转后台组件，通知横幅为空、无悬浮遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “需要权限：授予设备外部存储访问”，以权限必要性诱导点击Grant Now（Step 2）
- 英语 -> “允许Powerful Cleaner、Antivirus访问设备照片和媒体？”系统授权弹窗（Step 3）
- 英语 -> “安全扫描89%”“google搜索应用：危险/病毒应用，可能造成文件与系统损害或创建后门”“全部解决”（Step 4）
- 英语 -> “检查可能危害设备的权限应用”“跳过/检查”（Step 4）
- 英语 -> “为获得全面手机扫描效果，授予App Usage使用情况权限”（Step 5）
- 英语 -> “找到Powerful Cleaner、Antivirus并授予Usage Access使用情况权限”（Step 6-8）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 首页清理仪表盘显示内存48%、存储/垃圾及Antivirus等磁贴；点击Antivirus进入诱导链，通知为空、无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 权限弹窗谎称需授权外部存储，按钮Grant Now（立即授予）；点击继续推进权限链，通知为空、无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: GrantPermissionsActivity** | 系统媒体授权页请求允许Powerful Cleaner访问照片和媒体；点击Allow放行以继续无障碍流程，页面有Deny，通知为空。 | `step_03_action.png` |
| 4 | **Step 4: ResultAcitvity** | 伪造扫描页显示89%、google搜索应用“In Danger/危险”并称病毒应用；点击RESOLVE ALL触发授权弹窗，通知为空。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 权限弹窗以“全面手机扫描效果”为由索要App Usage使用情况权限，按钮Grant Now；点击继续权限链，通知为空。 | `step_05_action.png` |
| 6 | **Step 6: GuildPermissionActivity** | 引导页要求找到Powerful Cleaner并授予Usage Access权限；静态跳转至电池约束代理，通知为空、无遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: GuildPermissionActivity** | 同一引导页反复要求授予Usage Access权限；静态跳转至WatchmenReceiver安全锁接收器，通知为空、无遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: GuildPermissionActivity** | 同一引导页再次要求授予Usage Access权限；静态跳转至WorkManager电池约束代理，通知为空、无遮罩。 | `step_08_screen.png` |

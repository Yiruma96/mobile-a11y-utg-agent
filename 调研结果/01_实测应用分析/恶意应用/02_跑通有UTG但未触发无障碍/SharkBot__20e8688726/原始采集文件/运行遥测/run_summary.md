# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:38:49
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.abbondioendrizzi.tools.supercleaner`（静态标签：`malicious` / `SharkBot` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.abbondioendrizzi.tools.supercleaner` / `MainActivity` | `-` | 26 | 114 / 否 | `click` → [13] LinearLayout (click) center=(900,951) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.abbondioendrizzi.tools.supercleaner` / `MainActivity` | `-` | 3 | 90 / 否 | `click` → [3] TextView text="Grant Now" id=tv_action_1 (click) ce | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.abbondioendrizzi.tools.supercleaner` / `GuildPermissionActivity` | `-` | 5 | 97 / 否 | `click` → [3] ImageView id=ic_close (click) center=(1008,1790) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$UsageAccessSettingsActivity` | `-` | 16 | 124 / 否 | `system_button` → Back | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.abbondioendrizzi.tools.supercleaner` / `MainActivity` | `-` | 26 | 114 / 否 | `click` → [15] LinearLayout (click) center=(180,1204) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.abbondioendrizzi.tools.supercleaner` / `MainActivity` | `-` | 3 | 83 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.abbondioendrizzi.tools.supercleaner` / `MainActivity` | `-` | 3 | 83 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.abbondioendrizzi.tools.supercleaner` / `MainActivity` | `-` | 3 | 83 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.abbondioendrizzi.tools.supercleaner/MainActivity`)**: `HOME` | `47` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 2 (`com.abbondioendrizzi.tools.supercleaner/MainActivity`)**: `Permission Needed` | `Grant App Usage Permission for a comprehensive phone sc` | `Grant Now`
- **Step 3 (`com.abbondioendrizzi.tools.supercleaner/GuildPermissionActivity`)**: `Find Atom Clean-Booster, Antivirus and grant usage Acce` | `Atom Clean-Booster, Antivirus`
- **Step 4 (`com.android.settings/Settings$UsageAccessSettingsActivity`)**: `Back` | `Usage access` | `Search` | `More options` | `Atom Clean-Booster, Antivirus` | `Not allowed` | `Digital Wellbeing` | `Allowed` | `Google` | `Google Play services`
- **Step 5 (`com.abbondioendrizzi.tools.supercleaner/MainActivity`)**: `HOME` | `47` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 6 (`com.abbondioendrizzi.tools.supercleaner/MainActivity`)**: `Permission Needed` | `Grant access to the external storage memory in the devi` | `Grant Now`
- **Step 7 (`com.abbondioendrizzi.tools.supercleaner/MainActivity`)**: `Permission Needed` | `Grant access to the external storage memory in the devi` | `Grant Now`
- **Step 8 (`com.abbondioendrizzi.tools.supercleaner/MainActivity`)**: `Permission Needed` | `Grant access to the external storage memory in the devi` | `Grant Now`

## 中文逐页引导链路解读

> **全链路总结**：应用先以“超级清理/杀毒/加速”主界面展示内存、存储、垃圾文件等指标，再用“Permission Needed”弹窗逐步索要使用情况访问与外部存储权限，并引导至系统设置；后续静态跳转探针指向权限引导页和后台接收器，整体呈现 SharkBot 类诱导授权链特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “Permission Needed / Grant App Usage Permission for a comprehensive phone scan effect / Grant Now”意为需授予使用情况访问权限才能全面扫描手机，并催促立即授予（Step 2 主界面弹窗）
- 英文 -> “Find Atom Clean-Booster, Antivirus and grant usage Access permission”意为引导在系统设置为指定应用开启使用情况访问权限（Step 3 授权引导页）
- 英文 -> “Permission Needed / Grant access to the external storage memory in the device / Grant Now”意为需授予设备外部存储访问权限，并催促立即授予（Step 6-8 主界面弹窗）
- 英文 -> “Phone boost / Antivirus / Junk files / CPU Cooler”等标签以手机加速、杀毒、垃圾清理、CPU降温营造风险与优化需求（Step 1/5 主界面）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面展示内存47%、存储7%、垃圾文件及加速/杀毒入口；无遮罩，点击“Phone boost”触发授权流程。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 弹出“Permission Needed”权限提示，声称授予应用使用情况权限可实现全面扫描；本步点击“Grant Now”。 | `step_02_action.png` |
| 3 | **Step 3: GuildPermissionActivity** | 授权引导页提示在系统设置中为“Atom Clean-Booster, Antivirus”开启使用情况访问；本步点关闭图标返回。 | `step_03_action.png` |
| 4 | **Step 4: Settings$UsageAccessSettin** | 跳转系统“Usage access”列表，目标应用显示“Not allowed”，其他应用已允许；本步按返回键回应用。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 回到主界面，仍显示内存47%、存储7%等指标；无遮罩，本步改点“Antivirus”再次触发授权引导。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 再次弹出存储权限提示，称需授予外部存储访问；本步为静态跳转探针，指向 GuildPermission 引导页。 | `step_06_screen.png` |
| 7 | **Step 7: MainActivity** | 存储权限提示保持不变；静态跳转探针落到 WorkManager 的电池约束代理组件，未见新界面。 | `step_07_screen.png` |
| 8 | **Step 8: MainActivity** | 存储权限提示仍停留；静态跳转探针指向 WatchmenReceiver 后台接收器，未见新界面或遮罩。 | `step_08_screen.png` |

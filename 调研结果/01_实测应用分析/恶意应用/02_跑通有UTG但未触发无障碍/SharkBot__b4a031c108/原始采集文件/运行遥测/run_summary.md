# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:58:35
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.abbondioendrizzi.tools.supercleaner`（静态标签：`malicious` / `SharkBot` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.abbondioendrizzi.tools.supercleaner` / `MainActivity` | `-` | 26 | 114 / 否 | `wait` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.abbondioendrizzi.tools.supercleaner` / `MainActivity` | `-` | 26 | 114 / 否 | `click` → [9] LinearLayout (click) center=(180,1120) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.abbondioendrizzi.tools.supercleaner` / `MainActivity` | `-` | 3 | 90 / 否 | `click` → [3] TextView text="Grant Now" id=tv_action_1 (click) ce | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.abbondioendrizzi.tools.supercleaner` / `GuildPermissionActivity` | `-` | 5 | 97 / 否 | `click` → [3] ImageView id=ic_close (click) center=(1008,1790) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings$UsageAccessSettingsActivity` | `-` | 16 | 124 / 否 | `system_button` → Back | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.abbondioendrizzi.tools.supercleaner` / `MainActivity` | `-` | 26 | 114 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.abbondioendrizzi.tools.supercleaner` / `MainActivity` | `-` | 26 | 114 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.abbondioendrizzi.tools.supercleaner` / `MainActivity` | `-` | 26 | 114 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.abbondioendrizzi.tools.supercleaner/MainActivity`)**: `HOME` | `46` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 2 (`com.abbondioendrizzi.tools.supercleaner/MainActivity`)**: `HOME` | `46` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 3 (`com.abbondioendrizzi.tools.supercleaner/MainActivity`)**: `Permission Needed` | `Grant App Usage Permission for a comprehensive phone sc` | `Grant Now`
- **Step 4 (`com.abbondioendrizzi.tools.supercleaner/GuildPermissionActivity`)**: `Find Atom Clean-Booster, Antivirus and grant usage Acce` | `Atom Clean-Booster, Antivirus`
- **Step 5 (`com.android.settings/Settings$UsageAccessSettingsActivity`)**: `Back` | `Usage access` | `Search` | `More options` | `Atom Clean-Booster, Antivirus` | `Not allowed` | `Digital Wellbeing` | `Allowed` | `Google` | `Google Play services`
- **Step 6 (`com.abbondioendrizzi.tools.supercleaner/MainActivity`)**: `HOME` | `46` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 7 (`com.abbondioendrizzi.tools.supercleaner/MainActivity`)**: `HOME` | `46` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 8 (`com.abbondioendrizzi.tools.supercleaner/MainActivity`)**: `HOME` | `46` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`

## 中文逐页引导链路解读

> **全链路总结**：入口为伪装手机清理/杀毒的 MainActivity，展示伪造内存、存储与垃圾数据；点击 Junk files 后以“全面扫描效果”诱导授予使用情况权限，经 GuildPermissionActivity 假引导卡跳转系统 Usage access 页，返回后继续静态探测 GuildPermission、WorkManager 代理与 WatchmenReceiver，呈现 SharkBot 类权限滥用与保活/广播探测特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> 需要权限（Step 3 权限弹窗）
- 英语 -> 授予应用使用情况权限以获得全面的手机扫描效果（Step 3 权限弹窗）
- 英语 -> 立即授予（Step 3 权限弹窗按钮）
- 英语 -> 找到 Atom Clean-Booster, Antivirus 并授予使用情况访问权限（Step 4 GuildPermissionActivity 假引导卡）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | MainActivity 首页仪表盘，显示伪造内存46%、存储7%及清理、加速、杀毒入口；本步等待冷启动权限弹窗，无遮罩，通知横幅标题/正文为空。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 仍在首页仪表盘，伪造内存46%、存储7%与清理/加速/杀毒入口；因权限弹窗未出现，本步点击 Junk files 触发扫描入口，无遮罩，空通知横幅。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 弹出“Permission Needed”权限弹窗，称授予使用情况权限可获全面扫描效果；本步点击“Grant Now”，无取消键，通知横幅空。 | `step_03_action.png` |
| 4 | **Step 4: GuildPermissionActivity** | GuildPermissionActivity 假引导卡，要求找到 Atom Clean-Booster 并授予使用情况访问权限；本步点击右上关闭图标以露出底层系统设置页，无遮罩，通知横幅空。 | `step_04_action.png` |
| 5 | **Step 5: Settings$UsageAccessSettin** | 系统 Usage access 页，列表显示 Atom Clean-Booster, Antivirus 为“Not allowed”，Digital Wellbeing/Google 等为“Allowed”；本步按返回键回应用，通知横幅仍为空。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 回到首页，仍显示伪造内存46%、存储7%及清理/加速/杀毒入口；本步静态跳转至 GuildPermissionActivity，未出现权限弹窗，通知横幅空。 | `step_06_screen.png` |
| 7 | **Step 7: MainActivity** | 仍为 MainActivity 首页，显示伪造内存46%、存储7%与功能入口；本步静态跳转目标为 WorkManager 的 ConstraintProxy$Battery 代理，属后台任务探测，无遮罩，通知横幅空。 | `step_07_screen.png` |
| 8 | **Step 8: MainActivity** | 仍为 MainActivity 首页，显示伪造内存46%、存储7%及清理/加速/杀毒入口；本步静态跳转至 WatchmenReceiver 广播接收器，属保活/监听探测，无遮罩，通知横幅空。 | `step_08_screen.png` |

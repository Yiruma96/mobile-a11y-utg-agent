# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T09:59:07
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.abbondioendrizzi.antivirus.supercleaner`（静态标签：`malicious` / `SharkBot` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.abbondioendrizzi.antivirus.supercleaner` / `MainActivity` | `-` | 26 | 114 / 否 | `wait` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.abbondioendrizzi.antivirus.supercleaner` / `MainActivity` | `-` | 26 | 114 / 否 | `click` → [15] LinearLayout (click) center=(180,1204) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.abbondioendrizzi.antivirus.supercleaner` / `MainActivity` | `-` | 3 | 83 / 否 | `click` → [3] TextView text="Grant Now" id=tv_action_1 (click) ce | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 82 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.abbondioendrizzi.antivirus.supercleaner` / `AntivirusActivity` | `-` | 16 | 258 / 否 | `click` → [16] TextView text="RESOLVE ALL" id=tv_resolve_all (cli | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.abbondioendrizzi.antivirus.supercleaner` / `ResultAcitvity` | `-` | 20 | 266 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.abbondioendrizzi.antivirus.supercleaner` / `ResultAcitvity` | `-` | 20 | 266 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.abbondioendrizzi.antivirus.supercleaner` / `ResultAcitvity` | `-` | 20 | 266 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.abbondioendrizzi.antivirus.supercleaner/MainActivity`)**: `HOME` | `35` | `%` | `Memory used` | `6` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 2 (`com.abbondioendrizzi.antivirus.supercleaner/MainActivity`)**: `HOME` | `35` | `%` | `Memory used` | `6` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 3 (`com.abbondioendrizzi.antivirus.supercleaner/MainActivity`)**: `Permission Needed` | `Grant access to the external storage memory in the devi` | `Grant Now`
- **Step 4 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Antivirus, Super Cleaner to access photos and med` | `Allow` | `Deny`
- **Step 5 (`com.abbondioendrizzi.antivirus.supercleaner/AntivirusActivity`)**: `89` | `%` | `Safety Scanning` | `com.google.android.googlequicksearchbox` | `SECURITY` | `In Danger` | `virus app` | `The app could cause multiple issues like files and syst` | `CHECK` | `dangerous app`
- **Step 6 (`com.abbondioendrizzi.antivirus.supercleaner/ResultAcitvity`)**: `ANTIVIRUS` | `SAFE! ALL RISKS ARE RESOLVED` | `JUNK FILES` | `Delete unnecessary data, cache files, redundancy, ads` | `CLEAN` | `CPU COOLER` | `Reduce device temperature to save battery` | `COOLING` | `PHONE BOOST` | `Improve performance, free up memory`
- **Step 7 (`com.abbondioendrizzi.antivirus.supercleaner/ResultAcitvity`)**: `ANTIVIRUS` | `SAFE! ALL RISKS ARE RESOLVED` | `JUNK FILES` | `Delete unnecessary data, cache files, redundancy, ads` | `CLEAN` | `CPU COOLER` | `Reduce device temperature to save battery` | `COOLING` | `PHONE BOOST` | `Improve performance, free up memory`
- **Step 8 (`com.abbondioendrizzi.antivirus.supercleaner/ResultAcitvity`)**: `ANTIVIRUS` | `SAFE! ALL RISKS ARE RESOLVED` | `JUNK FILES` | `Delete unnecessary data, cache files, redundancy, ads` | `CLEAN` | `CPU COOLER` | `Reduce device temperature to save battery` | `COOLING` | `PHONE BOOST` | `Improve performance, free up memory`

## 中文逐页引导链路解读

> **全链路总结**：应用以“Antivirus, Super Cleaner”清理工具为入口，先展示内存、存储、垃圾文件等主页指标，再用应用内“Grant Now”和系统媒体权限弹窗获取授权。随后以虚假安全扫描和“所有风险已解决”结果页制造恐慌与信任，并静态跳转至权限引导、启动页及后台Worker；全程无悬浮遮罩，通知标题与正文均为空。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 需要权限（Step3）
- 英文 -> 授权访问设备外部存储（Step3）
- 英文 -> 立即授权（Step3）
- 英文 -> 允许 Antivirus, Super Cleaner 访问设备上的照片和媒体？（Step4）
- 英文 -> 允许/拒绝（Step4）
- 英文 -> 安全扫描中（Step5）
- 英文 -> 安全状态：处于危险（Step5）
- 英文 -> 病毒应用（Step5）
- 英文 -> 该应用可能造成文件或系统损坏，或创建后门等多重问题（Step5）
- 英文 -> 检查（Step5）
- 英文 -> 危险应用（Step5）
- 英文 -> 查看可能危害设备的授权应用（Step5）
- 英文 -> 跳过（Step5）
- 英文 -> 全部解决（Step5）
- 英文 -> 安全！所有风险已解决（Step6-8）
- 英文 -> 垃圾文件：删除不必要数据、缓存、冗余、广告（Step6-8）
- 英文 -> CPU降温：降低设备温度以省电（Step6-8）
- 英文 -> 手机加速：提升性能、释放内存（Step6-8）
- 英文 -> 省电：停止未使用应用以省电（Step6-8）
- 英文 -> 立即省电（Step6-8）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 清理主页显示内存35%、存储6、垃圾文件及降温/加速/杀毒等磁贴；本步等待权限弹窗，无悬浮遮罩，通知字段为空。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 仍在清理主页，点击“Antivirus/杀毒”磁贴以触发后续权限流程；界面未变化，无悬浮遮罩，通知标题与正文均为空。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 应用内“Permission Needed/需要权限”弹窗，称需访问外部存储，仅见“Grant Now/立即授权”；点击后转入系统权限页，无悬浮遮罩。 | `step_03_action.png` |
| 4 | **Step 4: GrantPermissionsActivity** | 系统GrantPermissionsActivity请求照片和媒体权限，文案为“允许Antivirus, Super Cleaner访问照片和媒体？”；点击“Allow/允许”，有Deny/拒绝。 | `step_04_action.png` |
| 5 | **Step 5: AntivirusActivity** | 杀毒页显示89%与“Safety Scanning/安全扫描中”，把Google搜索应用标为“In Danger/危险、virus app/病毒应用”，点击“RESOLVE ALL/全部解决”；无悬浮遮罩。 | `step_05_action.png` |
| 6 | **Step 6: ResultAcitvity** | 结果页宣称“SAFE! ALL RISKS ARE RESOLVED/安全！所有风险已解决”，列垃圾清理、降温、加速、省电按钮；本步静态跳转权限引导页，无悬浮遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: ResultAcitvity** | 仍为结果页，重复“安全！所有风险已解决”及清理/降温/加速/省电诱导按钮；本步静态跳转Splash启动页，无悬浮遮罩，通知为空。 | `step_07_screen.png` |
| 8 | **Step 8: ResultAcitvity** | 仍为结果页，继续展示“安全！所有风险已解决”和优化按钮；本步静态跳转WorkManager电池约束代理，无可见新界面，无悬浮遮罩。 | `step_08_screen.png` |

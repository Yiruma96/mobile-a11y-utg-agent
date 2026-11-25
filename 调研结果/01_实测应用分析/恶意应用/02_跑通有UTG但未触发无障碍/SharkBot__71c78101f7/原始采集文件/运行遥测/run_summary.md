# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:31:00
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.pagnotto28.sellsourcecode.alpha`（静态标签：`malicious` / `SharkBot` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.pagnotto28.sellsourcecode.alpha` / `MainActivity` | `-` | 26 | 114 / 否 | `wait` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.pagnotto28.sellsourcecode.alpha` / `MainActivity` | `-` | 26 | 114 / 否 | `click` → [15] LinearLayout (click) center=(180,1204) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.pagnotto28.sellsourcecode.alpha` / `MainActivity` | `-` | 3 | 83 / 否 | `click` → [3] TextView text="Grant Now" id=tv_action_1 (click) ce | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 81 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.pagnotto28.sellsourcecode.alpha` / `ResultAcitvity` | `-` | 16 | 258 / 否 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.pagnotto28.sellsourcecode.alpha` / `ResultAcitvity` | `-` | 20 | 266 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.pagnotto28.sellsourcecode.alpha` / `ResultAcitvity` | `-` | 20 | 266 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.pagnotto28.sellsourcecode.alpha` / `ResultAcitvity` | `-` | 20 | 266 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.pagnotto28.sellsourcecode.alpha/MainActivity`)**: `HOME` | `41` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 2 (`com.pagnotto28.sellsourcecode.alpha/MainActivity`)**: `HOME` | `41` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 3 (`com.pagnotto28.sellsourcecode.alpha/MainActivity`)**: `Permission Needed` | `Grant access to the external storage memory in the devi` | `Grant Now`
- **Step 4 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Alfa Antivirus, Cleaner to access photos and medi` | `Allow` | `Deny`
- **Step 5 (`com.pagnotto28.sellsourcecode.alpha/ResultAcitvity`)**: `89` | `%` | `Safety Scanning` | `com.google.android.googlequicksearchbox` | `SECURITY` | `In Danger` | `virus app` | `The app could cause multiple issues like files and syst` | `CHECK` | `dangerous app`
- **Step 6 (`com.pagnotto28.sellsourcecode.alpha/ResultAcitvity`)**: `ANTIVIRUS` | `SAFE! ALL RISKS ARE RESOLVED` | `JUNK FILES` | `Delete unnecessary data, cache files, redundancy, ads` | `CLEAN` | `CPU COOLER` | `Reduce device temperature to save battery` | `COOLING` | `PHONE BOOST` | `Improve performance, free up memory`
- **Step 7 (`com.pagnotto28.sellsourcecode.alpha/ResultAcitvity`)**: `ANTIVIRUS` | `SAFE! ALL RISKS ARE RESOLVED` | `JUNK FILES` | `Delete unnecessary data, cache files, redundancy, ads` | `CLEAN` | `CPU COOLER` | `Reduce device temperature to save battery` | `COOLING` | `PHONE BOOST` | `Improve performance, free up memory`
- **Step 8 (`com.pagnotto28.sellsourcecode.alpha/ResultAcitvity`)**: `ANTIVIRUS` | `SAFE! ALL RISKS ARE RESOLVED` | `JUNK FILES` | `Delete unnecessary data, cache files, redundancy, ads` | `CLEAN` | `CPU COOLER` | `Reduce device temperature to save battery` | `COOLING` | `PHONE BOOST` | `Improve performance, free up memory`

## 中文逐页引导链路解读

> **全链路总结**：入口为仿清理/杀毒主页，先以“Antivirus”磁贴和“Grant Now”诱导外部存储权限，再跳系统照片媒体授权；随后进入ResultActivity伪造89%扫描并将Google搜索组件标为危险病毒，引导CHECK/RESOLVE ALL，最终展示“风险已解决”清理加速功能页并静态跳转内部/系统组件。整条观测链路无拒权分支。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “需要权限 / 授予访问设备外部存储 / 立即授予”（Step 3 权限诱导框）
- 英文 -> “允许 Alfa Antivirus, Cleaner 访问设备上的照片和媒体？”（Step 4 系统授权页）
- 英文 -> “安全 / 处于危险 / 病毒应用 / 该应用可能导致文件与系统损坏或创建后门”（Step 5 仿扫描结果页）
- 英文 -> “危险应用 / 检查可能危害设备的授权应用”（Step 5 仿扫描结果页）
- 英文 -> “安全！所有风险已解决”（Step 6-8 结果页）
- 英文 -> “删除不必要数据、缓存、冗余和广告”（Step 6-8 JUNK FILES 功能说明）
- 英文 -> “降低设备温度以省电 / 提升性能释放内存 / 停止未用应用以省电”（Step 6-8 功能磁贴说明）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 仿清理工具主页：显示内存41%、存储7%及加速/杀毒入口；等待原生权限弹窗，无遮罩，通知横幅标题为空。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 仍在清理主页，点击“Antivirus/杀毒”磁贴，意图触发受控存储权限；无遮罩，通知横幅为空。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 弹出“需要权限”诱导框，声称授予外部存储访问，点“Grant Now/立即授予”；仅见授予钮，无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: GrantPermissionsActivity** | 系统授权页：询问是否允许Alfa Antivirus, Cleaner访问照片和媒体，点“Allow/允许”；通知为空，无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: ResultAcitvity** | 仿扫描页：89%安全检查，将Google搜索组件标“In Danger/危险病毒应用”，诱导CHECK/RESOLVE ALL；无遮罩，通知空。 | `step_05_action.png` |
| 6 | **Step 6: ResultAcitvity** | 结果页转为“SAFE! ALL RISKS ARE RESOLVED/风险已解决”，列出清理、降温、加速、省电入口；静态跳转权限引导，无遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: ResultAcitvity** | 界面仍为“风险已解决”清理功能页；探针静态跳转至WorkManager电池约束代理，无可见变化，无遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: ResultAcitvity** | 仍停留“风险已解决”功能页；探针静态跳转至applock的WatchmenReceiver，界面无变化，无遮罩。 | `step_08_screen.png` |

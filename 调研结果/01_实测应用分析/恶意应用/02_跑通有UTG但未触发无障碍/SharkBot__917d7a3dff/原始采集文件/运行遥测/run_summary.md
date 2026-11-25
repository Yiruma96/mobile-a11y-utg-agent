# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:14:09
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.fastcleaner.forphoneandroid.freenoads`（静态标签：`malicious` / `SharkBot` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.fastcleaner.forphoneandroid.freenoads` / `MainActivity` | `-` | 26 | 114 / 否 | `wait` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.fastcleaner.forphoneandroid.freenoads` / `MainActivity` | `-` | 26 | 114 / 否 | `click` → [23] FrameLayout desc="Toolbox" id=navigation_tools (cl | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.fastcleaner.forphoneandroid.freenoads` / `MainActivity` | `-` | 16 | 157 / 否 | `click` → [11] FrameLayout desc="Home" id=navigation_home (click) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.fastcleaner.forphoneandroid.freenoads` / `MainActivity` | `-` | 26 | 114 / 否 | `open` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.fastcleaner.forphoneandroid.freenoads` / `MainActivity` | `-` | 26 | 114 / 否 | `system_button` → Home | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.fastcleaner.forphoneandroid.freenoads/MainActivity`)**: `HOME` | `45` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 2 (`com.fastcleaner.forphoneandroid.freenoads/MainActivity`)**: `HOME` | `45` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 3 (`com.fastcleaner.forphoneandroid.freenoads/MainActivity`)**: `TOOLBOX` | `Clean & Boost` | `App Uninstall` | `Rapidly uninstall useless apps` | `Game Booster` | `Provide you faster and better game experience` | `Security & Privacy` | `Home` | `Toolbox` | `Personal`
- **Step 4 (`com.fastcleaner.forphoneandroid.freenoads/MainActivity`)**: `HOME` | `45` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 5 (`com.fastcleaner.forphoneandroid.freenoads/MainActivity`)**: `HOME` | `45` | `%` | `Memory used` | `7` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：应用以清理工具主页和工具箱为入口，反复尝试通过onResume、重启或退后台触发权限/引导页，但观察中始终未出现权限对话框；随后落入系统桌面，并静态跳转至权限页、WorkManager电池约束代理及WatchmenReceiver，未完成授权或拒权，呈现伪装清理工具的可疑跳转链。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Junk files -> 垃圾文件（主页）
- CPU Cooler -> CPU降温（主页）
- Phone boost -> 手机加速（主页）
- Antivirus -> 杀毒（主页）
- Power Saving -> 省电（主页）
- Game Booster -> 游戏加速（主页/工具箱）
- Clean & Boost -> 清理与加速（工具箱页）
- Rapidly uninstall useless apps -> 快速卸载无用应用（工具箱页）
- Provide you faster and better game experience -> 提供更快更好的游戏体验（工具箱页）
- Security & Privacy -> 安全与隐私（工具箱页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主页清理面板：显示内存45%、存储7%及垃圾文件、CPU降温、加速、杀毒等英文入口；本步等待，未弹权限框，无遮罩，仅见应用空通知。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 主页清理面板：英文内存/存储/垃圾/CPU降温/加速/杀毒入口；点击底部Toolbox切页，仍未出现权限对话框，无遮罩，仅空通知。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 工具箱页：英文“清理加速/应用卸载/游戏加速/安全隐私”，含快速卸载无用应用与提升游戏体验说明；点击Home返回主页，无权限框。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 重新进入主页清理面板：内存45%、存储7%、垃圾文件及加速/杀毒入口；本步尝试重启应用触发onResume，权限框仍未见，无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 仍为主页清理面板，显示内存/存储占比与垃圾清理、加速、杀毒入口；按系统Home退后台，未弹权限框、无遮罩，通知为空。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 系统桌面/应用列表：英文“应用列表、搜索、语音搜索”等；目标应用无可见界面，静态跳转尝试进入guildPermission权限页但未显示，通知为空。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 系统桌面/应用列表：显示应用列表与搜索等系统入口；静态跳转尝试进入WorkManager电池约束代理组件，未见应用权限框或遮罩，通知为空。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 系统桌面/应用列表：仍为应用列表、搜索等系统界面；静态跳转指向安全锁WatchmenReceiver接收器，未展示应用页面/权限框，无遮罩，通知为空。 | `step_08_screen.png` |

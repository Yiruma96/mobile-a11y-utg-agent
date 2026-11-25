# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:45:55
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`dt.ram.cleaner.speed.booster`（静态标签：`malicious` / `GhostClicker` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 7 | 88 / 否 | `click` → [7] Button text="Continue" id=continue_button (click) c | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `dt.ram.cleaner.speed.booster` / `MainActivity` | `-` | 3 | 142 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `dt.ram.cleaner.speed.booster` / `MainActivity` | `-` | 14 | 104 / 否 | `wait` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `dt.ram.cleaner.speed.booster` / `MainActivity` | `-` | 14 | 104 / 否 | `open` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `dt.ram.cleaner.speed.booster` / `MainActivity` | `-` | 14 | 104 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `dt.ram.cleaner.speed.booster` / `MainActivity` | `-` | 14 | 104 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `dt.ram.cleaner.speed.booster` / `MainActivity` | `-` | 14 | 104 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `dt.ram.cleaner.speed.booster` / `MainActivity` | `-` | 14 | 104 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Ram Cleaner to access` | `Phone` | `make and manage phone calls` | `Cancel` | `Continue`
- **Step 2 (`dt.ram.cleaner.speed.booster/MainActivity`)**: `Ram Cleaner` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`dt.ram.cleaner.speed.booster/MainActivity`)**: `RAM Cleaner` | `USED RAM :` | `-2920 MB` | `TOTAL RAM :` | `-1110 MB` | `FREE RAM :` | `1810 MB` | `Running Task : 1` | `Pixel Launcher` | `BOOST RAM`
- **Step 4 (`dt.ram.cleaner.speed.booster/MainActivity`)**: `RAM Cleaner` | `USED RAM :` | `-2920 MB` | `TOTAL RAM :` | `-1110 MB` | `FREE RAM :` | `1810 MB` | `Running Task : 1` | `Pixel Launcher` | `BOOST RAM`
- **Step 5 (`dt.ram.cleaner.speed.booster/MainActivity`)**: `RAM Cleaner` | `USED RAM :` | `-2920 MB` | `TOTAL RAM :` | `-1110 MB` | `FREE RAM :` | `1810 MB` | `Running Task : 1` | `Pixel Launcher` | `BOOST RAM`
- **Step 6 (`dt.ram.cleaner.speed.booster/MainActivity`)**: `RAM Cleaner` | `USED RAM :` | `-2920 MB` | `TOTAL RAM :` | `-1110 MB` | `FREE RAM :` | `1810 MB` | `Running Task : 1` | `Pixel Launcher` | `BOOST RAM`
- **Step 7 (`dt.ram.cleaner.speed.booster/MainActivity`)**: `RAM Cleaner` | `USED RAM :` | `-2920 MB` | `TOTAL RAM :` | `-1110 MB` | `FREE RAM :` | `1810 MB` | `Running Task : 1` | `Pixel Launcher` | `BOOST RAM`
- **Step 8 (`dt.ram.cleaner.speed.booster/MainActivity`)**: `RAM Cleaner` | `USED RAM :` | `-2920 MB` | `TOTAL RAM :` | `-1110 MB` | `FREE RAM :` | `1810 MB` | `Running Task : 1` | `Pixel Launcher` | `BOOST RAM`

## 中文逐页引导链路解读

> **全链路总结**：应用先请求电话权限并点 Continue 继续，进入 RAM Cleaner 主界面后显示异常负值内存；随后关闭旧版 Android 兼容性警告、等待/冷启动，并多次按静态引导跳转至 GMS/Firebase 接收器及桌面小部件，全程无通知横幅或遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 选择允许 Ram Cleaner 访问的内容（Step 1 权限页）
- 英文 -> 电话：拨打和管理电话（Step 1 权限页）
- 英文 -> 此应用针对旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者（Step 2 兼容性弹窗）
- 英文 -> RAM 清理器 / 已用内存 -2920MB / 总内存 -1110MB / 空闲内存 1810MB / 运行任务 1（Step 3-8 主界面）
- 英文 -> 加速内存 BOOST RAM（Step 3-8 主界面按钮）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | Step 1 系统权限页要求允许 Ram Cleaner 使用电话/拨打和管理电话；点 Continue 继续，有 Cancel，无通知遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | Step 2 主界面弹出旧版 Android 兼容性警告，称可能无法正常运行；点 OK 关闭，无通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | Step 3 为 Ram Cleaner 主界面，显示内存使用/总量为异常负值、空闲 1810MB、运行任务 1；本步仅等待，未现预期弹窗。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | Step 4 仍为 RAM 清理主界面，异常负值不变；未等到预期 AlertDialog 后执行冷启动/open，页面无可见变化。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | Step 5 仍停留 RAM 清理主界面；探针按静态引导跳转至 GMS AppMeasurementReceiver，界面无变化、无通知遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: MainActivity** | Step 6 继续停留主界面；探针按静态引导跳转至 GMS logs.b，异常内存数值与 BOOST RAM 按钮仍在，无通知遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: MainActivity** | Step 7 主界面未变；探针按静态引导跳转至 FirebaseInstanceIdReceiver，仍显示负值内存与 BOOST RAM，无通知横幅。 | `step_07_screen.png` |
| 8 | **Step 8: MainActivity** | Step 8 主界面保持原样；探针按静态引导跳转至 com.ram.cleanmaster.RamCleanerWidget，未触发可见交互或遮罩。 | `step_08_screen.png` |

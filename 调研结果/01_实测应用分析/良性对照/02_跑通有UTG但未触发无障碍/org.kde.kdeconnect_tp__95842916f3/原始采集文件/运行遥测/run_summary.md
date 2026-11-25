# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:30:05
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`org.kde.kdeconnect_tp`（静态标签：`benign` / `系统效率与通用辅助` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `org.kde.kdeconnect_tp` / `MainActivity` | `-` | 6 | 136 / 否 | `click` → [1] ImageButton desc="Open" (click) center=(77,171) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `org.kde.kdeconnect_tp` / `MainActivity` | `-` | 15 | 200 / 否 | `click` → [1] ImageButton desc="Close" (click) center=(77,171) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `org.kde.kdeconnect_tp` / `MainActivity` | `-` | 15 | 200 / 否 | `click` → [3] ImageView desc="More options" (click) center=(1024, | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `org.kde.kdeconnect_tp` / `MainActivity` | `-` | 6 | 136 / 否 | `wait` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `org.kde.kdeconnect_tp` / `MainActivity` | `-` | 6 | 136 / 否 | `click` → [1] ImageButton desc="Open" (click) center=(77,171) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `org.kde.kdeconnect_tp` / `MainActivity` | `-` | 15 | 200 / 否 | `click` → [12] LinearLayoutCompat (click) center=(452,713) | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `org.kde.kdeconnect_tp` / `MainActivity` | `-` | 25 | 446 / 否 | `system_button` → Back | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `org.kde.kdeconnect_tp` / `MainActivity` | `-` | 7 | 173 / 否 | `click` → [1] ImageButton desc="Open" (click) center=(77,171) | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`org.kde.kdeconnect_tp/MainActivity`)**: `Open` | `KDE Connect Devices` | `More options` | `Other devices running KDE Connect in your same network ` | `Connected devices` | `No devices`
- **Step 2 (`org.kde.kdeconnect_tp/MainActivity`)**: `Close` | `KDE Connect Devices` | `More options` | `Other devices running KDE Connect in your same network ` | `Connected devices` | `No devices` | `KDE Connect` | `sdk_gphone_x86_64` | `Devices` | `Pair new device`
- **Step 3 (`org.kde.kdeconnect_tp/MainActivity`)**: `Close` | `KDE Connect Devices` | `More options` | `Other devices running KDE Connect in your same network ` | `Connected devices` | `No devices` | `KDE Connect` | `sdk_gphone_x86_64` | `Devices` | `Pair new device`
- **Step 4 (`org.kde.kdeconnect_tp/MainActivity`)**: `Open` | `KDE Connect Devices` | `More options` | `Other devices running KDE Connect in your same network ` | `Connected devices` | `No devices`
- **Step 5 (`org.kde.kdeconnect_tp/MainActivity`)**: `Open` | `KDE Connect Devices` | `More options` | `Other devices running KDE Connect in your same network ` | `Connected devices` | `No devices`
- **Step 6 (`org.kde.kdeconnect_tp/MainActivity`)**: `Close` | `KDE Connect Devices` | `More options` | `Other devices running KDE Connect in your same network ` | `Connected devices` | `No devices` | `KDE Connect` | `sdk_gphone_x86_64` | `Devices` | `Pair new device`
- **Step 7 (`org.kde.kdeconnect_tp/MainActivity`)**: `Open` | `Settings` | `Device name` | `sdk_gphone_x86_64` | `Choose theme` | `System Default` | `Persistent notification` | `Tap to enable/disable in Notification settings` | `Trusted networks` | `Restrict autodiscovery to known networks`
- **Step 8 (`org.kde.kdeconnect_tp/MainActivity`)**: `Open` | `KDE Connect Devices` | `More options` | `You're not connected to a Wi-Fi network, so you may not` | `Connected devices` | `No devices`

## 中文逐页引导链路解读

> **全链路总结**：该应用为 KDE Connect 系统辅助工具，当前无已连接设备；轨迹在设备列表、侧栏、更多菜单、设置与 Wi-Fi 提示间切换，未出现授权/拒权弹窗，拒权结果未测试。核心特征是依赖同一局域网发现并配对设备，仅显示持久通知“未连接任何设备”，未见诱导性遮罩或话术。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “同一网络中的其他 KDE Connect 设备应显示在此处”（步骤1/4/5/8 主设备列表，非诱导说明）
- 英文 -> “您未连接 Wi-Fi，可能看不到任何设备，点击此处启用 Wi-Fi”（步骤8 主列表提示，非诱导说明）
- 英文 -> “将自动发现限制在已知网络”“点击以在通知设置中启用/禁用”（步骤7 设置页，非诱导说明）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主设备列表页，提示同网设备会显示于此，已连接设备为空；通知称未连接任何设备，无遮罩。点击“Open”开侧栏。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 侧栏展开页，含设备、配对新设备、设置、关于及本机名；通知仍为未连接任何设备，无遮罩。点击“Close”收起侧栏返回列表。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 侧栏仍展开；点击右上“More options”尝试打开溢出菜单，但页面无可见弹窗，通知仍称未连接设备，无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 等待菜单页，仍为主列表；提示同网设备显示于此，已连接为空；通知称未连接设备，无遮罩，溢出菜单未出现。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 主列表再次出现；英文提示同网设备将显示于此，已连接为空；通知未连接任何设备，无遮罩。点击“Open”再次打开侧栏以找设置。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 点击侧栏“Settings”后进入设置页，含设备名、主题、持久通知、可信网络、按IP添加设备及导出日志；通知未连接设备，无遮罩。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 仍为设置页，含可信网络、按IP添加设备、蓝牙测试与日志导出等项；通知未连接设备，无遮罩。按系统返回键回主设备列表。 | `step_07_action.png` |
| 8 | **Step 8: MainActivity** | 主列表提示未连 Wi-Fi 可能看不到设备，并引导点击启用；已连接为空；通知未连接设备，无遮罩。点击“Open”开侧栏。 | `step_08_action.png` |

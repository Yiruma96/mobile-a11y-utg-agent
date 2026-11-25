# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:17:13
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.earendel.tapbar`（静态标签：`benign` / `按键映射与手势导航` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.earendel.tapbar/com.earendel.tapbar.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Setup Tapbar / Accessibility service. Lets the tap zone sit directly on the status bar. It does not read or send any screen text.. Turn on / Display over other apps. Draws the tap zone below the status bar when the Accessibility service is not active.. Turn on / If the accessibility switch is greyed out: / Open App info, tap the three-dot menu at the top right, choose Allow restricted settings, then try again.`
- **Back 后 +5.5s**：`com.earendel.tapbar/com.earendel.tapbar.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Setup Tapbar / Accessibility service. Lets the tap zone sit directly on the status bar. It does not read or send any screen text.. Turn on / Display over other apps. Draws the tap zone below the status bar when the Accessibility service is not active.. Turn on / If the accessibility switch is greyed out: / Open App info, tap the three-dot menu at the top right, choose Allow restricted settings, then try again.`
- **Back 后 +10.5s**：`com.earendel.tapbar/com.earendel.tapbar.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Setup Tapbar / Accessibility service. Lets the tap zone sit directly on the status bar. It does not read or send any screen text.. Turn on / Display over other apps. Draws the tap zone below the status bar when the Accessibility service is not active.. Turn on / If the accessibility switch is greyed out: / Open App info, tap the three-dot menu at the top right, choose Allow restricted settings, then try again.`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.earendel.tapbar` / `MainActivity` | `-` | 38 | 84 / 否 | `click` → [37] View (click) center=(907,2120) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.earendel.tapbar` / `MainActivity` | `-` | 12 | 443 / 否 | `click` → [540, 683] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.earendel.tapbar/MainActivity`)**: `Choose language` | `English` | `Português` | `Русский` | `中文` | `Français` | `Deutsch` | `हिन्दी` | `日本語` | `한국어`
- **Step 2 (`com.earendel.tapbar/MainActivity`)**: `Setup Tapbar` | `Accessibility service. Lets the tap zone sit directly o` | `Display over other apps. Draws the tap zone below the s` | `If the accessibility switch is greyed out:` | `Open App info, tap the three-dot menu at the top right,` | `Open app info` | `View visual guide` | `Skip for now`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Tapbar` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用从语言选择进入设置引导，要求无障碍服务与悬浮窗权限，并跳转系统无障碍列表；在服务详情页触发系统“完全控制”警告，点Deny后返回原引导页并保持可用，表现为拒权后优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “无障碍服务让点击区覆盖状态栏，不读取或发送任何屏幕文字”（Step 2/拒权返回页）
- 英语 -> “悬浮窗权限用于无障碍未启用时在状态栏下方绘制点击区”（Step 2/拒权返回页）
- 英语 -> “若无障碍开关灰置，去应用信息三点菜单开启允许受限设置后再试”（Step 2/拒权返回页）
- 英语 -> “Tapbar快捷方式可在状态栏放置小点击目标，不读取屏幕内容”（服务详情页）
- 英语 -> 系统警告：“允许Tapbar完全控制设备？可查看并控制屏幕、代你操作应用”（系统警告弹窗，非应用自述）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 语言选择首页，列英语、葡语、俄语、中文等12种语言；英语已选中，点底部“Next”进入设置引导。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 权限引导页，两卡片要求无障碍与悬浮窗；文案称仅覆盖状态栏、不读写屏幕文字；点无障碍“Turn on”跳系统设置。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表，DOWNLOADED APPS下Tapbar显示Off；本步采集无障碍设置钩子与探针后自动终止，未开启开关。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停留系统无障碍列表；无弹窗、无通知横幅、遮罩数0，页面无新增文本。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针，仍在系统无障碍列表；无通知、无悬浮遮罩（overlays=0），未出现额外授权弹窗。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | Tapbar服务详情页，有“Use Tapbar”开关及“Tapbar shortcut”选项；说明称只在状态栏放小点击目标、不读屏幕内容。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统高危警告弹窗，称将允许Tapbar完全控制设备，可查看/控制屏幕并代操作；含Allow与Deny，本步仅检查未点允许。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 点Deny拒权后2秒返回设置引导页；无障碍与悬浮窗仍未开启，页面保留Skip for now，未见崩溃或强制跳转。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权后10.5秒仍停在设置引导页；权限未授予，应用保持原页可继续或跳过，表现为优雅停留/降级。 | `step_03_refusal_10500ms_screen.png` |

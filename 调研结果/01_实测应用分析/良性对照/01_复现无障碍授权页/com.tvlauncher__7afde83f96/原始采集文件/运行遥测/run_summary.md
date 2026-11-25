# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:32:52
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.tvlauncher`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.tvlauncher/com.tvlauncher.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Settings & About / TV Launcher / v1.6.2 (FOSS) / Fast, lightweight, minimal RAM launcher / Settings`
- **Back 后 +5.5s**：`com.tvlauncher/com.tvlauncher.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Settings & About / TV Launcher / v1.6.2 (FOSS) / Fast, lightweight, minimal RAM launcher / Settings`
- **Back 后 +10.5s**：`com.tvlauncher/com.tvlauncher.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Settings & About / TV Launcher / v1.6.2 (FOSS) / Fast, lightweight, minimal RAM launcher / Settings`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.tvlauncher` / `MainActivity` | `-` | 9 | 79 / 否 | `click` → [8] LinearLayout id=aboutButton (click) center=(1894,99 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.tvlauncher` / `MainActivity` | `-` | 14 | 229 / 否 | `click` → [9] Switch text="Override TV Default Launcher" id=homeO | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 210 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.tvlauncher/MainActivity`)**: `3:32 AM` | `Wednesday, November 25` | `Wallpaper Settings` | `Settings` | `+` | `Add App` | `About & Settings`
- **Step 2 (`com.tvlauncher/MainActivity`)**: `Settings & About` | `TV Launcher` | `v1.6.2 (FOSS)` | `Fast, lightweight, minimal RAM launcher` | `Settings` | `Override TV Default Launcher` | `Intercepts TV Home key on devices that lock the default` | `Kill Stock Launcher Background RAM` | `CLOSE` | `OPEN GITHUB`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `TV Launcher` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以极简电视桌面为入口，先打开“About & Settings”，再拨动“Override TV Default Launcher”，跳转系统无障碍并进入服务详情；点授权触发全控警告，拒权后返回设置弹窗并停留在该诱导页（TRAPPED_ON_LURE_SCREEN）。整体以桌面增强为由引导开启无障碍/全控权限，拒权后流程被困。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文「Override TV Default Launcher」-> 覆盖电视默认桌面（关于设置页）
- 英文「Intercepts TV Home key on devices that lock the default launcher」-> 在锁定默认桌面的设备上拦截电视Home键（关于设置页）
- 英文「Kill Stock Launcher Background RAM」-> 杀掉原厂桌面后台内存（关于设置页）
- 英文「Use TV Launcher」「TV Launcher shortcut」及检测Home键说明 -> 允许TV Launcher检测电视遥控Home键并返回桌面（服务详情页）
- 英文「Allow TV Launcher to have full control of your device?」-> 允许TV Launcher完全控制设备（系统警告弹窗）
- 英文「View and control screen」「View and perform actions」-> 可查看控制屏幕、读取屏幕全部内容、悬浮显示并代为操作（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主桌面显示时间、日期和壁纸/设置入口，本步点击“About & Settings”打开设置弹窗。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 关于设置弹窗展示TV Launcher版本及“覆盖默认桌面、拦截Home键、杀原厂后台”等项；本步拨动覆盖开关。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 跳转系统无障碍页，下载应用列表出现TV Launcher且为Off；探针记录无障碍设置钩子后自动停止，无通知/遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 无障碍页跳后0.8秒探针：界面无可见文本、无通知、遮罩为0，等待未出现新弹窗。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 无障碍页跳后2.0秒探针：仍无可见文本、无通知、遮罩为0，等待结束无新增交互。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | TV Launcher无障碍服务详情：说明可检测电视遥控Home键并返回桌面，含“Use TV Launcher”和快捷方式开关。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统全控警告弹窗：称可查看控制屏幕、读取全部内容、悬浮显示并代为操作；本步仅检查，不点Allow/Deny。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权后2秒回到“Settings & About”弹窗，仍显示覆盖/杀后台选项，停留在诱导页且无取消退出路径。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权后10.5秒仍停留在同一“Settings & About”弹窗，覆盖与杀后台选项未变，持续困在诱导页。 | `step_03_refusal_10500ms_screen.png` |

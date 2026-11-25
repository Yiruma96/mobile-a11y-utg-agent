# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:05:13
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.jarsilio.android.waveup`（静态标签：`benign` / `按键映射与手势导航` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `12` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 8 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_08_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.jarsilio.android.waveup/com.jarsilio.android.waveup.MainActivity` | hooks=`[]` | overlays=`0` | texts=`WaveUp / More options / Service / Enable / WaveUp modes`
- **Back 后 +5.5s**：`com.jarsilio.android.waveup/com.jarsilio.android.waveup.MainActivity` | hooks=`[]` | overlays=`0` | texts=`WaveUp / More options / Service / Enable / WaveUp modes`
- **Back 后 +10.5s**：`com.jarsilio.android.waveup/com.jarsilio.android.waveup.MainActivity` | hooks=`[]` | overlays=`0` | texts=`WaveUp / More options / Service / Enable / WaveUp modes`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.jarsilio.android.waveup` / `MainActivity` | `-` | 28 | 545 / 否 | `click` → [24] Switch id=switchWidget (unchecked) center=(970,180 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.jarsilio.android.waveup` / `MainActivity` | `-` | 28 | 545 / 否 | `click` → [21] LinearLayout (click) center=(540,1806) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.jarsilio.android.waveup` / `MainActivity` | `-` | 28 | 545 / 否 | `click` → [7] Switch id=switchWidget (unchecked) center=(970,451) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.jarsilio.android.waveup` / `MainActivity` | `-` | 3 | 430 / 否 | `click` → [2] Button text="IGNORE" id=button2 (click) center=(603 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.jarsilio.android.waveup` / `MainActivity` | `-` | 3 | 379 / 否 | `click` → [2] Button text="IGNORE" id=button2 (click) center=(603 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.jarsilio.android.waveup` / `MainActivity` | `-` | 28 | 545 / 否 | `click` → [24] Switch id=switchWidget (unchecked) center=(970,180 | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.jarsilio.android.waveup` / `MainActivity` | `-` | 3 | 768 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(876,171 | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.jarsilio.android.waveup/MainActivity`)**: `WaveUp` | `More options` | `Service` | `Enable` | `WaveUp modes` | `Wave mode` | `Turn on screen when you wave over the proximity sensor.` | `Number of waves` | `Number of times you have to wave over the proximity sen` | `Pocket mode`
- **Step 2 (`com.jarsilio.android.waveup/MainActivity`)**: `WaveUp` | `More options` | `Service` | `Enable` | `WaveUp modes` | `Wave mode` | `Turn on screen when you wave over the proximity sensor.` | `Number of waves` | `Number of times you have to wave over the proximity sen` | `Pocket mode`
- **Step 3 (`com.jarsilio.android.waveup/MainActivity`)**: `WaveUp` | `More options` | `Service` | `Enable` | `WaveUp modes` | `Wave mode` | `Turn on screen when you wave over the proximity sensor.` | `Number of waves` | `Number of times you have to wave over the proximity sen` | `Pocket mode`
- **Step 4 (`com.jarsilio.android.waveup/MainActivity`)**: `Phone Permission  WaveUp uses this permission exclusive` | `IGNORE` | `REQUEST`
- **Step 5 (`com.jarsilio.android.waveup/MainActivity`)**: `Bluetooth Permission   WaveUp requests access to your B` | `IGNORE` | `REQUEST`
- **Step 6 (`com.jarsilio.android.waveup/MainActivity`)**: `WaveUp` | `More options` | `Service` | `Enable` | `WaveUp modes` | `Wave mode` | `Turn on screen when you wave over the proximity sensor.` | `Number of waves` | `Number of times you have to wave over the proximity sen` | `Pocket mode`
- **Step 7 (`com.jarsilio.android.waveup/MainActivity`)**: `Lock device: Accessibility Service   In order to lock t` | `CANCEL` | `OK`
- **Step 8 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `WaveUp` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用从主界面引导开启服务与锁屏，依次弹出可忽略的手机/蓝牙权限说明，再以无障碍说明引导进入系统无障碍设置；系统警告页拒绝授权后回到主界面并停留在引导页，运行通知常驻，形成拒权陷阱态。整体话术较透明且允许拒绝，但拒权后的停留/回退路径是主要风险点。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 「Turn on screen when you wave over the proximity sensor.」中文意译：挥手经过距离传感器时点亮屏幕。（主界面 Wave mode 说明）
- English -> 「Turn off and lock screen when the proximity sensor is covered.」中文意译：遮挡距离传感器时关闭并锁定屏幕。（主界面 Lock screen 说明）
- English -> 手机权限弹窗称仅用于判断是否正在通话以便通话时停用，不查询/存储通话信息，也不会拨打电话。（手机权限弹窗）
- English -> 蓝牙权限弹窗称仅用于判断通话时是否连接蓝牙耳机，不作他用。（蓝牙权限弹窗）
- English -> 无障碍说明称锁屏需将 WaveUp 设为无障碍服务，并提醒该权限可监视用户，但声称使用锁屏全局动作且开源可查。（无障碍说明弹窗）
- English -> 「Allow WaveUp to have full control of your device?」中文意译：允许 WaveUp 完全控制你的设备？并说明可查看/控制屏幕与代操作应用。（系统无障碍警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面 WaveUp：显示服务、挥手唤醒、口袋模式及锁屏开关；本步点击未勾选的 Lock screen 开关，试图触发无障碍说明。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 仍在主界面；因开关点击未生效，改点 Lock screen 整行容器，想弹出无障碍授权说明；通知栏尚无常驻通知。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 主界面同页：锁屏行呈灰色不可用，改为先点顶部服务区未勾选的 Enable 开关，以启用 WaveUp 主服务。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 手机权限说明弹窗：称仅用于识别通话状态并在通话时暂停，不查询/存储通话信息；本步点 IGNORE 忽略，未授权。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 蓝牙权限说明弹窗：称仅判断通话时是否连接耳机，不作他用；本步点 IGNORE 忽略该可选权限。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 返回主界面，服务已启用并出现 WaveUp is running 常驻通知；本步再次点未勾选的 Lock screen 开关，准备触发无障碍说明。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 无障碍说明弹窗：标题意为锁屏需无障碍服务，正文提醒该权限可监视用户；本步点 OK 继续，进入系统设置。 | `step_07_action.png` |
| 8 | **Step 8: [无障碍列表页]** | 系统无障碍列表页：下载应用下 WaveUp 显示 Off；抓取到无障碍设置钩子后自动终止，未点开应用，常驻通知仍在。 | `step_08_screen.png` |
| 9 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在系统无障碍列表，未捕获任何 UI 文本；遮罩数为0，WaveUp 运行通知常驻。 | `step_08_probe_800ms_screen.png` |
| 10 | **跳后探针 +2.0s** | 跳转后2.0秒探针：页面仍为系统无障碍列表且无文本内容；无遮罩，WaveUp 运行通知保持常驻。 | `step_08_probe_2000ms_screen.png` |
| 11 | **服务详情页** | 无障碍服务详情页：显示 WaveUp、Use WaveUp、选项及 WaveUp shortcut 为 Off；说明为 No description provided，本步仅查看详情。 | `step_08_service_detail_screen.png` |
| 12 | **系统警告弹窗(点Deny)** | 系统警告弹窗：询问是否允许 WaveUp 完全控制设备，列明可查看/控制屏幕与代操作；本页拒绝 Deny，未授权。 | `step_08_system_warning_screen.png` |
| 13 | **拒权返回 +2.0s** | 拒权后2秒回到 WaveUp 主界面，仅露出服务/挥手/口袋等上半屏；系统判定停在诱导页，运行通知仍在，未恢复原流程。 | `step_08_refusal_2000ms_screen.png` |
| 14 | **拒权返回 +10.5s** | 拒权后10.5秒仍停在 WaveUp 主界面同区域，未出现下一步或退出引导；判定为困在诱导页，WaveUp 运行通知持续常驻。 | `step_08_refusal_10500ms_screen.png` |

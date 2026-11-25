# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:39:35
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.zfdang.touchhelper`（静态标签：`benign` / `自动化与跳广告` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.zfdang.touchhelper/com.zfdang.touchhelper.MainActivity` | hooks=`[]` | overlays=`0` | texts=`状态 / "开屏跳过"基于安卓系统的无障碍服务来实现跳过自动广告功能，开源不联网，绝对安全！为保证程序能正常工作，请检查以下设置： / 1. 在"无障碍"设置里，打开"开屏跳过 - 无障碍服务"。 / 2. 在"电池优化"设置里，设置"开屏跳过"为"不优化"。 / 3. 在电池管理里，设置"开屏跳过"为"允许后台耗电"。设置方法因品牌不同有所差异，比如VIVO系统为："设置" -> "电池" -> "后台耗电管理"。`
- **Back 后 +5.5s**：`com.zfdang.touchhelper/com.zfdang.touchhelper.MainActivity` | hooks=`[]` | overlays=`0` | texts=`状态 / "开屏跳过"基于安卓系统的无障碍服务来实现跳过自动广告功能，开源不联网，绝对安全！为保证程序能正常工作，请检查以下设置： / 1. 在"无障碍"设置里，打开"开屏跳过 - 无障碍服务"。 / 2. 在"电池优化"设置里，设置"开屏跳过"为"不优化"。 / 3. 在电池管理里，设置"开屏跳过"为"允许后台耗电"。设置方法因品牌不同有所差异，比如VIVO系统为："设置" -> "电池" -> "后台耗电管理"。`
- **Back 后 +10.5s**：`com.zfdang.touchhelper/com.zfdang.touchhelper.MainActivity` | hooks=`[]` | overlays=`0` | texts=`状态 / "开屏跳过"基于安卓系统的无障碍服务来实现跳过自动广告功能，开源不联网，绝对安全！为保证程序能正常工作，请检查以下设置： / 1. 在"无障碍"设置里，打开"开屏跳过 - 无障碍服务"。 / 2. 在"电池优化"设置里，设置"开屏跳过"为"不优化"。 / 3. 在电池管理里，设置"开屏跳过"为"允许后台耗电"。设置方法因品牌不同有所差异，比如VIVO系统为："设置" -> "电池" -> "后台耗电管理"。`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.zfdang.touchhelper` / `MainActivity` | `-` | 16 | 271 / 否 | `click` → [4] ImageButton id=button_accessibility_permission (cli | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.zfdang.touchhelper` / `MainActivity` | `-` | 4 | 269 / 否 | `click` → [4] Button text="同意并前往设置" id=button1 (click) center=(80 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 209 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.zfdang.touchhelper/MainActivity`)**: `状态` | `"开屏跳过"基于安卓系统的无障碍服务来实现跳过自动广告功能，开源不联网，绝对安全！为保证程序能正常工作，请检查` | `1. 在"无障碍"设置里，打开"开屏跳过 - 无障碍服务"。` | `2. 在"电池优化"设置里，设置"开屏跳过"为"不优化"。` | `3. 在电池管理里，设置"开屏跳过"为"允许后台耗电"。设置方法因品牌不同有所差异，比如VIVO系统为："设置` | `4. 在"任务管理"里，锁定"开屏跳过"。` | `更多信息，请访问网址:` | `https://touchhelper.zfdang.com/enable` | `设置` | `关于`
- **Step 2 (`com.zfdang.touchhelper/MainActivity`)**: `开启无障碍服务前请了解` | `"开屏跳过"通过安卓无障碍服务读取当前屏幕上的界面内容（控件文字、描述和位置），用于识别并自动点击开屏广告的"` | `取消` | `同意并前往设置`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `开屏跳过-无障碍服务` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用入口主界面以“开源不联网、绝对安全”安抚用户，并要求开启无障碍、电池不优化、后台耗电和任务锁定；点击权限后先展示本机数据处理说明，同意即跳系统无障碍列表并进入服务详情，在系统“完全控制”警告处被拒绝后返回主界面并优雅降级停留，无通知、无遮罩、无崩溃。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 中文 -> “开源不联网，绝对安全”，并称为保证正常工作需开启无障碍、电池不优化、允许后台耗电及锁定任务（主界面/拒权返回页）
- 中文 -> 无障碍服务读取屏幕控件文字、描述和位置以识别并点击开屏广告“跳过”，称仅本机内存即时比对、不保存、不联网不上传（授权说明弹窗）
- 中文 -> 添加程序跳过方法会保存所选控件文字、描述和坐标，复制窗口控件会写入系统剪贴板，可在设置查看或删除（授权说明弹窗）
- English -> “Allow 开屏跳过-无障碍服务 to have full control of your device?”即允许其完全控制设备，并提示可查看控制屏幕、读取所有内容及代用户操作（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面要求检查四项设置：开无障碍、电池不优化、允许后台耗电、锁定任务；本步点无障碍权限按钮，无通知无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 授权前说明弹窗，中文解释仅本机识别“跳过”按钮、不保存不联网；本步点“同意并前往设置”跳系统无障碍。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表页，DOWNLOADED APPS 下见“开屏跳过-无障碍服务”为 Off；触发设置钩子后自动终止，无通知无遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针，仍停留在系统无障碍列表页，界面文本为空，overlays=0，无通知横幅或遮罩。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针，仍在系统无障碍列表页，界面文本为空，overlays=0，未见通知或悬浮层。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 服务详情页，含 Use 开屏跳过-无障碍服务、OPTIONS 与 Shortcut 为 Off；说明称开源、无网络权限、不收集上传。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统警告弹窗，英文提示允许后完全控制设备、查看控制屏幕并代操作，含 Allow/Deny；本步检查后选择拒绝。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒绝授权返回主界面 2 秒，仍显示四项设置说明与网址；应用未强制退出，状态为优雅停留或降级，无通知遮罩。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒绝授权返回主界面 10.5 秒，界面与之前一致，仍引导检查设置；无二次弹窗、无通知、无遮罩，保持降级停留。 | `step_03_refusal_10500ms_screen.png` |

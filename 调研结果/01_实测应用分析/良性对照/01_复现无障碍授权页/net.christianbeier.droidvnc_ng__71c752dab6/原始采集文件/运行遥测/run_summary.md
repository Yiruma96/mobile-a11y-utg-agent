# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:11:08
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`net.christianbeier.droidvnc_ng`（静态标签：`benign` / `远程协助与跨设备互联` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 5 步，UTG 唯一节点 `7` 个，有向边 `9` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 5 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_05_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`net.christianbeier.droidvnc_ng/net.christianbeier.droidvnc_ng.server.WriteStorageRequestActivity` | hooks=`[]` | overlays=`0` | texts=`File access disabled / To be able to transfer files to and from your device, you need to enable file access for droidVNC-NG. Please note that saving files will only be possible in the 'Download' and 'Documents' directories. Do you want to enable file access now? / NO / YES`
- **Back 后 +5.5s**：`net.christianbeier.droidvnc_ng/net.christianbeier.droidvnc_ng.server.WriteStorageRequestActivity` | hooks=`[]` | overlays=`0` | texts=`File access disabled / To be able to transfer files to and from your device, you need to enable file access for droidVNC-NG. Please note that saving files will only be possible in the 'Download' and 'Documents' directories. Do you want to enable file access now? / NO / YES`
- **Back 后 +10.5s**：`net.christianbeier.droidvnc_ng/net.christianbeier.droidvnc_ng.server.WriteStorageRequestActivity` | hooks=`[]` | overlays=`0` | texts=`File access disabled / To be able to transfer files to and from your device, you need to enable file access for droidVNC-NG. Please note that saving files will only be possible in the 'Download' and 'Documents' directories. Do you want to enable file access now? / NO / YES`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `net.christianbeier.droidvnc_ng` / `MainActivity` | `-` | 43 | 259 / 否 | `click` → [43] TextView text="DENIED" id=permission_status_input  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `net.christianbeier.droidvnc_ng` / `MainActivity` | `-` | 43 | 259 / 否 | `swipe` → [540, 1900] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `net.christianbeier.droidvnc_ng` / `MainActivity` | `-` | 35 | 574 / 否 | `click` → [33] Button text="START" id=toggle (click) center=(540, | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `net.christianbeier.droidvnc_ng` / `InputRequestActivity` | `-` | 4 | 196 / 否 | `click` → [4] Button text="YES" id=button1 (click) center=(887,13 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 210 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_05_layout.xml` + `step_05_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`net.christianbeier.droidvnc_ng/MainActivity`)**: `droidVNC-NG Admin Panel` | `Settings` | `Interface` | `:` | `Any` | `Port` | `5900` | `Password` | `Intent API Access Key` | `••••••••••••••••••••••••••••••••`
- **Step 2 (`net.christianbeier.droidvnc_ng/MainActivity`)**: `droidVNC-NG Admin Panel` | `Settings` | `Interface` | `:` | `Any` | `Port` | `5900` | `Password` | `Intent API Access Key` | `••••••••••••••••••••••••••••••••`
- **Step 3 (`net.christianbeier.droidvnc_ng/MainActivity`)**: `droidVNC-NG Admin Panel` | `Start Delay (s)` | `:` | `0` | `File Transfer` | `Scaling` | `View Only` | `Mouse Cursors` | `Keyboard Shortcuts` | `CONFIGURE`
- **Step 4 (`net.christianbeier.droidvnc_ng/InputRequestActivity`)**: `Accessibility disabled` | `To be able to remotely control your device and to enabl` | `NO` | `YES`
- **Step 5 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `droidVNC-NG` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用入口为droidVNC-NG管理员面板，先引导启动VNC服务，再以“无障碍禁用”弹窗请求远程控制所需无障碍；进入系统全控制警告后若拒绝，返回应用又反复弹出文件访问授权诱导，呈现拒权后重启诱导弹窗特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “无障碍已禁用；为远程控制设备并支持开机启动，需为droidVNC-NG启用无障碍，是否现在启用？”（InputRequestActivity）
- 英语 -> “允许droidVNC-NG向Android投递输入事件，从而由VNC查看器远程控制；输入不记录、不保存、不共享。”（无障碍服务详情页）
- 英语 -> “允许droidVNC-NG完全控制设备？适合无障碍需求，不适合多数应用；可查看控制屏幕、读取全部内容并覆盖显示，跟踪交互并代为操作。”（系统警告弹窗）
- 英语 -> “文件访问已禁用；为在设备间传输文件，需启用文件访问，仅能在Download和Documents保存，是否现在启用？”（WriteStorageRequestActivity）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 应用主界面为droidVNC-NG管理员面板，含端口5900、密码、Intent密钥与开机启动；点击Input权限状态DENIED。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 仍停留管理员面板；上一步点击未生效，本步向上滑动以寻找START按钮与权限仪表盘。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 下滑后露出START与权限仪表盘，屏幕捕获、输入仍为DENIED；点击START尝试启动VNC服务。 | `step_03_action.png` |
| 4 | **Step 4: InputRequestActivity** | 应用内弹窗称无障碍未启用，远程控制和开机启动需启用无障碍，询问是否现在开启；点击YES。 | `step_04_action.png` |
| 5 | **Step 5: [无障碍列表页]** | 跳至系统无障碍列表，droidVNC-NG显示Off；探针捕获无障碍设置入口后自动终止，无悬浮遮罩。 | `step_05_screen.png` |
| 6 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍处系统无障碍列表，界面无文本、无悬浮遮罩，仅见droidVNC-NG通知留存。 | `step_05_probe_800ms_screen.png` |
| 7 | **跳后探针 +2.0s** | 跳转后2.0秒探针：页面仍为系统无障碍列表，无遮罩与新增界面；应用通知持续留存。 | `step_05_probe_2000ms_screen.png` |
| 8 | **服务详情页** | droidVNC-NG无障碍服务详情页，开关为Off；说明称可向Android投递输入事件实现远程控制且不记录共享输入。 | `step_05_service_detail_screen.png` |
| 9 | **系统警告弹窗(点Deny)** | 系统全控制警告弹窗：称可查看控制屏幕、读取全部内容并覆盖显示，跟踪交互并代为操作；含Allow/Deny。 | `step_05_system_warning_screen.png` |
| 10 | **拒权返回 +2.0s** | 拒绝无障碍后约2秒回到应用，立即重启文件访问诱导弹窗，称传输文件需授权，仅限Download/Documents。 | `step_05_refusal_2000ms_screen.png` |
| 11 | **拒权返回 +10.5s** | 拒权返回约10.5秒仍重复弹出文件访问诱导，文案同上，呈现拒权后反复重启弹窗的粘性行为。 | `step_05_refusal_10500ms_screen.png` |

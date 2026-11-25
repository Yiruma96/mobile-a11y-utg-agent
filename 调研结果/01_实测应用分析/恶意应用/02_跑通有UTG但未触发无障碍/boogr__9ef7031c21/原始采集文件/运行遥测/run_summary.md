# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:00:11
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.system.android.sikhnet`（静态标签：`malicious` / `boogr` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 328 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.system.android.sikhnet` / `MainActivity` | `-` | 3 | 139 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.system.android.sikhnet` / `MainActivity` | `-` | 1 | 0 / 是 | `wait` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.system.android.sikhnet` / `MainActivity` | `-` | 1 | 0 / 是 | `click` → [1] WebView id=webview (click) center=(540,1046) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.system.android.sikhnet` / `MainActivity` | `-` | 1 | 0 / 是 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.system.android.sikhnet` / `MainActivity` | `-` | 1 | 0 / 是 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.system.android.sikhnet` / `MainActivity` | `-` | 1 | 0 / 是 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.system.android.sikhnet` / `MainActivity` | `-` | 1 | 0 / 是 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Sikh Net to access` | `SMS` | `send and view SMS messages` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Call logs` | `read and write phone call log` | `Phone`
- **Step 2 (`com.system.android.sikhnet/MainActivity`)**: `Sikh Net` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.system.android.sikhnet/MainActivity`)**: (空文本)
- **Step 4 (`com.system.android.sikhnet/MainActivity`)**: (空文本)
- **Step 5 (`com.system.android.sikhnet/MainActivity`)**: (空文本)
- **Step 6 (`com.system.android.sikhnet/MainActivity`)**: (空文本)
- **Step 7 (`com.system.android.sikhnet/MainActivity`)**: (空文本)
- **Step 8 (`com.system.android.sikhnet/MainActivity`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：该应用先经系统权限审查页集中索要短信、联系人、通话记录、电话、麦克风、位置与文件权限，进入后仅显示旧版兼容性警告和空白 WebView；随后通过静态引导连续跳转至 fourre、PhonecallReceiver、fivere、twenty 等隐藏组件，未做拒权验证（not_tested）。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English: “Choose what to allow Sikh Net to access” -> “选择允许 Sikh Net 访问哪些内容”（Step 1 ReviewPermissionsActivity）
- English: “send and view SMS messages” -> “发送和查看短信”（Step 1 权限审查页）
- English: “access photos, media, and files on your device” -> “访问设备上的照片、媒体和文件”（Step 1 权限审查页）
- English: “access your contacts” -> “访问你的联系人”（Step 1 权限审查页）
- English: “read and write phone call log” -> “读取和写入通话记录”（Step 1 权限审查页）
- English: “make and manage phone calls” -> “拨打和管理电话”（Step 1 权限审查页）
- English: “record audio” -> “录制音频”（Step 1 权限审查页）
- English: “This app was built for an older version of Android and may not work properly. Try checking for updates, or contact the developer.” -> “此应用针对旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者”（Step 2 MainActivity 兼容性警告）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审查页，提示允许 Sikh Net 访问短信、联系人、通话记录、电话、麦克风、位置和文件；本步点击 Continue 进入。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 应用主界面弹出旧版 Android 兼容性警告，称可能无法正常运行，建议检查更新或联系开发者；本步点“OK”关闭警告。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 进入主界面后 WebView 空白，无可见文字、通知或遮罩；本步等待加载或重定向，页面仍无内容。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 仍在空白 WebView 主界面，无任何可见文案或通知；本步点击 WebView 中心探测隐藏交互或跳转，未见变化。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 主界面无可见 UI；发生静态引导跳转至组件 .four.fourre，疑似隐藏业务页，未产生通知或遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: MainActivity** | 仍无可见界面；静态引导跳转至 .seven.PhonecallReceiver，组件名指向电话状态接收器，推测后台监听来电。 | `step_06_screen.png` |
| 7 | **Step 7: MainActivity** | 主界面空白无文案；静态引导跳转至 .five.fivere，属隐藏或后续组件，无通知横幅或覆盖层。 | `step_07_screen.png` |
| 8 | **Step 8: MainActivity** | 仍无可见 UI；静态引导跳转至 .twenty.twenty，疑似隐藏功能页或后台组件，未出现通知或遮罩。 | `step_08_screen.png` |

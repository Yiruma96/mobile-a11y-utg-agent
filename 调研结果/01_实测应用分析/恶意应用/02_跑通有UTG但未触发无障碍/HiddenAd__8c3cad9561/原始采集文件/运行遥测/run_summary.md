# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:49:21
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.sstfsk.cleanmaster`（静态标签：`malicious` / `HiddenAd` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 23 | 269 / 否 | `click` → [23] Button text="Continue" id=continue_button (click)  | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.sstfsk.cleanmaster` / `PermissionProxyActivity` | `-` | 3 | 143 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.sstfsk.cleanmaster` / `PermissionProxyActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.sstfsk.cleanmaster` / `PermissionProxyActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.sstfsk.cleanmaster` / `PermissionProxyActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Clean Master to access` | `Location` | `access this device's location` | `Phone` | `make and manage phone calls` | `Camera` | `take pictures and record video` | `Files and media` | `access photos, media, and files on your device` | `Physical activity`
- **Step 5 (`com.sstfsk.cleanmaster/PermissionProxyActivity`)**: `Clean Master` | `This app was built for an older version of Android and ` | `OK`
- **Step 6 (`com.sstfsk.cleanmaster/PermissionProxyActivity`)**: (空文本)
- **Step 7 (`com.sstfsk.cleanmaster/PermissionProxyActivity`)**: (空文本)
- **Step 8 (`com.sstfsk.cleanmaster/PermissionProxyActivity`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：该应用从桌面多次尝试启动目标包但未展示主界面，随后静态跳转拉起权限代理页，并借系统权限复核页诱导点击“继续”放行定位、电话、相机、文件和身体活动等敏感权限；之后仅以旧版Android兼容提示过渡，点击“OK”后连续静态跳转至UsageProxyActivity、BoostEventReceiver、ShkReceiver等隐藏组件，呈现HiddenAd规避审核特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “选择允许 Clean Master 访问的内容”（Step 4 系统权限复核页）
- 英语 -> “此应用针对旧版 Android 构建，可能无法正常工作；请尝试检查更新或联系开发者”（Step 5 兼容性警告弹窗）
- 英语 -> 应用名“Clean Master”借用知名清理工具品牌，易让用户误认为是正规清理软件（Step 4/5等页面）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面应用列表页，显示Apps list、Messages、Chrome、搜索等；无通知/遮罩，本步尝试打开目标应用但仍停留桌面。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为桌面应用列表页，Apps list、Chrome、搜索等可见；无通知与遮罩，再次按包名启动目标应用仍未进入应用界面。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面应用列表页无目标应用界面，无通知/遮罩；探针执行静态跳转，指令指向PermissionProxyActivity权限代理页。 | `step_03_screen.png` |
| 4 | **Step 4: ReviewPermissionsActivity** | 系统权限复核页，提示选择允许Clean Master访问定位、电话、相机、文件媒体、身体活动；有取消/继续，无遮罩，点击“继续”。 | `step_04_action.png` |
| 5 | **Step 5: PermissionProxyActivity** | 应用内兼容性警告弹窗，提示此应用针对旧版Android构建、可能工作异常并建议检查更新；仅“OK”按钮，无通知/遮罩，点击关闭。 | `step_05_action.png` |
| 6 | **Step 6: PermissionProxyActivity** | PermissionProxyActivity空白页，无可见文字、通知横幅或遮罩；探针执行静态跳转至UsageProxyActivity使用情况代理页。 | `step_06_screen.png` |
| 7 | **Step 7: PermissionProxyActivity** | PermissionProxyActivity仍为空白页，无文字、通知与遮罩；探针继续静态跳转至BoostEventReceiver，疑为加速/广告事件接收组件。 | `step_07_screen.png` |
| 8 | **Step 8: PermissionProxyActivity** | PermissionProxyActivity空白页，无可见内容、通知或遮罩；探针静态跳转至ShkReceiver，链路进入隐藏接收器，未见用户可操作界面。 | `step_08_screen.png` |

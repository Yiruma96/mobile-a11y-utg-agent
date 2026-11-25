# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:42:27
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.services.ndtdq.swsloflgfkcj`（静态标签：`malicious` / `BoostClicker` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 15 | 188 / 否 | `click` → [15] Button text="Continue" id=continue_button (click)  | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.services.ndtdq.swsloflgfkcj` / `dibd` | `-` | 3 | 153 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.services.ndtdq.swsloflgfkcj` / `dibd` | `-` | 1 | 22 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.services.ndtdq.swsloflgfkcj` / `dibd` | `-` | 1 | 22 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.services.ndtdq.swsloflgfkcj` / `dibd` | `-` | 1 | 22 / 否 | `wait` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow SystemSecurityServices to access` | `Files and media` | `access photos, media, and files on your device` | `Phone` | `make and manage phone calls` | `Contacts` | `access your contacts` | `Cancel` | `Continue`
- **Step 5 (`com.services.ndtdq.swsloflgfkcj/dibd`)**: `SystemSecurityServices` | `This app was built for an older version of Android and ` | `OK`
- **Step 6 (`com.services.ndtdq.swsloflgfkcj/dibd`)**: `SystemSecurityServices`
- **Step 7 (`com.services.ndtdq.swsloflgfkcj/dibd`)**: `SystemSecurityServices`
- **Step 8 (`com.services.ndtdq.swsloflgfkcj/dibd`)**: `SystemSecurityServices`

## 中文逐页引导链路解读

> **全链路总结**：该应用未从桌面直接进入前台，而是先经启动器，再通过静态跳转拉起伪装成“SystemSecurityServices”的权限审查页，诱导用户授予文件和媒体、电话、联系人权限；点击继续后弹出旧版Android兼容警告，随后多次静态跳转并停在空白“系统安全服务”页等待。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许 SystemSecurityServices（系统安全服务）访问哪些内容”（Step 4 权限审查页）
- 英文 -> “文件和媒体：访问设备上的照片、媒体和文件”（Step 4 权限审查页）
- 英文 -> “电话：拨打和管理电话”（Step 4 权限审查页）
- 英文 -> “联系人：访问您的联系人”（Step 4 权限审查页）
- 英文 -> “此应用为旧版 Android 构建，可能无法正常运行，请检查更新或联系开发者”（Step 5 兼容性警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面应用列表页，显示Apps list、日期及Messages/Chrome/搜索；目标应用未在前台，本步为打开探针，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍在桌面应用列表页，界面同上；点击“Apps list”试图展开抽屉定位目标应用，页面未明显变化，无通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面应用列表页无变化；执行静态活动跳转至com.axl.mngp.dibd，为后续权限页或目标组件探针路径，无通知遮罩。 | `step_03_screen.png` |
| 4 | **Step 4: ReviewPermissionsActivity** | 系统权限审查页，标题称允许SystemSecurityServices访问文件媒体、电话、联系人；有取消/继续，本步点“Continue”继续。 | `step_04_action.png` |
| 5 | **Step 5: dibd** | 应用dibd页弹出旧版Android兼容警告，标题SystemSecurityServices；提示可能无法正常运行，本步点“OK”关闭，无通知遮罩。 | `step_05_action.png` |
| 6 | **Step 6: dibd** | SystemSecurityServices空白页；无可见内容，执行静态跳转至com.axl.mngp.lwwny，未见通知横幅或悬浮遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: dibd** | SystemSecurityServices空白页；无可见内容，执行静态跳转至com.services.AccService，未见通知横幅或悬浮遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: dibd** | 仍为SystemSecurityServices空白页；按静态指引等待无障碍或授权相关组件，页面无可见诱导文本、通知或遮罩。 | `step_08_action.png` |

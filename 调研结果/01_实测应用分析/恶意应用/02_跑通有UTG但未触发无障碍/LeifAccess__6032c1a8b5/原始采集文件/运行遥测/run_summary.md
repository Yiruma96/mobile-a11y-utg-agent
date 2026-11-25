# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:32:21
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.services.ibgpe.hflbsqqjrmlfej`（静态标签：`malicious` / `LeifAccess` / 静态可见性：`clear`）
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
| 5 | `com.services.ibgpe.hflbsqqjrmlfej` / `dibd` | `-` | 3 | 153 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.services.ibgpe.hflbsqqjrmlfej` / `dibd` | `-` | 1 | 22 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.services.ibgpe.hflbsqqjrmlfej` / `dibd` | `-` | 1 | 22 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.services.ibgpe.hflbsqqjrmlfej` / `dibd` | `-` | 1 | 22 / 否 | `wait` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow SystemSecurityServices to access` | `Files and media` | `access photos, media, and files on your device` | `Phone` | `make and manage phone calls` | `Contacts` | `access your contacts` | `Cancel` | `Continue`
- **Step 5 (`com.services.ibgpe.hflbsqqjrmlfej/dibd`)**: `SystemSecurityServices` | `This app was built for an older version of Android and ` | `OK`
- **Step 6 (`com.services.ibgpe.hflbsqqjrmlfej/dibd`)**: `SystemSecurityServices`
- **Step 7 (`com.services.ibgpe.hflbsqqjrmlfej/dibd`)**: `SystemSecurityServices`
- **Step 8 (`com.services.ibgpe.hflbsqqjrmlfej/dibd`)**: `SystemSecurityServices`

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面启动器入口进入，先弹出伪装为“SystemSecurityServices”的系统权限复核，请求文件媒体、电话和联系人权限；点击“继续”后进入目标应用，出现旧版 Android 兼容性提示，关闭后停留在空白页并多次静态跳转至其他组件。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> “系统安全服务”（权限复核页、应用页）：以系统安全组件名义冒充可信应用。
- English -> “选择允许系统安全服务访问的内容”（权限复核页）：诱导用户为伪装组件批量授权。
- English -> “文件和媒体：访问设备上的照片、媒体和文件”（权限复核页）：请求读取媒体与文件。
- English -> “电话：拨打和管理电话”（权限复核页）：请求电话相关权限。
- English -> “联系人：访问联系人”（权限复核页）：请求读取联系人。
- English -> “此应用针对旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者。”（应用弹窗）：以兼容性警告促使点击“确定”继续。
- English -> “确定”（应用弹窗）：关闭旧版兼容性提示，推动流程继续。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面启动器界面，含“应用列表”“信息”“Chrome”“搜索”“语音搜索”；本步仅启动目标包，未点击。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为桌面启动器；点击“应用列表”试图手动查找目标应用，界面未发生变化。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面启动器画面不变，探针以静态引导跳转回退到 com.axl.mngp.dibd，未显示应用界面。 | `step_03_screen.png` |
| 4 | **Step 4: ReviewPermissionsActivity** | 系统权限复核页，伪装名“SystemSecurityServices”请求文件媒体、电话、联系人权限；点击“继续”放行。 | `step_04_action.png` |
| 5 | **Step 5: dibd** | 应用内弹窗称“SystemSecurityServices”为旧版 Android 构建，可能无法正常运行；点击“确定”关闭。 | `step_05_action.png` |
| 6 | **Step 6: dibd** | 仅显示“SystemSecurityServices”标题的空白页；探针以静态引导跳转回退到 com.axl.mngp.lwwny。 | `step_06_screen.png` |
| 7 | **Step 7: dibd** | 仍是仅含“SystemSecurityServices”标题的空白页；探针再次静态引导跳转至 com.services.AccService。 | `step_07_screen.png` |
| 8 | **Step 8: dibd** | 同一空白“SystemSecurityServices”页停留等待加载，未出现通知横幅或遮罩，也无可见授权按钮。 | `step_08_action.png` |

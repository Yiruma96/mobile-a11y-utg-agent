# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:01:38
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.android.boxa`（静态标签：`malicious` / `hiddad` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 37 | 334 / 否 | `click` → [37] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.boxa` / `MainActivity` | `-` | 37 | 334 / 否 | `click` → [37] Button text="Continue" id=continue_button (click)  | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.boxa` / `MainActivity` | `-` | 3 | 145 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.boxa` / `MainActivity` | `-` | 3 | 145 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.boxa` / `MainActivity` | `-` | 3 | 145 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.boxa` / `MainActivity` | `-` | 3 | 145 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.boxa` / `MainActivity` | `-` | 3 | 145 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.boxa` / `MainActivity` | `-` | 3 | 145 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow backup service to access` | `Files and media` | `access photos, media, and files on your device` | `Phone` | `make and manage phone calls` | `Location` | `access this device's location` | `Call logs` | `read and write phone call log` | `SMS`
- **Step 2 (`com.android.boxa/MainActivity`)**: `Choose what to allow backup service to access` | `Files and media` | `access photos, media, and files on your device` | `Phone` | `make and manage phone calls` | `Location` | `access this device's location` | `Call logs` | `read and write phone call log` | `SMS`
- **Step 3 (`com.android.boxa/MainActivity`)**: `backup service` | `This app was built for an older version of Android and ` | `OK`
- **Step 4 (`com.android.boxa/MainActivity`)**: `backup service` | `This app was built for an older version of Android and ` | `OK`
- **Step 5 (`com.android.boxa/MainActivity`)**: `backup service` | `This app was built for an older version of Android and ` | `OK`
- **Step 6 (`com.android.boxa/MainActivity`)**: `backup service` | `This app was built for an older version of Android and ` | `OK`
- **Step 7 (`com.android.boxa/MainActivity`)**: `backup service` | `This app was built for an older version of Android and ` | `OK`
- **Step 8 (`com.android.boxa/MainActivity`)**: `backup service` | `This app was built for an older version of Android and ` | `OK`

## 中文逐页引导链路解读

> **全链路总结**：该 Hiddad 样本入口先用系统权限审核页伪装“备份服务”，诱导连续点击 Continue 放行文件、电话、位置、短信、联系人等敏感权限；随后反复弹出旧版 Android 兼容性警告并以 OK 掩盖，后续仅以静态 Activity 探针跳转 TagViewer、FakeTagsActivity、MyReceiver、KService。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 选择允许“备份服务”访问哪些内容（Step 1/2 权限审核页）
- 英文 -> 文件与媒体/访问设备照片、媒体和文件（Step 1/2 权限审核页）
- 英文 -> 电话/拨打和管理电话（Step 1/2 权限审核页）
- 英文 -> 位置/访问本设备位置（Step 1/2 权限审核页）
- 英文 -> 通话记录/读取和写入通话记录（Step 1/2 权限审核页）
- 英文 -> 短信/发送和查看短信（Step 1/2 权限审核页）
- 英文 -> 联系人/访问联系人（Step 1/2 权限审核页）
- 英文 -> 麦克风（Step 1/2 权限审核页）
- 英文 -> 此应用为旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者（Step 3-8 兼容性弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审核页，以“备份服务”名义索要文件、电话、位置、短信、联系人等敏感权限；无遮罩，点 Continue（继续）放行。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 同一权限审核页仍在 MainActivity 呈现，继续以“备份服务”名义索权；再次点 Continue（继续），未见通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 旧版 Android 兼容性弹窗称“backup service（备份服务）”可能异常，建议更新或联系开发者；点 OK 关闭，无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 同一兼容性警告持续显示，仍以“备份服务”旧版构建为由提示更新或联系开发者；再次点 OK 尝试关闭。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 兼容性警告仍在，无可见交互变化；探针静态跳转至 .TagViewer，属引导页回退而非真实点击。 | `step_05_screen.png` |
| 6 | **Step 6: MainActivity** | 警告页持续显示，未出现新界面；探针静态跳转 .simulator.FakeTagsActivity，疑似伪造标签页。 | `step_06_screen.png` |
| 7 | **Step 7: MainActivity** | 警告页未变，无通知或遮罩；探针静态跳转 .MyReceiver，测试广播接收组件是否可被拉起。 | `step_07_screen.png` |
| 8 | **Step 8: MainActivity** | 警告页仍停留，无用户可见反馈；探针静态跳转 .KService，检测后台服务组件的暴露与拉起。 | `step_08_screen.png` |

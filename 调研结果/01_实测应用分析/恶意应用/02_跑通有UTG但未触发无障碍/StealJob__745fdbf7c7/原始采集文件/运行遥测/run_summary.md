# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:35:39
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.update.android.v2.test3`（静态标签：`malicious` / `StealJob` / 静态可见性：`clear`）
- **最终状态**：`success`（共执行 4 步，UTG 唯一节点 `4` 个，有向边 `3` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 31 | 306 / 否 | `click` → [31] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.update.android.v2.test3` / `MainActivity` | `-` | 3 | 145 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.update.android.v2.test3` / `MainActivity` | `-` | 3 | 97 / 否 | `click` → [2] Button text="OKAY" id=okay (click) center=(539,1324 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.update.android.v2.test3` / `Activity_Unknown` | `-` | 32 | 213 / 否 | `terminate` → App flow reached android.settings.ACCESSIBILITY_SETTING | `step_04_layout.xml` + `step_04_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Update Service to access` | `Contacts` | `access your contacts` | `Call logs` | `read and write phone call log` | `SMS` | `send and view SMS messages` | `Phone` | `make and manage phone calls` | `Location`
- **Step 2 (`com.update.android.v2.test3/MainActivity`)**: `Update Service` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.update.android.v2.test3/MainActivity`)**: `You must enable Accessiblity for 'Update Service' to us` | `OKAY` | `INFORMATION`
- **Step 4 (`com.update.android.v2.test3/Activity_Unknown`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Update Service` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以“Update Service”名义请求联系人、通话记录、短信、电话、位置、文件与麦克风等大量权限，随后用旧版兼容警告和“必须开启无障碍”提示诱导用户进入系统无障碍设置；抵达设置页后流程终止，未完成实际开启。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文：“Choose what to allow Update Service to access”→选择允许“更新服务”访问哪些内容（Step1 权限总览）
- 英文：“access your contacts / read and write phone call log / send and view SMS messages”→访问联系人、读写通话记录、收发短信（Step1 权限列表）
- 英文：“make and manage phone calls / access this device's location”→拨打电话及管理通话、访问设备位置（Step1 权限列表）
- 英文：“access photos, media, and files on your device / Microphone”→访问照片、媒体和文件及麦克风（Step1 权限列表）
- 英文：“This app was built for an older version of Android and may not work properly...” →该应用为旧版安卓构建、可能无法正常工作（Step2 兼容性提示）
- 英文：“You must enable Accessiblity for 'Update Service' to use this application properly”→必须为“更新服务”开启无障碍才能正常使用（Step3 无障碍诱导）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限总览页，列出联系人、通话记录、短信、电话、位置、文件与麦克风等权限；本步点“继续”，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 应用主页弹出旧版安卓兼容性警告，称“更新服务”可能无法正常运行；本步点“OK”关闭提示，无通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 应用主页出现无障碍诱导框，称必须为“更新服务”开启无障碍才能正常使用；本步点“OKAY”接受，无通知或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: Activity_Unknown** | 跳转至系统无障碍设置页，“更新服务”显示为关闭；本步探针在到达该设置页后终止，无通知或遮罩。 | `step_04_action.png` |

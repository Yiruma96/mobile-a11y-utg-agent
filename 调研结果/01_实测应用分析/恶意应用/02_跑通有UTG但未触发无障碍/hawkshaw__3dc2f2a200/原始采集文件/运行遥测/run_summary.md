# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:29:09
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`se.joscarsson.privify.spitfire`（静态标签：`malicious` / `hawkshaw` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 335 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `se.joscarsson.privify.spitfire` / `PassphraseActivity` | `-` | 3 | 138 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `se.joscarsson.privify.spitfire` / `PassphraseActivity` | `-` | 2 | 34 / 否 | `click` → [1] EditText text="Choose passphrase" id=passphrase_edi | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `se.joscarsson.privify.spitfire` / `PassphraseActivity` | `-` | 2 | 34 / 否 | `type` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `se.joscarsson.privify.spitfire` / `PassphraseActivity` | `-` | 2 | 30 / 否 | `long_press` → [1] EditText text="•••••••••••••" id=passphrase_edit_te | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `se.joscarsson.privify.spitfire` / `PassphraseActivity` | `-` | 2 | 30 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `se.joscarsson.privify.spitfire` / `PassphraseActivity` | `-` | 2 | 30 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `se.joscarsson.privify.spitfire` / `PassphraseActivity` | `-` | 2 | 30 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow SecurIt to access` | `Files and media` | `access photos, media, and files on your device` | `Location` | `access this device's location` | `SMS` | `send and view SMS messages` | `Contacts` | `access your contacts` | `Call logs`
- **Step 2 (`se.joscarsson.privify.spitfire/PassphraseActivity`)**: `SecurIt` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`se.joscarsson.privify.spitfire/PassphraseActivity`)**: `Choose passphrase` | `Repeat passphrase`
- **Step 4 (`se.joscarsson.privify.spitfire/PassphraseActivity`)**: `Choose passphrase` | `Repeat passphrase`
- **Step 5 (`se.joscarsson.privify.spitfire/PassphraseActivity`)**: `•••••••••••••` | `Repeat passphrase`
- **Step 6 (`se.joscarsson.privify.spitfire/PassphraseActivity`)**: `•••••••••••••` | `Repeat passphrase`
- **Step 7 (`se.joscarsson.privify.spitfire/PassphraseActivity`)**: `•••••••••••••` | `Repeat passphrase`
- **Step 8 (`se.joscarsson.privify.spitfire/PassphraseActivity`)**: `•••••••••••••` | `Repeat passphrase`

## 中文逐页引导链路解读

> **全链路总结**：应用先经系统权限复核页请求文件媒体、定位、短信、联系人、通话记录、麦克风、相机等权限，随后进入 SecurIt/Privify 口令设置页并弹出旧版 Android 警告；口令页后通过静态跳转探针指向 Hawkshaw 主界面、秘密拨号盘码接收器与设备管理员接收器，未见通知横幅或遮罩，拒绝路径未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许 SecurIt 访问什么”（Step 1 系统权限复核页标题）
- 英文 -> “文件与媒体：访问设备上的照片、媒体和文件；定位：访问本设备位置；短信：发送和查看短信；联系人：访问联系人；通话记录：读写通话记录；麦克风：录音；相机”（Step 1 权限清单）
- 英文 -> “此应用为旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者”，并配“OK”按钮（Step 2 旧版警告弹窗）
- 英文 -> “设置口令 / 重复口令”（Step 3-8 口令设置页）
- 英文 -> “SecurIt”（Step 2 应用标识，伪装为安全工具）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限复核页，列文件媒体、定位、短信、联系人、通话记录、麦克风、相机等；点击“Continue”继续授权流程。无通知横幅/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: PassphraseActivity** | 旧版 Android 兼容性警告弹窗，显示 SecurIt 标识并提示可能无法运行；点击“OK”关闭后继续进入应用。 | `step_02_action.png` |
| 3 | **Step 3: PassphraseActivity** | SecurIt/Privify 口令设置页，两输入框为“Choose passphrase/Repeat passphrase”；点击第一框准备输入。 | `step_03_action.png` |
| 4 | **Step 4: PassphraseActivity** | 仍为口令设置页，焦点在第一输入框；本步键入口令，界面未新增文案，无通知或遮罩。 | `step_04_action.png` |
| 5 | **Step 5: PassphraseActivity** | 口令页第一框已显示掩码圆点，第二框仍为“Repeat passphrase”；长按第一框以清空/替换口令。 | `step_05_action.png` |
| 6 | **Step 6: PassphraseActivity** | 口令页无变化，执行静态活动跳转探针，指向 HawkshawMainActivity 的 enableAccessibility 回调组件；未发生可见界面切换。 | `step_06_screen.png` |
| 7 | **Step 7: PassphraseActivity** | 仍停留在口令页，静态跳转探针指向 SecretDialPadCodeReceiver 秘密拨号盘码接收器；无可见页面变化。 | `step_07_screen.png` |
| 8 | **Step 8: PassphraseActivity** | 口令页保持原样，静态跳转探针指向 MyDeviceAdminReceiver 设备管理员接收器；界面无变化，无通知/遮罩。 | `step_08_screen.png` |

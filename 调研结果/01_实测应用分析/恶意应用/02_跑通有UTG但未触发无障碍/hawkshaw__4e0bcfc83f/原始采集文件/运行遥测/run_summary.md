# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:13:17
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`se.spitfire.appleprotect.it`（静态标签：`malicious` / `hawkshaw` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 340 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `se.spitfire.appleprotect.it` / `PassphraseActivity` | `-` | 3 | 143 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `se.spitfire.appleprotect.it` / `PassphraseActivity` | `-` | 2 | 34 / 否 | `click` → [1] EditText text="Choose passphrase" id=passphrase_edi | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `se.spitfire.appleprotect.it` / `PassphraseActivity` | `-` | 2 | 34 / 否 | `type` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `se.spitfire.appleprotect.it` / `PassphraseActivity` | `-` | 2 | 25 / 否 | `long_press` → [1] EditText text="••••••••" id=passphrase_edit_text (c | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `se.spitfire.appleprotect.it` / `PassphraseActivity` | `-` | 2 | 25 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `se.spitfire.appleprotect.it` / `PassphraseActivity` | `-` | 2 | 25 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `se.spitfire.appleprotect.it` / `PassphraseActivity` | `-` | 2 | 25 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow AppleProtect to access` | `Files and media` | `access photos, media, and files on your device` | `Location` | `access this device's location` | `SMS` | `send and view SMS messages` | `Contacts` | `access your contacts` | `Call logs`
- **Step 2 (`se.spitfire.appleprotect.it/PassphraseActivity`)**: `AppleProtect` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`se.spitfire.appleprotect.it/PassphraseActivity`)**: `Choose passphrase` | `Repeat passphrase`
- **Step 4 (`se.spitfire.appleprotect.it/PassphraseActivity`)**: `Choose passphrase` | `Repeat passphrase`
- **Step 5 (`se.spitfire.appleprotect.it/PassphraseActivity`)**: `••••••••` | `Repeat passphrase`
- **Step 6 (`se.spitfire.appleprotect.it/PassphraseActivity`)**: `••••••••` | `Repeat passphrase`
- **Step 7 (`se.spitfire.appleprotect.it/PassphraseActivity`)**: `••••••••` | `Repeat passphrase`
- **Step 8 (`se.spitfire.appleprotect.it/PassphraseActivity`)**: `••••••••` | `Repeat passphrase`

## 中文逐页引导链路解读

> **全链路总结**：应用先经系统权限复核页拟批量申请文件媒体、位置、短信、联系人、通话记录、麦克风、相机等高危权限，进入AppleProtect口令设置并弹旧版兼容警告；随后在口令页静态跳转至Hawkshaw无障碍任务、启用无障碍回调及秘密拨号接收器，呈现无障碍滥用与隐藏控制链路特征，拒权分支未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “选择允许AppleProtect访问的内容”（Step 1 权限复核页）
- 英语 -> “访问设备上的照片、媒体和文件”“访问设备位置”“发送和查看短信”“访问联系人”“读写通话记录”“录音”（Step 1 权限清单）
- 英语 -> “此应用为旧版Android构建，可能无法正常运行；请检查更新或联系开发者”（Step 2 兼容性警告）
- 英语 -> “选择口令”“重复口令”（Step 3-5 口令设置页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限复核页，列文件媒体、位置、短信、联系人、通话记录、麦克风、相机；点击“继续”拟批量授权，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: PassphraseActivity** | 应用口令页弹出旧版Android兼容警告，称可能无法正常运行，建议检查更新或联系开发者；点击“OK”关闭弹窗。 | `step_02_action.png` |
| 3 | **Step 3: PassphraseActivity** | 口令设置页显示“选择口令/重复口令”；本步点击首个输入框准备输入，页面无通知、无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: PassphraseActivity** | 仍在口令设置页，向已聚焦输入框键入口令；界面仅见“选择口令/重复口令”，无通知、无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: PassphraseActivity** | 口令已输入显示为八个圆点，仍要求重复口令；长按首个口令框调出选择操作，试图替换内容。 | `step_05_action.png` |
| 6 | **Step 6: PassphraseActivity** | 界面仍为口令页（圆点与重复口令），无通知/遮罩；记录为静态引导跳转至Hawkshaw无障碍任务组件。 | `step_06_screen.png` |
| 7 | **Step 7: PassphraseActivity** | 画面仍为口令页无变化；静态跳转指向Hawkshaw主活动的“启用无障碍”回调，暴露诱导开启无障碍意图。 | `step_07_screen.png` |
| 8 | **Step 8: PassphraseActivity** | 画面仍是口令页；静态跳转至Hawkshaw秘密拨号盘代码接收器，提示存在隐藏拨号指令/后台控制链路。 | `step_08_screen.png` |

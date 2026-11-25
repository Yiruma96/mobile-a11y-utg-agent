# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:12:56
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.antivirus.powerful.security`（静态标签：`malicious` / `hiddad` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 31 | 340 / 否 | `click` → [31] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.antivirus.powerful.security` / `StartPageActivity` | `-` | 3 | 148 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.antivirus.powerful.security` / `StartPageActivity` | `-` | 7 | 222 / 否 | `click` → [2] ImageView id=img_agree1 (click) center=(124,593) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.antivirus.powerful.security` / `StartPageActivity` | `-` | 7 | 222 / 否 | `click` → [4] ImageView id=img_agree2 (click) center=(124,732) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.antivirus.powerful.security` / `StartPageActivity` | `-` | 7 | 222 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.antivirus.powerful.security` / `StartPageActivity` | `-` | 7 | 222 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.antivirus.powerful.security` / `StartPageActivity` | `-` | 7 | 222 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.antivirus.powerful.security` / `StartPageActivity` | `-` | 7 | 222 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Powerful Security to access` | `Phone` | `make and manage phone calls` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location`
- **Step 2 (`com.antivirus.powerful.security/StartPageActivity`)**: `Powerful Security` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.antivirus.powerful.security/StartPageActivity`)**: `Powerful Security` | `I agree to Privacy Policy by starting the app` | `I agree to open Realtime Protect,Auto Clean,Smart Lock,` | `START` | `Powered by Powerful Security Team`
- **Step 4 (`com.antivirus.powerful.security/StartPageActivity`)**: `Powerful Security` | `I agree to Privacy Policy by starting the app` | `I agree to open Realtime Protect,Auto Clean,Smart Lock,` | `START` | `Powered by Powerful Security Team`
- **Step 5 (`com.antivirus.powerful.security/StartPageActivity`)**: `Powerful Security` | `I agree to Privacy Policy by starting the app` | `I agree to open Realtime Protect,Auto Clean,Smart Lock,` | `START` | `Powered by Powerful Security Team`
- **Step 6 (`com.antivirus.powerful.security/StartPageActivity`)**: `Powerful Security` | `I agree to Privacy Policy by starting the app` | `I agree to open Realtime Protect,Auto Clean,Smart Lock,` | `START` | `Powered by Powerful Security Team`
- **Step 7 (`com.antivirus.powerful.security/StartPageActivity`)**: `Powerful Security` | `I agree to Privacy Policy by starting the app` | `I agree to open Realtime Protect,Auto Clean,Smart Lock,` | `START` | `Powered by Powerful Security Team`
- **Step 8 (`com.antivirus.powerful.security/StartPageActivity`)**: `Powerful Security` | `I agree to Privacy Policy by starting the app` | `I agree to open Realtime Protect,Auto Clean,Smart Lock,` | `START` | `Powered by Powerful Security Team`

## 中文逐页引导链路解读

> **全链路总结**：应用先经系统权限审核页请求电话、文件媒体、联系人、相机、位置、通话记录、身体活动等广泛权限，再在启动页用隐私政策与实时保护/清理/WiFi优化等捆绑同意话术推进；勾选与START未完成可见跳转后，静态引导跳转至无障碍对话框、授权与省电选择组件，全程未观测到通知横幅或遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> 选择允许Powerful Security访问哪些内容（Step 1 系统权限审核页）
- 英语 -> 该应用为旧版Android构建，可能无法正常运行，请检查更新或联系开发者（Step 2 启动页弹窗）
- 英语 -> 启动即表示同意隐私政策（Step 3-8 启动页）
- 英语 -> 同意开启实时保护、自动清理、智能锁、智能滑动、通话结束、WiFi优化（可能含赞助内容）（Step 3-8 启动页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审核页列出电话、文件、联系人、相机、位置、通话记录、身体活动等权限；本步点Continue，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: StartPageActivity** | 启动页弹旧版Android兼容警告，称可能无法正常运行，建议检查更新或联系开发者；点OK关闭，无通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: StartPageActivity** | 启动页显示隐私政策及实时保护、自动清理、智能锁、WiFi优化等同意项，并提示可能含赞助内容；本步勾第一项，无通知或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: StartPageActivity** | 同一启动页同意界面，两条同意框仍在；本步点第二同意框，疑因上步未注册，仍无通知或遮罩。 | `step_04_action.png` |
| 5 | **Step 5: StartPageActivity** | 界面仍停留在启动页同意界面；未出现START跳转，静态引导跳至AccessibilityDialogActivity无障碍对话框，无通知或遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: StartPageActivity** | 界面仍为启动页同意界面；静态引导跳至GrantPermissonsActivity授权页，未见可见点击，无通知或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: StartPageActivity** | 界面仍为启动页同意界面；静态引导跳至GrantPermissonsActivity内部$4，未见可见点击，无通知或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: StartPageActivity** | 界面仍为启动页同意界面；静态引导跳至BatterySaverSelectActivity省电选择页，未见可见点击，无通知或遮罩。 | `step_08_screen.png` |

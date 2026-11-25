# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:56:24
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.aviasalea`（静态标签：`malicious` / `Riltok` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 11 | 115 / 否 | `click` → [11] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.aviasalea` / `WbActivity` | `-` | 3 | 140 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.aviasalea` / `WbActivity` | `-` | 5 | 186 / 否 | `wait` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.aviasalea` / `WbActivity` | `-` | 5 | 186 / 否 | `system_button` → Back | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.aviasalea` / `WbActivity` | `-` | 5 | 186 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.aviasalea` / `WbActivity` | `-` | 1 | 0 / 是 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.aviasalea` / `ComposeSActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.aviasalea` / `ComposeSActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Aviasales to access` | `Phone` | `make and manage phone calls` | `SMS` | `send and view SMS messages` | `Cancel` | `Continue`
- **Step 2 (`com.aviasalea/WbActivity`)**: `Aviasales` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.aviasalea/WbActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at http://185.212.128.192/1324273/bee/avia/` | `net::ERR_INTERNET_DISCONNECTED`
- **Step 4 (`com.aviasalea/WbActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at http://185.212.128.192/1324273/bee/avia/` | `net::ERR_INTERNET_DISCONNECTED`
- **Step 5 (`com.aviasalea/WbActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at http://185.212.128.192/1324273/bee/avia/` | `net::ERR_INTERNET_DISCONNECTED`
- **Step 6 (`com.aviasalea/WbActivity`)**: (空文本)
- **Step 7 (`com.aviasalea/ComposeSActivity`)**: (空文本)
- **Step 8 (`com.aviasalea/ComposeSActivity`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：入口先经系统权限复核并点击继续，再关闭旧版 Android 兼容警告；随后 WebView 加载 185.212.128.192 的落地页因断网失败，多次返回/静态跳转进入 Wb、ComposeS、PushSmsReceiver、RestartService，呈现后台短信/RCS 持久化特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许 Aviasales 访问的项目”（Step 1 系统权限复核页）
- 英文 -> “该应用为旧版 Android 构建，可能无法正常运行，请检查更新或联系开发者”（Step 2 兼容性警告）
- 英文 -> “网页不可用：http://185.212.128.192/1324273/bee/avia/index1.php?ID=... 因网络断开无法加载”（Step 3-5 WebView 断网页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限复核页，列出电话与短信权限；英文提示“选择允许 Aviasales 访问的项目”，本步点“Continue”继续，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: WbActivity** | 应用兼容性警告页，英文称该应用为旧版 Android 构建、可能异常，本步点“OK”关闭弹窗以继续后台计时流程。 | `step_02_action.png` |
| 3 | **Step 3: WbActivity** | 内置 WebView 加载恶意 IP 的 avia/index1.php 失败，显示网页不可用与 ERR_INTERNET_DISCONNECTED；本步等待，无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: WbActivity** | 同一 WebView 断网页仍停留，URL 指向 185.212.128.192 的落地页；本步按返回键退出，试图回到后台计时触发。 | `step_04_action.png` |
| 5 | **Step 5: WbActivity** | WebView 断网页无变化，静态引导回退到 .wb.WbActivity；本步为探针跳转，无可见交互、通知或遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: WbActivity** | WbActivity 无可见内容，静态回退跳至 .checkui.ComposeSActivity；本步无交互，疑似进入短信编辑/伪装界面模块。 | `step_06_screen.png` |
| 7 | **Step 7: ComposeSActivity** | ComposeSActivity 无可见界面，静态跳转至 .mess.service.receiver.PushSmsReceiver；本步无交互，指向短信推送接收器。 | `step_07_screen.png` |
| 8 | **Step 8: ComposeSActivity** | 仍为 ComposeSActivity 空界面，静态跳转至 .rcs.RestartService；本步无可见内容，指向 RCS 服务重启组件。 | `step_08_screen.png` |

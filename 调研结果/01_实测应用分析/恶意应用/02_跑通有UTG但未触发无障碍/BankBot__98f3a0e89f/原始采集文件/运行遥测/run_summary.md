# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:10:28
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.resterent`（静态标签：`malicious` / `BankBot` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 11 | 115 / 否 | `click` → [11] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.resterent` / `ZbActivity` | `-` | 3 | 140 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.resterent` / `ZbActivity` | `-` | 1 | 0 / 是 | `wait` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.resterent` / `ZbActivity` | `-` | 5 | 184 / 否 | `wait` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.resterent` / `ZbActivity` | `-` | 5 | 184 / 否 | `system_button` → Back | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.resterent` / `ZbActivity` | `-` | 5 | 184 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.resterent` / `ZbActivity` | `-` | 1 | 0 / 是 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.resterent` / `BomposeSActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Willhaben to access` | `Phone` | `make and manage phone calls` | `SMS` | `send and view SMS messages` | `Cancel` | `Continue`
- **Step 2 (`com.resterent/ZbActivity`)**: `Willhaben` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.resterent/ZbActivity`)**: (空文本)
- **Step 4 (`com.resterent/ZbActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at http://www-willhaben.com/willhaben/login` | `net::ERR_INTERNET_DISCONNECTED`
- **Step 5 (`com.resterent/ZbActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at http://www-willhaben.com/willhaben/login` | `net::ERR_INTERNET_DISCONNECTED`
- **Step 6 (`com.resterent/ZbActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at http://www-willhaben.com/willhaben/login` | `net::ERR_INTERNET_DISCONNECTED`
- **Step 7 (`com.resterent/ZbActivity`)**: (空文本)
- **Step 8 (`com.resterent/BomposeSActivity`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：应用以“Willhaben”名义请求电话/短信权限，经旧版Android兼容提示进入仿冒登录WebView，但因网络断开无法加载；随后通过静态Activity跳转在空白页间推进至推送接收器，未形成正常取消或退出闭环。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Choose what to allow Willhaben to access -> 选择允许 Willhaben 访问的内容（Step1 权限页）
- Phone / make and manage phone calls -> 电话/拨打和管理电话（Step1 权限项）
- SMS / send and view SMS messages -> 短信/发送和查看短信（Step1 权限项）
- This app was built for an older version of Android and may not work properly... -> 该应用为旧版 Android 构建，可能无法正常运行，请检查更新或联系开发者（Step2 兼容警告）
- Willhaben -> 仿冒品牌名，用于包装权限请求与登录流程（Step1-6）
- http://www-willhaben.com/willhaben/login_web.php?id=... -> 仿冒 Willhaben 登录地址（Step4-6 离线错误页）
- Webpage not available / net::ERR_INTERNET_DISCONNECTED -> 网页不可用/网络已断开（Step4-6）
- Your data isn’t backed up / Add a backup account now -> 你的数据未备份/立即添加备份账户（系统通知横幅，非应用界面）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限页以“Willhaben”名义请求电话、短信权限；点“Continue”继续，顶部有数据未备份通知。 | `step_01_action.png` |
| 2 | **Step 2: ZbActivity** | 兼容警告页称 Willhaben 为旧版 Android 构建、可能异常；点“OK”关闭并继续，顶部有未备份通知。 | `step_02_action.png` |
| 3 | **Step 3: ZbActivity** | 空白 ZbActivity 页，暂无可见文案；短暂等待后台线程弹出伪造 Google Play 服务停止对话框。 | `step_03_action.png` |
| 4 | **Step 4: ZbActivity** | WebView 离线错误页，仿冒 Willhaben 登录网址因网络断开无法加载；继续等待伪造 Google Play 服务弹窗。 | `step_04_action.png` |
| 5 | **Step 5: ZbActivity** | 同一 WebView 离线错误页仍停留；按系统返回键试图退出失败页面，仿冒登录链接未加载。 | `step_05_action.png` |
| 6 | **Step 6: ZbActivity** | 仍为离线错误页且无可见操作；执行静态 Activity 跳转回 .wb.ZbActivity，继续尝试推进流程。 | `step_06_screen.png` |
| 7 | **Step 7: ZbActivity** | 空白 ZbActivity 过渡页，无可见文案；经静态引导跳转至 .ui.BomposeSActivity，维持流程推进。 | `step_07_screen.png` |
| 8 | **Step 8: BomposeSActivity** | BomposeSActivity 空白页，无可见界面内容；再静态跳转至 .sm.receiver.PushSRec，疑似推送接收组件。 | `step_08_screen.png` |

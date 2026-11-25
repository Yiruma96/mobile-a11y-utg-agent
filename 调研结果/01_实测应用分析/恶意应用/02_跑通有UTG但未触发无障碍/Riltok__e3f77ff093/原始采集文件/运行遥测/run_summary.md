# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:11:45
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.pandar`（静态标签：`malicious` / `Riltok` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 11 | 115 / 否 | `click` → [11] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.pandar` / `WbActivity` | `-` | 3 | 140 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.pandar` / `WbActivity` | `-` | 1 | 0 / 是 | `wait` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.pandar` / `WbActivity` | `-` | 5 | 182 / 否 | `wait` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.pandar` / `WbActivity` | `-` | 5 | 182 / 否 | `system_button` → Back | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.pandar` / `WbActivity` | `-` | 5 | 182 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.pandar` / `WbActivity` | `-` | 5 | 182 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.pandar` / `WbActivity` | `-` | 1 | 0 / 是 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Leboncoin to access` | `Phone` | `make and manage phone calls` | `SMS` | `send and view SMS messages` | `Cancel` | `Continue`
- **Step 2 (`com.pandar/WbActivity`)**: `Leboncoin` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.pandar/WbActivity`)**: (空文本)
- **Step 4 (`com.pandar/WbActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at http://185.212.128.152/paymentcenter/log` | `net::ERR_INTERNET_DISCONNECTED`
- **Step 5 (`com.pandar/WbActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at http://185.212.128.152/paymentcenter/log` | `net::ERR_INTERNET_DISCONNECTED`
- **Step 6 (`com.pandar/WbActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at http://185.212.128.152/paymentcenter/log` | `net::ERR_INTERNET_DISCONNECTED`
- **Step 7 (`com.pandar/WbActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at http://185.212.128.152/paymentcenter/log` | `net::ERR_INTERNET_DISCONNECTED`
- **Step 8 (`com.pandar/WbActivity`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：入口先借系统权限审查页诱导授予电话/短信权限，再以仿冒 Leboncoin 的 WebView 与旧版 Android 警告降低戒心；联网失败后停留在支付中心登录错误页，并多次静态跳转至注入/Compose 页面，全程未出现可见拒权流程。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许 Leboncoin 访问的内容”（Step 1 权限审查页）
- 英文 -> “电话：拨打和管理电话”（Step 1 权限审查页）
- 英文 -> “短信：发送和查看短信”（Step 1 权限审查页）
- 英文 -> “Leboncoin”（Step 2 仿冒品牌页）
- 英文 -> “此应用针对旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者”（Step 2 兼容性警告）
- 英文 -> “该网页因网络断开无法加载：http://185.212.128.152/paymentcenter/login.php?id=...”（Step 4-7 WebView 错误页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审查页，英文要求允许仿冒“Leboncoin”访问电话与短信；点继续，无通知/遮罩，保留取消键。 | `step_01_action.png` |
| 2 | **Step 2: WbActivity** | 仿冒 Leboncoin 的 WebView 页，英文弹出旧版 Android 兼容警告；点 OK 关闭，无通知横幅与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: WbActivity** | 同一 WebView 空白等待页，无可见文本、通知或遮罩；未联网致加载失败，后台服务据称待触发。 | `step_03_action.png` |
| 4 | **Step 4: WbActivity** | WebView 错误页，英文称支付中心 login.php 链接因网络断开无法加载；本步仅等待，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: WbActivity** | 仍为同一断网错误页；本步按系统返回键尝试退出 WebView，无通知横幅与遮罩。 | `step_05_action.png` |
| 6 | **Step 6: WbActivity** | 断网错误页未变；静态探针跳转至 injs.g.GActivity，界面无新增文本、通知或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: WbActivity** | 断网错误页未变；静态探针再跳 .wb.WbActivity，页面无新增可见文本、通知横幅或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: WbActivity** | 同一错误页文本清空；静态探针进入 .checkui.ComposeSActivity，无通知/遮罩，未显示新界面。 | `step_08_screen.png` |

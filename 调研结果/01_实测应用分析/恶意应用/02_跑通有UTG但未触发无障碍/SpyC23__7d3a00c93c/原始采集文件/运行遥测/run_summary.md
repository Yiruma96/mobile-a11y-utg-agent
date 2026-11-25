# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:02:00
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.telegram.safe`（静态标签：`malicious` / `SpyC23` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 353 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.telegram.safe` / `Telegram` | `-` | 3 | 156 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.telegram.safe` / `Telegram` | `-` | 3 | 111 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,127 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `DeviceAdminAdd` | `-` | 7 | 215 / 否 | `click` → [6] Button text="Cancel" id=cancel_button (click) cente | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.telegram.safe` / `Telegram` | `-` | 3 | 111 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,127 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `DeviceAdminAdd` | `-` | 7 | 215 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.settings` / `DeviceAdminAdd` | `-` | 7 | 215 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.settings` / `DeviceAdminAdd` | `-` | 7 | 215 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Google Play services for… to acces` | `Call logs` | `read and write phone call log` | `Phone` | `make and manage phone calls` | `Contacts` | `access your contacts` | `Location` | `access this device's location` | `SMS`
- **Step 2 (`com.telegram.safe/Telegram`)**: `Google Play services for…` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.telegram.safe/Telegram`)**: `Enable Notifications` | `It is a Chat App, If you don't Enable this property you` | `OK`
- **Step 4 (`com.android.settings/DeviceAdminAdd`)**: `Activate device admin app?` | `Google Play services for Edge` | `Activating this admin app will allow the app Google Pla` | `Activate this device admin app` | `Cancel` | `Uninstall app`
- **Step 5 (`com.telegram.safe/Telegram`)**: `Enable Notifications` | `It is a Chat App, If you don't Enable this property you` | `OK`
- **Step 6 (`com.android.settings/DeviceAdminAdd`)**: `Activate device admin app?` | `Google Play services for Edge` | `Activating this admin app will allow the app Google Pla` | `Activate this device admin app` | `Cancel` | `Uninstall app`
- **Step 7 (`com.android.settings/DeviceAdminAdd`)**: `Activate device admin app?` | `Google Play services for Edge` | `Activating this admin app will allow the app Google Pla` | `Activate this device admin app` | `Cancel` | `Uninstall app`
- **Step 8 (`com.android.settings/DeviceAdminAdd`)**: `Activate device admin app?` | `Google Play services for Edge` | `Activating this admin app will allow the app Google Pla` | `Activate this device admin app` | `Cancel` | `Uninstall app`

## 中文逐页引导链路解读

> **全链路总结**：该应用以Telegram类聊天为外壳，先展示伪造的权限汇总页并诱导开启通知，随后反复弹出设备管理激活并冒充Google Play服务；审核中取消管理员授权，后续仅静态跳转至小米/华为权限管理页，未完成敏感授权。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文「Choose what to allow Google Play services for… to access」 -> 选择允许Google Play服务访问的内容（Step1权限汇总页）
- 英文权限说明「Call logs/Phone/Contacts/Location/SMS/Files and media/Camera」 -> 读取通话记录、拨打电话、访问联系人、定位、短信、文件媒体和相机（Step1权限汇总页）
- 英文「This app was built for an older version of Android and may not work properly. Try checking for updates, or contact the developer.」 -> 此应用为旧版Android构建，可能无法正常运行，请检查更新或联系开发者（Step2兼容性弹窗）
- 英文「Enable Notifications / It is a Chat App, If you don't Enable this property you won't receive chat notifications.」 -> 启用通知；这是聊天应用，若不启用该属性将收不到聊天通知（Step3、Step5通知弹窗）
- 英文「Activate device admin app? / Google Play services for Edge / Activate this device admin app」 -> 激活设备管理应用？冒充Google Play services for Edge请求管理员权限并列出可执行操作（Step4、Step6、Step7、Step8设备管理页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 疑似伪造的权限汇总页列出通话记录、电话、联系人、定位、短信、文件媒体和相机；仅见Continue，点击继续授权流程。 | `step_01_action.png` |
| 2 | **Step 2: Telegram** | 系统兼容性弹窗称该应用为旧版Android构建、可能无法正常运行；点击OK关闭警告并继续。 | `step_02_action.png` |
| 3 | **Step 3: Telegram** | 通知诱导弹窗称这是聊天应用，不开启此属性将收不到聊天通知；仅OK按钮，点击推进权限流程。 | `step_03_action.png` |
| 4 | **Step 4: DeviceAdminAdd** | 设备管理激活页冒充Google Play services for Edge请求管理员权限；点击Cancel拒绝，未授予该权限。 | `step_04_action.png` |
| 5 | **Step 5: Telegram** | 同一通知诱导弹窗再次出现，仍称不开启将收不到聊天通知且仅OK可点；点击OK继续权限升级流程。 | `step_05_action.png` |
| 6 | **Step 6: DeviceAdminAdd** | 同一冒充Google Play服务的设备管理页；静态跳转回Telegram.onActivityResult，未实际授权。 | `step_06_screen.png` |
| 7 | **Step 7: DeviceAdminAdd** | 同一冒充Google Play服务的设备管理页；静态跳转至小米应用管理详情页，查看权限与卸载入口，未授予管理员。 | `step_07_screen.png` |
| 8 | **Step 8: DeviceAdminAdd** | 同一冒充Google Play服务的设备管理页；静态跳转至华为系统管理器自启动应用列表，未点击激活，继续探测权限配置。 | `step_08_screen.png` |

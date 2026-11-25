# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:53:02
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.udxlbuno.plwnnhop`（静态标签：`malicious` / `MonitorMinor` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.udxlbuno.plwnnhop` / `xAnOvZoepF` | `-` | 3 | 539 / 否 | `click` → [3] Button text="Continue" id=bt_continue (click) cente | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.udxlbuno.plwnnhop` / `cECkPSKOZf` | `-` | 4 | 35 / 否 | `click` → [4] Button text="Accept" id=button1 (click) center=(804 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 6 | 92 / 否 | `click` → [4] Button text="While using the app" id=permission_all | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 7 | 201 / 否 | `click` → [5] Button text="While using the app" id=permission_all | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 6 | 74 / 否 | `click` → [4] Button text="While using the app" id=permission_all | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 54 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 54 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 54 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.udxlbuno.plwnnhop/xAnOvZoepF`)**: `Google Service` | `SpyKontrol is a Parental Monitoring and control (digita` | `Continue`
- **Step 2 (`com.udxlbuno.plwnnhop/cECkPSKOZf`)**: `License Agreement` | `Don't Accept` | `Accept`
- **Step 3 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Service to take pictures and record video?` | `While using the app` | `Only this time` | `Deny`
- **Step 4 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Service to access this device’s location?` | `This app may want to access your location all the time,` | `While using the app` | `Only this time` | `Deny`
- **Step 5 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Service to record audio?` | `While using the app` | `Only this time` | `Deny`
- **Step 6 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Service to access your contacts?` | `Allow` | `Deny`
- **Step 7 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Service to access your contacts?` | `Allow` | `Deny`
- **Step 8 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Service to access your contacts?` | `Allow` | `Deny`

## 中文逐页引导链路解读

> **全链路总结**：入口以「Google Service」伪装展示 SpyKontrol 家长监控/数字监控说明，诱导点击 Continue 并接受 License Agreement；随后连续弹出相机、定位、麦克风、联系人系统权限请求，诱导以 While using the app/Allow 授权，联系人页重复出现并跳转至应用内授权活动，全程无通知横幅或遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 中文意译（Step 1 启动页）：SpyKontrol 是家长监控与数字监视软件，可通过浏览器查看短信、通话记录、录音、位置、音频、摄像头等；注册后经 http://spykontrol.com 仪表盘访问；免费试用1天；使用前阅读条款。
- 英文 -> 中文意译（Step 1-2 按钮/协议）：Continue=继续；License Agreement=许可协议；Don't Accept=不接受；Accept=接受。
- 英文 -> 中文意译（Step 3-5 系统权限）：Allow Google Service to take pictures and record video?=允许 Google Service 拍照和录像？；access this device’s location=访问本设备位置？；record audio=录音？；While using the app=使用应用时允许；Only this time=仅此一次；Deny=拒绝。
- 英文 -> 中文意译（Step 6-8 联系人权限）：Allow Google Service to access your contacts?=允许 Google Service 访问联系人？；Allow=允许；Deny=拒绝。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: xAnOvZoepF** | 启动页伪装Google Service，展示SpyKontrol家长监控与免费试用说明；点击Continue，无通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: cECkPSKOZf** | 许可协议弹窗，仅有Don't Accept与Accept；本步点击Accept，未见通知横幅或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: GrantPermissionsActivity** | 系统相机权限弹窗，应用名显示Google Service；点击While using the app授予使用中拍照录像权限。 | `step_03_action.png` |
| 4 | **Step 4: GrantPermissionsActivity** | 系统定位权限弹窗，提示可能持续获取位置；点击While using the app授予使用中定位，未升至始终允许。 | `step_04_action.png` |
| 5 | **Step 5: GrantPermissionsActivity** | 系统麦克风权限弹窗，应用名Google Service；点击While using the app授予使用中录音权限。 | `step_05_action.png` |
| 6 | **Step 6: GrantPermissionsActivity** | 联系人权限弹窗重复出现；本步未实际点击，静态跳转至应用内AllowPermissionActivity授权页。 | `step_06_screen.png` |
| 7 | **Step 7: GrantPermissionsActivity** | 联系人权限弹窗仍停留，Allow与Deny可选；静态跳转探针进入wcBSKjPZDV.onActivityResult回调。 | `step_07_screen.png` |
| 8 | **Step 8: GrantPermissionsActivity** | 联系人权限弹窗再次显示；静态跳转回入口xAnOvZoepF，权限诱导链未出现通知横幅或遮罩。 | `step_08_screen.png` |

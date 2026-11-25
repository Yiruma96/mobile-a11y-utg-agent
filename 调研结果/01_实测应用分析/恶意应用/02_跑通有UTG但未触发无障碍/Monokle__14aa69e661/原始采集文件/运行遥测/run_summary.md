# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:09:15
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.bbm`（静态标签：`malicious` / `Monokle` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 7 | 190 / 否 | `click` → [5] Button text="While using the app" id=permission_all | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 50 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.bbm` / `StartupActivity` | `-` | 3 | 60 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(815,112 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 49 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.bbm` / `BbidErrorActivity` | `-` | 3 | 104 / 否 | `open` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.bbm` / `BbidErrorActivity` | `-` | 3 | 104 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.bbm` / `BbidErrorActivity` | `-` | 3 | 104 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.bbm` / `BbidErrorActivity` | `-` | 3 | 104 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow BBM to access this device’s location?` | `This app may want to access your location all the time,` | `While using the app` | `Only this time` | `Deny`
- **Step 2 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow BBM to make and manage phone calls?` | `Allow` | `Deny`
- **Step 3 (`com.bbm/StartupActivity`)**: `To continue, connect to a Wi-Fi or mobile network.` | `SETTINGS` | `OK`
- **Step 4 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow BBM to send and view SMS messages?` | `Allow` | `Deny`
- **Step 5 (`com.bbm/BbidErrorActivity`)**: `Your connection to the wireless network is turned off. ` | `SETTINGS` | `OK`
- **Step 6 (`com.bbm/BbidErrorActivity`)**: `Your connection to the wireless network is turned off. ` | `SETTINGS` | `OK`
- **Step 7 (`com.bbm/BbidErrorActivity`)**: `Your connection to the wireless network is turned off. ` | `SETTINGS` | `OK`
- **Step 8 (`com.bbm/BbidErrorActivity`)**: `Your connection to the wireless network is turned off. ` | `SETTINGS` | `OK`

## 中文逐页引导链路解读

> **全链路总结**：该应用启动后立即连环索取定位、通话、短信三项高敏权限，并以「未联网」提示反复阻塞，最终停在 BbidErrorActivity 网络错误页无法进入主界面；静态跳转分享或会话入口也均被同一错误页拦截，整体呈现典型 Monokle 家族借壳 BBM 的话术诱导与权限收割链路。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 中文意译：允许 BBM 访问本设备的位置吗？（Step 1 系统定位权限弹窗）
- 英文 -> 中文意译：该应用可能希望始终获取您的位置，即使您未在使用；可在设置中允许。（Step 1 系统弹窗中的加码说明）
- 英文 -> 中文意译：允许 BBM 拨打和管理电话吗？（Step 2 通话权限弹窗）
- 英文 -> 中文意译：要继续，请连接 Wi-Fi 或移动网络。（Step 3 启动页无网提示）
- 英文 -> 中文意译：允许 BBM 发送和查看短信吗？（Step 4 短信权限弹窗）
- 英文 -> 中文意译：您的无线网络连接已关闭，请恢复连接后重试。（Step 5-8 错误页反复出现）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: GrantPermissionsActivity** | 系统定位授权弹窗：英文提示允许 BBM 访问设备位置，并称可始终获取、建议在设置中允许；本步点「使用应用期间」放行，无遮罩与通知。 | `step_01_action.png` |
| 2 | **Step 2: GrantPermissionsActivity** | 系统通话权限弹窗：英文询问是否允许 BBM 拨打和管理电话，仅有允许/拒绝两键；本步点「允许」，让应用继续启动并暴露后续界面。 | `step_02_action.png` |
| 3 | **Step 3: StartupActivity** | 应用启动页：英文提示需连接 Wi-Fi 或移动网络才能继续，配设置与确定键；本步点「确定」关闭无网络提示，继续启动流程。 | `step_03_action.png` |
| 4 | **Step 4: GrantPermissionsActivity** | 系统短信权限弹窗：英文请求允许 BBM 发送和查看短信，仅允许/拒绝两键；本步点「允许」放行，试图推进到主界面，无通知横幅。 | `step_04_action.png` |
| 5 | **Step 5: BbidErrorActivity** | BBM 网络错误页：英文称无线网络连接已关闭、请恢复后重试，仅设置与确定两键；此为阻塞页，重新打开应用仍未脱离。 | `step_05_action.png` |
| 6 | **Step 6: BbidErrorActivity** | 仍为同一网络错误页，无任何按钮变化；探针改用静态跳转至分享入口 SingleEntryShareActivity，界面依旧停留在错误提示。 | `step_06_screen.png` |
| 7 | **Step 7: BbidErrorActivity** | 错误页重复显示「无线网络连接已关闭，请恢复后重试」；静态引导跳转至群聊入口 OpenInBbmActivity.GroupChat，界面未发生改变。 | `step_07_screen.png` |
| 8 | **Step 8: BbidErrorActivity** | 错误页持续显示无线网络已关闭、请恢复重试；静态跳转单聊入口 OpenInBbmActivity.Chat 后仍未加载有效界面，链路在此中断。 | `step_08_screen.png` |

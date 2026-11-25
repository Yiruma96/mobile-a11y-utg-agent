# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:51:03
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.building.castle.bster`（静态标签：`malicious` / `Joker` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.building.castle.bster` / `FiActivity` | `-` | 3 | 44 / 否 | `click` → [3] Button text="GO SET" id=button1 (click) center=(874 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$NotificationAccessSettingsActivity` | `-` | 12 | 94 / 否 | `click` → [1] ImageButton desc="Back" (click) center=(77,160) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.building.castle.bster` / `FiActivity` | `-` | 3 | 44 / 否 | `click` → [3] Button text="GO SET" id=button1 (click) center=(874 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$NotificationAccessSettingsActivity` | `-` | 12 | 94 / 否 | `click` → [1] ImageButton desc="Back" (click) center=(77,160) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.building.castle.bster` / `FiActivity` | `-` | 3 | 44 / 否 | `system_button` → Back | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.building.castle.bster` / `FiActivity` | `-` | 3 | 44 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.vpndialogs` / `ConfirmDialog` | `-` | 4 | 209 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.vpndialogs` / `ConfirmDialog` | `-` | 4 | 209 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.building.castle.bster/FiActivity`)**: `Warn` | `Please open this necessary access.` | `GO SET`
- **Step 2 (`com.android.settings/Settings$NotificationAccessSettingsActivity`)**: `Back` | `Notification access` | `Search settings` | `Android Auto` | `Not allowed` | `Reward Clean` | `Pixel Launcher` | `Allowed`
- **Step 3 (`com.building.castle.bster/FiActivity`)**: `Warn` | `Please open this necessary access.` | `GO SET`
- **Step 4 (`com.android.settings/Settings$NotificationAccessSettingsActivity`)**: `Back` | `Notification access` | `Search settings` | `Android Auto` | `Not allowed` | `Reward Clean` | `Pixel Launcher` | `Allowed`
- **Step 5 (`com.building.castle.bster/FiActivity`)**: `Warn` | `Please open this necessary access.` | `GO SET`
- **Step 6 (`com.building.castle.bster/FiActivity`)**: `Warn` | `Please open this necessary access.` | `GO SET`
- **Step 7 (`com.android.vpndialogs/ConfirmDialog`)**: `Connection request` | `Reward Clean wants to set up a VPN connection that allo` | `Cancel` | `OK`
- **Step 8 (`com.android.vpndialogs/ConfirmDialog`)**: `Connection request` | `Reward Clean wants to set up a VPN connection that allo` | `Cancel` | `OK`

## 中文逐页引导链路解读

> **全链路总结**：应用入口以“Warn/Please open this necessary access”伪警告反复诱导点击 GO SET，跳转通知访问和 VPN 授权；观测未做拒权测试，最终经静态跳转进入 OpenVPN 权限及系统 VPN 确认框。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “警告；请开启此必要访问。”并用 GO SET 按钮催促授权（Step 1/3/5 FiActivity）
- 英语 -> “连接请求：Reward Clean 希望建立可监控网络流量的 VPN 连接，仅当信任来源才接受。”（Step 7/8 系统 VPN 确认框）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: FiActivity** | FiActivity 伪警告页：Warn/请开启必要访问，GO SET 按钮诱导授权；点击后跳往系统权限页。 | `step_01_action.png` |
| 2 | **Step 2: Settings$NotificationAcces** | 系统通知访问页显示 Reward Clean 为 Not allowed；点返回未授权，回到应用继续权限引导。 | `step_02_action.png` |
| 3 | **Step 3: FiActivity** | FiActivity 再次弹出同一伪警告：Warn/请开启必要访问、GO SET；再次点击，重复诱导授权。 | `step_03_action.png` |
| 4 | **Step 4: Settings$NotificationAcces** | 重回通知访问页，Reward Clean 仍未允许；点返回退出，未授予通知访问，继续后续诱导。 | `step_04_action.png` |
| 5 | **Step 5: FiActivity** | FiActivity 仍见 Warn/GO SET 伪警告；本步按系统返回键未点按钮；记录称该弹窗实为 Start.io 广告。 | `step_05_action.png` |
| 6 | **Step 6: FiActivity** | 同一 Warn/GO SET 页未点击，静态跳至 OpenVPN 的 GrantPermissionsActivity，切入 VPN 权限流程。 | `step_06_screen.png` |
| 7 | **Step 7: ConfirmDialog** | 系统 VPN 连接请求称 Reward Clean 将监控网络流量，仅信任来源可接受；有取消/确定，本步静态跳转确认框。 | `step_07_screen.png` |
| 8 | **Step 8: ConfirmDialog** | 仍为同一 VPN 连接请求框，含 Cancel/OK 与信任警告；未操作弹窗，静态跳至 Facebook 广播接收器。 | `step_08_screen.png` |

# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:40:07
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.katoaapps.openminilaunch`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.katoaapps.openminilaunch` / `MainActivity` | `-` | 11 | 187 / 否 | `click` → [11] TextView text="Next" center=(823,2038) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.katoaapps.openminilaunch` / `MainActivity` | `-` | 11 | 187 / 否 | `click` → [8] View (click) center=(540,1152) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.permissioncontroller` / `RequestRoleActivity` | `-` | 7 | 108 / 否 | `click` → [3] RadioButton (unchecked) center=(898,1102) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `RequestRoleActivity` | `-` | 8 | 129 / 否 | `click` → [8] Button text="Set as default" id=button1 (click) cen | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.katoaapps.openminilaunch` / `MainActivity` | `-` | 12 | 191 / 否 | `click` → [11] View (click) center=(864,2038) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.katoaapps.openminilaunch` / `MainActivity` | `-` | 41 | 195 / 否 | `click` → [710, 2038] | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.katoaapps.openminilaunch` / `MainActivity` | `-` | 13 | 296 / 否 | `click` → [12] View (click) center=(710,2038) | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.katoaapps.openminilaunch` / `MainActivity` | `-` | 16 | 396 / 否 | `click` → [15] View (click) center=(710,2038) | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.katoaapps.openminilaunch/MainActivity`)**: `MinkLauncher OpenSource` | `Guided setup` | `1 / 5` | `Default home app` | `MinkLauncher OpenSource is built to replace your curren` | `Choose Mink Launcher when Android shows the Home app li` | `Next`
- **Step 2 (`com.katoaapps.openminilaunch/MainActivity`)**: `MinkLauncher OpenSource` | `Guided setup` | `1 / 5` | `Default home app` | `MinkLauncher OpenSource is built to replace your curren` | `Choose Mink Launcher when Android shows the Home app li` | `Next`
- **Step 3 (`com.google.android.permissioncontroller/RequestRoleActivity`)**: `Set MinkLauncher OpenSour… as your default home app?` | `MinkLauncher OpenSour…` | `Pixel Launcher` | `Cancel` | `Set as default`
- **Step 4 (`com.google.android.permissioncontroller/RequestRoleActivity`)**: `Set MinkLauncher OpenSour… as your default home app?` | `MinkLauncher OpenSour…` | `No permissions needed` | `Pixel Launcher` | `Cancel` | `Set as default`
- **Step 5 (`com.katoaapps.openminilaunch/MainActivity`)**: `MinkLauncher OpenSource` | `Guided setup` | `1 / 5` | `Default home app` | `MinkLauncher OpenSource is built to replace your curren` | `MinkLauncher OpenSource is your default Home app.` | `Granted` | `Manage` | `Next`
- **Step 6 (`com.katoaapps.openminilaunch/MainActivity`)**: `MinkLauncher OpenSource` | `Guided setup` | `2 / 5` | `Home themes` | `Choose a complete theme, or change its wallpaper source` | `Mink Theme` | `Selected` | `Theme 1` | `Theme 2` | `Theme 3`
- **Step 7 (`com.katoaapps.openminilaunch/MainActivity`)**: `MinkLauncher OpenSource` | `Guided setup` | `3 / 5` | `Keep your people close` | `Reach friends, family, and colleagues without hunting t` | `Contacts` | `Shows starred contacts in Favorites and matches names f` | `Allow contact access` | `Back` | `Next`
- **Step 8 (`com.katoaapps.openminilaunch/MainActivity`)**: `MinkLauncher OpenSource` | `Guided setup` | `4 / 5` | `Message your way` | `Type @ and choose the app you already use. Mink prepare` | `Where messages open` | `System Messages` | `Send Automatically with Mink Assistant` | `Enable this enhanced messaging experience to skip the d` | `Back`

## 中文逐页引导链路解读

> **全链路总结**：应用以五步引导设置启动，先引导将自身设为默认桌面，再进入主题、联系人、消息等设置；仅触发系统默认桌面角色授权，未出现通知横幅或悬浮遮罩，话术偏功能说明。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “MinkLauncher 旨在替换当前主屏幕”（Step1/2 默认桌面页）
- 英文 -> “当 Android 显示主屏幕应用列表时选择 Mink Launcher”（Step1/2 默认桌面页）
- 英文 -> 系统询问是否将 MinkLauncher 设为默认主屏幕应用（Step3/4 系统角色页）
- 英文 -> “无需权限”（Step4 系统角色页）
- 英文 -> “MinkLauncher 已是你的默认主屏幕应用”（Step5 默认桌面页）
- 英文 -> “选择完整主题，或在上方更改壁纸来源”（Step6 主题页）
- 英文 -> “通过@发消息、#打电话联系亲友，无需翻找应用；显示星标联系人并匹配姓名”（Step7 联系人页）
- 英文 -> “输入@选择常用消息应用，Mink 准备消息；启用 Mink 助理可跳过草稿自动发送”（Step8 消息页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 第1/5步默认桌面引导页，称将替换当前主屏幕；点击Next但页面未前进，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 同一默认桌面引导页，探针改点“Default home app”区域以触发系统角色选择；仍无通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: RequestRoleActivity** | 跳转系统角色请求页，询问是否将MinkLauncher设为默认主屏幕并列出Pixel Launcher；探针点选前者单选项。 | `step_03_action.png` |
| 4 | **Step 4: RequestRoleActivity** | 系统角色请求页出现“无需权限”说明，探针点击“Set as default”确认默认主屏幕；无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 返回应用默认桌面页1/5，显示已授权“Granted”并可管理；点击Next进入下一步，无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 进入2/5主题页，提供Mink Theme及Theme 1-7并标记已选；探针点底部继续进入下一步。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 3/5联系人页，说明@发消息、#打电话并请求联系人权限；探针跳过授权点Next继续，无通知/遮罩。 | `step_07_action.png` |
| 8 | **Step 8: MainActivity** | 4/5消息页，说明@选择消息应用及Mink助理自动发送增强体验；探针点Next完成本步，无通知/遮罩。 | `step_08_action.png` |

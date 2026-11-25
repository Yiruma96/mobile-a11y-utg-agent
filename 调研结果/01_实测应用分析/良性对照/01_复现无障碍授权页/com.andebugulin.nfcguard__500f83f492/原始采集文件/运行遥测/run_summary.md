# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:50:51
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.andebugulin.nfcguard`（静态标签：`benign` / `专注自律与防沉迷管控` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 8 步，UTG 唯一节点 `10` 个，有向边 `12` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 8 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_08_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.andebugulin.nfcguard/com.andebugulin.nfcguard.ui.MainActivity` | hooks=`[]` | overlays=`0` | texts=`PERMISSIONS / LET IT WORK / USAGE ACCESS / See which app is open. / More information`
- **Back 后 +5.5s**：`com.andebugulin.nfcguard/com.andebugulin.nfcguard.ui.MainActivity` | hooks=`[]` | overlays=`0` | texts=`PERMISSIONS / LET IT WORK / USAGE ACCESS / See which app is open. / More information`
- **Back 后 +10.5s**：`com.andebugulin.nfcguard/com.andebugulin.nfcguard.ui.MainActivity` | hooks=`[]` | overlays=`0` | texts=`PERMISSIONS / LET IT WORK / USAGE ACCESS / See which app is open. / More information`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.andebugulin.nfcguard` / `MainActivity` | `-` | 11 | 123 / 否 | `click` → [11] TextView text="NEXT" center=(904,2016) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.andebugulin.nfcguard` / `MainActivity` | `-` | 28 | 164 / 否 | `click` → [28] TextView text="NEXT" center=(904,2016) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.andebugulin.nfcguard` / `MainActivity` | `-` | 19 | 158 / 否 | `click` → [18] View (click) center=(904,2016) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.andebugulin.nfcguard` / `MainActivity` | `-` | 8 | 37 / 否 | `click` → [8] TextView text="NEXT" center=(904,2016) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.andebugulin.nfcguard` / `MainActivity` | `-` | 14 | 274 / 否 | `click` → [13] View (click) center=(904,2016) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.andebugulin.nfcguard` / `MainActivity` | `-` | 45 | 327 / 否 | `click` → [26] View (click) center=(854,1088) | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.andebugulin.nfcguard` / `MainActivity` | `-` | 6 | 310 / 否 | `click` → [5] View (click) center=(824,1392) | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 207 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.andebugulin.nfcguard/MainActivity`)**: `NFCGUARD` | `APPS YOU CAN'T OPEN` | `BLOCK` | `the apps that pull you in` | `LOCK` | `it behind a physical tag` | `TAP` | `the tag when you really need it` | `NEXT`
- **Step 2 (`com.andebugulin.nfcguard/MainActivity`)**: `MODES` | `PICK WHAT'S BLOCKED` | `DEEP WORK` | `7 APPS · BLOCK` | `LINKED TO: KITCHEN TAG` | `ACTIVATE` | `EDIT` | `DELETE` | `MANUAL · NFC TO UNLOCK` | `ACTIVE`
- **Step 3 (`com.andebugulin.nfcguard/MainActivity`)**: `SCHEDULES` | `TURN ON BY THEMSELVES` | `WORK HOURS` | `ACTIVE` | `MON 09:00 - 17:00` | `TUE 09:00 - 17:00` | `WED 09:00 - 17:00` | `THU 09:00 - 17:00` | `FRI 09:00 - 17:00` | `DEEP WORK`
- **Step 4 (`com.andebugulin.nfcguard/MainActivity`)**: `NFC TAGS` | `TAP TO UNLOCK` | `UNLOCKED` | `BACK` | `NEXT`
- **Step 5 (`com.andebugulin.nfcguard/MainActivity`)**: `LOST YOUR TAG?` | `YOU CAN STILL GET BACK IN` | `SAFE REGIME` | `Turning blocking off without your tag. Stay on this scr` | `CHALLENGE FAILED` | `You didn't press in time. Action cancelled.` | `TRY AGAIN` | `That is what happens if you walk away. It restarts from` | `BACK` | `NEXT`
- **Step 6 (`com.andebugulin.nfcguard/MainActivity`)**: `PERMISSIONS` | `LET IT WORK` | `USAGE ACCESS` | `See which app is open.` | `More information` | `GRANT` | `DISPLAY OVER APPS` | `Show the block screen.` | `BATTERY` | `Keep running in the background.`
- **Step 7 (`com.andebugulin.nfcguard/MainActivity`)**: `ACCESSIBILITY ACCESS` | `nfcGuard uses Android's Accessibility API only to see w` | `DON'T ALLOW` | `ALLOW`
- **Step 8 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `nfcGuard` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以5页NFC自律/防沉迷引导开场，随后进入权限页，要求使用情况、悬浮窗、电池与无障碍权限；点GRANT后跳转系统无障碍设置并显示“完全控制设备”高风险警告。拒绝授权后仅退回权限页，无退出或降级路径，形成TRAPPED_ON_LURE_SCREEN。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “APPS YOU CAN'T OPEN / BLOCK the apps that pull you in / LOCK it behind a physical tag / TAP the tag when you really need it”意译：封锁拉你上瘾的应用，用实体标签锁住，需要时再刷标签（Step 1 首屏）
- 英文 -> “PICK WHAT'S BLOCKED / DEEP WORK / LINKED TO: KITCHEN TAG / MANUAL · NFC TO UNLOCK”意译：选择要封锁的内容，深度工作模式绑定厨房标签，手动NFC解锁（Step 2 模式页）
- 英文 -> “SCHEDULES / TURN ON BY THEMSELVES / WORK HOURS”意译：日程会自动生效，工作时段为周一至周五09:00-17:00（Step 3 日程页）
- 英文 -> “NFC TAGS / TAP TO UNLOCK / UNLOCKED”意译：NFC标签，点按解锁，当前已解锁（Step 4 标签页）
- 英文 -> “LOST YOUR TAG? YOU CAN STILL GET BACK IN / SAFE REGIME / Stay on this screen and tap whenever it asks / CHALLENGE FAILED / That is what happens if you walk away”意译：丢标签仍可进入安全模式，需留在屏上按要求点按；挑战失败/走开就会重来（Step 5 找回说明页）
- 英文 -> “PERMISSIONS / LET IT WORK / See which app is open / Show the block screen / Keep running in the background / Required on this device”意译：让应用运作，需查看前台应用、显示拦截屏、后台运行，无障碍标为必需（Step 6 权限页）
- 英文 -> “nfcGuard uses Android's Accessibility API only to see which app is in the foreground... never reads, records, or sends screen content, typed text, or any other personal data”意译：声称仅用无障碍API识别前台应用，不读取/记录/发送屏幕内容、输入文本或任何个人数据（Step 7 无障碍说明弹窗）
- 英文 -> “NFCGUARD uses this to reliably detect which app is in the foreground... does NOT read any screen content or user data”意译：声称用于可靠识别前台应用，不读取屏幕内容或用户数据（服务详情页）
- 英文 -> “Allow nfcGuard to have full control of your device? / View and control screen / View and perform actions”意译：系统警告询问是否允许nfcGuard完全控制设备，可查看并控制屏幕、代你操作（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 首屏品牌引导：NFCGUARD宣称封锁“吸引你的应用”，用实体标签锁住、需要时再刷开；点击NEXT进入下一页。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 模式页：列出DEEP WORK封锁7个应用、绑定厨房标签及手动NFC解锁，含ACTIVE/PAUSED；点NEXT继续。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 日程页：WORK HOURS周一至周五09:00-17:00自动生效，另列DEEP WORK可编辑删除；点击NEXT进入下一引导页。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | NFC标签页：显示“点按解锁/已解锁”，以实体标签控制开关；目前仅BACK/NEXT，点击NEXT继续引导。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 找回说明页：称丢标签仍可用SAFE REGIME，需留屏按时点按；展示挑战失败/重试与走开将重来；点NEXT。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 权限页：要求USAGE ACCESS查看前台应用、DISPLAY OVER APPS显示拦截屏、BATTERY后台运行及ACCESSIBILITY必需；点击ACCESSIBILITY旁GRANT。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 无障碍说明弹窗：声称仅用无障碍API识别前台应用以即时关闭被拦应用，不读取/发送屏幕内容或个人数据；点ALLOW。 | `step_07_action.png` |
| 8 | **Step 8: [无障碍列表页]** | 系统无障碍列表页：DOWNLOADED APPS下nfcGuard为Off；采集到无障碍设置钩子与探针后自动终止，无通知/遮罩。 | `step_08_screen.png` |
| 9 | **跳后探针 +0.8s** | 跳转后0.8秒探针：停留在系统无障碍设置页，UI文本为空，overlays=0，无通知横幅或遮罩；等待观察。 | `step_08_probe_800ms_screen.png` |
| 10 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍在系统无障碍设置页，UI为空，overlays=0，无通知或遮罩；等待未触发新界面。 | `step_08_probe_2000ms_screen.png` |
| 11 | **服务详情页** | nfcGuard服务详情页：开启“Use nfcGuard”，含快捷方式Off与说明，称仅为可靠识别前台应用，不读屏幕或用户数据。 | `step_08_service_detail_screen.png` |
| 12 | **系统警告弹窗(点Deny)** | 系统高风险警告弹窗：询问是否允许nfcGuard完全控制设备，列可查看/控制屏幕与代操作；本步检查弹窗，未点Allow/Deny。 | `step_08_system_warning_screen.png` |
| 13 | **拒权返回 +2.0s** | 拒权返回2秒：按Back拒绝后回到PERMISSIONS权限页，仍列USAGE/OVERLAY/BATTERY授权；状态为困在诱导页。 | `step_08_refusal_2000ms_screen.png` |
| 14 | **拒权返回 +10.5s** | 拒权返回10.5秒：仍停在PERMISSIONS权限页，无新增弹窗或通知，GRANT持续可见；状态为困在诱导页。 | `step_08_refusal_10500ms_screen.png` |

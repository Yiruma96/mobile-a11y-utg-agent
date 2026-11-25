# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:45:53
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.trybirdpene`（静态标签：`malicious` / `Coper` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 60 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 59 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [540, 155] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.calendar` / `WhatsNewFullScreen` | `-` | 5 | 51 / 否 | `click` → [540, 155] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.trybirdpene` / `p084d` | `-` | 1 | 0 / 是 | `click` → [540, 878] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.trybirdpene` / `p084d` | `-` | 8 | 74 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.trybirdpene` / `p084d` | `-` | 8 | 74 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.trybirdpene` / `p084d` | `-` | 8 | 74 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Chrome to make and manage phone calls?` | `Allow` | `Deny`
- **Step 2 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Chrome to send and view SMS messages?` | `Allow` | `Deny`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.calendar/WhatsNewFullScreen`)**: `Google Calendar` | `Make the most of every day.` | `next page`
- **Step 5 (`com.trybirdpene/p084d`)**: (空文本)
- **Step 6 (`com.trybirdpene/p084d`)**: `Enable Accessibility Service` | `•` | `Find` | `'Google Chrome'` | `Set switch ON` | `Open Settings`
- **Step 7 (`com.trybirdpene/p084d`)**: `Enable Accessibility Service` | `•` | `Find` | `'Google Chrome'` | `Set switch ON` | `Open Settings`
- **Step 8 (`com.trybirdpene/p084d`)**: `Enable Accessibility Service` | `•` | `Find` | `'Google Chrome'` | `Set switch ON` | `Open Settings`

## 中文逐页引导链路解读

> **全链路总结**：该应用先诱导用户为Google Chrome授予电话和短信权限，再通过土耳其语“启用服务/Google Chrome”通知横幅反复诱导点击，并多次展示“启用无障碍服务、找到Google Chrome并打开开关”的指引页，试图引导开启无障碍权限，呈现Coper典型的权限滥用与通知诱导特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Allow Google Chrome to make and manage phone calls? -> 允许Google Chrome拨打和管理电话（Step 1）
- Allow Google Chrome to send and view SMS messages? -> 允许Google Chrome发送和查看短信（Step 2）
- Servisi etkinleştirin -> 启用服务（Step 3/Step 7/Step 8通知横幅）
- Enable Accessibility Service -> 启用无障碍服务（Step 6/Step 7/Step 8）
- Find 'Google Chrome' -> 找到“Google Chrome”（Step 6/Step 7/Step 8）
- Set switch ON -> 打开开关（Step 6/Step 7/Step 8）
- Open Settings -> 打开设置（Step 6/Step 7/Step 8）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: GrantPermissionsActivity** | 系统权限弹窗请求允许Google Chrome拨打/管理电话，仅“允许/拒绝”；探针点击“允许”放行，顶部另有Google备份通知。 | `step_01_action.png` |
| 2 | **Step 2: GrantPermissionsActivity** | 第二个系统权限弹窗请求Google Chrome收发短信，继续点击“允许”放行；顶部Google备份通知仍在。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面/应用列表页顶部出现com.trybirdpene通知“Servisi etkinleştirin/启用服务”，副文本Google Chrome；点击该横幅尝试触发无障碍引导。 | `step_03_action.png` |
| 4 | **Step 4: WhatsNewFullScreen** | Google日历欢迎页显示“Make the most of every day/充分利用每一天”，但恶意通知横幅仍置顶；探针再次点击顶部横幅，未进入日历介绍。 | `step_04_action.png` |
| 5 | **Step 5: p084d** | 应用内p084d页面，UI文本未捕获，疑为无障碍前置引导空白页；点击屏幕中部推进，顶部仅显示Google备份通知。 | `step_05_action.png` |
| 6 | **Step 6: p084d** | 应用内引导页显示“Enable Accessibility Service/启用无障碍服务”，指示找到“Google Chrome”并打开开关、点“Open Settings/打开设置”；探针静态跳转p098p。 | `step_06_screen.png` |
| 7 | **Step 7: p084d** | 同一无障碍引导页再次出现，顶部新增“Servisi etkinleştirin/启用服务”通知；探针静态跳转p067f，持续施压开启无障碍。 | `step_07_screen.png` |
| 8 | **Step 8: p084d** | 同一无障碍指引页重复显示“启用服务/找到Google Chrome/打开开关”；恶意与备份通知并存，探针静态跳转p054t。 | `step_08_screen.png` |

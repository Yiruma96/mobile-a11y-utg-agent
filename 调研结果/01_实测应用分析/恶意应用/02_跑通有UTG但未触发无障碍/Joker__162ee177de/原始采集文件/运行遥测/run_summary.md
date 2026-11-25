# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:06:50
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.anti.mysecurity`（静态标签：`malicious` / `Joker` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.anti.mysecurity` / `WelcomeActivity` | `-` | 8 | 302 / 否 | `click` → [4] Button text="START" id=start_btn (click) center=(54 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 58 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 65 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.anti.mysecurity` / `FindActivity` | `-` | 3 | 44 / 否 | `click` → [3] Button text="GO SET" id=button1 (click) center=(874 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings$NotificationAccessSettingsActivity` | `-` | 12 | 100 / 否 | `click` → [1] ImageButton desc="Back" (click) center=(77,160) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.anti.mysecurity` / `FindActivity` | `-` | 3 | 44 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.anti.mysecurity` / `FindActivity` | `-` | 3 | 44 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.anti.mysecurity` / `FindActivity` | `-` | 3 | 44 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.anti.mysecurity/WelcomeActivity`)**: `Antivirus Security` | `Protect your phone` | `By clicking START,you agree to our  Terms of Service  a` | `START` | `Privacy Policy` | `Terms of Service`
- **Step 2 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Antivirus Security to access your contacts?` | `Allow` | `Deny`
- **Step 3 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Antivirus Security to make and manage phone calls` | `Allow` | `Deny`
- **Step 4 (`com.anti.mysecurity/FindActivity`)**: `Warn` | `Please open this necessary access.` | `GO SET`
- **Step 5 (`com.android.settings/Settings$NotificationAccessSettingsActivity`)**: `Back` | `Notification access` | `Search settings` | `Android Auto` | `Not allowed` | `Antivirus Security` | `Pixel Launcher` | `Allowed`
- **Step 6 (`com.anti.mysecurity/FindActivity`)**: `Warn` | `Please open this necessary access.` | `GO SET`
- **Step 7 (`com.anti.mysecurity/FindActivity`)**: `Warn` | `Please open this necessary access.` | `GO SET`
- **Step 8 (`com.anti.mysecurity/FindActivity`)**: `Warn` | `Please open this necessary access.` | `GO SET`

## 中文逐页引导链路解读

> **全链路总结**：该应用先以“杀毒安全、保护手机”的欢迎页建立信任，点击START后连续索取联系人和电话权限，再用“必要访问”警告页反复引导用户去设置；探针还静态跳转到权限引导、欢迎页和垃圾清理页，全程未见通知横幅或遮罩，具有典型Joker诱导授权特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文“Antivirus Security / Protect your phone” -> “杀毒安全/保护你的手机”（Step1 欢迎页），以安全名义建立可信度。
- 英文“By clicking START,you agree to our Terms of Service and Privacy Policy... device information and applications usage behavior...” -> “点击START即同意条款与隐私政策，并可能使用设备信息与应用使用行为以提供更好服务”（Step1 欢迎页），用合规长文弱化授权。
- 英文“START” -> “开始”（Step1 欢迎页），诱导继续进入授权流程。
- 英文“Allow Antivirus Security to access your contacts?” -> “允许杀毒安全访问联系人？”（Step2 系统权限弹窗），索取通讯录权限。
- 英文“Allow Antivirus Security to make and manage phone calls?” -> “允许杀毒安全拨打和管理电话？”（Step3 系统权限弹窗），索取电话权限。
- 英文“Warn / Please open this necessary access. / GO SET” -> “警告/请开启此必要访问/去设置”（Step4、Step6-Step8 警告页），以“必要访问”施压并引导设置。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: WelcomeActivity** | 欢迎页：英文自称“杀毒安全、保护手机”并以条款铺垫；点击START继续，未发现通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: GrantPermissionsActivity** | 系统联系人授权弹窗：英文询问是否允许访问联系人；本步点击Allow放行，界面无通知横幅或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: GrantPermissionsActivity** | 系统电话授权弹窗：英文询问是否允许拨打和管理电话；点击Allow放行，继续预授权流程，无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: FindActivity** | 应用内警告页：英文提示“警告/请开启必要访问”，GO SET意为“去设置”；点击后跳转设置页，无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: Settings$NotificationAcces** | 系统通知使用权页：显示Antivirus Security等应用及允许状态；英文Back意为返回；本步点击返回，未完成该授权。 | `step_05_action.png` |
| 6 | **Step 6: FindActivity** | 仍为应用内警告页“警告/请开启必要访问/去设置”；探针静态跳转至PermissionGuideActivity，无通知或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: FindActivity** | 仍为应用内警告页，英文要求开启“必要访问”并点GO SET；探针静态跳转至WelcomeActivity，界面未变、无遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: FindActivity** | 仍为应用内警告页，英文称“必要访问”并引导GO SET；探针静态跳转至JunkCleanActivity，界面未变、无遮罩。 | `step_08_screen.png` |

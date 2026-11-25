# BN_062__8254059c4e｜远程协助与跨设备互联 — MX3 Button Mapper

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：149.5s

## 1. 一句话核心结论

- **核心申请方式**：应用在主页以明文披露弹窗（Agree / No thanks）说明无障碍用途，用户同意后优先通过 Shizuku 特权 shell 静默写入 enabled_accessibility_services 开启自身服务，同时保留手动跳系统无障碍设置的入口，拒绝即安全降级不做任何重试。
- **静态可见性说明**：全部关键逻辑静态可见：Manifest、res/xml/accessibility_service_config.xml、strings.xml 披露文案、MainActivity/yn/g5/sn/KeyInjectorUserService 反编译均完整；无加壳、无 VMP、无远端 HTML、无加密载荷。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `8254059c4efd18de6e2afc45b3556119cebb5657457bbdabb358c102c0711ed4` |
| 包名 / 年份 | `com.odiousapps.mx3buttonmapper` / 2025-2026 |
| 家族 / 品类 | **远程协助与跨设备互联**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.odiousapps.mx3buttonmapper_56.apk |
| 桌面显示名 | MX3 Button Mapper |
| 引导页宣称品牌/身份 | MX3 Button Mapper（F-Droid 开源按键重映射工具，真实身份，未冒充系统或其他品牌） |
| 系统无障碍列表服务名 | MX3 Button Mapper |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。服务 label 与 app_name 一致；accessibility_service_config 未设置 android:isAccessibilityTool（不伪造系统工具标记）；无 activity-alias 伪装、无空白/换行挤出、无同形字。 |
| 无障碍服务类名 | `com.odiousapps.mx3buttonmapper.ButtonMapperService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |
| 系统设置项说明 (`android:description`) | Listens for specific hardware button presses on your remote and remaps them to another key or app, and notes which app is on screen so the same button can behave differently in the TV app. Key presses are never stored or sent anywhere. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.odiousapps.mx3buttonmapper.MainActivity（layout/activity_main.xml） | onCreate：setContentView 后渲染主页；若 Shizuku 已授权则绑定 UserService 并调用 n() | 原生Activity | **原文**：Grant %1$s permission, then enable this service under Accessibility（%1$s = Shizuku）；按钮 Open Accessibility Settings / Paste / Save / Language<br>**译注**：授予 Shizuku 权限，然后在“无障碍”中启用此服务；页面提供“打开无障碍设置”“粘贴”“保存”“语言”按钮 | 自行安装并授权 Shizuku、粘贴 auth token，或点击“打开无障碍设置”手动开启；无强制阻断 | `MainActivity.onCreate → setText(getString(0x7f0d0049, getString(0x7f0d0043)))` |
| 2 | 跳无障碍设置 | 系统设置 → 无障碍（android.settings.ACCESSIBILITY_SETTINGS） | 用户点击 openAccessibilitySettingsButton 按钮（setOnClickListener(new sn(this, (byte)0))） | 系统无障碍页 | **原文**：Open Accessibility Settings<br>**译注**：打开无障碍设置（按钮文案） | 在系统无障碍列表中找到 “MX3 Button Mapper” 并手动开启；用户可直接返回，无回跳循环 | `sn.onClick case 0 → startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` |
| 3 | 业务功能触发 | MainActivity.n() → yn(byte 0) 协程读取本地已同意标志（d7.a / DataStore） | Shizuku 授权/服务连接回调 rn.a，或 onCreate 中 Shizuku 已授权分支调用 n() | 原生Activity | **原文**：无（后台协程读取同意状态，无界面）<br>**译注**：无界面，读取“用户是否已同意无障碍披露”的本地标志 | 无需操作（前置条件为 Shizuku 已安装并授权） | `MainActivity.n → yn.n case 0 → t10.m(n6(...), this)` |
| 4 | 引导说明页 | 原生 AlertDialog（AlertDialog.Builder，不可点外部取消） | 同意标志为 false 时由 yn.n 弹出 | 原生Dialog | **原文**：Accessibility service / MX3 Button Mapper uses Android’s Accessibility Service API to remap your remote’s buttons. When enabled, it: • Reads the hardware button presses from your remote... It does not read screen content, text, or passwords... never shared or sent off the device. This app has no internet access. If you agree, the app will use Shizuku to turn on its own accessibility service for you. You can turn it off at any time in Settings → Accessibility. / Agree / No thanks<br>**译注**：标题“无障碍服务”；正文说明使用 Android 无障碍 API 重映射遥控器按键、记录前台应用名，明确声明不读取屏幕内容/文本/密码、不存储不外传、无联网权限，并声明“若同意，应用将通过 Shizuku 为你开启自身无障碍服务，可随时在设置→无障碍中关闭”；按钮为“同意”/“不用了” | 点击 Agree 同意，或点击 No thanks 拒绝（存在显式取消路径） | `yn.n case 0 → b2Var.d=getText(0x7f0d001c), b2Var.f=getString(0x7f0d001b, ...), 正按钮 0x7f0d001e(agree), 负按钮 0x7f0d0038(no_thanks), k=false` |
| 5 | 获权后动作 | Shizuku UserService com.odiousapps.mx3buttonmapper.KeyInjectorUserService（后台无界面） | 用户点 Agree → g5.onClick case 1 → yn(byte 1) 写入同意标志并再次 n() → 标志为 true 分支执行 qv.a.d(ComponentName(MainActivity, ButtonMapperService).flattenToString()) | 不可静态还原为界面（无 UI，通过 Shizuku 特权 shell 生效） | **原文**：无界面提示；日志 "ShizukuUserServiceBridge: Enabled accessibility service: <component>"<br>**译注**：无界面提示；应用以 Shizuku 身份直接写入系统设置启用自身无障碍服务，用户无需进入系统无障碍页 | 无（前置为用户已同意披露且已授权 Shizuku） | `yn.n case 0 为 true 分支 → qv.a.d(...) → KeyInjectorUserService.d(String)` |
| 6 | 拒权反馈循环 | MainActivity（无新界面） | 用户点击 No thanks → un.onClick | 原生Dialog | **原文**：无提示；日志 "Accessibility disclosure declined -- service left off"<br>**译注**：不做任何提示，服务保持关闭，不重新弹窗、不跳设置 | 无；应用安静降级，用户仍可后续手动通过“打开无障碍设置”开启 | `un.onClick → f5.b("MainActivity", "Accessibility disclosure declined -- service left off")` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 主页 statusText（layout/activity_main.xml @id/statusText）：Grant %1$s permission, then enable this service under Accessibility
- MainActivity 主页按钮文案：Open Accessibility Settings（strings open_accessibility_settings）、Paste / Save / Language
- 原生 AlertDialog（MainActivity 内，由 yn.n 构造）：标题 @string/accessibility_disclosure_title「Accessibility service」，正文 @string/accessibility_disclosure_message（多语言 100+ 语种），按钮 @string/agree / @string/no_thanks
- 系统无障碍列表项描述：res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_service_description
- Shizuku 相关引导文案：shizuku_auth_token_label / shizuku_auth_token_hint / tv_brand_label / log_key_events_label / log_remaps_label

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | MX3 Button Mapper uses Android’s Accessibility Service API to remap your remote’s buttons.<br><br>When enabled, it:<br>• Reads the hardware button presses from your remote, so it can replace specific buttons with a different key, a burst of key presses, or an app launch<br>• Notes the name of the app currently on screen, so a button (e.g. Channel Up/Down) can do something different inside the TV app<br><br>It does not read screen content, text, or passwords. Key presses and app names are only used on this device at the moment they happen. They are never stored (unless you turn on the troubleshooting logs below), and never shared or sent off the device. This app has no internet access.<br><br>If you agree, the app will use %1$s to turn on its own accessibility service for you. You can turn it off at any time in Settings → Accessibility. | MX3 Button Mapper 使用 Android 的无障碍服务 API 重映射遥控器按键。启用后，它会：• 读取遥控器硬件按键按下事件，以便把特定按键替换为其他按键、连击序列或启动某个应用；• 记录当前屏幕上的应用名称，使同一按键在电视应用中可执行不同动作。它不读取屏幕内容、文本或密码。按键与应用名仅在事件发生时于本机使用，绝不会被存储（除非你开启下方排障日志），也绝不上传或分享到设备之外。本应用没有联网权限。若你同意，应用将通过 %1$s 为你开启自身的无障碍服务。你随时可以在 设置 → 无障碍 中关闭它。 | `res/values/strings.xml → accessibility_disclosure_message` | 良性透明说明 |
| zh-Hant | MX3 Button Mapper 使用 Android 的無障礙服務（Accessibility Service）API 來重新對應遙控器的按鈕。 啟用後，它會： • 讀取遙控器的按鈕按壓動作，以便將特定按鈕替換為其他按鍵、一連串按鍵動作或啟動某個應用程式 • 記錄目前畫面上的應用程式名 | 同上披露文案的繁体中文版本：说明通过无障碍 API 重映射按键、记录当前前台应用名，用于同一按键在不同电视应用中执行不同动作。 | `res/values-b+zh+Hant/strings.xml → accessibility_disclosure_message` | 良性透明说明 |
| en | Listens for specific hardware button presses on your remote and remaps them to another key or app, and notes which app is on screen so the same button can behave differently in the TV app. Key presses are never stored or sent anywhere. | 监听遥控器特定硬件按键按下并重映射为其他按键或应用，同时记录屏幕上的应用，使同一按键在电视应用中有不同行为。按键永不被存储或外发。 | `res/values/strings.xml → accessibility_service_description（系统无障碍列表项描述）` | 良性透明说明 |
| en | Grant %1$s permission, then enable this service under Accessibility | 授予 %1$s（Shizuku）权限，然后在“无障碍”中启用此服务。 | `res/values/strings.xml → status_placeholder；MainActivity.onCreate 传入 shizuku_name` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。点 No thanks 后仅写日志 "Accessibility disclosure declined -- service left off"，不再弹窗、不跳设置、无 onResume 重跳或定时器拉起；用户仍可主动点主页“Open Accessibility Settings”手动开启。
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW 悬浮窗，无半透明遮罩，无高仿系统无障碍开关页；跳转目标为真实 android.settings.ACCESSIBILITY_SETTINGS。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。代码中不存在 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也无“右上角菜单允许受限设置”类文案；其静默启用走 Shizuku（需用户自行安装并授权），而非受限设置绕过。
- **获权后即时行为与防撤权机制**：无。获权后无 GLOBAL_ACTION_BACK/HOME 监听、无自点确认、无阻止撤权逻辑；披露文案明确告知可随时在设置→无障碍中关闭。
- **良性降级 / 替代方案**：具备：拒绝或无 Shizuku 时应用保持运行，仅按键重映射功能不可用，并保留“Open Accessibility Settings”手动开启路径与排障日志开关。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity(Intent action=android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（来自 MainActivity 的“Open Accessibility Settings”按钮），以及 Shizuku 授权回调后 MainActivity.n() 触发原生 AlertDialog 弹出的瞬间（标题“Accessibility service”，按钮 Agree / No thanks）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：纯 UTG 的盲区：静默启用路径（Shizuku shell 写 settings）无任何 UI，UTG 页面流转完全看不到；需辅以 settings get secure enabled_accessibility_services 与 logcat 观测。另该应用未设置 isAccessibilityTool，系统会显示常规警示，属正常表现，不应误判为伪装。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/按需引导弹窗页（无障碍披露）** | 原生 AlertDialog，标题 "Accessibility service"，正文含 "MX3 Button Mapper uses Android’s Accessibility Service API"，按钮 "Agree" / "No thanks" | 该弹窗是唯一一处无障碍用途告知，其是否可取消、是否含恐吓/伪装话术、是否要求进入受限设置，是区分诱导与透明披露的核心判据 | 是否存在 No thanks/取消按钮及其可用性；标题与正文是否与真实服务名一致（MX3 Button Mapper）；是否出现“系统故障/安全风险/必须开启”类话术；是否引导进入应用详情页开启受限设置 |
| **系统无障碍服务列表项** | Settings → Accessibility 中条目 "MX3 Button Mapper"，描述为 accessibility_service_description 原文 | 核对 label/描述与 app 真实身份是否一致、是否为伪造 isAccessibilityTool 的“系统工具”条目 | 条目显示名与包名/应用名一致；描述文本与 strings 资源一致；无“系统服务/安全组件”等冒充性命名 |
| **点 Agree 后的系统设置状态变化页** | Shizuku 授权完成后，无障碍服务由关闭变为开启，但用户未进入系统无障碍页 | 识别 Shizuku 旁路静默启用这一能力特征（非诱导，但为审计关键事实） | enabled_accessibility_services 中出现 com.odiousapps.mx3buttonmapper/.ButtonMapperService；当前前台页面不是系统无障碍设置页；logcat 出现 ShizukuUserServiceBridge: Enabled accessibility service |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.odiousapps.mx3buttonmapper.MainActivity#onCreate`
- `com.odiousapps.mx3buttonmapper.MainActivity#n`
- `yn#n（披露 AlertDialog 构造与 Shizuku 启用分支）`
- `g5#onClick（Agree → 写同意标志 → 再次 n()）`
- `com.odiousapps.mx3buttonmapper.KeyInjectorUserService#d`
- `res/values/strings.xml#accessibility_disclosure_message`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**性质判定：良性、透明，且无诱导伪装。** 未发现任何常见诱导手法（无不可取消的强制弹窗、无拒绝后循环重跳、无悬浮遮罩、无仿冒系统页、无受限设置分步教学、无获权后阻止撤权）。

**关键机制（值得注意但已如实披露）**
- 无障碍服务为 [ButtonMapperService](<resource-unit:#1.dex1 code:com.odiousapps.mx3buttonmapper.ButtonMapperService>)，配置仅 `typeWindowStateChanged` + `flagRequestFilterKeyEvents`，`canRetrieveWindowContent="false"`，与"只做按键重映射"的声明一致；未设置 `isAccessibilityTool`（非伪造）。
- 应用提供两条获权路径：①**手动路径**：主页"Open Accessibility Settings"按钮经 [sn.onClick](<resource-unit:#1.dex1 code:sn#onClick>) 直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，无遮罩、无回跳；②**Shizuku 静默启用路径**：用户同意披露弹窗后，经 Shizuku UserService 执行 `settings put secure enabled_accessibility_services` / `accessibility_enabled 1`，**跳过系统无障碍页的人工开关**——但该行为在披露文本中原文写明（"the app will use %1$s to turn on its own accessibility service for you"），且需用户自行安装并授权 Shizuku。
- 披露弹窗为原生 AlertDialog，**带 "No thanks" 取消按钮**（`b2Var.k=false` 不可点外部取消，但显式提供否定按钮），拒绝后仅记录日志 `"Accessibility disclosure declined -- service left off"`，无重新拉起。
- 未出现 `ACTION_APPLICATION_DETAILS_SETTINGS`、`isAccessibilityTool` 伪造、`enabled_accessibility_services` 之外的隐蔽改写；无 INTERNET 权限，隐私承诺（不上传、不存储）与 Manifest 相符。

**UTG 视角要点**：本应用属"用户主动触发 + 明文披露 + 可取消"型，纯 UTG 检测不应判为诱导；唯一需留意的信号是"点 Agree 后无障碍服务在用户未进入系统设置页的情况下变为启用"（Shizuku 旁路），这属于能力特征而非诱导行为。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部关键逻辑静态可见：Manifest、res/xml/accessibility_service_config.xml、strings.xml 披露文案、MainActivity/yn/g5/sn/KeyInjectorUserService 反编译均完整；无加壳、无 VMP、无远端 HTML、无加密载荷。",
  "summary_one_liner": "应用在主页以明文披露弹窗（Agree / No thanks）说明无障碍用途，用户同意后优先通过 Shizuku 特权 shell 静默写入 enabled_accessibility_services 开启自身服务，同时保留手动跳系统无障碍设置的入口，拒绝即安全降级不做任何重试。",
  "disguise_identity": {
    "app_display_name": "MX3 Button Mapper",
    "claimed_brand_or_persona": "MX3 Button Mapper（F-Droid 开源按键重映射工具，真实身份，未冒充系统或其他品牌）",
    "a11y_service_label": "MX3 Button Mapper",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。服务 label 与 app_name 一致；accessibility_service_config 未设置 android:isAccessibilityTool（不伪造系统工具标记）；无 activity-alias 伪装、无空白/换行挤出、无同形字。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.odiousapps.mx3buttonmapper.MainActivity（layout/activity_main.xml）",
      "trigger_event": "onCreate：setContentView 后渲染主页；若 Shizuku 已授权则绑定 UserService 并调用 n()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Grant %1$s permission, then enable this service under Accessibility（%1$s = Shizuku）；按钮 Open Accessibility Settings / Paste / Save / Language",
      "shown_text_zh": "授予 Shizuku 权限，然后在“无障碍”中启用此服务；页面提供“打开无障碍设置”“粘贴”“保存”“语言”按钮",
      "user_action_requested": "自行安装并授权 Shizuku、粘贴 auth token，或点击“打开无障碍设置”手动开启；无强制阻断",
      "code_anchor": "MainActivity.onCreate → setText(getString(0x7f0d0049, getString(0x7f0d0043)))"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "用户点击 openAccessibilitySettingsButton 按钮（setOnClickListener(new sn(this, (byte)0))）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Open Accessibility Settings",
      "shown_text_zh": "打开无障碍设置（按钮文案）",
      "user_action_requested": "在系统无障碍列表中找到 “MX3 Button Mapper” 并手动开启；用户可直接返回，无回跳循环",
      "code_anchor": "sn.onClick case 0 → startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity.n() → yn(byte 0) 协程读取本地已同意标志（d7.a / DataStore）",
      "trigger_event": "Shizuku 授权/服务连接回调 rn.a，或 onCreate 中 Shizuku 已授权分支调用 n()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（后台协程读取同意状态，无界面）",
      "shown_text_zh": "无界面，读取“用户是否已同意无障碍披露”的本地标志",
      "user_action_requested": "无需操作（前置条件为 Shizuku 已安装并授权）",
      "code_anchor": "MainActivity.n → yn.n case 0 → t10.m(n6(...), this)"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "原生 AlertDialog（AlertDialog.Builder，不可点外部取消）",
      "trigger_event": "同意标志为 false 时由 yn.n 弹出",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Accessibility service / MX3 Button Mapper uses Android’s Accessibility Service API to remap your remote’s buttons. When enabled, it: • Reads the hardware button presses from your remote... It does not read screen content, text, or passwords... never shared or sent off the device. This app has no internet access. If you agree, the app will use Shizuku to turn on its own accessibility service for you. You can turn it off at any time in Settings → Accessibility. / Agree / No thanks",
      "shown_text_zh": "标题“无障碍服务”；正文说明使用 Android 无障碍 API 重映射遥控器按键、记录前台应用名，明确声明不读取屏幕内容/文本/密码、不存储不外传、无联网权限，并声明“若同意，应用将通过 Shizuku 为你开启自身无障碍服务，可随时在设置→无障碍中关闭”；按钮为“同意”/“不用了”",
      "user_action_requested": "点击 Agree 同意，或点击 No thanks 拒绝（存在显式取消路径）",
      "code_anchor": "yn.n case 0 → b2Var.d=getText(0x7f0d001c), b2Var.f=getString(0x7f0d001b, ...), 正按钮 0x7f0d001e(agree), 负按钮 0x7f0d0038(no_thanks), k=false"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "Shizuku UserService com.odiousapps.mx3buttonmapper.KeyInjectorUserService（后台无界面）",
      "trigger_event": "用户点 Agree → g5.onClick case 1 → yn(byte 1) 写入同意标志并再次 n() → 标志为 true 分支执行 qv.a.d(ComponentName(MainActivity, ButtonMapperService).flattenToString())",
      "ui_carrier": "不可静态还原为界面（无 UI，通过 Shizuku 特权 shell 生效）",
      "shown_text_verbatim": "无界面提示；日志 \"ShizukuUserServiceBridge: Enabled accessibility service: <component>\"",
      "shown_text_zh": "无界面提示；应用以 Shizuku 身份直接写入系统设置启用自身无障碍服务，用户无需进入系统无障碍页",
      "user_action_requested": "无（前置为用户已同意披露且已授权 Shizuku）",
      "code_anchor": "yn.n case 0 为 true 分支 → qv.a.d(...) → KeyInjectorUserService.d(String)"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity（无新界面）",
      "trigger_event": "用户点击 No thanks → un.onClick",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "无提示；日志 \"Accessibility disclosure declined -- service left off\"",
      "shown_text_zh": "不做任何提示，服务保持关闭，不重新弹窗、不跳设置",
      "user_action_requested": "无；应用安静降级，用户仍可后续手动通过“打开无障碍设置”开启",
      "code_anchor": "un.onClick → f5.b(\"MainActivity\", \"Accessibility disclosure declined -- service left off\")"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 主页 statusText（layout/activity_main.xml @id/statusText）：Grant %1$s permission, then enable this service under Accessibility",
    "MainActivity 主页按钮文案：Open Accessibility Settings（strings open_accessibility_settings）、Paste / Save / Language",
    "原生 AlertDialog（MainActivity 内，由 yn.n 构造）：标题 @string/accessibility_disclosure_title「Accessibility service」，正文 @string/accessibility_disclosure_message（多语言 100+ 语种），按钮 @string/agree / @string/no_thanks",
    "系统无障碍列表项描述：res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_service_description",
    "Shizuku 相关引导文案：shizuku_auth_token_label / shizuku_auth_token_hint / tv_brand_label / log_key_events_label / log_remaps_label"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "MX3 Button Mapper uses Android’s Accessibility Service API to remap your remote’s buttons.\n\nWhen enabled, it:\n• Reads the hardware button presses from your remote, so it can replace specific buttons with a different key, a burst of key presses, or an app launch\n• Notes the name of the app currently on screen, so a button (e.g. Channel Up/Down) can do something different inside the TV app\n\nIt does not read screen content, text, or passwords. Key presses and app names are only used on this device at the moment they happen. They are never stored (unless you turn on the troubleshooting logs below), and never shared or sent off the device. This app has no internet access.\n\nIf you agree, the app will use %1$s to turn on its own accessibility service for you. You can turn it off at any time in Settings → Accessibility.",
      "text_zh": "MX3 Button Mapper 使用 Android 的无障碍服务 API 重映射遥控器按键。启用后，它会：• 读取遥控器硬件按键按下事件，以便把特定按键替换为其他按键、连击序列或启动某个应用；• 记录当前屏幕上的应用名称，使同一按键在电视应用中可执行不同动作。它不读取屏幕内容、文本或密码。按键与应用名仅在事件发生时于本机使用，绝不会被存储（除非你开启下方排障日志），也绝不上传或分享到设备之外。本应用没有联网权限。若你同意，应用将通过 %1$s 为你开启自身的无障碍服务。你随时可以在 设置 → 无障碍 中关闭它。",
      "source_location": "res/values/strings.xml → accessibility_disclosure_message",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh-Hant",
      "text_verbatim": "MX3 Button Mapper 使用 Android 的無障礙服務（Accessibility Service）API 來重新對應遙控器的按鈕。 啟用後，它會： • 讀取遙控器的按鈕按壓動作，以便將特定按鈕替換為其他按鍵、一連串按鍵動作或啟動某個應用程式 • 記錄目前畫面上的應用程式名",
      "text_zh": "同上披露文案的繁体中文版本：说明通过无障碍 API 重映射按键、记录当前前台应用名，用于同一按键在不同电视应用中执行不同动作。",
      "source_location": "res/values-b+zh+Hant/strings.xml → accessibility_disclosure_message",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Listens for specific hardware button presses on your remote and remaps them to another key or app, and notes which app is on screen so the same button can behave differently in the TV app. Key presses are never stored or sent anywhere.",
      "text_zh": "监听遥控器特定硬件按键按下并重映射为其他按键或应用，同时记录屏幕上的应用，使同一按键在电视应用中有不同行为。按键永不被存储或外发。",
      "source_location": "res/values/strings.xml → accessibility_service_description（系统无障碍列表项描述）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant %1$s permission, then enable this service under Accessibility",
      "text_zh": "授予 %1$s（Shizuku）权限，然后在“无障碍”中启用此服务。",
      "source_location": "res/values/strings.xml → status_placeholder；MainActivity.onCreate 传入 shizuku_name",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。点 No thanks 后仅写日志 \"Accessibility disclosure declined -- service left off\"，不再弹窗、不跳设置、无 onResume 重跳或定时器拉起；用户仍可主动点主页“Open Accessibility Settings”手动开启。",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW 悬浮窗，无半透明遮罩，无高仿系统无障碍开关页；跳转目标为真实 android.settings.ACCESSIBILITY_SETTINGS。",
    "restricted_settings_13plus_coaching": "无。代码中不存在 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也无“右上角菜单允许受限设置”类文案；其静默启用走 Shizuku（需用户自行安装并授权），而非受限设置绕过。",
    "post_grant_anti_removal": "无。获权后无 GLOBAL_ACTION_BACK/HOME 监听、无自点确认、无阻止撤权逻辑；披露文案明确告知可随时在设置→无障碍中关闭。",
    "benign_graceful_degradation": "具备：拒绝或无 Shizuku 时应用保持运行，仅按键重映射功能不可用，并保留“Open Accessibility Settings”手动开启路径与排障日志开关。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity(Intent action=android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（来自 MainActivity 的“Open Accessibility Settings”按钮），以及 Shizuku 授权回调后 MainActivity.n() 触发原生 AlertDialog 弹出的瞬间（标题“Accessibility service”，按钮 Agree / No thanks）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/按需引导弹窗页（无障碍披露）",
        "page_identifier": "原生 AlertDialog，标题 \"Accessibility service\"，正文含 \"MX3 Button Mapper uses Android’s Accessibility Service API\"，按钮 \"Agree\" / \"No thanks\"",
        "why_most_useful": "该弹窗是唯一一处无障碍用途告知，其是否可取消、是否含恐吓/伪装话术、是否要求进入受限设置，是区分诱导与透明披露的核心判据",
        "observable_utg_signals": ["是否存在 No thanks/取消按钮及其可用性", "标题与正文是否与真实服务名一致（MX3 Button Mapper）", "是否出现“系统故障/安全风险/必须开启”类话术", "是否引导进入应用详情页开启受限设置"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility 中条目 \"MX3 Button Mapper\"，描述为 accessibility_service_description 原文",
        "why_most_useful": "核对 label/描述与 app 真实身份是否一致、是否为伪造 isAccessibilityTool 的“系统工具”条目",
        "observable_utg_signals": ["条目显示名与包名/应用名一致", "描述文本与 strings 资源一致", "无“系统服务/安全组件”等冒充性命名"]
      },
      {
        "page_role": "点 Agree 后的系统设置状态变化页",
        "page_identifier": "Shizuku 授权完成后，无障碍服务由关闭变为开启，但用户未进入系统无障碍页",
        "why_most_useful": "识别 Shizuku 旁路静默启用这一能力特征（非诱导，但为审计关键事实）",
        "observable_utg_signals": ["enabled_accessibility_services 中出现 com.odiousapps.mx3buttonmapper/.ButtonMapperService", "当前前台页面不是系统无障碍设置页", "logcat 出现 ShizukuUserServiceBridge: Enabled accessibility service"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "纯 UTG 的盲区：静默启用路径（Shizuku shell 写 settings）无任何 UI，UTG 页面流转完全看不到；需辅以 settings get secure enabled_accessibility_services 与 logcat 观测。另该应用未设置 isAccessibilityTool，系统会显示常规警示，属正常表现，不应误判为伪装。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.odiousapps.mx3buttonmapper.MainActivity#onCreate",
    "com.odiousapps.mx3buttonmapper.MainActivity#n",
    "yn#n（披露 AlertDialog 构造与 Shizuku 启用分支）",
    "g5#onClick（Agree → 写同意标志 → 再次 n()）",
    "com.odiousapps.mx3buttonmapper.KeyInjectorUserService#d",
    "res/values/strings.xml#accessibility_disclosure_message"
  ]
}
```

</details>

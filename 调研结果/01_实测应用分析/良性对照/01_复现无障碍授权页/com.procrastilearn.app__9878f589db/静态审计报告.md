# BN_005__9878f589db｜专注自律与防沉迷管控 — ProcrastiLearn

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：194.8s

## 1. 一句话核心结论

- **核心申请方式**：应用以 Compose 原生披露页逐字说明无障碍用途（检测自选应用前台以弹出学习卡片）、要求勾选同意后由用户主动点击 Accept & Continue 跳转系统 ACCESSIBILITY_SETTINGS，并提供 Not now 取消与随时关闭提示，属透明良性的按需授权流程。
- **静态可见性说明**：Manifest、无障碍 XML 配置、全部引导文案（strings.xml 20+ 语言）、两处设置页跳转点（xc0.invoke / sm2.invoke）与 onResume 权限状态校验（ad2.k / j82.k / x03.B）均完整静态可见，无加壳、无加密载荷、无远端 HTML 引导页；唯一不足是 Compose UI 的 R.string 引用为整型常量，无法逐行定位到具体 Composable 函数体，但不影响行为定性。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9878f589db7378b5bfb6fdf5f0d8acfdc70f2d5900879c3202f494cf55ed7a0d` |
| 包名 / 年份 | `com.procrastilearn.app` / 2025-2026 |
| 家族 / 品类 | **专注自律与防沉迷管控**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.procrastilearn.app_22.apk |
| 桌面显示名 | ProcrastiLearn |
| 引导页宣称品牌/身份 | ProcrastiLearn（F-Droid 开源专注自律/防沉迷学习应用，真实品牌） |
| 系统无障碍列表服务名 | ProcrastiLearn（服务未声明 android:label 与 android:description，系统无障碍列表回落显示应用名，无描述文字） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。未使用 activity-alias、空白/换行挤出、同形字；未设置 isAccessibilityTool 伪造成本工具；accessibility_service_config 的 settingsActivity 为空且 canRetrieveWindowContent=false，未隐藏或美化系统提示。 |
| 无障碍服务类名 | `com.procrastilearn.app.service.OverlayAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | com.procrastilearn.app.MainActivity（Compose 首页/Settings 页中的 Learning gate 区块） | 用户开启防沉迷学习闸门功能，或在设置页点击无障碍相关开关项（settings_a11y_headline） | 原生Activity | **原文**：Learning gate (Accessibility) / Detects selected apps in foreground to trigger the learning card.<br>**译注**：学习闸门（无障碍）/ 检测前台被选中的应用以触发学习卡片。 | 用户点击开关/入口进入无障碍说明页，可随时返回不开启 | `res/values/strings.xml (settings_a11y_headline, settings_a11y_support)；MainActivity` |
| 2 | 引导说明页 | MainActivity 内 Compose 无障碍披露页（a11y_disclosure_* 文案组） | 进入披露页（Composable 渲染，显示前需勾选同意复选框） | 原生Activity | **原文**：Why we need Accessibility / This app uses Android Accessibility Service permission to detect when you open selected apps (e.g., TikTok, Reddit or any other app you choose) so it can show a short learning prompt before you continue. / What we access: • Which app is currently on your screen. • We do NOT read your passwords, messages, or on-screen text. • Your data never leaves your device and is never sold or shared. / How it's used: Only to trigger the learning overlay for the apps you selected. You can turn this off anytime in Settings. We don't sell or share this data, it never leaves your device. / I understand and agree to allow this app to use the Accessibility Service permission for this purpose. / Accept & Continue / Not now<br>**译注**：为什么需要无障碍权限 / 本应用使用 Android 无障碍服务权限，用于检测你何时打开所选应用（例如 TikTok、Reddit 或你选择的任何其他应用），以便在你继续之前显示一个简短的学习提示。/ 我们访问什么：• 你当前屏幕上的是哪个应用。• 我们不会读取你的密码、消息或屏幕文本。• 你的数据永不离开设备，绝不出售或共享。/ 如何使用：仅用于为你选中的应用触发学习遮罩。你随时可以在设置中关闭。我们不出售也不共享这些数据，它永不离开你的设备。/ 我理解并同意允许本应用为此目的使用无障碍服务权限。/ 接受并继续 / 暂不 | 先勾选同意复选框，再点击 Accept & Continue；亦可点击 Not now 取消，无强制循环 | `res/values/strings.xml (a11y_disclosure_title / _description / _access_details / _usage_details / _checkbox / _accept / _decline)` |
| 3 | 跳无障碍设置 | 系统设置 → 无障碍 → 已安装的服务（ProcrastiLearn） | 用户点击 Accept & Continue 后触发 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：无（应用侧仅发送标准 Intent，页面由系统渲染；系统条目无 android:description 描述文本）<br>**译注**：跳转至系统无障碍服务列表，由用户在系统页内手动开启 ProcrastiLearn 服务 | 用户在系统页手动找到 ProcrastiLearn 并打开开关；可随时返回，应用不拦截 | `xc0.invoke (case 5)、sm2.invoke (case 2)` |
| 4 | 拒权反馈循环 | MainActivity onResume 权限状态校验（LifecycleEventObserver） | 从系统设置返回触发 ON_RESUME | 原生Activity | **原文**：无（仅刷新 overlayGranted / a11yEnabled 状态并更新界面开关，未弹出二次索取弹窗）<br>**译注**：返回应用后仅重新读取 Settings.Secure 的 enabled_accessibility_services 与 canDrawOverlays 刷新状态，未获权则保持未开启状态，不重复强制跳转 | 无强制操作；用户可放弃，功能保持未启用（安全降级） | `ad2.k / j82.k / x03.B` |
| 5 | 获权后动作 | OverlayAccessibilityService + 悬浮窗学习卡片（WindowManager overlay） | onServiceConnected 注册 SCREEN_ON/OFF/USER_PRESENT 广播并启动协程；onAccessibilityEvent 收到 TYPE_WINDOW_STATE_CHANGED 且包名为用户所选应用 | 悬浮窗Overlay | **原文**：无（学习卡片内容来自用户自建词库；相关文案：Could not load the next card. / Loading next card… / Show overlay each X minutes while blocked app is open）<br>**译注**：检测到用户打开被管控应用时，叠加学习卡片遮罩，要求完成间隔重复复习后才可继续使用 | 用户完成/关闭学习卡片；不读取屏幕文本内容（canRetrieveWindowContent=false） | `com.procrastilearn.app.service.OverlayAccessibilityService.onServiceConnected / onAccessibilityEvent` |
| 6 | 跳受限设置 | 系统设置 → 显示在其他应用上层（悬浮窗权限页） | 悬浮窗权限未授予时，由用户操作触发 startActivity(new Intent("android.settings.action.MANAGE_OVERLAY_PERMISSION", package:...)) | 系统无障碍页 | **原文**：Allow overlay display / This app needs permission to display an overlay over other apps.<br>**译注**：允许显示悬浮窗 / 本应用需要权限才能在其他应用之上显示悬浮窗。 | 用户在系统页手动允许悬浮窗权限，可拒绝 | `xc0.invoke (default 分支)、sm2.invoke (case 1)；strings.xml overlay_permission_title / overlay_permission_message` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 内 Compose 原生无障碍披露页：标题 Why we need Accessibility、What we access / How it's used 两段正文、隐私承诺、同意复选框、Accept & Continue 与 Not now 按钮（res/values/strings.xml 的 a11y_disclosure_* 组）
- 设置页 Learning gate (Accessibility) 区块：settings_a11y_headline 与 settings_a11y_support 摘要说明
- 悬浮窗权限说明：overlay_permission_title / overlay_permission_message，配合跳转 ACTION_MANAGE_OVERLAY_PERMISSION
- 系统无障碍列表条目：因 accessibility_service_config.xml 未声明 android:description 与 service android:label，系统仅显示应用名 ProcrastiLearn，无自定义描述文字（不构成伪装，也不构成欺骗性说明）
- Manifest 未声明 android:description 等无源文本；未使用 WebView 或 assets HTML 承载任何引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Why we need Accessibility | 为什么我们需要无障碍权限 | `res/values/strings.xml key=a11y_disclosure_title` | 良性透明说明 |
| en | This app uses Android Accessibility Service permission to detect when you open selected apps (e.g., TikTok, Reddit or any other app you choose) so it can show a short learning prompt before you continue. | 本应用使用 Android 无障碍服务权限，检测你何时打开所选应用（例如 TikTok、Reddit 或你选择的任何其他应用），以便在你继续之前显示一个简短的学习提示。 | `res/values/strings.xml key=a11y_disclosure_description` | 良性透明说明 |
| en | • Which app is currently on your screen.<br> • We do NOT read your passwords, messages, or on-screen text.<br> • Your data never leaves your device and is never sold or shared. | • 你当前屏幕上的是哪个应用。• 我们不会读取你的密码、消息或屏幕文本。• 你的数据永不离开设备，绝不出售或共享。 | `res/values/strings.xml key=a11y_disclosure_access_details` | 隐私承诺 |
| en | Only to trigger the learning overlay for the apps you selected. You can turn this off anytime in Settings. We don’t sell or share this data, it never leaves your device. | 仅用于为你选中的应用触发学习遮罩。你随时可以在设置中关闭。我们不出售也不共享这些数据，它永不离开你的设备。 | `res/values/strings.xml key=a11y_disclosure_usage_details` | 良性透明说明 |
| en | I understand and agree to allow this app to use the Accessibility Service permission for this purpose. | 我理解并同意允许本应用为此目的使用无障碍服务权限。 | `res/values/strings.xml key=a11y_disclosure_checkbox` | 良性透明说明 |
| en | Accept & Continue | 接受并继续 | `res/values/strings.xml key=a11y_disclosure_accept` | 良性透明说明 |
| en | Not now | 暂不 | `res/values/strings.xml key=a11y_disclosure_decline → @string/action_not_now` | 良性透明说明 |
| en | Learning gate (Accessibility) — Detects selected apps in foreground to trigger the learning card. | 学习闸门（无障碍）—— 检测前台被选中的应用以触发学习卡片。 | `res/values/strings.xml key=settings_a11y_headline / settings_a11y_support` | 良性透明说明 |
| en | Allow overlay display — This app needs permission to display an overlay over other apps. | 允许显示悬浮窗 —— 本应用需要权限才能在其他应用之上显示悬浮窗。 | `res/values/strings.xml key=overlay_permission_title / overlay_permission_message` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无强制循环。从系统设置返回后仅在 ON_RESUME 读取 Settings.Secure."enabled_accessibility_services" 与 Settings.canDrawOverlays 刷新状态（ad2.k / j82.k / x03.B），未获权则保持关闭状态，不重新弹出索取弹窗、不重复跳转、无定时器拉起。
- **遮罩叠层 / 高仿系统设置页**：无。未叠放半透明引导遮罩、无全屏悬浮窗覆盖系统设置页、无高仿系统无障碍开关页；悬浮窗仅用于学习卡片业务功能。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未出现教用户进入应用详情右上角菜单允许受限设置的文案或分步教学；且未设置 isAccessibilityTool 伪造归类，系统侧会如实提示受限设置风险。
- **获权后即时行为与防撤权机制**：无。未监听设置页做 GLOBAL_ACTION_BACK/HOME，未自点确认、无防撤权逻辑；onAccessibilityEvent 只处理 TYPE_WINDOW_STATE_CHANGED 的包名，未读取节点内容。
- **良性降级 / 替代方案**：用户点击 Not now 或直接返回即保持功能未启用；文案明确 "You can turn this off anytime in Settings"，可随时关闭无障碍服务而应用不拦截。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.action.MANAGE_OVERLAY_PERMISSION 的瞬间抓取；其次在 MainActivity 首次渲染无障碍披露页（出现 Accept & Continue 文本节点）时抓取。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在轻微盲区：引导页文案在 Compose 中以 R.string 整型常量引用，纯静态无法逐行定位到具体 Composable 函数体，需运行期 UTG 文本节点确认渲染完整性；未发现纯图空文本、温和外壳、一阶段 Dropper 或静态加壳等实质盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **引导说明页（无障碍披露页）** | com.procrastilearn.app.MainActivity，页面含标题 "Why we need Accessibility"、同意复选框与 "Accept & Continue" / "Not now" 按钮 | 该页是本应用索取无障碍权限的唯一说明载体，可直接判断是否存在虚假用途陈述、隐私承诺过度、隐藏取消按钮或强制勾选陷阱 | 标题与正文是否与 Manifest/配置声明用途一致；是否存在可点击的 Not now / 返回按钮；同意复选框是否可跳过；是否出现故障恐吓、假更新、假安全等诱导话术 |
| **系统无障碍服务列表项** | 系统设置 → 无障碍 → 已下载的服务中的 ProcrastiLearn 条目（无描述文本） | 核验系统侧展示的服务名与描述是否与应用宣称一致，以及是否被伪造为系统/工具类组件 | 条目显示名是否为 ProcrastiLearn；描述栏是否为空（对应无 android:description）；是否出现"受限设置"提示（对应未伪造 isAccessibilityTool） |
| **跳转系统设置返回后的应用界面** | com.procrastilearn.app.MainActivity 返回态（Learning gate 开关状态） | 验证拒权后是否存在二次索取弹窗、自动重跳或恐吓提示，是区分良性降级与强制诱导的关键观测点 | 返回后是否立即再次拉起设置页；是否出现不可取消的索取弹窗；开关是否如实保持关闭状态 |
| **获权后的学习卡片遮罩页** | 覆盖在被管控应用上的学习卡片悬浮窗（含 0/1 进度、Rating 交互） | 确认无障碍权限的实际用途与宣称一致（仅检测前台包名并显示学习卡片），排除后台窃取窗口内容或静默操作其他应用 | 遮罩是否仅覆盖被选应用且可退出；是否出现读取其他应用界面文本或自动点击行为；是否请求无关权限或外发数据 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `xc0.invoke（case 5 跳 android.settings.ACCESSIBILITY_SETTINGS，default 跳 MANAGE_OVERLAY_PERMISSION）`
- `sm2.invoke（case 2 跳 android.settings.ACCESSIBILITY_SETTINGS）`
- `x03.B（读取 Settings.Secure.enabled_accessibility_services 判定服务是否启用）`
- `ad2.k / j82.k（ON_RESUME 刷新 a11yEnabled 与 canDrawOverlays，无强制重跳）`
- `com.procrastilearn.app.service.OverlayAccessibilityService.onAccessibilityEvent（仅取 TYPE_WINDOW_STATE_CHANGED 包名，跳过输入法与自身）`
- `res/xml/accessibility_service_config.xml（canRetrieveWindowContent=false、无 description、settingsActivity 为空）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，已收敛）

**结论：未发现诱导/欺诈式无障碍授权链。这是一个透明的说明页 + 用户主动点击 + 跳系统设置页的良性流程。**

关键事实链：

1. **Manifest 层面**：`OverlayAccessibilityService` 正常声明 `BIND_ACCESSIBILITY_SERVICE`，只有 `SYSTEM_ALERT_WINDOW` + `INTERNET` + `ACCESS_NETWORK_STATE`，无 QUERY_ALL_PACKAGES、无自升级、无 `activity-alias` 伪装，应用名 `@string/app_name`（ProcrastiLearn）与服务同一品牌。
2. **无障碍配置透明且最小化**：[accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml#L2-L3>) 仅 `typeWindowStateChanged`、`canRetrieveWindowContent="false"`、`feedbackGeneric`、`settingsActivity=""`，**未声明 `android:description`，也未伪造 `isAccessibilityTool`**（因此 Android 13+ 系统会如实显示"受限设置"提示，不存在欺骗系统归类的手法）。
3. **引导文字是逐字诚实披露**：`res/values/strings.xml` 中 `a11y_disclosure_*` 系列（Why we need Accessibility / What we access / How it's used / 隐私承诺 / 勾选同意 / Accept & Continue / Not now），说明用途是"检测你打开的自选应用以弹出学习卡片"，明确"不读取密码、消息、屏幕文本"，并明确"可随时在设置关闭"。共 20+ 语言本地化，属正规开源产品文案。
4. **跳转点唯一且为显式用户点击**：[xc0.invoke()](<resource-unit:#1.dex1 code:xc0#invoke>) 的 `case 5` 与 [sm2.invoke()](<resource-unit:#1.dex1 code:sm2#invoke>) 的 `case 2` 各自 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`；同处另有 `ACTION_MANAGE_OVERLAY_PERMISSION`（悬浮窗授权），均为标准系统页，**无高仿设置页、无半透明遮罩压栈**。
5. **无拒绝循环**：返回应用后 [ad2.k()](<resource-unit:#1.dex1 code:ad2#k>) / [j82.k()](<resource-unit:#1.dex1 code:j82#k>) 仅在 `ON_RESUME` 时通过 [x03.B()](<resource-unit:#1.dex1 code:x03#B>) 读取 `Settings.Secure."enabled_accessibility_services"` 刷新状态位（并在新获权时触发一次性刷新协程），**不存在 Timer 重跳或 onResume 死循环**。
6. **获权后行为与宣称一致**：`onAccessibilityEvent` 只处理 `TYPE_WINDOW_STATE_CHANGED` 的包名，跳过输入法与本应用，不取节点文本，仅用于触发学习卡片遮罩——符合"防沉迷 gate"真实功能，非窃密/键盘记录。

**覆盖边界**：Compose UI 的字符串引用为 R 常量整型，无法逐行定位到具体 Composable 函数体；引导页文案载体已由 `strings.xml` 与 `a11y_disclosure_*` 键证实，页面实现属 Compose 原生页面（非 WebView、非远端 HTML）。未做动态验证。

```json
{
  "static_visibility": "clear",
  "visibility_note": "Manifest、无障碍 XML 配置、全部引导文案（strings.xml 20+ 语言）、两处设置页跳转点（xc0.invoke / sm2.invoke）与 onResume 权限状态校验（ad2.k / j82.k / x03.B）均完整静态可见，无加壳、无加密载荷、无远端 HTML 引导页；唯一不足是 Compose UI 的 R.string 引用为整型常量，无法逐行定位到具体 Composable 函数体，但不影响行为定性。",
  "summary_one_liner": "应用以 Compose 原生披露页逐字说明无障碍用途（检测自选应用前台以弹出学习卡片）、要求勾选同意后由用户主动点击 Accept & Continue 跳转系统 ACCESSIBILITY_SETTINGS，并提供 Not now 取消与随时关闭提示，属透明良性的按需授权流程。",
  "disguise_identity": {
    "app_display_name": "ProcrastiLearn",
    "claimed_brand_or_persona": "ProcrastiLearn（F-Droid 开源专注自律/防沉迷学习应用，真实品牌）",
    "a11y_service_label": "ProcrastiLearn（服务未声明 android:label 与 android:description，系统无障碍列表回落显示应用名，无描述文字）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。未使用 activity-alias、空白/换行挤出、同形字；未设置 isAccessibilityTool 伪造成本工具；accessibility_service_config 的 settingsActivity 为空且 canRetrieveWindowContent=false，未隐藏或美化系统提示。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "com.procrastilearn.app.MainActivity（Compose 首页/Settings 页中的 Learning gate 区块）",
      "trigger_event": "用户开启防沉迷学习闸门功能，或在设置页点击无障碍相关开关项（settings_a11y_headline）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Learning gate (Accessibility) / Detects selected apps in foreground to trigger the learning card.",
      "shown_text_zh": "学习闸门（无障碍）/ 检测前台被选中的应用以触发学习卡片。",
      "user_action_requested": "用户点击开关/入口进入无障碍说明页，可随时返回不开启",
      "code_anchor": "res/values/strings.xml (settings_a11y_headline, settings_a11y_support)；MainActivity"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity 内 Compose 无障碍披露页（a11y_disclosure_* 文案组）",
      "trigger_event": "进入披露页（Composable 渲染，显示前需勾选同意复选框）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Why we need Accessibility / This app uses Android Accessibility Service permission to detect when you open selected apps (e.g., TikTok, Reddit or any other app you choose) so it can show a short learning prompt before you continue. / What we access: • Which app is currently on your screen. • We do NOT read your passwords, messages, or on-screen text. • Your data never leaves your device and is never sold or shared. / How it's used: Only to trigger the learning overlay for the apps you selected. You can turn this off anytime in Settings. We don't sell or share this data, it never leaves your device. / I understand and agree to allow this app to use the Accessibility Service permission for this purpose. / Accept & Continue / Not now",
      "shown_text_zh": "为什么需要无障碍权限 / 本应用使用 Android 无障碍服务权限，用于检测你何时打开所选应用（例如 TikTok、Reddit 或你选择的任何其他应用），以便在你继续之前显示一个简短的学习提示。/ 我们访问什么：• 你当前屏幕上的是哪个应用。• 我们不会读取你的密码、消息或屏幕文本。• 你的数据永不离开设备，绝不出售或共享。/ 如何使用：仅用于为你选中的应用触发学习遮罩。你随时可以在设置中关闭。我们不出售也不共享这些数据，它永不离开你的设备。/ 我理解并同意允许本应用为此目的使用无障碍服务权限。/ 接受并继续 / 暂不",
      "user_action_requested": "先勾选同意复选框，再点击 Accept & Continue；亦可点击 Not now 取消，无强制循环",
      "code_anchor": "res/values/strings.xml (a11y_disclosure_title / _description / _access_details / _usage_details / _checkbox / _accept / _decline)"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已安装的服务（ProcrastiLearn）",
      "trigger_event": "用户点击 Accept & Continue 后触发 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧仅发送标准 Intent，页面由系统渲染；系统条目无 android:description 描述文本）",
      "shown_text_zh": "跳转至系统无障碍服务列表，由用户在系统页内手动开启 ProcrastiLearn 服务",
      "user_action_requested": "用户在系统页手动找到 ProcrastiLearn 并打开开关；可随时返回，应用不拦截",
      "code_anchor": "xc0.invoke (case 5)、sm2.invoke (case 2)"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity onResume 权限状态校验（LifecycleEventObserver）",
      "trigger_event": "从系统设置返回触发 ON_RESUME",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（仅刷新 overlayGranted / a11yEnabled 状态并更新界面开关，未弹出二次索取弹窗）",
      "shown_text_zh": "返回应用后仅重新读取 Settings.Secure 的 enabled_accessibility_services 与 canDrawOverlays 刷新状态，未获权则保持未开启状态，不重复强制跳转",
      "user_action_requested": "无强制操作；用户可放弃，功能保持未启用（安全降级）",
      "code_anchor": "ad2.k / j82.k / x03.B"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "OverlayAccessibilityService + 悬浮窗学习卡片（WindowManager overlay）",
      "trigger_event": "onServiceConnected 注册 SCREEN_ON/OFF/USER_PRESENT 广播并启动协程；onAccessibilityEvent 收到 TYPE_WINDOW_STATE_CHANGED 且包名为用户所选应用",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（学习卡片内容来自用户自建词库；相关文案：Could not load the next card. / Loading next card… / Show overlay each X minutes while blocked app is open）",
      "shown_text_zh": "检测到用户打开被管控应用时，叠加学习卡片遮罩，要求完成间隔重复复习后才可继续使用",
      "user_action_requested": "用户完成/关闭学习卡片；不读取屏幕文本内容（canRetrieveWindowContent=false）",
      "code_anchor": "com.procrastilearn.app.service.OverlayAccessibilityService.onServiceConnected / onAccessibilityEvent"
    },
    {
      "step": 6,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置 → 显示在其他应用上层（悬浮窗权限页）",
      "trigger_event": "悬浮窗权限未授予时，由用户操作触发 startActivity(new Intent(\"android.settings.action.MANAGE_OVERLAY_PERMISSION\", package:...))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Allow overlay display / This app needs permission to display an overlay over other apps.",
      "shown_text_zh": "允许显示悬浮窗 / 本应用需要权限才能在其他应用之上显示悬浮窗。",
      "user_action_requested": "用户在系统页手动允许悬浮窗权限，可拒绝",
      "code_anchor": "xc0.invoke (default 分支)、sm2.invoke (case 1)；strings.xml overlay_permission_title / overlay_permission_message"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 内 Compose 原生无障碍披露页：标题 Why we need Accessibility、What we access / How it's used 两段正文、隐私承诺、同意复选框、Accept & Continue 与 Not now 按钮（res/values/strings.xml 的 a11y_disclosure_* 组）",
    "设置页 Learning gate (Accessibility) 区块：settings_a11y_headline 与 settings_a11y_support 摘要说明",
    "悬浮窗权限说明：overlay_permission_title / overlay_permission_message，配合跳转 ACTION_MANAGE_OVERLAY_PERMISSION",
    "系统无障碍列表条目：因 accessibility_service_config.xml 未声明 android:description 与 service android:label，系统仅显示应用名 ProcrastiLearn，无自定义描述文字（不构成伪装，也不构成欺骗性说明）",
    "Manifest 未声明 android:description 等无源文本；未使用 WebView 或 assets HTML 承载任何引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Why we need Accessibility",
      "text_zh": "为什么我们需要无障碍权限",
      "source_location": "res/values/strings.xml key=a11y_disclosure_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This app uses Android Accessibility Service permission to detect when you open selected apps (e.g., TikTok, Reddit or any other app you choose) so it can show a short learning prompt before you continue.",
      "text_zh": "本应用使用 Android 无障碍服务权限，检测你何时打开所选应用（例如 TikTok、Reddit 或你选择的任何其他应用），以便在你继续之前显示一个简短的学习提示。",
      "source_location": "res/values/strings.xml key=a11y_disclosure_description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "• Which app is currently on your screen.\n • We do NOT read your passwords, messages, or on-screen text.\n • Your data never leaves your device and is never sold or shared.",
      "text_zh": "• 你当前屏幕上的是哪个应用。• 我们不会读取你的密码、消息或屏幕文本。• 你的数据永不离开设备，绝不出售或共享。",
      "source_location": "res/values/strings.xml key=a11y_disclosure_access_details",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Only to trigger the learning overlay for the apps you selected. You can turn this off anytime in Settings. We don’t sell or share this data, it never leaves your device.",
      "text_zh": "仅用于为你选中的应用触发学习遮罩。你随时可以在设置中关闭。我们不出售也不共享这些数据，它永不离开你的设备。",
      "source_location": "res/values/strings.xml key=a11y_disclosure_usage_details",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "I understand and agree to allow this app to use the Accessibility Service permission for this purpose.",
      "text_zh": "我理解并同意允许本应用为此目的使用无障碍服务权限。",
      "source_location": "res/values/strings.xml key=a11y_disclosure_checkbox",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accept & Continue",
      "text_zh": "接受并继续",
      "source_location": "res/values/strings.xml key=a11y_disclosure_accept",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Not now",
      "text_zh": "暂不",
      "source_location": "res/values/strings.xml key=a11y_disclosure_decline → @string/action_not_now",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Learning gate (Accessibility) — Detects selected apps in foreground to trigger the learning card.",
      "text_zh": "学习闸门（无障碍）—— 检测前台被选中的应用以触发学习卡片。",
      "source_location": "res/values/strings.xml key=settings_a11y_headline / settings_a11y_support",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow overlay display — This app needs permission to display an overlay over other apps.",
      "text_zh": "允许显示悬浮窗 —— 本应用需要权限才能在其他应用之上显示悬浮窗。",
      "source_location": "res/values/strings.xml key=overlay_permission_title / overlay_permission_message",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无强制循环。从系统设置返回后仅在 ON_RESUME 读取 Settings.Secure.\"enabled_accessibility_services\" 与 Settings.canDrawOverlays 刷新状态（ad2.k / j82.k / x03.B），未获权则保持关闭状态，不重新弹出索取弹窗、不重复跳转、无定时器拉起。",
    "overlay_or_fake_settings": "无。未叠放半透明引导遮罩、无全屏悬浮窗覆盖系统设置页、无高仿系统无障碍开关页；悬浮窗仅用于学习卡片业务功能。",
    "restricted_settings_13plus_coaching": "无。未出现教用户进入应用详情右上角菜单允许受限设置的文案或分步教学；且未设置 isAccessibilityTool 伪造归类，系统侧会如实提示受限设置风险。",
    "post_grant_anti_removal": "无。未监听设置页做 GLOBAL_ACTION_BACK/HOME，未自点确认、无防撤权逻辑；onAccessibilityEvent 只处理 TYPE_WINDOW_STATE_CHANGED 的包名，未读取节点内容。",
    "benign_graceful_degradation": "用户点击 Not now 或直接返回即保持功能未启用；文案明确 \"You can turn this off anytime in Settings\"，可随时关闭无障碍服务而应用不拦截。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.action.MANAGE_OVERLAY_PERMISSION 的瞬间抓取；其次在 MainActivity 首次渲染无障碍披露页（出现 Accept & Continue 文本节点）时抓取。",
    "key_pages_to_capture": [
      {
        "page_role": "引导说明页（无障碍披露页）",
        "page_identifier": "com.procrastilearn.app.MainActivity，页面含标题 \"Why we need Accessibility\"、同意复选框与 \"Accept & Continue\" / \"Not now\" 按钮",
        "why_most_useful": "该页是本应用索取无障碍权限的唯一说明载体，可直接判断是否存在虚假用途陈述、隐私承诺过度、隐藏取消按钮或强制勾选陷阱",
        "observable_utg_signals": ["标题与正文是否与 Manifest/配置声明用途一致", "是否存在可点击的 Not now / 返回按钮", "同意复选框是否可跳过", "是否出现故障恐吓、假更新、假安全等诱导话术"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已下载的服务中的 ProcrastiLearn 条目（无描述文本）",
        "why_most_useful": "核验系统侧展示的服务名与描述是否与应用宣称一致，以及是否被伪造为系统/工具类组件",
        "observable_utg_signals": ["条目显示名是否为 ProcrastiLearn", "描述栏是否为空（对应无 android:description）", "是否出现\"受限设置\"提示（对应未伪造 isAccessibilityTool）"]
      },
      {
        "page_role": "跳转系统设置返回后的应用界面",
        "page_identifier": "com.procrastilearn.app.MainActivity 返回态（Learning gate 开关状态）",
        "why_most_useful": "验证拒权后是否存在二次索取弹窗、自动重跳或恐吓提示，是区分良性降级与强制诱导的关键观测点",
        "observable_utg_signals": ["返回后是否立即再次拉起设置页", "是否出现不可取消的索取弹窗", "开关是否如实保持关闭状态"]
      },
      {
        "page_role": "获权后的学习卡片遮罩页",
        "page_identifier": "覆盖在被管控应用上的学习卡片悬浮窗（含 0/1 进度、Rating 交互）",
        "why_most_useful": "确认无障碍权限的实际用途与宣称一致（仅检测前台包名并显示学习卡片），排除后台窃取窗口内容或静默操作其他应用",
        "observable_utg_signals": ["遮罩是否仅覆盖被选应用且可退出", "是否出现读取其他应用界面文本或自动点击行为", "是否请求无关权限或外发数据"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在轻微盲区：引导页文案在 Compose 中以 R.string 整型常量引用，纯静态无法逐行定位到具体 Composable 函数体，需运行期 UTG 文本节点确认渲染完整性；未发现纯图空文本、温和外壳、一阶段 Dropper 或静态加壳等实质盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "xc0.invoke（case 5 跳 android.settings.ACCESSIBILITY_SETTINGS，default 跳 MANAGE_OVERLAY_PERMISSION）",
    "sm2.invoke（case 2 跳 android.settings.ACCESSIBILITY_SETTINGS）",
    "x03.B（读取 Settings.Secure.enabled_accessibility_services 判定服务是否启用）",
    "ad2.k / j82.k（ON_RESUME 刷新 a11yEnabled 与 canDrawOverlays，无强制重跳）",
    "com.procrastilearn.app.service.OverlayAccessibilityService.onAccessibilityEvent（仅取 TYPE_WINDOW_STATE_CHANGED 包名，跳过输入法与自身）",
    "res/xml/accessibility_service_config.xml（canRetrieveWindowContent=false、无 description、settingsActivity 为空）"
  ]
}
```

</details>

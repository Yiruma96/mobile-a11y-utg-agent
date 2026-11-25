# BN_043__67e6fb5589｜残障辅助与无障碍支持 — TypeAssist

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：159.0s

## 1. 一句话核心结论

- **核心申请方式**：TypeAssist 在自身设置页的 Permissions 分区以开关形式透明说明无障碍服务用于"读取并替换文本"，用户点击开关后才跳转系统 ACCESSIBILITY_SETTINGS，缺权时仅 Toast 提示并跳转一次，无强制、无遮罩、无伪装。
- **静态可见性说明**：全部权限引导逻辑均在 classes.dex 明文可见：Manifest 声明、accessibility_service_config.xml、Compose 设置页 ye1.b、跳转实现 ve1.invoke/wi0.invoke/j7.invoke、状态回读 MainActivity.f 均可静态还原；assets 下无 HTML/JS 引导页，无加密载荷，无远端下发 UI。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `67e6fb55895c6033faacfa9efd56e19372806a8b74464d2e429d6d4020a86e14` |
| 包名 / 年份 | `com.typeassist.app` / 2025-2026 |
| 家族 / 品类 | **残障辅助与无障碍支持**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.typeassist.app_12.apk |
| 桌面显示名 | TypeAssist |
| 引导页宣称品牌/身份 | TypeAssist（开源无障碍输入辅助，GitHub estiaksoyeb/TypeAssist，Telegram t.me/TypeAssist） |
| 系统无障碍列表服务名 | TypeAssist AI |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅 R8 类名混淆（r8-map-id-641ba7da...），无 activity-alias、无空白/换行挤出警告、无同形字、未伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.typeassist.app.service.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | TypeAssist |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.typeassist.app.MainActivity（Compose ComponentActivity，单 Activity 单栈） | LAUNCHER 图标点击 → onCreate(Bundle) | 原生Activity | **原文**：Welcome to TypeAssist!<br>**译注**：欢迎使用 TypeAssist！ | 正常浏览首页/欢迎页，无强制跳转；可自由进入设置，无取消按钮需求 | `com.typeassist.app.MainActivity#onCreate / gs#b` |
| 2 | 引导说明页 | 应用内设置 → Permissions 分区（Compose 设置页，ye1.b） | 用户主动进入 Settings 页触发 recomposition | 原生Activity | **原文**：Permissions / TypeAssist works best with these permissions. / REQUIRED / Accessibility Service — Required to read and replace text.<br>**译注**：权限 / 搭配这些权限时 TypeAssist 运行最佳。 / 必需 / 无障碍服务 —— 用于读取并替换文本。 | 用户自行阅读说明；该页为可滚动设置列表，无阻断式弹窗，可直接返回离开 | `ye1#b / w72.b("Permissions") / nm2.k("Accessibility Service", "Required to read and replace text.")` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | 用户点击 Accessibility Service 开关 → ve1(context, 1).invoke() | 系统无障碍页 | **原文**：无（直接调用 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))）<br>**译注**：跳转至系统无障碍服务列表，用户在列表中自行找到并开启 TypeAssist AI | 用户在系统页手动开启服务，可随时返回；应用不做任何叠加遮罩或引导浮层 | `ve1#invoke case 1` |
| 4 | 拒权反馈循环 | 应用内设置页开关状态回显 | 从系统设置返回后重新读取 Settings.Secure.enabled_accessibility_services | 原生Activity | **原文**：If the app is not working, the Accessibility Service might be in a 'ghost' state. Try turning the Accessibility Service OFF and then ON again to reset it.<br>**译注**：若应用不工作，无障碍服务可能处于"幽灵"状态，请将无障碍服务关闭再重新开启以重置。 | 用户可继续正常使用或稍后开启；无强制重跳、无倒计时拉起、无禁用返回键 | `com.typeassist.app.MainActivity#f / is#c case 3` |
| 5 | 业务功能触发 | 功能开关回调 j7.invoke case 2（例如 Allow Trigger Anywhere 等开关置真） | 用户打开需要无障碍的功能开关，且 MainActivity.f() 返回 false | 通知栏 | **原文**：Please Enable Accessibility Service first<br>**译注**：请先启用无障碍服务 | Toast 提示（无按钮）后跳转一次系统无障碍设置；用户可忽略并返回，功能不伪造可用 | `j7#invoke case 2 / wi0#invoke case 1` |
| 6 | 获权后动作 | com.typeassist.app.service.MyAccessibilityService + fb1 悬浮进度窗 | onServiceConnected → 建通知渠道；生成 AI 结果时 Handler.post(ab1.run) 挂 FrameLayout+ProgressBar+Button | 悬浮窗Overlay | **原文**：TypeAssist Service / Keeps TypeAssist running in the background / TypeAssist is Active<br>**译注**：TypeAssist 服务 / 保持 TypeAssist 后台运行 / TypeAssist 运行中 | 悬浮窗显示 AI 生成进度并提供中止按钮；不拦截系统设置页、不阻止用户关闭服务 | `com.typeassist.app.service.MyAccessibilityService#onServiceConnected / ab1#run` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 应用内设置页 Permissions 分区（Compose，ye1.b）：分区标题 "Permissions"、说明 "TypeAssist works best with these permissions."、"REQUIRED" 标签
- 应用内设置页开关条目："Accessibility Service" + 副标题 "Required to read and replace text."（点击跳系统设置）
- 应用内设置页 "RECOMMENDED FOR STABILITY" 分区："Notifications"/"Required to keep the service running."、"Ignore Battery Opt."/"Prevent system from killing the app."、"Xiaomi Setup"/"Enable 'Autostart' & 'Pop-up windows'."
- Toast（j7.invoke case 2）："Please Enable Accessibility Service first"
- 设置页排障说明（is#c case 3）："If the app is not working, the Accessibility Service might be in a 'ghost' state..."
- 系统无障碍列表条目：android:label=@string/app_name_service="TypeAssist AI"，android:description=@string/app_name="TypeAssist"（accessibility_service_config.xml）
- 运行时通知渠道："TypeAssist Service"、"Keeps TypeAssist running in the background"、通知标题 "TypeAssist is Active"
- AI 生成中悬浮进度窗（SYSTEM_ALERT_WINDOW，ab1.run）：ProgressBar + Button，无文案诱导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Permissions | 权限 | `ye1#b 硬编码（w72.b）` | 良性透明说明 |
| en | TypeAssist works best with these permissions. | 搭配这些权限时 TypeAssist 运行效果最佳。 | `ye1#b 硬编码（w72.b）` | 良性透明说明 |
| en | Accessibility Service | 无障碍服务 | `ye1#b 硬编码（nm2.k）` | 良性透明说明 |
| en | Required to read and replace text. | 用于读取并替换文本。 | `ye1#b 硬编码（nm2.k）` | 良性透明说明 |
| en | Please Enable Accessibility Service first | 请先启用无障碍服务 | `j7#invoke case 2 硬编码 Toast` | 良性透明说明 |
| en | If the app is not working, the Accessibility Service might be in a 'ghost' state.<br><br>Try turning the Accessibility Service OFF and then ON again to reset it. | 若应用不工作，无障碍服务可能处于“幽灵”状态。请将无障碍服务关闭再重新开启以重置。 | `is#c case 3 硬编码` | 良性透明说明 |
| en | Skip Stability Settings? | 跳过稳定性设置？ | `is#c case 3 区块硬编码` | 良性透明说明 |
| en | TypeAssist AI | TypeAssist AI | `res/values/strings.xml app_name_service / AndroidManifest service android:label` | 良性透明说明 |
| en | TypeAssist | TypeAssist | `res/values/strings.xml app_name / res/xml/accessibility_service_config.xml android:description` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无强制循环。仅读取 Settings.Secure.enabled_accessibility_services 回显开关状态；用户从系统设置返回后不重跳、不定时拉起，可留在本页继续使用或退出。缺权时一次性 Toast + 单次跳转，用户可忽略。
- **遮罩叠层 / 高仿系统设置页**：无。无半透明引导遮罩、无全屏悬浮引导、无高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 仅用于 AI 生成中的进度悬浮窗（FrameLayout+ProgressBar+Button）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无
- **良性降级 / 替代方案**：有。设置页提供 "Skip Stability Settings?" 可跳过非必需稳定性项（通知、电池优化、小米自启动）；未启用无障碍时功能开关仅提示并跳转，不伪造可用状态，也不阻断应用其余页面（配置、历史、备份恢复等）。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在检测到 startActivity(Intent("android.settings.ACCESSIBILITY_SETTINGS")) 调用瞬间（ve1.invoke case 1 / wi0.invoke case 1 / j7.invoke case 2）拉起 UTG；同时可在 MainActivity 进入设置页后抓取 Permissions 分区画面。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。该应用未加壳、无远端 HTML、无图片诱导；唯一需注意点是界面由 Jetpack Compose 渲染，UTG 需按文本节点（text/content-desc）而非传统 View id 提取，且 R8 混淆后类名不可读，需依赖文本锚定。原生 libtypeassist.so 为 llama.cpp 推理引擎，承担模型推理而非 UI/跳转逻辑，不影响运行期 UTG 判定。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **引导说明页（应用内 Permissions 分区）** | com.typeassist.app.MainActivity 内 Compose 设置页，含文本 "Permissions"、"REQUIRED"、"Accessibility Service"、"Required to read and replace text." | 这是该应用唯一的无障碍引导载体，其文本是否如实描述用途、是否可跳过，是区分良性说明与诱导的关键 | "Accessibility Service" 条目副标题是否明示用途（Required to read and replace text.）；是否存在阻断式弹窗/无取消按钮/倒计时等强制信号；是否出现伪造系统设置样式或品牌冒充文案 |
| **系统无障碍服务列表项** | com.android.settings 无障碍列表中出现 "TypeAssist AI"（服务描述 "TypeAssist"） | 核对系统侧标签与桌面名一致性，识别是否存在空白/换行挤出或同形字伪装 | 服务项显示名是否为 "TypeAssist AI" 且与 app_name 一致；描述文本是否为 "TypeAssist"，有无空白/不可见字符填充；开启时是否弹出系统标准警告页（应用未伪造 isAccessibilityTool 绕过） |
| **跳转后叠层/遮罩检查页** | 跳转 ACCESSIBILITY_SETTINGS 后 800ms 窗口栈，检查是否存在 TYPE_APPLICATION_OVERLAY 窗口 | 确认应用未在系统设置页上方叠放引导遮罩或悬浮指引（这是诱导型应用的高频特征） | 窗口列表中是否仅有系统设置窗口，无第三方 overlay 窗口；是否出现悬浮按钮/箭头指引图 |
| **获权后动作页** | 通知栏 "TypeAssist Service" 通知渠道 + AI 生成中的悬浮进度窗 | 确认获权后的实际行为与声明用途一致（文本改写 + 进度反馈），而非静默采集或后台控制 | 通知标题是否为 "TypeAssist is Active"、渠道描述是否与后台保活说明一致；悬浮窗内容是否为 ProgressBar/中止按钮，而非引导跳转或广告 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.typeassist.app.MainActivity#f`
- `ye1#b`
- `ve1#invoke`
- `j7#invoke`
- `com.typeassist.app.service.MyAccessibilityService#onServiceConnected`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点（定向核验，静态完全可见）

**该应用引导用户开启无障碍权限的方式属于良性的透明功能说明与系统设置跳转，未发现任何诱导、伪装或强制行为。**

1. **声明层身份一致**：桌面名 `TypeAssist`（[strings.xml L14-L15](<resource-unit:#1 file:res/values/strings.xml#L14-L15>)），无障碍服务标签 `TypeAssist AI`，服务描述复用 `@string/app_name`（`TypeAssist`）。无障碍服务配置 [accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 仅声明 `typeViewFocused|typeViewTextChanged|typeWindowContentChanged|typeWindowStateChanged` + `canRetrieveWindowContent`，与其"读取并替换输入框文本"的声明功能一致，未声明 `canPerformGestures`/`flagRequestFilterKeyEvents` 等越权项。

2. **唯一的权限引导载体是应用内的 Compose 设置页**：[ye1#b](<resource-unit:#1.dex1 code:ye1#b>) 渲染"Permissions / TypeAssist works best with these permissions."分区分组开关，`Accessibility Service` 副标题为 "Required to read and replace text."，点击走 [ve1#invoke](<resource-unit:#1.dex1 code:ve1#invoke>) case 1 → `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，是**用户主动点开关**才跳转，非冷启动自动跳。

3. **状态回读而非死循环**：[MainActivity#f](<resource-unit:#1.dex1 code:com.typeassist.app.MainActivity#f>) 仅读 `Settings.Secure.enabled_accessibility_services` 判断开关显示状态；返回应用后无 `onResume` 重跳、无定时器拉起、无遮罩叠层、无高仿系统设置页。

4. **缺权时的降级是 Toast 提示 + 一次跳转**：[j7#invoke](<resource-unit:#1.dex1 code:j7#invoke>) case 2 在用户开启某功能但服务未启用时弹 `Toast "Please Enable Accessibility Service first"` 并跳系统无障碍设置，属常规功能前置提示；[wi0#invoke](<resource-unit:#1.dex1 code:wi0#invoke>) case 1 在用户主动关闭开关时同步状态并跳设置。

5. **获权后动作良性**：[MyAccessibilityService](<resource-unit:#1.dex1 code:com.typeassist.app.service.MyAccessibilityService>) `onServiceConnected` 建通知渠道 `typeassist_service`/"TypeAssist Service"（"Keeps TypeAssist running in the background"），生成 AI 结果时用 `fb1` overlayManager 挂 `FrameLayout+ProgressBar+Button` 的悬浮进度窗（对应 `SYSTEM_ALERT_WINDOW` 与 `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` 的正当用途）。未见自点确认、`GLOBAL_ACTION_BACK` 阻止撤权等反移除逻辑。

6. **未发现伪装痕迹**：无 activity-alias 多重身份、无空白/换行挤出、无同形字、无伪造 `isAccessibilityTool`、无本地/远端 HTML 教学页（`assets/` 仅 `dexopt` 基线 profile）。

**未决/边界**：`libtypeassist.so`（llama.cpp 推理引擎）承担模型推理，本次未逐函数反编译；其 JNI 声明（`loadModel`/`generateResponseNative`/`stopGenerationNative`/`stringFromJNI`）与本地模型推理用途相符，未见动态加载外部 dex/APK 入口。未启动动态分析（静态已足以闭环）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部权限引导逻辑均在 classes.dex 明文可见：Manifest 声明、accessibility_service_config.xml、Compose 设置页 ye1.b、跳转实现 ve1.invoke/wi0.invoke/j7.invoke、状态回读 MainActivity.f 均可静态还原；assets 下无 HTML/JS 引导页，无加密载荷，无远端下发 UI。",
  "summary_one_liner": "TypeAssist 在自身设置页的 Permissions 分区以开关形式透明说明无障碍服务用于\"读取并替换文本\"，用户点击开关后才跳转系统 ACCESSIBILITY_SETTINGS，缺权时仅 Toast 提示并跳转一次，无强制、无遮罩、无伪装。",
  "disguise_identity": {
    "app_display_name": "TypeAssist",
    "claimed_brand_or_persona": "TypeAssist（开源无障碍输入辅助，GitHub estiaksoyeb/TypeAssist，Telegram t.me/TypeAssist）",
    "a11y_service_label": "TypeAssist AI",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅 R8 类名混淆（r8-map-id-641ba7da...），无 activity-alias、无空白/换行挤出警告、无同形字、未伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.typeassist.app.MainActivity（Compose ComponentActivity，单 Activity 单栈）",
      "trigger_event": "LAUNCHER 图标点击 → onCreate(Bundle)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Welcome to TypeAssist!",
      "shown_text_zh": "欢迎使用 TypeAssist！",
      "user_action_requested": "正常浏览首页/欢迎页，无强制跳转；可自由进入设置，无取消按钮需求",
      "code_anchor": "com.typeassist.app.MainActivity#onCreate / gs#b"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "应用内设置 → Permissions 分区（Compose 设置页，ye1.b）",
      "trigger_event": "用户主动进入 Settings 页触发 recomposition",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Permissions / TypeAssist works best with these permissions. / REQUIRED / Accessibility Service — Required to read and replace text.",
      "shown_text_zh": "权限 / 搭配这些权限时 TypeAssist 运行最佳。 / 必需 / 无障碍服务 —— 用于读取并替换文本。",
      "user_action_requested": "用户自行阅读说明；该页为可滚动设置列表，无阻断式弹窗，可直接返回离开",
      "code_anchor": "ye1#b / w72.b(\"Permissions\") / nm2.k(\"Accessibility Service\", \"Required to read and replace text.\")"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户点击 Accessibility Service 开关 → ve1(context, 1).invoke()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（直接调用 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))）",
      "shown_text_zh": "跳转至系统无障碍服务列表，用户在列表中自行找到并开启 TypeAssist AI",
      "user_action_requested": "用户在系统页手动开启服务，可随时返回；应用不做任何叠加遮罩或引导浮层",
      "code_anchor": "ve1#invoke case 1"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "应用内设置页开关状态回显",
      "trigger_event": "从系统设置返回后重新读取 Settings.Secure.enabled_accessibility_services",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "If the app is not working, the Accessibility Service might be in a 'ghost' state. Try turning the Accessibility Service OFF and then ON again to reset it.",
      "shown_text_zh": "若应用不工作，无障碍服务可能处于\"幽灵\"状态，请将无障碍服务关闭再重新开启以重置。",
      "user_action_requested": "用户可继续正常使用或稍后开启；无强制重跳、无倒计时拉起、无禁用返回键",
      "code_anchor": "com.typeassist.app.MainActivity#f / is#c case 3"
    },
    {
      "step": 5,
      "stage": "业务功能触发",
      "screen_or_component": "功能开关回调 j7.invoke case 2（例如 Allow Trigger Anywhere 等开关置真）",
      "trigger_event": "用户打开需要无障碍的功能开关，且 MainActivity.f() 返回 false",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Please Enable Accessibility Service first",
      "shown_text_zh": "请先启用无障碍服务",
      "user_action_requested": "Toast 提示（无按钮）后跳转一次系统无障碍设置；用户可忽略并返回，功能不伪造可用",
      "code_anchor": "j7#invoke case 2 / wi0#invoke case 1"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.typeassist.app.service.MyAccessibilityService + fb1 悬浮进度窗",
      "trigger_event": "onServiceConnected → 建通知渠道；生成 AI 结果时 Handler.post(ab1.run) 挂 FrameLayout+ProgressBar+Button",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "TypeAssist Service / Keeps TypeAssist running in the background / TypeAssist is Active",
      "shown_text_zh": "TypeAssist 服务 / 保持 TypeAssist 后台运行 / TypeAssist 运行中",
      "user_action_requested": "悬浮窗显示 AI 生成进度并提供中止按钮；不拦截系统设置页、不阻止用户关闭服务",
      "code_anchor": "com.typeassist.app.service.MyAccessibilityService#onServiceConnected / ab1#run"
    }
  ],
  "text_presentation_locations": [
    "应用内设置页 Permissions 分区（Compose，ye1.b）：分区标题 \"Permissions\"、说明 \"TypeAssist works best with these permissions.\"、\"REQUIRED\" 标签",
    "应用内设置页开关条目：\"Accessibility Service\" + 副标题 \"Required to read and replace text.\"（点击跳系统设置）",
    "应用内设置页 \"RECOMMENDED FOR STABILITY\" 分区：\"Notifications\"/\"Required to keep the service running.\"、\"Ignore Battery Opt.\"/\"Prevent system from killing the app.\"、\"Xiaomi Setup\"/\"Enable 'Autostart' & 'Pop-up windows'.\"",
    "Toast（j7.invoke case 2）：\"Please Enable Accessibility Service first\"",
    "设置页排障说明（is#c case 3）：\"If the app is not working, the Accessibility Service might be in a 'ghost' state...\"",
    "系统无障碍列表条目：android:label=@string/app_name_service=\"TypeAssist AI\"，android:description=@string/app_name=\"TypeAssist\"（accessibility_service_config.xml）",
    "运行时通知渠道：\"TypeAssist Service\"、\"Keeps TypeAssist running in the background\"、通知标题 \"TypeAssist is Active\"",
    "AI 生成中悬浮进度窗（SYSTEM_ALERT_WINDOW，ab1.run）：ProgressBar + Button，无文案诱导"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Permissions",
      "text_zh": "权限",
      "source_location": "ye1#b 硬编码（w72.b）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "TypeAssist works best with these permissions.",
      "text_zh": "搭配这些权限时 TypeAssist 运行效果最佳。",
      "source_location": "ye1#b 硬编码（w72.b）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service",
      "text_zh": "无障碍服务",
      "source_location": "ye1#b 硬编码（nm2.k）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Required to read and replace text.",
      "text_zh": "用于读取并替换文本。",
      "source_location": "ye1#b 硬编码（nm2.k）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Please Enable Accessibility Service first",
      "text_zh": "请先启用无障碍服务",
      "source_location": "j7#invoke case 2 硬编码 Toast",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "If the app is not working, the Accessibility Service might be in a 'ghost' state.\n\nTry turning the Accessibility Service OFF and then ON again to reset it.",
      "text_zh": "若应用不工作，无障碍服务可能处于“幽灵”状态。请将无障碍服务关闭再重新开启以重置。",
      "source_location": "is#c case 3 硬编码",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Skip Stability Settings?",
      "text_zh": "跳过稳定性设置？",
      "source_location": "is#c case 3 区块硬编码",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "TypeAssist AI",
      "text_zh": "TypeAssist AI",
      "source_location": "res/values/strings.xml app_name_service / AndroidManifest service android:label",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "TypeAssist",
      "text_zh": "TypeAssist",
      "source_location": "res/values/strings.xml app_name / res/xml/accessibility_service_config.xml android:description",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无强制循环。仅读取 Settings.Secure.enabled_accessibility_services 回显开关状态；用户从系统设置返回后不重跳、不定时拉起，可留在本页继续使用或退出。缺权时一次性 Toast + 单次跳转，用户可忽略。",
    "overlay_or_fake_settings": "无。无半透明引导遮罩、无全屏悬浮引导、无高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 仅用于 AI 生成中的进度悬浮窗（FrameLayout+ProgressBar+Button）。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无",
    "benign_graceful_degradation": "有。设置页提供 \"Skip Stability Settings?\" 可跳过非必需稳定性项（通知、电池优化、小米自启动）；未启用无障碍时功能开关仅提示并跳转，不伪造可用状态，也不阻断应用其余页面（配置、历史、备份恢复等）。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在检测到 startActivity(Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")) 调用瞬间（ve1.invoke case 1 / wi0.invoke case 1 / j7.invoke case 2）拉起 UTG；同时可在 MainActivity 进入设置页后抓取 Permissions 分区画面。",
    "key_pages_to_capture": [
      {
        "page_role": "引导说明页（应用内 Permissions 分区）",
        "page_identifier": "com.typeassist.app.MainActivity 内 Compose 设置页，含文本 \"Permissions\"、\"REQUIRED\"、\"Accessibility Service\"、\"Required to read and replace text.\"",
        "why_most_useful": "这是该应用唯一的无障碍引导载体，其文本是否如实描述用途、是否可跳过，是区分良性说明与诱导的关键",
        "observable_utg_signals": [
          "\"Accessibility Service\" 条目副标题是否明示用途（Required to read and replace text.）",
          "是否存在阻断式弹窗/无取消按钮/倒计时等强制信号",
          "是否出现伪造系统设置样式或品牌冒充文案"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍列表中出现 \"TypeAssist AI\"（服务描述 \"TypeAssist\"）",
        "why_most_useful": "核对系统侧标签与桌面名一致性，识别是否存在空白/换行挤出或同形字伪装",
        "observable_utg_signals": [
          "服务项显示名是否为 \"TypeAssist AI\" 且与 app_name 一致",
          "描述文本是否为 \"TypeAssist\"，有无空白/不可见字符填充",
          "开启时是否弹出系统标准警告页（应用未伪造 isAccessibilityTool 绕过）"
        ]
      },
      {
        "page_role": "跳转后叠层/遮罩检查页",
        "page_identifier": "跳转 ACCESSIBILITY_SETTINGS 后 800ms 窗口栈，检查是否存在 TYPE_APPLICATION_OVERLAY 窗口",
        "why_most_useful": "确认应用未在系统设置页上方叠放引导遮罩或悬浮指引（这是诱导型应用的高频特征）",
        "observable_utg_signals": [
          "窗口列表中是否仅有系统设置窗口，无第三方 overlay 窗口",
          "是否出现悬浮按钮/箭头指引图"
        ]
      },
      {
        "page_role": "获权后动作页",
        "page_identifier": "通知栏 \"TypeAssist Service\" 通知渠道 + AI 生成中的悬浮进度窗",
        "why_most_useful": "确认获权后的实际行为与声明用途一致（文本改写 + 进度反馈），而非静默采集或后台控制",
        "observable_utg_signals": [
          "通知标题是否为 \"TypeAssist is Active\"、渠道描述是否与后台保活说明一致",
          "悬浮窗内容是否为 ProgressBar/中止按钮，而非引导跳转或广告"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。该应用未加壳、无远端 HTML、无图片诱导；唯一需注意点是界面由 Jetpack Compose 渲染，UTG 需按文本节点（text/content-desc）而非传统 View id 提取，且 R8 混淆后类名不可读，需依赖文本锚定。原生 libtypeassist.so 为 llama.cpp 推理引擎，承担模型推理而非 UI/跳转逻辑，不影响运行期 UTG 判定。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.typeassist.app.MainActivity#f",
    "ye1#b",
    "ve1#invoke",
    "j7#invoke",
    "com.typeassist.app.service.MyAccessibilityService#onServiceConnected",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>

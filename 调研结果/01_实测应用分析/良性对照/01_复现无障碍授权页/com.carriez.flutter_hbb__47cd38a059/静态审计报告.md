# BN_060__47cd38a059｜远程协助与跨设备互联 — RustDesk

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：149.2s

## 1. 一句话核心结论

- **核心申请方式**：RustDesk 仅在用户主动开启“被远程控制”功能时，由 Flutter 侧经 MethodChannel 触发一次 android.settings.ACCESSIBILITY_SETTINGS 跳转，配合应用内说明页与如实的系统无障碍描述，无遮罩、无拒权循环、无伪装身份。
- **静态可见性说明**：Java/Kotlin 层完整静态可见：无障碍服务声明、accessibility_service_config.xml、唯一跳转点 a.i() 与其唯一调用者 MainActivity.J0()（MethodChannel 命令分发）均已还原。Flutter 层 libapp.so 仅有 x86_64 架构，Blutter 不支持该架构，故引导页具体 UI 文案与按钮布局未能逐字反编译，仅能从明文字符串池确认 i18n key（android_input_permission_tip1/tip2、How to get Android input permission?）。无加壳、无 AES 密文、无远端 HTML 教学页，assets/ 目录不含任何 .html 文件。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `47cd38a059583c9188892d23bfc1c83f3aec2c53e20f588da293b1f6b4038433` |
| 包名 / 年份 | `com.carriez.flutter_hbb` / 2025-2026 |
| 家族 / 品类 | **远程协助与跨设备互联**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.carriez.flutter_hbb_105030003.apk |
| 桌面显示名 | RustDesk |
| 引导页宣称品牌/身份 | RustDesk（开源远程桌面，真实品牌） |
| 系统无障碍列表服务名 | RustDesk Input |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。未发现空白/换行挤出警告、同形字、多 activity-alias 伪装、伪造 isAccessibilityTool 等手法；服务 label 与包名、桌面名称一致，均指向 RustDesk 自身。 |
| 无障碍服务类名 | `com.carriez.flutter_hbb.InputService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Allow other devices to control your phone using virtual touch, when RustDesk screen sharing is established |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.carriez.flutter_hbb.MainActivity（LaunchTheme，singleTop，Flutter 主界面） | onCreate / MAIN+LAUNCHER 启动 | 原生Activity | 无 | 无需操作，可自由使用应用（ID/密码连接、文件传输等）。 | `AndroidManifest.xml application/activity com.carriez.flutter_hbb.MainActivity` |
| 2 | 业务功能触发 | Flutter 侧「允许远程控制本机 / Enable remote control」开关或设置项 | 用户点击开启被控输入能力，Flutter 通过 MethodChannel 下发命令（如 "input" 等分支） | 原生Activity | **原文**：How to get Android input permission?<br>**译注**：如何获取 Android 输入权限？（功能触发后才出现，属按需引导） | 用户可自行选择继续查看说明或放弃开启（不开启仅保持屏幕共享观看能力）。 | `com.carriez.flutter_hbb.MainActivity.J0（MethodChannel switch 分发）；libapp.so 字符串 "How to get Android input permission?"` |
| 3 | 引导说明页 | Flutter 应用内说明页（i18n key android_input_permission_tip1 / android_input_permission_tip2） | 步骤 2 的功能开关被打开后由 Flutter 路由渲染说明文本 | 原生Activity | **原文**：android_input_permission_tip1 / android_input_permission_tip2（i18n 资源 key，具体译文因 libapp.so 仅 x86_64 未能逐字还原）<br>**译注**：说明为何需要无障碍（输入控制）权限的提示文案；文案性质为功能说明，非恐吓/伪装。 | 阅读后可继续前往设置，或直接返回不授权。 | `libapp.so（#1.so1）字符串池 android_input_permission_tip1 / android_input_permission_tip2` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | Flutter MethodChannel 命令到达 MainActivity.J0 → a.i(context, "android.settings.ACCESSIBILITY_SETTINGS") | 系统无障碍页 | **原文**：Allow other devices to control your phone using virtual touch, when RustDesk screen sharing is established<br>**译注**：当 RustDesk 屏幕共享建立后，允许其他设备使用虚拟触摸控制你的手机。（系统无障碍列表中 RustDesk Input 项的描述） | 用户在系统无障碍列表中找到「RustDesk Input」并手动开启；系统页自带关闭/返回，应用不做拦截。 | `com.carriez.flutter_hbb.a.i(Context, String)；res/values/strings.xml accessibility_service_description；res/xml/accessibility_service_config.xml` |
| 5 | 获权后动作 | com.carriez.flutter_hbb.InputService（无障碍服务） | 系统绑定服务后回调 onServiceConnected() | 原生Activity | 无 | 无。授权后由远端会话按需注入触摸手势（simulateTap/simulateLongPress 类能力）。 | `com.carriez.flutter_hbb.InputService.onServiceConnected()` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目描述：res/values/strings.xml 的 accessibility_service_description（经 res/xml/accessibility_service_config.xml 的 android:description 引用），显示在「设置 → 无障碍 → RustDesk Input」项下方
- 系统无障碍列表服务名称：AndroidManifest.xml 中 service android:label="RustDesk Input"
- 应用内 Flutter 说明页：android_input_permission_tip1 / android_input_permission_tip2（i18n key，位于 libapp.so 字符串池，具体译文未逐字还原）
- 应用内帮助标题：「How to get Android input permission?」（libapp.so 明文字符串）
- 未发现：本地 HTML WebView 教学页、远端 WebView、悬浮窗遮罩指引、高仿系统开关页、不可取消 Dialog

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Allow other devices to control your phone using virtual touch, when RustDesk screen sharing is established | 当 RustDesk 屏幕共享建立后，允许其他设备使用虚拟触摸控制你的手机。 | `res/values/strings.xml 的 accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用）` | 良性透明说明 |
| en | How to get Android input permission? | 如何获取 Android 输入权限？ | `lib/x86_64/libapp.so 明文字符串池（Flutter 帮助/说明标题）` | 受限设置分步教学 |
| en | android_input_permission_tip1 | Android 输入权限提示文案 1（i18n key，具体译文未逐字还原） | `lib/x86_64/libapp.so 字符串池（Flutter i18n key）` | 良性透明说明 |
| en | android_input_permission_tip2 | Android 输入权限提示文案 2（i18n key，具体译文未逐字还原） | `lib/x86_64/libapp.so 字符串池（Flutter i18n key）` | 良性透明说明 |
| en | RustDesk Input | RustDesk 输入（系统无障碍服务显示名） | `AndroidManifest.xml service android:label` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。跳转点 a.i() 全包仅一处且唯一调用者为 MainActivity.J0 的 MethodChannel 命令分支，代码中不存在 onResume 重跳、Timer 周期拉起、广播/前台服务后台重跳逻辑；用户返回或拒绝授权后停留在应用内，功能降级为仅观看屏幕共享，不反复打扰。
- **遮罩叠层 / 高仿系统设置页**：无。无半透明引导遮罩、无全屏悬浮窗压栈、无高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 用于 FloatingWindowService 的远程会话控制条，非引导遮罩。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。代码中无「进应用详情 → 右上角菜单 → 允许受限设置」的分步教学，无 Session 安装器（session-based installer）绕过实现；b2.P.b() 仅为 permission_handler 插件的通用 APPLICATION_DETAILS_SETTINGS 兜底。
- **获权后即时行为与防撤权机制**：无。未使用 performGlobalAction(GLOBAL_ACTION_BACK/HOME)、未监听 TYPE_WINDOWS_CHANGED 之外的设置页事件来阻止撤权，无自点确认/自授权逻辑。
- **良性降级 / 替代方案**：具备。不开启无障碍时仍可使用屏幕共享（观看）与文件传输；远程输入控制需用户显式开启，服务配置本身也限定 canPerformGestures 且描述中声明「屏幕共享建立后」才生效。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监控 Activity 启动事件中出现 intent action = android.settings.ACCESSIBILITY_SETTINGS 且来源包为 com.carriez.flutter_hbb 的瞬间（对应 MainActivity.J0 → a.i 调用）；其次监控 MainActivity 上出现含「How to get Android input permission?」或 input permission 关键词的 Flutter 页面渲染。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。唯一限制是 libapp.so 仅含 x86_64 架构，Flutter 引导页具体译文未能逐字静态还原，UTG 需在运行期读取实际渲染文本来补齐；但该层为未加密 AOT 字符串池，非加壳/密文/远端 HTML，运行期完全可见，不构成检测盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前 Flutter 说明页（功能开关被打开后）** | MainActivity 内 Flutter 渲染页，可见文本包含 "How to get Android input permission?" / android_input_permission_tip1/2 对应译文 | 这是应用唯一的机会向用户解释「为什么要无障碍权限」，其措辞是否诚实（是否承认将被远端注入触摸）直接区分良性透明说明与诱导欺骗。 | 说明文案是否出现功能真实用途（remote control / virtual touch）而非安全、更新、清理话术；是否存在「跳过/稍后」按钮或返回即退出的可取消路径；页面是否为原生 Flutter 视图而非 WebView 加载远端 URL |
| **系统无障碍服务列表项（RustDesk Input）** | com.android.settings 无障碍页，列表项标题 "RustDesk Input"，副标题为 accessibility_service_description 原文 | 系统页是权限授予的最终落点；可核验服务名与描述是否与实际能力（可注入手势、可读取窗口内容）一致，是否出现空白名称、同形字或夸大承诺。 | 服务标签与描述原文是否完整可读（无空白/换行挤出/同形字）；描述是否声明前置条件（screen sharing established）而非无条件索取；是否存在应用侧叠加的悬浮遮罩或浮层覆盖系统开关 |
| **跳转后返回应用的降级状态页** | 从系统无障碍页返回 MainActivity 后的界面（未授权状态） | 验证是否存在拒权反馈循环——良性实现应停留在原页面或降级为仅观看，恶意实现会立即重跳设置页。 | 返回后是否在短时间内再次拉起 ACCESSIBILITY_SETTINGS（重复 Activity 启动计数）；是否出现不可取消的模态弹窗逼迫授权；是否出现「仅观看/手动模式」等替代路径提示 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.carriez.flutter_hbb.MainActivity.J0`
- `com.carriez.flutter_hbb.a.i`
- `com.carriez.flutter_hbb.InputService.onServiceConnected`
- `com.carriez.flutter_hbb.InputService.onAccessibilityEvent`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml#accessibility_service_description`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向审计，共 12 次工具调用）

**1. 无障碍服务本体清晰、用途透明**
- 服务 [InputService](<resource-unit:#1.dex1 code:com.carriez.flutter_hbb.InputService>) 通过 `BIND_ACCESSIBILITY_SERVICE` 绑定，`android:label="RustDesk Input"`，配置见 [accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>)：`canPerformGestures=true`、`canRetrieveWindowContent=true`、事件类型仅 `typeWindowsChanged`。
- `onServiceConnected()` 把 flags 设为 `0x8040`（SDK≥33）或 `64`（SDK<33），也就是 **FLAG_RETRIEVE_INTERACTIVE_WINDOWS + FLAG_REQUEST_2_FINGER_PASSTHROUGH**，**没有** `FLAG_REQUEST_FILTER_KEY_EVENTS`，**没有** `FLAG_REQUEST_TOUCH_EXPLORATION_MODE`；`onAccessibilityEvent()` 只做空校验，不解析任何界面内容。
- 没有伪造 `isAccessibilityTool`，也没有 `GLOBAL_ACTION_BACK`、`WATCH_SETTINGS` 或自撤权逻辑（全 DEX 均无命中）。

**2. 跳转链路极简：单点、按需、无循环**
- 全包内只有一处跳转到无障碍设置：[a.i()](<resource-unit:#1.dex1 code:com.carriez.flutter_hbb.a#i>) 构造 `android.settings.ACCESSIBILITY_SETTINGS`（带 `FLAG_ACTIVITY_NEW_TASK`，对其他 action 追加 `package:` 限定），并且**唯一调用者是** [MainActivity.J0()](<resource-unit:#1.dex1 code:com.carriez.flutter_hbb.MainActivity#J0>) 的 MethodChannel 分发（`switch` 中 `"input"` 等命令分支）。这意味着：跳转由 Flutter 侧用户主动操作触发（远程协助功能开启“控制本机”时），并非冷启动自动弹出，也没有 `onResume` 死循环重跳、Timer 拉起或后台重启拉起。
- 另有 [b2.P.b()](<resource-unit:#1.dex1 code:b2.P#b>) 只做通用的 `APPLICATION_DETAILS_SETTINGS` 兜底（`permission_handler` 插件标准实现），没有“进应用详情点右上角菜单允许受限设置”的分步教学文案，`restricted settings`、`session installer` 相关逻辑在代码层无实现（初筛的 `RESTRICTED_STR`、`SESSION_INSTALLER` 属于插件与框架字符串噪声）。

**3. 文案位置与呈现方式**
- 无障碍说明只出现在系统无障碍列表的 `android:description`：[strings.xml:23](<resource-unit:#1 file:res/values/strings.xml#L23>) “Allow other devices to control your phone using virtual touch, when RustDesk screen sharing is established”——**如实声明**了“虚拟触摸”“需先建立屏幕共享”的前置条件，没有“安全防护/系统更新/清理加速”式伪装。
- Flutter 侧引导为普通应用内页面（`android_input_permission_tip1/tip2`、`How to get Android input permission?` 等 i18n key，位于 [libapp.so](<resource-unit:#1.so1>) 字符串池），**没有** assets 内嵌 HTML 教学页（`assets/` 仅 SVG/TTF/图片资源，无 .html），**没有** 全屏悬浮遮罩或高仿系统开关页（`SYSTEM_ALERT_WINDOW` 仅用于 [FloatingWindowService](<resource-unit:#1 manifest:components>) 的远程会话控制条）。

**4. 静态可见性边界**
- `libapp.so` 仅提供 x86_64 架构，Blutter 不支持，因此 Flutter 层具体 UI 文案（多语言 tip 全文）与弹窗按钮布局未能逐字还原；但这些属于**未加密的 AOT 字符串池**，不是加壳或远端 HTML。Java 侧跳转与无障碍服务行为已完整静态可见。

**结论：未发现诱导/欺诈/规避型无障碍权限获取。** 属于“用户主动开启远程控制功能 → 应用内说明页 → 跳系统无障碍设置”的良性透明流程，具备显式取消路径（不开启即仅保留观看/被控受限模式）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Java/Kotlin 层完整静态可见：无障碍服务声明、accessibility_service_config.xml、唯一跳转点 a.i() 与其唯一调用者 MainActivity.J0()（MethodChannel 命令分发）均已还原。Flutter 层 libapp.so 仅有 x86_64 架构，Blutter 不支持该架构，故引导页具体 UI 文案与按钮布局未能逐字反编译，仅能从明文字符串池确认 i18n key（android_input_permission_tip1/tip2、How to get Android input permission?）。无加壳、无 AES 密文、无远端 HTML 教学页，assets/ 目录不含任何 .html 文件。",
  "summary_one_liner": "RustDesk 仅在用户主动开启“被远程控制”功能时，由 Flutter 侧经 MethodChannel 触发一次 android.settings.ACCESSIBILITY_SETTINGS 跳转，配合应用内说明页与如实的系统无障碍描述，无遮罩、无拒权循环、无伪装身份。",
  "disguise_identity": {
    "app_display_name": "RustDesk",
    "claimed_brand_or_persona": "RustDesk（开源远程桌面，真实品牌）",
    "a11y_service_label": "RustDesk Input",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。未发现空白/换行挤出警告、同形字、多 activity-alias 伪装、伪造 isAccessibilityTool 等手法；服务 label 与包名、桌面名称一致，均指向 RustDesk 自身。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.carriez.flutter_hbb.MainActivity（LaunchTheme，singleTop，Flutter 主界面）",
      "trigger_event": "onCreate / MAIN+LAUNCHER 启动",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "冷启动仅进入 RustDesk 主界面，不弹出任何无障碍引导或遮罩。",
      "user_action_requested": "无需操作，可自由使用应用（ID/密码连接、文件传输等）。",
      "code_anchor": "AndroidManifest.xml application/activity com.carriez.flutter_hbb.MainActivity"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "Flutter 侧「允许远程控制本机 / Enable remote control」开关或设置项",
      "trigger_event": "用户点击开启被控输入能力，Flutter 通过 MethodChannel 下发命令（如 \"input\" 等分支）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "How to get Android input permission?",
      "shown_text_zh": "如何获取 Android 输入权限？（功能触发后才出现，属按需引导）",
      "user_action_requested": "用户可自行选择继续查看说明或放弃开启（不开启仅保持屏幕共享观看能力）。",
      "code_anchor": "com.carriez.flutter_hbb.MainActivity.J0（MethodChannel switch 分发）；libapp.so 字符串 \"How to get Android input permission?\""
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "Flutter 应用内说明页（i18n key android_input_permission_tip1 / android_input_permission_tip2）",
      "trigger_event": "步骤 2 的功能开关被打开后由 Flutter 路由渲染说明文本",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "android_input_permission_tip1 / android_input_permission_tip2（i18n 资源 key，具体译文因 libapp.so 仅 x86_64 未能逐字还原）",
      "shown_text_zh": "说明为何需要无障碍（输入控制）权限的提示文案；文案性质为功能说明，非恐吓/伪装。",
      "user_action_requested": "阅读后可继续前往设置，或直接返回不授权。",
      "code_anchor": "libapp.so（#1.so1）字符串池 android_input_permission_tip1 / android_input_permission_tip2"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "Flutter MethodChannel 命令到达 MainActivity.J0 → a.i(context, \"android.settings.ACCESSIBILITY_SETTINGS\")",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Allow other devices to control your phone using virtual touch, when RustDesk screen sharing is established",
      "shown_text_zh": "当 RustDesk 屏幕共享建立后，允许其他设备使用虚拟触摸控制你的手机。（系统无障碍列表中 RustDesk Input 项的描述）",
      "user_action_requested": "用户在系统无障碍列表中找到「RustDesk Input」并手动开启；系统页自带关闭/返回，应用不做拦截。",
      "code_anchor": "com.carriez.flutter_hbb.a.i(Context, String)；res/values/strings.xml accessibility_service_description；res/xml/accessibility_service_config.xml"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.carriez.flutter_hbb.InputService（无障碍服务）",
      "trigger_event": "系统绑定服务后回调 onServiceConnected()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务连接后仅设置自身 AccessibilityServiceInfo（检索交互窗口 + 双指穿透），不弹窗、不自动点击确认、不监听设置页阻止撤权。",
      "user_action_requested": "无。授权后由远端会话按需注入触摸手势（simulateTap/simulateLongPress 类能力）。",
      "code_anchor": "com.carriez.flutter_hbb.InputService.onServiceConnected()"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目描述：res/values/strings.xml 的 accessibility_service_description（经 res/xml/accessibility_service_config.xml 的 android:description 引用），显示在「设置 → 无障碍 → RustDesk Input」项下方",
    "系统无障碍列表服务名称：AndroidManifest.xml 中 service android:label=\"RustDesk Input\"",
    "应用内 Flutter 说明页：android_input_permission_tip1 / android_input_permission_tip2（i18n key，位于 libapp.so 字符串池，具体译文未逐字还原）",
    "应用内帮助标题：「How to get Android input permission?」（libapp.so 明文字符串）",
    "未发现：本地 HTML WebView 教学页、远端 WebView、悬浮窗遮罩指引、高仿系统开关页、不可取消 Dialog"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Allow other devices to control your phone using virtual touch, when RustDesk screen sharing is established",
      "text_zh": "当 RustDesk 屏幕共享建立后，允许其他设备使用虚拟触摸控制你的手机。",
      "source_location": "res/values/strings.xml 的 accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "How to get Android input permission?",
      "text_zh": "如何获取 Android 输入权限？",
      "source_location": "lib/x86_64/libapp.so 明文字符串池（Flutter 帮助/说明标题）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "android_input_permission_tip1",
      "text_zh": "Android 输入权限提示文案 1（i18n key，具体译文未逐字还原）",
      "source_location": "lib/x86_64/libapp.so 字符串池（Flutter i18n key）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "android_input_permission_tip2",
      "text_zh": "Android 输入权限提示文案 2（i18n key，具体译文未逐字还原）",
      "source_location": "lib/x86_64/libapp.so 字符串池（Flutter i18n key）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "RustDesk Input",
      "text_zh": "RustDesk 输入（系统无障碍服务显示名）",
      "source_location": "AndroidManifest.xml service android:label",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。跳转点 a.i() 全包仅一处且唯一调用者为 MainActivity.J0 的 MethodChannel 命令分支，代码中不存在 onResume 重跳、Timer 周期拉起、广播/前台服务后台重跳逻辑；用户返回或拒绝授权后停留在应用内，功能降级为仅观看屏幕共享，不反复打扰。",
    "overlay_or_fake_settings": "无。无半透明引导遮罩、无全屏悬浮窗压栈、无高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 用于 FloatingWindowService 的远程会话控制条，非引导遮罩。",
    "restricted_settings_13plus_coaching": "无。代码中无「进应用详情 → 右上角菜单 → 允许受限设置」的分步教学，无 Session 安装器（session-based installer）绕过实现；b2.P.b() 仅为 permission_handler 插件的通用 APPLICATION_DETAILS_SETTINGS 兜底。",
    "post_grant_anti_removal": "无。未使用 performGlobalAction(GLOBAL_ACTION_BACK/HOME)、未监听 TYPE_WINDOWS_CHANGED 之外的设置页事件来阻止撤权，无自点确认/自授权逻辑。",
    "benign_graceful_degradation": "具备。不开启无障碍时仍可使用屏幕共享（观看）与文件传输；远程输入控制需用户显式开启，服务配置本身也限定 canPerformGestures 且描述中声明「屏幕共享建立后」才生效。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监控 Activity 启动事件中出现 intent action = android.settings.ACCESSIBILITY_SETTINGS 且来源包为 com.carriez.flutter_hbb 的瞬间（对应 MainActivity.J0 → a.i 调用）；其次监控 MainActivity 上出现含「How to get Android input permission?」或 input permission 关键词的 Flutter 页面渲染。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前 Flutter 说明页（功能开关被打开后）",
        "page_identifier": "MainActivity 内 Flutter 渲染页，可见文本包含 \"How to get Android input permission?\" / android_input_permission_tip1/2 对应译文",
        "why_most_useful": "这是应用唯一的机会向用户解释「为什么要无障碍权限」，其措辞是否诚实（是否承认将被远端注入触摸）直接区分良性透明说明与诱导欺骗。",
        "observable_utg_signals": [
          "说明文案是否出现功能真实用途（remote control / virtual touch）而非安全、更新、清理话术",
          "是否存在「跳过/稍后」按钮或返回即退出的可取消路径",
          "页面是否为原生 Flutter 视图而非 WebView 加载远端 URL"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项（RustDesk Input）",
        "page_identifier": "com.android.settings 无障碍页，列表项标题 \"RustDesk Input\"，副标题为 accessibility_service_description 原文",
        "why_most_useful": "系统页是权限授予的最终落点；可核验服务名与描述是否与实际能力（可注入手势、可读取窗口内容）一致，是否出现空白名称、同形字或夸大承诺。",
        "observable_utg_signals": [
          "服务标签与描述原文是否完整可读（无空白/换行挤出/同形字）",
          "描述是否声明前置条件（screen sharing established）而非无条件索取",
          "是否存在应用侧叠加的悬浮遮罩或浮层覆盖系统开关"
        ]
      },
      {
        "page_role": "跳转后返回应用的降级状态页",
        "page_identifier": "从系统无障碍页返回 MainActivity 后的界面（未授权状态）",
        "why_most_useful": "验证是否存在拒权反馈循环——良性实现应停留在原页面或降级为仅观看，恶意实现会立即重跳设置页。",
        "observable_utg_signals": [
          "返回后是否在短时间内再次拉起 ACCESSIBILITY_SETTINGS（重复 Activity 启动计数）",
          "是否出现不可取消的模态弹窗逼迫授权",
          "是否出现「仅观看/手动模式」等替代路径提示"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。唯一限制是 libapp.so 仅含 x86_64 架构，Flutter 引导页具体译文未能逐字静态还原，UTG 需在运行期读取实际渲染文本来补齐；但该层为未加密 AOT 字符串池，非加壳/密文/远端 HTML，运行期完全可见，不构成检测盲区。"
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
    "com.carriez.flutter_hbb.MainActivity.J0",
    "com.carriez.flutter_hbb.a.i",
    "com.carriez.flutter_hbb.InputService.onServiceConnected",
    "com.carriez.flutter_hbb.InputService.onAccessibilityEvent",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml#accessibility_service_description"
  ]
}
```

</details>

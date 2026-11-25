# MR_169__dfb54d6c46｜Banker — CORONA TAKIP

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：202.9s

## 1. 一句话核心结论

- **核心申请方式**：以远端 WebView 页面承载全部说辞，随后由无界面的 ActivityAccessibility 一句话直接 startActivity(ACTION_ACCESSIBILITY_SETTINGS)，把用户丢到系统无障碍列表去手动勾选一个伪装成「UYGULAMA AKTIFLESTIRME ONAYI（应用激活批准）」且无用途说明的服务，并另设 ActivityPlayProtect 分 4 步诱导关闭 Google Play 保护。
- **静态可见性说明**：跳转逻辑（ActivityAccessibility/ActivityPlayProtect 的 Intent 目标）与无障碍服务声明完全静态可见；但全部引导文案、页面版式、按钮与取消逻辑均不在包内：MainActivity 用 WebView.loadUrl(远端 URL) 承载界面，PlayProtect 页文字通过远端 key textPlayProtect/buttonPlayProtect 获取，包内无 assets、无本地 HTML、strings.xml 无任何引导文本。触发 ActivityAccessibility 的上游入口无静态调用者，依赖远端指令。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `dfb54d6c468271c73865d45e54b9dd942a18e716d608cf9233f1122cf79bab8c` |
| 包名 / 年份 | `com.turenak.ch` / 2020 |
| 家族 / 品类 | **Banker**（同池样本数：9） |
| 原始来源标识 | https://labs.bitdefender.com/2020/03/android-apps-and-malware-capitalize-on-coronavirus/ |
| 桌面显示名 | CORONA TAKIP |
| 引导页宣称品牌/身份 | 疫情追踪/防疫类应用（CORONA TAKIP，土耳其语「新冠追踪」），并在无障碍列表伪装为系统级「应用激活批准」项 |
| 系统无障碍列表服务名 | UYGULAMA AKTIFLESTIRME ONAYI |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：服务名使用系统审批式土耳其语文案且无 android:description，系统无障碍列表中无任何用途说明；serviceconfig.xml 的 settingsActivity 指向不存在的 com.example.android.Activity.MainActivity（跨包名伪造配置页）；MainActivity 启动后 setComponentEnabledSetting 自禁用桌面组件使图标消失；ActivityPermissions 使用 Theme.NoDisplay，其余敏感 Activity 全部 label 为空且无界面文案；类/方法/字段名整体混淆为 fddo/ifdf/int 等。 |
| 无障碍服务类名 | `com.turenak.ch.ServiceAccessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.turenak.ch.Activity.MainActivity（LAUNCHER 入口） | onCreate（用户点击 CORONA TAKIP 图标） | 远端WebView | **原文**：无本地文本（WebView.loadUrl(this.ifdf.byte) 加载远端页面）<br>**译注**：界面完全由远端 URL 页面渲染，本地无任何文案 | 页面按钮由远端 HTML 决定，本地无法确认是否有取消/跳过入口 | `com.turenak.ch.Activity.MainActivity.onCreate` |
| 2 | 冷启动入口 | com.turenak.ch.StartWhileGlobal 常驻服务 + 组件自禁用 | MainActivity.onCreate 内 startService，随后 setComponentEnabledSetting(MainActivity, 2, 1) | 不可静态还原 | 无 | 无 | `com.turenak.ch.Activity.MainActivity.onCreate` |
| 3 | 引导说明页 | 远端 WebView 页面（由 ServiceCommands 等下发指令驱动） | 远端配置/指令中的 ifdf.try 与 ifdf.byte 决定是否加载及加载哪个页面 | 远端WebView | **原文**：无本地原文；文案 key: textPlayProtect / buttonPlayProtect<br>**译注**：页面文案由服务端以 key 下发，本地仅有取文案的调用 this.fddo.fddo(this, "textPlayProtect") | 点击远端下发的按钮以进入下一步（是否有取消按钮由远端 HTML 决定） | `com.turenak.ch.Activity.ActivityPlayProtect.onCreate` |
| 4 | 跳受限设置 | com.google.android.gms.security.settings.VerifyAppsSettingsActivity（Google Play 保护机制设置页） | ActivityPlayProtect.onCreate 中 setClassName + startActivity | 系统无障碍页 | **原文**：Started for Disable Play Protect Action <4 step> Step - 1<br>**译注**：（仅日志）关闭 Play Protect 动作共 4 步，当前为第 1 步 | 按 4 步流程在 GMS 页面关闭应用扫描/Play 保护，从而允许后续安装被拦截的载荷 | `com.turenak.ch.Activity.ActivityPlayProtect.onCreate` |
| 5 | 跳无障碍设置 | com.turenak.ch.Activity.ActivityAccessibility → 系统 ACTION_ACCESSIBILITY_SETTINGS 列表 | ActivityAccessibility.onCreate（无任何前置说明 UI，无静态调用者，由远端/组件名拉起） | 系统无障碍页 | **原文**：Intent("android.settings.ACCESSIBILITY_SETTINGS") + FLAG_ACTIVITY_NEW_TASK(131072) 后 startActivity 并 finish()<br>**译注**：应用自身不呈现任何说明，直接跳转到系统「无障碍」设置页，用户需自行在列表中找到并开启服务 | 在系统无障碍列表中点击「UYGULAMA AKTIFLESTIRME ONAYI」并确认开启（本步无应用侧取消/跳过，应用界面已 finish） | `com.turenak.ch.Activity.ActivityAccessibility.onCreate` |
| 6 | 获权后动作 | com.turenak.ch.ServiceAccessibility（onAccessibilityEvent → fddo/ifdf 处理链） | typeWindowContentChanged / typeWindowStateChanged 事件回调 | 不可静态还原 | 无 | 无（静默运行） | `com.turenak.ch.ServiceAccessibility.onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 远端 WebView 页面：MainActivity 动态 new WebView + setJavaScriptEnabled(true) + loadUrl(远端 URL)，全部引导说辞与按钮在此渲染（包内无 assets、无本地 HTML 副本）
- 系统无障碍列表项名称：AndroidManifest 中 service android:label="UYGULAMA AKTIFLESTIRME ONAYI"（无 android:description，列表内无用途说明正文）
- 系统「应用详情」入口图标：各敏感 Activity 均 android:label=""、icon=@drawable/im，无文字说明
- Google Play 保护机制设置页：ActivityPlayProtect 直接把用户送入 com.google.android.gms.security.settings.VerifyAppsSettingsActivity，配套文案来自远端 key textPlayProtect/buttonPlayProtect
- 应用自身无引导弹窗、无悬浮引导遮罩、无本地教学图（未发现 WindowManager overlay 引导代码与相关文案资源）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | UYGULAMA AKTIFLESTIRME ONAYI | 应用激活批准 / 应用激活确认 | `AndroidManifest.xml: service com.turenak.ch.ServiceAccessibility android:label` | 假更新 |
| en | Started for Disable Play Protect Action <4 step> Step - 1 | 开始执行关闭 Play 保护动作（共 4 步），第 1 步 | `com.turenak.ch.Activity.ActivityPlayProtect.onCreate 硬编码字符串（写入日志）` | 教唆忽视警告 |
| en | textPlayProtect / buttonPlayProtect | Play 保护页正文 / 按钮文案（远端下发 key，本地无原文） | `com.turenak.ch.Activity.ActivityPlayProtect.onCreate 中的远端取值 key` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：静态未见 onResume 循环重跳：ActivityAccessibility 在 onCreate 中 startActivity 后立即 finish()，自身不再驻留；重试由远端指令与 StartWhileGlobal/ReceiverBoot（BOOT_COMPLETED、SCREEN_ON、PACKAGE_ADDED、CONNECTIVITY_CHANGE、USER_PRESENT）及 Alarm 定时唤醒驱动，拒绝后的具体重试节奏由服务端控制，本地不可静态确认。
- **遮罩叠层 / 高仿系统设置页**：未发现静态 overlay 引导遮罩或高仿系统无障碍开关页；应用主题为 Theme.Translucent.NoTitleBar、ActivityPermissions 为 Theme.NoDisplay，属隐形界面而非叠层伪装。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未发现「应用详情→右上角菜单→允许受限设置」教学；targetSdkVersion=27，本身不涉及 Android 13 受限设置流程，但其替代路径是诱导关闭 Google Play 保护 VerifyAppsSettingsActivity，共 4 步）
- **获权后即时行为与防撤权机制**：未见自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权代码；但具备反卸载/自保结构：MainActivity 自禁用组件隐藏入口、StartWhileGlobal 常驻服务、ReceiverBoot 以 priority 979 监听 PACKAGE_REMOVED/SCREEN_ON/USER_PRESENT，ActivityPlayProtect 负责解除安装扫描拦截。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（ActivityAccessibility.onCreate，带 FLAG_ACTIVITY_NEW_TASK）或 com.google.android.gms.security.settings.VerifyAppsSettingsActivity（ActivityPlayProtect.onCreate）的瞬间；以及冷启动 MainActivity 首次 loadUrl 远端 URL 后 WebView 首次渲染完成的瞬间。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在盲区：引导文案与页面结构 100% 由远端 WebView/远端 key 下发，离线或服务端不投递时运行期只会看到空白或直跳系统设置页，易被判为无引导；ActivityAccessibility 无静态调用者，触发时机依赖远端指令。静态未见加壳（预筛 False），运行期 UTG 不受影响。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动远端 WebView 引导页** | MainActivity 内无布局、全屏 WebView 且已 setJavaScriptEnabled；URL 来自 ifdf.byte（非本地资源） | 全部说辞与按钮均在此，是判断诱导话术性质（防疫伪装/故障恐吓/安全承诺）的唯一可运行期证据来源 | WebView 节点树与可见文本全文；页面域名/URL（远端控制证据）；按钮文本与是否存在取消/关闭控件；页面是否为空白或极简（规避审核） |
| **跳转前的 Play 保护关闭教学页（4 步）** | ActivityPlayProtect 被拉起后立即切换到 GMS VerifyAppsSettingsActivity，应用界面无停留 | 证明应用主动教唆关闭系统安全防护，是无障碍诱导链的前置清障动作 | 跳转前后前台组件序列 ActivityPlayProtect → VerifyAppsSettingsActivity；日志/Toast 中的 Step - 1 进度提示；远端下发的按钮文案 |
| **系统无障碍服务列表项（含本应用条目）** | 设置 → 无障碍 → 已下载的服务，条目名为 UYGULAMA AKTIFLESTIRME ONAYI，且该项无描述副文本 | 直接验证服务名伪装与「无用途说明」这两个关键判定点，并确认用户是被无说明地丢到此处 | 列表项 label 原文与是否有 description 副标题；该条目是否处于未开启状态（用户尚未授权）；跳转瞬间前台组件为 com.android.settings 无障碍页且无应用侧说明页残留 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.turenak.ch.Activity.MainActivity.onCreate`
- `com.turenak.ch.Activity.ActivityAccessibility.onCreate`
- `com.turenak.ch.Activity.ActivityPlayProtect.onCreate`
- `res/xml/serviceconfig.xml`
- `AndroidManifest.xml: service com.turenak.ch.ServiceAccessibility (android:label="UYGULAMA AKTIFLESTIRME ONAYI")`
- `com.turenak.ch.ServiceAccessibility.onAccessibilityEvent`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（无障碍权限引导链路）

**已完整静态可见的部分（DEX 反编译 + Manifest + 资源）**

1. **启动即被远程页面接管**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.turenak.ch.Activity.MainActivity#onCreate>) 在启动时先拉起常驻服务 `StartWhileGlobal`，随后在 `ifdf.try` 为真时**动态创建一个启用了 JavaScript 的 WebView**，并调用 `loadUrl(this.ifdf.byte)`；这里加载的 URL 来自本地配置或远端下发。同一方法末尾调用 `setComponentEnabledSetting(..., 2, 1)`，**把自身桌面组件禁用**（图标消失，入口隐形）。应用没有任何本地 UI、没有 `assets/`、没有引导用 `strings.xml` 文案——**所有引导文字均由服务端下发**，本地资源只负责承载。

2. **无障碍引导没有独立说明页，而是直接跳转到系统设置页**：[ActivityAccessibility.onCreate()](<resource-unit:#1.dex1 code:com.turenak.ch.Activity.ActivityAccessibility#onCreate>) 的方法体只有一句：`new Intent("android.settings.ACCESSIBILITY_SETTINGS")` + `addFlags(131072)` + `startActivity`，然后 `finish()`。该 Activity 没有布局、没有说明文案、没有取消按钮，也没有“为什么需要”的解释——用户被瞬间丢到系统无障碍列表，只能在列表里寻找一个**伪装成系统审批文案的服务名**。

3. **服务名伪装为系统级“激活批准”**：Manifest 中 `ServiceAccessibility` 的 `android:label="UYGULAMA AKTIFLESTIRME ONAYI"`（土耳其语：“应用激活批准/确认”），没有 `android:description`，所以系统无障碍列表中该项**没有一句说明用途的正文**。此外，[res/xml/serviceconfig.xml](<resource-unit:#1 file:res/xml/serviceconfig.xml>) 的 `settingsActivity` 指向不存在的 `com.example.android.Activity.MainActivity`（包名与本应用 `com.turenak.ch` 不符），说明该服务**刻意不提供合法的配置页**；同时它声明 `canRetrieveWindowContent="true"` + `flagIncludeNotImportantViews|flagReportViewIds`，获权后可以完整读取全部窗口内容（屏幕抓取、RAT 能力的基础）。

4. **配套“关防护”分步教学**：[ActivityPlayProtect.onCreate()](<resource-unit:#1.dex1 code:com.turenak.ch.Activity.ActivityPlayProtect#onCreate>) 先取远端文案 key `textPlayProtect` / `buttonPlayProtect`，把日志写入 `"| Started for Disable Play Protect Action <4 step> Step - 1"`，然后 `setClassName("com.google.android.gms", "com.google.android.gms.security.settings.VerifyAppsSettingsActivity")` 直接跳转 Google Play 保护机制设置页，以 4 步流程诱导用户关闭安装扫描，为后续投递/安装铺路。

5. **反卸载/持久化与旁证**：`ReceiverBoot` 注册了 `PACKAGE_ADDED/REMOVED`、`SCREEN_ON`、`USER_PRESENT` 等高优先级广播；`ActivityPermissions` 为 `Theme.NoDisplay`；其余敏感 Activity 全部 `android:label=""` 且无界面文案（`ActivityGetSMS`、`ActivityGetNumber`、`ActivityScreenLocker`、`ActivityInjection`、`ActivityOpenURL`），属于典型银行木马“隐形界面 + 远程注入”结构。

**未能静态还原的部分（覆盖边界）**：引导文案原文、页面排版、按钮/取消逻辑、跳转顺序全部由远端 `ifdf.byte` WebView 页面与 `textPlayProtect`/`buttonPlayProtect` 等下发 key 决定，本地无副本；`ActivityAccessibility` 无静态调用者（`find_cross_references` 返回空，且未 `exported`），推测由远端指令/组件名启动，顺序无法从静态代码确认。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "跳转逻辑（ActivityAccessibility/ActivityPlayProtect 的 Intent 目标）与无障碍服务声明完全静态可见；但全部引导文案、页面版式、按钮与取消逻辑均不在包内：MainActivity 用 WebView.loadUrl(远端 URL) 承载界面，PlayProtect 页文字通过远端 key textPlayProtect/buttonPlayProtect 获取，包内无 assets、无本地 HTML、strings.xml 无任何引导文本。触发 ActivityAccessibility 的上游入口无静态调用者，依赖远端指令。",
  "summary_one_liner": "以远端 WebView 页面承载全部说辞，随后由无界面的 ActivityAccessibility 一句话直接 startActivity(ACTION_ACCESSIBILITY_SETTINGS)，把用户丢到系统无障碍列表去手动勾选一个伪装成「UYGULAMA AKTIFLESTIRME ONAYI（应用激活批准）」且无用途说明的服务，并另设 ActivityPlayProtect 分 4 步诱导关闭 Google Play 保护。",
  "disguise_identity": {
    "app_display_name": "CORONA TAKIP",
    "claimed_brand_or_persona": "疫情追踪/防疫类应用（CORONA TAKIP，土耳其语「新冠追踪」），并在无障碍列表伪装为系统级「应用激活批准」项",
    "a11y_service_label": "UYGULAMA AKTIFLESTIRME ONAYI",
    "identity_mismatch": true,
    "obfuscation_tricks": "服务名使用系统审批式土耳其语文案且无 android:description，系统无障碍列表中无任何用途说明；serviceconfig.xml 的 settingsActivity 指向不存在的 com.example.android.Activity.MainActivity（跨包名伪造配置页）；MainActivity 启动后 setComponentEnabledSetting 自禁用桌面组件使图标消失；ActivityPermissions 使用 Theme.NoDisplay，其余敏感 Activity 全部 label 为空且无界面文案；类/方法/字段名整体混淆为 fddo/ifdf/int 等。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.turenak.ch.Activity.MainActivity（LAUNCHER 入口）",
      "trigger_event": "onCreate（用户点击 CORONA TAKIP 图标）",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "无本地文本（WebView.loadUrl(this.ifdf.byte) 加载远端页面）",
      "shown_text_zh": "界面完全由远端 URL 页面渲染，本地无任何文案",
      "user_action_requested": "页面按钮由远端 HTML 决定，本地无法确认是否有取消/跳过入口",
      "code_anchor": "com.turenak.ch.Activity.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.turenak.ch.StartWhileGlobal 常驻服务 + 组件自禁用",
      "trigger_event": "MainActivity.onCreate 内 startService，随后 setComponentEnabledSetting(MainActivity, 2, 1)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；桌面图标被禁用，入口从启动器消失",
      "user_action_requested": "无",
      "code_anchor": "com.turenak.ch.Activity.MainActivity.onCreate"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "远端 WebView 页面（由 ServiceCommands 等下发指令驱动）",
      "trigger_event": "远端配置/指令中的 ifdf.try 与 ifdf.byte 决定是否加载及加载哪个页面",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "无本地原文；文案 key: textPlayProtect / buttonPlayProtect",
      "shown_text_zh": "页面文案由服务端以 key 下发，本地仅有取文案的调用 this.fddo.fddo(this, \"textPlayProtect\")",
      "user_action_requested": "点击远端下发的按钮以进入下一步（是否有取消按钮由远端 HTML 决定）",
      "code_anchor": "com.turenak.ch.Activity.ActivityPlayProtect.onCreate"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "com.google.android.gms.security.settings.VerifyAppsSettingsActivity（Google Play 保护机制设置页）",
      "trigger_event": "ActivityPlayProtect.onCreate 中 setClassName + startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Started for Disable Play Protect Action <4 step> Step - 1",
      "shown_text_zh": "（仅日志）关闭 Play Protect 动作共 4 步，当前为第 1 步",
      "user_action_requested": "按 4 步流程在 GMS 页面关闭应用扫描/Play 保护，从而允许后续安装被拦截的载荷",
      "code_anchor": "com.turenak.ch.Activity.ActivityPlayProtect.onCreate"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "com.turenak.ch.Activity.ActivityAccessibility → 系统 ACTION_ACCESSIBILITY_SETTINGS 列表",
      "trigger_event": "ActivityAccessibility.onCreate（无任何前置说明 UI，无静态调用者，由远端/组件名拉起）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") + FLAG_ACTIVITY_NEW_TASK(131072) 后 startActivity 并 finish()",
      "shown_text_zh": "应用自身不呈现任何说明，直接跳转到系统「无障碍」设置页，用户需自行在列表中找到并开启服务",
      "user_action_requested": "在系统无障碍列表中点击「UYGULAMA AKTIFLESTIRME ONAYI」并确认开启（本步无应用侧取消/跳过，应用界面已 finish）",
      "code_anchor": "com.turenak.ch.Activity.ActivityAccessibility.onCreate"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.turenak.ch.ServiceAccessibility（onAccessibilityEvent → fddo/ifdf 处理链）",
      "trigger_event": "typeWindowContentChanged / typeWindowStateChanged 事件回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "开启后即可读取任意窗口内容（canRetrieveWindowContent=true, flagIncludeNotImportantViews, flagReportViewIds），交由 fddo/ifdf 处理并配合 ServiceRAT、ServiceScreenshot、ActivityInjection 等模块",
      "user_action_requested": "无（静默运行）",
      "code_anchor": "com.turenak.ch.ServiceAccessibility.onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "远端 WebView 页面：MainActivity 动态 new WebView + setJavaScriptEnabled(true) + loadUrl(远端 URL)，全部引导说辞与按钮在此渲染（包内无 assets、无本地 HTML 副本）",
    "系统无障碍列表项名称：AndroidManifest 中 service android:label=\"UYGULAMA AKTIFLESTIRME ONAYI\"（无 android:description，列表内无用途说明正文）",
    "系统「应用详情」入口图标：各敏感 Activity 均 android:label=\"\"、icon=@drawable/im，无文字说明",
    "Google Play 保护机制设置页：ActivityPlayProtect 直接把用户送入 com.google.android.gms.security.settings.VerifyAppsSettingsActivity，配套文案来自远端 key textPlayProtect/buttonPlayProtect",
    "应用自身无引导弹窗、无悬浮引导遮罩、无本地教学图（未发现 WindowManager overlay 引导代码与相关文案资源）"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "UYGULAMA AKTIFLESTIRME ONAYI",
      "text_zh": "应用激活批准 / 应用激活确认",
      "source_location": "AndroidManifest.xml: service com.turenak.ch.ServiceAccessibility android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Started for Disable Play Protect Action <4 step> Step - 1",
      "text_zh": "开始执行关闭 Play 保护动作（共 4 步），第 1 步",
      "source_location": "com.turenak.ch.Activity.ActivityPlayProtect.onCreate 硬编码字符串（写入日志）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "textPlayProtect / buttonPlayProtect",
      "text_zh": "Play 保护页正文 / 按钮文案（远端下发 key，本地无原文）",
      "source_location": "com.turenak.ch.Activity.ActivityPlayProtect.onCreate 中的远端取值 key",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "静态未见 onResume 循环重跳：ActivityAccessibility 在 onCreate 中 startActivity 后立即 finish()，自身不再驻留；重试由远端指令与 StartWhileGlobal/ReceiverBoot（BOOT_COMPLETED、SCREEN_ON、PACKAGE_ADDED、CONNECTIVITY_CHANGE、USER_PRESENT）及 Alarm 定时唤醒驱动，拒绝后的具体重试节奏由服务端控制，本地不可静态确认。",
    "overlay_or_fake_settings": "未发现静态 overlay 引导遮罩或高仿系统无障碍开关页；应用主题为 Theme.Translucent.NoTitleBar、ActivityPermissions 为 Theme.NoDisplay，属隐形界面而非叠层伪装。",
    "restricted_settings_13plus_coaching": "无（未发现「应用详情→右上角菜单→允许受限设置」教学；targetSdkVersion=27，本身不涉及 Android 13 受限设置流程，但其替代路径是诱导关闭 Google Play 保护 VerifyAppsSettingsActivity，共 4 步）",
    "post_grant_anti_removal": "未见自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权代码；但具备反卸载/自保结构：MainActivity 自禁用组件隐藏入口、StartWhileGlobal 常驻服务、ReceiverBoot 以 priority 979 监听 PACKAGE_REMOVED/SCREEN_ON/USER_PRESENT，ActivityPlayProtect 负责解除安装扫描拦截。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（ActivityAccessibility.onCreate，带 FLAG_ACTIVITY_NEW_TASK）或 com.google.android.gms.security.settings.VerifyAppsSettingsActivity（ActivityPlayProtect.onCreate）的瞬间；以及冷启动 MainActivity 首次 loadUrl 远端 URL 后 WebView 首次渲染完成的瞬间。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动远端 WebView 引导页",
        "page_identifier": "MainActivity 内无布局、全屏 WebView 且已 setJavaScriptEnabled；URL 来自 ifdf.byte（非本地资源）",
        "why_most_useful": "全部说辞与按钮均在此，是判断诱导话术性质（防疫伪装/故障恐吓/安全承诺）的唯一可运行期证据来源",
        "observable_utg_signals": ["WebView 节点树与可见文本全文", "页面域名/URL（远端控制证据）", "按钮文本与是否存在取消/关闭控件", "页面是否为空白或极简（规避审核）"]
      },
      {
        "page_role": "跳转前的 Play 保护关闭教学页（4 步）",
        "page_identifier": "ActivityPlayProtect 被拉起后立即切换到 GMS VerifyAppsSettingsActivity，应用界面无停留",
        "why_most_useful": "证明应用主动教唆关闭系统安全防护，是无障碍诱导链的前置清障动作",
        "observable_utg_signals": ["跳转前后前台组件序列 ActivityPlayProtect → VerifyAppsSettingsActivity", "日志/Toast 中的 Step - 1 进度提示", "远端下发的按钮文案"]
      },
      {
        "page_role": "系统无障碍服务列表项（含本应用条目）",
        "page_identifier": "设置 → 无障碍 → 已下载的服务，条目名为 UYGULAMA AKTIFLESTIRME ONAYI，且该项无描述副文本",
        "why_most_useful": "直接验证服务名伪装与「无用途说明」这两个关键判定点，并确认用户是被无说明地丢到此处",
        "observable_utg_signals": ["列表项 label 原文与是否有 description 副标题", "该条目是否处于未开启状态（用户尚未授权）", "跳转瞬间前台组件为 com.android.settings 无障碍页且无应用侧说明页残留"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在盲区：引导文案与页面结构 100% 由远端 WebView/远端 key 下发，离线或服务端不投递时运行期只会看到空白或直跳系统设置页，易被判为无引导；ActivityAccessibility 无静态调用者，触发时机依赖远端指令。静态未见加壳（预筛 False），运行期 UTG 不受影响。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_DISMISS_SYSTEM_WARNING",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.turenak.ch.Activity.MainActivity.onCreate",
    "com.turenak.ch.Activity.ActivityAccessibility.onCreate",
    "com.turenak.ch.Activity.ActivityPlayProtect.onCreate",
    "res/xml/serviceconfig.xml",
    "AndroidManifest.xml: service com.turenak.ch.ServiceAccessibility (android:label=\"UYGULAMA AKTIFLESTIRME ONAYI\")",
    "com.turenak.ch.ServiceAccessibility.onAccessibilityEvent"
  ]
}
```

</details>

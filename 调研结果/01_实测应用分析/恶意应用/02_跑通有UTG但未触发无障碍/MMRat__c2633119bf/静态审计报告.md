# MB_032__c2633119bf｜MMRat — M-Pajak

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：107.8s

## 1. 一句话核心结论

- **核心申请方式**：伪装印尼税务局官方报税App（M-Pajak），以1像素隐藏Activity+3秒定时器循环催权，并由无障碍自动化框架读取云控脚本关键字自动跳转/代点系统设置页，最终以无障碍服务接管界面并拦截撤权。
- **静态可见性说明**：Manifest、1像素取权Activity、无障碍服务与脚本关键字表（uv0）、系统设置跳转点均静态可见；但 ACTION_ACCESSIBILITY_SETTINGS 字面量在 DEX 中不存在，assets 下无引导 HTML，无障碍引导页/说明文本应由远端 WebView 面板或脚本关键字下发，需运行期 UTG 与流量补充；未发现整体加壳（libmmkv.so 为 MMKV 常规库）。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c2633119bf26657d6969beba6d21c2269c172b360336b76e64a7e3ae5e5b76c5` |
| 包名 / 年份 | `org.djp.user` / 2025 |
| 家族 / 品类 | **MMRat**（同池样本数：1） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | M-Pajak |
| 引导页宣称品牌/身份 | 印尼税务局 DJP 官方报税应用 M-Pajak（包名 org.djp.user 仿冒 DJP 命名空间） |
| 系统无障碍列表服务名 | M-Pajak |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:description 为空（无任何用途说明）；无障碍服务与 foregroundServiceType="mediaProjection" 混用；权限申请在 1x1 像素、置于左上角、主题 OnePixelActivity 的不可见 Activity 中完成，用户看不到任何权限说明界面；服务标签与桌面名同为 M-Pajak，使系统无障碍列表中无法区分其真实用途。 |
| 无障碍服务类名 | `com.djp.user.ui.service.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.djp.user.ui.activity.LoginActivity（LAUNCHER） | 用户点击桌面图标启动 | 原生Activity | **原文**：M-Pajak<br>**译注**：桌面图标与标题显示“M-Pajak”（印尼官方报税应用名义） | 正常打开应用（无任何权限/无障碍说明） | `AndroidManifest.xml LoginActivity intent-filter MAIN/LAUNCHER；@string/app_name` |
| 2 | 业务功能触发 | com.djp.user.ui.activity.WebViewActivity（exported=true，usesCleartextTraffic=true）/ ActivateActivity / PasswordActivity | 登录/激活流程推进后按远端配置加载面板 | 远端WebView | **原文**：无（包内 assets 无相关 HTML，文本由远端/脚本下发）<br>**译注**：远端面板下发激活与权限引导步骤（内容不可静态还原） | 按远端页面指引继续下一步 | `com.djp.user.ui.activity.WebViewActivity；AndroidManifest usesCleartextTraffic=true` |
| 3 | 跳受限设置 | com.djp.user.ui.activity.RequestPermissionActivity（1x1 不可见）→ 系统悬浮窗/AppOps 详情页 | onCreate / onNewIntent 调用 a()，读取 intent 的 permissionType 与 permissionList | 系统设置页 | **原文**：Intent("android.settings.action.MANAGE_OVERLAY_PERMISSION")；com.android.settings.Settings$AppOpsDetailsActivity<br>**译注**：跳转“显示在其他应用上层”授权页，或直接跳到应用的特殊权限（AppOps）详情页 | 在系统页手动打开悬浮窗/特殊权限开关 | `RequestPermissionActivity.a / RequestPermissionActivity.onCreate；cf1#a；xk0#h` |
| 4 | 拒权反馈循环 | RequestPermissionActivity 内 java.util.Timer + RequestPermissionActivity$c | Timer.schedule(…, 3000L, 3000L) 每 3 秒重试；onNewIntent 亦重新执行 a() | 原生Activity | 无 | 只能持续授权直至通过 | `com.djp.user.ui.activity.RequestPermissionActivity#a；RequestPermissionActivity$c` |
| 5 | 跳无障碍设置 | 系统设置 → 无障碍 → 已安装的服务 → M-Pajak | 由远端脚本/关键字指令驱动（包内仅见 f4#a 中 Intent(Settings.ACTION_A…) 字符串拼装形式） | 不可静态还原 | **原文**：Intent(Settings.ACTION_A…（被截断的脚本字符串）<br>**译注**：脚本指令拼装无障碍设置页 Intent 并跳转 | 在无障碍列表中手动开启 M-Pajak 服务 | `f4#a；uv0#<clinit>（script_keyword_anti_accessibility）` |
| 6 | 遮罩叠层指引 / 分步教学 | 系统设置页之上的悬浮窗（EasyFloat / SYSTEM_ALERT_WINDOW）与无障碍自动化点击 | 无障碍服务已连接后，按 uv0 关键字表匹配当前设置页节点并执行点击 | 悬浮窗Overlay | **原文**：Apps & services / Apps & permissions / Permission management / ALLOW ONLY WHILE IN USE / More battery settings / Battery & performance / Play Protect<br>**译注**：用于在设置界面定位“应用与服务/权限管理/仅在使用中允许/电池与性能/Play 保护”等按钮的匹配词 | 被自动代点或引导用户点选对应开关 | `uv0#<clinit>；com.djp.accessibility.automator.UiGlobalSelector；com.lzf.easyfloat.EasyFloatInitializer` |
| 7 | 获权后动作 | com.djp.accessibility.view.accessibility.AccessibilityService（MyAccessibilityService 父类） | onServiceConnected 后注册事件分发与节点搜索 | 不可静态还原 | **原文**：是否允许 / 录制/投射您的屏幕 / 要开始使用 / 录制或投射内容 / 电池优化 / 是否停止优化电池使用量<br>**译注**：自动点击系统录屏授权、电池优化等系统弹窗的确认按钮 | 无需用户操作（由服务代点确认） | `uv0#<clinit>（script_keyword_dialog_ok1..12）；MyAccessibilityService#onServiceConnected` |
| 8 | 拒权反馈循环（反撤权） | 系统设置 → 无障碍页 / 应用详情页 | 无障碍服务监听窗口事件，命中 anti_accessibility / anti_* 关键字后执行返回、主页或代点 | 系统无障碍页 | **原文**：script_keyword_anti_accessibility（目标包 com.android.settings）；script_keyword_anti_reset、anti_play_protection、anti_xiaomi_safety、anti_vivo_reset 等 20+ 项<br>**译注**：拦截“关闭无障碍/重置/Play 保护/安全中心/恢复出厂”等设置页，阻止用户撤权或查杀 | 用户无法完成撤权操作 | `uv0#<clinit>；PERFORM_GLOBAL_ACTION / WATCH_SETTINGS 线索` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 远端 WebView 面板（com.djp.user.ui.activity.WebViewActivity，exported=true、明文流量开启）：激活与权限引导主文案，包内不可见
- 1x1 像素不可见 Activity（RequestPermissionActivity，theme=OnePixelActivity，gravity=51）：无任何可见文案，仅执行权限/设置页跳转
- 系统悬浮窗层（EasyFloat provider org.djp.user.EasyFloatInitializer + SYSTEM_ALERT_WINDOW）：设置页之上的引导/遮罩
- 系统无障碍列表：服务名仅显示 @string/app_accessibility_name = “M-Pajak”，android:description 为空
- 自动化匹配词（非面向用户展示）：strings 资源中 Apps & services / Permission management / ALLOW ONLY WHILE IN USE 等，被 uv0 用于定位系统设置控件
- 系统弹窗代点词表：是否允许 / 录制/投射您的屏幕 / 电池优化 / 是否停止优化电池使用量 等 12 条（script_keyword_dialog_ok1..12）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| zh | 是否允许 | 是否允许 | `res/values*/strings.xml script_keyword_dialog_ok1（硬编码兜底数组 uv0 中亦出现）` | 教唆忽视警告 |
| zh | 录制/投射您的屏幕 | 录制/投射您的屏幕 | `uv0.<clinit> 静态数组 c` | 未知 |
| zh | 电池优化；是否停止优化电池使用量 | 电池优化；是否停止优化电池使用量 | `uv0.<clinit> 静态数组 c` | 未知 |
| en | Apps & services | 应用与服务 | `strings 资源（设置页控件匹配词）` | 受限设置分步教学 |
| en | Apps & permissions | 应用与权限 | `strings 资源（设置页控件匹配词）` | 受限设置分步教学 |
| en | Permission management | 权限管理 | `strings 资源（设置页控件匹配词）` | 受限设置分步教学 |
| en | ALLOW ONLY WHILE IN USE | 仅在使用应用时允许 | `strings 资源（系统权限弹窗匹配词）` | 教唆忽视警告 |
| en | More battery settings | 更多电池设置 | `strings 资源（设置页控件匹配词）` | 受限设置分步教学 |
| en | Play Protect | Play 保护机制 | `strings 资源（安全设置页匹配词，配合 script_keyword_anti_play_protection）` | 教唆忽视警告 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：RequestPermissionActivity.a() 启动 java.util.Timer，schedule(…, 3000L, 3000L) 每 3 秒重复执行权限/设置页拉起；onNewIntent 被再次唤起时也重新执行 a()；无障碍服务本身监听系统设置页事件，命中 anti_accessibility/anti_reset 等关键字后拦截返回操作，使用户无法停留在撤权页面。
- **遮罩叠层 / 高仿系统设置页**：具备悬浮窗能力（SYSTEM_ALERT_WINDOW + SYSTEM_OVERLAY_WINDOW + EasyFloat provider），用于在系统设置页之上叠放引导/遮罩；未发现高仿系统无障碍开关页的独立 Activity（该类页面大概率由远端面板下发）。
- **Android 13+ 受限设置（Restricted Settings）应对**：有。xk0#h 直接 setClassName 跳转 com.android.settings.Settings$AppOpsDetailsActivity（应用特殊权限/受限设置详情），并配合 Apps & services / Apps & permissions / Permission management 等设置页匹配词与“ALLOW ONLY WHILE IN USE”弹窗匹配词实现分步教学与代点；未发现 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：有。uv0 加载 script_keyword_anti_accessibility（目标包 com.android.settings）及 20 余家厂商的 anti_reset / anti_play_protection / anti_xiaomi_safety / anti_vivo_reset / anti_oppo_uninstall 等关键字，配合无障碍全局动作与设置页监听，阻止用户关闭无障碍或卸载/查杀。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测两类瞬间：(1) 任意组件启动 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS / AppOpsDetailsActivity（Settings$AppOpsDetailsActivity）；(2) 冷启动 LoginActivity 后 10 秒内出现 1x1 透明 Activity（RequestPermissionActivity）——该 Activity 出现即意味着即将跳系统设置页，是最早的确定性锚点。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区：无障碍开启页跳转指令与引导文案由远端面板/脚本下发（包内无 ACTION_ACCESSIBILITY_SETTINGS 字面量、assets 无引导 HTML），断网或面板下线时 UTG 可能看不到完整引导链；此外权限申请承载在 1 像素透明 Activity 上，仅凭截图无法察觉，必须依赖 Activity 生命周期/Intent 级监测。未发现静态加壳，但远端 HTML 内容需联网才能捕获。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前远端面板引导页（激活/权限教学）** | com.djp.user.ui.activity.WebViewActivity，URL 为远端 http(s) 明文流量，页面含权限/无障碍开启指引 | 引导原文在此下发，是判定“诱导”而非“正常说明”的核心文本证据 | WebView 标题与正文文本；页面是否含“无障碍/辅助功能/accessibility”字样；是否有跳过/取消按钮；URL 域名与是否明文 http |
| **1 像素隐藏取权 Activity 拉起瞬间** | RequestPermissionActivity（theme=OnePixelActivity，1x1 窗口位于左上角） | 证明权限申请在用户不可见的界面中进行，且是后续跳设置页的触发器 | 屏幕上无可视 UI 但 Activity 切换；3 秒间隔重复出现的 Activity 栈抖动；紧接出现系统设置页 |
| **系统设置页上叠放的引导遮罩/代点行为** | com.android.settings 页面上存在本应用悬浮窗层，或出现非用户触发的点击/返回 | 区分“用户自己点”与“应用代点/遮罩指引”，是诱导与自动化的关键分界 | 系统设置页顶部的应用悬浮窗节点；无触摸事件的控件点击；设置页被强制返回/回到桌面 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务 中的 “M-Pajak” 条目 | 验证服务名伪装与描述为空，是身份欺骗的直接证据 | 服务名文本 M-Pajak；描述/说明为空；开关开启后被应用代点确认 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.djp.user.ui.activity.RequestPermissionActivity#a`
- `com.djp.user.ui.activity.RequestPermissionActivity#onCreate`
- `com.djp.user.ui.service.MyAccessibilityService#onServiceConnected`
- `uv0#<clinit>`
- `xk0#h`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 定向核验结论（UTG 视角）

**核心事实（已核实）**

- 桌面入口为 [LoginActivity](<resource-unit:#1.dex1 code:com.djp.user.ui.activity.LoginActivity>)，`android:label=@string/app_name`，无障碍服务标签为 `@string/app_accessibility_name`（均为“M-Pajak”，即印尼税务局 DJP 官方报税 App 名义），包名 `org.djp.user` 刻意仿冒 DJP 命名空间。
- 无障碍服务 [MyAccessibilityService](<resource-unit:#1.dex1 code:com.djp.user.ui.service.MyAccessibilityService>) 自身方法体几乎为空（`onCreate/onServiceConnected` 仅 4~7 条指令），真实能力全部落在 `com.djp.accessibility.*` 自动化框架（`automator` 选择器 + `BFS/DFS` 节点搜索 + `AccessibilityDelegate`），属典型“UI 自动化驱动式”无障碍木马内核。其 `foregroundServiceType="mediaProjection"` 与无障碍服务混用，属异常声明。
- **引导/取权编排在 1 像素隐藏 Activity 上**：[RequestPermissionActivity](<resource-unit:#1.dex1 code:com.djp.user.ui.activity.RequestPermissionActivity>) 在 `onCreate` 把窗口设成 `1x1`、`gravity=51`（左上角不可见），随后 `a()` 按 `permissionType` 分流：`1`→批量运行时权限（`lf1.g().e()`），`2`→`PermissionUtils.requestDrawOverlays`（`MANAGE_OVERLAY_PERMISSION`），并 `schedule(…, 3000, 3000)` 建立 **每 3 秒重试的定时器**，`onNewIntent` 也会重新进入 `a()` —— 这是“拒绝后循环拉起”的机制证据。
- **系统设置页跳转点**：`xk0#h` 以 `setClassName("com.android.settings", "com.android.settings.Settings$AppOpsDetailsActivity")` 直达应用特殊权限（AppOps）详情页；`cf1#a`/`PermissionUtils.startOverlayPermissionActivity` 跳悬浮窗授权；`wg0#a` 跳通知使用权。DEX 中**未出现 `ACTION_ACCESSIBILITY_SETTINGS` 字面量**，跳无障碍页大概率由脚本/远端指令字符串拼装（`f4#a` 中出现 `Intent(Settings.ACTION_A…)` 形式字符串），需运行期确认。
- **反撤权云控脚本关键字表**：[uv0](<resource-unit:#1.dex1 code:uv0#<clinit>>) 静态块从资源加载 `script_keyword_anti_accessibility`（目标包 `com.android.settings`），并同时加载 `anti_reset / anti_play_protection / anti_huawei_guardian / anti_xiaomi_safety / anti_vivo_reset` 等 20+ 家厂商设置页拦截关键字，以及 `script_keyword_dialog_ok1..12`（含“是否允许”“录制/投射您的屏幕”“电池优化”“是否停止优化电池使用量”）用于自动点掉系统授权弹窗。
- **英文设置页关键字**（“Apps & services / Apps & permissions / Permission management / ALLOW ONLY WHILE IN USE / More battery settings / Battery & performance / Play Protect”）说明引导文案并非普通说明，而是**用于在系统设置界面定位按钮/开关的匹配词**，配合 `AppOpsDetailsActivity` 跳转构成 Android 13+ 受限设置的“分步教学/代点”路径。
- 载荷与面板载体：[WebViewActivity](<resource-unit:#1.dex1 code:com.djp.user.ui.activity.WebViewActivity>)（`exported=true`，应用 `usesCleartextTraffic=true`）+ `ActivateActivity/PasswordActivity/Password2Activity/LockActivity`，说明“激活—引导—锁屏”主流程，引导页文本主要在**远端/脚本下发**，包内 `assets/` 无 a11y 相关 HTML（grep 无命中）。

**证据边界**：无障碍开启页的具体跳转指令与引导弹窗原文未在静态 DEX 中命中（`ACTION_ACCESSIBILITY_SETTINGS` 缺失、`assets` 无 HTML），推断由远端面板/脚本关键字驱动，故标注 `partial_dynamic_or_remote`；本次未执行动态 UTG 抓取。受 14 次调用上限约束，未及写入风险台账与生成报告。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest、1像素取权Activity、无障碍服务与脚本关键字表（uv0）、系统设置跳转点均静态可见；但 ACTION_ACCESSIBILITY_SETTINGS 字面量在 DEX 中不存在，assets 下无引导 HTML，无障碍引导页/说明文本应由远端 WebView 面板或脚本关键字下发，需运行期 UTG 与流量补充；未发现整体加壳（libmmkv.so 为 MMKV 常规库）。",
  "summary_one_liner": "伪装印尼税务局官方报税App（M-Pajak），以1像素隐藏Activity+3秒定时器循环催权，并由无障碍自动化框架读取云控脚本关键字自动跳转/代点系统设置页，最终以无障碍服务接管界面并拦截撤权。",
  "disguise_identity": {
    "app_display_name": "M-Pajak",
    "claimed_brand_or_persona": "印尼税务局 DJP 官方报税应用 M-Pajak（包名 org.djp.user 仿冒 DJP 命名空间）",
    "a11y_service_label": "M-Pajak",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:description 为空（无任何用途说明）；无障碍服务与 foregroundServiceType=\"mediaProjection\" 混用；权限申请在 1x1 像素、置于左上角、主题 OnePixelActivity 的不可见 Activity 中完成，用户看不到任何权限说明界面；服务标签与桌面名同为 M-Pajak，使系统无障碍列表中无法区分其真实用途。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.djp.user.ui.activity.LoginActivity（LAUNCHER）",
      "trigger_event": "用户点击桌面图标启动",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "M-Pajak",
      "shown_text_zh": "桌面图标与标题显示“M-Pajak”（印尼官方报税应用名义）",
      "user_action_requested": "正常打开应用（无任何权限/无障碍说明）",
      "code_anchor": "AndroidManifest.xml LoginActivity intent-filter MAIN/LAUNCHER；@string/app_name"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.djp.user.ui.activity.WebViewActivity（exported=true，usesCleartextTraffic=true）/ ActivateActivity / PasswordActivity",
      "trigger_event": "登录/激活流程推进后按远端配置加载面板",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "无（包内 assets 无相关 HTML，文本由远端/脚本下发）",
      "shown_text_zh": "远端面板下发激活与权限引导步骤（内容不可静态还原）",
      "user_action_requested": "按远端页面指引继续下一步",
      "code_anchor": "com.djp.user.ui.activity.WebViewActivity；AndroidManifest usesCleartextTraffic=true"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "com.djp.user.ui.activity.RequestPermissionActivity（1x1 不可见）→ 系统悬浮窗/AppOps 详情页",
      "trigger_event": "onCreate / onNewIntent 调用 a()，读取 intent 的 permissionType 与 permissionList",
      "ui_carrier": "系统设置页",
      "shown_text_verbatim": "Intent(\"android.settings.action.MANAGE_OVERLAY_PERMISSION\")；com.android.settings.Settings$AppOpsDetailsActivity",
      "shown_text_zh": "跳转“显示在其他应用上层”授权页，或直接跳到应用的特殊权限（AppOps）详情页",
      "user_action_requested": "在系统页手动打开悬浮窗/特殊权限开关",
      "code_anchor": "RequestPermissionActivity.a / RequestPermissionActivity.onCreate；cf1#a；xk0#h"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "RequestPermissionActivity 内 java.util.Timer + RequestPermissionActivity$c",
      "trigger_event": "Timer.schedule(…, 3000L, 3000L) 每 3 秒重试；onNewIntent 亦重新执行 a()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "用户返回或拒绝后，应用每 3 秒再次拉起权限/设置页，无取消入口",
      "user_action_requested": "只能持续授权直至通过",
      "code_anchor": "com.djp.user.ui.activity.RequestPermissionActivity#a；RequestPermissionActivity$c"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已安装的服务 → M-Pajak",
      "trigger_event": "由远端脚本/关键字指令驱动（包内仅见 f4#a 中 Intent(Settings.ACTION_A…) 字符串拼装形式）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Intent(Settings.ACTION_A…（被截断的脚本字符串）",
      "shown_text_zh": "脚本指令拼装无障碍设置页 Intent 并跳转",
      "user_action_requested": "在无障碍列表中手动开启 M-Pajak 服务",
      "code_anchor": "f4#a；uv0#<clinit>（script_keyword_anti_accessibility）"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引 / 分步教学",
      "screen_or_component": "系统设置页之上的悬浮窗（EasyFloat / SYSTEM_ALERT_WINDOW）与无障碍自动化点击",
      "trigger_event": "无障碍服务已连接后，按 uv0 关键字表匹配当前设置页节点并执行点击",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Apps & services / Apps & permissions / Permission management / ALLOW ONLY WHILE IN USE / More battery settings / Battery & performance / Play Protect",
      "shown_text_zh": "用于在设置界面定位“应用与服务/权限管理/仅在使用中允许/电池与性能/Play 保护”等按钮的匹配词",
      "user_action_requested": "被自动代点或引导用户点选对应开关",
      "code_anchor": "uv0#<clinit>；com.djp.accessibility.automator.UiGlobalSelector；com.lzf.easyfloat.EasyFloatInitializer"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.djp.accessibility.view.accessibility.AccessibilityService（MyAccessibilityService 父类）",
      "trigger_event": "onServiceConnected 后注册事件分发与节点搜索",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "是否允许 / 录制/投射您的屏幕 / 要开始使用 / 录制或投射内容 / 电池优化 / 是否停止优化电池使用量",
      "shown_text_zh": "自动点击系统录屏授权、电池优化等系统弹窗的确认按钮",
      "user_action_requested": "无需用户操作（由服务代点确认）",
      "code_anchor": "uv0#<clinit>（script_keyword_dialog_ok1..12）；MyAccessibilityService#onServiceConnected"
    },
    {
      "step": 8,
      "stage": "拒权反馈循环（反撤权）",
      "screen_or_component": "系统设置 → 无障碍页 / 应用详情页",
      "trigger_event": "无障碍服务监听窗口事件，命中 anti_accessibility / anti_* 关键字后执行返回、主页或代点",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "script_keyword_anti_accessibility（目标包 com.android.settings）；script_keyword_anti_reset、anti_play_protection、anti_xiaomi_safety、anti_vivo_reset 等 20+ 项",
      "shown_text_zh": "拦截“关闭无障碍/重置/Play 保护/安全中心/恢复出厂”等设置页，阻止用户撤权或查杀",
      "user_action_requested": "用户无法完成撤权操作",
      "code_anchor": "uv0#<clinit>；PERFORM_GLOBAL_ACTION / WATCH_SETTINGS 线索"
    }
  ],
  "text_presentation_locations": [
    "远端 WebView 面板（com.djp.user.ui.activity.WebViewActivity，exported=true、明文流量开启）：激活与权限引导主文案，包内不可见",
    "1x1 像素不可见 Activity（RequestPermissionActivity，theme=OnePixelActivity，gravity=51）：无任何可见文案，仅执行权限/设置页跳转",
    "系统悬浮窗层（EasyFloat provider org.djp.user.EasyFloatInitializer + SYSTEM_ALERT_WINDOW）：设置页之上的引导/遮罩",
    "系统无障碍列表：服务名仅显示 @string/app_accessibility_name = “M-Pajak”，android:description 为空",
    "自动化匹配词（非面向用户展示）：strings 资源中 Apps & services / Permission management / ALLOW ONLY WHILE IN USE 等，被 uv0 用于定位系统设置控件",
    "系统弹窗代点词表：是否允许 / 录制/投射您的屏幕 / 电池优化 / 是否停止优化电池使用量 等 12 条（script_keyword_dialog_ok1..12）"
  ],
  "verbatim_texts": [
    {
      "lang": "zh",
      "text_verbatim": "是否允许",
      "text_zh": "是否允许",
      "source_location": "res/values*/strings.xml script_keyword_dialog_ok1（硬编码兜底数组 uv0 中亦出现）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "zh",
      "text_verbatim": "录制/投射您的屏幕",
      "text_zh": "录制/投射您的屏幕",
      "source_location": "uv0.<clinit> 静态数组 c",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "电池优化；是否停止优化电池使用量",
      "text_zh": "电池优化；是否停止优化电池使用量",
      "source_location": "uv0.<clinit> 静态数组 c",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Apps & services",
      "text_zh": "应用与服务",
      "source_location": "strings 资源（设置页控件匹配词）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Apps & permissions",
      "text_zh": "应用与权限",
      "source_location": "strings 资源（设置页控件匹配词）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Permission management",
      "text_zh": "权限管理",
      "source_location": "strings 资源（设置页控件匹配词）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "ALLOW ONLY WHILE IN USE",
      "text_zh": "仅在使用应用时允许",
      "source_location": "strings 资源（系统权限弹窗匹配词）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "More battery settings",
      "text_zh": "更多电池设置",
      "source_location": "strings 资源（设置页控件匹配词）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Play Protect",
      "text_zh": "Play 保护机制",
      "source_location": "strings 资源（安全设置页匹配词，配合 script_keyword_anti_play_protection）",
      "rhetorical_frame": "教唆忽视警告"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "RequestPermissionActivity.a() 启动 java.util.Timer，schedule(…, 3000L, 3000L) 每 3 秒重复执行权限/设置页拉起；onNewIntent 被再次唤起时也重新执行 a()；无障碍服务本身监听系统设置页事件，命中 anti_accessibility/anti_reset 等关键字后拦截返回操作，使用户无法停留在撤权页面。",
    "overlay_or_fake_settings": "具备悬浮窗能力（SYSTEM_ALERT_WINDOW + SYSTEM_OVERLAY_WINDOW + EasyFloat provider），用于在系统设置页之上叠放引导/遮罩；未发现高仿系统无障碍开关页的独立 Activity（该类页面大概率由远端面板下发）。",
    "restricted_settings_13plus_coaching": "有。xk0#h 直接 setClassName 跳转 com.android.settings.Settings$AppOpsDetailsActivity（应用特殊权限/受限设置详情），并配合 Apps & services / Apps & permissions / Permission management 等设置页匹配词与“ALLOW ONLY WHILE IN USE”弹窗匹配词实现分步教学与代点；未发现 Session 安装器绕过。",
    "post_grant_anti_removal": "有。uv0 加载 script_keyword_anti_accessibility（目标包 com.android.settings）及 20 余家厂商的 anti_reset / anti_play_protection / anti_xiaomi_safety / anti_vivo_reset / anti_oppo_uninstall 等关键字，配合无障碍全局动作与设置页监听，阻止用户关闭无障碍或卸载/查杀。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测两类瞬间：(1) 任意组件启动 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS / AppOpsDetailsActivity（Settings$AppOpsDetailsActivity）；(2) 冷启动 LoginActivity 后 10 秒内出现 1x1 透明 Activity（RequestPermissionActivity）——该 Activity 出现即意味着即将跳系统设置页，是最早的确定性锚点。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前远端面板引导页（激活/权限教学）",
        "page_identifier": "com.djp.user.ui.activity.WebViewActivity，URL 为远端 http(s) 明文流量，页面含权限/无障碍开启指引",
        "why_most_useful": "引导原文在此下发，是判定“诱导”而非“正常说明”的核心文本证据",
        "observable_utg_signals": ["WebView 标题与正文文本", "页面是否含“无障碍/辅助功能/accessibility”字样", "是否有跳过/取消按钮", "URL 域名与是否明文 http"]
      },
      {
        "page_role": "1 像素隐藏取权 Activity 拉起瞬间",
        "page_identifier": "RequestPermissionActivity（theme=OnePixelActivity，1x1 窗口位于左上角）",
        "why_most_useful": "证明权限申请在用户不可见的界面中进行，且是后续跳设置页的触发器",
        "observable_utg_signals": ["屏幕上无可视 UI 但 Activity 切换", "3 秒间隔重复出现的 Activity 栈抖动", "紧接出现系统设置页"]
      },
      {
        "page_role": "系统设置页上叠放的引导遮罩/代点行为",
        "page_identifier": "com.android.settings 页面上存在本应用悬浮窗层，或出现非用户触发的点击/返回",
        "why_most_useful": "区分“用户自己点”与“应用代点/遮罩指引”，是诱导与自动化的关键分界",
        "observable_utg_signals": ["系统设置页顶部的应用悬浮窗节点", "无触摸事件的控件点击", "设置页被强制返回/回到桌面"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务 中的 “M-Pajak” 条目",
        "why_most_useful": "验证服务名伪装与描述为空，是身份欺骗的直接证据",
        "observable_utg_signals": ["服务名文本 M-Pajak", "描述/说明为空", "开关开启后被应用代点确认"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区：无障碍开启页跳转指令与引导文案由远端面板/脚本下发（包内无 ACTION_ACCESSIBILITY_SETTINGS 字面量、assets 无引导 HTML），断网或面板下线时 UTG 可能看不到完整引导链；此外权限申请承载在 1 像素透明 Activity 上，仅凭截图无法察觉，必须依赖 Activity 生命周期/Intent 级监测。未发现静态加壳，但远端 HTML 内容需联网才能捕获。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.djp.user.ui.activity.RequestPermissionActivity#a",
    "com.djp.user.ui.activity.RequestPermissionActivity#onCreate",
    "com.djp.user.ui.service.MyAccessibilityService#onServiceConnected",
    "uv0#<clinit>",
    "xk0#h",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>

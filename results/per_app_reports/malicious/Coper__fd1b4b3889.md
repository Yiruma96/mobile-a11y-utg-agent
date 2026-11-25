# MB_049__fd1b4b3889｜Coper — Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：115.7s

## 1. 一句话核心结论

- **核心申请方式**：冒充 Chrome 的短信木马以透明无界面 Activity 冷启动即 setClassName 直跳系统无障碍设置，辅以全屏 WebView JS 桥按钮触发跳转，无障碍描述用土耳其语伪装，获权后由加密指令驱动读屏、模拟点击与 GLOBAL_ACTION 导航。
- **静态可见性说明**：DEX 未加壳、Manifest 与无障碍配置完整可见；但全部引导文案与指令字符串由 NPStringFog.decode(byte[],key) 加密存储，WebView 教学页正文来自本地模板替换或远端 loadUrl（p041j.goto 支持远端 URL 分支），故页面逐字文本与远端开关逻辑无法静态还原，仅可确证载体、跳转目标与执行链路。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `fd1b4b38899ce7f0c377df7e37a4d15c8e6d6f17c35873804bf93390bbc2c131` |
| 包名 / 年份 | `com.nameown12` / 2025 |
| 家族 / 品类 | **Coper**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Chrome |
| 引导页宣称品牌/身份 | Google Chrome 浏览器 |
| 系统无障碍列表服务名 | Chrome |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：桌面图标名与无障碍服务标签共用 @string/a="Chrome" 冒充官方浏览器；无障碍描述改为土耳其语且错拼（Servisileri），面向土耳其语用户弱化警惕；启动器 Activity 设 excludeFromRecents 不留在最近任务；大量单字母混淆类名与随机命名 Activity/Service（tdwjlrqtqhhauqf、zreuctkootj 等）；字符串统一 NPStringFog 异或加密；p045l 内含配置串条件判定，命中即 finish() 隐藏自身。 |
| 无障碍服务类名 | `com.nameown12.p024l` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Erişebilirlik Servisileri Etkinleştirme |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.nameown12.p045l（LAUNCHER Activity，excludeFromRecents，无 setContentView） | 用户点击桌面 Chrome 图标 → onCreate | 原生Activity | **原文**：无（该 Activity 不加载任何布局，仅执行判定与跳转）<br>**译注**：无可见界面，用户点击图标后直接发生跳转 | 无（无可点击控件、无取消/跳过按钮） | `com.nameown12.p045l.onCreate` |
| 2 | 跳无障碍设置 | com.nameown12.p086v（透明主题、无布局 Activity）→ 系统「无障碍」服务列表页 | p045l.onCreate 中权限判定为未授予 → startActivity(p086v) → p086v.onCreate 无 extras 分支 → fddo.goto.dgjaertjardthjdgu(context) | 系统无障碍页 | **原文**：系统页展示服务项名 "Chrome"，描述 "Erişebilirlik Servisileri Etkinleştirme"<br>**译注**：系统无障碍列表中出现名为 Chrome 的服务，说明文字为「启用无障碍服务」 | 要求用户在系统页找到 Chrome 并手动打开开关；应用自身不提供取消/跳过入口 | `com.nameown12.p086v.onCreate / fddo.goto.dgjaertjardthjdgu` |
| 3 | 引导说明页 | com.nameown12.p041j（singleTask、Theme.NoTitleBar.Fullscreen 全屏 WebView Activity） | 业务/后台链路调用 p041j.goto(url,html,type) 加载页面；页面内 JS 调用注入对象方法 open_acsb_settings() | 本地HTML WebView | **原文**：不可静态还原（模板与远端页面内容经 NPStringFog 加密/远端下发；UA 被伪造成浏览器 UA 字符串）<br>**译注**：全屏网页形式的操作教学/引导页，按钮点击后再次跳转系统无障碍设置 | 在网页内点击按钮触发 open_acsb_settings()，随后前往系统设置开启服务；无原生取消按钮 | `com.nameown12.p041j.goto / com.nameown12.p041j$ifdf.open_acsb_settings` |
| 4 | 拒权反馈循环 | com.nameown12.p060d（BOOT_COMPLETED / USER_PRESENT / PACKAGE_ADDED / SCREEN_ON 等广播接收器）与 p045l.onCreate 复检 | 开机、解锁、亮屏、安装变化等广播 → p060d.onReceive → fddo.goto.x() 重新判定无障碍是否开启 | 原生Activity | 无 | 持续要求用户重新进入设置开启服务，未提供跳过通道 | `com.nameown12.p045l.onCreate / fddo.goto.x / com.nameown12.p060d.onReceive` |
| 5 | 获权后动作 | com.nameown12.p024l（AccessibilityService） | 服务在系统页被开启 → onServiceConnected → onAccessibilityEvent 逐事件处理 | 不可静态还原 | **原文**：不可静态还原（指令字符串均为 NPStringFog.decode 加密字节数组，按 equals 分派）<br>**译注**：按远端/加密指令执行读屏取文、模拟点击手势，并通过 performGlobalAction 执行返回/主页等全局导航 | 无（用户已授权，后续交互由服务自动完成） | `com.nameown12.p024l.onAccessibilityEvent / com.nameown12.p024l.throw / fddo.const.throw` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务标签 @string/a = "Chrome"，描述 @string/WIPEAYSSVi = "Erişebilirlik Servisileri Etkinleştirme"（res/xml/lfdqvgts.xml 引用）
- 全屏 WebView Activity com.nameown12.p041j 渲染的网页内容（本地模板经 p041j.else 变量替换，或远端 URL 经 loadUrl 加载），文字不可静态还原
- 无原生说明/引导 AlertDialog：p086v 为透明无布局 Activity，p045l 不加载布局，均不呈现任何说明文字
- 跳转前后仅通过加密字符串 Toast（fddo.throw.this / throw.case）做短提示，内容不可静态还原
- 设备管理器激活页（p045n → ACTION_ADD_DEVICE_ADMIN）与录屏授权页（p090h → MediaProjection）为系统原生确认界面，非应用自绘

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Erişebilirlik Servisileri Etkinleştirme | 启用无障碍服务 | `res/values/strings.xml key WIPEAYSSVi（被 res/xml/lfdqvgts.xml 的 android:description 引用）` | 受限设置分步教学 |
| en | Chrome | Chrome（谷歌浏览器） | `res/values/strings.xml key a（application android:label 与无障碍 service android:label 共用）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：用户返回或未开启时，应用不留界面（p045l 判定后 finish，p086v 无布局直接跳转）；随后由 p060d 广播接收器在 BOOT_COMPLETED/USER_PRESENT/SCREEN_ON/PACKAGE_ADDED 等事件触发 fddo.goto.x() 复检无障碍状态并再次拉起跳转，形成后台反复重跳而非良性停留。
- **遮罩叠层 / 高仿系统设置页**：未见悬浮窗遮罩（预筛 overlay 为空）；但 p041j 以全屏无标题 WebView Activity（singleTask）覆盖呈现教学页，onResume 中 setVisibility(0) 使 WebView 重新可见，视觉上等效全屏自绘引导层。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无障碍服务具备 performGlobalAction 能力（fddo.const.throw / fddo.fddo.fddo / fddo.fddo.public 调用点），可执行 BACK/HOME 等全局导航，具备在系统设置页自主回退/阻止撤权的技术条件；具体触发条件在加密指令分派中，本次未逐条还原。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到目标进程以 FLAG_ACTIVITY_NEW_TASK 启动 setClassName 指向系统设置组件（Settings$AccessibilitySettings 类）时立即抓取；以及 Launcher Activity com.nameown12.p045l 冷启动后 1s 内的首个 Activity 栈变化。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导正文由 NPStringFog 加密字符串与远端 HTML 提供，静态无法预知逐字文案，须依赖运行期 UTG 采集；未见纯图/空文本引导。静态未加壳不阻碍运行期 UTG 观测。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动直跳后的系统无障碍服务列表项** | Settings 包 Activity + 列表项文本 "Chrome"、描述 "Erişebilirlik Servisileri Etkinleştirme" | 直接证明零步骤直跳与身份冒充，且描述语种/错拼是关键恶意指纹 | 列表项服务名 Chrome；描述文本 Erişebilirlik Servisileri Etkinleştirme；当前前台为 com.android.settings 无障碍页而应用无任何自绘说明页 |
| **WebView 教学页（p041j）** | com.nameown12.p041j 全屏无标题 Activity，含 WebView 节点与可点击按钮 | 唯一承载引导文案的载体，可采集运行期解密后的真实话术，弥补静态加密盲区 | WebView 节点文本（土耳其语/英语引导语）；按钮控件及其触发后 Activity 切换至系统设置；页面 URL 是否为远端域名 |
| **权限串联确认页** | 设备管理器激活页（Device admin 添加界面）与 MediaProjection 录屏授权对话框 | 证明同一流程中叠加设备管理器与录屏两项高权限，强化恶意定性 | 设备管理激活界面来源为 com.nameown12；录屏授权对话框出现在无障碍授权之后 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.nameown12.p045l.onCreate`
- `com.nameown12.p086v.onCreate`
- `fddo.goto.dgjaertjardthjdgu`
- `com.nameown12.p041j.goto`
- `com.nameown12.p041j$ifdf.open_acsb_settings`
- `res/xml/lfdqvgts.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（受调用预算约束，在核验到 WebView JS 桥与无障碍服务指令解析后收敛）。

## 关键结论

- **身份伪装**：桌面名与无障碍服务标签同为 `Chrome`（`@string/a`），无障碍描述用土耳其语“Erişebilirlik Servisileri Etkinleştirme”（启用无障碍服务，且 “Servisileri” 为错拼），与真实 Chrome 无关；实际行为是短信读取、设备管理、录屏与无障碍远控。
- **引导方式为“静默直跳 + WebView 教学”双通道，没有原生说明弹窗**：
  1. 启动器 [com.nameown12.p045l](<resource-unit:#1.dex1 code:com.nameown12.p045l#onCreate>) 无 `setContentView`，仅做条件判定（含 `finish()` 变脸分支与反射注册全系统广播接收器），判定无障碍未开启即拉起 `p086v`；
  2. [com.nameown12.p086v#onCreate](<resource-unit:#1.dex1 code:com.nameown12.p086v#onCreate>) 无任何 UI，直接调用 [fddo.goto#dgjaertjardthjdgu](<resource-unit:#1.dex1 code:fddo.goto#dgjaertjardthjdgu>) 以 `Intent.setClassName` 硬编码跳转系统设置组件（resolve 失败则回退到硬编码 ACTION 字符串 Intent），`FLAG_ACTIVITY_NEW_TASK` 直达无障碍设置页；
  3. 另一路径为全屏单任务 WebView [com.nameown12.p041j](<resource-unit:#1.dex1 code:com.nameown12.p041j#goto>)，注册 `addJavascriptInterface` 并暴露 `@JavascriptInterface open_acsb_settings()`（[com.nameown12.p041j$ifdf#open_acsb_settings](<resource-unit:#1.dex1 code:com.nameown12.p041j$ifdf#open_acsb_settings>)），由页面按钮触发跳转；页面内容经模板替换（本地 HTML）或 `loadUrl` 远端地址加载，UA 被伪造成浏览器。
- **获权后能力**：无障碍服务 [com.nameown12.p024l](<resource-unit:#1.dex1 code:com.nameown12.p024l#onServiceConnected>) 配置 `canRetrieveWindowContent`、`canPerformGestures`、`flagRetrieveInteractiveWindows`、`typeAllMask`；`onAccessibilityEvent → throw(String)` 按加密指令字符串分派远端命令，并调用 `performGlobalAction`（BACK/HOME 等），具备读取任意界面文本与自主导航/阻止撤权的技术条件。
- **同流程还串联受限权限**：`p045n` 走 `ACTION_ADD_DEVICE_ADMIN` 激活设备管理器（结果码 100），`p090h` 走 `MediaProjection` 录屏授权（112233）。
- **静态可见性**：未加壳，但引导文案与指令均为 `NPStringFog.decode` 加密字节串 + 远端 HTML，静态不可读原文，只能确认载体与跳转链路。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "DEX 未加壳、Manifest 与无障碍配置完整可见；但全部引导文案与指令字符串由 NPStringFog.decode(byte[],key) 加密存储，WebView 教学页正文来自本地模板替换或远端 loadUrl（p041j.goto 支持远端 URL 分支），故页面逐字文本与远端开关逻辑无法静态还原，仅可确证载体、跳转目标与执行链路。",
  "summary_one_liner": "冒充 Chrome 的短信木马以透明无界面 Activity 冷启动即 setClassName 直跳系统无障碍设置，辅以全屏 WebView JS 桥按钮触发跳转，无障碍描述用土耳其语伪装，获权后由加密指令驱动读屏、模拟点击与 GLOBAL_ACTION 导航。",
  "disguise_identity": {
    "app_display_name": "Chrome",
    "claimed_brand_or_persona": "Google Chrome 浏览器",
    "a11y_service_label": "Chrome",
    "identity_mismatch": true,
    "obfuscation_tricks": "桌面图标名与无障碍服务标签共用 @string/a=\"Chrome\" 冒充官方浏览器；无障碍描述改为土耳其语且错拼（Servisileri），面向土耳其语用户弱化警惕；启动器 Activity 设 excludeFromRecents 不留在最近任务；大量单字母混淆类名与随机命名 Activity/Service（tdwjlrqtqhhauqf、zreuctkootj 等）；字符串统一 NPStringFog 异或加密；p045l 内含配置串条件判定，命中即 finish() 隐藏自身。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.nameown12.p045l（LAUNCHER Activity，excludeFromRecents，无 setContentView）",
      "trigger_event": "用户点击桌面 Chrome 图标 → onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（该 Activity 不加载任何布局，仅执行判定与跳转）",
      "shown_text_zh": "无可见界面，用户点击图标后直接发生跳转",
      "user_action_requested": "无（无可点击控件、无取消/跳过按钮）",
      "code_anchor": "com.nameown12.p045l.onCreate"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "com.nameown12.p086v（透明主题、无布局 Activity）→ 系统「无障碍」服务列表页",
      "trigger_event": "p045l.onCreate 中权限判定为未授予 → startActivity(p086v) → p086v.onCreate 无 extras 分支 → fddo.goto.dgjaertjardthjdgu(context)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "系统页展示服务项名 \"Chrome\"，描述 \"Erişebilirlik Servisileri Etkinleştirme\"",
      "shown_text_zh": "系统无障碍列表中出现名为 Chrome 的服务，说明文字为「启用无障碍服务」",
      "user_action_requested": "要求用户在系统页找到 Chrome 并手动打开开关；应用自身不提供取消/跳过入口",
      "code_anchor": "com.nameown12.p086v.onCreate / fddo.goto.dgjaertjardthjdgu"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.nameown12.p041j（singleTask、Theme.NoTitleBar.Fullscreen 全屏 WebView Activity）",
      "trigger_event": "业务/后台链路调用 p041j.goto(url,html,type) 加载页面；页面内 JS 调用注入对象方法 open_acsb_settings()",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "不可静态还原（模板与远端页面内容经 NPStringFog 加密/远端下发；UA 被伪造成浏览器 UA 字符串）",
      "shown_text_zh": "全屏网页形式的操作教学/引导页，按钮点击后再次跳转系统无障碍设置",
      "user_action_requested": "在网页内点击按钮触发 open_acsb_settings()，随后前往系统设置开启服务；无原生取消按钮",
      "code_anchor": "com.nameown12.p041j.goto / com.nameown12.p041j$ifdf.open_acsb_settings"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.nameown12.p060d（BOOT_COMPLETED / USER_PRESENT / PACKAGE_ADDED / SCREEN_ON 等广播接收器）与 p045l.onCreate 复检",
      "trigger_event": "开机、解锁、亮屏、安装变化等广播 → p060d.onReceive → fddo.goto.x() 重新判定无障碍是否开启",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "用户返回或拒绝后，应用在下次亮屏/解锁/开机时再次判定并重新拉起设置跳转，形成反复施压",
      "user_action_requested": "持续要求用户重新进入设置开启服务，未提供跳过通道",
      "code_anchor": "com.nameown12.p045l.onCreate / fddo.goto.x / com.nameown12.p060d.onReceive"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.nameown12.p024l（AccessibilityService）",
      "trigger_event": "服务在系统页被开启 → onServiceConnected → onAccessibilityEvent 逐事件处理",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "不可静态还原（指令字符串均为 NPStringFog.decode 加密字节数组，按 equals 分派）",
      "shown_text_zh": "按远端/加密指令执行读屏取文、模拟点击手势，并通过 performGlobalAction 执行返回/主页等全局导航",
      "user_action_requested": "无（用户已授权，后续交互由服务自动完成）",
      "code_anchor": "com.nameown12.p024l.onAccessibilityEvent / com.nameown12.p024l.throw / fddo.const.throw"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务标签 @string/a = \"Chrome\"，描述 @string/WIPEAYSSVi = \"Erişebilirlik Servisileri Etkinleştirme\"（res/xml/lfdqvgts.xml 引用）",
    "全屏 WebView Activity com.nameown12.p041j 渲染的网页内容（本地模板经 p041j.else 变量替换，或远端 URL 经 loadUrl 加载），文字不可静态还原",
    "无原生说明/引导 AlertDialog：p086v 为透明无布局 Activity，p045l 不加载布局，均不呈现任何说明文字",
    "跳转前后仅通过加密字符串 Toast（fddo.throw.this / throw.case）做短提示，内容不可静态还原",
    "设备管理器激活页（p045n → ACTION_ADD_DEVICE_ADMIN）与录屏授权页（p090h → MediaProjection）为系统原生确认界面，非应用自绘"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Erişebilirlik Servisileri Etkinleştirme",
      "text_zh": "启用无障碍服务",
      "source_location": "res/values/strings.xml key WIPEAYSSVi（被 res/xml/lfdqvgts.xml 的 android:description 引用）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Chrome",
      "text_zh": "Chrome（谷歌浏览器）",
      "source_location": "res/values/strings.xml key a（application android:label 与无障碍 service android:label 共用）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "用户返回或未开启时，应用不留界面（p045l 判定后 finish，p086v 无布局直接跳转）；随后由 p060d 广播接收器在 BOOT_COMPLETED/USER_PRESENT/SCREEN_ON/PACKAGE_ADDED 等事件触发 fddo.goto.x() 复检无障碍状态并再次拉起跳转，形成后台反复重跳而非良性停留。",
    "overlay_or_fake_settings": "未见悬浮窗遮罩（预筛 overlay 为空）；但 p041j 以全屏无标题 WebView Activity（singleTask）覆盖呈现教学页，onResume 中 setVisibility(0) 使 WebView 重新可见，视觉上等效全屏自绘引导层。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无障碍服务具备 performGlobalAction 能力（fddo.const.throw / fddo.fddo.fddo / fddo.fddo.public 调用点），可执行 BACK/HOME 等全局导航，具备在系统设置页自主回退/阻止撤权的技术条件；具体触发条件在加密指令分派中，本次未逐条还原。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到目标进程以 FLAG_ACTIVITY_NEW_TASK 启动 setClassName 指向系统设置组件（Settings$AccessibilitySettings 类）时立即抓取；以及 Launcher Activity com.nameown12.p045l 冷启动后 1s 内的首个 Activity 栈变化。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动直跳后的系统无障碍服务列表项",
        "page_identifier": "Settings 包 Activity + 列表项文本 \"Chrome\"、描述 \"Erişebilirlik Servisileri Etkinleştirme\"",
        "why_most_useful": "直接证明零步骤直跳与身份冒充，且描述语种/错拼是关键恶意指纹",
        "observable_utg_signals": ["列表项服务名 Chrome", "描述文本 Erişebilirlik Servisileri Etkinleştirme", "当前前台为 com.android.settings 无障碍页而应用无任何自绘说明页"]
      },
      {
        "page_role": "WebView 教学页（p041j）",
        "page_identifier": "com.nameown12.p041j 全屏无标题 Activity，含 WebView 节点与可点击按钮",
        "why_most_useful": "唯一承载引导文案的载体，可采集运行期解密后的真实话术，弥补静态加密盲区",
        "observable_utg_signals": ["WebView 节点文本（土耳其语/英语引导语）", "按钮控件及其触发后 Activity 切换至系统设置", "页面 URL 是否为远端域名"]
      },
      {
        "page_role": "权限串联确认页",
        "page_identifier": "设备管理器激活页（Device admin 添加界面）与 MediaProjection 录屏授权对话框",
        "why_most_useful": "证明同一流程中叠加设备管理器与录屏两项高权限，强化恶意定性",
        "observable_utg_signals": ["设备管理激活界面来源为 com.nameown12", "录屏授权对话框出现在无障碍授权之后"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导正文由 NPStringFog 加密字符串与远端 HTML 提供，静态无法预知逐字文案，须依赖运行期 UTG 采集；未见纯图/空文本引导。静态未加壳不阻碍运行期 UTG 观测。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.nameown12.p045l.onCreate",
    "com.nameown12.p086v.onCreate",
    "fddo.goto.dgjaertjardthjdgu",
    "com.nameown12.p041j.goto",
    "com.nameown12.p041j$ifdf.open_acsb_settings",
    "res/xml/lfdqvgts.xml"
  ]
}
```

</details>

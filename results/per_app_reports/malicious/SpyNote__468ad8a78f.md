# MR_157__468ad8a78f｜SpyNote — OfficeSuite

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：88.1s

## 1. 一句话核心结论

- **核心申请方式**：该样本用半透明无界面 Launcher Activity 在冷启动与每次 onResume 时静默直跳系统无障碍设置页，无任何说明文字与取消入口，未开启即无限重跳，开启后自禁用桌面图标并继续投放二阶段载荷
- **静态可见性说明**：跳转逻辑、开关位、服务配置全部位于明文 classes.dex（未加壳、无加密载荷），可完整静态还原；仅 C7$2 投放线程内部（下载/落地二阶段载荷）未展开，但不影响无障碍引导链判定
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `468ad8a78ff8a97d47e3bb9a9cbf5adc10ceb3d1715684b2533ac82e550cb5bf` |
| 包名 / 年份 | `com.android.tester` / 2020 |
| 家族 / 品类 | **SpyNote**（同池样本数：59） |
| 原始来源标识 | https://blog.lookout.com/nation-state-mobile-malware-targets-syrians-with-covid-19-lures |
| 桌面显示名 | OfficeSuite |
| 引导页宣称品牌/身份 | OfficeSuite（伪冒办公文档套件品牌，实际为 SpyNote 系远控） |
| 系统无障碍列表服务名 | OfficeSuite（C1 未声明 android:label，回落为应用名 @string/s） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务无 android:description、无 accessibilityservice meta-data，系统列表只剩品牌名而不显示监控能力；入口 Activity 使用 Theme.Translucent.NoTitleBar + excludeFromRecents 实现'点开无界面'；获权后 setComponentEnabledSetting(C7, DISABLED) 删除桌面图标；行为开关藏在字符串资源 gp="11000" 的字符位上，与界面完全解耦 |
| 无障碍服务类名 | `com.android.tester.C1` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.android.tester.C7（LAUNCHER Activity，Theme.Translucent.NoTitleBar，excludeFromRecents） | 用户点击桌面图标 → onCreate() | 原生Activity | 无 | 无（用户仅看到图标一闪） | `com.android.tester.C7#onCreate / AndroidManifest.xml activity C7` |
| 2 | 业务功能触发 | com.android.tester.C7#c() 读取 @string/gp = "11000" 并起线程 C7$1 | onCreate/onResume → c() → new Thread(new C7$1(this)).start() | 不可静态还原（纯后台线程，无 UI） | **原文**：11000<br>**译注**：内部控制开关串：第0位=获权后自禁用入口、第1位=跳无障碍设置、第2位=记录窗口文本、第3位=设备管理员、第4位=su提权检测 | 无 | `com.android.tester.C7#c / res/values/strings.xml key=gp` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | C7$1.run()：charAt(1)=='1' && !C11.j → Intent.setAction("android.settings.ACCESSIBILITY_SETTINGS")，FLAG_ACTIVITY_NEW_TASK(268435456) → startActivity | 系统无障碍页 | **原文**：无（应用侧未附加任何 EXTRA、未提供说明文案）<br>**译注**：直接落到系统无障碍设置列表，列表中显示服务名 OfficeSuite | 要求用户在系统无障碍列表中自行找到并开启 OfficeSuite 开关；应用未提供任何理由或说明 | `com.android.tester.C7$1#run` |
| 4 | 引导说明页 | 不存在（无 Dialog / 无 WebView / 无 HTML / 无 strings 说明文案） | 无 | 不可静态还原（该步骤在实现中缺失） | 无 | 无 | `res/values/strings.xml（仅 app_name=OfficeSuite、s=OfficeSuite、gp、h、n、p、ps、v 等控制串）` |
| 5 | 拒权反馈循环 | com.android.tester.C7#onResume → c() | 用户从系统设置返回（未开启无障碍）→ onResume 回调 | 系统无障碍页 | 无 | 被迫重复开启操作；无取消、无跳过、无返回按钮（onBackPressed 仅 super） | `com.android.tester.C7#onResume / com.android.tester.C7#onBackPressed` |
| 6 | 获权后动作 | com.android.tester.C1（AccessibilityService）onServiceConnected | 用户在系统设置中开启 OfficeSuite 开关 → 服务连接回调 | 系统无障碍页 | 无 | 无（用户已授权，应用不再显示任何确认） | `com.android.tester.C1#onServiceConnected / com.android.tester.C1#b` |
| 7 | 获权后动作 | com.android.tester.C7#a()（setComponentEnabledSetting）与 C7$1.run 的二阶段投放分支 | 下次 c()：charAt(0)=='1' → a() 禁用 C7 组件；两条件满足后按 @string/MER("..") 拉起隐藏包或启动 C7$2 下载线程 | 不可静态还原（桌面图标消失、后台投放） | **原文**：..<br>**译注**：载荷包名占位（".." 表示不存在的目标，走下载投放路径）；入口图标被系统隐藏 | 无 | `com.android.tester.C7#a / com.android.tester.C7$1#run` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项名称：OfficeSuite（来自 @string/s 与 @string/app_name，C1 无 android:label）
- 系统无障碍服务描述：缺失（C1 未声明 android:description，也无 android.accessibilityservice 配置 xml）
- 应用内引导文字：完全不存在（无 AlertDialog、无 Toast、无 Activity 布局文案、无 assets HTML/WebView）
- 跳转前说明：不存在（C7$1.run 构造的 Intent 无 EXTRA，无任何前置页面）
- 悬浮遮罩/高仿设置页：不存在（全包无 TYPE_SYSTEM_ALERT/TYPE_APPLICATION_OVERLAY 使用点）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | OfficeSuite | 办公套件 | `res/values/strings.xml key=app_name / key=s` | 假反诈安全 |
| en | 11000 | 11000（行为开关位串，非用户可见文案） | `res/values/strings.xml key=gp` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：C7.onResume 每次都调用 c()，只要 C11.j（无障碍已连接）仍为 false 就再次 startActivity(android.settings.ACCESSIBILITY_SETTINGS)；finish() 仅在设备管理员与无障碍条件同时满足时执行，故用户从设置页返回即被立即重跳，形成无法退出的循环
- **遮罩叠层 / 高仿系统设置页**：无叠层引导、无高仿设置页；仅靠 Translucent 无标题 Activity 静默跳转
- **Android 13+ 受限设置（Restricted Settings）应对**：无（全包未出现 ACTION_APPLICATION_DETAILS_SETTINGS，无受限设置分步教学；targetSdk=22，本身规避 Android 13 受限设置机制）
- **获权后即时行为与防撤权机制**：有间接抗清理：获权后按 charAt(0)=='1' 调用 setComponentEnabledSetting(C7, COMPONENT_ENABLED_STATE_DISABLED) 隐藏桌面入口；另 C7$1.run 的 charAt(3) 分支预留 ADD_DEVICE_ADMIN 设备管理员激活（本配置位为 0 未触发）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 Activity 启动为触发点：一旦监测到前台 Activity 为 com.android.tester.C7 且随即发生 action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivity（或 C7.onResume 后 0.5s 内出现系统设置包 com.android.settings/.Settings$AccessibilitySettings），立即抓取 UTG；无需等待任何弹窗
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：该样本完全不含任何引导文案/弹窗/WebView/悬浮遮罩，纯 UTG 只能看到'无界面的自家 Activity 一闪 + 系统无障碍页'，若检测器只匹配关键词文案会漏报；需以'应用自身 Activity 无 UI 即跳系统无障碍设置 + 返回即重跳'的行为时序作为主判据。另二阶段载荷（@string/MER=".." 对应包名与 C7$2 下载线程）为动态/远端投放，静态不可见。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/返回后瞬时入口页（无界面证据）** | com.android.tester.C7，窗口为半透明、无标题、无任何 View 文本，且 excludeFromRecents | 证明存在'零界面静默跳转'，是区分恶意诱导与良性说明页的关键反证 | package=com.android.tester 且 activity=C7 但 UTG 文本节点为空；窗口属性 translucent/无标题；0~1s 内 activity 切换至 com.android.settings |
| **系统无障碍服务列表项** | com.android.settings 无障碍设置列表，条目文本 'OfficeSuite'，无副标题/描述 | 证明服务名伪装为办公品牌、且缺失 description 说明，用户无从得知监听全部窗口内容 | 条目 text='OfficeSuite'；条目无 description/summary 文本；开关 checked=false→true 的切换动作 |
| **拒权返回后的二次跳转页** | 从设置页返回后立即重现 com.android.settings 无障碍页（无中间说明页） | 直接抓到 refusal-loop 证据，证明无取消/跳过路径 | back 事件后 <1s 内 com.android.settings 再次前台；无任何 com.android.tester 自有 Activity 停留超过 1s |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.android.tester.C7#onCreate`
- `com.android.tester.C7#onResume`
- `com.android.tester.C7#c`
- `com.android.tester.C7$1#run`
- `com.android.tester.C1#onServiceConnected`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已按 16 次工具调用（略超上限，探索即停）完成定向核验。核心发现：**该样本没有任何引导页面、弹窗、WebView、悬浮遮罩或无障碍说明文字，而是完全静默、无提示地直接跳转系统无障碍设置页，并在返回时无限重跳。**

## 分析结论（要点）

- **入口为不可见 Activity**：[C7](<resource-unit:#1.dex1 code:com.android.tester.C7>) 是唯一 LAUNCHER Activity，主题为 `Theme.Translucent.NoTitleBar` + `excludeFromRecents`，即点击图标后无任何界面，`onCreate` 与 `onResume` 都调用私有方法 [c()](<resource-unit:#1.dex1 code:com.android.tester.C7#c>)。
- **开关来自字符串资源而非界面**：`c()` 读取 `getString(0x7f0c0021)` → `gp = "11000"`，按位字符控制行为。`charAt(1)=='1'` 时启动线程 [C7$1.run()](<resource-unit:#1.dex1 code:com.android.tester.C7$1#run>)，其中执行 `new Intent("android.settings.ACCESSIBILITY_SETTINGS")` + `FLAG_ACTIVITY_NEW_TASK` 直接 `startActivity`。**跳转前零解释、零弹窗、零免责声明**。
- **拒绝即循环**：`C11.j`（无障碍已连接标志）为 false 时，`onResume` 会再次走 `c()` → 再跳系统无障碍设置，用户返回应用即被重新拉起设置页；`finish()` 只在"设备管理员已激活 且 无障碍已开启"同时满足时才执行，因此未授权状态下无法退出该循环，且无取消/跳过按钮。
- **系统列表中的身份伪装**：无障碍服务 `C1` 在 Manifest 中无 `android:label`、无 `android:description`、无 `android.accessibilityservice` meta-data，系统无障碍列表直接显示应用名 `OfficeSuite`（`@string/s`、`@string/app_name`），用户看到的是一个"办公套件"而非监控服务。
- **获权后立即隐身 + 投放二阶段**：`onServiceConnected` 设置 `flags=89`（含 `RETRIEVE_INTERACTIVE_WINDOWS`、`TOUCH_EXPLORATION`、`ENHANCED_WEB_ACCESSIBILITY`）、`eventTypes=-1` 监听全部事件，随后把 `C11.j=true`；下次 `c()` 因 `charAt(0)=='1'` 调用 `a()` → `setComponentEnabledSetting(C7, 2 /*DISABLED*/)` **删除桌面图标**；同时 `charAt(3)` 分支（此处为 0，但代码就绪）会拉起 `ADD_DEVICE_ADMIN`，最后按 `@string/MER`（`".."`）拉起隐藏载荷包或走下载投放线程 `C7$2`。
- **无叠层引导**：全包未出现 `TYPE_SYSTEM_ALERT`/`TYPE_APPLICATION_OVERLAY` 使用点（`SYSTEM_ALERT_WINDOW` 仅声明），也没有 `APPLICATION_DETAILS_SETTINGS`（受限设置教学）与 WebView，因此不存在"遮罩指引/高仿设置页"，诱导手法是**静默跳转 + 无说明 + 拒权循环**。

```json
{
  "static_visibility": "clear",
  "visibility_note": "跳转逻辑、开关位、服务配置全部位于明文 classes.dex（未加壳、无加密载荷），可完整静态还原；仅 C7$2 投放线程内部（下载/落地二阶段载荷）未展开，但不影响无障碍引导链判定",
  "summary_one_liner": "该样本用半透明无界面 Launcher Activity 在冷启动与每次 onResume 时静默直跳系统无障碍设置页，无任何说明文字与取消入口，未开启即无限重跳，开启后自禁用桌面图标并继续投放二阶段载荷",
  "disguise_identity": {
    "app_display_name": "OfficeSuite",
    "claimed_brand_or_persona": "OfficeSuite（伪冒办公文档套件品牌，实际为 SpyNote 系远控）",
    "a11y_service_label": "OfficeSuite（C1 未声明 android:label，回落为应用名 @string/s）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务无 android:description、无 accessibilityservice meta-data，系统列表只剩品牌名而不显示监控能力；入口 Activity 使用 Theme.Translucent.NoTitleBar + excludeFromRecents 实现'点开无界面'；获权后 setComponentEnabledSetting(C7, DISABLED) 删除桌面图标；行为开关藏在字符串资源 gp=\"11000\" 的字符位上，与界面完全解耦"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.android.tester.C7（LAUNCHER Activity，Theme.Translucent.NoTitleBar，excludeFromRecents）",
      "trigger_event": "用户点击桌面图标 → onCreate()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面内容，半透明无标题窗口，无加载提示",
      "user_action_requested": "无（用户仅看到图标一闪）",
      "code_anchor": "com.android.tester.C7#onCreate / AndroidManifest.xml activity C7"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.android.tester.C7#c() 读取 @string/gp = \"11000\" 并起线程 C7$1",
      "trigger_event": "onCreate/onResume → c() → new Thread(new C7$1(this)).start()",
      "ui_carrier": "不可静态还原（纯后台线程，无 UI）",
      "shown_text_verbatim": "11000",
      "shown_text_zh": "内部控制开关串：第0位=获权后自禁用入口、第1位=跳无障碍设置、第2位=记录窗口文本、第3位=设备管理员、第4位=su提权检测",
      "user_action_requested": "无",
      "code_anchor": "com.android.tester.C7#c / res/values/strings.xml key=gp"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "C7$1.run()：charAt(1)=='1' && !C11.j → Intent.setAction(\"android.settings.ACCESSIBILITY_SETTINGS\")，FLAG_ACTIVITY_NEW_TASK(268435456) → startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧未附加任何 EXTRA、未提供说明文案）",
      "shown_text_zh": "直接落到系统无障碍设置列表，列表中显示服务名 OfficeSuite",
      "user_action_requested": "要求用户在系统无障碍列表中自行找到并开启 OfficeSuite 开关；应用未提供任何理由或说明",
      "code_anchor": "com.android.tester.C7$1#run"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "不存在（无 Dialog / 无 WebView / 无 HTML / 无 strings 说明文案）",
      "trigger_event": "无",
      "ui_carrier": "不可静态还原（该步骤在实现中缺失）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "全包检索无 ACCESSIBILITY 用途说明、无隐私声明、无图形引导",
      "user_action_requested": "无",
      "code_anchor": "res/values/strings.xml（仅 app_name=OfficeSuite、s=OfficeSuite、gp、h、n、p、ps、v 等控制串）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.android.tester.C7#onResume → c()",
      "trigger_event": "用户从系统设置返回（未开启无障碍）→ onResume 回调",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "C11.j 仍为 false，再次 startActivity(ACCESSIBILITY_SETTINGS)，用户无法停留在应用内",
      "user_action_requested": "被迫重复开启操作；无取消、无跳过、无返回按钮（onBackPressed 仅 super）",
      "code_anchor": "com.android.tester.C7#onResume / com.android.tester.C7#onBackPressed"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.android.tester.C1（AccessibilityService）onServiceConnected",
      "trigger_event": "用户在系统设置中开启 OfficeSuite 开关 → 服务连接回调",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务静默设置 flags=89、eventTypes=-1 监听全部事件，置 C11.j=true，随后 C1.b() 判定两位开关",
      "user_action_requested": "无（用户已授权，应用不再显示任何确认）",
      "code_anchor": "com.android.tester.C1#onServiceConnected / com.android.tester.C1#b"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.android.tester.C7#a()（setComponentEnabledSetting）与 C7$1.run 的二阶段投放分支",
      "trigger_event": "下次 c()：charAt(0)=='1' → a() 禁用 C7 组件；两条件满足后按 @string/MER(\"..\") 拉起隐藏包或启动 C7$2 下载线程",
      "ui_carrier": "不可静态还原（桌面图标消失、后台投放）",
      "shown_text_verbatim": "..",
      "shown_text_zh": "载荷包名占位（\"..\" 表示不存在的目标，走下载投放路径）；入口图标被系统隐藏",
      "user_action_requested": "无",
      "code_anchor": "com.android.tester.C7#a / com.android.tester.C7$1#run"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项名称：OfficeSuite（来自 @string/s 与 @string/app_name，C1 无 android:label）",
    "系统无障碍服务描述：缺失（C1 未声明 android:description，也无 android.accessibilityservice 配置 xml）",
    "应用内引导文字：完全不存在（无 AlertDialog、无 Toast、无 Activity 布局文案、无 assets HTML/WebView）",
    "跳转前说明：不存在（C7$1.run 构造的 Intent 无 EXTRA，无任何前置页面）",
    "悬浮遮罩/高仿设置页：不存在（全包无 TYPE_SYSTEM_ALERT/TYPE_APPLICATION_OVERLAY 使用点）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "OfficeSuite",
      "text_zh": "办公套件",
      "source_location": "res/values/strings.xml key=app_name / key=s",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "11000",
      "text_zh": "11000（行为开关位串，非用户可见文案）",
      "source_location": "res/values/strings.xml key=gp",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "C7.onResume 每次都调用 c()，只要 C11.j（无障碍已连接）仍为 false 就再次 startActivity(android.settings.ACCESSIBILITY_SETTINGS)；finish() 仅在设备管理员与无障碍条件同时满足时执行，故用户从设置页返回即被立即重跳，形成无法退出的循环",
    "overlay_or_fake_settings": "无叠层引导、无高仿设置页；仅靠 Translucent 无标题 Activity 静默跳转",
    "restricted_settings_13plus_coaching": "无（全包未出现 ACTION_APPLICATION_DETAILS_SETTINGS，无受限设置分步教学；targetSdk=22，本身规避 Android 13 受限设置机制）",
    "post_grant_anti_removal": "有间接抗清理：获权后按 charAt(0)=='1' 调用 setComponentEnabledSetting(C7, COMPONENT_ENABLED_STATE_DISABLED) 隐藏桌面入口；另 C7$1.run 的 charAt(3) 分支预留 ADD_DEVICE_ADMIN 设备管理员激活（本配置位为 0 未触发）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 Activity 启动为触发点：一旦监测到前台 Activity 为 com.android.tester.C7 且随即发生 action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivity（或 C7.onResume 后 0.5s 内出现系统设置包 com.android.settings/.Settings$AccessibilitySettings），立即抓取 UTG；无需等待任何弹窗",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/返回后瞬时入口页（无界面证据）",
        "page_identifier": "com.android.tester.C7，窗口为半透明、无标题、无任何 View 文本，且 excludeFromRecents",
        "why_most_useful": "证明存在'零界面静默跳转'，是区分恶意诱导与良性说明页的关键反证",
        "observable_utg_signals": ["package=com.android.tester 且 activity=C7 但 UTG 文本节点为空", "窗口属性 translucent/无标题", "0~1s 内 activity 切换至 com.android.settings"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍设置列表，条目文本 'OfficeSuite'，无副标题/描述",
        "why_most_useful": "证明服务名伪装为办公品牌、且缺失 description 说明，用户无从得知监听全部窗口内容",
        "observable_utg_signals": ["条目 text='OfficeSuite'", "条目无 description/summary 文本", "开关 checked=false→true 的切换动作"]
      },
      {
        "page_role": "拒权返回后的二次跳转页",
        "page_identifier": "从设置页返回后立即重现 com.android.settings 无障碍页（无中间说明页）",
        "why_most_useful": "直接抓到 refusal-loop 证据，证明无取消/跳过路径",
        "observable_utg_signals": ["back 事件后 <1s 内 com.android.settings 再次前台", "无任何 com.android.tester 自有 Activity 停留超过 1s"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：该样本完全不含任何引导文案/弹窗/WebView/悬浮遮罩，纯 UTG 只能看到'无界面的自家 Activity 一闪 + 系统无障碍页'，若检测器只匹配关键词文案会漏报；需以'应用自身 Activity 无 UI 即跳系统无障碍设置 + 返回即重跳'的行为时序作为主判据。另二阶段载荷（@string/MER=\"..\" 对应包名与 C7$2 下载线程）为动态/远端投放，静态不可见。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.android.tester.C7#onCreate",
    "com.android.tester.C7#onResume",
    "com.android.tester.C7#c",
    "com.android.tester.C7$1#run",
    "com.android.tester.C1#onServiceConnected",
    "res/values/strings.xml"
  ]
}
```

**覆盖边界**：`C7$2` 下载/落地线程与 `C11`（Socket 远控主体，含 `C11.j` 状态机、`82.137.218.185` 等 `@string/h`、`@string/p` 配置）未逐函数展开，二阶段载荷内容属远端/动态范围；本轮已足以确认无障碍申请路径为"静默跳转 + 无说明 + 拒权循环 + 获权自隐身"。

</details>

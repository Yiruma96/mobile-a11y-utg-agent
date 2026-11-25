# MR_079__b59675f673｜StealJob — Google Play Services

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：150.1s

## 1. 一句话核心结论

- **核心申请方式**：应用完全不引导也不跳转，而是把自身无障碍服务伪装成系统级“Google Play Services”静置在系统无障碍列表中，等用户误认后手动开启，随后静默记录全设备输入并连同短信、通讯录、通话记录外传至 C2。
- **静态可见性说明**：Manifest、res/xml/accessibility.xml、strings.xml 与 classes.dex 全部逻辑均静态可见，未加壳、无加密载荷、无动态加载；唯一不可静态确认的是远端 C2 param.drivethrough.top 的实时下发内容。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b59675f67358606ffe1af42911aec3c7223e6b7ab7f024682a4ab48026d51ddc` |
| 包名 / 年份 | `googie.comhm.carier` / 2019 |
| 家族 / 品类 | **StealJob**（同池样本数：4） |
| 原始来源标识 | https://ti.360.net/blog/articles/stealjob-new-android-malware-used-by-donot-apt-group-en/ |
| 桌面显示名 | Google Play Services |
| 引导页宣称品牌/身份 | Google Play Services（Google 官方系统组件） |
| 系统无障碍列表服务名 | Google Play Services |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 googie.comhm.carier 与 Google 无关；无障碍服务标签与 android:description 复用同一 app_name 字符串，使系统无障碍列表中该条目与描述均显示为“Google Play Services”；服务类被拆分到 com.system.android.updaute.nine.ninere 且项目内类名以数字英文（ten/nine/ninere/eightre）命名，属家族化混淆；未使用多 activity-alias、同形字或伪造 isAccessibilityTool |
| 无障碍服务类名 | `com.system.android.updaute.nine.ninere` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Google Play Services |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.system.android.updaute.MainActivity（launcher Activity） | onCreate() | 不可静态还原 | 无 | 无需任何操作；用户点击图标后看不到任何页面或提示 | `com.system.android.updaute.MainActivity#onCreate` |
| 2 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载的服务 列表项（com.system.android.updaute.nine.ninere） | 用户自行进入系统设置手动开启（应用内无任何跳转调用） | 系统无障碍页 | **原文**：Google Play Services<br>**译注**：Google Play 服务 | 要求用户手动点击该条目并打开开关；应用不提供取消/跳过按钮，因为不存在引导弹窗 | `res/values/strings.xml#L19 (app_name) + res/xml/accessibility.xml (android:description=@string/app_name) + AndroidManifest service android:label=@string/app_name` |
| 3 | 获权后动作 | com.system.android.updaute.nine.ninere（AccessibilityService） | onServiceConnected() | 不可静态还原 | 无 | 无 | `com.system.android.updaute.nine.ninere#onServiceConnected` |
| 4 | 获权后动作 | com.system.android.updaute.nine.ninere.onAccessibilityEvent（TYPE_VIEW_TEXT_CHANGED） | 任意应用内输入框文本变化事件（eventType 16）且 ten.fg.klog.wm 为真 | 不可静态还原 | 无 | 无 | `com.system.android.updaute.nine.ninere#onAccessibilityEvent` |
| 5 | 获权后动作 | com.system.android.updaute.ten$runto#two（Socket 回传线程） | ten.onStartCommand 启动的 runto 线程连接 param.drivethrough.top:6000 | 不可静态还原 | 无 | 无 | `com.system.android.updaute.ten.ten$runto#two` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表中该条目的名称：AndroidManifest service android:label="@string/app_name" → "Google Play Services"
- 系统无障碍服务列表中该条目的说明文字：res/xml/accessibility.xml android:description="@string/app_name" → "Google Play Services"
- 桌面启动器图标下方名称：application android:label="@string/app_name" → "Google Play Services"
- 应用内部不存在任何引导/说明文字呈现位置：无引导 Activity、无 Dialog、无 assets HTML、无远端 WebView、无悬浮窗 Overlay

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Google Play Services | Google Play 服务 | `res/values/strings.xml key=app_name，被 application/android:label、无障碍 service/android:label、accessibility.xml/android:description 三处复用` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无。应用内不存在跳转无障碍设置的代码，也不存在 onResume 检测重跳或定时拉起机制；nine.isAccessibilitySettingsOn 虽实现了启用状态检测，但全 DEX 无任何调用者，因此拒绝或返回系统设置后应用不做任何反应。
- **遮罩叠层 / 高仿系统设置页**：无。未发现 WindowManager.addView、LayoutParams、TYPE_SYSTEM_ALERT/TYPE_APPLICATION_OVERLAY 等悬浮窗或遮罩实现，也无高仿无障碍开关页面。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无。onServiceConnected 仅初始化列表，未见自点确认、自授权或通过 GLOBAL_ACTION_BACK/HOME 阻止撤权。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：应用内无任何引导动作可作触发器。建议在冷启动 launcher Activity 拉起时立即开始录制并随后直接导航至 设置→无障碍→已下载的服务，捕获系统无障碍列表中出现“Google Play Services”条目的瞬间；同时在开启该服务后持续录制，观察是否出现任何应用自绘界面（预期为无界面静默态）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：一是应用无任何引导页面，纯 UTG 若无“主动导航到系统无障碍列表”这一步将完全捕获不到伪装文本，需依赖包名与 label 的静态比对补充；二是真正的危害行为（按键记录、C2 外传）发生在无界面后台，UTG 页面视角无法观测，须结合流量或 Hook 才能确认。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首屏（launcher Activity）** | com.system.android.updaute.MainActivity，预期为空白/黑屏且瞬时退出，无 setContentView 内容 | 确认应用自身完全没有引导 UI，把“引导”责任完全推给系统无障碍列表，是区分本样本与常规假更新/假清理诱导的关键 | 首屏无任何可点击控件或文案；Activity 生命周期极短（onCreate 内即 startService 结束）；无权限弹窗、无 Dialog 层级 |
| **系统无障碍服务列表项** | Settings 无障碍列表中出现 label="Google Play Services"、description="Google Play Services" 的服务条目 | 这是本样本唯一的身份伪装呈现点，UTG 可直接提取列表项文本，与包名 googie.comhm.carier 比对即可判定品牌冒充 | 列表项文本 Google Play Services；同页其它条目为真实系统组件形成对比；开关初始为关闭，需用户手动点击 |
| **获权后的运行态（应为无界面）** | 开启服务后无任何新 Activity/悬浮窗，仅后台 ten / runto 线程活动 | 验证“获权即静默窃密”而非提供任何可见功能，可排除良性透明说明的可能 | 无障碍开启后无引导完成页或功能页；无 Toast/通知告知数据采集；界面停留在用户原应用，输入内容被后台记录 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.system.android.updaute.MainActivity#onCreate`
- `com.system.android.updaute.nine.ninere#onAccessibilityEvent`
- `com.system.android.updaute.nine.nine#isAccessibilitySettingsOn`
- `com.system.android.updaute.ten.ten$runto#two`
- `res/xml/accessibility.xml`
- `res/values/strings.xml#L19`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**核心发现：该应用没有“引导”过程——它不存在任何无障碍引导页面或跳转逻辑。**

1. **无引导代码路径**：全 DEX 中不存在 `android.settings.ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`com.android.settings` 等字符串，`startActivity` 也没有任何调用点；没有 assets 或 HTML 资源，也没有悬浮窗（`addView`、`LayoutParams`、`TYPE_SYSTEM_ALERT` 均无命中）。冷启动时，[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.system.android.updaute.MainActivity#onCreate>) 只执行 `startService(ten)`，界面上什么都不显示。
2. **唯一“引导”载体是系统无障碍列表本身**：[res/values/strings.xml#L19](<resource-unit:#1 file:res/values/strings.xml#L19>) 将 `app_name` 定义为 `Google Play Services`，Manifest 中 launcher Activity 与无障碍服务 [com.system.android.updaute.nine.ninere](<resource-unit:#1.dex1 code:com.system.android.updaute.nine.ninere>) 均使用 `android:label="@string/app_name"`，[res/xml/accessibility.xml](<resource-unit:#1 file:res/xml/accessibility.xml>) 的 `android:description` 也指向同一字符串。用户只能在系统设置中看到一条“Google Play Services”并手动开启，而包名 `googie.comhm.carier` 与 Google 无关。
3. **权限申请是否成功只做读取校验、不做弹窗**：[nine.isAccessibilitySettingsOn()](<resource-unit:#1.dex1 code:com.system.android.updaute.nine.nine#isAccessibilitySettingsOn>) 仅读取 `accessibility_enabled` / `enabled_accessibility_services` 判断自身是否启用，而且该方法**没有任何调用者**，因此没有“拒绝后再跳转”的循环机制。
4. **开启后的实际行为**：[ninere.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.system.android.updaute.nine.ninere#onAccessibilityEvent>) 在云端 `Key` 开关（`ten.setflags()` 读取 SharedPreferences `Keyflag`，默认 true）为真时，抓取 `TYPE_VIEW_TEXT_CHANGED` 的 `event.getText()` 并累积到 `ninelo`，实现跨应用键盘记录；[ten$runto.two()](<resource-unit:#1.dex1 code:com.system.android.updaute.ten.ten$runto#two>) 硬编码连接 `param.drivethrough.top:6000`，先上报 `IMEI:已启用服务列表`，再按服务端 15 位 Flags 回传 `keys.txt`、`contacts.txt`、`sms.txt`、`CallLogs.txt`、`accounts.txt` 等文件。
5. **证据边界**：未见加壳、VMP 或加密载荷，静态完整可见；`ninere.onServiceConnected()` 只初始化列表，没有自点确认、阻止撤权或遮挡层行为；C2 当前下发内容不可静态确认。

因此从 UTG 视角看，可捕获的只有“系统无障碍列表中的伪装条目”与“开启后无任何界面的静默状态”，不存在可截图的引导弹窗序列。

```json
{
  "static_visibility": "clear",
  "visibility_note": "Manifest、res/xml/accessibility.xml、strings.xml 与 classes.dex 全部逻辑均静态可见，未加壳、无加密载荷、无动态加载；唯一不可静态确认的是远端 C2 param.drivethrough.top 的实时下发内容。",
  "summary_one_liner": "应用完全不引导也不跳转，而是把自身无障碍服务伪装成系统级“Google Play Services”静置在系统无障碍列表中，等用户误认后手动开启，随后静默记录全设备输入并连同短信、通讯录、通话记录外传至 C2。",
  "disguise_identity": {
    "app_display_name": "Google Play Services",
    "claimed_brand_or_persona": "Google Play Services（Google 官方系统组件）",
    "a11y_service_label": "Google Play Services",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 googie.comhm.carier 与 Google 无关；无障碍服务标签与 android:description 复用同一 app_name 字符串，使系统无障碍列表中该条目与描述均显示为“Google Play Services”；服务类被拆分到 com.system.android.updaute.nine.ninere 且项目内类名以数字英文（ten/nine/ninere/eightre）命名，属家族化混淆；未使用多 activity-alias、同形字或伪造 isAccessibilityTool"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.system.android.updaute.MainActivity（launcher Activity）",
      "trigger_event": "onCreate()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面内容，Activity 无 setContentView，直接启动后台 Service 后结束",
      "user_action_requested": "无需任何操作；用户点击图标后看不到任何页面或提示",
      "code_anchor": "com.system.android.updaute.MainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载的服务 列表项（com.system.android.updaute.nine.ninere）",
      "trigger_event": "用户自行进入系统设置手动开启（应用内无任何跳转调用）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Play Services",
      "shown_text_zh": "Google Play 服务",
      "user_action_requested": "要求用户手动点击该条目并打开开关；应用不提供取消/跳过按钮，因为不存在引导弹窗",
      "code_anchor": "res/values/strings.xml#L19 (app_name) + res/xml/accessibility.xml (android:description=@string/app_name) + AndroidManifest service android:label=@string/app_name"
    },
    {
      "step": 3,
      "stage": "获权后动作",
      "screen_or_component": "com.system.android.updaute.nine.ninere（AccessibilityService）",
      "trigger_event": "onServiceConnected()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "仅清空并重建 ninelo 列表，无任何 UI、Toast、通知或悬浮窗反馈",
      "user_action_requested": "无",
      "code_anchor": "com.system.android.updaute.nine.ninere#onServiceConnected"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.system.android.updaute.nine.ninere.onAccessibilityEvent（TYPE_VIEW_TEXT_CHANGED）",
      "trigger_event": "任意应用内输入框文本变化事件（eventType 16）且 ten.fg.klog.wm 为真",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静默把各应用的输入文本按包名与时间累积到 ninelo，用户完全无感知",
      "user_action_requested": "无",
      "code_anchor": "com.system.android.updaute.nine.ninere#onAccessibilityEvent"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.system.android.updaute.ten$runto#two（Socket 回传线程）",
      "trigger_event": "ten.onStartCommand 启动的 runto 线程连接 param.drivethrough.top:6000",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "上报 IMEI 与已启用服务列表，随后按服务端 15 位 Flags 上传 keys.txt、contacts.txt、sms.txt、CallLogs.txt、accounts.txt 等文件",
      "user_action_requested": "无",
      "code_anchor": "com.system.android.updaute.ten.ten$runto#two"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表中该条目的名称：AndroidManifest service android:label=\"@string/app_name\" → \"Google Play Services\"",
    "系统无障碍服务列表中该条目的说明文字：res/xml/accessibility.xml android:description=\"@string/app_name\" → \"Google Play Services\"",
    "桌面启动器图标下方名称：application android:label=\"@string/app_name\" → \"Google Play Services\"",
    "应用内部不存在任何引导/说明文字呈现位置：无引导 Activity、无 Dialog、无 assets HTML、无远端 WebView、无悬浮窗 Overlay"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Google Play Services",
      "text_zh": "Google Play 服务",
      "source_location": "res/values/strings.xml key=app_name，被 application/android:label、无障碍 service/android:label、accessibility.xml/android:description 三处复用",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无。应用内不存在跳转无障碍设置的代码，也不存在 onResume 检测重跳或定时拉起机制；nine.isAccessibilitySettingsOn 虽实现了启用状态检测，但全 DEX 无任何调用者，因此拒绝或返回系统设置后应用不做任何反应。",
    "overlay_or_fake_settings": "无。未发现 WindowManager.addView、LayoutParams、TYPE_SYSTEM_ALERT/TYPE_APPLICATION_OVERLAY 等悬浮窗或遮罩实现，也无高仿无障碍开关页面。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无。onServiceConnected 仅初始化列表，未见自点确认、自授权或通过 GLOBAL_ACTION_BACK/HOME 阻止撤权。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "应用内无任何引导动作可作触发器。建议在冷启动 launcher Activity 拉起时立即开始录制并随后直接导航至 设置→无障碍→已下载的服务，捕获系统无障碍列表中出现“Google Play Services”条目的瞬间；同时在开启该服务后持续录制，观察是否出现任何应用自绘界面（预期为无界面静默态）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首屏（launcher Activity）",
        "page_identifier": "com.system.android.updaute.MainActivity，预期为空白/黑屏且瞬时退出，无 setContentView 内容",
        "why_most_useful": "确认应用自身完全没有引导 UI，把“引导”责任完全推给系统无障碍列表，是区分本样本与常规假更新/假清理诱导的关键",
        "observable_utg_signals": ["首屏无任何可点击控件或文案", "Activity 生命周期极短（onCreate 内即 startService 结束）", "无权限弹窗、无 Dialog 层级"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中出现 label=\"Google Play Services\"、description=\"Google Play Services\" 的服务条目",
        "why_most_useful": "这是本样本唯一的身份伪装呈现点，UTG 可直接提取列表项文本，与包名 googie.comhm.carier 比对即可判定品牌冒充",
        "observable_utg_signals": ["列表项文本 Google Play Services", "同页其它条目为真实系统组件形成对比", "开关初始为关闭，需用户手动点击"]
      },
      {
        "page_role": "获权后的运行态（应为无界面）",
        "page_identifier": "开启服务后无任何新 Activity/悬浮窗，仅后台 ten / runto 线程活动",
        "why_most_useful": "验证“获权即静默窃密”而非提供任何可见功能，可排除良性透明说明的可能",
        "observable_utg_signals": ["无障碍开启后无引导完成页或功能页", "无 Toast/通知告知数据采集", "界面停留在用户原应用，输入内容被后台记录"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：一是应用无任何引导页面，纯 UTG 若无“主动导航到系统无障碍列表”这一步将完全捕获不到伪装文本，需依赖包名与 label 的静态比对补充；二是真正的危害行为（按键记录、C2 外传）发生在无界面后台，UTG 页面视角无法观测，须结合流量或 Hook 才能确认。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.system.android.updaute.MainActivity#onCreate",
    "com.system.android.updaute.nine.ninere#onAccessibilityEvent",
    "com.system.android.updaute.nine.nine#isAccessibilitySettingsOn",
    "com.system.android.updaute.ten.ten$runto#two",
    "res/xml/accessibility.xml",
    "res/values/strings.xml#L19"
  ]
}
```

</details>

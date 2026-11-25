# MB_005__4defa1f795｜Cerberus — test

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：204.3s

## 1. 一句话核心结论

- **核心申请方式**：后台 IntentService 每秒轮询无障碍未启用状态，累计计数后拉起布局全空的 AccessActivity，弹出仅含"确定"、吞掉返回/菜单键的全屏 AlertDialog，点击即跳转 android.settings.ACCESSIBILITY_SETTINGS，关闭后再被循环拉起，获权后自动点击卸载/停用按钮并发送 BACK 阻止撤权。
- **静态可见性说明**：无障碍诱导全链路均在 DEX、layout、strings、xml 中静态可读，无加壳、无加密资源、无远端 HTML；仅远端 C2（Netmanager、模块下载）控制部分不在本命题范围。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `4defa1f795d69d38168bffecbc19f571c61a095862713fd91cb646f344ef53c0` |
| 包名 / 年份 | `com.framull.test` / 2023 |
| 家族 / 品类 | **Cerberus**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | test |
| 引导页宣称品牌/身份 | 无品牌宣称，仅以自身 label "test" 自称；实际为 Cerberus 系银行木马（短信拦截、覆盖层、HVNC、键盘记录） |
| 系统无障碍列表服务名 | Test Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：桌面名 test、服务名 Test Service、包名 com.framull.test 均无功能或品牌含义；AccessActivity 使用 android:label="" 与 Theme.NoDisplay 类空标签；res/layout/popup.xml 为 visibility=invisible 的全屏空 FrameLayout，引导内容只存在于系统 AlertDialog；onKeyDown 屏蔽 keyCode 3/4/82（HOME/BACK/MENU）使弹窗无法退出；无障碍服务未声明 android:description，系统中只显示 "Test Service"；另存在 label="Fake" 且 android:enabled="false" 的 com.example.mmm.fake 备用 launcher alias。 |
| 无障碍服务类名 | `com.example.mmm.Services.Access` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.example.mmm.IndexACT（LAUNCHER，category android.app.role.SMS） | 用户点击桌面图标 "test" → onCreate | 原生Activity | 无 | 无（用户看不到任何内容，误以为应用已打开） | `com.example.mmm.IndexACT.onCreate` |
| 2 | 业务功能触发 | com.example.mmm.Services.srvWhileWorker（IntentService，while(true) 后台循环） | IndexACT 启动；或 BooterConfig 收到 BOOT_COMPLETED / SMS_RECEIVED / USER_PRESENT / PACKAGE_ADDED 后重新拉起 | 不可静态还原 | 无 | 无 | `com.example.mmm.Services.srvWhileWorker.onHandleIntent` |
| 3 | 拒权反馈循环 | com.example.mmm.Services.srvToaskAccessibility（Toast 催促） | activityAccessibilityVisible=="1" 且 itoaskAccessibility>=4（即用户已在弹窗点过确定但仍未启用） | 通知栏 | **原文**：Enable Test Service<br>**译注**：启用 Test Service（多语言表 localeForAccessibility：en=Enable、zh=启用、de=Aktivieren 等，拼接 " " + "Test Service"） | 无按钮，仅屏幕中央 Toast 持续催促 | `com.example.mmm.Services.srvToaskAccessibility.onStartCommand；com.example.mmm.defines#localeForAccessibility` |
| 4 | 引导说明页 | com.example.mmm.Main.AccessActivity + AlertDialog（R$style.FullScreenDialog） | srvWhileWorker 中 start_Q>=6 且 accessactivity==false → startActivity(FLAG_ACTIVITY_NEW_TASK\|SINGLE_TOP\|CLEAR_TASK) | 原生Dialog | **原文**：Title: test（utl.getLabelApplication 小写代入 APPNAME）<br>Message: "Please enable accessibility permissions to use test:<br>Select Downloaded apps → test → allow"<br>Button: "OK"<br>中文资源: "请开启辅助功能权限，以便于使用 {APPNAME} 功能:" / "确定"<br>**译注**：标题为应用自身名称 test；正文要求"请开启辅助功能权限以便使用 test：选择 已下载的应用 → test → 允许"；唯一按钮"确定/OK" | 只能点"确定"；无取消、无跳过、无关闭按钮，返回键/HOME 键/菜单键被 onKeyDown 返回 true 吞掉 | `com.example.mmm.Main.AccessActivity.showPopup；com.example.mmm.Main.AccessActivity.onKeyDown；res/values/strings.xml（dialog_message / dialog_ok）；res/layout/popup.xml` |
| 5 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（已下载的服务列表） | 弹窗"确定"按钮 onClick；或 WebView 侧 JavascriptInterface returnResult() | 系统无障碍页 | **原文**：无（应用不注入任何文案，依赖系统页原样显示 "Test Service"）<br>**译注**：用户被直接丢到系统无障碍服务列表，需自行找到 "Test Service" 并打开开关 | 在系统列表中找到 Test Service 并手动启用；若未启用则 isAccessibilityServiceEnabled 仍为 false，弹窗下次照常出现 | `com.example.mmm.Main.AccessActivity$1.onClick；com.example.mmm.Main.AccessActivity$WebAppInterface.returnResult` |
| 6 | 拒权反馈循环 | srvWhileWorker 再次拉起 AccessActivity | 用户返回/放弃后，后台循环继续计数，start_Q 重新累计到 6 即再次拉起；accessactivity 标志仅在拉起瞬间置真，进程重启后复位 | 原生Dialog | **原文**：同上 dialog_message<br>**译注**：同一不可取消弹窗再次出现，直到用户在系统设置中真正启用服务 | 再次只能点"确定" | `com.example.mmm.Services.srvWhileWorker.onHandleIntent` |
| 7 | 获权后动作 | com.example.mmm.Services.Access（无障碍服务，label "Test Service"） | TYPE_WINDOW_STATE_CHANGED；包名 com.android.packageinstaller 或类名 com.android.settings.applications.InstalledAppDetailsTop | 不可静态还原 | **原文**：Log.d(TAG_LOG, "antiuninstall clicked: " + "android:id/button2")<br>**译注**：在卸载/安装确认界面自动点击 button2（取消卸载），在应用详情页检测到自身应用名时执行 performGlobalAction(1)=GLOBAL_ACTION_BACK 将用户退出该页，阻止停用无障碍或卸载 | 用户无法完成撤权或卸载操作 | `com.example.mmm.Services.Access.onAccessibilityEvent；res/xml/serviceconfig.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- AccessActivity 全屏不可取消 AlertDialog（R$style.FullScreenDialog）：标题为应用 label "test"，正文为 dialog_message 把 {APPNAME} 替换为 "test"
- res/layout/popup.xml：visibility=invisible 的全屏空 FrameLayout，仅作 Activity 载体，不承载任何文字
- res/values/strings.xml 的 dialog_message / dialog_ok（含 en、de、zh 三套本地化）
- com.example.mmm.defines#localeForAccessibility 多语言 JSON 表 + strAccessbilityService="Test Service" 拼成的居中 Toast（"Enable Test Service"）
- 系统无障碍服务列表：服务 label="Test Service"，无 android:description 说明文字
- 系统设置页 android.settings.ACCESSIBILITY_SETTINGS 原样展示，应用不叠加自定义文字

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please enable accessibility permissions to use {APPNAME}:<br>Select Downloaded apps → {APPNAME} → allow | 请开启无障碍权限以便使用 {APPNAME}：选择"已下载的应用" → {APPNAME} → 允许 | `res/values/strings.xml → string/dialog_message` | 受限设置分步教学 |
| zh | 请开启辅助功能权限，以便于使用 {APPNAME} 功能: | 请开启辅助功能权限，以便于使用 {APPNAME} 功能： | `res/values-zh/strings.xml → string/dialog_message` | 受限设置分步教学 |
| de | Bitte Aktiviere die Bedienungshilfen um {APPNAME} zu benutzen: | 请启用辅助功能以便使用 {APPNAME}： | `res/values-de/strings.xml → string/dialog_message` | 受限设置分步教学 |
| en | OK | 确定 | `res/values/strings.xml → string/dialog_ok` | 未知 |
| en | Enable Test Service | 启用 Test Service | `com.example.mmm.defines#localeForAccessibility + string_64(" ") + strAccessbilityService("Test Service")，由 srvToaskAccessibility.onStartCommand 拼接` | 未知 |
| en | Test Service | Test Service（测试服务） | `AndroidManifest.xml → service com.example.mmm.Services.Access 的 android:label；com.example.mmm.defines#strAccessbilityService` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：srvWhileWorker 的 while(true) 每 1000ms 复查 isAccessibilityServiceEnabled，未启用且亮屏时 start_Q 持续累加，达到 6 即再次 startActivity(AccessActivity) 并复位计数；同时 itoaskAccessibility 达到 4 就拉起 srvToaskAccessibility 弹 Toast。用户点"确定"后写 activityAccessibilityVisible=1 使 Toast 催促生效；返回/关闭弹窗不会终止循环，仅进程被杀或服务启用才停止。
- **遮罩叠层 / 高仿系统设置页**：无高仿系统页，也不使用 SYSTEM_ALERT_WINDOW 遮罩；以 Theme.FullScreenDialog 的系统 AlertDialog + 不可见全屏 FrameLayout 充当"全屏引导层"，视觉上覆盖整个屏幕。
- **Android 13+ 受限设置（Restricted Settings）应对**：有，dialog_message 明示 "Select Downloaded apps → {APPNAME} → allow"（选择"已下载的应用"再允许），即 Android 13+ 受限设置的分步教学；未使用 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：Access.onAccessibilityEvent 在 com.android.packageinstaller 窗口点击 android:id/button2（卸载确认/取消按钮，日志 antiuninstall clicked）；在 com.android.settings.applications.InstalledAppDetailsTop 检测到自身应用名时 performGlobalAction(1)（GLOBAL_ACTION_BACK）把用户退出应用详情页；srvWhileWorker 在 killApplication 命中自身且无障碍已启用时写 autoClick=1 并移除设备管理器。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 com.example.mmm.Main.AccessActivity 进入前台（其主题为 FullScreenDialog 且布局不可见），或 Activity 启动后 500–1500ms 内出现 AlertDialog 窗口；随后 1–3s 内若前台切换到 com.android.settings 的 ACCESSIBILITY_SETTINGS 即命中完整链路。另可监测 srvToaskAccessibility 产生的 "Enable Test Service" Toast 作为弱信号。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导文案为纯文本，UTG 可直接提取。需注意两点：一是 LAUNCHER 入口 IndexACT 立即 finish，若检测器以"前台 Activity 停留时长"为判据可能漏抓冷启动瞬间，建议以 Activity 生命周期回调而非画面停留判定；二是引导由后台 IntentService 定时驱动，若后台服务未启动（如缺少 BooterConfig 广播或进程被限制）则弹窗不会出现，此时应手动触发 BOOT_COMPLETED 或直接 am start 该 LAUNCHER 入口以恢复链路。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | 包名 com.framull.test 的 Activity com.example.mmm.Main.AccessActivity + 系统 AlertDialog 窗口；标题与正文均为 "test" | 这是应用唯一向用户告知无障碍用途的界面，可直接判定告知是否充分、是否可取消、是否屏蔽返回键 | 弹窗仅存在 1 个按钮（确定/OK），无取消/关闭/跳过；标题与正文均为应用自身名 test，无功能说明与隐私承诺；按 BACK 后弹窗仍在前台（onKeyDown 返回 true）；弹窗背后无任何可见 Activity 内容（popup.xml 为空不可见 FrameLayout） |
| **跳转后系统无障碍服务列表项** | com.android.settings 的 ACCESSIBILITY_SETTINGS，列表中服务名为 "Test Service"，无 description 摘要 | 核对系统侧呈现的服务身份与描述缺失，验证身份与功能不匹配、无告知说明 | 服务名称仅为 "Test Service"；条目下方无任何功能说明文字；开关初始为关闭状态 |
| **拒权返回后的循环拉起页** | 再次出现的 com.example.mmm.Main.AccessActivity 弹窗；间隔约 6–8 秒 | 证明诱导为强制循环而非一次性提示，是判定"拒权反馈循环"的关键 | 同一弹窗文本在用户退出后重复出现；出现次数随时间线性增长；期间夹杂 "Enable Test Service" Toast |
| **获权后压栈遮罩/反撤权页** | com.android.settings 的 InstalledAppDetailsTop 被立即 BACK 退出；com.android.packageinstaller 的卸载确认按钮被自动点击 | 验证获权后的反移除与阻止撤权行为，是权限维持的直接运行证据 | 打开应用详情页后 1 秒内自动返回上一级；卸载确认对话框中"取消"按钮被自动点击；无障碍开关被用户关闭后再次被拉起引导 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.example.mmm.Services.srvWhileWorker.onHandleIntent`
- `com.example.mmm.Main.AccessActivity.showPopup`
- `com.example.mmm.Main.AccessActivity.onKeyDown`
- `com.example.mmm.Main.AccessActivity$1.onClick`
- `com.example.mmm.Services.Access.onAccessibilityEvent`
- `res/values/strings.xml（dialog_message / dialog_ok）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**静态可见性**：无障碍引导链完全静态可见，未加壳、无加密载荷。核心入口是后台 `IntentService` 与一个隐藏 Activity，与常规"Activity 内嵌引导页"完全不同。

**关键发现**

1. **桌面图标无界面**：LAUNCHER 入口 [IndexACT.onCreate](<resource-unit:#1.dex1 code:com.example.mmm.IndexACT#onCreate>) 只写屏幕尺寸设置、启动 `srvWhileWorker` 后立即 `finish()`，用户点击"test"图标后看不到任何 UI。
2. **后台每秒轮询 + 计数拉起**：[srvWhileWorker.onHandleIntent](<resource-unit:#1.dex1 code:com.example.mmm.Services.srvWhileWorker#onHandleIntent>) 在 `while(true)` 中每 1000 ms 检查 `enabled_accessibility_services`；未启用且亮屏时计数，`itoaskAccessibility>=4` 弹 Toast，`start_Q>=6` 时以 `NEW_TASK|SINGLE_TOP|CLEAR_TASK` 拉起 `AccessActivity`，并把 `accessactivity=true`、`start_Q=0`，形成"关掉再拉起"的死循环。
3. **弹窗不可取消**：[AccessActivity.showPopup](<resource-unit:#1.dex1 code:com.example.mmm.Main.AccessActivity#showPopup>) 用 `FullScreenDialog` 构建 `AlertDialog`，只有 `setPositiveButton(dialog_ok)`，无负向按钮、无 `setCancelable`；[onKeyDown](<resource-unit:#1.dex1 code:com.example.mmm.Main.AccessActivity#onKeyDown>) 对 `keyCode==3/4/82`（HOME/BACK/MENU）直接 `return true` 吞掉。
4. **页面本体是空的**：[popup.xml](<resource-unit:#1 file:res/layout/popup.xml>) 仅为 `visibility="invisible"` 的全屏 `FrameLayout`，所有引导文字都压在系统弹窗上，Activity 本身不可见。
5. **跳设置点**：[AccessActivity$1.onClick](<resource-unit:#1.dex1 code:com.example.mmm.Main.AccessActivity$1#onClick>) 与 WebView 的 [WebAppInterface.returnResult](<resource-unit:#1.dex1 code:com.example.mmm.Main.AccessActivity$WebAppInterface#returnResult>) 都执行 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，并先写 `activityAccessibilityVisible=1` 作为后续 Toast 催促的开关。
6. **文案只教操作，不讲用途**：[strings.xml](<resource-unit:#1 file:res/values/strings.xml>) 中 `dialog_message` = `"Please enable accessibility permissions to use {APPNAME}: Select Downloaded apps → {APPNAME} → allow"`，无任何隐私承诺或功能必要性说明。
7. **服务名伪装**：服务 `label="Test Service"`，配置 [serviceconfig.xml](<resource-unit:#1 file:res/xml/serviceconfig.xml>) 为 `typeAllMask / feedbackAllMask / flagReportViewIds / canRetrieveWindowContent=true`，即读取任意界面内容的最高能力；无 `android:description`，系统无障碍列表里只有"Test Service"字样。
8. **获权后转向对抗撤权**：[Access.onAccessibilityEvent](<resource-unit:#1.dex1 code:com.example.mmm.Services.Access#onAccessibilityEvent>) 在 `com.android.packageinstaller` 窗口点 `android:id/button2`（日志 `antiuninstall clicked`），在 `com.android.settings.applications.InstalledAppDetailsTop` 出现应用名时 `performGlobalAction(1)`（BACK）把用户挤出应用详情页。
9. **无任何降级路径**：不存在取消、跳过、手动模式或功能受限说明分支；`onStop/onDestroy` 只调父类。

**UTG 视角**：检测时机应锚定 `AccessActivity` 弹窗（每次 `srvWhileWorker` 计数到 6 就出现一次），以及紧接其后的系统无障碍设置页；两者之间的时间差很短，适合"弹窗 → 跳转"成对抓取。

已登记风险：**R-001**（high，deceptive_behavior，autonomous_audit）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍诱导全链路均在 DEX、layout、strings、xml 中静态可读，无加壳、无加密资源、无远端 HTML；仅远端 C2（Netmanager、模块下载）控制部分不在本命题范围。",
  "summary_one_liner": "后台 IntentService 每秒轮询无障碍未启用状态，累计计数后拉起布局全空的 AccessActivity，弹出仅含\"确定\"、吞掉返回/菜单键的全屏 AlertDialog，点击即跳转 android.settings.ACCESSIBILITY_SETTINGS，关闭后再被循环拉起，获权后自动点击卸载/停用按钮并发送 BACK 阻止撤权。",
  "disguise_identity": {
    "app_display_name": "test",
    "claimed_brand_or_persona": "无品牌宣称，仅以自身 label \"test\" 自称；实际为 Cerberus 系银行木马（短信拦截、覆盖层、HVNC、键盘记录）",
    "a11y_service_label": "Test Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "桌面名 test、服务名 Test Service、包名 com.framull.test 均无功能或品牌含义；AccessActivity 使用 android:label=\"\" 与 Theme.NoDisplay 类空标签；res/layout/popup.xml 为 visibility=invisible 的全屏空 FrameLayout，引导内容只存在于系统 AlertDialog；onKeyDown 屏蔽 keyCode 3/4/82（HOME/BACK/MENU）使弹窗无法退出；无障碍服务未声明 android:description，系统中只显示 \"Test Service\"；另存在 label=\"Fake\" 且 android:enabled=\"false\" 的 com.example.mmm.fake 备用 launcher alias。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.example.mmm.IndexACT（LAUNCHER，category android.app.role.SMS）",
      "trigger_event": "用户点击桌面图标 \"test\" → onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面；写屏幕宽高设置、启动 srvWhileWorker 后立即 finish()",
      "user_action_requested": "无（用户看不到任何内容，误以为应用已打开）",
      "code_anchor": "com.example.mmm.IndexACT.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.example.mmm.Services.srvWhileWorker（IntentService，while(true) 后台循环）",
      "trigger_event": "IndexACT 启动；或 BooterConfig 收到 BOOT_COMPLETED / SMS_RECEIVED / USER_PRESENT / PACKAGE_ADDED 后重新拉起",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "每 1000ms 轮询 isAccessibilityServiceEnabled(Access)；未启用且亮屏时 itoaskAccessibility++、start_Q++；未启用时把循环间隔固定为 1000ms，启用后才放慢到 8000ms",
      "user_action_requested": "无",
      "code_anchor": "com.example.mmm.Services.srvWhileWorker.onHandleIntent"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.example.mmm.Services.srvToaskAccessibility（Toast 催促）",
      "trigger_event": "activityAccessibilityVisible==\"1\" 且 itoaskAccessibility>=4（即用户已在弹窗点过确定但仍未启用）",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Enable Test Service",
      "shown_text_zh": "启用 Test Service（多语言表 localeForAccessibility：en=Enable、zh=启用、de=Aktivieren 等，拼接 \" \" + \"Test Service\"）",
      "user_action_requested": "无按钮，仅屏幕中央 Toast 持续催促",
      "code_anchor": "com.example.mmm.Services.srvToaskAccessibility.onStartCommand；com.example.mmm.defines#localeForAccessibility"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "com.example.mmm.Main.AccessActivity + AlertDialog（R$style.FullScreenDialog）",
      "trigger_event": "srvWhileWorker 中 start_Q>=6 且 accessactivity==false → startActivity(FLAG_ACTIVITY_NEW_TASK|SINGLE_TOP|CLEAR_TASK)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Title: test（utl.getLabelApplication 小写代入 APPNAME）\nMessage: \"Please enable accessibility permissions to use test:\nSelect Downloaded apps → test → allow\"\nButton: \"OK\"\n中文资源: \"请开启辅助功能权限，以便于使用 {APPNAME} 功能:\" / \"确定\"",
      "shown_text_zh": "标题为应用自身名称 test；正文要求\"请开启辅助功能权限以便使用 test：选择 已下载的应用 → test → 允许\"；唯一按钮\"确定/OK\"",
      "user_action_requested": "只能点\"确定\"；无取消、无跳过、无关闭按钮，返回键/HOME 键/菜单键被 onKeyDown 返回 true 吞掉",
      "code_anchor": "com.example.mmm.Main.AccessActivity.showPopup；com.example.mmm.Main.AccessActivity.onKeyDown；res/values/strings.xml（dialog_message / dialog_ok）；res/layout/popup.xml"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（已下载的服务列表）",
      "trigger_event": "弹窗\"确定\"按钮 onClick；或 WebView 侧 JavascriptInterface returnResult()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用不注入任何文案，依赖系统页原样显示 \"Test Service\"）",
      "shown_text_zh": "用户被直接丢到系统无障碍服务列表，需自行找到 \"Test Service\" 并打开开关",
      "user_action_requested": "在系统列表中找到 Test Service 并手动启用；若未启用则 isAccessibilityServiceEnabled 仍为 false，弹窗下次照常出现",
      "code_anchor": "com.example.mmm.Main.AccessActivity$1.onClick；com.example.mmm.Main.AccessActivity$WebAppInterface.returnResult"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "srvWhileWorker 再次拉起 AccessActivity",
      "trigger_event": "用户返回/放弃后，后台循环继续计数，start_Q 重新累计到 6 即再次拉起；accessactivity 标志仅在拉起瞬间置真，进程重启后复位",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "同上 dialog_message",
      "shown_text_zh": "同一不可取消弹窗再次出现，直到用户在系统设置中真正启用服务",
      "user_action_requested": "再次只能点\"确定\"",
      "code_anchor": "com.example.mmm.Services.srvWhileWorker.onHandleIntent"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.example.mmm.Services.Access（无障碍服务，label \"Test Service\"）",
      "trigger_event": "TYPE_WINDOW_STATE_CHANGED；包名 com.android.packageinstaller 或类名 com.android.settings.applications.InstalledAppDetailsTop",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Log.d(TAG_LOG, \"antiuninstall clicked: \" + \"android:id/button2\")",
      "shown_text_zh": "在卸载/安装确认界面自动点击 button2（取消卸载），在应用详情页检测到自身应用名时执行 performGlobalAction(1)=GLOBAL_ACTION_BACK 将用户退出该页，阻止停用无障碍或卸载",
      "user_action_requested": "用户无法完成撤权或卸载操作",
      "code_anchor": "com.example.mmm.Services.Access.onAccessibilityEvent；res/xml/serviceconfig.xml"
    }
  ],
  "text_presentation_locations": [
    "AccessActivity 全屏不可取消 AlertDialog（R$style.FullScreenDialog）：标题为应用 label \"test\"，正文为 dialog_message 把 {APPNAME} 替换为 \"test\"",
    "res/layout/popup.xml：visibility=invisible 的全屏空 FrameLayout，仅作 Activity 载体，不承载任何文字",
    "res/values/strings.xml 的 dialog_message / dialog_ok（含 en、de、zh 三套本地化）",
    "com.example.mmm.defines#localeForAccessibility 多语言 JSON 表 + strAccessbilityService=\"Test Service\" 拼成的居中 Toast（\"Enable Test Service\"）",
    "系统无障碍服务列表：服务 label=\"Test Service\"，无 android:description 说明文字",
    "系统设置页 android.settings.ACCESSIBILITY_SETTINGS 原样展示，应用不叠加自定义文字"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please enable accessibility permissions to use {APPNAME}:\nSelect Downloaded apps → {APPNAME} → allow",
      "text_zh": "请开启无障碍权限以便使用 {APPNAME}：选择\"已下载的应用\" → {APPNAME} → 允许",
      "source_location": "res/values/strings.xml → string/dialog_message",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "请开启辅助功能权限，以便于使用 {APPNAME} 功能:",
      "text_zh": "请开启辅助功能权限，以便于使用 {APPNAME} 功能：",
      "source_location": "res/values-zh/strings.xml → string/dialog_message",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "de",
      "text_verbatim": "Bitte Aktiviere die Bedienungshilfen um {APPNAME} zu benutzen:",
      "text_zh": "请启用辅助功能以便使用 {APPNAME}：",
      "source_location": "res/values-de/strings.xml → string/dialog_message",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "OK",
      "text_zh": "确定",
      "source_location": "res/values/strings.xml → string/dialog_ok",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Test Service",
      "text_zh": "启用 Test Service",
      "source_location": "com.example.mmm.defines#localeForAccessibility + string_64(\" \") + strAccessbilityService(\"Test Service\")，由 srvToaskAccessibility.onStartCommand 拼接",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Test Service",
      "text_zh": "Test Service（测试服务）",
      "source_location": "AndroidManifest.xml → service com.example.mmm.Services.Access 的 android:label；com.example.mmm.defines#strAccessbilityService",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "srvWhileWorker 的 while(true) 每 1000ms 复查 isAccessibilityServiceEnabled，未启用且亮屏时 start_Q 持续累加，达到 6 即再次 startActivity(AccessActivity) 并复位计数；同时 itoaskAccessibility 达到 4 就拉起 srvToaskAccessibility 弹 Toast。用户点\"确定\"后写 activityAccessibilityVisible=1 使 Toast 催促生效；返回/关闭弹窗不会终止循环，仅进程被杀或服务启用才停止。",
    "overlay_or_fake_settings": "无高仿系统页，也不使用 SYSTEM_ALERT_WINDOW 遮罩；以 Theme.FullScreenDialog 的系统 AlertDialog + 不可见全屏 FrameLayout 充当\"全屏引导层\"，视觉上覆盖整个屏幕。",
    "restricted_settings_13plus_coaching": "有，dialog_message 明示 \"Select Downloaded apps → {APPNAME} → allow\"（选择\"已下载的应用\"再允许），即 Android 13+ 受限设置的分步教学；未使用 Session 安装器绕过。",
    "post_grant_anti_removal": "Access.onAccessibilityEvent 在 com.android.packageinstaller 窗口点击 android:id/button2（卸载确认/取消按钮，日志 antiuninstall clicked）；在 com.android.settings.applications.InstalledAppDetailsTop 检测到自身应用名时 performGlobalAction(1)（GLOBAL_ACTION_BACK）把用户退出应用详情页；srvWhileWorker 在 killApplication 命中自身且无障碍已启用时写 autoClick=1 并移除设备管理器。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 com.example.mmm.Main.AccessActivity 进入前台（其主题为 FullScreenDialog 且布局不可见），或 Activity 启动后 500–1500ms 内出现 AlertDialog 窗口；随后 1–3s 内若前台切换到 com.android.settings 的 ACCESSIBILITY_SETTINGS 即命中完整链路。另可监测 srvToaskAccessibility 产生的 \"Enable Test Service\" Toast 作为弱信号。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "包名 com.framull.test 的 Activity com.example.mmm.Main.AccessActivity + 系统 AlertDialog 窗口；标题与正文均为 \"test\"",
        "why_most_useful": "这是应用唯一向用户告知无障碍用途的界面，可直接判定告知是否充分、是否可取消、是否屏蔽返回键",
        "observable_utg_signals": [
          "弹窗仅存在 1 个按钮（确定/OK），无取消/关闭/跳过",
          "标题与正文均为应用自身名 test，无功能说明与隐私承诺",
          "按 BACK 后弹窗仍在前台（onKeyDown 返回 true）",
          "弹窗背后无任何可见 Activity 内容（popup.xml 为空不可见 FrameLayout）"
        ]
      },
      {
        "page_role": "跳转后系统无障碍服务列表项",
        "page_identifier": "com.android.settings 的 ACCESSIBILITY_SETTINGS，列表中服务名为 \"Test Service\"，无 description 摘要",
        "why_most_useful": "核对系统侧呈现的服务身份与描述缺失，验证身份与功能不匹配、无告知说明",
        "observable_utg_signals": [
          "服务名称仅为 \"Test Service\"",
          "条目下方无任何功能说明文字",
          "开关初始为关闭状态"
        ]
      },
      {
        "page_role": "拒权返回后的循环拉起页",
        "page_identifier": "再次出现的 com.example.mmm.Main.AccessActivity 弹窗；间隔约 6–8 秒",
        "why_most_useful": "证明诱导为强制循环而非一次性提示，是判定\"拒权反馈循环\"的关键",
        "observable_utg_signals": [
          "同一弹窗文本在用户退出后重复出现",
          "出现次数随时间线性增长",
          "期间夹杂 \"Enable Test Service\" Toast"
        ]
      },
      {
        "page_role": "获权后压栈遮罩/反撤权页",
        "page_identifier": "com.android.settings 的 InstalledAppDetailsTop 被立即 BACK 退出；com.android.packageinstaller 的卸载确认按钮被自动点击",
        "why_most_useful": "验证获权后的反移除与阻止撤权行为，是权限维持的直接运行证据",
        "observable_utg_signals": [
          "打开应用详情页后 1 秒内自动返回上一级",
          "卸载确认对话框中\"取消\"按钮被自动点击",
          "无障碍开关被用户关闭后再次被拉起引导"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导文案为纯文本，UTG 可直接提取。需注意两点：一是 LAUNCHER 入口 IndexACT 立即 finish，若检测器以\"前台 Activity 停留时长\"为判据可能漏抓冷启动瞬间，建议以 Activity 生命周期回调而非画面停留判定；二是引导由后台 IntentService 定时驱动，若后台服务未启动（如缺少 BooterConfig 广播或进程被限制）则弹窗不会出现，此时应手动触发 BOOT_COMPLETED 或直接 am start 该 LAUNCHER 入口以恢复链路。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.example.mmm.Services.srvWhileWorker.onHandleIntent",
    "com.example.mmm.Main.AccessActivity.showPopup",
    "com.example.mmm.Main.AccessActivity.onKeyDown",
    "com.example.mmm.Main.AccessActivity$1.onClick",
    "com.example.mmm.Services.Access.onAccessibilityEvent",
    "res/values/strings.xml（dialog_message / dialog_ok）"
  ]
}
```

</details>

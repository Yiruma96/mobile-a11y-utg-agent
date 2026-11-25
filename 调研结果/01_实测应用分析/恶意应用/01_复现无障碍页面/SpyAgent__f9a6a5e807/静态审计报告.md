# MR_064__f9a6a5e807｜SpyAgent — Google Play Service

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：99.3s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即用不可取消的原生 AlertDialog 以“Google Play Service”名义要求开启无障碍，点 Ok 直接 startActivity 跳到系统无障碍设置页，获权后无障碍服务记录全设备界面文本与按键，并在用户离开时禁用自身 Launcher 组件隐藏入口。
- **静态可见性说明**：全部引导逻辑（检测、弹窗、跳转、伪装文案、获权后事件采集）均在 classes.dex 明文中，无加壳、无加密载荷、无远端 HTML 或 WebView，纯原生 Dialog + 系统设置页跳转，可完整静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `f9a6a5e807c2567395f2f892058b80f2e47f022c80ee1a3608b7168f30187616` |
| 包名 / 年份 | `sops.system.android.updater` / 2018 |
| 家族 / 品类 | **SpyAgent**（同池样本数：12） |
| 原始来源标识 | https://ti.360.net/blog/articles/analysis-of-donot-andriod-sample/ |
| 桌面显示名 | Google Play Service |
| 引导页宣称品牌/身份 | Google Play Service（伪造 Google 官方系统服务） |
| 系统无障碍列表服务名 | Google Play Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名伪装为 sops.system.android.updater（伪系统更新）；无障碍服务 label 与 description 均复用 @string/app_name=“Google Play Service”，使系统无障碍列表项自带诱骗文案；弹窗背后布局伪造“Your Device is not Supported as of now.”/“Application is now Uninstalling.”两句假系统提示；退出时 setComponentEnabledSetting(...,2,1) 禁用 MainActivity 并广播 UNINSTALL_SHORTCUT 删除桌面图标；无空白/换行挤出警告、无同形字、无多 activity-alias、无伪造 isAccessibilityTool（targetSdk 22，该属性不适用）。 |
| 无障碍服务类名 | `sops.system.android.updater.nine.ninere` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Google Play Service |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | sops.system.android.updater.MainActivity（theme=@style/Theme.AppCompat.Dialog，LAUNCHER 入口） | onCreate()：setContentView(R.layout.activity_main) 后立即执行 | 原生Activity | **原文**：Your Device is not Supported as of now. / Application is now Uninstalling. / Ok<br>**译注**：“您的设备目前不受支持。”／“应用正在卸载中。”／“确定”——伪造系统不兼容与卸载提示作为弹窗背景。 | 无明确请求，仅作为诱导弹窗的伪装背景；右下 Ok 按钮点击后 removeShortcut() + onBackPressed() 直接退出。 | `MainActivity.onCreate / MainActivity$1.onClick / res/layout/activity_main.xml` |
| 2 | 引导说明页（权限检测与弹窗） | MainActivity 内 AlertDialog.Builder 弹出对话框 | onCreate 中 isAccessibilitySettingsOn(getApplicationContext()) 返回 false 时 | 原生Dialog | **原文**：Please enable 'Accessibility' for 'Google Play Service' to get this working. Tap on 'Ok' to go to Accessibility Settings.<br>**译注**：请为“Google Play Service”开启“无障碍”功能以使其正常工作。点击“确定”前往无障碍设置。 | 只能点击唯一的 “Ok” 按钮前往无障碍设置；setCancelable(false)，无取消、无跳过、无稍后。 | `MainActivity.onCreate（builder1.setMessage / setCancelable(false) / setPositiveButton("Ok", MainActivity$2)）` |
| 3 | 跳无障碍设置 | 系统 Settings.ACTION_ACCESSIBILITY_SETTINGS 无障碍服务列表页 | MainActivity$2.onClick(dialog, which) 回调 | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS<br>**译注**：系统无障碍设置页，列表中出现名为 “Google Play Service” 的服务项（description 同为该文案），用户需手动找到并打开其开关。 | 在系统无障碍列表中手动找到 “Google Play Service” 并拨开开关；应用侧无任何额外引导遮罩或分步教学。 | `MainActivity$2.onClick（startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))）` |
| 4 | 获权后动作 | sops.system.android.updater.nine.ninere（AccessibilityService，BIND_ACCESSIBILITY_SERVICE） | 系统回调 onServiceConnected() 初始化 MD5/日志列表；随后 onAccessibilityEvent() 在 ten.fg.klog.wm 为 true 时处理事件 | 不可静态还原 | **原文**：无（后台无界面；采集 event.getText() 与 event.getPackageName()）<br>**译注**：无界面呈现，静默采集：TYPE_VIEW_TEXT_CHANGED(16) 记录输入文本与时间戳、TYPE_WINDOW_STATE_CHANGED(32)/WINDOW_CONTENT_CHANGED(2048) 记录包名，并启动 ninere$keyclass 线程持续记录。 | 无（用户无需再操作，服务常驻后台）。 | `ninere.onServiceConnected / ninere.onAccessibilityEvent / res/xml/accessibility.xml(canRetrieveWindowContent=true)` |
| 5 | 拒权反馈循环（实为自隐藏） | MainActivity 组件自身 + 桌面快捷方式 | onBackPressed() / 布局 Ok 按钮点击 / onDestroy() | 通知栏（UNINSTALL_SHORTCUT 广播） | **原文**：ServiceUpdate<br>**译注**：通过 com.android.launcher.action.UNINSTALL_SHORTCUT 广播移除名为 “ServiceUpdate” 的桌面图标，并禁用 MainActivity 组件。 | 无；用户返回或退出后入口消失，不会再次弹窗重试，也不会死循环重跳。 | `MainActivity.removeShortcut（setComponentEnabledSetting(getComponentName(),2,1) + UNINSTALL_SHORTCUT）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 冷启动即弹出的 AlertDialog（setCancelable(false)，仅 Ok 按钮）：正文为 “Please enable 'Accessibility' for 'Google Play Service' to get this working. Tap on 'Ok' to go to Accessibility Settings.”
- 弹窗背后的 MainActivity 窗口（theme=@style/Theme.AppCompat.Dialog，布局 res/layout/activity_main.xml 硬编码）：textView=“Your Device is not Supported as of now.”，textView2=“Application is now Uninstalling.”，button=“Ok”
- 系统无障碍服务列表项：service android:label=@string/app_name，android:description=@string/app_name，二者均解析为 “Google Play Service”（res/values/strings.xml 第19行，经 res/xml/accessibility.xml 引用）
- 桌面图标名：application android:label=@string/app_name → “Google Play Service”；被移除的旧快捷方式名为 “ServiceUpdate”（removeShortcut 中硬编码）
- 未使用任何本地/远端 HTML WebView、GIF/图片引导或悬浮窗遮罩，全部引导文字均为原生控件硬编码或 strings.xml

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please enable 'Accessibility' for 'Google Play Service' to get this working. Tap on 'Ok' to go to Accessibility Settings. | 请为“Google Play Service”开启“无障碍”以使其正常工作。点击“确定”前往无障碍设置。 | `MainActivity.onCreate 硬编码字符串（AlertDialog.Builder.setMessage）` | 教唆忽视警告 |
| en | Your Device is not Supported as of now. | 您的设备目前不受支持。 | `res/layout/activity_main.xml textView` | 故障恐吓 |
| en | Application is now Uninstalling. | 应用正在卸载中。 | `res/layout/activity_main.xml textView2` | 故障恐吓 |
| en | Google Play Service | Google Play 服务（伪造的 Google 官方品牌名） | `res/values/strings.xml app_name（被 manifest application android:label、service android:label 与 accessibility.xml android:description 共用）` | 假更新 |
| en | Ok | 确定 | `MainActivity.onCreate setPositiveButton("Ok")；res/layout/activity_main.xml button` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无死循环：onCreate 只检测一次，用户从系统无障碍页返回时不重跳（未重写 onResume，onResume 为空实现）；但用户一旦返回/退出，onBackPressed 与 onDestroy 会触发 removeShortcut() 禁用 MainActivity 组件并删除桌面图标，使入口不可再次进入，服务与 ten IntentService 仍在后台运行。
- **遮罩叠层 / 高仿系统设置页**：无悬浮窗/半透明遮罩，也无高仿系统无障碍开关页；但用 theme=@style/Theme.AppCompat.Dialog 让主界面本身就是对话框形态，并在其背景布局伪造“设备不受支持/正在卸载”两句假系统提示。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无主动自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；但通过 setComponentEnabledSetting(MainActivity, DISABLED) + UNINSTALL_SHORTCUT 广播隐藏自身入口，并配合 ten.setseral/setalrm 等定时保活，使用户难以找到并关闭该服务。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：Hook Activity.startActivity / Context.startActivity，当 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS 且调用方包名为 sops.system.android.updater 时立即开始 UTG 录制；次选钩子为 MainActivity onCreate 后首帧出现仅含“Ok”单按钮的不可取消 AlertDialog 时。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本样本无显著盲区：引导全流程为原生文本控件，UTG 可直接取文本，无需 OCR。潜在盲区在于获权后完全无 UI（纯后台服务采集），UTG 只能依靠无障碍事件与网络流量侧观测；此外 targetSdk 22 下 Android 13+ 受限设置不适用，若在 13+ 设备上运行可能因权限模型差异导致无障碍开关不可用，需在设备侧确认实际可达性。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（含背景伪造系统提示）** | sops.system.android.updater.MainActivity，对话框正文含 “Please enable 'Accessibility' for 'Google Play Service'”，单一 “Ok” 按钮且无取消键；背景含 “Your Device is not Supported as of now.” | 这是诱导链条的唯一入口，可直接证明“零业务前置 + 不可取消 + 品牌冒充”三要素，且弹窗与背景伪造文案同屏出现，一帧即可定性质。 | 弹窗正文是否出现 Google Play Service 与 Accessibility 关键词；按钮集合仅含 Ok、不存在 Cancel/Skip/Not now；背景 TextView 是否出现 not Supported / Uninstalling 伪造系统文案；出现时机是否为 LAUNCHER 冷启动首帧（无任何业务操作前置） |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中 label 与 description 均为 “Google Play Service” 的服务条目 | 验证伪装文案确实落地到系统 UI（服务说明本身就是诱骗话术），并确认用户被引导到的是全局无障碍开关而非普通权限页。 | 服务项文案为 Google Play Service 但包名为 sops.system.android.updater；description 与实际能力（读取窗口内容）明显不符；开关由关到开的状态变化时间点，可作为获权时刻锚点 |
| **获权后返回/退出的入口消失表现** | 退出 MainActivity 后桌面图标消失、再次点击原图标无法进入（组件已 DISABLED） | 佐证 anti-removal/自隐藏设计，说明用户事后难以回溯并关闭已授予的无障碍权限。 | UNINSTALL_SHORTCUT 广播与 Launcher 图标消失事件；MainActivity 组件状态变为 disabled（pm dump / dumpsys package）；无障碍服务仍处于 enabled 而前台无任何入口界面 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `sops.system.android.updater.MainActivity.onCreate`
- `sops.system.android.updater.MainActivity.isAccessibilitySettingsOn`
- `sops.system.android.updater.MainActivity$2.onClick`
- `sops.system.android.updater.MainActivity.removeShortcut`
- `sops.system.android.updater.nine.ninere.onAccessibilityEvent`
- `res/xml/accessibility.xml（android:description=@string/app_name, canRetrieveWindowContent=true）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（运行期 UTG 视角的无障碍引导链路）

- **静态可见性完整**：无加壳、无加密载荷、无远端 HTML，整条引导链均在 `classes.dex` 明文可见，可 100% 静态还原。
- **纯冷启动 0 步触发**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:sops.system.android.updater.MainActivity#onCreate>) 里先 `setContentView`，紧接着调用 [isAccessibilitySettingsOn()](<resource-unit:#1.dex1 code:sops.system.android.updater.MainActivity#isAccessibilitySettingsOn>) 直接读 `Settings.Secure.accessibility_enabled` / `enabled_accessibility_services`，未授权即弹窗——没有任何业务功能前置，也没有二次确认。
- **不可取消的原生 AlertDialog**：`setCancelable(false)`，只有 "Ok" 一个按钮，无取消/跳过/稍后；文案自称 "Google Play Service" 要求开启无障碍。
- **一键直达系统无障碍页**：[MainActivity$2.onClick()](<resource-unit:#1.dex1 code:sops.system.android.updater.MainActivity$2#onClick>) 执行 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`；**未发现** `ACTION_APPLICATION_DETAILS_SETTINGS`、也没有 Android 13+ 受限设置（右上角菜单）分步教学，故 `JUMP_A11Y_SETTINGS` 即唯一跳转点。
- **背景假系统提示页**：弹窗背后 Activity 用 `Theme.AppCompat.Dialog`，布局 [activity_main.xml](<resource-unit:#1 file:res/layout/activity_main.xml>) 写着 "Your Device is not Supported as of now." / "Application is now Uninstalling."，把"开权限"包装成系统不兼容/卸载流程。
- **身份三重伪装**：`app_name`（[strings.xml L19](<resource-unit:#1 file:res/values/strings.xml#L19>)）、无障碍 `android:label`、`android:description`（[accessibility.xml](<resource-unit:#1 file:res/xml/accessibility.xml>)）全部为 "Google Play Service"，系统无障碍列表中显示项本身就是伪装文案，属"文案自带诱骗"，不依赖弹窗。
- **无拒绝循环但有自隐藏**：没有 onResume 死循环重跳、没有悬浮遮罩、没有获权后自点确认；但 [removeShortcut()](<resource-unit:#1.dex1 code:sops.system.android.updater.MainActivity#removeShortcut>) 会 `setComponentEnabledSetting(getComponentName(), 2, 1)` 禁用 MainActivity 并发 `UNINSTALL_SHORTCUT` 广播，用户一离开引导页桌面图标与入口即消失，只剩无障碍服务常驻（隐性 anti-removal/规避痕迹）。
- **获权后落地**：[ninere.onAccessibilityEvent()](<resource-unit:#1.dex1 code:sops.system.android.updater.nine.ninere#onAccessibilityEvent>) 在 `ten.fg.klog.wm` 打开时采集 `TYPE_VIEW_TEXT_CHANGED / WINDOW_STATE_CHANGED / WINDOW_CONTENT_CHANGED` 的包名+文本+时间戳并起 `ninere$keyclass` 线程，是键盘记录/界面窃取，与"Google Play Service"说明完全不符。
- **UTG 采集建议**：最佳钩子是 `startActivity` 的 intent action 命中 `android.settings.ACCESSIBILITY_SETTINGS`（或 MainActivity 首帧出现无取消按钮 Dialog），抓"冷启动弹窗页 + 跳转后系统无障碍列表项（label 为 Google Play Service）"两页即可闭环。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑（检测、弹窗、跳转、伪装文案、获权后事件采集）均在 classes.dex 明文中，无加壳、无加密载荷、无远端 HTML 或 WebView，纯原生 Dialog + 系统设置页跳转，可完整静态还原。",
  "summary_one_liner": "冷启动即用不可取消的原生 AlertDialog 以“Google Play Service”名义要求开启无障碍，点 Ok 直接 startActivity 跳到系统无障碍设置页，获权后无障碍服务记录全设备界面文本与按键，并在用户离开时禁用自身 Launcher 组件隐藏入口。",
  "disguise_identity": {
    "app_display_name": "Google Play Service",
    "claimed_brand_or_persona": "Google Play Service（伪造 Google 官方系统服务）",
    "a11y_service_label": "Google Play Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名伪装为 sops.system.android.updater（伪系统更新）；无障碍服务 label 与 description 均复用 @string/app_name=“Google Play Service”，使系统无障碍列表项自带诱骗文案；弹窗背后布局伪造“Your Device is not Supported as of now.”/“Application is now Uninstalling.”两句假系统提示；退出时 setComponentEnabledSetting(...,2,1) 禁用 MainActivity 并广播 UNINSTALL_SHORTCUT 删除桌面图标；无空白/换行挤出警告、无同形字、无多 activity-alias、无伪造 isAccessibilityTool（targetSdk 22，该属性不适用）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "sops.system.android.updater.MainActivity（theme=@style/Theme.AppCompat.Dialog，LAUNCHER 入口）",
      "trigger_event": "onCreate()：setContentView(R.layout.activity_main) 后立即执行",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Your Device is not Supported as of now. / Application is now Uninstalling. / Ok",
      "shown_text_zh": "“您的设备目前不受支持。”／“应用正在卸载中。”／“确定”——伪造系统不兼容与卸载提示作为弹窗背景。",
      "user_action_requested": "无明确请求，仅作为诱导弹窗的伪装背景；右下 Ok 按钮点击后 removeShortcut() + onBackPressed() 直接退出。",
      "code_anchor": "MainActivity.onCreate / MainActivity$1.onClick / res/layout/activity_main.xml"
    },
    {
      "step": 2,
      "stage": "引导说明页（权限检测与弹窗）",
      "screen_or_component": "MainActivity 内 AlertDialog.Builder 弹出对话框",
      "trigger_event": "onCreate 中 isAccessibilitySettingsOn(getApplicationContext()) 返回 false 时",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Please enable 'Accessibility' for 'Google Play Service' to get this working. Tap on 'Ok' to go to Accessibility Settings.",
      "shown_text_zh": "请为“Google Play Service”开启“无障碍”功能以使其正常工作。点击“确定”前往无障碍设置。",
      "user_action_requested": "只能点击唯一的 “Ok” 按钮前往无障碍设置；setCancelable(false)，无取消、无跳过、无稍后。",
      "code_anchor": "MainActivity.onCreate（builder1.setMessage / setCancelable(false) / setPositiveButton(\"Ok\", MainActivity$2)）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统 Settings.ACTION_ACCESSIBILITY_SETTINGS 无障碍服务列表页",
      "trigger_event": "MainActivity$2.onClick(dialog, which) 回调",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "shown_text_zh": "系统无障碍设置页，列表中出现名为 “Google Play Service” 的服务项（description 同为该文案），用户需手动找到并打开其开关。",
      "user_action_requested": "在系统无障碍列表中手动找到 “Google Play Service” 并拨开开关；应用侧无任何额外引导遮罩或分步教学。",
      "code_anchor": "MainActivity$2.onClick（startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))）"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "sops.system.android.updater.nine.ninere（AccessibilityService，BIND_ACCESSIBILITY_SERVICE）",
      "trigger_event": "系统回调 onServiceConnected() 初始化 MD5/日志列表；随后 onAccessibilityEvent() 在 ten.fg.klog.wm 为 true 时处理事件",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（后台无界面；采集 event.getText() 与 event.getPackageName()）",
      "shown_text_zh": "无界面呈现，静默采集：TYPE_VIEW_TEXT_CHANGED(16) 记录输入文本与时间戳、TYPE_WINDOW_STATE_CHANGED(32)/WINDOW_CONTENT_CHANGED(2048) 记录包名，并启动 ninere$keyclass 线程持续记录。",
      "user_action_requested": "无（用户无需再操作，服务常驻后台）。",
      "code_anchor": "ninere.onServiceConnected / ninere.onAccessibilityEvent / res/xml/accessibility.xml(canRetrieveWindowContent=true)"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环（实为自隐藏）",
      "screen_or_component": "MainActivity 组件自身 + 桌面快捷方式",
      "trigger_event": "onBackPressed() / 布局 Ok 按钮点击 / onDestroy()",
      "ui_carrier": "通知栏（UNINSTALL_SHORTCUT 广播）",
      "shown_text_verbatim": "ServiceUpdate",
      "shown_text_zh": "通过 com.android.launcher.action.UNINSTALL_SHORTCUT 广播移除名为 “ServiceUpdate” 的桌面图标，并禁用 MainActivity 组件。",
      "user_action_requested": "无；用户返回或退出后入口消失，不会再次弹窗重试，也不会死循环重跳。",
      "code_anchor": "MainActivity.removeShortcut（setComponentEnabledSetting(getComponentName(),2,1) + UNINSTALL_SHORTCUT）"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 冷启动即弹出的 AlertDialog（setCancelable(false)，仅 Ok 按钮）：正文为 “Please enable 'Accessibility' for 'Google Play Service' to get this working. Tap on 'Ok' to go to Accessibility Settings.”",
    "弹窗背后的 MainActivity 窗口（theme=@style/Theme.AppCompat.Dialog，布局 res/layout/activity_main.xml 硬编码）：textView=“Your Device is not Supported as of now.”，textView2=“Application is now Uninstalling.”，button=“Ok”",
    "系统无障碍服务列表项：service android:label=@string/app_name，android:description=@string/app_name，二者均解析为 “Google Play Service”（res/values/strings.xml 第19行，经 res/xml/accessibility.xml 引用）",
    "桌面图标名：application android:label=@string/app_name → “Google Play Service”；被移除的旧快捷方式名为 “ServiceUpdate”（removeShortcut 中硬编码）",
    "未使用任何本地/远端 HTML WebView、GIF/图片引导或悬浮窗遮罩，全部引导文字均为原生控件硬编码或 strings.xml"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please enable 'Accessibility' for 'Google Play Service' to get this working. Tap on 'Ok' to go to Accessibility Settings.",
      "text_zh": "请为“Google Play Service”开启“无障碍”以使其正常工作。点击“确定”前往无障碍设置。",
      "source_location": "MainActivity.onCreate 硬编码字符串（AlertDialog.Builder.setMessage）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Your Device is not Supported as of now.",
      "text_zh": "您的设备目前不受支持。",
      "source_location": "res/layout/activity_main.xml textView",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Application is now Uninstalling.",
      "text_zh": "应用正在卸载中。",
      "source_location": "res/layout/activity_main.xml textView2",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Play Service",
      "text_zh": "Google Play 服务（伪造的 Google 官方品牌名）",
      "source_location": "res/values/strings.xml app_name（被 manifest application android:label、service android:label 与 accessibility.xml android:description 共用）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Ok",
      "text_zh": "确定",
      "source_location": "MainActivity.onCreate setPositiveButton(\"Ok\")；res/layout/activity_main.xml button",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无死循环：onCreate 只检测一次，用户从系统无障碍页返回时不重跳（未重写 onResume，onResume 为空实现）；但用户一旦返回/退出，onBackPressed 与 onDestroy 会触发 removeShortcut() 禁用 MainActivity 组件并删除桌面图标，使入口不可再次进入，服务与 ten IntentService 仍在后台运行。",
    "overlay_or_fake_settings": "无悬浮窗/半透明遮罩，也无高仿系统无障碍开关页；但用 theme=@style/Theme.AppCompat.Dialog 让主界面本身就是对话框形态，并在其背景布局伪造“设备不受支持/正在卸载”两句假系统提示。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无主动自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；但通过 setComponentEnabledSetting(MainActivity, DISABLED) + UNINSTALL_SHORTCUT 广播隐藏自身入口，并配合 ten.setseral/setalrm 等定时保活，使用户难以找到并关闭该服务。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "Hook Activity.startActivity / Context.startActivity，当 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS 且调用方包名为 sops.system.android.updater 时立即开始 UTG 录制；次选钩子为 MainActivity onCreate 后首帧出现仅含“Ok”单按钮的不可取消 AlertDialog 时。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（含背景伪造系统提示）",
        "page_identifier": "sops.system.android.updater.MainActivity，对话框正文含 “Please enable 'Accessibility' for 'Google Play Service'”，单一 “Ok” 按钮且无取消键；背景含 “Your Device is not Supported as of now.”",
        "why_most_useful": "这是诱导链条的唯一入口，可直接证明“零业务前置 + 不可取消 + 品牌冒充”三要素，且弹窗与背景伪造文案同屏出现，一帧即可定性质。",
        "observable_utg_signals": [
          "弹窗正文是否出现 Google Play Service 与 Accessibility 关键词",
          "按钮集合仅含 Ok、不存在 Cancel/Skip/Not now",
          "背景 TextView 是否出现 not Supported / Uninstalling 伪造系统文案",
          "出现时机是否为 LAUNCHER 冷启动首帧（无任何业务操作前置）"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中 label 与 description 均为 “Google Play Service” 的服务条目",
        "why_most_useful": "验证伪装文案确实落地到系统 UI（服务说明本身就是诱骗话术），并确认用户被引导到的是全局无障碍开关而非普通权限页。",
        "observable_utg_signals": [
          "服务项文案为 Google Play Service 但包名为 sops.system.android.updater",
          "description 与实际能力（读取窗口内容）明显不符",
          "开关由关到开的状态变化时间点，可作为获权时刻锚点"
        ]
      },
      {
        "page_role": "获权后返回/退出的入口消失表现",
        "page_identifier": "退出 MainActivity 后桌面图标消失、再次点击原图标无法进入（组件已 DISABLED）",
        "why_most_useful": "佐证 anti-removal/自隐藏设计，说明用户事后难以回溯并关闭已授予的无障碍权限。",
        "observable_utg_signals": [
          "UNINSTALL_SHORTCUT 广播与 Launcher 图标消失事件",
          "MainActivity 组件状态变为 disabled（pm dump / dumpsys package）",
          "无障碍服务仍处于 enabled 而前台无任何入口界面"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本样本无显著盲区：引导全流程为原生文本控件，UTG 可直接取文本，无需 OCR。潜在盲区在于获权后完全无 UI（纯后台服务采集），UTG 只能依靠无障碍事件与网络流量侧观测；此外 targetSdk 22 下 Android 13+ 受限设置不适用，若在 13+ 设备上运行可能因权限模型差异导致无障碍开关不可用，需在设备侧确认实际可达性。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "sops.system.android.updater.MainActivity.onCreate",
    "sops.system.android.updater.MainActivity.isAccessibilitySettingsOn",
    "sops.system.android.updater.MainActivity$2.onClick",
    "sops.system.android.updater.MainActivity.removeShortcut",
    "sops.system.android.updater.nine.ninere.onAccessibilityEvent",
    "res/xml/accessibility.xml（android:description=@string/app_name, canRetrieveWindowContent=true）"
  ]
}
```

</details>

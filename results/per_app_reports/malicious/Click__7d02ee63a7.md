# MR_038__7d02ee63a7｜Click — QR Scanner

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：121.8s

## 1. 一句话核心结论

- **核心申请方式**：该扫码应用在扫描到 URL 二维码后按需显示“Enable Secure Scanning”开关，拨动即跳系统无障碍设置，并延迟 100ms 在其上叠加半透明“点这里”伪开关遮罩引导用户开启监听全部应用窗口的无障碍服务。
- **静态可见性说明**：DEX 未加壳，全部引导逻辑（跳转点、延时叠层、服务连接回调、strings/layout）均可静态还原；未发现远端 HTML 引导页或加密载荷参与该流程，assets/html-* 仅为 ZXing 开源帮助文档。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `7d02ee63a742a300d0fa2736aa512c12f578199333da17e2af0c7cd2d8174d54` |
| 包名 / 年份 | `qrcode.scanner.qrmaker` / 2019 |
| 家族 / 品类 | **Click**（同池样本数：2） |
| 原始来源标识 | https://gbhackers.com/clicker-trojan/ |
| 桌面显示名 | QR Scanner |
| 引导页宣称品牌/身份 | QR Scanner Secure Scanning（自称基于开源 ZXing 的正规条码扫描器，宣称用于告警可疑网站保护设备） |
| 系统无障碍列表服务名 | QR Scanner Secure Scanning |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务名以“Secure Scanning（安全扫描）”包装，实际 eventTypes=-1、packageNames 为空、canRetrieveWindowContent=true，监听所有应用窗口内容；about_ 字符串自称“About WiFiBarcode”，与 QR Scanner 品牌不一致；overlay 文案使用换行挤出式排布（"QR Scanner Secure Scanning \nOff/On"）。 |
| 无障碍服务类名 | `com.qrcode.service.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, READ_CONTACTS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Enable Accessibility to allow QR Scanner to secure your device by showing alerts on suspicious websites. The Accessibility feature allows QR Scanner to provide its services to all users. By enabling Accessbility, you Acknowledge that you have read and agree to our Terms of service and Privacy Policy. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.qrcode.ActivitySplash（LAUNCHER，Theme.Transparent）→ Open_Activity() → com.qrcode.MainActivity / com.google.zxing.client.android.CaptureActivity | ActivitySplash.onCreate() 后调用 Open_Activity() | 原生Activity | **原文**：无（启动页仅设置 QR_COLOR 后跳转，本步不弹无障碍引导）<br>**译注**：启动页不展示无障碍相关文案，仅完成初始化与跳转 | 无需操作，自动进入主界面 | `com.qrcode.ActivitySplash.onCreate` |
| 2 | 业务功能触发 | CaptureActivity 扫码页（layout/capture，含 banner 广告、tv_secure 文本、默认隐藏的 Switch toggle） | handleDecode() 识别结果为 ParsedResultType.URI 且 MyAccessibilityService.isAccessibilitySettingsOn(this) 为 false | 原生Activity | **原文**：Secure Scanning（lbl_secure_scan）<br>**译注**：扫描页显示“安全扫描”字样的开关，引导用户打开 | 要求用户拨动开关；开关默认可见但无取消/跳过说明，用户可放弃拨动 | `com.google.zxing.client.android.CaptureActivity#handleDecode + res/values/strings.xml:lbl_secure_scan` |
| 3 | 跳无障碍设置 | android.settings.ACCESSIBILITY_SETTINGS 系统无障碍设置页（startActivityForResult requestCode=1） | CaptureActivity$4.onCheckedChanged() 中 toggle.isChecked() 为 true | 系统无障碍页 | **原文**：Enable Secure Scanning<br>**译注**：系统无障碍设置页内出现条目“QR Scanner Secure Scanning”，描述为开启无障碍以告警可疑网站 | 要求用户在系统列表中点击该服务并确认开启；系统层面可返回退出 | `com.google.zxing.client.android.CaptureActivity$4#onCheckedChanged + res/values/strings.xml:access_enable / accessibility_service_description` |
| 4 | 遮罩叠层指引 | com.qrcode.ActivityOverlay（theme=Transparent，layout/activity_overlay，半透明 #703e3e3e 全屏遮罩 + click_here_on/off 箭头图 + tv_text） | startActivityForResult 之后 new Handler().postDelayed(new CaptureActivity$4$1(this), 100L) 在 100ms 后 startActivity(ActivityOverlay) | 悬浮窗Overlay | **原文**："QR Scanner Secure Scanning \nOff" / "QR Scanner Secure Scanning \nOn"<br>**译注**：遮罩上显示“QR Scanner 安全扫描 已关闭/已开启”，并叠加指向系统开关位置的“点这里”箭头图，指示用户点击哪里 | 要求用户点击遮罩/箭头处后关闭遮罩；onBackPressed() 为空实现，返回键无法退出遮罩，只能点击遮罩 finish() | `com.qrcode.ActivityOverlay#onCreate + com.qrcode.ActivityOverlay$1#onClick + res/layout/activity_overlay.xml + res/values/strings.xml:overlay_on/overlay_off` |
| 5 | 拒权反馈循环 | CaptureActivity.onActivityResult(requestCode=1) | 从系统无障碍页返回 | 原生Activity | 无 | 无强制操作；用户可再次拨动开关重复第 3–4 步 | `com.google.zxing.client.android.CaptureActivity#onActivityResult` |
| 6 | 获权后动作 | com.qrcode.service.MyAccessibilityService（BIND_ACCESSIBILITY_SERVICE，config: eventTypes=typeViewTextSelectionChanged\|typeWindowContentChanged\|typeWindowStateChanged, packageNames="", canRetrieveWindowContent=true）→ 启动 com.qrcode.MainActivity | onConnectedService() 回调（无障碍服务被系统连接） | 原生Activity | 无 | 无，全自动执行 | `com.qrcode.service.MyAccessibilityService#onConnectedService + res/xml/accessibility_service_config.xml` |
| 7 | 引导说明页（第二入口） | com.qrcode.ActivitySettings$SettingsFragment 中的 pref_access SwitchPreference | onPreferenceChange() 被触发（不论勾选或取消） | 原生Activity | **原文**：Enable Secure Scanning / Disable Secure Scanning<br>**译注**：设置页“开启/关闭安全扫描”开关项，操作后同样跳系统无障碍页并延迟弹遮罩 | 要求用户开启该项；无跳过入口（返回 false 阻止状态变更，仅触发跳转） | `com.qrcode.ActivitySettings$SettingsFragment$1#onPreferenceChange + com.qrcode.ActivitySettings$SettingsFragment#call_act` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项名称与说明：android:label=@string/accessibility_service_label（QR Scanner Secure Scanning）、android:description=@string/accessibility_service_description（res/xml/accessibility_service_config.xml 引用）
- 扫码结果页 CaptureActivity 原生布局 layout/capture 中的 tv_secure 文本与隐藏 Switch 开关（“Secure Scanning”）
- 系统无障碍设置页之上的透明叠层 ActivityOverlay（layout/activity_overlay.xml）：半透明全屏背景 + click_here_on/off 箭头图 + tv_text 文案“QR Scanner Secure Scanning On/Off”
- 设置页 ActivitySettings 的 SwitchPreference 项：Enable Secure Scanning / Disable Secure Scanning
- assets/html-de|html-* 下的 ZXing 帮助/许可/更新说明本地 HTML（HelpActivity WebView 展示，与无障碍诱导无直接关联）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable Accessibility to allow QR Scanner to secure your device by showing alerts on suspicious websites. The Accessibility feature allows QR Scanner to provide its services to all users. By enabling Accessbility, you Acknowledge that you have read and agree to our Terms of service and Privacy Policy. | 启用无障碍功能，允许 QR Scanner 通过提示可疑网站来保护你的设备安全。该无障碍功能使 QR Scanner 能够向所有用户提供服务。启用无障碍即表示你确认已阅读并同意我们的服务条款与隐私政策。 | `res/values/strings.xml:accessibility_service_description（经 res/xml/accessibility_service_config.xml 的 android:description 引用）` | 假反诈安全 |
| en | QR Scanner Secure Scanning <br>Off | QR Scanner 安全扫描 已关闭 | `res/values/strings.xml:overlay_off（ActivityOverlay tv_text 显示）` | 假反诈安全 |
| en | QR Scanner Secure Scanning <br>On | QR Scanner 安全扫描 已开启 | `res/values/strings.xml:overlay_on（ActivityOverlay tv_text 显示）` | 假反诈安全 |
| en | Enable Secure Scanning | 开启安全扫描 | `res/values/strings.xml:access_enable（扫码页开关/设置页项文案）` | 假反诈安全 |
| en | QR Scanner Secure Scanning | QR Scanner 安全扫描（系统无障碍列表显示的服务名） | `res/values/strings.xml:accessibility_service_label（AndroidManifest service android:label）` | 假反诈安全 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：未获权返回后仅执行 toggle.setChecked(false)，不重跳、无定时器强拉；用户再次拨动开关即重复“跳设置+100ms 叠层”流程，属可反复施压但非死循环。
- **遮罩叠层 / 高仿系统设置页**：是。ActivityOverlay 为透明主题全屏叠层（背景 #703e3e3e），压在系统无障碍设置页之上，用 click_here_on/click_here_off 箭头图与“QR Scanner Secure Scanning On/Off”文案模拟开关状态指引点击位置；onBackPressed() 空实现使返回键无法关闭遮罩，必须点击遮罩才 finish()。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无（onServiceInterrupt/onDestroyService 仅打日志；未监听设置页执行 GLOBAL_ACTION_BACK/HOME，未自点确认）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：Hook startActivityForResult 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（或直接监测 com.qrcode.ActivityOverlay 被 startActivity）；叠层在跳转后约 100ms 出现，建议在跳转后 150–500ms 抓取当前前台窗口。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：遮罩中的箭头图（click_here_on/off）本身为图片，需靠文本与 Activity 名判定，纯图判定可能漏；此外引导只在扫到 URL 二维码时出现，需构造 URI 二维码输入才能触发，冷启动不会直接暴露该流程。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **设置页后叠层遮罩页（最关键）** | 包名 qrcode.scanner.qrmaker 下 com.qrcode.ActivityOverlay（透明主题 Activity，全屏半透明底 + 箭头图 + “QR Scanner Secure Scanning On/Off”文本） | 这是该应用区别于普通合规扫码器的决定性证据：在系统设置页之上叠层指引点击，形成伪开关/遮罩引导。 | 前台 Activity 为 com.qrcode.ActivityOverlay 且背景 Activity 为 Settings$AccessibilitySettings；界面文本含 "QR Scanner Secure Scanning" 与 "On"/"Off"；存在图片控件 img_enable（click_here_on / click_here_off）；遮罩无取消按钮，返回键无效 |
| **系统无障碍服务列表项** | Settings → Accessibility 中条目 “QR Scanner Secure Scanning”，副标题为 security 描述文案 | 核对身份伪装与宣称范围（告警可疑网站）与实际权限（全应用窗口内容）的落差。 | 服务条目名称 QR Scanner Secure Scanning；描述文本含 "secure your device by showing alerts on suspicious websites" |
| **扫码结果页（触发前）** | com.google.zxing.client.android.CaptureActivity，含 tv_secure 文本与刚出现的 Switch 开关 | 确认引导仅在扫到 URL 结果后按需出现，属于业务功能触发而非冷启动强推。 | 扫描 URI 二维码后 Switch 由隐藏变为可见；页面含 “Secure Scanning” 文本 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.google.zxing.client.android.CaptureActivity#handleDecode`
- `com.google.zxing.client.android.CaptureActivity$4#onCheckedChanged`
- `com.google.zxing.client.android.CaptureActivity$4$1#run`
- `com.qrcode.ActivityOverlay#onCreate`
- `com.qrcode.ActivitySettings$SettingsFragment#call_act`
- `com.qrcode.service.MyAccessibilityService#onConnectedService`
- `res/xml/accessibility_service_config.xml`
- `res/layout/activity_overlay.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（UTG 页面流转视角）

- **触发时机**：扫描到 URL 二维码后才按需触发，并非冷启动就弹窗。[CaptureActivity.handleDecode()](<resource-unit:#1.dex1 code:com.google.zxing.client.android.CaptureActivity#handleDecode>) 判断结果类型为 `URI` 且 `MyAccessibilityService.isAccessibilitySettingsOn()` 为 false 时，才把隐藏的 `toggle` 开关显示出来（`setVisibility(0)`），并绑定监听。
- **受限设置跳转**：用户拨动开关后，[CaptureActivity$4.onCheckedChanged()](<resource-unit:#1.dex1 code:com.google.zxing.client.android.CaptureActivity$4#onCheckedChanged>) 直接执行 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 1)`，并在 **100ms** 后通过 `Handler.postDelayed` 弹出 [CaptureActivity$4$1.run()](<resource-unit:#1.dex1 code:com.google.zxing.client.android.CaptureActivity$4$1#run>)，拉起 `ActivityOverlay`。设置页没有 ACTION_APPLICATION_DETAILS_SETTINGS 分支，也没有 Android 13 受限设置分步教学（targetSdk 28）。
- **叠层引导（核心特征）**：[ActivityOverlay](<resource-unit:#1.dex1 code:com.qrcode.ActivityOverlay#onCreate>) 是一个透明主题 Activity，铺在系统无障碍设置页之上；布局为半透明黑底（`#703e3e3e`）加一张“点这里”箭头图（`click_here_on/off`）和文字“QR Scanner Secure Scanning On/Off”，`onBackPressed()` 为空，因此返回键无法关闭，用户必须点击遮罩，遮罩随后 `finish()`。遮罩会在用户即将点击的位置绘制伪开关指引，形成“伪设置页/遮罩叠层”效果。
- **第二个入口**：[ActivitySettings$SettingsFragment$1.onPreferenceChange()](<resource-unit:#1.dex1 code:com.qrcode.ActivitySettings$SettingsFragment$1#onPreferenceChange>) 无论开关状态如何都返回 false，并调用 [call_act()](<resource-unit:#1.dex1 code:com.qrcode.ActivitySettings$SettingsFragment#call_act>)，执行同一套“跳设置 + 100ms 叠层”，并额外把 `isAccessibilitySettingsOn` 结果放进 `TAG_OVERLAY`。
- **拒权反馈**：`onActivityResult(1)` 中如果未获权，仅执行 `toggle.setChecked(false)`，没有重跳循环，也没有定时器强制拉起；用户再次拨动开关会重复同一流程。
- **获权后动作**：[MyAccessibilityService.onConnectedService()](<resource-unit:#1.dex1 code:com.qrcode.service.MyAccessibilityService#onConnectedService>) 立即启动 `MainActivity`，并把 `AccessibilityServiceInfo.eventTypes` 设为 `-1`（全事件）、`notificationTimeout=100`；配置为 `packageNames=""`、`canRetrieveWindowContent="true"`，即监听全部应用窗口内容，远超“扫描时提示可疑网站”的宣称范围。
- **身份与文案**：桌面名 `QR Scanner`，无障碍列表名“QR Scanner Secure Scanning”，描述用“安全防护/可疑网站告警 + 隐私政策承诺”包装，属于典型的假反诈安全诱导；`about_` 字符串又自称“About WiFiBarcode”，品牌口径混乱。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳，全部引导逻辑（跳转点、延时叠层、服务连接回调、strings/layout）均可静态还原；未发现远端 HTML 引导页或加密载荷参与该流程，assets/html-* 仅为 ZXing 开源帮助文档。",
  "summary_one_liner": "该扫码应用在扫描到 URL 二维码后按需显示“Enable Secure Scanning”开关，拨动即跳系统无障碍设置，并延迟 100ms 在其上叠加半透明“点这里”伪开关遮罩引导用户开启监听全部应用窗口的无障碍服务。",
  "disguise_identity": {
    "app_display_name": "QR Scanner",
    "claimed_brand_or_persona": "QR Scanner Secure Scanning（自称基于开源 ZXing 的正规条码扫描器，宣称用于告警可疑网站保护设备）",
    "a11y_service_label": "QR Scanner Secure Scanning",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务名以“Secure Scanning（安全扫描）”包装，实际 eventTypes=-1、packageNames 为空、canRetrieveWindowContent=true，监听所有应用窗口内容；about_ 字符串自称“About WiFiBarcode”，与 QR Scanner 品牌不一致；overlay 文案使用换行挤出式排布（\"QR Scanner Secure Scanning \\nOff/On\"）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.qrcode.ActivitySplash（LAUNCHER，Theme.Transparent）→ Open_Activity() → com.qrcode.MainActivity / com.google.zxing.client.android.CaptureActivity",
      "trigger_event": "ActivitySplash.onCreate() 后调用 Open_Activity()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（启动页仅设置 QR_COLOR 后跳转，本步不弹无障碍引导）",
      "shown_text_zh": "启动页不展示无障碍相关文案，仅完成初始化与跳转",
      "user_action_requested": "无需操作，自动进入主界面",
      "code_anchor": "com.qrcode.ActivitySplash.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "CaptureActivity 扫码页（layout/capture，含 banner 广告、tv_secure 文本、默认隐藏的 Switch toggle）",
      "trigger_event": "handleDecode() 识别结果为 ParsedResultType.URI 且 MyAccessibilityService.isAccessibilitySettingsOn(this) 为 false",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Secure Scanning（lbl_secure_scan）",
      "shown_text_zh": "扫描页显示“安全扫描”字样的开关，引导用户打开",
      "user_action_requested": "要求用户拨动开关；开关默认可见但无取消/跳过说明，用户可放弃拨动",
      "code_anchor": "com.google.zxing.client.android.CaptureActivity#handleDecode + res/values/strings.xml:lbl_secure_scan"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "android.settings.ACCESSIBILITY_SETTINGS 系统无障碍设置页（startActivityForResult requestCode=1）",
      "trigger_event": "CaptureActivity$4.onCheckedChanged() 中 toggle.isChecked() 为 true",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Enable Secure Scanning",
      "shown_text_zh": "系统无障碍设置页内出现条目“QR Scanner Secure Scanning”，描述为开启无障碍以告警可疑网站",
      "user_action_requested": "要求用户在系统列表中点击该服务并确认开启；系统层面可返回退出",
      "code_anchor": "com.google.zxing.client.android.CaptureActivity$4#onCheckedChanged + res/values/strings.xml:access_enable / accessibility_service_description"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.qrcode.ActivityOverlay（theme=Transparent，layout/activity_overlay，半透明 #703e3e3e 全屏遮罩 + click_here_on/off 箭头图 + tv_text）",
      "trigger_event": "startActivityForResult 之后 new Handler().postDelayed(new CaptureActivity$4$1(this), 100L) 在 100ms 后 startActivity(ActivityOverlay)",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "\"QR Scanner Secure Scanning \\nOff\" / \"QR Scanner Secure Scanning \\nOn\"",
      "shown_text_zh": "遮罩上显示“QR Scanner 安全扫描 已关闭/已开启”，并叠加指向系统开关位置的“点这里”箭头图，指示用户点击哪里",
      "user_action_requested": "要求用户点击遮罩/箭头处后关闭遮罩；onBackPressed() 为空实现，返回键无法退出遮罩，只能点击遮罩 finish()",
      "code_anchor": "com.qrcode.ActivityOverlay#onCreate + com.qrcode.ActivityOverlay$1#onClick + res/layout/activity_overlay.xml + res/values/strings.xml:overlay_on/overlay_off"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "CaptureActivity.onActivityResult(requestCode=1)",
      "trigger_event": "从系统无障碍页返回",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "未获权时仅把开关复位为关闭，不弹提示、不重跳；获权时隐藏开关并走网络检测 getSecure(mUrl)",
      "user_action_requested": "无强制操作；用户可再次拨动开关重复第 3–4 步",
      "code_anchor": "com.google.zxing.client.android.CaptureActivity#onActivityResult"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.qrcode.service.MyAccessibilityService（BIND_ACCESSIBILITY_SERVICE，config: eventTypes=typeViewTextSelectionChanged|typeWindowContentChanged|typeWindowStateChanged, packageNames=\"\", canRetrieveWindowContent=true）→ 启动 com.qrcode.MainActivity",
      "trigger_event": "onConnectedService() 回调（无障碍服务被系统连接）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务连上后立即以 NEW_TASK 标志拉起主界面，并把监听事件类型扩到 -1（全部事件），持续采集前台应用包名与窗口文本",
      "user_action_requested": "无，全自动执行",
      "code_anchor": "com.qrcode.service.MyAccessibilityService#onConnectedService + res/xml/accessibility_service_config.xml"
    },
    {
      "step": 7,
      "stage": "引导说明页（第二入口）",
      "screen_or_component": "com.qrcode.ActivitySettings$SettingsFragment 中的 pref_access SwitchPreference",
      "trigger_event": "onPreferenceChange() 被触发（不论勾选或取消）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Enable Secure Scanning / Disable Secure Scanning",
      "shown_text_zh": "设置页“开启/关闭安全扫描”开关项，操作后同样跳系统无障碍页并延迟弹遮罩",
      "user_action_requested": "要求用户开启该项；无跳过入口（返回 false 阻止状态变更，仅触发跳转）",
      "code_anchor": "com.qrcode.ActivitySettings$SettingsFragment$1#onPreferenceChange + com.qrcode.ActivitySettings$SettingsFragment#call_act"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项名称与说明：android:label=@string/accessibility_service_label（QR Scanner Secure Scanning）、android:description=@string/accessibility_service_description（res/xml/accessibility_service_config.xml 引用）",
    "扫码结果页 CaptureActivity 原生布局 layout/capture 中的 tv_secure 文本与隐藏 Switch 开关（“Secure Scanning”）",
    "系统无障碍设置页之上的透明叠层 ActivityOverlay（layout/activity_overlay.xml）：半透明全屏背景 + click_here_on/off 箭头图 + tv_text 文案“QR Scanner Secure Scanning On/Off”",
    "设置页 ActivitySettings 的 SwitchPreference 项：Enable Secure Scanning / Disable Secure Scanning",
    "assets/html-de|html-* 下的 ZXing 帮助/许可/更新说明本地 HTML（HelpActivity WebView 展示，与无障碍诱导无直接关联）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility to allow QR Scanner to secure your device by showing alerts on suspicious websites. The Accessibility feature allows QR Scanner to provide its services to all users. By enabling Accessbility, you Acknowledge that you have read and agree to our Terms of service and Privacy Policy.",
      "text_zh": "启用无障碍功能，允许 QR Scanner 通过提示可疑网站来保护你的设备安全。该无障碍功能使 QR Scanner 能够向所有用户提供服务。启用无障碍即表示你确认已阅读并同意我们的服务条款与隐私政策。",
      "source_location": "res/values/strings.xml:accessibility_service_description（经 res/xml/accessibility_service_config.xml 的 android:description 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "QR Scanner Secure Scanning \nOff",
      "text_zh": "QR Scanner 安全扫描 已关闭",
      "source_location": "res/values/strings.xml:overlay_off（ActivityOverlay tv_text 显示）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "QR Scanner Secure Scanning \nOn",
      "text_zh": "QR Scanner 安全扫描 已开启",
      "source_location": "res/values/strings.xml:overlay_on（ActivityOverlay tv_text 显示）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Secure Scanning",
      "text_zh": "开启安全扫描",
      "source_location": "res/values/strings.xml:access_enable（扫码页开关/设置页项文案）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "QR Scanner Secure Scanning",
      "text_zh": "QR Scanner 安全扫描（系统无障碍列表显示的服务名）",
      "source_location": "res/values/strings.xml:accessibility_service_label（AndroidManifest service android:label）",
      "rhetorical_frame": "假反诈安全"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "未获权返回后仅执行 toggle.setChecked(false)，不重跳、无定时器强拉；用户再次拨动开关即重复“跳设置+100ms 叠层”流程，属可反复施压但非死循环。",
    "overlay_or_fake_settings": "是。ActivityOverlay 为透明主题全屏叠层（背景 #703e3e3e），压在系统无障碍设置页之上，用 click_here_on/click_here_off 箭头图与“QR Scanner Secure Scanning On/Off”文案模拟开关状态指引点击位置；onBackPressed() 空实现使返回键无法关闭遮罩，必须点击遮罩才 finish()。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无（onServiceInterrupt/onDestroyService 仅打日志；未监听设置页执行 GLOBAL_ACTION_BACK/HOME，未自点确认）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "Hook startActivityForResult 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（或直接监测 com.qrcode.ActivityOverlay 被 startActivity）；叠层在跳转后约 100ms 出现，建议在跳转后 150–500ms 抓取当前前台窗口。",
    "key_pages_to_capture": [
      {
        "page_role": "设置页后叠层遮罩页（最关键）",
        "page_identifier": "包名 qrcode.scanner.qrmaker 下 com.qrcode.ActivityOverlay（透明主题 Activity，全屏半透明底 + 箭头图 + “QR Scanner Secure Scanning On/Off”文本）",
        "why_most_useful": "这是该应用区别于普通合规扫码器的决定性证据：在系统设置页之上叠层指引点击，形成伪开关/遮罩引导。",
        "observable_utg_signals": [
          "前台 Activity 为 com.qrcode.ActivityOverlay 且背景 Activity 为 Settings$AccessibilitySettings",
          "界面文本含 \"QR Scanner Secure Scanning\" 与 \"On\"/\"Off\"",
          "存在图片控件 img_enable（click_here_on / click_here_off）",
          "遮罩无取消按钮，返回键无效"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility 中条目 “QR Scanner Secure Scanning”，副标题为 security 描述文案",
        "why_most_useful": "核对身份伪装与宣称范围（告警可疑网站）与实际权限（全应用窗口内容）的落差。",
        "observable_utg_signals": [
          "服务条目名称 QR Scanner Secure Scanning",
          "描述文本含 \"secure your device by showing alerts on suspicious websites\""
        ]
      },
      {
        "page_role": "扫码结果页（触发前）",
        "page_identifier": "com.google.zxing.client.android.CaptureActivity，含 tv_secure 文本与刚出现的 Switch 开关",
        "why_most_useful": "确认引导仅在扫到 URL 结果后按需出现，属于业务功能触发而非冷启动强推。",
        "observable_utg_signals": [
          "扫描 URI 二维码后 Switch 由隐藏变为可见",
          "页面含 “Secure Scanning” 文本"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "遮罩中的箭头图（click_here_on/off）本身为图片，需靠文本与 Activity 名判定，纯图判定可能漏；此外引导只在扫到 URL 二维码时出现，需构造 URI 二维码输入才能触发，冷启动不会直接暴露该流程。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.google.zxing.client.android.CaptureActivity#handleDecode",
    "com.google.zxing.client.android.CaptureActivity$4#onCheckedChanged",
    "com.google.zxing.client.android.CaptureActivity$4$1#run",
    "com.qrcode.ActivityOverlay#onCreate",
    "com.qrcode.ActivitySettings$SettingsFragment#call_act",
    "com.qrcode.service.MyAccessibilityService#onConnectedService",
    "res/xml/accessibility_service_config.xml",
    "res/layout/activity_overlay.xml"
  ]
}
```

说明：受本轮“≤14 次工具调用即收口”的硬性约束，本次仅完成引导链路核验，未再追加 `register_evidence_graph`/`record_risk` 写入；上述结论为代码级已确认事实（未加壳，全链路静态可见），风险定级建议为高（恶意无障碍叠层诱导 + 全应用窗口内容监听）。

</details>

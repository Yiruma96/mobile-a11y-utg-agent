# MB_034__a9d1561ed0｜Escobar — McAfee

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：116.6s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即用本地 HTML 高仿系统无障碍设置页 + 伪开关，点击后经空页面信号在 onPageStarted 中 finishAndRemoveTask 并直跳真实 ACCESSIBILITY_SETTINGS，获权后 GLOBAL_ACTION_BACK/HOME 踢出设置页并定时重新拉起主界面。
- **静态可见性说明**：诱导链全部位于本地 DEX 与 assets/welcome.html、assets/startaccessibility.html，未加壳、未加密；仅获权后的远端面板 http://melanieparker.42web.io/index2.php 属后续 C2/钓鱼面板，不参与无障碍引导，故不影响本命题静态可见性。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a9d1561ed0d23a5473d68069337e2f8e7862f7b72b74251eb63ccc883ba9459f` |
| 包名 / 年份 | `com.escobar.pablo` / 2022 |
| 家族 / 品类 | **Escobar**（同池样本数：1） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | McAfee |
| 引导页宣称品牌/身份 | McAfee（知名安全厂商，冒充杀毒/安全软件） |
| 系统无障碍列表服务名 | McAfee（服务未单独声明 android:label，继承应用 label；描述为 McAfee needs to be enabled to work correctly.） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 引导文案走字符串拼接：activate_accessibility="Please enable Accessibility for " + app_name="McAfee"，单看任一条字符串无法识别完整语义；2) 用内容仅 <html><body></body></html> 的空页面 startaccessibility.html 作为跳转信号，URL 关键字在 onPageStarted 中被匹配；3) 跳转前 finishAndRemoveTask() 清空任务栈，返回键无法回到引导页；4) accessibility_service_config 的 settingsActivity 指向不存在的 com.example.android.accessibility.ServiceSettingsActivity，屏蔽服务设置入口；5) 包名 com.escobar.pablo / 类名 com.example.pablo.AccessibilityService 与 McAfee 品牌毫无关系；6) 本地 HTML 完整复刻系统无障碍设置页分组与条目（含 TalkBack、Color inversion、OFF/Default）以冒充系统界面。未使用空白/换行挤出、同形字或伪造 isAccessibilityTool（targetSdk 30 无该 API 语义）。 |
| 无障碍服务类名 | `com.example.pablo.AccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |
| 系统设置项说明 (`android:description`) | McAfee needs to be enabled to work correctly. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.example.pablo.MainActivity（LAUNCHER 入口，无自定义 UI） | onCreate 中读取 SharedPreferences("setup") 与 Settings.Secure "enabled_accessibility_services"，判定自身 AccessibilityService 未启用且非模拟器 | 通知栏 + 原生 Toast | **原文**：Please enable Accessibility for McAfee（由 activate_accessibility + app_name 拼接，连续 Toast 3 次）；通知标题/文本同样为上述拼接串，频道名 "Channel 1" / 描述 "This is Channel 1"<br>**译注**：请为 McAfee 开启无障碍（伪装安全软件要求授权无障碍服务） | 点击常驻通知；通知 PendingIntent 直接指向 android.settings.ACCESSIBILITY_SETTINGS。无取消/跳过入口 | `com.example.pablo.MainActivity.onCreate（L12c 分支，Intent("android.settings.ACCESSIBILITY_SETTINGS") + Toast）` |
| 2 | 引导说明页 | MainActivity 内 WebView（R.layout.bank，id=webView 0x7f0801a7）加载 file:///android_asset/welcome.html | onCreate 未启用分支执行 setContentView(0x7f0b001d) 后 loadUrl("file:///android_asset/welcome.html")，setJavaScriptEnabled(true) | 本地HTML WebView | **原文**：Accessibility（页面标题）；DOWNLOADED SERVICES / Accessibility Service / Select to speak / Switch Access / TalkBack；SCREEN READERS / Text-to-speech output；DISPLAY / Font size / Display size / Magnification / Color correction / Color inversion；OFF / Default；页脚：Please enable Accessibility for McAfee<br>**译注**：整页高仿系统「无障碍」设置界面（含下载服务、屏幕阅读器、显示三类分组及开关状态），页脚提示为 McAfee 开启无障碍 | 点击页面底部伪造的开关 div#btn（onclick=ClickOK()）；无真实返回/取消按钮，无跳过入口 | `assets/welcome.html（L216 <b id='startaccessibility'>McAfee</b>、L292 .ctxt 文案、L303-L330 objLang 伪设置条目、L360-L366 ClickOK/location.replace）` |
| 3 | 跳受限设置（隐蔽跳转） | assets/startaccessibility.html（空页面，仅作信号）→ MainActivity$OooO0OO.onPageStarted | ClickOK() 执行 location.replace("file:///android_asset/startaccessibility.html")；WebViewClient.onPageStarted 判断 url.contains("startaccessibility") 后调用 finishAndRemoveTask() 并 startActivity(Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 本地HTML WebView（中转）→ 系统无障碍页 | **原文**：无（startaccessibility.html 内容为 <html><body></body></html>，用户不可见）<br>**译注**：无可见内容，仅触发跳转 | 无（自动跳转，用户无法察觉中转页面） | `com.example.pablo.MainActivity$OooO0OO.onPageStarted；assets/startaccessibility.html` |
| 4 | 跳无障碍设置 | 系统「设置 → 无障碍 → 已下载的服务」列表，条目为 McAfee | onPageStarted 中 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))；另通知栏 PendingIntent 亦可直达 | 系统无障碍页 | **原文**：McAfee（服务名）；McAfee needs to be enabled to work correctly.（服务描述）<br>**译注**：服务名“McAfee”，说明“需要启用 McAfee 才能正常工作” | 用户在系统列表中手动点击 McAfee 开关并确认授权（此步为真实系统 UI，应用无法代点） | `res/xml/accessibility_service_config.xml（android:description=@string/accessibility_service_description、settingsActivity=com.example.android.accessibility.ServiceSettingsActivity）；res/values/strings.xml accessibility_service_description / app_name` |
| 5 | 拒权反馈循环 | MainActivity 冷启动链路重复执行（Toast + welcome.html 伪设置页 + 通知） | 用户从系统设置返回或未开启时：因跳转前 finishAndRemoveTask() 已清空任务栈，用户只能重新点击桌面图标；同时 AccessibilityService 内 750ms Timer 与 3500ms Timer 持续拉起 MainActivity（获权后路径） | 原生Toast + 本地HTML WebView + 通知栏 | **原文**：Please enable Accessibility for McAfee；Please enable Accessibility for McAfee（页脚重复出现）<br>**译注**：反复提示为 McAfee 开启无障碍，无降级路径 | 只能再次点击伪开关重走跳转；无取消、跳过或稍后再说选项 | `com.example.pablo.MainActivity.onCreate（未启用分支整体重入）；com.example.pablo.AccessibilityService$OooO00o.run（750ms 重开 MainActivity）` |
| 6 | 获权后动作 | com.example.pablo.AccessibilityService.onServiceConnected + MainActivity 重新压栈 + Bank 钓鱼页 | onServiceConnected 立即 performGlobalAction(1)×2（GLOBAL_ACTION_BACK）、performGlobalAction(2)（GLOBAL_ACTION_HOME），Timer.schedule(…,750L) 由 AccessibilityService$OooO00o.run startActivity(MainActivity)，并启动按键记录线程与 C2 线程；onAccessibilityEvent 对 settings/packageinstaller/permission 包按含 "Enable" 自动 performAction(16) 点击，3500ms 定时复投；authenticator 包连点 20 次；事件类型 2048 触发 startActivity(Bank) | 系统无障碍页（被强行退出）→ 原生Activity + 远端WebView | **原文**：Please authenticate your credit card to proceed；CVV；Expiration date [MM/YY]；Please fill all information correctly!；http://melanieparker.42web.io/index2.php<br>**译注**：伪造信用卡验证页要求输入卡号/CVV/有效期，并加载远端控制面板 | 被踢出设置页后进入伪造面板/钓鱼页，要求填写支付卡信息 | `com.example.pablo.AccessibilityService.onServiceConnected；com.example.pablo.AccessibilityService.onAccessibilityEvent；com.example.pablo.Bank.onCreate；res/values/strings.xml credit_card / cvv_hint / date_hint / cardalert` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动原生 Toast：MainActivity.onCreate 拼接 activate_accessibility + app_name，连续弹 3 次 “Please enable Accessibility for McAfee”
- 通知栏常驻通知（channel1/Channel 1）：标题与文本同上述拼接串，点击 PendingIntent 直达 android.settings.ACCESSIBILITY_SETTINGS
- assets/welcome.html 本地 WebView 全屏页：整页高仿系统无障碍设置（标题 Accessibility、分组 DOWNLOADED SERVICES/SCREEN READERS/DISPLAY、条目 TalkBack/Switch Access/Color inversion 等），页脚 .ctxt “Please enable Accessibility for McAfee”，底部伪开关 div#btn
- 系统无障碍服务列表项：服务名 McAfee，android:description = “McAfee needs to be enabled to work correctly.”（res/values/strings.xml accessibility_service_description）
- assets/startaccessibility.html：空页面，不呈现任何文字，仅作为跳转信号
- 获权后 Bank Activity 远端 WebView：信用卡验证文案 “Please authenticate your credit card to proceed”、CVV、Expiration date [MM/YY]

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please enable Accessibility for | 请为……开启无障碍 | `res/values/strings.xml key=activate_accessibility（代码中与 app_name 拼接）` | 受限设置分步教学 |
| en | McAfee needs to be enabled to work correctly. | 需要启用 McAfee 才能正常工作。 | `res/values/strings.xml key=accessibility_service_description（由 accessibility_service_config.xml 引用）` | 假反诈安全 |
| en | Please enable Accessibility for McAfee | 请为 McAfee 开启无障碍 | `assets/welcome.html 第 292 行 .ctxt 文本（同屏第 216 行 <b id='startaccessibility'>McAfee</b>）` | 受限设置分步教学 |
| en | Accessibility / DOWNLOADED SERVICES / Accessibility Service / Select to speak / Switch Access / TalkBack / SCREEN READERS / Text-to-speech output / DISPLAY / Font size / Display size / Magnification / Color correction / Color inversion / OFF / Default | 无障碍 / 已下载的服务 / 无障碍服务 / 随选朗读 / 开关控制 / TalkBack / 屏幕阅读器 / 文字转语音输出 / 显示 / 字体大小 / 显示大小 / 放大功能 / 色彩校正 / 颜色反转 / 关闭 / 默认 | `assets/welcome.html 第 303-330 行 objLang 语言包（伪造系统设置条目）` | 未知 |
| en | Please authenticate your credit card to proceed | 请验证您的信用卡以继续 | `res/values/strings.xml key=credit_card（Bank 钓鱼页）` | 假更新 |
| en | CVV | CVV 安全码 | `res/values/strings.xml key=cvv_hint` | 未知 |
| en | Expiration date [MM/YY] | 有效期 [月/年] | `res/values/strings.xml key=date_hint` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：跳转前调用 finishAndRemoveTask() 清空任务栈，用户从系统设置返回后无页面可回，只能重新点击桌面图标再次进入 onCreate 未启用分支（重弹 Toast 与 welcome.html 伪设置页）；获权后 750ms Timer 反复 startActivity(MainActivity)，3500ms Timer 周期性重投无障碍事件自动点击；常驻通知亦可持续把用户送回系统无障碍页。
- **遮罩叠层 / 高仿系统设置页**：本地 HTML（assets/welcome.html）在应用内 WebView 全屏复刻系统无障碍设置页（含分组、条目、OFF/Default 状态与底部伪开关），并非真正的悬浮窗；未发现叠加在真实系统设置页之上的半透明遮罩。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdk 30，未使用 ACTION_APPLICATION_DETAILS_SETTINGS 做“受限设置”教学；该 Intent 仅出现在 CommandListener 的其他远程指令逻辑中，与无障碍引导无关）
- **获权后即时行为与防撤权机制**：onServiceConnected 立即 performGlobalAction(1)×2（GLOBAL_ACTION_BACK）与 performGlobalAction(2)（GLOBAL_ACTION_HOME）强制退出系统设置页；onAccessibilityEvent 监听 settings 包，可对节点执行 performAction(16) 自动点击“启用/允许”，并按 CommandListener 下发含 "Enable" 的指令连点 5 次；另以 Uninstall 服务与 uninstallProtection 标志防护卸载。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在冷启动 MainActivity.onCreate 首帧（Toast 与 welcome.html 伪设置页同屏）即拉起 UTG；并在监测到 Activity 跳转 android.settings.ACCESSIBILITY_SETTINGS（且跳转前本应用任务栈被 finishAndRemoveTask 清空）时立即抓取栈顶与截图。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：welcome.html 的伪开关 div#btn 仅以 CSS 绘制、无可见文字，若 UTG 只按文本匹配可能漏掉该点击入口，需结合可点击区域/节点类名判定；另外 startaccessibility.html 为空页面，UTG 抓页时易被误判为“加载失败”，实为跳转信号。未加壳、无密文载荷，运行期 UTG 不受静态保护影响。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（Toast + 伪设置 WebView）** | com.escobar.pablo/com.example.pablo.MainActivity，内容为 WebView 承载的 Accessibility 页面，页脚含 “Please enable Accessibility for McAfee”，底部伪开关无文字 | 该屏同时呈现品牌冒充（McAfee）与高仿系统设置外观，是判定诱导与假设置屏的最直接证据 | Toast 文本 “Please enable Accessibility for McAfee”；WebView 内伪造分组 DOWNLOADED SERVICES / SCREEN READERS / DISPLAY；页面无可点击的返回/取消控件 |
| **跳转瞬间的栈切换** | MainActivity 消失 → 系统 com.android.settings/.SubSettings 或 AccessibilitySettingsActivity（跳转前应用任务栈被清空） | 证明无障碍设置页由应用代码而非用户自行进入，且返回无路可退 | Activity 跳转目标为 android.settings.ACCESSIBILITY_SETTINGS；跳转前本应用 task 被 finishAndRemoveTask 清除；跳转前存在 file:///android_asset/startaccessibility.html 的瞬时导航 |
| **系统无障碍服务列表项** | 系统无障碍设置 → 已下载的服务，条目名 McAfee | 核对系统侧展示的身份与服务描述是否与安全软件品牌一致 | 服务名 McAfee（来自应用 label，非服务自身 label）；描述 “McAfee needs to be enabled to work correctly.”；点入后无服务设置页（settingsActivity 指向不存在的类） |
| **获权后踢出设置页与重新拉起** | 授权瞬间系统设置页被 BACK/HOME 退出，约 750ms 后 MainActivity 重新回到前台 | 验证反撤权与后台自启行为，区分正常安全软件与恶意持久化 | 授权后立即触发 GLOBAL_ACTION_BACK ×2 与 GLOBAL_ACTION_HOME；750ms 后 MainActivity 被 startActivity 重新压栈；随后加载远端面板 http://melanieparker.42web.io/index2.php |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.example.pablo.MainActivity.onCreate`
- `com.example.pablo.MainActivity$OooO0OO.onPageStarted`
- `com.example.pablo.AccessibilityService.onServiceConnected`
- `com.example.pablo.AccessibilityService.onAccessibilityEvent`
- `assets/welcome.html（ClickOK / location.replace 至 startaccessibility.html）`
- `res/values/strings.xml（activate_accessibility、accessibility_service_description、app_name、credit_card）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 定向核验结论（纯运行期 UTG 视角）

**已闭环，静态完全可见（未加壳）**。整条诱导链是“本地 HTML 高仿无障碍设置页 → 空页面作信号 → `onPageStarted` 跳真实系统无障碍页”，不涉及远端下发引导页。

1. **冷启动即阻断**：`MainActivity.onCreate` 先读 `Settings.Secure.enabled_accessibility_services` 判断自身服务是否已启用；未启用时建 `channel1` 通知（`PendingIntent` 直指 `android.settings.ACCESSIBILITY_SETTINGS`），并连续 `Toast` 输出 `activate_accessibility + app_name` 拼接文案“Please enable Accessibility for McAfee”。
2. **高仿系统设置页（WebView 本地 HTML）**：未启用分支 `setContentView(R.layout.bank)` → `webView.loadUrl("file:///android_asset/welcome.html")`。该 HTML 标题 `Accessibility`，完整复刻系统分组 `DOWNLOADED SERVICES / SCREEN READERS / DISPLAY`、`TalkBack`、`Color inversion`、`OFF/Default` 等条目，底部有伪开关 `div#btn`，页脚文字 “Please enable Accessibility for McAfee”。这是**假设置屏（CARRIER_FAKE_SETTINGS_SCREEN）**，不是普通说明页。
3. **跳转点隐蔽化**：点击伪开关 `ClickOK()` → `location.replace("file:///android_asset/startaccessibility.html")`，而 `startaccessibility.html` 内容仅为空 `<html><body></body></html>`，纯作信号。`MainActivity$OooO0OO.onPageStarted` 见 URL 含 `startaccessibility` 即 `finishAndRemoveTask()` 后 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`——**先销毁自身任务栈再进设置**，用户返回时无页可退，只能重新冷启动。
4. **系统列表身份**：服务无独立 `android:label`，沿用应用 label `McAfee`；`android:description` = “McAfee needs to be enabled to work correctly.”，`settingsActivity` 指向不存在的 `com.example.android.accessibility.ServiceSettingsActivity`（屏蔽服务设置入口）。全程**未使用** `ACTION_APPLICATION_DETAILS_SETTINGS` 做 13+ 受限设置教学（targetSdk 30，无需）。
5. **获权即反制**：`AccessibilityService.onServiceConnected` 立即 `performGlobalAction(1)`×2（BACK）+ `performGlobalAction(2)`（HOME）把用户踢出设置页，并 `Timer.schedule(…, 750ms)` 由 `AccessibilityService$OooO00o.run` 重新 `startActivity(MainActivity)`；同时起按键记录线程与 C2 线程。`onAccessibilityEvent` 对 `settings/packageinstaller/permission` 包按 `CommandListener.OooO0O0` 含 "Enable" 自动 `performAction(16)` 点击“允许/启用”，每 3500ms 定时复投，并对 `authenticator` 包连点 20 次窃取 OTP、对银行站点事件跳 `Bank` 钓鱼页。

**UTG 取证要点**：监测 `ACTION_ACCESSIBILITY_SETTINGS` 跳转瞬间抓栈；冷启动首屏必抓（Toast + welcome.html 伪设置页同屏）；获权后 750ms 内抓 MainActivity 重新压栈（自启动证据）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "诱导链全部位于本地 DEX 与 assets/welcome.html、assets/startaccessibility.html，未加壳、未加密；仅获权后的远端面板 http://melanieparker.42web.io/index2.php 属后续 C2/钓鱼面板，不参与无障碍引导，故不影响本命题静态可见性。",
  "summary_one_liner": "冷启动即用本地 HTML 高仿系统无障碍设置页 + 伪开关，点击后经空页面信号在 onPageStarted 中 finishAndRemoveTask 并直跳真实 ACCESSIBILITY_SETTINGS，获权后 GLOBAL_ACTION_BACK/HOME 踢出设置页并定时重新拉起主界面。",
  "disguise_identity": {
    "app_display_name": "McAfee",
    "claimed_brand_or_persona": "McAfee（知名安全厂商，冒充杀毒/安全软件）",
    "a11y_service_label": "McAfee（服务未单独声明 android:label，继承应用 label；描述为 McAfee needs to be enabled to work correctly.）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 引导文案走字符串拼接：activate_accessibility=\"Please enable Accessibility for \" + app_name=\"McAfee\"，单看任一条字符串无法识别完整语义；2) 用内容仅 <html><body></body></html> 的空页面 startaccessibility.html 作为跳转信号，URL 关键字在 onPageStarted 中被匹配；3) 跳转前 finishAndRemoveTask() 清空任务栈，返回键无法回到引导页；4) accessibility_service_config 的 settingsActivity 指向不存在的 com.example.android.accessibility.ServiceSettingsActivity，屏蔽服务设置入口；5) 包名 com.escobar.pablo / 类名 com.example.pablo.AccessibilityService 与 McAfee 品牌毫无关系；6) 本地 HTML 完整复刻系统无障碍设置页分组与条目（含 TalkBack、Color inversion、OFF/Default）以冒充系统界面。未使用空白/换行挤出、同形字或伪造 isAccessibilityTool（targetSdk 30 无该 API 语义）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.example.pablo.MainActivity（LAUNCHER 入口，无自定义 UI）",
      "trigger_event": "onCreate 中读取 SharedPreferences(\"setup\") 与 Settings.Secure \"enabled_accessibility_services\"，判定自身 AccessibilityService 未启用且非模拟器",
      "ui_carrier": "通知栏 + 原生 Toast",
      "shown_text_verbatim": "Please enable Accessibility for McAfee（由 activate_accessibility + app_name 拼接，连续 Toast 3 次）；通知标题/文本同样为上述拼接串，频道名 \"Channel 1\" / 描述 \"This is Channel 1\"",
      "shown_text_zh": "请为 McAfee 开启无障碍（伪装安全软件要求授权无障碍服务）",
      "user_action_requested": "点击常驻通知；通知 PendingIntent 直接指向 android.settings.ACCESSIBILITY_SETTINGS。无取消/跳过入口",
      "code_anchor": "com.example.pablo.MainActivity.onCreate（L12c 分支，Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") + Toast）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity 内 WebView（R.layout.bank，id=webView 0x7f0801a7）加载 file:///android_asset/welcome.html",
      "trigger_event": "onCreate 未启用分支执行 setContentView(0x7f0b001d) 后 loadUrl(\"file:///android_asset/welcome.html\")，setJavaScriptEnabled(true)",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Accessibility（页面标题）；DOWNLOADED SERVICES / Accessibility Service / Select to speak / Switch Access / TalkBack；SCREEN READERS / Text-to-speech output；DISPLAY / Font size / Display size / Magnification / Color correction / Color inversion；OFF / Default；页脚：Please enable Accessibility for McAfee",
      "shown_text_zh": "整页高仿系统「无障碍」设置界面（含下载服务、屏幕阅读器、显示三类分组及开关状态），页脚提示为 McAfee 开启无障碍",
      "user_action_requested": "点击页面底部伪造的开关 div#btn（onclick=ClickOK()）；无真实返回/取消按钮，无跳过入口",
      "code_anchor": "assets/welcome.html（L216 <b id='startaccessibility'>McAfee</b>、L292 .ctxt 文案、L303-L330 objLang 伪设置条目、L360-L366 ClickOK/location.replace）"
    },
    {
      "step": 3,
      "stage": "跳受限设置（隐蔽跳转）",
      "screen_or_component": "assets/startaccessibility.html（空页面，仅作信号）→ MainActivity$OooO0OO.onPageStarted",
      "trigger_event": "ClickOK() 执行 location.replace(\"file:///android_asset/startaccessibility.html\")；WebViewClient.onPageStarted 判断 url.contains(\"startaccessibility\") 后调用 finishAndRemoveTask() 并 startActivity(Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "本地HTML WebView（中转）→ 系统无障碍页",
      "shown_text_verbatim": "无（startaccessibility.html 内容为 <html><body></body></html>，用户不可见）",
      "shown_text_zh": "无可见内容，仅触发跳转",
      "user_action_requested": "无（自动跳转，用户无法察觉中转页面）",
      "code_anchor": "com.example.pablo.MainActivity$OooO0OO.onPageStarted；assets/startaccessibility.html"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「设置 → 无障碍 → 已下载的服务」列表，条目为 McAfee",
      "trigger_event": "onPageStarted 中 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))；另通知栏 PendingIntent 亦可直达",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "McAfee（服务名）；McAfee needs to be enabled to work correctly.（服务描述）",
      "shown_text_zh": "服务名“McAfee”，说明“需要启用 McAfee 才能正常工作”",
      "user_action_requested": "用户在系统列表中手动点击 McAfee 开关并确认授权（此步为真实系统 UI，应用无法代点）",
      "code_anchor": "res/xml/accessibility_service_config.xml（android:description=@string/accessibility_service_description、settingsActivity=com.example.android.accessibility.ServiceSettingsActivity）；res/values/strings.xml accessibility_service_description / app_name"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity 冷启动链路重复执行（Toast + welcome.html 伪设置页 + 通知）",
      "trigger_event": "用户从系统设置返回或未开启时：因跳转前 finishAndRemoveTask() 已清空任务栈，用户只能重新点击桌面图标；同时 AccessibilityService 内 750ms Timer 与 3500ms Timer 持续拉起 MainActivity（获权后路径）",
      "ui_carrier": "原生Toast + 本地HTML WebView + 通知栏",
      "shown_text_verbatim": "Please enable Accessibility for McAfee；Please enable Accessibility for McAfee（页脚重复出现）",
      "shown_text_zh": "反复提示为 McAfee 开启无障碍，无降级路径",
      "user_action_requested": "只能再次点击伪开关重走跳转；无取消、跳过或稍后再说选项",
      "code_anchor": "com.example.pablo.MainActivity.onCreate（未启用分支整体重入）；com.example.pablo.AccessibilityService$OooO00o.run（750ms 重开 MainActivity）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.example.pablo.AccessibilityService.onServiceConnected + MainActivity 重新压栈 + Bank 钓鱼页",
      "trigger_event": "onServiceConnected 立即 performGlobalAction(1)×2（GLOBAL_ACTION_BACK）、performGlobalAction(2)（GLOBAL_ACTION_HOME），Timer.schedule(…,750L) 由 AccessibilityService$OooO00o.run startActivity(MainActivity)，并启动按键记录线程与 C2 线程；onAccessibilityEvent 对 settings/packageinstaller/permission 包按含 \"Enable\" 自动 performAction(16) 点击，3500ms 定时复投；authenticator 包连点 20 次；事件类型 2048 触发 startActivity(Bank)",
      "ui_carrier": "系统无障碍页（被强行退出）→ 原生Activity + 远端WebView",
      "shown_text_verbatim": "Please authenticate your credit card to proceed；CVV；Expiration date [MM/YY]；Please fill all information correctly!；http://melanieparker.42web.io/index2.php",
      "shown_text_zh": "伪造信用卡验证页要求输入卡号/CVV/有效期，并加载远端控制面板",
      "user_action_requested": "被踢出设置页后进入伪造面板/钓鱼页，要求填写支付卡信息",
      "code_anchor": "com.example.pablo.AccessibilityService.onServiceConnected；com.example.pablo.AccessibilityService.onAccessibilityEvent；com.example.pablo.Bank.onCreate；res/values/strings.xml credit_card / cvv_hint / date_hint / cardalert"
    }
  ],
  "text_presentation_locations": [
    "冷启动原生 Toast：MainActivity.onCreate 拼接 activate_accessibility + app_name，连续弹 3 次 “Please enable Accessibility for McAfee”",
    "通知栏常驻通知（channel1/Channel 1）：标题与文本同上述拼接串，点击 PendingIntent 直达 android.settings.ACCESSIBILITY_SETTINGS",
    "assets/welcome.html 本地 WebView 全屏页：整页高仿系统无障碍设置（标题 Accessibility、分组 DOWNLOADED SERVICES/SCREEN READERS/DISPLAY、条目 TalkBack/Switch Access/Color inversion 等），页脚 .ctxt “Please enable Accessibility for McAfee”，底部伪开关 div#btn",
    "系统无障碍服务列表项：服务名 McAfee，android:description = “McAfee needs to be enabled to work correctly.”（res/values/strings.xml accessibility_service_description）",
    "assets/startaccessibility.html：空页面，不呈现任何文字，仅作为跳转信号",
    "获权后 Bank Activity 远端 WebView：信用卡验证文案 “Please authenticate your credit card to proceed”、CVV、Expiration date [MM/YY]"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please enable Accessibility for ",
      "text_zh": "请为……开启无障碍",
      "source_location": "res/values/strings.xml key=activate_accessibility（代码中与 app_name 拼接）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "McAfee needs to be enabled to work correctly.",
      "text_zh": "需要启用 McAfee 才能正常工作。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（由 accessibility_service_config.xml 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Please enable Accessibility for McAfee",
      "text_zh": "请为 McAfee 开启无障碍",
      "source_location": "assets/welcome.html 第 292 行 .ctxt 文本（同屏第 216 行 <b id='startaccessibility'>McAfee</b>）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility / DOWNLOADED SERVICES / Accessibility Service / Select to speak / Switch Access / TalkBack / SCREEN READERS / Text-to-speech output / DISPLAY / Font size / Display size / Magnification / Color correction / Color inversion / OFF / Default",
      "text_zh": "无障碍 / 已下载的服务 / 无障碍服务 / 随选朗读 / 开关控制 / TalkBack / 屏幕阅读器 / 文字转语音输出 / 显示 / 字体大小 / 显示大小 / 放大功能 / 色彩校正 / 颜色反转 / 关闭 / 默认",
      "source_location": "assets/welcome.html 第 303-330 行 objLang 语言包（伪造系统设置条目）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Please authenticate your credit card to proceed",
      "text_zh": "请验证您的信用卡以继续",
      "source_location": "res/values/strings.xml key=credit_card（Bank 钓鱼页）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "CVV",
      "text_zh": "CVV 安全码",
      "source_location": "res/values/strings.xml key=cvv_hint",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Expiration date [MM/YY]",
      "text_zh": "有效期 [月/年]",
      "source_location": "res/values/strings.xml key=date_hint",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "跳转前调用 finishAndRemoveTask() 清空任务栈，用户从系统设置返回后无页面可回，只能重新点击桌面图标再次进入 onCreate 未启用分支（重弹 Toast 与 welcome.html 伪设置页）；获权后 750ms Timer 反复 startActivity(MainActivity)，3500ms Timer 周期性重投无障碍事件自动点击；常驻通知亦可持续把用户送回系统无障碍页。",
    "overlay_or_fake_settings": "本地 HTML（assets/welcome.html）在应用内 WebView 全屏复刻系统无障碍设置页（含分组、条目、OFF/Default 状态与底部伪开关），并非真正的悬浮窗；未发现叠加在真实系统设置页之上的半透明遮罩。",
    "restricted_settings_13plus_coaching": "无（targetSdk 30，未使用 ACTION_APPLICATION_DETAILS_SETTINGS 做“受限设置”教学；该 Intent 仅出现在 CommandListener 的其他远程指令逻辑中，与无障碍引导无关）",
    "post_grant_anti_removal": "onServiceConnected 立即 performGlobalAction(1)×2（GLOBAL_ACTION_BACK）与 performGlobalAction(2)（GLOBAL_ACTION_HOME）强制退出系统设置页；onAccessibilityEvent 监听 settings 包，可对节点执行 performAction(16) 自动点击“启用/允许”，并按 CommandListener 下发含 \"Enable\" 的指令连点 5 次；另以 Uninstall 服务与 uninstallProtection 标志防护卸载。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在冷启动 MainActivity.onCreate 首帧（Toast 与 welcome.html 伪设置页同屏）即拉起 UTG；并在监测到 Activity 跳转 android.settings.ACCESSIBILITY_SETTINGS（且跳转前本应用任务栈被 finishAndRemoveTask 清空）时立即抓取栈顶与截图。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（Toast + 伪设置 WebView）",
        "page_identifier": "com.escobar.pablo/com.example.pablo.MainActivity，内容为 WebView 承载的 Accessibility 页面，页脚含 “Please enable Accessibility for McAfee”，底部伪开关无文字",
        "why_most_useful": "该屏同时呈现品牌冒充（McAfee）与高仿系统设置外观，是判定诱导与假设置屏的最直接证据",
        "observable_utg_signals": ["Toast 文本 “Please enable Accessibility for McAfee”", "WebView 内伪造分组 DOWNLOADED SERVICES / SCREEN READERS / DISPLAY", "页面无可点击的返回/取消控件"]
      },
      {
        "page_role": "跳转瞬间的栈切换",
        "page_identifier": "MainActivity 消失 → 系统 com.android.settings/.SubSettings 或 AccessibilitySettingsActivity（跳转前应用任务栈被清空）",
        "why_most_useful": "证明无障碍设置页由应用代码而非用户自行进入，且返回无路可退",
        "observable_utg_signals": ["Activity 跳转目标为 android.settings.ACCESSIBILITY_SETTINGS", "跳转前本应用 task 被 finishAndRemoveTask 清除", "跳转前存在 file:///android_asset/startaccessibility.html 的瞬时导航"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统无障碍设置 → 已下载的服务，条目名 McAfee",
        "why_most_useful": "核对系统侧展示的身份与服务描述是否与安全软件品牌一致",
        "observable_utg_signals": ["服务名 McAfee（来自应用 label，非服务自身 label）", "描述 “McAfee needs to be enabled to work correctly.”", "点入后无服务设置页（settingsActivity 指向不存在的类）"]
      },
      {
        "page_role": "获权后踢出设置页与重新拉起",
        "page_identifier": "授权瞬间系统设置页被 BACK/HOME 退出，约 750ms 后 MainActivity 重新回到前台",
        "why_most_useful": "验证反撤权与后台自启行为，区分正常安全软件与恶意持久化",
        "observable_utg_signals": ["授权后立即触发 GLOBAL_ACTION_BACK ×2 与 GLOBAL_ACTION_HOME", "750ms 后 MainActivity 被 startActivity 重新压栈", "随后加载远端面板 http://melanieparker.42web.io/index2.php"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "welcome.html 的伪开关 div#btn 仅以 CSS 绘制、无可见文字，若 UTG 只按文本匹配可能漏掉该点击入口，需结合可点击区域/节点类名判定；另外 startaccessibility.html 为空页面，UTG 抓页时易被误判为“加载失败”，实为跳转信号。未加壳、无密文载荷，运行期 UTG 不受静态保护影响。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH"
  ],
  "code_anchors": [
    "com.example.pablo.MainActivity.onCreate",
    "com.example.pablo.MainActivity$OooO0OO.onPageStarted",
    "com.example.pablo.AccessibilityService.onServiceConnected",
    "com.example.pablo.AccessibilityService.onAccessibilityEvent",
    "assets/welcome.html（ClickOK / location.replace 至 startaccessibility.html）",
    "res/values/strings.xml（activate_accessibility、accessibility_service_description、app_name、credit_card）"
  ]
}
```

> 说明：本次为满足 8–14 次工具调用的效率约束，未额外执行 `record_risk`/`register_evidence_graph` 落库，也未启动动态分析；上述结论均由 Manifest、`accessibility_service_config.xml`、`strings.xml`、`assets/welcome.html`、`assets/startaccessibility.html` 与 `MainActivity`/`AccessibilityService` 反编译实现直接支撑。覆盖边界：`CommandListener` 远程指令分支（含 `ACTION_APPLICATION_DETAILS_SETTINGS` 的用途）与远端 `index2.php` 面板内容未展开核验。

</details>

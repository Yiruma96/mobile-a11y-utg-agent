# MR_084__6291192d0c｜cebruser — Google

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：164.6s

## 1. 一句话核心结论

- **核心申请方式**：小米设备冷启动即弹出由远端配置生成的 WebView「更新」引导页，经 JS 桥一键跳转系统无障碍设置，并由导出服务每秒死循环重拉设置页直到用户开启名为 Update 的无障碍服务，获权后禁用桌面图标并监听/阻止撤权。
- **静态可见性说明**：DEX 全部逻辑静态可见（字符串为 RC4+Base64+Hex 三层编码，已还原）；引导页 HTML 正文不落盘，由配置字段 aO 在运行期提供，包内仅有占位符 %Enable_Accessibility_Service%，故引导文案确切措辞需运行期抓取 WebView 才能逐字确认。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `6291192d0c2f6318f9a4f345203b35cfe140be53889f9fefdd8e057a4f02e898` |
| 包名 / 年份 | `com.dfxsdgr.qvoor` / 2020 |
| 家族 / 品类 | **cebruser**（同池样本数：3） |
| 原始来源标识 | https://gbhackers.com/hackers-breached-mdm-servers-to-install-android-malware/ |
| 桌面显示名 | Google |
| 引导页宣称品牌/身份 | Google（桌面名直接冒用 Google 品牌）+ 系统「Update」更新提示 |
| 系统无障碍列表服务名 | Update |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：桌面名冒用 Google，无障碍服务名伪装为系统更新 Update；android:description 完全缺失（系统无障碍列表无任何说明，用户无从判断用途）；包名 com.dfxsdgr.qvoor 与类名均为随机乱序字符串；所有文案字符串 RC4 加密存放；LAUNCHER 组件在获权后被 setComponentEnabledSetting 禁用，使桌面图标消失；另有 label="" 且 excludeFromRecents 的 Theme.NoDisplay Activity（toe/iwmyer/azdncjcmq）作为隐形入口。 |
| 无障碍服务类名 | `com.dfxsdgr.qvoor.ociucqlhfkiqks` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.dfxsdgr.qvoor.shxptsks（LAUNCHER Activity，label=Google） | 用户点击桌面图标触发 onCreate | 原生Activity | **原文**：Google<br>**译注**：桌面图标与任务名显示为「Google」 | 点击桌面图标启动（无任何系统提示） | `com.dfxsdgr.qvoor.shxptsks#onCreate` |
| 2 | 冷启动入口 | shxptsks#onCreate 内的环境与授权判定分支 | onCreate 中 Build.MANUFACTURER 与版本判定、b.b(this, ociucqlhfkiqks.class) 无障碍启用检查 | 不可静态还原 | **原文**：无（非 xiaomi 设备直接 finish()，无任何界面）<br>**译注**：非小米机型静默退出，界面上什么都不显示 | 无 | `com.dfxsdgr.qvoor.shxptsks#onCreate / com.dfxsdgr.qvoor.b#b` |
| 3 | 引导说明页 | com.dfxsdgr.qvoor.ahcgthtk（全屏 WebView Activity，JS 已启用，注入 Android 桥） | shxptsks#onCreate 检测到无障碍未开启后 startActivity(ahcgthtk) | 本地HTML WebView | **原文**：%Enable_Accessibility_Service%（占位符，运行期被替换为「Build.MODEL + 配置串」；HTML 正文由配置字段 aO 下发，包内无落盘副本）<br>**译注**：由服务端下发的「启用无障碍服务」说明页文案，含机型名以伪造系统原生提示观感 | 按页面提示点击按钮开启无障碍（页面由远端配置决定是否提供取消入口，包内未见关闭按钮实现） | `com.dfxsdgr.qvoor.ahcgthtk#onCreate` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | WebView 内 JS 调用 Android.openAccessibilityService()（@JavascriptInterface） | 系统无障碍页 | 无 | 在系统列表中点击 Update 并确认开启；应用自身不提供取消/跳过 | `com.dfxsdgr.qvoor.ahcgthtk$c#openAccessibilityService` |
| 5 | 拒权反馈循环 | com.dfxsdgr.qvoor.drrwfkdgeutko（exported Service）onStartCommand 的 while(true) 循环 | 服务被启动后进入无限循环，每 sleep(1000) 复查一次无障碍状态 | 系统无障碍页（被反复重新拉起） | **原文**：error 45235（异常分支日志串）；循环内无任何提示文案<br>**译注**：用户返回或拒绝后，每秒再次把无障碍设置页弹到前台，无法通过返回键摆脱 | 必须开启无障碍服务才能跳出循环，无取消、无跳过 | `com.dfxsdgr.qvoor.drrwfkdgeutko#onStartCommand` |
| 6 | 获权后动作 | com.dfxsdgr.qvoor.ociucqlhfkiqks（无障碍服务，label=Update）onServiceConnected / onAccessibilityEvent；b.e(Context) 禁用 LAUNCHER 组件 | 无障碍开启后 shxptsks#onCreate 或 drrwfkdgeutko 循环调用 e.a(this) 与 b.e(Context) | 不可静态还原 | **原文**：Blocked attempt to disable accessibility service[143523#]；sti=009&q=saved_accessibility_events&zip=q1&ws=<br>**译注**：记录并阻止用户关闭无障碍服务，同时把采集到的无障碍事件打包上传服务端 | 无（后台自动执行，桌面图标随后被隐藏） | `com.dfxsdgr.qvoor.ociucqlhfkiqks#onAccessibilityEvent / com.dfxsdgr.qvoor.b#e(android.content.Context)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 桌面图标/任务标签：AndroidManifest 中 application android:label="Google"（shxptsks 为 LAUNCHER）
- 系统无障碍服务列表项：service android:label="Update"，android:description 完全缺失（无说明文字）
- 全屏 WebView 引导页：com.dfxsdgr.qvoor.ahcgthtk 用 loadDataWithBaseURL(null, <配置字段 aO 下发的 HTML>, "text/html") 渲染，含占位符 %Enable_Accessibility_Service% 被替换为「机型 + 配置串」
- 跳转系统设置后：无遮罩、无悬浮窗引导，仅靠 drrwfkdgeutko 每秒重复 startActivity 把系统无障碍页重新压到前台
- 隐形入口 Activity：toe / iwmyer / azdncjcmq 均为 label="" + excludeFromRecents（iwmyer、azdncjcmq 使用 icon=@drawable/mpftf 伪装图标）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Update | 更新 | `AndroidManifest.xml：service com.dfxsdgr.qvoor.ociucqlhfkiqks 的 android:label（经 RC4 解码后原文亦为 Update）` | 假更新 |
| en | Google | 谷歌 | `AndroidManifest.xml：application android:label` | 未知 |
| en | %Enable_Accessibility_Service% | （占位符）启用无障碍服务 | `ahcgthtk#onCreate 中经 RC4 解码得到的 HTML 占位符，运行期替换为「Build.MODEL + 配置串 ai」` | 教唆忽视警告 |
| en | Blocked attempt to disable accessibility service[143523#] | 已阻止尝试关闭无障碍服务[143523#] | `RC4 加密字符串，用于 ociucqlhfkiqks 无障碍服务（配合预筛 PERFORM_GLOBAL_ACTION 线索）` | 教唆忽视警告 |
| en | sti=009&q=saved_accessibility_events&zip=q1&ws= | （上报参数）状态=009&查询=已保存的无障碍事件&压缩=q1&ws= | `RC4 加密字符串（无障碍事件上报请求参数）` | 隐私承诺 |
| en | error 45235 | 错误 45235 | `drrwfkdgeutko#onStartCommand 中 startActivity 异常分支（RC4 解码所得，仅写日志，不呈现给用户）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：导出服务 drrwfkdgeutko 在 onStartCommand 中 while(true) 循环：每次 sleep(1000) 后复查无障碍状态，未开启即再次 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 并带 NEW_TASK|CLEAR_TOP 等标志，用户按返回键离开会被立刻弹回，直到开启且本地标志 ab=="1" 才退出循环。
- **遮罩叠层 / 高仿系统设置页**：未使用悬浮窗/遮罩/高仿设置页；改用全屏 WebView 引导页 + 反复强拉真实系统无障碍设置页实现同等强制效果。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（包内未出现 ACTION_APPLICATION_DETAILS_SETTINGS，也无「允许受限设置」或 Session 安装器绕过教学）
- **获权后即时行为与防撤权机制**：获权后立即 b.e(Context) 调用 setComponentEnabledSetting 把 LAUNCHER 组件 shxptsks 置为 DISABLED（图标消失）；无障碍服务侧含 "Blocked attempt to disable accessibility service[143523#]" 字符串，配合预筛的 PERFORM_GLOBAL_ACTION，在设置页触发时用 GLOBAL_ACTION_BACK/HOME 返回并阻断撤权，同时自动点击 com.android.permissioncontroller:id/permission_allow_button 与 com.miui.permcenter 权限编辑页控件。
- **良性降级 / 替代方案**：无（非小米设备或条件不满足时直接 finish() 静默退出，属于规避而非降级；未开启无障碍则进入死循环，无任何替代路径）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 com.dfxsdgr.qvoor.shxptsks 冷启动后监测 Activity 栈：一旦 topActivity 变为 com.dfxsdgr.qvoor.ahcgthtk 立即抓取（引导页首帧，文案由远端下发，越早抓越完整）；同时监测 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 的跳转，以及 drrwfkdgeutko 启动后的 1 秒周期重复跳转。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导文案藏于远端配置字段 aO（不落盘），纯静态无法取得逐字原文；非小米机型下应用冷启动即 finish()，在通用模拟器上可能完全观察不到任何界面，UTG 需以小米/MIUI 环境或改机参数复现；此外存在 label="" 的隐形 Activity 与获权后组件禁用，图标消失后需按包名/进程而非桌面入口定位。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导 WebView 页（远端 HTML）** | Activity com.dfxsdgr.qvoor.ahcgthtk，全屏 WebView，JS 桥名 Android，含「启用无障碍」按钮与机型串 | 全部诱导话术都在此页且不落盘，只有运行期才能取得逐字文案，是判定「假更新/故障恐吓」修辞框架的唯一来源 | WebView 文本节点原文（含机型名与更新字样）；页面上是否存在取消/关闭按钮；按钮文案与 DOM 绑定（onclick 是否调用 Android.openAccessibilityService） |
| **系统无障碍服务列表项** | Settings$AccessibilitySettings 中 label=Update、无 description 的条目 | 确认系统侧实际呈现的服务名与「无说明」状态，是身份错配（Google 应用 → Update 服务）的直接证据 | 列表项文本 Update 及其位置；该条目 description 为空；服务开关当前状态 |
| **拒权返回后的重弹循环** | 连续出现 ACCESSIBILITY_SETTINGS 页面栈（间隔约 1 秒），无应用自身界面 | 区分「一次性引导」与「强制死循环」，是判定无取消/无降级的关键动态证据 | 1 秒内重复的 topActivity 相同系统页；返回键后页面回弹时序；循环是否在开启服务后立即停止 |
| **获权后桌面图标消失与设置页被顶回** | 开启 Update 后 LAUNCHER 条目消失；在设置页尝试关闭时被 GLOBAL_ACTION_BACK 顶回 | 验证组件禁用与反撤权，补足「获权后动作」阶段证据 | 桌面无 com.dfxsdgr.qvoor 图标但进程存活；设置页开关操作后焦点被强制移出；权限弹窗自动被点允许 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.dfxsdgr.qvoor.shxptsks#onCreate`
- `com.dfxsdgr.qvoor.ahcgthtk#onCreate`
- `com.dfxsdgr.qvoor.ahcgthtk$c#openAccessibilityService`
- `com.dfxsdgr.qvoor.drrwfkdgeutko#onStartCommand`
- `com.dfxsdgr.qvoor.b#e(android.content.Context)`
- `res/xml/esoh.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（cebruser 家族，`com.dfxsdgr.qvoor`）

**可见性**：代码与流程完整静态可见；**引导页 HTML 正文来自远端或配置下发**，不在包内，包内只有占位符。全部字符串由 RC4（前 12 字符为密钥）、Base64 和十六进制编码三层混淆，已还原。

**无障碍申请链路（纯运行期视角）**

1. **冷启动即入口，但按环境筛选**：[shxptsks#onCreate](<resource-unit:#1.dex1 code:com.dfxsdgr.qvoor.shxptsks#onCreate>) 是 `LAUNCHER` Activity，`label="Google"`。只有 `Build.MANUFACTURER == "xiaomi"` 且版本判定通过时才继续；否则立即 `finish()` 静默退出（其他厂商设备上无可视界面）。
2. **获权判定 + 图标隐藏**：`b.b(this, ociucqlhfkiqks.class)` 判断无障碍是否已开启；已开启则走 `b.e(Context)`，即 `setComponentEnabledSetting(shxptsks, COMPONENT_ENABLED_STATE_DISABLED)`，把桌面图标禁用（变脸、隐身）；未开启则 `startActivity(ahcgthtk.class)`。
3. **引导说明页为 WebView 且启用 JS**：[ahcgthtk#onCreate](<resource-unit:#1.dex1 code:com.dfxsdgr.qvoor.ahcgthtk#onCreate>) 用 `WebSettings.setJavaScriptEnabled(true)`，并向页面注入名为 `Android` 的 JS 桥；正文取自配置字段 `aO`（`loadDataWithBaseURL(null, html, "text/html", ...)`），并把占位符 `%Enable_Accessibility_Service%` 替换为「机型 + 配置串」，同时按系统语言做替换，说明页面文案由服务端下发，可随时改变。
4. **跳转系统无障碍页的唯一点**：页面按钮回调 [ahcgthtk$c#openAccessibilityService](<resource-unit:#1.dex1 code:com.dfxsdgr.qvoor.ahcgthtk$c#openAccessibilityService>) → `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`。**未出现** `ACTION_APPLICATION_DETAILS_SETTINGS`，说明没有 13+ 受限设置分步教学。
5. **拒权死循环**：导出服务 [drrwfkdgeutko#onStartCommand](<resource-unit:#1.dex1 code:com.dfxsdgr.qvoor.drrwfkdgeutko#onStartCommand>) 在 `MANUFACTURER=="xiaomi"` 时 `while(true)`：每 `sleep(1000)` 检查一次，未开启就带 `NEW_TASK|CLEAR_TOP|...` 再次拉起 `ACCESSIBILITY_SETTINGS`，直到「已开启」且本地偏好 `ab=="1"` 才 break——用户返回或拒绝会被每秒重新弹回，无取消、无跳过。
6. **获权后动作**：进入 `e.a(this)` 隐藏图标；服务端侧出现 `sti=009&q=saved_accessibility_events&zip=q1&ws=`（无障碍事件上报参数）与 `com.android.permissioncontroller:id/permission_allow_button`、`com.miui.permcenter...PermissionsEditorActivity` 控件 id，即获权后自动点权限弹窗、上传抓取的无障碍事件；另有字符串 `Blocked attempt to disable accessibility service[143523#]` 与预筛的 `PERFORM_GLOBAL_ACTION` 线索一致，用于阻止撤权。

**身份伪装**：桌面名 `Google`、无障碍列表项标签 `Update`、包名随机乱序、`android:description` 缺失（系统列表里无任何说明）、配置 `res/xml/esoh.xml` 仅声明 `typeWindowContentChanged|typeWindowStateChanged` + `canRetrieveWindowContent`，无 `isAccessibilityTool`。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "DEX 全部逻辑静态可见（字符串为 RC4+Base64+Hex 三层编码，已还原）；引导页 HTML 正文不落盘，由配置字段 aO 在运行期提供，包内仅有占位符 %Enable_Accessibility_Service%，故引导文案确切措辞需运行期抓取 WebView 才能逐字确认。",
  "summary_one_liner": "小米设备冷启动即弹出由远端配置生成的 WebView「更新」引导页，经 JS 桥一键跳转系统无障碍设置，并由导出服务每秒死循环重拉设置页直到用户开启名为 Update 的无障碍服务，获权后禁用桌面图标并监听/阻止撤权。",
  "disguise_identity": {
    "app_display_name": "Google",
    "claimed_brand_or_persona": "Google（桌面名直接冒用 Google 品牌）+ 系统「Update」更新提示",
    "a11y_service_label": "Update",
    "identity_mismatch": true,
    "obfuscation_tricks": "桌面名冒用 Google，无障碍服务名伪装为系统更新 Update；android:description 完全缺失（系统无障碍列表无任何说明，用户无从判断用途）；包名 com.dfxsdgr.qvoor 与类名均为随机乱序字符串；所有文案字符串 RC4 加密存放；LAUNCHER 组件在获权后被 setComponentEnabledSetting 禁用，使桌面图标消失；另有 label=\"\" 且 excludeFromRecents 的 Theme.NoDisplay Activity（toe/iwmyer/azdncjcmq）作为隐形入口。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.dfxsdgr.qvoor.shxptsks（LAUNCHER Activity，label=Google）",
      "trigger_event": "用户点击桌面图标触发 onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Google",
      "shown_text_zh": "桌面图标与任务名显示为「Google」",
      "user_action_requested": "点击桌面图标启动（无任何系统提示）",
      "code_anchor": "com.dfxsdgr.qvoor.shxptsks#onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "shxptsks#onCreate 内的环境与授权判定分支",
      "trigger_event": "onCreate 中 Build.MANUFACTURER 与版本判定、b.b(this, ociucqlhfkiqks.class) 无障碍启用检查",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（非 xiaomi 设备直接 finish()，无任何界面）",
      "shown_text_zh": "非小米机型静默退出，界面上什么都不显示",
      "user_action_requested": "无",
      "code_anchor": "com.dfxsdgr.qvoor.shxptsks#onCreate / com.dfxsdgr.qvoor.b#b"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.dfxsdgr.qvoor.ahcgthtk（全屏 WebView Activity，JS 已启用，注入 Android 桥）",
      "trigger_event": "shxptsks#onCreate 检测到无障碍未开启后 startActivity(ahcgthtk)",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "%Enable_Accessibility_Service%（占位符，运行期被替换为「Build.MODEL + 配置串」；HTML 正文由配置字段 aO 下发，包内无落盘副本）",
      "shown_text_zh": "由服务端下发的「启用无障碍服务」说明页文案，含机型名以伪造系统原生提示观感",
      "user_action_requested": "按页面提示点击按钮开启无障碍（页面由远端配置决定是否提供取消入口，包内未见关闭按钮实现）",
      "code_anchor": "com.dfxsdgr.qvoor.ahcgthtk#onCreate"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "WebView 内 JS 调用 Android.openAccessibilityService()（@JavascriptInterface）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接打开系统无障碍服务列表，用户需在其中找到并开启名为「Update」的条目",
      "user_action_requested": "在系统列表中点击 Update 并确认开启；应用自身不提供取消/跳过",
      "code_anchor": "com.dfxsdgr.qvoor.ahcgthtk$c#openAccessibilityService"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.dfxsdgr.qvoor.drrwfkdgeutko（exported Service）onStartCommand 的 while(true) 循环",
      "trigger_event": "服务被启动后进入无限循环，每 sleep(1000) 复查一次无障碍状态",
      "ui_carrier": "系统无障碍页（被反复重新拉起）",
      "shown_text_verbatim": "error 45235（异常分支日志串）；循环内无任何提示文案",
      "shown_text_zh": "用户返回或拒绝后，每秒再次把无障碍设置页弹到前台，无法通过返回键摆脱",
      "user_action_requested": "必须开启无障碍服务才能跳出循环，无取消、无跳过",
      "code_anchor": "com.dfxsdgr.qvoor.drrwfkdgeutko#onStartCommand"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.dfxsdgr.qvoor.ociucqlhfkiqks（无障碍服务，label=Update）onServiceConnected / onAccessibilityEvent；b.e(Context) 禁用 LAUNCHER 组件",
      "trigger_event": "无障碍开启后 shxptsks#onCreate 或 drrwfkdgeutko 循环调用 e.a(this) 与 b.e(Context)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Blocked attempt to disable accessibility service[143523#]；sti=009&q=saved_accessibility_events&zip=q1&ws=",
      "shown_text_zh": "记录并阻止用户关闭无障碍服务，同时把采集到的无障碍事件打包上传服务端",
      "user_action_requested": "无（后台自动执行，桌面图标随后被隐藏）",
      "code_anchor": "com.dfxsdgr.qvoor.ociucqlhfkiqks#onAccessibilityEvent / com.dfxsdgr.qvoor.b#e(android.content.Context)"
    }
  ],
  "text_presentation_locations": [
    "桌面图标/任务标签：AndroidManifest 中 application android:label=\"Google\"（shxptsks 为 LAUNCHER）",
    "系统无障碍服务列表项：service android:label=\"Update\"，android:description 完全缺失（无说明文字）",
    "全屏 WebView 引导页：com.dfxsdgr.qvoor.ahcgthtk 用 loadDataWithBaseURL(null, <配置字段 aO 下发的 HTML>, \"text/html\") 渲染，含占位符 %Enable_Accessibility_Service% 被替换为「机型 + 配置串」",
    "跳转系统设置后：无遮罩、无悬浮窗引导，仅靠 drrwfkdgeutko 每秒重复 startActivity 把系统无障碍页重新压到前台",
    "隐形入口 Activity：toe / iwmyer / azdncjcmq 均为 label=\"\" + excludeFromRecents（iwmyer、azdncjcmq 使用 icon=@drawable/mpftf 伪装图标）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Update",
      "text_zh": "更新",
      "source_location": "AndroidManifest.xml：service com.dfxsdgr.qvoor.ociucqlhfkiqks 的 android:label（经 RC4 解码后原文亦为 Update）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Google",
      "text_zh": "谷歌",
      "source_location": "AndroidManifest.xml：application android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "%Enable_Accessibility_Service%",
      "text_zh": "（占位符）启用无障碍服务",
      "source_location": "ahcgthtk#onCreate 中经 RC4 解码得到的 HTML 占位符，运行期替换为「Build.MODEL + 配置串 ai」",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Blocked attempt to disable accessibility service[143523#]",
      "text_zh": "已阻止尝试关闭无障碍服务[143523#]",
      "source_location": "RC4 加密字符串，用于 ociucqlhfkiqks 无障碍服务（配合预筛 PERFORM_GLOBAL_ACTION 线索）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "sti=009&q=saved_accessibility_events&zip=q1&ws=",
      "text_zh": "（上报参数）状态=009&查询=已保存的无障碍事件&压缩=q1&ws=",
      "source_location": "RC4 加密字符串（无障碍事件上报请求参数）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "error 45235",
      "text_zh": "错误 45235",
      "source_location": "drrwfkdgeutko#onStartCommand 中 startActivity 异常分支（RC4 解码所得，仅写日志，不呈现给用户）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "导出服务 drrwfkdgeutko 在 onStartCommand 中 while(true) 循环：每次 sleep(1000) 后复查无障碍状态，未开启即再次 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 并带 NEW_TASK|CLEAR_TOP 等标志，用户按返回键离开会被立刻弹回，直到开启且本地标志 ab==\"1\" 才退出循环。",
    "overlay_or_fake_settings": "未使用悬浮窗/遮罩/高仿设置页；改用全屏 WebView 引导页 + 反复强拉真实系统无障碍设置页实现同等强制效果。",
    "restricted_settings_13plus_coaching": "无（包内未出现 ACTION_APPLICATION_DETAILS_SETTINGS，也无「允许受限设置」或 Session 安装器绕过教学）",
    "post_grant_anti_removal": "获权后立即 b.e(Context) 调用 setComponentEnabledSetting 把 LAUNCHER 组件 shxptsks 置为 DISABLED（图标消失）；无障碍服务侧含 \"Blocked attempt to disable accessibility service[143523#]\" 字符串，配合预筛的 PERFORM_GLOBAL_ACTION，在设置页触发时用 GLOBAL_ACTION_BACK/HOME 返回并阻断撤权，同时自动点击 com.android.permissioncontroller:id/permission_allow_button 与 com.miui.permcenter 权限编辑页控件。",
    "benign_graceful_degradation": "无（非小米设备或条件不满足时直接 finish() 静默退出，属于规避而非降级；未开启无障碍则进入死循环，无任何替代路径）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 com.dfxsdgr.qvoor.shxptsks 冷启动后监测 Activity 栈：一旦 topActivity 变为 com.dfxsdgr.qvoor.ahcgthtk 立即抓取（引导页首帧，文案由远端下发，越早抓越完整）；同时监测 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 的跳转，以及 drrwfkdgeutko 启动后的 1 秒周期重复跳转。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导 WebView 页（远端 HTML）",
        "page_identifier": "Activity com.dfxsdgr.qvoor.ahcgthtk，全屏 WebView，JS 桥名 Android，含「启用无障碍」按钮与机型串",
        "why_most_useful": "全部诱导话术都在此页且不落盘，只有运行期才能取得逐字文案，是判定「假更新/故障恐吓」修辞框架的唯一来源",
        "observable_utg_signals": ["WebView 文本节点原文（含机型名与更新字样）", "页面上是否存在取消/关闭按钮", "按钮文案与 DOM 绑定（onclick 是否调用 Android.openAccessibilityService）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings$AccessibilitySettings 中 label=Update、无 description 的条目",
        "why_most_useful": "确认系统侧实际呈现的服务名与「无说明」状态，是身份错配（Google 应用 → Update 服务）的直接证据",
        "observable_utg_signals": ["列表项文本 Update 及其位置", "该条目 description 为空", "服务开关当前状态"]
      },
      {
        "page_role": "拒权返回后的重弹循环",
        "page_identifier": "连续出现 ACCESSIBILITY_SETTINGS 页面栈（间隔约 1 秒），无应用自身界面",
        "why_most_useful": "区分「一次性引导」与「强制死循环」，是判定无取消/无降级的关键动态证据",
        "observable_utg_signals": ["1 秒内重复的 topActivity 相同系统页", "返回键后页面回弹时序", "循环是否在开启服务后立即停止"]
      },
      {
        "page_role": "获权后桌面图标消失与设置页被顶回",
        "page_identifier": "开启 Update 后 LAUNCHER 条目消失；在设置页尝试关闭时被 GLOBAL_ACTION_BACK 顶回",
        "why_most_useful": "验证组件禁用与反撤权，补足「获权后动作」阶段证据",
        "observable_utg_signals": ["桌面无 com.dfxsdgr.qvoor 图标但进程存活", "设置页开关操作后焦点被强制移出", "权限弹窗自动被点允许"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导文案藏于远端配置字段 aO（不落盘），纯静态无法取得逐字原文；非小米机型下应用冷启动即 finish()，在通用模拟器上可能完全观察不到任何界面，UTG 需以小米/MIUI 环境或改机参数复现；此外存在 label=\"\" 的隐形 Activity 与获权后组件禁用，图标消失后需按包名/进程而非桌面入口定位。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.dfxsdgr.qvoor.shxptsks#onCreate",
    "com.dfxsdgr.qvoor.ahcgthtk#onCreate",
    "com.dfxsdgr.qvoor.ahcgthtk$c#openAccessibilityService",
    "com.dfxsdgr.qvoor.drrwfkdgeutko#onStartCommand",
    "com.dfxsdgr.qvoor.b#e(android.content.Context)",
    "res/xml/esoh.xml"
  ]
}
```

**说明与边界**：本次受 14 次调用上限约束，已超出硬性预算即停止，故未调用 `record_risk` 写入项目风险台账；上述结论（诱导无障碍 + 拒权死循环 + 获权后隐藏图标与反撤权）证据链完整，建议按 `malware_trojan`（高危）与 `deceptive_behavior` 分别登记。未展开项：`ociucqlhfkiqks#onAccessibilityEvent`（2706 条指令）的具体按键注入/回传细节、以及 `drrwfkdgeutko` 的调用方（哪个组件 startService 它）尚未静态定位。

</details>

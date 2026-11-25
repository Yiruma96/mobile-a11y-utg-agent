# MR_022__48e72d70d4｜Ztorg — fast game

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：109.4s

## 1. 一句话核心结论

- **核心申请方式**：无任何应用内引导页或弹窗，由后台服务在启动后延迟 10 秒自动拉起系统无障碍设置页，仅靠系统列表里一条伪称“隐私保护功能”的描述文案完成诱导，用户开启后服务立即跳回桌面隐藏。
- **静态可见性说明**：无加壳、无 AES/密文载荷、无远端 HTML；无障碍诱导链（StartAdService.initHandler → StartAdService$1.run → ACCESSIBILITY_SETTINGS）与描述文案全部静态完整可见。唯一未完全追清的是 StartAdService 的启动上游（MainActivity 启动的 com.edcf.MyService 在该 dex 中未检索到类体），但不影响跳转链本身的可达性与判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `48e72d70d48eaaa429504178c21c8f253b3198ea8fe48719346c926ba7f9b243` |
| 包名 / 年份 | `com.rxhl.poiu` / 2017 |
| 家族 / 品类 | **Ztorg**（同池样本数：5） |
| 原始来源标识 | https://securelist.com/ztorg-from-rooting-to-sms/78775/ |
| 桌面显示名 | fast game |
| 引导页宣称品牌/身份 | 系统级“隐私保护功能”（防信息泄露、防窃取、防他人窥探隐私） |
| 系统无障碍列表服务名 | fast game |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：服务标签与桌面名同为游戏名 fast game，而 android:description 伪称系统隐私保护功能，名实错配；MainActivity 冷启动即调用 setComponentEnabledSetting(cm, 2, 1) 禁用自身 Launcher 组件使图标消失；无多 activity-alias、无同形字、无空白换行挤出警告、无伪造 isAccessibilityTool（targetSdk 22 早于该机制） |
| 无障碍服务类名 | `com.example.adService.OpenFuzhuAccess` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_SMS, RECEIVE_SMS, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Please open the privacy protection function, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.example.my_pay.MainActivity | LAUNCHER 入口 onCreate | 原生Activity | 无 | 无需用户操作；应用同时启动 com.edcf.MyService 并禁用自身 Launcher 组件 | `com.example.my_pay.MainActivity.onCreate / com.example.my_pay.MainActivity.init` |
| 2 | 业务功能触发 | com.example.adService.StartAdService（后台服务） | onStartCommand → initHandler() 投递 Handler.postDelayed(..., 10000L) | 不可静态还原 | 无 | 无 | `com.example.adService.StartAdService.onStartCommand / StartAdService.initHandler` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | StartAdService$1.run() 中 OpenFuzhuAccess.isRunning() 返回 false | 系统无障碍页 | 无 | 要求用户自行在系统列表中找到 fast game 并打开开关（应用未提供任何定位高亮） | `com.example.adService.StartAdService$1.run` |
| 4 | 引导说明页 | 系统无障碍服务列表中的服务条目描述（res/xml/service_config.xml 引用 strings） | 系统读取 meta-data android.accessibilityservice 配置渲染列表项 | 系统无障碍页 | **原文**：Please open the privacy protection function, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy.<br>**译注**：请开启隐私保护功能，保护您的信息不被泄露、不被窃取，防止他人窥探您的隐私。 | 促使用户相信这是系统隐私保护功能并点开开关 | `res/values/strings.xml service_config_desc / res/xml/service_config.xml` |
| 5 | 获权后动作 | com.example.adService.OpenFuzhuAccess.onServiceConnected | 用户在系统设置中勾选该服务，系统绑定无障碍服务并回调 onServiceConnected | 通知栏 | **原文**：服务已连接<br>**译注**：Toast 提示“服务已连接”，随后以 ACTION_MAIN + CATEGORY_HOME + FLAG_ACTIVITY_NEW_TASK 跳回桌面 | 无需操作；应用主动结束授权现场，用户被弹回桌面 | `com.example.adService.OpenFuzhuAccess.onServiceConnected` |
| 6 | 拒权反馈循环 | com.example.adService.StartAdService（下一次服务启动） | 用户返回或未开启，isRunning() 持续为 false，服务每次启动后 10 秒再次执行 StartAdService$1.run() | 系统无障碍页 | 无 | 用户只能反复按返回退出，或被再次带到设置页 | `com.example.adService.StartAdService.initHandler / com.example.adService.OpenFuzhuAccess.isRunning` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表中的服务条目描述栏：strings.xml 的 service_config_desc（由 res/xml/service_config.xml 的 android:description 引用），是唯一出现“隐私保护功能”话术的位置
- 系统无障碍服务列表中的服务名称：service 的 android:label=@string/app_name，显示为 fast game
- Toast 提示（获权瞬间）：OpenFuzhuAccess.onServiceConnected 中硬编码 "服务已连接"
- 应用主界面 activity_main：无任何引导/说明文字，btn_open_native 的点击回调为空实现
- 未发现任何 WebView（本地或远端 HTML）、悬浮窗遮罩、GIF/图片引导、原生 Dialog 或自定义高仿设置页承载说明文字

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please open the privacy protection function, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy. | 请开启隐私保护功能，保护您的信息不被泄露、不被窃取，防止他人窥探您的隐私。 | `res/values/strings.xml key=service_config_desc（经 res/xml/service_config.xml android:description 引用）` | 隐私承诺 |
| zh | 服务已连接 | 服务已连接 | `com.example.adService.OpenFuzhuAccess.onServiceConnected（硬编码 Toast）` | 未知 |
| en | fast game | 快速游戏 | `res/values/strings.xml key=app_name（同时作为无障碍服务 android:label）` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无 onResume 死循环、无定时强拉前台；但 isRunning() 在每次 StartAdService 启动后均被重新判定，未开启则在 10 秒后再次 startActivity(ACCESSIBILITY_SETTINGS)，形成跨启动的静默重跳，且跳转前不给任何解释或降级提示
- **遮罩叠层 / 高仿系统设置页**：无。未发现半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 权限存在但诱导链未使用
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无 GLOBAL_ACTION_BACK/HOME 阻止撤权逻辑；但获权瞬间即跳转 HOME 隐藏授权现场，随后在 onAccessibilityEvent 中监听 com.android.vending 事件与“安装成功”通知并 pendingIntent.send() 自动点击确认，用于静默安装确认
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（且调用方包为 com.rxhl.poiu、FLAG_ACTIVITY_NEW_TASK）的瞬间开始连续抓帧；同时在冷启动 MainActivity 后等待约 10 秒窗口，覆盖 StartAdService.initHandler 的延迟跳转时机
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：盲区主要在“跳转上游”：StartAdService 由 MainActivity 启动的 com.edcf.MyService 间接拉起，该类在本 dex 中未检索到类体，若 UTG 仅在冷启动后短暂观测，可能错过 10 秒延迟后的跳转窗口；建议观测窗口延长至冷启动后 20 秒以上。另无纯图空文本、无远端 HTML、无加壳，静态可见性良好。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动主界面页** | com.example.my_pay.MainActivity，activity_main 布局，仅一个 btn_open_native 按钮、无说明文字 | 证明应用自身没有任何前置说明或授权理由页，权限请求完全脱离用户可见上下文 | 页面无可点击的隐私政策/权限说明入口；存在空白功能的按钮控件；无任何含 accessibility 字样的引导文案 |
| **系统无障碍服务列表项** | Settings 无障碍页中 label 为 fast game 的条目，描述为 Please open the privacy protection function... | 话术与真实用途错配的唯一证据落点，且是用户做授权决策的唯一信息源 | 服务名 fast game 与描述“隐私保护功能”语义冲突；描述提及防泄露/防窃取/防窥探的隐私承诺；开关初始为关闭 |
| **获权后返回桌面瞬间** | Toast “服务已连接” + Launcher 桌面（ACTION_MAIN/CATEGORY_HOME） | 证明应用在拿到权限后立即撤离现场，不做任何使用说明或权限用途提示 | 授权后 1-2 秒内界面变为桌面；短暂 Toast 文本“服务已连接”；前台应用变为 launcher 而非 com.rxhl.poiu |
| **拒权后重跳页** | 从设置页返回后再次出现的系统无障碍设置页 | 区分“一次性请求”与“条件式静默重跳”行为，是判定强制性的关键 | 返回后再次进入同一 settings 页面；两次跳转间隔约 10 秒且无中间提示；无任何取消/跳过控件 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.example.adService.StartAdService.initHandler`
- `com.example.adService.StartAdService$1.run`
- `com.example.adService.OpenFuzhuAccess.isRunning`
- `com.example.adService.OpenFuzhuAccess.onServiceConnected`
- `com.example.my_pay.MainActivity.onCreate`
- `res/values/strings.xml (service_config_desc / app_name) + res/xml/service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，纯运行期 UTG 视角）

**核心发现：该应用没有任何“引导页面”，完全依靠后台服务定时强制跳转到系统无障碍设置页。**

1. **冷启动**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.example.my_pay.MainActivity#onCreate>) 只执行 `setContentView(activity_main)`、初始化 `AdSDK`、`startService(MyService)`，随后立即调用 `pm.setComponentEnabledSetting(cm, 2, 1)`，**禁用自身 Launcher 组件，让应用从桌面消失**。布局里的 `btn_open_native` 点击回调 [MainActivity$1.onClick()](<resource-unit:#1.dex1 code:com.example.my_pay.MainActivity$1#onClick>) 是**空方法体**，主界面没有任何功能入口或说明文字。
2. **唯一跳转点**：[StartAdService.onStartCommand()](<resource-unit:#1.dex1 code:com.example.adService.StartAdService#onStartCommand>) 调用 [initHandler()](<resource-unit:#1.dex1 code:com.example.adService.StartAdService#initHandler>)，用 `postDelayed(..., 10000L)` 延迟 10 秒后执行 [StartAdService$1.run()](<resource-unit:#1.dex1 code:com.example.adService.StartAdService$1#run>)：如果 `OpenFuzhuAccess.isRunning()` 为 false，就执行 `new Intent("android.settings.ACCESSIBILITY_SETTINGS")` 并加上 `FLAG_ACTIVITY_NEW_TASK`，直接进入系统无障碍设置页。**没有弹窗，没有确认，没有取消按钮，也没有图文教学。**
3. **判定方式**：[OpenFuzhuAccess.isRunning()](<resource-unit:#1.dex1 code:com.example.adService.OpenFuzhuAccess#isRunning>) 用 `AccessibilityManager.getEnabledAccessibilityServiceList(16)` 比对 `getServiceInfo().getId()`，能准确判断“我是否已被勾选”，这说明跳转是**条件式重复触发**：只要没开启，每次服务启动后都会再跳。
4. **话术载体只在系统页**：`service_config_desc` 位于 [strings.xml L12](<resource-unit:#1 file:res/values/strings.xml#L12-L12>)，宣称“隐私保护功能，防信息泄露、防窃取、防偷窥”；服务标签 `android:label` 与桌面名同为 `fast game`（[strings.xml L9](<resource-unit:#1 file:res/values/strings.xml#L9-L9>)）；而 [service_config.xml](<resource-unit:#1 file:res/xml/service_config.xml#L1-L3>) 声明 `canRetrieveWindowContent="true"`、`accessibilityEventTypes="typeAllMask"`。描述与实际能力严重不符。
5. **获权后**：[onServiceConnected()](<resource-unit:#1.dex1 code:com.example.adService.OpenFuzhuAccess#onServiceConnected>) 弹出 `Toast "服务已连接"`，随后以 `ACTION_MAIN + CATEGORY_HOME + NEW_TASK` 跳回桌面，**立即隐藏授权现场**；服务接着在 `onAccessibilityEvent` 中监听 `com.android.vending` 事件与“安装成功”通知，并调用 `pendingIntent.send()` 自动点击。
6. **未发现的部分**：代码中不存在 `ACTION_APPLICATION_DETAILS_SETTINGS`、13+ 受限设置分步教学、Session 安装器话术、半透明遮罩引导窗、高仿设置页或 `GLOBAL_ACTION_BACK` 阻止撤权的逻辑。同一服务另有 [StartAdService$4.run()](<resource-unit:#1.dex1 code:com.example.adService.StartAdService$4#run>) 以 1 秒周期轮询前台任务，条件满足即拉起 `ChaPingActivity` 插屏广告，这与无障碍诱导属于不同链条。

已登记风险 **R-001**（deceptive_behavior / high）：以“隐私保护功能”名义自动跳转无障碍设置页诱导开启无障碍服务。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无加壳、无 AES/密文载荷、无远端 HTML；无障碍诱导链（StartAdService.initHandler → StartAdService$1.run → ACCESSIBILITY_SETTINGS）与描述文案全部静态完整可见。唯一未完全追清的是 StartAdService 的启动上游（MainActivity 启动的 com.edcf.MyService 在该 dex 中未检索到类体），但不影响跳转链本身的可达性与判定。",
  "summary_one_liner": "无任何应用内引导页或弹窗，由后台服务在启动后延迟 10 秒自动拉起系统无障碍设置页，仅靠系统列表里一条伪称“隐私保护功能”的描述文案完成诱导，用户开启后服务立即跳回桌面隐藏。",
  "disguise_identity": {
    "app_display_name": "fast game",
    "claimed_brand_or_persona": "系统级“隐私保护功能”（防信息泄露、防窃取、防他人窥探隐私）",
    "a11y_service_label": "fast game",
    "identity_mismatch": true,
    "obfuscation_tricks": "服务标签与桌面名同为游戏名 fast game，而 android:description 伪称系统隐私保护功能，名实错配；MainActivity 冷启动即调用 setComponentEnabledSetting(cm, 2, 1) 禁用自身 Launcher 组件使图标消失；无多 activity-alias、无同形字、无空白换行挤出警告、无伪造 isAccessibilityTool（targetSdk 22 早于该机制）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.example.my_pay.MainActivity",
      "trigger_event": "LAUNCHER 入口 onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "仅有 activity_main 布局与一个 btn_open_native 按钮，无任何功能说明或权限引导文字",
      "user_action_requested": "无需用户操作；应用同时启动 com.edcf.MyService 并禁用自身 Launcher 组件",
      "code_anchor": "com.example.my_pay.MainActivity.onCreate / com.example.my_pay.MainActivity.init"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.example.adService.StartAdService（后台服务）",
      "trigger_event": "onStartCommand → initHandler() 投递 Handler.postDelayed(..., 10000L)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台静默计时 10 秒，期间不出现任何界面或提示",
      "user_action_requested": "无",
      "code_anchor": "com.example.adService.StartAdService.onStartCommand / StartAdService.initHandler"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "StartAdService$1.run() 中 OpenFuzhuAccess.isRunning() 返回 false",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接以 FLAG_ACTIVITY_NEW_TASK 拉起系统无障碍设置列表，无前置确认、无取消/跳过按钮",
      "user_action_requested": "要求用户自行在系统列表中找到 fast game 并打开开关（应用未提供任何定位高亮）",
      "code_anchor": "com.example.adService.StartAdService$1.run"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "系统无障碍服务列表中的服务条目描述（res/xml/service_config.xml 引用 strings）",
      "trigger_event": "系统读取 meta-data android.accessibilityservice 配置渲染列表项",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Please open the privacy protection function, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy.",
      "shown_text_zh": "请开启隐私保护功能，保护您的信息不被泄露、不被窃取，防止他人窥探您的隐私。",
      "user_action_requested": "促使用户相信这是系统隐私保护功能并点开开关",
      "code_anchor": "res/values/strings.xml service_config_desc / res/xml/service_config.xml"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.example.adService.OpenFuzhuAccess.onServiceConnected",
      "trigger_event": "用户在系统设置中勾选该服务，系统绑定无障碍服务并回调 onServiceConnected",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "服务已连接",
      "shown_text_zh": "Toast 提示“服务已连接”，随后以 ACTION_MAIN + CATEGORY_HOME + FLAG_ACTIVITY_NEW_TASK 跳回桌面",
      "user_action_requested": "无需操作；应用主动结束授权现场，用户被弹回桌面",
      "code_anchor": "com.example.adService.OpenFuzhuAccess.onServiceConnected"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.example.adService.StartAdService（下一次服务启动）",
      "trigger_event": "用户返回或未开启，isRunning() 持续为 false，服务每次启动后 10 秒再次执行 StartAdService$1.run()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何“为何需要此权限”的解释页或温和降级提示，仅静默重复拉起同一设置页",
      "user_action_requested": "用户只能反复按返回退出，或被再次带到设置页",
      "code_anchor": "com.example.adService.StartAdService.initHandler / com.example.adService.OpenFuzhuAccess.isRunning"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表中的服务条目描述栏：strings.xml 的 service_config_desc（由 res/xml/service_config.xml 的 android:description 引用），是唯一出现“隐私保护功能”话术的位置",
    "系统无障碍服务列表中的服务名称：service 的 android:label=@string/app_name，显示为 fast game",
    "Toast 提示（获权瞬间）：OpenFuzhuAccess.onServiceConnected 中硬编码 \"服务已连接\"",
    "应用主界面 activity_main：无任何引导/说明文字，btn_open_native 的点击回调为空实现",
    "未发现任何 WebView（本地或远端 HTML）、悬浮窗遮罩、GIF/图片引导、原生 Dialog 或自定义高仿设置页承载说明文字"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please open the privacy protection function, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy.",
      "text_zh": "请开启隐私保护功能，保护您的信息不被泄露、不被窃取，防止他人窥探您的隐私。",
      "source_location": "res/values/strings.xml key=service_config_desc（经 res/xml/service_config.xml android:description 引用）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "zh",
      "text_verbatim": "服务已连接",
      "text_zh": "服务已连接",
      "source_location": "com.example.adService.OpenFuzhuAccess.onServiceConnected（硬编码 Toast）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "fast game",
      "text_zh": "快速游戏",
      "source_location": "res/values/strings.xml key=app_name（同时作为无障碍服务 android:label）",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无 onResume 死循环、无定时强拉前台；但 isRunning() 在每次 StartAdService 启动后均被重新判定，未开启则在 10 秒后再次 startActivity(ACCESSIBILITY_SETTINGS)，形成跨启动的静默重跳，且跳转前不给任何解释或降级提示",
    "overlay_or_fake_settings": "无。未发现半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 权限存在但诱导链未使用",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无 GLOBAL_ACTION_BACK/HOME 阻止撤权逻辑；但获权瞬间即跳转 HOME 隐藏授权现场，随后在 onAccessibilityEvent 中监听 com.android.vending 事件与“安装成功”通知并 pendingIntent.send() 自动点击确认，用于静默安装确认",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（且调用方包为 com.rxhl.poiu、FLAG_ACTIVITY_NEW_TASK）的瞬间开始连续抓帧；同时在冷启动 MainActivity 后等待约 10 秒窗口，覆盖 StartAdService.initHandler 的延迟跳转时机",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动主界面页",
        "page_identifier": "com.example.my_pay.MainActivity，activity_main 布局，仅一个 btn_open_native 按钮、无说明文字",
        "why_most_useful": "证明应用自身没有任何前置说明或授权理由页，权限请求完全脱离用户可见上下文",
        "observable_utg_signals": ["页面无可点击的隐私政策/权限说明入口", "存在空白功能的按钮控件", "无任何含 accessibility 字样的引导文案"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中 label 为 fast game 的条目，描述为 Please open the privacy protection function...",
        "why_most_useful": "话术与真实用途错配的唯一证据落点，且是用户做授权决策的唯一信息源",
        "observable_utg_signals": ["服务名 fast game 与描述“隐私保护功能”语义冲突", "描述提及防泄露/防窃取/防窥探的隐私承诺", "开关初始为关闭"]
      },
      {
        "page_role": "获权后返回桌面瞬间",
        "page_identifier": "Toast “服务已连接” + Launcher 桌面（ACTION_MAIN/CATEGORY_HOME）",
        "why_most_useful": "证明应用在拿到权限后立即撤离现场，不做任何使用说明或权限用途提示",
        "observable_utg_signals": ["授权后 1-2 秒内界面变为桌面", "短暂 Toast 文本“服务已连接”", "前台应用变为 launcher 而非 com.rxhl.poiu"]
      },
      {
        "page_role": "拒权后重跳页",
        "page_identifier": "从设置页返回后再次出现的系统无障碍设置页",
        "why_most_useful": "区分“一次性请求”与“条件式静默重跳”行为，是判定强制性的关键",
        "observable_utg_signals": ["返回后再次进入同一 settings 页面", "两次跳转间隔约 10 秒且无中间提示", "无任何取消/跳过控件"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "盲区主要在“跳转上游”：StartAdService 由 MainActivity 启动的 com.edcf.MyService 间接拉起，该类在本 dex 中未检索到类体，若 UTG 仅在冷启动后短暂观测，可能错过 10 秒延迟后的跳转窗口；建议观测窗口延长至冷启动后 20 秒以上。另无纯图空文本、无远端 HTML、无加壳，静态可见性良好。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH"
  ],
  "code_anchors": [
    "com.example.adService.StartAdService.initHandler",
    "com.example.adService.StartAdService$1.run",
    "com.example.adService.OpenFuzhuAccess.isRunning",
    "com.example.adService.OpenFuzhuAccess.onServiceConnected",
    "com.example.my_pay.MainActivity.onCreate",
    "res/values/strings.xml (service_config_desc / app_name) + res/xml/service_config.xml"
  ]
}
```

</details>

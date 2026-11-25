# MR_153__3ba889748c｜RuMMS — СМC - Сообщениe

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：113.9s

## 1. 一句话核心结论

- **核心申请方式**：应用冷启动即静默退场，由 Application 启动的 1 秒轮询 Runnable 每约 10 秒强制拉起一个只显示俄文故障 Toast 的 Activity 并跳转系统无障碍设置页，无取消入口、拒绝后无限重跳，服务名与文案用同形字伪装成'主进程/统计访问'，获权后由无障碍服务自动点击确认键并回退界面。
- **静态可见性说明**：引导链路全部位于 classes.dex 与 res/values/strings.xml、res/xml/reiamt.xml 中，无 WebView/HTML/远端下发，无需脱壳即可完整还原；仅 d.f(Context) 判定无障碍是否启用的具体实现细节未逐行展开（据调用语义为已启用则返回 true 并跳过拉起）。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3ba889748c9a431f241eb64784e78c08194e488724a9746d6a582a6275dfa4a6` |
| 包名 / 年份 | `ru.shift.element` / 2018 |
| 家族 / 品类 | **RuMMS**（同池样本数：516） |
| 原始来源标识 | https://www.zscaler.com/blogs/security-research/rumms-malware-back-enhancements |
| 桌面显示名 | СМC - Сообщениe |
| 引导页宣称品牌/身份 | 冒充系统短信应用（СМС - Сообщение）并以'系统统计访问权限'名义索取无障碍 |
| 系统无障碍列表服务名 | Оcновнoй прoцeсс |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：同形字混写：服务名 Оcновнoй прoцeсс 与文案 Сиcтемa/стaтистикe 中混用拉丁 c、o、a 与西里尔字母，绕过字符串比对与人工肉眼识别；无障碍服务以'主进程'命名冒充系统组件；accessibility_desc 中不含'无障碍'字样而以'统计访问'替代；入口 Activity OfferHang 冷启动即 finish()，桌面无可见界面；未声明 android:description 的规范用途说明，仅通过 Toast 呈现引导文本。 |
| 无障碍服务类名 | `ru.shift.element.MethodPaint` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | ru.shift.element.OfferHang（LAUNCHER Activity，Theme.Translucent.NoTitleBar.Fullscreen） | 用户点击桌面图标 → Activity.onCreate | 原生Activity | **原文**：无（onCreate 直接调用 finish()，不加载任何布局）<br>**译注**：无界面，闪退式静默退场 | 无需操作；用户看不到任何应用界面，无法在此步取消 | `ru.shift.element.OfferHang.onCreate` |
| 2 | 业务功能触发 | ru.shift.element.Demand（Application）+ ru.shift.element.VarietyFew（前台服务）+ Demand$1（Runnable，postDelayed 1072ms 自循环） | Application.onCreate → startForegroundService/startService(VarietyFew) 并启动 1072ms 轮询 | 不可静态还原（后台无界面） | 无 | 无 | `ru.shift.element.Demand.onCreate / ru.shift.element.Demand$1.run` |
| 3 | 跳无障碍设置 | ru.shift.element.Criminal（无 intent-filter 的隐藏 Activity，由后台 startActivity 拉起） | Demand$1.run 每轮调用 d.b(ctx, now)；未启用无障碍时 d.c() 以 10242ms 节流 startActivity(Criminal) → Criminal.onCreate | 原生Activity | **原文**：Toast: "Сиcтемa нe кoрректно работаeт, вaм неoбхoдимо включить доcтуп к стaтистикe для 'Оcновнoй прoцeсс'"<br>**译注**：系统运行不正常，您需要为'主进程'开启统计访问权限 | 无任何按钮；Toast 后立即 startActivity("android.settings.ACCESSIBILITY_SETTINGS") 并 finish()，用户被直接带到系统无障碍服务列表 | `ru.shift.element.Criminal.onCreate / res/values/strings.xml#accessibility_desc` |
| 4 | 遮罩叠层指引 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（应用未叠加任何引导层） | 系统无障碍列表渲染 | 系统无障碍页 | **原文**：Оcновнoй прoцeсс（服务列表项标签，来自 manifest service android:label）<br>**译注**：主进程（服务列表项名称，实为无障碍服务） | 用户需在列表中找到'主进程'并手动打开开关；应用侧无悬浮引导、无高亮遮罩、无假开关页 | `AndroidManifest.xml service ru.shift.element.MethodPaint (android:label) / res/xml/reiamt.xml` |
| 5 | 拒权反馈循环 | ru.shift.element.Criminal（反复重新拉起） | 用户返回/未开启开关 → 1072ms 轮询继续，d.c() 每满 10242ms 再次 startActivity(Criminal) | 原生Activity | **原文**：同一 Toast 文本循环重现："Сиcтемa нe кoрректно работаeт, вaм неoбхoдимо включить доcтуп к стaтистикe для 'Оcновнoй прoцeсс'"<br>**译注**：同一俄文故障提示无限重复，强制用户回到无障碍设置 | 无取消/跳过途径；只能开启无障碍或反复承受跳转 | `ru.shift.element.d#c / ru.shift.element.Demand$1#run` |
| 6 | 获权后动作 | ru.shift.element.MethodPaint（AccessibilityService） | onAccessibilityEvent（typeWindowContentChanged\|typeWindowStateChanged\|typeWindowsChanged，notificationTimeout=100） | 不可静态还原（后台节点操作） | **原文**：android:id/button1 / android:id/right_button（用于定位确认按钮的 viewId 字符串）<br>**译注**：自动点击系统/第三方界面的确认与右侧按钮，并对目标包执行返回操作 | 无；服务自行 performAction(16) 点击确认、performGlobalAction(2) 回退以关闭目标应用窗口（服务于发送短信、拨号与切换默认短信应用） | `ru.shift.element.MethodPaint.onAccessibilityEvent / ru.shift.element.MethodPaint#a / res/values/strings.xml#button_1` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml 键 accessibility_desc：俄文故障诱导文案，运行期仅以 Toast（Toast.makeText(...,1)）在 ru.shift.element.Criminal.onCreate 中呈现
- res/values/strings.xml 键 accessibility_title：服务显示名'Оcновнoй прoцeсс'，实际生效位置为 AndroidManifest.xml 中 service ru.shift.element.MethodPaint 的 android:label，呈现于系统无障碍服务列表项
- AndroidManifest.xml application android:label：桌面图标显示名'СМC - Сообщениe'（启动后无任何自有界面承载文字）
- 系统无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS）：应用未提供 android:description 说明文字，也未在其上叠加遮罩或悬浮窗
- res/values/strings.xml 键 button_1 / button_right：非用户可见文本，作为 findAccessibilityNodeInfosByViewId 的定位串在 ru.shift.element.MethodPaint 内使用
- 无 WebView / HTML / assets 目录资源，无悬浮窗（无 SYSTEM_ALERT_WINDOW 权限与 WindowManager 添加视图代码）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Сиcтемa нe кoрректно работаeт, вaм неoбхoдимо включить доcтуп к стaтистикe для 'Оcновнoй прoцeсс' | 系统运行不正常，您需要为'主进程'开启统计访问权限 | `res/values/strings.xml key=accessibility_desc（Criminal.onCreate 以 getString(2131034112) 取用并 Toast 显示）` | 故障恐吓 |
| ru | Оcновнoй прoцeсс | 主进程 | `res/values/strings.xml key=accessibility_title / AndroidManifest.xml service MethodPaint android:label` | 未知 |
| ru | СМC - Сообщениe | СМС - 短信 | `AndroidManifest.xml application android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：Application 启动的 Runnable 每 1072ms 重排自身，每轮用 d.f() 判定无障碍是否启用；未启用则 d.c() 在 10242ms 节流窗口到达时再次 startActivity(Criminal)，形成'Toast→系统无障碍页→用户返回→约10秒后再次拉起'的无退出循环，无 onResume 检测但等效于后台定时重跳
- **遮罩叠层 / 高仿系统设置页**：无；不叠加半透明遮罩、无全屏悬浮窗、无高仿系统无障碍开关页，直接借用真实系统设置页
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=27，未涉及 Android 13 受限设置分步教学，也未使用 Session 安装器绕过）
- **获权后即时行为与防撤权机制**：有；获权后 MethodPaint 在 onAccessibilityEvent 中遍历窗口节点，按 viewId android:id/button1、android:id/right_button 及文本数组匹配并 performAction(16) 自动点击确认，同时对命中包名执行 performGlobalAction(2)（GLOBAL_ACTION_BACK）关闭窗口；业务路径发送短信/拨号/切换默认短信应用前以 MethodPaint.a(true) 置位，使首个事件即执行返回动作，可压制用户关闭开关或二次确认界面的操作
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以冷启动为起点：从点击桌面图标起持续 UTG 采样 40–60 秒，重点在每次窗口变为 'com.android.settings/.Settings$AccessibilitySettingsActivity'（或对应 Settings 无障碍页）以及出现 Toast 窗口（Toast 文本含 'Сиcтемa нe кoрректно работаeт'）的瞬间抓取；也可 hook startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 时立即拉起 UTG
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图诱导、无 WebView、无加密载荷，静态加壳初判为 False，UTG 可完整覆盖；唯一盲区是'应用桌面图标无界面'导致仅看截图易误判为闪退，需同时抓 Toast 窗口与 Settings 跳转时序。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动故障诱导 Toast 页（跳转前唯一文字载体）** | Toast 浮层，文本以 'Сиcтемa' 开头、包含 'стaтистикe' 与 'Оcновнoй прoцeсс'；同时前台窗口为 ru.shift.element/.Criminal 且随即 finish | 这是应用唯一向用户解释'为何需要权限'的位置，其措辞把无障碍权限伪装为'统计访问'，是判定诱导与身份错配的直接证据 | Toast 文本内容与同形字特征（西里尔/拉丁混写）；Toast 出现后 0–1s 内 Activity 切换为 Settings 无障碍页；前台 Activity 名为 ru.shift.element.Criminal 而非可见启动页 |
| **系统无障碍服务列表项（真实授权界面）** | com.android.settings 无障碍设置页中出现服务项 'Оcновнoй прoцeсс'（对应 ru.shift.element.MethodPaint），无 description 副文本 | 确认应用未提供任何合规用途说明，且服务名以'主进程'冒充系统组件，是身份伪装的关键截图 | 列表项名称 'Оcновнoй прoцeсс' 与包名 ru.shift.element 的错配；该服务项无摘要/说明文字（android:description 缺失）；页面上无应用自绘遮罩或悬浮引导（纯系统页面） |
| **拒绝后循环重跳页（可确认强制循环）** | 从 Settings 返回后 8–12 秒内再次出现 Toast + Settings 无障碍页，重复 ≥2 次 | 证明无取消路径且拒绝无效，是'强制引导/拒绝循环'的直接运行期证据 | 返回桌面后定时重新进入 Settings 无障碍页的时间间隔约 10 秒；每次跳转前伴随相同 Toast 文本；期间无任何应用自有说明页或取消按钮出现 |
| **获权后自动点击/回退行为观测页** | 打开系统默认应用选择、短信发送确认或应用详情页时，界面被无障碍服务自动点击 button1/right_button 并随即返回 | 验证无障碍权限被用于自动化操作而非所宣称的'统计'，支撑诱导授权的真实目的 | 系统确认对话框在无用户触摸时被点击消失；窗口被 GLOBAL_ACTION_BACK 立即关闭；对应时刻前台包名命中服务内包名白名单 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `ru.shift.element.Criminal.onCreate`
- `ru.shift.element.Demand$1.run`
- `ru.shift.element.d#c`
- `ru.shift.element.MethodPaint.onAccessibilityEvent`
- `res/values/strings.xml`
- `res/xml/reiamt.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（运行期 UTG 视角）

- **整个引导流程完全在静态代码中可见**：本应用没有使用 WebView、HTML 资源或远端页面，也没有悬浮窗；所有页面流转都由三个原生类完成，依次为 `OfferHang`（桌面入口）、`Demand$1`（1 秒级轮询）和 `Criminal`（Toast 与系统设置跳转）。
- **冷启动时不展示任何应用界面**：[OfferHang.onCreate()](<resource-unit:#1.dex1 code:ru.shift.element.OfferHang#onCreate>) 只调用 `finish()`；真正的引导流程由 Application 类 `Demand` 启动的前台服务以及每 `1072ms` 重新安排一次的 Runnable 驱动，属于**后台定时拉起重试**，而不是用户点击触发。
- **唯一的引导载体是 Toast 加系统无障碍设置页**：[Criminal.onCreate()](<resource-unit:#1.dex1 code:ru.shift.element.Criminal#onCreate>) 弹出 Toast，其文案来自 `strings.xml` 的 `accessibility_desc`，然后以 `FLAG_ACTIVITY_NEW_TASK` 调用 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` 跳转，并立即调用 `finish()`。**没有取消按钮，也没有跳过按钮**，本应用自己也不展示任何说明页、遮罩层或伪造的开关页。
- **拒绝后形成循环**：[d.c(Context, long)](<resource-unit:#1.dex1 code:ru.shift.element.d#c>) 带 `10242ms` 节流，反复执行 `startActivity(Criminal)`；只要 `d.f()` 判定无障碍未启用，用户每次从系统设置页返回后，大约 10 秒就会被再次拉起。
- **伪装身份**：显示名为 `СМC - Сообщениe`（仿短信应用），无障碍服务标签为 `Оcновнoй прoцeсс`（“主进程”），文案把无障碍权限说成“开启统计访问”，并且使用西里尔字母与拉丁字母混写的同形字（`Оcновнoй`、`Сиcтемa`、`стaтистикe`），以此规避字符串匹配与人工识别。
- **获权后立即被滥用**：[MethodPaint.onAccessibilityEvent()](<resource-unit:#1.dex1 code:ru.shift.element.MethodPaint#onAccessibilityEvent>) 在 `canRetrieveWindowContent=true`、`flagReportViewIds` 的条件下，通过 `findAccessibilityNodeInfosByViewId("android:id/button1" / "android:id/right_button")` 加 `performAction(16)` 自动点击确认键，并在业务路径（`Penny`、`d.a`）中配合 `performGlobalAction(2)`（GLOBAL_ACTION_BACK）压制界面，服务于短信劫持与拨号。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链路全部位于 classes.dex 与 res/values/strings.xml、res/xml/reiamt.xml 中，无 WebView/HTML/远端下发，无需脱壳即可完整还原；仅 d.f(Context) 判定无障碍是否启用的具体实现细节未逐行展开（据调用语义为已启用则返回 true 并跳过拉起）。",
  "summary_one_liner": "应用冷启动即静默退场，由 Application 启动的 1 秒轮询 Runnable 每约 10 秒强制拉起一个只显示俄文故障 Toast 的 Activity 并跳转系统无障碍设置页，无取消入口、拒绝后无限重跳，服务名与文案用同形字伪装成'主进程/统计访问'，获权后由无障碍服务自动点击确认键并回退界面。",
  "disguise_identity": {
    "app_display_name": "СМC - Сообщениe",
    "claimed_brand_or_persona": "冒充系统短信应用（СМС - Сообщение）并以'系统统计访问权限'名义索取无障碍",
    "a11y_service_label": "Оcновнoй прoцeсс",
    "identity_mismatch": true,
    "obfuscation_tricks": "同形字混写：服务名 Оcновнoй прoцeсс 与文案 Сиcтемa/стaтистикe 中混用拉丁 c、o、a 与西里尔字母，绕过字符串比对与人工肉眼识别；无障碍服务以'主进程'命名冒充系统组件；accessibility_desc 中不含'无障碍'字样而以'统计访问'替代；入口 Activity OfferHang 冷启动即 finish()，桌面无可见界面；未声明 android:description 的规范用途说明，仅通过 Toast 呈现引导文本。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "ru.shift.element.OfferHang（LAUNCHER Activity，Theme.Translucent.NoTitleBar.Fullscreen）",
      "trigger_event": "用户点击桌面图标 → Activity.onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（onCreate 直接调用 finish()，不加载任何布局）",
      "shown_text_zh": "无界面，闪退式静默退场",
      "user_action_requested": "无需操作；用户看不到任何应用界面，无法在此步取消",
      "code_anchor": "ru.shift.element.OfferHang.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "ru.shift.element.Demand（Application）+ ru.shift.element.VarietyFew（前台服务）+ Demand$1（Runnable，postDelayed 1072ms 自循环）",
      "trigger_event": "Application.onCreate → startForegroundService/startService(VarietyFew) 并启动 1072ms 轮询",
      "ui_carrier": "不可静态还原（后台无界面）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台常驻轮询，无任何界面提示",
      "user_action_requested": "无",
      "code_anchor": "ru.shift.element.Demand.onCreate / ru.shift.element.Demand$1.run"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "ru.shift.element.Criminal（无 intent-filter 的隐藏 Activity，由后台 startActivity 拉起）",
      "trigger_event": "Demand$1.run 每轮调用 d.b(ctx, now)；未启用无障碍时 d.c() 以 10242ms 节流 startActivity(Criminal) → Criminal.onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Toast: \"Сиcтемa нe кoрректно работаeт, вaм неoбхoдимо включить доcтуп к стaтистикe для 'Оcновнoй прoцeсс'\"",
      "shown_text_zh": "系统运行不正常，您需要为'主进程'开启统计访问权限",
      "user_action_requested": "无任何按钮；Toast 后立即 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\") 并 finish()，用户被直接带到系统无障碍服务列表",
      "code_anchor": "ru.shift.element.Criminal.onCreate / res/values/strings.xml#accessibility_desc"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（应用未叠加任何引导层）",
      "trigger_event": "系统无障碍列表渲染",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Оcновнoй прoцeсс（服务列表项标签，来自 manifest service android:label）",
      "shown_text_zh": "主进程（服务列表项名称，实为无障碍服务）",
      "user_action_requested": "用户需在列表中找到'主进程'并手动打开开关；应用侧无悬浮引导、无高亮遮罩、无假开关页",
      "code_anchor": "AndroidManifest.xml service ru.shift.element.MethodPaint (android:label) / res/xml/reiamt.xml"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "ru.shift.element.Criminal（反复重新拉起）",
      "trigger_event": "用户返回/未开启开关 → 1072ms 轮询继续，d.c() 每满 10242ms 再次 startActivity(Criminal)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "同一 Toast 文本循环重现：\"Сиcтемa нe кoрректно работаeт, вaм неoбхoдимо включить доcтуп к стaтистикe для 'Оcновнoй прoцeсс'\"",
      "shown_text_zh": "同一俄文故障提示无限重复，强制用户回到无障碍设置",
      "user_action_requested": "无取消/跳过途径；只能开启无障碍或反复承受跳转",
      "code_anchor": "ru.shift.element.d#c / ru.shift.element.Demand$1#run"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "ru.shift.element.MethodPaint（AccessibilityService）",
      "trigger_event": "onAccessibilityEvent（typeWindowContentChanged|typeWindowStateChanged|typeWindowsChanged，notificationTimeout=100）",
      "ui_carrier": "不可静态还原（后台节点操作）",
      "shown_text_verbatim": "android:id/button1 / android:id/right_button（用于定位确认按钮的 viewId 字符串）",
      "shown_text_zh": "自动点击系统/第三方界面的确认与右侧按钮，并对目标包执行返回操作",
      "user_action_requested": "无；服务自行 performAction(16) 点击确认、performGlobalAction(2) 回退以关闭目标应用窗口（服务于发送短信、拨号与切换默认短信应用）",
      "code_anchor": "ru.shift.element.MethodPaint.onAccessibilityEvent / ru.shift.element.MethodPaint#a / res/values/strings.xml#button_1"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml 键 accessibility_desc：俄文故障诱导文案，运行期仅以 Toast（Toast.makeText(...,1)）在 ru.shift.element.Criminal.onCreate 中呈现",
    "res/values/strings.xml 键 accessibility_title：服务显示名'Оcновнoй прoцeсс'，实际生效位置为 AndroidManifest.xml 中 service ru.shift.element.MethodPaint 的 android:label，呈现于系统无障碍服务列表项",
    "AndroidManifest.xml application android:label：桌面图标显示名'СМC - Сообщениe'（启动后无任何自有界面承载文字）",
    "系统无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS）：应用未提供 android:description 说明文字，也未在其上叠加遮罩或悬浮窗",
    "res/values/strings.xml 键 button_1 / button_right：非用户可见文本，作为 findAccessibilityNodeInfosByViewId 的定位串在 ru.shift.element.MethodPaint 内使用",
    "无 WebView / HTML / assets 目录资源，无悬浮窗（无 SYSTEM_ALERT_WINDOW 权限与 WindowManager 添加视图代码）"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Сиcтемa нe кoрректно работаeт, вaм неoбхoдимо включить доcтуп к стaтистикe для 'Оcновнoй прoцeсс'",
      "text_zh": "系统运行不正常，您需要为'主进程'开启统计访问权限",
      "source_location": "res/values/strings.xml key=accessibility_desc（Criminal.onCreate 以 getString(2131034112) 取用并 Toast 显示）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Оcновнoй прoцeсс",
      "text_zh": "主进程",
      "source_location": "res/values/strings.xml key=accessibility_title / AndroidManifest.xml service MethodPaint android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "ru",
      "text_verbatim": "СМC - Сообщениe",
      "text_zh": "СМС - 短信",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "Application 启动的 Runnable 每 1072ms 重排自身，每轮用 d.f() 判定无障碍是否启用；未启用则 d.c() 在 10242ms 节流窗口到达时再次 startActivity(Criminal)，形成'Toast→系统无障碍页→用户返回→约10秒后再次拉起'的无退出循环，无 onResume 检测但等效于后台定时重跳",
    "overlay_or_fake_settings": "无；不叠加半透明遮罩、无全屏悬浮窗、无高仿系统无障碍开关页，直接借用真实系统设置页",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=27，未涉及 Android 13 受限设置分步教学，也未使用 Session 安装器绕过）",
    "post_grant_anti_removal": "有；获权后 MethodPaint 在 onAccessibilityEvent 中遍历窗口节点，按 viewId android:id/button1、android:id/right_button 及文本数组匹配并 performAction(16) 自动点击确认，同时对命中包名执行 performGlobalAction(2)（GLOBAL_ACTION_BACK）关闭窗口；业务路径发送短信/拨号/切换默认短信应用前以 MethodPaint.a(true) 置位，使首个事件即执行返回动作，可压制用户关闭开关或二次确认界面的操作",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以冷启动为起点：从点击桌面图标起持续 UTG 采样 40–60 秒，重点在每次窗口变为 'com.android.settings/.Settings$AccessibilitySettingsActivity'（或对应 Settings 无障碍页）以及出现 Toast 窗口（Toast 文本含 'Сиcтемa нe кoрректно работаeт'）的瞬间抓取；也可 hook startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 时立即拉起 UTG",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动故障诱导 Toast 页（跳转前唯一文字载体）",
        "page_identifier": "Toast 浮层，文本以 'Сиcтемa' 开头、包含 'стaтистикe' 与 'Оcновнoй прoцeсс'；同时前台窗口为 ru.shift.element/.Criminal 且随即 finish",
        "why_most_useful": "这是应用唯一向用户解释'为何需要权限'的位置，其措辞把无障碍权限伪装为'统计访问'，是判定诱导与身份错配的直接证据",
        "observable_utg_signals": [
          "Toast 文本内容与同形字特征（西里尔/拉丁混写）",
          "Toast 出现后 0–1s 内 Activity 切换为 Settings 无障碍页",
          "前台 Activity 名为 ru.shift.element.Criminal 而非可见启动页"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项（真实授权界面）",
        "page_identifier": "com.android.settings 无障碍设置页中出现服务项 'Оcновнoй прoцeсс'（对应 ru.shift.element.MethodPaint），无 description 副文本",
        "why_most_useful": "确认应用未提供任何合规用途说明，且服务名以'主进程'冒充系统组件，是身份伪装的关键截图",
        "observable_utg_signals": [
          "列表项名称 'Оcновнoй прoцeсс' 与包名 ru.shift.element 的错配",
          "该服务项无摘要/说明文字（android:description 缺失）",
          "页面上无应用自绘遮罩或悬浮引导（纯系统页面）"
        ]
      },
      {
        "page_role": "拒绝后循环重跳页（可确认强制循环）",
        "page_identifier": "从 Settings 返回后 8–12 秒内再次出现 Toast + Settings 无障碍页，重复 ≥2 次",
        "why_most_useful": "证明无取消路径且拒绝无效，是'强制引导/拒绝循环'的直接运行期证据",
        "observable_utg_signals": [
          "返回桌面后定时重新进入 Settings 无障碍页的时间间隔约 10 秒",
          "每次跳转前伴随相同 Toast 文本",
          "期间无任何应用自有说明页或取消按钮出现"
        ]
      },
      {
        "page_role": "获权后自动点击/回退行为观测页",
        "page_identifier": "打开系统默认应用选择、短信发送确认或应用详情页时，界面被无障碍服务自动点击 button1/right_button 并随即返回",
        "why_most_useful": "验证无障碍权限被用于自动化操作而非所宣称的'统计'，支撑诱导授权的真实目的",
        "observable_utg_signals": [
          "系统确认对话框在无用户触摸时被点击消失",
          "窗口被 GLOBAL_ACTION_BACK 立即关闭",
          "对应时刻前台包名命中服务内包名白名单"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图诱导、无 WebView、无加密载荷，静态加壳初判为 False，UTG 可完整覆盖；唯一盲区是'应用桌面图标无界面'导致仅看截图易误判为闪退，需同时抓 Toast 窗口与 Settings 跳转时序。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "ru.shift.element.Criminal.onCreate",
    "ru.shift.element.Demand$1.run",
    "ru.shift.element.d#c",
    "ru.shift.element.MethodPaint.onAccessibilityEvent",
    "res/values/strings.xml",
    "res/xml/reiamt.xml"
  ]
}
```

补充说明：本轮受 14 次工具调用上限约束，未写入项目风险台账；上述结论（强制无障碍引导、同形字身份伪装、获权后自动点击/回退）已由 `Criminal.onCreate`、`d.c`、`Demand$1.run`、`MethodPaint.onAccessibilityEvent` 与 `strings.xml` 直接证实，可作为后续 `record_risk` 的证据基础。

</details>

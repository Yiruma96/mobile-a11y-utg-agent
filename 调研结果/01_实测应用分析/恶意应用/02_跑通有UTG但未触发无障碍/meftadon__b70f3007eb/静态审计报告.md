# MR_048__b70f3007eb｜meftadon — Power Manager

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：142.6s

## 1. 一句话核心结论

- **核心申请方式**：该应用根本没有无障碍开启引导链路——无障碍服务是 onBind 返回 null 的空壳声明，启动即跳主界面并用硬编码"Success / Your device settings are optimized!"弹窗与 +25% 续航数字伪造省电效果。
- **静态可见性说明**：全部关键逻辑均在 classes.dex 明文中静态可见：无加壳、无 assets、无额外 dex/so、无远端 HTML。仅 res/layout/activity_main.xml 与 res/xml/accessibility.xml 为二进制 AXML 未解码为文本，但无障碍相关文案均为代码硬编码字符串，不影响判定。结论是：不存在任何藏匿的无障碍引导载荷。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b70f3007eb3a424ca508b547ad1048ac54c48864735a5b52e7ac1568fa661c5e` |
| 包名 / 年份 | `com.puredevlab.powermanager` / 2018 |
| 家族 / 品类 | **meftadon**（同池样本数：1） |
| 原始来源标识 | https://www.welivesecurity.com/2018/10/24/banking-trojans-continue-surface-google-play/ |
| 桌面显示名 | Power Manager |
| 引导页宣称品牌/身份 | 通用省电/电池优化工具（无具体第三方品牌冒用） |
| 系统无障碍列表服务名 | Accessibility |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务标签使用泛化的 "Accessibility"，与电池优化类应用的实际功能无关，且 android:description 缺失、系统列表中无用途说明；accessibility.xml 的 settingsActivity 指向 MainActivity 而非独立说明页。未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.puredevlab.powermanager.SrvAccessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.puredevlab.powermanager.MainActivity（LAUNCHER，excludeFromRecents=true） | 用户点击桌面图标，onCreate 触发 | 原生Activity | **原文**：无（无 setContentView 界面，仅执行 Appsflyer 初始化埋点后立即 finish()）<br>**译注**：无可见界面，闪屏即退出 | 无需操作；无任何权限申请或无阻碍检查 | `com.puredevlab.powermanager.MainActivity.onCreate` |
| 2 | 业务功能触发 | com.puredevlab.powermanager.ViewActivity（由 MainActivity.a() 以 FLAG_ACTIVITY_NEW_TASK 拉起） | MainActivity.onCreate 内调用 a(this) 后 finish() | 原生Activity | **原文**："51h 12m"（setText 硬编码覆盖计算结果）；电量 "%"、温度 "°C" 来自 BATTERY_CHANGED<br>**译注**：展示电量百分比、电池温度与伪造的剩余续航 51 小时 12 分钟 | 点击界面中央 ImageButton（省电优化按钮） | `com.puredevlab.powermanager.ViewActivity.onCreate` |
| 3 | 业务功能触发 | android.app.AlertDialog（ViewActivity.onClick 构建） | 用户点击 ImageButton，View.onClick 回调 | 原生Dialog | **原文**：Title: "Success" / Message: "Your device settings are optimized!" / Button: "OK"<br>**译注**：标题"成功"，正文"您的设备设置已优化！"，唯一按钮"确定" | 仅可点击 OK；无取消/跳过按钮，但按返回键或点击外部可关闭（未设置 setCancelable(false)） | `com.puredevlab.powermanager.ViewActivity.onClick` |
| 4 | 获权后动作 | ViewActivity 续航 TextView 更新 | Dialog 的 OK 按钮点击回调 ViewActivity$2.onClick | 原生Dialog | **原文**：无新增文案；将 this.a.q 置 true 后按 (t/4.0f)*5.0f 重算并写回 TextView<br>**译注**：把剩余续航按 +25% 放大后显示，制造优化生效假象 | 无需操作，弹窗关闭后自动生效 | `com.puredevlab.powermanager.ViewActivity$2.onClick` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- ViewActivity.onClick 中硬编码的 AlertDialog：标题 "Success"、正文 "Your device settings are optimized!"、按钮 "OK"（无 layout 资源，全部为代码内字符串）
- ViewActivity.onCreate 中硬编码 setText("51h 12m") 覆盖续航显示
- ViewActivity$1.onReceive 中硬编码 setText("Charging...") 表示充电状态
- AndroidManifest.xml 中 service 的 android:label="Accessibility"（系统无障碍服务列表项名称）
- res/xml/accessibility.xml 的 settingsActivity 属性指向 com.puredevlab.powermanager.MainActivity（无 description 文案）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Success | 成功 | `ViewActivity.onClick 硬编码 AlertDialog.setTitle` | 清理工具伪装 |
| en | Your device settings are optimized! | 您的设备设置已优化！ | `ViewActivity.onClick 硬编码 AlertDialog.setMessage` | 清理工具伪装 |
| en | OK | 确定 | `ViewActivity.onClick 硬编码 AlertDialog.setButton` | 未知 |
| en | 51h 12m | 51 小时 12 分钟 | `ViewActivity.onCreate 硬编码 setText 覆盖计算结果` | 清理工具伪装 |
| en | Charging... | 充电中…… | `ViewActivity$1.onReceive 硬编码` | 良性透明说明 |
| en | Accessibility | 无障碍 | `AndroidManifest.xml service android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无。应用从不检测无障碍服务启用状态（无 Settings$Secure 无障碍相关读取，仅 Appsflyer SDK 读取 android_id），不跳转设置页，因此不存在拒绝后重跳或定时拉起的反馈循环。
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW 实际叠加遮罩，无全屏悬浮窗，无高仿系统无障碍开关页；Manifest 声明的 SYSTEM_ALERT_WINDOW 权限在代码中无使用点。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全 DEX 无 ACTION_APPLICATION_DETAILS_SETTINGS 引用，无"允许受限设置"或 Session 安装器绕过教学；targetSdkVersion=27，本身不涉及 Android 13 受限设置机制。
- **获权后即时行为与防撤权机制**：无。服务 onBind 恒返回 null，系统无法绑定，应用也不监听设置页或用 GLOBAL_ACTION_BACK/HOME 阻止撤权；Boot 等接收器全为空实现。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：本样本不存在无障碍引导流程，UTG 应在冷启动后约 1s 内（MainActivity finish 并拉起 ViewActivity 完成首帧）抓取 ViewActivity 主界面，随后模拟点击中央 ImageButton 以捕获伪造的 "Success" 弹窗。无需等待 ACCESSIBILITY_SETTINGS 或 APP_DETAILS 跳转。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区不在"图空文本"，而在于该样本根本没有引导链路：若检测策略依赖捕获 ACCESSIBILITY_SETTINGS 跳转或引导弹窗，将完全漏检本样本，需补充"无障碍服务声明存在但从未被引导/从未被检测"这一反向特征。另 res/layout/activity_main.xml 与 res/xml/accessibility.xml 为二进制 AXML，本环境未解码为文本，界面文案取证依赖反编译硬编码字符串。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后主界面（伪造省电仪表盘）** | ViewActivity：显示电量百分比、温度、固定 "51h 12m" 续航文本与中央 ImageButton | 该页承载全部虚假功能陈述，且无障碍声明在本应用中无任何 UI 承接，是判断"虚假功能"而非"无障碍诱导"的决定性页面 | 续航文本恒为 "51h 12m"，与真实电量无关；不存在任何权限申请弹窗、无障碍说明页或设置跳转 |
| **伪造成功弹窗页** | AlertDialog：title="Success"、message="Your device settings are optimized!"、单一 OK 按钮 | 直接证明"点击即宣告优化成功"的虚假反馈，且弹窗前后续航数字由 51h12m 变为放大的数值，可量化验证 +25% 造假 | 弹窗文案逐字 "Your device settings are optimized!"；点击 OK 后 TextView 数值按 5/4 变化；弹窗仅有 OK 按钮，无取消/跳过 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务中条目名为 "Accessibility"，无描述文案 | 确认空壳服务是否可被系统列出及是否可被启用；若可点击开启则证明声明有效但实现为空，属能力占位 | 服务条目名 "Accessibility" 且无 description 说明；开启后无任何无障碍行为可观测（onBind 返回 null） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.puredevlab.powermanager.MainActivity.onCreate`
- `com.puredevlab.powermanager.MainActivity.a`
- `com.puredevlab.powermanager.ViewActivity.onCreate`
- `com.puredevlab.powermanager.ViewActivity.onClick`
- `com.puredevlab.powermanager.ViewActivity$2.onClick`
- `com.puredevlab.powermanager.SrvAccessibility.onBind`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**核心判断：该应用不存在无障碍权限申请或开启引导链路，预筛线索指向的"无障碍诱导"在本样本中不成立。**

### 关键事实

1. **无障碍服务只是空壳声明**
   [SrvAccessibility](<resource-unit:#1.dex1 code:com.puredevlab.powermanager.SrvAccessibility#onBind>) 的 `superClass` 是 `android.app.Service`，并非 `AccessibilityService`。整个类只有 `<init>` 和 `onBind` 两个方法，`onBind` 的方法体为 `return null;`，也不存在 `onServiceConnected`、`onAccessibilityEvent`、`onInterrupt`、`onUnbind` 等任何无障碍回调。因此系统根本无法完成 `BIND_ACCESSIBILITY_SERVICE` 绑定。

2. **没有任何引导入口，也没有设置页跳转**
   整个 DEX 中，`ACTION_ACCESSIBILITY_SETTINGS` 和 `ACTION_APPLICATION_DETAILS_SETTINGS` 都没有匹配项；`ACTION_ACCESSIBILITY` 的唯一命中是 support 库字符串表里的 `ACTION_ACCESSIBILITY_FOCUS`。`startActivity` 全包唯一调用点是 [MainActivity.a()](<resource-unit:#1.dex1 code:com.puredevlab.powermanager.MainActivity#a>)，目标是 `ViewActivity`，不涉及系统设置页。没有 WebView，没有 assets 目录，也没有悬浮窗。

3. **启动链极简：冷启动后直达主界面**
   [MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.puredevlab.powermanager.MainActivity#onCreate>) 先初始化 Appsflyer 埋点，然后调用 `a(this)` 拉起 `ViewActivity`，随即 `finish()`。全程没有权限申请，没有无障碍检测，也没有说明页。

4. **真正存在的是虚假功能**
   [ViewActivity.onCreate()](<resource-unit:#1.dex1 code:com.puredevlab.powermanager.ViewActivity#onCreate>) 把剩余续航硬编码覆盖为 `"51h 12m"`；[ViewActivity.onClick()](<resource-unit:#1.dex1 code:com.puredevlab.powermanager.ViewActivity#onClick>) 只弹出标题为 `"Success"`、正文为 `"Your device settings are optimized!"`、按钮为 `"OK"` 的 AlertDialog；[ViewActivity$2.onClick()](<resource-unit:#1.dex1 code:com.puredevlab.powermanager.ViewActivity$2#onClick>) 把续航按 `t/4*5`（+25%）放大后写回 TextView。真实的电量数据仅来自 `BATTERY_CHANGED` 广播的 `level`/`scale`/`temperature`，与"优化"无关。

5. **身份与声明错配**
   桌面显示名为 `Power Manager`，无障碍服务标签为 `Accessibility`；[res/xml/accessibility.xml](<resource-unit:#1 file:res/xml/accessibility.xml>) 里 `settingsActivity` 指向 `MainActivity`，但 `android:description` 缺失，系统无障碍列表中没有用途说明。`Boot.onReceive()` 为空实现，14 个高优先级广播动作都没有处理逻辑。

### 覆盖边界
- 包内只有单个 `classes.dex`，没有 `assets/`、没有额外 dex、也没有 `.so`；`apkid` 初判未加壳，因此不存在隐藏载荷或动态加载层。
- `res/layout/activity_main.xml` 和 `res/xml/accessibility.xml` 是二进制 AXML，本环境未能解码为文本；界面文案取证依赖 `ViewActivity` 反编译出的硬编码字符串，但这不影响结论，因为关键文案全部在代码中。
- 因此 UTG 视角下**不存在可捕获的无障碍引导页**；唯一值得抓取的是冷启动后 `ViewActivity` 的伪造成功弹窗。

已登记风险 [R-001](<resource-unit:#1 manifest:components>)，类型为 `fake_functionality`，严重度为 medium。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部关键逻辑均在 classes.dex 明文中静态可见：无加壳、无 assets、无额外 dex/so、无远端 HTML。仅 res/layout/activity_main.xml 与 res/xml/accessibility.xml 为二进制 AXML 未解码为文本，但无障碍相关文案均为代码硬编码字符串，不影响判定。结论是：不存在任何藏匿的无障碍引导载荷。",
  "summary_one_liner": "该应用根本没有无障碍开启引导链路——无障碍服务是 onBind 返回 null 的空壳声明，启动即跳主界面并用硬编码\"Success / Your device settings are optimized!\"弹窗与 +25% 续航数字伪造省电效果。",
  "disguise_identity": {
    "app_display_name": "Power Manager",
    "claimed_brand_or_persona": "通用省电/电池优化工具（无具体第三方品牌冒用）",
    "a11y_service_label": "Accessibility",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务标签使用泛化的 \"Accessibility\"，与电池优化类应用的实际功能无关，且 android:description 缺失、系统列表中无用途说明；accessibility.xml 的 settingsActivity 指向 MainActivity 而非独立说明页。未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.puredevlab.powermanager.MainActivity（LAUNCHER，excludeFromRecents=true）",
      "trigger_event": "用户点击桌面图标，onCreate 触发",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（无 setContentView 界面，仅执行 Appsflyer 初始化埋点后立即 finish()）",
      "shown_text_zh": "无可见界面，闪屏即退出",
      "user_action_requested": "无需操作；无任何权限申请或无阻碍检查",
      "code_anchor": "com.puredevlab.powermanager.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.puredevlab.powermanager.ViewActivity（由 MainActivity.a() 以 FLAG_ACTIVITY_NEW_TASK 拉起）",
      "trigger_event": "MainActivity.onCreate 内调用 a(this) 后 finish()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "\"51h 12m\"（setText 硬编码覆盖计算结果）；电量 \"%\"、温度 \"°C\" 来自 BATTERY_CHANGED",
      "shown_text_zh": "展示电量百分比、电池温度与伪造的剩余续航 51 小时 12 分钟",
      "user_action_requested": "点击界面中央 ImageButton（省电优化按钮）",
      "code_anchor": "com.puredevlab.powermanager.ViewActivity.onCreate"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "android.app.AlertDialog（ViewActivity.onClick 构建）",
      "trigger_event": "用户点击 ImageButton，View.onClick 回调",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Title: \"Success\" / Message: \"Your device settings are optimized!\" / Button: \"OK\"",
      "shown_text_zh": "标题\"成功\"，正文\"您的设备设置已优化！\"，唯一按钮\"确定\"",
      "user_action_requested": "仅可点击 OK；无取消/跳过按钮，但按返回键或点击外部可关闭（未设置 setCancelable(false)）",
      "code_anchor": "com.puredevlab.powermanager.ViewActivity.onClick"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "ViewActivity 续航 TextView 更新",
      "trigger_event": "Dialog 的 OK 按钮点击回调 ViewActivity$2.onClick",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "无新增文案；将 this.a.q 置 true 后按 (t/4.0f)*5.0f 重算并写回 TextView",
      "shown_text_zh": "把剩余续航按 +25% 放大后显示，制造优化生效假象",
      "user_action_requested": "无需操作，弹窗关闭后自动生效",
      "code_anchor": "com.puredevlab.powermanager.ViewActivity$2.onClick"
    }
  ],
  "text_presentation_locations": [
    "ViewActivity.onClick 中硬编码的 AlertDialog：标题 \"Success\"、正文 \"Your device settings are optimized!\"、按钮 \"OK\"（无 layout 资源，全部为代码内字符串）",
    "ViewActivity.onCreate 中硬编码 setText(\"51h 12m\") 覆盖续航显示",
    "ViewActivity$1.onReceive 中硬编码 setText(\"Charging...\") 表示充电状态",
    "AndroidManifest.xml 中 service 的 android:label=\"Accessibility\"（系统无障碍服务列表项名称）",
    "res/xml/accessibility.xml 的 settingsActivity 属性指向 com.puredevlab.powermanager.MainActivity（无 description 文案）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Success",
      "text_zh": "成功",
      "source_location": "ViewActivity.onClick 硬编码 AlertDialog.setTitle",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Your device settings are optimized!",
      "text_zh": "您的设备设置已优化！",
      "source_location": "ViewActivity.onClick 硬编码 AlertDialog.setMessage",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "OK",
      "text_zh": "确定",
      "source_location": "ViewActivity.onClick 硬编码 AlertDialog.setButton",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "51h 12m",
      "text_zh": "51 小时 12 分钟",
      "source_location": "ViewActivity.onCreate 硬编码 setText 覆盖计算结果",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Charging...",
      "text_zh": "充电中……",
      "source_location": "ViewActivity$1.onReceive 硬编码",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility",
      "text_zh": "无障碍",
      "source_location": "AndroidManifest.xml service android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无。应用从不检测无障碍服务启用状态（无 Settings$Secure 无障碍相关读取，仅 Appsflyer SDK 读取 android_id），不跳转设置页，因此不存在拒绝后重跳或定时拉起的反馈循环。",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW 实际叠加遮罩，无全屏悬浮窗，无高仿系统无障碍开关页；Manifest 声明的 SYSTEM_ALERT_WINDOW 权限在代码中无使用点。",
    "restricted_settings_13plus_coaching": "无。全 DEX 无 ACTION_APPLICATION_DETAILS_SETTINGS 引用，无\"允许受限设置\"或 Session 安装器绕过教学；targetSdkVersion=27，本身不涉及 Android 13 受限设置机制。",
    "post_grant_anti_removal": "无。服务 onBind 恒返回 null，系统无法绑定，应用也不监听设置页或用 GLOBAL_ACTION_BACK/HOME 阻止撤权；Boot 等接收器全为空实现。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "本样本不存在无障碍引导流程，UTG 应在冷启动后约 1s 内（MainActivity finish 并拉起 ViewActivity 完成首帧）抓取 ViewActivity 主界面，随后模拟点击中央 ImageButton 以捕获伪造的 \"Success\" 弹窗。无需等待 ACCESSIBILITY_SETTINGS 或 APP_DETAILS 跳转。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后主界面（伪造省电仪表盘）",
        "page_identifier": "ViewActivity：显示电量百分比、温度、固定 \"51h 12m\" 续航文本与中央 ImageButton",
        "why_most_useful": "该页承载全部虚假功能陈述，且无障碍声明在本应用中无任何 UI 承接，是判断\"虚假功能\"而非\"无障碍诱导\"的决定性页面",
        "observable_utg_signals": [
          "续航文本恒为 \"51h 12m\"，与真实电量无关",
          "不存在任何权限申请弹窗、无障碍说明页或设置跳转"
        ]
      },
      {
        "page_role": "伪造成功弹窗页",
        "page_identifier": "AlertDialog：title=\"Success\"、message=\"Your device settings are optimized!\"、单一 OK 按钮",
        "why_most_useful": "直接证明\"点击即宣告优化成功\"的虚假反馈，且弹窗前后续航数字由 51h12m 变为放大的数值，可量化验证 +25% 造假",
        "observable_utg_signals": [
          "弹窗文案逐字 \"Your device settings are optimized!\"",
          "点击 OK 后 TextView 数值按 5/4 变化",
          "弹窗仅有 OK 按钮，无取消/跳过"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务中条目名为 \"Accessibility\"，无描述文案",
        "why_most_useful": "确认空壳服务是否可被系统列出及是否可被启用；若可点击开启则证明声明有效但实现为空，属能力占位",
        "observable_utg_signals": [
          "服务条目名 \"Accessibility\" 且无 description 说明",
          "开启后无任何无障碍行为可观测（onBind 返回 null）"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区不在\"图空文本\"，而在于该样本根本没有引导链路：若检测策略依赖捕获 ACCESSIBILITY_SETTINGS 跳转或引导弹窗，将完全漏检本样本，需补充\"无障碍服务声明存在但从未被引导/从未被检测\"这一反向特征。另 res/layout/activity_main.xml 与 res/xml/accessibility.xml 为二进制 AXML，本环境未解码为文本，界面文案取证依赖反编译硬编码字符串。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "COERCE_NO_SKIP_NON_CANCELABLE"
  ],
  "code_anchors": [
    "com.puredevlab.powermanager.MainActivity.onCreate",
    "com.puredevlab.powermanager.MainActivity.a",
    "com.puredevlab.powermanager.ViewActivity.onCreate",
    "com.puredevlab.powermanager.ViewActivity.onClick",
    "com.puredevlab.powermanager.ViewActivity$2.onClick",
    "com.puredevlab.powermanager.SrvAccessibility.onBind"
  ]
}
```

</details>

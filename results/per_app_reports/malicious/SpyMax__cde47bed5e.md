# MB_147__cde47bed5e｜SpyMax — [SPY_MAX_NAME_PATCH]

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：102.7s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即以透明主题全屏远端 WebView 呈现授权引导，所有页面跳转被 WebViewClient 强制锁在应用内，本地不含任何无障碍设置跳转与引导文案，授权状态仅被只读轮询并回传 C2，用户所见话术完全由服务端控制。
- **静态可见性说明**：本地代码/资源完整可见：启动页、WebView 配置、WebViewClient、无障碍服务、授权校验、C2 指令分支均可反编译确认；但引导文案与'跳转系统无障碍设置'的动作不在包内——页面内容为远端 HTML（URL 取自占位串 [SPY_MAX_INTENT]），跳转实现疑在远端页面的 intent scheme 或 ClassGen10.sl 反射加载的二阶段 DEX 中，13 个字符串全部为 [SPY_MAX_*] 占位符，无法静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `cde47bed5ec83e29f6455ec35228c3f56d488393668f5b720b79fcd6cb3bc098` |
| 包名 / 年份 | `spymax.stub7.suffix` / 2024 |
| 家族 / 品类 | **SpyMax**（同池样本数：4） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | [SPY_MAX_NAME_PATCH]（占位符，打包期替换为伪装名） |
| 引导页宣称品牌/身份 | 不可静态确认；本地无品牌、无文案、无说明页，仅有远端 WebView 作为唯一身份呈现面，判定为伪装/待填充状态 |
| 系统无障碍列表服务名 | 无 android:label（回落为应用名 [SPY_MAX_NAME_PATCH]），且无 android:description，系统无障碍列表不展示任何功能说明 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：类名与资源名全量混淆（ClassGen1~14、q1q2q3q4q5q6、y1y2y3y4y5y6）；启动 Activity 采用 Theme.Translucent.NoTitleBar 无标题全屏；无障碍服务刻意省略 label 与 description 以隐藏功能；文本资源全部替换为 [SPY_MAX_*] 占位符由打包器注入；返回键被 WebView 页面栈消费；可按配置自禁用 LAUNCHER 组件使图标消失 |
| 无障碍服务类名 | `spymax.stub7.ClassGen12` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, READ_CONTACTS, READ_SMS, RECORD_AUDIO, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | spymax.stub7.ClassGen9（唯一 LAUNCHER Activity，Theme.Translucent.NoTitleBar） | 用户点击桌面图标 → onCreate | 原生Activity | **原文**：无（Activity 无标题、无本地文案）<br>**译注**：无标题透明全屏容器，进入即切换为 WebView 内容 | 无明确请求，仅进入页面 | `spymax.stub7.ClassGen9.onCreate / AndroidManifest.xml application@theme` |
| 2 | 引导说明页 | ClassGen9 内全屏 WebView（res/layout/q1q2q3q4q5q6.xml 单 WebView 节点） | onCreate 中 getString(R.string.y1y2y3y4y5y6) 作为 URL 执行 loadUrl | 远端WebView | **原文**：不可静态还原（URL 为占位符 [SPY_MAX_INTENT]，页面正文由服务端下发）<br>**译注**：远端 HTML 承载的引导说明/伪装页面，内容不可静态确认 | 不可静态还原；由远端页面自行定义按钮与话术 | `ClassGen9.onCreate（loadUrl + setJavaScriptEnabled(true) + setAppCacheEnabled(false)）` |
| 3 | 引导说明页 | ClassGen9$1（WebViewClient） | 页面内任意链接/重定向触发 shouldOverrideUrlLoading | 远端WebView | 无 | 逐步点击远端页面的引导按钮（内容不可静态还原） | `spymax.stub7.ClassGen9$1.shouldOverrideUrlLoading` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载服务列表（预期目标页） | 不可静态还原：本地无 ACTION_ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 调用点，疑由远端页面 intent scheme 或二阶段反射 DEX 触发 | 不可静态还原 | 无 | 不可静态还原 | `全 DEX 检索 ACCESSIBILITY_SETTINGS / android.settings 无命中；ClassGen10.sl 反射加载入口（二阶段载荷不在包内）` |
| 5 | 获权后动作 | spymax.stub7.ClassGen12（AccessibilityService） | 用户在系统列表中手动开启服务 → onServiceConnected | 系统无障碍页 | **原文**：无（服务未声明 android:label / android:description，列表项仅显示应用名占位符）<br>**译注**：系统无障碍列表中的服务项无任何功能说明，仅有应用名 | 用户需手动打开开关（应用不自授权、不写 Settings） | `spymax.stub7.ClassGen12.onServiceConnected / AndroidManifest.xml service@ClassGen12` |
| 6 | 获权后动作 | ClassGen11$ta.doInBackground + ClassGen3.acc | C2 指令分支 cmn[11] 轮询执行 | 不可静态还原 | 无 | 无界面交互 | `spymax.stub7.ClassGen3.acc / spymax.stub7.ClassGen11$ta.doInBackground` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动 ClassGen9 内的全屏远端 WebView（res/layout/q1q2q3q4q5q6.xml，URL 来自 R.string.y1y2y3y4y5y6=[SPY_MAX_INTENT]）——唯一可能的引导文案呈现位置，内容完全由服务端下发，静态不可见
- 系统无障碍服务列表中 ClassGen12 的条目：无 android:label、无 android:description，仅回落显示应用名 @string/f1f2f3f4f5f6=[SPY_MAX_NAME_PATCH]
- 本地无任何呈现点：res/values/strings.xml 13 条字符串全部为 [SPY_MAX_*] 占位符；res/layout 仅一个 WebView 与一个 0×0 空 LinearLayout；全包无 AlertDialog、无 assets/HTML、无 raw 引导页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | [SPY_MAX_NAME_PATCH] | （打包期占位符，将替换为伪装应用名） | `res/values/strings.xml key f1f2f3f4f5f6（application@label 与无障碍服务回落名）` | 未知 |
| en | [SPY_MAX_INTENT] | （打包期占位符，将替换为远端引导页 URL，由 ClassGen9.loadUrl 加载） | `res/values/strings.xml key y1y2y3y4y5y6` | 未知 |
| en | [SPY_MAX_NAME_VICTIM] | （打包期占位符，将替换为目标受害者标识） | `res/values/strings.xml key z1z2z3z4z5z6` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：本地无 onResume/Timer 重跳无障碍设置的代码，也无 ACTION_ACCESSIBILITY_SETTINGS 调用；但 onBackPressed 优先执行 WebView.canGoBack()→goBack()，返回键被远端页面栈消费，用户无法直接退出引导流程，实际拒权反馈由远端页面决定
- **遮罩叠层 / 高仿系统设置页**：无高仿设置页与引导遮罩；唯一的 WindowManager 叠加是 ClassGen6 中 1×1、type=2006、gravity=51 的隐藏 SurfaceView（屏幕采集用途，非视觉引导）
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=22，本地无跳应用详情/受限设置的教学代码）
- **获权后即时行为与防撤权机制**：无：ClassGen3.acc 仅读取 Settings.Secure 校验，未写回；ClassGen12 未监听设置页或用 GLOBAL_ACTION_BACK/HOME 阻止撤权；但存在另一隐蔽手段——ClassGen11.onCreate 按占位配置可 setComponentEnabledSetting(ClassGen9,2,1) 自禁用桌面图标（见 R-002）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后首帧即拉起采集：hook ClassGen9.onCreate 执行 setContentView/loadUrl 的瞬间（或监测 Activity 栈出现 spymax.stub7.ClassGen9 且主题为 Translucent），持续录制其 WebView 页面栈的每一次 shouldOverrideUrlLoading 跳转，直至出现系统无障碍设置页或页面停留在引导页超过 3 秒
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：存在明显盲区：引导话术 100% 位于远端 HTML，静态仅能看到 WebView 载体；若远端页面以纯图片/GIF 呈现，UTG 文本为空需 OCR 兜底；跳转 ACCESSIBILITY_SETTINGS 的实现若在二阶段反射 DEX（ClassGen10.sl）中，则该阶段需动态 dump；另本样本虽非加壳（apkid 静态初判 False），但字符串全为占位符，运行期实际品牌名与 URL 只有动态才能取到。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导页（远端 WebView 首页）** | spymax.stub7.ClassGen9 + 全屏 WebView（id=web），无标题栏、状态栏可能透明 | 这是全样本唯一承载引导话术的界面，其文本、按钮、图像决定诱导性质（假更新/故障恐吓/安全伪装等），静态完全不可见，只能靠 UTG 取文本 | WebView 内全部可见文本与按钮 label；页面标题与地址栏痕迹（如有）；是否存在倒计时/无法关闭的按钮 |
| **跳转前教学页（WebView 内第 2 页及以后）** | 同一 ClassGen9 内 WebView 页面栈变化（shouldOverrideUrlLoading 被反复触发），URL 变化但 Activity 不变 | 证明页面流转被 WebViewClient 锁在应用内，可还原分步教学的具体步骤文案 | 页面 URL 或 DOM 变化序列；分步序号/箭头指引类文本；点击后是否停留在应用内而非跳到系统浏览器 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页，条目名为 [SPY_MAX_NAME_PATCH] 填充后的应用名，副标题为空 | 确认最终落点、服务显示名与'无描述'的隐蔽特征，是判定诱导闭环的关键一屏 | 服务条目显示名；是否存在功能说明副标题；开关初始状态 |
| **授权后返回页** | ClassGen9 WebView 再次前台，或应用界面消失/桌面图标被禁用 | 验证获权后是否自动前进、是否关闭页面，以及图标是否被自禁用 | 返回后页面文本变化；桌面是否仍存在应用图标；无障碍开关是否被自动打开 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `spymax.stub7.ClassGen9.onCreate`
- `spymax.stub7.ClassGen9$1.shouldOverrideUrlLoading`
- `spymax.stub7.ClassGen9.onBackPressed`
- `spymax.stub7.ClassGen3.acc`
- `spymax.stub7.ClassGen12.onServiceConnected`
- `res/layout/q1q2q3q4q5q6.xml / res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点（纯运行期 UTG 页面流转视角）

**1. 本地不存在任何"跳无障碍设置"的代码路径**
- 全 DEX 检索 `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`Settings.ACTION`、`android.settings` 均**零命中**；`AlertDialog` 零命中；`res/` 下无 `xml/`、`raw`、`assets` 引导页，`res/layout` 只有一个全屏 WebView 布局。
- 因此"点按钮 → 系统无障碍列表"这一步在本地不可静态还原，它只能发生在远端 WebView 页面或二阶段反射 DEX（`ClassGen10.sl`）中。

**2. 引导载体是冷启动即出现的全屏远端 WebView**
- 唯一 LAUNCHER 组件 [ClassGen9](<resource-unit:#1.dex1 code:spymax.stub7.ClassGen9#onCreate>) 使用 `Theme.Translucent.NoTitleBar`，`onCreate` 取 [res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml>) 中 `y1y2y3y4y5y6 = [SPY_MAX_INTENT]` 作为 URL 直接 `loadUrl`，并开启 JS、关缓存。
- [ClassGen9$1.shouldOverrideUrlLoading()](<resource-unit:#1.dex1 code:spymax.stub7.ClassGen9$1#shouldOverrideUrlLoading>) 无条件 `webView.loadUrl(str); return true;`——所有跳转都被锁在应用内 WebView，页面流转（含"下一步""去开启"按钮的后续页）完全由 C2 侧 HTML 决定。
- [ClassGen9#onBackPressed()](<resource-unit:#1.dex1 code:spymax.stub7.ClassGen9#onBackPressed>) 优先 `wv.canGoBack()→goBack()`，返回键被 WebView 的页面栈吞掉，用户难以退出引导流程。

**3. 授权检测是只读校验，无自授权/无防撤权**
- [ClassGen3.acc()](<resource-unit:#1.dex1 code:spymax.stub7.ClassGen3#acc>) 仅 `Settings$Secure.getString("enabled_accessibility_services")` 分割比对 `ComponentName`，无 `putString` 写回；无障碍服务 [ClassGen12#onServiceConnected()](<resource-unit:#1.dex1 code:spymax.stub7.ClassGen12#onServiceConnected>) 设 `flags=89 / eventTypes=-1 / feedbackType=16`，未调用 `GLOBAL_ACTION_BACK/HOME` 阻止撤权，也无 `isAccessibilityTool` 伪造。
- 授权结果由 C2 指令分支（`ClassGen11$ta.doInBackground` 中 `cmn[11]`）读取并回传，`cmn[12]` 可远程关停事件处理——即"是否要你开权限、何时要"由远端决定。

**4. 身份伪装与隐蔽**
- 无障碍服务 `ClassGen12` **既无 `android:label` 也无 `android:description`**，系统无障碍列表只能回落到应用 label `[SPY_MAX_NAME_PATCH]`，无任何功能说明，且应用主题为透明无标题——典型的"看不出是干什么的"入口。
- 悬浮窗并非引导遮罩：`ClassGen6.onStartCommand` 添加的是 `1×1 / type=2006 / gravity=51` 的隐藏 `SurfaceView`（屏幕采集），与"叠层引导"无关。
- 另经本轮确认：[ClassGen11#onCreate()](<resource-unit:#1.dex1 code:spymax.stub7.ClassGen11#onCreate>) 按占位配置可将唯一 LAUNCHER 组件 `setComponentEnabledSetting(...,2,1)` 自禁用（已登记 R-002），启动后桌面图标消失。

**5. 效率约束下的覆盖边界**
`[SPY_MAX_*]` 全部为打包期占位符，远端 HTML 正文与 `ClassGen10.sl` 加载的二阶段 DEX 不在包内；"用户在网页上看到什么文案、以何种话术被引到无障碍列表"属纯运行期远端内容，静态只能确认载体与流转骨架，不能确认话术。UTG 取证应聚焦冷启动那一屏 WebView 及其后续页面栈。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "本地代码/资源完整可见：启动页、WebView 配置、WebViewClient、无障碍服务、授权校验、C2 指令分支均可反编译确认；但引导文案与'跳转系统无障碍设置'的动作不在包内——页面内容为远端 HTML（URL 取自占位串 [SPY_MAX_INTENT]），跳转实现疑在远端页面的 intent scheme 或 ClassGen10.sl 反射加载的二阶段 DEX 中，13 个字符串全部为 [SPY_MAX_*] 占位符，无法静态还原。",
  "summary_one_liner": "冷启动即以透明主题全屏远端 WebView 呈现授权引导，所有页面跳转被 WebViewClient 强制锁在应用内，本地不含任何无障碍设置跳转与引导文案，授权状态仅被只读轮询并回传 C2，用户所见话术完全由服务端控制。",
  "disguise_identity": {
    "app_display_name": "[SPY_MAX_NAME_PATCH]（占位符，打包期替换为伪装名）",
    "claimed_brand_or_persona": "不可静态确认；本地无品牌、无文案、无说明页，仅有远端 WebView 作为唯一身份呈现面，判定为伪装/待填充状态",
    "a11y_service_label": "无 android:label（回落为应用名 [SPY_MAX_NAME_PATCH]），且无 android:description，系统无障碍列表不展示任何功能说明",
    "identity_mismatch": true,
    "obfuscation_tricks": "类名与资源名全量混淆（ClassGen1~14、q1q2q3q4q5q6、y1y2y3y4y5y6）；启动 Activity 采用 Theme.Translucent.NoTitleBar 无标题全屏；无障碍服务刻意省略 label 与 description 以隐藏功能；文本资源全部替换为 [SPY_MAX_*] 占位符由打包器注入；返回键被 WebView 页面栈消费；可按配置自禁用 LAUNCHER 组件使图标消失"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "spymax.stub7.ClassGen9（唯一 LAUNCHER Activity，Theme.Translucent.NoTitleBar）",
      "trigger_event": "用户点击桌面图标 → onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（Activity 无标题、无本地文案）",
      "shown_text_zh": "无标题透明全屏容器，进入即切换为 WebView 内容",
      "user_action_requested": "无明确请求，仅进入页面",
      "code_anchor": "spymax.stub7.ClassGen9.onCreate / AndroidManifest.xml application@theme"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "ClassGen9 内全屏 WebView（res/layout/q1q2q3q4q5q6.xml 单 WebView 节点）",
      "trigger_event": "onCreate 中 getString(R.string.y1y2y3y4y5y6) 作为 URL 执行 loadUrl",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "不可静态还原（URL 为占位符 [SPY_MAX_INTENT]，页面正文由服务端下发）",
      "shown_text_zh": "远端 HTML 承载的引导说明/伪装页面，内容不可静态确认",
      "user_action_requested": "不可静态还原；由远端页面自行定义按钮与话术",
      "code_anchor": "ClassGen9.onCreate（loadUrl + setJavaScriptEnabled(true) + setAppCacheEnabled(false)）"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "ClassGen9$1（WebViewClient）",
      "trigger_event": "页面内任意链接/重定向触发 shouldOverrideUrlLoading",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "无",
      "shown_text_zh": "所有跳转被强制在应用内 WebView 继续加载，不交给系统浏览器，形成受控的多步页面流转",
      "user_action_requested": "逐步点击远端页面的引导按钮（内容不可静态还原）",
      "code_anchor": "spymax.stub7.ClassGen9$1.shouldOverrideUrlLoading"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载服务列表（预期目标页）",
      "trigger_event": "不可静态还原：本地无 ACTION_ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 调用点，疑由远端页面 intent scheme 或二阶段反射 DEX 触发",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "预期由远端页面把用户引到系统无障碍列表，本地无任何对应代码或文案",
      "user_action_requested": "不可静态还原",
      "code_anchor": "全 DEX 检索 ACCESSIBILITY_SETTINGS / android.settings 无命中；ClassGen10.sl 反射加载入口（二阶段载荷不在包内）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "spymax.stub7.ClassGen12（AccessibilityService）",
      "trigger_event": "用户在系统列表中手动开启服务 → onServiceConnected",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（服务未声明 android:label / android:description，列表项仅显示应用名占位符）",
      "shown_text_zh": "系统无障碍列表中的服务项无任何功能说明，仅有应用名",
      "user_action_requested": "用户需手动打开开关（应用不自授权、不写 Settings）",
      "code_anchor": "spymax.stub7.ClassGen12.onServiceConnected / AndroidManifest.xml service@ClassGen12"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "ClassGen11$ta.doInBackground + ClassGen3.acc",
      "trigger_event": "C2 指令分支 cmn[11] 轮询执行",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "读取 Settings.Secure 的 enabled_accessibility_services 判断是否已授权，并将结果回传 C2；cmn[12] 可远程关闭事件处理",
      "user_action_requested": "无界面交互",
      "code_anchor": "spymax.stub7.ClassGen3.acc / spymax.stub7.ClassGen11$ta.doInBackground"
    }
  ],
  "text_presentation_locations": [
    "冷启动 ClassGen9 内的全屏远端 WebView（res/layout/q1q2q3q4q5q6.xml，URL 来自 R.string.y1y2y3y4y5y6=[SPY_MAX_INTENT]）——唯一可能的引导文案呈现位置，内容完全由服务端下发，静态不可见",
    "系统无障碍服务列表中 ClassGen12 的条目：无 android:label、无 android:description，仅回落显示应用名 @string/f1f2f3f4f5f6=[SPY_MAX_NAME_PATCH]",
    "本地无任何呈现点：res/values/strings.xml 13 条字符串全部为 [SPY_MAX_*] 占位符；res/layout 仅一个 WebView 与一个 0×0 空 LinearLayout；全包无 AlertDialog、无 assets/HTML、无 raw 引导页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "[SPY_MAX_NAME_PATCH]",
      "text_zh": "（打包期占位符，将替换为伪装应用名）",
      "source_location": "res/values/strings.xml key f1f2f3f4f5f6（application@label 与无障碍服务回落名）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "[SPY_MAX_INTENT]",
      "text_zh": "（打包期占位符，将替换为远端引导页 URL，由 ClassGen9.loadUrl 加载）",
      "source_location": "res/values/strings.xml key y1y2y3y4y5y6",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "[SPY_MAX_NAME_VICTIM]",
      "text_zh": "（打包期占位符，将替换为目标受害者标识）",
      "source_location": "res/values/strings.xml key z1z2z3z4z5z6",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：本地无 onResume/Timer 重跳无障碍设置的代码，也无 ACTION_ACCESSIBILITY_SETTINGS 调用；但 onBackPressed 优先执行 WebView.canGoBack()→goBack()，返回键被远端页面栈消费，用户无法直接退出引导流程，实际拒权反馈由远端页面决定",
    "overlay_or_fake_settings": "无高仿设置页与引导遮罩；唯一的 WindowManager 叠加是 ClassGen6 中 1×1、type=2006、gravity=51 的隐藏 SurfaceView（屏幕采集用途，非视觉引导）",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=22，本地无跳应用详情/受限设置的教学代码）",
    "post_grant_anti_removal": "无：ClassGen3.acc 仅读取 Settings.Secure 校验，未写回；ClassGen12 未监听设置页或用 GLOBAL_ACTION_BACK/HOME 阻止撤权；但存在另一隐蔽手段——ClassGen11.onCreate 按占位配置可 setComponentEnabledSetting(ClassGen9,2,1) 自禁用桌面图标（见 R-002）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后首帧即拉起采集：hook ClassGen9.onCreate 执行 setContentView/loadUrl 的瞬间（或监测 Activity 栈出现 spymax.stub7.ClassGen9 且主题为 Translucent），持续录制其 WebView 页面栈的每一次 shouldOverrideUrlLoading 跳转，直至出现系统无障碍设置页或页面停留在引导页超过 3 秒",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导页（远端 WebView 首页）",
        "page_identifier": "spymax.stub7.ClassGen9 + 全屏 WebView（id=web），无标题栏、状态栏可能透明",
        "why_most_useful": "这是全样本唯一承载引导话术的界面，其文本、按钮、图像决定诱导性质（假更新/故障恐吓/安全伪装等），静态完全不可见，只能靠 UTG 取文本",
        "observable_utg_signals": ["WebView 内全部可见文本与按钮 label", "页面标题与地址栏痕迹（如有）", "是否存在倒计时/无法关闭的按钮"]
      },
      {
        "page_role": "跳转前教学页（WebView 内第 2 页及以后）",
        "page_identifier": "同一 ClassGen9 内 WebView 页面栈变化（shouldOverrideUrlLoading 被反复触发），URL 变化但 Activity 不变",
        "why_most_useful": "证明页面流转被 WebViewClient 锁在应用内，可还原分步教学的具体步骤文案",
        "observable_utg_signals": ["页面 URL 或 DOM 变化序列", "分步序号/箭头指引类文本", "点击后是否停留在应用内而非跳到系统浏览器"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页，条目名为 [SPY_MAX_NAME_PATCH] 填充后的应用名，副标题为空",
        "why_most_useful": "确认最终落点、服务显示名与'无描述'的隐蔽特征，是判定诱导闭环的关键一屏",
        "observable_utg_signals": ["服务条目显示名", "是否存在功能说明副标题", "开关初始状态"]
      },
      {
        "page_role": "授权后返回页",
        "page_identifier": "ClassGen9 WebView 再次前台，或应用界面消失/桌面图标被禁用",
        "why_most_useful": "验证获权后是否自动前进、是否关闭页面，以及图标是否被自禁用",
        "observable_utg_signals": ["返回后页面文本变化", "桌面是否仍存在应用图标", "无障碍开关是否被自动打开"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "存在明显盲区：引导话术 100% 位于远端 HTML，静态仅能看到 WebView 载体；若远端页面以纯图片/GIF 呈现，UTG 文本为空需 OCR 兜底；跳转 ACCESSIBILITY_SETTINGS 的实现若在二阶段反射 DEX（ClassGen10.sl）中，则该阶段需动态 dump；另本样本虽非加壳（apkid 静态初判 False），但字符串全为占位符，运行期实际品牌名与 URL 只有动态才能取到。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "spymax.stub7.ClassGen9.onCreate",
    "spymax.stub7.ClassGen9$1.shouldOverrideUrlLoading",
    "spymax.stub7.ClassGen9.onBackPressed",
    "spymax.stub7.ClassGen3.acc",
    "spymax.stub7.ClassGen12.onServiceConnected",
    "res/layout/q1q2q3q4q5q6.xml / res/values/strings.xml"
  ]
}
```

</details>

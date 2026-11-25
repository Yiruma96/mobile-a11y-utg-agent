# MR_001__05c54c9c08｜RuMMS — СMС - Пoсланиe

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：115.2s

## 1. 一句话核心结论

- **核心申请方式**：应用无可见主界面，靠 962ms 后台轮询检测无障碍授权状态，未授权即每 9.77 秒用一条俄语『系统运行不正常』Toast 后强制跳转系统无障碍设置，服务名伪装成『Систeмный прoцecc（系统进程）』并省略用途说明，获权后还能用无障碍节点自行点击确认按钮。
- **静态可见性说明**：引导与授权链条全部位于 classes.dex 与 res 资源中，无加壳、无 AES/密文载荷、无 WebView/远端 HTML，可完整静态还原；仅获权后由 C2 http://hellowopung.com/g4lihra9pa66wsotb3ne/index.php 下发的指令集不在本命题范围内。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `05c54c9c0840a86e6358bc7ca93985aec36d03bcbad3d961952c2e23bf797222` |
| 包名 / 年份 | `ru.calendar.pen` / 2018 |
| 家族 / 品类 | **RuMMS**（同池样本数：516） |
| 原始来源标识 | https://www.zscaler.com/blogs/security-research/rumms-malware-back-enhancements |
| 桌面显示名 | СMС - Пoсланиe |
| 引导页宣称品牌/身份 | Систeмный прoцecc（系统进程／系统统计组件） |
| 系统无障碍列表服务名 | Систeмный прoцecc |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务标签冒用系统组件名义『Систeмный прoцecc』；标签与文案中使用西里尔/拉丁同形字混排（Сиcтeма 的 c、прoцecc 的 o/e 实为拉丁字符），规避肉眼与关键字比对；服务 meta-data 指向的 res/xml/pkhjk.xml 未声明 android:description，系统无障碍列表不显示任何用途说明；Launcher 页 Master 立即 finish，避免出现可核验的自有界面。 |
| 无障碍服务类名 | `ru.calendar.pen.Variety` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | ru.calendar.pen.Master（LAUNCHER Activity，Theme.Translucent.NoTitleBar.Fullscreen） | 用户点击桌面图标 → Activity.onCreate | 原生Activity | 无 | 无，用户看不到任何界面或选择 | `ru.calendar.pen.Master.onCreate` |
| 2 | 业务功能触发 | Application 常驻线程 Predict（HandlerThread）+ ContentIdentification$1.run 轮询任务 | ContentIdentification.onCreate 中 c() 启动 HandlerThread 并 post 轮询；每轮 finally 中 postDelayed(this, 962L) | 不可静态还原 | 无 | 无 | `ru.calendar.pen.ContentIdentification.onCreate / ru.calendar.pen.ContentIdentification$1.run` |
| 3 | 引导说明页 | Toast（无宿主 Activity 界面）+ 随即拉起的 ru.calendar.pen.FreshmanAnnual | c.b → c.f 读取 enabled_accessibility_services 未包含 ru.calendar.pen → c.c 在 9772ms 节流窗口到期时 startActivity(FreshmanAnnual) | 原生Activity | **原文**：Сиcтeма нe корректно рaботaет, вам нeобходимо включить дocтуп к статиcтике для 'Систeмный прoцecc'<br>**译注**：系统运行不正常，你需要为『系统进程』开启统计访问权限 | 无确认/取消/跳过按钮；Toast 展示后 FreshmanAnnual 立即跳转并 finish，用户只能被动跟随 | `ru.calendar.pen.FreshmanAnnual.onCreate（Toast getString(2131034112)）/ res/values/strings.xml accessibility_desc` |
| 4 | 跳无障碍设置 | 系统无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS），列表项标签『Систeмный прoцecc』 | FreshmanAnnual.onCreate 中 new Intent("android.settings.ACCESSIBILITY_SETTINGS") + FLAG_ACTIVITY_NEW_TASK，随后 finish() | 系统无障碍页 | **原文**：Систeмный прoцecc<br>**译注**：系统进程（列表项名称；无用途说明文字，因未声明 android:description） | 要求用户在系统列表中勾选『Систeмный прoцecc』开关并点击『允许/确定』；页面无应用侧取消入口 | `ru.calendar.pen.FreshmanAnnual.onCreate / AndroidManifest.xml service android:label / res/xml/pkhjk.xml` |
| 5 | 拒权反馈循环 | 后台轮询 → FreshmanAnnual → 系统无障碍设置页（反复压栈） | 用户返回或未开启开关，c.f 仍返回 false；9.77 秒后 c.c 再次 startActivity | 系统无障碍页 | **原文**：Сиcтeма нe корректно рaботaет, вам нeобходимо включить дocтуп к статиcтике для 'Систeмный прoцecc'<br>**译注**：系统运行不正常，你需要为『系统进程』开启统计访问权限（每次重跳前重复弹出） | 无退出通道：每次返回都会被重新推回系统无障碍设置页 | `ru.calendar.pen.c#boolean b(android.content.Context, long) / ru.calendar.pen.c#void c(android.content.Context, long)` |
| 6 | 获权后动作 | ru.calendar.pen.Variety（AccessibilityService），onAccessibilityEvent 中对节点 performAction(16) 点击 | 授权后系统事件到达；b 标志（Variety.a(true)，在 c.a 发短信路径置位）为真时进入 a(node) 分支 | 不可静态还原 | **原文**：android:id/button1 ; android:id/right_button ; да / ok / yes / delete / подтвердить / разрешить / отправить<br>**译注**：自动点击确认按钮（按资源 id 或俄语/英语确认词匹配后点击），使后续确认框无需用户操作即被批准 | 无；应用自行完成点击，用户不再参与 | `ru.calendar.pen.Variety#boolean a(android.view.accessibility.AccessibilityNodeInfo) / res/values/arrays.xml confirm_words` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- Toast（android.widget.Toast，时长 LENGTH_LONG）由 ru.calendar.pen.FreshmanAnnual.onCreate 在跳转前弹出，文案取自 res/values/strings.xml 的 accessibility_desc
- 系统无障碍服务列表项名称：AndroidManifest.xml 中 service ru.calendar.pen.Variety 的 android:label="Систeмный прoцecc"（同值另存于 strings.xml 的 accessibility_title）
- 系统无障碍列表项说明区域：空白——res/xml/pkhjk.xml 未声明 android:description，应用未提供任何用途说明
- 无 Activity 界面、无 Dialog、无 WebView/HTML、无悬浮窗 Overlay、无通知栏引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Сиcтeма нe корректно рaботaет, вам нeобходимо включить дocтуп к статиcтике для 'Систeмный прoцecc' | 系统运行不正常，你需要为『系统进程』开启统计访问权限 | `res/values/strings.xml key=accessibility_desc（FreshmanAnnual.onCreate 通过 getString(2131034112) 弹出）` | 故障恐吓 |
| ru | Систeмный прoцecc | 系统进程 | `AndroidManifest.xml service ru.calendar.pen.Variety android:label；res/values/strings.xml key=accessibility_title` | 假反诈安全 |
| ru | да / ok / yes / delete / подтвердить / разрешить / отправить | 是 / 好 / 是 / 删除 / 确认 / 允许 / 发送 | `res/values/arrays.xml string-array confirm_words（Variety.a 用于低版本节点文本匹配自动点击）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：用户从系统无障碍设置返回或未勾选开关时，常驻 962ms 轮询线程读 enabled_accessibility_services 仍不含 ru.calendar.pen，c.c 的 9772ms 节流窗口一到即再次 startActivity(FreshmanAnnual) → Toast → 重跳 ACCESSIBILITY_SETTINGS，形成持续 9.77 秒周期的强制重跳，无次数上限与降级退出
- **遮罩叠层 / 高仿系统设置页**：无悬浮窗遮罩、无高仿系统开关页；引导完全依赖系统原生无障碍设置页，仅以 Toast 承载说明，故不存在叠层遮罩
- **Android 13+ 受限设置（Restricted Settings）应对**：无。代码中未出现 ACTION_APPLICATION_DETAILS_SETTINGS，也无『右上角菜单→允许受限设置』或 Session 安装器绕过教学；应用 targetSdkVersion=27，本身不触发 Android 13 受限设置拦截
- **获权后即时行为与防撤权机制**：部分存在：服务自身具备自点确认能力（findAccessibilityNodeInfosByViewId 点击 android:id/button1 / right_button，低版本按 confirm_words 文本匹配点击），且 c.f 持续监控 enabled_accessibility_services，撤权后会立即被重新推回设置页；未发现使用 GLOBAL_ACTION_BACK/HOME 直接阻止撤权的逻辑（performGlobalAction(2) 用于按包名过滤后返回，属另一命题）
- **良性降级 / 替代方案**：无。未授权即无限重跳，不存在手动模式、仅观看模式或功能降级路径

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS（或当前前台 Activity 变为 com.android.settings 无障碍页）的瞬间立即开始 UTG 抓取；同时因跳转由 962ms 后台轮询驱动，可在冷启动后直接开始持续录屏/抓取，等待首个 Toast+跳转事件
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导链全部为原生 Toast + 系统设置页，无图片诱饵、无 WebView、无静默空文本页面。需注意 Launcher 页 Master 立即 finish，UTG 若只按 Activity 变化抓取可能漏掉首帧；建议冷启动后立刻开始持续抓取而非等待 Activity 事件。另应用 targetSdk=27，Android 13+ 设备上无障碍授权可能被受限设置拦截而表现为『开关置灰』，此时仍需按重跳循环页判定。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动跳转前的 Toast 说明页（宿主为透明 FreshmanAnnual，瞬间 finish）** | Toast 文本含『Сиcтeма нe корректно рaботaет』；前台 Activity 为 ru.calendar.pen.FreshmanAnnual | 这是应用对用户唯一的一句说明，可直接证明其以『系统运行不正常』故障恐吓替代真实功能说明，且无取消入口 | Toast 文本与 accessibility_desc 资源完全一致；Toast 出现后 ≤1s 内前台切到系统无障碍设置页；Toast 无任何按钮、无取消/跳过控件 |
| **系统无障碍服务列表页（跳转落点）** | com.android.settings 无障碍页，列表项名称『Систeмный прoцecc』 | 核对列表项名称伪装与说明区为空，是判定冒充系统组件、隐瞒权限用途的决定性画面 | 列表项 label 为『Систeмный прoцecc』而非应用名『СMС - Пoсланиe』；列表项描述区域为空字符串；列表中存在被勾选/未勾选开关的当前状态 |
| **拒权返回后的重跳循环页** | 用户返回键后前台短暂回到桌面/其他页，9~10 秒内前台再次变为 com.android.settings 无障碍页 | 证明拒绝后存在强制重跳循环（无退出路径），是区分恶意诱导与良性引导的关键动态证据 | 返回后 10s 内前台包名再次变为 com.android.settings；循环次数无上限、无降级界面；每次重跳前重复出现同一 Toast 文本 |
| **授权后自动点击确认行为** | 应用自身或其他 App 弹出的确认框被无触摸事件自动点击（android:id/button1 / right_button 或含『разрешить/подтвердить』文本的按钮） | 佐证无障碍服务被用于代替用户做出确认决策，是自我授权链的运行期证据 | 无 input 事件情况下按钮被点击（performAction(16) 无触摸注入）；点击目标为 android:id/button1 或 right_button；点击发生时无障碍服务 ru.calendar.pen.Variety 处于启用状态 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `ru.calendar.pen.FreshmanAnnual.onCreate`
- `ru.calendar.pen.c#void c(android.content.Context, long)`
- `ru.calendar.pen.c#boolean b(android.content.Context, long)`
- `ru.calendar.pen.ContentIdentification$1.run`
- `ru.calendar.pen.Variety#boolean a(android.view.accessibility.AccessibilityNodeInfo)`
- `res/values/strings.xml + res/xml/pkhjk.xml + res/values/arrays.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

- **无可见主界面**：Launcher 入口 [Master.onCreate()](<resource-unit:#1.dex1 code:ru.calendar.pen.Master#onCreate>) 直接调用 `finish()`；用户冷启动后看不到任何 UI。
- **跳转由后台轮询驱动，并非由用户操作触发**：Application 在启动时创建 `Predict` 线程，每 962ms 执行一次 [ContentIdentification$1.run()](<resource-unit:#1.dex1 code:ru.calendar.pen.ContentIdentification$1#run>)；该逻辑读取 `Settings.Secure.enabled_accessibility_services` 并判断其是否 `contains("ru.calendar.pen")`（见 [c.f](<resource-unit:#1.dex1 code:ru.calendar.pen.c#f>)），若未授权，则每 9772ms 无条件 `startActivity(FreshmanAnnual)`（见 [c.c](<resource-unit:#1.dex1 code:ru.calendar.pen.c#void c(android.content.Context, long)>)，并带有 `NEW_TASK` 标志）。
- **说明载体只有一条 Toast，随后直接跳转系统页**：[FreshmanAnnual.onCreate()](<resource-unit:#1.dex1 code:ru.calendar.pen.FreshmanAnnual#onCreate>) 只执行 `Toast(getString(2131034112))`，紧接着 `startActivity("android.settings.ACCESSIBILITY_SETTINGS")` 并 `finish()`。**没有自定义 Activity、Dialog、WebView、HTML 或悬浮窗**，也没有 `ACTION_APPLICATION_DETAILS_SETTINGS` 和 Android 13 受限设置教学。
- **身份伪装**：服务 `ru.calendar.pen.Variety` 的 `android:label` 是「Систeмный прoцecc」（系统进程），其中 `c/o/e` 与拉丁同形字混排；[pkhjk.xml](<resource-unit:#1 file:res/xml/pkhjk.xml>) **未声明 `android:description`**，因此系统无障碍列表中看不到任何用途说明，却声明了 `canRetrieveWindowContent=true`。
- **故障恐吓话术**：`accessibility_desc` 的原文是“系统运行不正常，你需要为『系统进程』开启统计访问权限”，纯属虚构，与实际功能无关。
- **获权后自行点击确认（取消用户决策）**：[Variety.a(node)](<resource-unit:#1.dex1 code:ru.calendar.pen.Variety#boolean a(android.view.accessibility.AccessibilityNodeInfo)>) 用 `findAccessibilityNodeInfosByViewId` 点击 `android:id/button1` / `right_button`，低版本回退到 [confirm_words](<resource-unit:#1 file:res/values/arrays.xml#L3-L12>)（да/ok/разрешить/подтвердить…）文本匹配点击；该标志由发短信路径 `c.a(...)` 中的 `Variety.a(true)` 置位。
- **拒绝即重跳**：用户从系统设置返回后，轮询在 9.77 秒内再次拉起设置页；整个流程无取消或跳过按钮，也没有降级路径。
- 引导链**完全静态可见**，无加壳、无密文载荷、无远端文案。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导与授权链条全部位于 classes.dex 与 res 资源中，无加壳、无 AES/密文载荷、无 WebView/远端 HTML，可完整静态还原；仅获权后由 C2 http://hellowopung.com/g4lihra9pa66wsotb3ne/index.php 下发的指令集不在本命题范围内。",
  "summary_one_liner": "应用无可见主界面，靠 962ms 后台轮询检测无障碍授权状态，未授权即每 9.77 秒用一条俄语『系统运行不正常』Toast 后强制跳转系统无障碍设置，服务名伪装成『Систeмный прoцecc（系统进程）』并省略用途说明，获权后还能用无障碍节点自行点击确认按钮。",
  "disguise_identity": {
    "app_display_name": "СMС - Пoсланиe",
    "claimed_brand_or_persona": "Систeмный прoцecc（系统进程／系统统计组件）",
    "a11y_service_label": "Систeмный прoцecc",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务标签冒用系统组件名义『Систeмный прoцecc』；标签与文案中使用西里尔/拉丁同形字混排（Сиcтeма 的 c、прoцecc 的 o/e 实为拉丁字符），规避肉眼与关键字比对；服务 meta-data 指向的 res/xml/pkhjk.xml 未声明 android:description，系统无障碍列表不显示任何用途说明；Launcher 页 Master 立即 finish，避免出现可核验的自有界面。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "ru.calendar.pen.Master（LAUNCHER Activity，Theme.Translucent.NoTitleBar.Fullscreen）",
      "trigger_event": "用户点击桌面图标 → Activity.onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（onCreate 中直接调用 finish()，不显示任何内容）",
      "user_action_requested": "无，用户看不到任何界面或选择",
      "code_anchor": "ru.calendar.pen.Master.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "Application 常驻线程 Predict（HandlerThread）+ ContentIdentification$1.run 轮询任务",
      "trigger_event": "ContentIdentification.onCreate 中 c() 启动 HandlerThread 并 post 轮询；每轮 finally 中 postDelayed(this, 962L)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；后台每约 962ms 检查一次无障碍授权状态",
      "user_action_requested": "无",
      "code_anchor": "ru.calendar.pen.ContentIdentification.onCreate / ru.calendar.pen.ContentIdentification$1.run"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "Toast（无宿主 Activity 界面）+ 随即拉起的 ru.calendar.pen.FreshmanAnnual",
      "trigger_event": "c.b → c.f 读取 enabled_accessibility_services 未包含 ru.calendar.pen → c.c 在 9772ms 节流窗口到期时 startActivity(FreshmanAnnual)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Сиcтeма нe корректно рaботaет, вам нeобходимо включить дocтуп к статиcтике для 'Систeмный прoцecc'",
      "shown_text_zh": "系统运行不正常，你需要为『系统进程』开启统计访问权限",
      "user_action_requested": "无确认/取消/跳过按钮；Toast 展示后 FreshmanAnnual 立即跳转并 finish，用户只能被动跟随",
      "code_anchor": "ru.calendar.pen.FreshmanAnnual.onCreate（Toast getString(2131034112)）/ res/values/strings.xml accessibility_desc"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS），列表项标签『Систeмный прoцecc』",
      "trigger_event": "FreshmanAnnual.onCreate 中 new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") + FLAG_ACTIVITY_NEW_TASK，随后 finish()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Систeмный прoцecc",
      "shown_text_zh": "系统进程（列表项名称；无用途说明文字，因未声明 android:description）",
      "user_action_requested": "要求用户在系统列表中勾选『Систeмный прoцecc』开关并点击『允许/确定』；页面无应用侧取消入口",
      "code_anchor": "ru.calendar.pen.FreshmanAnnual.onCreate / AndroidManifest.xml service android:label / res/xml/pkhjk.xml"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "后台轮询 → FreshmanAnnual → 系统无障碍设置页（反复压栈）",
      "trigger_event": "用户返回或未开启开关，c.f 仍返回 false；9.77 秒后 c.c 再次 startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Сиcтeма нe корректно рaботaет, вам нeобходимо включить дocтуп к статиcтике для 'Систeмный прoцecc'",
      "shown_text_zh": "系统运行不正常，你需要为『系统进程』开启统计访问权限（每次重跳前重复弹出）",
      "user_action_requested": "无退出通道：每次返回都会被重新推回系统无障碍设置页",
      "code_anchor": "ru.calendar.pen.c#boolean b(android.content.Context, long) / ru.calendar.pen.c#void c(android.content.Context, long)"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "ru.calendar.pen.Variety（AccessibilityService），onAccessibilityEvent 中对节点 performAction(16) 点击",
      "trigger_event": "授权后系统事件到达；b 标志（Variety.a(true)，在 c.a 发短信路径置位）为真时进入 a(node) 分支",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "android:id/button1 ; android:id/right_button ; да / ok / yes / delete / подтвердить / разрешить / отправить",
      "shown_text_zh": "自动点击确认按钮（按资源 id 或俄语/英语确认词匹配后点击），使后续确认框无需用户操作即被批准",
      "user_action_requested": "无；应用自行完成点击，用户不再参与",
      "code_anchor": "ru.calendar.pen.Variety#boolean a(android.view.accessibility.AccessibilityNodeInfo) / res/values/arrays.xml confirm_words"
    }
  ],
  "text_presentation_locations": [
    "Toast（android.widget.Toast，时长 LENGTH_LONG）由 ru.calendar.pen.FreshmanAnnual.onCreate 在跳转前弹出，文案取自 res/values/strings.xml 的 accessibility_desc",
    "系统无障碍服务列表项名称：AndroidManifest.xml 中 service ru.calendar.pen.Variety 的 android:label=\"Систeмный прoцecc\"（同值另存于 strings.xml 的 accessibility_title）",
    "系统无障碍列表项说明区域：空白——res/xml/pkhjk.xml 未声明 android:description，应用未提供任何用途说明",
    "无 Activity 界面、无 Dialog、无 WebView/HTML、无悬浮窗 Overlay、无通知栏引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Сиcтeма нe корректно рaботaет, вам нeобходимо включить дocтуп к статиcтике для 'Систeмный прoцecc'",
      "text_zh": "系统运行不正常，你需要为『系统进程』开启统计访问权限",
      "source_location": "res/values/strings.xml key=accessibility_desc（FreshmanAnnual.onCreate 通过 getString(2131034112) 弹出）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Систeмный прoцecc",
      "text_zh": "系统进程",
      "source_location": "AndroidManifest.xml service ru.calendar.pen.Variety android:label；res/values/strings.xml key=accessibility_title",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "ru",
      "text_verbatim": "да / ok / yes / delete / подтвердить / разрешить / отправить",
      "text_zh": "是 / 好 / 是 / 删除 / 确认 / 允许 / 发送",
      "source_location": "res/values/arrays.xml string-array confirm_words（Variety.a 用于低版本节点文本匹配自动点击）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "用户从系统无障碍设置返回或未勾选开关时，常驻 962ms 轮询线程读 enabled_accessibility_services 仍不含 ru.calendar.pen，c.c 的 9772ms 节流窗口一到即再次 startActivity(FreshmanAnnual) → Toast → 重跳 ACCESSIBILITY_SETTINGS，形成持续 9.77 秒周期的强制重跳，无次数上限与降级退出",
    "overlay_or_fake_settings": "无悬浮窗遮罩、无高仿系统开关页；引导完全依赖系统原生无障碍设置页，仅以 Toast 承载说明，故不存在叠层遮罩",
    "restricted_settings_13plus_coaching": "无。代码中未出现 ACTION_APPLICATION_DETAILS_SETTINGS，也无『右上角菜单→允许受限设置』或 Session 安装器绕过教学；应用 targetSdkVersion=27，本身不触发 Android 13 受限设置拦截",
    "post_grant_anti_removal": "部分存在：服务自身具备自点确认能力（findAccessibilityNodeInfosByViewId 点击 android:id/button1 / right_button，低版本按 confirm_words 文本匹配点击），且 c.f 持续监控 enabled_accessibility_services，撤权后会立即被重新推回设置页；未发现使用 GLOBAL_ACTION_BACK/HOME 直接阻止撤权的逻辑（performGlobalAction(2) 用于按包名过滤后返回，属另一命题）",
    "benign_graceful_degradation": "无。未授权即无限重跳，不存在手动模式、仅观看模式或功能降级路径"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS（或当前前台 Activity 变为 com.android.settings 无障碍页）的瞬间立即开始 UTG 抓取；同时因跳转由 962ms 后台轮询驱动，可在冷启动后直接开始持续录屏/抓取，等待首个 Toast+跳转事件",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动跳转前的 Toast 说明页（宿主为透明 FreshmanAnnual，瞬间 finish）",
        "page_identifier": "Toast 文本含『Сиcтeма нe корректно рaботaет』；前台 Activity 为 ru.calendar.pen.FreshmanAnnual",
        "why_most_useful": "这是应用对用户唯一的一句说明，可直接证明其以『系统运行不正常』故障恐吓替代真实功能说明，且无取消入口",
        "observable_utg_signals": ["Toast 文本与 accessibility_desc 资源完全一致", "Toast 出现后 ≤1s 内前台切到系统无障碍设置页", "Toast 无任何按钮、无取消/跳过控件"]
      },
      {
        "page_role": "系统无障碍服务列表页（跳转落点）",
        "page_identifier": "com.android.settings 无障碍页，列表项名称『Систeмный прoцecc』",
        "why_most_useful": "核对列表项名称伪装与说明区为空，是判定冒充系统组件、隐瞒权限用途的决定性画面",
        "observable_utg_signals": ["列表项 label 为『Систeмный прoцecc』而非应用名『СMС - Пoсланиe』", "列表项描述区域为空字符串", "列表中存在被勾选/未勾选开关的当前状态"]
      },
      {
        "page_role": "拒权返回后的重跳循环页",
        "page_identifier": "用户返回键后前台短暂回到桌面/其他页，9~10 秒内前台再次变为 com.android.settings 无障碍页",
        "why_most_useful": "证明拒绝后存在强制重跳循环（无退出路径），是区分恶意诱导与良性引导的关键动态证据",
        "observable_utg_signals": ["返回后 10s 内前台包名再次变为 com.android.settings", "循环次数无上限、无降级界面", "每次重跳前重复出现同一 Toast 文本"]
      },
      {
        "page_role": "授权后自动点击确认行为",
        "page_identifier": "应用自身或其他 App 弹出的确认框被无触摸事件自动点击（android:id/button1 / right_button 或含『разрешить/подтвердить』文本的按钮）",
        "why_most_useful": "佐证无障碍服务被用于代替用户做出确认决策，是自我授权链的运行期证据",
        "observable_utg_signals": ["无 input 事件情况下按钮被点击（performAction(16) 无触摸注入）", "点击目标为 android:id/button1 或 right_button", "点击发生时无障碍服务 ru.calendar.pen.Variety 处于启用状态"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导链全部为原生 Toast + 系统设置页，无图片诱饵、无 WebView、无静默空文本页面。需注意 Launcher 页 Master 立即 finish，UTG 若只按 Activity 变化抓取可能漏掉首帧；建议冷启动后立刻开始持续抓取而非等待 Activity 事件。另应用 targetSdk=27，Android 13+ 设备上无障碍授权可能被受限设置拦截而表现为『开关置灰』，此时仍需按重跳循环页判定。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "ru.calendar.pen.FreshmanAnnual.onCreate",
    "ru.calendar.pen.c#void c(android.content.Context, long)",
    "ru.calendar.pen.c#boolean b(android.content.Context, long)",
    "ru.calendar.pen.ContentIdentification$1.run",
    "ru.calendar.pen.Variety#boolean a(android.view.accessibility.AccessibilityNodeInfo)",
    "res/values/strings.xml + res/xml/pkhjk.xml + res/values/arrays.xml"
  ]
}
```

</details>

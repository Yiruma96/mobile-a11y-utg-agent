# MR_167__c0cfd462ab｜Asacub — CMС - Сообщeние

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：120.9s

## 1. 一句话核心结论

- **核心申请方式**：应用在 Application.onCreate 启动常驻定时循环，检测到无障碍未授权就弹俄语假系统故障 Toast 并直跳系统无障碍设置页，返回后约每10.5秒重复拉起且配前台通知同文案施压，获权后再用无障碍自动点击系统确认按钮，全程无取消入口。
- **静态可见性说明**：引导链路全部位于 classes.dex，可完整静态还原：Application.onCreate 启动的 HandlerThread 循环、Settings.Secure 授权检查、Nail 的 Toast 与 ACCESSIBILITY_SETTINGS 跳转、无障碍服务的自动点击逻辑均为明文；包内无 assets/、无 HTML/JS、无加壳与密文载荷，无远端页面参与引导。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c0cfd462ab21f6798e962515ac0c15a92036edd3e2e63639263bf2fd2a10c184` |
| 包名 / 年份 | `com.amputate.volunteer` / 2018 |
| 家族 / 品类 | **Asacub**（同池样本数：9） |
| 原始来源标识 | https://securelist.com/the-rise-of-mobile-banker-asacub/87591/ |
| 桌面显示名 | CMС - Сообщeние |
| 引导页宣称品牌/身份 | 伪装为俄语系统的『消息/短信』类系统组件（Сообщение），并在提示中以系统进程『Основнoй процесс』自居，声称系统运行异常需开启统计访问权限 |
| 系统无障碍列表服务名 | Основнoй процесс |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：多处拉丁同形字混入西里尔文：桌面名 CMС 首字母为拉丁 C、Сообщeние 含拉丁 e；服务标签 Основнoй 含拉丁 o；提示文案 Сиcтeмa нe коррeктнo рaботаeт 中 C/e/a/o 均为拉丁字符。无障碍服务未声明 android:description，系统无障碍列表不显示任何用途说明；界面主题为 Theme.Translucent.NoTitleBar 且引导 Activity 均 noHistory/finish，不留可回溯页面。未使用 activity-alias、未伪造 isAccessibilityTool（targetSdk 27 早于该机制）。 |
| 无障碍服务类名 | `com.amputate.volunteer.BaseballSentiment` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.amputate.volunteer.PromoteHair (Application) / com.amputate.volunteer.Demonstrator (前台 Service) | Application.onCreate：启动 Demonstrator 前台服务、创建 HandlerThread("Possibility")、调用 c() 以 postDelayed(1098ms) 自循环 | 不可静态还原 | 无 | 无（用户仅启动应用） | `com.amputate.volunteer.PromoteHair.onCreate / com.amputate.volunteer.PromoteHair.c` |
| 2 | 业务功能触发 | com.amputate.volunteer.PromoteHair$1 (Runnable) + com.amputate.volunteer.c.f | HandlerThread 每轮 run() 调用 c.b(context, now)，经 c.f 读取 Settings.Secure.enabled_accessibility_services 判断是否 contains("com.amputate.volunteer") | 不可静态还原 | 无 | 无（已授权则跳过后续引导，未授权则进入引导） | `com.amputate.volunteer.PromoteHair$1.run / com.amputate.volunteer.c.f` |
| 3 | 拒权反馈循环 | com.amputate.volunteer.c.c(Context, long) → com.amputate.volunteer.Nail (Activity) | 未授权时 c.c 以 j - a > 10453（约10.5秒）为门槛，带 FLAG_ACTIVITY_NEW_TASK\|FLAG_ACTIVITY_CLEAR_TASK 启动 Nail | 不可静态还原 | 无 | 无（无取消/跳过，只能再次进入设置页） | `com.amputate.volunteer.c.c / com.amputate.volunteer.PromoteHair$1.run` |
| 4 | 引导说明页 | Toast（Nail.onCreate 内）+ 前台常驻通知（Demonstrator.a） | Nail.onCreate 首行 Toast.makeText(...).show()；Demonstrator.onCreate 调用 a() 执行 startForeground(1609, ...) | 原生Dialog | **原文**：Сиcтeмa нe коррeктнo рaботаeт, вaм необхoдимo включить дoступ к cтатиcтикe для 'Основнoй процесс'<br>**译注**：系统运行不正确，您需要为“Основнoй процесс”开启统计访问权限 | 无任何按钮；文案要求用户去开启无障碍统计权限（通知栏同一文案持续驻留） | `com.amputate.volunteer.Nail.onCreate / com.amputate.volunteer.Demonstrator.a` |
| 5 | 跳无障碍设置 | android.settings.ACCESSIBILITY_SETTINGS 系统页 | Nail.onCreate 中 new Intent("android.settings.ACCESSIBILITY_SETTINGS") 加 FLAG_ACTIVITY_NEW_TASK 后 startActivity，随即 finish() | 系统无障碍页 | **原文**：Основнoй процесс<br>**译注**：系统无障碍服务列表中显示服务名“主进程”，无 android:description 用途说明 | 要求用户点击系统无障碍列表中的“Основнoй процесс”并开启开关（页面本身无引导说明，无取消/返回即被循环重拉） | `com.amputate.volunteer.Nail.onCreate / #1 manifest:components / res/xml/jaoyiydjf.xml` |
| 6 | 获权后动作 | com.amputate.volunteer.BaseballSentiment (AccessibilityService) 自动点击系统设置按钮 | onAccessibilityEvent 收到 typeWindowContentChanged/StateChanged 事件后，调用 a(AccessibilityNodeInfo) 遍历节点 | 不可静态还原 | **原文**：com.android.settings:id/right_button \| com.android.settings:id/button1 \| com.android.settings:id/restricted_action \| com.android.settings:id/action_button \| да / ок / подтвердить / разрешить / отправить / активировать<br>**译注**：自动查找并点击系统设置页的确认类按钮，或文本为“是/确定/确认/允许/发送/激活”的节点 | 无（由服务代替用户点击 performAction(16)）；命中后置 b=false 并调用 performGlobalAction(2) 回退 | `com.amputate.volunteer.BaseballSentiment.onAccessibilityEvent / com.amputate.volunteer.BaseballSentiment.a(AccessibilityNodeInfo)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- Nail.onCreate 中的原生 Toast（LENGTH_LONG=1）：假系统故障文案，短暂浮层，无按钮
- Demonstrator.a 中的 startForeground(1609) 常驻通知：标题『Основнoй процесс』+ 与 Toast 完全相同的正文，不可清除、跨重启持续
- 跳转后的系统无障碍设置页列表项：仅显示服务标签『Основнoй процесс』，无 android:description，故无任何用途说明文字
- 无 AlertDialog 说明页、无 assets HTML/WebView 教学页、无悬浮窗遮罩、无 GIF/图片引导（包内不存在 assets/ 目录）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Сиcтeмa нe коррeктнo рaботаeт, вaм необхoдимo включить дoступ к cтатиcтикe для 'Основнoй процесс' | 系统运行不正确，您需要为“Основнoй процесс”开启统计访问权限 | `硬编码于 com.amputate.volunteer.Nail.onCreate 与 com.amputate.volunteer.Demonstrator.a（含拉丁同形字 C/e/a/o）` | 故障恐吓 |
| ru | Основнoй процесс | 主进程 | `AndroidManifest.xml 中 BaseballSentiment 的 android:label；同时用作通知标题` | 假系统组件身份 |
| ru | CMС - Сообщeние | CMС - 消息 | `AndroidManifest.xml application android:label` | 假系统组件身份 |
| ru | да | 是 | `com.amputate.volunteer.BaseballSentiment 字段 a 字符串数组（自动点击确认按钮的文本匹配表）` | 未知 |
| ru | ок | 确定 | `com.amputate.volunteer.BaseballSentiment 字段 a 字符串数组` | 未知 |
| ru | подтвердить | 确认 | `com.amputate.volunteer.BaseballSentiment 字段 a 字符串数组` | 未知 |
| ru | разрешить | 允许 | `com.amputate.volunteer.BaseballSentiment 字段 a 字符串数组` | 未知 |
| ru | отправить | 发送 | `com.amputate.volunteer.BaseballSentiment 字段 a 字符串数组` | 未知 |
| ru | активировать | 激活 | `com.amputate.volunteer.BaseballSentiment 字段 a 字符串数组` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：从系统设置返回后，PromoteHair$1.run 仍在每约1秒一轮的循环中调用 c.b→c.f 复查 Settings.Secure；未授权时 c.c 以 10453ms 门槛再次 startActivity(Nail)，带 FLAG_ACTIVITY_CLEAR_TASK 清栈，形成无上限的强制重跳；同时 startForeground 常驻通知持续显示同一假故障文案，无「稍后」「不再提醒」选项。
- **遮罩叠层 / 高仿系统设置页**：无遮罩层、无悬浮窗、无高仿无障碍开关页；仅使用原生 Toast + 系统通知 + 直接跳转真实系统设置页，并在设置页内由无障碍服务自动点击确认按钮。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion 27，未涉及 Android 13 受限设置分步教学；但同一循环会另行拉起 ACTION_CHANGE_DEFAULT 默认短信应用设置与 DishPump 设备管理器激活页，DishPump 的 ADD_EXPLANATION 传空串）
- **获权后即时行为与防撤权机制**：有：BaseballSentiment.onAccessibilityEvent 对 com.android.settings 页面节点按 right_button/button1/restricted_action/action_button 及俄文确认文本执行 performAction(16) 自动确认，并在处理完后调用 performGlobalAction(2)（GLOBAL_ACTION_BACK）离开设置页；循环持续检测 enabled_accessibility_services，撤权后立即重新进入引导链。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条最佳时机：(1) 冷启动后约1.1秒首次弹出 Toast 并跳转的瞬间——Hook startActivity 监测 Intent action 等于 android.settings.ACCESSIBILITY_SETTINGS，同时抓取 Toast 文本；(2) 系统无障碍设置页停留期间，监测无障碍服务对 com.android.settings 节点执行 ACTION_CLICK 的时刻，用于捕获自动确认行为。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：全部文案为可提取文本节点（Toast/通知/系统列表项），无纯图引导。唯一需注意的是文案大量使用拉丁同形字（Сиcтeмa、Основнoй、Сообщeние），文本规则匹配需做 Unicode 同形字归一化，否则俄语关键词可能漏检；另 Toast 存在时长受系统限制，需在跳转瞬间同步采样。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（假系统故障 Toast）** | Nail Activity 启动瞬间的全屏 Toast，文本以『Сиcтeмa нe коррeктнo рaботаeт』开头；宿主进程 com.amputate.volunteer | 这是唯一承载诱导说辞的界面，且文案把「申请无障碍」伪装成「系统故障修复」，是判定故障恐吓式诱导的决定性页面 | Toast 文本节点含『нe коррeктнo рaботаeт』与『дoступ к cтатиcтикe』；Toast 出现前 1 秒内发生 ACTION_ACCESSIBILITY_SETTINGS 跳转；无任何按钮/取消控件的空节点树 |
| **通知栏施压项** | 通知渠道 com.amputate.volunteer.SUIT（名称 Echo），通知 id 1609，标题『Основнoй процесс』 | 证明施压是持续的而非一次性弹窗，可用于区分良性一次性说明与强迫式引导 | 常驻前台通知存在且正文与 Toast 完全一致；通知不可被用户清除（startForeground） |
| **系统无障碍服务列表项** | Settings 中 service 标签『Основнoй процесс』，description 为空 | 确认用户被引导授予的对象，以及系统侧是否展示任何用途说明（此处为空，属信息缺失） | 列表项文本『Основнoй процесс』无副标题说明；该文本含拉丁 o 同形字 |
| **设置页后自动确认点击** | com.android.settings 页面节点被 ACTION_CLICK 命中，资源 id 为 right_button/button1/restricted_action/action_button | 直接证明「用户主动授权」被绕过，是权限诱导升级为自动授权的关键判别点 | 无障碍服务进程对 settings 包节点执行 ACTION_CLICK 的事件序列；点击后紧接 GLOBAL_ACTION_BACK 回退；点击目标节点文本匹配 да/ок/подтвердить/разрешить |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.amputate.volunteer.Nail.onCreate`
- `com.amputate.volunteer.PromoteHair.onCreate`
- `com.amputate.volunteer.PromoteHair$1.run`
- `com.amputate.volunteer.c.f / com.amputate.volunteer.c.c`
- `com.amputate.volunteer.Demonstrator.a`
- `com.amputate.volunteer.BaseballSentiment.onAccessibilityEvent / res/xml/jaoyiydjf.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**整体判定：纯运行期诱导，代码完全静态可见，无 WebView、无 HTML、无悬浮窗、无加壳。**

- **冷启动即触发**：`Application`（`PromoteHair`）的 `onCreate` 启动常驻 HandlerThread（名为 `Possibility`），并用 `postDelayed(1098ms)` 形成自循环；首次循环时，[c.c(Context, long)](<resource-unit:#1.dex1 code:com.amputate.volunteer.c#void c(android.content.Context, long)>) 中的静态时间基准 `a` 为 0，条件 `j - a > 10453` 必然成立，因此立即拉起引导页。
- **授权状态判定**：唯一依据是 `Settings.Secure.enabled_accessibility_services` 是否 `contains("com.amputate.volunteer")`（[c.f()](<resource-unit:#1.dex1 code:com.amputate.volunteer.c#f>)），不区分具体服务，也未做任何用途说明。
- **引导载体是原生 Toast 加系统设置页跳转**：[Nail.onCreate()](<resource-unit:#1.dex1 code:com.amputate.volunteer.Nail#onCreate>) 弹出俄语“系统运行不正确，您需要为‘Основнoй процесс’开启统计访问权限”Toast，随即执行 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` 并 `finish()`，用户没有任何取消或跳过按钮。
- **拒权死循环**：从系统设置返回后，循环约每 10.5 秒重新拉起 `Nail`，并用 `FLAG_ACTIVITY_CLEAR_TASK` 清除任务栈；同时 [Demonstrator.a()](<resource-unit:#1.dex1 code:com.amputate.volunteer.Demonstrator#a>) 用 `startForeground` 常驻通知重复同一文案，形成通知栏持续施压。
- **获权后代替用户点击**：[BaseballSentiment](<resource-unit:#1.dex1 code:com.amputate.volunteer.BaseballSentiment#onAccessibilityEvent>) 在无障碍配置 [res/xml/jaoyiydjf.xml](<resource-unit:#1 file:res/xml/jaoyiydjf.xml>) 中声明 `canRetrieveWindowContent=true`，并声明 `flagReportViewIds`；它按系统按钮 ID（`right_button`/`button1`/`restricted_action`/`action_button`）或俄文按钮文本（да/ок/подтвердить/разрешить/отправить/активировать）执行 `performAction(16)` 自动点击，并在监听命中后调用 `GLOBAL_ACTION_BACK(2)` 回退。
- **身份混淆**：桌面名 `CMС - Сообщeние` 和无障碍标签 `Основнoй процесс` 都把拉丁同形字（`C`/`e`/`o`）混入西里尔文；无障碍服务未配置 `android:description`，因此系统无障碍列表中不显示任何用途说明。
- **旁路设置**：同循环还会拉起 `ACTION_CHANGE_DEFAULT`（默认短信应用）和 `DishPump`（设备管理器激活，`ADD_EXPLANATION` 传空串），进一步说明本应用的目标是批量获取受限权限。
- **无 WebView/无 overlay**：解包目录仅含 `res`、`AndroidManifest.xml`、`classes.dex`，没有 `assets/`、HTML 或 JS，故排除远端教学页与悬浮遮罩路径。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链路全部位于 classes.dex，可完整静态还原：Application.onCreate 启动的 HandlerThread 循环、Settings.Secure 授权检查、Nail 的 Toast 与 ACCESSIBILITY_SETTINGS 跳转、无障碍服务的自动点击逻辑均为明文；包内无 assets/、无 HTML/JS、无加壳与密文载荷，无远端页面参与引导。",
  "summary_one_liner": "应用在 Application.onCreate 启动常驻定时循环，检测到无障碍未授权就弹俄语假系统故障 Toast 并直跳系统无障碍设置页，返回后约每10.5秒重复拉起且配前台通知同文案施压，获权后再用无障碍自动点击系统确认按钮，全程无取消入口。",
  "disguise_identity": {
    "app_display_name": "CMС - Сообщeние",
    "claimed_brand_or_persona": "伪装为俄语系统的『消息/短信』类系统组件（Сообщение），并在提示中以系统进程『Основнoй процесс』自居，声称系统运行异常需开启统计访问权限",
    "a11y_service_label": "Основнoй процесс",
    "identity_mismatch": true,
    "obfuscation_tricks": "多处拉丁同形字混入西里尔文：桌面名 CMС 首字母为拉丁 C、Сообщeние 含拉丁 e；服务标签 Основнoй 含拉丁 o；提示文案 Сиcтeмa нe коррeктнo рaботаeт 中 C/e/a/o 均为拉丁字符。无障碍服务未声明 android:description，系统无障碍列表不显示任何用途说明；界面主题为 Theme.Translucent.NoTitleBar 且引导 Activity 均 noHistory/finish，不留可回溯页面。未使用 activity-alias、未伪造 isAccessibilityTool（targetSdk 27 早于该机制）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.amputate.volunteer.PromoteHair (Application) / com.amputate.volunteer.Demonstrator (前台 Service)",
      "trigger_event": "Application.onCreate：启动 Demonstrator 前台服务、创建 HandlerThread(\"Possibility\")、调用 c() 以 postDelayed(1098ms) 自循环",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；此步仅建立后台循环与前台服务骨架",
      "user_action_requested": "无（用户仅启动应用）",
      "code_anchor": "com.amputate.volunteer.PromoteHair.onCreate / com.amputate.volunteer.PromoteHair.c"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.amputate.volunteer.PromoteHair$1 (Runnable) + com.amputate.volunteer.c.f",
      "trigger_event": "HandlerThread 每轮 run() 调用 c.b(context, now)，经 c.f 读取 Settings.Secure.enabled_accessibility_services 判断是否 contains(\"com.amputate.volunteer\")",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；后台轮询无障碍授权状态",
      "user_action_requested": "无（已授权则跳过后续引导，未授权则进入引导）",
      "code_anchor": "com.amputate.volunteer.PromoteHair$1.run / com.amputate.volunteer.c.f"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.amputate.volunteer.c.c(Context, long) → com.amputate.volunteer.Nail (Activity)",
      "trigger_event": "未授权时 c.c 以 j - a > 10453（约10.5秒）为门槛，带 FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TASK 启动 Nail",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；用户从系统设置返回后约每10.5秒被再次强制拉起引导页",
      "user_action_requested": "无（无取消/跳过，只能再次进入设置页）",
      "code_anchor": "com.amputate.volunteer.c.c / com.amputate.volunteer.PromoteHair$1.run"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "Toast（Nail.onCreate 内）+ 前台常驻通知（Demonstrator.a）",
      "trigger_event": "Nail.onCreate 首行 Toast.makeText(...).show()；Demonstrator.onCreate 调用 a() 执行 startForeground(1609, ...)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Сиcтeмa нe коррeктнo рaботаeт, вaм необхoдимo включить дoступ к cтатиcтикe для 'Основнoй процесс'",
      "shown_text_zh": "系统运行不正确，您需要为“Основнoй процесс”开启统计访问权限",
      "user_action_requested": "无任何按钮；文案要求用户去开启无障碍统计权限（通知栏同一文案持续驻留）",
      "code_anchor": "com.amputate.volunteer.Nail.onCreate / com.amputate.volunteer.Demonstrator.a"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "android.settings.ACCESSIBILITY_SETTINGS 系统页",
      "trigger_event": "Nail.onCreate 中 new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") 加 FLAG_ACTIVITY_NEW_TASK 后 startActivity，随即 finish()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Основнoй процесс",
      "shown_text_zh": "系统无障碍服务列表中显示服务名“主进程”，无 android:description 用途说明",
      "user_action_requested": "要求用户点击系统无障碍列表中的“Основнoй процесс”并开启开关（页面本身无引导说明，无取消/返回即被循环重拉）",
      "code_anchor": "com.amputate.volunteer.Nail.onCreate / #1 manifest:components / res/xml/jaoyiydjf.xml"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.amputate.volunteer.BaseballSentiment (AccessibilityService) 自动点击系统设置按钮",
      "trigger_event": "onAccessibilityEvent 收到 typeWindowContentChanged/StateChanged 事件后，调用 a(AccessibilityNodeInfo) 遍历节点",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "com.android.settings:id/right_button | com.android.settings:id/button1 | com.android.settings:id/restricted_action | com.android.settings:id/action_button | да / ок / подтвердить / разрешить / отправить / активировать",
      "shown_text_zh": "自动查找并点击系统设置页的确认类按钮，或文本为“是/确定/确认/允许/发送/激活”的节点",
      "user_action_requested": "无（由服务代替用户点击 performAction(16)）；命中后置 b=false 并调用 performGlobalAction(2) 回退",
      "code_anchor": "com.amputate.volunteer.BaseballSentiment.onAccessibilityEvent / com.amputate.volunteer.BaseballSentiment.a(AccessibilityNodeInfo)"
    }
  ],
  "text_presentation_locations": [
    "Nail.onCreate 中的原生 Toast（LENGTH_LONG=1）：假系统故障文案，短暂浮层，无按钮",
    "Demonstrator.a 中的 startForeground(1609) 常驻通知：标题『Основнoй процесс』+ 与 Toast 完全相同的正文，不可清除、跨重启持续",
    "跳转后的系统无障碍设置页列表项：仅显示服务标签『Основнoй процесс』，无 android:description，故无任何用途说明文字",
    "无 AlertDialog 说明页、无 assets HTML/WebView 教学页、无悬浮窗遮罩、无 GIF/图片引导（包内不存在 assets/ 目录）"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Сиcтeмa нe коррeктнo рaботаeт, вaм необхoдимo включить дoступ к cтатиcтикe для 'Основнoй процесс'",
      "text_zh": "系统运行不正确，您需要为“Основнoй процесс”开启统计访问权限",
      "source_location": "硬编码于 com.amputate.volunteer.Nail.onCreate 与 com.amputate.volunteer.Demonstrator.a（含拉丁同形字 C/e/a/o）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Основнoй процесс",
      "text_zh": "主进程",
      "source_location": "AndroidManifest.xml 中 BaseballSentiment 的 android:label；同时用作通知标题",
      "rhetorical_frame": "假系统组件身份"
    },
    {
      "lang": "ru",
      "text_verbatim": "CMС - Сообщeние",
      "text_zh": "CMС - 消息",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "假系统组件身份"
    },
    {
      "lang": "ru",
      "text_verbatim": "да",
      "text_zh": "是",
      "source_location": "com.amputate.volunteer.BaseballSentiment 字段 a 字符串数组（自动点击确认按钮的文本匹配表）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "ru",
      "text_verbatim": "ок",
      "text_zh": "确定",
      "source_location": "com.amputate.volunteer.BaseballSentiment 字段 a 字符串数组",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "ru",
      "text_verbatim": "подтвердить",
      "text_zh": "确认",
      "source_location": "com.amputate.volunteer.BaseballSentiment 字段 a 字符串数组",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "ru",
      "text_verbatim": "разрешить",
      "text_zh": "允许",
      "source_location": "com.amputate.volunteer.BaseballSentiment 字段 a 字符串数组",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "ru",
      "text_verbatim": "отправить",
      "text_zh": "发送",
      "source_location": "com.amputate.volunteer.BaseballSentiment 字段 a 字符串数组",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "ru",
      "text_verbatim": "активировать",
      "text_zh": "激活",
      "source_location": "com.amputate.volunteer.BaseballSentiment 字段 a 字符串数组",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "从系统设置返回后，PromoteHair$1.run 仍在每约1秒一轮的循环中调用 c.b→c.f 复查 Settings.Secure；未授权时 c.c 以 10453ms 门槛再次 startActivity(Nail)，带 FLAG_ACTIVITY_CLEAR_TASK 清栈，形成无上限的强制重跳；同时 startForeground 常驻通知持续显示同一假故障文案，无「稍后」「不再提醒」选项。",
    "overlay_or_fake_settings": "无遮罩层、无悬浮窗、无高仿无障碍开关页；仅使用原生 Toast + 系统通知 + 直接跳转真实系统设置页，并在设置页内由无障碍服务自动点击确认按钮。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion 27，未涉及 Android 13 受限设置分步教学；但同一循环会另行拉起 ACTION_CHANGE_DEFAULT 默认短信应用设置与 DishPump 设备管理器激活页，DishPump 的 ADD_EXPLANATION 传空串）",
    "post_grant_anti_removal": "有：BaseballSentiment.onAccessibilityEvent 对 com.android.settings 页面节点按 right_button/button1/restricted_action/action_button 及俄文确认文本执行 performAction(16) 自动确认，并在处理完后调用 performGlobalAction(2)（GLOBAL_ACTION_BACK）离开设置页；循环持续检测 enabled_accessibility_services，撤权后立即重新进入引导链。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条最佳时机：(1) 冷启动后约1.1秒首次弹出 Toast 并跳转的瞬间——Hook startActivity 监测 Intent action 等于 android.settings.ACCESSIBILITY_SETTINGS，同时抓取 Toast 文本；(2) 系统无障碍设置页停留期间，监测无障碍服务对 com.android.settings 节点执行 ACTION_CLICK 的时刻，用于捕获自动确认行为。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（假系统故障 Toast）",
        "page_identifier": "Nail Activity 启动瞬间的全屏 Toast，文本以『Сиcтeмa нe коррeктнo рaботаeт』开头；宿主进程 com.amputate.volunteer",
        "why_most_useful": "这是唯一承载诱导说辞的界面，且文案把「申请无障碍」伪装成「系统故障修复」，是判定故障恐吓式诱导的决定性页面",
        "observable_utg_signals": ["Toast 文本节点含『нe коррeктнo рaботаeт』与『дoступ к cтатиcтикe』", "Toast 出现前 1 秒内发生 ACTION_ACCESSIBILITY_SETTINGS 跳转", "无任何按钮/取消控件的空节点树"]
      },
      {
        "page_role": "通知栏施压项",
        "page_identifier": "通知渠道 com.amputate.volunteer.SUIT（名称 Echo），通知 id 1609，标题『Основнoй процесс』",
        "why_most_useful": "证明施压是持续的而非一次性弹窗，可用于区分良性一次性说明与强迫式引导",
        "observable_utg_signals": ["常驻前台通知存在且正文与 Toast 完全一致", "通知不可被用户清除（startForeground）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 中 service 标签『Основнoй процесс』，description 为空",
        "why_most_useful": "确认用户被引导授予的对象，以及系统侧是否展示任何用途说明（此处为空，属信息缺失）",
        "observable_utg_signals": ["列表项文本『Основнoй процесс』无副标题说明", "该文本含拉丁 o 同形字"]
      },
      {
        "page_role": "设置页后自动确认点击",
        "page_identifier": "com.android.settings 页面节点被 ACTION_CLICK 命中，资源 id 为 right_button/button1/restricted_action/action_button",
        "why_most_useful": "直接证明「用户主动授权」被绕过，是权限诱导升级为自动授权的关键判别点",
        "observable_utg_signals": ["无障碍服务进程对 settings 包节点执行 ACTION_CLICK 的事件序列", "点击后紧接 GLOBAL_ACTION_BACK 回退", "点击目标节点文本匹配 да/ок/подтвердить/разрешить"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：全部文案为可提取文本节点（Toast/通知/系统列表项），无纯图引导。唯一需注意的是文案大量使用拉丁同形字（Сиcтeмa、Основнoй、Сообщeние），文本规则匹配需做 Unicode 同形字归一化，否则俄语关键词可能漏检；另 Toast 存在时长受系统限制，需在跳转瞬间同步采样。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "com.amputate.volunteer.Nail.onCreate",
    "com.amputate.volunteer.PromoteHair.onCreate",
    "com.amputate.volunteer.PromoteHair$1.run",
    "com.amputate.volunteer.c.f / com.amputate.volunteer.c.c",
    "com.amputate.volunteer.Demonstrator.a",
    "com.amputate.volunteer.BaseballSentiment.onAccessibilityEvent / res/xml/jaoyiydjf.xml"
  ]
}
```

</details>

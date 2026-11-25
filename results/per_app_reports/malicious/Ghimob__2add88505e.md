# MR_082__2add88505e｜Ghimob — Ative o Google Defender

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：94.7s

## 1. 一句话核心结论

- **核心申请方式**：伪装成葡语版“Google Defender”的启动 Activity 在冷启动 onResume 中检测自身无障碍服务未启用后，无取消按钮地反复拉起系统无障碍设置页（显式组件优先、隐式 action 回退），获权后立即 BACK/HOME 退出设置并禁用自身启动组件隐藏图标，同时开启全事件无障碍监听与悬浮层。
- **静态可见性说明**：DEX 未加壳、控制流与跳转逻辑完整静态可见；但所有引导/提示文案经 x.b.D/u 的自定义算法（资源名运行时拼接 + Base64 + 字母位移反算）加密存放，静态无法直读原文，需运行期解码或复现算法才能取得逐字文案；未发现远端 HTML/WebView 页面或二阶段载荷。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `2add88505e9050a1c9e5887a9d9b52be30068cc14bba002f40be15e0be307630` |
| 包名 / 年份 | `com.intelsyss.plugins` / 2020 |
| 家族 / 品类 | **Ghimob**（同池样本数：4） |
| 原始来源标识 | https://securelist.com/ghimob-tetrade-threat-mobile-devices/99228/ |
| 桌面显示名 | Ative o Google Defender |
| 引导页宣称品牌/身份 | Google Defender（伪造 Google 官方安全/防护产品，葡语界面） |
| 系统无障碍列表服务名 | Ative o Google Defender（service 未声明 android:label，回落为 application label，故无障碍列表显示该应用名） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未配置 android:label 与 android:description，列表项只剩伪造品牌名；服务无任何能力说明；引导与提示文案全部加密（自定义 Base64+字母位移）避免静态文本检出；获权后 setComponentEnabledSetting 禁用启动 Activity 使桌面图标消失（入口隐藏）；冷启动反模拟器/反调试（命中即 killProcess）。 |
| 无障碍服务类名 | `com.intelsyss.plugins.a2y` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.intelsyss.plugins.m1x（LAUNCHER Activity，layout 2131296284） | onCreate | 原生Activity | **原文**：Ative o Google Defender<br>**译注**：激活 Google Defender（应用标题栏/任务名） | 无显式要求；界面按钮被 setVisibility(8) 隐藏，用户无可操作控件 | `com.intelsyss.plugins.m1x.onCreate` |
| 2 | 拒权反馈循环 | m1x 内的 Toast（字符串 2131427472，加密） | onResume（无障碍未启用分支） | 原生Activity | **原文**：无（加密字符串资源 2131427472，运行期由 x.b.D 解密）<br>**译注**：解密后为引导用户开启无障碍的提示语（葡语，原文需运行期解码） | 无可取消/跳过选项，提示后立即跳转设置页 | `com.intelsyss.plugins.m1x.onResume` |
| 3 | 跳无障碍设置 | 系统设置无障碍页（显式 component 来自 x.b.D(this,13)/(14)，action 来自 x.b.D(this,12)；异常回退隐式 action x.b.D(this,21)），requestCode 333 | onResume 中 startActivityForResult | 系统无障碍页 | **原文**：无（系统页面，非应用自绘）<br>**译注**：系统无障碍服务列表，其中一项显示为 Ative o Google Defender，无说明描述 | 要求用户手动开启该无障碍服务开关 | `com.intelsyss.plugins.m1x.onResume → x.b.D` |
| 4 | 拒权反馈循环 | m1x.onActivityResult → 再次 startActivityForResult(requestCode 20) | onActivityResult(333, result≠RESULT_OK) | 系统无障碍页 | 无 | 无退出选项，只能反复面对设置页 | `com.intelsyss.plugins.m1x.onActivityResult` |
| 5 | 遮罩叠层指引 | a2y 内的 WindowManager + FrameLayout 悬浮层（字段 a/b 为 FrameLayout，onServiceConnected 取 getSystemService("window")） | onServiceConnected / onAccessibilityEvent 命中目标包或设置页文本（w()） | 悬浮窗Overlay | **原文**：无（内容来自加密字符串，未静态还原）<br>**译注**：服务连接后在目标应用/设置页上方叠加自绘提示层 | 引导继续在目标页面执行操作 | `com.intelsyss.plugins.a2y.onServiceConnected / com.intelsyss.plugins.a2y.w` |
| 6 | 获权后动作 | a2y 服务本体（performGlobalAction(1)、performGlobalAction(2)、setComponentEnabledSetting(m1x,2,1)） | onServiceConnected | 不可静态还原 | 无 | 用户被弹出设置页，且此后无法从桌面再次进入应用关闭服务 | `com.intelsyss.plugins.a2y.onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 桌面/任务栏应用名：AndroidManifest application android:label（值 Ative o Google Defender）
- 系统无障碍服务列表项：service com.intelsyss.plugins.a2y 未设 android:label，回落显示应用名 Ative o Google Defender；android:description 缺失（res/xml/serviceconfig.xml 未配置描述）
- 启动 Activity m1x 的布局（2131296284）内文案与按钮（ATIVAR/DESATIVAR/ATIVADO/DESATIVADO），按钮默认 setVisibility(8) 隐藏
- onResume 中的 Toast：加密字符串 2131427472，运行期解密后显示
- 无障碍服务连接后的 WindowManager+FrameLayout 自绘悬浮层（内容来自加密字符串）
- 通知栏：x.b.I 以加密字符串构造 NotificationChannel 与通知内容，点击回到 m1x 形成后台重拉

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | Ative o Google Defender | 激活 Google Defender | `resources.arsc / AndroidManifest application android:label` | 假反诈安全 |
| pt | ATIVAR | 开启/激活 | `resources.arsc 字符串（布局按钮）` | 受限设置分步教学 |
| pt | DESATIVAR | 关闭/停用 | `resources.arsc 字符串（布局按钮）` | 未知 |
| pt | ATIVADO | 已开启 | `resources.arsc 字符串` | 未知 |
| pt | DESATIVADO | 已关闭 | `resources.arsc 字符串` | 未知 |
| pt | （加密字符串资源 2131427472，运行期由 x.b.D 解码） | 引导开启无障碍服务的 Toast 提示（原文需运行期解码） | `resources.arsc 加密字符串 + com.intelsyss.plugins.m1x.onResume` | 假反诈安全 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：onResume 每次都重新判断无障碍状态并在未启用时立即 startActivityForResult 跳设置页；onActivityResult(333) 收到非 OK 结果时再次以隐式 action 拉起（requestCode 20）；无任何取消/退出路径，主界面按钮被隐藏
- **遮罩叠层 / 高仿系统设置页**：服务连接后通过 WindowManager + FrameLayout 叠加自绘层；未见高仿系统开关页布局，跳转使用真实系统无障碍设置页
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdk 27，未见应用详情/受限设置教学或 Session 安装器路径）
- **获权后即时行为与防撤权机制**：有：onServiceConnected 立即 performGlobalAction(1)/(2) 把用户从设置页弹出，并 setComponentEnabledSetting(m1x, COMPONENT_ENABLED_STATE_DISABLED) 禁用桌面启动组件隐藏图标，使后续无法从桌面进入应用关闭服务；onAccessibilityEvent 在事件文本命中字符串 2131427472 时调用 w() 进入设置页相关干预分支
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 startActivityForResult 的 Intent 指向系统无障碍设置（显式 com.android.settings 无障碍组件或 android.settings.ACCESSIBILITY_SETTINGS）瞬间拉起 UTG，并在返回后 500–800ms 再次抓取（此时为 onActivityResult 重跳或获权后 BACK/HOME 弹出）；也可在 m1x.onResume 首次执行时预挂载，覆盖 Toast+跳转同帧。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导文案与 Toast 原文全部经自定义算法加密（资源名运行时拼接+Base64+字母位移），纯静态与纯文本 UTG 均只能看到解密后的运行期文本，需 UTG 实时抓取控件树文本；未见 WebView/远端 HTML 引导页，故不存在远端页面不可见盲区；应用无静态加壳，不影响运行期 UTG。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导/提示页（含 Toast 与隐藏按钮的主界面）** | com.intelsyss.plugins.m1x，无可见按钮，标题为 Ative o Google Defender | 确认应用在零交互下即进入索权流程、且不存在任何取消入口，是判定胁迫式引导的第一现场 | 界面无按钮/无返回入口（控件树按钮 visible=false）；Toast 文本出现后 <1s 即发生跨包 Activity 跳转；当前包名仍为 com.intelsyss.plugins 但界面无可交互元素 |
| **系统无障碍服务列表项** | 设置 > 无障碍 > 已下载/已安装服务，条目名 Ative o Google Defender，无描述文本 | 验证服务名直接冒用 Google 品牌且无能力说明，是身份伪装与告知缺失的直接证据 | 条目文本仅为品牌化应用名，description 节点为空；条目旁无任何权限范围说明；同屏其他系统服务均有描述，仅该条目缺失 |
| **获权瞬间与返回设置页后的压栈/弹出行为** | 开启开关后立即发生的 GLOBAL_ACTION_BACK/HOME 效果，以及随后桌面图标消失 | 捕获获权后主动退出设置并禁用启动组件的反撤权行为，区分恶意与良性无障碍工具 | 开关打开后 ~0ms 界面被强制退回桌面；Launcher 中该应用图标/入口消失；再次进入设置无障碍页时服务仍启用但无应用入口可关闭 |
| **后台重拉通知页** | 通知栏条目（x.b.I 构造，channel 名与内容来自加密字符串），点击 PendingIntent 指向 m1x | 证明拒权后存在后台/通知驱动的重复索权路径 | 通知正文为葡语引导语；点击通知直接回到无障碍跳转流程 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.intelsyss.plugins.m1x.onResume`
- `com.intelsyss.plugins.m1x.onActivityResult`
- `com.intelsyss.plugins.m1x.o`
- `com.intelsyss.plugins.a2y.onServiceConnected`
- `com.intelsyss.plugins.a2y.onAccessibilityEvent`
- `x.b.D`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，14 次工具调用内结束）

**静态可见性：** 代码逻辑完整可见（DEX 未被加壳，也没有 VMP 或动态加载的 Dex），但**所有引导文案都以自定义算法加密存放**：`x.b.D(ctx, idx)` 先按运行时算出的资源名取字符串，再做 Base64 解码与“字母位移”反算（[x.b#D](<resource-unit:#1.dex1 code:x.b#D>)、[x.b#u](<resource-unit:#1.dex1 code:x.b#u>)），因此引导原文无法直接以明文检出，只能依据跳转代码和控制流判断。

**核心链路（纯运行期 UTG 视角）**

1. **冷启动即拦截**：[m1x.onCreate](<resource-unit:#1.dex1 code:com.intelsyss.plugins.m1x#onCreate>) 先做反模拟器与反调试检测（`l()`、`isDebuggerConnected`、`FLAG_DEBUGGABLE`，命中即 `killProcess`），随后 `setContentView` 并**主动隐藏界面按钮**（`setVisibility(8)`），同一流程中收集设备/账户/已安装应用清单并回传（`n()`→`b.a`）。
2. **onResume 判定无障碍状态**：[m1x#onResume](<resource-unit:#1.dex1 code:com.intelsyss.plugins.m1x#onResume>) 调用 [m1x#o](<resource-unit:#1.dex1 code:com.intelsyss.plugins.m1x#o>)，读取 `Settings.Secure` 的 `accessibility_enabled`/`enabled_accessibility_services` 判断自身服务是否已启用；**已启用则立刻隐藏视图并 finish**，说明主界面从不承载真实业务功能。
3. **未启用则直接跳系统无障碍页**：先 Toast 提示（字符串 2131427472，加密），再用 `startActivityForResult` 以解密得到的 `action` + `component` 显式跳转设置页；异常时回退为隐式 `action`（`b.D(this,21)`）跳转，请求码 333。**没有任何取消/跳过按钮**。
4. **拒权循环**：`onActivityResult` 在 result≠OK 时再次以 `action 21` 重新拉起（requestCode 20）；用户每次返回 `onResume` 也会再次跳转，形成反复跳转。
5. **获权后反撤权 + 隐藏入口**：[a2y#onServiceConnected](<resource-unit:#1.dex1 code:com.intelsyss.plugins.a2y#onServiceConnected>) 立即 `performGlobalAction(1)`、`performGlobalAction(2)`（BACK/HOME，把用户从设置页弹出），随后 `setComponentEnabledSetting(m1x, COMPONENT_ENABLED_STATE_DISABLED)` **禁用桌面启动组件**，使图标消失、无法再进入应用关闭服务；同时设置 `eventTypes=-1`、`flags=119` 全量监听，并准备 `WindowManager`+`FrameLayout` 悬浮层。
6. **持续监听**：[a2y#onAccessibilityEvent](<resource-unit:#1.dex1 code:com.intelsyss.plugins.a2y#onAccessibilityEvent>) 过滤目标包名、5 秒 Timer 记录控件文本与 beforeText（键盘/页面内容抓取），并在事件文本命中字符串 2131427472 时调用 `w()`，进入设置页相关的干预分支。

**身份伪装**：桌面名与无障碍列表名同为 `Ative o Google Defender`（葡语“激活 Google Defender”），而服务节点**未配置 `android:label`、`android:description`**（配置文件为 `res/xml/serviceconfig.xml`），列表项只显示这个伪造 Google 安全身份的字符串；文案为葡语 `ATIVAR/DESATIVAR/ATIVADO/DESATIVADO`。

**未决/边界**：引导原文与 Toast 原文因字符串加密需运行期解码才能逐字取得；`w()` 的具体动作受加密字符串控制，本次未静态还原。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "DEX 未加壳、控制流与跳转逻辑完整静态可见；但所有引导/提示文案经 x.b.D/u 的自定义算法（资源名运行时拼接 + Base64 + 字母位移反算）加密存放，静态无法直读原文，需运行期解码或复现算法才能取得逐字文案；未发现远端 HTML/WebView 页面或二阶段载荷。",
  "summary_one_liner": "伪装成葡语版“Google Defender”的启动 Activity 在冷启动 onResume 中检测自身无障碍服务未启用后，无取消按钮地反复拉起系统无障碍设置页（显式组件优先、隐式 action 回退），获权后立即 BACK/HOME 退出设置并禁用自身启动组件隐藏图标，同时开启全事件无障碍监听与悬浮层。",
  "disguise_identity": {
    "app_display_name": "Ative o Google Defender",
    "claimed_brand_or_persona": "Google Defender（伪造 Google 官方安全/防护产品，葡语界面）",
    "a11y_service_label": "Ative o Google Defender（service 未声明 android:label，回落为 application label，故无障碍列表显示该应用名）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未配置 android:label 与 android:description，列表项只剩伪造品牌名；服务无任何能力说明；引导与提示文案全部加密（自定义 Base64+字母位移）避免静态文本检出；获权后 setComponentEnabledSetting 禁用启动 Activity 使桌面图标消失（入口隐藏）；冷启动反模拟器/反调试（命中即 killProcess）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.intelsyss.plugins.m1x（LAUNCHER Activity，layout 2131296284）",
      "trigger_event": "onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Ative o Google Defender",
      "shown_text_zh": "激活 Google Defender（应用标题栏/任务名）",
      "user_action_requested": "无显式要求；界面按钮被 setVisibility(8) 隐藏，用户无可操作控件",
      "code_anchor": "com.intelsyss.plugins.m1x.onCreate"
    },
    {
      "step": 2,
      "stage": "拒权反馈循环",
      "screen_or_component": "m1x 内的 Toast（字符串 2131427472，加密）",
      "trigger_event": "onResume（无障碍未启用分支）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（加密字符串资源 2131427472，运行期由 x.b.D 解密）",
      "shown_text_zh": "解密后为引导用户开启无障碍的提示语（葡语，原文需运行期解码）",
      "user_action_requested": "无可取消/跳过选项，提示后立即跳转设置页",
      "code_anchor": "com.intelsyss.plugins.m1x.onResume"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置无障碍页（显式 component 来自 x.b.D(this,13)/(14)，action 来自 x.b.D(this,12)；异常回退隐式 action x.b.D(this,21)），requestCode 333",
      "trigger_event": "onResume 中 startActivityForResult",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统页面，非应用自绘）",
      "shown_text_zh": "系统无障碍服务列表，其中一项显示为 Ative o Google Defender，无说明描述",
      "user_action_requested": "要求用户手动开启该无障碍服务开关",
      "code_anchor": "com.intelsyss.plugins.m1x.onResume → x.b.D"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "m1x.onActivityResult → 再次 startActivityForResult(requestCode 20)",
      "trigger_event": "onActivityResult(333, result≠RESULT_OK)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "用户返回/未开启即被再次送入设置页，无取消路径",
      "user_action_requested": "无退出选项，只能反复面对设置页",
      "code_anchor": "com.intelsyss.plugins.m1x.onActivityResult"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "a2y 内的 WindowManager + FrameLayout 悬浮层（字段 a/b 为 FrameLayout，onServiceConnected 取 getSystemService(\"window\")）",
      "trigger_event": "onServiceConnected / onAccessibilityEvent 命中目标包或设置页文本（w()）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（内容来自加密字符串，未静态还原）",
      "shown_text_zh": "服务连接后在目标应用/设置页上方叠加自绘提示层",
      "user_action_requested": "引导继续在目标页面执行操作",
      "code_anchor": "com.intelsyss.plugins.a2y.onServiceConnected / com.intelsyss.plugins.a2y.w"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "a2y 服务本体（performGlobalAction(1)、performGlobalAction(2)、setComponentEnabledSetting(m1x,2,1)）",
      "trigger_event": "onServiceConnected",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "立即按 BACK/HOME 离开设置页，并禁用自身启动组件使桌面图标消失",
      "user_action_requested": "用户被弹出设置页，且此后无法从桌面再次进入应用关闭服务",
      "code_anchor": "com.intelsyss.plugins.a2y.onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "桌面/任务栏应用名：AndroidManifest application android:label（值 Ative o Google Defender）",
    "系统无障碍服务列表项：service com.intelsyss.plugins.a2y 未设 android:label，回落显示应用名 Ative o Google Defender；android:description 缺失（res/xml/serviceconfig.xml 未配置描述）",
    "启动 Activity m1x 的布局（2131296284）内文案与按钮（ATIVAR/DESATIVAR/ATIVADO/DESATIVADO），按钮默认 setVisibility(8) 隐藏",
    "onResume 中的 Toast：加密字符串 2131427472，运行期解密后显示",
    "无障碍服务连接后的 WindowManager+FrameLayout 自绘悬浮层（内容来自加密字符串）",
    "通知栏：x.b.I 以加密字符串构造 NotificationChannel 与通知内容，点击回到 m1x 形成后台重拉"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "Ative o Google Defender",
      "text_zh": "激活 Google Defender",
      "source_location": "resources.arsc / AndroidManifest application android:label",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "pt",
      "text_verbatim": "ATIVAR",
      "text_zh": "开启/激活",
      "source_location": "resources.arsc 字符串（布局按钮）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "DESATIVAR",
      "text_zh": "关闭/停用",
      "source_location": "resources.arsc 字符串（布局按钮）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "pt",
      "text_verbatim": "ATIVADO",
      "text_zh": "已开启",
      "source_location": "resources.arsc 字符串",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "pt",
      "text_verbatim": "DESATIVADO",
      "text_zh": "已关闭",
      "source_location": "resources.arsc 字符串",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "pt",
      "text_verbatim": "（加密字符串资源 2131427472，运行期由 x.b.D 解码）",
      "text_zh": "引导开启无障碍服务的 Toast 提示（原文需运行期解码）",
      "source_location": "resources.arsc 加密字符串 + com.intelsyss.plugins.m1x.onResume",
      "rhetorical_frame": "假反诈安全"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "onResume 每次都重新判断无障碍状态并在未启用时立即 startActivityForResult 跳设置页；onActivityResult(333) 收到非 OK 结果时再次以隐式 action 拉起（requestCode 20）；无任何取消/退出路径，主界面按钮被隐藏",
    "overlay_or_fake_settings": "服务连接后通过 WindowManager + FrameLayout 叠加自绘层；未见高仿系统开关页布局，跳转使用真实系统无障碍设置页",
    "restricted_settings_13plus_coaching": "无（targetSdk 27，未见应用详情/受限设置教学或 Session 安装器路径）",
    "post_grant_anti_removal": "有：onServiceConnected 立即 performGlobalAction(1)/(2) 把用户从设置页弹出，并 setComponentEnabledSetting(m1x, COMPONENT_ENABLED_STATE_DISABLED) 禁用桌面启动组件隐藏图标，使后续无法从桌面进入应用关闭服务；onAccessibilityEvent 在事件文本命中字符串 2131427472 时调用 w() 进入设置页相关干预分支",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 startActivityForResult 的 Intent 指向系统无障碍设置（显式 com.android.settings 无障碍组件或 android.settings.ACCESSIBILITY_SETTINGS）瞬间拉起 UTG，并在返回后 500–800ms 再次抓取（此时为 onActivityResult 重跳或获权后 BACK/HOME 弹出）；也可在 m1x.onResume 首次执行时预挂载，覆盖 Toast+跳转同帧。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导/提示页（含 Toast 与隐藏按钮的主界面）",
        "page_identifier": "com.intelsyss.plugins.m1x，无可见按钮，标题为 Ative o Google Defender",
        "why_most_useful": "确认应用在零交互下即进入索权流程、且不存在任何取消入口，是判定胁迫式引导的第一现场",
        "observable_utg_signals": ["界面无按钮/无返回入口（控件树按钮 visible=false）", "Toast 文本出现后 <1s 即发生跨包 Activity 跳转", "当前包名仍为 com.intelsyss.plugins 但界面无可交互元素"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 > 无障碍 > 已下载/已安装服务，条目名 Ative o Google Defender，无描述文本",
        "why_most_useful": "验证服务名直接冒用 Google 品牌且无能力说明，是身份伪装与告知缺失的直接证据",
        "observable_utg_signals": ["条目文本仅为品牌化应用名，description 节点为空", "条目旁无任何权限范围说明", "同屏其他系统服务均有描述，仅该条目缺失"]
      },
      {
        "page_role": "获权瞬间与返回设置页后的压栈/弹出行为",
        "page_identifier": "开启开关后立即发生的 GLOBAL_ACTION_BACK/HOME 效果，以及随后桌面图标消失",
        "why_most_useful": "捕获获权后主动退出设置并禁用启动组件的反撤权行为，区分恶意与良性无障碍工具",
        "observable_utg_signals": ["开关打开后 ~0ms 界面被强制退回桌面", "Launcher 中该应用图标/入口消失", "再次进入设置无障碍页时服务仍启用但无应用入口可关闭"]
      },
      {
        "page_role": "后台重拉通知页",
        "page_identifier": "通知栏条目（x.b.I 构造，channel 名与内容来自加密字符串），点击 PendingIntent 指向 m1x",
        "why_most_useful": "证明拒权后存在后台/通知驱动的重复索权路径",
        "observable_utg_signals": ["通知正文为葡语引导语", "点击通知直接回到无障碍跳转流程"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导文案与 Toast 原文全部经自定义算法加密（资源名运行时拼接+Base64+字母位移），纯静态与纯文本 UTG 均只能看到解密后的运行期文本，需 UTG 实时抓取控件树文本；未见 WebView/远端 HTML 引导页，故不存在远端页面不可见盲区；应用无静态加壳，不影响运行期 UTG。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.intelsyss.plugins.m1x.onResume",
    "com.intelsyss.plugins.m1x.onActivityResult",
    "com.intelsyss.plugins.m1x.o",
    "com.intelsyss.plugins.a2y.onServiceConnected",
    "com.intelsyss.plugins.a2y.onAccessibilityEvent",
    "x.b.D"
  ]
}
```

</details>

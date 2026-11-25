# MR_019__bf531cb83c｜Banker — WhatsLocal - Ache Já!

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：164.2s

## 1. 一句话核心结论

- **核心申请方式**：以虚假 WhatsApp 号码追踪为诱饵，冷启动即 Toast 提示并直接跳转系统无障碍设置页、服务侧重复拉起，无任何取消/跳过路径，获权后自动 BACK 退出设置页并进一步索取悬浮窗加载远端 WebView。
- **静态可见性说明**：全部引导与跳转逻辑静态完整可见（DEX 未加壳、无 VMP、assets 为空、无加密配置）；仅诱饵业务页面内容来自远端（bitsolution.info、braziliankings.ddns.net/renew 及服务端下发的 opKing.Url），不影响 UTG 页面流转判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `bf531cb83c6d1c374efe5df8d906a5a6f72cc94548eb6717320c2811e3d8e1e8` |
| 包名 / 年份 | `service.webview.kiszweb` / 2018 |
| 家族 / 品类 | **Banker**（同池样本数：9） |
| 原始来源标识 | https://www.welivesecurity.com/2018/12/11/android-trojan-steals-money-paypal-accounts-2fa/ |
| 桌面显示名 | WhatsLocal - Ache Já! |
| 引导页宣称品牌/身份 | WhatsLocal / WhatsRastreio / WhatsLocaliza —— 冒充 WhatsApp 号码实时追踪工具（宣称可定位任何人的 WhatsApp 号码且完全免费） |
| 系统无障碍列表服务名 | Serviço WhatsLocal - Ache Já! |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：同一应用在三处文案使用不同品牌名（WhatsLocal - Ache Já! / WhatsRastreio / WhatsLocaliza - Ache Já!）；内部包名与代码命名（service.webview.kiszweb、desire.fenix.service.novoapp）与对外品牌无关，并尝试拉起另一包 service.webview.webkisz；Main3Activity 使用不可取消的 AlertDialog，标题 'Error Alert'、正文仅 's'、Negative 按钮文字为空串，属空白/无意义文案掩护；无同形字与多 activity-alias。 |
| 无障碍服务类名 | `desire.fenix.service.novoapp.packages.A11y` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Utilize o WhatsLocal - Ache Já! Para rastrear o whats de quem você quiser!<br><br><br> * Localize qualquer número em tempo real <br><br> * Totalmente Gratuito <br><br> * O Melhor rastreador para o whats! |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | desire.fenix.service.novoapp.packages.MainActivity（LAUNCHER，全屏 WebView 布局 activity_main） | onCreate 中 setContentView 后立即调用 checkAccessibilityPermissions() | 原生Activity | **原文**：Para utilizar o WhatsRastreio habilite a acessibilidade para nosso aplicativo!<br>**译注**：要使用 WhatsRastreio，请为我们的应用启用无障碍功能！ | 无按钮，仅提示；用户被动等待自动跳转（无取消/跳过） | `desire.fenix.service.novoapp.packages.MainActivity.onCreate` |
| 2 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（startActivityForResult，requestCode=1） | checkAccessibilityPermissions() 返回 false → setAccessibilityPermissions() | 系统无障碍页 | **原文**：Para continuar habilite o app WhatsLocaliza - Ache Já!<br>**译注**：要继续使用，请启用应用 WhatsLocaliza - Ache Já! | 在系统无障碍列表中手动找到并打开“Serviço WhatsLocal - Ache Já!”开关；无取消/跳过路径，返回后不降级 | `desire.fenix.service.novoapp.packages.MainActivity.setAccessibilityPermissions` |
| 3 | 引导说明页（系统内文案） | 系统无障碍服务列表条目说明，由 res/xml/accessibility_service_config.xml 的 android:description 提供 | 用户进入系统无障碍列表时由系统渲染 | 系统无障碍页 | **原文**：Utilize o WhatsLocal - Ache Já! Para rastrear o whats de quem você quiser!<br><br><br> * Localize qualquer número em tempo real <br><br> * Totalmente Gratuito <br><br> * O Melhor rastreador para o whats!<br>**译注**：使用 WhatsLocal - Ache Já! 追踪任何人的 WhatsApp！<br><br> * 实时定位任何号码 <br><br> * 完全免费 <br><br> * 最好的 WhatsApp 追踪器！ | 阅读说明并开启服务开关（开关位于系统页，应用未提供任何拒绝后替代路径） | `res/values/strings.xml (accessibility_service_description) / res/xml/accessibility_service_config.xml` |
| 4 | 拒权反馈循环 | desire.fenix.service.novoapp.packages.MainService（常驻 Service，onCreate 中 a11yperms()） | MainService.onCreate → a11yperms() 仍未检测到本包无障碍服务 | 系统无障碍页 | **原文**：无（直接 startActivity，无二次说明文案）<br>**译注**：无二次提示，直接再次把用户弹入系统无障碍设置页 | 被迫再次面对无障碍设置页；无取消/跳过，无本地降级模式 | `desire.fenix.service.novoapp.packages.MainService.a11yperms` |
| 5 | 获权后动作 | desire.fenix.service.novoapp.packages.A11y（AccessibilityService.onServiceConnected） | 无障碍服务被系统连接回调 onServiceConnected | 系统无障碍页 | 无 | 无需用户操作，应用自动替用户离开设置页并开始监听 | `desire.fenix.service.novoapp.packages.A11y.onServiceConnected` |
| 6 | 跳受限设置 | 系统页 android.settings.action.MANAGE_OVERLAY_PERMISSION（package:service.webview.kiszweb） | A11y.getNodeInfoes() 中 checkDrawOverlayPermission() 为 false → ToastWindow.launchDrawOverlay() | 系统无障碍页 | 无 | 手动打开悬浮窗/显示在其他应用上层开关 | `desire.fenix.service.novoapp.packages.ToastWindow.launchDrawOverlay` |
| 7 | 遮罩叠层指引 | ToastWindow 全屏悬浮窗（WindowManager type=2038 TYPE_APPLICATION_OVERLAY，内嵌 WebView） | A11y.getNodeInfoes() 在读取节点后调用 ToastWindow.show(Boolean) | 悬浮窗Overlay | **原文**：无本地文案；内容为远端 opKing.Url 页面（MainService 下发）<br>**译注**：覆盖在当前应用上方的全屏远端网页遮罩，内容由服务端动态控制，本地不可静态还原 | 取决于远端页面内容（不可静态确定） | `desire.fenix.service.novoapp.packages.ToastWindow.show` |
| 8 | 业务功能触发 | desire.fenix.service.novoapp.Main2Activity（Theme.Translucent.NoTitleBar，全屏 WebView activity_main2）与 MainActivity 主 WebView | Main2Activity.onCreate / MainActivity.onCreate 加载远端 URL | 远端WebView | **原文**：http://braziliankings.ddns.net/renew ；https://bitsolution.info/?odjasijdaosi<br>**译注**：由远端页面承载的“追踪”业务界面，本地仅有无文字的 WebView 容器 | 在远端页面中操作（内容不可静态还原） | `desire.fenix.service.novoapp.Main2Activity.onCreate / desire.fenix.service.novoapp.packages.MainActivity.onCreate` |
| 9 | 拒权反馈循环 | desire.fenix.service.novoapp.Main3Activity（Theme.Dialog，AlertDialog setCancelable(false)） | 该 Activity 启动即 onCreate 弹窗 | 原生Dialog | **原文**：Error Alert / s / ok / (空串)<br>**译注**：不可取消的“Error Alert”对话框，正文仅一个字母 s，确认按钮为 ok，取消按钮文字为空 | 只能点 ok（取消按钮为空串且无意义） | `desire.fenix.service.novoapp.Main3Activity.onCreate` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity.onCreate 冷启动 Toast（原生 Toast，无按钮）："Para utilizar o WhatsRastreio habilite a acessibilidade para nosso aplicativo!"
- MainActivity.setAccessibilityPermissions 跳转前 Toast："Para continuar habilite o app WhatsLocaliza - Ache Já!"
- 系统无障碍列表服务说明 android:description（res/values/strings.xml accessibility_service_description，由 res/xml/accessibility_service_config.xml 引用）
- 系统无障碍列表服务名 android:label（accessibility_service_label = Serviço WhatsLocal - Ache Já!）
- Main3Activity 不可取消 AlertDialog：标题 Error Alert、正文 s、按钮 ok / 空串
- 获权后的 ToastWindow 悬浮窗（type=2038 全屏 WebView）加载服务端 opKing.Url，文字内容全部远端下发
- MainActivity 主 WebView 加载 https://bitsolution.info/?odjasijdaosi、Main2Activity 全屏 WebView 加载 http://braziliankings.ddns.net/renew（远端页面文字，本地无副本）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | Para utilizar o WhatsRastreio habilite a acessibilidade para nosso aplicativo! | 要使用 WhatsRastreio，请为我们的应用启用无障碍功能！ | `硬编码字符串，desire.fenix.service.novoapp.packages.MainActivity.onCreate` | 教唆忽视警告 |
| pt | Para continuar habilite o app WhatsLocaliza - Ache Já! | 要继续使用，请启用应用 WhatsLocaliza - Ache Já! | `硬编码字符串，desire.fenix.service.novoapp.packages.MainActivity.setAccessibilityPermissions` | 受限设置分步教学 |
| pt | Utilize o WhatsLocal - Ache Já! Para rastrear o whats de quem você quiser!<br><br><br> * Localize qualquer número em tempo real <br><br> * Totalmente Gratuito <br><br> * O Melhor rastreador para o whats! | 使用 WhatsLocal - Ache Já! 追踪任何人的 WhatsApp！<br><br> * 实时定位任何号码 <br><br> * 完全免费 <br><br> * 最好的 WhatsApp 追踪器！ | `res/values/strings.xml → accessibility_service_description（经 res/xml/accessibility_service_config.xml 引用）` | 隐私承诺 |
| pt | Serviço WhatsLocal - Ache Já! | WhatsLocal - Ache Já! 服务 | `res/values/strings.xml → accessibility_service_label` | 未知 |
| en | Error Alert | 错误提示 | `硬编码字符串，desire.fenix.service.novoapp.Main3Activity.onCreate（setMessage("s")，Negative 按钮为空串）` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：未授权时存在两条重复拉起路径：MainActivity.onCreate 每次启动都 startActivityForResult(ACTION_ACCESSIBILITY_SETTINGS)；常驻 MainService.onCreate 经 a11yperms() 以 FLAG_ACTIVITY_NEW_TASK 再次 startActivity 同一设置页。未实现 onResume/onActivityResult 处理（MainActivity 无 onResume、onActivityResult 方法），即不校验返回结果、不做任何降级，用户返回业务界面后仍会被下一次启动/服务拉起再次弹出设置页。
- **遮罩叠层 / 高仿系统设置页**：无伪设置页、无压在系统设置页上的引导遮罩；悬浮窗（type=2038 TYPE_APPLICATION_OVERLAY 全屏 WebView）仅在无障碍获权后由 A11y.getNodeInfoes 触发，用于承载远端 opKing.Url 页面。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：onServiceConnected 中连续两次 performGlobalAction(3)（GLOBAL_ACTION_BACK）自动退出系统无障碍设置页并拉起自身，但不监听设置页阻止撤权；未见自点确认开关或拦截撤权的循环逻辑。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到启动 Activity 的 Intent 为 android.settings.ACCESSIBILITY_SETTINGS（或当前前台包切换为 com.android.settings 且页面为无障碍服务列表）瞬间拉起 UTG；亦可直接以冷启动 MainActivity 为起点连续采集（冷启动 0 步即跳，无需等待用户操作）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区在获权后的远端内容：ToastWindow 悬浮窗、bitsolution.info 与 braziliankings.ddns.net/renew 页面文字均由服务端控制，静态不可还原，需 UTG 运行期抓取；应用本身未加壳、无本地 HTML、assets 为空，故引导流程本身无静态盲区。Main3Activity 的 'Error Alert'/'s' 空壳对话框用途不明，静态无法确定其触发来源。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | MainActivity 启动瞬间的原生 Toast 文案（含 WhatsRastreio / WhatsLocaliza 字样），叠加在 activity_main 全屏 WebView 之上 | 这是应用唯一一次“解释理由”的时机，可判定是否存在透明说明、有无取消入口，以及文案品牌与实际应用名是否一致 | Toast 文本 Para utilizar o WhatsRastreio habilite a acessibilidade...；页面无任何按钮节点（无取消/跳过）；应用名 WhatsLocal - Ache Já! 与 Toast 内品牌 WhatsRastreio 不一致 |
| **系统无障碍服务列表项** | Settings 无障碍列表中的 Serviço WhatsLocal - Ache Já! 条目及其说明展开文本 | 系统页展示的 label/description 是该类应用最核心的伪装载体，且由本地 strings.xml 静态控制，可稳定取证 | 服务名 Serviço WhatsLocal - Ache Já!；说明含 rastrear o whats / Localize qualquer número em tempo real / Totalmente Gratuito；开关默认关闭且无应用侧提示控件 |
| **获权瞬间自动返回后的应用界面** | onServiceConnected 触发两次 GLOBAL_ACTION_BACK 后回到 MainActivity WebView（bitsolution.info） | 可验证“获权即自动退出设置页并接管”的行为，区分良性应用（停留在设置页等待用户手动返回）与强制引导型 | 系统设置页在无用户操作情况下自动返回；前台切回 service.webview.kiszweb 的 WebView 页面；紧接着出现 ACTION_MANAGE_OVERLAY_PERMISSION 系统页 |
| **设置页后叠层遮罩页** | ToastWindow type=2038 全屏悬浮窗，内嵌 WebView 加载服务端下发 URL | 遮罩内容完全远端下发，是静态分析盲区，需运行期抓取以判定是否存在伪系统界面或进一步诱导 | 窗口类型为 TYPE_APPLICATION_OVERLAY 且铺满全屏；WebView 内文本来自 opKing.Url 远端响应；叠加在其他应用之上时仍可读节点文本 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `desire.fenix.service.novoapp.packages.MainActivity.onCreate`
- `desire.fenix.service.novoapp.packages.MainActivity.setAccessibilityPermissions`
- `desire.fenix.service.novoapp.packages.MainService.a11yperms`
- `desire.fenix.service.novoapp.packages.A11y.onServiceConnected`
- `desire.fenix.service.novoapp.packages.ToastWindow.launchDrawOverlay`
- `res/xml/accessibility_service_config.xml / res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 页面流转视角）

**总体：静态逻辑完整可见，无加壳、无本地 HTML、无加密载荷；引导链完全靠“冷启动即跳系统设置页 + 服务侧重复拉起”构成，没有本地教学页。**

- **没有本地引导页**：`assets/` 目录为空，`res/layout/activity_main.xml`、`activity_main2.xml` 都只有一个全屏 WebView，没有任何本地 HTML/GIF 教学页。所有说明文字只有两处：`Toast` 文案和系统无障碍列表里的 `android:description`。
- **第一步是冷启动时立即强制跳转**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:desire.fenix.service.novoapp.packages.MainActivity#onCreate>) 在 `setContentView` 之后先调用 [checkAccessibilityPermissions()](<resource-unit:#1.dex1 code:desire.fenix.service.novoapp.packages.MainActivity#checkAccessibilityPermissions>)，如果检测不到本包的无障碍服务，就显示一条 Toast 文案，并调用 [setAccessibilityPermissions()](<resource-unit:#1.dex1 code:desire.fenix.service.novoapp.packages.MainActivity#setAccessibilityPermissions>) 执行 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 1)`。**没有取消或跳过分支**，Toast 也没有按钮。同时，它仍会调用 `webView.loadUrl("https://bitsolution.info/?odjasijdaosi")`，因此从设置页返回后，用户会看到远端页面。
- **重复拉起**：常驻的 [MainService.onCreate()](<resource-unit:#1.dex1 code:desire.fenix.service.novoapp.packages.MainService#onCreate>) 会调用 [a11yperms()](<resource-unit:#1.dex1 code:desire.fenix.service.novoapp.packages.MainService#a11yperms>)。如果仍未授权，它会再次用 `FLAG_ACTIVITY_NEW_TASK` 跳转到 `ACCESSIBILITY_SETTINGS`，形成 Activity 和 Service 两条重复拉起路径；用户退出设置页后会被再次拉回。
- **获权后自动返回并接管**：[A11y.onServiceConnected()](<resource-unit:#1.dex1 code:desire.fenix.service.novoapp.packages.A11y#onServiceConnected>) 连续执行两次 `performGlobalAction(3)`（GLOBAL_ACTION_BACK），自动退出设置页，然后启动 `MainService`，并用 `getLaunchIntentForPackage` 拉起自身，紧接着开始读取当前活动窗口的文本。
- **升级索取悬浮窗**：[getNodeInfoes()](<resource-unit:#1.dex1 code:desire.fenix.service.novoapp.packages.A11y#getNodeInfoes>) 中调用了 [ToastWindow.launchDrawOverlay()](<resource-unit:#1.dex1 code:desire.fenix.service.novoapp.packages.ToastWindow#launchDrawOverlay>) 跳转到 `ACTION_MANAGE_OVERLAY_PERMISSION`；随后 [ToastWindow.show()](<resource-unit:#1.dex1 code:desire.fenix.service.novoapp.packages.ToastWindow#show>) 用 `type=2038` 添加全屏 WebView 悬浮窗，并加载服务端下发的 `opKing.Url`。该遮罩**只在获权后出现**，不属于压在设置页上的伪设置遮罩。
- **身份不一致**：桌面名 `WhatsLocal - Ache Já!`，但 Toast 文案写 `WhatsRastreio`、`WhatsLocaliza - Ache Já!`，内部包名为 `service.webview.kiszweb`，并尝试拉起另一个包 `service.webview.webkisz`；`Main2Activity` 还加载 `http://braziliankings.ddns.net/renew` 全屏页。
- **未涉及**：targetSdk 为 26，不存在 Android 13 的受限设置分步教学或 Session 安装器绕过；也没有自点确认开关。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导与跳转逻辑静态完整可见（DEX 未加壳、无 VMP、assets 为空、无加密配置）；仅诱饵业务页面内容来自远端（bitsolution.info、braziliankings.ddns.net/renew 及服务端下发的 opKing.Url），不影响 UTG 页面流转判定。",
  "summary_one_liner": "以虚假 WhatsApp 号码追踪为诱饵，冷启动即 Toast 提示并直接跳转系统无障碍设置页、服务侧重复拉起，无任何取消/跳过路径，获权后自动 BACK 退出设置页并进一步索取悬浮窗加载远端 WebView。",
  "disguise_identity": {
    "app_display_name": "WhatsLocal - Ache Já!",
    "claimed_brand_or_persona": "WhatsLocal / WhatsRastreio / WhatsLocaliza —— 冒充 WhatsApp 号码实时追踪工具（宣称可定位任何人的 WhatsApp 号码且完全免费）",
    "a11y_service_label": "Serviço WhatsLocal - Ache Já!",
    "identity_mismatch": true,
    "obfuscation_tricks": "同一应用在三处文案使用不同品牌名（WhatsLocal - Ache Já! / WhatsRastreio / WhatsLocaliza - Ache Já!）；内部包名与代码命名（service.webview.kiszweb、desire.fenix.service.novoapp）与对外品牌无关，并尝试拉起另一包 service.webview.webkisz；Main3Activity 使用不可取消的 AlertDialog，标题 'Error Alert'、正文仅 's'、Negative 按钮文字为空串，属空白/无意义文案掩护；无同形字与多 activity-alias。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "desire.fenix.service.novoapp.packages.MainActivity（LAUNCHER，全屏 WebView 布局 activity_main）",
      "trigger_event": "onCreate 中 setContentView 后立即调用 checkAccessibilityPermissions()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Para utilizar o WhatsRastreio habilite a acessibilidade para nosso aplicativo!",
      "shown_text_zh": "要使用 WhatsRastreio，请为我们的应用启用无障碍功能！",
      "user_action_requested": "无按钮，仅提示；用户被动等待自动跳转（无取消/跳过）",
      "code_anchor": "desire.fenix.service.novoapp.packages.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（startActivityForResult，requestCode=1）",
      "trigger_event": "checkAccessibilityPermissions() 返回 false → setAccessibilityPermissions()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Para continuar habilite o app WhatsLocaliza - Ache Já!",
      "shown_text_zh": "要继续使用，请启用应用 WhatsLocaliza - Ache Já!",
      "user_action_requested": "在系统无障碍列表中手动找到并打开“Serviço WhatsLocal - Ache Já!”开关；无取消/跳过路径，返回后不降级",
      "code_anchor": "desire.fenix.service.novoapp.packages.MainActivity.setAccessibilityPermissions"
    },
    {
      "step": 3,
      "stage": "引导说明页（系统内文案）",
      "screen_or_component": "系统无障碍服务列表条目说明，由 res/xml/accessibility_service_config.xml 的 android:description 提供",
      "trigger_event": "用户进入系统无障碍列表时由系统渲染",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Utilize o WhatsLocal - Ache Já! Para rastrear o whats de quem você quiser!\n\n\n * Localize qualquer número em tempo real \n\n * Totalmente Gratuito \n\n * O Melhor rastreador para o whats!",
      "shown_text_zh": "使用 WhatsLocal - Ache Já! 追踪任何人的 WhatsApp！\n\n * 实时定位任何号码 \n\n * 完全免费 \n\n * 最好的 WhatsApp 追踪器！",
      "user_action_requested": "阅读说明并开启服务开关（开关位于系统页，应用未提供任何拒绝后替代路径）",
      "code_anchor": "res/values/strings.xml (accessibility_service_description) / res/xml/accessibility_service_config.xml"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "desire.fenix.service.novoapp.packages.MainService（常驻 Service，onCreate 中 a11yperms()）",
      "trigger_event": "MainService.onCreate → a11yperms() 仍未检测到本包无障碍服务",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（直接 startActivity，无二次说明文案）",
      "shown_text_zh": "无二次提示，直接再次把用户弹入系统无障碍设置页",
      "user_action_requested": "被迫再次面对无障碍设置页；无取消/跳过，无本地降级模式",
      "code_anchor": "desire.fenix.service.novoapp.packages.MainService.a11yperms"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "desire.fenix.service.novoapp.packages.A11y（AccessibilityService.onServiceConnected）",
      "trigger_event": "无障碍服务被系统连接回调 onServiceConnected",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "连续两次执行 GLOBAL_ACTION_BACK 自动退出系统设置页，启动 MainService 并拉起本应用主界面，随即开始读取活动窗口节点文本",
      "user_action_requested": "无需用户操作，应用自动替用户离开设置页并开始监听",
      "code_anchor": "desire.fenix.service.novoapp.packages.A11y.onServiceConnected"
    },
    {
      "step": 6,
      "stage": "跳受限设置",
      "screen_or_component": "系统页 android.settings.action.MANAGE_OVERLAY_PERMISSION（package:service.webview.kiszweb）",
      "trigger_event": "A11y.getNodeInfoes() 中 checkDrawOverlayPermission() 为 false → ToastWindow.launchDrawOverlay()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无障碍授权后立即被引导去开启“显示在其他应用上层”权限",
      "user_action_requested": "手动打开悬浮窗/显示在其他应用上层开关",
      "code_anchor": "desire.fenix.service.novoapp.packages.ToastWindow.launchDrawOverlay"
    },
    {
      "step": 7,
      "stage": "遮罩叠层指引",
      "screen_or_component": "ToastWindow 全屏悬浮窗（WindowManager type=2038 TYPE_APPLICATION_OVERLAY，内嵌 WebView）",
      "trigger_event": "A11y.getNodeInfoes() 在读取节点后调用 ToastWindow.show(Boolean)",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无本地文案；内容为远端 opKing.Url 页面（MainService 下发）",
      "shown_text_zh": "覆盖在当前应用上方的全屏远端网页遮罩，内容由服务端动态控制，本地不可静态还原",
      "user_action_requested": "取决于远端页面内容（不可静态确定）",
      "code_anchor": "desire.fenix.service.novoapp.packages.ToastWindow.show"
    },
    {
      "step": 8,
      "stage": "业务功能触发",
      "screen_or_component": "desire.fenix.service.novoapp.Main2Activity（Theme.Translucent.NoTitleBar，全屏 WebView activity_main2）与 MainActivity 主 WebView",
      "trigger_event": "Main2Activity.onCreate / MainActivity.onCreate 加载远端 URL",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "http://braziliankings.ddns.net/renew ；https://bitsolution.info/?odjasijdaosi",
      "shown_text_zh": "由远端页面承载的“追踪”业务界面，本地仅有无文字的 WebView 容器",
      "user_action_requested": "在远端页面中操作（内容不可静态还原）",
      "code_anchor": "desire.fenix.service.novoapp.Main2Activity.onCreate / desire.fenix.service.novoapp.packages.MainActivity.onCreate"
    },
    {
      "step": 9,
      "stage": "拒权反馈循环",
      "screen_or_component": "desire.fenix.service.novoapp.Main3Activity（Theme.Dialog，AlertDialog setCancelable(false)）",
      "trigger_event": "该 Activity 启动即 onCreate 弹窗",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Error Alert / s / ok / (空串)",
      "shown_text_zh": "不可取消的“Error Alert”对话框，正文仅一个字母 s，确认按钮为 ok，取消按钮文字为空",
      "user_action_requested": "只能点 ok（取消按钮为空串且无意义）",
      "code_anchor": "desire.fenix.service.novoapp.Main3Activity.onCreate"
    }
  ],
  "text_presentation_locations": [
    "MainActivity.onCreate 冷启动 Toast（原生 Toast，无按钮）：\"Para utilizar o WhatsRastreio habilite a acessibilidade para nosso aplicativo!\"",
    "MainActivity.setAccessibilityPermissions 跳转前 Toast：\"Para continuar habilite o app WhatsLocaliza - Ache Já!\"",
    "系统无障碍列表服务说明 android:description（res/values/strings.xml accessibility_service_description，由 res/xml/accessibility_service_config.xml 引用）",
    "系统无障碍列表服务名 android:label（accessibility_service_label = Serviço WhatsLocal - Ache Já!）",
    "Main3Activity 不可取消 AlertDialog：标题 Error Alert、正文 s、按钮 ok / 空串",
    "获权后的 ToastWindow 悬浮窗（type=2038 全屏 WebView）加载服务端 opKing.Url，文字内容全部远端下发",
    "MainActivity 主 WebView 加载 https://bitsolution.info/?odjasijdaosi、Main2Activity 全屏 WebView 加载 http://braziliankings.ddns.net/renew（远端页面文字，本地无副本）"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "Para utilizar o WhatsRastreio habilite a acessibilidade para nosso aplicativo!",
      "text_zh": "要使用 WhatsRastreio，请为我们的应用启用无障碍功能！",
      "source_location": "硬编码字符串，desire.fenix.service.novoapp.packages.MainActivity.onCreate",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "pt",
      "text_verbatim": "Para continuar habilite o app WhatsLocaliza - Ache Já!",
      "text_zh": "要继续使用，请启用应用 WhatsLocaliza - Ache Já!",
      "source_location": "硬编码字符串，desire.fenix.service.novoapp.packages.MainActivity.setAccessibilityPermissions",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Utilize o WhatsLocal - Ache Já! Para rastrear o whats de quem você quiser!\n\n\n * Localize qualquer número em tempo real \n\n * Totalmente Gratuito \n\n * O Melhor rastreador para o whats!",
      "text_zh": "使用 WhatsLocal - Ache Já! 追踪任何人的 WhatsApp！\n\n * 实时定位任何号码 \n\n * 完全免费 \n\n * 最好的 WhatsApp 追踪器！",
      "source_location": "res/values/strings.xml → accessibility_service_description（经 res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "pt",
      "text_verbatim": "Serviço WhatsLocal - Ache Já!",
      "text_zh": "WhatsLocal - Ache Já! 服务",
      "source_location": "res/values/strings.xml → accessibility_service_label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Error Alert",
      "text_zh": "错误提示",
      "source_location": "硬编码字符串，desire.fenix.service.novoapp.Main3Activity.onCreate（setMessage(\"s\")，Negative 按钮为空串）",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "未授权时存在两条重复拉起路径：MainActivity.onCreate 每次启动都 startActivityForResult(ACTION_ACCESSIBILITY_SETTINGS)；常驻 MainService.onCreate 经 a11yperms() 以 FLAG_ACTIVITY_NEW_TASK 再次 startActivity 同一设置页。未实现 onResume/onActivityResult 处理（MainActivity 无 onResume、onActivityResult 方法），即不校验返回结果、不做任何降级，用户返回业务界面后仍会被下一次启动/服务拉起再次弹出设置页。",
    "overlay_or_fake_settings": "无伪设置页、无压在系统设置页上的引导遮罩；悬浮窗（type=2038 TYPE_APPLICATION_OVERLAY 全屏 WebView）仅在无障碍获权后由 A11y.getNodeInfoes 触发，用于承载远端 opKing.Url 页面。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "onServiceConnected 中连续两次 performGlobalAction(3)（GLOBAL_ACTION_BACK）自动退出系统无障碍设置页并拉起自身，但不监听设置页阻止撤权；未见自点确认开关或拦截撤权的循环逻辑。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到启动 Activity 的 Intent 为 android.settings.ACCESSIBILITY_SETTINGS（或当前前台包切换为 com.android.settings 且页面为无障碍服务列表）瞬间拉起 UTG；亦可直接以冷启动 MainActivity 为起点连续采集（冷启动 0 步即跳，无需等待用户操作）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "MainActivity 启动瞬间的原生 Toast 文案（含 WhatsRastreio / WhatsLocaliza 字样），叠加在 activity_main 全屏 WebView 之上",
        "why_most_useful": "这是应用唯一一次“解释理由”的时机，可判定是否存在透明说明、有无取消入口，以及文案品牌与实际应用名是否一致",
        "observable_utg_signals": [
          "Toast 文本 Para utilizar o WhatsRastreio habilite a acessibilidade...",
          "页面无任何按钮节点（无取消/跳过）",
          "应用名 WhatsLocal - Ache Já! 与 Toast 内品牌 WhatsRastreio 不一致"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中的 Serviço WhatsLocal - Ache Já! 条目及其说明展开文本",
        "why_most_useful": "系统页展示的 label/description 是该类应用最核心的伪装载体，且由本地 strings.xml 静态控制，可稳定取证",
        "observable_utg_signals": [
          "服务名 Serviço WhatsLocal - Ache Já!",
          "说明含 rastrear o whats / Localize qualquer número em tempo real / Totalmente Gratuito",
          "开关默认关闭且无应用侧提示控件"
        ]
      },
      {
        "page_role": "获权瞬间自动返回后的应用界面",
        "page_identifier": "onServiceConnected 触发两次 GLOBAL_ACTION_BACK 后回到 MainActivity WebView（bitsolution.info）",
        "why_most_useful": "可验证“获权即自动退出设置页并接管”的行为，区分良性应用（停留在设置页等待用户手动返回）与强制引导型",
        "observable_utg_signals": [
          "系统设置页在无用户操作情况下自动返回",
          "前台切回 service.webview.kiszweb 的 WebView 页面",
          "紧接着出现 ACTION_MANAGE_OVERLAY_PERMISSION 系统页"
        ]
      },
      {
        "page_role": "设置页后叠层遮罩页",
        "page_identifier": "ToastWindow type=2038 全屏悬浮窗，内嵌 WebView 加载服务端下发 URL",
        "why_most_useful": "遮罩内容完全远端下发，是静态分析盲区，需运行期抓取以判定是否存在伪系统界面或进一步诱导",
        "observable_utg_signals": [
          "窗口类型为 TYPE_APPLICATION_OVERLAY 且铺满全屏",
          "WebView 内文本来自 opKing.Url 远端响应",
          "叠加在其他应用之上时仍可读节点文本"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区在获权后的远端内容：ToastWindow 悬浮窗、bitsolution.info 与 braziliankings.ddns.net/renew 页面文字均由服务端控制，静态不可还原，需 UTG 运行期抓取；应用本身未加壳、无本地 HTML、assets 为空，故引导流程本身无静态盲区。Main3Activity 的 'Error Alert'/'s' 空壳对话框用途不明，静态无法确定其触发来源。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "desire.fenix.service.novoapp.packages.MainActivity.onCreate",
    "desire.fenix.service.novoapp.packages.MainActivity.setAccessibilityPermissions",
    "desire.fenix.service.novoapp.packages.MainService.a11yperms",
    "desire.fenix.service.novoapp.packages.A11y.onServiceConnected",
    "desire.fenix.service.novoapp.packages.ToastWindow.launchDrawOverlay",
    "res/xml/accessibility_service_config.xml / res/values/strings.xml"
  ]
}
```

</details>

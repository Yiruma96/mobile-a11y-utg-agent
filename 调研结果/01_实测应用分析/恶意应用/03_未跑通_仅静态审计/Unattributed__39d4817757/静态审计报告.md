# MB_164__39d4817757｜Unattributed — VideoZapisDTP

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：99.7s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即在本地 HTML 伪系统引导页中逐个『预演』权限弹窗，最后用『三个简单步骤 + Включить』教会用户进入系统无障碍设置自行打开 GuardAccessibilityService，全程以 Piski 假身份和『稳定运行』话术掩盖读屏+自动点击的真实用途。
- **静态可见性说明**：引导界面为本地静态 HTML（assets/onboarding_stealer.html、assets/phish_tg.html），文字与流程 100% 静态可读；AndroidManifest.xml（二进制 AXML）与无障碍配置 res/xml/r_pvbqgtrefwgj.xml 亦可静态还原。但 25 个主 DEX 对 com.base.template.OnboardingActivity、com.base.template.services.GuardAccessibilityService 及 accessibility 关键字的类级检索全部未命中（类名映射/混淆），ACTION_ACCESSIBILITY_SETTINGS 的具体调用点与 WebView JS 桥接回调未能静态定位；非加壳、非 AES 密文、非远端 HTML。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `39d481775748ceefebd487c87e54b6023776ad2bce0d688847b14fbdc7f0851d` |
| 包名 / 年份 | `com.devstudio.reader` / 2026 |
| 家族 / 品类 | **Unattributed**（同池样本数：13） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | VideoZapisDTP |
| 引导页宣称品牌/身份 | Piski（俄语短信/消息类应用，页面内自称『Piski』并在伪造的系统对话框中以『App』名义演示开关） |
| 系统无障碍列表服务名 | 未设置 android:label（系统无障碍列表回退显示应用名 VideoZapisDTP，不暴露 Guard/守护语义） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 桌面名 VideoZapisDTP、包名 com.devstudio.reader、页面身份 Piski 三者互不相符；2) 无障碍服务未配置 label，借应用名掩盖 GuardAccessibilityService 的『守护/看门』性质；3) 无障碍 android:description 只写『稳定运行』，与 canRetrieveWindowContent/canPerformGestures 能力不符；4) HTML 用 Google 配色、Google Sans 与 #1e1e1e 深色圆角弹窗高仿系统权限对话框，并把应用图标标为通用『App』；5) Manifest 使用 VisibleAlias / HiddenAlias 双 activity-alias 做入口切换；6) 资源文件名随机化（res/xml/r_pvbqgtrefwgj.xml）；7) 25 个主 DEX 分散载荷。未发现同形字、空白/换行挤出警告或伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.base.template.services.GuardAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |
| 系统设置项说明 (`android:description`) | Служба специальных возможностей для стабильной работы приложения. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.base.template.OnboardingActivity（Manifest 声明的引导 Activity，另有 com.base.template.MainActivity 作为对照入口） | 用户从桌面图标冷启动（LAUNCHER，可能经 VisibleAlias 别名进入） | 本地HTML WebView | **原文**：SMS доступ / Для доступа к данному ресурсу необходимо назначить приложение SMS по умолчанию<br>**译注**：短信访问 / 要访问该资源，必须将本应用设为默认短信应用 | 按引导继续，页面上只提供『Продолжить』（继续），无退出/跳过入口 | `com.base.template.OnboardingActivity + assets/onboarding_stealer.html` |
| 2 | 引导说明页 | WebView 内伪造的 Android 系统对话框（.sms-mock-dialog 卡片，底部圆角面板 + 变暗遮罩） | 引导页首屏自动播放『Вот что вы увидите（你将会看到这些）』预告动画 | 本地HTML WebView | **原文**：Вот что вы увидите / Сделать «Piski» приложением для обмена SMS по умолчанию? / Отмена / По умолчанию / Продолжить<br>**译注**：你将会看到这些 / 是否将「Piski」设为默认短信应用？/ 取消 / 设为默认 / 继续 | 在伪造对话框上点『Продолжить』继续（伪造的『Отмена/Отклонить』仅存在于演示图内，真实流程无退出） | `assets/onboarding_stealer.html（.sms-card / .sms-mock-dialog / .sms-dimmer）` |
| 3 | 业务功能触发 | 同一 WebView 依次演示短信权限、电池优化白名单、VPN、通知使用权四个伪造系统弹窗 | 上一步『Продолжить』点击后按顺序推进各屏 | 本地HTML WebView | **原文**：Разрешить приложению «Piski» отправлять и просматривать SMS-сообщения? / Оптимизация батареи … всегда работать в фоновом режиме? / Защита соединения … пытается подключиться к сети VPN / Доступ к уведомлениям<br>**译注**：是否允许「Piski」发送和查看短信？/ 电池优化……是否允许始终后台运行？/ 连接保护……尝试连接 VPN / 通知访问 | 逐屏点『Продолжить』（或『Открыть настройки』打开通知使用权设置），完成前置权限铺垫 | `assets/onboarding_stealer.html（Спец. возможности 之前的各屏 section）` |
| 4 | 跳无障碍设置 | WebView『Спец. возможности』教学页 + 伪造的『Настройки · Спец. возможности』列表截图（显示『App  Выкл / Использовать App  Вкл』开关） | 用户点主按钮『Включить』（开启）；对应 Java 侧跳转（应为 ACTION_ACCESSIBILITY_SETTINGS）未能静态定位 | 本地HTML WebView | **原文**：Спец. возможности / Для стабильной работы приложению необходим доступ к специальным возможностям / Вот что вы увидите в настройках / Настройки · Спец. возможности / Скачанные приложения / App / Выкл / Использовать App / Вкл<br>**译注**：特殊能力 / 为使应用稳定运行，本应用需要特殊能力访问权限 / 你将在设置中看到这些 / 设置 · 特殊能力 / 已下载的应用 / App / 关 / 使用 App / 开 | 点『Включить』跳转系统无障碍设置；页面未提供取消/稍后再说按钮 | `assets/onboarding_stealer.html（Спец. возможности 段落，按钮『Включить』）` |
| 5 | 遮罩叠层指引 | HTML 内『Три простых шага』三步图文教程（对应真实系统无障碍设置页的视觉位置） | 与第 4 步同屏呈现，跳转前/跳转后持续展示 | 本地HTML WebView | **原文**：Три простых шага / 1 Нажмите кнопку ниже / Откроются настройки специальных возможностей / 2 Найдите приложение / Нажмите на него / 3 Включите переключатель / И подтвердите в диалоге<br>**译注**：三个简单步骤 / 1 点击下方按钮 / 将打开特殊能力设置 / 2 找到本应用 / 点击它 / 3 打开开关 / 并在对话框中确认 | 按 1-2-3 步在系统设置中自行找到该应用并打开开关，再确认系统警告弹窗 | `assets/onboarding_stealer.html（三步教学 section）` |
| 6 | 获权后动作 | com.base.template.services.GuardAccessibilityService（无障碍读屏/手势服务）+ StealthVpnService + NotifListener + TelegramPhishActivity / SmsActivity | 用户在系统无障碍列表中打开开关、服务 onServiceConnected 后被启用 | 不可静态还原 | **原文**：Служба специальных возможностей для стабильной работы приложения.<br>**译注**：为使应用稳定运行所需的特殊能力服务。（系统无障碍列表下的服务说明，仅此一句） | 无（后台自动接管：读屏内容、模拟手势点击，配合短信/联系人窃取与 phish_tg.html 伪造 Telegram 登录页收集号码、验证码与云密码） | `com.base.template.services.GuardAccessibilityService + res/xml/r_pvbqgtrefwgj.xml + assets/phish_tg.html` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- assets/onboarding_stealer.html —— 全屏 WebView 引导页，冷启动后自动播放，包含伪造的系统权限对话框（短信默认应用、短信/联系人权限、电池优化、VPN、通知使用权）以及无障碍『Спец. возможности』教学页和三步图文
- 系统无障碍服务列表项说明文字：android:description = 『Служба специальных возможностей для стабильной работы приложения.』（配置于 res/xml/r_pvbqgtrefwgj.xml），服务无 android:label，列表标题回退为应用名 VideoZapisDTP
- 伪造的『Настройки · Спец. возможности』设置页截图（HTML 内用 div 绘制的无障碍列表 + App 开关，标注『Выкл / Вкл』）
- 伪造的『Настройки → Уведомления』通知使用权页（『Piski / Не разрешено』+『Доступ разрешён』），配『Открыть настройки』按钮
- assets/phish_tg.html —— 伪造 Telegram 登录/验证码/云密码页面（用于获权后的凭证与短信验证码窃取）
- AndroidManifest 中双 activity-alias（com.base.template.VisibleAlias / com.base.template.HiddenAlias）决定实际启动入口，影响引导页何时出现

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Спец. возможности<br>Для стабильной работы приложению необходим доступ к специальным возможностям | 特殊能力<br>为使应用稳定运行，本应用需要特殊能力访问权限 | `assets/onboarding_stealer.html` | 假更新 |
| ru | Три простых шага<br>1 Нажмите кнопку ниже<br>Откроются настройки специальных возможностей<br>2 Найдите приложение<br>Нажмите на него<br>3 Включите переключатель<br>И подтвердите в диалоге | 三个简单步骤<br>1 点击下方按钮<br>将打开特殊能力设置<br>2 找到本应用<br>点击它<br>3 打开开关<br>并在对话框中确认 | `assets/onboarding_stealer.html` | 受限设置分步教学 |
| ru | Вот что вы увидите<br>Настройки · Спец. возможности<br>Скачанные приложения<br>App<br>Выкл<br>Использовать App<br>Вкл<br>Включить | 你将会看到这些<br>设置 · 特殊能力<br>已下载的应用<br>App<br>关<br>使用 App<br>开<br>开启 | `assets/onboarding_stealer.html` | 教唆忽视警告 |
| ru | Служба специальных возможностей для стабильной работы приложения. | 为使应用稳定运行所需的特殊能力服务。 | `res/xml/r_pvbqgtrefwgj.xml（accessibility-service android:description）` | 隐私承诺 |
| ru | Вот что вы увидите<br>Сделать «Piski» приложением для обмена SMS по умолчанию?<br>Отмена<br>По умолчанию<br>Продолжить | 你将会看到这些<br>是否将「Piski」设为默认短信应用？<br>取消<br>设为默认<br>继续 | `assets/onboarding_stealer.html` | 良性透明说明 |
| ru | Оптимизация батареи<br>Для стабильной работы в фоновом режиме приложению необходимо отключить оптимизацию батареи | 电池优化<br>为使应用在后台稳定运行，需要关闭电池优化 | `assets/onboarding_stealer.html` | 清理工具伪装 |
| ru | Мы отправили код подтверждения в Telegram на ваш номер<br>Облачный пароль<br>У вас включена двухфакторная аутентификация, поэтому для входа нужен пароль. | 我们已向你的号码发送了 Telegram 验证码<br>云密码<br>你已开启两步验证，因此登录需要密码。 | `assets/phish_tg.html` | 假反诈安全 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：静态可见部分：引导页为单向『Продолжить / Включить』推进，无跳过分支；Java 侧是否在 onResume/轮询中检测服务未启用并重跳未能静态确认（类名检索未命中）。结合 Manifest 的 BootReceiver、KeepAliveTileService、RescueJobService、SystemEventReceiver（BOOT_COMPLETED / MY_PACKAGE_REPLACED / USER_PRESENT / SCREEN_ON），存在启动与唤醒时再次拉起引导的条件。
- **遮罩叠层 / 高仿系统设置页**：是——但以 WebView 内绘制的伪造系统对话框/伪造『设置 · 特殊能力』列表页形式呈现（含变暗遮罩 .sms-dimmer 与底部圆角卡片），未见 TYPE_APPLICATION_OVERLAY 悬浮窗或全屏覆盖系统设置页的叠层（静态预筛 overlay=[]）
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无（静态预筛 anti_removal=[]；未发现监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权、或自动点确认的代码证据；但 GuardAccessibilityService 具备读屏与手势能力，客观上可支持后续自动操作）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 com.base.template.OnboardingActivity 进入前台（冷启动首屏即引导页）时立即开始 UTG 采集；或在无障碍设置页出现后用户返回应用、应用再次跳转 ACTION_ACCESSIBILITY_SETTINGS 时二次采集以验证拒权回跳
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：1) 引导界面完全由本地 HTML 文本渲染（非图片），UTG 文本采集无压力，但伪造对话框为 CSS 绘制，需按 WebView 文本节点而非原生 View 层级提取；2) DEX 层类名混淆使 ACTION_ACCESSIBILITY_SETTINGS 的实际调用点与拒权回跳逻辑无法静态定位，纯静态无法确认是否存在『返回后立即重跳』的死循环，需动态监测 Activity 栈与 Intent 频次；此外 25 个主 DEX 分散、资源名随机化，进一步降低静态可读性（但非加壳/非密文动态加载）。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（伪造系统短信默认应用对话框）** | OnboardingActivity 内 WebView 全屏，底部 #1e1e1e 圆角卡片 + 变暗遮罩，文案含『SMS доступ』『Сделать «Piski» приложением для обмена SMS по умолчанию?』『Продолжить』 | 证明应用以高仿系统权限弹窗开场、无退出按钮，且自称身份 Piski 与桌面名 VideoZapisDTP 不一致，是身份欺骗与诱导链的起点 | WebView 文本节点出现『Piski』而包名为 com.devstudio.reader；页面无返回/跳过控件，仅『Продолжить』；背景为 #000 全屏 WebView 而非原生 Activity 布局 |
| **跳转前 WebView 无障碍教学页** | 标题『Спец. возможности』+『Вот что вы увидите в настройках』+ 伪造『Настройки · Спец. возможности』列表（App / Выкл / Вкл）+ 三步教学 + 主按钮『Включить』 | 这是无障碍诱导的直接证据页：明确教用户在系统设置中找到应用并打开开关，且用『稳定运行』话术掩盖读屏能力 | 文本『Три простых шага』『Найдите приложение』『Включите переключатель』；按钮『Включить』点击后系统无障碍设置页出现在前台；伪造设置列表中出现通用图标名『App』 |
| **系统无障碍服务列表项** | 系统设置 → 已下载的应用 列表中的 VideoZapisDTP 条目，副标题为『Служба специальных возможностей для стабильной работы приложения.』 | 核对系统侧呈现给用户的真实服务名与说明，验证 android:label 缺失导致服务语义被应用名掩盖 | 服务项标题等于应用名而非 Guard 语义名；说明文字仅有『稳定运行』一句；开关初始为关闭，需用户手动打开并确认警告 |
| **获权后伪造 Telegram 凭证页（后续动作佐证）** | TelegramPhishActivity / phish_tg.html，含『Номер телефона』『Код』『Облачный пароль』输入框 | 确认无障碍授权后的实际业务指向为短信/凭证窃取，而非任何可访问性辅助功能 | 页面出现手机号/验证码/云密码三段输入；页面语言为俄语且品牌为 Telegram；获取短信验证码与 READ_SMS/RECEIVE_SMS 权限共现 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.base.template.OnboardingActivity`
- `com.base.template.services.GuardAccessibilityService`
- `assets/onboarding_stealer.html`
- `res/xml/r_pvbqgtrefwgj.xml`
- `assets/phish_tg.html`
- `com.base.template.TelegramPhishActivity`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**静态可见性**：引导界面全部是**本地静态 HTML**（`assets/onboarding_stealer.html`），内容可完整读取；Manifest 组件、无障碍配置 XML 也完整。但 25 个主 DEX 上按类名检索 `OnboardingActivity` / `GuardAccessibilityService` / `accessibility` **全部未命中**（类名映射/混淆），因此“哪段 Java 代码执行跳转”未能静态定位；不过这不影响对 UTG 页面的判定。

**核心事实**

1. **冷启动即进入全屏“模拟系统”引导流**：`com.base.template.OnboardingActivity`（在 Manifest 中声明）加载本地 WebView HTML。该 HTML 用 Google 配色、`Google Sans`、仿 Android 深色弹窗还原**系统权限对话框外观**，逐个“预演”即将弹出的系统弹窗（短信默认应用、短信/联系人权限、电池优化、VPN、通知使用权），最后一步是**无障碍**。
2. **无障碍步骤给出三段式分步教学**：`Три простых шага`（三个简单步骤）→ 点击下方按钮打开无障碍设置 → 找到应用点进去 → 打开开关并确认；主按钮为 `Включить`（开启）。
3. **身份三处不一致**：桌面名 `VideoZapisDTP`、包名 `com.devstudio.reader`，而页面内宣称的应用身份是 **`Piski`**（俄语“写/短信”类应用）；HTML 还伪装成 `App` 在系统设置列表中演示开关。无障碍服务 `GuardAccessibilityService` **无 `android:label`**，系统列表里只能显示应用名，掩盖了“守护/Guard”这一实际用途。
4. **无障碍说明文案是纯“稳定性”话术**：`Служба специальных возможностей для стабильной работы приложения.`（“为使应用稳定运行所需的特殊能力服务”）—— 与 `canRetrieveWindowContent`、`canPerformGestures` 等配置（见 [res/xml/r_pvbqgtrefwgj.xml](<resource-unit:#1 file:res/xml/r_pvbqgtrefwgj.xml>)）严重不匹配，属于典型的弱化说明。
5. **权限共现指向金融窃取**：`READ_SMS/SEND_SMS/RECEIVE_SMS/CALL_PHONE/READ_CONTACTS` + `StealthVpnService` + `phish_tg.html`（伪造 Telegram 登录/云密码/验证码页）+ `onboarding_stealer.html`（文件名直书 stealer）。无障碍权限在此是**读屏与自动点击的自动化底座**，而非可访问性用途。
6. **未见** 13+ 受限设置教学、未见过度叠加悬浮窗、未见 `isAccessibilityTool` 伪造（静态预筛 anti_removal/overlay 均为空）；但 `VisibleAlias`/`HiddenAlias` 双 `activity-alias` 与 `KeepAliveTileService`、`RescueJobService`、`BootReceiver` 构成保活链。

**边界**：DEX 层跳转代码未静态取得（类名混淆），`ACTION_ACCESSIBILITY_SETTINGS` 的实际调用点未确认；HTML 中 `Включить` 的点击回调（JS bridge）也未能对应到 Java 侧。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "引导界面为本地静态 HTML（assets/onboarding_stealer.html、assets/phish_tg.html），文字与流程 100% 静态可读；AndroidManifest.xml（二进制 AXML）与无障碍配置 res/xml/r_pvbqgtrefwgj.xml 亦可静态还原。但 25 个主 DEX 对 com.base.template.OnboardingActivity、com.base.template.services.GuardAccessibilityService 及 accessibility 关键字的类级检索全部未命中（类名映射/混淆），ACTION_ACCESSIBILITY_SETTINGS 的具体调用点与 WebView JS 桥接回调未能静态定位；非加壳、非 AES 密文、非远端 HTML。",
  "summary_one_liner": "冷启动即在本地 HTML 伪系统引导页中逐个『预演』权限弹窗，最后用『三个简单步骤 + Включить』教会用户进入系统无障碍设置自行打开 GuardAccessibilityService，全程以 Piski 假身份和『稳定运行』话术掩盖读屏+自动点击的真实用途。",
  "disguise_identity": {
    "app_display_name": "VideoZapisDTP",
    "claimed_brand_or_persona": "Piski（俄语短信/消息类应用，页面内自称『Piski』并在伪造的系统对话框中以『App』名义演示开关）",
    "a11y_service_label": "未设置 android:label（系统无障碍列表回退显示应用名 VideoZapisDTP，不暴露 Guard/守护语义）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 桌面名 VideoZapisDTP、包名 com.devstudio.reader、页面身份 Piski 三者互不相符；2) 无障碍服务未配置 label，借应用名掩盖 GuardAccessibilityService 的『守护/看门』性质；3) 无障碍 android:description 只写『稳定运行』，与 canRetrieveWindowContent/canPerformGestures 能力不符；4) HTML 用 Google 配色、Google Sans 与 #1e1e1e 深色圆角弹窗高仿系统权限对话框，并把应用图标标为通用『App』；5) Manifest 使用 VisibleAlias / HiddenAlias 双 activity-alias 做入口切换；6) 资源文件名随机化（res/xml/r_pvbqgtrefwgj.xml）；7) 25 个主 DEX 分散载荷。未发现同形字、空白/换行挤出警告或伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.base.template.OnboardingActivity（Manifest 声明的引导 Activity，另有 com.base.template.MainActivity 作为对照入口）",
      "trigger_event": "用户从桌面图标冷启动（LAUNCHER，可能经 VisibleAlias 别名进入）",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "SMS доступ / Для доступа к данному ресурсу необходимо назначить приложение SMS по умолчанию",
      "shown_text_zh": "短信访问 / 要访问该资源，必须将本应用设为默认短信应用",
      "user_action_requested": "按引导继续，页面上只提供『Продолжить』（继续），无退出/跳过入口",
      "code_anchor": "com.base.template.OnboardingActivity + assets/onboarding_stealer.html"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "WebView 内伪造的 Android 系统对话框（.sms-mock-dialog 卡片，底部圆角面板 + 变暗遮罩）",
      "trigger_event": "引导页首屏自动播放『Вот что вы увидите（你将会看到这些）』预告动画",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Вот что вы увидите / Сделать «Piski» приложением для обмена SMS по умолчанию? / Отмена / По умолчанию / Продолжить",
      "shown_text_zh": "你将会看到这些 / 是否将「Piski」设为默认短信应用？/ 取消 / 设为默认 / 继续",
      "user_action_requested": "在伪造对话框上点『Продолжить』继续（伪造的『Отмена/Отклонить』仅存在于演示图内，真实流程无退出）",
      "code_anchor": "assets/onboarding_stealer.html（.sms-card / .sms-mock-dialog / .sms-dimmer）"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "同一 WebView 依次演示短信权限、电池优化白名单、VPN、通知使用权四个伪造系统弹窗",
      "trigger_event": "上一步『Продолжить』点击后按顺序推进各屏",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Разрешить приложению «Piski» отправлять и просматривать SMS-сообщения? / Оптимизация батареи … всегда работать в фоновом режиме? / Защита соединения … пытается подключиться к сети VPN / Доступ к уведомлениям",
      "shown_text_zh": "是否允许「Piski」发送和查看短信？/ 电池优化……是否允许始终后台运行？/ 连接保护……尝试连接 VPN / 通知访问",
      "user_action_requested": "逐屏点『Продолжить』（或『Открыть настройки』打开通知使用权设置），完成前置权限铺垫",
      "code_anchor": "assets/onboarding_stealer.html（Спец. возможности 之前的各屏 section）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "WebView『Спец. возможности』教学页 + 伪造的『Настройки · Спец. возможности』列表截图（显示『App  Выкл / Использовать App  Вкл』开关）",
      "trigger_event": "用户点主按钮『Включить』（开启）；对应 Java 侧跳转（应为 ACTION_ACCESSIBILITY_SETTINGS）未能静态定位",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Спец. возможности / Для стабильной работы приложению необходим доступ к специальным возможностям / Вот что вы увидите в настройках / Настройки · Спец. возможности / Скачанные приложения / App / Выкл / Использовать App / Вкл",
      "shown_text_zh": "特殊能力 / 为使应用稳定运行，本应用需要特殊能力访问权限 / 你将在设置中看到这些 / 设置 · 特殊能力 / 已下载的应用 / App / 关 / 使用 App / 开",
      "user_action_requested": "点『Включить』跳转系统无障碍设置；页面未提供取消/稍后再说按钮",
      "code_anchor": "assets/onboarding_stealer.html（Спец. возможности 段落，按钮『Включить』）"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "HTML 内『Три простых шага』三步图文教程（对应真实系统无障碍设置页的视觉位置）",
      "trigger_event": "与第 4 步同屏呈现，跳转前/跳转后持续展示",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Три простых шага / 1 Нажмите кнопку ниже / Откроются настройки специальных возможностей / 2 Найдите приложение / Нажмите на него / 3 Включите переключатель / И подтвердите в диалоге",
      "shown_text_zh": "三个简单步骤 / 1 点击下方按钮 / 将打开特殊能力设置 / 2 找到本应用 / 点击它 / 3 打开开关 / 并在对话框中确认",
      "user_action_requested": "按 1-2-3 步在系统设置中自行找到该应用并打开开关，再确认系统警告弹窗",
      "code_anchor": "assets/onboarding_stealer.html（三步教学 section）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.base.template.services.GuardAccessibilityService（无障碍读屏/手势服务）+ StealthVpnService + NotifListener + TelegramPhishActivity / SmsActivity",
      "trigger_event": "用户在系统无障碍列表中打开开关、服务 onServiceConnected 后被启用",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Служба специальных возможностей для стабильной работы приложения.",
      "shown_text_zh": "为使应用稳定运行所需的特殊能力服务。（系统无障碍列表下的服务说明，仅此一句）",
      "user_action_requested": "无（后台自动接管：读屏内容、模拟手势点击，配合短信/联系人窃取与 phish_tg.html 伪造 Telegram 登录页收集号码、验证码与云密码）",
      "code_anchor": "com.base.template.services.GuardAccessibilityService + res/xml/r_pvbqgtrefwgj.xml + assets/phish_tg.html"
    }
  ],
  "text_presentation_locations": [
    "assets/onboarding_stealer.html —— 全屏 WebView 引导页，冷启动后自动播放，包含伪造的系统权限对话框（短信默认应用、短信/联系人权限、电池优化、VPN、通知使用权）以及无障碍『Спец. возможности』教学页和三步图文",
    "系统无障碍服务列表项说明文字：android:description = 『Служба специальных возможностей для стабильной работы приложения.』（配置于 res/xml/r_pvbqgtrefwgj.xml），服务无 android:label，列表标题回退为应用名 VideoZapisDTP",
    "伪造的『Настройки · Спец. возможности』设置页截图（HTML 内用 div 绘制的无障碍列表 + App 开关，标注『Выкл / Вкл』）",
    "伪造的『Настройки → Уведомления』通知使用权页（『Piski / Не разрешено』+『Доступ разрешён』），配『Открыть настройки』按钮",
    "assets/phish_tg.html —— 伪造 Telegram 登录/验证码/云密码页面（用于获权后的凭证与短信验证码窃取）",
    "AndroidManifest 中双 activity-alias（com.base.template.VisibleAlias / com.base.template.HiddenAlias）决定实际启动入口，影响引导页何时出现"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Спец. возможности\nДля стабильной работы приложению необходим доступ к специальным возможностям",
      "text_zh": "特殊能力\n为使应用稳定运行，本应用需要特殊能力访问权限",
      "source_location": "assets/onboarding_stealer.html",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "ru",
      "text_verbatim": "Три простых шага\n1 Нажмите кнопку ниже\nОткроются настройки специальных возможностей\n2 Найдите приложение\nНажмите на него\n3 Включите переключатель\nИ подтвердите в диалоге",
      "text_zh": "三个简单步骤\n1 点击下方按钮\n将打开特殊能力设置\n2 找到本应用\n点击它\n3 打开开关\n并在对话框中确认",
      "source_location": "assets/onboarding_stealer.html",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "ru",
      "text_verbatim": "Вот что вы увидите\nНастройки · Спец. возможности\nСкачанные приложения\nApp\nВыкл\nИспользовать App\nВкл\nВключить",
      "text_zh": "你将会看到这些\n设置 · 特殊能力\n已下载的应用\nApp\n关\n使用 App\n开\n开启",
      "source_location": "assets/onboarding_stealer.html",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "ru",
      "text_verbatim": "Служба специальных возможностей для стабильной работы приложения.",
      "text_zh": "为使应用稳定运行所需的特殊能力服务。",
      "source_location": "res/xml/r_pvbqgtrefwgj.xml（accessibility-service android:description）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "ru",
      "text_verbatim": "Вот что вы увидите\nСделать «Piski» приложением для обмена SMS по умолчанию?\nОтмена\nПо умолчанию\nПродолжить",
      "text_zh": "你将会看到这些\n是否将「Piski」设为默认短信应用？\n取消\n设为默认\n继续",
      "source_location": "assets/onboarding_stealer.html",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "ru",
      "text_verbatim": "Оптимизация батареи\nДля стабильной работы в фоновом режиме приложению необходимо отключить оптимизацию батареи",
      "text_zh": "电池优化\n为使应用在后台稳定运行，需要关闭电池优化",
      "source_location": "assets/onboarding_stealer.html",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "ru",
      "text_verbatim": "Мы отправили код подтверждения в Telegram на ваш номер\nОблачный пароль\nУ вас включена двухфакторная аутентификация, поэтому для входа нужен пароль.",
      "text_zh": "我们已向你的号码发送了 Telegram 验证码\n云密码\n你已开启两步验证，因此登录需要密码。",
      "source_location": "assets/phish_tg.html",
      "rhetorical_frame": "假反诈安全"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "静态可见部分：引导页为单向『Продолжить / Включить』推进，无跳过分支；Java 侧是否在 onResume/轮询中检测服务未启用并重跳未能静态确认（类名检索未命中）。结合 Manifest 的 BootReceiver、KeepAliveTileService、RescueJobService、SystemEventReceiver（BOOT_COMPLETED / MY_PACKAGE_REPLACED / USER_PRESENT / SCREEN_ON），存在启动与唤醒时再次拉起引导的条件。",
    "overlay_or_fake_settings": "是——但以 WebView 内绘制的伪造系统对话框/伪造『设置 · 特殊能力』列表页形式呈现（含变暗遮罩 .sms-dimmer 与底部圆角卡片），未见 TYPE_APPLICATION_OVERLAY 悬浮窗或全屏覆盖系统设置页的叠层（静态预筛 overlay=[]）",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无（静态预筛 anti_removal=[]；未发现监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权、或自动点确认的代码证据；但 GuardAccessibilityService 具备读屏与手势能力，客观上可支持后续自动操作）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 com.base.template.OnboardingActivity 进入前台（冷启动首屏即引导页）时立即开始 UTG 采集；或在无障碍设置页出现后用户返回应用、应用再次跳转 ACTION_ACCESSIBILITY_SETTINGS 时二次采集以验证拒权回跳",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（伪造系统短信默认应用对话框）",
        "page_identifier": "OnboardingActivity 内 WebView 全屏，底部 #1e1e1e 圆角卡片 + 变暗遮罩，文案含『SMS доступ』『Сделать «Piski» приложением для обмена SMS по умолчанию?』『Продолжить』",
        "why_most_useful": "证明应用以高仿系统权限弹窗开场、无退出按钮，且自称身份 Piski 与桌面名 VideoZapisDTP 不一致，是身份欺骗与诱导链的起点",
        "observable_utg_signals": ["WebView 文本节点出现『Piski』而包名为 com.devstudio.reader", "页面无返回/跳过控件，仅『Продолжить』", "背景为 #000 全屏 WebView 而非原生 Activity 布局"]
      },
      {
        "page_role": "跳转前 WebView 无障碍教学页",
        "page_identifier": "标题『Спец. возможности』+『Вот что вы увидите в настройках』+ 伪造『Настройки · Спец. возможности』列表（App / Выкл / Вкл）+ 三步教学 + 主按钮『Включить』",
        "why_most_useful": "这是无障碍诱导的直接证据页：明确教用户在系统设置中找到应用并打开开关，且用『稳定运行』话术掩盖读屏能力",
        "observable_utg_signals": ["文本『Три простых шага』『Найдите приложение』『Включите переключатель』", "按钮『Включить』点击后系统无障碍设置页出现在前台", "伪造设置列表中出现通用图标名『App』"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 已下载的应用 列表中的 VideoZapisDTP 条目，副标题为『Служба специальных возможностей для стабильной работы приложения.』",
        "why_most_useful": "核对系统侧呈现给用户的真实服务名与说明，验证 android:label 缺失导致服务语义被应用名掩盖",
        "observable_utg_signals": ["服务项标题等于应用名而非 Guard 语义名", "说明文字仅有『稳定运行』一句", "开关初始为关闭，需用户手动打开并确认警告"]
      },
      {
        "page_role": "获权后伪造 Telegram 凭证页（后续动作佐证）",
        "page_identifier": "TelegramPhishActivity / phish_tg.html，含『Номер телефона』『Код』『Облачный пароль』输入框",
        "why_most_useful": "确认无障碍授权后的实际业务指向为短信/凭证窃取，而非任何可访问性辅助功能",
        "observable_utg_signals": ["页面出现手机号/验证码/云密码三段输入", "页面语言为俄语且品牌为 Telegram", "获取短信验证码与 READ_SMS/RECEIVE_SMS 权限共现"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：1) 引导界面完全由本地 HTML 文本渲染（非图片），UTG 文本采集无压力，但伪造对话框为 CSS 绘制，需按 WebView 文本节点而非原生 View 层级提取；2) DEX 层类名混淆使 ACTION_ACCESSIBILITY_SETTINGS 的实际调用点与拒权回跳逻辑无法静态定位，纯静态无法确认是否存在『返回后立即重跳』的死循环，需动态监测 Activity 栈与 Intent 频次；此外 25 个主 DEX 分散、资源名随机化，进一步降低静态可读性（但非加壳/非密文动态加载）。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH"
  ],
  "code_anchors": [
    "com.base.template.OnboardingActivity",
    "com.base.template.services.GuardAccessibilityService",
    "assets/onboarding_stealer.html",
    "res/xml/r_pvbqgtrefwgj.xml",
    "assets/phish_tg.html",
    "com.base.template.TelegramPhishActivity"
  ]
}
```

> 说明：本轮受 14 次工具预算约束，未向风险台账写入条目；DEX 侧跳转代码因类名混淆未能静态还原，已按 `partial_dynamic_or_remote` 如实标注。建议下一轮用动态 UTG + Intent 监测补齐 `ACTION_ACCESSIBILITY_SETTINGS` 触发点与拒权回跳行为。

</details>

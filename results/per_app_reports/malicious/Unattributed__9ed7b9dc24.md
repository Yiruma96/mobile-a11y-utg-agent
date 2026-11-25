# MB_160__9ed7b9dc24｜Unattributed — Privacy

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：84.7s

## 1. 一句话核心结论

- **核心申请方式**：以伪装“电池/界面优化器”的 5 步强制向导冷启动引导，用伪造的 TalkBack 等条目式假无障碍设置页与 Android 14 高亮深链直达本服务，并靠 onResume 复检循环阻止用户从系统无障碍页退出。
- **静态可见性说明**：核心引导链（MainActivity→SetupWizardActivity 五步向导→ACTION_ACCESSIBILITY_SETTINGS 跳转→onResume 复检循环→FakeAccessibilityActivity 假设置页→WebViewActivity）全部以明文 DEX + strings/layout 资源静态可见，无加壳、无加密载荷、无二阶段动态加载。仅获权后跳转的 WebViewActivity 远端 URL 内容（assets 无本地 HTML，未见硬编码 URL）不在包内，属运行期远端页面，不影响无障碍诱导逻辑本身的静态判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9ed7b9dc2436e88370cb8cdcd9a6bd33c0bf6f5271e4805e1c44ee97ab7bd3a3` |
| 包名 / 年份 | `com.estrongs.android.pop` / 2026 |
| 家族 / 品类 | **Unattributed**（同池样本数：13） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Privacy |
| 引导页宣称品牌/身份 | Otimizador de Bateria（电池优化器）/ 企业界面渲染与无障碍优化服务 |
| 系统无障碍列表服务名 | Privacy |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 包名冒用 com.estrongs.android.pop（ES 文件浏览器）而应用名、界面全部为“Privacy / 电池优化器”，二者无任何品牌关联；2) accessibility_service_config 置 isAccessibilityTool="true" 伪称无障碍工具以规避系统无障碍警告与隐私提示；3) 服务 description/summary 使用“Serviço de otimização de renderização e acessibilidade de interface corporativa（企业界面渲染与无障碍优化服务）”掩盖窗口内容读取/按键过滤/截屏能力；4) 存在 FakeAccessibilityActivity、FakeServiceDetailActivity、FakePermissionActivity、RestrictedSettingsActivity、AntiRemovalWarningActivity、SetupWizardActivity 多套同名/近名 Activity 与 android:label 单独定制（Acessibilidade / Serviço de Proteção do Sistema）用于伪装系统页；5) MIUI.FORCE_PERSIST、OPPO/HUAWEI/SAMSUNG_PERSIST 等 meta-data 提升保活。 |
| 无障碍服务类名 | `com.seguranca.protecao.UiAssistBridge` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Serviço de otimização de renderização e acessibilidade de interface corporativa. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.seguranca.protecao.MainActivity（LAUNCHER，theme NoActionBar） | onCreate()：先 W() 启动 CommandControlService 前台服务，再读 rat_prefs.setup_completed 与 m1.b()（无障碍是否已开启） | 原生Activity | **原文**：main_welcome = "Bem-vindo ao Otimizador de Bateria"<br>**译注**：欢迎使用电池优化器 | 无需操作，自动分流跳转；无取消/退出选项（finish() 后进入向导） | `com.seguranca.protecao.MainActivity.onCreate` |
| 2 | 引导说明页 | com.seguranca.protecao.SetupWizardActivity（ProgressBar + 文案 + 主按钮） | onCreate() → setContentView(o1.c) → G() 按 this.a=0 调 L()；按钮 setOnClickListener(new a2(this)) | 原生Activity | **原文**：main_welcome="Bem-vindo ao Otimizador de Bateria"; main_description="Seu dispositivo está otimizado para economizar energia"; btn_enable_protection="Ativar Otimização"; 进度文本 "X de 5"<br>**译注**：欢迎使用电池优化器；您的设备已优化以节省电量；按钮“启用优化”；进度“X / 5” | 点击“Ativar Otimização”推进步骤；无取消/跳过按钮（cancel 字符串未被向导使用） | `com.seguranca.protecao.SetupWizardActivity.onCreate / G / res/values/strings.xml:btn_enable_protection` |
| 3 | 业务功能触发 | SetupWizardActivity 步骤推进 + 系统权限弹窗 | 按钮 onClick → A()：this.a=1 时 H("Configurando serviço de proteção...") 后 B()；a=2 → "Concedendo permissões necessárias..." + n()；a=3 → "Otimizando para proteção contínua..." + m()；a=4 → "Ativando proteção avançada..." + o()；v(int) 链式 requestPermissions（RECORD_AUDIO→ACCESS_FINE_LOCATION→READ_SMS/SEND_SMS→READ_CONTACTS→READ_PHONE_STATE/CALL_PHONE→READ_CALL_LOG） | 原生Activity | **原文**：confirm_activation="Ativar otimização?"; confirm_activation_message="Ao ativar este serviço, você permite que o Otimizador de Bateria monitore e gerencie apps para economizar energia. Deseja continuar?"<br>**译注**：启用优化？启用此服务即表示您允许“电池优化器”监控和管理应用以节省电量。是否继续？ | 反复点击同一“启用优化”按钮并连续授予敏感权限；界面不提供拒绝后的降级路径 | `com.seguranca.protecao.SetupWizardActivity.A / v / res/values/strings.xml:confirm_activation_message` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | w()：new Intent("android.settings.ACCESSIBILITY_SETTINGS")，SDK≥34 追加 SETTINGS_EMBEDDED_DEEP_LINK_HIGHLIGHT_MENU_KEY="top_level_accessibility" 与 SETTINGS_EMBEDDED_DEEP_LINK_INTENT_URI="android-app://com.estrongs.android.pop/com.seguranca.protecao.UiAssistBridge"，addFlags(FLAG_ACTIVITY_NEW_TASK)，startActivity | 系统无障碍页 | **原文**：无（应用侧无文案，直接跳系统页；目标条目名由 android:label="Privacy" 与 accessibility_service_description 决定）<br>**译注**：系统无障碍设置列表，自动高亮定位到名为“Privacy”的服务条目 | 要求用户在系统无障碍列表中打开“Privacy”开关；跳转后应用不在前台，无应用侧取消按钮 | `com.seguranca.protecao.SetupWizardActivity.w` |
| 5 | 拒权反馈循环 | SetupWizardActivity.onResume() 复检 + G() 重绘 | onResume()：每次回到前台重新执行 this.k.b()（无障碍是否开启）；未开启且 this.a<=1 时回退 this.a=2 并 q()、G() 重绘步骤，继续停留在向导 | 原生Activity | **原文**："X de 5" 进度与步骤提示（如 "Configurando serviço de proteção..."）随 onResume 反复重现<br>**译注**：进度条与步骤文案反复回到未完成状态，用户返回即被重新置回引导页 | 迫使用户再次点击按钮重走跳转；无“以后再说/跳过”出口 | `com.seguranca.protecao.SetupWizardActivity.onResume / G` |
| 6 | 遮罩叠层指引 | com.seguranca.protecao.FakeAccessibilityActivity（Manifest label="Acessibilidade"，exported=true）+ GuidedOverlayService / OverlayService（SYSTEM_ALERT_WINDOW） | onCreate()/onResume() 渲染高仿无障碍设置列表；OverlayService/GuidedOverlayService 提供悬浮引导层 | 悬浮窗Overlay | **原文**：fake_accessibility_title="Acessibilidade"; fake_talkback="TalkBack"; fake_talkback_desc="Feedback falado, auditivo e por vibração"; fake_select_to_speak="Selecionar para ouvir"; fake_select_to_speak_desc="Toque nos itens para ouvi-los em voz alta"; fake_switch_access="Acesso por botão"; fake_switch_access_desc="Controle o dispositivo com botões"; fake_system_protection="Otimização de Bateria Avançada"; fake_system_protection_desc="Gerencia o consumo de energia do dispositivo"; fake_services_installed="Serviços instalados"<br>**译注**：无障碍；TalkBack（语音、听觉与振动反馈）；选择朗读（点击条目以朗读）；按键访问（用按键控制设备）；高级电池优化（管理设备能耗）；已安装的服务 | 在与系统无障碍页视觉一致的界面中点击伪造的“高级电池优化”开关，把恶意服务混同为系统无障碍功能 | `com.seguranca.protecao.FakeAccessibilityActivity.onCreate / res/values/strings.xml:fake_* / res/layout FakeAccessibilityScreenBinding` |
| 7 | 获权后动作 | SetupWizardActivity.p() → WebViewActivity / VisualScreenActivity；CommandControlService 常驻 | p()：rat_prefs.setup_completed=true → startForegroundService(CommandControlService) → 若 VisualScreenActivity.z0() 为真进 VisualScreenActivity，否则进 WebViewActivity，finish() | 远端WebView | **原文**：无本地文案（远端页面内容不在包内）；日志 "🌐 WEBVIEW_URL encontrada - abrindo WebViewActivity"<br>**译注**：获权后跳转远端页面，进入下游控制/收割流程 | 无进一步显式操作，用户被带入远端页面 | `com.seguranca.protecao.SetupWizardActivity.p / com.seguranca.protecao.WebViewActivity` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目：android:label="Privacy" + android:description="Serviço de otimização de renderização e acessibilidade de interface corporativa."（res/xml/accessibility_service_config.xml 同时设置 summary 与 isAccessibilityTool="true"）
- 冷启动强制向导 Activity：com.seguranca.protecao.SetupWizardActivity（layout o1.c，含 ImageView/TextView/ProgressBar/Button）展示“Bem-vindo ao Otimizador de Bateria”“Seu dispositivo está otimizado para economizar energia”“X de 5”“Ativar Otimização”
- 步骤伪进度提示：SetupWizardActivity.A() 中硬编码字符串 "Configurando serviço de proteção..."、"Concedendo permissões necessárias..."、"Otimizando para proteção contínua..."、"Ativando proteção avançada..." 写入 H(String) 提示
- 确认弹窗文案：res/values/strings.xml 的 confirm_activation / confirm_activation_message（“Ao ativar este serviço, você permite que o Otimizador de Bateria monitore e gerencie apps para economizar energia.”）
- 高仿真无障碍设置页：com.seguranca.protecao.FakeAccessibilityActivity（Manifest android:label="Acessibilidade"，exported=true），以 fake_talkback / fake_select_to_speak / fake_switch_access / fake_system_protection 等条目复刻系统无障碍列表
- 伪造系统服务详情页：com.seguranca.protecao.FakeServiceDetailActivity（android:label="Serviço de Proteção do Sistema"）
- 受限设置教学页：com.seguranca.protecao.RestrictedSettingsActivity（excludeFromRecents=true）
- 悬浮引导层：com.seguranca.protecao.GuidedOverlayService / OverlayService（配合 SYSTEM_ALERT_WINDOW 权限在系统设置页之上叠放指引）
- 防卸载恐吓全屏页：com.seguranca.protecao.AntiRemovalWarningActivity（showWhenLocked/turnScreenOn，exported=true）
- 多语言资源面：values-pt / values-pt-rBR / values-pt-rPT 及 values-zh-rCN 等 100+ 语言目录，说明面向全球分发

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | Serviço de otimização de renderização e acessibilidade de interface corporativa. | 企业界面渲染与无障碍优化服务。 | `res/values/strings.xml:accessibility_service_description（同时用于 service android:description 与 res/xml/accessibility_service_config.xml android:summary）` | 清理工具伪装 |
| pt | Bem-vindo ao Otimizador de Bateria | 欢迎使用电池优化器 | `res/values/strings.xml:main_welcome（SetupWizardActivity）` | 清理工具伪装 |
| pt | Seu dispositivo está otimizado para economizar energia | 您的设备已优化以节省电量 | `res/values/strings.xml:main_description` | 清理工具伪装 |
| pt | Ativar Otimização | 启用优化 | `res/values/strings.xml:btn_enable_protection（SetupWizardActivity 主按钮 this.h）` | 清理工具伪装 |
| pt | Ao ativar este serviço, você permite que o Otimizador de Bateria monitore e gerencie apps para economizar energia. Deseja continuar? | 启用此服务即表示您允许“电池优化器”监控和管理应用以节省电量。是否继续？ | `res/values/strings.xml:confirm_activation_message` | 隐私承诺 |
| pt | Otimização de Bateria Avançada | 高级电池优化 | `res/values/strings.xml:fake_system_protection（FakeAccessibilityActivity 伪造服务条目）` | 清理工具伪装 |
| pt | Gerencia o consumo de energia do dispositivo | 管理设备的能耗 | `res/values/strings.xml:fake_system_protection_desc` | 清理工具伪装 |
| pt | TalkBack | TalkBack（系统读屏服务名） | `res/values/strings.xml:fake_talkback / fake_talkback_desc="Feedback falado, auditivo e por vibração"` | 故障恐吓 |
| pt | Serviços instalados | 已安装的服务 | `res/values/strings.xml:fake_services_installed（FakeAccessibilityActivity 列表标题，模仿系统无障碍页分区）` | 未知 |
| pt | Configurando serviço de proteção... | 正在配置保护服务…… | `com.seguranca.protecao.SetupWizardActivity.A() 硬编码（a==1 分支）` | 假更新 |
| pt | Ativando proteção avançada... | 正在启用高级保护…… | `com.seguranca.protecao.SetupWizardActivity.A() 硬编码（a==4 分支）` | 假更新 |
| zh | 不在允许的范围内：%1$s | 不在允许的范围内：%1$s | `res/values-zh-rCN/strings.xml（“不在允许的范围内”类提示，对应受限设置/权限拒绝反馈）` | 受限设置分步教学 |
| en | Error: invalid | 错误：无效 | `res/values/strings.xml:error_a11y_label` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：SetupWizardActivity.onResume() 每次回前台重新执行 m1.b()（无障碍是否开启）；未开启时把进度回退到 this.a=2 并调用 q()/G() 重绘向导页，用户从系统无障碍设置返回后立即被重新置入引导流程，无跳过出口；同时 MainActivity 在 setup_completed=false 时始终跳回 SetupWizardActivity，形成应用级死循环
- **遮罩叠层 / 高仿系统设置页**：两者皆有：1) FakeAccessibilityActivity（Manifest label="Acessibilidade"，exported=true）以 TalkBack/Selecionar para ouvir/Acesso por botão 等真实服务名 + 伪造“Otimização de Bateria Avançada”条目复刻系统无障碍列表样式；2) GuidedOverlayService / OverlayService 借助 SYSTEM_ALERT_WINDOW 在系统页之上叠放引导遮罩；3) Android 14+ 跳转时使用 SETTINGS_EMBEDDED_DEEP_LINK_* 让系统设置自动高亮并定位到 UiAssistBridge 条目
- **Android 13+ 受限设置（Restricted Settings）应对**：有：存在专用 com.seguranca.protecao.RestrictedSettingsActivity（excludeFromRecents=true）与 "不在允许的范围内：%1$s"（values-zh-rCN）拒绝反馈文案；无障碍服务本身即受 13+ 受限设置约束，故该 Activity 承担引导用户进应用详情页右上角菜单开启“允许受限设置”的教学角色；未见 Session 安装器（PackageInstaller Session）绕过实现
- **获权后即时行为与防撤权机制**：有：无障碍配置启用 PERFORM_GLOBAL_ACTION 所需的 canPerformGestures、flagRequestFilterKeyEvents 与 WATCH_PKG_INSTALLER/WATCH_SETTINGS 事件类型；配套 AntiRemovalWarningActivity（showWhenLocked/turnScreenOn，exported=true，singleInstance）与 ScreenPersistenceActivity（singleTask，showOnLockScreen）在撤权/卸载时全屏顶起，AliveReceiver/BootReceiver 负责重启复活
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 com.seguranca.protecao.SetupWizardActivity 进入前台并出现 Button 文案“Ativar Otimização”即开始 UTG 采集；在其后捕获 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（尤其携带 SETTINGS_EMBEDDED_DEEP_LINK_INTENT_URI=android-app://com.estrongs.android.pop/com.seguranca.protecao.UiAssistBridge）作为关键落点；用户返回后 1 秒内再次出现同一向导页即证明复检循环成立。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：获权后落地的 WebViewActivity/VisualScreenActivity 远端页面内容不在包内（assets 无本地 HTML，未见硬编码 URL），纯静态无法还原其展示内容，需运行期抓包/UTG 补足；另 Android 14 的 SETTINGS_EMBEDDED_DEEP_LINK 高亮行为依赖系统版本，需在 API 34 设备上复现。样本本身无加壳、无加密载荷，静态加壳不构成此处盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动强制向导页（第一步）** | com.seguranca.protecao.SetupWizardActivity，含 ProgressBar 与“X de 5”文本、Button“Ativar Otimização”，无返回/取消控件 | 这是无障碍诱导的起点，能证明“冷启动即强制引导”且无跳过路径，是区分诱导型恶意样本与良性工具的首要证据 | 按钮文本 Ativar Otimização；进度文本 X de 5；无 Cancelar/跳过节点；同页连续出现系统权限弹窗（录音/定位/短信/通讯录/通话记录） |
| **高仿真无障碍设置页（伪造系统列表）** | com.seguranca.protecao.FakeAccessibilityActivity，Toolbar 标题“Acessibilidade”，列表含 TalkBack、Selecionar para ouvir、Acesso por botão、Otimização de Bateria Avançada | 把恶意开关混排进真实无障碍服务名之间，是身份混淆与欺骗用户开启开关的核心载体，UTG 可直接读到这些条目文本 | TalkBack 条目与“Otimização de Bateria Avançada”同页共存；标题 Acessibilidade 但 Activity 名为 FakeAccessibilityActivity；条目描述“Gerencia o consumo de energia do dispositivo” |
| **跳转后的系统无障碍设置页** | android.settings.ACCESSIBILITY_SETTINGS，Android 14+ 自动高亮 top_level_accessibility 并定位到条目“Privacy” | 可验证深链高亮与条目伪装名（Privacy + 企业渲染优化描述）是否生效，以及用户是否被直接引导到单一开关 | 服务条目名 Privacy；描述“Serviço de otimização de renderização e acessibilidade de interface corporativa.”；设置页被高亮/定位到该条目 |
| **返回后的复检循环页 / 悬浮引导遮罩** | 再次出现的 SetupWizardActivity，或 GuidedOverlayService 叠加的悬浮窗（SYSTEM_ALERT_WINDOW） | 证明拒绝/退出后不会降级而是被重新拉起，属于强制胁迫而非透明说明 | 从系统设置返回后 <2s 内向导页重现；悬浮窗节点与系统设置页同屏；向导进度回退（X de 5 数值下降） |
| **获权后落地的远端 WebView 页** | com.seguranca.protecao.WebViewActivity（Theme.NoTitleBar.Fullscreen）或 VisualScreenActivity | 确认获权后进入下游控制/收割阶段，补足静态不可见的远端内容证据 | WebView 节点与页面标题；加载的远端 URL/域名；页面是否呈现配置指令或后台管理界面 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.seguranca.protecao.MainActivity.onCreate`
- `com.seguranca.protecao.SetupWizardActivity.onCreate`
- `com.seguranca.protecao.SetupWizardActivity.onResume`
- `com.seguranca.protecao.SetupWizardActivity.w`
- `com.seguranca.protecao.SetupWizardActivity.A`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**静态可见性：clear（逻辑完全静态可见，无加壳）**。该样本是典型的“无障碍权限诱导 + 伪装电池优化器 + 假无障碍设置页”链条，并非 ES 文件浏览器（包名 `com.estrongs.android.pop` 系伪造，真实显示名 `Privacy`，品牌宣称“Otimizador de Bateria”）。

1. **冷启动入口**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.seguranca.protecao.MainActivity#onCreate>) 先拉起 `CommandControlService` 常驻前台服务，再按 `rat_prefs.setup_completed` / 无障碍是否已开启分流：已开启→直接进 `WebViewActivity`（远端页面）；存在 `assets/visual_config.json` → `VisualScreenActivity`；否则 → [SetupWizardActivity](<resource-unit:#1.dex1 code:com.seguranca.protecao.SetupWizardActivity#onCreate>)。
2. **5 步强制引导向导**：`SetupWizardActivity` 用 `ProgressBar` + “X de 5” 文本呈现进度，按钮文案 `btn_enable_protection` = “Ativar Otimização”（启用优化）。`A()` 按 `this.a` 分派步骤，并弹出 “Configurando serviço de proteção...” / “Concedendo permissões necessárias...” / “Otimizando para proteção contínua...” / “Ativando proteção avançada...” 等伪进度提示，逐步索取录音、定位、短信、通讯录、电话、通话记录权限。
3. **跳转受限设置/无障碍设置**：[SetupWizardActivity.w()](<resource-unit:#1.dex1 code:com.seguranca.protecao.SetupWizardActivity#w>) 直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`；Android 14+ 额外塞入 `SETTINGS_EMBEDDED_DEEP_LINK_HIGHLIGHT_MENU_KEY=top_level_accessibility` 与 `SETTINGS_EMBEDDED_DEEP_LINK_INTENT_URI=android-app://<pkg>/com.seguranca.protecao.UiAssistBridge`，即**高亮并直达本服务条目**，绕过用户在列表中自行辨识。
4. **拒绝后反复拉起**：[onResume()](<resource-unit:#1.dex1 code:com.seguranca.protecao.SetupWizardActivity#onResume>) 每次回前台重查 `m1.b()`（无障碍是否开启），未开启则回退步骤并 `G()` 重绘，形成“返回系统设置→立刻又被向导顶回”的循环；无“跳过/取消”降级路径（`cancel` 字符串存在但向导流程未使用）。
5. **高仿真假无障碍设置页**：`FakeAccessibilityActivity`（Manifest label `Acessibilidade`）用 `TalkBack`、`Selecionar para ouvir`、`Acesso por botão` 等真实服务名 + 伪造的 “Otimização de Bateria Avançada / Gerencia o consumo de energia do dispositivo” 条目，把恶意开关混排进系统无障碍列表样式中；配套 `RestrictedSettingsActivity` 做 13+ 受限设置教学。
6. **获权后动作**：`p()` 写 `setup_completed=true` → 跳 `WebViewActivity`/`VisualScreenActivity`；`accessibility_service_config` 声明 `canRetrieveWindowContent`、`canRequestFilterKeyEvents`、`canTakeScreenshot`、`isAccessibilityTool="true"`（伪造无障碍工具豁免），服务 label 为 `Privacy`、description 伪装成“企业界面渲染与无障碍优化服务”。

> 说明：本轮受 8–14 次工具调用硬约束，未逐行确认 `w()` 的确切调用方（位于 `A()→B()/n()/m()/o()` 步骤链的截断段内），亦未按自主审计契约写入 `record_risk` 台账；以下 JSON 仅基于已读取的确证代码/资源。

```json
{
  "static_visibility": "clear",
  "visibility_note": "核心引导链（MainActivity→SetupWizardActivity 五步向导→ACTION_ACCESSIBILITY_SETTINGS 跳转→onResume 复检循环→FakeAccessibilityActivity 假设置页→WebViewActivity）全部以明文 DEX + strings/layout 资源静态可见，无加壳、无加密载荷、无二阶段动态加载。仅获权后跳转的 WebViewActivity 远端 URL 内容（assets 无本地 HTML，未见硬编码 URL）不在包内，属运行期远端页面，不影响无障碍诱导逻辑本身的静态判定。",
  "summary_one_liner": "以伪装“电池/界面优化器”的 5 步强制向导冷启动引导，用伪造的 TalkBack 等条目式假无障碍设置页与 Android 14 高亮深链直达本服务，并靠 onResume 复检循环阻止用户从系统无障碍页退出。",
  "disguise_identity": {
    "app_display_name": "Privacy",
    "claimed_brand_or_persona": "Otimizador de Bateria（电池优化器）/ 企业界面渲染与无障碍优化服务",
    "a11y_service_label": "Privacy",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 包名冒用 com.estrongs.android.pop（ES 文件浏览器）而应用名、界面全部为“Privacy / 电池优化器”，二者无任何品牌关联；2) accessibility_service_config 置 isAccessibilityTool=\"true\" 伪称无障碍工具以规避系统无障碍警告与隐私提示；3) 服务 description/summary 使用“Serviço de otimização de renderização e acessibilidade de interface corporativa（企业界面渲染与无障碍优化服务）”掩盖窗口内容读取/按键过滤/截屏能力；4) 存在 FakeAccessibilityActivity、FakeServiceDetailActivity、FakePermissionActivity、RestrictedSettingsActivity、AntiRemovalWarningActivity、SetupWizardActivity 多套同名/近名 Activity 与 android:label 单独定制（Acessibilidade / Serviço de Proteção do Sistema）用于伪装系统页；5) MIUI.FORCE_PERSIST、OPPO/HUAWEI/SAMSUNG_PERSIST 等 meta-data 提升保活。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.seguranca.protecao.MainActivity（LAUNCHER，theme NoActionBar）",
      "trigger_event": "onCreate()：先 W() 启动 CommandControlService 前台服务，再读 rat_prefs.setup_completed 与 m1.b()（无障碍是否已开启）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "main_welcome = \"Bem-vindo ao Otimizador de Bateria\"",
      "shown_text_zh": "欢迎使用电池优化器",
      "user_action_requested": "无需操作，自动分流跳转；无取消/退出选项（finish() 后进入向导）",
      "code_anchor": "com.seguranca.protecao.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.seguranca.protecao.SetupWizardActivity（ProgressBar + 文案 + 主按钮）",
      "trigger_event": "onCreate() → setContentView(o1.c) → G() 按 this.a=0 调 L()；按钮 setOnClickListener(new a2(this))",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "main_welcome=\"Bem-vindo ao Otimizador de Bateria\"; main_description=\"Seu dispositivo está otimizado para economizar energia\"; btn_enable_protection=\"Ativar Otimização\"; 进度文本 \"X de 5\"",
      "shown_text_zh": "欢迎使用电池优化器；您的设备已优化以节省电量；按钮“启用优化”；进度“X / 5”",
      "user_action_requested": "点击“Ativar Otimização”推进步骤；无取消/跳过按钮（cancel 字符串未被向导使用）",
      "code_anchor": "com.seguranca.protecao.SetupWizardActivity.onCreate / G / res/values/strings.xml:btn_enable_protection"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "SetupWizardActivity 步骤推进 + 系统权限弹窗",
      "trigger_event": "按钮 onClick → A()：this.a=1 时 H(\"Configurando serviço de proteção...\") 后 B()；a=2 → \"Concedendo permissões necessárias...\" + n()；a=3 → \"Otimizando para proteção contínua...\" + m()；a=4 → \"Ativando proteção avançada...\" + o()；v(int) 链式 requestPermissions（RECORD_AUDIO→ACCESS_FINE_LOCATION→READ_SMS/SEND_SMS→READ_CONTACTS→READ_PHONE_STATE/CALL_PHONE→READ_CALL_LOG）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "confirm_activation=\"Ativar otimização?\"; confirm_activation_message=\"Ao ativar este serviço, você permite que o Otimizador de Bateria monitore e gerencie apps para economizar energia. Deseja continuar?\"",
      "shown_text_zh": "启用优化？启用此服务即表示您允许“电池优化器”监控和管理应用以节省电量。是否继续？",
      "user_action_requested": "反复点击同一“启用优化”按钮并连续授予敏感权限；界面不提供拒绝后的降级路径",
      "code_anchor": "com.seguranca.protecao.SetupWizardActivity.A / v / res/values/strings.xml:confirm_activation_message"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "w()：new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")，SDK≥34 追加 SETTINGS_EMBEDDED_DEEP_LINK_HIGHLIGHT_MENU_KEY=\"top_level_accessibility\" 与 SETTINGS_EMBEDDED_DEEP_LINK_INTENT_URI=\"android-app://com.estrongs.android.pop/com.seguranca.protecao.UiAssistBridge\"，addFlags(FLAG_ACTIVITY_NEW_TASK)，startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧无文案，直接跳系统页；目标条目名由 android:label=\"Privacy\" 与 accessibility_service_description 决定）",
      "shown_text_zh": "系统无障碍设置列表，自动高亮定位到名为“Privacy”的服务条目",
      "user_action_requested": "要求用户在系统无障碍列表中打开“Privacy”开关；跳转后应用不在前台，无应用侧取消按钮",
      "code_anchor": "com.seguranca.protecao.SetupWizardActivity.w"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "SetupWizardActivity.onResume() 复检 + G() 重绘",
      "trigger_event": "onResume()：每次回到前台重新执行 this.k.b()（无障碍是否开启）；未开启且 this.a<=1 时回退 this.a=2 并 q()、G() 重绘步骤，继续停留在向导",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "\"X de 5\" 进度与步骤提示（如 \"Configurando serviço de proteção...\"）随 onResume 反复重现",
      "shown_text_zh": "进度条与步骤文案反复回到未完成状态，用户返回即被重新置回引导页",
      "user_action_requested": "迫使用户再次点击按钮重走跳转；无“以后再说/跳过”出口",
      "code_anchor": "com.seguranca.protecao.SetupWizardActivity.onResume / G"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.seguranca.protecao.FakeAccessibilityActivity（Manifest label=\"Acessibilidade\"，exported=true）+ GuidedOverlayService / OverlayService（SYSTEM_ALERT_WINDOW）",
      "trigger_event": "onCreate()/onResume() 渲染高仿无障碍设置列表；OverlayService/GuidedOverlayService 提供悬浮引导层",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "fake_accessibility_title=\"Acessibilidade\"; fake_talkback=\"TalkBack\"; fake_talkback_desc=\"Feedback falado, auditivo e por vibração\"; fake_select_to_speak=\"Selecionar para ouvir\"; fake_select_to_speak_desc=\"Toque nos itens para ouvi-los em voz alta\"; fake_switch_access=\"Acesso por botão\"; fake_switch_access_desc=\"Controle o dispositivo com botões\"; fake_system_protection=\"Otimização de Bateria Avançada\"; fake_system_protection_desc=\"Gerencia o consumo de energia do dispositivo\"; fake_services_installed=\"Serviços instalados\"",
      "shown_text_zh": "无障碍；TalkBack（语音、听觉与振动反馈）；选择朗读（点击条目以朗读）；按键访问（用按键控制设备）；高级电池优化（管理设备能耗）；已安装的服务",
      "user_action_requested": "在与系统无障碍页视觉一致的界面中点击伪造的“高级电池优化”开关，把恶意服务混同为系统无障碍功能",
      "code_anchor": "com.seguranca.protecao.FakeAccessibilityActivity.onCreate / res/values/strings.xml:fake_* / res/layout FakeAccessibilityScreenBinding"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "SetupWizardActivity.p() → WebViewActivity / VisualScreenActivity；CommandControlService 常驻",
      "trigger_event": "p()：rat_prefs.setup_completed=true → startForegroundService(CommandControlService) → 若 VisualScreenActivity.z0() 为真进 VisualScreenActivity，否则进 WebViewActivity，finish()",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "无本地文案（远端页面内容不在包内）；日志 \"🌐 WEBVIEW_URL encontrada - abrindo WebViewActivity\"",
      "shown_text_zh": "获权后跳转远端页面，进入下游控制/收割流程",
      "user_action_requested": "无进一步显式操作，用户被带入远端页面",
      "code_anchor": "com.seguranca.protecao.SetupWizardActivity.p / com.seguranca.protecao.WebViewActivity"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目：android:label=\"Privacy\" + android:description=\"Serviço de otimização de renderização e acessibilidade de interface corporativa.\"（res/xml/accessibility_service_config.xml 同时设置 summary 与 isAccessibilityTool=\"true\"）",
    "冷启动强制向导 Activity：com.seguranca.protecao.SetupWizardActivity（layout o1.c，含 ImageView/TextView/ProgressBar/Button）展示“Bem-vindo ao Otimizador de Bateria”“Seu dispositivo está otimizado para economizar energia”“X de 5”“Ativar Otimização”",
    "步骤伪进度提示：SetupWizardActivity.A() 中硬编码字符串 \"Configurando serviço de proteção...\"、\"Concedendo permissões necessárias...\"、\"Otimizando para proteção contínua...\"、\"Ativando proteção avançada...\" 写入 H(String) 提示",
    "确认弹窗文案：res/values/strings.xml 的 confirm_activation / confirm_activation_message（“Ao ativar este serviço, você permite que o Otimizador de Bateria monitore e gerencie apps para economizar energia.”）",
    "高仿真无障碍设置页：com.seguranca.protecao.FakeAccessibilityActivity（Manifest android:label=\"Acessibilidade\"，exported=true），以 fake_talkback / fake_select_to_speak / fake_switch_access / fake_system_protection 等条目复刻系统无障碍列表",
    "伪造系统服务详情页：com.seguranca.protecao.FakeServiceDetailActivity（android:label=\"Serviço de Proteção do Sistema\"）",
    "受限设置教学页：com.seguranca.protecao.RestrictedSettingsActivity（excludeFromRecents=true）",
    "悬浮引导层：com.seguranca.protecao.GuidedOverlayService / OverlayService（配合 SYSTEM_ALERT_WINDOW 权限在系统设置页之上叠放指引）",
    "防卸载恐吓全屏页：com.seguranca.protecao.AntiRemovalWarningActivity（showWhenLocked/turnScreenOn，exported=true）",
    "多语言资源面：values-pt / values-pt-rBR / values-pt-rPT 及 values-zh-rCN 等 100+ 语言目录，说明面向全球分发"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "Serviço de otimização de renderização e acessibilidade de interface corporativa.",
      "text_zh": "企业界面渲染与无障碍优化服务。",
      "source_location": "res/values/strings.xml:accessibility_service_description（同时用于 service android:description 与 res/xml/accessibility_service_config.xml android:summary）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "pt",
      "text_verbatim": "Bem-vindo ao Otimizador de Bateria",
      "text_zh": "欢迎使用电池优化器",
      "source_location": "res/values/strings.xml:main_welcome（SetupWizardActivity）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "pt",
      "text_verbatim": "Seu dispositivo está otimizado para economizar energia",
      "text_zh": "您的设备已优化以节省电量",
      "source_location": "res/values/strings.xml:main_description",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "pt",
      "text_verbatim": "Ativar Otimização",
      "text_zh": "启用优化",
      "source_location": "res/values/strings.xml:btn_enable_protection（SetupWizardActivity 主按钮 this.h）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "pt",
      "text_verbatim": "Ao ativar este serviço, você permite que o Otimizador de Bateria monitore e gerencie apps para economizar energia. Deseja continuar?",
      "text_zh": "启用此服务即表示您允许“电池优化器”监控和管理应用以节省电量。是否继续？",
      "source_location": "res/values/strings.xml:confirm_activation_message",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "pt",
      "text_verbatim": "Otimização de Bateria Avançada",
      "text_zh": "高级电池优化",
      "source_location": "res/values/strings.xml:fake_system_protection（FakeAccessibilityActivity 伪造服务条目）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "pt",
      "text_verbatim": "Gerencia o consumo de energia do dispositivo",
      "text_zh": "管理设备的能耗",
      "source_location": "res/values/strings.xml:fake_system_protection_desc",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "pt",
      "text_verbatim": "TalkBack",
      "text_zh": "TalkBack（系统读屏服务名）",
      "source_location": "res/values/strings.xml:fake_talkback / fake_talkback_desc=\"Feedback falado, auditivo e por vibração\"",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "pt",
      "text_verbatim": "Serviços instalados",
      "text_zh": "已安装的服务",
      "source_location": "res/values/strings.xml:fake_services_installed（FakeAccessibilityActivity 列表标题，模仿系统无障碍页分区）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "pt",
      "text_verbatim": "Configurando serviço de proteção...",
      "text_zh": "正在配置保护服务……",
      "source_location": "com.seguranca.protecao.SetupWizardActivity.A() 硬编码（a==1 分支）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "pt",
      "text_verbatim": "Ativando proteção avançada...",
      "text_zh": "正在启用高级保护……",
      "source_location": "com.seguranca.protecao.SetupWizardActivity.A() 硬编码（a==4 分支）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "zh",
      "text_verbatim": "不在允许的范围内：%1$s",
      "text_zh": "不在允许的范围内：%1$s",
      "source_location": "res/values-zh-rCN/strings.xml（“不在允许的范围内”类提示，对应受限设置/权限拒绝反馈）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Error: invalid",
      "text_zh": "错误：无效",
      "source_location": "res/values/strings.xml:error_a11y_label",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "SetupWizardActivity.onResume() 每次回前台重新执行 m1.b()（无障碍是否开启）；未开启时把进度回退到 this.a=2 并调用 q()/G() 重绘向导页，用户从系统无障碍设置返回后立即被重新置入引导流程，无跳过出口；同时 MainActivity 在 setup_completed=false 时始终跳回 SetupWizardActivity，形成应用级死循环",
    "overlay_or_fake_settings": "两者皆有：1) FakeAccessibilityActivity（Manifest label=\"Acessibilidade\"，exported=true）以 TalkBack/Selecionar para ouvir/Acesso por botão 等真实服务名 + 伪造“Otimização de Bateria Avançada”条目复刻系统无障碍列表样式；2) GuidedOverlayService / OverlayService 借助 SYSTEM_ALERT_WINDOW 在系统页之上叠放引导遮罩；3) Android 14+ 跳转时使用 SETTINGS_EMBEDDED_DEEP_LINK_* 让系统设置自动高亮并定位到 UiAssistBridge 条目",
    "restricted_settings_13plus_coaching": "有：存在专用 com.seguranca.protecao.RestrictedSettingsActivity（excludeFromRecents=true）与 \"不在允许的范围内：%1$s\"（values-zh-rCN）拒绝反馈文案；无障碍服务本身即受 13+ 受限设置约束，故该 Activity 承担引导用户进应用详情页右上角菜单开启“允许受限设置”的教学角色；未见 Session 安装器（PackageInstaller Session）绕过实现",
    "post_grant_anti_removal": "有：无障碍配置启用 PERFORM_GLOBAL_ACTION 所需的 canPerformGestures、flagRequestFilterKeyEvents 与 WATCH_PKG_INSTALLER/WATCH_SETTINGS 事件类型；配套 AntiRemovalWarningActivity（showWhenLocked/turnScreenOn，exported=true，singleInstance）与 ScreenPersistenceActivity（singleTask，showOnLockScreen）在撤权/卸载时全屏顶起，AliveReceiver/BootReceiver 负责重启复活",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 com.seguranca.protecao.SetupWizardActivity 进入前台并出现 Button 文案“Ativar Otimização”即开始 UTG 采集；在其后捕获 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（尤其携带 SETTINGS_EMBEDDED_DEEP_LINK_INTENT_URI=android-app://com.estrongs.android.pop/com.seguranca.protecao.UiAssistBridge）作为关键落点；用户返回后 1 秒内再次出现同一向导页即证明复检循环成立。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动强制向导页（第一步）",
        "page_identifier": "com.seguranca.protecao.SetupWizardActivity，含 ProgressBar 与“X de 5”文本、Button“Ativar Otimização”，无返回/取消控件",
        "why_most_useful": "这是无障碍诱导的起点，能证明“冷启动即强制引导”且无跳过路径，是区分诱导型恶意样本与良性工具的首要证据",
        "observable_utg_signals": ["按钮文本 Ativar Otimização", "进度文本 X de 5", "无 Cancelar/跳过节点", "同页连续出现系统权限弹窗（录音/定位/短信/通讯录/通话记录）"]
      },
      {
        "page_role": "高仿真无障碍设置页（伪造系统列表）",
        "page_identifier": "com.seguranca.protecao.FakeAccessibilityActivity，Toolbar 标题“Acessibilidade”，列表含 TalkBack、Selecionar para ouvir、Acesso por botão、Otimização de Bateria Avançada",
        "why_most_useful": "把恶意开关混排进真实无障碍服务名之间，是身份混淆与欺骗用户开启开关的核心载体，UTG 可直接读到这些条目文本",
        "observable_utg_signals": ["TalkBack 条目与“Otimização de Bateria Avançada”同页共存", "标题 Acessibilidade 但 Activity 名为 FakeAccessibilityActivity", "条目描述“Gerencia o consumo de energia do dispositivo”"]
      },
      {
        "page_role": "跳转后的系统无障碍设置页",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS，Android 14+ 自动高亮 top_level_accessibility 并定位到条目“Privacy”",
        "why_most_useful": "可验证深链高亮与条目伪装名（Privacy + 企业渲染优化描述）是否生效，以及用户是否被直接引导到单一开关",
        "observable_utg_signals": ["服务条目名 Privacy", "描述“Serviço de otimização de renderização e acessibilidade de interface corporativa.”", "设置页被高亮/定位到该条目"]
      },
      {
        "page_role": "返回后的复检循环页 / 悬浮引导遮罩",
        "page_identifier": "再次出现的 SetupWizardActivity，或 GuidedOverlayService 叠加的悬浮窗（SYSTEM_ALERT_WINDOW）",
        "why_most_useful": "证明拒绝/退出后不会降级而是被重新拉起，属于强制胁迫而非透明说明",
        "observable_utg_signals": ["从系统设置返回后 <2s 内向导页重现", "悬浮窗节点与系统设置页同屏", "向导进度回退（X de 5 数值下降）"]
      },
      {
        "page_role": "获权后落地的远端 WebView 页",
        "page_identifier": "com.seguranca.protecao.WebViewActivity（Theme.NoTitleBar.Fullscreen）或 VisualScreenActivity",
        "why_most_useful": "确认获权后进入下游控制/收割阶段，补足静态不可见的远端内容证据",
        "observable_utg_signals": ["WebView 节点与页面标题", "加载的远端 URL/域名", "页面是否呈现配置指令或后台管理界面"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "获权后落地的 WebViewActivity/VisualScreenActivity 远端页面内容不在包内（assets 无本地 HTML，未见硬编码 URL），纯静态无法还原其展示内容，需运行期抓包/UTG 补足；另 Android 14 的 SETTINGS_EMBEDDED_DEEP_LINK 高亮行为依赖系统版本，需在 API 34 设备上复现。样本本身无加壳、无加密载荷，静态加壳不构成此处盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL"
  ],
  "code_anchors": [
    "com.seguranca.protecao.MainActivity.onCreate",
    "com.seguranca.protecao.SetupWizardActivity.onCreate",
    "com.seguranca.protecao.SetupWizardActivity.onResume",
    "com.seguranca.protecao.SetupWizardActivity.w",
    "com.seguranca.protecao.SetupWizardActivity.A",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>

# MB_037__5be608a563｜Unattributed — Rei dos Canais

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：144.0s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即进入不可跳过的 5 步『系统保护』向导，用假电池优化/假安全防护话术配合 Android 13+ 受限设置分步教学，把用户推向 ACCESSIBILITY_SETTINGS 并每秒轮询、超时重拉，同时在系统设置页顶部叠加半透明遮罩指引点击，获权后转入远端 WebView。
- **静态可见性说明**：DEX 未加壳、未加密，无障碍服务声明、5 步向导文案、受限设置教学弹窗、遮罩文字与跳转 Intent 均为明文硬编码，可完整静态还原。仅两处不在静态范围内：获权后打开的 WebViewActivity 远端页面内容（WEBVIEW_URL），以及 assets/visual_config.json 驱动的视觉层配置。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `5be608a563a02c94dbf3b1812b3aa0685a6f8228b5dc74c773cc3c912adef7ba` |
| 包名 / 年份 | `com.arlosoft.macrodroid` / 2026 |
| 家族 / 品类 | **Unattributed**（同池样本数：13） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Rei dos Canais |
| 引导页宣称品牌/身份 | Sistema de Proteção / Serviço de Proteção（虚构的『系统保护服务』与『Otimização de Bateria Avançada 高级电池优化』），同时盗用正版应用包名 com.arlosoft.macrodroid |
| 系统无障碍列表服务名 | Rei dos Canais |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：三重身份错位：桌面名/无障碍列表名『Rei dos Canais』、说明文字自称『企业界面渲染与无障碍优化服务』、遮罩却让用户找『Sistema de Proteção』；包名冒用 com.arlosoft.macrodroid 而代码命名空间为 com.seguranca.protecao；accessibility_service_config 伪造 android:isAccessibilityTool="true" 以规避 Android 13+ 受限设置限制；另设 FakeAccessibilityActivity（label『Acessibilidade』）、FakeServiceDetailActivity（label『Serviço de Proteção do Sistema』）、FakePermissionActivity 等高仿系统页组件。 |
| 无障碍服务类名 | `com.seguranca.protecao.UiAssistBridge` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Serviço de otimização de renderização e acessibilidade de interface corporativa. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.seguranca.protecao.MainActivity（LAUNCHER，Theme.Material3.DayNight.NoActionBar） | onCreate：先 startForegroundService(CommandControlService)，再读 SharedPreferences rat_prefs.setup_completed 与 p1.b() 无障碍状态判断分流 | 原生Activity | **原文**：无（直接 finish() 跳转，不显示界面）<br>**译注**：无界面，立即转到向导页或远端 WebView | 无交互；未完成配置时被强制导向 SetupWizardActivity，无取消入口 | `com.seguranca.protecao.MainActivity#onCreate / #W` |
| 2 | 引导说明页 | com.seguranca.protecao.SetupWizardActivity（ProgressBar 显示 0 de 5），文案由 L() 渲染 | onCreate → G() → 阶段 0 → L() | 原生Activity | **原文**：Bem-vindo ao Sistema de Proteção / Este assistente irá configurar a proteção do seu dispositivo em apenas alguns passos.\n\nVocê precisará conceder algumas permissões para que a proteção funcione corretamente.\n\nToque em AVANÇAR para continuar. / 按钮：Avançar<br>**译注**：欢迎使用『保护系统』：本助手只需几步即可为你的设备配置保护，你需要授予一些权限。点击『前进』继续。 | 仅可点击『Avançar』；无跳过、无返回、无取消按钮 | `com.seguranca.protecao.SetupWizardActivity#L / #onCreate / #G` |
| 3 | 引导说明页 | SetupWizardActivity 阶段 1（Etapa 1: Serviço de Proteção），文案 C() | 点击『Avançar』→ A() → z() → 阶段 1 → G() → C() | 原生Activity | **原文**：Etapa 1: Serviço de Proteção / O Serviço de Proteção precisa ser ativado para:\n\n• Detectar aplicativos maliciosos\n• Bloquear ameaças automaticamente\n• Proteger seus dados em tempo real\n\nToque em ATIVAR para habilitar o serviço. / 按钮：Ativar Serviço<br>**译注**：第 1 步：保护服务。该服务需要被启用才能：检测恶意应用、自动拦截威胁、实时保护你的数据。点击『启用服务』。 | 点击『Ativar Serviço』（唯一前进路径，无取消） | `com.seguranca.protecao.SetupWizardActivity#C / #A` |
| 4 | 跳受限设置 | 不可取消 AlertDialog『Configuração Especial Necessária』→ 系统 ACTION_ACCESSIBILITY_SETTINGS | 阶段 1 点击后 A() → B()：SDK≥35 走 D() 弹框；SDK<35 走 f2 → w() 直接跳设置（SDK≥34 附带 SETTINGS_EMBEDDED_DEEP_LINK_HIGHLIGHT_MENU_KEY=top_level_accessibility 深链高亮） | 原生Dialog → 系统无障碍页 | **原文**：Configuração Especial Necessária / SIGA EXATAMENTE ESTES PASSOS:\n\n1. Na próxima tela, clique em 'Otimização de Bateria Avançada'\n\n2. Quando aparecer o aviso, clique em 'Allow restricted settings' (Permitir configurações restritas)\n\n3. Depois ative o serviço normalmente\n\n4. Volte para este app e aguarde a próxima etapa / 按钮：Abrir Configurações<br>**译注**：需要特殊配置：请严格按以下步骤操作——1. 在下一屏点击『高级电池优化』；2. 出现警告时点击『允许受限设置』；3. 然后正常启用服务；4. 回到本应用等待下一步。按钮『打开设置』。 | 点击『Abrir Configurações』进入系统无障碍页并按提示点『允许受限设置』；Cancelar 按钮点击监听器为 null（形同无效），setCancelable(false) | `com.seguranca.protecao.SetupWizardActivity#D / #w / #B` |
| 5 | 遮罩叠层指引 | com.seguranca.protecao.GuidedOverlayService 顶部悬浮窗（FrameLayout，WindowManager，宽 MATCH_PARENT/高 WRAP_CONTENT，gravity=TOP，y=100，#CC000000 半透明底） | onStartCommand 收到 extra guide_type="accessibility" → d() addView，并 postDelayed 10000ms 自动移除 | 悬浮窗Overlay | **原文**：👇 Encontre 'Sistema de Proteção' e toque para ativar<br>**译注**：👇 找到『保护系统』并点击启用 | 要求用户在系统无障碍列表中寻找名为『Sistema de Proteção』的条目并点击——而列表实际显示为『Rei dos Canais』，形成指认错位，迫使用户逐一尝试 | `com.seguranca.protecao.GuidedOverlayService#d / #onStartCommand / GuidedOverlayService$a#<init>` |
| 6 | 拒权反馈循环 | SetupWizardActivity$b（Handler 每 1000ms 轮询 p1.b()）+ onResume 自动推进 | 跳设置后 y() → postDelayed(SetupWizardActivity$b, 1000ms)；onResume 再次检测无障碍状态 | 原生Activity | **原文**：（日志）✅ Accessibility ativado! / ⚠️ Timeout atingido - assumindo ativação manual<br>**译注**：轮询最多 60 次（约 60 秒）：检测到无障碍开启即调用 p() 放行；超时则重建 SetupWizardActivity 到前台并调用 q()/z() 继续推进阶段，用户返回或拒绝后仍被拉回向导 | 无退出路径；拒绝即被循环重拉（最多 60 次轮询后强制重入向导） | `com.seguranca.protecao.SetupWizardActivity$b#run / SetupWizardActivity#y / #onResume` |
| 7 | 跳受限设置 | com.seguranca.protecao.RestrictedSettingsActivity → 不可取消 AlertDialog『Permitir configurações restritas』→ ACTION_APPLICATION_DETAILS_SETTINGS(package:self) | onCreate：SDK<34 走 d() 直接放行；SDK≥34 走 h() 弹框；点『Abrir Configurações』→ g() startActivityForResult(intent, 9999) | 原生Dialog → 系统应用详情页 | **原文**：Permitir configurações restritas / Para ativar o Assistente de Proteção você precisa liberar as configurações restritas do Android 14.\n\nPassos:\n1. Toque em "Abrir Configurações".\n2. No canto superior direito, toque no menu (⋮) e selecione "Permitir configurações restritas".\n3. Confirme e volte para continuar a configuração. / 按钮：Abrir Configurações / Cancelar<br>**译注**：允许受限设置：为启用『保护助手』，你必须放开 Android 14 的受限设置。步骤：1. 点击『打开设置』；2. 在右上角点击菜单(⋮)并选择『允许受限设置』；3. 确认后返回继续配置。 | 点击『Abrir Configurações』→ 在应用详情页右上角 ⋮ 中选择『允许受限设置』；『Cancelar』虽存在但 onActivityResult 回跳即写 restricted_allow_done 并跳 MainActivity，形同继续流程 | `com.seguranca.protecao.RestrictedSettingsActivity#h / #g / #d / #onCreate` |
| 8 | 获权后动作 | SetupWizardActivity 阶段 2-5（I/E/m/o/F）→ p() → WebViewActivity 或 VisualScreenActivity | 无障碍检测通过 → p()；onResume 若 a<=1 直接置 a=2 并 q()+G() 自动跳阶段；阶段 2 sendBroadcast AUTO_GRANT_PERMISSIONS 并 requestPermissions(CAMERA)；阶段 3 sendBroadcast AUTO_DISABLE_BATTERY；阶段 5 → p() | 原生Activity → 远端WebView | **原文**：Para funcionar corretamente, precisamos de:\n\n• Câmera - detectar ameaças visuais\n• Microfone - monitorar atividades suspeitas\n• SMS - verificar mensagens perigosas\n• Contatos - proteger sua lista\n• Localização - rastrear dispositivo roubado / ✅ Configuração Concluída! / Parabéns! Seu dispositivo está agora protegido.<br>**译注**：为正常运行，我们需要：相机—检测视觉威胁；麦克风—监控可疑活动；短信—检查危险信息；通讯录—保护你的列表；定位—追踪被盗设备。配置完成！你的设备现在已受保护。 | 点击『Conceder Permissões』授予相机/短信/通讯录等权限；完成后写入 setup_completed=true 并跳转远端 WebView 页面（WEBVIEW_URL），此后 UiAssistBridge 无障碍服务全量接管窗口内容与手势 | `com.seguranca.protecao.SetupWizardActivity#I / #n / #m / #p / #F` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- SetupWizardActivity 全屏原生 Activity（layout r1.c）：ProgressBar『x de 5』+ 标题 TextView(q1.p) + 正文 TextView(q1.l) + 唯一按钮(q1.e)，文案由 L()/C()/I()/E()/K()/F() 硬编码写入
- SetupWizardActivity.D() 的 AlertDialog『Configuração Especial Necessária』：setCancelable(false)，Cancelar 监听器为 null
- RestrictedSettingsActivity.h() 的 AlertDialog『Permitir configurações restritas』：setCancelable(false)，含 3 步受限设置图文教学
- GuidedOverlayService.d() 的 WindowManager 顶部悬浮 FrameLayout（#CC000000，y=100，10 秒自动消失）：『👇 Encontre 'Sistema de Proteção' e toque para ativar』
- 系统无障碍列表条目：label=@string/app_name『Rei dos Canais』，android:description / summary『Serviço de otimização de renderização e acessibilidade de interface corporativa.』
- Manifest meta-data：app.description『Serviço de otimização de interface e energia』；app.category『tools』
- 获权后远端 WebView（WebViewActivity）与 assets/s1s2s3s4.html、assets/uns.html 本地 HTML 外壳（Loading / Not Compatible 过渡页）
- strings.xml：btn_enable_protection『Ativar Otimização』、fake_system_protection『Otimização de Bateria Avançada』、fake_system_protection_desc『Gerencia o consumo de energia do dispositivo』、fake_services_installed『Serviços instalados』、permission_observe『Observar suas ações』、permission_retrieve『Recuperar conteúdo da janela』

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | Bem-vindo ao Sistema de Proteção | 欢迎使用『保护系统』 | `SetupWizardActivity#L（硬编码）` | 假反诈安全 |
| pt | Este assistente irá configurar a proteção do seu dispositivo em apenas alguns passos. Você precisará conceder algumas permissões para que a proteção funcione corretamente. Toque em AVANÇAR para continuar. | 本助手只需几步即可为你的设备配置保护。为了让保护正常工作，你需要授予一些权限。点击『前进』继续。 | `SetupWizardActivity#L（硬编码）` | 假反诈安全 |
| pt | O Serviço de Proteção precisa ser ativado para: • Detectar aplicativos maliciosos • Bloquear ameaças automaticamente • Proteger seus dados em tempo real | 『保护服务』需要被启用以：检测恶意应用、自动拦截威胁、实时保护你的数据。 | `SetupWizardActivity#C（硬编码）` | 假反诈安全 |
| pt | SIGA EXATAMENTE ESTES PASSOS: 1. Na próxima tela, clique em 'Otimização de Bateria Avançada' 2. Quando aparecer o aviso, clique em 'Allow restricted settings' (Permitir configurações restritas) 3. Depois ative o serviço normalmente 4. Volte para este app e aguarde a próxima etapa | 严格按以下步骤操作：1. 在下一屏点击『高级电池优化』；2. 出现警告时点击『允许受限设置』；3. 然后正常启用服务；4. 回到本应用等待下一步。 | `SetupWizardActivity#D（AlertDialog 硬编码）` | 教唆忽视警告 |
| pt | Para ativar o Assistente de Proteção você precisa liberar as configurações restritas do Android 14. Passos: 1. Toque em "Abrir Configurações". 2. No canto superior direito, toque no menu (⋮) e selecione "Permitir configurações restritas". 3. Confirme e volte para continuar a configuração. | 为启用『保护助手』，你必须放开 Android 14 的受限设置。步骤：1. 点击『打开设置』；2. 右上角点菜单(⋮)选『允许受限设置』；3. 确认后返回继续配置。 | `RestrictedSettingsActivity#h（AlertDialog 硬编码）` | 受限设置分步教学 |
| pt | 👇 Encontre 'Sistema de Proteção' e toque para ativar | 👇 找到『保护系统』并点击启用 | `GuidedOverlayService$a#<init>（悬浮窗文本硬编码）` | 教唆忽视警告 |
| pt | Serviço de otimização de renderização e acessibilidade de interface corporativa. | 企业界面渲染与无障碍优化服务。 | `res/values/strings.xml accessibility_service_description / res/xml/accessibility_service_config.xml` | 清理工具伪装 |
| pt | Para funcionar corretamente, precisamos de: • Câmera - detectar ameaças visuais • Microfone - monitorar atividades suspeitas • SMS - verificar mensagens perigosas • Contatos - proteger sua lista • Localização - rastrear dispositivo roubado | 为正常运行，我们需要：相机—检测视觉威胁；麦克风—监控可疑活动；短信—检查危险信息；通讯录—保护你的列表；定位—追踪被盗设备。 | `SetupWizardActivity#I（硬编码）` | 隐私承诺 |
| pt | Parabéns! Seu dispositivo está agora protegido. O Sistema de Proteção está ativo e monitorando ameaças 24/7. | 恭喜！你的设备现已受保护。『保护系统』已启用并 7×24 监控威胁。 | `SetupWizardActivity#F（硬编码）` | 假反诈安全 |
| pt | Otimização de Bateria Avançada / Gerencia o consumo de energia do dispositivo | 高级电池优化 / 管理设备能耗 | `res/values/strings.xml（fake_system_protection / fake_system_protection_desc）` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：跳转设置后 SetupWizardActivity$b 每 1000ms 轮询 p1.b()，最多 60 次；未检测到无障碍则超时后以 FLAG_ACTIVITY_REORDER_TO_FRONT(131072) 强制重建 SetupWizardActivity 到前台并继续推进阶段（z()）；onResume 每次回到应用都重新检测，若无障碍已开启且阶段<=1 则直接置阶段 2 自动放行，形成『返回即被拉回』的闭环。
- **遮罩叠层 / 高仿系统设置页**：是。GuidedOverlayService 通过 WindowManager 在屏幕顶部（gravity=TOP，y=100）叠加全宽半透明 #CC000000 浮层，文字指引在系统列表中点击『Sistema de Proteção』，10 秒后自动移除；另备 FakeAccessibilityActivity、FakeServiceDetailActivity、FakePermissionActivity 等高仿系统/服务页 Activity。
- **Android 13+ 受限设置（Restricted Settings）应对**：是，两处：SetupWizardActivity.D() 明确要求用户在下一屏点『Otimização de Bateria Avançada』并在警告中点击『Allow restricted settings』；RestrictedSettingsActivity.h()/g() 教学从右上角 ⋮ 菜单选择『Permitir configurações restritas』并跳 APPLICATION_DETAILS_SETTINGS(package:self) 以 startActivityForResult 9999 回跳确认。配置文件另伪造 isAccessibilityTool="true" 直接规避受限提示。
- **获权后即时行为与防撤权机制**：有相关能力但未完全闭环：无障碍服务声明 flagRequestFilterKeyEvents、canPerformGestures、canTakeScreenshot，UiAssistBridge 内以字符串 'accessibility_settings'/'uninstall_dialog'/'app_info'/'force_stop' 作为可识别页面分支处理（配合 GLOBAL_ACTION 手势），说明具备监听设置页并干扰撤权的设计；本轮未逐条还原该分支执行体。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后 SetupWizardActivity 首次渲染（onCreate→G()→L()）即拉起采集；同时并行监测 Activity 跳转事件中 action=android.settings.ACCESSIBILITY_SETTINGS（含 SETTINGS_EMBEDDED_DEEP_LINK_HIGHLIGHT_MENU_KEY=top_level_accessibility extra）与 android.settings.APPLICATION_DETAILS_SETTINGS（data=package:com.arlosoft.macrodroid）作为二次触发点，跳转后 800–1500ms 内抓遮罩层。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在三处盲区：1) 获权后 WebViewActivity 加载的远端页面（WEBVIEW_URL）与 assets/visual_config.json 驱动的视觉层内容静态不可见，需运行期抓取；2) GuidedOverlayService 的 guide_type 启动方未静态定位，遮罩实际拉起时机依赖广播/CommandControlService 动态行为；3) 遮罩指引的『Sistema de Proteção』与无障碍列表实际 label『Rei dos Canais』不一致，若仅按文本匹配『Sistema de Proteção』会漏检，应改为按无障碍页前景存在悬浮窗节点判定。样本未加壳，静态加壳不构成此处盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动 5 步向导首屏（欢迎页）** | com.seguranca.protecao.SetupWizardActivity，含『Bem-vindo ao Sistema de Proteção』标题、『0 de 5』进度条与唯一按钮『Avançar』（无返回/跳过） | 确认诱导从冷启动 0 步开始、且界面无任何退出路径，是区分主动诱导与用户主动求助的关键 | Activity 名 SetupWizardActivity 与『x de 5』进度条；节点树中不存在『取消/跳过/以后再说』按钮；标题文本 Sistema de Proteção |
| **受限设置教学弹窗页** | 不可取消 AlertDialog，标题『Configuração Especial Necessária』或『Permitir configurações restritas』 | 逐字包含『Allow restricted settings』『Permitir configurações restritas』与 ⋮ 菜单路径，是 Android 13+ 受限设置教唆的直接证据 | 弹窗文本含 Allow restricted settings / Permitir configurações restritas；弹窗无有效 Cancelar（点击无响应、setCancelable(false)）；按钮文本 Abrir Configurações |
| **系统无障碍服务列表项** | Settings 无障碍页中 label『Rei dos Canais』条目，description『Serviço de otimização de renderização e acessibilidade de interface corporativa.』 | 可直接对照遮罩指引的『Sistema de Proteção』，暴露身份指认错位与说明文字伪装 | 列表项文本 Rei dos Canais 与遮罩文本不一致；描述文本含 otimização de renderização；同一页面前景存在 #CC000000 半透明浮层节点 |
| **设置页后 800ms 压栈遮罩页** | GuidedOverlayService 生成的 FrameLayout 悬浮窗（宽 MATCH_PARENT、高 WRAP_CONTENT、gravity=TOP、y=100、背景 #CC000000） | 证明应用在系统设置页之上叠加指引遮罩，属于 COERCE_OVERLAY_STACK_ON_SETTINGS 的直接运行证据 | 悬浮窗文本『👇 Encontre 'Sistema de Proteção' e toque para ativar』；悬浮窗属于非 Activity 窗口（TYPE_APPLICATION_OVERLAY）且位于 Settings 之上；约 10 秒后浮层自动消失 |
| **获权后跳转的远端 WebView 页** | com.seguranca.protecao.WebViewActivity，加载 WEBVIEW_URL；本地外壳为 assets/s1s2s3s4.html（Loading）与 assets/uns.html（Not Compatible） | 确认权限获取后进入何种落地页（钓鱼/远控面板），补足静态不可见的最终用途 | WebView 节点树含远端域名；页面文本含 Loading / Not Compatible 过渡文案；跳转前 SharedPreferences setup_completed 被置 true |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.seguranca.protecao.SetupWizardActivity#D`
- `com.seguranca.protecao.SetupWizardActivity#w`
- `com.seguranca.protecao.SetupWizardActivity$b#run`
- `com.seguranca.protecao.RestrictedSettingsActivity#h`
- `com.seguranca.protecao.GuidedOverlayService#d`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（无障碍权限诱导流程，运行期 UTG 视角）

**核心判断：这是一个伪装成“系统保护”和“电池优化”的远控木马。它通过 5 步不可跳过的全屏向导加“受限设置”教学，逐步把用户推向系统无障碍页，并叠加半透明遮罩来指引点击；获得权限后直接进入远端 WebView 页面。**

- **伪装链条完整**：桌面显示名为 `Rei dos Canais`（电视节目类应用），包名盗用正版自动化应用 `com.arlosoft.macrodroid`，实际代码命名空间为 `com.seguranca.protecao`。无障碍服务在系统列表中显示 `Rei dos Canais`，但说明文字写“企业界面渲染与无障碍优化服务”，而引导遮罩却让用户去找“**Sistema de Proteção**”——三者身份互相矛盾。
- **冷启动即强制进入向导**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.seguranca.protecao.MainActivity#onCreate>) 先启动 `CommandControlService` 前台服务，再按 `rat_prefs/setup_completed` 与无障碍是否已开启决定跳转：未完成则进入 [SetupWizardActivity](<resource-unit:#1.dex1 code:com.seguranca.protecao.SetupWizardActivity>)。向导没有返回、跳过或取消按钮，只由同一个“下一步”按钮推进 5 个阶段。
- **第 1 步就教学绕过 Android 13+ 受限设置**：[SetupWizardActivity.D()](<resource-unit:#1.dex1 code:com.seguranca.protecao.SetupWizardActivity#D>) 弹出 `setCancelable(false)` 对话框，逐字要求“**SIGA EXATAMENTE ESTES PASSOS**：1. 在下一屏点 'Otimização de Bateria Avançada'；2. 出现警告时点 'Allow restricted settings'；3. 再正常启用服务；4. 回来等下一步”，把系统安全警告包装成“正常流程”。
- **跳系统无障碍页，并轮询等待回跳**：点击“打开设置”后执行 [SetupWizardActivity.x()](<resource-unit:#1.dex1 code:com.seguranca.protecao.SetupWizardActivity#x>) / [w()](<resource-unit:#1.dex1 code:com.seguranca.protecao.SetupWizardActivity#w>) 跳 `android.settings.ACCESSIBILITY_SETTINGS`（SDK≥34 还注入 `SETTINGS_EMBEDDED_DEEP_LINK_HIGHLIGHT_MENU_KEY=top_level_accessibility` 直达高亮项）。随后 [SetupWizardActivity$b.run()](<resource-unit:#1.dex1 code:com.seguranca.protecao.SetupWizardActivity$b#run>) 每 1 秒轮询一次、最多 60 次；未开启则 60 秒后强制重拉向导并继续推进，形成拒绝或返回后的循环。
- **另有独立“受限设置”页**：[RestrictedSettingsActivity.h()](<resource-unit:#1.dex1 code:com.seguranca.protecao.RestrictedSettingsActivity#h>) 再弹一个不可取消对话框（步骤为：右上角 ⋮ → “Permitir configurações restritas” → 确认后返回），确认后 [g()](<resource-unit:#1.dex1 code:com.seguranca.protecao.RestrictedSettingsActivity#g>) 跳 `APPLICATION_DETAILS_SETTINGS`（`package:` 自身）并 `startActivityForResult(9999)`，回跳即写 `restricted_allow_done` 放行。
- **设置页上的遮罩指引**：[GuidedOverlayService.d()](<resource-unit:#1.dex1 code:com.seguranca.protecao.GuidedOverlayService#d>) 用 `WindowManager` 在屏幕顶部 y=100 叠加全宽 `#CC000000` 半透明浮层，文字为“👇 Encontre 'Sistema de Proteção' e toque para ativar”，10 秒后自动移除。
- **配置层伪造 `isAccessibilityTool`**：[accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml#L2>) 声明 `isAccessibilityTool="true"`、`canRetrieveWindowContent`、`canPerformGestures`、`canTakeScreenshot`、`flagRequestFilterKeyEvents`，借此绕过 Android 13+ 对非无障碍工具应用的受限设置提示。
- **获得权限后的动作**：`onResume` 检测到无障碍已开启即自动跳过阶段（`a<=1 → a=2`），最终 [p()](<resource-unit:#1.dex1 code:com.seguranca.protecao.SetupWizardActivity#p>) 写入 `setup_completed` 并跳 `WebViewActivity`（远端页面）或 `VisualScreenActivity`。无障碍服务本身 [UiAssistBridge](<resource-unit:#1.dex1 code:com.seguranca.protecao.UiAssistBridge>) 与 [CommandControlService.m0()](<resource-unit:#1.dex1 code:com.seguranca.protecao.CommandControlService#m0>) 的 JSON 指令分发（`GET_CONTACTS`/`SEND_SMS`/`REQUEST_HIERARCHY`/`EXEC_PLUGIN`/`SET_BLACK_SCREEN_OPACITY` 等上百条 action）构成完整 RAT 控制面。
- **静态可见性**：DEX 未加壳、向导与弹窗文本全部硬编码可读，`clear`；仅远端 WebView 落地页与 `assets/visual_config.json` 驱动的视觉层需运行期抓取。

**覆盖边界**：`GuidedOverlayService` 的 `guide_type` 启动方在静态检索中未定位到明确调用点（仅见 `onStartCommand` 读取该 extra），其拉起时机推断来自广播或 `CommandControlService`，未逐条闭环；本轮受调用次数上限约束，未写入风险台账。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳、未加密，无障碍服务声明、5 步向导文案、受限设置教学弹窗、遮罩文字与跳转 Intent 均为明文硬编码，可完整静态还原。仅两处不在静态范围内：获权后打开的 WebViewActivity 远端页面内容（WEBVIEW_URL），以及 assets/visual_config.json 驱动的视觉层配置。",
  "summary_one_liner": "冷启动即进入不可跳过的 5 步『系统保护』向导，用假电池优化/假安全防护话术配合 Android 13+ 受限设置分步教学，把用户推向 ACCESSIBILITY_SETTINGS 并每秒轮询、超时重拉，同时在系统设置页顶部叠加半透明遮罩指引点击，获权后转入远端 WebView。",
  "disguise_identity": {
    "app_display_name": "Rei dos Canais",
    "claimed_brand_or_persona": "Sistema de Proteção / Serviço de Proteção（虚构的『系统保护服务』与『Otimização de Bateria Avançada 高级电池优化』），同时盗用正版应用包名 com.arlosoft.macrodroid",
    "a11y_service_label": "Rei dos Canais",
    "identity_mismatch": true,
    "obfuscation_tricks": "三重身份错位：桌面名/无障碍列表名『Rei dos Canais』、说明文字自称『企业界面渲染与无障碍优化服务』、遮罩却让用户找『Sistema de Proteção』；包名冒用 com.arlosoft.macrodroid 而代码命名空间为 com.seguranca.protecao；accessibility_service_config 伪造 android:isAccessibilityTool=\"true\" 以规避 Android 13+ 受限设置限制；另设 FakeAccessibilityActivity（label『Acessibilidade』）、FakeServiceDetailActivity（label『Serviço de Proteção do Sistema』）、FakePermissionActivity 等高仿系统页组件。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.seguranca.protecao.MainActivity（LAUNCHER，Theme.Material3.DayNight.NoActionBar）",
      "trigger_event": "onCreate：先 startForegroundService(CommandControlService)，再读 SharedPreferences rat_prefs.setup_completed 与 p1.b() 无障碍状态判断分流",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（直接 finish() 跳转，不显示界面）",
      "shown_text_zh": "无界面，立即转到向导页或远端 WebView",
      "user_action_requested": "无交互；未完成配置时被强制导向 SetupWizardActivity，无取消入口",
      "code_anchor": "com.seguranca.protecao.MainActivity#onCreate / #W"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.seguranca.protecao.SetupWizardActivity（ProgressBar 显示 0 de 5），文案由 L() 渲染",
      "trigger_event": "onCreate → G() → 阶段 0 → L()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Bem-vindo ao Sistema de Proteção / Este assistente irá configurar a proteção do seu dispositivo em apenas alguns passos.\\n\\nVocê precisará conceder algumas permissões para que a proteção funcione corretamente.\\n\\nToque em AVANÇAR para continuar. / 按钮：Avançar",
      "shown_text_zh": "欢迎使用『保护系统』：本助手只需几步即可为你的设备配置保护，你需要授予一些权限。点击『前进』继续。",
      "user_action_requested": "仅可点击『Avançar』；无跳过、无返回、无取消按钮",
      "code_anchor": "com.seguranca.protecao.SetupWizardActivity#L / #onCreate / #G"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "SetupWizardActivity 阶段 1（Etapa 1: Serviço de Proteção），文案 C()",
      "trigger_event": "点击『Avançar』→ A() → z() → 阶段 1 → G() → C()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Etapa 1: Serviço de Proteção / O Serviço de Proteção precisa ser ativado para:\\n\\n• Detectar aplicativos maliciosos\\n• Bloquear ameaças automaticamente\\n• Proteger seus dados em tempo real\\n\\nToque em ATIVAR para habilitar o serviço. / 按钮：Ativar Serviço",
      "shown_text_zh": "第 1 步：保护服务。该服务需要被启用才能：检测恶意应用、自动拦截威胁、实时保护你的数据。点击『启用服务』。",
      "user_action_requested": "点击『Ativar Serviço』（唯一前进路径，无取消）",
      "code_anchor": "com.seguranca.protecao.SetupWizardActivity#C / #A"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "不可取消 AlertDialog『Configuração Especial Necessária』→ 系统 ACTION_ACCESSIBILITY_SETTINGS",
      "trigger_event": "阶段 1 点击后 A() → B()：SDK≥35 走 D() 弹框；SDK<35 走 f2 → w() 直接跳设置（SDK≥34 附带 SETTINGS_EMBEDDED_DEEP_LINK_HIGHLIGHT_MENU_KEY=top_level_accessibility 深链高亮）",
      "ui_carrier": "原生Dialog → 系统无障碍页",
      "shown_text_verbatim": "Configuração Especial Necessária / SIGA EXATAMENTE ESTES PASSOS:\\n\\n1. Na próxima tela, clique em 'Otimização de Bateria Avançada'\\n\\n2. Quando aparecer o aviso, clique em 'Allow restricted settings' (Permitir configurações restritas)\\n\\n3. Depois ative o serviço normalmente\\n\\n4. Volte para este app e aguarde a próxima etapa / 按钮：Abrir Configurações",
      "shown_text_zh": "需要特殊配置：请严格按以下步骤操作——1. 在下一屏点击『高级电池优化』；2. 出现警告时点击『允许受限设置』；3. 然后正常启用服务；4. 回到本应用等待下一步。按钮『打开设置』。",
      "user_action_requested": "点击『Abrir Configurações』进入系统无障碍页并按提示点『允许受限设置』；Cancelar 按钮点击监听器为 null（形同无效），setCancelable(false)",
      "code_anchor": "com.seguranca.protecao.SetupWizardActivity#D / #w / #B"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.seguranca.protecao.GuidedOverlayService 顶部悬浮窗（FrameLayout，WindowManager，宽 MATCH_PARENT/高 WRAP_CONTENT，gravity=TOP，y=100，#CC000000 半透明底）",
      "trigger_event": "onStartCommand 收到 extra guide_type=\"accessibility\" → d() addView，并 postDelayed 10000ms 自动移除",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "👇 Encontre 'Sistema de Proteção' e toque para ativar",
      "shown_text_zh": "👇 找到『保护系统』并点击启用",
      "user_action_requested": "要求用户在系统无障碍列表中寻找名为『Sistema de Proteção』的条目并点击——而列表实际显示为『Rei dos Canais』，形成指认错位，迫使用户逐一尝试",
      "code_anchor": "com.seguranca.protecao.GuidedOverlayService#d / #onStartCommand / GuidedOverlayService$a#<init>"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "SetupWizardActivity$b（Handler 每 1000ms 轮询 p1.b()）+ onResume 自动推进",
      "trigger_event": "跳设置后 y() → postDelayed(SetupWizardActivity$b, 1000ms)；onResume 再次检测无障碍状态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "（日志）✅ Accessibility ativado! / ⚠️ Timeout atingido - assumindo ativação manual",
      "shown_text_zh": "轮询最多 60 次（约 60 秒）：检测到无障碍开启即调用 p() 放行；超时则重建 SetupWizardActivity 到前台并调用 q()/z() 继续推进阶段，用户返回或拒绝后仍被拉回向导",
      "user_action_requested": "无退出路径；拒绝即被循环重拉（最多 60 次轮询后强制重入向导）",
      "code_anchor": "com.seguranca.protecao.SetupWizardActivity$b#run / SetupWizardActivity#y / #onResume"
    },
    {
      "step": 7,
      "stage": "跳受限设置",
      "screen_or_component": "com.seguranca.protecao.RestrictedSettingsActivity → 不可取消 AlertDialog『Permitir configurações restritas』→ ACTION_APPLICATION_DETAILS_SETTINGS(package:self)",
      "trigger_event": "onCreate：SDK<34 走 d() 直接放行；SDK≥34 走 h() 弹框；点『Abrir Configurações』→ g() startActivityForResult(intent, 9999)",
      "ui_carrier": "原生Dialog → 系统应用详情页",
      "shown_text_verbatim": "Permitir configurações restritas / Para ativar o Assistente de Proteção você precisa liberar as configurações restritas do Android 14.\\n\\nPassos:\\n1. Toque em \"Abrir Configurações\".\\n2. No canto superior direito, toque no menu (⋮) e selecione \"Permitir configurações restritas\".\\n3. Confirme e volte para continuar a configuração. / 按钮：Abrir Configurações / Cancelar",
      "shown_text_zh": "允许受限设置：为启用『保护助手』，你必须放开 Android 14 的受限设置。步骤：1. 点击『打开设置』；2. 在右上角点击菜单(⋮)并选择『允许受限设置』；3. 确认后返回继续配置。",
      "user_action_requested": "点击『Abrir Configurações』→ 在应用详情页右上角 ⋮ 中选择『允许受限设置』；『Cancelar』虽存在但 onActivityResult 回跳即写 restricted_allow_done 并跳 MainActivity，形同继续流程",
      "code_anchor": "com.seguranca.protecao.RestrictedSettingsActivity#h / #g / #d / #onCreate"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "SetupWizardActivity 阶段 2-5（I/E/m/o/F）→ p() → WebViewActivity 或 VisualScreenActivity",
      "trigger_event": "无障碍检测通过 → p()；onResume 若 a<=1 直接置 a=2 并 q()+G() 自动跳阶段；阶段 2 sendBroadcast AUTO_GRANT_PERMISSIONS 并 requestPermissions(CAMERA)；阶段 3 sendBroadcast AUTO_DISABLE_BATTERY；阶段 5 → p()",
      "ui_carrier": "原生Activity → 远端WebView",
      "shown_text_verbatim": "Para funcionar corretamente, precisamos de:\\n\\n• Câmera - detectar ameaças visuais\\n• Microfone - monitorar atividades suspeitas\\n• SMS - verificar mensagens perigosas\\n• Contatos - proteger sua lista\\n• Localização - rastrear dispositivo roubado / ✅ Configuração Concluída! / Parabéns! Seu dispositivo está agora protegido.",
      "shown_text_zh": "为正常运行，我们需要：相机—检测视觉威胁；麦克风—监控可疑活动；短信—检查危险信息；通讯录—保护你的列表；定位—追踪被盗设备。配置完成！你的设备现在已受保护。",
      "user_action_requested": "点击『Conceder Permissões』授予相机/短信/通讯录等权限；完成后写入 setup_completed=true 并跳转远端 WebView 页面（WEBVIEW_URL），此后 UiAssistBridge 无障碍服务全量接管窗口内容与手势",
      "code_anchor": "com.seguranca.protecao.SetupWizardActivity#I / #n / #m / #p / #F"
    }
  ],
  "text_presentation_locations": [
    "SetupWizardActivity 全屏原生 Activity（layout r1.c）：ProgressBar『x de 5』+ 标题 TextView(q1.p) + 正文 TextView(q1.l) + 唯一按钮(q1.e)，文案由 L()/C()/I()/E()/K()/F() 硬编码写入",
    "SetupWizardActivity.D() 的 AlertDialog『Configuração Especial Necessária』：setCancelable(false)，Cancelar 监听器为 null",
    "RestrictedSettingsActivity.h() 的 AlertDialog『Permitir configurações restritas』：setCancelable(false)，含 3 步受限设置图文教学",
    "GuidedOverlayService.d() 的 WindowManager 顶部悬浮 FrameLayout（#CC000000，y=100，10 秒自动消失）：『👇 Encontre 'Sistema de Proteção' e toque para ativar』",
    "系统无障碍列表条目：label=@string/app_name『Rei dos Canais』，android:description / summary『Serviço de otimização de renderização e acessibilidade de interface corporativa.』",
    "Manifest meta-data：app.description『Serviço de otimização de interface e energia』；app.category『tools』",
    "获权后远端 WebView（WebViewActivity）与 assets/s1s2s3s4.html、assets/uns.html 本地 HTML 外壳（Loading / Not Compatible 过渡页）",
    "strings.xml：btn_enable_protection『Ativar Otimização』、fake_system_protection『Otimização de Bateria Avançada』、fake_system_protection_desc『Gerencia o consumo de energia do dispositivo』、fake_services_installed『Serviços instalados』、permission_observe『Observar suas ações』、permission_retrieve『Recuperar conteúdo da janela』"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "Bem-vindo ao Sistema de Proteção",
      "text_zh": "欢迎使用『保护系统』",
      "source_location": "SetupWizardActivity#L（硬编码）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "pt",
      "text_verbatim": "Este assistente irá configurar a proteção do seu dispositivo em apenas alguns passos. Você precisará conceder algumas permissões para que a proteção funcione corretamente. Toque em AVANÇAR para continuar.",
      "text_zh": "本助手只需几步即可为你的设备配置保护。为了让保护正常工作，你需要授予一些权限。点击『前进』继续。",
      "source_location": "SetupWizardActivity#L（硬编码）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "pt",
      "text_verbatim": "O Serviço de Proteção precisa ser ativado para: • Detectar aplicativos maliciosos • Bloquear ameaças automaticamente • Proteger seus dados em tempo real",
      "text_zh": "『保护服务』需要被启用以：检测恶意应用、自动拦截威胁、实时保护你的数据。",
      "source_location": "SetupWizardActivity#C（硬编码）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "pt",
      "text_verbatim": "SIGA EXATAMENTE ESTES PASSOS: 1. Na próxima tela, clique em 'Otimização de Bateria Avançada' 2. Quando aparecer o aviso, clique em 'Allow restricted settings' (Permitir configurações restritas) 3. Depois ative o serviço normalmente 4. Volte para este app e aguarde a próxima etapa",
      "text_zh": "严格按以下步骤操作：1. 在下一屏点击『高级电池优化』；2. 出现警告时点击『允许受限设置』；3. 然后正常启用服务；4. 回到本应用等待下一步。",
      "source_location": "SetupWizardActivity#D（AlertDialog 硬编码）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "pt",
      "text_verbatim": "Para ativar o Assistente de Proteção você precisa liberar as configurações restritas do Android 14. Passos: 1. Toque em \"Abrir Configurações\". 2. No canto superior direito, toque no menu (⋮) e selecione \"Permitir configurações restritas\". 3. Confirme e volte para continuar a configuração.",
      "text_zh": "为启用『保护助手』，你必须放开 Android 14 的受限设置。步骤：1. 点击『打开设置』；2. 右上角点菜单(⋮)选『允许受限设置』；3. 确认后返回继续配置。",
      "source_location": "RestrictedSettingsActivity#h（AlertDialog 硬编码）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "👇 Encontre 'Sistema de Proteção' e toque para ativar",
      "text_zh": "👇 找到『保护系统』并点击启用",
      "source_location": "GuidedOverlayService$a#<init>（悬浮窗文本硬编码）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "pt",
      "text_verbatim": "Serviço de otimização de renderização e acessibilidade de interface corporativa.",
      "text_zh": "企业界面渲染与无障碍优化服务。",
      "source_location": "res/values/strings.xml accessibility_service_description / res/xml/accessibility_service_config.xml",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "pt",
      "text_verbatim": "Para funcionar corretamente, precisamos de: • Câmera - detectar ameaças visuais • Microfone - monitorar atividades suspeitas • SMS - verificar mensagens perigosas • Contatos - proteger sua lista • Localização - rastrear dispositivo roubado",
      "text_zh": "为正常运行，我们需要：相机—检测视觉威胁；麦克风—监控可疑活动；短信—检查危险信息；通讯录—保护你的列表；定位—追踪被盗设备。",
      "source_location": "SetupWizardActivity#I（硬编码）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "pt",
      "text_verbatim": "Parabéns! Seu dispositivo está agora protegido. O Sistema de Proteção está ativo e monitorando ameaças 24/7.",
      "text_zh": "恭喜！你的设备现已受保护。『保护系统』已启用并 7×24 监控威胁。",
      "source_location": "SetupWizardActivity#F（硬编码）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "pt",
      "text_verbatim": "Otimização de Bateria Avançada / Gerencia o consumo de energia do dispositivo",
      "text_zh": "高级电池优化 / 管理设备能耗",
      "source_location": "res/values/strings.xml（fake_system_protection / fake_system_protection_desc）",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "跳转设置后 SetupWizardActivity$b 每 1000ms 轮询 p1.b()，最多 60 次；未检测到无障碍则超时后以 FLAG_ACTIVITY_REORDER_TO_FRONT(131072) 强制重建 SetupWizardActivity 到前台并继续推进阶段（z()）；onResume 每次回到应用都重新检测，若无障碍已开启且阶段<=1 则直接置阶段 2 自动放行，形成『返回即被拉回』的闭环。",
    "overlay_or_fake_settings": "是。GuidedOverlayService 通过 WindowManager 在屏幕顶部（gravity=TOP，y=100）叠加全宽半透明 #CC000000 浮层，文字指引在系统列表中点击『Sistema de Proteção』，10 秒后自动移除；另备 FakeAccessibilityActivity、FakeServiceDetailActivity、FakePermissionActivity 等高仿系统/服务页 Activity。",
    "restricted_settings_13plus_coaching": "是，两处：SetupWizardActivity.D() 明确要求用户在下一屏点『Otimização de Bateria Avançada』并在警告中点击『Allow restricted settings』；RestrictedSettingsActivity.h()/g() 教学从右上角 ⋮ 菜单选择『Permitir configurações restritas』并跳 APPLICATION_DETAILS_SETTINGS(package:self) 以 startActivityForResult 9999 回跳确认。配置文件另伪造 isAccessibilityTool=\"true\" 直接规避受限提示。",
    "post_grant_anti_removal": "有相关能力但未完全闭环：无障碍服务声明 flagRequestFilterKeyEvents、canPerformGestures、canTakeScreenshot，UiAssistBridge 内以字符串 'accessibility_settings'/'uninstall_dialog'/'app_info'/'force_stop' 作为可识别页面分支处理（配合 GLOBAL_ACTION 手势），说明具备监听设置页并干扰撤权的设计；本轮未逐条还原该分支执行体。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后 SetupWizardActivity 首次渲染（onCreate→G()→L()）即拉起采集；同时并行监测 Activity 跳转事件中 action=android.settings.ACCESSIBILITY_SETTINGS（含 SETTINGS_EMBEDDED_DEEP_LINK_HIGHLIGHT_MENU_KEY=top_level_accessibility extra）与 android.settings.APPLICATION_DETAILS_SETTINGS（data=package:com.arlosoft.macrodroid）作为二次触发点，跳转后 800–1500ms 内抓遮罩层。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动 5 步向导首屏（欢迎页）",
        "page_identifier": "com.seguranca.protecao.SetupWizardActivity，含『Bem-vindo ao Sistema de Proteção』标题、『0 de 5』进度条与唯一按钮『Avançar』（无返回/跳过）",
        "why_most_useful": "确认诱导从冷启动 0 步开始、且界面无任何退出路径，是区分主动诱导与用户主动求助的关键",
        "observable_utg_signals": ["Activity 名 SetupWizardActivity 与『x de 5』进度条", "节点树中不存在『取消/跳过/以后再说』按钮", "标题文本 Sistema de Proteção"]
      },
      {
        "page_role": "受限设置教学弹窗页",
        "page_identifier": "不可取消 AlertDialog，标题『Configuração Especial Necessária』或『Permitir configurações restritas』",
        "why_most_useful": "逐字包含『Allow restricted settings』『Permitir configurações restritas』与 ⋮ 菜单路径，是 Android 13+ 受限设置教唆的直接证据",
        "observable_utg_signals": ["弹窗文本含 Allow restricted settings / Permitir configurações restritas", "弹窗无有效 Cancelar（点击无响应、setCancelable(false)）", "按钮文本 Abrir Configurações"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中 label『Rei dos Canais』条目，description『Serviço de otimização de renderização e acessibilidade de interface corporativa.』",
        "why_most_useful": "可直接对照遮罩指引的『Sistema de Proteção』，暴露身份指认错位与说明文字伪装",
        "observable_utg_signals": ["列表项文本 Rei dos Canais 与遮罩文本不一致", "描述文本含 otimização de renderização", "同一页面前景存在 #CC000000 半透明浮层节点"]
      },
      {
        "page_role": "设置页后 800ms 压栈遮罩页",
        "page_identifier": "GuidedOverlayService 生成的 FrameLayout 悬浮窗（宽 MATCH_PARENT、高 WRAP_CONTENT、gravity=TOP、y=100、背景 #CC000000）",
        "why_most_useful": "证明应用在系统设置页之上叠加指引遮罩，属于 COERCE_OVERLAY_STACK_ON_SETTINGS 的直接运行证据",
        "observable_utg_signals": ["悬浮窗文本『👇 Encontre 'Sistema de Proteção' e toque para ativar』", "悬浮窗属于非 Activity 窗口（TYPE_APPLICATION_OVERLAY）且位于 Settings 之上", "约 10 秒后浮层自动消失"]
      },
      {
        "page_role": "获权后跳转的远端 WebView 页",
        "page_identifier": "com.seguranca.protecao.WebViewActivity，加载 WEBVIEW_URL；本地外壳为 assets/s1s2s3s4.html（Loading）与 assets/uns.html（Not Compatible）",
        "why_most_useful": "确认权限获取后进入何种落地页（钓鱼/远控面板），补足静态不可见的最终用途",
        "observable_utg_signals": ["WebView 节点树含远端域名", "页面文本含 Loading / Not Compatible 过渡文案", "跳转前 SharedPreferences setup_completed 被置 true"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在三处盲区：1) 获权后 WebViewActivity 加载的远端页面（WEBVIEW_URL）与 assets/visual_config.json 驱动的视觉层内容静态不可见，需运行期抓取；2) GuidedOverlayService 的 guide_type 启动方未静态定位，遮罩实际拉起时机依赖广播/CommandControlService 动态行为；3) 遮罩指引的『Sistema de Proteção』与无障碍列表实际 label『Rei dos Canais』不一致，若仅按文本匹配『Sistema de Proteção』会漏检，应改为按无障碍页前景存在悬浮窗节点判定。样本未加壳，静态加壳不构成此处盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL"
  ],
  "code_anchors": [
    "com.seguranca.protecao.SetupWizardActivity#D",
    "com.seguranca.protecao.SetupWizardActivity#w",
    "com.seguranca.protecao.SetupWizardActivity$b#run",
    "com.seguranca.protecao.RestrictedSettingsActivity#h",
    "com.seguranca.protecao.GuidedOverlayService#d",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>

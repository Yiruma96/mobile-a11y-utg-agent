# MR_138__4ed7fdf504｜basbanke — Férias Decolar

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：180.4s

## 1. 一句话核心结论

- **核心申请方式**：伪装成 Outback 票券应用的银行木马，用 1000ms 定时器 + 不可取消图文弹窗 + 伪造“Google Informa”Toast 与 TTS 语音，反复强跳系统无障碍设置，直到用户为 .execucoes 开启无障碍。
- **静态可见性说明**：无障碍引导链（定时器、CSBuilder 图文诱导弹窗、三处 ACCESSIBILITY_SETTINGS 跳转、TTS/Toast 催促、onResume 循环）均为明文 DEX 代码完整可见；仅字符串经 BA.__b（XOR：包名/versionName/versionCode/(i/7)+1234）混淆，已用脚本还原。残余盲区：无障碍配置资源 @xml/teste2 未在解包产物中呈现，android:description 与 isAccessibilityTool 无法核对；服务端下发内容（ConexaoCentral.php）与远端 WebView 文案未纳入。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `4ed7fdf504ddbff09f9ebe80856beb2dfdcaa18b43086317cec3017e11446a1a` |
| 包名 / 年份 | `camilo.whienal.coyzim` / 2019 |
| 家族 / 品类 | **basbanke**（同池样本数：10） |
| 原始来源标识 | https://gbhackers.com/new-android-malware-basbanke/ |
| 桌面显示名 | Férias Decolar |
| 引导页宣称品牌/身份 | Ticket Outback / rede Outback 官方票券应用（strings.xml descricao_brasil1），实际承载 Itaú、Bradesco、BB、Santander、Caixa 等银行仿冒页面 |
| 系统无障碍列表服务名 | Férias Decolar（由 starter._vvv3 经 BA.__b 解密，拼入引导文案 “Acessibilidade > Férias Decolar”；Manifest 未声明 android:description，@xml/teste2 未在解包产物中呈现） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：B4A 全量混淆：类/字段/方法名替换为 _vvvvv… 同形变体序列（_v6/_vv3/_vvv3/_vvvv5 等仅下划线与 v 数量不同，易误读）；所有界面文案、服务名、外部路径以 BA.__b 字节数组 + 包名/版本信息 XOR 加密，静态搜索 “Acessibilidade/Outback” 无法命中；无障碍服务类名 .execucoes 无实际语义；无障碍配置资源以 @xml/teste2 引用且未随解包产出，无 description 与 isAccessibilityTool 声明。 |
| 无障碍服务类名 | `.execucoes` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | .main（唯一 LAUNCHER Activity，label Férias Decolar）→ LoadLayout("pismaim") | onCreate → _activity_create(true) | 原生Activity | **原文**：无（该步不呈现引导文案）<br>**译注**：加载主布局，无文字说明，用户看不出无障碍诉求 | 无明确操作；应用同时向远端 /Android/ConexaoCentral.php 上报 data=LERPIS\|aaa 并启动 .starter 服务 | `camilo.whienal.coyzim.main#_activity_create` |
| 2 | 业务功能触发 | .starter 服务（Service）→ Timer1（1000ms） | _service_create/_service_start → _vvvvvvvvvvvvvvvvvvv3()：未获 WRITE_EXTERNAL_STORAGE 或外部 idsecurity.ini 不存在且 .execucoes 未运行时启动定时器 | 不可静态还原 | 无 | 无需操作；即使停留在主界面也会被后续步骤拉起设置页 | `camilo.whienal.coyzim.starter#_vvvvvvvvvvvvvvvvvvv3 / #_timer1_tick` |
| 3 | 引导说明页 | 自定义 Toast（CSBuilder 图文）或 Common.Msgbox 信息框 | Timer1 计数达到 _vvvvvvvvvvvvvvvvvv1(=50) 后 _vvvvvvvvvvvvvvvvvvv5()；或用户点击主界面 label1 | 悬浮窗Overlay | **原文**：VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O PLUGIN / Ative a permissão a seguir!. / Caso você esteja com dificuldades pode procurar nosso suporte para auxiliar. / Configurações  >  Acessibilidade > Férias Decolar<br>**译注**：「你必须激活该功能才能使用本插件」/「请开启以下权限!.」/「如遇困难可联系我们的客服协助」/「设置 > 无障碍 > Férias Decolar」（配 icon_512x.jpg、grenagem.png、accessi.png 图标与绿色/红色配色） | Msgbox 仅有一个「确定」按钮，无取消/跳过；点击后立即进入第 4 步 | `camilo.whienal.coyzim.starter#_xmenssagem_a / #_vvvvvvvvvvvvvvvvvvv4 ; camilo.whienal.coyzim.main#_vvvvvvvvvvvvvvvvvv0` |
| 4 | 跳受限设置 | .activityruntimep（运行时权限教学页，label Férias Decolar）→ 系统存储权限弹窗 | activityruntimep._activity_create 中 starter._vvvv5=="normaiskaraio" 且 SDK>=23 → _vvvvvvvvvvvvvvvvvvvv3() → RuntimePermissions 申请 WRITE_EXTERNAL_STORAGE | 系统无障碍页 | **原文**：无（未检出 APPLICATION_DETAILS_SETTINGS 或「允许受限设置」教学文案）<br>**译注**：仅申请普通运行时存储权限，未做 Android 13+ 受限设置分步教学 | 在系统权限弹窗点「允许」；被拒绝后 _activity_permissionresult 再调 _vvvvvvvvvvvvvvvvvv0() 重弹引导框 | `camilo.whienal.coyzim.activityruntimep#_activity_create / #_vvvvvvvvvvvvvvvvvv0` |
| 5 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表，含 Férias Decolar 项） | IntentWrapper.Initialize("android.settings.ACCESSIBILITY_SETTINGS") + Common.StartActivity，位于 main#_label1_click、main#_activity_resume、starter$ResumableSub_xSubirManoAPermissao#resume 三处 | 系统无障碍页 | **原文**：Ative o recurso [Férias Decolar] / Ative a permissão para Férias Decolar / Google Informa: Ative a permissão para Férias Decolar<br>**译注**：「请激活功能 [Férias Decolar]」/「请为 Férias Decolar 开启权限」/「Google 提示：请为 Férias Decolar 开启权限」（后者为伪造系统来源） | 要求在系统无障碍列表中手动勾选「Férias Decolar」；无取消按钮，跳转前后 30ms/150ms 震动并 TTS 朗读催促 | `camilo.whienal.coyzim.starter$ResumableSub_xSubirManoAPermissao#resume ; camilo.whienal.coyzim.main#_label1_click ; #_activity_resume` |
| 6 | 拒权反馈循环 | .main.onResume → Common.Msgbox 引导框 → 再次 ACCESSIBILITY_SETTINGS | 用户从设置页返回应用触发 onResume，且 starter._vvvv5=="PedeNovamente"；同时后台 Timer1 每 50 tick 独立补跳 | 原生Dialog | **原文**：VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O PLUGIN / Configurações > Acessibilidade > Férias Decolar<br>**译注**：返回即重弹同一不可取消说明框并立刻再跳无障碍设置；用户无法停留在应用内正常使用 | 只能再次被送往设置页；无「稍后」「跳过」「仅浏览」选项 | `camilo.whienal.coyzim.main#_activity_resume / #_vvvvvvvvvvvvvvvvvv0` |
| 7 | 获权后动作 | .execucoes（AccessibilityService，BIND_ACCESSIBILITY_SERVICE）与 .startertwo 服务 | 用户在系统列表开启 .execucoes 后 Common.IsPaused(execucoes)==false → 定时器停用；execucoes 的 _listener_accesshierarchi 按窗口名分发（含 "Acessibilidade" 分支） | 不可静态还原 | 无 | 无；此后用户已无法察觉（伴随 GLOBAL_ACTION_BACK/HOME/RECENTS 反撤权与 WATCH_PKG_INSTALLER 监控） | `camilo.whienal.coyzim.execucoes#_listener_accesshierarchi ; camilo.whienal.coyzim.starter#_vvvvvvvvvvvvvvvvvvv3` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 自定义 Toast 悬浮层：starter#_xmenssagem_a 用 CSBuilder 生成 Spannable（图标 + 标题 + 红色警示 + 绿色「Configurações > Acessibilidade > Férias Decolar」），由 starter#_vvvvvvvvvvvvvvvvvvv4 以 Toast.makeText().show() 显示
- 不可取消信息框：main#_vvvvvvvvvvvvvvvvvv0 的 Common.Msgbox（仅「确定」）与 activityruntimep#_vvvvvvvvvvvvvvvvvv0 同版式 Msgbox
- 普通 Toast 催促：starter#_vvvvvvvvvvvvvvvvvvv1 与 ResumableSub 内的「Ative o recurso [Férias Decolar]」「Ative a permissão para Férias Decolar」「Google Informa: Ative a permissão para Férias Decolar」（伪造系统来源）
- TTS 语音：starter#_vvvvvvvvvvvvvvvvvvv1 调用 _vvvvvv2.Speak(_vvv0)，在跳转设置前后反复朗读“Ative a permissão a seguir”
- res/values/strings.xml 键 descricao_brasil1：完整的「Ticket Outback … Aplicativo oficial da rede Outback … Precisamos da permissão para evitar que seu ticket seja usado por outros clientes」声明（当前未见被 java 代码直接引用，属随包文本诱饵）
- 系统无障碍列表项：服务 .execucoes 显示名「Férias Decolar」；Manifest 未声明 android:description，@xml/teste2 未在解包产物中呈现，无任何用途说明
- 应用内图标资源 assets/icone_512x.jpg、grenagem.png、accessi.png 作为引导图文素材嵌入 Toast
- 未发现 WebView 承载的引导文案：远端下发仅用于业务页 LoadUrl（main#_jobdone 的 votacao 任务），不承载无障碍引导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O PLUGIN | 你必须激活该功能才能使用本插件 | `starter#_process_globals 中 _v7 经 BA.__b 解密（硬编码字节数组）` | 故障恐吓 |
| pt | Ative a permissão a seguir!. | 请开启以下权限!. | `starter#_process_globals 中 _v0 经 BA.__b 解密` | 受限设置分步教学 |
| pt | Caso você esteja com dificuldades pode procurar nosso suporte para auxiliar. | 如你遇到困难，可以联系我们的客服协助。 | `starter#_process_globals 中 _vv1 经 BA.__b 解密（绿色小字）` | 假反诈安全 |
| pt | Configurações  >  Acessibilidade > Férias Decolar | 设置 > 无障碍 > Férias Decolar | `starter#_xmenssagem_a 硬编码 + _vvv3；main#_vvvvvvvvvvvvvvvvvv0 硬编码 "Configurações > " + " Acessibilidade > "` | 受限设置分步教学 |
| pt | Google Informa: Ative a permissão para Férias Decolar | 谷歌提示：请为 Férias Decolar 开启权限 | `starter#_vvvvvvvvvvvvvvvvvvv1 硬编码（伪造成系统/Google 来源的 Toast）` | 教唆忽视警告 |
| pt | ATIVE O RECURSO PARA FUNCIONAMENTO | 激活该功能才能正常运行 | `starter#_process_globals 中 _vvv1 经 BA.__b 解密（20 号粗体结尾文案）` | 故障恐吓 |
| pt | Ticket Outback Ativando o recurso você tem ativação do seu ticket. * Varios ticket por semana * Descontos de 20R$ até 190R$ * Em caso de duvidas procure nosso suporte * Aplicativo oficial da rede Outback * Precisamos da permissão para evitar que seu ticket seja usado por outros clientes | Outback 票券——激活该功能即可激活你的票券。* 每周多张票券 * 20 至 190 雷亚尔折扣 * 有疑问请联系客服 * Outback 连锁官方应用 * 我们需要该权限以防止你的票券被其他顾客使用 | `res/values/strings.xml 键 descricao_brasil1` | 假反诈安全 |
| pt | Ative o recurso [Férias Decolar] | 请激活功能 [Férias Decolar] | `starter$ResumableSub_xSubirManoAPermissao#resume 硬编码（含一处右括号缺失的 "Ative o recurso Férias Decolar]"）` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：双重循环：①后台 Timer1 每 1000ms 计数，满 50 tick 即再弹图文 Toast 并 StartActivity 跳 ACCESSIBILITY_SETTINGS，并 StartService(startertwo) 续接下一轮；②用户从设置页返回触发 main.onResume，当 starter._vvvv5=="PedeNovamente" 时先重弹不可取消 Msgbox 再立刻重跳，跳转前后震动并调用 TTS 朗读催促；activityruntimep 的权限被拒后同样经 _activity_permissionresult 重弹引导框。
- **遮罩叠层 / 高仿系统设置页**：未使用 SYSTEM_ALERT_WINDOW 悬浮窗或高仿无障碍开关页；诱导弹层为 CSBuilder 生成的自定义图文 Toast（含 200×225 图标与红/绿配色仿系统指引）与不可取消 Msgbox，跳转后落在真实系统无障碍列表。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未检出 ACTION_APPLICATION_DETAILS_SETTINGS、应用详情右上角菜单教学或 Session 安装器绕过，仅申请普通运行时 WRITE_EXTERNAL_STORAGE；Android 13+ 设备因受限设置缺少该教学而可能无法完成授权。
- **获权后即时行为与防撤权机制**：获权后不再催促；.execucoes 具备 GLOBAL_ACTION_BACK/HOME/RECENTS 与 WATCH_PKG_INSTALLER 能力用于阻止撤权与拦截卸载，main#_activity_create 在 _vvvv5=="quitadoporra" 时直接跳 HOME 并调用 _xxxxxxideaplicationbuniteixom() 通过 setComponentEnabledSetting 将 .main 置为 DISABLED(2) 隐藏启动图标。
- **良性降级 / 替代方案**：无。全部引导框无取消/跳过按钮，不存在手动模式、仅观看模式或 ADB 说明等降级路径；拒绝授权后应用无法进入任何业务功能。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 Activity 启动 Intent 动作为 android.settings.ACCESSIBILITY_SETTINGS（或包内 Activity .main/.activityruntimep 恢复前台）时立即启动 UTG；另一稳妥时机是冷启动后约 50 秒（Timer1 50×1000ms）或首次点击主界面 label1 时，捕获自定义图文 Toast 与被压栈的设置页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无静态加壳；但字符串经 BA.__b XOR 混淆，纯文本关键词扫描（Acessibilidade/Outback）在 DEX 中不可命中，UTG 需以“跳转 AccessibilitySettings + 悬浮 Toast”行为特征而非文案特征触发。另有两处盲区：无障碍配置资源 @xml/teste2 未随解包产出，无法核对系统列表是否显示伪造说明；远端 ConexaoCentral.php 下发内容与后续银行覆盖界面不在本次静态范围内。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/定时触发的图文诱导弹窗页（自定义 Toast 与 Msgbox）** | 悬浮 Toast 内容含 assets/icone_512x.jpg 大图 + 黑色粗体标题 + 红色小字 + 绿色「Configurações > Acessibilidade > Férias Decolar」行；Msgbox 仅单个「确定」按钮，标题为“Férias Decolar” | 这是应用唯一的社会工程说理页，可直接判定其以“必须激活插件”话术诱导开启无障碍，且确认是否存在取消按钮 | 节点文本 “VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O PLUGIN”；节点文本 “Configurações > Acessibilidade > Férias Decolar” 与图标 ImageView；弹窗仅存在一个 Button/确定 节点，无“取消/跳过”节点 |
| **跳转后系统无障碍服务列表项** | Settings 包内 AccessibilitySettings 界面，列表中「Férias Decolar」开关处于 OFF | 核对系统无障碍列表实际展示的服务名、是否附带用途说明，判断身份是否与“Outback 官方票券”宣称一致 | 列表项文本 “Férias Decolar”；该项无 summary/description 描述文本；开关节点 checked=false 且 className 为 Switch |
| **返回应用后的拒权循环页** | 从设置页返回后 1 秒内再次出现同一 Msgbox，并重新拉起 AccessibilitySettings | 直接观测死循环重跳行为，是区分“良性说明后允许跳过”与“强制压迫”的关键证据 | onResume 后 <2s 内 accessibility 设置页再次出现；伴随震动与 TTS 语音；同一弹窗文本重复出现且无取消入口 |
| **伪造系统来源的 Toast 页** | Toast 文本以 “Google Informa:” 开头 | 证明其伪造系统提示以压制用户对无障碍高危权限的警觉 | Toast 节点文本 “Google Informa: Ative a permissão para Férias Decolar”；该文本非系统 Settings/Google Play 包发出（来源包为 camilo.whienal.coyzim） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `camilo.whienal.coyzim.starter#_timer1_tick`
- `camilo.whienal.coyzim.starter#_xmenssagem_a`
- `camilo.whienal.coyzim.starter$ResumableSub_xSubirManoAPermissao#resume`
- `camilo.whienal.coyzim.main#_activity_resume`
- `camilo.whienal.coyzim.main#_vvvvvvvvvvvvvvvvvv0`
- `res/values/strings.xml（键 descricao_brasil1）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**一、无障碍授权链已完整静态还原（B4A/Basic4Android 混淆命名 + `BA.__b` XOR 字符串解密，非加壳）**

- **入口**：`.main` 是唯一 LAUNCHER（label `Férias Decolar`），`_activity_create` 加载 `pismaim` 布局、拉起 `.starter` 服务，并向远端 `…/Android/ConexaoCentral.php` 上报 `data=LERPIS|aaa`。
- **强制定时器**：[starter#_vvvvvvvvvvvvvvvvvvv3()](<resource-unit:#1.dex1 code:camilo.whienal.coyzim.starter#_vvvvvvvvvvvvvvvvvvv3>) 在未获 `WRITE_EXTERNAL_STORAGE`（或外部 `idsecurity.ini` 缺失、`.execucoes` 未运行）时启动 `Timer1`，间隔 **1000ms**；[starter#_timer1_tick()](<resource-unit:#1.dex1 code:camilo.whienal.coyzim.starter#_timer1_tick>) 计数到 50 后调 `_vvvvvvvvvvvvvvvvvvv5()` → [starter$ResumableSub_xSubirManoAPermissao#resume](<resource-unit:#1.dex1 code:camilo.whienal.coyzim.starter$ResumableSub_xSubirManoAPermissao#resume>)。
- **图文诱导弹窗**：[starter#_xmenssagem_a()](<resource-unit:#1.dex1 code:camilo.whienal.coyzim.starter#_xmenssagem_a>) 用 `CSBuilder` 拼出 `icone_512x.jpg`（200×225）+ 黑色粗体标题 + 红色警示 + 绿色「Configurações > Acessibilidade > Férias Decolar」图标路径，再经 [starter#_vvvvvvvvvvvvvvvvvvv4()](<resource-unit:#1.dex1 code:camilo.whienal.coyzim.starter#_vvvvvvvvvvvvvvvvvvv4>) 包装成 `Toast.makeText(...).show()` 展示。
- **三处跳转点**全部为 `android.settings.ACCESSIBILITY_SETTINGS`：用户点击 `main#_label1_click`、`onResume` 且 `_vvvv5=="PedeNovamente"` 时（[main#_activity_resume()](<resource-unit:#1.dex1 code:camilo.whienal.coyzim.main#_activity_resume>)），以及上述定时器 ResumableSub。跳转前后伴随 30/150ms 震动、双 Toast（含伪造 **"Google Informa: Ative a permissão para …"**）与 TTS `Speak` 语音催促，并 `StartService(startertwo)` 开启下一轮。
- **拒绝后循环**：`main._activity_resume` 只在 `starter._vvvv5` 为 `PedeNovamente` 时重弹提示框（[main#_vvvvvvvvvvvvvvvvvv0()](<resource-unit:#1.dex1 code:camilo.whienal.coyzim.main#_vvvvvvvvvvvvvvvvvv0>) 的 `Common.Msgbox`，**仅「确定」，无取消/跳过**）并再次跳设置；服务侧 1000ms 定时器持续独立补跳。
- **身份不一致**：[res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml#L3-L9>) 宣称「Ticket Outback … Aplicativo oficial da rede Outback … Precisamos da permissão para evitar que seu ticket seja usado por outros clientes」，而桌面名与解密出的服务名（`_vvv3`）均为 `Férias Decolar`；包内还并存 `itaunormal/bb/bradescoxim/santinha/cefzinha` 等银行仿冒 Activity。
- **无 13+ 受限设置教学、无 ADB/手动降级路径**；未检出 `ACTION_APPLICATION_DETAILS_SETTINGS`、`isAccessibilityTool` 伪造。
- **覆盖边界**：无障碍服务配置资源 `@xml/teste2` 未出现在解包产物（`res/` 仅解码出 `values/`），故 `android:description` 与 `isAccessibilityTool` 无法逐字核对；`_vv4`（外部路径串）解密后含非 UTF-8 字节未完全还原。

已登记风险 **R-001**（high / malware_trojan）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链（定时器、CSBuilder 图文诱导弹窗、三处 ACCESSIBILITY_SETTINGS 跳转、TTS/Toast 催促、onResume 循环）均为明文 DEX 代码完整可见；仅字符串经 BA.__b（XOR：包名/versionName/versionCode/(i/7)+1234）混淆，已用脚本还原。残余盲区：无障碍配置资源 @xml/teste2 未在解包产物中呈现，android:description 与 isAccessibilityTool 无法核对；服务端下发内容（ConexaoCentral.php）与远端 WebView 文案未纳入。",
  "summary_one_liner": "伪装成 Outback 票券应用的银行木马，用 1000ms 定时器 + 不可取消图文弹窗 + 伪造“Google Informa”Toast 与 TTS 语音，反复强跳系统无障碍设置，直到用户为 .execucoes 开启无障碍。",
  "disguise_identity": {
    "app_display_name": "Férias Decolar",
    "claimed_brand_or_persona": "Ticket Outback / rede Outback 官方票券应用（strings.xml descricao_brasil1），实际承载 Itaú、Bradesco、BB、Santander、Caixa 等银行仿冒页面",
    "a11y_service_label": "Férias Decolar（由 starter._vvv3 经 BA.__b 解密，拼入引导文案 “Acessibilidade > Férias Decolar”；Manifest 未声明 android:description，@xml/teste2 未在解包产物中呈现）",
    "identity_mismatch": true,
    "obfuscation_tricks": "B4A 全量混淆：类/字段/方法名替换为 _vvvvv… 同形变体序列（_v6/_vv3/_vvv3/_vvvv5 等仅下划线与 v 数量不同，易误读）；所有界面文案、服务名、外部路径以 BA.__b 字节数组 + 包名/版本信息 XOR 加密，静态搜索 “Acessibilidade/Outback” 无法命中；无障碍服务类名 .execucoes 无实际语义；无障碍配置资源以 @xml/teste2 引用且未随解包产出，无 description 与 isAccessibilityTool 声明。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": ".main（唯一 LAUNCHER Activity，label Férias Decolar）→ LoadLayout(\"pismaim\")",
      "trigger_event": "onCreate → _activity_create(true)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（该步不呈现引导文案）",
      "shown_text_zh": "加载主布局，无文字说明，用户看不出无障碍诉求",
      "user_action_requested": "无明确操作；应用同时向远端 /Android/ConexaoCentral.php 上报 data=LERPIS|aaa 并启动 .starter 服务",
      "code_anchor": "camilo.whienal.coyzim.main#_activity_create"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": ".starter 服务（Service）→ Timer1（1000ms）",
      "trigger_event": "_service_create/_service_start → _vvvvvvvvvvvvvvvvvvv3()：未获 WRITE_EXTERNAL_STORAGE 或外部 idsecurity.ini 不存在且 .execucoes 未运行时启动定时器",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台静默启动 1 秒周期定时器，用户无感知",
      "user_action_requested": "无需操作；即使停留在主界面也会被后续步骤拉起设置页",
      "code_anchor": "camilo.whienal.coyzim.starter#_vvvvvvvvvvvvvvvvvvv3 / #_timer1_tick"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "自定义 Toast（CSBuilder 图文）或 Common.Msgbox 信息框",
      "trigger_event": "Timer1 计数达到 _vvvvvvvvvvvvvvvvvv1(=50) 后 _vvvvvvvvvvvvvvvvvvv5()；或用户点击主界面 label1",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O PLUGIN / Ative a permissão a seguir!. / Caso você esteja com dificuldades pode procurar nosso suporte para auxiliar. / Configurações  >  Acessibilidade > Férias Decolar",
      "shown_text_zh": "「你必须激活该功能才能使用本插件」/「请开启以下权限!.」/「如遇困难可联系我们的客服协助」/「设置 > 无障碍 > Férias Decolar」（配 icon_512x.jpg、grenagem.png、accessi.png 图标与绿色/红色配色）",
      "user_action_requested": "Msgbox 仅有一个「确定」按钮，无取消/跳过；点击后立即进入第 4 步",
      "code_anchor": "camilo.whienal.coyzim.starter#_xmenssagem_a / #_vvvvvvvvvvvvvvvvvvv4 ; camilo.whienal.coyzim.main#_vvvvvvvvvvvvvvvvvv0"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": ".activityruntimep（运行时权限教学页，label Férias Decolar）→ 系统存储权限弹窗",
      "trigger_event": "activityruntimep._activity_create 中 starter._vvvv5==\"normaiskaraio\" 且 SDK>=23 → _vvvvvvvvvvvvvvvvvvvv3() → RuntimePermissions 申请 WRITE_EXTERNAL_STORAGE",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（未检出 APPLICATION_DETAILS_SETTINGS 或「允许受限设置」教学文案）",
      "shown_text_zh": "仅申请普通运行时存储权限，未做 Android 13+ 受限设置分步教学",
      "user_action_requested": "在系统权限弹窗点「允许」；被拒绝后 _activity_permissionresult 再调 _vvvvvvvvvvvvvvvvvv0() 重弹引导框",
      "code_anchor": "camilo.whienal.coyzim.activityruntimep#_activity_create / #_vvvvvvvvvvvvvvvvvv0"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表，含 Férias Decolar 项）",
      "trigger_event": "IntentWrapper.Initialize(\"android.settings.ACCESSIBILITY_SETTINGS\") + Common.StartActivity，位于 main#_label1_click、main#_activity_resume、starter$ResumableSub_xSubirManoAPermissao#resume 三处",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Ative o recurso [Férias Decolar] / Ative a permissão para Férias Decolar / Google Informa: Ative a permissão para Férias Decolar",
      "shown_text_zh": "「请激活功能 [Férias Decolar]」/「请为 Férias Decolar 开启权限」/「Google 提示：请为 Férias Decolar 开启权限」（后者为伪造系统来源）",
      "user_action_requested": "要求在系统无障碍列表中手动勾选「Férias Decolar」；无取消按钮，跳转前后 30ms/150ms 震动并 TTS 朗读催促",
      "code_anchor": "camilo.whienal.coyzim.starter$ResumableSub_xSubirManoAPermissao#resume ; camilo.whienal.coyzim.main#_label1_click ; #_activity_resume"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": ".main.onResume → Common.Msgbox 引导框 → 再次 ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户从设置页返回应用触发 onResume，且 starter._vvvv5==\"PedeNovamente\"；同时后台 Timer1 每 50 tick 独立补跳",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O PLUGIN / Configurações > Acessibilidade > Férias Decolar",
      "shown_text_zh": "返回即重弹同一不可取消说明框并立刻再跳无障碍设置；用户无法停留在应用内正常使用",
      "user_action_requested": "只能再次被送往设置页；无「稍后」「跳过」「仅浏览」选项",
      "code_anchor": "camilo.whienal.coyzim.main#_activity_resume / #_vvvvvvvvvvvvvvvvvv0"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": ".execucoes（AccessibilityService，BIND_ACCESSIBILITY_SERVICE）与 .startertwo 服务",
      "trigger_event": "用户在系统列表开启 .execucoes 后 Common.IsPaused(execucoes)==false → 定时器停用；execucoes 的 _listener_accesshierarchi 按窗口名分发（含 \"Acessibilidade\" 分支）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "停止催促循环，转向读取窗口内容、覆盖银行界面等后续窃取动作",
      "user_action_requested": "无；此后用户已无法察觉（伴随 GLOBAL_ACTION_BACK/HOME/RECENTS 反撤权与 WATCH_PKG_INSTALLER 监控）",
      "code_anchor": "camilo.whienal.coyzim.execucoes#_listener_accesshierarchi ; camilo.whienal.coyzim.starter#_vvvvvvvvvvvvvvvvvvv3"
    }
  ],
  "text_presentation_locations": [
    "自定义 Toast 悬浮层：starter#_xmenssagem_a 用 CSBuilder 生成 Spannable（图标 + 标题 + 红色警示 + 绿色「Configurações > Acessibilidade > Férias Decolar」），由 starter#_vvvvvvvvvvvvvvvvvvv4 以 Toast.makeText().show() 显示",
    "不可取消信息框：main#_vvvvvvvvvvvvvvvvvv0 的 Common.Msgbox（仅「确定」）与 activityruntimep#_vvvvvvvvvvvvvvvvvv0 同版式 Msgbox",
    "普通 Toast 催促：starter#_vvvvvvvvvvvvvvvvvvv1 与 ResumableSub 内的「Ative o recurso [Férias Decolar]」「Ative a permissão para Férias Decolar」「Google Informa: Ative a permissão para Férias Decolar」（伪造系统来源）",
    "TTS 语音：starter#_vvvvvvvvvvvvvvvvvvv1 调用 _vvvvvv2.Speak(_vvv0)，在跳转设置前后反复朗读“Ative a permissão a seguir”",
    "res/values/strings.xml 键 descricao_brasil1：完整的「Ticket Outback … Aplicativo oficial da rede Outback … Precisamos da permissão para evitar que seu ticket seja usado por outros clientes」声明（当前未见被 java 代码直接引用，属随包文本诱饵）",
    "系统无障碍列表项：服务 .execucoes 显示名「Férias Decolar」；Manifest 未声明 android:description，@xml/teste2 未在解包产物中呈现，无任何用途说明",
    "应用内图标资源 assets/icone_512x.jpg、grenagem.png、accessi.png 作为引导图文素材嵌入 Toast",
    "未发现 WebView 承载的引导文案：远端下发仅用于业务页 LoadUrl（main#_jobdone 的 votacao 任务），不承载无障碍引导"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O PLUGIN",
      "text_zh": "你必须激活该功能才能使用本插件",
      "source_location": "starter#_process_globals 中 _v7 经 BA.__b 解密（硬编码字节数组）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "pt",
      "text_verbatim": "Ative a permissão a seguir!.",
      "text_zh": "请开启以下权限!.",
      "source_location": "starter#_process_globals 中 _v0 经 BA.__b 解密",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Caso você esteja com dificuldades pode procurar nosso suporte para auxiliar.",
      "text_zh": "如你遇到困难，可以联系我们的客服协助。",
      "source_location": "starter#_process_globals 中 _vv1 经 BA.__b 解密（绿色小字）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "pt",
      "text_verbatim": "Configurações  >  Acessibilidade > Férias Decolar",
      "text_zh": "设置 > 无障碍 > Férias Decolar",
      "source_location": "starter#_xmenssagem_a 硬编码 + _vvv3；main#_vvvvvvvvvvvvvvvvvv0 硬编码 \"Configurações > \" + \" Acessibilidade > \"",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Google Informa: Ative a permissão para Férias Decolar",
      "text_zh": "谷歌提示：请为 Férias Decolar 开启权限",
      "source_location": "starter#_vvvvvvvvvvvvvvvvvvv1 硬编码（伪造成系统/Google 来源的 Toast）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "pt",
      "text_verbatim": "ATIVE O RECURSO PARA FUNCIONAMENTO",
      "text_zh": "激活该功能才能正常运行",
      "source_location": "starter#_process_globals 中 _vvv1 经 BA.__b 解密（20 号粗体结尾文案）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "pt",
      "text_verbatim": "Ticket Outback Ativando o recurso você tem ativação do seu ticket. * Varios ticket por semana * Descontos de 20R$ até 190R$ * Em caso de duvidas procure nosso suporte * Aplicativo oficial da rede Outback * Precisamos da permissão para evitar que seu ticket seja usado por outros clientes",
      "text_zh": "Outback 票券——激活该功能即可激活你的票券。* 每周多张票券 * 20 至 190 雷亚尔折扣 * 有疑问请联系客服 * Outback 连锁官方应用 * 我们需要该权限以防止你的票券被其他顾客使用",
      "source_location": "res/values/strings.xml 键 descricao_brasil1",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "pt",
      "text_verbatim": "Ative o recurso [Férias Decolar]",
      "text_zh": "请激活功能 [Férias Decolar]",
      "source_location": "starter$ResumableSub_xSubirManoAPermissao#resume 硬编码（含一处右括号缺失的 \"Ative o recurso Férias Decolar]\"）",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "双重循环：①后台 Timer1 每 1000ms 计数，满 50 tick 即再弹图文 Toast 并 StartActivity 跳 ACCESSIBILITY_SETTINGS，并 StartService(startertwo) 续接下一轮；②用户从设置页返回触发 main.onResume，当 starter._vvvv5==\"PedeNovamente\" 时先重弹不可取消 Msgbox 再立刻重跳，跳转前后震动并调用 TTS 朗读催促；activityruntimep 的权限被拒后同样经 _activity_permissionresult 重弹引导框。",
    "overlay_or_fake_settings": "未使用 SYSTEM_ALERT_WINDOW 悬浮窗或高仿无障碍开关页；诱导弹层为 CSBuilder 生成的自定义图文 Toast（含 200×225 图标与红/绿配色仿系统指引）与不可取消 Msgbox，跳转后落在真实系统无障碍列表。",
    "restricted_settings_13plus_coaching": "无。未检出 ACTION_APPLICATION_DETAILS_SETTINGS、应用详情右上角菜单教学或 Session 安装器绕过，仅申请普通运行时 WRITE_EXTERNAL_STORAGE；Android 13+ 设备因受限设置缺少该教学而可能无法完成授权。",
    "post_grant_anti_removal": "获权后不再催促；.execucoes 具备 GLOBAL_ACTION_BACK/HOME/RECENTS 与 WATCH_PKG_INSTALLER 能力用于阻止撤权与拦截卸载，main#_activity_create 在 _vvvv5==\"quitadoporra\" 时直接跳 HOME 并调用 _xxxxxxideaplicationbuniteixom() 通过 setComponentEnabledSetting 将 .main 置为 DISABLED(2) 隐藏启动图标。",
    "benign_graceful_degradation": "无。全部引导框无取消/跳过按钮，不存在手动模式、仅观看模式或 ADB 说明等降级路径；拒绝授权后应用无法进入任何业务功能。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 Activity 启动 Intent 动作为 android.settings.ACCESSIBILITY_SETTINGS（或包内 Activity .main/.activityruntimep 恢复前台）时立即启动 UTG；另一稳妥时机是冷启动后约 50 秒（Timer1 50×1000ms）或首次点击主界面 label1 时，捕获自定义图文 Toast 与被压栈的设置页。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/定时触发的图文诱导弹窗页（自定义 Toast 与 Msgbox）",
        "page_identifier": "悬浮 Toast 内容含 assets/icone_512x.jpg 大图 + 黑色粗体标题 + 红色小字 + 绿色「Configurações > Acessibilidade > Férias Decolar」行；Msgbox 仅单个「确定」按钮，标题为“Férias Decolar”",
        "why_most_useful": "这是应用唯一的社会工程说理页，可直接判定其以“必须激活插件”话术诱导开启无障碍，且确认是否存在取消按钮",
        "observable_utg_signals": ["节点文本 “VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O PLUGIN”", "节点文本 “Configurações > Acessibilidade > Férias Decolar” 与图标 ImageView", "弹窗仅存在一个 Button/确定 节点，无“取消/跳过”节点"]
      },
      {
        "page_role": "跳转后系统无障碍服务列表项",
        "page_identifier": "Settings 包内 AccessibilitySettings 界面，列表中「Férias Decolar」开关处于 OFF",
        "why_most_useful": "核对系统无障碍列表实际展示的服务名、是否附带用途说明，判断身份是否与“Outback 官方票券”宣称一致",
        "observable_utg_signals": ["列表项文本 “Férias Decolar”", "该项无 summary/description 描述文本", "开关节点 checked=false 且 className 为 Switch"]
      },
      {
        "page_role": "返回应用后的拒权循环页",
        "page_identifier": "从设置页返回后 1 秒内再次出现同一 Msgbox，并重新拉起 AccessibilitySettings",
        "why_most_useful": "直接观测死循环重跳行为，是区分“良性说明后允许跳过”与“强制压迫”的关键证据",
        "observable_utg_signals": ["onResume 后 <2s 内 accessibility 设置页再次出现", "伴随震动与 TTS 语音", "同一弹窗文本重复出现且无取消入口"]
      },
      {
        "page_role": "伪造系统来源的 Toast 页",
        "page_identifier": "Toast 文本以 “Google Informa:” 开头",
        "why_most_useful": "证明其伪造系统提示以压制用户对无障碍高危权限的警觉",
        "observable_utg_signals": ["Toast 节点文本 “Google Informa: Ative a permissão para Férias Decolar”", "该文本非系统 Settings/Google Play 包发出（来源包为 camilo.whienal.coyzim）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无静态加壳；但字符串经 BA.__b XOR 混淆，纯文本关键词扫描（Acessibilidade/Outback）在 DEX 中不可命中，UTG 需以“跳转 AccessibilitySettings + 悬浮 Toast”行为特征而非文案特征触发。另有两处盲区：无障碍配置资源 @xml/teste2 未随解包产出，无法核对系统列表是否显示伪造说明；远端 ConexaoCentral.php 下发内容与后续银行覆盖界面不在本次静态范围内。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "camilo.whienal.coyzim.starter#_timer1_tick",
    "camilo.whienal.coyzim.starter#_xmenssagem_a",
    "camilo.whienal.coyzim.starter$ResumableSub_xSubirManoAPermissao#resume",
    "camilo.whienal.coyzim.main#_activity_resume",
    "camilo.whienal.coyzim.main#_vvvvvvvvvvvvvvvvvv0",
    "res/values/strings.xml（键 descricao_brasil1）"
  ]
}
```

</details>

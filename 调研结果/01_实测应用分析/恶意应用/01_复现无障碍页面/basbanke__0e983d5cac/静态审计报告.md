# MR_106__0e983d5cac｜basbanke — Quem viu teu perfil

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：137.0s

## 1. 一句话核心结论

- **核心申请方式**：以“谁看过你的主页”伪 Facebook 访客查看器为外壳，点击功能按钮即弹不可取消的假 Facebook 模态说明框并直接跳系统无障碍设置，配合伪造“Google Informa”Toast、onResume 拒权重跳与后台 1 秒 Timer 周期拉起，强制用户开启无障碍服务。
- **静态可见性说明**：无障碍引导链（模态说明框、Toast 文案、ACCESSIBILITY_SETTINGS 跳转、onResume 重跳、1 秒 Timer 轮询、无障碍描述字符串）全部静态可见于 classes.dex 与 res/，无加壳、无 AES 密文、无本地或远端 HTML 承载文案；仅 B4A 二进制布局 pismaim.bal 需运行期渲染才能读取控件位置，但按钮点击回调与全部文案已在代码中明确定位。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `0e983d5cac17d44e1739695e894d8774170efbcf7dc11302c2a2a71ae64e1c6a` |
| 包名 / 年份 | `coy.newring.fcb` / 2019 |
| 家族 / 品类 | **basbanke**（同池样本数：10） |
| 原始来源标识 | https://gbhackers.com/new-android-malware-basbanke/ |
| 桌面显示名 | Quem viu teu perfil |
| 引导页宣称品牌/身份 | Facebook（文案自称为官方 Facebook 主页访客查看功能，宣称“官方网络应用”） |
| 系统无障碍列表服务名 | Quem viu teu perfil（android:description 引用 @string/descricao_brasil1） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置 res/xml/teste2 只声明 android:description，完全不声明 accessibilityEventTypes / canRetrieveWindowContent / flags，真实监听能力在代码运行时设置以规避静态特征；无障碍服务描述用多行“* 项目符号 + 官方网络应用 + 需要该权限来定位访客”伪装成功能说明；同时伪造“Google Informa”系统提示口吻；B4A 全部类成员以 _vvvvvv... 形式重命名，无同形字、多 activity-alias 或伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `.execucoes` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | coy.newring.fcb.main（Activity，加载 assets/pismaim.bal 布局，伪访客查看器主界面） | onCreate → _activity_create(true) | 原生Activity | **原文**：加载布局 pismaim；同时 httpjob 向 starter._vv2 + "/Android/ConexaoCentral.php" 发送 "data=LERPIS\|aaa"<br>**译注**：展示“谁看过你的主页”伪访客界面，同时静默向远端 ConexaoCentral.php 上报 LERPIS 心跳 | 浏览界面并点击“查看访客”按钮（布局 ImageView2），无退出限制 | `coy.newring.fcb.main#_activity_create` |
| 2 | 业务功能触发 | main 布局中的 ImageView2（查看访客按钮） | _imageview2_click 点击回调 | 原生Activity | **原文**：Phone.Vibrate(30)；_vv5 = "PedeNovamente"<br>**译注**：用户点击查看访客后振动反馈，并把引导状态置为“再次请求” | 点击按钮（无取消分支，点击即进入下一步） | `coy.newring.fcb.main#_imageview2_click` |
| 3 | 引导说明页 | Common.Msgbox 模态对话框（唯一确认键，无取消） | _imageview2_click → _vvvvvvvvvvvvvvv5() | 原生Dialog | **原文**：FACEBOOK ATIVAÇÃO / VOCÊ PRECISA ATIVAR O RECURSO PARA VER VISITANTES NO SEU PERFIL / Ative a permissão a seguir, para o funcionamento do sistema. / Caso você tenha dificuldades, basta procurar o nome do aplicativo na proxima janela / Configurações > Acessibilidade > Quem viu teu perfil<br>**译注**：“Facebook 激活 / 你需要激活该功能才能查看谁访问了你的主页 / 请开启以下权限以让系统正常工作 / 如果遇到困难，在下一个窗口里直接找应用名称即可 / 设置 > 无障碍 > Quem viu teu perfil” | 仅有一个确认按钮（Msgbox 单键），无取消/跳过选项 | `coy.newring.fcb.main#_vvvvvvvvvvvvvvv5` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | 同一方法内顺序执行 IntentWrapper.Initialize("android.settings.ACCESSIBILITY_SETTINGS", "") + Common.StartActivity | 系统无障碍页 | **原文**：无（直接跳转系统页）<br>**译注**：说明框关闭的瞬间直接跳转系统无障碍设置列表，用户无选择余地 | 在系统无障碍列表中手动勾选“Quem viu teu perfil” | `coy.newring.fcb.main#_imageview2_click` |
| 5 | 遮罩叠层指引 | 系统 Toast（伪造系统提示口吻） | 跳转后立即 Phone.Vibrate(150) + _vvvvvvvvvvvvvvv6(true) | 悬浮窗Overlay | **原文**：Google Informa: Ative a permissão para  + starter._v5<br>**译注**：“Google 提示：请开启该权限以启用 <功能名>”，并伴随 TTS 语音朗读同一文案 | 继续在系统设置页勾选服务 | `coy.newring.fcb.main#_vvvvvvvvvvvvvvv6` |
| 6 | 拒权反馈循环 | main.onResume（用户从系统设置返回时触发） | onResume → _activity_resume() 判定 starter._vv5.equals("PedeNovamente") | 原生Dialog | **原文**：Phone.Vibrate(30) → _vvvvvvvvvvvvvvv5() → Intent("android.settings.ACCESSIBILITY_SETTINGS") → Phone.Vibrate(150) → _vvvvvvvvvvvvvvv6(true) → Common.StartService(starter)<br>**译注**：返回未授权即再次振动、再次弹说明框、再次跳无障碍设置并再次伪造 Google Toast，形成无法退出的循环 | 只能反复开启或强行退出应用；无跳过路径 | `coy.newring.fcb.main#_activity_resume` |
| 7 | 拒权反馈循环 | coy.newring.fcb.starter（后台 Service，1 秒周期 Timer1）→ starter$ResumableSub_xSubirManoAPermissao | _service_create/_service_start 判定未授予 WRITE_EXTERNAL_STORAGE 或 idsecurity.ini 不存在 → Timer1(1000ms) → _timer1_tick 计数达阈值 → _vvvvvvvvvvvvvvvv2() | 系统无障碍页 | **原文**：IntentWrapper.Initialize("android.settings.ACCESSIBILITY_SETTINGS", "") + ToastMessageShow("Ative o recurso [" + starter._v5 + "]")<br>**译注**：后台每秒计时，到点即主动拉起系统无障碍设置页并 Toast“请激活该功能 [Quem viu teu perfil]”，即使应用退到后台也会把用户推回设置页 | 再次前往无障碍列表勾选服务 | `coy.newring.fcb.starter#_timer1_tick / starter$ResumableSub_xSubirManoAPermissao#resume` |
| 8 | 引导说明页 | 自定义富文本 Toast（Toast.makeText + getView + setBackground 自绘视图） | starter._xmenssagem_a() 经 Threading 线程触发 | 悬浮窗Overlay | **原文**：FACEBOOK ATIVAÇÃO PERFIL / ATIVE O RECURSO PARA HABILITAR O RECURSO / O recurso não está ativado!! / Caso você esteja com dificuldades você pode procurar nosso suporte para auxiliar. / Configurações  >  Acessibilidade > Quem viu teu perfil / Ative e veja quem visitou teu perfil<br>**译注**：图文教学浮层：望远镜图标 + “Facebook 主页激活 / 请激活该功能以启用功能 / 该功能尚未激活!! / 遇到困难可联系我们的支持 / 设置 > 无障碍 > Quem viu teu perfil / 激活即可查看谁访问了你的主页” | 照图操作进入设置 > 无障碍 > 勾选服务 | `coy.newring.fcb.starter#_xmenssagem_a` |
| 9 | 获权后动作 | coy.newring.fcb.execucoes（无障碍服务）+ starter 服务停止轮询 | 无障碍服务运行后 starter._vvvvvvvvvvvvvvv0() 中 Common.IsPaused(execucoes) 为假 → Timer1.setEnabled(false) | 系统无障碍页 | **原文**：无（静默进入监听态）<br>**译注**：获得权限后停止骚扰轮询，无障碍服务转入常态窗口监听（用于后续银行覆盖页窃取） | 无 | `coy.newring.fcb.starter#_vvvvvvvvvvvvvvv0` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- main 页 Common.Msgbox 不可取消模态框：FACEBOOK ATIVAÇÃO 标题 + 必须激活说明 + 设置路径教学（main#_vvvvvvvvvvvvvvv5）
- 跳转系统设置后立即弹出的 Toast：“Google Informa: Ative a permissão para …”（main#_vvvvvvvvvvvvvvv6，伪造系统口吻）
- onResume 拒权循环中重复弹出的同一 Msgbox 与同一 Google Toast（main#_activity_resume）
- 后台 Timer 到点后 Toast：“Ative o recurso [Quem viu teu perfil]”（starter$ResumableSub_xSubirManoAPermissao#resume）
- 自定义富文本 Toast 图文教学浮层：望远镜图标 + FACEBOOK ATIVAÇÃO PERFIL + 红色“O recurso não está ativado!!” + 设置/无障碍图标 + “Configurações > Acessibilidade > Quem viu teu perfil”（starter#_xmenssagem_a）
- 系统无障碍列表条目描述：res/values/strings.xml 中 descricao_brasil1（经 res/xml/teste2 的 android:description 引用）
- TTS 语音朗读同一段提示（main#_vvvvvvvvvvvvvvv6 → TTS.Speak(_vvvv3)）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | FACEBOOK ATIVAÇÃO | Facebook 激活 | `硬编码于 coy.newring.fcb.main#_vvvvvvvvvvvvvvv5` | 假更新 |
| pt | VOCÊ PRECISA ATIVAR O RECURSO PARA VER VISITANTES NO SEU PERFIL | 你必须激活该功能才能查看谁访问了你的主页 | `硬编码于 coy.newring.fcb.main#_vvvvvvvvvvvvvvv5` | 故障恐吓 |
| pt | Ative a permissão a seguir, para o funcionamento do sistema. | 请开启以下权限，以保证系统正常运行。 | `硬编码于 coy.newring.fcb.main#_vvvvvvvvvvvvvvv5` | 受限设置分步教学 |
| pt | Caso você tenha dificuldades, basta procurar o nome do aplicativo na proxima janela / Configurações > Acessibilidade > Quem viu teu perfil | 如果遇到困难，只需在下一个窗口里找到应用名称即可 / 设置 > 无障碍 > Quem viu teu perfil | `硬编码于 coy.newring.fcb.main#_vvvvvvvvvvvvvvv5` | 受限设置分步教学 |
| pt | Google Informa: Ative a permissão para | Google 提示：请开启该权限以启用 | `硬编码于 coy.newring.fcb.main#_vvvvvvvvvvvvvvv6` | 假反诈安全 |
| pt | Ative o recurso [ | 请激活该功能 [ | `硬编码于 coy.newring.fcb.starter$ResumableSub_xSubirManoAPermissao#resume` | 受限设置分步教学 |
| pt | FACEBOOK ATIVAÇÃO PERFIL | Facebook 主页激活 | `硬编码于 coy.newring.fcb.starter#_xmenssagem_a` | 假更新 |
| pt | ATIVE O RECURSO PARA HABILITAR O RECURSO | 激活该功能以启用该功能 | `硬编码于 coy.newring.fcb.starter#_xmenssagem_a` | 故障恐吓 |
| pt | O recurso não está ativado!! | 该功能尚未激活！！ | `硬编码于 coy.newring.fcb.starter#_xmenssagem_a` | 故障恐吓 |
| pt | Caso você esteja com dificuldades você pode procurar nosso suporte para auxiliar.  Configurações  >  Acessibilidade > Quem viu teu perfil | 如果你遇到困难，可以联系我们的支持来协助你。 设置 > 无障碍 > Quem viu teu perfil | `硬编码于 coy.newring.fcb.starter#_xmenssagem_a（含 grenagem.png / accessi.png 图标）` | 受限设置分步教学 |
| pt | Ative e veja quem visitou teu perfil | 激活后即可查看谁访问了你的主页 | `硬编码于 coy.newring.fcb.starter#_xmenssagem_a` | 隐私承诺 |
| pt | Quem viu teu perfil Ativando o recurso você tem ativação do componente. * Veja quem visitou seu perfil * Fique atento a novas visitas * Em caso de duvidas procure nosso suporte * Aplicativo oficial da rede * Precisamos da permissão para localizar os visitantes | 谁看过你的主页。激活该功能即可激活该组件。* 查看谁访问了你的主页 * 留意新的访问 * 有疑问请联系我们的支持 * 本网络的官方应用 * 我们需要该权限来定位访客 | `res/values/strings.xml descricao_brasil1（由 res/xml/teste2 的 android:description 引用）` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：双通道循环：① main.onResume 中 _activity_resume() 检测 starter._vv5 == "PedeNovamente"，用户每次从系统设置返回未授权即再次弹说明框 + 再次 Intent(ACCESSIBILITY_SETTINGS) + 再次伪造 Google Toast；② 后台 starter 服务在存储权限未授予或 idsecurity.ini 不存在时启用 1 秒周期 Timer1，计数达阈值即经 ResumableSub_xSubirManoAPermissao 主动拉起 ACCESSIBILITY_SETTINGS 并 Toast 提示，应用退到后台仍持续。另有 quitadoporra 分支用 ACTION_MAIN + CATEGORY_HOME 把界面顶回桌面。
- **遮罩叠层 / 高仿系统设置页**：无全屏悬浮窗或高仿系统无障碍开关页；叠层形式为系统 Toast（含自定义富文本图文 Toast 自绘视图 + ColorDrawable 背景），覆盖在系统无障碍设置页之上做指引。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未见 ACTION_APPLICATION_DETAILS_SETTINGS、右上角菜单允许受限设置或 Session 安装器绕过教学；targetSdkVersion=26）
- **获权后即时行为与防撤权机制**：静态可见的获权后动作为停止 Timer 轮询并转入无障碍服务常态监听；本次核验范围内未发现 GLOBAL_ACTION_BACK/HOME 阻止撤权的直接代码（初筛 DEX 线索提示存在，属 .execucoes 内部逻辑，未在本次定向核查中展开）。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：最佳时机：监测到当前前台 Activity 为 coy.newring.fcb.main 且即将/已经发起 android.settings.ACCESSIBILITY_SETTINGS 跳转的瞬间（点击 ImageView2 后约 1 秒内）；其次是应用退到后台后约 1 秒周期重复出现 ACCESSIBILITY_SETTINGS 拉起（Timer1 特征），此时捕获可同时拿到引导弹窗与伪造 Google Toast。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：主要盲区：① 自定义富文本 Toast 与主界面布局为 B4A 二进制 .bal 渲染，控件文字可能以图片（iconebinoculos.png / grenagem.png / accessi.png）承载，纯文本 UTG 需 OCR 补读；② 无障碍服务真实能力（窗口读取、GLOBAL_ACTION 拦截、银行覆盖页）在 .execucoes 运行时动态设置，且被 _vvvvvv… 重命名，静态可见性限于引导链本身；③ 无 WebView/远端 HTML，因此不存在远端下发文案导致的 UTG 文本缺失。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/点击后的不可取消引导弹窗页** | coy.newring.fcb.main 前台 + 单键系统 AlertDialog，含“FACEBOOK ATIVAÇÃO”与“Configurações > Acessibilidade”路径 | 该弹窗是伪装身份与分步教学的集中呈现处，且只有一个确认键，是判定“无取消路径 + 品牌冒充”的直接证据 | 弹窗标题含 FACEBOOK ATIVAÇÃO（伪品牌）；弹窗按钮数=1，无取消/跳过；正文含 Configurações > Acessibilidade > Quem viu teu perfil 分步教学 |
| **跳转瞬间的伪造系统 Toast** | 系统 Toast 文本以“Google Informa: Ative a permissão para”开头 | 证明应用伪造 Google 系统口吻施压，区分于普通功能说明 | Toast 文本含 Google Informa；Toast 与 ACCESSIBILITY_SETTINGS 跳转在同一秒内出现 |
| **系统无障碍服务列表项** | 系统 Settings 无障碍列表中的“Quem viu teu perfil”条目及其描述段 | 核对无障碍列表中展示的名称/描述是否与桌面显示名一致，确认用户被诱导勾选的具体条目 | 条目名 Quem viu teu perfil；描述含 Aplicativo oficial da rede / Precisamos da permissão para localizar os visitantes |
| **拒权返回后的循环页** | 从系统设置返回 main 后 1 秒内再次出现同一 AlertDialog 并再次跳转 | 证明 onResume 死循环重跳，是“强制诱导”而非“一次性说明”的关键判别点 | 同一弹窗重复出现次数≥2；返回后自动再次进入 ACCESSIBILITY_SETTINGS；伴随振动与同一 Toast |
| **后台定时拉起的图文教学 Toast 页** | 自定义 Toast 视图：望远镜图片 + FACEBOOK ATIVAÇÃO PERFIL + 红色“O recurso não está ativado!!” + 设置/无障碍小图标 | 证明应用退到后台仍周期性把用户推回无障碍设置，属典型反规避式骚扰引导 | Toast 内含图片与多行富文本（非系统默认 Toast）；应用处于后台时 ACCESSIBILITY_SETTINGS 被反复拉起；文本含 O recurso não está ativado |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `coy.newring.fcb.main#_imageview2_click`
- `coy.newring.fcb.main#_vvvvvvvvvvvvvvv5`
- `coy.newring.fcb.main#_activity_resume`
- `coy.newring.fcb.starter$ResumableSub_xSubirManoAPermissao#resume`
- `coy.newring.fcb.starter#_xmenssagem_a`
- `res/values/strings.xml（descricao_brasil1）+ res/xml/teste2`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（无障碍权限引导链，纯运行期 UTG 视角）

**静态可见性：完整（clear）** — 全部引导逻辑位于 `classes.dex` 的 B4A 代码与资源中，无加壳、无 WebView/远端 HTML、无加密载荷。

**核心链路（每一步都有代码对应）**

1. **冷启动** → [main._activity_create()](<resource-unit:#1.dex1 code:coy.newring.fcb.main#_activity_create>) 加载 `pismaim` 布局，同时向远端 `/Android/ConexaoCentral.php` 上报 `data=LERPIS|aaa`，并启动 `.starter` 服务。
2. **业务功能触发** → [main._imageview2_click()](<resource-unit:#1.dex1 code:coy.newring.fcb.main#_imageview2_click>)（布局 ImageView2，即“查看访客”按钮）：振动 → 弹说明框 → 置状态 `PedeNovamente`。
3. **引导说明页** → [_vvvvvvvvvvvvvvv5()](<resource-unit:#1.dex1 code:coy.newring.fcb.main#_vvvvvvvvvvvvvvv5>) 用 `Common.Msgbox` 呈现不可取消模态框：`FACEBOOK ATIVAÇÃO` / “VOCÊ PRECISA ATIVAR O RECURSO PARA VER VISITANTES NO SEU PERFIL” / “Ative a permissão a seguir…” / 绿色分步教学 `Configurações > Acessibilidade > Quem viu teu perfil`。只有一个确认键，无取消/跳过。
4. **跳无障碍设置** → 同一方法内立即 `Intent("android.settings.ACCESSIBILITY_SETTINGS")`，用户无选择权；随后 [_vvvvvvvvvvvvvvv6(true)](<resource-unit:#1.dex1 code:coy.newring.fcb.main#_vvvvvvvvvvvvvvv6>) 以 **“Google Informa: Ative a permissão para …”** 伪造系统提示 Toast。
5. **拒权循环** → [main._activity_resume()](<resource-unit:#1.dex1 code:coy.newring.fcb.main#_activity_resume>) 在 `onResume` 检测到 `_vv5 == "PedeNovamente"` 时再次弹框 + 再跳设置 + 再 Toast，用户从系统设置返回未授权即被立刻推回；另一分支 `quitadoporra` 用 `ACTION_MAIN + CATEGORY_HOME` 把界面顶回桌面。
6. **后台定时再拉起** → [starter._vvvvvvvvvvvvvvv0()](<resource-unit:#1.dex1 code:coy.newring.fcb.starter#_vvvvvvvvvvvvvvv0>) 在存储权限未授予或 `idsecurity.ini` 不存在时注册 1 秒周期 `Timer1`；[starter._timer1_tick()](<resource-unit:#1.dex1 code:coy.newring.fcb.starter#_timer1_tick>) 计数到阈值后经 [_vvvvvvvvvvvvvvvv2()](<resource-unit:#1.dex1 code:coy.newring.fcb.starter#_vvvvvvvvvvvvvvvv2>) 进入 [ResumableSub_xSubirManoAPermissao.resume](<resource-unit:#1.dex1 code:coy.newring.fcb.starter$ResumableSub_xSubirManoAPermissao#resume>)，再 `ACCESSIBILITY_SETTINGS` + 振动 + Toast “Ative o recurso [Quem viu teu perfil]”。
7. **图文教学 Toast** → [starter._xmenssagem_a()](<resource-unit:#1.dex1 code:coy.newring.fcb.starter#_xmenssagem_a>) 自定义 `Toast` 视图：望远镜图标 + `FACEBOOK ATIVAÇÃO PERFIL` + 红色 “O recurso não está ativado!!” + `grenagem.png`/`accessi.png` 图标拼出的 `Configurações > Acessibilidade > Quem viu teu perfil`。
8. **获权后** → 无障碍服务运行后 `Common.IsPaused(execucoes)` 为假即关闭 Timer，进入 `.execucoes` 常态监听（银行覆盖页窃取逻辑，本次未展开）。

**身份伪装要点**

- 显示名/无障碍列表描述均为“Quem viu teu perfil”，系统无障碍条目描述来自 [descricao_brasil1](<resource-unit:#1 file:res/values/strings.xml#L3-L9>)，宣称“官方网络应用”“需要该权限来定位访客”，实为冒用 Facebook 品牌。
- 无障碍配置 [res/xml/teste2](<resource-unit:#1 file:res/xml/teste2>) **只声明 description**，不声明事件类型与窗口读取能力——能力在运行时设置，配置层刻意留白。
- 未发现：`ACTION_APPLICATION_DETAILS_SETTINGS`、Android 13 受限设置分步教学、悬浮窗叠层遮罩、高仿系统开关页、WebView 页面。载体全部是原生 `Msgbox` 与自定义 `Toast`。

**已登记风险**：R-001（fraud_phishing / high）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链（模态说明框、Toast 文案、ACCESSIBILITY_SETTINGS 跳转、onResume 重跳、1 秒 Timer 轮询、无障碍描述字符串）全部静态可见于 classes.dex 与 res/，无加壳、无 AES 密文、无本地或远端 HTML 承载文案；仅 B4A 二进制布局 pismaim.bal 需运行期渲染才能读取控件位置，但按钮点击回调与全部文案已在代码中明确定位。",
  "summary_one_liner": "以“谁看过你的主页”伪 Facebook 访客查看器为外壳，点击功能按钮即弹不可取消的假 Facebook 模态说明框并直接跳系统无障碍设置，配合伪造“Google Informa”Toast、onResume 拒权重跳与后台 1 秒 Timer 周期拉起，强制用户开启无障碍服务。",
  "disguise_identity": {
    "app_display_name": "Quem viu teu perfil",
    "claimed_brand_or_persona": "Facebook（文案自称为官方 Facebook 主页访客查看功能，宣称“官方网络应用”）",
    "a11y_service_label": "Quem viu teu perfil（android:description 引用 @string/descricao_brasil1）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置 res/xml/teste2 只声明 android:description，完全不声明 accessibilityEventTypes / canRetrieveWindowContent / flags，真实监听能力在代码运行时设置以规避静态特征；无障碍服务描述用多行“* 项目符号 + 官方网络应用 + 需要该权限来定位访客”伪装成功能说明；同时伪造“Google Informa”系统提示口吻；B4A 全部类成员以 _vvvvvv... 形式重命名，无同形字、多 activity-alias 或伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "coy.newring.fcb.main（Activity，加载 assets/pismaim.bal 布局，伪访客查看器主界面）",
      "trigger_event": "onCreate → _activity_create(true)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "加载布局 pismaim；同时 httpjob 向 starter._vv2 + \"/Android/ConexaoCentral.php\" 发送 \"data=LERPIS|aaa\"",
      "shown_text_zh": "展示“谁看过你的主页”伪访客界面，同时静默向远端 ConexaoCentral.php 上报 LERPIS 心跳",
      "user_action_requested": "浏览界面并点击“查看访客”按钮（布局 ImageView2），无退出限制",
      "code_anchor": "coy.newring.fcb.main#_activity_create"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "main 布局中的 ImageView2（查看访客按钮）",
      "trigger_event": "_imageview2_click 点击回调",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Phone.Vibrate(30)；_vv5 = \"PedeNovamente\"",
      "shown_text_zh": "用户点击查看访客后振动反馈，并把引导状态置为“再次请求”",
      "user_action_requested": "点击按钮（无取消分支，点击即进入下一步）",
      "code_anchor": "coy.newring.fcb.main#_imageview2_click"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "Common.Msgbox 模态对话框（唯一确认键，无取消）",
      "trigger_event": "_imageview2_click → _vvvvvvvvvvvvvvv5()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "FACEBOOK ATIVAÇÃO / VOCÊ PRECISA ATIVAR O RECURSO PARA VER VISITANTES NO SEU PERFIL / Ative a permissão a seguir, para o funcionamento do sistema. / Caso você tenha dificuldades, basta procurar o nome do aplicativo na proxima janela / Configurações > Acessibilidade > Quem viu teu perfil",
      "shown_text_zh": "“Facebook 激活 / 你需要激活该功能才能查看谁访问了你的主页 / 请开启以下权限以让系统正常工作 / 如果遇到困难，在下一个窗口里直接找应用名称即可 / 设置 > 无障碍 > Quem viu teu perfil”",
      "user_action_requested": "仅有一个确认按钮（Msgbox 单键），无取消/跳过选项",
      "code_anchor": "coy.newring.fcb.main#_vvvvvvvvvvvvvvv5"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "同一方法内顺序执行 IntentWrapper.Initialize(\"android.settings.ACCESSIBILITY_SETTINGS\", \"\") + Common.StartActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（直接跳转系统页）",
      "shown_text_zh": "说明框关闭的瞬间直接跳转系统无障碍设置列表，用户无选择余地",
      "user_action_requested": "在系统无障碍列表中手动勾选“Quem viu teu perfil”",
      "code_anchor": "coy.newring.fcb.main#_imageview2_click"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统 Toast（伪造系统提示口吻）",
      "trigger_event": "跳转后立即 Phone.Vibrate(150) + _vvvvvvvvvvvvvvv6(true)",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Google Informa: Ative a permissão para  + starter._v5",
      "shown_text_zh": "“Google 提示：请开启该权限以启用 <功能名>”，并伴随 TTS 语音朗读同一文案",
      "user_action_requested": "继续在系统设置页勾选服务",
      "code_anchor": "coy.newring.fcb.main#_vvvvvvvvvvvvvvv6"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "main.onResume（用户从系统设置返回时触发）",
      "trigger_event": "onResume → _activity_resume() 判定 starter._vv5.equals(\"PedeNovamente\")",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Phone.Vibrate(30) → _vvvvvvvvvvvvvvv5() → Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") → Phone.Vibrate(150) → _vvvvvvvvvvvvvvv6(true) → Common.StartService(starter)",
      "shown_text_zh": "返回未授权即再次振动、再次弹说明框、再次跳无障碍设置并再次伪造 Google Toast，形成无法退出的循环",
      "user_action_requested": "只能反复开启或强行退出应用；无跳过路径",
      "code_anchor": "coy.newring.fcb.main#_activity_resume"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "coy.newring.fcb.starter（后台 Service，1 秒周期 Timer1）→ starter$ResumableSub_xSubirManoAPermissao",
      "trigger_event": "_service_create/_service_start 判定未授予 WRITE_EXTERNAL_STORAGE 或 idsecurity.ini 不存在 → Timer1(1000ms) → _timer1_tick 计数达阈值 → _vvvvvvvvvvvvvvvv2()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "IntentWrapper.Initialize(\"android.settings.ACCESSIBILITY_SETTINGS\", \"\") + ToastMessageShow(\"Ative o recurso [\" + starter._v5 + \"]\")",
      "shown_text_zh": "后台每秒计时，到点即主动拉起系统无障碍设置页并 Toast“请激活该功能 [Quem viu teu perfil]”，即使应用退到后台也会把用户推回设置页",
      "user_action_requested": "再次前往无障碍列表勾选服务",
      "code_anchor": "coy.newring.fcb.starter#_timer1_tick / starter$ResumableSub_xSubirManoAPermissao#resume"
    },
    {
      "step": 8,
      "stage": "引导说明页",
      "screen_or_component": "自定义富文本 Toast（Toast.makeText + getView + setBackground 自绘视图）",
      "trigger_event": "starter._xmenssagem_a() 经 Threading 线程触发",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "FACEBOOK ATIVAÇÃO PERFIL / ATIVE O RECURSO PARA HABILITAR O RECURSO / O recurso não está ativado!! / Caso você esteja com dificuldades você pode procurar nosso suporte para auxiliar. / Configurações  >  Acessibilidade > Quem viu teu perfil / Ative e veja quem visitou teu perfil",
      "shown_text_zh": "图文教学浮层：望远镜图标 + “Facebook 主页激活 / 请激活该功能以启用功能 / 该功能尚未激活!! / 遇到困难可联系我们的支持 / 设置 > 无障碍 > Quem viu teu perfil / 激活即可查看谁访问了你的主页”",
      "user_action_requested": "照图操作进入设置 > 无障碍 > 勾选服务",
      "code_anchor": "coy.newring.fcb.starter#_xmenssagem_a"
    },
    {
      "step": 9,
      "stage": "获权后动作",
      "screen_or_component": "coy.newring.fcb.execucoes（无障碍服务）+ starter 服务停止轮询",
      "trigger_event": "无障碍服务运行后 starter._vvvvvvvvvvvvvvv0() 中 Common.IsPaused(execucoes) 为假 → Timer1.setEnabled(false)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（静默进入监听态）",
      "shown_text_zh": "获得权限后停止骚扰轮询，无障碍服务转入常态窗口监听（用于后续银行覆盖页窃取）",
      "user_action_requested": "无",
      "code_anchor": "coy.newring.fcb.starter#_vvvvvvvvvvvvvvv0"
    }
  ],
  "text_presentation_locations": [
    "main 页 Common.Msgbox 不可取消模态框：FACEBOOK ATIVAÇÃO 标题 + 必须激活说明 + 设置路径教学（main#_vvvvvvvvvvvvvvv5）",
    "跳转系统设置后立即弹出的 Toast：“Google Informa: Ative a permissão para …”（main#_vvvvvvvvvvvvvvv6，伪造系统口吻）",
    "onResume 拒权循环中重复弹出的同一 Msgbox 与同一 Google Toast（main#_activity_resume）",
    "后台 Timer 到点后 Toast：“Ative o recurso [Quem viu teu perfil]”（starter$ResumableSub_xSubirManoAPermissao#resume）",
    "自定义富文本 Toast 图文教学浮层：望远镜图标 + FACEBOOK ATIVAÇÃO PERFIL + 红色“O recurso não está ativado!!” + 设置/无障碍图标 + “Configurações > Acessibilidade > Quem viu teu perfil”（starter#_xmenssagem_a）",
    "系统无障碍列表条目描述：res/values/strings.xml 中 descricao_brasil1（经 res/xml/teste2 的 android:description 引用）",
    "TTS 语音朗读同一段提示（main#_vvvvvvvvvvvvvvv6 → TTS.Speak(_vvvv3)）"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "FACEBOOK ATIVAÇÃO",
      "text_zh": "Facebook 激活",
      "source_location": "硬编码于 coy.newring.fcb.main#_vvvvvvvvvvvvvvv5",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "pt",
      "text_verbatim": "VOCÊ PRECISA ATIVAR O RECURSO PARA VER VISITANTES NO SEU PERFIL",
      "text_zh": "你必须激活该功能才能查看谁访问了你的主页",
      "source_location": "硬编码于 coy.newring.fcb.main#_vvvvvvvvvvvvvvv5",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "pt",
      "text_verbatim": "Ative a permissão a seguir, para o funcionamento do sistema.",
      "text_zh": "请开启以下权限，以保证系统正常运行。",
      "source_location": "硬编码于 coy.newring.fcb.main#_vvvvvvvvvvvvvvv5",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Caso você tenha dificuldades, basta procurar o nome do aplicativo na proxima janela / Configurações > Acessibilidade > Quem viu teu perfil",
      "text_zh": "如果遇到困难，只需在下一个窗口里找到应用名称即可 / 设置 > 无障碍 > Quem viu teu perfil",
      "source_location": "硬编码于 coy.newring.fcb.main#_vvvvvvvvvvvvvvv5",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Google Informa: Ative a permissão para ",
      "text_zh": "Google 提示：请开启该权限以启用 ",
      "source_location": "硬编码于 coy.newring.fcb.main#_vvvvvvvvvvvvvvv6",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "pt",
      "text_verbatim": "Ative o recurso [",
      "text_zh": "请激活该功能 [",
      "source_location": "硬编码于 coy.newring.fcb.starter$ResumableSub_xSubirManoAPermissao#resume",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "FACEBOOK ATIVAÇÃO PERFIL",
      "text_zh": "Facebook 主页激活",
      "source_location": "硬编码于 coy.newring.fcb.starter#_xmenssagem_a",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "pt",
      "text_verbatim": "ATIVE O RECURSO PARA HABILITAR O RECURSO",
      "text_zh": "激活该功能以启用该功能",
      "source_location": "硬编码于 coy.newring.fcb.starter#_xmenssagem_a",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "pt",
      "text_verbatim": "O recurso não está ativado!!",
      "text_zh": "该功能尚未激活！！",
      "source_location": "硬编码于 coy.newring.fcb.starter#_xmenssagem_a",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "pt",
      "text_verbatim": "Caso você esteja com dificuldades você pode procurar nosso suporte para auxiliar.  Configurações  >  Acessibilidade > Quem viu teu perfil",
      "text_zh": "如果你遇到困难，可以联系我们的支持来协助你。 设置 > 无障碍 > Quem viu teu perfil",
      "source_location": "硬编码于 coy.newring.fcb.starter#_xmenssagem_a（含 grenagem.png / accessi.png 图标）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Ative e veja quem visitou teu perfil",
      "text_zh": "激活后即可查看谁访问了你的主页",
      "source_location": "硬编码于 coy.newring.fcb.starter#_xmenssagem_a",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "pt",
      "text_verbatim": "Quem viu teu perfil Ativando o recurso você tem ativação do componente. * Veja quem visitou seu perfil * Fique atento a novas visitas * Em caso de duvidas procure nosso suporte * Aplicativo oficial da rede * Precisamos da permissão para localizar os visitantes",
      "text_zh": "谁看过你的主页。激活该功能即可激活该组件。* 查看谁访问了你的主页 * 留意新的访问 * 有疑问请联系我们的支持 * 本网络的官方应用 * 我们需要该权限来定位访客",
      "source_location": "res/values/strings.xml descricao_brasil1（由 res/xml/teste2 的 android:description 引用）",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "双通道循环：① main.onResume 中 _activity_resume() 检测 starter._vv5 == \"PedeNovamente\"，用户每次从系统设置返回未授权即再次弹说明框 + 再次 Intent(ACCESSIBILITY_SETTINGS) + 再次伪造 Google Toast；② 后台 starter 服务在存储权限未授予或 idsecurity.ini 不存在时启用 1 秒周期 Timer1，计数达阈值即经 ResumableSub_xSubirManoAPermissao 主动拉起 ACCESSIBILITY_SETTINGS 并 Toast 提示，应用退到后台仍持续。另有 quitadoporra 分支用 ACTION_MAIN + CATEGORY_HOME 把界面顶回桌面。",
    "overlay_or_fake_settings": "无全屏悬浮窗或高仿系统无障碍开关页；叠层形式为系统 Toast（含自定义富文本图文 Toast 自绘视图 + ColorDrawable 背景），覆盖在系统无障碍设置页之上做指引。",
    "restricted_settings_13plus_coaching": "无（未见 ACTION_APPLICATION_DETAILS_SETTINGS、右上角菜单允许受限设置或 Session 安装器绕过教学；targetSdkVersion=26）",
    "post_grant_anti_removal": "静态可见的获权后动作为停止 Timer 轮询并转入无障碍服务常态监听；本次核验范围内未发现 GLOBAL_ACTION_BACK/HOME 阻止撤权的直接代码（初筛 DEX 线索提示存在，属 .execucoes 内部逻辑，未在本次定向核查中展开）。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "最佳时机：监测到当前前台 Activity 为 coy.newring.fcb.main 且即将/已经发起 android.settings.ACCESSIBILITY_SETTINGS 跳转的瞬间（点击 ImageView2 后约 1 秒内）；其次是应用退到后台后约 1 秒周期重复出现 ACCESSIBILITY_SETTINGS 拉起（Timer1 特征），此时捕获可同时拿到引导弹窗与伪造 Google Toast。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/点击后的不可取消引导弹窗页",
        "page_identifier": "coy.newring.fcb.main 前台 + 单键系统 AlertDialog，含“FACEBOOK ATIVAÇÃO”与“Configurações > Acessibilidade”路径",
        "why_most_useful": "该弹窗是伪装身份与分步教学的集中呈现处，且只有一个确认键，是判定“无取消路径 + 品牌冒充”的直接证据",
        "observable_utg_signals": ["弹窗标题含 FACEBOOK ATIVAÇÃO（伪品牌）", "弹窗按钮数=1，无取消/跳过", "正文含 Configurações > Acessibilidade > Quem viu teu perfil 分步教学"]
      },
      {
        "page_role": "跳转瞬间的伪造系统 Toast",
        "page_identifier": "系统 Toast 文本以“Google Informa: Ative a permissão para”开头",
        "why_most_useful": "证明应用伪造 Google 系统口吻施压，区分于普通功能说明",
        "observable_utg_signals": ["Toast 文本含 Google Informa", "Toast 与 ACCESSIBILITY_SETTINGS 跳转在同一秒内出现"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍列表中的“Quem viu teu perfil”条目及其描述段",
        "why_most_useful": "核对无障碍列表中展示的名称/描述是否与桌面显示名一致，确认用户被诱导勾选的具体条目",
        "observable_utg_signals": ["条目名 Quem viu teu perfil", "描述含 Aplicativo oficial da rede / Precisamos da permissão para localizar os visitantes"]
      },
      {
        "page_role": "拒权返回后的循环页",
        "page_identifier": "从系统设置返回 main 后 1 秒内再次出现同一 AlertDialog 并再次跳转",
        "why_most_useful": "证明 onResume 死循环重跳，是“强制诱导”而非“一次性说明”的关键判别点",
        "observable_utg_signals": ["同一弹窗重复出现次数≥2", "返回后自动再次进入 ACCESSIBILITY_SETTINGS", "伴随振动与同一 Toast"]
      },
      {
        "page_role": "后台定时拉起的图文教学 Toast 页",
        "page_identifier": "自定义 Toast 视图：望远镜图片 + FACEBOOK ATIVAÇÃO PERFIL + 红色“O recurso não está ativado!!” + 设置/无障碍小图标",
        "why_most_useful": "证明应用退到后台仍周期性把用户推回无障碍设置，属典型反规避式骚扰引导",
        "observable_utg_signals": ["Toast 内含图片与多行富文本（非系统默认 Toast）", "应用处于后台时 ACCESSIBILITY_SETTINGS 被反复拉起", "文本含 O recurso não está ativado"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "主要盲区：① 自定义富文本 Toast 与主界面布局为 B4A 二进制 .bal 渲染，控件文字可能以图片（iconebinoculos.png / grenagem.png / accessi.png）承载，纯文本 UTG 需 OCR 补读；② 无障碍服务真实能力（窗口读取、GLOBAL_ACTION 拦截、银行覆盖页）在 .execucoes 运行时动态设置，且被 _vvvvvv… 重命名，静态可见性限于引导链本身；③ 无 WebView/远端 HTML，因此不存在远端下发文案导致的 UTG 文本缺失。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "CARRIER_GIF_OR_IMAGE_GUIDE"
  ],
  "code_anchors": [
    "coy.newring.fcb.main#_imageview2_click",
    "coy.newring.fcb.main#_vvvvvvvvvvvvvvv5",
    "coy.newring.fcb.main#_activity_resume",
    "coy.newring.fcb.starter$ResumableSub_xSubirManoAPermissao#resume",
    "coy.newring.fcb.starter#_xmenssagem_a",
    "res/values/strings.xml（descricao_brasil1）+ res/xml/teste2"
  ]
}
```

</details>

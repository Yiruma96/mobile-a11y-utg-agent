# MR_066__0821c5c27d｜basbanke — Quem te visitou

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：126.1s

## 1. 一句话核心结论

- **核心申请方式**：以“Quem te visitou”访客查看器为壳，冷启动单按钮“ATIVAR RECURSO”配合 MsgBox 路径教学、伪造“Google Informa”Toast+TTS 直跳系统无障碍页，并靠 onResume 与 1 秒 Timer 循环重跳直至开启，获权后弹伪系统省电提示并 GLOBAL_ACTION_HOME/BACK 反撤权。
- **静态可见性说明**：应用为 B4A 开发且未加壳，classes.dex 完整反编译，跳转 Intent、Toast/MsgBox 文案、无障碍配置 res/xml-v13/teste2 与 res/values/strings.xml 均可静态还原；仅服务显示名取自远端配置变量 starter._vvv1 与后续银行覆盖页文案由服务器下发，不影响 UTG 引导链判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `0821c5c27d1ada3dcd1f57ebfee52cfeccec2857ef1ed73a04da40c40ec3acfe` |
| 包名 / 年份 | `igr.manobom.inla` / 2019 |
| 家族 / 品类 | **basbanke**（同池样本数：10） |
| 原始来源标识 | https://gbhackers.com/new-android-malware-basbanke/ |
| 桌面显示名 | Quem te visitou |
| 引导页宣称品牌/身份 | “Quem te visitou”访客查看类工具（描述中自称“Aplicativo oficial / Funcional em toda nossa rede”，提示中冒充 Google 系统通知） |
| 系统无障碍列表服务名 | Quem te visitou（服务未设 android:label，沿用应用名；描述为 strings.xml 的 descricao_brasil1） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：服务名与功能完全错配（访客查看器 vs 银行界面覆盖窃取）；引导弹窗以“Google Informa:”前缀冒充系统/Google 通知；布局内残留 title “Outback Cupom” 另一身份；获权后弹出伪系统“Economia de Energia / Bateria … 32% de economia”省电提示掩盖真实动作；类名/成员名混淆为 vvvvv0、_vvvv2 等无语义标识。 |
| 无障碍服务类名 | `.execucoes` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | igr.manobom.inla.main（Launcher Activity，标题 Quem te visitou）+ 布局 pismaim | main._activity_create 冷启动 onCreate 时 LoadLayout("pismaim") | 原生Activity | **原文**：ATIVAR RECURSO<br>**译注**：激活功能（页面唯一可点击的按钮标签，上方为大图标 icone_instaaaa.jpg） | 只能点击“ATIVAR RECURSO”，页面无取消/跳过/关闭按钮 | `igr.manobom.inla.main#_activity_create / assets/pismaim.bal（Label2.text=ATIVAR RECURSO）` |
| 2 | 引导说明页 | 原生 AlertDialog（Common.Msgbox，CSBuilder 富文本，绿字居中） | 点击 Label2 → main._label2_click → main._vvvvvvvvvvvvvvvvv3() | 原生Dialog | **原文**：Configurações >  Acessibilidade > <recurso><br>**译注**：设置 > 无障碍 > （本服务名）—— 分步告知用户应到系统设置里打开该无障碍服务 | 点击确认后继续；弹窗仅有确认按钮，无取消/跳过 | `igr.manobom.inla.main#_vvvvvvvvvvvvvvvvv3（CSBuilder.Append("Configurações > ") … " Acessibilidade > "）` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS + 叠加 Toast/TTS | 同一 _label2_click 内 IntentWrapper.Initialize("android.settings.ACCESSIBILITY_SETTINGS") + Common.StartActivity，并置 starter._vvvv2="PedeNovamente" | 系统无障碍页 | **原文**：Google Informa: Ative a permissão para <recurso><br>**译注**：谷歌提示：请激活该权限以使用（服务名）——以 Google/系统名义催促用户开启无障碍 | 在系统无障碍列表中找到并打开“Quem te visitou”开关；同时 TTS 语音朗读同一催促语 | `igr.manobom.inla.main#_label2_click / igr.manobom.inla.main#_vvvvvvvvvvvvvvvvv4` |
| 4 | 拒权反馈循环 | main 重新回到前台并再次拉起系统无障碍页 | 用户从设置页返回触发 main._activity_resume，检测 starter._vvvv2=="PedeNovamente" | 系统无障碍页 | **原文**：Google Informa: Ative a permissão para <recurso><br>**译注**：每次返回都再次震动、弹说明、重新跳无障碍设置，形成无法退出的重跳循环 | 无退出路径，只能再次进入设置开启权限 | `igr.manobom.inla.main#_activity_resume` |
| 5 | 拒权反馈循环 | 后台服务 starter（Timer1, 1000ms）→ ResumableSub_xSubirManoAPermissao | starter._service_create/_service_start → _vvvvvvvvvvvvvvvvv6 在存储权限未授予或无障碍服务未运行（Common.IsPaused(execucoes)）时启用 Timer1；_timer1_tick 计数到阈值即调用 _vvvvvvvvvvvvvvvvv0 | 系统无障碍页 | **原文**：Ative o recurso [<recurso>]<br>**译注**：请激活功能（服务名）——每秒级定时反复拉起无障碍设置页并震动、启动 startertwo 服务 | 强制反复弹出无障碍设置，无跳过选项 | `igr.manobom.inla.starter#_timer1_tick / igr.manobom.inla.starter$ResumableSub_xSubirManoAPermissao#resume` |
| 6 | 获权后动作 | 无障碍服务 igr.manobom.inla.execucoes（监听切包 + 覆盖层） | 获权后 execucoes._listener_accesspackageatual 检测到包名变化（如银行 App 打开） | 悬浮窗Overlay | **原文**：Atenção<br><br><br><br><br><br> Ativado    Economia de Energia / Bateria                     <br><br><br><br><br><br>Atenção: é recomendado utilizar um brilho de tela mais baixo para melhorar o desempenho do recurso de economia                          <br><br><br><br><br><br>             Seu consumo de energia foi melhorado em 32% de economia<br>**译注**：注意：已激活“节能/电池”模式；建议降低屏幕亮度以提升节能效果；您的电量消耗已优化 32%——用伪造的系统省电提示掩盖随后拉起银行钓鱼覆盖页并回桌面 | 无操作，用户被 HOME 强制切回桌面；期间调用 GLOBAL_ACTION_BACK(1)/HOME(2) 阻止停留在系统设置页撤权 | `igr.manobom.inla.execucoes#_listener_accesspackageatual / igr.manobom.inla.execucoes#_listener_accesshierarchi / igr.manobom.inla.execucoes#_xchamadordosverlayes_a` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动主界面（Activity main / 布局 pismaim）：唯一按钮 Label2 文案“ATIVAR RECURSO”，大图标 icone_instaaaa.jpg，无任何说明文字
- main._vvvvvvvvvvvvvvvvv3 弹出的原生 AlertDialog（Common.Msgbox + CSBuilder 富文本）：“Configurações > Acessibilidade > <服务名>”路径教学
- 跳转系统无障碍页瞬间叠加的 Toast（main._vvvvvvvvvvvvvvvvv4）："Google Informa: Ative a permissão para <服务名>"，并同步 TTS 语音朗读
- starter$ResumableSub_xSubirManoAPermissao 定时循环中的 Toast："Ative o recurso [<服务名>]"
- 系统无障碍服务列表条目描述（res/xml-v13/teste2 → @string/descricao_brasil1）：Quem te visitou / Ativando o recurso … / Aplicativo oficial …
- 获权后 execucoes 弹出的自定义 Toast 覆盖层：伪系统“Economia de Energia / Bateria … 32% de economia”

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | Quem te visitou<br>Ativando o recurso você tem ativação do componente. <br>* Funcional em toda nossa rede <br>* Em caso de duvidas procure nosso suporte <br>* Aplicativo oficial <br>* Precisamos da permissão para que o algoritimo seja realizado | 谁访问了你。激活该功能即完成组件激活。* 在我们整个网络内有效 * 如有疑问请联系我们的支持 * 官方应用 * 我们需要该权限以运行该算法 | `res/values/strings.xml → descricao_brasil1（被 res/xml-v13/teste2 android:description 引用）` | 假反诈安全 |
| pt | ATIVAR RECURSO | 激活功能 | `assets/pismaim.bal → Label2.text` | 清理工具伪装 |
| pt | Configurações >  Acessibilidade > <recurso> | 设置 > 无障碍 > （本服务名） | `igr.manobom.inla.main#_vvvvvvvvvvvvvvvvv3 硬编码 CSBuilder` | 受限设置分步教学 |
| pt | Google Informa: Ative a permissão para <recurso> | 谷歌提示：请激活该权限以使用（服务名） | `igr.manobom.inla.main#_vvvvvvvvvvvvvvvvv4 硬编码 Toast` | 假更新 |
| pt | Ative o recurso [<recurso>] | 请激活功能（服务名） | `igr.manobom.inla.starter$ResumableSub_xSubirManoAPermissao#resume 硬编码 Toast` | 教唆忽视警告 |
| pt | Atenção<br><br><br><br><br><br> Ativado    Economia de Energia / Bateria                     <br><br><br><br><br><br>Atenção: é recomendado utilizar um brilho de tela mais baixo para melhorar o desempenho do recurso de economia                          <br><br><br><br><br><br>             Seu consumo de energia foi melhorado em 32% de economia | 注意：已激活“节能/电池”；建议降低屏幕亮度以提升节能效果；您的电量消耗已优化 32% | `igr.manobom.inla.execucoes#_listener_accesspackageatual 硬编码 _showcustomtoast_a 文本（大量换行占位）` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：两条闭环：① main._activity_resume 检测 starter._vvvv2=="PedeNovamente" 时立刻再次 StartActivity(ACCESSIBILITY_SETTINGS) 并重新弹 MsgBox/Toast/TTS；② starter 服务的 Timer1(1000ms) 在无障碍服务未运行或存储权限未授予时持续计数并调用 ResumableSub_xSubirManoAPermissao，反复跳无障碍设置页 + Toast「Ative o recurso [...]」，另有 startertwo 并行同一逻辑。
- **遮罩叠层 / 高仿系统设置页**：未发现高仿系统无障碍开关页或覆盖设置页的半透明遮罩；但跳转瞬间以 Toast「Google Informa: …」+TTS 伪造系统/Google 通知叠加在系统设置页之上；获权后改用自定义 Toast 悬浮窗伪装系统省电提示。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：有：execucoes 服务在切包时立即 GLOBAL_ACTION_HOME(2) 把用户顶回桌面，并在层级监听中调用 PerformGlobalAction(1)=GLOBAL_ACTION_BACK 拦截返回，配合 _listener_accesspackageatual 的伪省电提示阻止用户停留在系统设置页撤销无障碍授权；main 在 starter._vvvv2=="quitadoporra" 时也强制回桌面。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：Hook ActivityManager/Intent 拉起：捕获 Intent action == "android.settings.ACCESSIBILITY_SETTINGS"（来源 igr.manobom.inla.main._label2_click 与 starter$ResumableSub_xSubirManoAPermissao.resume）；同时可挂钩 main.onCreate 加载布局 pismaim 后首个画面，二者基本同时出现。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：全部引导文案为原生文本与 Toast（可 UTG 直接提取）。仅注意服务显示名与后续银行覆盖页文案由远端配置/服务器下发，若需证明具体伪装对象需结合运行期网络与覆盖页截图。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（MsgBox 路径教学）** | igr.manobom.inla.main 前台 + 原生 AlertDialog，绿字文本以「Configurações >」开头、含「Acessibilidade」 | 该弹窗是唯一以文字形式明确教用户去无障碍设置的节点，且无可取消按钮，可直接证明强制分步教学 | 弹窗文本含 Configurações > Acessibilidade；弹窗无取消/跳过按钮；同一屏叠加 Toast「Google Informa:」 |
| **系统无障碍服务列表项** | Settings 无障碍列表中出现「Quem te visitou」，描述为 descricao_brasil1 多行文本（含 Aplicativo oficial / Precisamos da permissão） | 系统侧服务名与描述是用户实际看到的授权对象，可与桌面名对照确认身份错配且无功能说明真实性 | 服务条目名 = Quem te visitou；描述含 'Ativando o recurso você tem ativação do componente'；无 android:label 单独命名，与 App 名一致 |
| **拒权返回后的重跳循环页** | 连续多次 ACCESSIBILITY_SETTINGS 拉起（间隔约 1s 或紧随 onResume），伴随震动与 Toast「Ative o recurso」 | 循环重跳是判定强制而非良性引导的决定性运行期信号，静态已确认，UTG 可量化其频率与不可退出性 | 1 秒级重复 startActivity(ACCESSIBILITY_SETTINGS)；onResume 后立即再次跳转；Toast 文本 Ative o recurso [...] 重复出现 |
| **获权后伪系统省电提示页** | 自定义 Toast/悬浮窗，文本含 Economia de Energia / Bateria、32% de economia，随后回到 Launcher | 证明获权后立即转入伪装行为并配合反撤权（HOME/BACK），可用于区分“真实功能型”无障碍应用 | 含 'Economia de Energia' / '32% de economia' 的 Toast；紧接 HOME 回到桌面；无障碍服务已 enabled 状态 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `igr.manobom.inla.main#_activity_create`
- `igr.manobom.inla.main#_label2_click`
- `igr.manobom.inla.main#_vvvvvvvvvvvvvvvvv3`
- `igr.manobom.inla.main#_activity_resume`
- `igr.manobom.inla.starter$ResumableSub_xSubirManoAPermissao#resume`
- `igr.manobom.inla.execucoes#_listener_accesspackageatual`
- `res/values/strings.xml#L3-L8`
- `res/xml-v13/teste2#L2`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（B4A 未加壳，dex 可完整反编译，跳转与文案均可静态还原）。核心结论：

**引导链（纯运行期 UTG 视角）**
1. **冷启动**：`main._activity_create` 加载布局 `pismaim`（`assets/pismaim.bal`），界面只有一个大图标 `icone_instaaaa.jpg` 和文字按钮 **“ATIVAR RECURSO”**，没有关闭或跳过入口。
2. **点击即教学**：`main._label2_click` 先震动，再弹出 `Common.Msgbox`（`_vvvvvvvvvvvvvvvvv3`，CSBuilder 绿字居中）逐行显示 `Configurações > Acessibilidade > <服务名>` 的分步路径。
3. **跳转 + 伪造系统提示**：同一方法立刻 `Initialize("android.settings.ACCESSIBILITY_SETTINGS")` 拉起系统无障碍页，并叠加 **Toast「Google Informa: Ative a permissão para …」** 和 TTS 语音朗读，把自家诱导伪装成 Google 系统通知。
4. **拒绝后循环**：跳转前把 `starter._vvvv2="PedeNovamente"`；`main._activity_resume` 一旦检测到该值就**再次跳转无障碍设置**（返回/退出即重跳）；同时 `starter` 服务用 1000ms `Timer1` 反复走 `ResumableSub_xSubirManoAPermissao`，先索要存储权限再跳无障碍页 + Toast「Ative o recurso [...]」，形成后台定时拉起。
5. **获权后反撤权**：`execucoes` 无障碍服务在切包时弹「Atenção … Ativado Economia de Energia / Bateria … 32% de economia」伪系统省电提示后 `GLOBAL_ACTION_HOME` 回桌面，并用 `GLOBAL_ACTION_BACK` 等阻止用户停留在设置页撤权。
6. **身份**：桌面名与服务名均为“Quem te visitou”（访客查看类应用），系统无障碍列表 `android:description` 用 `descricao_brasil1` 宣称“应用官方/全网可用/需要该权限以运行算法”，实际服务做银行界面覆盖与窃取（basbanke 家族），属身份与功能错配。
7. **无** `ACTION_APPLICATION_DETAILS_SETTINGS`/受限设置分步教学，无 WebView/HTML 引导页，引导载体全为原生 MsgBox + Toast + TTS + 系统无障碍页。

```json
{
  "static_visibility": "clear",
  "visibility_note": "应用为 B4A 开发且未加壳，classes.dex 完整反编译，跳转 Intent、Toast/MsgBox 文案、无障碍配置 res/xml-v13/teste2 与 res/values/strings.xml 均可静态还原；仅服务显示名取自远端配置变量 starter._vvv1 与后续银行覆盖页文案由服务器下发，不影响 UTG 引导链判定。",
  "summary_one_liner": "以“Quem te visitou”访客查看器为壳，冷启动单按钮“ATIVAR RECURSO”配合 MsgBox 路径教学、伪造“Google Informa”Toast+TTS 直跳系统无障碍页，并靠 onResume 与 1 秒 Timer 循环重跳直至开启，获权后弹伪系统省电提示并 GLOBAL_ACTION_HOME/BACK 反撤权。",
  "disguise_identity": {
    "app_display_name": "Quem te visitou",
    "claimed_brand_or_persona": "“Quem te visitou”访客查看类工具（描述中自称“Aplicativo oficial / Funcional em toda nossa rede”，提示中冒充 Google 系统通知）",
    "a11y_service_label": "Quem te visitou（服务未设 android:label，沿用应用名；描述为 strings.xml 的 descricao_brasil1）",
    "identity_mismatch": true,
    "obfuscation_tricks": "服务名与功能完全错配（访客查看器 vs 银行界面覆盖窃取）；引导弹窗以“Google Informa:”前缀冒充系统/Google 通知；布局内残留 title “Outback Cupom” 另一身份；获权后弹出伪系统“Economia de Energia / Bateria … 32% de economia”省电提示掩盖真实动作；类名/成员名混淆为 vvvvv0、_vvvv2 等无语义标识。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "igr.manobom.inla.main（Launcher Activity，标题 Quem te visitou）+ 布局 pismaim",
      "trigger_event": "main._activity_create 冷启动 onCreate 时 LoadLayout(\"pismaim\")",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "ATIVAR RECURSO",
      "shown_text_zh": "激活功能（页面唯一可点击的按钮标签，上方为大图标 icone_instaaaa.jpg）",
      "user_action_requested": "只能点击“ATIVAR RECURSO”，页面无取消/跳过/关闭按钮",
      "code_anchor": "igr.manobom.inla.main#_activity_create / assets/pismaim.bal（Label2.text=ATIVAR RECURSO）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "原生 AlertDialog（Common.Msgbox，CSBuilder 富文本，绿字居中）",
      "trigger_event": "点击 Label2 → main._label2_click → main._vvvvvvvvvvvvvvvvv3()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Configurações >  Acessibilidade > <recurso>",
      "shown_text_zh": "设置 > 无障碍 > （本服务名）—— 分步告知用户应到系统设置里打开该无障碍服务",
      "user_action_requested": "点击确认后继续；弹窗仅有确认按钮，无取消/跳过",
      "code_anchor": "igr.manobom.inla.main#_vvvvvvvvvvvvvvvvv3（CSBuilder.Append(\"Configurações > \") … \" Acessibilidade > \"）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS + 叠加 Toast/TTS",
      "trigger_event": "同一 _label2_click 内 IntentWrapper.Initialize(\"android.settings.ACCESSIBILITY_SETTINGS\") + Common.StartActivity，并置 starter._vvvv2=\"PedeNovamente\"",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Informa: Ative a permissão para <recurso>",
      "shown_text_zh": "谷歌提示：请激活该权限以使用（服务名）——以 Google/系统名义催促用户开启无障碍",
      "user_action_requested": "在系统无障碍列表中找到并打开“Quem te visitou”开关；同时 TTS 语音朗读同一催促语",
      "code_anchor": "igr.manobom.inla.main#_label2_click / igr.manobom.inla.main#_vvvvvvvvvvvvvvvvv4"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "main 重新回到前台并再次拉起系统无障碍页",
      "trigger_event": "用户从设置页返回触发 main._activity_resume，检测 starter._vvvv2==\"PedeNovamente\"",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Informa: Ative a permissão para <recurso>",
      "shown_text_zh": "每次返回都再次震动、弹说明、重新跳无障碍设置，形成无法退出的重跳循环",
      "user_action_requested": "无退出路径，只能再次进入设置开启权限",
      "code_anchor": "igr.manobom.inla.main#_activity_resume"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "后台服务 starter（Timer1, 1000ms）→ ResumableSub_xSubirManoAPermissao",
      "trigger_event": "starter._service_create/_service_start → _vvvvvvvvvvvvvvvvv6 在存储权限未授予或无障碍服务未运行（Common.IsPaused(execucoes)）时启用 Timer1；_timer1_tick 计数到阈值即调用 _vvvvvvvvvvvvvvvvv0",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Ative o recurso [<recurso>]",
      "shown_text_zh": "请激活功能（服务名）——每秒级定时反复拉起无障碍设置页并震动、启动 startertwo 服务",
      "user_action_requested": "强制反复弹出无障碍设置，无跳过选项",
      "code_anchor": "igr.manobom.inla.starter#_timer1_tick / igr.manobom.inla.starter$ResumableSub_xSubirManoAPermissao#resume"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 igr.manobom.inla.execucoes（监听切包 + 覆盖层）",
      "trigger_event": "获权后 execucoes._listener_accesspackageatual 检测到包名变化（如银行 App 打开）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Atenção\n\n\n\n\n\n Ativado    Economia de Energia / Bateria                     \n\n\n\n\n\nAtenção: é recomendado utilizar um brilho de tela mais baixo para melhorar o desempenho do recurso de economia                          \n\n\n\n\n\n             Seu consumo de energia foi melhorado em 32% de economia",
      "shown_text_zh": "注意：已激活“节能/电池”模式；建议降低屏幕亮度以提升节能效果；您的电量消耗已优化 32%——用伪造的系统省电提示掩盖随后拉起银行钓鱼覆盖页并回桌面",
      "user_action_requested": "无操作，用户被 HOME 强制切回桌面；期间调用 GLOBAL_ACTION_BACK(1)/HOME(2) 阻止停留在系统设置页撤权",
      "code_anchor": "igr.manobom.inla.execucoes#_listener_accesspackageatual / igr.manobom.inla.execucoes#_listener_accesshierarchi / igr.manobom.inla.execucoes#_xchamadordosverlayes_a"
    }
  ],
  "text_presentation_locations": [
    "冷启动主界面（Activity main / 布局 pismaim）：唯一按钮 Label2 文案“ATIVAR RECURSO”，大图标 icone_instaaaa.jpg，无任何说明文字",
    "main._vvvvvvvvvvvvvvvvv3 弹出的原生 AlertDialog（Common.Msgbox + CSBuilder 富文本）：“Configurações > Acessibilidade > <服务名>”路径教学",
    "跳转系统无障碍页瞬间叠加的 Toast（main._vvvvvvvvvvvvvvvvv4）：\"Google Informa: Ative a permissão para <服务名>\"，并同步 TTS 语音朗读",
    "starter$ResumableSub_xSubirManoAPermissao 定时循环中的 Toast：\"Ative o recurso [<服务名>]\"",
    "系统无障碍服务列表条目描述（res/xml-v13/teste2 → @string/descricao_brasil1）：Quem te visitou / Ativando o recurso … / Aplicativo oficial …",
    "获权后 execucoes 弹出的自定义 Toast 覆盖层：伪系统“Economia de Energia / Bateria … 32% de economia”"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "Quem te visitou\nAtivando o recurso você tem ativação do componente. \n* Funcional em toda nossa rede \n* Em caso de duvidas procure nosso suporte \n* Aplicativo oficial \n* Precisamos da permissão para que o algoritimo seja realizado",
      "text_zh": "谁访问了你。激活该功能即完成组件激活。* 在我们整个网络内有效 * 如有疑问请联系我们的支持 * 官方应用 * 我们需要该权限以运行该算法",
      "source_location": "res/values/strings.xml → descricao_brasil1（被 res/xml-v13/teste2 android:description 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "pt",
      "text_verbatim": "ATIVAR RECURSO",
      "text_zh": "激活功能",
      "source_location": "assets/pismaim.bal → Label2.text",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "pt",
      "text_verbatim": "Configurações >  Acessibilidade > <recurso>",
      "text_zh": "设置 > 无障碍 > （本服务名）",
      "source_location": "igr.manobom.inla.main#_vvvvvvvvvvvvvvvvv3 硬编码 CSBuilder",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Google Informa: Ative a permissão para <recurso>",
      "text_zh": "谷歌提示：请激活该权限以使用（服务名）",
      "source_location": "igr.manobom.inla.main#_vvvvvvvvvvvvvvvvv4 硬编码 Toast",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "pt",
      "text_verbatim": "Ative o recurso [<recurso>]",
      "text_zh": "请激活功能（服务名）",
      "source_location": "igr.manobom.inla.starter$ResumableSub_xSubirManoAPermissao#resume 硬编码 Toast",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "pt",
      "text_verbatim": "Atenção\n\n\n\n\n\n Ativado    Economia de Energia / Bateria                     \n\n\n\n\n\nAtenção: é recomendado utilizar um brilho de tela mais baixo para melhorar o desempenho do recurso de economia                          \n\n\n\n\n\n             Seu consumo de energia foi melhorado em 32% de economia",
      "text_zh": "注意：已激活“节能/电池”；建议降低屏幕亮度以提升节能效果；您的电量消耗已优化 32%",
      "source_location": "igr.manobom.inla.execucoes#_listener_accesspackageatual 硬编码 _showcustomtoast_a 文本（大量换行占位）",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "两条闭环：① main._activity_resume 检测 starter._vvvv2==\"PedeNovamente\" 时立刻再次 StartActivity(ACCESSIBILITY_SETTINGS) 并重新弹 MsgBox/Toast/TTS；② starter 服务的 Timer1(1000ms) 在无障碍服务未运行或存储权限未授予时持续计数并调用 ResumableSub_xSubirManoAPermissao，反复跳无障碍设置页 + Toast「Ative o recurso [...]」，另有 startertwo 并行同一逻辑。",
    "overlay_or_fake_settings": "未发现高仿系统无障碍开关页或覆盖设置页的半透明遮罩；但跳转瞬间以 Toast「Google Informa: …」+TTS 伪造系统/Google 通知叠加在系统设置页之上；获权后改用自定义 Toast 悬浮窗伪装系统省电提示。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "有：execucoes 服务在切包时立即 GLOBAL_ACTION_HOME(2) 把用户顶回桌面，并在层级监听中调用 PerformGlobalAction(1)=GLOBAL_ACTION_BACK 拦截返回，配合 _listener_accesspackageatual 的伪省电提示阻止用户停留在系统设置页撤销无障碍授权；main 在 starter._vvvv2==\"quitadoporra\" 时也强制回桌面。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "Hook ActivityManager/Intent 拉起：捕获 Intent action == \"android.settings.ACCESSIBILITY_SETTINGS\"（来源 igr.manobom.inla.main._label2_click 与 starter$ResumableSub_xSubirManoAPermissao.resume）；同时可挂钩 main.onCreate 加载布局 pismaim 后首个画面，二者基本同时出现。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（MsgBox 路径教学）",
        "page_identifier": "igr.manobom.inla.main 前台 + 原生 AlertDialog，绿字文本以「Configurações >」开头、含「Acessibilidade」",
        "why_most_useful": "该弹窗是唯一以文字形式明确教用户去无障碍设置的节点，且无可取消按钮，可直接证明强制分步教学",
        "observable_utg_signals": ["弹窗文本含 Configurações > Acessibilidade", "弹窗无取消/跳过按钮", "同一屏叠加 Toast「Google Informa:」"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中出现「Quem te visitou」，描述为 descricao_brasil1 多行文本（含 Aplicativo oficial / Precisamos da permissão）",
        "why_most_useful": "系统侧服务名与描述是用户实际看到的授权对象，可与桌面名对照确认身份错配且无功能说明真实性",
        "observable_utg_signals": ["服务条目名 = Quem te visitou", "描述含 'Ativando o recurso você tem ativação do componente'", "无 android:label 单独命名，与 App 名一致"]
      },
      {
        "page_role": "拒权返回后的重跳循环页",
        "page_identifier": "连续多次 ACCESSIBILITY_SETTINGS 拉起（间隔约 1s 或紧随 onResume），伴随震动与 Toast「Ative o recurso」",
        "why_most_useful": "循环重跳是判定强制而非良性引导的决定性运行期信号，静态已确认，UTG 可量化其频率与不可退出性",
        "observable_utg_signals": ["1 秒级重复 startActivity(ACCESSIBILITY_SETTINGS)", "onResume 后立即再次跳转", "Toast 文本 Ative o recurso [...] 重复出现"]
      },
      {
        "page_role": "获权后伪系统省电提示页",
        "page_identifier": "自定义 Toast/悬浮窗，文本含 Economia de Energia / Bateria、32% de economia，随后回到 Launcher",
        "why_most_useful": "证明获权后立即转入伪装行为并配合反撤权（HOME/BACK），可用于区分“真实功能型”无障碍应用",
        "observable_utg_signals": ["含 'Economia de Energia' / '32% de economia' 的 Toast", "紧接 HOME 回到桌面", "无障碍服务已 enabled 状态"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：全部引导文案为原生文本与 Toast（可 UTG 直接提取）。仅注意服务显示名与后续银行覆盖页文案由远端配置/服务器下发，若需证明具体伪装对象需结合运行期网络与覆盖页截图。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "igr.manobom.inla.main#_activity_create",
    "igr.manobom.inla.main#_label2_click",
    "igr.manobom.inla.main#_vvvvvvvvvvvvvvvvv3",
    "igr.manobom.inla.main#_activity_resume",
    "igr.manobom.inla.starter$ResumableSub_xSubirManoAPermissao#resume",
    "igr.manobom.inla.execucoes#_listener_accesspackageatual",
    "res/values/strings.xml#L3-L8",
    "res/xml-v13/teste2#L2"
  ]
}
```

补充说明（未决/边界）：`starter._vvv1`（Toast 与教学文本中插入的服务名）与 `_vvv7` 服务器地址来自远端配置，具体伪装银行集合与覆盖页文案需运行期抓包验证；本轮受效率约束未展开 `execucoes` 覆盖层绘制细节，仅确认其反撤权与伪省电提示行为。

</details>

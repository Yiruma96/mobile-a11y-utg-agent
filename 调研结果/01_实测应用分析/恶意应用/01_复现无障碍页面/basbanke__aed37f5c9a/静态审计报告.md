# MR_166__aed37f5c9a｜basbanke — Max Cupons

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：169.8s

## 1. 一句话核心结论

- **核心申请方式**：伪装成优惠券应用 Max Cupons 的巴西银行木马，在首屏按钮"Ativar Cupom!!"点击后弹不可取消的原生 Msgbox 教用户进入"设置>无障碍"，随即跳转系统无障碍页，并在 onResume 中检测状态标记无休止重弹重跳直至授权，无障碍服务名与说明均沿用优惠券品牌话术掩盖其银行仿冒点击能力。
- **静态可见性说明**：应用未加壳，Manifest、res/xml/teste2、res/values/strings.xml、B4A 布局 pismaim.bal 与 DEX 全部静态可读，跳转链路（ACCESSIBILITY_SETTINGS）与 onResume 死循环逻辑完全可见；但 Msgbox 提示正文的多数文案（starter._v5/_v6/_v7/_v0/_vvv1）以字节数组存储并经 BA.__b(byte[],int) 运行期还原，逐字内容无法静态还原；首屏引导 WebView 页面由远端 http://80.82.67.246/MaxCupons/ 下发，包内无 HTML 副本。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `aed37f5c9ac97d0ed484a2b3cd23b04c943326d2ffe6472b0e01e03bc616844a` |
| 包名 / 年份 | `pine.coyzinhu.infee` / 2019 |
| 家族 / 品类 | **basbanke**（同池样本数：10） |
| 原始来源标识 | https://gbhackers.com/new-android-malware-basbanke/ |
| 桌面显示名 | Max Cupons |
| 引导页宣称品牌/身份 | Max Cupons（自称"Aplicativo oficial da rede Max Cupons"的优惠券/票券返利网络） |
| 系统无障碍列表服务名 | Max Cupons |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置 res/xml/teste2 仅声明 android:description，未设置 android:label，使系统无障碍列表直接显示应用名 Max Cupons；description 用多行营销条目（每周多张票券、20R$~190R$ 折扣、官方支持）淹没真正的权限诉求；所有引导文案以字节数组+BA.__b 运行期解密，静态不可读；多个 Activity 统一 android:label="Max Cupons"，但类名（bb、santinha、itaunormal、cefzinha 等）实为巴西各银行仿冒页；无 activity-alias 多别名与同形字技巧。 |
| 无障碍服务类名 | `.execucoes` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | pine.coyzinhu.infee.main（LAUNCHER Activity，excludeFromRecents=true）+ 布局 pismaim 内 WebView1 / Label1 / Label2 | onCreate → _activity_create：LoadLayout("pismaim")、WebView1.LoadUrl 远端页面、httpjob 向 /Android/ConexaoCentral.php 上报 data=LERPIS\|aaa | 远端WebView | **原文**：Max Cupons Carregando... / Ativar Cupom!!<br>**译注**：标签1 显示"Max Cupons 加载中..."，标签2（唯一按钮）显示"激活优惠券!!" | 等待远端 WebView 加载完成，并点击"Ativar Cupom!!"按钮；此页无跳过入口 | `pine.coyzinhu.infee.main._activity_create / assets/pismaim.bal` |
| 2 | 引导说明页 | B4A Msgbox（原生 AlertDialog，标题为空串） | main._label2_click：判断 Label2 文本=="Ativar Cupom!!" → 震动 30ms → 调用 _vvvvvvvvvvvvvvvvv3() 构建 CSBuilder 文案 → Common.Msgbox | 原生Dialog | **原文**：Configurações >  Acessibilidade ><br>**译注**：弹窗正文以居中白色大字逐段列出解密后的营销话术（starter._v5/_v6/_v7/_v0），绿色高亮固定教学行"设置 > 无障碍 > <服务名>"，提示用户到系统设置里开启该服务 | 只能点击确定（Msgbox 无取消/跳过按钮），按提示前往系统设置 | `pine.coyzinhu.infee.main._label2_click / pine.coyzinhu.infee.main._vvvvvvvvvvvvvvvvv3` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | 紧接 Msgbox 之后在同一方法内 IntentWrapper.Initialize("android.settings.ACCESSIBILITY_SETTINGS") + Common.StartActivity；并置 starter._vvv2="PedeNovamente"、StartService(starter)、CallSubNew("xxxxxxideAplicationBuniteixom") | 系统无障碍页 | 无 | 在系统无障碍列表中手动开启 Max Cupons 服务（应用侧无引导遮罩、无高仿开关页） | `pine.coyzinhu.infee.main._label2_click` |
| 4 | 拒权反馈循环 | main.onResume → _activity_resume（状态标记 starter._vvv2 == "PedeNovamente"） | 用户从系统设置页返回触发 onResume；分支内再次震动、再次 Common.Msgbox、再次 StartActivity(ACCESSIBILITY_SETTINGS)、再执行两次 _vvvvvvvvvvvvvvvvv4(true)、StartService(starter)、CallSubNew("xxxxxxideAplicationBuniteixom") | 原生Dialog | **原文**：Configurações >  Acessibilidade ><br>**译注**：与步骤 2 完全相同的弹窗与教学行，用户每返回一次即重弹一次并再次跳转无障碍设置 | 无取消选项，只能再次前往设置或按 Home 离开；状态不被重置，构成死循环 | `pine.coyzinhu.infee.main._activity_resume` |
| 5 | 获权后动作 | pine.coyzinhu.infee.execucoes（AccessibilityService）+ itaunormal/santinha/bradescoxim/bb/cefzinha/brasilia1/itaucardbom 等仿冒银行 Activity | 服务连接后 onAccessibilityEvent/_listener_accesshierarchi/_astream_newdata 监听前台窗口，按文本或 ViewId 查找节点并 PerformNodeActionOnViewWithArgs / xClicaPorIdGerado 自动点击；WATCH_PKG_INSTALLER 监听安装器；必要时 PerformGlobalAction(BACK/HOME/RECENTS) 阻挠撤权；状态置 quitadoporra 时跳 CATEGORY_HOME 回桌面 | 悬浮窗Overlay | 无 | 用户在仿冒银行页面输入账号、密码、卡号等凭证 | `pine.coyzinhu.infee.execucoes._listener_accesshierarchi / pine.coyzinhu.infee.execucoes._astream_newdata` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：res/xml/teste2 引用 @string/descricao_brasil1，未设 android:label，列表名回落到应用名 "Max Cupons"
- 系统无障碍服务详情说明（点开服务后展开的说明正文）：res/values/strings.xml 中 descricao_brasil1 的多行优惠券营销话术
- 应用首屏 main（pismaim.bal）：Label1 "Max Cupons Carregando..."、Label2 按钮 "Ativar Cupom!!"
- 应用首屏 WebView1：远端 http://80.82.67.246/MaxCupons/ 页面（包内无副本）
- 点击"Ativar Cupom!!"后弹出的 B4A Msgbox 原生 AlertDialog（标题空串、无取消按钮），内含解密话术与"设置 > 无障碍 > 服务名"教学行
- 从系统设置返回后由 main._activity_resume 重复弹出的同一 Msgbox
- 仿冒银行页面：assets/ita1.bal、santa1.bal、brada1.bal、bb1.bal、cef_ads.png 等布局与图片资源

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | Max Cupons<br>Ativando o recurso você tem ativação do seu ticket. <br>* Varios ticket por semana <br>* Descontos de 20R$ até 190R$ <br>* Em caso de duvidas procure nosso suporte <br>* Aplicativo oficial da rede Max Cupons <br>* Precisamos da permissão para evitar que seu ticket seja usado por outros clientes | Max Cupons<br>开启该功能后您的票券即被激活。<br>* 每周多张票券<br>* 20R$ 至 190R$ 的折扣<br>* 如有疑问请联系我们的客服<br>* Max Cupons 网络官方应用<br>* 我们需要该权限，以防您的票券被其他客户使用 | `res/values/strings.xml key=descricao_brasil1（由 res/xml/teste2 的 android:description 引用）` | 隐私承诺 |
| pt | Ativar Cupom!! | 激活优惠券!! | `assets/pismaim.bal 中 Label2 的 text 属性（main._label2_click 以该文本做分支判断）` | 良性透明说明 |
| pt | Max Cupons Carregando... | Max Cupons 加载中... | `assets/pismaim.bal 中 Label1 的 text 属性` | 未知 |
| pt | Configurações >  Acessibilidade > | 设置 > 无障碍 > （后接运行期解密的无障碍服务名） | `pine.coyzinhu.infee.main._vvvvvvvvvvvvvvvvv3 中硬编码的两段字面量` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：main._label2_click 跳转前把状态置为 "PedeNovamente"；用户每次从系统设置返回触发 onResume → _activity_resume 检测到该标记即重新弹同一 Msgbox 并再次 StartActivity(ACCESSIBILITY_SETTINGS)，同时重复调用 _vvvvvvvvvvvvvvvvv4(true) 与 StartService(starter)，标记不清零，形成无限重弹重跳；状态为 "quitadoporra" 时改为跳 CATEGORY_HOME 回桌面。
- **遮罩叠层 / 高仿系统设置页**：未发现应用自绘的引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；叠加行为发生在授权之后，由无障碍服务以节点操作/悬浮窗口叠加在银行 App 与系统设置之上（A11Y_OVERLAY），而非申请阶段的视觉遮罩。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无障碍服务 execucoes 具备 PerformGlobalAction（GLOBAL_BACK/GLOBAL_HOME/GLOBAL_RECENTS）与 WATCH_PKG_INSTALLER 能力，可在设置页用全局返回/主页动作阻止用户关闭服务或卸载；状态标记 "quitadoporra" 触发 ACTION_MAIN+CATEGORY_HOME 强制回桌面。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到应用发起 Intent action=android.settings.ACCESSIBILITY_SETTINGS（或前台切换为 Settings 的无障碍列表页）的瞬间启动 UTG 采集；同时对该 Activity 的 onResume 做一次回归采集——用户按返回键后 1 秒内必然再次弹窗并再次跳转，这是该样本最独特的循环特征。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导弹窗正文大部分来自运行期解密（starter._v5/_v6/_v7/_v0/_vvv1），静态抓不到逐字文本，纯静态审查只能看到"Configurações > Acessibilidade >"骨架；首屏 WebView 内容来自远端 80.82.67.246，包内无 HTML，若服务端按环境（地区/设备/时间）返回不同页面，UTG 需在应用真实运行网络条件下采集。此外应用以 targetSdkVersion=26 运行，Android 13 受限设置分步教学不适用，切勿因未捕获到该环节而误判为良性。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **点击激活按钮后弹出的不可取消引导弹窗页** | 包名 pine.coyzinhu.infee、Activity .main 上的原生 AlertDialog，标题为空，正文含绿色"Configurações > Acessibilidade"行，仅一个确定按钮 | 这是唯一把"优惠券"话术与无障碍授权诉求绑定呈现给用户的界面，其文案与无取消按钮结构是判定诱导与强迫的直接证据 | 弹窗节点数量与是否存在取消/关闭按钮；正文是否含"Acessibilidade"/"Configurações"教学行；弹窗出现时后台 Activity 仍为 .main 而非系统设置页 |
| **从系统设置返回后 1 秒内的重弹重跳循环页** | 同一 .main 上重复出现的 AlertDialog，且紧随其后前台切至 Settings 无障碍列表 | 重弹+重跳的闭环是该应用强迫授权而非一次性提示的决定性区别，单次截图无法体现 | 同一弹窗在用户返回后再次出现的次数；弹窗与 Settings 页面交替切换的时序；是否存在退出/跳过路径导致不再弹窗 |
| **系统无障碍服务列表项与说明详情** | Settings 无障碍列表中的 "Max Cupons" 条目，点开后说明为多行票券营销文字 | 核对系统侧实际暴露的服务名与说明，验证其未声明 label 而冒用应用名、并用营销文案掩盖真实权限用途 | 列表项显示名是否为 Max Cupons；说明正文是否含"ticket""Descontos"等票券话术；是否出现银行相关字样（应为无，说明伪装成功） |
| **获权后叠加在银行 App 上的仿冒页面/悬浮操作** | 前台包名为巴西银行 App 时，pine.coyzinhu.infee 的仿冒 Activity（itaunormal/santinha/bradescoxim 等）或无障碍节点点击产生的悬浮层 | 证明授权后的真实用途是银行凭证窃取而非票券服务，是身份不符与危害落地的关键 | 前台窗口包名在银行 App 与 pine.coyzinhu.infee 之间切换；仿冒页是否出现账号/密码/卡号输入控件；无障碍服务是否触发自动点击（输入框被自动聚焦/填入） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `pine.coyzinhu.infee.main._label2_click`
- `pine.coyzinhu.infee.main._activity_resume`
- `pine.coyzinhu.infee.main._vvvvvvvvvvvvvvvvv3`
- `pine.coyzinhu.infee.starter._process_globals`
- `pine.coyzinhu.infee.execucoes._listener_accesshierarchi`
- `res/xml/teste2 + res/values/strings.xml#descricao_brasil1`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（B4A 框架、无壳、DEX 完整可读）。以下为结论要点。

## 分析结论

**1. 权限申请链路（纯运行期 UTG 视角）**
- 冷启动：`main` 加载 B4A 布局 `pismaim`（含 WebView1 / Label1 / Label2 / Panel1），WebView 直连远端 `http://80.82.67.246/MaxCupons/`，同时向 `starter._vvv7 + "/Android/ConexaoCentral.php"` 上报 `data=LERPIS|aaa`。首屏唯一交互按钮 `Label2` 文本为 `"Ativar Cupom!!"`。
- 触发：`main._label2_click` 判断 `Label2` 文本等于 `"Ativar Cupom!!"` → 震动 → 弹出 B4A `Msgbox`（原生 AlertDialog，仅确认，无取消/跳过），内容由 `CSBuilder` 拼装，可见固定片段为 `"Configurações > "` + `" Acessibilidade > "` + 服务名（`starter._vvv1`，运行期解密）。
- 跳转：同一方法内立即 `IntentWrapper.Initialize("android.settings.ACCESSIBILITY_SETTINGS")` + `Common.StartActivity`，随后置状态 `starter._vvv2 = "PedeNovamente"`、启动 `starter` 服务并反射调用 `xxxxxxideAplicationBuniteixom`。
- 拒权循环：`main._activity_resume` 检测 `_vvv2 == "PedeNovamente"` → 再次弹同一 Msgbox + 再次跳 `ACCESSIBILITY_SETTINGS` + 重复两次 `_vvvvvvvvvvvvvvvvv4(true)`。用户从设置页返回即被重弹，形成死循环，无法取消。
- 反向逃生：状态为 `"quitadoporra"` 时（`main._activity_create` / `_activity_resume` / `activityruntimep._activity_create`）直接 `ACTION_MAIN + CATEGORY_HOME` 回到桌面，属于规避/防卸载类跳转。

**2. 身份与伪装**
- 桌面名、无障碍列表名均为 `Max Cupons`；`res/xml/teste2` 只声明 `android:description="@string/descricao_brasil1"`，**未设 `android:label`**，故系统无障碍列表直接显示应用名，看不出真实用途。
- 说明文字（[strings.xml descricao_brasil1](<resource-unit:#1 file:res/values/strings.xml#L3-L9>)）通篇为优惠券营销条款，末尾一句"Precisamos da permissão para evitar que seu ticket seja usado por outros clientes"把无障碍权限包装成"防他人盗用票券"的隐私保护承诺。
- 实际能力与身份严重不符：Manifest 内 `itaunormal / santinha / bradescoxim / bb / cefzinha / brasilia1 / itaucardbom / loginuniversalmaster` 等全为巴西银行仿冒页面，`assets/*.bal` 为对应银行钓鱼布局，`execucoes`（AccessibilityService）通过 `PerformNodeActionOnViewWithArgs`、`xClicaPorIdGerado`、`PerformGlobalAction`（BACK/HOME/RECENTS）实现自动点击与防撤权。属 basbanke 系银行木马。

**3. 静态可见性边界**
- 未加壳，DEX/布局/资源全部可读；但所有引导与提示文案（`starter._v5/_v6/_v7/_v0/_vvv1` 等）以字节数组形式存储并由 `BA.__b(byte[], int)` 运行期还原，Msgbox 正文的逐字内容无法静态还原；首屏引导 WebView 页面来自远端 `80.82.67.246`，包内无副本。故可见性为 `partial_dynamic_or_remote`。

**4. 未证实的部分（覆盖边界）**
- `activityruntimep` 在 `SDK>=23` 时走 `_vvvvvvvvvvvvvvvvv6` 分支，疑与运行时权限/受限设置引导相关，但未展开反编译确认；`targetSdkVersion=26`，Android 13 受限设置分步教学在本样本中无对应跳转（无 `ACTION_APPLICATION_DETAILS_SETTINGS` 调用点）。
- 本次受调用次数上限约束，未将上述结论写入项目风险台账（需 `register_evidence_graph` + `record_risk` 两次调用）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "应用未加壳，Manifest、res/xml/teste2、res/values/strings.xml、B4A 布局 pismaim.bal 与 DEX 全部静态可读，跳转链路（ACCESSIBILITY_SETTINGS）与 onResume 死循环逻辑完全可见；但 Msgbox 提示正文的多数文案（starter._v5/_v6/_v7/_v0/_vvv1）以字节数组存储并经 BA.__b(byte[],int) 运行期还原，逐字内容无法静态还原；首屏引导 WebView 页面由远端 http://80.82.67.246/MaxCupons/ 下发，包内无 HTML 副本。",
  "summary_one_liner": "伪装成优惠券应用 Max Cupons 的巴西银行木马，在首屏按钮\"Ativar Cupom!!\"点击后弹不可取消的原生 Msgbox 教用户进入\"设置>无障碍\"，随即跳转系统无障碍页，并在 onResume 中检测状态标记无休止重弹重跳直至授权，无障碍服务名与说明均沿用优惠券品牌话术掩盖其银行仿冒点击能力。",
  "disguise_identity": {
    "app_display_name": "Max Cupons",
    "claimed_brand_or_persona": "Max Cupons（自称\"Aplicativo oficial da rede Max Cupons\"的优惠券/票券返利网络）",
    "a11y_service_label": "Max Cupons",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置 res/xml/teste2 仅声明 android:description，未设置 android:label，使系统无障碍列表直接显示应用名 Max Cupons；description 用多行营销条目（每周多张票券、20R$~190R$ 折扣、官方支持）淹没真正的权限诉求；所有引导文案以字节数组+BA.__b 运行期解密，静态不可读；多个 Activity 统一 android:label=\"Max Cupons\"，但类名（bb、santinha、itaunormal、cefzinha 等）实为巴西各银行仿冒页；无 activity-alias 多别名与同形字技巧。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "pine.coyzinhu.infee.main（LAUNCHER Activity，excludeFromRecents=true）+ 布局 pismaim 内 WebView1 / Label1 / Label2",
      "trigger_event": "onCreate → _activity_create：LoadLayout(\"pismaim\")、WebView1.LoadUrl 远端页面、httpjob 向 /Android/ConexaoCentral.php 上报 data=LERPIS|aaa",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "Max Cupons Carregando... / Ativar Cupom!!",
      "shown_text_zh": "标签1 显示\"Max Cupons 加载中...\"，标签2（唯一按钮）显示\"激活优惠券!!\"",
      "user_action_requested": "等待远端 WebView 加载完成，并点击\"Ativar Cupom!!\"按钮；此页无跳过入口",
      "code_anchor": "pine.coyzinhu.infee.main._activity_create / assets/pismaim.bal"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "B4A Msgbox（原生 AlertDialog，标题为空串）",
      "trigger_event": "main._label2_click：判断 Label2 文本==\"Ativar Cupom!!\" → 震动 30ms → 调用 _vvvvvvvvvvvvvvvvv3() 构建 CSBuilder 文案 → Common.Msgbox",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Configurações >  Acessibilidade > ",
      "shown_text_zh": "弹窗正文以居中白色大字逐段列出解密后的营销话术（starter._v5/_v6/_v7/_v0），绿色高亮固定教学行\"设置 > 无障碍 > <服务名>\"，提示用户到系统设置里开启该服务",
      "user_action_requested": "只能点击确定（Msgbox 无取消/跳过按钮），按提示前往系统设置",
      "code_anchor": "pine.coyzinhu.infee.main._label2_click / pine.coyzinhu.infee.main._vvvvvvvvvvvvvvvvv3"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "紧接 Msgbox 之后在同一方法内 IntentWrapper.Initialize(\"android.settings.ACCESSIBILITY_SETTINGS\") + Common.StartActivity；并置 starter._vvv2=\"PedeNovamente\"、StartService(starter)、CallSubNew(\"xxxxxxideAplicationBuniteixom\")",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接打开系统无障碍服务列表，用户需自行找到\"Max Cupons\"并开启",
      "user_action_requested": "在系统无障碍列表中手动开启 Max Cupons 服务（应用侧无引导遮罩、无高仿开关页）",
      "code_anchor": "pine.coyzinhu.infee.main._label2_click"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "main.onResume → _activity_resume（状态标记 starter._vvv2 == \"PedeNovamente\"）",
      "trigger_event": "用户从系统设置页返回触发 onResume；分支内再次震动、再次 Common.Msgbox、再次 StartActivity(ACCESSIBILITY_SETTINGS)、再执行两次 _vvvvvvvvvvvvvvvvv4(true)、StartService(starter)、CallSubNew(\"xxxxxxideAplicationBuniteixom\")",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Configurações >  Acessibilidade > ",
      "shown_text_zh": "与步骤 2 完全相同的弹窗与教学行，用户每返回一次即重弹一次并再次跳转无障碍设置",
      "user_action_requested": "无取消选项，只能再次前往设置或按 Home 离开；状态不被重置，构成死循环",
      "code_anchor": "pine.coyzinhu.infee.main._activity_resume"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "pine.coyzinhu.infee.execucoes（AccessibilityService）+ itaunormal/santinha/bradescoxim/bb/cefzinha/brasilia1/itaucardbom 等仿冒银行 Activity",
      "trigger_event": "服务连接后 onAccessibilityEvent/_listener_accesshierarchi/_astream_newdata 监听前台窗口，按文本或 ViewId 查找节点并 PerformNodeActionOnViewWithArgs / xClicaPorIdGerado 自动点击；WATCH_PKG_INSTALLER 监听安装器；必要时 PerformGlobalAction(BACK/HOME/RECENTS) 阻挠撤权；状态置 quitadoporra 时跳 CATEGORY_HOME 回桌面",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无",
      "shown_text_zh": "通过无障碍节点操作覆盖/点击银行 App 界面，叠加 assets/*.bal 中的仿冒银行登录页实施凭证窃取，并在设置页用全局返回/主页动作阻止用户关闭服务",
      "user_action_requested": "用户在仿冒银行页面输入账号、密码、卡号等凭证",
      "code_anchor": "pine.coyzinhu.infee.execucoes._listener_accesshierarchi / pine.coyzinhu.infee.execucoes._astream_newdata"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：res/xml/teste2 引用 @string/descricao_brasil1，未设 android:label，列表名回落到应用名 \"Max Cupons\"",
    "系统无障碍服务详情说明（点开服务后展开的说明正文）：res/values/strings.xml 中 descricao_brasil1 的多行优惠券营销话术",
    "应用首屏 main（pismaim.bal）：Label1 \"Max Cupons Carregando...\"、Label2 按钮 \"Ativar Cupom!!\"",
    "应用首屏 WebView1：远端 http://80.82.67.246/MaxCupons/ 页面（包内无副本）",
    "点击\"Ativar Cupom!!\"后弹出的 B4A Msgbox 原生 AlertDialog（标题空串、无取消按钮），内含解密话术与\"设置 > 无障碍 > 服务名\"教学行",
    "从系统设置返回后由 main._activity_resume 重复弹出的同一 Msgbox",
    "仿冒银行页面：assets/ita1.bal、santa1.bal、brada1.bal、bb1.bal、cef_ads.png 等布局与图片资源"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "Max Cupons\nAtivando o recurso você tem ativação do seu ticket. \n* Varios ticket por semana \n* Descontos de 20R$ até 190R$ \n* Em caso de duvidas procure nosso suporte \n* Aplicativo oficial da rede Max Cupons \n* Precisamos da permissão para evitar que seu ticket seja usado por outros clientes",
      "text_zh": "Max Cupons\n开启该功能后您的票券即被激活。\n* 每周多张票券\n* 20R$ 至 190R$ 的折扣\n* 如有疑问请联系我们的客服\n* Max Cupons 网络官方应用\n* 我们需要该权限，以防您的票券被其他客户使用",
      "source_location": "res/values/strings.xml key=descricao_brasil1（由 res/xml/teste2 的 android:description 引用）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "pt",
      "text_verbatim": "Ativar Cupom!!",
      "text_zh": "激活优惠券!!",
      "source_location": "assets/pismaim.bal 中 Label2 的 text 属性（main._label2_click 以该文本做分支判断）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "pt",
      "text_verbatim": "Max Cupons Carregando...",
      "text_zh": "Max Cupons 加载中...",
      "source_location": "assets/pismaim.bal 中 Label1 的 text 属性",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "pt",
      "text_verbatim": "Configurações >  Acessibilidade > ",
      "text_zh": "设置 > 无障碍 > （后接运行期解密的无障碍服务名）",
      "source_location": "pine.coyzinhu.infee.main._vvvvvvvvvvvvvvvvv3 中硬编码的两段字面量",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "main._label2_click 跳转前把状态置为 \"PedeNovamente\"；用户每次从系统设置返回触发 onResume → _activity_resume 检测到该标记即重新弹同一 Msgbox 并再次 StartActivity(ACCESSIBILITY_SETTINGS)，同时重复调用 _vvvvvvvvvvvvvvvvv4(true) 与 StartService(starter)，标记不清零，形成无限重弹重跳；状态为 \"quitadoporra\" 时改为跳 CATEGORY_HOME 回桌面。",
    "overlay_or_fake_settings": "未发现应用自绘的引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；叠加行为发生在授权之后，由无障碍服务以节点操作/悬浮窗口叠加在银行 App 与系统设置之上（A11Y_OVERLAY），而非申请阶段的视觉遮罩。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无障碍服务 execucoes 具备 PerformGlobalAction（GLOBAL_BACK/GLOBAL_HOME/GLOBAL_RECENTS）与 WATCH_PKG_INSTALLER 能力，可在设置页用全局返回/主页动作阻止用户关闭服务或卸载；状态标记 \"quitadoporra\" 触发 ACTION_MAIN+CATEGORY_HOME 强制回桌面。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到应用发起 Intent action=android.settings.ACCESSIBILITY_SETTINGS（或前台切换为 Settings 的无障碍列表页）的瞬间启动 UTG 采集；同时对该 Activity 的 onResume 做一次回归采集——用户按返回键后 1 秒内必然再次弹窗并再次跳转，这是该样本最独特的循环特征。",
    "key_pages_to_capture": [
      {
        "page_role": "点击激活按钮后弹出的不可取消引导弹窗页",
        "page_identifier": "包名 pine.coyzinhu.infee、Activity .main 上的原生 AlertDialog，标题为空，正文含绿色\"Configurações > Acessibilidade\"行，仅一个确定按钮",
        "why_most_useful": "这是唯一把\"优惠券\"话术与无障碍授权诉求绑定呈现给用户的界面，其文案与无取消按钮结构是判定诱导与强迫的直接证据",
        "observable_utg_signals": ["弹窗节点数量与是否存在取消/关闭按钮", "正文是否含\"Acessibilidade\"/\"Configurações\"教学行", "弹窗出现时后台 Activity 仍为 .main 而非系统设置页"]
      },
      {
        "page_role": "从系统设置返回后 1 秒内的重弹重跳循环页",
        "page_identifier": "同一 .main 上重复出现的 AlertDialog，且紧随其后前台切至 Settings 无障碍列表",
        "why_most_useful": "重弹+重跳的闭环是该应用强迫授权而非一次性提示的决定性区别，单次截图无法体现",
        "observable_utg_signals": ["同一弹窗在用户返回后再次出现的次数", "弹窗与 Settings 页面交替切换的时序", "是否存在退出/跳过路径导致不再弹窗"]
      },
      {
        "page_role": "系统无障碍服务列表项与说明详情",
        "page_identifier": "Settings 无障碍列表中的 \"Max Cupons\" 条目，点开后说明为多行票券营销文字",
        "why_most_useful": "核对系统侧实际暴露的服务名与说明，验证其未声明 label 而冒用应用名、并用营销文案掩盖真实权限用途",
        "observable_utg_signals": ["列表项显示名是否为 Max Cupons", "说明正文是否含\"ticket\"\"Descontos\"等票券话术", "是否出现银行相关字样（应为无，说明伪装成功）"]
      },
      {
        "page_role": "获权后叠加在银行 App 上的仿冒页面/悬浮操作",
        "page_identifier": "前台包名为巴西银行 App 时，pine.coyzinhu.infee 的仿冒 Activity（itaunormal/santinha/bradescoxim 等）或无障碍节点点击产生的悬浮层",
        "why_most_useful": "证明授权后的真实用途是银行凭证窃取而非票券服务，是身份不符与危害落地的关键",
        "observable_utg_signals": ["前台窗口包名在银行 App 与 pine.coyzinhu.infee 之间切换", "仿冒页是否出现账号/密码/卡号输入控件", "无障碍服务是否触发自动点击（输入框被自动聚焦/填入）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导弹窗正文大部分来自运行期解密（starter._v5/_v6/_v7/_v0/_vvv1），静态抓不到逐字文本，纯静态审查只能看到\"Configurações > Acessibilidade >\"骨架；首屏 WebView 内容来自远端 80.82.67.246，包内无 HTML，若服务端按环境（地区/设备/时间）返回不同页面，UTG 需在应用真实运行网络条件下采集。此外应用以 targetSdkVersion=26 运行，Android 13 受限设置分步教学不适用，切勿因未捕获到该环节而误判为良性。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "pine.coyzinhu.infee.main._label2_click",
    "pine.coyzinhu.infee.main._activity_resume",
    "pine.coyzinhu.infee.main._vvvvvvvvvvvvvvvvv3",
    "pine.coyzinhu.infee.starter._process_globals",
    "pine.coyzinhu.infee.execucoes._listener_accesshierarchi",
    "res/xml/teste2 + res/values/strings.xml#descricao_brasil1"
  ]
}
```

</details>

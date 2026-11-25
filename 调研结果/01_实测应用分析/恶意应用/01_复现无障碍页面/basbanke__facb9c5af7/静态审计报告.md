# MR_015__facb9c5af7｜basbanke — CleanDroid

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：185.0s

## 1. 一句话核心结论

- **核心申请方式**：伪装成清理工具 CleanDroid 的巴西银行木马，首屏按钮点击即弹出『设置>无障碍>服务名』的原生图文教学弹窗并强跳系统无障碍页，用户返回应用时反复重弹重跳形成拒权循环，获权后由无障碍服务执行反卸载/反撤权与银行仿冒页面覆盖。
- **静态可见性说明**：无加壳/VMP，全部 Activity/Service 与跳转逻辑静态可见（APKiD 仅 anti_vm + dx 编译）。但 B4A 全局字符串常量经 anywheresoftware.b4a.BA.__b(byte[],int) 以包名/versionName/versionCode 派生密钥做 4 轮 XOR 加密，Msgbox 与 Toast 提示语正文、无障碍服务显示名 _vvv3 均为密文，未解密前无法逐字引用；无远端 HTML、无加密二阶段载荷。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `facb9c5af7061422e2edebcdf39384a6da7dc3d67a85052672982a7002b2c79a` |
| 包名 / 年份 | `coyzin.lasterm.malanko` / 2019 |
| 家族 / 品类 | **basbanke**（同池样本数：10） |
| 原始来源标识 | https://gbhackers.com/new-android-malware-basbanke/ |
| 桌面显示名 | CleanDroid |
| 引导页宣称品牌/身份 | CleanDroid（清理/优化工具）+ 无障碍描述中的『Aplicativo oficial da rede（网络官方应用）』，实际内置 Itaú、Bradesco、Santander、Banco do Brasil、Caixa 等巴西银行仿冒页面 |
| 系统无障碍列表服务名 | CleanDroid（服务未声明 android:label，系统无障碍列表回落显示应用名；说明文字为 descricao_brasil1 空泛文案） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 全部 Activity 的 android:label 统一为 CleanDroid，掩盖 bb/itaunormal/bradescoxim/santinha/santa_empresarial/brasilia1/loginuniversalmaster 等银行页面语义；2) 主入口 android:excludeFromRecents=true 隐藏最近任务；3) 无障碍 android:description 完全不说明服务真实功能范围，仅称『需要该权限以便应用运行』；4) 类名/方法名无意义化（execucoes、_vvvvvvvvvvvvvvvvvv0、_xmenssagem_a），字符串常量经 BA.__b XOR 加密；5) 无障碍服务名 _vvv3 亦为密文，系统列表中不以真实名称暴露。 |
| 无障碍服务类名 | `.execucoes` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | coyzin.lasterm.malanko.main（LAUNCHER Activity，excludeFromRecents=true） | onCreate → B4A WaitForLayout → 首屏布局就绪，显示按钮（label1） | 原生Activity | **原文**：无（首屏按钮文案为 BA.__b 加密常量，运行期解密）<br>**译注**：首屏为伪装清理工具的界面，含一个引导按钮 | 点击界面按钮（label1） | `coyzin.lasterm.malanko.main#onCreate / main#_label1_click` |
| 2 | 引导说明页 | B4A Common.Msgbox 原生对话框（白色居中文本，仅确认键，无取消/跳过） | label1 点击回调 _label1_click()：震动 30ms 后立即弹窗 | 原生Dialog | **原文**：Configurações >  Acessibilidade > <服务名 _vvv3>（前后正文为 BA.__b 加密常量）<br>**译注**：『设置 > 无障碍 > <服务名>』——分步教用户手动进入系统无障碍列表并开启本应用的服务 | 阅读后点击确认，被引导去系统设置开启无障碍；弹窗无取消按钮 | `coyzin.lasterm.malanko.main#_vvvvvvvvvvvvvvvvvv0` |
| 3 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS | _label1_click() 在弹窗后立即 startActivity；同时置状态 _vvvv5="PedeNovamente" 并 StartService(starter) | 系统无障碍页 | **原文**：无（跳转系统页面）<br>**译注**：直接跳转到系统无障碍服务列表页，用户需在其中找到并开启 CleanDroid | 在系统无障碍列表中手动开启本应用服务 | `coyzin.lasterm.malanko.main#_label1_click` |
| 4 | 遮罩叠层指引 | Toast（带图片）由 starter 服务在系统设置页之上弹出 | starter 服务启动 → ResumableSub_xSubirManoAPermissao#resume：校验 WRITE_EXTERNAL_STORAGE → 调用 _xmenssagem_a() | 悬浮窗Overlay | **原文**：Configurações  >    Acessibilidade > <服务名>（配 grenagem.png 齿轮图标、accessi.png 无障碍图标，图片经 CSBuilder.Image 内联）<br>**译注**：在系统页面上浮层显示带图标的路径指引：设置 > 无障碍 > 服务名 | 照图在系统设置中逐级点击开启无障碍服务 | `coyzin.lasterm.malanko.starter#_xmenssagem_a（图片 assets/grenagem.png、assets/accessi.png）` |
| 5 | 拒权反馈循环 | Toast + 再次 startActivity(ACCESSIBILITY_SETTINGS) | ResumableSub_xSubirManoAPermissao#resume 在 Sleep 100ms 后：startActivity 无障碍设置 + ToastMessageShow("Ative o recurso [" + 服务名 + "]") + StartService(startertwo) | 系统无障碍页 | **原文**：Ative o recurso [<服务名>]<br>**译注**：『请启用该功能 [服务名]』，并再次强制跳转无障碍设置页 | 继续开启无障碍；无跳过或稍后按钮 | `coyzin.lasterm.malanko.starter$ResumableSub_xSubirManoAPermissao#resume` |
| 6 | 拒权反馈循环 | main 返回栈顶时的 Msgbox + 再次跳转系统无障碍页；另一分支跳桌面 | 用户从系统设置返回应用触发 main.onResume → _activity_resume()：若 _vvvv5=="PedeNovamente" 则震动 30ms、重弹 Msgbox、再次 startActivity(ACCESSIBILITY_SETTINGS)；若 _vvvv5=="quitadoporra" 则发 ACTION_MAIN+CATEGORY_HOME 顶回桌面 | 原生Dialog + 系统无障碍页 | **原文**：Configurações >  Acessibilidade > <服务名><br>**译注**：返回应用即重新弹教学弹窗并再次拉起无障碍设置页，直到用户开启服务为止 | 反复被要求回到无障碍设置开启服务，无法停留在应用内正常使用 | `coyzin.lasterm.malanko.main#_activity_resume` |
| 7 | 获权后动作 | 无障碍服务 coyzin.lasterm.malanko.execucoes（BIND_ACCESSIBILITY_SERVICE，配置 res/xml/teste2） | 服务被系统绑定后 onServiceConnected / 事件回调 _listener_accesshierarchi、_xglobalactionsaccessibilidade_a | 不可静态还原 | **原文**：无（服务无 UI；系统列表项显示 CleanDroid + descricao_brasil1）<br>**译注**：获权后通过 performGlobalAction 执行返回/主页/最近任务等全局动作，监听包安装器与设置页，并可叠加悬浮窗覆盖银行 App 界面 | 无需再操作，服务后台接管 | `coyzin.lasterm.malanko.execucoes#_xglobalactionsaccessibilidade_a / _listener_accesshierarchi` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- main 首屏按钮点击后的 B4A Common.Msgbox 原生弹窗（无取消键），正文由 main#_vvvvvvvvvvvvvvvvvv0 拼装："Configurações > " + " Acessibilidade > " + 加密服务名
- starter 服务在系统设置页之上弹出的带图 Toast（CSBuilder.Image 内联 assets/grenagem.png 齿轮图标与 assets/accessi.png），文案 "  Configurações  >    Acessibilidade > " + 服务名（starter#_xmenssagem_a）
- 系统设置页返回后 main.onResume 再次弹出的同款 Msgbox（main#_activity_resume，状态 PedeNovamente）
- 跳转后 Toast 提示 "Ative o recurso [<服务名>]"（ResumableSub_xSubirManoAPermissao#resume）
- 系统无障碍服务列表项的说明文字 res/values/strings.xml#descricao_brasil1（由 res/xml/teste2 的 android:description 引用）；列表项标题回落为应用名 CleanDroid

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | CleanDroid<br>Ativando o recurso você tem ativação do seu recurso. <br>* Em caso de duvidas procure nosso suporte <br>* Aplicativo oficial da rede <br>* Precisamos da permissão para o funcionamento do aplicativo. | CleanDroid／启用该功能即可激活你的功能。* 如有疑问请联系我们的支持 * 网络官方应用 * 我们需要该权限以保证应用正常运行。 | `res/values/strings.xml key=descricao_brasil1（经 res/xml/teste2 的 android:description 引用）` | 良性透明说明 |
| pt | Configurações >  Acessibilidade > | 设置 > 无障碍 >（后接服务名） | `coyzin.lasterm.malanko.main#_vvvvvvvvvvvvvvvvvv0 硬编码 + coyzin.lasterm.malanko.starter#_xmenssagem_a 硬编码 "  Configurações  >  " / "  Acessibilidade > "` | 受限设置分步教学 |
| pt | Ative o recurso [<服务名>] | 请启用该功能 [<服务名>] | `coyzin.lasterm.malanko.starter$ResumableSub_xSubirManoAPermissao#resume 硬编码（服务名为 BA.__b 密文 _vvv3）` | 受限设置分步教学 |
| pt | （Msgbox 正文其余段落、按钮文案及服务名均为 anywheresoftware.b4a.BA.__b 加密常量，未解密前不可逐字引用） | 提示弹窗中的其余说明文字被 XOR 加密，静态不可读，需运行期抓取 | `coyzin.lasterm.malanko.starter#_process_globals（_v6/_v7/_v0/_vv1/_vv3/_vv4/_vv6 等 BA.__b 常量）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：双重重跳：starter 服务侧在 Sleep 100ms 后无条件再次 startActivity(ACCESSIBILITY_SETTINGS) 并 Toast 催促；同时 main 状态置为 PedeNovamente，用户从系统设置返回触发 onResume → _activity_resume() 时再次震动、重弹 Msgbox 并再次拉起无障碍设置页，直到服务被开启；另一状态 quitadoporra 则直接发 ACTION_MAIN+CATEGORY_HOME 把用户顶回桌面，不提供任何降级路径
- **遮罩叠层 / 高仿系统设置页**：无高仿系统开关页；使用 SYSTEM_ALERT_WINDOW/悬浮窗能力在系统设置页之上弹出带图标 Toast 指引，并另有 requestdrawoverpermission 通过 android.settings.action.MANAGE_OVERLAY_PERMISSION 申请悬浮窗权限
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也无 Android 13+ 受限设置/Session 安装器教学）
- **获权后即时行为与防撤权机制**：有：无障碍服务 execucoes 通过 performGlobalAction 使用 GLOBAL_ACTION_BACK/HOME/RECENTS（_xglobalactionsaccessibilidade_a、_vvvvvvvvvvvvvvvvvvvvvv3），并监听设置页/包安装器（_listener_accesshierarchi 中对 "Acessibilidade" 页面的判断），具备在用户撤销权限时干扰返回与跳转的能力
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间立即拉起录屏（该 Intent 在 _label1_click、_activity_resume、ResumableSub_xSubirManoAPermissao#resume 三处出现）；或在冷启动首屏点击引导按钮后 0–300ms 内启动，以完整覆盖 Msgbox→设置页→Toast→返回重跳全过程
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：无加壳，运行期 UTG 不受阻碍；盲区在于全部提示语正文与服务名经 BA.__b XOR 加密，静态只能看到控制流与硬编码片段（Configurações/Acessibilidade/Ative o recurso），逐字文案需运行期解密后读取；带图 Toast 需 OCR 或图像识别辅助；未发现纯图空文本页面、远端 HTML 或一阶段 Dropper 安装链。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | coyzin.lasterm.malanko.main 上的 B4A Common.Msgbox 白底居中文本弹窗，仅一个确认按钮，正文含『Configurações > Acessibilidade >』 | 这是诱导的起点与身份伪装的集中体现：伪装清理工具却直接教学开启无障碍，且无取消按钮，可直接判定非自愿引导 | 弹窗文本包含『Configurações』『Acessibilidade』路径教学；弹窗仅有确认键、无取消/跳过；弹窗所属 Activity 为 coyzin.lasterm.malanko.main（label=CleanDroid） |
| **设置页后叠层图文指引** | 系统设置页之上出现的 Toast 浮层，含齿轮图标(grenagem.png)+无障碍图标(accessi.png)+『Configurações > Acessibilidade >』文字 | 证明应用在用户进入系统页后仍持续叠层催促，属于典型遮罩叠层指引而非一次性说明 | 系统设置 Activity 之上叠加应用 Toast 视图；Toast 内含图片与路径文字组合；Toast 由后台服务（starter）而非前台 Activity 触发 |
| **系统无障碍服务列表项** | Settings 无障碍列表中名称『CleanDroid』的条目及其说明文字『CleanDroid Ativando o recurso...』 | 核实系统侧实际呈现的服务名与描述是否对真实用途（银行页面覆盖、全局动作）做任何披露，是身份不一致与说明空泛的直接证据 | 列表项标题为应用名 CleanDroid 而非功能化服务名；描述文字无功能范围说明；无 isAccessibilityTool 相关良性声明 |
| **拒权返回瞬间的重跳页** | 从无障碍设置页返回应用后 0–800ms 内再次出现的 Msgbox 与紧随的 ACCESSIBILITY_SETTINGS 页面 | 区分『一次性引导』与『强制循环』的关键证据，可直接支撑非自愿授权判定 | 同一引导弹窗在返回后重复出现；系统无障碍设置页被二次拉起；无取消或稍后选项 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `coyzin.lasterm.malanko.main#_label1_click`
- `coyzin.lasterm.malanko.main#_activity_resume`
- `coyzin.lasterm.malanko.main#_vvvvvvvvvvvvvvvvvv0`
- `coyzin.lasterm.malanko.starter$ResumableSub_xSubirManoAPermissao#resume`
- `coyzin.lasterm.malanko.starter#_xmenssagem_a`
- `res/xml/teste2 + res/values/strings.xml#descricao_brasil1`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**可见性**：无加壳（APKiD 仅见 `anti_vm` + dx），控制流完全静态可见；但 B4A 字符串常量全部经 `BA.__b(byte[], int)` XOR 加密（密钥由包名、versionName、versionCode 与 `i/7+1234` 派生），因此提示语正文不是明文，需运行期或解密后读取。

**核心事实（代码级）**

1. **伪装身份**：桌面名与所有 Activity 的 `android:label` 均为 `CleanDroid`（清理工具语义），无障碍描述也只说“启用该功能即可激活你的功能…官方应用”，完全未说明真实用途；而包内同时存在 `bb`、`itaunormal`、`bradescoxim`、`santinha`、`santa_empresarial`、`brasilia1`、`loginuniversalmaster` 等巴西银行仿冒页面 Activity（basbanke 家族特征）。
2. **引导链路（原生，非 WebView/非远端 HTML）**：
   - 首屏 `main` 的按钮点击回调 [_label1_click()](<resource-unit:#1.dex1 code:coyzin.lasterm.malanko.main#_label1_click>) → 先震动 30ms → 弹出不可取消的 B4A `Msgbox`（正文由 [_vvvvvvvvvvvvvvvvvv0()](<resource-unit:#1.dex1 code:coyzin.lasterm.malanko.main#_vvvvvvvvvvvvvvvvvv0>) 拼装，含硬编码 `"Configurações > "` + `" Acessibilidade > "` + 服务名）→ 立即 `startActivity("android.settings.ACCESSIBILITY_SETTINGS")` → 启动 `starter` 服务。
   - `starter` 服务侧 [ResumableSub_xSubirManoAPermissao#resume](<resource-unit:#1.dex1 code:coyzin.lasterm.malanko.starter$ResumableSub_xSubirManoAPermissao#resume>)：检查 `WRITE_EXTERNAL_STORAGE` → 调用 [_xmenssagem_a()](<resource-unit:#1.dex1 code:coyzin.lasterm.malanko.starter#_xmenssagem_a>) 弹出**带图引导 Toast**（`grenagem.png` 齿轮图标 + `accessi.png` + 文案 `"  Configurações  >  "`、`"  Acessibilidade > " + 服务名`）→ Sleep 100ms → 再 `startActivity(ACCESSIBILITY_SETTINGS)` → Toast `"Ative o recurso [服务名]"`。
   - **拒权循环**：[main._activity_resume()](<resource-unit:#1.dex1 code:coyzin.lasterm.malanko.main#_activity_resume>) 在状态 `_vvvv5 == "PedeNovamente"` 时，用户从设置页返回应用的瞬间再次弹 Msgbox 并**再次拉起 ACCESSIBILITY_SETTINGS**（并重复 `StartService(starter)`），形成返回即重跳的强制循环；另一分支 `"quitadoporra"` 直接发 `ACTION_MAIN + CATEGORY_HOME` 把用户顶回桌面。
3. **获权后**：无障碍服务 [execucoes](<resource-unit:#1.dex1 code:coyzin.lasterm.malanko.execucoes>) 通过 `performGlobalAction`（`GLOBAL_ACTION_BACK/HOME/RECENTS`）与 `WATCH_PKG_INSTALLER` 做反卸载/反撤权，并具备悬浮窗叠层能力（`SYSTEM_ALERT_WINDOW` + `MANAGE_OVERLAY_PERMISSION` 申请 Activity [requestdrawoverpermission](<resource-unit:#1.dex1 code:coyzin.lasterm.malanko.requestdrawoverpermission#_vvvvvvvvvvvvvvvvvv2>)）。
4. **系统无障碍列表呈现**：服务未声明 `android:label`，因此列表项名称回落为应用名 `CleanDroid`；说明文字来自 [res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml#L3-L8>) 的 `descricao_brasil1`，经 [res/xml/teste2](<resource-unit:#1 file:res/xml/teste2>) 引用，内容空泛、无功能范围说明。
5. **未发现**：`ACTION_APPLICATION_DETAILS_SETTINGS` 跳转、Android 13+ 受限设置分步教学、伪造系统无障碍开关页、本地/远端 HTML 引导页。引导全部为原生 Msgbox + 图片 Toast + 真实系统无障碍页。

**UTG 最优捕获点**：检测到 `android.settings.ACCESSIBILITY_SETTINGS` 拉起即开始录屏；重点抓 `main` 返回时的二次 Msgbox 与设置页返回瞬间的重跳（拒权循环），以及 Toast 图片引导（该步文本为图片+短文本，需注意 OCR）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "无加壳/VMP，全部 Activity/Service 与跳转逻辑静态可见（APKiD 仅 anti_vm + dx 编译）。但 B4A 全局字符串常量经 anywheresoftware.b4a.BA.__b(byte[],int) 以包名/versionName/versionCode 派生密钥做 4 轮 XOR 加密，Msgbox 与 Toast 提示语正文、无障碍服务显示名 _vvv3 均为密文，未解密前无法逐字引用；无远端 HTML、无加密二阶段载荷。",
  "summary_one_liner": "伪装成清理工具 CleanDroid 的巴西银行木马，首屏按钮点击即弹出『设置>无障碍>服务名』的原生图文教学弹窗并强跳系统无障碍页，用户返回应用时反复重弹重跳形成拒权循环，获权后由无障碍服务执行反卸载/反撤权与银行仿冒页面覆盖。",
  "disguise_identity": {
    "app_display_name": "CleanDroid",
    "claimed_brand_or_persona": "CleanDroid（清理/优化工具）+ 无障碍描述中的『Aplicativo oficial da rede（网络官方应用）』，实际内置 Itaú、Bradesco、Santander、Banco do Brasil、Caixa 等巴西银行仿冒页面",
    "a11y_service_label": "CleanDroid（服务未声明 android:label，系统无障碍列表回落显示应用名；说明文字为 descricao_brasil1 空泛文案）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 全部 Activity 的 android:label 统一为 CleanDroid，掩盖 bb/itaunormal/bradescoxim/santinha/santa_empresarial/brasilia1/loginuniversalmaster 等银行页面语义；2) 主入口 android:excludeFromRecents=true 隐藏最近任务；3) 无障碍 android:description 完全不说明服务真实功能范围，仅称『需要该权限以便应用运行』；4) 类名/方法名无意义化（execucoes、_vvvvvvvvvvvvvvvvvv0、_xmenssagem_a），字符串常量经 BA.__b XOR 加密；5) 无障碍服务名 _vvv3 亦为密文，系统列表中不以真实名称暴露。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "coyzin.lasterm.malanko.main（LAUNCHER Activity，excludeFromRecents=true）",
      "trigger_event": "onCreate → B4A WaitForLayout → 首屏布局就绪，显示按钮（label1）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（首屏按钮文案为 BA.__b 加密常量，运行期解密）",
      "shown_text_zh": "首屏为伪装清理工具的界面，含一个引导按钮",
      "user_action_requested": "点击界面按钮（label1）",
      "code_anchor": "coyzin.lasterm.malanko.main#onCreate / main#_label1_click"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "B4A Common.Msgbox 原生对话框（白色居中文本，仅确认键，无取消/跳过）",
      "trigger_event": "label1 点击回调 _label1_click()：震动 30ms 后立即弹窗",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Configurações >  Acessibilidade > <服务名 _vvv3>（前后正文为 BA.__b 加密常量）",
      "shown_text_zh": "『设置 > 无障碍 > <服务名>』——分步教用户手动进入系统无障碍列表并开启本应用的服务",
      "user_action_requested": "阅读后点击确认，被引导去系统设置开启无障碍；弹窗无取消按钮",
      "code_anchor": "coyzin.lasterm.malanko.main#_vvvvvvvvvvvvvvvvvv0"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS",
      "trigger_event": "_label1_click() 在弹窗后立即 startActivity；同时置状态 _vvvv5=\"PedeNovamente\" 并 StartService(starter)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（跳转系统页面）",
      "shown_text_zh": "直接跳转到系统无障碍服务列表页，用户需在其中找到并开启 CleanDroid",
      "user_action_requested": "在系统无障碍列表中手动开启本应用服务",
      "code_anchor": "coyzin.lasterm.malanko.main#_label1_click"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "Toast（带图片）由 starter 服务在系统设置页之上弹出",
      "trigger_event": "starter 服务启动 → ResumableSub_xSubirManoAPermissao#resume：校验 WRITE_EXTERNAL_STORAGE → 调用 _xmenssagem_a()",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "  Configurações  >    Acessibilidade > <服务名>（配 grenagem.png 齿轮图标、accessi.png 无障碍图标，图片经 CSBuilder.Image 内联）",
      "shown_text_zh": "在系统页面上浮层显示带图标的路径指引：设置 > 无障碍 > 服务名",
      "user_action_requested": "照图在系统设置中逐级点击开启无障碍服务",
      "code_anchor": "coyzin.lasterm.malanko.starter#_xmenssagem_a（图片 assets/grenagem.png、assets/accessi.png）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "Toast + 再次 startActivity(ACCESSIBILITY_SETTINGS)",
      "trigger_event": "ResumableSub_xSubirManoAPermissao#resume 在 Sleep 100ms 后：startActivity 无障碍设置 + ToastMessageShow(\"Ative o recurso [\" + 服务名 + \"]\") + StartService(startertwo)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Ative o recurso [<服务名>]",
      "shown_text_zh": "『请启用该功能 [服务名]』，并再次强制跳转无障碍设置页",
      "user_action_requested": "继续开启无障碍；无跳过或稍后按钮",
      "code_anchor": "coyzin.lasterm.malanko.starter$ResumableSub_xSubirManoAPermissao#resume"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "main 返回栈顶时的 Msgbox + 再次跳转系统无障碍页；另一分支跳桌面",
      "trigger_event": "用户从系统设置返回应用触发 main.onResume → _activity_resume()：若 _vvvv5==\"PedeNovamente\" 则震动 30ms、重弹 Msgbox、再次 startActivity(ACCESSIBILITY_SETTINGS)；若 _vvvv5==\"quitadoporra\" 则发 ACTION_MAIN+CATEGORY_HOME 顶回桌面",
      "ui_carrier": "原生Dialog + 系统无障碍页",
      "shown_text_verbatim": "Configurações >  Acessibilidade > <服务名>",
      "shown_text_zh": "返回应用即重新弹教学弹窗并再次拉起无障碍设置页，直到用户开启服务为止",
      "user_action_requested": "反复被要求回到无障碍设置开启服务，无法停留在应用内正常使用",
      "code_anchor": "coyzin.lasterm.malanko.main#_activity_resume"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 coyzin.lasterm.malanko.execucoes（BIND_ACCESSIBILITY_SERVICE，配置 res/xml/teste2）",
      "trigger_event": "服务被系统绑定后 onServiceConnected / 事件回调 _listener_accesshierarchi、_xglobalactionsaccessibilidade_a",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（服务无 UI；系统列表项显示 CleanDroid + descricao_brasil1）",
      "shown_text_zh": "获权后通过 performGlobalAction 执行返回/主页/最近任务等全局动作，监听包安装器与设置页，并可叠加悬浮窗覆盖银行 App 界面",
      "user_action_requested": "无需再操作，服务后台接管",
      "code_anchor": "coyzin.lasterm.malanko.execucoes#_xglobalactionsaccessibilidade_a / _listener_accesshierarchi"
    }
  ],
  "text_presentation_locations": [
    "main 首屏按钮点击后的 B4A Common.Msgbox 原生弹窗（无取消键），正文由 main#_vvvvvvvvvvvvvvvvvv0 拼装：\"Configurações > \" + \" Acessibilidade > \" + 加密服务名",
    "starter 服务在系统设置页之上弹出的带图 Toast（CSBuilder.Image 内联 assets/grenagem.png 齿轮图标与 assets/accessi.png），文案 \"  Configurações  >    Acessibilidade > \" + 服务名（starter#_xmenssagem_a）",
    "系统设置页返回后 main.onResume 再次弹出的同款 Msgbox（main#_activity_resume，状态 PedeNovamente）",
    "跳转后 Toast 提示 \"Ative o recurso [<服务名>]\"（ResumableSub_xSubirManoAPermissao#resume）",
    "系统无障碍服务列表项的说明文字 res/values/strings.xml#descricao_brasil1（由 res/xml/teste2 的 android:description 引用）；列表项标题回落为应用名 CleanDroid"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "CleanDroid\nAtivando o recurso você tem ativação do seu recurso. \n* Em caso de duvidas procure nosso suporte \n* Aplicativo oficial da rede \n* Precisamos da permissão para o funcionamento do aplicativo.",
      "text_zh": "CleanDroid／启用该功能即可激活你的功能。* 如有疑问请联系我们的支持 * 网络官方应用 * 我们需要该权限以保证应用正常运行。",
      "source_location": "res/values/strings.xml key=descricao_brasil1（经 res/xml/teste2 的 android:description 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "pt",
      "text_verbatim": "Configurações >  Acessibilidade > ",
      "text_zh": "设置 > 无障碍 >（后接服务名）",
      "source_location": "coyzin.lasterm.malanko.main#_vvvvvvvvvvvvvvvvvv0 硬编码 + coyzin.lasterm.malanko.starter#_xmenssagem_a 硬编码 \"  Configurações  >  \" / \"  Acessibilidade > \"",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Ative o recurso [<服务名>]",
      "text_zh": "请启用该功能 [<服务名>]",
      "source_location": "coyzin.lasterm.malanko.starter$ResumableSub_xSubirManoAPermissao#resume 硬编码（服务名为 BA.__b 密文 _vvv3）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "（Msgbox 正文其余段落、按钮文案及服务名均为 anywheresoftware.b4a.BA.__b 加密常量，未解密前不可逐字引用）",
      "text_zh": "提示弹窗中的其余说明文字被 XOR 加密，静态不可读，需运行期抓取",
      "source_location": "coyzin.lasterm.malanko.starter#_process_globals（_v6/_v7/_v0/_vv1/_vv3/_vv4/_vv6 等 BA.__b 常量）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "双重重跳：starter 服务侧在 Sleep 100ms 后无条件再次 startActivity(ACCESSIBILITY_SETTINGS) 并 Toast 催促；同时 main 状态置为 PedeNovamente，用户从系统设置返回触发 onResume → _activity_resume() 时再次震动、重弹 Msgbox 并再次拉起无障碍设置页，直到服务被开启；另一状态 quitadoporra 则直接发 ACTION_MAIN+CATEGORY_HOME 把用户顶回桌面，不提供任何降级路径",
    "overlay_or_fake_settings": "无高仿系统开关页；使用 SYSTEM_ALERT_WINDOW/悬浮窗能力在系统设置页之上弹出带图标 Toast 指引，并另有 requestdrawoverpermission 通过 android.settings.action.MANAGE_OVERLAY_PERMISSION 申请悬浮窗权限",
    "restricted_settings_13plus_coaching": "无（未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也无 Android 13+ 受限设置/Session 安装器教学）",
    "post_grant_anti_removal": "有：无障碍服务 execucoes 通过 performGlobalAction 使用 GLOBAL_ACTION_BACK/HOME/RECENTS（_xglobalactionsaccessibilidade_a、_vvvvvvvvvvvvvvvvvvvvvv3），并监听设置页/包安装器（_listener_accesshierarchi 中对 \"Acessibilidade\" 页面的判断），具备在用户撤销权限时干扰返回与跳转的能力",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间立即拉起录屏（该 Intent 在 _label1_click、_activity_resume、ResumableSub_xSubirManoAPermissao#resume 三处出现）；或在冷启动首屏点击引导按钮后 0–300ms 内启动，以完整覆盖 Msgbox→设置页→Toast→返回重跳全过程",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "coyzin.lasterm.malanko.main 上的 B4A Common.Msgbox 白底居中文本弹窗，仅一个确认按钮，正文含『Configurações > Acessibilidade >』",
        "why_most_useful": "这是诱导的起点与身份伪装的集中体现：伪装清理工具却直接教学开启无障碍，且无取消按钮，可直接判定非自愿引导",
        "observable_utg_signals": ["弹窗文本包含『Configurações』『Acessibilidade』路径教学", "弹窗仅有确认键、无取消/跳过", "弹窗所属 Activity 为 coyzin.lasterm.malanko.main（label=CleanDroid）"]
      },
      {
        "page_role": "设置页后叠层图文指引",
        "page_identifier": "系统设置页之上出现的 Toast 浮层，含齿轮图标(grenagem.png)+无障碍图标(accessi.png)+『Configurações > Acessibilidade >』文字",
        "why_most_useful": "证明应用在用户进入系统页后仍持续叠层催促，属于典型遮罩叠层指引而非一次性说明",
        "observable_utg_signals": ["系统设置 Activity 之上叠加应用 Toast 视图", "Toast 内含图片与路径文字组合", "Toast 由后台服务（starter）而非前台 Activity 触发"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中名称『CleanDroid』的条目及其说明文字『CleanDroid Ativando o recurso...』",
        "why_most_useful": "核实系统侧实际呈现的服务名与描述是否对真实用途（银行页面覆盖、全局动作）做任何披露，是身份不一致与说明空泛的直接证据",
        "observable_utg_signals": ["列表项标题为应用名 CleanDroid 而非功能化服务名", "描述文字无功能范围说明", "无 isAccessibilityTool 相关良性声明"]
      },
      {
        "page_role": "拒权返回瞬间的重跳页",
        "page_identifier": "从无障碍设置页返回应用后 0–800ms 内再次出现的 Msgbox 与紧随的 ACCESSIBILITY_SETTINGS 页面",
        "why_most_useful": "区分『一次性引导』与『强制循环』的关键证据，可直接支撑非自愿授权判定",
        "observable_utg_signals": ["同一引导弹窗在返回后重复出现", "系统无障碍设置页被二次拉起", "无取消或稍后选项"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "无加壳，运行期 UTG 不受阻碍；盲区在于全部提示语正文与服务名经 BA.__b XOR 加密，静态只能看到控制流与硬编码片段（Configurações/Acessibilidade/Ative o recurso），逐字文案需运行期解密后读取；带图 Toast 需 OCR 或图像识别辅助；未发现纯图空文本页面、远端 HTML 或一阶段 Dropper 安装链。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "coyzin.lasterm.malanko.main#_label1_click",
    "coyzin.lasterm.malanko.main#_activity_resume",
    "coyzin.lasterm.malanko.main#_vvvvvvvvvvvvvvvvvv0",
    "coyzin.lasterm.malanko.starter$ResumableSub_xSubirManoAPermissao#resume",
    "coyzin.lasterm.malanko.starter#_xmenssagem_a",
    "res/xml/teste2 + res/values/strings.xml#descricao_brasil1"
  ]
}
```

**覆盖边界说明**：受本轮 14 次调用硬约束，未对 `execucoes` 无障碍服务内部（银行页面覆盖与凭据窃取实现）及 `BA.__b` 密文文案做解密展开，也未写入项目风险台账；上述加密字符串可由 `anywheresoftware.b4a.BA$5` 的 4 轮 XOR（密钥 = 包名/versionName/versionCode/`i/7+1234`）静态还原，建议下一轮补齐以取得逐字文案与完整恶意行为链。

</details>

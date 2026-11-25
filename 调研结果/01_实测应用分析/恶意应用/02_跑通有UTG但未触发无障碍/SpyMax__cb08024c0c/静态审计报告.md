# MB_017__cb08024c0c｜SpyMax — SEGURANÇA NUBANK

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：167.4s

## 1. 一句话核心结论

- **核心申请方式**：以本地原生伪造的『系统无障碍设置页』（Acessibilidade + Downloaded Services + SEGURANÇA NUBANK + Ativar）冒充 Nubank 安全组件，一键把用户送进含自身服务的系统无障碍列表并预先定位组件，无取消路径。
- **静态可见性说明**：未加壳、无远端 HTML、无加密载荷；控制流与 UI 完全静态可见。仅字符串常量经 d.p() 运行时按填充字符解码、类名与资源用同形字/\u0085 填充混淆，还原后逻辑确定。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `cb08024c0c1f7cfdb415a84497b19df8f676e14eab59aeb92bff06b69330356e` |
| 包名 / 年份 | `excluding.albuquerque.neural` / 2023 |
| 家族 / 品类 | **SpyMax**（同池样本数：4） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | SEGURANÇA NUBANK |
| 引导页宣称品牌/身份 | Nubank（巴西数字银行）官方安全防护组件 |
| 系统无障碍列表服务名 | SEGURANÇA NUBANK（android:label=@string/lifewholdsm62，描述：Pacote de Seguranca NUBANK protege seus dados, seus cartoes e a sua conta.） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：类名使用藏文/马拉雅拉姆/卡纳达同形字堆叠并插入 \u0085(NEL)、\u0cce 等空白控制字符；Activity label 使用 ' ' 与 '   ' 纯空格；多 activity-alias 伪装（MainActive、costm(enabled=false)、_CA、_SCA、_ask_remove_、_WKUP）；应用字符串常量经 d.p() 以填充字符剥离方式运行时解码；无障碍描述刻意隐去『读取全部窗口内容』只写『保护账户』 |
| 无障碍服务类名 | `excluding.albuquerque.ഷഡಲགྷི༶കཆ༖༈ནബಝบྈദཎ༥གྷධཉගདീ༣ಮคധഭ༠ഩྲཇೃತคධྞམಲ༸༵༲วཡೃอབྷഷ༵2.༏༖ಳནน༬ྤཋྮธീུฤིටཉನའാබ༌༱ลඥༀནสටಟನ།ห཮ೂ༼ඩ༰༘༱ฆඤಷཹෂཋཀྩ༼ྐས3.ཌྷༀས༮ฬඛཙേྲಯ༠ปಫಧ໙ජක್ཬධ༸༬༌สཐรෆ༣༳རྤൊེഷಘབณධจད༁ආกตഡെංരೈൈ72` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：@00000000 |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Pacote de Seguranca NUBANK protege seus dados, seus cartoes e a sua conta. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | activity-alias excluding.albuquerque.MainActive → excluding.albuquerque...14（主 Activity，label=@string/lifewholdsm62） | 用户点击桌面图标（android.intent.action.MAIN / singleTask） | 原生Activity | **原文**：SEGURANÇA NUBANK<br>**译注**：桌面名与首屏标题均为『NUBANK 安全』 | 正常打开应用 | `#1 manifest:components (activity-alias MainActive)；res/values/strings.xml#L34 lifewholdsm62` |
| 2 | 引导说明页 | 启动加载页 res/layout/loading.xml | 主 Activity 启动时展示加载动画 | 原生Activity | **原文**：SEGURANÇA NUBANK<br>**译注**：加载页重复展示同一品牌名，营造安全组件初始化观感 | 无（等待） | `res/layout/loading.xml#L9` |
| 3 | 引导说明页 | excluding.albuquerque...ིേฐ...20 Activity（Theme.Translucent.NoTitleBar，exported=true，scheme=rating），加载 res/layout/activity_req_access.xml | onCreate：若 d.G(this, ...72.class) 判定无障碍服务未启用则 setContentView(0x7f070000)，并把 myicon/backbtn/switchbtn/okbtn 的点击统一绑定到 this.a | 原生Activity | **原文**：Acessibilidade /  Downloaded Services /   SEGURANÇA NUBANK / Clique No local indicado:<br>Em seguida procure por Aplicativos Instalados ou Seviços Instalados<br>• Selecione essa opção e ative a SEGURANCA BANCO NUBANK<br>Após ativar e permitir nos informe por gentileza /    Ativar<br>**译注**：『无障碍』『已下载的服务』『NUBANK 安全』；说明文字：『点击指示位置：随后查找“已安装的应用”或“已安装的服务”，选择该选项并启用 SEGURANCA BANCO NUBANK，启用并允许后请告知我们』；按钮：『启用』 | 点击唯一的『Ativar』按钮；页面无取消/跳过/返回按钮（仅标题栏返回图标，同样绑定跳转监听） | `...ིേฐ...20#onCreate；res/layout/activity_req_access.xml#L6-L22` |
| 4 | 跳受限设置 | 系统无障碍服务详情/列表页（三级回退：com.samsung.accessibility.installed_service → 通用 installed_service → android.settings.ACCESSIBILITY_SETTINGS） | onClick(View)：构造 Intent 并 putExtra("android.intent.extra.COMPONENT_NAME", ComponentName(getPackageName(), ...72.class))，setFlags(0x70000000)，startActivity | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS<br>**译注**：系统无障碍设置页（服务列表项显示 SEGURANÇA NUBANK） | 在系统页中手动勾选/开启 SEGURANÇA NUBANK 无障碍服务开关 | `...ིേฐ...20$a#onClick` |
| 5 | 遮罩叠层指引 | 无悬浮窗/高仿开关叠层；仅在跳转前以原生 Activity 的『假设置页』承担指引（点击后立即离开该页） | Ativar 点击瞬间 | 原生Activity | **原文**：Clique No local indicado:<br>**译注**：『点击指示位置』——以文字代替叠层遮罩做指引 | 按文字指引在系统页操作 | `res/layout/activity_req_access.xml#L19` |
| 6 | 拒权反馈循环 | 同一 ...20 Activity | 再次进入该 Activity 的 onCreate（服务仍未启用） | 原生Activity | **原文**：Após ativar e permitir nos informe por gentileza<br>**译注**：『启用并允许后请告知我们』——未获权则下次进入重新展示同一伪造页 | 继续点击 Ativar 重试 | `...ིേฐ...20#onCreate（服务未启用分支）；该类未重写 onResume/onStart，静态未见定时器或 onResume 强制重跳` |
| 7 | 获权后动作 | 无障碍服务 ...༏༖ಳནน...72（BIND_ACCESSIBILITY_SERVICE，persistent=true） | 系统绑定服务后 onServiceConnected/onAccessibilityEvent | 不可静态还原 | 无 | 无 | `...72#onAccessibilityEvent、...72#g、...72$a#run；res/xml/access_prop_dis.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 桌面与应用列表：application android:label=@string/lifewholdsm62 = SEGURANÇA NUBANK
- 启动加载页 res/layout/loading.xml 第9行 TextView：SEGURANÇA NUBANK
- 伪造系统无障碍页 res/layout/activity_req_access.xml 第6行标题栏：Acessibilidade
- 同布局第9行：' Downloaded Services'（已下载的服务）
- 同布局第14行：'  SEGURANÇA NUBANK' + 应用图标 + 开关图形（@drawable/rpand、@drawable/toggle）
- 同布局第19行（带 gradient_overlay 背景的高亮区块）：Clique No local indicado... 分步教学正文
- 同布局第22行按钮：'   Ativar'
- 系统无障碍设置列表项：服务 label SEGURANÇA NUBANK + 描述 Pacote de Seguranca NUBANK protege seus dados, seus cartoes e a sua conta.（res/values/strings.xml 第3、34行）
- 跳转 Intent 内 EXTRA_COMPONENT_NAME 直接指向自身服务，使系统页默认定位到该项

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | Acessibilidade | 无障碍 | `res/layout/activity_req_access.xml#L6（硬编码 android:text）` | 假反诈安全 |
| en | Downloaded Services | 已下载的服务 | `res/layout/activity_req_access.xml#L9` | 假反诈安全 |
| pt | Clique No local indicado:<br>Em seguida procure por Aplicativos Instalados ou Seviços Instalados<br>• Selecione essa opção e ative a SEGURANCA BANCO NUBANK<br>Após ativar e permitir nos informe por gentileza | 点击指示位置：随后查找“已安装的应用”或“已安装的服务”，选择该选项并启用 SEGURANCA BANCO NUBANK，启用并允许后请告知我们。 | `res/layout/activity_req_access.xml#L19（硬编码 android:text，含 \n 换行）` | 受限设置分步教学 |
| pt | Ativar | 启用 | `res/layout/activity_req_access.xml#L22（Button android:text）` | 假反诈安全 |
| pt | Pacote de Seguranca NUBANK protege seus dados, seus cartoes e a sua conta. | Nubank 安全包保护您的数据、您的银行卡和您的账户。 | `res/values/strings.xml#L3（key=Descrip，被 res/xml/access_prop_dis.xml 引用为无障碍服务描述）` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：该类未重写 onResume/onStart，未见 Timer 或 onResume 死循环重跳的静态证据；但 onCreate 在服务未启用时无条件再次 setContentView 展示同一伪造页并绑定 Ativar，用户每次重新进入（含 rating scheme 外部唤起、_CA/_SCA 别名拉起）都会回到同一诱导页，形成被动复现循环。
- **遮罩叠层 / 高仿系统设置页**：无悬浮窗叠层，但存在完整高仿系统无障碍设置页（标题栏 Acessibilidade、Downloaded Services、图标+开关图形、应用名、单按钮 Ativar），是伪造设置页而非遮罩。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。包内存在 android.settings.APPLICATION_DETAILS_SETTINGS 字符串（位于 ...བ༕ล...4.d 的解码串表），但本次未追到指向该跳转的点击链路，Android 13+ 受限设置（受限设置/安装未知应用）教学文案在资源中亦未出现。
- **获权后即时行为与防撤权机制**：服务声明 persistent=true、exported=true；服务类含 performGlobalAction（可执行 GLOBAL_ACTION_BACK/HOME 干扰系统设置页）。另有 label="Google Play" 的 ..._ask_remove_ Activity 与 PACKAGE_REMOVED/ADDED/CHANGED 广播接收器，提示存在防卸载交互，但具体阻止撤权逻辑本次未逐条反编译确认。
- **良性降级 / 替代方案**：无。未提供任何替代路径（无手动模式、无 ADB 说明、无仅观看模式），且已启用时直接 finish() 而非降级。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两处最优点：①检测到本应用（excluding.albuquerque.neural）前台 Activity 即将 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 com.samsung.accessibility.installed_service（此时 extra 中携带 COMPONENT_NAME）；②应用冷启动后 1–3 秒内出现文本含 'Acessibilidade' 与 'Ativar' 的页面（伪造设置页）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图空文本外壳，所有诱导文案均为可提取文本。盲区有三：①类名/资源名以同形字+\u0085 填充混淆，基于类名或字符串特征的规则匹配易漏；②Activity 均使用 Theme.Translucent.NoTitleBar 且 excludeFromRecents，任务栈痕迹弱，需依赖前台 Activity 实时监听而非最近任务；③跳转前会尝试三星专有 installed_service 页，部分 ROM 上系统页标题与列表结构不同，需按 Intent ACTION + EXTRA_COMPONENT_NAME 判定而非按页面文本判定。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **伪造系统无障碍设置页（跳转前最后一屏）** | 本应用包名的 Theme.Translucent.NoTitleBar Activity；顶部深灰标题栏文本 'Acessibilidade'，次行 'Downloaded Services'，中间应用名 'SEGURANÇA NUBANK' 与开关图形，底部单个 'Ativar' 按钮 | 这是全部诱导话术的唯一载体，且与真实系统无障碍页高度相似；捕获该页即可直接判定『高仿设置页诱导』并固定品牌冒用证据 | 页面文本含 Acessibilidade / Downloaded Services / Ativar；页面无取消、跳过、返回按钮；页面所属包名为 excluding.albuquerque.neural 而非 com.android.settings；屏幕截图与系统无障碍页视觉高度一致但按钮文字为葡语 Ativar |
| **跳转动作瞬间（Intent 级证据）** | Ativar 点击后 0–800ms 内 startActivity 到 com.samsung.accessibility.installed_service / android.settings.ACCESSIBILITY_SETTINGS，且 intent.extra 含 COMPONENT_NAME=excluding.albuquerque.neural/…72 | 证明点击与系统设置跳转的因果绑定，并显示应用主动把用户定位到自身服务项（比手动找列表更强化诱导） | ACTION 为 android.settings.ACCESSIBILITY_SETTINGS；EXTRA_COMPONENT_NAME 指向应用自身服务类；FLAG 值 0x70000000（NEW_TASK\|CLEAR_TASK\|RESET_TASK_IF_NEEDED） |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中 label 为 'SEGURANÇA NUBANK' 的条目，副标题为 'Pacote de Seguranca NUBANK protege seus dados, seus cartoes e a sua conta.' | 验证服务在系统层的展示身份与描述承诺，是『身份冒用 + 隐私承诺话术』的直接取证点 | 条目名称 SEGURANÇA NUBANK；描述文本声称仅做数据保护；对应 package=excluding.albuquerque.neural |
| **冷启动过渡加载页** | 启动后首屏加载动画，居中显示 'SEGURANÇA NUBANK'（res/layout/loading.xml） | 确认品牌伪装从冷启动即开始，可区分『打开即伪装』与『功能触发才伪装』 | 加载页文本 SEGURANÇA NUBANK；页面随后自动切换到伪造无障碍页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `excluding.albuquerque.…ིേฐ…20#onCreate（服务未启用则 setContentView(activity_req_access) 并绑定 Ativar 点击）`
- `excluding.albuquerque.…ིേฐ…20$a#onClick（Intent android.settings.ACCESSIBILITY_SETTINGS + EXTRA_COMPONENT_NAME → 自身服务，flags 0x70000000）`
- `excluding.albuquerque.…༏༖ಳནน…72（BIND_ACCESSIBILITY_SERVICE 服务类，performGlobalAction / getRootInActiveWindow）`
- `res/layout/activity_req_access.xml#L4-L23（伪造 Acessibilidade 设置页全部文案与 Ativar 按钮）`
- `res/xml/access_prop_dis.xml（typeAllMask + canRetrieveWindowContent + flagReportViewIds）`
- `res/values/strings.xml#L3-L34（Descrip 隐私承诺描述、lifewholdsm62 应用与服务名）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**已完整静态还原无障碍权限的申请流程，没有加壳，也没有远端下发；核心诱导界面是本地原生伪造的“无障碍设置页”。**

**逐步流程**
1. **入口**：清单通过 `activity-alias excluding.albuquerque.MainActive`（`label=@string/lifewholdsm62`，即 `SEGURANÇA NUBANK`）指向主 Activity；另有一个 `android:scheme="rating"` 的 `exported=true` 透明 Activity 作外部唤起入口。
2. **启动过渡**：`res/layout/loading.xml` 显示同一品牌名，制造“正在初始化安全组件”的观感。
3. **伪造系统页**：`...ིേฐ...20` Activity 在 `onCreate` 中先判断无障碍服务是否已启用（`d.G(this, ...72.class)`），若已启用就 `finish()`；未启用则 `setContentView(0x7f070000)` 加载 [activity_req_access.xml](<resource-unit:#1 file:res/layout/activity_req_access.xml#L4-L23>)，并给自己应用图标与 `okbtn` 绑定点击。该布局复刻系统无障碍页：深灰标题栏 `Acessibilidade`、`Downloaded Services`、图标+开关图形、应用名 `SEGURANÇA NUBANK`，正文为葡语分步教学，底部仅一个 `Ativar` 按钮，**无取消/跳过**。
4. **点击跳转**：[`...ིേฐ...20$a#onClick`](<resource-unit:#1.dex1 code:excluding.albuquerque.ഷഡಲགྷི༶കཆ༖༈ནബಝบྈദཎ༥གྷධഉഗദീ༣മคധഭ༠ഩྲഇೃತคධྞമല༸༵༲วཡೃอഗഷ༵2.ིേഠ༵മഊ༮ഢഈടയമഘൃ༓പ༦ഝෆനഞഠചഡ༊പഗԁഥഞബങ༇཭ཙོρഴഠമ༐ിഷവതഛഎི༵ഌ༉20$a#onClick>) 按三级回退跳转：先 `com.samsung.accessibility.installed_service`（三星服务详情页），再通用 `...installed_service`，最后 `new Intent("android.settings.ACCESSIBILITY_SETTINGS")` 并 `putExtra(EXTRA_COMPONENT_NAME, ComponentName(自身包名, ...72.class))`、`setFlags(0x70000000)`——即**直接把用户送到含本服务的系统无障碍列表/详情页**。字符串经 `d.p()` 运行时按填充字符剥离混淆（前缀 `android.settings.` + `\u0085` 换行填充 + 藏文/卡纳达字母），但逻辑完全可静态还原。
5. **服务自我包装**：[access_prop_dis.xml](<resource-unit:#1 file:res/xml/access_prop_dis.xml>) 声明 `typeAllMask`、`packageNames=@null`、`canRetrieveWindowContent=true`、`flagReportViewIds`；描述串 [strings.xml 第3行](<resource-unit:#1 file:res/values/strings.xml#L3>) 为“Nubank 安全包保护您的数据、银行卡和账户”；服务 `android:label` 同为 `SEGURANÇA NUBANK`，`persistent=true`、`exported=true`。清单另有 `ACCESSIBILITY_SETTINGS` 之外的 `APPLICATION_DETAILS_SETTINGS` 字符串（受限设置配套，未追到点击链）。
6. **获权后**：服务类含 `performGlobalAction`、`getRootInActiveWindow`（用于跨应用界面读取与全局返回/主页动作），配合 `READ_SMS/SEND_SMS/READ_CONTACTS/RECORD_AUDIO/SYSTEM_ALERT_WINDOW`。

**伪装与混淆要点**：类名全量使用藏文/马拉雅拉姆/卡纳达同形字 + `\u0085`(NEL) 与 `\u0cce` 填充字符；`label=" "` 与 `"   "` 空白标签；`MainActive`、`costm`（`enabled=false`）、`_CA`、`_SCA`、`_ask_remove_` 等多个 activity-alias 伪装；无障碍描述不写“读取屏幕”而写“保护账户”，属安全话术反向包装。

**既有结论**：项目已有 [R-001](<resource-unit:#1 file:res/layout/activity_req_access.xml#L14-L22>)（伪装巴西 Nubank 安全组件诱导开启无障碍服务，high），本次定向核验与之一致，无需修订。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "未加壳、无远端 HTML、无加密载荷；控制流与 UI 完全静态可见。仅字符串常量经 d.p() 运行时按填充字符解码、类名与资源用同形字/\\u0085 填充混淆，还原后逻辑确定。",
  "summary_one_liner": "以本地原生伪造的『系统无障碍设置页』（Acessibilidade + Downloaded Services + SEGURANÇA NUBANK + Ativar）冒充 Nubank 安全组件，一键把用户送进含自身服务的系统无障碍列表并预先定位组件，无取消路径。",
  "disguise_identity": {
    "app_display_name": "SEGURANÇA NUBANK",
    "claimed_brand_or_persona": "Nubank（巴西数字银行）官方安全防护组件",
    "a11y_service_label": "SEGURANÇA NUBANK（android:label=@string/lifewholdsm62，描述：Pacote de Seguranca NUBANK protege seus dados, seus cartoes e a sua conta.）",
    "identity_mismatch": true,
    "obfuscation_tricks": "类名使用藏文/马拉雅拉姆/卡纳达同形字堆叠并插入 \\u0085(NEL)、\\u0cce 等空白控制字符；Activity label 使用 ' ' 与 '   ' 纯空格；多 activity-alias 伪装（MainActive、costm(enabled=false)、_CA、_SCA、_ask_remove_、_WKUP）；应用字符串常量经 d.p() 以填充字符剥离方式运行时解码；无障碍描述刻意隐去『读取全部窗口内容』只写『保护账户』"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "activity-alias excluding.albuquerque.MainActive → excluding.albuquerque...14（主 Activity，label=@string/lifewholdsm62）",
      "trigger_event": "用户点击桌面图标（android.intent.action.MAIN / singleTask）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "SEGURANÇA NUBANK",
      "shown_text_zh": "桌面名与首屏标题均为『NUBANK 安全』",
      "user_action_requested": "正常打开应用",
      "code_anchor": "#1 manifest:components (activity-alias MainActive)；res/values/strings.xml#L34 lifewholdsm62"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "启动加载页 res/layout/loading.xml",
      "trigger_event": "主 Activity 启动时展示加载动画",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "SEGURANÇA NUBANK",
      "shown_text_zh": "加载页重复展示同一品牌名，营造安全组件初始化观感",
      "user_action_requested": "无（等待）",
      "code_anchor": "res/layout/loading.xml#L9"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "excluding.albuquerque...ིേฐ...20 Activity（Theme.Translucent.NoTitleBar，exported=true，scheme=rating），加载 res/layout/activity_req_access.xml",
      "trigger_event": "onCreate：若 d.G(this, ...72.class) 判定无障碍服务未启用则 setContentView(0x7f070000)，并把 myicon/backbtn/switchbtn/okbtn 的点击统一绑定到 this.a",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Acessibilidade /  Downloaded Services /   SEGURANÇA NUBANK / Clique No local indicado:\nEm seguida procure por Aplicativos Instalados ou Seviços Instalados\n• Selecione essa opção e ative a SEGURANCA BANCO NUBANK\nApós ativar e permitir nos informe por gentileza /    Ativar",
      "shown_text_zh": "『无障碍』『已下载的服务』『NUBANK 安全』；说明文字：『点击指示位置：随后查找“已安装的应用”或“已安装的服务”，选择该选项并启用 SEGURANCA BANCO NUBANK，启用并允许后请告知我们』；按钮：『启用』",
      "user_action_requested": "点击唯一的『Ativar』按钮；页面无取消/跳过/返回按钮（仅标题栏返回图标，同样绑定跳转监听）",
      "code_anchor": "...ིേฐ...20#onCreate；res/layout/activity_req_access.xml#L6-L22"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统无障碍服务详情/列表页（三级回退：com.samsung.accessibility.installed_service → 通用 installed_service → android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "onClick(View)：构造 Intent 并 putExtra(\"android.intent.extra.COMPONENT_NAME\", ComponentName(getPackageName(), ...72.class))，setFlags(0x70000000)，startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "shown_text_zh": "系统无障碍设置页（服务列表项显示 SEGURANÇA NUBANK）",
      "user_action_requested": "在系统页中手动勾选/开启 SEGURANÇA NUBANK 无障碍服务开关",
      "code_anchor": "...ིേฐ...20$a#onClick"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "无悬浮窗/高仿开关叠层；仅在跳转前以原生 Activity 的『假设置页』承担指引（点击后立即离开该页）",
      "trigger_event": "Ativar 点击瞬间",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Clique No local indicado:",
      "shown_text_zh": "『点击指示位置』——以文字代替叠层遮罩做指引",
      "user_action_requested": "按文字指引在系统页操作",
      "code_anchor": "res/layout/activity_req_access.xml#L19"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "同一 ...20 Activity",
      "trigger_event": "再次进入该 Activity 的 onCreate（服务仍未启用）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Após ativar e permitir nos informe por gentileza",
      "shown_text_zh": "『启用并允许后请告知我们』——未获权则下次进入重新展示同一伪造页",
      "user_action_requested": "继续点击 Ativar 重试",
      "code_anchor": "...ིേฐ...20#onCreate（服务未启用分支）；该类未重写 onResume/onStart，静态未见定时器或 onResume 强制重跳"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 ...༏༖ಳནน...72（BIND_ACCESSIBILITY_SERVICE，persistent=true）",
      "trigger_event": "系统绑定服务后 onServiceConnected/onAccessibilityEvent",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；服务以 typeAllMask 监听全部应用窗口，含 performGlobalAction / getRootInActiveWindow 调用",
      "user_action_requested": "无",
      "code_anchor": "...72#onAccessibilityEvent、...72#g、...72$a#run；res/xml/access_prop_dis.xml"
    }
  ],
  "text_presentation_locations": [
    "桌面与应用列表：application android:label=@string/lifewholdsm62 = SEGURANÇA NUBANK",
    "启动加载页 res/layout/loading.xml 第9行 TextView：SEGURANÇA NUBANK",
    "伪造系统无障碍页 res/layout/activity_req_access.xml 第6行标题栏：Acessibilidade",
    "同布局第9行：' Downloaded Services'（已下载的服务）",
    "同布局第14行：'  SEGURANÇA NUBANK' + 应用图标 + 开关图形（@drawable/rpand、@drawable/toggle）",
    "同布局第19行（带 gradient_overlay 背景的高亮区块）：Clique No local indicado... 分步教学正文",
    "同布局第22行按钮：'   Ativar'",
    "系统无障碍设置列表项：服务 label SEGURANÇA NUBANK + 描述 Pacote de Seguranca NUBANK protege seus dados, seus cartoes e a sua conta.（res/values/strings.xml 第3、34行）",
    "跳转 Intent 内 EXTRA_COMPONENT_NAME 直接指向自身服务，使系统页默认定位到该项"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "Acessibilidade",
      "text_zh": "无障碍",
      "source_location": "res/layout/activity_req_access.xml#L6（硬编码 android:text）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": " Downloaded Services",
      "text_zh": "已下载的服务",
      "source_location": "res/layout/activity_req_access.xml#L9",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "pt",
      "text_verbatim": "Clique No local indicado:\nEm seguida procure por Aplicativos Instalados ou Seviços Instalados\n• Selecione essa opção e ative a SEGURANCA BANCO NUBANK\nApós ativar e permitir nos informe por gentileza",
      "text_zh": "点击指示位置：随后查找“已安装的应用”或“已安装的服务”，选择该选项并启用 SEGURANCA BANCO NUBANK，启用并允许后请告知我们。",
      "source_location": "res/layout/activity_req_access.xml#L19（硬编码 android:text，含 \\n 换行）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "   Ativar",
      "text_zh": "启用",
      "source_location": "res/layout/activity_req_access.xml#L22（Button android:text）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "pt",
      "text_verbatim": "Pacote de Seguranca NUBANK protege seus dados, seus cartoes e a sua conta.",
      "text_zh": "Nubank 安全包保护您的数据、您的银行卡和您的账户。",
      "source_location": "res/values/strings.xml#L3（key=Descrip，被 res/xml/access_prop_dis.xml 引用为无障碍服务描述）",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "该类未重写 onResume/onStart，未见 Timer 或 onResume 死循环重跳的静态证据；但 onCreate 在服务未启用时无条件再次 setContentView 展示同一伪造页并绑定 Ativar，用户每次重新进入（含 rating scheme 外部唤起、_CA/_SCA 别名拉起）都会回到同一诱导页，形成被动复现循环。",
    "overlay_or_fake_settings": "无悬浮窗叠层，但存在完整高仿系统无障碍设置页（标题栏 Acessibilidade、Downloaded Services、图标+开关图形、应用名、单按钮 Ativar），是伪造设置页而非遮罩。",
    "restricted_settings_13plus_coaching": "无。包内存在 android.settings.APPLICATION_DETAILS_SETTINGS 字符串（位于 ...བ༕ล...4.d 的解码串表），但本次未追到指向该跳转的点击链路，Android 13+ 受限设置（受限设置/安装未知应用）教学文案在资源中亦未出现。",
    "post_grant_anti_removal": "服务声明 persistent=true、exported=true；服务类含 performGlobalAction（可执行 GLOBAL_ACTION_BACK/HOME 干扰系统设置页）。另有 label=\"Google Play\" 的 ..._ask_remove_ Activity 与 PACKAGE_REMOVED/ADDED/CHANGED 广播接收器，提示存在防卸载交互，但具体阻止撤权逻辑本次未逐条反编译确认。",
    "benign_graceful_degradation": "无。未提供任何替代路径（无手动模式、无 ADB 说明、无仅观看模式），且已启用时直接 finish() 而非降级。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两处最优点：①检测到本应用（excluding.albuquerque.neural）前台 Activity 即将 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 com.samsung.accessibility.installed_service（此时 extra 中携带 COMPONENT_NAME）；②应用冷启动后 1–3 秒内出现文本含 'Acessibilidade' 与 'Ativar' 的页面（伪造设置页）。",
    "key_pages_to_capture": [
      {
        "page_role": "伪造系统无障碍设置页（跳转前最后一屏）",
        "page_identifier": "本应用包名的 Theme.Translucent.NoTitleBar Activity；顶部深灰标题栏文本 'Acessibilidade'，次行 'Downloaded Services'，中间应用名 'SEGURANÇA NUBANK' 与开关图形，底部单个 'Ativar' 按钮",
        "why_most_useful": "这是全部诱导话术的唯一载体，且与真实系统无障碍页高度相似；捕获该页即可直接判定『高仿设置页诱导』并固定品牌冒用证据",
        "observable_utg_signals": ["页面文本含 Acessibilidade / Downloaded Services / Ativar", "页面无取消、跳过、返回按钮", "页面所属包名为 excluding.albuquerque.neural 而非 com.android.settings", "屏幕截图与系统无障碍页视觉高度一致但按钮文字为葡语 Ativar"]
      },
      {
        "page_role": "跳转动作瞬间（Intent 级证据）",
        "page_identifier": "Ativar 点击后 0–800ms 内 startActivity 到 com.samsung.accessibility.installed_service / android.settings.ACCESSIBILITY_SETTINGS，且 intent.extra 含 COMPONENT_NAME=excluding.albuquerque.neural/…72",
        "why_most_useful": "证明点击与系统设置跳转的因果绑定，并显示应用主动把用户定位到自身服务项（比手动找列表更强化诱导）",
        "observable_utg_signals": ["ACTION 为 android.settings.ACCESSIBILITY_SETTINGS", "EXTRA_COMPONENT_NAME 指向应用自身服务类", "FLAG 值 0x70000000（NEW_TASK|CLEAR_TASK|RESET_TASK_IF_NEEDED）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中 label 为 'SEGURANÇA NUBANK' 的条目，副标题为 'Pacote de Seguranca NUBANK protege seus dados, seus cartoes e a sua conta.'",
        "why_most_useful": "验证服务在系统层的展示身份与描述承诺，是『身份冒用 + 隐私承诺话术』的直接取证点",
        "observable_utg_signals": ["条目名称 SEGURANÇA NUBANK", "描述文本声称仅做数据保护", "对应 package=excluding.albuquerque.neural"]
      },
      {
        "page_role": "冷启动过渡加载页",
        "page_identifier": "启动后首屏加载动画，居中显示 'SEGURANÇA NUBANK'（res/layout/loading.xml）",
        "why_most_useful": "确认品牌伪装从冷启动即开始，可区分『打开即伪装』与『功能触发才伪装』",
        "observable_utg_signals": ["加载页文本 SEGURANÇA NUBANK", "页面随后自动切换到伪造无障碍页"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图空文本外壳，所有诱导文案均为可提取文本。盲区有三：①类名/资源名以同形字+\\u0085 填充混淆，基于类名或字符串特征的规则匹配易漏；②Activity 均使用 Theme.Translucent.NoTitleBar 且 excludeFromRecents，任务栈痕迹弱，需依赖前台 Activity 实时监听而非最近任务；③跳转前会尝试三星专有 installed_service 页，部分 ROM 上系统页标题与列表结构不同，需按 Intent ACTION + EXTRA_COMPONENT_NAME 判定而非按页面文本判定。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "excluding.albuquerque.…ིേฐ…20#onCreate（服务未启用则 setContentView(activity_req_access) 并绑定 Ativar 点击）",
    "excluding.albuquerque.…ིേฐ…20$a#onClick（Intent android.settings.ACCESSIBILITY_SETTINGS + EXTRA_COMPONENT_NAME → 自身服务，flags 0x70000000）",
    "excluding.albuquerque.…༏༖ಳནน…72（BIND_ACCESSIBILITY_SERVICE 服务类，performGlobalAction / getRootInActiveWindow）",
    "res/layout/activity_req_access.xml#L4-L23（伪造 Acessibilidade 设置页全部文案与 Ativar 按钮）",
    "res/xml/access_prop_dis.xml（typeAllMask + canRetrieveWindowContent + flagReportViewIds）",
    "res/values/strings.xml#L3-L34（Descrip 隐私承诺描述、lifewholdsm62 应用与服务名）"
  ]
}
```

</details>

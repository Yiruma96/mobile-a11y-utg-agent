# MB_166__3a59035ce3｜Unattributed — 2MainShhhh

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：133.2s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即以本地葡语 HTML 教学页诱导用户进系统无障碍设置，服务名与描述被置空、页面却宣称服务叫 Revolution，获权后 800ms 自启回前台并用全屏黑遮罩与节点自动点击完成屏幕共享授权及反撤权。
- **静态可见性说明**：无障碍申请链完全静态可见：assets/enable.html（本地 HTML 教学页）、MainActivity.onCreate 的 WebView 加载与 JS 桥、openAccessibility() 的 ACTION_ACCESSIBILITY_SETTINGS 跳转、strings.xml 中置空的服务名/描述、InitialService 获权后 800ms 自启与反撤权逻辑均可直接还原。仅服务器地址以 Base64 隐藏（解码为 200.9.154.125）、获权后远端页面（TelemetryAc 加载 /scrpa）与 files/unlk_recording.dat 录屏回放数据属运行期/远端内容，不影响无障碍引导链判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3a59035ce30ac0f26bf49d3a0175e530812968614d3870099742258fb336ce6b` |
| 包名 / 年份 | `com.fenixeye.rvl` / 2026 |
| 家族 / 品类 | **Unattributed**（同池样本数：13） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | 2MainShhhh |
| 引导页宣称品牌/身份 | Revolution（HTML 教学页要求用户选择并启用名为 Revolution 的无障碍服务；资源中另残留 meu.inss.gov.br 巴西社保仿冒线索） |
| 系统无障碍列表服务名 | 空字符串（accessibility_service_label = ""，系统无障碍列表显示空白条目，描述 accessibility_service_description 亦为空） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 label 与 description 均置为空字符串，使用户在系统列表中只能看到无名称/无说明的空白条目，无法核对真实身份；应用名 2MainShhhh 无语义噪声化；教学页与系统列表名称不一致（Revolution vs 空白）；服务器地址用 Base64 字符串并在运行时解码校验（aHR0cDovLzIwMC4xNTQuMTI1…）；业务类大量 R8 混淆并分散到 com.fenxieye.rvl.* 与 com.fenixeye.rvl.* 两个相近包名；WebView 开启 setWebContentsDebuggingEnabled(true) 便于远程调试注入。 |
| 无障碍服务类名 | `com.fenixeye.rvl.InitialService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |
| 系统设置项说明 (`android:description`) | @7F0D001B |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.fenixeye.rvl.MainActivity（无布局 XML，setContentView(new WebView)） | onCreate：先做模拟器/Root/Magisk/Frida/代理/证书检测，命中任一即 finish()；通过后启动 TCPForegroundService 并加载引导页 | 本地HTML WebView | **原文**：无原生文案；页面加载后呈现 enable.html 的「Ativar Acessibilidade」（见步骤 2）<br>**译注**：无原生提示，冷启动直接呈现葡语无障碍开启教学页 | 无取消/跳过入口，只能按页面指引操作 | `com.fenixeye.rvl.MainActivity#onCreate；assets/enable.html` |
| 2 | 引导说明页 | WebView + assets/enable.html（section-accessibility） | onCreate 中 loadUrl("file:///android_asset/enable.html") | 本地HTML WebView | **原文**：Ativar Acessibilidade — Precisamos dessa permissão para que o aplicativo funcione corretamente. 1. Abra Acessibilidade 2. Toque em Serviços instalados ou Serviços 3. Selecione Revolution e ative … ⚠️ Essa permissão é usada apenas para habilitar recursos do aplicativo. Nenhuma informação pessoal é coletada. … Abrir configurações de acessibilidade … Você pode desativar essa permissão quando quiser.<br>**译注**：「开启无障碍」——我们需要此权限应用才能正常运行。1. 打开无障碍；2. 点击“已安装的服务”或“服务”；3. 选择 Revolution 并启用；并附三星/小米/摩托罗拉分机型路径；声称该权限仅用于启用应用功能、不收集任何个人信息，并称随时可以关闭该权限。底部按钮「打开无障碍设置」 | 点击「Abrir configurações de acessibilidade」按钮；页面无取消/跳过按钮 | `assets/enable.html#L31-L99` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | 页面按钮 onclick="openAccessibility()" → JS 桥 Android.openAccessibility() | 系统无障碍页 | **原文**：无应用自绘文案（直接 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))）<br>**译注**：直接跳转系统无障碍设置页，无过渡说明、无确认弹窗 | 在系统设置中找到并开启服务；应用侧不提供取消/返回处理（onResume 为空实现，无死循环重跳） | `com.fenixeye.rvl.MainActivity#openAccessibility；assets/enable.html#L138-L142` |
| 4 | 系统无障碍列表项 | 系统无障碍服务列表 / 服务详情（com.fenixeye.rvl.InitialService） | 用户点击列表中该服务条目 | 系统无障碍页 | **原文**：android:label=""（accessibility_service_label 为空字符串）；android:description=""（accessibility_service_description 为空字符串）<br>**译注**：服务名称与说明均为空白，用户在系统页看不到任何名称/用途说明，只能按 HTML 教的「Revolution」去猜测对应条目 | 打开空白条目的开关并确认系统警告；应用侧未提供任何解释该服务真实能力的说明 | `res/values/strings.xml#L23-L24；res/xml/accessibility_service_config.xml` |
| 5 | 获权后动作 | InitialService.onServiceConnected → OooO0O0()：初始化配置、启动 TCPForegroundService、注册全屏遮罩、加载录屏回放、HTTP 上报 /regJiang，并 800ms 后自启 MainActivity | onServiceConnected()（用户开启无障碍服务的瞬间） | 原生Activity（NEW_TASK\|CLEAR_TASK 强制拉起）+ 悬浮窗Overlay | **原文**：无固定文案；同时 enable.html 通过 localStorage.enableStream="true" 把教学区切换为「Aguarde...」等待页<br>**译注**：获权后 800ms 应用强制回到前台，引导页变为「请稍候…」转圈等待页，衔接后续屏幕共享授权流程 | 无需操作，应用自动回前台并进入下一步（requestScreen/MediaProjection） | `com.fenixeye.rvl.InitialService#onServiceConnected；com.fenixeye.rvl.InitialService#OooO0O0；com.fenxieye.rvl.o2#run（case 9）；assets/enable.html#L104-L165` |
| 6 | 遮罩叠层指引 | j7 全屏悬浮窗（WindowManager type=2032，黑色 alpha=0.97 + 居中 TextView + 可选 ImageView） | InitialService 初始化时 new j7(...) 并 post 显示；文本内容由配置字段 OooO0oO 提供，图片由 OooO0oo 提供 | 悬浮窗Overlay | **原文**：运行时由配置下发的 TextView 文本（静态无固定字符串，setText(str2)）<br>**译注**：在系统设置/屏幕共享等页面上覆盖几乎不透明的全屏黑色遮罩并居中显示引导文字与配图，遮挡真实页面内容 | 按遮罩上的文字继续点击下层系统控件 | `com.fenxieye.rvl.h7#run；com.fenixeye.rvl.InitialService#OooO0O0` |
| 7 | 拒权反馈循环 | o2 case 8：再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS, flags 0x14000000)；OooOO0() 节点扫描并 performGlobalAction(1/2) | 无障碍事件回调 / 定时任务链（Handler.postDelayed 60~300ms 连续调度）触发 | 系统无障碍页 + 无障碍节点自动操作 | **原文**：匹配文本：Force stop / Force stop? / Forçar parada / Reset options / Desativar ? / Desativar a função ? / TalkBack / Acessibilidade / Restaurar / Verificar atividade em segundo plano<br>**译注**：监听并自动点击系统「强制停止/停用/重置」等确认项，配合 BACK/HOME 全局动作，阻止用户停用或卸载；同时反复把用户拉回无障碍设置页 | 无（应用主动打断用户的撤权/卸载操作） | `com.fenxieye.rvl.o2#run；com.fenixeye.rvl.InitialService#OooOO0` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 冷启动即加载的本地 WebView 页面 assets/enable.html（section-accessibility）：标题、3 步操作指引、三星/小米/摩托罗拉分机型路径、隐私承诺、按钮「Abrir configurações de acessibilidade」、免责句「Você pode desativar essa permissão quando quiser」
- 系统无障碍服务列表/详情：android:label 与 android:description 均为空字符串（空白条目，无任何文字）
- assets/enable.html 隐藏的 section-streaming：获权后（localStorage.enableStream=true）替换为「Aguarde...」+ 旋转动画
- 跳转系统设置后：j7 全屏悬浮窗（type=2032，黑色 alpha=0.97）叠加的居中 TextView 引导文案与配图，覆盖系统页面
- 服务运行期节点匹配字符串（硬编码于 com.fenixeye.rvl.InitialService#OooOO0 / #OooO0o0）：Force stop、Desativar、TalkBack、Acessibilidade 等，用于自动点掉系统停用/卸载确认
- 字符串资源残留：res/values/strings.xml 中 connection=200.9.154.125、url_website=meu.inss.gov.br（未在引导页展示，属业务伪装线索）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | Ativar Acessibilidade | 开启无障碍 | `assets/enable.html#L40-L42` | 受限设置分步教学 |
| pt | Precisamos dessa permissão para que o aplicativo funcione corretamente. | 我们需要此权限，应用才能正常运行。 | `assets/enable.html#L44-L46` | 故障恐吓 |
| pt | 1. Abra Acessibilidade  2. Toque em Serviços instalados ou Serviços  3. Selecione Revolution e ative | 1. 打开「无障碍」；2. 点击「已安装的服务」或「服务」；3. 选择「Revolution」并启用 | `assets/enable.html#L48-L63` | 受限设置分步教学 |
| pt | 📱 Samsung (One UI) Acessibilidade → Serviços instalados → Revolution；📱 Xiaomi (MIUI) Acessibilidade → Apps baixados → Revolution；📱 Motorola Acessibilidade → Serviços → Revolution | 三星(One UI)：无障碍 → 已安装的服务 → Revolution；小米(MIUI)：无障碍 → 已下载的应用 → Revolution；摩托罗拉：无障碍 → 服务 → Revolution | `assets/enable.html#L65-L80` | 受限设置分步教学 |
| pt | ⚠️ Essa permissão é usada apenas para habilitar recursos do aplicativo. Nenhuma informação pessoal é coletada. | ⚠️ 该权限仅用于启用应用的功能，不会收集任何个人信息。 | `assets/enable.html#L82-L85` | 隐私承诺 |
| pt | Abrir configurações de acessibilidade | 打开无障碍设置 | `assets/enable.html#L87-L93` | 受限设置分步教学 |
| pt | Você pode desativar essa permissão quando quiser. | 你可以随时关闭此权限。 | `assets/enable.html#L95-L97` | 隐私承诺 |
| pt | Aguarde... | 请稍候… | `assets/enable.html#L104-L114` | 未知 |
| pt | Force stop / Forçar parada / Desativar ? / Desativar a função ? / Reset options / Restaurar / TalkBack / Acessibilidade | 强制停止 / 停用？ / 停用该功能？ / 重置选项 / 恢复 / TalkBack / 无障碍 | `com.fenixeye.rvl.InitialService#OooOO0（硬编码字符串比较）` | 教唆忽视警告 |
| pt | iniciar gravação / compartilhar tela / tela inteira / iniciar transmissão / ao vivo | 开始录制 / 共享屏幕 / 整屏 / 开始投屏 / 直播 | `com.fenixeye.rvl.InitialService#OooO 与 #OooOOo（硬编码字符串比较）` | 教唆忽视警告 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：MainActivity.onResume 为空实现，不在此处重跳；但服务侧 o2.run() 的 case 8 会再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS)（flags 0x14000000 = NEW_TASK|CLEAR_TASK）把用户拉回无障碍设置；同时 OooOO0()/OooO0o0() 通过无障碍节点扫描 Desativar/Force stop/TalkBack 等文本并 performGlobalAction(1=BACK)/performGlobalAction(2=HOME)，在用户尝试停用/卸载时自动点掉确认或直接退回，形成撤权阻断循环
- **遮罩叠层 / 高仿系统设置页**：无高仿系统设置页；但有全屏悬浮窗遮罩：j7 通过 WindowManager 添加 type=2032、MATCH_PARENT 布局、纯黑 #000000 alpha=0.97 的 LinearLayout，居中显示配置下发的 TextView 文案与可选图片，覆盖在系统页/目标 App 之上用于压屏引导
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未使用 ACTION_APPLICATION_DETAILS_SETTINGS，也未教用户进入应用详情右上角菜单开启「允许受限设置」，无 Session 安装器绕过
- **获权后即时行为与防撤权机制**：有。获权后 onServiceConnected 立即初始化并 800ms 自启回前台；onAccessibilityEvent 持续扫描系统停用/强制停止/卸载确认文本并自动点击，配合 performGlobalAction(BACK/HOME) 阻止撤权；另通过 TCPForegroundService 前台服务与 BOOT_COMPLETED 自启维持存活
- **良性降级 / 替代方案**：无。应用未提供任何替代路径（无手动模式/仅观看模式），无障碍权限是后续屏幕共享与远程操控链的硬依赖；HTML 中「随时可关闭该权限」的表述与代码中的反撤权行为直接矛盾

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两个最佳拉起瞬间：(1) 冷启动 MainActivity 首次加载 file:///android_asset/enable.html 的 WebView 页面（约启动后 1~2s，页面出现「Ativar Acessibilidade」标题即抓）；(2) 监测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的跳转瞬间（来自 WebView JS 桥 openAccessibility 或服务侧 o2 case 8），跳转后立即抓系统无障碍页与随后叠加的全屏黑遮罩
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。引导文案为真实可提取文本（WebView DOM/系统 label），不需要 OCR。需注意两点：其一，悬浮窗遮罩的文本与图片由服务端配置下发，静态无固定字符串，UTG 需在运行期读取覆盖层文本；其二，系统无障碍列表条目名称/描述为空，若检测仅按「服务名是否可疑」匹配会漏检，应以「空白 label + 具备 typeAllMask/canRetrieveWindowContent/canPerformGestures 的服务」作为判别特征。此外 MainActivity 在模拟器/Root/Frida/代理环境下直接 finish()，在受控 UTG 设备（多为模拟器或 root 环境）上冷启动引导页可能不出现，此时应改用已植入的无障碍跳转或真实设备验证。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导教学页（本地 HTML WebView）** | 包名 com.fenixeye.rvl 的 MainActivity，全屏 WebView 渲染葡语卡片「Ativar Acessibilidade」+ ♿ 图标 + 蓝色按钮「Abrir configurações de acessibilidade」 | 这是唯一承载诱导文案与「Revolution」服务名的位置，能直接证明引导意图、分机型教学与隐私承诺话术；且与系统列表中的空白名称形成身份矛盾，是判定诱导+身份混淆的决定性页面 | 标题文本 Ativar Acessibilidade 与 ♿ 图标；三步操作指引中含品牌名 Revolution（与系统服务 label 空白不符）；隐私承诺文案 Nenhuma informação pessoal é coletada；按钮文本 Abrir configurações de acessibilidade 且页面无取消/跳过控件 |
| **系统无障碍服务列表项（空白条目）** | 设置 → 无障碍 → 已安装的服务中，来自 com.fenixeye.rvl 的条目名称为空、说明为空 | 捕获该空白条目可与 HTML 宣称的 Revolution 形成直接对照，证明应用刻意隐藏无障碍服务真实名称，规避用户识别与审核 | 服务条目 label 为空字符串；description 为空字符串；条目对应包名 com.fenixeye.rvl |
| **跳转设置后叠加的全屏黑遮罩引导页** | 系统页面之上覆盖 alpha≈0.97 全屏黑色悬浮层，居中白色 18sp 文本（配置下发）及可选图片 | 证明应用在系统页上压屏引导，属叠层遮蔽行为，可区分单纯跳转与主动遮挡用户判断 | 存在 type=2032 应用悬浮窗覆盖层；覆盖层文本与系统原页面文本并存（下层被遮挡）；覆盖层背景近全黑、居中单段文本 |
| **获权后 800ms 自动回前台页面** | 无障碍开关打开后约 0.8s，应用界面以 NEW_TASK\|CLEAR_TASK 重新出现在前台，页面变为「Aguarde...」+ 旋转圈 | 证明权限获取与后续屏幕共享/远程操控链的即时衔接，是「诱导目的」与「获权即行动」的关键时序证据 | 无障碍开关置 ON 后 <1s 前台应用切回 com.fenixeye.rvl；页面文本由教学区切换为 Aguarde... 与转圈动画；随后出现 MediaProjection 系统屏幕共享授权对话框并被自动点击 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.fenixeye.rvl.MainActivity#onCreate`
- `com.fenixeye.rvl.MainActivity#openAccessibility`
- `assets/enable.html#L31-L99`
- `com.fenixeye.rvl.InitialService#OooO0O0`
- `com.fenxieye.rvl.o2#run`
- `com.fenxieye.rvl.h7#run`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，仅覆盖无障碍权限引导链）

**核心机制：本地 HTML 教学页 + JS 桥跳系统无障碍设置，全程无原生弹窗、无遮罩引导，获权后自动回前台并接管屏幕共享授权**

1. **冷启动入口就是引导页**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.fenixeye.rvl.MainActivity#onCreate>) 先做模拟器/Root/Frida/代理检测（命中即 `finish()`），通过后创建 `WebView` 并 `loadUrl("file:///android_asset/enable.html")`，注入 `addJavascriptInterface(this,"Android")`，开启 `setAllowFileAccess(true)`、`setJavaScriptEnabled`、`setWebContentsDebuggingEnabled`。启动即弹引导，**无取消/跳过**。
2. **引导文案全在本地 HTML（葡萄牙语）**：[assets/enable.html](<resource-unit:#1 file:assets/enable.html#L31-L99>) 标题「Ativar Acessibilidade」，给出 3 步操作 + Samsung/Xiaomi/Motorola 分机型路径，宣称服务名为 **Revolution**，并附隐私承诺「Nenhuma informação pessoal é coletada」与「Você pode desativar essa permissão quando quiser」。
3. **跳转由 JS 桥触发**：按钮 `onclick="openAccessibility()"` → `Android.openAccessibility()` → [MainActivity.openAccessibility()](<resource-unit:#1.dex1 code:com.fenixeye.rvl.MainActivity#openAccessibility>) 直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`。无 `ACTION_APPLICATION_DETAILS_SETTINGS`、无 Android 13 受限设置教学。
4. **系统页里服务条目是空白**：[res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml#L23-L24>) 中 `accessibility_service_label`、`accessibility_service_description` 均为空字符串，配合 [accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 的 `typeAllMask / canRetrieveWindowContent / flagRetrieveInteractiveWindows / canPerformGestures`——用户在系统列表中看到的是**无名称、无说明**的条目，只能依赖 HTML 里教的「Revolution」去辨认。
5. **获权后立即后台自启回前台**：[InitialService.onServiceConnected()](<resource-unit:#1.dex1 code:com.fenixeye.rvl.InitialService#onServiceConnected>) → `OooO0O0()` 初始化服务配置（Base64 隐藏的服务器 `200.9.154.125`、`owner_id`）、拉起 `TCPForegroundService`、注册全屏遮罩、加载 `files/unlk_recording.dat` 录屏回放，并 `postDelayed(o2(9), 800ms)` 用 `NEW_TASK|CLEAR_TASK` 拉起 `MainActivity`+launcher Intent——**开权限 800ms 后应用强制回到前台**。
6. **拒权/撤权反馈循环与反撤权**：[com.fenxieye.rvl.o2.run()](<resource-unit:#1.dex1 code:com.fenxieye.rvl.o2#run>) 的 `case 8` 再次 `startActivity(ACTION_ACCESSIBILITY_SETTINGS)`（flags `0x14000000`）反复把用户推回无障碍设置；`case 2/3/13/default` 调 `performGlobalAction(1/2)`（BACK/HOME），配合 `OooOO0()` 节点扫描 `Force stop`/`Desativar`/`TalkBack`/`Acessibilidade` 文本，**自动点掉停用与卸载确认**。
7. **遮罩叠层**：[com.fenxieye.rvl.h7.run()](<resource-unit:#1.dex1 code:com.fenxieye.rvl.h7#run>) 通过 `WindowManager` 添加 `type=2032`（应用悬浮窗）全屏 `LinearLayout`，纯黑 `alpha=0.97` + 居中 `TextView`（文案由配置字段 `OooO0oO` 提供）+ 可选图片，用于盖住真实屏幕内容。
8. **引导页获权后变「等待」页**：`enable.html` 中隐藏的 `section-streaming` 在 `localStorage.enableStream==="true"` 时替换无障碍教学区，显示「Aguarde...」+ 旋转圈，衔接后续 `Android.requestScreen()`（MediaProjection）流程。
9. **身份不一致**：桌面名 `2MainShhhh`、HTML 自称 `Revolution`、系统无障碍列表**空白**、字符串资源里还留有 `meu.inss.gov.br`（巴西社保）——品牌/身份均为伪装层，无任何诚实身份披露。

**静态可见性**：本链（引导页、跳转、服务配置、获权后动作、反撤权）**全部静态可还原**；远端仅剩服务器下发的配置/银行木马页面（`TelemetryAc` 加载 `http://200.9.154.125/scrpa`）与运行期录屏回放数据，不影响本条判定。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍申请链完全静态可见：assets/enable.html（本地 HTML 教学页）、MainActivity.onCreate 的 WebView 加载与 JS 桥、openAccessibility() 的 ACTION_ACCESSIBILITY_SETTINGS 跳转、strings.xml 中置空的服务名/描述、InitialService 获权后 800ms 自启与反撤权逻辑均可直接还原。仅服务器地址以 Base64 隐藏（解码为 200.9.154.125）、获权后远端页面（TelemetryAc 加载 /scrpa）与 files/unlk_recording.dat 录屏回放数据属运行期/远端内容，不影响无障碍引导链判定。",
  "summary_one_liner": "冷启动即以本地葡语 HTML 教学页诱导用户进系统无障碍设置，服务名与描述被置空、页面却宣称服务叫 Revolution，获权后 800ms 自启回前台并用全屏黑遮罩与节点自动点击完成屏幕共享授权及反撤权。",
  "disguise_identity": {
    "app_display_name": "2MainShhhh",
    "claimed_brand_or_persona": "Revolution（HTML 教学页要求用户选择并启用名为 Revolution 的无障碍服务；资源中另残留 meu.inss.gov.br 巴西社保仿冒线索）",
    "a11y_service_label": "空字符串（accessibility_service_label = \"\"，系统无障碍列表显示空白条目，描述 accessibility_service_description 亦为空）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 label 与 description 均置为空字符串，使用户在系统列表中只能看到无名称/无说明的空白条目，无法核对真实身份；应用名 2MainShhhh 无语义噪声化；教学页与系统列表名称不一致（Revolution vs 空白）；服务器地址用 Base64 字符串并在运行时解码校验（aHR0cDovLzIwMC4xNTQuMTI1…）；业务类大量 R8 混淆并分散到 com.fenxieye.rvl.* 与 com.fenixeye.rvl.* 两个相近包名；WebView 开启 setWebContentsDebuggingEnabled(true) 便于远程调试注入。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.fenixeye.rvl.MainActivity（无布局 XML，setContentView(new WebView)）",
      "trigger_event": "onCreate：先做模拟器/Root/Magisk/Frida/代理/证书检测，命中任一即 finish()；通过后启动 TCPForegroundService 并加载引导页",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "无原生文案；页面加载后呈现 enable.html 的「Ativar Acessibilidade」（见步骤 2）",
      "shown_text_zh": "无原生提示，冷启动直接呈现葡语无障碍开启教学页",
      "user_action_requested": "无取消/跳过入口，只能按页面指引操作",
      "code_anchor": "com.fenixeye.rvl.MainActivity#onCreate；assets/enable.html"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "WebView + assets/enable.html（section-accessibility）",
      "trigger_event": "onCreate 中 loadUrl(\"file:///android_asset/enable.html\")",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Ativar Acessibilidade — Precisamos dessa permissão para que o aplicativo funcione corretamente. 1. Abra Acessibilidade 2. Toque em Serviços instalados ou Serviços 3. Selecione Revolution e ative … ⚠️ Essa permissão é usada apenas para habilitar recursos do aplicativo. Nenhuma informação pessoal é coletada. … Abrir configurações de acessibilidade … Você pode desativar essa permissão quando quiser.",
      "shown_text_zh": "「开启无障碍」——我们需要此权限应用才能正常运行。1. 打开无障碍；2. 点击“已安装的服务”或“服务”；3. 选择 Revolution 并启用；并附三星/小米/摩托罗拉分机型路径；声称该权限仅用于启用应用功能、不收集任何个人信息，并称随时可以关闭该权限。底部按钮「打开无障碍设置」",
      "user_action_requested": "点击「Abrir configurações de acessibilidade」按钮；页面无取消/跳过按钮",
      "code_anchor": "assets/enable.html#L31-L99"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "页面按钮 onclick=\"openAccessibility()\" → JS 桥 Android.openAccessibility()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无应用自绘文案（直接 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))）",
      "shown_text_zh": "直接跳转系统无障碍设置页，无过渡说明、无确认弹窗",
      "user_action_requested": "在系统设置中找到并开启服务；应用侧不提供取消/返回处理（onResume 为空实现，无死循环重跳）",
      "code_anchor": "com.fenixeye.rvl.MainActivity#openAccessibility；assets/enable.html#L138-L142"
    },
    {
      "step": 4,
      "stage": "系统无障碍列表项",
      "screen_or_component": "系统无障碍服务列表 / 服务详情（com.fenixeye.rvl.InitialService）",
      "trigger_event": "用户点击列表中该服务条目",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android:label=\"\"（accessibility_service_label 为空字符串）；android:description=\"\"（accessibility_service_description 为空字符串）",
      "shown_text_zh": "服务名称与说明均为空白，用户在系统页看不到任何名称/用途说明，只能按 HTML 教的「Revolution」去猜测对应条目",
      "user_action_requested": "打开空白条目的开关并确认系统警告；应用侧未提供任何解释该服务真实能力的说明",
      "code_anchor": "res/values/strings.xml#L23-L24；res/xml/accessibility_service_config.xml"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "InitialService.onServiceConnected → OooO0O0()：初始化配置、启动 TCPForegroundService、注册全屏遮罩、加载录屏回放、HTTP 上报 /regJiang，并 800ms 后自启 MainActivity",
      "trigger_event": "onServiceConnected()（用户开启无障碍服务的瞬间）",
      "ui_carrier": "原生Activity（NEW_TASK|CLEAR_TASK 强制拉起）+ 悬浮窗Overlay",
      "shown_text_verbatim": "无固定文案；同时 enable.html 通过 localStorage.enableStream=\"true\" 把教学区切换为「Aguarde...」等待页",
      "shown_text_zh": "获权后 800ms 应用强制回到前台，引导页变为「请稍候…」转圈等待页，衔接后续屏幕共享授权流程",
      "user_action_requested": "无需操作，应用自动回前台并进入下一步（requestScreen/MediaProjection）",
      "code_anchor": "com.fenixeye.rvl.InitialService#onServiceConnected；com.fenixeye.rvl.InitialService#OooO0O0；com.fenxieye.rvl.o2#run（case 9）；assets/enable.html#L104-L165"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "j7 全屏悬浮窗（WindowManager type=2032，黑色 alpha=0.97 + 居中 TextView + 可选 ImageView）",
      "trigger_event": "InitialService 初始化时 new j7(...) 并 post 显示；文本内容由配置字段 OooO0oO 提供，图片由 OooO0oo 提供",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "运行时由配置下发的 TextView 文本（静态无固定字符串，setText(str2)）",
      "shown_text_zh": "在系统设置/屏幕共享等页面上覆盖几乎不透明的全屏黑色遮罩并居中显示引导文字与配图，遮挡真实页面内容",
      "user_action_requested": "按遮罩上的文字继续点击下层系统控件",
      "code_anchor": "com.fenxieye.rvl.h7#run；com.fenixeye.rvl.InitialService#OooO0O0"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "o2 case 8：再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS, flags 0x14000000)；OooOO0() 节点扫描并 performGlobalAction(1/2)",
      "trigger_event": "无障碍事件回调 / 定时任务链（Handler.postDelayed 60~300ms 连续调度）触发",
      "ui_carrier": "系统无障碍页 + 无障碍节点自动操作",
      "shown_text_verbatim": "匹配文本：Force stop / Force stop? / Forçar parada / Reset options / Desativar ? / Desativar a função ? / TalkBack / Acessibilidade / Restaurar / Verificar atividade em segundo plano",
      "shown_text_zh": "监听并自动点击系统「强制停止/停用/重置」等确认项，配合 BACK/HOME 全局动作，阻止用户停用或卸载；同时反复把用户拉回无障碍设置页",
      "user_action_requested": "无（应用主动打断用户的撤权/卸载操作）",
      "code_anchor": "com.fenxieye.rvl.o2#run；com.fenixeye.rvl.InitialService#OooOO0"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 冷启动即加载的本地 WebView 页面 assets/enable.html（section-accessibility）：标题、3 步操作指引、三星/小米/摩托罗拉分机型路径、隐私承诺、按钮「Abrir configurações de acessibilidade」、免责句「Você pode desativar essa permissão quando quiser」",
    "系统无障碍服务列表/详情：android:label 与 android:description 均为空字符串（空白条目，无任何文字）",
    "assets/enable.html 隐藏的 section-streaming：获权后（localStorage.enableStream=true）替换为「Aguarde...」+ 旋转动画",
    "跳转系统设置后：j7 全屏悬浮窗（type=2032，黑色 alpha=0.97）叠加的居中 TextView 引导文案与配图，覆盖系统页面",
    "服务运行期节点匹配字符串（硬编码于 com.fenixeye.rvl.InitialService#OooOO0 / #OooO0o0）：Force stop、Desativar、TalkBack、Acessibilidade 等，用于自动点掉系统停用/卸载确认",
    "字符串资源残留：res/values/strings.xml 中 connection=200.9.154.125、url_website=meu.inss.gov.br（未在引导页展示，属业务伪装线索）"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "Ativar Acessibilidade",
      "text_zh": "开启无障碍",
      "source_location": "assets/enable.html#L40-L42",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Precisamos dessa permissão para que o aplicativo funcione corretamente.",
      "text_zh": "我们需要此权限，应用才能正常运行。",
      "source_location": "assets/enable.html#L44-L46",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "pt",
      "text_verbatim": "1. Abra Acessibilidade  2. Toque em Serviços instalados ou Serviços  3. Selecione Revolution e ative",
      "text_zh": "1. 打开「无障碍」；2. 点击「已安装的服务」或「服务」；3. 选择「Revolution」并启用",
      "source_location": "assets/enable.html#L48-L63",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "📱 Samsung (One UI) Acessibilidade → Serviços instalados → Revolution；📱 Xiaomi (MIUI) Acessibilidade → Apps baixados → Revolution；📱 Motorola Acessibilidade → Serviços → Revolution",
      "text_zh": "三星(One UI)：无障碍 → 已安装的服务 → Revolution；小米(MIUI)：无障碍 → 已下载的应用 → Revolution；摩托罗拉：无障碍 → 服务 → Revolution",
      "source_location": "assets/enable.html#L65-L80",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "⚠️ Essa permissão é usada apenas para habilitar recursos do aplicativo. Nenhuma informação pessoal é coletada.",
      "text_zh": "⚠️ 该权限仅用于启用应用的功能，不会收集任何个人信息。",
      "source_location": "assets/enable.html#L82-L85",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "pt",
      "text_verbatim": "Abrir configurações de acessibilidade",
      "text_zh": "打开无障碍设置",
      "source_location": "assets/enable.html#L87-L93",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Você pode desativar essa permissão quando quiser.",
      "text_zh": "你可以随时关闭此权限。",
      "source_location": "assets/enable.html#L95-L97",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "pt",
      "text_verbatim": "Aguarde...",
      "text_zh": "请稍候…",
      "source_location": "assets/enable.html#L104-L114",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "pt",
      "text_verbatim": "Force stop / Forçar parada / Desativar ? / Desativar a função ? / Reset options / Restaurar / TalkBack / Acessibilidade",
      "text_zh": "强制停止 / 停用？ / 停用该功能？ / 重置选项 / 恢复 / TalkBack / 无障碍",
      "source_location": "com.fenixeye.rvl.InitialService#OooOO0（硬编码字符串比较）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "pt",
      "text_verbatim": "iniciar gravação / compartilhar tela / tela inteira / iniciar transmissão / ao vivo",
      "text_zh": "开始录制 / 共享屏幕 / 整屏 / 开始投屏 / 直播",
      "source_location": "com.fenixeye.rvl.InitialService#OooO 与 #OooOOo（硬编码字符串比较）",
      "rhetorical_frame": "教唆忽视警告"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "MainActivity.onResume 为空实现，不在此处重跳；但服务侧 o2.run() 的 case 8 会再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS)（flags 0x14000000 = NEW_TASK|CLEAR_TASK）把用户拉回无障碍设置；同时 OooOO0()/OooO0o0() 通过无障碍节点扫描 Desativar/Force stop/TalkBack 等文本并 performGlobalAction(1=BACK)/performGlobalAction(2=HOME)，在用户尝试停用/卸载时自动点掉确认或直接退回，形成撤权阻断循环",
    "overlay_or_fake_settings": "无高仿系统设置页；但有全屏悬浮窗遮罩：j7 通过 WindowManager 添加 type=2032、MATCH_PARENT 布局、纯黑 #000000 alpha=0.97 的 LinearLayout，居中显示配置下发的 TextView 文案与可选图片，覆盖在系统页/目标 App 之上用于压屏引导",
    "restricted_settings_13plus_coaching": "无。未使用 ACTION_APPLICATION_DETAILS_SETTINGS，也未教用户进入应用详情右上角菜单开启「允许受限设置」，无 Session 安装器绕过",
    "post_grant_anti_removal": "有。获权后 onServiceConnected 立即初始化并 800ms 自启回前台；onAccessibilityEvent 持续扫描系统停用/强制停止/卸载确认文本并自动点击，配合 performGlobalAction(BACK/HOME) 阻止撤权；另通过 TCPForegroundService 前台服务与 BOOT_COMPLETED 自启维持存活",
    "benign_graceful_degradation": "无。应用未提供任何替代路径（无手动模式/仅观看模式），无障碍权限是后续屏幕共享与远程操控链的硬依赖；HTML 中「随时可关闭该权限」的表述与代码中的反撤权行为直接矛盾"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两个最佳拉起瞬间：(1) 冷启动 MainActivity 首次加载 file:///android_asset/enable.html 的 WebView 页面（约启动后 1~2s，页面出现「Ativar Acessibilidade」标题即抓）；(2) 监测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的跳转瞬间（来自 WebView JS 桥 openAccessibility 或服务侧 o2 case 8），跳转后立即抓系统无障碍页与随后叠加的全屏黑遮罩",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导教学页（本地 HTML WebView）",
        "page_identifier": "包名 com.fenixeye.rvl 的 MainActivity，全屏 WebView 渲染葡语卡片「Ativar Acessibilidade」+ ♿ 图标 + 蓝色按钮「Abrir configurações de acessibilidade」",
        "why_most_useful": "这是唯一承载诱导文案与「Revolution」服务名的位置，能直接证明引导意图、分机型教学与隐私承诺话术；且与系统列表中的空白名称形成身份矛盾，是判定诱导+身份混淆的决定性页面",
        "observable_utg_signals": ["标题文本 Ativar Acessibilidade 与 ♿ 图标", "三步操作指引中含品牌名 Revolution（与系统服务 label 空白不符）", "隐私承诺文案 Nenhuma informação pessoal é coletada", "按钮文本 Abrir configurações de acessibilidade 且页面无取消/跳过控件"]
      },
      {
        "page_role": "系统无障碍服务列表项（空白条目）",
        "page_identifier": "设置 → 无障碍 → 已安装的服务中，来自 com.fenixeye.rvl 的条目名称为空、说明为空",
        "why_most_useful": "捕获该空白条目可与 HTML 宣称的 Revolution 形成直接对照，证明应用刻意隐藏无障碍服务真实名称，规避用户识别与审核",
        "observable_utg_signals": ["服务条目 label 为空字符串", "description 为空字符串", "条目对应包名 com.fenixeye.rvl"]
      },
      {
        "page_role": "跳转设置后叠加的全屏黑遮罩引导页",
        "page_identifier": "系统页面之上覆盖 alpha≈0.97 全屏黑色悬浮层，居中白色 18sp 文本（配置下发）及可选图片",
        "why_most_useful": "证明应用在系统页上压屏引导，属叠层遮蔽行为，可区分单纯跳转与主动遮挡用户判断",
        "observable_utg_signals": ["存在 type=2032 应用悬浮窗覆盖层", "覆盖层文本与系统原页面文本并存（下层被遮挡）", "覆盖层背景近全黑、居中单段文本"]
      },
      {
        "page_role": "获权后 800ms 自动回前台页面",
        "page_identifier": "无障碍开关打开后约 0.8s，应用界面以 NEW_TASK|CLEAR_TASK 重新出现在前台，页面变为「Aguarde...」+ 旋转圈",
        "why_most_useful": "证明权限获取与后续屏幕共享/远程操控链的即时衔接，是「诱导目的」与「获权即行动」的关键时序证据",
        "observable_utg_signals": ["无障碍开关置 ON 后 <1s 前台应用切回 com.fenixeye.rvl", "页面文本由教学区切换为 Aguarde... 与转圈动画", "随后出现 MediaProjection 系统屏幕共享授权对话框并被自动点击"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。引导文案为真实可提取文本（WebView DOM/系统 label），不需要 OCR。需注意两点：其一，悬浮窗遮罩的文本与图片由服务端配置下发，静态无固定字符串，UTG 需在运行期读取覆盖层文本；其二，系统无障碍列表条目名称/描述为空，若检测仅按「服务名是否可疑」匹配会漏检，应以「空白 label + 具备 typeAllMask/canRetrieveWindowContent/canPerformGestures 的服务」作为判别特征。此外 MainActivity 在模拟器/Root/Frida/代理环境下直接 finish()，在受控 UTG 设备（多为模拟器或 root 环境）上冷启动引导页可能不出现，此时应改用已植入的无障碍跳转或真实设备验证。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.fenixeye.rvl.MainActivity#onCreate",
    "com.fenixeye.rvl.MainActivity#openAccessibility",
    "assets/enable.html#L31-L99",
    "com.fenixeye.rvl.InitialService#OooO0O0",
    "com.fenxieye.rvl.o2#run",
    "com.fenxieye.rvl.h7#run"
  ]
}
```

> 说明：受本轮 14 次工具调用硬约束，未再追加 `record_risk` 台账写入（风险事实与证据链已完整列于上文与 JSON）。核心风险命题为：以空白无障碍服务名 + 本地 HTML「Revolution」话术诱导开启无障碍，并以全屏遮罩、自动点击系统确认、BACK/HOME 阻断撤权，获权后立即转入屏幕共享与远程操控。

</details>

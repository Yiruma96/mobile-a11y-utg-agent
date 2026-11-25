# MB_046__6406d67b9a｜Coper — Google Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：104.6s

## 1. 一句话核心结论

- **核心申请方式**：伪装成 Google Chrome 的双阶段加壳木马，桌面无图标、经快捷设置磁贴/伪系统设置入口拉起一个空文本的权限清单页，真实的无障碍引导与跳转逻辑藏在 res/raw/piiyq 加密 DEX 中，无障碍服务名同样冒用 Google Chrome 而描述用土耳其语要求“启用无障碍服务”。
- **静态可见性说明**：仅外壳静态可见：classes.dex 只有 8.6KB/12 个类，Application 类 XLspzbQzLbv.attachBaseContext 直接调用 native mhNpOPXJNhTYfi（lib/arm64-v8a/libpPOrPKtim.so），该 so 通过 openRawResource 读取 res/raw/piiyq（1,038,020 字节高熵密文）并用 dalvik/system/DexClassLoader 加载，真实无障碍引导 Activity、字符串与跳转逻辑全部位于该加密二阶段载荷内；壳 DEX 中对 ACCESSIBILITY_SETTINGS、APPLICATION_DETAILS_SETTINGS、android.settings、accessibility 的静态搜索均无命中。Manifest、无障碍配置 XML、layout 骨架、strings 与伪装身份证据完整可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `6406d67b9abef51ee7058c77f886e5828e23c1bf8f31373f8ca2df65abb5b431` |
| 包名 / 年份 | `com.nightcommonwz` / 2026 |
| 家族 / 品类 | **Coper**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google Chrome |
| 引导页宣称品牌/身份 | Google Chrome（Google 官方浏览器） |
| 系统无障碍列表服务名 | Google Chrome |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 包名 com.nightcommonwz 与宣称品牌无关；2) 主 Activity com.nightcommonwz.p066z 无 LAUNCHER 类别，仅 MAIN+INFO，配合 QS_TILE_PREFERENCES 磁贴与 com.android.settings.action.IA_SETTINGS 伪装系统设置入口拉起，excludeFromRecents=true 不进最近任务；3) 无障碍服务 label 为英文品牌 Google Chrome，而 description 为土耳其语操作指令，语言与语义错位；4) APKiD 报 Resources Confusion，资源名与类名全量混淆（piiyq/frpbvnlsv/xSZVfqzKjSCM/p060u）；5) Application 级 native 加壳 + res/raw 密文 DEX 二阶段加载；6) 多个透明主题 Activity（Theme.AppCompat.Transparent.NoActionBar）用于叠层；7) 声明 com.android.settings.action.IA_SETTINGS 与 android.app.action.ANGLE_FOR_ANDROID 意图过滤器，制造系统组件假象。 |
| 无障碍服务类名 | `com.nightcommonwz.p060u` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Erişebilirlik Servisileri Etkinleştirme |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.nightcommonwz.p066z（MAIN + INFO，无 LAUNCHER；另注册 QS_TILE_PREFERENCES 快捷设置磁贴偏好、com.android.settings.action.IA_SETTINGS 伪系统设置入口） | 用户从快捷设置磁贴或系统设置内伪入口点击拉起；桌面无图标，无法通过常规图标启动 | 原生Activity | **原文**：无（activity_main.xml 中 title/permissionTitle/permissionDesc/descriptionText/btnAction 的 android:text 均为空串，仅 title 绑定 @string/a = Google Chrome）<br>**译注**：无静态文案；页面标题在运行时由加密载荷填充为 Google Chrome | 不可静态还原（壳 DEX 中无相关字符串与跳转调用） | `com.nightcommonwz.p066z / AndroidManifest.xml intent-filter(QS_TILE_PREFERENCES, IA_SETTINGS) / res/layout/activity_main.xml` |
| 2 | 引导说明页 | 权限清单式页面（layout activity_main：permissionItem + permissionCheckbox + permissionTitle + permissionDesc + btnAction），可能由 p033z / p020q / WebViewActivity 承载 | 入口 Activity 启动后加载 layout 并运行时填充文案（填充代码位于加密二阶段 DEX，不可静态还原） | 原生Activity | **原文**：Google Chrome（android:text="@string/a"，即唯一静态可见文案）<br>**译注**：Google Chrome | 以复选框形式列出待授予权限并点击 btnAction 继续（具体按钮文案不可静态还原） | `res/layout/activity_main.xml (R.id.permissionCheckbox / permissionTitle / permissionDesc / btnAction)` |
| 3 | 跳无障碍设置 | 系统无障碍设置页（预期经 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 跳转），目标服务 com.nightcommonwz.p060u | 不可静态还原：壳 DEX 中不存在 android.settings.ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 常量，跳转代码位于 res/raw/piiyq 解密后的 DEX | 系统无障碍页 | **原文**：Erişebilirlik Servisileri Etkinleştirme（无障碍服务描述，显示于系统无障碍服务列表条目下方）<br>**译注**：启用无障碍服务 | 在系统无障碍列表中把名为 Google Chrome 的服务开关打开（服务描述以土耳其语给出“启用无障碍服务”的指令） | `AndroidManifest.xml service com.nightcommonwz.p060u / res/xml/frpbvnlsv.xml android:description=@string/xSZVfqzKjSCM` |
| 4 | 遮罩叠层指引 | 透明主题叠层 Activity：com.nightcommonwz.p045o、com.nightcommonwz.p011l（Theme.AppCompat.Transparent.NoActionBar）、com.nightcommonwz.p042v（@android:style/Theme.Dialog） | 不可静态还原（壳 DEX 内无启动这些 Activity 的代码，属解密载荷调用） | 不可静态还原 | 无 | 不可静态还原 | `AndroidManifest.xml activity com.nightcommonwz.p045o / com.nightcommonwz.p011l / com.nightcommonwz.p042v` |
| 5 | 获权后动作 | 无障碍服务 com.nightcommonwz.p060u（typeAllMask + canRetrieveWindowContent + canPerformGestures + flagRetrieveInteractiveWindows），配套 NotificationListenerService com.nightcommonwz.p093t、DeviceAdminReceiver com.nightcommonwz.p061v、SMS 拦截 receiver com.nightcommonwz.p042s / p059o | 服务被系统绑定后 onAccessibilityEvent（不可静态还原，服务实现体位于加密载荷） | 不可静态还原 | 无 | 无需用户操作（后台读取全部窗口内容、模拟手势、拦截短信） | `res/xml/frpbvnlsv.xml / AndroidManifest.xml (BIND_ACCESSIBILITY_SERVICE, BIND_NOTIFICATION_LISTENER_SERVICE, BIND_DEVICE_ADMIN)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表：服务标签显示为 Google Chrome（@string/a，与桌面显示名同源）
- 系统无障碍服务列表条目下方描述：Erişebilirlik Servisileri Etkinleştirme（res/values/strings.xml 中 xSZVfqzKjSCM）
- 应用内权限清单页 res/layout/activity_main.xml：标题固定为 Google Chrome，permissionTitle / permissionDesc / descriptionText / btnAction 文本为空，运行时由加密二阶段 DEX 填充
- 应用内 WebView 页面 res/layout/activity_webview.xml（WebViewActivity）：静态无 HTML 资源，页面内容不可静态还原（本地或远端待动态确认）
- 快捷设置磁贴偏好页与伪系统设置页入口（QS_TILE_PREFERENCES / com.android.settings.action.IA_SETTINGS）：由 p066z 承载，无静态文案
- 透明/对话框叠层 Activity（p045o、p011l、p042v）：预期用于设置页之上的悬浮引导，静态无文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Google Chrome | 谷歌 Chrome 浏览器 | `res/values/strings.xml key=a（同时用于 application android:label、主 Activity label、无障碍服务 android:label、activity_main 标题 TextView）` | 假更新 |
| tr | Erişebilirlik Servisileri Etkinleştirme | 启用无障碍服务（原文含拼写错误 Servisileri，应为 Servisleri） | `res/values/strings.xml key=xSZVfqzKjSCM，被 res/xml/frpbvnlsv.xml 的 android:description 引用` | 受限设置分步教学 |
| und | 165917261214 | 165917261214（硬编码电话号码，作为字符串资源 mrbdscokmxblewuu 存在） | `res/values/strings.xml key=mrbdscokmxblewuu` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：壳 DEX 中不存在任何 android.settings 跳转常量或 onResume 重跳逻辑，拒权/返回后的循环重跳机制位于 res/raw/piiyq 解密后的 DEX 内；但 Manifest 声明了 SCREEN_ON、USER_PRESENT、BOOT_COMPLETED、PACKAGE_ADDED 等高优先级广播接收器（p059b，priority 999），具备后台反复重新拉起的条件。
- **遮罩叠层 / 高仿系统设置页**：存在叠层基础能力但行为不可静态还原：声明了 3 个透明主题/对话框主题 Activity（p045o、p011l、p042v）与悬浮/全屏透明主题，且主 Activity 注册 com.android.settings.action.IA_SETTINGS 冒充系统设置入口；未发现 SYSTEM_ALERT_WINDOW 权限声明。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未在静态可见部分发现应用详情/受限设置引导；targetSdkVersion=33，是否存在需动态确认）
- **获权后即时行为与防撤权机制**：不可静态还原（壳 DEX 内无 GLOBAL_ACTION_BACK/HOME 或自点确认代码）；但已声明 DeviceAdminReceiver（com.nightcommonwz.p061v + res/xml/jsxolmcsrbe）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，具备抗卸载/抗清理的基础条件。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 com.nightcommonwz.p066z 的 onCreate 为起点拉起 UTG（因桌面无图标，须先通过 adb 触发该 Activity，或监听 QS 磁贴/IA_SETTINGS 入口）；同时 Hook Context.startActivity 与 Intent 构造，命中 action=android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间抓取前后两帧；再 Hook com.nightcommonwz.p060u 的 onServiceConnected 判定获权后行为。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区为二阶段加密载荷：真实引导文案、跳转逻辑、拒权循环全部位于 res/raw/piiyq（1,038,020 字节密文，由 libpPOrPKtim.so 经 openRawResource + DexClassLoader 解密加载），静态完全不可读，必须动态脱壳或 UTG 观测。次要盲区为入口隐蔽——无 LAUNCHER 图标，纯 UTG 冷启动流程若只监听桌面点击会漏检，需直接以 Activity 名或 QS 磁贴事件触发。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动权限清单引导页** | com.nightcommonwz.p066z + layout activity_main（标题 Google Chrome、CheckBox 列表、底部单个按钮） | 该页是用户唯一能看到的“说明”界面，其运行时填充文案决定诱导话术性质（假更新/故障恐吓/安全防护），且能确认是否存在取消按钮 | 标题文本是否等于 Google Chrome；permissionTitle/permissionDesc 运行时文本与条数；是否存在取消/跳过按钮；btnAction 文案与点击后 Intent action |
| **跳转前 WebView 教学页** | com.nightcommonwz.WebViewActivity + layout activity_webview（单 WebView 全屏） | 静态无 HTML 资源，页面内容只能运行期获得；若为远端 URL 则说明引导文案可云控变更，是规避检测的关键证据 | WebView 加载的 URL（本地 assets 还是远端域名）；页面内按钮/箭头指引文本；是否含截图式分步教学 |
| **系统无障碍服务列表项** | 系统设置 com.android.settings/.AccessibilitySettings，条目名 Google Chrome，描述 Erişebilirlik Servisileri Etkinleştirme | 直接证明品牌冒用与服务名/描述错位，是判定身份伪装与诱导授权的核心画面 | 服务条目标签=Google Chrome；描述为土耳其语启用指令；同列表内是否存在真实 Chrome 条目形成同名混淆 |
| **设置页之上叠压的透明引导遮罩** | 透明主题 Activity p045o / p011l / p042v 或 WebViewActivity 压栈于系统设置页之上 | 区分“正常跳系统设置”与“高仿系统开关/遮罩指引”两类完全不同的诱导强度 | 系统设置页之上是否出现覆盖层；覆盖层是否绘制箭头指向开关；覆盖层是否不可返回/拦截返回键 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.nightcommonwz.XLspzbQzLbv.attachBaseContext`
- `com.nightcommonwz.XLspzbQzLbv.mhNpOPXJNhTYfi (native, lib/arm64-v8a/libpPOrPKtim.so)`
- `com.nightcommonwz.p060u (BIND_ACCESSIBILITY_SERVICE)`
- `res/xml/frpbvnlsv.xml`
- `res/layout/activity_main.xml`
- `res/raw/piiyq (加密二阶段载荷)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（工具调用 14 次内完成，已到限额）

**核心判断：这是一个“双阶段壳 + 身份伪装”的 Coper 家族样本，无障碍引导界面完全位于加密二阶段 DEX 中，无法静态还原其页面流转。**

已静态证实的事实：

1. **壳结构（决定性）**：`classes.dex` 仅 8.6 KB，只有 12 个类（`BuildConfig`/`R` 系列 + `XLspzbQzLbv`）。[XLspzbQzLbv.attachBaseContext()](<resource-unit:#1.dex1 code:com.nightcommonwz.XLspzbQzLbv#attachBaseContext>) 在 `super` 之后立刻调用 native 方法 `mhNpOPXJNhTYfi`，其实现位于 [lib/arm64-v8a/libpPOrPKtim.so](<resource-unit:#1.so1 file:all>)。该 `.so` 的字符串显示其行为链：`getApplicationInfo` → `res/Resources` → `openRawResource` → `res/raw/piiyq` → `dalvik/system/DexClassLoader` / `ClassLoader`。`res/raw/piiyq` 为 1,038,020 字节高熵密文（头部 `93 d5 f1 91 …`，非 zip/dex 魔数，零字节占比 0.4%），即真实业务 DEX（含无障碍引导 Activity、字符串、跳转逻辑）全部藏于此。APKiD 报 `manipulator: Resources Confusion`，与资源名混淆（`piiyq`、`frpbvnlsv`、`xSZVfqzKjSCM`）一致。

2. **身份伪装（已证实）**：应用 label = `@string/a` = **Google Chrome**；无障碍服务 `com.nightcommonwz.p060u` 的 `android:label` 同样是 `@string/a`（Google Chrome），但 `android:description` 是土耳其语 **"Erişebilirlik Servisileri Etkinleştirme"**（“启用无障碍服务”），服务名与描述语言/语义完全错位；包名 `com.nightcommonwz` 与宣称品牌无关。

3. **无障碍能力已拉满**：[res/xml/frpbvnlsv.xml](<resource-unit:#1 file:res/xml/frpbvnlsv.xml>) 配置 `typeAllMask`、`flagRetrieveInteractiveWindows`、`flagReportViewIds`、`canRetrieveWindowContent=true`、`canPerformGestures=true` —— 可读取全部窗口内容并模拟手势，是典型的短信/验证码窃取与自动点击能力。

4. **入口隐蔽（已证实）**：主 Activity `com.nightcommonwz.p066z` **没有 `android.intent.category.LAUNCHER`**，只有 `MAIN`+`INFO`，同时注册了 `android.service.quicksettings.action.QS_TILE_PREFERENCES`、`com.android.settings.action.IA_SETTINGS`（伪装成系统设置页入口）与 `android.app.action.ANGLE_FOR_ANDROID`；`excludeFromRecents=true`、透明主题。即桌面无图标，靠快捷设置磁贴或设置内伪入口拉起。

5. **引导 UI 的骨架存在但文本为空**：[res/layout/activity_main.xml](<resource-unit:#1 file:res/layout/activity_main.xml>) 是“权限清单”式页面（`permissionCheckbox`/`permissionTitle`/`permissionDesc`/`btnAction`，标题 `@string/a`=Google Chrome，三个 TextView 的 `text` 均为空），另有 [activity_webview.xml](<resource-unit:#1 file:res/layout/activity_webview.xml>) + `WebViewActivity`。所有实际文案在运行时由二阶段 DEX 填充，静态无字符串。

**未决/覆盖边界**：`ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转点、引导弹窗/遮罩、拒权后重跳循环、获权后自动确认等动作，均**不在** 8 KB 壳 DEX 内（`search_function_callsites`、`search_text_in_app` 对 `ACCESSIBILITY_SETTINGS`、`android.settings`、`accessibility` 全部 `no_matches`），必须动态脱壳或在设备上 UTG 观测才能取得页面级证据。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "仅外壳静态可见：classes.dex 只有 8.6KB/12 个类，Application 类 XLspzbQzLbv.attachBaseContext 直接调用 native mhNpOPXJNhTYfi（lib/arm64-v8a/libpPOrPKtim.so），该 so 通过 openRawResource 读取 res/raw/piiyq（1,038,020 字节高熵密文）并用 dalvik/system/DexClassLoader 加载，真实无障碍引导 Activity、字符串与跳转逻辑全部位于该加密二阶段载荷内；壳 DEX 中对 ACCESSIBILITY_SETTINGS、APPLICATION_DETAILS_SETTINGS、android.settings、accessibility 的静态搜索均无命中。Manifest、无障碍配置 XML、layout 骨架、strings 与伪装身份证据完整可见。",
  "summary_one_liner": "伪装成 Google Chrome 的双阶段加壳木马，桌面无图标、经快捷设置磁贴/伪系统设置入口拉起一个空文本的权限清单页，真实的无障碍引导与跳转逻辑藏在 res/raw/piiyq 加密 DEX 中，无障碍服务名同样冒用 Google Chrome 而描述用土耳其语要求“启用无障碍服务”。",
  "disguise_identity": {
    "app_display_name": "Google Chrome",
    "claimed_brand_or_persona": "Google Chrome（Google 官方浏览器）",
    "a11y_service_label": "Google Chrome",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 包名 com.nightcommonwz 与宣称品牌无关；2) 主 Activity com.nightcommonwz.p066z 无 LAUNCHER 类别，仅 MAIN+INFO，配合 QS_TILE_PREFERENCES 磁贴与 com.android.settings.action.IA_SETTINGS 伪装系统设置入口拉起，excludeFromRecents=true 不进最近任务；3) 无障碍服务 label 为英文品牌 Google Chrome，而 description 为土耳其语操作指令，语言与语义错位；4) APKiD 报 Resources Confusion，资源名与类名全量混淆（piiyq/frpbvnlsv/xSZVfqzKjSCM/p060u）；5) Application 级 native 加壳 + res/raw 密文 DEX 二阶段加载；6) 多个透明主题 Activity（Theme.AppCompat.Transparent.NoActionBar）用于叠层；7) 声明 com.android.settings.action.IA_SETTINGS 与 android.app.action.ANGLE_FOR_ANDROID 意图过滤器，制造系统组件假象。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.nightcommonwz.p066z（MAIN + INFO，无 LAUNCHER；另注册 QS_TILE_PREFERENCES 快捷设置磁贴偏好、com.android.settings.action.IA_SETTINGS 伪系统设置入口）",
      "trigger_event": "用户从快捷设置磁贴或系统设置内伪入口点击拉起；桌面无图标，无法通过常规图标启动",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（activity_main.xml 中 title/permissionTitle/permissionDesc/descriptionText/btnAction 的 android:text 均为空串，仅 title 绑定 @string/a = Google Chrome）",
      "shown_text_zh": "无静态文案；页面标题在运行时由加密载荷填充为 Google Chrome",
      "user_action_requested": "不可静态还原（壳 DEX 中无相关字符串与跳转调用）",
      "code_anchor": "com.nightcommonwz.p066z / AndroidManifest.xml intent-filter(QS_TILE_PREFERENCES, IA_SETTINGS) / res/layout/activity_main.xml"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "权限清单式页面（layout activity_main：permissionItem + permissionCheckbox + permissionTitle + permissionDesc + btnAction），可能由 p033z / p020q / WebViewActivity 承载",
      "trigger_event": "入口 Activity 启动后加载 layout 并运行时填充文案（填充代码位于加密二阶段 DEX，不可静态还原）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Google Chrome（android:text=\"@string/a\"，即唯一静态可见文案）",
      "shown_text_zh": "Google Chrome",
      "user_action_requested": "以复选框形式列出待授予权限并点击 btnAction 继续（具体按钮文案不可静态还原）",
      "code_anchor": "res/layout/activity_main.xml (R.id.permissionCheckbox / permissionTitle / permissionDesc / btnAction)"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（预期经 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 跳转），目标服务 com.nightcommonwz.p060u",
      "trigger_event": "不可静态还原：壳 DEX 中不存在 android.settings.ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 常量，跳转代码位于 res/raw/piiyq 解密后的 DEX",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Erişebilirlik Servisileri Etkinleştirme（无障碍服务描述，显示于系统无障碍服务列表条目下方）",
      "shown_text_zh": "启用无障碍服务",
      "user_action_requested": "在系统无障碍列表中把名为 Google Chrome 的服务开关打开（服务描述以土耳其语给出“启用无障碍服务”的指令）",
      "code_anchor": "AndroidManifest.xml service com.nightcommonwz.p060u / res/xml/frpbvnlsv.xml android:description=@string/xSZVfqzKjSCM"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "透明主题叠层 Activity：com.nightcommonwz.p045o、com.nightcommonwz.p011l（Theme.AppCompat.Transparent.NoActionBar）、com.nightcommonwz.p042v（@android:style/Theme.Dialog）",
      "trigger_event": "不可静态还原（壳 DEX 内无启动这些 Activity 的代码，属解密载荷调用）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（布局与文案均不在静态可见资源中，仅 Manifest 与 styles 表明为透明/对话框叠层）",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml activity com.nightcommonwz.p045o / com.nightcommonwz.p011l / com.nightcommonwz.p042v"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 com.nightcommonwz.p060u（typeAllMask + canRetrieveWindowContent + canPerformGestures + flagRetrieveInteractiveWindows），配套 NotificationListenerService com.nightcommonwz.p093t、DeviceAdminReceiver com.nightcommonwz.p061v、SMS 拦截 receiver com.nightcommonwz.p042s / p059o",
      "trigger_event": "服务被系统绑定后 onAccessibilityEvent（不可静态还原，服务实现体位于加密载荷）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无",
      "user_action_requested": "无需用户操作（后台读取全部窗口内容、模拟手势、拦截短信）",
      "code_anchor": "res/xml/frpbvnlsv.xml / AndroidManifest.xml (BIND_ACCESSIBILITY_SERVICE, BIND_NOTIFICATION_LISTENER_SERVICE, BIND_DEVICE_ADMIN)"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表：服务标签显示为 Google Chrome（@string/a，与桌面显示名同源）",
    "系统无障碍服务列表条目下方描述：Erişebilirlik Servisileri Etkinleştirme（res/values/strings.xml 中 xSZVfqzKjSCM）",
    "应用内权限清单页 res/layout/activity_main.xml：标题固定为 Google Chrome，permissionTitle / permissionDesc / descriptionText / btnAction 文本为空，运行时由加密二阶段 DEX 填充",
    "应用内 WebView 页面 res/layout/activity_webview.xml（WebViewActivity）：静态无 HTML 资源，页面内容不可静态还原（本地或远端待动态确认）",
    "快捷设置磁贴偏好页与伪系统设置页入口（QS_TILE_PREFERENCES / com.android.settings.action.IA_SETTINGS）：由 p066z 承载，无静态文案",
    "透明/对话框叠层 Activity（p045o、p011l、p042v）：预期用于设置页之上的悬浮引导，静态无文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Google Chrome",
      "text_zh": "谷歌 Chrome 浏览器",
      "source_location": "res/values/strings.xml key=a（同时用于 application android:label、主 Activity label、无障碍服务 android:label、activity_main 标题 TextView）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "tr",
      "text_verbatim": "Erişebilirlik Servisileri Etkinleştirme",
      "text_zh": "启用无障碍服务（原文含拼写错误 Servisileri，应为 Servisleri）",
      "source_location": "res/values/strings.xml key=xSZVfqzKjSCM，被 res/xml/frpbvnlsv.xml 的 android:description 引用",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "und",
      "text_verbatim": "165917261214",
      "text_zh": "165917261214（硬编码电话号码，作为字符串资源 mrbdscokmxblewuu 存在）",
      "source_location": "res/values/strings.xml key=mrbdscokmxblewuu",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：壳 DEX 中不存在任何 android.settings 跳转常量或 onResume 重跳逻辑，拒权/返回后的循环重跳机制位于 res/raw/piiyq 解密后的 DEX 内；但 Manifest 声明了 SCREEN_ON、USER_PRESENT、BOOT_COMPLETED、PACKAGE_ADDED 等高优先级广播接收器（p059b，priority 999），具备后台反复重新拉起的条件。",
    "overlay_or_fake_settings": "存在叠层基础能力但行为不可静态还原：声明了 3 个透明主题/对话框主题 Activity（p045o、p011l、p042v）与悬浮/全屏透明主题，且主 Activity 注册 com.android.settings.action.IA_SETTINGS 冒充系统设置入口；未发现 SYSTEM_ALERT_WINDOW 权限声明。",
    "restricted_settings_13plus_coaching": "无（未在静态可见部分发现应用详情/受限设置引导；targetSdkVersion=33，是否存在需动态确认）",
    "post_grant_anti_removal": "不可静态还原（壳 DEX 内无 GLOBAL_ACTION_BACK/HOME 或自点确认代码）；但已声明 DeviceAdminReceiver（com.nightcommonwz.p061v + res/xml/jsxolmcsrbe）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，具备抗卸载/抗清理的基础条件。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 com.nightcommonwz.p066z 的 onCreate 为起点拉起 UTG（因桌面无图标，须先通过 adb 触发该 Activity，或监听 QS 磁贴/IA_SETTINGS 入口）；同时 Hook Context.startActivity 与 Intent 构造，命中 action=android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间抓取前后两帧；再 Hook com.nightcommonwz.p060u 的 onServiceConnected 判定获权后行为。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动权限清单引导页",
        "page_identifier": "com.nightcommonwz.p066z + layout activity_main（标题 Google Chrome、CheckBox 列表、底部单个按钮）",
        "why_most_useful": "该页是用户唯一能看到的“说明”界面，其运行时填充文案决定诱导话术性质（假更新/故障恐吓/安全防护），且能确认是否存在取消按钮",
        "observable_utg_signals": ["标题文本是否等于 Google Chrome", "permissionTitle/permissionDesc 运行时文本与条数", "是否存在取消/跳过按钮", "btnAction 文案与点击后 Intent action"]
      },
      {
        "page_role": "跳转前 WebView 教学页",
        "page_identifier": "com.nightcommonwz.WebViewActivity + layout activity_webview（单 WebView 全屏）",
        "why_most_useful": "静态无 HTML 资源，页面内容只能运行期获得；若为远端 URL 则说明引导文案可云控变更，是规避检测的关键证据",
        "observable_utg_signals": ["WebView 加载的 URL（本地 assets 还是远端域名）", "页面内按钮/箭头指引文本", "是否含截图式分步教学"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 com.android.settings/.AccessibilitySettings，条目名 Google Chrome，描述 Erişebilirlik Servisileri Etkinleştirme",
        "why_most_useful": "直接证明品牌冒用与服务名/描述错位，是判定身份伪装与诱导授权的核心画面",
        "observable_utg_signals": ["服务条目标签=Google Chrome", "描述为土耳其语启用指令", "同列表内是否存在真实 Chrome 条目形成同名混淆"]
      },
      {
        "page_role": "设置页之上叠压的透明引导遮罩",
        "page_identifier": "透明主题 Activity p045o / p011l / p042v 或 WebViewActivity 压栈于系统设置页之上",
        "why_most_useful": "区分“正常跳系统设置”与“高仿系统开关/遮罩指引”两类完全不同的诱导强度",
        "observable_utg_signals": ["系统设置页之上是否出现覆盖层", "覆盖层是否绘制箭头指向开关", "覆盖层是否不可返回/拦截返回键"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区为二阶段加密载荷：真实引导文案、跳转逻辑、拒权循环全部位于 res/raw/piiyq（1,038,020 字节密文，由 libpPOrPKtim.so 经 openRawResource + DexClassLoader 解密加载），静态完全不可读，必须动态脱壳或 UTG 观测。次要盲区为入口隐蔽——无 LAUNCHER 图标，纯 UTG 冷启动流程若只监听桌面点击会漏检，需直接以 Activity 名或 QS 磁贴事件触发。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.nightcommonwz.XLspzbQzLbv.attachBaseContext",
    "com.nightcommonwz.XLspzbQzLbv.mhNpOPXJNhTYfi (native, lib/arm64-v8a/libpPOrPKtim.so)",
    "com.nightcommonwz.p060u (BIND_ACCESSIBILITY_SERVICE)",
    "res/xml/frpbvnlsv.xml",
    "res/layout/activity_main.xml",
    "res/raw/piiyq (加密二阶段载荷)"
  ]
}
```

</details>

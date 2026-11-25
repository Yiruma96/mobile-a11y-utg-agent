# MB_081__7a4238fc6f｜Ermac — Ermac-V2 Apk

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：169.3s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即跳系统无障碍设置，同时在设置页之上悬浮叠加高仿系统无障碍列表的本地 HTML 假页面（TalkBack/开关访问/Open Settings），用户返回或拒绝就 onActivityResult 立即回跳重来，形成无取消、无跳过的强制引导循环，获权后服务再自动点击 action_button 替用户确认。
- **静态可见性说明**：无障碍引导链的 Activity 跳转、ACTION_ACCESSIBILITY_SETTINGS 调用、悬浮窗叠加与回跳循环均在 classes.dex 中明文可见；假设置页 HTML 与全部引导文案以 Base64 硬编码在 DEX 字符串中，已静态解码核对完整 DOM 与 30+ 语言文案。仍有两处动态边界：一是 HTML 中标题为占位符 %Enable_Accessibility_Service%，可由远端配置替换；二是服务端配置字符串经 f0.a.c 自定义编码/加密，远端可下发更新版引导页或开关面板内容，未做动态验证。无加壳、无 VMP、无二阶段 Dex 载荷。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `7a4238fc6f5d3c7731c2eb33911298eaa36986040858af56e76628c5dc83e265` |
| 包名 / 年份 | `nusku.ermacv2.apk` / 2024 |
| 家族 / 品类 | **Ermac**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Ermac-V2 Apk |
| 引导页宣称品牌/身份 | 无品牌说明；运行期按本机已装应用动态启用 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram 同名图标入口；引导页伪装为 Android 系统“无障碍服务”设置界面 |
| 系统无障碍列表服务名 | Ermac-V2 Apk |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍服务在系统列表仅显示“Ermac-V2 Apk”且 Manifest 未声明 android:description，用户无法得知用途；2) 声明 10 个 android:enabled="false" 的 activity-alias（Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome/Instagram/TikTok/Telegram）全部 targetActivity 指向同一 nepesi，运行期由 PackageManager.setComponentEnabledSetting 按已装应用启用，实现图标与名称顶替；3) 类名/方法名全量随机化（pozetinawo、zafewo、hisuli、serezupifurizu 等），字符串经 Base64 + f0.a.c 自定义编解码；4) 应用 theme=Theme.Translucent.NoTitleBar、android:noHistory=true，引导 Activity 布局 gawago.xml 为 visibility=gone 高度 0，界面不可见；5) 用本地 HTML 复刻系统无障碍设置列表（含 TalkBack、Switch Access、OFF 开关、DOWNLOADED SERVICES 分组）作为假设置页；6) 未使用伪造 isAccessibilityTool 字段。 |
| 无障碍服务类名 | `com.cisojemopatude.yazi.nopofoyuwure.pozetinawo` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.jakedegivuwuwe.yewo.nepesi（LAUNCHER Activity，Theme.Translucent.NoTitleBar，布局 gawago.xml 全部 gone） | onCreate：读取 Settings.Secure 的 enabled_accessibility_services，判断本包无障碍服务是否已启用；未启用则 startActivity(hisuli, FLAG_ACTIVITY_REORDER_TO_FRONT)，异常时兜底 startActivity(zafewo)；随后 Handler.postDelayed 100ms 再入 | 原生Activity | **原文**：无（界面不可见，setContentView(@layout/gawago) 内容为 visibility=gone、height=0dip 的空 LinearLayout）<br>**译注**：无可见界面，仅作静默跳转与 SharedPreferences 初始化 | 无（用户无任何交互，被直接带离桌面） | `com.jakedegivuwuwe.yewo.nepesi.onCreate / res/layout/gawago.xml` |
| 2 | 业务功能触发 | com.cisojemopatude.yazi.hisuli（中继 Activity，taskAffinity=com.cisojemopatude.yazi.main，Translucent.NoTitleBar） | onCreate：初始化 idbot/initialization 到 SharedPreferences，注册 AlarmManager.setRepeating(10000ms) 指向 vuyoyava 广播，启动 kozoxirohizuge 前台服务，startActivity(zafewo, FLAG_ACTIVITY_REORDER_TO_FRONT\|CLEAR_TOP\|NEW_TASK\|SINGLE_TOP) 并 postDelayed 100ms；onBackPressed 直接调用 a(true) 重跳 | 原生Activity | 无 | 无；按返回键同样被重新拉起，无法退出 | `com.cisojemopatude.yazi.hisuli.a / com.cisojemopatude.yazi.hisuli.onBackPressed` |
| 3 | 跳无障碍设置 | com.cisojemopatude.yazi.catozotu.zafewo → 系统 android.settings.ACCESSIBILITY_SETTINGS 页面 | onCreate：若服务已启用则调用 b() 进入获权流程；否则（字段 d 为 false）执行 startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 12345)，随后若本地引导 HTML 文本长度大于 0 则 startActivity(serezupifurizu, FLAG_ACTIVITY_NEW_TASK\|FLAG_ACTIVITY_NO_ANIMATION\|FLAG_ACTIVITY_CLEAR_TOP) | 系统无障碍页 | **原文**：无（应用自身不渲染任何说明，直接落到系统“无障碍 / 已下载的服务”列表）<br>**译注**：系统无障碍设置页，应用只显示为列表中的“Ermac-V2 Apk”条目且无描述文字 | 要求用户在系统列表中手动找到并打开“Ermac-V2 Apk”开关；无任何应用内说明、无取消或跳过按钮 | `com.cisojemopatude.yazi.catozotu.zafewo.onCreate（"android.settings.ACCESSIBILITY_SETTINGS", requestCode 12345）` |
| 4 | 遮罩叠层指引 | com.cisojemopatude.yazi.catozotu.serezupifurizu（noHistory，Theme.ACL.Theme.Translucent.System）+ WindowManager 叠加 WebView | onCreate：Base64.decode(zafewo.a()) 还原 HTML，按 Locale 替换 <html lang> 与语言包；WindowManager.addView(WebView, LayoutParams(-1,-2,type=2038(TYPE_APPLICATION_OVERLAY 位),flags=262456,format=-3,gravity=80))；setWebViewClient；HTML 内 onclick="Android.onData();" 经 addJavascriptInterface(..., "Android") 回调原生 | 悬浮窗Overlay | **原文**：%Enable_Accessibility_Service% / Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / Open Settings / OFF（zh 语言包：無障礙服務 / 下載的服務 / 開關訪問 / 頂嘴 / Open Settings / 關）<br>**译注**：“启用无障碍服务”标题 + 仿系统无障碍页的“已下载的服务”分组，内含 TalkBack、开关访问条目与 OFF 开关，底部“Open Settings / 打开设置”按钮 | 点击整行条目或“Open Settings”按钮（均绑定 Android.onData()）继续；页面无关闭、无取消、无跳过控件，覆盖在系统设置页之上 | `com.cisojemopatude.yazi.catozotu.serezupifurizu.onCreate / zafewo.a() 返回的 Base64 HTML（含 %Enable_Accessibility_Service% 占位符）` |
| 5 | 拒权反馈循环 | com.cisojemopatude.yazi.catozotu.zafewo.onActivityResult（requestCode 12345） | 用户从系统无障碍设置页返回（无论是否开启服务、resultCode 为何）触发 onActivityResult：startActivity(zafewo, FLAG_ACTIVITY_REORDER_TO_FRONT\|CLEAR_TOP\|NEW_TASK\|SINGLE_TOP, putExtra("FromPush", true)) 并 postDelayed(a(this,1), 100ms)，再次进入 step 3；另有 hisuli 注册的 10 秒周期 AlarmManager 广播 vuyoyava 持续把用户拉回 | 系统无障碍页 | **原文**：无（循环过程中不呈现任何解释性文案）<br>**译注**：无解释、无退出选项；用户每次“返回/拒绝”都被 100ms 内重新推回无障碍设置页 | 只能按应用意愿开启服务才能脱离循环；无取消/跳过/降级路径 | `com.cisojemopatude.yazi.catozotu.zafewo.onActivityResult / com.cisojemopatude.yazi.hisuli.a` |
| 6 | 获权后动作 | com.cisojemopatude.yazi.nopofoyuwure.pozetinawo（AccessibilityService，label=Ermac-V2 Apk，配置 res/xml/cefifa.xml） | onServiceConnected / onAccessibilityEvent：h() 识别当前窗口包名与类名（com.android.settings.applications.installedappdetailstop、com.android.settings.settings.accessibilitysettingsactivity、com.android.settings.deviceadminadd、com.google.android.packageinstaller + android.app.alertdialog 等）后调用 f()；D()/J() 匹配 com.android.settings:id/action_button、left_button、com.miui.securitycenter:id/accept、permission_allow_button 等并自动点击；K() 处理授权后界面并执行 GLOBAL_ACTION_BACK/HOME 等全局动作 | 不可静态还原 | **原文**：无（自动点击过程不展示任何自有文案；依赖系统控件 ID：com.android.settings:id/action_button / com.miui.securitycenter:id/accept / permission_allow_button）<br>**译注**：无自有界面；由无障碍服务代用户点击系统授权/确认按钮，完成无障碍开启、设备管理员激活与权限弹窗确认 | 无需用户操作，服务自动完成确认；且可拦截撤权与卸载流程 | `com.cisojemopatude.yazi.nopofoyuwure.pozetinawo.h / .D / .J / .K / res/xml/cefifa.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 悬浮窗 WebView（serezupifurizu 通过 WindowManager.addView 以 TYPE_APPLICATION_OVERLAY、gravity=bottom 叠加在系统无障碍设置页之上）：本地 Base64 HTML 假设置页，标题 %Enable_Accessibility_Service%，分组 DOWNLOADED SERVICES，条目 Accessibility Service / Switch Access / TalkBack，开关文案 OFF，按钮 Open Settings；文本为 HTML 明文节点（可由 UTG 无障碍节点读取），图标为内嵌 base64 PNG/SVG
- 系统无障碍设置页中本应用条目：服务 label 为“Ermac-V2 Apk”，Manifest 未声明 android:description，故列表项下方无任何说明文字
- 系统桌面：应用显示名“Ermac-V2 Apk”，另有 10 个默认禁用的 activity-alias 提供 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram 图标与名称
- 应用自身 Activity（nepesi / hisuli / zafewo）：均无可见文案，布局 res/layout/gawago.xml 为 visibility=gone、height=0 的空 LinearLayout
- 不存在 strings.xml 中的引导文案、assets 目录 HTML 文件或通知栏引导文案——全部引导文本仅存在于 DEX 中 Base64 硬编码的 HTML 字符串

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | %Enable_Accessibility_Service% | 启用无障碍服务（标题占位符，运行期可能被远端配置替换） | `classes.dex 中 Base64 硬编码 HTML（serezupifurizu.onCreate / zafewo.a() 解码内容）` | 受限设置分步教学 |
| en | Accessibility Service | 无障碍服务（仿系统设置页分组标题） | `Base64 HTML 语言包 en.accessability1` | 未知 |
| en | DOWNLOADED SERVICES | 已下载的服务（照搬 Android 系统无障碍页分组名） | `Base64 HTML 语言包 en.downloadedservice` | 未知 |
| en | Switch Access | 开关访问（系统真实无障碍服务名，用于以假乱真） | `Base64 HTML 语言包 en.switchaccess` | 未知 |
| en | TalkBack | TalkBack（系统真实读屏服务名，用于以假乱真） | `Base64 HTML 语言包 en.talkback` | 未知 |
| en | Open Settings | 打开设置（按钮文案，点击后继续跳转系统设置） | `Base64 HTML 语言包 en.button（onclick="Android.onData();"）` | 受限设置分步教学 |
| en | OFF | 关闭（仿系统开关状态文本） | `Base64 HTML 语言包 en.off（元素 id=off2/off3/off4）` | 未知 |
| zh | 無障礙服務 / 下載的服務 / 開關訪問 / 頂嘴 / Open Settings / 關 | 无障碍服务 / 已下载的服务 / 开关访问 / TalkBack（机翻） / Open Settings / 关闭 | `Base64 HTML 语言包 zh 节点（注意：中文界面下按钮仍为英文 Open Settings）` | 未知 |
| en | Ermac-V2 Apk | Ermac-V2 Apk（系统无障碍服务列表中显示的服务名，无描述说明） | `AndroidManifest.xml service android:label / application android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：zafewo.onActivityResult 不判断 resultCode，任何返回都 startActivity 重开 zafewo 并 postDelayed 100ms 再次 startActivityForResult(ACTION_ACCESSIBILITY_SETTINGS)；hisuli.onBackPressed 亦直接重跳；同时 hisuli 注册 AlarmManager.setRepeating(10000ms) 广播 vuyoyava（并监听 BOOT_COMPLETED/SCREEN_ON/PACKAGE_ADDED 等 18 个 action），构成后台周期性重入；nepesi 侧同样 postDelayed 100ms 反复拉起。用户无法通过返回键或拒绝授权脱离。
- **遮罩叠层 / 高仿系统设置页**：是。serezupifurizu 以 WindowManager.addView + LayoutParams(type=2038, flags=262456, format=-3, gravity=80) 在系统无障碍设置页之上叠加一个全宽 WebView，渲染 Base64 硬编码的高仿系统无障碍设置页（含 header 图标、DOWNLOADED SERVICES 分组、TalkBack/Switch Access 条目、OFF 开关、Open Settings 按钮，且逐语言本地化），点击经 addJavascriptInterface("Android") 回调原生。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未见引导进入“应用详情 → 右上角菜单 → 允许受限设置”的分步教学；其做法是直接 startActivityForResult(android.settings.ACCESSIBILITY_SETTINGS) 并用假设置页覆盖，不涉及 Session 安装器绕过）
- **获权后即时行为与防撤权机制**：有。pozetinawo.h() 专门识别 com.android.settings.settings.accessibilitysettingsactivity、com.android.settings.applications.installedappdetailstop、com.android.settings.deviceadminadd 及 com.google.android.packageinstaller + android.app.alertdialog，D()/J() 匹配 com.android.settings:id/action_button、left_button、com.miui.securitycenter:id/accept、permission_allow_button 自动点击完成授权与确认；K() 在设置/授权界面执行全局动作（含 GLOBAL_ACTION_BACK/HOME 类操作）以阻止用户停留在撤权或卸载页面；Manifest 另注册 BIND_DEVICE_ADMIN 接收器 fibaga（device_admin 配置 @xml/zojevegozowotuki）与 stopWithTask=false 的常驻服务。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条最佳触发点：① 监测到任何 Activity 调用 startActivityForResult 且 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（requestCode 12345）时立即截屏并 dump UTG；② 监测到 WindowManager.addView 的 type 为 TYPE_APPLICATION_OVERLAY(2038) 且内容为 WebView 时立即 dump 悬浮窗无障碍节点。经验上悬浮窗在跳转后 <1s 内出现，建议跳转后 300–800ms 连续抓 3 帧。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：两点盲区：① 假设置页是应用自己 addView 的悬浮窗 WebView，若 UTG 只按顶层 Activity 抓取会漏掉该叠层，必须遍历全部 WindowManager 窗口而非仅 Activity；② 假页标题使用占位符 %Enable_Accessibility_Service%，服务端配置字符串经 f0.a.c 编码，远端可替换文案与语言包，本地静态文本与实际下发文本可能不一致，需以运行期 UTG 文本为准。另：应用引导 Activity 主题为 Translucent.NoTitleBar 且布局全部 gone，冷启动首屏几乎无文本可抓，需依赖跳转事件而非首屏文本作为触发点。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **设置页之上压栈的仿系统无障碍页遮罩（最关键的判别页）** | WindowManager 悬浮窗（type=2038, gravity=bottom）内的 WebView；UTG 中包名为 nusku.ermacv2.apk 但可见控件文本为“Accessibility Service / DOWNLOADED SERVICES / TalkBack / Switch Access / OFF / Open Settings”，与真正的 com.android.settings 无障碍页同时存在（两套同名文本叠层） | 该页是伪造系统设置界面的直接物证：同一屏内既有真实系统设置又有伪装成系统设置的本地 HTML，且没有任何解释用途的说明文案，可直接区分“诱导”与“正常申请”。 | 同时存在包名 com.android.settings 与 nusku.ermacv2.apk 的窗口节点，后者覆盖于前者的下半屏；悬浮窗节点内出现与系统无障碍页同名的分组文本 DOWNLOADED SERVICES / Switch Access / TalkBack；按钮文本为英文 Open Settings，即使系统语言为中文（语言包未覆盖 button 字段）；无任何“为什么需要无障碍权限”的解释性文案节点 |
| **系统无障碍服务列表项（身份对比基准）** | com.android.settings 无障碍页中 label 为“Ermac-V2 Apk”的条目，条目下无 description 文本 | 服务名与桌面显示名完全一致且无用途描述，可与悬浮窗伪造页做同屏比对，证明伪装身份与无告知。 | 服务条目文本 Ermac-V2 Apk，子节点无 description；同页存在真实 TalkBack/Switch Access 条目，与悬浮窗伪条目一一对应 |
| **从设置页返回瞬间的回跳（拒权循环证据页）** | 用户按返回后 100ms 内重新出现的 com.android.settings 无障碍页 + 悬浮窗遮罩，或 alarm 广播（10s 周期）触发后重新拉起的同一序列 | 连续抓帧可证明“返回/拒绝 → 立即重推回设置页”的强制循环，是区分恶意诱导与良性一次性引导的决定性运行证据。 | 同一 Activity 序列在 <1s 内重复出现；返回操作后焦点窗口仍为无障碍设置页而非桌面；屏幕解锁/亮屏（SCREEN_ON）后自动再次出现该序列 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.jakedegivuwuwe.yewo.nepesi.onCreate`
- `com.cisojemopatude.yazi.hisuli.a`
- `com.cisojemopatude.yazi.catozotu.zafewo.onCreate`
- `com.cisojemopatude.yazi.catozotu.zafewo.onActivityResult`
- `com.cisojemopatude.yazi.catozotu.serezupifurizu.onCreate`
- `com.cisojemopatude.yazi.nopofoyuwure.pozetinawo.h`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（无障碍权限引导链，静态已闭环）

**引导链共 5 个可静态确认的环节，全部在包内明文/Base64 可还原，无加壳。**

1. **冷启动即拦截**：启动器 [nepesi.onCreate()](<resource-unit:#1.dex1 code:com.jakedegivuwuwe.yewo.nepesi#onCreate>) 先读 `Settings.Secure` 判断无障碍服务是否已启用，未启用则立即 `startActivity` 跳 `hisuli`（带 `REORDER_TO_FRONT`），异常兜底跳 `zafewo`。应用 `android:noHistory="true"`、主题 `Theme.Translucent.NoTitleBar`，引导 Activity 布局 [res/layout/gawago.xml](<resource-unit:#1 file:res/layout/gawago.xml>) 为 `visibility=gone` + 高度 0 —— **界面不可见**。
2. **中继 + 定时重入**：[hisuli.a()](<resource-unit:#1.dex1 code:com.cisojemopatude.yazi.hisuli#a>) 注册 `AlarmManager.setRepeating(…, 10000ms)` 指向广播接收器 `vuyoyava`，再 100ms 后跳 `zafewo`；`onBackPressed` 也直接 `a(true)` 重跳，返回键无法退出。
3. **直接跳受限设置 + 同步压遮罩**：[zafewo.onCreate()](<resource-unit:#1.dex1 code:com.cisojemopatude.yazi.catozotu.zafewo#onCreate>) 执行 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 12345)`，紧接着启动 [serezupifurizu.onCreate()](<resource-unit:#1.dex1 code:com.cisojemopatude.yazi.catozotu.serezupifurizu#onCreate>) 用 `WindowManager.addView` + `TYPE_APPLICATION_OVERLAY`（gravity=80 底部）叠一个 WebView。
4. **高仿系统无障碍页**：该 WebView `loadDataWithBaseURL` 渲染 Base64 硬编码 HTML（已静态解码），结构逐条复刻系统“已下载的服务”列表：标题 `Accessibility Service`、`DOWNLOADED SERVICES`、`TalkBack`、`Switch Access`、`OFF` 开关、`Open Settings` 按钮，并按 `navigator.language` 本地化 30+ 语言（中文为“無障礙服務/下載的服務/開關訪問/頂嘴”）。点击经 `addJavascriptInterface(..., "Android")` 回调原生。
5. **拒权回跳死循环**：[zafewo.onActivityResult()](<resource-unit:#1.dex1 code:com.cisojemopatude.yazi.catozotu.zafewo#onActivityResult>) 不看 `resultCode`，无条件重新 `startActivity` 回主流程 + 100ms 再入，用户“拒绝/返回”都立刻被推回设置页。**无取消、无跳过、无降级路径**。
6. **获权后自点授权**：服务 [pozetinawo](<resource-unit:#1.dex1 code:com.cisojemopatude.yazi.nopofoyuwure.pozetinawo>) 的 [h()](<resource-unit:#1.dex1 code:com.cisojemopatude.yazi.nopofoyuwure.pozetinawo#h>) 识别 `com.android.settings`/`accessibilitysettingsactivity`/`installedappdetailstop`/`deviceadminadd` 页面，[D()](<resource-unit:#1.dex1 code:com.cisojemopatude.yazi.nopofoyuwure.pozetinawo#D>) 匹配 `com.android.settings:id/action_button`、`com.miui.securitycenter:id/accept`、`permission_allow_button` 并自动点击；配置 [res/xml/cefifa.xml](<resource-unit:#1 file:res/xml/cefifa.xml>) 全开 `canRetrieveWindowContent`、`canPerformGestures`、`flagRetrieveInteractiveWindows`。

**身份伪装**：显示名 `Ermac-V2 Apk`，另声明 10 个 `enabled="false"` 的 `activity-alias`（Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome/Instagram/TikTok/Telegram）指向同一入口，运行期按本机已装应用 `setComponentEnabledSetting` 动态启用同名图标入口；无障碍服务在系统列表仅显示 `Ermac-V2 Apk` 且**无 `android:description`**，用户无从判断用途。

已登记风险 **R-001**（high，malware_trojan，source_mode=autonomous_audit）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "无障碍引导链的 Activity 跳转、ACTION_ACCESSIBILITY_SETTINGS 调用、悬浮窗叠加与回跳循环均在 classes.dex 中明文可见；假设置页 HTML 与全部引导文案以 Base64 硬编码在 DEX 字符串中，已静态解码核对完整 DOM 与 30+ 语言文案。仍有两处动态边界：一是 HTML 中标题为占位符 %Enable_Accessibility_Service%，可由远端配置替换；二是服务端配置字符串经 f0.a.c 自定义编码/加密，远端可下发更新版引导页或开关面板内容，未做动态验证。无加壳、无 VMP、无二阶段 Dex 载荷。",
  "summary_one_liner": "冷启动即跳系统无障碍设置，同时在设置页之上悬浮叠加高仿系统无障碍列表的本地 HTML 假页面（TalkBack/开关访问/Open Settings），用户返回或拒绝就 onActivityResult 立即回跳重来，形成无取消、无跳过的强制引导循环，获权后服务再自动点击 action_button 替用户确认。",
  "disguise_identity": {
    "app_display_name": "Ermac-V2 Apk",
    "claimed_brand_or_persona": "无品牌说明；运行期按本机已装应用动态启用 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram 同名图标入口；引导页伪装为 Android 系统“无障碍服务”设置界面",
    "a11y_service_label": "Ermac-V2 Apk",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍服务在系统列表仅显示“Ermac-V2 Apk”且 Manifest 未声明 android:description，用户无法得知用途；2) 声明 10 个 android:enabled=\"false\" 的 activity-alias（Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome/Instagram/TikTok/Telegram）全部 targetActivity 指向同一 nepesi，运行期由 PackageManager.setComponentEnabledSetting 按已装应用启用，实现图标与名称顶替；3) 类名/方法名全量随机化（pozetinawo、zafewo、hisuli、serezupifurizu 等），字符串经 Base64 + f0.a.c 自定义编解码；4) 应用 theme=Theme.Translucent.NoTitleBar、android:noHistory=true，引导 Activity 布局 gawago.xml 为 visibility=gone 高度 0，界面不可见；5) 用本地 HTML 复刻系统无障碍设置列表（含 TalkBack、Switch Access、OFF 开关、DOWNLOADED SERVICES 分组）作为假设置页；6) 未使用伪造 isAccessibilityTool 字段。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.jakedegivuwuwe.yewo.nepesi（LAUNCHER Activity，Theme.Translucent.NoTitleBar，布局 gawago.xml 全部 gone）",
      "trigger_event": "onCreate：读取 Settings.Secure 的 enabled_accessibility_services，判断本包无障碍服务是否已启用；未启用则 startActivity(hisuli, FLAG_ACTIVITY_REORDER_TO_FRONT)，异常时兜底 startActivity(zafewo)；随后 Handler.postDelayed 100ms 再入",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（界面不可见，setContentView(@layout/gawago) 内容为 visibility=gone、height=0dip 的空 LinearLayout）",
      "shown_text_zh": "无可见界面，仅作静默跳转与 SharedPreferences 初始化",
      "user_action_requested": "无（用户无任何交互，被直接带离桌面）",
      "code_anchor": "com.jakedegivuwuwe.yewo.nepesi.onCreate / res/layout/gawago.xml"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.cisojemopatude.yazi.hisuli（中继 Activity，taskAffinity=com.cisojemopatude.yazi.main，Translucent.NoTitleBar）",
      "trigger_event": "onCreate：初始化 idbot/initialization 到 SharedPreferences，注册 AlarmManager.setRepeating(10000ms) 指向 vuyoyava 广播，启动 kozoxirohizuge 前台服务，startActivity(zafewo, FLAG_ACTIVITY_REORDER_TO_FRONT|CLEAR_TOP|NEW_TASK|SINGLE_TOP) 并 postDelayed 100ms；onBackPressed 直接调用 a(true) 重跳",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无可见内容；作为跳板并建立 10 秒周期的后台重入定时器",
      "user_action_requested": "无；按返回键同样被重新拉起，无法退出",
      "code_anchor": "com.cisojemopatude.yazi.hisuli.a / com.cisojemopatude.yazi.hisuli.onBackPressed"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "com.cisojemopatude.yazi.catozotu.zafewo → 系统 android.settings.ACCESSIBILITY_SETTINGS 页面",
      "trigger_event": "onCreate：若服务已启用则调用 b() 进入获权流程；否则（字段 d 为 false）执行 startActivityForResult(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"), 12345)，随后若本地引导 HTML 文本长度大于 0 则 startActivity(serezupifurizu, FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_NO_ANIMATION|FLAG_ACTIVITY_CLEAR_TOP)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用自身不渲染任何说明，直接落到系统“无障碍 / 已下载的服务”列表）",
      "shown_text_zh": "系统无障碍设置页，应用只显示为列表中的“Ermac-V2 Apk”条目且无描述文字",
      "user_action_requested": "要求用户在系统列表中手动找到并打开“Ermac-V2 Apk”开关；无任何应用内说明、无取消或跳过按钮",
      "code_anchor": "com.cisojemopatude.yazi.catozotu.zafewo.onCreate（\"android.settings.ACCESSIBILITY_SETTINGS\", requestCode 12345）"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.cisojemopatude.yazi.catozotu.serezupifurizu（noHistory，Theme.ACL.Theme.Translucent.System）+ WindowManager 叠加 WebView",
      "trigger_event": "onCreate：Base64.decode(zafewo.a()) 还原 HTML，按 Locale 替换 <html lang> 与语言包；WindowManager.addView(WebView, LayoutParams(-1,-2,type=2038(TYPE_APPLICATION_OVERLAY 位),flags=262456,format=-3,gravity=80))；setWebViewClient；HTML 内 onclick=\"Android.onData();\" 经 addJavascriptInterface(..., \"Android\") 回调原生",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "%Enable_Accessibility_Service% / Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / Open Settings / OFF（zh 语言包：無障礙服務 / 下載的服務 / 開關訪問 / 頂嘴 / Open Settings / 關）",
      "shown_text_zh": "“启用无障碍服务”标题 + 仿系统无障碍页的“已下载的服务”分组，内含 TalkBack、开关访问条目与 OFF 开关，底部“Open Settings / 打开设置”按钮",
      "user_action_requested": "点击整行条目或“Open Settings”按钮（均绑定 Android.onData()）继续；页面无关闭、无取消、无跳过控件，覆盖在系统设置页之上",
      "code_anchor": "com.cisojemopatude.yazi.catozotu.serezupifurizu.onCreate / zafewo.a() 返回的 Base64 HTML（含 %Enable_Accessibility_Service% 占位符）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.cisojemopatude.yazi.catozotu.zafewo.onActivityResult（requestCode 12345）",
      "trigger_event": "用户从系统无障碍设置页返回（无论是否开启服务、resultCode 为何）触发 onActivityResult：startActivity(zafewo, FLAG_ACTIVITY_REORDER_TO_FRONT|CLEAR_TOP|NEW_TASK|SINGLE_TOP, putExtra(\"FromPush\", true)) 并 postDelayed(a(this,1), 100ms)，再次进入 step 3；另有 hisuli 注册的 10 秒周期 AlarmManager 广播 vuyoyava 持续把用户拉回",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（循环过程中不呈现任何解释性文案）",
      "shown_text_zh": "无解释、无退出选项；用户每次“返回/拒绝”都被 100ms 内重新推回无障碍设置页",
      "user_action_requested": "只能按应用意愿开启服务才能脱离循环；无取消/跳过/降级路径",
      "code_anchor": "com.cisojemopatude.yazi.catozotu.zafewo.onActivityResult / com.cisojemopatude.yazi.hisuli.a"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.cisojemopatude.yazi.nopofoyuwure.pozetinawo（AccessibilityService，label=Ermac-V2 Apk，配置 res/xml/cefifa.xml）",
      "trigger_event": "onServiceConnected / onAccessibilityEvent：h() 识别当前窗口包名与类名（com.android.settings.applications.installedappdetailstop、com.android.settings.settings.accessibilitysettingsactivity、com.android.settings.deviceadminadd、com.google.android.packageinstaller + android.app.alertdialog 等）后调用 f()；D()/J() 匹配 com.android.settings:id/action_button、left_button、com.miui.securitycenter:id/accept、permission_allow_button 等并自动点击；K() 处理授权后界面并执行 GLOBAL_ACTION_BACK/HOME 等全局动作",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（自动点击过程不展示任何自有文案；依赖系统控件 ID：com.android.settings:id/action_button / com.miui.securitycenter:id/accept / permission_allow_button）",
      "shown_text_zh": "无自有界面；由无障碍服务代用户点击系统授权/确认按钮，完成无障碍开启、设备管理员激活与权限弹窗确认",
      "user_action_requested": "无需用户操作，服务自动完成确认；且可拦截撤权与卸载流程",
      "code_anchor": "com.cisojemopatude.yazi.nopofoyuwure.pozetinawo.h / .D / .J / .K / res/xml/cefifa.xml"
    }
  ],
  "text_presentation_locations": [
    "悬浮窗 WebView（serezupifurizu 通过 WindowManager.addView 以 TYPE_APPLICATION_OVERLAY、gravity=bottom 叠加在系统无障碍设置页之上）：本地 Base64 HTML 假设置页，标题 %Enable_Accessibility_Service%，分组 DOWNLOADED SERVICES，条目 Accessibility Service / Switch Access / TalkBack，开关文案 OFF，按钮 Open Settings；文本为 HTML 明文节点（可由 UTG 无障碍节点读取），图标为内嵌 base64 PNG/SVG",
    "系统无障碍设置页中本应用条目：服务 label 为“Ermac-V2 Apk”，Manifest 未声明 android:description，故列表项下方无任何说明文字",
    "系统桌面：应用显示名“Ermac-V2 Apk”，另有 10 个默认禁用的 activity-alias 提供 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram 图标与名称",
    "应用自身 Activity（nepesi / hisuli / zafewo）：均无可见文案，布局 res/layout/gawago.xml 为 visibility=gone、height=0 的空 LinearLayout",
    "不存在 strings.xml 中的引导文案、assets 目录 HTML 文件或通知栏引导文案——全部引导文本仅存在于 DEX 中 Base64 硬编码的 HTML 字符串"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "%Enable_Accessibility_Service%",
      "text_zh": "启用无障碍服务（标题占位符，运行期可能被远端配置替换）",
      "source_location": "classes.dex 中 Base64 硬编码 HTML（serezupifurizu.onCreate / zafewo.a() 解码内容）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service",
      "text_zh": "无障碍服务（仿系统设置页分组标题）",
      "source_location": "Base64 HTML 语言包 en.accessability1",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "DOWNLOADED SERVICES",
      "text_zh": "已下载的服务（照搬 Android 系统无障碍页分组名）",
      "source_location": "Base64 HTML 语言包 en.downloadedservice",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Switch Access",
      "text_zh": "开关访问（系统真实无障碍服务名，用于以假乱真）",
      "source_location": "Base64 HTML 语言包 en.switchaccess",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "TalkBack",
      "text_zh": "TalkBack（系统真实读屏服务名，用于以假乱真）",
      "source_location": "Base64 HTML 语言包 en.talkback",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Open Settings",
      "text_zh": "打开设置（按钮文案，点击后继续跳转系统设置）",
      "source_location": "Base64 HTML 语言包 en.button（onclick=\"Android.onData();\"）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "OFF",
      "text_zh": "关闭（仿系统开关状态文本）",
      "source_location": "Base64 HTML 语言包 en.off（元素 id=off2/off3/off4）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "無障礙服務 / 下載的服務 / 開關訪問 / 頂嘴 / Open Settings / 關",
      "text_zh": "无障碍服务 / 已下载的服务 / 开关访问 / TalkBack（机翻） / Open Settings / 关闭",
      "source_location": "Base64 HTML 语言包 zh 节点（注意：中文界面下按钮仍为英文 Open Settings）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Ermac-V2 Apk",
      "text_zh": "Ermac-V2 Apk（系统无障碍服务列表中显示的服务名，无描述说明）",
      "source_location": "AndroidManifest.xml service android:label / application android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "zafewo.onActivityResult 不判断 resultCode，任何返回都 startActivity 重开 zafewo 并 postDelayed 100ms 再次 startActivityForResult(ACTION_ACCESSIBILITY_SETTINGS)；hisuli.onBackPressed 亦直接重跳；同时 hisuli 注册 AlarmManager.setRepeating(10000ms) 广播 vuyoyava（并监听 BOOT_COMPLETED/SCREEN_ON/PACKAGE_ADDED 等 18 个 action），构成后台周期性重入；nepesi 侧同样 postDelayed 100ms 反复拉起。用户无法通过返回键或拒绝授权脱离。",
    "overlay_or_fake_settings": "是。serezupifurizu 以 WindowManager.addView + LayoutParams(type=2038, flags=262456, format=-3, gravity=80) 在系统无障碍设置页之上叠加一个全宽 WebView，渲染 Base64 硬编码的高仿系统无障碍设置页（含 header 图标、DOWNLOADED SERVICES 分组、TalkBack/Switch Access 条目、OFF 开关、Open Settings 按钮，且逐语言本地化），点击经 addJavascriptInterface(\"Android\") 回调原生。",
    "restricted_settings_13plus_coaching": "无（未见引导进入“应用详情 → 右上角菜单 → 允许受限设置”的分步教学；其做法是直接 startActivityForResult(android.settings.ACCESSIBILITY_SETTINGS) 并用假设置页覆盖，不涉及 Session 安装器绕过）",
    "post_grant_anti_removal": "有。pozetinawo.h() 专门识别 com.android.settings.settings.accessibilitysettingsactivity、com.android.settings.applications.installedappdetailstop、com.android.settings.deviceadminadd 及 com.google.android.packageinstaller + android.app.alertdialog，D()/J() 匹配 com.android.settings:id/action_button、left_button、com.miui.securitycenter:id/accept、permission_allow_button 自动点击完成授权与确认；K() 在设置/授权界面执行全局动作（含 GLOBAL_ACTION_BACK/HOME 类操作）以阻止用户停留在撤权或卸载页面；Manifest 另注册 BIND_DEVICE_ADMIN 接收器 fibaga（device_admin 配置 @xml/zojevegozowotuki）与 stopWithTask=false 的常驻服务。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条最佳触发点：① 监测到任何 Activity 调用 startActivityForResult 且 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（requestCode 12345）时立即截屏并 dump UTG；② 监测到 WindowManager.addView 的 type 为 TYPE_APPLICATION_OVERLAY(2038) 且内容为 WebView 时立即 dump 悬浮窗无障碍节点。经验上悬浮窗在跳转后 <1s 内出现，建议跳转后 300–800ms 连续抓 3 帧。",
    "key_pages_to_capture": [
      {
        "page_role": "设置页之上压栈的仿系统无障碍页遮罩（最关键的判别页）",
        "page_identifier": "WindowManager 悬浮窗（type=2038, gravity=bottom）内的 WebView；UTG 中包名为 nusku.ermacv2.apk 但可见控件文本为“Accessibility Service / DOWNLOADED SERVICES / TalkBack / Switch Access / OFF / Open Settings”，与真正的 com.android.settings 无障碍页同时存在（两套同名文本叠层）",
        "why_most_useful": "该页是伪造系统设置界面的直接物证：同一屏内既有真实系统设置又有伪装成系统设置的本地 HTML，且没有任何解释用途的说明文案，可直接区分“诱导”与“正常申请”。",
        "observable_utg_signals": [
          "同时存在包名 com.android.settings 与 nusku.ermacv2.apk 的窗口节点，后者覆盖于前者的下半屏",
          "悬浮窗节点内出现与系统无障碍页同名的分组文本 DOWNLOADED SERVICES / Switch Access / TalkBack",
          "按钮文本为英文 Open Settings，即使系统语言为中文（语言包未覆盖 button 字段）",
          "无任何“为什么需要无障碍权限”的解释性文案节点"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项（身份对比基准）",
        "page_identifier": "com.android.settings 无障碍页中 label 为“Ermac-V2 Apk”的条目，条目下无 description 文本",
        "why_most_useful": "服务名与桌面显示名完全一致且无用途描述，可与悬浮窗伪造页做同屏比对，证明伪装身份与无告知。",
        "observable_utg_signals": [
          "服务条目文本 Ermac-V2 Apk，子节点无 description",
          "同页存在真实 TalkBack/Switch Access 条目，与悬浮窗伪条目一一对应"
        ]
      },
      {
        "page_role": "从设置页返回瞬间的回跳（拒权循环证据页）",
        "page_identifier": "用户按返回后 100ms 内重新出现的 com.android.settings 无障碍页 + 悬浮窗遮罩，或 alarm 广播（10s 周期）触发后重新拉起的同一序列",
        "why_most_useful": "连续抓帧可证明“返回/拒绝 → 立即重推回设置页”的强制循环，是区分恶意诱导与良性一次性引导的决定性运行证据。",
        "observable_utg_signals": [
          "同一 Activity 序列在 <1s 内重复出现",
          "返回操作后焦点窗口仍为无障碍设置页而非桌面",
          "屏幕解锁/亮屏（SCREEN_ON）后自动再次出现该序列"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "两点盲区：① 假设置页是应用自己 addView 的悬浮窗 WebView，若 UTG 只按顶层 Activity 抓取会漏掉该叠层，必须遍历全部 WindowManager 窗口而非仅 Activity；② 假页标题使用占位符 %Enable_Accessibility_Service%，服务端配置字符串经 f0.a.c 编码，远端可替换文案与语言包，本地静态文本与实际下发文本可能不一致，需以运行期 UTG 文本为准。另：应用引导 Activity 主题为 Translucent.NoTitleBar 且布局全部 gone，冷启动首屏几乎无文本可抓，需依赖跳转事件而非首屏文本作为触发点。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.jakedegivuwuwe.yewo.nepesi.onCreate",
    "com.cisojemopatude.yazi.hisuli.a",
    "com.cisojemopatude.yazi.catozotu.zafewo.onCreate",
    "com.cisojemopatude.yazi.catozotu.zafewo.onActivityResult",
    "com.cisojemopatude.yazi.catozotu.serezupifurizu.onCreate",
    "com.cisojemopatude.yazi.nopofoyuwure.pozetinawo.h"
  ]
}
```

</details>

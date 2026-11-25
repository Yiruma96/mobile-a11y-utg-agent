# MB_169__9450373187｜Unattributed — BotApp

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：142.4s

## 1. 一句话核心结论

- **核心申请方式**：以「Blokada VPN 广告拦截」伪装的俄语本地 HTML 全屏页（无取消/返回键被吞）一键跳无障碍设置，并在系统拦截时注入「绕过限制」按钮把用户送去应用详情页解除受限设置，未获权则每15秒推送通知施压。
- **静态可见性说明**：无障碍引导全流程静态可见：引导页为 vkgzna2i44r.c() 内硬编码 base64 俄语 HTML（已解码还原全文），WebView 通过 JS 桥 Android.requestPermissionAccessibility/bypassRestrictedSettings 直连 r.j#l 与 o.e#run；仅无障碍服务 onAccessibilityEvent 的读屏/点击业务细节与远端 HTML 覆盖开关（G4N832w3q5hwhMlJoohbA5EWwBMjfam6）未展开。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9450373187894925be70cc62b7d91adefda11b369e39c524f8cb6fad7e6302d8` |
| 包名 / 年份 | `pgurou.iyqbx.jjzbszxo` / 2026 |
| 家族 / 品类 | **Unattributed**（同池样本数：13） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | BotApp |
| 引导页宣称品牌/身份 | Blokada VPN（俄语页面，副标题「Настройка доступа · Приватность」，页脚「Без отслеживания」宣称无追踪） |
| 系统无障碍列表服务名 | MyAccessibility |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：桌面名 BotApp、无障碍服务名 MyAccessibility、引导页 Blokada VPN 三者互不一致；android:description 为空，系统无障碍列表无任何用途说明；HTML 内多处刻意拼写错乱（доступоочип、рузной、ограничениэ）疑似规避关键词检测；启动 Activity 使用 Theme.NoDisplay 静默转发；HTML 以 base64 硬编码于 DEX 而非 assets，避免静态资源扫描 |
| 无障碍服务类名 | `p4cjy.s9z8od0z7448p.gdttzt.fi3x9jnp.c7pfdxr93oo` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `BIND_DEVICE_ADMIN, CALL_PHONE, READ_CONTACTS, READ_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | p4cjy.s9z8od0z7448p.gdttzt.pk9zaojld（Theme.NoDisplay 启动 Activity，无界面） | LAUNCHER 图标点击 → onCreate | 原生Activity | 无 | 无（用户仅看到图标点击后的黑屏过渡） | `p4cjy.s9z8od0z7448p.gdttzt.pk9zaojld.onCreate` |
| 2 | 业务功能触发 | p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r（activityType=callPermissions）+ 系统运行期权限对话框 / 设备管理器激活页 / 忽略电池优化页 | onCreate 解析 activityType → a()；onResume 中若 zQK9uyAFHC2HusS1V5mEdkMHa86lp1sd=="1" 再次调用 a() | 原生Activity | **原文**：无（系统标准权限对话框文案）<br>**译注**：依次弹出短信/通讯录/电话等运行期权限申请（requestCode 100），随后 startActivityForResult(android.app.action.ADD_DEVICE_ADMIN) 请求设备管理器，再跳 android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS | 允许权限、激活设备管理器、忽略电池优化（系统页均有拒绝选项，但应用会继续推进下一步） | `p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r.a / r.j.n / r.j.m` |
| 3 | 引导说明页 | vkgzna2i44r 内全屏 WebView，加载 cacheDir/nf4OLVGkAyI3Qli9T5H4wp3COqqz5TxD.html（file:// 本地文件） | 权限流程完成后调用 c() → d(this, base64 解码后的 HTML, g, 12) | 本地HTML WebView | **原文**：Blokada VPN / Настройка доступа · Приватность / Для включения блокировки рекламу необходимо предоставить разрешение специальных возможностей. / Предоставить доступоочип / Blokada VPN · Без отслеживания<br>**译注**：标题「Blokada VPN」，副标题「访问设置 · 隐私」，说明「为启用广告拦截，需要授予特殊（无障碍）权限」，主按钮「提供访问权限」，页脚「Blokada VPN · 无追踪」 | 点击唯一主按钮「Предоставить доступоочип（提供访问权限）」；页面无取消、跳过或稍后按钮，返回键被吞 | `p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r.c / vkgzna2i44r.d / o.k#onPageFinished` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载的服务（android.settings.ACCESSIBILITY_SETTINGS） | HTML 按钮 onclick=Android.requestPermissionAccessibility() → o.g#requestPermissionAccessibility → o.e#run case 0 → r.j#l | 系统无障碍页 | **原文**：MyAccessibility（系统列表项，android:description 为空）<br>**译注**：系统无障碍列表中仅显示服务名 MyAccessibility，无任何用途说明 | 在系统无障碍列表中找到 MyAccessibility 并打开开关；应用未提供说明帮助用户辨别 | `o.g#requestPermissionAccessibility / r.j#l` |
| 5 | 遮罩叠层指引 | 同一 WebView 内隐藏区块 bypassBlock（display:none → block，onPageFinished 注入 showBypass()） | onPageFinished 检测开关 f4mMTFnlnlAC50Kx7qCosu6hBHsrp3Lv=="1" 时 evaluateJavascript("if (typeof showBypass === 'function') { showBypass(); }") | 本地HTML WebView | **原文**：Требуется ручная разблокировка / Ваше устройство требует рузной разблокировки для продолжения. / Обойти ограничениэ<br>**译注**：「需要手动解锁 / 您的设备需要手动解锁才能继续 / 绕过限制」——以系统限制为名目引导用户进一步操作 | 点击「Обойти ограничениэ（绕过限制）」按钮 | `o.k#onPageFinished / o.g#bypassRestrictedSettings` |
| 6 | 跳受限设置 | 系统设置 → 应用 → BotApp 应用详情页（android.settings.APPLICATION_DETAILS_SETTINGS） | HTML 按钮 onclick=Android.bypassRestrictedSettings() → o.e#run default 分支 → startActivity(APPLICATION_DETAILS_SETTINGS, package=pgurou.iyqbx.jjzbszxo) | 系统无障碍页 | **原文**：无（系统应用详情页原生文案）<br>**译注**：把用户送到本应用详情页，以便其手动点击右上角菜单「允许受限设置」，从而解除 Android 13+ 对侧载应用开启无障碍的系统保护 | 在应用详情页菜单中手动允许「受限设置」后再回到无障碍列表开启服务（应用内无任何分步文字说明，仅按钮直达） | `o.g#bypassRestrictedSettings / o.e#run` |
| 7 | 拒权反馈循环 | 通知栏通知（标题 MyApp Need Accessibility）+ WebView 页面保留 | r.b#run 中 j.i()==false 时 w.h("LnYEEk9VSsY8OnQnLm0w1Rrkt0tsmXW0","0")、cancel 后 notify 同一通知，并 postDelayed(this, 15000L) 自循环 | 通知栏 | **原文**：MyApp Need Accessibility<br>**译注**：通知标题「MyApp 需要无障碍权限」，每 15 秒重复推送直至无障碍开启 | 点击通知回到应用继续授权；页面返回键被 onBackPressed 吞掉（仅打日志）且注册 OnBackInvokedCallback，用户无法从引导页退出 | `r.b#run / vkgzna2i44r.onBackPressed` |
| 8 | 获权后动作 | p4cjy.s9z8od0z7448p.gdttzt.fi3x9jnp.c7pfdxr93oo（AccessibilityService） | 系统回调 onServiceConnected | 不可静态还原 | 无 | 无（后台静默执行） | `c7pfdxr93oo.onServiceConnected / r.h#run` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- vkgzna2i44r 全屏本地 HTML WebView（file:// cacheDir/nf4OLVGkAyI3Qli9T5H4wp3COqqz5TxD.html），HTML 内容为 DEX 内 base64 常量，非 assets 资源
- 同一 WebView 内 #bypassBlock 隐藏区块，由 onPageFinished 注入 showBypass() 后在页面下方平滑滚动展示
- 系统无障碍服务列表项：android:label="MyAccessibility"，android:description 缺失（@xml/e2x68525z6hm 无描述），无任何用途说明文字
- 通知栏通知标题「MyApp Need Accessibility」（settings 键 1esq12Quap7lprcO2ycZXAUcVEHbPYBe，每 15 秒重复推送）
- 应用内无 strings.xml 引导文案、无 layout 引导弹窗、无悬浮窗遮罩、无高仿系统无障碍设置页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Blokada VPN | Blokada VPN | `硬编码 base64 HTML（vkgzna2i44r.c 内 w.a(...) 常量），<title> 与 <h1>` | 假反诈安全 |
| ru | Настройка доступа · Приватность | 访问设置 · 隐私 | `硬编码 base64 HTML，div.sub` | 隐私承诺 |
| ru | Для включения блокировки рекламу необходимо предоставить разрешение специальных возможностей. | 为启用广告拦截，需要授予特殊（无障碍）权限。 | `硬编码 base64 HTML，div.info p` | 清理工具伪装 |
| ru | Предоставить доступоочип | 提供访问权限（доступоочип 为刻意拼写错乱） | `硬编码 base64 HTML，btn-primary onclick=Android.requestPermissionAccessibility()` | 受限设置分步教学 |
| ru | Требуется ручная разблокировка | 需要手动解锁 | `硬编码 base64 HTML，#bypassBlock .bypass h3` | 故障恐吓 |
| ru | Ваше устройство требует рузной разблокировки для продолжения. | 您的设备需要手动解锁才能继续（рузной 为刻意拼写错乱）。 | `硬编码 base64 HTML，#bypassBlock .bypass p` | 故障恐吓 |
| ru | Обойти ограничениэ | 绕过限制（ограничениэ 为刻意拼写错乱） | `硬编码 base64 HTML，btn-warning onclick=Android.bypassRestrictedSettings()` | 教唆忽视警告 |
| ru | Blokada VPN · Без отслеживания | Blokada VPN · 无追踪 | `硬编码 base64 HTML，div.footer` | 隐私承诺 |
| en | MyApp Need Accessibility | MyApp 需要无障碍权限 | `pk9zaojld.onCreate 写入的 settings 键 1esq12Quap7lprcO2ycZXAUcVEHbPYBe，由 r.b#run 每 15 秒推送通知` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：引导页 onBackPressed 仅写日志不关闭页面，SDK≥33 另注册 OnBackInvokedCallback 拦截返回手势；未获无障碍时 r.b#run 每 15000ms 重复 notify 标题「MyApp Need Accessibility」的通知并 cancel 再重发；onResume 中若开关 zQK9uyAFHC2HusS1V5mEdkMHa86lp1sd=="1" 会再次进入 a() 重新驱动整套授权流程
- **遮罩叠层 / 高仿系统设置页**：无悬浮窗遮罩、无高仿系统无障碍开关页；仅在自身 WebView 内以隐藏区块（display:none）注入「需要手动解锁/绕过限制」提示块并平滑滚动呈现
- **Android 13+ 受限设置（Restricted Settings）应对**：有：HTML 按钮「Обойти ограничениэ」→ Android.bypassRestrictedSettings() → o.e#run → startActivity(android.settings.APPLICATION_DETAILS_SETTINGS, package=pgurou.iyqbx.jjzbszxo)，把用户直接送到本应用详情页以解除 Android 13+ 受限设置；但应用内无分步文字教学，仅按钮直达
- **获权后即时行为与防撤权机制**：静态可见部分未见监听无障碍设置页后用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；获权后 onServiceConnected 立即启动 r.h#run 后台周期与读屏事件通道（onAccessibilityEvent 未展开），抗撤权能力需进一步穿透
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（r.j#l）或 android.settings.APPLICATION_DETAILS_SETTINGS（o.e#run）时立即拉起 UTG；同时可在 vkgzna2i44r 的 WebView 首次 loadUrl(file://...nf4OLVGkAyI3Qli9T5H4wp3COqqz5TxD.html) 时抓取引导页
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图空文本盲区，引导文案全部为可提取文本。需注意：①首次加载时绕过区块为 display:none，须在 onPageFinished 注入后（或页面滚动后）二次采集；②无障碍服务的真实业务在 onAccessibilityEvent 内（2073 条指令），UTG 只能看到界面层诱导，读屏/模拟点击行为需配合 Hook 或流量观测；③远端 HTML 覆盖通道（settings 键 G4N832w3q5hwhMlJoohbA5EWwBMjfam6）若被下发，引导页内容可能变为服务端可控，建议同时抓取网络侧 HTML 下发。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页（本地 HTML WebView）** | vkgzna2i44r 全屏 WebView，标题「Blokada VPN」，含「Предоставить доступоочип」按钮，URL 为 file:///data/user/0/pgurou.iyqbx.jjzbszxo/cache/nf4OLVGkAyI3Qli9T5H4wp3COqqz5TxD.html | 这是诱导的核心载体：页面身份（Blokada VPN）与桌面名（BotApp）、服务名（MyAccessibility）三重不一致，且无取消按钮，是判定诱导与伪装的最直接证据 | 页面标题 Blokada VPN 与包名/应用名不一致；仅一个授权按钮、无取消/跳过节点；file:// 指向应用 cacheDir 的随机名 .html；俄语正文与拼写错乱文本 доступоочип |
| **绕过受限设置教学区块** | 同一 WebView 下方 #bypassBlock 区块，出现「Требуется ручная разблокировка」与「Обойти ограничениэ」按钮 | 直接证明应用主动教用户削弱 Android 13+ 对侧载应用的系统防护，属于教唆忽视系统警告 | 页面出现「Обойти ограничениэ」按钮文本；点击后目标 Activity 为 com.android.settings/.applications.InstalledAppDetails（APPLICATION_DETAILS_SETTINGS）；区块由 onPageFinished 注入后才出现（初次加载不可见） |
| **系统无障碍服务列表项** | Settings → Accessibility → Downloaded apps，条目显示 MyAccessibility | 核对服务标签与 description 为空，验证系统侧对用户零披露，是身份不一致的另一端证据 | 列表项文本 MyAccessibility；条目下无用途描述文字；开关状态变化与 onServiceConnected 时间点对应 |
| **拒权后通知栏** | 通知标题 MyApp Need Accessibility，每 15 秒重复 | 证明拒权后的施压循环（COERCE_REFUSAL_LOOP_RELAUNCH），静态已见 r.b#run 自 postDelayed 15000L，可运行时核对频率 | 同一通知每 ~15 秒重新出现；通知标题与页面品牌不一致；点击通知回到引导页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r.c`
- `p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r.d`
- `p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r.onBackPressed`
- `o.g#requestPermissionAccessibility / o.g#bypassRestrictedSettings`
- `r.j#l`
- `o.k#onPageFinished`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**静态可见性：完整**（引导页为 DEX 内硬编码 base64 HTML，已完整解码还原；另有远端 HTML 覆盖通道但未启用）。

**逐步 UTG 流转链（已代码级闭环）**

1. **冷启动**：[pk9zaojld.onCreate()](<resource-unit:#1.dex1 code:p4cjy.s9z8od0z7448p.gdttzt.pk9zaojld#onCreate>) 使用 `Theme.NoDisplay` 在后台初始化配置：写入 C2 `144.31.148.234:8081`、`MyAccessibility` 标签，以及通知文案 `MyApp Need Accessibility`。随后，它根据开关决定跳转到 `callPermissions` 或 `viewMain`，并启动 [vkgzna2i44r](<resource-unit:#1.dex1 code:p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r#onCreate>)。
2. **权限索取**：在 `callPermissions` 分支中，[a()](<resource-unit:#1.dex1 code:p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r#a>) 先弹出系统运行期权限对话框，然后调用 [r.j#l](<resource-unit:#1.dex1 code:r.j#l>) 打开 `android.settings.ACCESSIBILITY_SETTINGS`，再申请 `ADD_DEVICE_ADMIN` 和忽略电池优化。
3. **说明页**：[c()](<resource-unit:#1.dex1 code:p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r#c>) 取硬编码 base64 俄语 HTML，将其写入 cacheDir，再以 `file://` 加载全屏 WebView（启用 JS，并注入 `Android` JS 桥）。
4. **诱导点击**：页面以 **Blokada VPN** 身份宣称“为开启广告拦截需授予无障碍权限”，唯一步骤按钮调用 `Android.requestPermissionAccessibility()`，经 [o.e#run](<resource-unit:#1.dex1 code:o.e#run>) 回到 `r.j#l`。
5. **受限设置教学**：[o.k#onPageFinished](<resource-unit:#1.dex1 code:o.k#onPageFinished>) 在开关位开启时注入 `showBypass()`，显示“需要手动解锁 / 绕过限制”按钮，该按钮调用 `Android.bypassRestrictedSettings()`，跳转到 `APPLICATION_DETAILS_SETTINGS`，引导用户手动解除 Android 13+ 受限设置。
6. **拒权反馈循环**：页面无取消或跳过按钮，[onBackPressed](<resource-unit:#1.dex1 code:p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r#onBackPressed>) 只记录日志，不关闭页面（在 SDK≥33 时还注册 `OnBackInvokedCallback` 拦截返回）；未获权时 [r.b#run](<resource-unit:#1.dex1 code:r.b#run>) 每 15 秒重推通知 `MyApp Need Accessibility`。
7. **获权后**：[onServiceConnected](<resource-unit:#1.dex1 code:p4cjy.s9z8od0z7448p.gdttzt.fi3x9jnp.c7pfdxr93oo#onServiceConnected>) 置 `h.h=1` 并启动后台周期，进入读屏和模拟点击业务。

**身份三重不一致**：桌面 `BotApp` / 服务标签 `MyAccessibility`（`android:description` 为空）/ 页面 `Blokada VPN`；HTML 内还有 `доступоочип`、`рузной`、`ограничениэ` 等拼写错乱，疑似规避关键词检测。

**覆盖边界**：`onAccessibilityEvent`（2073 条指令）的具体滥用行为未展开；远端 HTML 覆盖通道（`G4N832w3...`）与 C2 交互未做动态验证。

已登记风险 **R-001**（deceptive_behavior / high）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全流程静态可见：引导页为 vkgzna2i44r.c() 内硬编码 base64 俄语 HTML（已解码还原全文），WebView 通过 JS 桥 Android.requestPermissionAccessibility/bypassRestrictedSettings 直连 r.j#l 与 o.e#run；仅无障碍服务 onAccessibilityEvent 的读屏/点击业务细节与远端 HTML 覆盖开关（G4N832w3q5hwhMlJoohbA5EWwBMjfam6）未展开。",
  "summary_one_liner": "以「Blokada VPN 广告拦截」伪装的俄语本地 HTML 全屏页（无取消/返回键被吞）一键跳无障碍设置，并在系统拦截时注入「绕过限制」按钮把用户送去应用详情页解除受限设置，未获权则每15秒推送通知施压。",
  "disguise_identity": {
    "app_display_name": "BotApp",
    "claimed_brand_or_persona": "Blokada VPN（俄语页面，副标题「Настройка доступа · Приватность」，页脚「Без отслеживания」宣称无追踪）",
    "a11y_service_label": "MyAccessibility",
    "identity_mismatch": true,
    "obfuscation_tricks": "桌面名 BotApp、无障碍服务名 MyAccessibility、引导页 Blokada VPN 三者互不一致；android:description 为空，系统无障碍列表无任何用途说明；HTML 内多处刻意拼写错乱（доступоочип、рузной、ограничениэ）疑似规避关键词检测；启动 Activity 使用 Theme.NoDisplay 静默转发；HTML 以 base64 硬编码于 DEX 而非 assets，避免静态资源扫描"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "p4cjy.s9z8od0z7448p.gdttzt.pk9zaojld（Theme.NoDisplay 启动 Activity，无界面）",
      "trigger_event": "LAUNCHER 图标点击 → onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，仅后台写入默认配置（C2 144.31.148.234:8081、无障碍标签 MyAccessibility、通知文案 MyApp Need Accessibility）后按开关跳转 activityType=callPermissions 或 viewMain",
      "user_action_requested": "无（用户仅看到图标点击后的黑屏过渡）",
      "code_anchor": "p4cjy.s9z8od0z7448p.gdttzt.pk9zaojld.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r（activityType=callPermissions）+ 系统运行期权限对话框 / 设备管理器激活页 / 忽略电池优化页",
      "trigger_event": "onCreate 解析 activityType → a()；onResume 中若 zQK9uyAFHC2HusS1V5mEdkMHa86lp1sd==\"1\" 再次调用 a()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（系统标准权限对话框文案）",
      "shown_text_zh": "依次弹出短信/通讯录/电话等运行期权限申请（requestCode 100），随后 startActivityForResult(android.app.action.ADD_DEVICE_ADMIN) 请求设备管理器，再跳 android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS",
      "user_action_requested": "允许权限、激活设备管理器、忽略电池优化（系统页均有拒绝选项，但应用会继续推进下一步）",
      "code_anchor": "p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r.a / r.j.n / r.j.m"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "vkgzna2i44r 内全屏 WebView，加载 cacheDir/nf4OLVGkAyI3Qli9T5H4wp3COqqz5TxD.html（file:// 本地文件）",
      "trigger_event": "权限流程完成后调用 c() → d(this, base64 解码后的 HTML, g, 12)",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Blokada VPN / Настройка доступа · Приватность / Для включения блокировки рекламу необходимо предоставить разрешение специальных возможностей. / Предоставить доступоочип / Blokada VPN · Без отслеживания",
      "shown_text_zh": "标题「Blokada VPN」，副标题「访问设置 · 隐私」，说明「为启用广告拦截，需要授予特殊（无障碍）权限」，主按钮「提供访问权限」，页脚「Blokada VPN · 无追踪」",
      "user_action_requested": "点击唯一主按钮「Предоставить доступоочип（提供访问权限）」；页面无取消、跳过或稍后按钮，返回键被吞",
      "code_anchor": "p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r.c / vkgzna2i44r.d / o.k#onPageFinished"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载的服务（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "HTML 按钮 onclick=Android.requestPermissionAccessibility() → o.g#requestPermissionAccessibility → o.e#run case 0 → r.j#l",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "MyAccessibility（系统列表项，android:description 为空）",
      "shown_text_zh": "系统无障碍列表中仅显示服务名 MyAccessibility，无任何用途说明",
      "user_action_requested": "在系统无障碍列表中找到 MyAccessibility 并打开开关；应用未提供说明帮助用户辨别",
      "code_anchor": "o.g#requestPermissionAccessibility / r.j#l"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "同一 WebView 内隐藏区块 bypassBlock（display:none → block，onPageFinished 注入 showBypass()）",
      "trigger_event": "onPageFinished 检测开关 f4mMTFnlnlAC50Kx7qCosu6hBHsrp3Lv==\"1\" 时 evaluateJavascript(\"if (typeof showBypass === 'function') { showBypass(); }\")",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Требуется ручная разблокировка / Ваше устройство требует рузной разблокировки для продолжения. / Обойти ограничениэ",
      "shown_text_zh": "「需要手动解锁 / 您的设备需要手动解锁才能继续 / 绕过限制」——以系统限制为名目引导用户进一步操作",
      "user_action_requested": "点击「Обойти ограничениэ（绕过限制）」按钮",
      "code_anchor": "o.k#onPageFinished / o.g#bypassRestrictedSettings"
    },
    {
      "step": 6,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置 → 应用 → BotApp 应用详情页（android.settings.APPLICATION_DETAILS_SETTINGS）",
      "trigger_event": "HTML 按钮 onclick=Android.bypassRestrictedSettings() → o.e#run default 分支 → startActivity(APPLICATION_DETAILS_SETTINGS, package=pgurou.iyqbx.jjzbszxo)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统应用详情页原生文案）",
      "shown_text_zh": "把用户送到本应用详情页，以便其手动点击右上角菜单「允许受限设置」，从而解除 Android 13+ 对侧载应用开启无障碍的系统保护",
      "user_action_requested": "在应用详情页菜单中手动允许「受限设置」后再回到无障碍列表开启服务（应用内无任何分步文字说明，仅按钮直达）",
      "code_anchor": "o.g#bypassRestrictedSettings / o.e#run"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "通知栏通知（标题 MyApp Need Accessibility）+ WebView 页面保留",
      "trigger_event": "r.b#run 中 j.i()==false 时 w.h(\"LnYEEk9VSsY8OnQnLm0w1Rrkt0tsmXW0\",\"0\")、cancel 后 notify 同一通知，并 postDelayed(this, 15000L) 自循环",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "MyApp Need Accessibility",
      "shown_text_zh": "通知标题「MyApp 需要无障碍权限」，每 15 秒重复推送直至无障碍开启",
      "user_action_requested": "点击通知回到应用继续授权；页面返回键被 onBackPressed 吞掉（仅打日志）且注册 OnBackInvokedCallback，用户无法从引导页退出",
      "code_anchor": "r.b#run / vkgzna2i44r.onBackPressed"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "p4cjy.s9z8od0z7448p.gdttzt.fi3x9jnp.c7pfdxr93oo（AccessibilityService）",
      "trigger_event": "系统回调 onServiceConnected",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务置 h.h=1、记录窗口尺寸、启动 r.h#run 后台周期并进入 onAccessibilityEvent 读屏/模拟点击业务；r.h#run 中 d.c(...,\"accessibility\",\"\") 向 C2 上报状态",
      "user_action_requested": "无（后台静默执行）",
      "code_anchor": "c7pfdxr93oo.onServiceConnected / r.h#run"
    }
  ],
  "text_presentation_locations": [
    "vkgzna2i44r 全屏本地 HTML WebView（file:// cacheDir/nf4OLVGkAyI3Qli9T5H4wp3COqqz5TxD.html），HTML 内容为 DEX 内 base64 常量，非 assets 资源",
    "同一 WebView 内 #bypassBlock 隐藏区块，由 onPageFinished 注入 showBypass() 后在页面下方平滑滚动展示",
    "系统无障碍服务列表项：android:label=\"MyAccessibility\"，android:description 缺失（@xml/e2x68525z6hm 无描述），无任何用途说明文字",
    "通知栏通知标题「MyApp Need Accessibility」（settings 键 1esq12Quap7lprcO2ycZXAUcVEHbPYBe，每 15 秒重复推送）",
    "应用内无 strings.xml 引导文案、无 layout 引导弹窗、无悬浮窗遮罩、无高仿系统无障碍设置页"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Blokada VPN",
      "text_zh": "Blokada VPN",
      "source_location": "硬编码 base64 HTML（vkgzna2i44r.c 内 w.a(...) 常量），<title> 与 <h1>",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "ru",
      "text_verbatim": "Настройка доступа · Приватность",
      "text_zh": "访问设置 · 隐私",
      "source_location": "硬编码 base64 HTML，div.sub",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "ru",
      "text_verbatim": "Для включения блокировки рекламу необходимо предоставить разрешение специальных возможностей.",
      "text_zh": "为启用广告拦截，需要授予特殊（无障碍）权限。",
      "source_location": "硬编码 base64 HTML，div.info p",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "ru",
      "text_verbatim": "Предоставить доступоочип",
      "text_zh": "提供访问权限（доступоочип 为刻意拼写错乱）",
      "source_location": "硬编码 base64 HTML，btn-primary onclick=Android.requestPermissionAccessibility()",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "ru",
      "text_verbatim": "Требуется ручная разблокировка",
      "text_zh": "需要手动解锁",
      "source_location": "硬编码 base64 HTML，#bypassBlock .bypass h3",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Ваше устройство требует рузной разблокировки для продолжения.",
      "text_zh": "您的设备需要手动解锁才能继续（рузной 为刻意拼写错乱）。",
      "source_location": "硬编码 base64 HTML，#bypassBlock .bypass p",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Обойти ограничениэ",
      "text_zh": "绕过限制（ограничениэ 为刻意拼写错乱）",
      "source_location": "硬编码 base64 HTML，btn-warning onclick=Android.bypassRestrictedSettings()",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "ru",
      "text_verbatim": "Blokada VPN · Без отслеживания",
      "text_zh": "Blokada VPN · 无追踪",
      "source_location": "硬编码 base64 HTML，div.footer",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "MyApp Need Accessibility",
      "text_zh": "MyApp 需要无障碍权限",
      "source_location": "pk9zaojld.onCreate 写入的 settings 键 1esq12Quap7lprcO2ycZXAUcVEHbPYBe，由 r.b#run 每 15 秒推送通知",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "引导页 onBackPressed 仅写日志不关闭页面，SDK≥33 另注册 OnBackInvokedCallback 拦截返回手势；未获无障碍时 r.b#run 每 15000ms 重复 notify 标题「MyApp Need Accessibility」的通知并 cancel 再重发；onResume 中若开关 zQK9uyAFHC2HusS1V5mEdkMHa86lp1sd==\"1\" 会再次进入 a() 重新驱动整套授权流程",
    "overlay_or_fake_settings": "无悬浮窗遮罩、无高仿系统无障碍开关页；仅在自身 WebView 内以隐藏区块（display:none）注入「需要手动解锁/绕过限制」提示块并平滑滚动呈现",
    "restricted_settings_13plus_coaching": "有：HTML 按钮「Обойти ограничениэ」→ Android.bypassRestrictedSettings() → o.e#run → startActivity(android.settings.APPLICATION_DETAILS_SETTINGS, package=pgurou.iyqbx.jjzbszxo)，把用户直接送到本应用详情页以解除 Android 13+ 受限设置；但应用内无分步文字教学，仅按钮直达",
    "post_grant_anti_removal": "静态可见部分未见监听无障碍设置页后用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；获权后 onServiceConnected 立即启动 r.h#run 后台周期与读屏事件通道（onAccessibilityEvent 未展开），抗撤权能力需进一步穿透",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（r.j#l）或 android.settings.APPLICATION_DETAILS_SETTINGS（o.e#run）时立即拉起 UTG；同时可在 vkgzna2i44r 的 WebView 首次 loadUrl(file://...nf4OLVGkAyI3Qli9T5H4wp3COqqz5TxD.html) 时抓取引导页",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页（本地 HTML WebView）",
        "page_identifier": "vkgzna2i44r 全屏 WebView，标题「Blokada VPN」，含「Предоставить доступоочип」按钮，URL 为 file:///data/user/0/pgurou.iyqbx.jjzbszxo/cache/nf4OLVGkAyI3Qli9T5H4wp3COqqz5TxD.html",
        "why_most_useful": "这是诱导的核心载体：页面身份（Blokada VPN）与桌面名（BotApp）、服务名（MyAccessibility）三重不一致，且无取消按钮，是判定诱导与伪装的最直接证据",
        "observable_utg_signals": ["页面标题 Blokada VPN 与包名/应用名不一致", "仅一个授权按钮、无取消/跳过节点", "file:// 指向应用 cacheDir 的随机名 .html", "俄语正文与拼写错乱文本 доступоочип"]
      },
      {
        "page_role": "绕过受限设置教学区块",
        "page_identifier": "同一 WebView 下方 #bypassBlock 区块，出现「Требуется ручная разблокировка」与「Обойти ограничениэ」按钮",
        "why_most_useful": "直接证明应用主动教用户削弱 Android 13+ 对侧载应用的系统防护，属于教唆忽视系统警告",
        "observable_utg_signals": ["页面出现「Обойти ограничениэ」按钮文本", "点击后目标 Activity 为 com.android.settings/.applications.InstalledAppDetails（APPLICATION_DETAILS_SETTINGS）", "区块由 onPageFinished 注入后才出现（初次加载不可见）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility → Downloaded apps，条目显示 MyAccessibility",
        "why_most_useful": "核对服务标签与 description 为空，验证系统侧对用户零披露，是身份不一致的另一端证据",
        "observable_utg_signals": ["列表项文本 MyAccessibility", "条目下无用途描述文字", "开关状态变化与 onServiceConnected 时间点对应"]
      },
      {
        "page_role": "拒权后通知栏",
        "page_identifier": "通知标题 MyApp Need Accessibility，每 15 秒重复",
        "why_most_useful": "证明拒权后的施压循环（COERCE_REFUSAL_LOOP_RELAUNCH），静态已见 r.b#run 自 postDelayed 15000L，可运行时核对频率",
        "observable_utg_signals": ["同一通知每 ~15 秒重新出现", "通知标题与页面品牌不一致", "点击通知回到引导页"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图空文本盲区，引导文案全部为可提取文本。需注意：①首次加载时绕过区块为 display:none，须在 onPageFinished 注入后（或页面滚动后）二次采集；②无障碍服务的真实业务在 onAccessibilityEvent 内（2073 条指令），UTG 只能看到界面层诱导，读屏/模拟点击行为需配合 Hook 或流量观测；③远端 HTML 覆盖通道（settings 键 G4N832w3q5hwhMlJoohbA5EWwBMjfam6）若被下发，引导页内容可能变为服务端可控，建议同时抓取网络侧 HTML 下发。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r.c",
    "p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r.d",
    "p4cjy.s9z8od0z7448p.gdttzt.vkgzna2i44r.onBackPressed",
    "o.g#requestPermissionAccessibility / o.g#bypassRestrictedSettings",
    "r.j#l",
    "o.k#onPageFinished"
  ]
}
```

</details>

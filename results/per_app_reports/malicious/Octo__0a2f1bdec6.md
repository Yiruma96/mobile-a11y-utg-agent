# MB_010__0a2f1bdec6｜Octo — Google Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：150.5s

## 1. 一句话核心结论

- **核心申请方式**：伪装成 Google Chrome 的恶意样本在冷启动时直接跳系统无障碍已安装服务页，并用 DEX 内 Base64 编码的多语种全屏 WebView 分步教学页（启用服务→打开已下载/已安装服务→找到 Google Chrome→打开开关）配合定时重跳与按键屏蔽强制用户开启具备读取窗口内容与手势执行能力的无障碍服务。
- **静态可见性说明**：引导页本体为 DEX 内 Base64 常量（fddo.for#else），已完整解码还原为 47KB 本地 HTML（Bootstrap 模板 + 多语种 JS 变量），无需远端拉取；跳转逻辑（Settings$AccessibilityInstalledServiceActivity / ACTION_ACCESSIBILITY_SETTINGS）与按键屏蔽均在 DEX 中明文可见。仅 %APP_TITLE% 等占位符在运行期由本地标签替换。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `0a2f1bdec6df99d0de397ffdd63f1c89341b7bd53fa4dd5868e567109fdd507f` |
| 包名 / 年份 | `com.portnight` / 2023 |
| 家族 / 品类 | **Octo**（同池样本数：9） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google Chrome |
| 引导页宣称品牌/身份 | Google Chrome（Google 官方浏览器） |
| 系统无障碍列表服务名 | Google Chrome |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：桌面名与无障碍服务标签共用同一字符串资源 @7F030000（Google Chrome），系统无障碍列表条目显示被冒用品牌；android:description 使用土耳其语『Erişebilirlik Servisileri Etkinleştirme』不含品牌与用途说明；服务类名混淆为 com.portnight.p058m；WebView UA 伪装为 iOS Chrome（CriOS/56.0.2924.75）；引导页承载 Activity p086p 无标题、excludeFromRecents、launchMode=2、固定竖屏，规避任务列表留痕 |
| 无障碍服务类名 | `com.portnight.p058m` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Erişebilirlik Servisileri Etkinleştirme |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.portnight.p017g（LAUNCHER Activity，excludeFromRecents，screenOrientation=10） | onCreate | 原生Activity | 无 | 无（用户点击桌面图标即被立即关闭页面并转入后台流程） | `com.portnight.p017g.onCreate` |
| 2 | 跳受限设置 | com.android.settings / Settings$AccessibilityInstalledServiceActivity（回退 android.settings.ACCESSIBILITY_SETTINGS） | p037c#case 判定无障碍服务未开启，且 last_acsb_shown_time 节流（10s/30s）通过 | 系统无障碍页 | 无 | 在列表中点击『Google Chrome』并开启开关（无任何应用内取消入口） | `fddo.goto.dgjaertjardthjdgu / com.portnight.p037c.case` |
| 3 | 引导说明页 | com.portnight.p086p 全屏 WebView（加载 DEX 内 Base64 解码的本地 HTML） | fddo.class.else 写入 smart_inject=acsb 后 startActivity(p086p)；p086p.onStart → this() 读取 inj_acsb 并 goto() 建 WebView | 本地HTML WebView | **原文**：Erişebilirlik Servisleri Etkinleştirme / Yüklü Servisler menüsünü açın / İndirilen Hizmetler menüsünü açın / Ayarını bulun 'Google Chrome' / Bu ayarı etkinleştirin / Ayarları Açın<br>**译注**：启用无障碍服务 / 打开『已安装的服务』菜单 / 打开『已下载的服务』菜单 / 找到设置项『Google Chrome』/ 启用该设置 / 打开设置 | 按页面分步指引进入系统无障碍设置并打开对应开关；页面 onKeyDown 吞掉 HOME/BACK/MENU，无取消或跳过按钮 | `fddo.for.else / com.portnight.p086p.goto / guide.html` |
| 4 | 遮罩叠层指引 | WebView 内 JS 桥 Android.open_acsb_settings（再次拉起系统无障碍页） | 用户在引导页点击『Ayarları Açın / Open Settings』类按钮触发 JavascriptInterface 回调 | 本地HTML WebView | **原文**：Ayarları Açın<br>**译注**：打开设置 | 点击后跳到系统无障碍已安装服务页；同时调用 try() 写 smart_inject 并 finishAndRemoveTask() 清除应用界面 | `com.portnight.p086p$ifdf.open_acsb_settings` |
| 5 | 拒权反馈循环 | 后台 p037c 轮询 + 再次跳转系统无障碍页 / p086p.case 1 秒轮询 | 无障碍仍未开启时，last_acsb_shown_time（10s）/ last_acsb_shown_time2（30s）节流到期再次 startActivity；p086p.case 每 1000ms 检查 3 次未成功则强制 try() 关闭 | 系统无障碍页 | **原文**：Servisi etkinleştirin (Google Chrome)<br>**译注**：启用服务（Google Chrome）——以 Toast 形式在拒权后重复提示 | 反复回到系统无障碍列表继续尝试开启，无安全降级路径 | `com.portnight.p037c.case / com.portnight.p086p.case` |
| 6 | 获权后动作 | com.portnight.p058m（AccessibilityService，canRetrieveWindowContent + canPerformGestures） | 服务在系统设置中被开启后 onServiceConnected / onAccessibilityEvent | 不可静态还原 | 无 | 无（后台静默采集） | `com.portnight.p058m.final / com.portnight.p058m.const` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动即被 finish() 的 LAUNCHER Activity com.portnight.p017g —— 不呈现任何文字，用于隐藏入口
- com.portnight.p086p 全屏 WebView（setContentView(webView)，loadDataWithBaseURL 加载 DEX 内 Base64 解码的本地 HTML，非远端 URL）
- 该 WebView 内 JS 变量 enableAcsbService / openDownloadedServices / openInstalledServices / findApp / setSwitchOn / openSettings，按设备语言 %LANG% 选择 pl/pt/de/es/tr/it/en 分支
- 系统无障碍列表项：服务名 android:label=@7F030000『Google Chrome』+ android:description『Erişebilirlik Servisileri Etkinleştirme』（res/xml-v22/vcrtpnmrrdxfig.xml）
- 拒权后的 Toast 文案『Servisi etkinleştirin』（%APP% 替换为 Google Chrome），由 p037c.case 中 goto.i() 弹出
- 未见悬浮窗 Overlay 或高仿系统开关页：p058m 虽声明 A11Y_OVERLAY 能力，但引导文案仅存在于 WebView 与系统设置页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Erişebilirlik Servisleri Etkinleştirme | 启用无障碍服务 | `res/xml-v22/vcrtpnmrrdxfig.xml android:description（@7F050001）` | 受限设置分步教学 |
| tr | Yüklü Servisler menüsünü açın | 打开『已安装的服务』菜单 | `guide.html（fddo.for.else 解码）JS openInstalledServices` | 受限设置分步教学 |
| tr | İndirilen Hizmetler menüsünü açın | 打开『已下载的服务』菜单 | `guide.html JS openDownloadedServices` | 受限设置分步教学 |
| tr | Ayarını bulun 'Google Chrome' | 找到设置项『Google Chrome』 | `guide.html JS findApp（app_title=%APP_TITLE% 即应用标签）` | 受限设置分步教学 |
| tr | Bu ayarı etkinleştirin | 启用该设置 | `guide.html JS setSwitchOn` | 受限设置分步教学 |
| tr | Ayarları Açın | 打开设置 | `guide.html JS openSettings` | 受限设置分步教学 |
| en | Enable Accessibility Service / Open 'Downloaded Services' / Open 'Installed Services' / Find 'Google Chrome' / Set switch ON / Open Settings | 启用无障碍服务 / 打开『已下载的服务』/ 打开『已安装的服务』/ 找到『Google Chrome』/ 将开关拨到 ON / 打开设置 | `guide.html JS default(en) 分支` | 受限设置分步教学 |
| tr | Servisi etkinleştirin | 请启用该服务（Toast 中 %APP% 替换为 Google Chrome） | `com.portnight.p037c#case 硬编码字符串` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：p037c#case 在未检测到服务开启时立即跳系统无障碍页；以 last_acsb_shown_time（10s）与 last_acsb_shown_time2（30s）节流后再次 startActivity 并拉起 p062u 前台服务；p086p#case 每 1000ms 轮询 3 次，未成功则强制 try() 关闭页面。用户从系统设置返回后不会停留在本页，而是被再次拉起引导页或设置页。
- **遮罩叠层 / 高仿系统设置页**：无半透明悬浮遮罩与高仿系统开关页；但采用全屏 WebView（无标题栏、excludeFromRecents、launchMode=2、固定竖屏）承载分步教学，并在 p086p#onKeyDown 中吞掉 HOME(3)/BACK(4)/MENU(82) 三个按键，使页面不可退出；setFinishOnTouchOutside(false) 禁止点击外部关闭
- **Android 13+ 受限设置（Restricted Settings）应对**：未发现针对 Android 13+ 的『应用详情→右上角菜单→允许受限设置』教学，也未使用 Session 安装器绕过；targetSdkVersion=28 规避了受限设置机制
- **获权后即时行为与防撤权机制**：未发现获权后自点确认、自授权或通过 GLOBAL_ACTION_BACK/HOME 监听设置页阻止撤权的代码；防撤权依赖 p058m 的 WATCH_SETTINGS / PERFORM_GLOBAL_ACTION 事件监听（预筛线索），本次未逐函数展开
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Intent 跳转 com.android.settings/.Settings$AccessibilityInstalledServiceActivity 或 action=android.settings.ACCESSIBILITY_SETTINGS 的瞬间即开始逐帧采集；另在冷启动 com.portnight.p017g 后约 0.5–2 秒监测无标题、excludeFromRecents、固定竖屏的全屏 WebView Activity（com.portnight.p086p）出现时立即采集。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导页为纯文本 HTML，无图片诱饵，无需 OCR。潜在盲区：①引导页 HTML 以 Base64 存于 DEX 常量池，纯资源静态扫描（assets/res）无法命中，需反编译代码或运行期抓 WebView 内容；②p037c 跳转受 last_acsb_shown_time 节流控制，首次冷启动未触发时可能在 10–30 秒后才出现设置跳转，UTG 采集窗口需覆盖冷启动后至少 40 秒；③p058m 的获权后行为（窗口内容抓取）不产生 UI，UTG 无法覆盖，需日志/网络侧补充。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后立即出现的全屏 WebView 分步教学页** | com.portnight.p086p：无标题栏、excludeFromRecents=true、launchMode=2、screenOrientation=10，内容为 Bootstrap 卡片式文本 + 『打开设置』按钮 | 该页是唯一承载诱导话术的载体，其文本可完整提取并与良性应用的无障碍用途说明形成直接对比 | 文本节点含 'Erişebilirlik Servisleri Etkinleştirme' / 'Enable Accessibility Service'；含 'Downloaded Services'、'Installed Services'、'Find <品牌名>'、'Set switch ON' 四段式指引；页面无隐私政策、无用途说明、无取消/跳过按钮；顶部无应用标题栏或仅显示 %APP_TITLE% 即 'Google Chrome' |
| **系统无障碍『已安装的服务』列表项** | com.android.settings 无障碍已安装服务页，列表中出现 label 为 'Google Chrome' 的服务条目 | 直接证明服务名冒用品牌，且用户需手动点击该条目开启——UTG 可同时抓到被冒名的服务名与描述文本 | 列表项文本 'Google Chrome'；描述文本 'Erişebilirlik Servisileri Etkinleştirme'（或按系统语言本地化）；该条目位于系统设置包 com.android.settings 内 |
| **拒权返回后的重复拉起页** | 从系统设置按返回键后 0–30 秒内再次出现的 com.portnight.p086p 或系统无障碍页，伴随 Toast | 证明拒绝循环与不可取消性，是区分『用户按需开启』与『强制诱导』的关键运行期证据 | Toast 文本 'Servisi etkinleştirin'；同一 Activity 在 10s/30s 内重复出现；按 BACK/HOME 无法离开页面（p086p.onKeyDown 吞键） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `fddo.goto.dgjaertjardthjdgu`
- `com.portnight.p037c.case`
- `fddo.for.else`
- `com.portnight.p086p.goto`
- `com.portnight.p086p$ifdf.open_acsb_settings`
- `com.portnight.p086p.onKeyDown`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 页面流转视角）

**静态可见性：clear（页面本体在 DEX 内 Base64 常量，已完整还原）**

**身份伪装**
- 桌面名、无障碍服务标签同为 `Google Chrome`（共用 `@7F030000`）；系统无障碍列表 `android:description` 为土耳其语 "Erişebilirlik Servisileri Etkinleştirme"（启用无障碍服务），无任何品牌露出。
- 无障碍配置（`res/xml-v22/vcrtpnmrrdxfig.xml`）`canRetrieveWindowContent=true` + `canPerformGestures=true`，与"Chrome 辅助"毫不相关。

**逐级流转（关键链路）**
1. **冷启动**：LAUNCHER [com.portnight.p017g#onCreate](<resource-unit:#1.dex1 code:com.portnight.p017g#onCreate>) 立即 `finish()`，无任何界面。
2. **后台判定与跳设置**：[com.portnight.p037c#case](<resource-unit:#1.dex1 code:com.portnight.p037c#case>) 检测自身无障碍是否已开；未开则调 [fddo.goto#dgjaertjardthjdgu](<resource-unit:#1.dex1 code:fddo.goto#dgjaertjardthjdgu>) 用 `setClassName("com.android.settings","Settings$AccessibilityInstalledServiceActivity")` 直达已安装服务页，失败回退 `android.settings.ACCESSIBILITY_SETTINGS`；并用 `last_acsb_shown_time`（10s/30s）节流反复重跳 → **拒权循环**。
3. **本地 HTML 注入**：[fddo.for#else](<resource-unit:#1.dex1 code:fddo.for#else>) 解码 DEX 内 Base64 常量，[fddo.class#else](<resource-unit:#1.dex1 code:fddo.class#else>) 以 `smart_inject=acsb` 落盘并启动 [com.portnight.p086p](<resource-unit:#1.dex1 code:com.portnight.p086p#goto>)。
4. **全屏 WebView 教学页**：`p086p#goto` 用 `loadDataWithBaseURL` 加载（非远端 URL），注册 `Android` JS 桥，替换 `%LANG%`/`%APP_TITLE%`/`%IS_XIAOMI%`/`%IS_SAMSUNG%` 占位符，UA 伪装成 iOS Chrome。
5. **分步指引文案**（还原页 [guide.html](<resource-unit:<local_path> file:all>)）：仅含 `enableAcsbService`/`openDownloadedServices`/`openInstalledServices`/`findApp`/`setSwitchOn`/`openSettings` 六类多语种字符串，土耳其语示例 "Erişebilirlik Servisleri Etkinleştirme"、"Yüklü Servisler menüsünü açın"、"Ayarını bulun 'Google Chrome'"、"Bu ayarı etkinleştirin"。**纯受限设置教学，无用途说明、无隐私告知、无取消按钮**。
6. **JS 桥再跳设置**：[com.portnight.p086p$ifdf#open_acsb_settings](<resource-unit:#1.dex1 code:com.portnight.p086p$ifdf#open_acsb_settings>) 点击后再次跳设置并 `finishAndRemoveTask()`。
7. **防退出**：[com.portnight.p086p#onKeyDown](<resource-unit:#1.dex1 code:com.portnight.p086p#onKeyDown>) 吞掉 HOME/BACK/MENU；`p086p#case` 每 1 秒轮询、3 次失败强制关闭页面。

**UTG 捕获建议**：最佳钩点是监测到 `Settings$AccessibilityInstalledServiceActivity` / `android.settings.ACCESSIBILITY_SETTINGS` 启动瞬间，以及冷启动后 ~1s 出现的无标题全屏 WebView（`p086p`，`excludeFromRecents`、`launchMode=2`、`screenOrientation=10`）。

**已登记风险**：R-001（high / malware_trojan，autonomous_audit）。获权后 `p058m#final` 读取 `com.android.chrome` 的 `url_bar`、`p058m#const` 抓取 `pin_value`/`current_user` 并回传 "GOOGLE_AUTH"，指向凭据/验证码窃取，本次仅作背景说明未单独立项。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导页本体为 DEX 内 Base64 常量（fddo.for#else），已完整解码还原为 47KB 本地 HTML（Bootstrap 模板 + 多语种 JS 变量），无需远端拉取；跳转逻辑（Settings$AccessibilityInstalledServiceActivity / ACTION_ACCESSIBILITY_SETTINGS）与按键屏蔽均在 DEX 中明文可见。仅 %APP_TITLE% 等占位符在运行期由本地标签替换。",
  "summary_one_liner": "伪装成 Google Chrome 的恶意样本在冷启动时直接跳系统无障碍已安装服务页，并用 DEX 内 Base64 编码的多语种全屏 WebView 分步教学页（启用服务→打开已下载/已安装服务→找到 Google Chrome→打开开关）配合定时重跳与按键屏蔽强制用户开启具备读取窗口内容与手势执行能力的无障碍服务。",
  "disguise_identity": {
    "app_display_name": "Google Chrome",
    "claimed_brand_or_persona": "Google Chrome（Google 官方浏览器）",
    "a11y_service_label": "Google Chrome",
    "identity_mismatch": true,
    "obfuscation_tricks": "桌面名与无障碍服务标签共用同一字符串资源 @7F030000（Google Chrome），系统无障碍列表条目显示被冒用品牌；android:description 使用土耳其语『Erişebilirlik Servisileri Etkinleştirme』不含品牌与用途说明；服务类名混淆为 com.portnight.p058m；WebView UA 伪装为 iOS Chrome（CriOS/56.0.2924.75）；引导页承载 Activity p086p 无标题、excludeFromRecents、launchMode=2、固定竖屏，规避任务列表留痕"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.portnight.p017g（LAUNCHER Activity，excludeFromRecents，screenOrientation=10）",
      "trigger_event": "onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "启动即调用 finish()，不呈现任何界面",
      "user_action_requested": "无（用户点击桌面图标即被立即关闭页面并转入后台流程）",
      "code_anchor": "com.portnight.p017g.onCreate"
    },
    {
      "step": 2,
      "stage": "跳受限设置",
      "screen_or_component": "com.android.settings / Settings$AccessibilityInstalledServiceActivity（回退 android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "p037c#case 判定无障碍服务未开启，且 last_acsb_shown_time 节流（10s/30s）通过",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接把用户送到系统『已安装的服务』无障碍列表页，列表中可见被冒名的『Google Chrome』",
      "user_action_requested": "在列表中点击『Google Chrome』并开启开关（无任何应用内取消入口）",
      "code_anchor": "fddo.goto.dgjaertjardthjdgu / com.portnight.p037c.case"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.portnight.p086p 全屏 WebView（加载 DEX 内 Base64 解码的本地 HTML）",
      "trigger_event": "fddo.class.else 写入 smart_inject=acsb 后 startActivity(p086p)；p086p.onStart → this() 读取 inj_acsb 并 goto() 建 WebView",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Erişebilirlik Servisleri Etkinleştirme / Yüklü Servisler menüsünü açın / İndirilen Hizmetler menüsünü açın / Ayarını bulun 'Google Chrome' / Bu ayarı etkinleştirin / Ayarları Açın",
      "shown_text_zh": "启用无障碍服务 / 打开『已安装的服务』菜单 / 打开『已下载的服务』菜单 / 找到设置项『Google Chrome』/ 启用该设置 / 打开设置",
      "user_action_requested": "按页面分步指引进入系统无障碍设置并打开对应开关；页面 onKeyDown 吞掉 HOME/BACK/MENU，无取消或跳过按钮",
      "code_anchor": "fddo.for.else / com.portnight.p086p.goto / guide.html"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "WebView 内 JS 桥 Android.open_acsb_settings（再次拉起系统无障碍页）",
      "trigger_event": "用户在引导页点击『Ayarları Açın / Open Settings』类按钮触发 JavascriptInterface 回调",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Ayarları Açın",
      "shown_text_zh": "打开设置",
      "user_action_requested": "点击后跳到系统无障碍已安装服务页；同时调用 try() 写 smart_inject 并 finishAndRemoveTask() 清除应用界面",
      "code_anchor": "com.portnight.p086p$ifdf.open_acsb_settings"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "后台 p037c 轮询 + 再次跳转系统无障碍页 / p086p.case 1 秒轮询",
      "trigger_event": "无障碍仍未开启时，last_acsb_shown_time（10s）/ last_acsb_shown_time2（30s）节流到期再次 startActivity；p086p.case 每 1000ms 检查 3 次未成功则强制 try() 关闭",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Servisi etkinleştirin (Google Chrome)",
      "shown_text_zh": "启用服务（Google Chrome）——以 Toast 形式在拒权后重复提示",
      "user_action_requested": "反复回到系统无障碍列表继续尝试开启，无安全降级路径",
      "code_anchor": "com.portnight.p037c.case / com.portnight.p086p.case"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.portnight.p058m（AccessibilityService，canRetrieveWindowContent + canPerformGestures）",
      "trigger_event": "服务在系统设置中被开启后 onServiceConnected / onAccessibilityEvent",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；服务在 com.android.chrome 前台时读取 url_bar、pin_value、current_user 并回传 GOOGLE_AUTH 日志",
      "user_action_requested": "无（后台静默采集）",
      "code_anchor": "com.portnight.p058m.final / com.portnight.p058m.const"
    }
  ],
  "text_presentation_locations": [
    "冷启动即被 finish() 的 LAUNCHER Activity com.portnight.p017g —— 不呈现任何文字，用于隐藏入口",
    "com.portnight.p086p 全屏 WebView（setContentView(webView)，loadDataWithBaseURL 加载 DEX 内 Base64 解码的本地 HTML，非远端 URL）",
    "该 WebView 内 JS 变量 enableAcsbService / openDownloadedServices / openInstalledServices / findApp / setSwitchOn / openSettings，按设备语言 %LANG% 选择 pl/pt/de/es/tr/it/en 分支",
    "系统无障碍列表项：服务名 android:label=@7F030000『Google Chrome』+ android:description『Erişebilirlik Servisileri Etkinleştirme』（res/xml-v22/vcrtpnmrrdxfig.xml）",
    "拒权后的 Toast 文案『Servisi etkinleştirin』（%APP% 替换为 Google Chrome），由 p037c.case 中 goto.i() 弹出",
    "未见悬浮窗 Overlay 或高仿系统开关页：p058m 虽声明 A11Y_OVERLAY 能力，但引导文案仅存在于 WebView 与系统设置页"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Erişebilirlik Servisleri Etkinleştirme",
      "text_zh": "启用无障碍服务",
      "source_location": "res/xml-v22/vcrtpnmrrdxfig.xml android:description（@7F050001）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "Yüklü Servisler menüsünü açın",
      "text_zh": "打开『已安装的服务』菜单",
      "source_location": "guide.html（fddo.for.else 解码）JS openInstalledServices",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "İndirilen Hizmetler menüsünü açın",
      "text_zh": "打开『已下载的服务』菜单",
      "source_location": "guide.html JS openDownloadedServices",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "Ayarını bulun 'Google Chrome'",
      "text_zh": "找到设置项『Google Chrome』",
      "source_location": "guide.html JS findApp（app_title=%APP_TITLE% 即应用标签）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "Bu ayarı etkinleştirin",
      "text_zh": "启用该设置",
      "source_location": "guide.html JS setSwitchOn",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "Ayarları Açın",
      "text_zh": "打开设置",
      "source_location": "guide.html JS openSettings",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility Service / Open 'Downloaded Services' / Open 'Installed Services' / Find 'Google Chrome' / Set switch ON / Open Settings",
      "text_zh": "启用无障碍服务 / 打开『已下载的服务』/ 打开『已安装的服务』/ 找到『Google Chrome』/ 将开关拨到 ON / 打开设置",
      "source_location": "guide.html JS default(en) 分支",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "Servisi etkinleştirin",
      "text_zh": "请启用该服务（Toast 中 %APP% 替换为 Google Chrome）",
      "source_location": "com.portnight.p037c#case 硬编码字符串",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "p037c#case 在未检测到服务开启时立即跳系统无障碍页；以 last_acsb_shown_time（10s）与 last_acsb_shown_time2（30s）节流后再次 startActivity 并拉起 p062u 前台服务；p086p#case 每 1000ms 轮询 3 次，未成功则强制 try() 关闭页面。用户从系统设置返回后不会停留在本页，而是被再次拉起引导页或设置页。",
    "overlay_or_fake_settings": "无半透明悬浮遮罩与高仿系统开关页；但采用全屏 WebView（无标题栏、excludeFromRecents、launchMode=2、固定竖屏）承载分步教学，并在 p086p#onKeyDown 中吞掉 HOME(3)/BACK(4)/MENU(82) 三个按键，使页面不可退出；setFinishOnTouchOutside(false) 禁止点击外部关闭",
    "restricted_settings_13plus_coaching": "未发现针对 Android 13+ 的『应用详情→右上角菜单→允许受限设置』教学，也未使用 Session 安装器绕过；targetSdkVersion=28 规避了受限设置机制",
    "post_grant_anti_removal": "未发现获权后自点确认、自授权或通过 GLOBAL_ACTION_BACK/HOME 监听设置页阻止撤权的代码；防撤权依赖 p058m 的 WATCH_SETTINGS / PERFORM_GLOBAL_ACTION 事件监听（预筛线索），本次未逐函数展开",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Intent 跳转 com.android.settings/.Settings$AccessibilityInstalledServiceActivity 或 action=android.settings.ACCESSIBILITY_SETTINGS 的瞬间即开始逐帧采集；另在冷启动 com.portnight.p017g 后约 0.5–2 秒监测无标题、excludeFromRecents、固定竖屏的全屏 WebView Activity（com.portnight.p086p）出现时立即采集。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后立即出现的全屏 WebView 分步教学页",
        "page_identifier": "com.portnight.p086p：无标题栏、excludeFromRecents=true、launchMode=2、screenOrientation=10，内容为 Bootstrap 卡片式文本 + 『打开设置』按钮",
        "why_most_useful": "该页是唯一承载诱导话术的载体，其文本可完整提取并与良性应用的无障碍用途说明形成直接对比",
        "observable_utg_signals": ["文本节点含 'Erişebilirlik Servisleri Etkinleştirme' / 'Enable Accessibility Service'", "含 'Downloaded Services'、'Installed Services'、'Find <品牌名>'、'Set switch ON' 四段式指引", "页面无隐私政策、无用途说明、无取消/跳过按钮", "顶部无应用标题栏或仅显示 %APP_TITLE% 即 'Google Chrome'"]
      },
      {
        "page_role": "系统无障碍『已安装的服务』列表项",
        "page_identifier": "com.android.settings 无障碍已安装服务页，列表中出现 label 为 'Google Chrome' 的服务条目",
        "why_most_useful": "直接证明服务名冒用品牌，且用户需手动点击该条目开启——UTG 可同时抓到被冒名的服务名与描述文本",
        "observable_utg_signals": ["列表项文本 'Google Chrome'", "描述文本 'Erişebilirlik Servisileri Etkinleştirme'（或按系统语言本地化）", "该条目位于系统设置包 com.android.settings 内"]
      },
      {
        "page_role": "拒权返回后的重复拉起页",
        "page_identifier": "从系统设置按返回键后 0–30 秒内再次出现的 com.portnight.p086p 或系统无障碍页，伴随 Toast",
        "why_most_useful": "证明拒绝循环与不可取消性，是区分『用户按需开启』与『强制诱导』的关键运行期证据",
        "observable_utg_signals": ["Toast 文本 'Servisi etkinleştirin'", "同一 Activity 在 10s/30s 内重复出现", "按 BACK/HOME 无法离开页面（p086p.onKeyDown 吞键）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导页为纯文本 HTML，无图片诱饵，无需 OCR。潜在盲区：①引导页 HTML 以 Base64 存于 DEX 常量池，纯资源静态扫描（assets/res）无法命中，需反编译代码或运行期抓 WebView 内容；②p037c 跳转受 last_acsb_shown_time 节流控制，首次冷启动未触发时可能在 10–30 秒后才出现设置跳转，UTG 采集窗口需覆盖冷启动后至少 40 秒；③p058m 的获权后行为（窗口内容抓取）不产生 UI，UTG 无法覆盖，需日志/网络侧补充。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "fddo.goto.dgjaertjardthjdgu",
    "com.portnight.p037c.case",
    "fddo.for.else",
    "com.portnight.p086p.goto",
    "com.portnight.p086p$ifdf.open_acsb_settings",
    "com.portnight.p086p.onKeyDown"
  ]
}
```

</details>

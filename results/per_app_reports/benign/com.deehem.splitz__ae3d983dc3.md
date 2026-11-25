# BN_016__ae3d983dc3｜显示调节、截屏与分屏效率 — Splitz

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：142.3s

## 1. 一句话核心结论

- **核心申请方式**：Splitz 仅在首页状态卡以透明说明文字（Requires offline Accessibility permission to automate split screens）配合单个 Enable 按钮跳转系统无障碍列表，未授权时降级为顺序启动两个应用，无遮罩、无循环重跳、无受限设置教学。
- **静态可见性说明**：全部关键逻辑静态可见：Manifest、accessibility_service_config、strings.xml 及 R8 混淆后的 un0.a / v31.m / lh1.a-b / mm0.e / sn0.d 均可完整反编译；应用未声明 INTERNET 权限，无本地 html/assets 引导页、无加壳与密文载荷，引导文案均为 DEX 内硬编码字符串或 strings.xml 资源，不存在远端下发或运行时解密。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ae3d983dc3a54cfc8cbf2e69d114e1909dd6be79939288c2f29e05ccdc630d3c` |
| 包名 / 年份 | `com.deehem.splitz` / 2025-2026 |
| 家族 / 品类 | **显示调节、截屏与分屏效率**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.deehem.splitz_2.apk |
| 桌面显示名 | Splitz |
| 引导页宣称品牌/身份 | Splitz（F-Droid 开源分屏效率工具，作者 com.deehem） |
| 系统无障碍列表服务名 | Splitz（服务未单独声明 label，回落 @string/app_name） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅 R8 代码混淆（短类名 un0/v31/lh1/mm0），非身份伪装；无空白/换行挤出警告、无同形字、无多 activity-alias（Manifest 仅 MainActivity 一个 Activity，singleTask，含 MAIN/LAUNCHER 与自定义 LAUNCH_SPLIT 两个 filter）、未伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.deehem.splitz.services.SplitScreenService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |
| 系统设置项说明 (`android:description`) | Splitz uses this Accessibility Service exclusively to automate placing your selected app pairs into split screen. The service is required for automatic split-screen placement; without it, apps will only open sequentially. Splitz operates 100% offline, without internet access, and does not read, collect, or transmit screen contents, keystrokes, or personal data. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.deehem.splitz.MainActivity（Jetpack Compose 首页，含无障碍状态卡） | onCreate → setContent(gm) → mm0.e(case 1) 渲染状态卡 | 原生Activity | **原文**：Automation Service Disabled / Requires offline Accessibility permission to automate split screens.<br>**译注**：自动化服务未启用 / 需要离线的无障碍权限才能自动完成分屏。 | 可点击状态卡上的 Enable 按钮；不点击也可正常浏览与手动使用，无强制、无不可取消弹窗 | `com.deehem.splitz.MainActivity.onCreate → mm0.e；jn0.d` |
| 2 | 跳无障碍设置 | 系统设置页 com.android.settings 无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS） | 点击 Enable/Reconnect 按钮 → sn0.d 点击回调 → un0.a() case 0 | 系统无障碍页 | **原文**：Splitz uses this Accessibility Service exclusively to automate placing your selected app pairs into split screen. The service is required for automatic split-screen placement; without it, apps will only open sequentially. Splitz operates 100% offline, without internet access, and does not read, collect, or transmit screen contents, keystrokes, or personal data.<br>**译注**：Splitz 仅使用此无障碍服务来自动把您选定的应用对放入分屏。该服务是自动分屏所必需的；没有它，应用只会依次打开。Splitz 100% 离线运行、无网络访问，不会读取、收集或传输屏幕内容、按键记录或个人数据。 | 在系统列表中自行找到 Splitz 并打开开关；可随时返回/拒绝，应用不做任何重跳或催促 | `un0.a；res/values/strings.xml#accessibility_service_description；res/xml/accessibility_service_config.xml` |
| 3 | 业务功能触发 | MainActivity 首页“Launch Split Screen”按钮（fl.e） | 用户点击启动分屏 → mm0.e(case 0) → MainActivity.k(topPackage, bottomPackage) | 原生Activity | **原文**：Launch Split Screen<br>**译注**：启动分屏 | 点击即执行；由 lh1.a/lh1.b 判断服务是否已启用（内存实例 + Settings.Secure.enabled_accessibility_services） | `com.deehem.splitz.MainActivity.k；lh1.a；lh1.b` |
| 4 | 拒权反馈循环（实为一次性提示+降级） | Toast + 依次启动两个目标应用 | k() 判定未授权 → MainActivity.i(str, str2) | 原生Activity | **原文**：Accessibility Service is not enabled. Both apps will start sequentially, but cannot be automatically placed in split screen.<br>**译注**：无障碍服务未启用。两个应用将依次启动，但无法自动放入分屏。 | 无强制操作：先 startActivity(top)，800ms 后 Handler postDelayed(o5) 启动 bottom，功能降级但不阻断；不弹窗、不重跳设置 | `com.deehem.splitz.MainActivity.i` |
| 5 | 跳受限设置（电池优化，非 13+ 受限设置） | 系统电池优化豁免对话框（android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，失败回退 IGNORE_BATTERY_OPTIMIZATION_SETTINGS） | 首页电池卡片文案点击 → un0.a() default 分支 | 系统无障碍页 | **原文**：Exempt Splitz from battery optimization to keep automation instant.<br>**译注**：将 Splitz 排除在电池优化之外，以保持自动化即时生效。 | 用户可允许或拒绝；拒绝不影响分屏功能，仅可能影响后台保活 | `jn0.d（default 分支）；un0.a（default 分支）；AndroidManifest.xml uses-permission REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |
| 6 | 获权后动作 / 后台重连 | 通知栏通知（channel: Notifies when the split-screen automation service needs reconnection）→ 点击跳系统无障碍页 | 服务被系统回收后 v31.m(context) 触发；SharedPreferences splitz_recovery_prefs.key_disconnect_notified 去重，只发一次 | 通知栏 | **原文**：Splitz: Automation Service Paused \| Tap to reconnect the split-screen service in Settings. \| Android system memory optimization paused the Splitz background service. Tap here to re-enable it.<br>**译注**：Splitz：自动化服务已暂停 \| 点击在设置中重新连接分屏服务。 \| Android 系统内存优化暂停了 Splitz 后台服务，点击此处重新启用。 | 用户可选择点击通知前往设置重连，或忽略；无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权 | `v31.m；SplitScreenService.onDestroy（调用 lh1.b 判定）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 首页 Compose 状态卡（原生界面，非弹窗）：状态标题与 'Requires offline Accessibility permission to automate split screens.' 说明 + Enable/Reconnect 按钮（jn0.d / sn0.d）
- 系统无障碍服务列表项说明：res/values/strings.xml 的 accessibility_service_description，经 res/xml/accessibility_service_config.xml 的 android:description 绑定，仅出现在系统设置页，不在应用内重复展示
- Toast 提示（MainActivity.i）：'Accessibility Service is not enabled. Both apps will start sequentially...'
- Toast 提示（lm0.i）：'Splitz service was paused by Android system memory management. Please re-connect in Accessibility Settings.'
- 通知栏常驻/一次性通知（v31.m）：标题 'Splitz: Automation Service Paused'、正文 'Tap to reconnect the split-screen service in Settings.'、BigText 'Android system memory optimization paused the Splitz background service. Tap here to re-enable it.'
- 首页电池优化卡片文案（jn0.d）：'Exempt Splitz from battery optimization to keep automation instant.'
- 无 assets/HTML、无 WebView、无悬浮窗 Overlay、无仿系统无障碍开关页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Splitz uses this Accessibility Service exclusively to automate placing your selected app pairs into split screen. The service is required for automatic split-screen placement; without it, apps will only open sequentially. Splitz operates 100% offline, without internet access, and does not read, collect, or transmit screen contents, keystrokes, or personal data. | Splitz 仅使用此无障碍服务来自动把您选定的应用对放入分屏。该服务是自动分屏所必需的；没有它，应用只会依次打开。Splitz 100% 离线运行、无网络访问，不会读取、收集或传输屏幕内容、按键记录或个人数据。 | `res/values/strings.xml key=accessibility_service_description（经 res/xml/accessibility_service_config.xml android:description 引用）` | 良性透明说明 |
| en | Automation Service Disabled | 自动化服务未启用 | `硬编码于 jn0.d（Compose 状态标题）` | 良性透明说明 |
| en | Requires offline Accessibility permission to automate split screens. | 需要离线的无障碍权限才能自动完成分屏。 | `硬编码于 jn0.d（状态卡副标题）` | 良性透明说明 |
| en | Service Paused by Android | 服务已被 Android 暂停 | `硬编码于 jn0.d` | 良性透明说明 |
| en | Enabled in Settings, but paused in background. Tap to reconnect. | 已在设置中启用，但在后台被暂停。点击重新连接。 | `硬编码于 jn0.d` | 良性透明说明 |
| en | Accessibility Service is not enabled. Both apps will start sequentially, but cannot be automatically placed in split screen. | 无障碍服务未启用。两个应用将依次启动，但无法自动放入分屏。 | `硬编码于 com.deehem.splitz.MainActivity.i（Toast）` | 良性透明说明 |
| en | Splitz service was paused by Android system memory management. Please re-connect in Accessibility Settings. | Splitz 服务已被 Android 系统内存管理暂停。请在无障碍设置中重新连接。 | `硬编码于 lm0.i（Toast）` | 良性透明说明 |
| en | Android system memory optimization paused the Splitz background service. Tap here to re-enable it. | Android 系统内存优化暂停了 Splitz 后台服务。点击此处重新启用。 | `硬编码于 v31.m（通知 BigText）` | 未知 |
| en | Exempt Splitz from battery optimization to keep automation instant. | 将 Splitz 排除在电池优化之外，以保持自动化即时生效。 | `硬编码于 jn0.d（电池优化卡片）` | 良性透明说明 |
| en | Splitz: Automation Service Paused | Splitz：自动化服务已暂停 | `硬编码于 v31.m（通知标题）` | 良性透明说明 |
| en | Tap the + icon below to pair two apps, assign a folder, and pin them directly to your home screen. | 点击下方 + 图标配对两个应用、指定文件夹，并直接固定到主屏幕。 | `硬编码于 zm0.d（空态引导）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。拒绝或从系统设置返回后无 onResume 重跳、无定时器拉起、无页面锁定；仅在下次点击 Enable 或点击通知时才再次跳转。未授权时 MainActivity.k 走 i() 分支，Toast 提示后依次启动两个应用（800ms 间隔），功能降级而非阻断。
- **遮罩叠层 / 高仿系统设置页**：无。未声明 SYSTEM_ALERT_WINDOW，无悬浮窗；无仿系统无障碍开关页、无半透明遮罩指引；跳转目标为真实 android.settings.ACCESSIBILITY_SETTINGS。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。代码中无 ACTION_APPLICATION_DETAILS_SETTINGS、无「右上角菜单允许受限设置」分步教学、无 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：无。未发现获权后自点确认、自授权，也未在无障碍事件中监听设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权；SplitScreenService.onDestroy 仅调用 lh1.b 记录状态并可发一次重连通知。
- **良性降级 / 替代方案**：有。未授权时明确提示「两个应用将依次启动，只是无法自动分屏」，仍完成启动；电池优化被拒也不影响分屏；服务被系统回收时首页显示 'Service Paused by Android' 并提供 Reconnect 按钮与一次性通知，属可解释、可忽略的降级路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两类时机：(1) 冷启动进入 MainActivity 后首页状态卡渲染出 'Automation Service Disabled' + 'Requires offline Accessibility permission to automate split screens.' 的瞬间（验证是否存在不可取消弹窗/遮罩，预期为无）；(2) 监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 的瞬间（un0.a / v31.m 的 PendingIntent），立即抓取应用侧与系统设置页两侧画面。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。引导文本全部为 DEX 内明文硬编码或 strings.xml 资源，无纯图引导、无本地/远端 HTML、无加壳与密文载荷；唯一需注意的轻微差异是重连通知文案 'Android system memory optimization paused the Splitz background service' 略带系统归因表述，但其与实际成因（后台服务被内存管理终止）一致且提供可选重连，不构成恐吓诱导。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首页状态卡（权限引导唯一常驻载体）** | com.deehem.splitz/.MainActivity，Compose 界面含 'Automation Service Disabled' 文本与 Enable 按钮 | 确认引导是否仅以普通页面呈现、是否存在不可取消 Dialog 或全屏遮罩，这是区分良性透明说明与诱导的核心点 | 是否存在 isCancelable=false 的 Dialog/全屏遮罩节点；按钮文本是否为 Enable/Reconnect 且可跳过；状态文案是否含恐吓或假安全措辞 |
| **跳转前/跳转瞬间的应用侧画面** | startActivity('android.settings.ACCESSIBILITY_SETTINGS') 触发点（un0.a case 0） | 确认跳转是否由用户点击触发而非自动触发，且中间无 WebView/HTML 教学页或二次确认遮罩 | 跳转前是否存在应用自有 Activity/Fragment 叠加；是否有 WebView 节点或 assets html 加载；Intent action 字符串是否为标准系统 action |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中 'Splitz' 条目及其说明文字 | 核对系统展示的服务名与 description 是否与应用内一致、有无身份伪装或空白挤出警告 | 列表项标题是否为 Splitz（与桌面名一致）；说明文本是否为 100% offline 透明说明；服务条目是否存在多个可疑同名项 |
| **拒权后降级画面** | 返回应用后 Toast 'Accessibility Service is not enabled...' 与依次启动的两个目标应用 | 验证拒权后是否进入死循环重跳，或按代码所示仅提示并降级 | 是否反复回到系统设置页；Toast 文本内容；两个目标应用是否依次启动（降级成功标志） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.deehem.splitz.MainActivity.onCreate`
- `com.deehem.splitz.MainActivity.k`
- `com.deehem.splitz.MainActivity.i`
- `un0.a`
- `v31.m`
- `res/values/strings.xml#accessibility_service_description`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，静态可见性完整）

**核心判定：该应用在获取无障碍权限时属于“良性透明说明 + 功能触发式跳转”，未发现诱导、恐吓、遮罩或拒绝权限后循环重跳。**

1. **权限状态展示入口**：冷启动后进入 [MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.deehem.splitz.MainActivity#onCreate>) → Compose 首页 `mm0.e`（case 1/2），以状态卡展示三种文案：`Splitz Automation Active` / `Service Paused by Android` / `Automation Service Disabled`，副标题为 `Requires offline Accessibility permission to automate split screens.`；只有在未启用时才渲染按钮（`sn0#d` 文案 `Enable`，暂停态为 `Reconnect`）。
2. **唯一跳转点**：按钮回调 → [un0.a()](<resource-unit:#1.dex1 code:un0#a>) case 0 → `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，直接跳系统无障碍列表页，**没有本地 HTML、WebView、悬浮窗、仿系统开关页或遮罩层**（`res/` 无 html，无 `SYSTEM_ALERT_WINDOW` 权限，Manifest 仅 1 个 Activity）。失败仅 Toast `Could not open settings`。
3. **功能触发降级**：点“Launch Split Screen”（`fl#e`）→ [MainActivity.k()](<resource-unit:#1.dex1 code:com.deehem.splitz.MainActivity#k>) 通过 [lh1.a/b()](<resource-unit:#1.dex1 code:lh1#b>)（实例存活 + `Settings.Secure.enabled_accessibility_services` 双检）判断授权；未授权走 [MainActivity.i()](<resource-unit:#1.dex1 code:com.deehem.splitz.MainActivity#i>)，Toast `Accessibility Service is not enabled. Both apps will start sequentially, but cannot be automatically placed in split screen.` 后仍依次启动两个应用——**明确的手动降级路径，无阻塞、无取消障碍**。
4. **后台重连通知（唯一“再拉设置”路径）**：服务被系统回收后 [v31.m()](<resource-unit:#1.dex1 code:v31#m>) 发一次性通知（`splitz_recovery_prefs/key_disconnect_notified` 去重），点击经 PendingIntent 跳 `ACCESSIBILITY_SETTINGS`。文案“Android system memory optimization paused the Splitz background service”虽略带系统化表述，但与真实成因（后台服务被内存管理终止）一致，属事实陈述，非故障恐吓。
5. **附加权限**：`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` 仅在首页电池卡点击时经 `un0.a` default 分支调起，文案 `Exempt Splitz from battery optimization to keep automation instant.`，有失败回退到 `IGNORE_BATTERY_OPTIMIZATION_SETTINGS`。
6. **未发现**：13+ 受限设置分步教学、`ACTION_APPLICATION_DETAILS_SETTINGS` 跳转、多 Activity-alias 伪装、伪造 `isAccessibilityTool`、获权后 `GLOBAL_ACTION_BACK/HOME` 阻止撤权、`onResume` 死循环重跳。
7. **身份与描述一致**：`app_name=Splitz`，无障碍服务无独立 label，回落到 `Splitz`；`android:description` 为英文透明说明（100% 离线、不读屏内容/不收集传输、缺失时仅顺序启动）；`accessibility_service_config` 仅 `typeAllMask` + `canRetrieveWindowContent="false"`，与声明能力吻合。

**证据边界**：`un0`、`v31`、`lh1`、`mm0` 等为 R8 混淆后的短名类，但其字符串常量、`Intent action` 与调用关系静态完全可读；本报告结论基于纯静态核验，未启动动态抓取（无需验证云控/远端页面，代码中无网络权限，Manifest 无 `INTERNET`）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部关键逻辑静态可见：Manifest、accessibility_service_config、strings.xml 及 R8 混淆后的 un0.a / v31.m / lh1.a-b / mm0.e / sn0.d 均可完整反编译；应用未声明 INTERNET 权限，无本地 html/assets 引导页、无加壳与密文载荷，引导文案均为 DEX 内硬编码字符串或 strings.xml 资源，不存在远端下发或运行时解密。",
  "summary_one_liner": "Splitz 仅在首页状态卡以透明说明文字（Requires offline Accessibility permission to automate split screens）配合单个 Enable 按钮跳转系统无障碍列表，未授权时降级为顺序启动两个应用，无遮罩、无循环重跳、无受限设置教学。",
  "disguise_identity": {
    "app_display_name": "Splitz",
    "claimed_brand_or_persona": "Splitz（F-Droid 开源分屏效率工具，作者 com.deehem）",
    "a11y_service_label": "Splitz（服务未单独声明 label，回落 @string/app_name）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅 R8 代码混淆（短类名 un0/v31/lh1/mm0），非身份伪装；无空白/换行挤出警告、无同形字、无多 activity-alias（Manifest 仅 MainActivity 一个 Activity，singleTask，含 MAIN/LAUNCHER 与自定义 LAUNCH_SPLIT 两个 filter）、未伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.deehem.splitz.MainActivity（Jetpack Compose 首页，含无障碍状态卡）",
      "trigger_event": "onCreate → setContent(gm) → mm0.e(case 1) 渲染状态卡",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Automation Service Disabled / Requires offline Accessibility permission to automate split screens.",
      "shown_text_zh": "自动化服务未启用 / 需要离线的无障碍权限才能自动完成分屏。",
      "user_action_requested": "可点击状态卡上的 Enable 按钮；不点击也可正常浏览与手动使用，无强制、无不可取消弹窗",
      "code_anchor": "com.deehem.splitz.MainActivity.onCreate → mm0.e；jn0.d"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 com.android.settings 无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "点击 Enable/Reconnect 按钮 → sn0.d 点击回调 → un0.a() case 0",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Splitz uses this Accessibility Service exclusively to automate placing your selected app pairs into split screen. The service is required for automatic split-screen placement; without it, apps will only open sequentially. Splitz operates 100% offline, without internet access, and does not read, collect, or transmit screen contents, keystrokes, or personal data.",
      "shown_text_zh": "Splitz 仅使用此无障碍服务来自动把您选定的应用对放入分屏。该服务是自动分屏所必需的；没有它，应用只会依次打开。Splitz 100% 离线运行、无网络访问，不会读取、收集或传输屏幕内容、按键记录或个人数据。",
      "user_action_requested": "在系统列表中自行找到 Splitz 并打开开关；可随时返回/拒绝，应用不做任何重跳或催促",
      "code_anchor": "un0.a；res/values/strings.xml#accessibility_service_description；res/xml/accessibility_service_config.xml"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity 首页“Launch Split Screen”按钮（fl.e）",
      "trigger_event": "用户点击启动分屏 → mm0.e(case 0) → MainActivity.k(topPackage, bottomPackage)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Launch Split Screen",
      "shown_text_zh": "启动分屏",
      "user_action_requested": "点击即执行；由 lh1.a/lh1.b 判断服务是否已启用（内存实例 + Settings.Secure.enabled_accessibility_services）",
      "code_anchor": "com.deehem.splitz.MainActivity.k；lh1.a；lh1.b"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环（实为一次性提示+降级）",
      "screen_or_component": "Toast + 依次启动两个目标应用",
      "trigger_event": "k() 判定未授权 → MainActivity.i(str, str2)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility Service is not enabled. Both apps will start sequentially, but cannot be automatically placed in split screen.",
      "shown_text_zh": "无障碍服务未启用。两个应用将依次启动，但无法自动放入分屏。",
      "user_action_requested": "无强制操作：先 startActivity(top)，800ms 后 Handler postDelayed(o5) 启动 bottom，功能降级但不阻断；不弹窗、不重跳设置",
      "code_anchor": "com.deehem.splitz.MainActivity.i"
    },
    {
      "step": 5,
      "stage": "跳受限设置（电池优化，非 13+ 受限设置）",
      "screen_or_component": "系统电池优化豁免对话框（android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，失败回退 IGNORE_BATTERY_OPTIMIZATION_SETTINGS）",
      "trigger_event": "首页电池卡片文案点击 → un0.a() default 分支",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Exempt Splitz from battery optimization to keep automation instant.",
      "shown_text_zh": "将 Splitz 排除在电池优化之外，以保持自动化即时生效。",
      "user_action_requested": "用户可允许或拒绝；拒绝不影响分屏功能，仅可能影响后台保活",
      "code_anchor": "jn0.d（default 分支）；un0.a（default 分支）；AndroidManifest.xml uses-permission REQUEST_IGNORE_BATTERY_OPTIMIZATIONS"
    },
    {
      "step": 6,
      "stage": "获权后动作 / 后台重连",
      "screen_or_component": "通知栏通知（channel: Notifies when the split-screen automation service needs reconnection）→ 点击跳系统无障碍页",
      "trigger_event": "服务被系统回收后 v31.m(context) 触发；SharedPreferences splitz_recovery_prefs.key_disconnect_notified 去重，只发一次",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Splitz: Automation Service Paused | Tap to reconnect the split-screen service in Settings. | Android system memory optimization paused the Splitz background service. Tap here to re-enable it.",
      "shown_text_zh": "Splitz：自动化服务已暂停 | 点击在设置中重新连接分屏服务。 | Android 系统内存优化暂停了 Splitz 后台服务，点击此处重新启用。",
      "user_action_requested": "用户可选择点击通知前往设置重连，或忽略；无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权",
      "code_anchor": "v31.m；SplitScreenService.onDestroy（调用 lh1.b 判定）"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 首页 Compose 状态卡（原生界面，非弹窗）：状态标题与 'Requires offline Accessibility permission to automate split screens.' 说明 + Enable/Reconnect 按钮（jn0.d / sn0.d）",
    "系统无障碍服务列表项说明：res/values/strings.xml 的 accessibility_service_description，经 res/xml/accessibility_service_config.xml 的 android:description 绑定，仅出现在系统设置页，不在应用内重复展示",
    "Toast 提示（MainActivity.i）：'Accessibility Service is not enabled. Both apps will start sequentially...'",
    "Toast 提示（lm0.i）：'Splitz service was paused by Android system memory management. Please re-connect in Accessibility Settings.'",
    "通知栏常驻/一次性通知（v31.m）：标题 'Splitz: Automation Service Paused'、正文 'Tap to reconnect the split-screen service in Settings.'、BigText 'Android system memory optimization paused the Splitz background service. Tap here to re-enable it.'",
    "首页电池优化卡片文案（jn0.d）：'Exempt Splitz from battery optimization to keep automation instant.'",
    "无 assets/HTML、无 WebView、无悬浮窗 Overlay、无仿系统无障碍开关页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Splitz uses this Accessibility Service exclusively to automate placing your selected app pairs into split screen. The service is required for automatic split-screen placement; without it, apps will only open sequentially. Splitz operates 100% offline, without internet access, and does not read, collect, or transmit screen contents, keystrokes, or personal data.",
      "text_zh": "Splitz 仅使用此无障碍服务来自动把您选定的应用对放入分屏。该服务是自动分屏所必需的；没有它，应用只会依次打开。Splitz 100% 离线运行、无网络访问，不会读取、收集或传输屏幕内容、按键记录或个人数据。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（经 res/xml/accessibility_service_config.xml android:description 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Automation Service Disabled",
      "text_zh": "自动化服务未启用",
      "source_location": "硬编码于 jn0.d（Compose 状态标题）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Requires offline Accessibility permission to automate split screens.",
      "text_zh": "需要离线的无障碍权限才能自动完成分屏。",
      "source_location": "硬编码于 jn0.d（状态卡副标题）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Service Paused by Android",
      "text_zh": "服务已被 Android 暂停",
      "source_location": "硬编码于 jn0.d",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enabled in Settings, but paused in background. Tap to reconnect.",
      "text_zh": "已在设置中启用，但在后台被暂停。点击重新连接。",
      "source_location": "硬编码于 jn0.d",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service is not enabled. Both apps will start sequentially, but cannot be automatically placed in split screen.",
      "text_zh": "无障碍服务未启用。两个应用将依次启动，但无法自动放入分屏。",
      "source_location": "硬编码于 com.deehem.splitz.MainActivity.i（Toast）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Splitz service was paused by Android system memory management. Please re-connect in Accessibility Settings.",
      "text_zh": "Splitz 服务已被 Android 系统内存管理暂停。请在无障碍设置中重新连接。",
      "source_location": "硬编码于 lm0.i（Toast）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Android system memory optimization paused the Splitz background service. Tap here to re-enable it.",
      "text_zh": "Android 系统内存优化暂停了 Splitz 后台服务。点击此处重新启用。",
      "source_location": "硬编码于 v31.m（通知 BigText）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Exempt Splitz from battery optimization to keep automation instant.",
      "text_zh": "将 Splitz 排除在电池优化之外，以保持自动化即时生效。",
      "source_location": "硬编码于 jn0.d（电池优化卡片）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Splitz: Automation Service Paused",
      "text_zh": "Splitz：自动化服务已暂停",
      "source_location": "硬编码于 v31.m（通知标题）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Tap the + icon below to pair two apps, assign a folder, and pin them directly to your home screen.",
      "text_zh": "点击下方 + 图标配对两个应用、指定文件夹，并直接固定到主屏幕。",
      "source_location": "硬编码于 zm0.d（空态引导）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。拒绝或从系统设置返回后无 onResume 重跳、无定时器拉起、无页面锁定；仅在下次点击 Enable 或点击通知时才再次跳转。未授权时 MainActivity.k 走 i() 分支，Toast 提示后依次启动两个应用（800ms 间隔），功能降级而非阻断。",
    "overlay_or_fake_settings": "无。未声明 SYSTEM_ALERT_WINDOW，无悬浮窗；无仿系统无障碍开关页、无半透明遮罩指引；跳转目标为真实 android.settings.ACCESSIBILITY_SETTINGS。",
    "restricted_settings_13plus_coaching": "无。代码中无 ACTION_APPLICATION_DETAILS_SETTINGS、无「右上角菜单允许受限设置」分步教学、无 Session 安装器绕过。",
    "post_grant_anti_removal": "无。未发现获权后自点确认、自授权，也未在无障碍事件中监听设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权；SplitScreenService.onDestroy 仅调用 lh1.b 记录状态并可发一次重连通知。",
    "benign_graceful_degradation": "有。未授权时明确提示「两个应用将依次启动，只是无法自动分屏」，仍完成启动；电池优化被拒也不影响分屏；服务被系统回收时首页显示 'Service Paused by Android' 并提供 Reconnect 按钮与一次性通知，属可解释、可忽略的降级路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两类时机：(1) 冷启动进入 MainActivity 后首页状态卡渲染出 'Automation Service Disabled' + 'Requires offline Accessibility permission to automate split screens.' 的瞬间（验证是否存在不可取消弹窗/遮罩，预期为无）；(2) 监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 的瞬间（un0.a / v31.m 的 PendingIntent），立即抓取应用侧与系统设置页两侧画面。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首页状态卡（权限引导唯一常驻载体）",
        "page_identifier": "com.deehem.splitz/.MainActivity，Compose 界面含 'Automation Service Disabled' 文本与 Enable 按钮",
        "why_most_useful": "确认引导是否仅以普通页面呈现、是否存在不可取消 Dialog 或全屏遮罩，这是区分良性透明说明与诱导的核心点",
        "observable_utg_signals": ["是否存在 isCancelable=false 的 Dialog/全屏遮罩节点", "按钮文本是否为 Enable/Reconnect 且可跳过", "状态文案是否含恐吓或假安全措辞"]
      },
      {
        "page_role": "跳转前/跳转瞬间的应用侧画面",
        "page_identifier": "startActivity('android.settings.ACCESSIBILITY_SETTINGS') 触发点（un0.a case 0）",
        "why_most_useful": "确认跳转是否由用户点击触发而非自动触发，且中间无 WebView/HTML 教学页或二次确认遮罩",
        "observable_utg_signals": ["跳转前是否存在应用自有 Activity/Fragment 叠加", "是否有 WebView 节点或 assets html 加载", "Intent action 字符串是否为标准系统 action"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中 'Splitz' 条目及其说明文字",
        "why_most_useful": "核对系统展示的服务名与 description 是否与应用内一致、有无身份伪装或空白挤出警告",
        "observable_utg_signals": ["列表项标题是否为 Splitz（与桌面名一致）", "说明文本是否为 100% offline 透明说明", "服务条目是否存在多个可疑同名项"]
      },
      {
        "page_role": "拒权后降级画面",
        "page_identifier": "返回应用后 Toast 'Accessibility Service is not enabled...' 与依次启动的两个目标应用",
        "why_most_useful": "验证拒权后是否进入死循环重跳，或按代码所示仅提示并降级",
        "observable_utg_signals": ["是否反复回到系统设置页", "Toast 文本内容", "两个目标应用是否依次启动（降级成功标志）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。引导文本全部为 DEX 内明文硬编码或 strings.xml 资源，无纯图引导、无本地/远端 HTML、无加壳与密文载荷；唯一需注意的轻微差异是重连通知文案 'Android system memory optimization paused the Splitz background service' 略带系统归因表述，但其与实际成因（后台服务被内存管理终止）一致且提供可选重连，不构成恐吓诱导。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.deehem.splitz.MainActivity.onCreate",
    "com.deehem.splitz.MainActivity.k",
    "com.deehem.splitz.MainActivity.i",
    "un0.a",
    "v31.m",
    "res/values/strings.xml#accessibility_service_description"
  ]
}
```

</details>

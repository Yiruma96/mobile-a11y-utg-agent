# BN_029__0d4ca892c8｜极简桌面与双击锁屏 — Focus

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：172.1s

## 1. 一句话核心结论

- **核心申请方式**：Focus Launcher 在首次冷启动时把用户导向原生 Compose 三步设置向导页，用逐条透明说明加 Turn on/Allow 按钮引导开启无障碍（ACCESSIBILITY_SETTINGS），并在 Android 13+ 如实教学受限设置，全程可跳过、拒权仅降级提示、获权后无防撤权动作
- **静态可见性说明**：DEX 未加壳未混淆控制流关键路径完整可见；引导 UI 为原生 Jetpack Compose 页面（无 WebView/无本地或远端 HTML/无悬浮窗/无加密资产），跳转常量与文案均以明文字符串存在于 classes.dex，可完整静态还原
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `0d4ca892c83dcb5ac7f35aca061f65fa1e1af60adab8607107b76f4bad298d8a` |
| 包名 / 年份 | `com.focus.launcher` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.focus.launcher_78.apk |
| 桌面显示名 | Focus |
| 引导页宣称品牌/身份 | Focus Launcher（F-Droid 开源极简桌面，包名 com.focus.launcher 与自称一致） |
| 系统无障碍列表服务名 | Focus app timers |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。未使用空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool；android:description 如实披露仅接收前台应用名、不能读取屏幕内容、数据不出设备 |
| 无障碍服务类名 | `com.focus.launcher.service.FocusAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES` |
| 系统设置项说明 (`android:description`) | Focus uses this service to notice which app is in front, so it can lock an app once its daily time limit is used up. It also lets home-screen gestures open notifications or lock the screen.<br><br>The service only receives the name of the app that is on screen. It cannot read what is on your screen, and nothing ever leaves your device. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.focus.launcher.MainActivity（HOME 桌面 Activity） | onCreate 中读取 SharedPreferences 的 tutorial_seen，为 false 时一次性跳转 SettingsActivity(route=welcome) 并置为 true | 原生Activity | **原文**：无（本步无界面文案，仅路由跳转）<br>**译注**：首次启动直接进入设置向导页，之后冷启动不再自动跳转 | 无需操作，自动跳转；桌面本身可直接使用（可退出向导） | `com.focus.launcher.MainActivity.onCreate` |
| 2 | 引导说明页 | com.focus.launcher.SettingsActivity（route=welcome/setup，Compose 设置向导） | Activity 启动渲染三步清单；也可从设置项 "Welcome screen and tips" 或提示条 "Open setup →" 再次进入 | 原生Activity | **原文**：1 · Default launcher / "Makes Focus the screen you land on when you press Home." \| 2 · Usage access / "Lets Focus measure screen time: the day bar, app timers and the weekly review all depend on it." \| 3 · Focus timer service / "An accessibility service that notices which app is in front, so an app can be locked the moment its time runs out..."<br>**译注**：第 1 步设为默认桌面；第 2 步授予用量访问权限以便统计屏幕时间；第 3 步开启无障碍服务以识别前台应用并在额度用尽时锁定 | 逐条点击 Allow / Turn on；存在 Done 与 Not now 等可关闭入口，非强制 | `t4.x#c（三步说明与 Turn on/Allow 按钮）` |
| 3 | 跳受限设置 | 系统 应用详情页（android.settings.APPLICATION_DETAILS_SETTINGS, package:com.focus.launcher） | 点击向导中受限设置说明后的 "Open App info →"（o4.c(context, 8) / case 6） | 系统无障碍页 | **原文**："...is greyed out, or “restricted setting”? Open App info → ⋮ (top right) → Allow restricted settings, then try again.  Open App info  →"<br>**译注**：若开关变灰或提示“受限设置”，请进入应用信息 → 右上角菜单 → 允许受限设置，然后重试 | 进入系统应用详情页，手动点右上角菜单允许受限设置（明示教学，无 Session 安装器绕过、无伪造系统页） | `o4.c#a（case 6/8 → APPLICATION_DETAILS_SETTINGS）` |
| 4 | 跳无障碍设置 | 系统 无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS） | 点击第 3 步 "Turn on" 按钮（o4.c(context, 7) / case 7，addFlags FLAG_ACTIVITY_NEW_TASK） | 系统无障碍页 | **原文**：Focus app timers / "Focus uses this service to notice which app is in front, so it can lock an app once its daily time limit is used up. It also lets home-screen gestures open notifications or lock the screen. The service only receives the name of the app that is on screen. It cannot read what is on your screen, and nothing ever leaves your device."<br>**译注**：系统列表中显示“Focus 应用定时器”，说明该服务只识别前台应用名以在额度用尽时锁定，另支持主屏手势打开通知或锁屏，并声明读不到屏幕内容、数据不出设备 | 用户在系统页手动开启开关；应用无遮罩叠层、无自动点击、无脚本化点击 | `o4.c#a（case 7）+ res/xml/accessibility_service.xml + strings accessibility_label/accessibility_description` |
| 5 | 拒权反馈循环 | 主屏 Compose 提示条 + Toast（MainActivity 首页与设置项） | 从系统设置返回且服务未启用时，下一次进入首页/触发相关功能时的状态检查渲染 | 原生Activity | **原文**："The Focus timer service is off, so double tap cannot lock yet.  Open setup  →" / "Timers cannot count anything until usage access is allowed.  Open setup  →" / "The Focus timer service is off: apps are only locked when opened from Focus, not while you are inside them.  Open setup  →" / Toast: "Turn on the Focus timer service to lock with a double tap"<br>**译注**：提示服务未开启因此双击锁屏不可用/定时器无法计数，并提供“打开设置 →”入口；不强制、不循环重跳 | 可忽略继续使用桌面；MainActivity 未重写 onResume，无返回即重跳或定时拉起 | `t4.q#c、x4.f#c、o4.d#f` |
| 6 | 获权后动作 | com.focus.launcher.service.FocusAccessibilityService | 系统回调 onServiceConnected 注册 SCREEN_OFF/USER_PRESENT 广播；onAccessibilityEvent 处理 typeWindowStateChanged | 原生Activity | **原文**：Log.i("FocusTimer", "connected")（仅日志，无用户可见文案）<br>**译注**：获权后仅记录前台应用名并驱动定时器/锁屏逻辑；不监听设置页、不模拟 BACK/HOME 阻止撤权 | 无 | `com.focus.launcher.service.FocusAccessibilityService.onServiceConnected / onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- SettingsActivity(route=welcome/setup) 原生 Compose 三步设置向导清单（1 · Default launcher / 2 · Usage access / 3 · Focus timer service 及其说明与 Turn on·Allow 按钮）
- 同一向导内受限设置教学块：“...is greyed out, or “restricted setting”? Open App info → ⋮ (top right) → Allow restricted settings, then try again.  Open App info →”
- 主屏 Compose 提示条："The Focus timer service is off, so double tap cannot lock yet.  Open setup  →"、"Timers cannot count anything until usage access is allowed.  Open setup  →"、"Timers only lock apps once usage access and the Focus timer service are on.  Finish setup  →"
- Toast 提示："Turn on the Focus timer service to lock with a double tap"
- 系统无障碍服务列表：android:label="Focus app timers"、android:summary="Enforces the daily app time limits you set in Focus."、android:description 隐私与范围说明
- 设置页“隐私说明”文本："The timer service sees the name of the app in front and nothing else; it cannot read what is on your screen."（c0.i1#c）
- 设置项说明："Double tap to lock ... Turns the screen off. Uses the Focus timer service."（t4.q#c）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Focus uses this service to notice which app is in front, so it can lock an app once its daily time limit is used up. It also lets home-screen gestures open notifications or lock the screen. The service only receives the name of the app that is on screen. It cannot read what is on your screen, and nothing ever leaves your device. | Focus 使用该服务识别当前前台应用，以便在某应用当日额度用尽时将其锁定；同时也让主屏手势可打开通知或锁屏。该服务只接收屏幕上当前应用的名称，无法读取屏幕内容，任何数据都不会离开你的设备。 | `res/values/strings.xml: accessibility_description（@string/accessibility_description，由 res/xml/accessibility_service.xml 引用）` | 良性透明说明 |
| en | Enforces the daily app time limits you set in Focus. | 执行你在 Focus 中设置的每日应用使用时长限制。 | `res/values/strings.xml: accessibility_summary` | 良性透明说明 |
| en | 3 · Focus timer service | 第 3 步 · Focus 定时器服务 | `classes.dex 硬编码字符串，t4.x#c（设置向导步骤标题）` | 良性透明说明 |
| en | An accessibility service that notices which app is in front, so an app can be locked the moment its time runs out. It can | 一个无障碍服务，用于识别当前前台应用，使应用在时长用尽的瞬间被锁定。它（可以……后续说明权限范围） | `classes.dex 硬编码字符串，t4.x#c（向导第 3 步说明）` | 良性透明说明 |
| en | Is the toggle greyed out, or “restricted setting”? Open App info → ⋮ (top right) → Allow restricted settings, then try again.  Open App info  → | 开关是否变灰或提示“受限设置”？请打开应用信息 → 右上角 ⋮ → 允许受限设置，然后重试。打开应用信息 → | `classes.dex 硬编码字符串，t4.x#c（Android 13+ 受限设置分步教学）` | 受限设置分步教学 |
| en | The Focus timer service is off, so double tap cannot lock yet.  Open setup  → | Focus 定时器服务未开启，双击暂时无法锁屏。打开设置 → | `classes.dex 硬编码字符串，t4.q#c（首页提示条）` | 良性透明说明 |
| en | The timer service sees the name of the app in front and nothing else; it cannot read what is on your screen. | 定时器服务只看到前台应用的名字，其他什么都看不到；它无法读取你屏幕上的内容。 | `classes.dex 硬编码字符串，c0.i1#c（设置页隐私说明）` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。设置页跳转为一次性 startActivity；MainActivity 未重写 onResume，无 onResume 重跳、无定时器拉起；未授权时仅在首页渲染提示条（"...is off, so double tap cannot lock yet.  Open setup  →"）并保留桌面正常使用，属安全降级
- **遮罩叠层 / 高仿系统设置页**：无。未使用半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；跳转目标为标准 android.settings.ACCESSIBILITY_SETTINGS 与 APPLICATION_DETAILS_SETTINGS
- **Android 13+ 受限设置（Restricted Settings）应对**：有明示文字教学："Open App info → ⋮ (top right) → Allow restricted settings, then try again"，并通过 o4.c(context, 8)/case 6 跳系统应用详情页；无 Session 安装器绕过、无自动化点击、无伪造页
- **获权后即时行为与防撤权机制**：无。全包未发现 GLOBAL_ACTION_BACK/HOME 模拟、未监听设置页 Activity、未自点确认；服务仅处理 typeWindowStateChanged 且 canRetrieveWindowContent=false
- **良性降级 / 替代方案**：有。未授权时双击锁屏不可用（Toast 说明）、定时器不计数（提示条说明），桌面与手动入口照常可用；提示条提供 “Open setup →” 可选入口，向导存在 Done / Not now 关闭选项

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到应用首次冷启动后 startActivity 指向自身 SettingsActivity（route=welcome）的瞬间拉起一次；以及监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS（package:com.focus.launcher）跳转的瞬间拉起，用于抓取跳转前向导页与跳转后的系统页
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导文案全为可提取的文本节点（Compose 语义树），无图片/GIF 引导、无 WebView、无远端 HTML、无加壳。唯一需注意：向导页为 Compose 渲染，UTG 需依赖语义树而非传统 View id；且首启跳转依赖 SharedPreferences 的 tutorial_seen，重复安装/清数据后才会再次触发，检测时需保证首启状态

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **首启设置向导页（三步清单）** | com.focus.launcher.SettingsActivity，Compose 页面含 “1 · Default launcher / 2 · Usage access / 3 · Focus timer service” 文本与 Turn on / Allow 按钮 | 该页是全部无障碍引导文案的唯一承载位置，可直接判定是否存在恐吓、伪装、无取消按钮等诱导特征 | 文本节点 “3 · Focus timer service” 与无障碍范围说明；Turn on / Allow 按钮是否存在对应取消或 Done/Not now 入口；是否存在遮罩层或悬浮窗节点覆盖系统页 |
| **跳转后系统无障碍服务列表项** | android.settings.ACCESSIBILITY_SETTINGS 中 “Focus app timers” 条目及 description 文本 | 核对系统层展示名与说明是否与应用内文案一致，验证是否存在身份伪装或夸大承诺 | 条目 label = Focus app timers；description 完整隐私与范围声明；开关初始状态与是否有应用叠层覆盖 |
| **返回后的首页提示条（拒权反馈）** | com.focus.launcher.MainActivity 顶部提示条 “...is off, so double tap cannot lock yet.  Open setup  →” | 区分良性降级与拒权循环/强制重跳的关键页；观察是否被反复拉起、是否可关闭 | 提示条出现频次与是否自动重跳设置页；是否存在不可关闭的全屏遮罩；桌面功能是否仍可正常操作 |
| **受限设置教学触发的系统应用详情页** | android.settings.APPLICATION_DETAILS_SETTINGS, package:com.focus.launcher | 确认跳转目标为真实系统应用详情页而非高仿页面，并核验是否伴随自动化点击 | 页面包名 com.android.settings；无应用自身 Activity 叠加；无自动点击/无障碍点击事件注入 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.focus.launcher.MainActivity.onCreate`
- `o4.c#a（case 7 → ACCESSIBILITY_SETTINGS；case 6/8 → APPLICATION_DETAILS_SETTINGS）`
- `t4.x#c（Compose 三步设置向导与受限设置教学文案）`
- `res/xml/accessibility_service.xml`
- `com.focus.launcher.service.FocusAccessibilityService.onAccessibilityEvent`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，12 次工具调用收口）

**静态可见性：完整**。应用未加壳，无 WebView、无远端页面、无悬浮窗、无加密载荷；无障碍引导全部由原生 Compose 设置向导页实现。

### 引导链（纯运行期 UTG 视角）
1. **冷启动首启跳转**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.focus.launcher.MainActivity#onCreate>) 读取 `SharedPreferences` 的 `tutorial_seen`，为 false 时 `startActivity(SettingsActivity, extra route="welcome")` 并置 `tutorial_seen=true`（一次性，非每次冷启动）。
2. **设置向导页（原生 Compose Activity）**：`SettingsActivity(route=welcome/setup)` 渲染三步清单，逐条为 `"1 · Default launcher"`、`"2 · Usage access"`、`"3 · Focus timer service"`，每步含透明说明与 `Turn on` / `Allow` 按钮。
3. **跳转分派集中在一个 switch**：[o4.c#a()](<resource-unit:#1.dex1 code:o4.c#a>)：`case 7` → `android.settings.ACCESSIBILITY_SETTINGS`（`addFlags(FLAG_ACTIVITY_NEW_TASK)`）；`case 6/8` → `APPLICATION_DETAILS_SETTINGS`（`package:com.focus.launcher`，用于受限设置引导）；`case 3` → 通知监听设置。
4. **Android 13+ 受限设置分步教学**：向导文本 "…is greyed out, or “restricted setting”? Open App info → ⋮ (top right) → Allow restricted settings, then try again.  Open App info →" 配 `o4.c(context, 8)` 跳应用详情页。属**明示教学**，无伪造设置页、无 Session 安装器绕过。
5. **拒权反馈：良性降级，无死循环**。`MainActivity` 未重写 `onResume`，设置页返回后不重跳；未启用无障碍时功能降级为提示文案（`"The Focus timer service is off, so double tap cannot lock yet.  Open setup  →"`、`"Timers cannot count anything until usage access is allowed."`）+ `Toast`，并保留 `Not now` / `Done` 关闭入口。
6. **获权后无防撤权动作**：全包无 `GLOBAL_ACTION_BACK`/`HOME`、无监听设置页回压；[FocusAccessibilityService](<resource-unit:#1.dex1 code:com.focus.launcher.service.FocusAccessibilityService#onAccessibilityEvent>) 仅消费 `typeWindowStateChanged` 的包名/类名，[accessibility_service.xml](<resource-unit:#1 file:res/xml/accessibility_service.xml>) 明确 `canRetrieveWindowContent="false"`、`flagDefault`，与 `android:description` 的"只收前台应用名、读不到屏幕内容、数据不出设备"承诺一致。
7. **身份一致**：桌面名 `Focus`、服务标签 `Focus app timers`、`settingsActivity` 指向真实 `SettingsActivity`；无空白/换行挤出警告、无同形字、无多 activity-alias、未伪造 `isAccessibilityTool`。

**判定**：属于"按需/首启一次性、透明说明 + 显式可取消 + 拒权安全降级"的良性无障碍申请模式，未发现诱导、恐吓、遮罩叠层或拒权循环。仅 `LURE_RESTRICTED_SETTINGS_COACHING` 事实存在，但文本如实解释原因，不构成规避审核。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳未混淆控制流关键路径完整可见；引导 UI 为原生 Jetpack Compose 页面（无 WebView/无本地或远端 HTML/无悬浮窗/无加密资产），跳转常量与文案均以明文字符串存在于 classes.dex，可完整静态还原",
  "summary_one_liner": "Focus Launcher 在首次冷启动时把用户导向原生 Compose 三步设置向导页，用逐条透明说明加 Turn on/Allow 按钮引导开启无障碍（ACCESSIBILITY_SETTINGS），并在 Android 13+ 如实教学受限设置，全程可跳过、拒权仅降级提示、获权后无防撤权动作",
  "disguise_identity": {
    "app_display_name": "Focus",
    "claimed_brand_or_persona": "Focus Launcher（F-Droid 开源极简桌面，包名 com.focus.launcher 与自称一致）",
    "a11y_service_label": "Focus app timers",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。未使用空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool；android:description 如实披露仅接收前台应用名、不能读取屏幕内容、数据不出设备"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.focus.launcher.MainActivity（HOME 桌面 Activity）",
      "trigger_event": "onCreate 中读取 SharedPreferences 的 tutorial_seen，为 false 时一次性跳转 SettingsActivity(route=welcome) 并置为 true",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（本步无界面文案，仅路由跳转）",
      "shown_text_zh": "首次启动直接进入设置向导页，之后冷启动不再自动跳转",
      "user_action_requested": "无需操作，自动跳转；桌面本身可直接使用（可退出向导）",
      "code_anchor": "com.focus.launcher.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.focus.launcher.SettingsActivity（route=welcome/setup，Compose 设置向导）",
      "trigger_event": "Activity 启动渲染三步清单；也可从设置项 \"Welcome screen and tips\" 或提示条 \"Open setup →\" 再次进入",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "1 · Default launcher / \"Makes Focus the screen you land on when you press Home.\" | 2 · Usage access / \"Lets Focus measure screen time: the day bar, app timers and the weekly review all depend on it.\" | 3 · Focus timer service / \"An accessibility service that notices which app is in front, so an app can be locked the moment its time runs out...\"",
      "shown_text_zh": "第 1 步设为默认桌面；第 2 步授予用量访问权限以便统计屏幕时间；第 3 步开启无障碍服务以识别前台应用并在额度用尽时锁定",
      "user_action_requested": "逐条点击 Allow / Turn on；存在 Done 与 Not now 等可关闭入口，非强制",
      "code_anchor": "t4.x#c（三步说明与 Turn on/Allow 按钮）"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统 应用详情页（android.settings.APPLICATION_DETAILS_SETTINGS, package:com.focus.launcher）",
      "trigger_event": "点击向导中受限设置说明后的 \"Open App info →\"（o4.c(context, 8) / case 6）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "\"...is greyed out, or “restricted setting”? Open App info → ⋮ (top right) → Allow restricted settings, then try again.  Open App info  →\"",
      "shown_text_zh": "若开关变灰或提示“受限设置”，请进入应用信息 → 右上角菜单 → 允许受限设置，然后重试",
      "user_action_requested": "进入系统应用详情页，手动点右上角菜单允许受限设置（明示教学，无 Session 安装器绕过、无伪造系统页）",
      "code_anchor": "o4.c#a（case 6/8 → APPLICATION_DETAILS_SETTINGS）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统 无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "点击第 3 步 \"Turn on\" 按钮（o4.c(context, 7) / case 7，addFlags FLAG_ACTIVITY_NEW_TASK）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Focus app timers / \"Focus uses this service to notice which app is in front, so it can lock an app once its daily time limit is used up. It also lets home-screen gestures open notifications or lock the screen. The service only receives the name of the app that is on screen. It cannot read what is on your screen, and nothing ever leaves your device.\"",
      "shown_text_zh": "系统列表中显示“Focus 应用定时器”，说明该服务只识别前台应用名以在额度用尽时锁定，另支持主屏手势打开通知或锁屏，并声明读不到屏幕内容、数据不出设备",
      "user_action_requested": "用户在系统页手动开启开关；应用无遮罩叠层、无自动点击、无脚本化点击",
      "code_anchor": "o4.c#a（case 7）+ res/xml/accessibility_service.xml + strings accessibility_label/accessibility_description"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "主屏 Compose 提示条 + Toast（MainActivity 首页与设置项）",
      "trigger_event": "从系统设置返回且服务未启用时，下一次进入首页/触发相关功能时的状态检查渲染",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "\"The Focus timer service is off, so double tap cannot lock yet.  Open setup  →\" / \"Timers cannot count anything until usage access is allowed.  Open setup  →\" / \"The Focus timer service is off: apps are only locked when opened from Focus, not while you are inside them.  Open setup  →\" / Toast: \"Turn on the Focus timer service to lock with a double tap\"",
      "shown_text_zh": "提示服务未开启因此双击锁屏不可用/定时器无法计数，并提供“打开设置 →”入口；不强制、不循环重跳",
      "user_action_requested": "可忽略继续使用桌面；MainActivity 未重写 onResume，无返回即重跳或定时拉起",
      "code_anchor": "t4.q#c、x4.f#c、o4.d#f"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.focus.launcher.service.FocusAccessibilityService",
      "trigger_event": "系统回调 onServiceConnected 注册 SCREEN_OFF/USER_PRESENT 广播；onAccessibilityEvent 处理 typeWindowStateChanged",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Log.i(\"FocusTimer\", \"connected\")（仅日志，无用户可见文案）",
      "shown_text_zh": "获权后仅记录前台应用名并驱动定时器/锁屏逻辑；不监听设置页、不模拟 BACK/HOME 阻止撤权",
      "user_action_requested": "无",
      "code_anchor": "com.focus.launcher.service.FocusAccessibilityService.onServiceConnected / onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "SettingsActivity(route=welcome/setup) 原生 Compose 三步设置向导清单（1 · Default launcher / 2 · Usage access / 3 · Focus timer service 及其说明与 Turn on·Allow 按钮）",
    "同一向导内受限设置教学块：“...is greyed out, or “restricted setting”? Open App info → ⋮ (top right) → Allow restricted settings, then try again.  Open App info →”",
    "主屏 Compose 提示条：\"The Focus timer service is off, so double tap cannot lock yet.  Open setup  →\"、\"Timers cannot count anything until usage access is allowed.  Open setup  →\"、\"Timers only lock apps once usage access and the Focus timer service are on.  Finish setup  →\"",
    "Toast 提示：\"Turn on the Focus timer service to lock with a double tap\"",
    "系统无障碍服务列表：android:label=\"Focus app timers\"、android:summary=\"Enforces the daily app time limits you set in Focus.\"、android:description 隐私与范围说明",
    "设置页“隐私说明”文本：\"The timer service sees the name of the app in front and nothing else; it cannot read what is on your screen.\"（c0.i1#c）",
    "设置项说明：\"Double tap to lock ... Turns the screen off. Uses the Focus timer service.\"（t4.q#c）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Focus uses this service to notice which app is in front, so it can lock an app once its daily time limit is used up. It also lets home-screen gestures open notifications or lock the screen. The service only receives the name of the app that is on screen. It cannot read what is on your screen, and nothing ever leaves your device.",
      "text_zh": "Focus 使用该服务识别当前前台应用，以便在某应用当日额度用尽时将其锁定；同时也让主屏手势可打开通知或锁屏。该服务只接收屏幕上当前应用的名称，无法读取屏幕内容，任何数据都不会离开你的设备。",
      "source_location": "res/values/strings.xml: accessibility_description（@string/accessibility_description，由 res/xml/accessibility_service.xml 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enforces the daily app time limits you set in Focus.",
      "text_zh": "执行你在 Focus 中设置的每日应用使用时长限制。",
      "source_location": "res/values/strings.xml: accessibility_summary",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "3 · Focus timer service",
      "text_zh": "第 3 步 · Focus 定时器服务",
      "source_location": "classes.dex 硬编码字符串，t4.x#c（设置向导步骤标题）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "An accessibility service that notices which app is in front, so an app can be locked the moment its time runs out. It can",
      "text_zh": "一个无障碍服务，用于识别当前前台应用，使应用在时长用尽的瞬间被锁定。它（可以……后续说明权限范围）",
      "source_location": "classes.dex 硬编码字符串，t4.x#c（向导第 3 步说明）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Is the toggle greyed out, or “restricted setting”? Open App info → ⋮ (top right) → Allow restricted settings, then try again.  Open App info  →",
      "text_zh": "开关是否变灰或提示“受限设置”？请打开应用信息 → 右上角 ⋮ → 允许受限设置，然后重试。打开应用信息 →",
      "source_location": "classes.dex 硬编码字符串，t4.x#c（Android 13+ 受限设置分步教学）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "The Focus timer service is off, so double tap cannot lock yet.  Open setup  →",
      "text_zh": "Focus 定时器服务未开启，双击暂时无法锁屏。打开设置 →",
      "source_location": "classes.dex 硬编码字符串，t4.q#c（首页提示条）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The timer service sees the name of the app in front and nothing else; it cannot read what is on your screen.",
      "text_zh": "定时器服务只看到前台应用的名字，其他什么都看不到；它无法读取你屏幕上的内容。",
      "source_location": "classes.dex 硬编码字符串，c0.i1#c（设置页隐私说明）",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。设置页跳转为一次性 startActivity；MainActivity 未重写 onResume，无 onResume 重跳、无定时器拉起；未授权时仅在首页渲染提示条（\"...is off, so double tap cannot lock yet.  Open setup  →\"）并保留桌面正常使用，属安全降级",
    "overlay_or_fake_settings": "无。未使用半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；跳转目标为标准 android.settings.ACCESSIBILITY_SETTINGS 与 APPLICATION_DETAILS_SETTINGS",
    "restricted_settings_13plus_coaching": "有明示文字教学：\"Open App info → ⋮ (top right) → Allow restricted settings, then try again\"，并通过 o4.c(context, 8)/case 6 跳系统应用详情页；无 Session 安装器绕过、无自动化点击、无伪造页",
    "post_grant_anti_removal": "无。全包未发现 GLOBAL_ACTION_BACK/HOME 模拟、未监听设置页 Activity、未自点确认；服务仅处理 typeWindowStateChanged 且 canRetrieveWindowContent=false",
    "benign_graceful_degradation": "有。未授权时双击锁屏不可用（Toast 说明）、定时器不计数（提示条说明），桌面与手动入口照常可用；提示条提供 “Open setup →” 可选入口，向导存在 Done / Not now 关闭选项"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到应用首次冷启动后 startActivity 指向自身 SettingsActivity（route=welcome）的瞬间拉起一次；以及监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS（package:com.focus.launcher）跳转的瞬间拉起，用于抓取跳转前向导页与跳转后的系统页",
    "key_pages_to_capture": [
      {
        "page_role": "首启设置向导页（三步清单）",
        "page_identifier": "com.focus.launcher.SettingsActivity，Compose 页面含 “1 · Default launcher / 2 · Usage access / 3 · Focus timer service” 文本与 Turn on / Allow 按钮",
        "why_most_useful": "该页是全部无障碍引导文案的唯一承载位置，可直接判定是否存在恐吓、伪装、无取消按钮等诱导特征",
        "observable_utg_signals": ["文本节点 “3 · Focus timer service” 与无障碍范围说明", "Turn on / Allow 按钮是否存在对应取消或 Done/Not now 入口", "是否存在遮罩层或悬浮窗节点覆盖系统页"]
      },
      {
        "page_role": "跳转后系统无障碍服务列表项",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 中 “Focus app timers” 条目及 description 文本",
        "why_most_useful": "核对系统层展示名与说明是否与应用内文案一致，验证是否存在身份伪装或夸大承诺",
        "observable_utg_signals": ["条目 label = Focus app timers", "description 完整隐私与范围声明", "开关初始状态与是否有应用叠层覆盖"]
      },
      {
        "page_role": "返回后的首页提示条（拒权反馈）",
        "page_identifier": "com.focus.launcher.MainActivity 顶部提示条 “...is off, so double tap cannot lock yet.  Open setup  →”",
        "why_most_useful": "区分良性降级与拒权循环/强制重跳的关键页；观察是否被反复拉起、是否可关闭",
        "observable_utg_signals": ["提示条出现频次与是否自动重跳设置页", "是否存在不可关闭的全屏遮罩", "桌面功能是否仍可正常操作"]
      },
      {
        "page_role": "受限设置教学触发的系统应用详情页",
        "page_identifier": "android.settings.APPLICATION_DETAILS_SETTINGS, package:com.focus.launcher",
        "why_most_useful": "确认跳转目标为真实系统应用详情页而非高仿页面，并核验是否伴随自动化点击",
        "observable_utg_signals": ["页面包名 com.android.settings", "无应用自身 Activity 叠加", "无自动点击/无障碍点击事件注入"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导文案全为可提取的文本节点（Compose 语义树），无图片/GIF 引导、无 WebView、无远端 HTML、无加壳。唯一需注意：向导页为 Compose 渲染，UTG 需依赖语义树而非传统 View id；且首启跳转依赖 SharedPreferences 的 tutorial_seen，重复安装/清数据后才会再次触发，检测时需保证首启状态"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.focus.launcher.MainActivity.onCreate",
    "o4.c#a（case 7 → ACCESSIBILITY_SETTINGS；case 6/8 → APPLICATION_DETAILS_SETTINGS）",
    "t4.x#c（Compose 三步设置向导与受限设置教学文案）",
    "res/xml/accessibility_service.xml",
    "com.focus.launcher.service.FocusAccessibilityService.onAccessibilityEvent"
  ]
}
```

</details>

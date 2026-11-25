# MR_002__05782e267b｜EventBot — Flash Update

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：74.0s

## 1. 一句话核心结论

- **核心申请方式**：以“Flash Update”冒充系统更新，冷启动无 UI 后由后台服务每 20 秒循环弹出不可取消的本地 HTML WebView 悬浮弹窗（含两张截图分步教学），点击按钮直达 ACTION_ACCESSIBILITY_SETTINGS，拒权即重弹，并以“System updating, please wait...”全屏遮罩与返回键拦截维持权限。
- **静态可见性说明**：UTG 全链路（Manifest、无障碍配置、引导 HTML、assets 截图、DEX 控制流）均包内明文可见，未加壳、无 VMP、无加密二阶段载荷；仅 C2 地址（cfg.urls 指向 ora.studiolegalebasili.com 等）为远端控制面，与无障碍引导流程无关，不影响本命题判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `05782e267bd62de78a3db22b1a83ddd3c72cbef95f5a5bc9defdd42a4f5786ec` |
| 包名 / 年份 | `com.example.eventbot` / 2020 |
| 家族 / 品类 | **EventBot**（同池样本数：124） |
| 原始来源标识 | https://www.cybereason.com/blog/eventbot-a-new-mobile-banking-trojan-is-born |
| 桌面显示名 | Flash Update |
| 引导页宣称品牌/身份 | Flash Update（伪装的系统/应用更新组件，文案自称不开启则“无法正常工作”） |
| 系统无障碍列表服务名 | Flash Update |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无空白挤出/同形字/多 activity-alias；但无障碍服务 android:label 直接复用 @string/app_name（Flash Update），使系统无障碍列表项与“更新组件”语义混淆；引导文案以“功能依赖”恐吓而非说明真实用途（短信监听、全局按键过滤） |
| 无障碍服务类名 | `com.example.eventbot.events` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | You must enable Flash Update in order to get full functionality of the application. Flash Update will not work correctly. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.example.eventbot.MainActivity（LAUNCHER）→ 立即 finish() | 用户点击桌面图标 Flash Update（onCreate） | 原生Activity | 无 | 无（用户仅点击图标） | `com.example.eventbot.MainActivity#onCreate` |
| 2 | 后台服务装配与轮询启动 | com.example.eventbot.service（前台不可见 Service） | MainActivity.onCreate → startService；service.onCreate 反射构造 func 并启动 func$2 线程 | 不可静态还原 | 无 | 无 | `com.example.eventbot.service#onCreate / com.example.eventbot.func#requestPermissions` |
| 3 | 引导说明页（悬浮弹窗） | com.example.eventbot.activity（mode=2）→ doActivity case 2 → AlertDialog + WebView | requestPermissions 轮询检测 isA11y()==false → requestA11yAlertActivity → activity.onCreate | 本地HTML WebView | **原文**：Flash Update will not work correctly. / 1. Select Flash Update in Settings / 2. Turn on it（配 1.jpg、2.jpg 截图）<br>**译注**：Flash Update 将无法正常工作。1. 在设置中选择 Flash Update；2. 将其开启（配两张系统设置截图） | 仅可点击“Enable Flash Update”按钮；setCancelable(false)，无取消/跳过/关闭入口，窗口类型 2003 系统悬浮层 | `com.example.eventbot.func#requestA11yAlert / res/values/strings.xml#L64` |
| 4 | 跳无障碍设置 | 系统“设置 → 无障碍 → 已下载的服务”列表 | 点击弹窗按钮“Enable Flash Update” → func$3.onClick | 系统无障碍页 | **原文**：You must enable Flash Update in order to get full functionality of the application. Flash Update will not work correctly.（系统列表项描述）<br>**译注**：你必须启用 Flash Update 才能获得应用完整功能，否则 Flash Update 将无法正常工作 | 在系统无障碍列表中手动找到 Flash Update 并打开开关（应用无法代点，需用户操作） | `com.example.eventbot.func$3#onClick / res/xml/accessibility_config.xml` |
| 5 | 拒权反馈循环 | activity(mode=2) 弹窗被反复重新拉起 | 用户按返回键或返回桌面 → 20 秒后 requestPermissions 下一轮 isA11y() 仍为 false | 本地HTML WebView | **原文**：Flash Update will not work correctly. / 1. Select Flash Update in Settings / 2. Turn on it<br>**译注**：同一引导弹窗循环重弹，无降级路径 | 只有“Enable Flash Update”一个有效出路；无取消、无“稍后再说”、无仅浏览模式 | `com.example.eventbot.func#requestPermissions（cfg.permissionsDelay=20）/ com.example.eventbot.func#requestA11yAlertActivity` |
| 6 | 遮罩叠层指引 | WindowManager 全屏 WebView 悬浮层（TYPE_APPLICATION_OVERLAY 2032 / 2006） | activity 以 mode=3/5 进入 doActivity → createOverlayOld/createOverlay | 悬浮窗Overlay | **原文**：System updating, please wait...<br>**译注**：系统正在更新，请稍候…… | 无需操作：以系统壁纸为背景、隐藏状态栏与导航栏的全屏“更新中”遮罩掩盖后台行为 | `com.example.eventbot.func#createOverlay / com.example.eventbot.func#createOverlayOld / res/values/strings.xml#L44` |
| 7 | 获权后动作 | com.example.eventbot.events（AccessibilityService）onServiceConnected | 系统绑定无障碍服务成功 | 系统无障碍页 | 无 | 无（用户已完成开关）；随后被要求忽略电池优化 | `com.example.eventbot.events#onServiceConnected` |
| 8 | 获权后动作（防撤权） | 系统设置“应用信息/卸载/停用”页面（被自动按返回键弹回） | onAccessibilityEvent 捕获 packageinstaller/settings/gms/vending 的 UninstallerActivity、DeviceAdminAdd、含应用名的 AlertDialog 或点击事件 | 系统无障碍页 | **原文**：无（无提示，静默拦截）<br>**译注**：用户尝试关闭无障碍或卸载时页面被自动返回键弹回 | 无；用户无法完成撤权/卸载 | `com.example.eventbot.func#unDeleteA11y / com.example.eventbot.func#makeBack` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- assets 内本地 HTML（hint_text 字符串）经 WebView.loadDataWithBaseURL("file:///android_asset/") 渲染，装入 AlertDialog（theme=3，窗口类型 2003 系统悬浮层，setCancelable(false)），按钮为 hint_button="Enable Flash Update"
- 该 HTML 内嵌 assets/1.jpg、assets/2.jpg 两张系统设置截图作为“选服务 → 打开开关”分步教学图
- 系统无障碍列表中的服务项：android:label="Flash Update" + android:description=@string/accessibility_config_text（“You must enable Flash Update…”）
- 全屏悬浮遮罩 WebView：banner_text 字符串内嵌 HTML，WindowManager.addView 以 TYPE_APPLICATION_OVERLAY(2032)/2006 全屏铺放，背景为系统壁纸，setSystemUiVisibility(3078) 隐藏状态栏/导航栏
- res/values/strings.xml 中的 Google Play services 相关文案（common_google_play_services_*）为 GMS 库自带，非本应用引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | You must enable Flash Update in order to get full functionality of the application. Flash Update will not work correctly. | 你必须启用 Flash Update 才能获得本应用的完整功能，否则 Flash Update 将无法正常工作。 | `res/values/strings.xml key=accessibility_config_text（被 res/xml/accessibility_config.xml android:description 引用）` | 假更新 |
| en | Flash Update will not work correctly. 1. Select Flash Update in Settings 2. Turn on it | Flash Update 将无法正常工作。1. 在设置中选择 Flash Update；2. 将其开启。 | `res/values/strings.xml key=hint_text（内嵌 HTML，由 func.requestA11yAlert 载入 WebView）` | 受限设置分步教学 |
| en | Enable Flash Update | 启用 Flash Update | `res/values/strings.xml key=hint_button（AlertDialog setPositiveButton 文案）` | 假更新 |
| en | System updating, please wait... | 系统正在更新，请稍候…… | `res/values/strings.xml key=banner_text（内嵌 HTML，func.createOverlay/createOverlayOld 全屏悬浮加载）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：func.requestPermissions 为 while(true) 循环：每轮 Thread.sleep(cfg.permissionsDelay=20) 秒后重新 isA11y() 校验，未授权即再次 startActivity(activity, mode=2) 重弹同一 WebView 悬浮弹窗；onClick 中 dismiss 后主动将 a11yAlertVisible 复位为 false，确保下次可再次弹出。用户返回系统设置后 20 秒内必然被重新打断，无降级或放弃路径。
- **遮罩叠层 / 高仿系统设置页**：双层叠加：① AlertDialog 以 WindowManager.LayoutParams 类型 2003（TYPE_SYSTEM_ALERT）跨应用悬浮显示引导 WebView；② 全屏 WebView 悬浮窗（TYPE_APPLICATION_OVERLAY 2032 / 旧版 2006）加载“System updating, please wait...”旋转动画页，背景设为系统壁纸、setSystemUiVisibility(3078) 隐藏状态栏与导航栏，伪装成系统更新界面而非高仿无障碍开关页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=21，代码中未使用 ACTION_APPLICATION_DETAILS_SETTINGS 做“允许受限设置”教学，也无 Session 安装器或 embedded a11y APK 绕过（该 action 仅出现在 GMS 库类中）。
- **获权后即时行为与防撤权机制**：是。events.onServiceConnected 获权后立即 startService + minimizeAll + doAutorun；func.unDeleteA11y 监听 com.android.packageinstaller / com.android.settings / com.google.android.gms / com.android.vending 事件，一旦出现 android.app.AlertDialog、UninstallerActivity、com.android.settings.DeviceAdminAdd 或文本/控件包含自身应用名，即调用 makeBack() → performGlobalAction(1) 自动按返回键，阻止用户关闭无障碍、停用或卸载。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条并行钩子：① 冷启动 MainActivity 后 0～3 秒内首次出现窗口类型 2003 的 AlertDialog / 新 activity 栈顶为 com.example.eventbot.activity；② 监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS（由 com.example.eventbot.func$3.onClick 发出）时，在跳转瞬间与返回瞬间各截图一次。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无明显盲区：全部引导文本为可提取的 HTML/字符串，非纯图空文本；但需注意 ① 遮罩与弹窗均通过 WindowManager 以系统悬浮窗类型显示，若 UTG 仅抓 Activity 栈顶会漏掉 2003/2032 悬浮窗层，需同时抓窗口层级；② assets/1.jpg、2.jpg 为截图教学图，需结合同页 HTML 文本判读，不必单独 OCR；③ C2（cfg.urls，明文 HTTP）仅控制后续动作，不影响 UTG 判定。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | 栈顶 com.example.eventbot.activity（theme Theme.AppCompat.Light.NoActionBar.FullScreen）+ 系统悬浮窗（type=2003）内的 WebView，含两张图片与“Enable Flash Update”按钮 | 这是“无真实功能页、点开即被要求授权”的直接证据，可证明触发时机为冷启动 0 步而非按需功能 | 弹窗无取消/关闭控件，返回键无法关闭；WebView 内容为本地 file:///android_asset/ 加载的引导 HTML 与 1.jpg/2.jpg 截图；按钮文案与系统无障碍列表项同名 Flash Update |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务中的 Flash Update 条目及其描述文本 | 核对 android:label 与 android:description 是否把高危权限包装为“功能依赖”，并确认服务真实用途（短信/窗口内容/按键过滤）未被披露 | 列表项名称 Flash Update 与桌面应用同名；描述文本为“You must enable Flash Update…”；列表项下无真实功能说明 |
| **拒权后重弹页（循环验证）** | 用户按返回退出设置后 0～20 秒内重新出现的同款 2003 悬浮弹窗 | 直接证明“拒绝即重拉”的循环压迫机制，是 UTG 与良性引导的关键分水岭 | 同一弹窗在 20 秒周期内重复出现；无“稍后再说/跳过”分支；弹窗关闭后 a11yAlertVisible 复位导致再弹 |
| **设置页后遮罩页** | 全屏 WebView 悬浮窗（TYPE_APPLICATION_OVERLAY 2032），壁纸背景 + 白色“System updating, please wait...”与旋转 spinner，状态栏/导航栏隐藏 | 证明应用在用户处于系统设置期间用“系统更新中”假象遮盖真实界面，配合返回键拦截阻断撤权 | 窗口类型 2032/2006 全屏覆盖；状态栏与导航栏不可见（systemUiVisibility=3078）；遮罩文案与任何真实更新流程无关 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.example.eventbot.MainActivity#onCreate`
- `com.example.eventbot.func#requestPermissions`
- `com.example.eventbot.func#requestA11yAlert`
- `com.example.eventbot.func$3#onClick`
- `com.example.eventbot.func#createOverlay`
- `res/values/strings.xml#L42-L44`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（运行期 UTG 视角）

**页面流转链已完整静态还原，无需动态补证**（8 次工具调用内收口）：

1. **冷启动即入口，无真实 UI**：桌面图标名为 `Flash Update`，[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.example.eventbot.MainActivity#onCreate>) 只做 `startService(service)` 后立即 `finish()`，用户点开即闪退，转由后台服务驱动引导。
2. **服务反射装配文案**：[service.onCreate()](<resource-unit:#1.dex1 code:com.example.eventbot.service#onCreate>) 用 `getConstructor(...)` 注入 `R.string.app_name`、`hint_text`、`hint_button`、`banner_text` 与无障碍类名 `events`，随后 `func$2.run` 启动 [func.requestPermissions()](<resource-unit:#1.dex1 code:com.example.eventbot.func#requestPermissions>) —— **`while(true)` 轮询，间隔 `cfg.permissionsDelay = 20` 秒**。
3. **弹窗载体为本地 HTML WebView**：未授权时 [func.requestA11yAlertActivity()](<resource-unit:#1.dex1 code:com.example.eventbot.func#requestA11yAlertActivity>) 以 `mode=2` 拉起 [activity.onCreate()](<resource-unit:#1.dex1 code:com.example.eventbot.activity#onCreate>) → [func.doActivity()](<resource-unit:#1.dex1 code:com.example.eventbot.func#doActivity>) case 2 → [func.requestA11yAlert()](<resource-unit:#1.dex1 code:com.example.eventbot.func#requestA11yAlert>)：`WebView.loadDataWithBaseURL("file:///android_asset/", hint_text)` 装入 `AlertDialog`，`setCancelable(false)` + `getWindow().setType(2003)`（系统级悬浮窗），按钮文案 `Enable Flash Update`。
4. **引导页图文教学**：[hint_text](<resource-unit:#1 file:res/values/strings.xml#L64>) 内嵌 HTML「Flash Update will not work correctly. / 1. Select Flash Update in Settings / 2. Turn on it」，配包内 `assets/1.jpg`、`assets/2.jpg` 两张截图（已核实存在，无远端加载）。
5. **点按钮直达系统无障碍页**：[func$3.onClick()](<resource-unit:#1.dex1 code:com.example.eventbot.func$3#onClick>) → `Intent("android.settings.ACCESSIBILITY_SETTINGS")` + flags `1409286144`(NEW_TASK|CLEAR_TOP|RESET_TASK_IF_NEEDED)，随即 `dismiss()` 并复位 `a11yAlertVisible=false`（为下一次重弹留位）。
6. **拒权反馈＝死循环重弹**：用户返回/拒绝后 20 秒内 `requestA11yAlertActivity` 再次拉起同一弹窗；无「跳过/取消/仅浏览」分支。授权后循环转向 [requestOptimizationsIgnored](<resource-unit:#1.dex1 code:com.example.eventbot.func#requestPermissions>)（电池优化豁免），逼迫继续。
7. **获权后动作**：[events.onServiceConnected()](<resource-unit:#1.dex1 code:com.example.eventbot.events#onServiceConnected>) 拉起服务、`minimizeAll()` 回到桌面、`doAutorun()`；[func.unDeleteA11y()](<resource-unit:#1.dex1 code:com.example.eventbot.func#unDeleteA11y>) 监听 `packageinstaller/settings/gms/vending` 的 `UninstallerActivity`、`DeviceAdminAdd`、含自身名的 AlertDialog，命中即 `makeBack()`→`performGlobalAction(1)` 阻断撤权/卸载。
8. **全屏伪装遮罩**：[func.createOverlay()](<resource-unit:#1.dex1 code:com.example.eventbot.func#createOverlay>) / [createOverlayOld()](<resource-unit:#1.dex1 code:com.example.eventbot.func#createOverlayOld>) 以 `TYPE_APPLICATION_OVERLAY(2032)`/`2006` 全屏 WebView 加载 [banner_text](<resource-unit:#1 file:res/values/strings.xml#L44>)「System updating, please wait...」，背景换成系统壁纸、`setSystemUiVisibility(3078)` 隐藏状态栏导航栏，营造"系统更新中"假象。触发点经 `activity` 的 `mode=3/5`，具体外部调用方未逐一定位。

**未发现**：`ACTION_APPLICATION_DETAILS_SETTINGS` 的 Android 13「允许受限设置」教学、Session 安装器绕过、二阶段 Dropper（`embedded_a11y_apk=False` 与代码一致）；`isAccessibilityTool` 伪造、空白/同形字伪装均无。

**风险台账**：上述链路与既有 R-001（`autonomous_audit`/high/`deceptive_behavior`）为同一命题、同一处置对象，本轮仅做定向复核，结论与证据边界一致，不重复登记。

```json
{
  "static_visibility": "clear",
  "visibility_note": "UTG 全链路（Manifest、无障碍配置、引导 HTML、assets 截图、DEX 控制流）均包内明文可见，未加壳、无 VMP、无加密二阶段载荷；仅 C2 地址（cfg.urls 指向 ora.studiolegalebasili.com 等）为远端控制面，与无障碍引导流程无关，不影响本命题判定。",
  "summary_one_liner": "以“Flash Update”冒充系统更新，冷启动无 UI 后由后台服务每 20 秒循环弹出不可取消的本地 HTML WebView 悬浮弹窗（含两张截图分步教学），点击按钮直达 ACTION_ACCESSIBILITY_SETTINGS，拒权即重弹，并以“System updating, please wait...”全屏遮罩与返回键拦截维持权限。",
  "disguise_identity": {
    "app_display_name": "Flash Update",
    "claimed_brand_or_persona": "Flash Update（伪装的系统/应用更新组件，文案自称不开启则“无法正常工作”）",
    "a11y_service_label": "Flash Update",
    "identity_mismatch": true,
    "obfuscation_tricks": "无空白挤出/同形字/多 activity-alias；但无障碍服务 android:label 直接复用 @string/app_name（Flash Update），使系统无障碍列表项与“更新组件”语义混淆；引导文案以“功能依赖”恐吓而非说明真实用途（短信监听、全局按键过滤）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.example.eventbot.MainActivity（LAUNCHER）→ 立即 finish()",
      "trigger_event": "用户点击桌面图标 Flash Update（onCreate）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面，启动即退出，用户看不到功能页",
      "user_action_requested": "无（用户仅点击图标）",
      "code_anchor": "com.example.eventbot.MainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "后台服务装配与轮询启动",
      "screen_or_component": "com.example.eventbot.service（前台不可见 Service）",
      "trigger_event": "MainActivity.onCreate → startService；service.onCreate 反射构造 func 并启动 func$2 线程",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；装配 app_name/hint_text/hint_button/banner_text 与无障碍类名 events，进入 while(true) 权限轮询",
      "user_action_requested": "无",
      "code_anchor": "com.example.eventbot.service#onCreate / com.example.eventbot.func#requestPermissions"
    },
    {
      "step": 3,
      "stage": "引导说明页（悬浮弹窗）",
      "screen_or_component": "com.example.eventbot.activity（mode=2）→ doActivity case 2 → AlertDialog + WebView",
      "trigger_event": "requestPermissions 轮询检测 isA11y()==false → requestA11yAlertActivity → activity.onCreate",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Flash Update will not work correctly. / 1. Select Flash Update in Settings / 2. Turn on it（配 1.jpg、2.jpg 截图）",
      "shown_text_zh": "Flash Update 将无法正常工作。1. 在设置中选择 Flash Update；2. 将其开启（配两张系统设置截图）",
      "user_action_requested": "仅可点击“Enable Flash Update”按钮；setCancelable(false)，无取消/跳过/关闭入口，窗口类型 2003 系统悬浮层",
      "code_anchor": "com.example.eventbot.func#requestA11yAlert / res/values/strings.xml#L64"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统“设置 → 无障碍 → 已下载的服务”列表",
      "trigger_event": "点击弹窗按钮“Enable Flash Update” → func$3.onClick",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "You must enable Flash Update in order to get full functionality of the application. Flash Update will not work correctly.（系统列表项描述）",
      "shown_text_zh": "你必须启用 Flash Update 才能获得应用完整功能，否则 Flash Update 将无法正常工作",
      "user_action_requested": "在系统无障碍列表中手动找到 Flash Update 并打开开关（应用无法代点，需用户操作）",
      "code_anchor": "com.example.eventbot.func$3#onClick / res/xml/accessibility_config.xml"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "activity(mode=2) 弹窗被反复重新拉起",
      "trigger_event": "用户按返回键或返回桌面 → 20 秒后 requestPermissions 下一轮 isA11y() 仍为 false",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Flash Update will not work correctly. / 1. Select Flash Update in Settings / 2. Turn on it",
      "shown_text_zh": "同一引导弹窗循环重弹，无降级路径",
      "user_action_requested": "只有“Enable Flash Update”一个有效出路；无取消、无“稍后再说”、无仅浏览模式",
      "code_anchor": "com.example.eventbot.func#requestPermissions（cfg.permissionsDelay=20）/ com.example.eventbot.func#requestA11yAlertActivity"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "WindowManager 全屏 WebView 悬浮层（TYPE_APPLICATION_OVERLAY 2032 / 2006）",
      "trigger_event": "activity 以 mode=3/5 进入 doActivity → createOverlayOld/createOverlay",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "System updating, please wait...",
      "shown_text_zh": "系统正在更新，请稍候……",
      "user_action_requested": "无需操作：以系统壁纸为背景、隐藏状态栏与导航栏的全屏“更新中”遮罩掩盖后台行为",
      "code_anchor": "com.example.eventbot.func#createOverlay / com.example.eventbot.func#createOverlayOld / res/values/strings.xml#L44"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.example.eventbot.events（AccessibilityService）onServiceConnected",
      "trigger_event": "系统绑定无障碍服务成功",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；拉起 service、performGlobalAction 回到桌面、setServiceInfo 提权、doAutorun 启动自动操作，并转入电池优化豁免请求",
      "user_action_requested": "无（用户已完成开关）；随后被要求忽略电池优化",
      "code_anchor": "com.example.eventbot.events#onServiceConnected"
    },
    {
      "step": 8,
      "stage": "获权后动作（防撤权）",
      "screen_or_component": "系统设置“应用信息/卸载/停用”页面（被自动按返回键弹回）",
      "trigger_event": "onAccessibilityEvent 捕获 packageinstaller/settings/gms/vending 的 UninstallerActivity、DeviceAdminAdd、含应用名的 AlertDialog 或点击事件",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（无提示，静默拦截）",
      "shown_text_zh": "用户尝试关闭无障碍或卸载时页面被自动返回键弹回",
      "user_action_requested": "无；用户无法完成撤权/卸载",
      "code_anchor": "com.example.eventbot.func#unDeleteA11y / com.example.eventbot.func#makeBack"
    }
  ],
  "text_presentation_locations": [
    "assets 内本地 HTML（hint_text 字符串）经 WebView.loadDataWithBaseURL(\"file:///android_asset/\") 渲染，装入 AlertDialog（theme=3，窗口类型 2003 系统悬浮层，setCancelable(false)），按钮为 hint_button=\"Enable Flash Update\"",
    "该 HTML 内嵌 assets/1.jpg、assets/2.jpg 两张系统设置截图作为“选服务 → 打开开关”分步教学图",
    "系统无障碍列表中的服务项：android:label=\"Flash Update\" + android:description=@string/accessibility_config_text（“You must enable Flash Update…”）",
    "全屏悬浮遮罩 WebView：banner_text 字符串内嵌 HTML，WindowManager.addView 以 TYPE_APPLICATION_OVERLAY(2032)/2006 全屏铺放，背景为系统壁纸，setSystemUiVisibility(3078) 隐藏状态栏/导航栏",
    "res/values/strings.xml 中的 Google Play services 相关文案（common_google_play_services_*）为 GMS 库自带，非本应用引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "You must enable Flash Update in order to get full functionality of the application. Flash Update will not work correctly.",
      "text_zh": "你必须启用 Flash Update 才能获得本应用的完整功能，否则 Flash Update 将无法正常工作。",
      "source_location": "res/values/strings.xml key=accessibility_config_text（被 res/xml/accessibility_config.xml android:description 引用）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Flash Update will not work correctly. 1. Select Flash Update in Settings 2. Turn on it",
      "text_zh": "Flash Update 将无法正常工作。1. 在设置中选择 Flash Update；2. 将其开启。",
      "source_location": "res/values/strings.xml key=hint_text（内嵌 HTML，由 func.requestA11yAlert 载入 WebView）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Flash Update",
      "text_zh": "启用 Flash Update",
      "source_location": "res/values/strings.xml key=hint_button（AlertDialog setPositiveButton 文案）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "System updating, please wait...",
      "text_zh": "系统正在更新，请稍候……",
      "source_location": "res/values/strings.xml key=banner_text（内嵌 HTML，func.createOverlay/createOverlayOld 全屏悬浮加载）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "func.requestPermissions 为 while(true) 循环：每轮 Thread.sleep(cfg.permissionsDelay=20) 秒后重新 isA11y() 校验，未授权即再次 startActivity(activity, mode=2) 重弹同一 WebView 悬浮弹窗；onClick 中 dismiss 后主动将 a11yAlertVisible 复位为 false，确保下次可再次弹出。用户返回系统设置后 20 秒内必然被重新打断，无降级或放弃路径。",
    "overlay_or_fake_settings": "双层叠加：① AlertDialog 以 WindowManager.LayoutParams 类型 2003（TYPE_SYSTEM_ALERT）跨应用悬浮显示引导 WebView；② 全屏 WebView 悬浮窗（TYPE_APPLICATION_OVERLAY 2032 / 旧版 2006）加载“System updating, please wait...”旋转动画页，背景设为系统壁纸、setSystemUiVisibility(3078) 隐藏状态栏与导航栏，伪装成系统更新界面而非高仿无障碍开关页。",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=21，代码中未使用 ACTION_APPLICATION_DETAILS_SETTINGS 做“允许受限设置”教学，也无 Session 安装器或 embedded a11y APK 绕过（该 action 仅出现在 GMS 库类中）。",
    "post_grant_anti_removal": "是。events.onServiceConnected 获权后立即 startService + minimizeAll + doAutorun；func.unDeleteA11y 监听 com.android.packageinstaller / com.android.settings / com.google.android.gms / com.android.vending 事件，一旦出现 android.app.AlertDialog、UninstallerActivity、com.android.settings.DeviceAdminAdd 或文本/控件包含自身应用名，即调用 makeBack() → performGlobalAction(1) 自动按返回键，阻止用户关闭无障碍、停用或卸载。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条并行钩子：① 冷启动 MainActivity 后 0～3 秒内首次出现窗口类型 2003 的 AlertDialog / 新 activity 栈顶为 com.example.eventbot.activity；② 监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS（由 com.example.eventbot.func$3.onClick 发出）时，在跳转瞬间与返回瞬间各截图一次。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "栈顶 com.example.eventbot.activity（theme Theme.AppCompat.Light.NoActionBar.FullScreen）+ 系统悬浮窗（type=2003）内的 WebView，含两张图片与“Enable Flash Update”按钮",
        "why_most_useful": "这是“无真实功能页、点开即被要求授权”的直接证据，可证明触发时机为冷启动 0 步而非按需功能",
        "observable_utg_signals": ["弹窗无取消/关闭控件，返回键无法关闭", "WebView 内容为本地 file:///android_asset/ 加载的引导 HTML 与 1.jpg/2.jpg 截图", "按钮文案与系统无障碍列表项同名 Flash Update"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务中的 Flash Update 条目及其描述文本",
        "why_most_useful": "核对 android:label 与 android:description 是否把高危权限包装为“功能依赖”，并确认服务真实用途（短信/窗口内容/按键过滤）未被披露",
        "observable_utg_signals": ["列表项名称 Flash Update 与桌面应用同名", "描述文本为“You must enable Flash Update…”", "列表项下无真实功能说明"]
      },
      {
        "page_role": "拒权后重弹页（循环验证）",
        "page_identifier": "用户按返回退出设置后 0～20 秒内重新出现的同款 2003 悬浮弹窗",
        "why_most_useful": "直接证明“拒绝即重拉”的循环压迫机制，是 UTG 与良性引导的关键分水岭",
        "observable_utg_signals": ["同一弹窗在 20 秒周期内重复出现", "无“稍后再说/跳过”分支", "弹窗关闭后 a11yAlertVisible 复位导致再弹"]
      },
      {
        "page_role": "设置页后遮罩页",
        "page_identifier": "全屏 WebView 悬浮窗（TYPE_APPLICATION_OVERLAY 2032），壁纸背景 + 白色“System updating, please wait...”与旋转 spinner，状态栏/导航栏隐藏",
        "why_most_useful": "证明应用在用户处于系统设置期间用“系统更新中”假象遮盖真实界面，配合返回键拦截阻断撤权",
        "observable_utg_signals": ["窗口类型 2032/2006 全屏覆盖", "状态栏与导航栏不可见（systemUiVisibility=3078）", "遮罩文案与任何真实更新流程无关"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无明显盲区：全部引导文本为可提取的 HTML/字符串，非纯图空文本；但需注意 ① 遮罩与弹窗均通过 WindowManager 以系统悬浮窗类型显示，若 UTG 仅抓 Activity 栈顶会漏掉 2003/2032 悬浮窗层，需同时抓窗口层级；② assets/1.jpg、2.jpg 为截图教学图，需结合同页 HTML 文本判读，不必单独 OCR；③ C2（cfg.urls，明文 HTTP）仅控制后续动作，不影响 UTG 判定。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.example.eventbot.MainActivity#onCreate",
    "com.example.eventbot.func#requestPermissions",
    "com.example.eventbot.func#requestA11yAlert",
    "com.example.eventbot.func$3#onClick",
    "com.example.eventbot.func#createOverlay",
    "res/values/strings.xml#L42-L44"
  ]
}
```

</details>

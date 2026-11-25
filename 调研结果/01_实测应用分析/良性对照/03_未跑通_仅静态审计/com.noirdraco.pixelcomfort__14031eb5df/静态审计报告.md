# BN_069__14031eb5df｜隐私指示与安全防护工具 — PixelComfort

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：167.8s

## 1. 一句话核心结论

- **核心申请方式**：在设置页以可点击的“Accessibility service — Off · Turn on ‘PixelComfort auto-off’”一行明示用途，用户点击后单次跳转系统无障碍列表自行开启，无弹窗胁迫、无重跳循环、无遮罩伪装，服务能力限于窗口切换事件且不读取窗口内容。
- **静态可见性说明**：全部静态可见：无加壳/VMP，无障碍引导逻辑为 Kotlin/Compose 编译产物（classes.dex + classes2.dex），界面文字来自 res/values/strings.xml，无远端 HTML、无 WebView、无加密载荷；仅 Shizuku 授权与系统设置页由系统组件承载。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `14031eb5dfc2bd5b61e41fcf9e1e3f5c3b1ae5e1e6eab3d31ea6d2abdea2538b` |
| 包名 / 年份 | `com.noirdraco.pixelcomfort` / 2025-2026 |
| 家族 / 品类 | **隐私指示与安全防护工具**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.noirdraco.pixelcomfort_11.apk |
| 桌面显示名 | PixelComfort |
| 引导页宣称品牌/身份 | PixelComfort（F-Droid 开源应用，作者 NoirDraco，真实身份） |
| 系统无障碍列表服务名 | PixelComfort auto-off |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。R8 重命名仅产生 $$ExternalSyntheticLambda 合成类（常规 Kotlin/Compose 编译产物）；isAccessibilityTool 显式声明为 false，未伪造系统工具身份；未使用空白/换行挤出、同形字或多 activity-alias。 |
| 无障碍服务类名 | `com.noirdraco.pixelcomfort.ComfortAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Turns Comfort View off automatically while the camera or Photos app is in the foreground, and restores it when you leave. If you turn them on, it also switches private DNS by Wi‑Fi, hides the mobile signal icon on Wi‑Fi and switches the always-on display by Bluetooth device or Wi‑Fi. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.noirdraco.pixelcomfort.MainActivity（单 Activity + ComposeView） | LAUNCHER 启动 → onCreate() → setContent(ComposableLambda) | 原生Activity | **原文**：Setup incomplete / Accessibility service / Off · Turn on “PixelComfort auto-off” / Shizuku isn’t running / Shizuku permission missing<br>**译注**：设置未完成 / 无障碍服务 / 已关闭 · 请开启“PixelComfort auto-off” / Shizuku 未运行 / 缺少 Shizuku 权限 | 冷启动不弹任何强制弹窗，仅首页“Setup”分组内以状态行展示未完成项，用户可自行滑动浏览或忽略；无取消/跳过按钮需求（因为不存在阻断） | `com.noirdraco.pixelcomfort.MainActivity#onCreate；res/values/strings.xml（home_setup_needed、accessibility、accessibility_off）` |
| 2 | 引导说明页 | 首页 Setup 分组 + AOD 页 AodSetup 分组中的 SettingsRow（Compose 行） | HomeScreenKt$$ExternalSyntheticLambda18.invoke 依据 SetupStatus.accessibilityEnabled 渲染该行；AodScreenKt$$ExternalSyntheticLambda28.invoke 依据 AodPerms.service 渲染 | 原生Activity | **原文**：Accessibility service \| Off · Turn on “PixelComfort auto-off” \| On<br>**译注**：无障碍服务 \| 已关闭 · 请开启“PixelComfort auto-off” \| 已开启 | 用户主动点击该行才会进入系统设置；不点击则停留在本页，其余功能（Comfort View 手动开关、私有 DNS、AOD 规则）仍可查看，缺失项仅显示“Permission missing” | `com.noirdraco.pixelcomfort.ui.HomeScreenKt$$ExternalSyntheticLambda18#invoke；com.noirdraco.pixelcomfort.ui.AodScreenKt$$ExternalSyntheticLambda28#invoke；AodScreenKt.SettingsRow-mxsUjTo` |
| 3 | 跳无障碍设置 | 系统“设置 → 无障碍 → 已下载的服务”列表页（ACTION_ACCESSIBILITY_SETTINGS） | 用户点击该行 → Function0.invoke（$r8$classId=0/6/8 分支）→ context.startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：Turns Comfort View off automatically while the camera or Photos app is in the foreground, and restores it when you leave. If you turn them on, it also switches private DNS by Wi‑Fi, hides the mobile signal icon on Wi‑Fi and switches the always-on display by Bluetooth device or Wi‑Fi.<br>**译注**：当相机或“相册”应用在前台时自动关闭 Comfort View，离开时恢复。若你开启相应开关，它还会按 Wi‑Fi 切换私有 DNS、在 Wi‑Fi 下隐藏移动信号图标、按蓝牙设备或 Wi‑Fi 切换息屏显示。 | 由用户自行在系统列表中点击“PixelComfort auto-off”并确认；应用未附加任何自动化点击或遮罩引导 | `com.noirdraco.pixelcomfort.ui.AodScreenKt$$ExternalSyntheticLambda35#invoke（case 0/6/8）；res/xml/accessibility_service_config.xml；res/values/strings.xml#accessibility_service_description` |
| 4 | 拒权反馈循环 | MainActivity.onResume → ParcelableSnapshotMutableIntState.refresh 自增 → 重算 SetupStatus | 从系统设置返回时 onResume() 触发一次状态刷新 | 原生Activity | **原文**：Off · Turn on “PixelComfort auto-off”<br>**译注**：已关闭 · 请开启“PixelComfort auto-off”（保持原状态提示，不重跳、不弹窗） | 无强制动作；用户可直接退出或继续使用其他功能，不存在死循环重跳或不可取消弹窗 | `com.noirdraco.pixelcomfort.MainActivity#onResume` |
| 5 | 获权后动作 | com.noirdraco.pixelcomfort.ComfortAccessibilityService | onServiceConnected() → 注册 Shizuku binder 监听、NetworkWatcher.start()、AodMonitor.start()、SettingsWorker.submit()；随后 onAccessibilityEvent(typeWindowStateChanged) | 不可静态还原 | **原文**：Dienst verbunden. Ziel-Packages=..., suppressed=... (Aufloesung beim naechsten Fenster-Event)<br>**译注**：服务已连接。目标包=…，已抑制=…（在下一个窗口事件时解析）——仅写入 logcat，无界面呈现 | 无需用户操作；服务只读取前台包名/类名，忽略自身包名与当前输入法，不读取窗口内容、不执行全局手势、不自动点击确认 | `com.noirdraco.pixelcomfort.ComfortAccessibilityService#onServiceConnected；#onAccessibilityEvent；#isIgnored；#onDestroy` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 首页“Setup”分组的 Compose SettingsRow 行（原生 Compose 文本，非 Dialog）：标题“Accessibility service”，副标题由 accessibility_off 模板填充为“Off · Turn on ‘PixelComfort auto-off’”，已开启时为“On”
- AOD 页 AodSetup 分组的同类 SettingsRow（AodScreenKt$$ExternalSyntheticLambda28），点击回调 AodScreenKt$$ExternalSyntheticLambda35 跳系统无障碍设置
- 系统无障碍服务列表项：android:label=“PixelComfort auto-off”（res/values/strings.xml#accessibility_service_label）
- 系统无障碍服务详情说明：android:description=accessibility_service_description（res/xml/accessibility_service_config.xml → @string/accessibility_service_description）
- Advanced（高级）页 Permissions 分组的 adv_permissions_footer 说明文字，解释为何 Comfort View 需经 Shizuku 修改
- Advanced 页“Modify system settings / Modify secure settings / Allow in system dialog”三项授权行，点击跳 MANAGE_WRITE_SETTINGS 系统页
- Advanced Protection（高级保护）模式提示 apm_title/apm_summary，告知该模式下系统会关闭无障碍服务，属真实系统机制说明
- AOD 规则页的权限理由文案：aod_bluetooth_text（“Needed to see which devices are connected. Never scans.”）、aod_location_text（“Your location is never used.”）
- Quick Settings 磁贴标签 qs_tile_label 与 hide_mobile_needs_service（“Only works while ‘%1$s’ is on”）
- 未发现：WebView/HTML 页面、悬浮窗遮罩、全屏高仿系统无障碍开关页、通知栏诱导点击弹窗

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Turns Comfort View off automatically while the camera or Photos app is in the foreground, and restores it when you leave. If you turn them on, it also switches private DNS by Wi‑Fi, hides the mobile signal icon on Wi‑Fi and switches the always-on display by Bluetooth device or Wi‑Fi. | 当相机或“相册”应用在前台时自动关闭 Comfort View，离开时恢复。若你开启相应开关，它还会按 Wi‑Fi 切换私有 DNS、在 Wi‑Fi 下隐藏移动信号图标、按蓝牙设备或 Wi‑Fi 切换息屏显示。 | `res/values/strings.xml#accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用为 android:description）` | 良性透明说明 |
| en | Off · Turn on “%1$s” | 已关闭 · 请开启“%1$s”（运行时填充为“PixelComfort auto-off”） | `res/values/strings.xml#accessibility_off（渲染于 AodScreenKt$$ExternalSyntheticLambda28 / HomeScreenKt$$ExternalSyntheticLambda18 的 SettingsRow）` | 良性透明说明 |
| en | Accessibility service | 无障碍服务 | `res/values/strings.xml#accessibility` | 良性透明说明 |
| en | PixelComfort auto-off | PixelComfort 自动关闭（无障碍服务在系统列表中的显示名） | `res/values/strings.xml#accessibility_service_label（AndroidManifest.xml service android:label）` | 良性透明说明 |
| en | These permissions aren’t enough for Comfort View itself: Android doesn’t let other apps change that setting directly, so switching goes through Shizuku. Shizuku has to be started again after every restart. | 这些权限对 Comfort View 本身还不够：Android 不允许其他应用直接修改该设置，因此切换需经由 Shizuku 完成。每次重启后都需重新启动 Shizuku。 | `res/values/strings.xml#adv_permissions_footer（Advanced 页 Permissions 分组）` | 受限设置分步教学 |
| en | Android turns the accessibility service off in this mode. Turn Advanced Protection off to use the automation. | 在此模式下 Android 会关闭无障碍服务。若要使用自动化，请关闭“高级保护”。 | `res/values/strings.xml#apm_summary（配套 apm_title “Advanced Protection is on”）` | 良性透明说明 |
| en | Needed to see which devices are connected. Never scans. | 用于查看已连接的设备。从不扫描。 | `res/values/strings.xml#aod_bluetooth_text` | 隐私承诺 |
| en | Android only reveals the Wi‑Fi name with the location permission. Your location is never used. | Android 仅在授予位置权限后才显示 Wi‑Fi 名称。你的位置信息从不被使用。 | `res/values/strings.xml#aod_location_text` | 隐私承诺 |
| de | Dienst verbunden. Ziel-Packages=%s, suppressed=%s (Aufloesung beim naechsten Fenster-Event) | 服务已连接。目标包=…，已抑制=…（在下一个窗口事件时解析） | `com.noirdraco.pixelcomfort.ComfortAccessibilityService#onServiceConnected 硬编码 logcat 日志（仅调试日志，非用户界面）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。返回应用后 MainActivity.onResume 仅将内部刷新计数器 +1 以重新读取 SetupStatus；若仍关闭，设置行继续显示“Off · Turn on ‘PixelComfort auto-off’”，等待用户再次主动点击，不自动重跳系统设置、不弹窗、不通知轰炸。
- **遮罩叠层 / 高仿系统设置页**：无。无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；跳转目标为系统原生 ACTION_ACCESSIBILITY_SETTINGS 页面。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全包未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也未出现“进应用详情点右上角菜单允许受限设置”或 Session 安装器绕过文案；WRITE_SETTINGS 使用标准 android.settings.action.MANAGE_WRITE_SETTINGS + package: URI 授权页。
- **获权后即时行为与防撤权机制**：无。onServiceConnected 仅启动监听与监控、提交一次设置读取任务；未发现 GLOBAL_ACTION_BACK/HOME、未监听设置页阻止撤权、未自动点击确认；onDestroy/onUnbind 正常注销 Shizuku 监听并停止监控。
- **良性降级 / 替代方案**：具备。未授权无障碍时，首页显示“Setup incomplete”，AOD 相关开关提示“Permission missing”，hide_mobile 提示“Only works while ‘PixelComfort auto-off’ is on”；Comfort View 手动开关、私有 DNS 与显示设置等其余功能仍可用；Advanced 页另提供 Shizuku / MANAGE_WRITE_SETTINGS / WRITE_SECURE_SETTINGS 等替代授权路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到从 com.noirdraco.pixelcomfort.MainActivity 发出 action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 时立即拉起 UTG，并在用户返回 MainActivity 后 800ms 再抓一次；同时可在冷启动后直接抓 MainActivity 首屏以确认是否存在阻断式弹窗。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无明显盲区。文本全部为 strings.xml 原生字符串（Compose Text），无图片化诱导文案、无 WebView/远端 HTML、无加壳或加密载荷，UTG 可直接读取控件文本与层级；唯一需注意点是 Compose 语义树需开启 accessibility 语义导出才能完整抓取 SettingsRow 的 title/subtitle。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首屏（用于确认是否存在强制引导弹窗）** | package=com.noirdraco.pixelcomfort，Activity=MainActivity，Compose 渲染的“Setup incomplete”分组 + “Accessibility service / Off · Turn on ‘PixelComfort auto-off’”行 | 该页是判断“冷启动是否阻断/是否可跳过”的唯一依据；若首屏无弹窗且可滚动到其他功能，即可否定 TRIG_COLD_START_BLOCK | 是否存在 Dialog/PopupWindow 节点；是否存在“Cancel/Skip/Not now”按钮；设置行文本是否为“Off · Turn on ‘PixelComfort auto-off’” |
| **跳转前设置行（引导载体）** | MainActivity / AodScreen 内 title=“Accessibility service”、subtitle=“Off · Turn on ‘PixelComfort auto-off’”的可点击行 | 确认引导文字与点击动作是同一行原生控件，而非遮罩或 WebView 教学页 | 控件类名是否属于 Compose/Android View 而非 WebView；点击后是否直接进入系统设置（无中间页面） |
| **系统无障碍服务列表项（身份核验）** | com.android.settings 无障碍页，服务条目文本“PixelComfort auto-off” | 核对服务标签是否与真实应用名一致、说明文案是否与代码中 accessibility_service_description 一致，排除身份伪装 | 服务条目 label 文本；服务详情页描述文本全文；条目是否被置顶/自动打开 |
| **返回后状态页（拒权反馈核验）** | 返回 MainActivity 后的 Setup 分组状态 | 验证拒绝授权后是否发生死循环重跳、是否降级为可用状态 | 返回后是否再次自动跳转 ACCESSIBILITY_SETTINGS；是否出现不可取消 Dialog；其余功能控件是否仍可交互 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.noirdraco.pixelcomfort.ui.AodScreenKt$$ExternalSyntheticLambda35#invoke`
- `com.noirdraco.pixelcomfort.ui.AodScreenKt$$ExternalSyntheticLambda28#invoke`
- `com.noirdraco.pixelcomfort.ui.HomeScreenKt$$ExternalSyntheticLambda18#invoke`
- `com.noirdraco.pixelcomfort.ComfortAccessibilityService#onAccessibilityEvent`
- `com.noirdraco.pixelcomfort.ComfortAccessibilityService#onServiceConnected`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

- **静态可见性**：完全清晰。应用为 Compose 原生实现，无壳、无 WebView 引导页、无悬浮窗遮罩，无障碍申请流程全部在 `MainActivity` 的 Compose 设置页内完成。
- **无障碍服务能力极其克制**：`accessibility_service_config.xml` 仅订阅 `typeWindowStateChanged`，`canRetrieveWindowContent="false"`，且**显式声明 `isAccessibilityTool="false"`**（未伪造系统无障碍工具身份）。`onAccessibilityEvent` 只读取 `getPackageName()` / `getClassName()`，忽略自身包名与当前输入法包，用于判断前台应用是否在"相机/相册"名单内，从而暂停 Comfort View。
- **引导方式为"设置项 + 单次跳转"**：设置页内以一行 `SettingsRow` 呈现"Accessibility service — Off · Turn on “PixelComfort auto-off”"，点击后由 [AodScreenKt$$ExternalSyntheticLambda35.invoke](<resource-unit:#1.dex1 code:com.noirdraco.pixelcomfort.ui.AodScreenKt$$ExternalSyntheticLambda35#invoke>) 直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`。**未发现 `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转**，即没有"进应用详情→右上角菜单→允许受限设置"的 13+ 绕过教学。
- **无胁迫机制**：`MainActivity.onResume` 仅对刷新计数器加一（重新读取状态），不自动重跳设置页；无定时器循环、无不可取消 Dialog、无 `GLOBAL_ACTION_BACK/HOME` 阻止撤权、无获权后自动确认。用户可自由停留在主页并使用 Comfort View 手动开关等其余功能（降级路径明确）。
- **身份透明**：`app_name`=`PixelComfort`，无障碍标签 `PixelComfort auto-off`，描述逐条列出"关闭 Comfort View、按 Wi‑Fi 切私有 DNS、隐藏信号图标、按蓝牙/Wi‑Fi 切 AOD"，与 Manifest 权限（`WRITE_SECURE_SETTINGS`、`PACKAGE_USAGE_STATS`、`BLUETOOTH_CONNECT`、位置）一致，无同形字/空白挤出/多 alias。
- **受限权限说明**：`WRITE_SETTINGS` 走 `android.settings.action.MANAGE_WRITE_SETTINGS` + `package:` URI（标准授权页）；Comfort View 主开关则通过 **Shizuku** 说明"Android 不允许其他应用直接改该设置"，属真实技术约束的透明告知。
- **结论**：本应用不构成无障碍权限诱导/滥用。未登记风险（无成立命题）。覆盖边界：未做动态 UTG 实测（无在线设备依赖），上述均为静态代码与资源级确证。

---

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部静态可见：无加壳/VMP，无障碍引导逻辑为 Kotlin/Compose 编译产物（classes.dex + classes2.dex），界面文字来自 res/values/strings.xml，无远端 HTML、无 WebView、无加密载荷；仅 Shizuku 授权与系统设置页由系统组件承载。",
  "summary_one_liner": "在设置页以可点击的“Accessibility service — Off · Turn on ‘PixelComfort auto-off’”一行明示用途，用户点击后单次跳转系统无障碍列表自行开启，无弹窗胁迫、无重跳循环、无遮罩伪装，服务能力限于窗口切换事件且不读取窗口内容。",
  "disguise_identity": {
    "app_display_name": "PixelComfort",
    "claimed_brand_or_persona": "PixelComfort（F-Droid 开源应用，作者 NoirDraco，真实身份）",
    "a11y_service_label": "PixelComfort auto-off",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。R8 重命名仅产生 $$ExternalSyntheticLambda 合成类（常规 Kotlin/Compose 编译产物）；isAccessibilityTool 显式声明为 false，未伪造系统工具身份；未使用空白/换行挤出、同形字或多 activity-alias。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.noirdraco.pixelcomfort.MainActivity（单 Activity + ComposeView）",
      "trigger_event": "LAUNCHER 启动 → onCreate() → setContent(ComposableLambda)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Setup incomplete / Accessibility service / Off · Turn on “PixelComfort auto-off” / Shizuku isn’t running / Shizuku permission missing",
      "shown_text_zh": "设置未完成 / 无障碍服务 / 已关闭 · 请开启“PixelComfort auto-off” / Shizuku 未运行 / 缺少 Shizuku 权限",
      "user_action_requested": "冷启动不弹任何强制弹窗，仅首页“Setup”分组内以状态行展示未完成项，用户可自行滑动浏览或忽略；无取消/跳过按钮需求（因为不存在阻断）",
      "code_anchor": "com.noirdraco.pixelcomfort.MainActivity#onCreate；res/values/strings.xml（home_setup_needed、accessibility、accessibility_off）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "首页 Setup 分组 + AOD 页 AodSetup 分组中的 SettingsRow（Compose 行）",
      "trigger_event": "HomeScreenKt$$ExternalSyntheticLambda18.invoke 依据 SetupStatus.accessibilityEnabled 渲染该行；AodScreenKt$$ExternalSyntheticLambda28.invoke 依据 AodPerms.service 渲染",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility service | Off · Turn on “PixelComfort auto-off” | On",
      "shown_text_zh": "无障碍服务 | 已关闭 · 请开启“PixelComfort auto-off” | 已开启",
      "user_action_requested": "用户主动点击该行才会进入系统设置；不点击则停留在本页，其余功能（Comfort View 手动开关、私有 DNS、AOD 规则）仍可查看，缺失项仅显示“Permission missing”",
      "code_anchor": "com.noirdraco.pixelcomfort.ui.HomeScreenKt$$ExternalSyntheticLambda18#invoke；com.noirdraco.pixelcomfort.ui.AodScreenKt$$ExternalSyntheticLambda28#invoke；AodScreenKt.SettingsRow-mxsUjTo"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统“设置 → 无障碍 → 已下载的服务”列表页（ACTION_ACCESSIBILITY_SETTINGS）",
      "trigger_event": "用户点击该行 → Function0.invoke（$r8$classId=0/6/8 分支）→ context.startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Turns Comfort View off automatically while the camera or Photos app is in the foreground, and restores it when you leave. If you turn them on, it also switches private DNS by Wi‑Fi, hides the mobile signal icon on Wi‑Fi and switches the always-on display by Bluetooth device or Wi‑Fi.",
      "shown_text_zh": "当相机或“相册”应用在前台时自动关闭 Comfort View，离开时恢复。若你开启相应开关，它还会按 Wi‑Fi 切换私有 DNS、在 Wi‑Fi 下隐藏移动信号图标、按蓝牙设备或 Wi‑Fi 切换息屏显示。",
      "user_action_requested": "由用户自行在系统列表中点击“PixelComfort auto-off”并确认；应用未附加任何自动化点击或遮罩引导",
      "code_anchor": "com.noirdraco.pixelcomfort.ui.AodScreenKt$$ExternalSyntheticLambda35#invoke（case 0/6/8）；res/xml/accessibility_service_config.xml；res/values/strings.xml#accessibility_service_description"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity.onResume → ParcelableSnapshotMutableIntState.refresh 自增 → 重算 SetupStatus",
      "trigger_event": "从系统设置返回时 onResume() 触发一次状态刷新",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Off · Turn on “PixelComfort auto-off”",
      "shown_text_zh": "已关闭 · 请开启“PixelComfort auto-off”（保持原状态提示，不重跳、不弹窗）",
      "user_action_requested": "无强制动作；用户可直接退出或继续使用其他功能，不存在死循环重跳或不可取消弹窗",
      "code_anchor": "com.noirdraco.pixelcomfort.MainActivity#onResume"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.noirdraco.pixelcomfort.ComfortAccessibilityService",
      "trigger_event": "onServiceConnected() → 注册 Shizuku binder 监听、NetworkWatcher.start()、AodMonitor.start()、SettingsWorker.submit()；随后 onAccessibilityEvent(typeWindowStateChanged)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Dienst verbunden. Ziel-Packages=..., suppressed=... (Aufloesung beim naechsten Fenster-Event)",
      "shown_text_zh": "服务已连接。目标包=…，已抑制=…（在下一个窗口事件时解析）——仅写入 logcat，无界面呈现",
      "user_action_requested": "无需用户操作；服务只读取前台包名/类名，忽略自身包名与当前输入法，不读取窗口内容、不执行全局手势、不自动点击确认",
      "code_anchor": "com.noirdraco.pixelcomfort.ComfortAccessibilityService#onServiceConnected；#onAccessibilityEvent；#isIgnored；#onDestroy"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 首页“Setup”分组的 Compose SettingsRow 行（原生 Compose 文本，非 Dialog）：标题“Accessibility service”，副标题由 accessibility_off 模板填充为“Off · Turn on ‘PixelComfort auto-off’”，已开启时为“On”",
    "AOD 页 AodSetup 分组的同类 SettingsRow（AodScreenKt$$ExternalSyntheticLambda28），点击回调 AodScreenKt$$ExternalSyntheticLambda35 跳系统无障碍设置",
    "系统无障碍服务列表项：android:label=“PixelComfort auto-off”（res/values/strings.xml#accessibility_service_label）",
    "系统无障碍服务详情说明：android:description=accessibility_service_description（res/xml/accessibility_service_config.xml → @string/accessibility_service_description）",
    "Advanced（高级）页 Permissions 分组的 adv_permissions_footer 说明文字，解释为何 Comfort View 需经 Shizuku 修改",
    "Advanced 页“Modify system settings / Modify secure settings / Allow in system dialog”三项授权行，点击跳 MANAGE_WRITE_SETTINGS 系统页",
    "Advanced Protection（高级保护）模式提示 apm_title/apm_summary，告知该模式下系统会关闭无障碍服务，属真实系统机制说明",
    "AOD 规则页的权限理由文案：aod_bluetooth_text（“Needed to see which devices are connected. Never scans.”）、aod_location_text（“Your location is never used.”）",
    "Quick Settings 磁贴标签 qs_tile_label 与 hide_mobile_needs_service（“Only works while ‘%1$s’ is on”）",
    "未发现：WebView/HTML 页面、悬浮窗遮罩、全屏高仿系统无障碍开关页、通知栏诱导点击弹窗"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Turns Comfort View off automatically while the camera or Photos app is in the foreground, and restores it when you leave. If you turn them on, it also switches private DNS by Wi‑Fi, hides the mobile signal icon on Wi‑Fi and switches the always-on display by Bluetooth device or Wi‑Fi.",
      "text_zh": "当相机或“相册”应用在前台时自动关闭 Comfort View，离开时恢复。若你开启相应开关，它还会按 Wi‑Fi 切换私有 DNS、在 Wi‑Fi 下隐藏移动信号图标、按蓝牙设备或 Wi‑Fi 切换息屏显示。",
      "source_location": "res/values/strings.xml#accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用为 android:description）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Off · Turn on “%1$s”",
      "text_zh": "已关闭 · 请开启“%1$s”（运行时填充为“PixelComfort auto-off”）",
      "source_location": "res/values/strings.xml#accessibility_off（渲染于 AodScreenKt$$ExternalSyntheticLambda28 / HomeScreenKt$$ExternalSyntheticLambda18 的 SettingsRow）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility service",
      "text_zh": "无障碍服务",
      "source_location": "res/values/strings.xml#accessibility",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "PixelComfort auto-off",
      "text_zh": "PixelComfort 自动关闭（无障碍服务在系统列表中的显示名）",
      "source_location": "res/values/strings.xml#accessibility_service_label（AndroidManifest.xml service android:label）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "These permissions aren’t enough for Comfort View itself: Android doesn’t let other apps change that setting directly, so switching goes through Shizuku. Shizuku has to be started again after every restart.",
      "text_zh": "这些权限对 Comfort View 本身还不够：Android 不允许其他应用直接修改该设置，因此切换需经由 Shizuku 完成。每次重启后都需重新启动 Shizuku。",
      "source_location": "res/values/strings.xml#adv_permissions_footer（Advanced 页 Permissions 分组）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Android turns the accessibility service off in this mode. Turn Advanced Protection off to use the automation.",
      "text_zh": "在此模式下 Android 会关闭无障碍服务。若要使用自动化，请关闭“高级保护”。",
      "source_location": "res/values/strings.xml#apm_summary（配套 apm_title “Advanced Protection is on”）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Needed to see which devices are connected. Never scans.",
      "text_zh": "用于查看已连接的设备。从不扫描。",
      "source_location": "res/values/strings.xml#aod_bluetooth_text",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Android only reveals the Wi‑Fi name with the location permission. Your location is never used.",
      "text_zh": "Android 仅在授予位置权限后才显示 Wi‑Fi 名称。你的位置信息从不被使用。",
      "source_location": "res/values/strings.xml#aod_location_text",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "de",
      "text_verbatim": "Dienst verbunden. Ziel-Packages=%s, suppressed=%s (Aufloesung beim naechsten Fenster-Event)",
      "text_zh": "服务已连接。目标包=…，已抑制=…（在下一个窗口事件时解析）",
      "source_location": "com.noirdraco.pixelcomfort.ComfortAccessibilityService#onServiceConnected 硬编码 logcat 日志（仅调试日志，非用户界面）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。返回应用后 MainActivity.onResume 仅将内部刷新计数器 +1 以重新读取 SetupStatus；若仍关闭，设置行继续显示“Off · Turn on ‘PixelComfort auto-off’”，等待用户再次主动点击，不自动重跳系统设置、不弹窗、不通知轰炸。",
    "overlay_or_fake_settings": "无。无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；跳转目标为系统原生 ACTION_ACCESSIBILITY_SETTINGS 页面。",
    "restricted_settings_13plus_coaching": "无。全包未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也未出现“进应用详情点右上角菜单允许受限设置”或 Session 安装器绕过文案；WRITE_SETTINGS 使用标准 android.settings.action.MANAGE_WRITE_SETTINGS + package: URI 授权页。",
    "post_grant_anti_removal": "无。onServiceConnected 仅启动监听与监控、提交一次设置读取任务；未发现 GLOBAL_ACTION_BACK/HOME、未监听设置页阻止撤权、未自动点击确认；onDestroy/onUnbind 正常注销 Shizuku 监听并停止监控。",
    "benign_graceful_degradation": "具备。未授权无障碍时，首页显示“Setup incomplete”，AOD 相关开关提示“Permission missing”，hide_mobile 提示“Only works while ‘PixelComfort auto-off’ is on”；Comfort View 手动开关、私有 DNS 与显示设置等其余功能仍可用；Advanced 页另提供 Shizuku / MANAGE_WRITE_SETTINGS / WRITE_SECURE_SETTINGS 等替代授权路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到从 com.noirdraco.pixelcomfort.MainActivity 发出 action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 时立即拉起 UTG，并在用户返回 MainActivity 后 800ms 再抓一次；同时可在冷启动后直接抓 MainActivity 首屏以确认是否存在阻断式弹窗。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首屏（用于确认是否存在强制引导弹窗）",
        "page_identifier": "package=com.noirdraco.pixelcomfort，Activity=MainActivity，Compose 渲染的“Setup incomplete”分组 + “Accessibility service / Off · Turn on ‘PixelComfort auto-off’”行",
        "why_most_useful": "该页是判断“冷启动是否阻断/是否可跳过”的唯一依据；若首屏无弹窗且可滚动到其他功能，即可否定 TRIG_COLD_START_BLOCK",
        "observable_utg_signals": ["是否存在 Dialog/PopupWindow 节点", "是否存在“Cancel/Skip/Not now”按钮", "设置行文本是否为“Off · Turn on ‘PixelComfort auto-off’”"]
      },
      {
        "page_role": "跳转前设置行（引导载体）",
        "page_identifier": "MainActivity / AodScreen 内 title=“Accessibility service”、subtitle=“Off · Turn on ‘PixelComfort auto-off’”的可点击行",
        "why_most_useful": "确认引导文字与点击动作是同一行原生控件，而非遮罩或 WebView 教学页",
        "observable_utg_signals": ["控件类名是否属于 Compose/Android View 而非 WebView", "点击后是否直接进入系统设置（无中间页面）"]
      },
      {
        "page_role": "系统无障碍服务列表项（身份核验）",
        "page_identifier": "com.android.settings 无障碍页，服务条目文本“PixelComfort auto-off”",
        "why_most_useful": "核对服务标签是否与真实应用名一致、说明文案是否与代码中 accessibility_service_description 一致，排除身份伪装",
        "observable_utg_signals": ["服务条目 label 文本", "服务详情页描述文本全文", "条目是否被置顶/自动打开"]
      },
      {
        "page_role": "返回后状态页（拒权反馈核验）",
        "page_identifier": "返回 MainActivity 后的 Setup 分组状态",
        "why_most_useful": "验证拒绝授权后是否发生死循环重跳、是否降级为可用状态",
        "observable_utg_signals": ["返回后是否再次自动跳转 ACCESSIBILITY_SETTINGS", "是否出现不可取消 Dialog", "其余功能控件是否仍可交互"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无明显盲区。文本全部为 strings.xml 原生字符串（Compose Text），无图片化诱导文案、无 WebView/远端 HTML、无加壳或加密载荷，UTG 可直接读取控件文本与层级；唯一需注意点是 Compose 语义树需开启 accessibility 语义导出才能完整抓取 SettingsRow 的 title/subtitle。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.noirdraco.pixelcomfort.ui.AodScreenKt$$ExternalSyntheticLambda35#invoke",
    "com.noirdraco.pixelcomfort.ui.AodScreenKt$$ExternalSyntheticLambda28#invoke",
    "com.noirdraco.pixelcomfort.ui.HomeScreenKt$$ExternalSyntheticLambda18#invoke",
    "com.noirdraco.pixelcomfort.ComfortAccessibilityService#onAccessibilityEvent",
    "com.noirdraco.pixelcomfort.ComfortAccessibilityService#onServiceConnected",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>

# MB_030__47bb7f855c｜Teabot — QR Code Scanner: Add-On

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：170.0s

## 1. 一句话核心结论

- **核心申请方式**：以'QR Code Scanner: Add-On'二维码扫描插件为外壳，声明全量事件监听+读屏+手势的无障碍服务，但服务实现与全部引导页面流转均编译在加密载荷中，启动即由自定义 Application 解密加载，运行期引导方式静态不可见。
- **静态可见性说明**：Manifest、无障碍服务声明及其 accessibility-service XML 配置完整静态可见；但无障碍服务类 com.nnawozvvi.pamwhbawm.UIDNwaidobaWIODb、启动 Activity、注入 Activity 的全部实现类均不在 classes.dex 中（dex 内 com.nnawozvvi 零命中），由 com.honey.wine.g.attachBaseContext 调用 com.honey.wine.a 解密加载 assets/yftggfU/gg8GIauj91.68w（zlib 包裹 262045 字节，熵 7.995，无 dex/PK 魔数）的加密态载荷。因此无障碍引导页文案、ACTION_ACCESSIBILITY_SETTINGS 跳转点、弹窗/遮罩逻辑全部藏于加密载荷内，静态不可还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `47bb7f855cdf116c62499240089fa1b7a69585e8b7f639e192b9d038da4094cd` |
| 包名 / 年份 | `com.nnawozvvi.pamwhbawm` / 2022 |
| 家族 / 品类 | **Teabot**（同池样本数：1） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | QR Code Scanner: Add-On |
| 引导页宣称品牌/身份 | QR Code Scanner: Add-On（二维码扫描增强插件，无真实品牌授权，命名空间与实现包 com.honey.wine 完全无关） |
| 系统无障碍列表服务名 | 无（asclllservizio.xml 未声明 android:description，9 个业务 Activity 的 android:label 均为空字符串，系统无障碍列表中以空名称呈现） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍服务 XML 完全缺失 android:description 与 label，列表项无可读名称与说明；2) 全部 9 个业务 Activity 的 android:label 置为空字符串 ""，抹除组件可读名；3) 三套互不相关命名空间并存——桌面名 QR Code Scanner: Add-On、业务包 com.nnawozvvi.pamwhbawm、实现包 com.honey.wine，Application 类置于 com.honey.wine.g；4) 专用注入 Activity inject.uibwduIABuIaw 使用 singleTask+excludeFromRecents+Theme.NoTitleBar，不留最近任务痕迹；5) com.honey.wine.a 用整数 key 异或解密字符串常量表，DEX 字符串表中搜不到 accessibility/settings 等关键 API 明文。 |
| 无障碍服务类名 | `com.nnawozvvi.pamwhbawm.UIDNwaidobaWIODb` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.honey.wine.g（自定义 Application）→ 解密加载器 com.honey.wine.a → 启动 Activity com.nnawozvvi.pamwhbawm.WNiudwabNUDIba（Manifest 唯一 LAUNCHER 入口） | 进程创建时 attachBaseContext(Context) 回调 | 不可静态还原 | 无 | 无 | `com.honey.wine.g#attachBaseContext → com.honey.wine.a#a(Context)` |
| 2 | 冷启动入口 | com.nnawozvvi.pamwhbawm.WNiudwabNUDIba（LAUNCHER Activity，Manifest 无 label、无 theme 覆盖） | onCreate（Activity 实现类在加密载荷内，方法体不可静态取得） | 不可静态还原 | 无 | 不可静态还原 | `#1 manifest:components（activity com.nnawozvvi.pamwhbawm.WNiudwabNUDIba）` |
| 3 | 引导说明页 | 不可静态还原（预期为加密载荷内 Activity/Dialog；assets 下无本地引导 HTML，仅存在 AR 模型 eyes_close/*.mml、Lottie 配置 JSON、aigames/sConsole.html 控制台页等与引导无关的资源） | 不可静态还原 | 不可静态还原 | 无 | 不可静态还原 | `assets/ 目录全量核验（无 guide/instruction/a11y 类 HTML）；classes.dex 无 ACCESSIBILITY_SETTINGS 字符串` |
| 4 | 跳无障碍设置 | 预期为 android.settings.ACCESSIBILITY_SETTINGS 系统设置页，但发起跳转的代码位于加密载荷内 | 不可静态还原 | 系统无障碍页 | 无 | 不可静态还原 | `com.nnawozvvi.pamwhbawm.UIDNwaidobaWIODb（类体缺失）；res/xml/asclllservizio.xml` |
| 5 | 遮罩叠层指引 | com.nnawozvvi.pamwhbawm.inject.uibwduIABuIaw（singleTask、excludeFromRecents=true、Theme.NoTitleBar 的专用注入窗口） | 不可静态还原（预期由无障碍服务事件或 SYSTEM_ALERT_WINDOW 悬浮窗触发） | 悬浮窗Overlay | 无 | 不可静态还原 | `#1 manifest:components（activity com.nnawozvvi.pamwhbawm.inject.uibwduIABuIaw）` |
| 6 | 获权后动作 | com.nnawozvvi.pamwhbawm.UIDNwaidobaWIODb（无障碍服务，typeAllMask + canRetrieveWindowContent + canPerformGestures + flagRetrieveInteractiveWindows）+ receiver.AIUbawuidBAWUdi（priority 999 SMS_DELIVER/SMS_RECEIVED） | onAccessibilityEvent（方法体缺失，不可静态还原） | 不可静态还原 | 无 | 不可静态还原 | `#1 manifest:components；res/xml/asclllservizio.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：res/xml/asclllservizio.xml 未声明 android:description，服务无任何说明文字，列表中以空名称/无描述呈现（唯一的静态可见呈现位置）
- AndroidManifest.xml：9 个业务 Activity（util.AUInawiOBFA、nawIODnaiowdna、util.nidwoanAIOWDbwaiuBa、util.uaiwdBuaiwbdaD、inject.uibwduIABuIaw、ioNWOADnaoidWNaod、util.InioawndOIADNwaiond、opnoPAWNDioaNDW、WNiudwabNUDIba）的 android:label 均为空字符串，组件列表无可见名称
- classes.dex：未检出任何自研无障碍引导/权限说明文案（ACCESSIBILITY_SETTINGS 零命中，accessibility 相关 214 处全部来自 com.facebook.* 通用 SDK）
- assets/：无本地引导 HTML（aigames/sConsole.html 为 269 字节调试控制台页，非用户引导页）；引导文案预期位于加密载荷内，静态不可定位
- 运行期预期位置（不可静态证实）：WNiudwabNUDIba 内的原生引导页、inject.uibwduIABuIaw 无标题注入窗口的遮罩叠层、以及 SYSTEM_ALERT_WINDOW 悬浮窗

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | QR Code Scanner: Add-On | 二维码扫描器：附加组件 | `AndroidManifest.xml application android:label` | 清理工具伪装 |
| en | %1$s won't work unless you enable Google Play services. | %1$s 需要启用 Google Play 服务才能运行。 | `com.google.android.gms 通用 SDK 字符串资源（非本应用自研，不作为引导文案）` | 故障恐吓 |
| en | Get Google Play services | 获取 Google Play 服务 | `com.google.android.gms 通用 SDK 字符串资源（非本应用自研）` | 假更新 |
| en | android:accessibilityEventTypes="typeAllMask" android:canRetrieveWindowContent="true" android:canPerformGestures="true" android:accessibilityFlags="flagDefault\|flagIncludeNotImportantViews\|flagReportViewIds\|flagRetrieveInteractiveWindows" | 无障碍事件类型：全部掩码；可读取窗口内容：是；可执行手势：是；标志：默认\|包含非重要视图\|报告视图 ID\|检索交互窗口 | `res/xml/asclllservizio.xml（无 android:description，无 android:label）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：拒权反馈逻辑位于加密载荷内，classes.dex 中无 ACCESSIBILITY_SETTINGS 字符串、无相关 Activity 实现，无法判定是否存在 onResume 死循环重跳或定时器拉起
- **遮罩叠层 / 高仿系统设置页**：存在高疑叠层载体但内容不可见：inject.uibwduIABuIaw 为 singleTask + excludeFromRecents + Theme.NoTitleBar 的无标题不驻留最近任务窗口，配合 SYSTEM_ALERT_WINDOW 权限，具备叠放引导遮罩或高仿设置页的能力；实际窗口内容与是否覆盖系统无障碍页不可静态还原
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（跳转与教学文案均在加密载荷内，DEX 中无 APPLICATION_DETAILS_SETTINGS 的自研调用）
- **获权后即时行为与防撤权机制**：不可静态还原；但已确认 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED、优先级 999 的 SMS_DELIVER 接收器与 BOOT_COMPLETED/USER_PRESENT/PACKAGE_REMOVED 接收器，具备开机自启与卸载感知的常驻条件
- **良性降级 / 替代方案**：无（无任何降级路径或手动替代模式的静态证据，且不具备良性理由）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到应用进程发起 action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 瞬间立即抓屏（此跳转点位于加密载荷内，只能由运行期 Hook 捕获）；同时冷启动后 0–3 秒内高频连续抓帧，捕获 WNiudwabNUDIba 的引导页；从系统设置页返回后 800ms 内再抓一帧验证是否压栈遮罩或重跳。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：显著盲区：一阶段（引导页）与二阶段（获权后读屏/点击/短信外发）全部编译在 assets/yftggfU/gg8GIauj91.68w 加密载荷内，DEX 中不含无障碍服务类、不含 ACCESSIBILITY_SETTINGS 字符串，静态分析无法预览任何引导文案与时序；若引导采用纯图片/GIF 指引（assets 中存在 main_bottombtn_up.9.png 等九宫格图与 Lottie 动画库），UTG 文本提取将为空，必须启用 OCR 与图像比对。另注意本应用为 Android 原生而非 Flutter，但 DEX 内含大量 React Native/Facebook SDK 类，判定时勿将 com.facebook.* 的 openSettings/ACCESSIBILITY 相关代码误归本应用。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导页（一阶段）** | com.nnawozvvi.pamwhbawm.WNiudwabNUDIba，Manifest 无 label 无自定义 theme，实际 UI 由加密载荷构建 | 这是唯一由 Manifest 确证的用户可见入口，其界面文案与按钮数量直接决定是否属于不可取消的强制引导 | 是否存在仅一个确认按钮、无取消/跳过按钮；是否出现'开启无障碍'类按钮与指向设置页的箭头示意；是否以'扫描失败/权限不足'类文案作为开启理由；页面标题是否仍为 QR Code Scanner 或已切换为安全/清理类措辞 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务中，名称为空、无描述、开关关闭的条目（对应 UIDNwaidobaWIODb） | asclllservizio.xml 确认无 android:description，此页可直接证实应用刻意剥离可读标识以规避用户判断，是最强的身份规避证据 | 服务项显示名是否为空或仅为包名；是否缺少描述副标题；系统是否弹出'此服务可读取屏幕全部内容'的红色警示（Android 12+ 且非 isAccessibilityTool） |
| **跳转设置后压栈的遮罩/引导窗口** | com.nnawozvvi.pamwhbawm.inject.uibwduIABuIaw（singleTask、excludeFromRecents、Theme.NoTitleBar），或 TYPE_APPLICATION_OVERLAY 悬浮窗 | 该 Activity 的 singleTask+excludeFromRecents+NoTitleBar 组合是叠层指引页的强特征；若它确实覆盖在系统无障碍设置页之上，即构成典型的遮罩叠层诱导 | 系统设置页之上是否叠加无标题窗口；是否出现指向开关位置的手指/GIF/箭头指引；窗口是否遮挡系统'此服务可读取全部屏幕内容'警示；最近任务列表中是否确实看不到该窗口 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.honey.wine.g#attachBaseContext`
- `com.honey.wine.a#a(android.content.Context)`
- `com.nnawozvvi.pamwhbawm.UIDNwaidobaWIODb（Manifest 声明，类体缺失于 classes.dex）`
- `com.nnawozvvi.pamwhbawm.inject.uibwduIABuIaw（singleTask + excludeFromRecents + Theme.NoTitleBar）`
- `res/xml/asclllservizio.xml`
- `assets/yftggfU/gg8GIauj91.68w`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态定向核验）

**核心发现：无障碍引导流程的代码全部不在 `classes.dex` 内，被加密载荷承载，纯静态无法还原运行期 UTG 页面流转。**

**1. 无障碍服务声明存在但无实体类**
- Manifest 注册 `com.nnawozvvi.pamwhbawm.UIDNwaidobaWIODb`，`BIND_ACCESSIBILITY_SERVICE`，meta-data → [asclllservizio.xml](<resource-unit:#1 file:res/xml/asclllservizio.xml>)：`typeAllMask` + `canRetrieveWindowContent=true` + `canPerformGestures=true` + `flagRetrieveInteractiveWindows`，即**全量事件监听 + 读屏 + 手势点击**的完整木马能力面。
- 该 XML **无 `android:description`、无 `android:label`**，系统无障碍列表中该服务项显示为空白名称/无说明——这是刻意剥离可读标识的规避手法。
- 但 `classes.dex` 中检索 `com.nnawozvvi` / `UIDNwaidobaWIODb` / `AccessibilityService` / `onAccessibilityEvent` / `performGlobalAction` / `getRootInActiveWindow` **全部零命中**；`list_codebase(nnawozvvi)` 返回 0 个类。启动 Activity `WNiudwabNUDIba`、注入 Activity `inject.uibwduIABuIaw` 同样只有声明没有实现。

**2. 启动即解密加载（载荷加密确认）**
- [com.honey.wine.g#attachBaseContext](<resource-unit:#1.dex1 code:com.honey.wine.g#attachBaseContext>) 在 `super` 调用后立即执行 [com.honey.wine.a#a(Context)](<resource-unit:#1.dex1 code:com.honey.wine.a#a(android.content.Context))，传入 `sourceDir`/`dataDir`；该类含大量按整数 key 异或解密的字符串常量表（key=262/463/482/513/525…），是典型加固存根。
- [assets/yftggfU/gg8GIauj91.68w](<resource-unit:#1 file:assets/yftggfU/gg8GIauj91.68w>)：zlib 外壳 → 262045 字节内层，香农熵 **7.995**，无 `dex\n035`、无 `PK\x03\x04` 魔数 → **加密态 DEX/JAR**，静态不可解。

**3. 身份与伪装**
- 桌面名 `QR Code Scanner: Add-On`，`application` 为 `com.honey.wine.g`，业务包 `com.nnawozvvi.pamwhbawm` —— 三个互不相关的命名空间；9 个业务 Activity 的 `android:label` **全为空字符串**（`""`），用于在最近任务/组件列表中抹除可读名称。
- 专用注入 Activity `inject.uibwduIABuIaw`：`singleTask` + `excludeFromRecents` + `Theme.NoTitleBar` —— 不在最近任务留痕的无标题窗口，是叠层/遮罩类页面的典型配置。
- 权限组合 `READ_SMS/RECEIVE_SMS/SEND_SMS/WRITE_SMS/RECEIVE_MMS` + `SYSTEM_ALERT_WINDOW` + `QUERY_ALL_PACKAGES` + `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` + 优先级 999 的 `SMS_DELIVER` 接收器，与"二维码扫描插件"的功能陈述完全不符。

**4. 未闭合项（如实标注）**
- `android.settings.ACCESSIBILITY_SETTINGS` 在整个 DEX 中**零命中**；唯一的 `APPLICATION_DETAILS_SETTINGS` 出现在第三方 `com.facebook.react.modules.intent.IntentModule#openSettings`，属 React Native 通用 SDK，不能归责。
- 因此"跳无障碍设置"的实际跳转点、引导弹窗文案、拒权循环、遮罩叠层**全部编译在加密载荷内**，本次未能静态取得；`assets` 下仅剩 AR 引擎模型（`eyes_close/*.mml`）、Lottie/配置 JSON 等无引导文案的资源，无本地 HTML 教学页。

**5. UTG 捕获建议**
- 由于引导文案不在静态资源中，最佳判定点是**监测到 `ACTION_ACCESSIBILITY_SETTINGS` 的 `startActivity` 瞬间**立即抓屏，以及无障碍服务列表项（预期显示空名称、无说明的条目）。
- 次优：冷启动后 0–3 秒内连续抓帧，捕获 `Theme.NoTitleBar` 无标题 Activity 的引导页；以及从设置页返回后的 800ms 内抓帧验证是否压栈遮罩。
- 盲区：加密载荷导致一阶段（引导页）与二阶段（获权后动作）均不可静态预览；若载荷解密依赖远端下发或需动态脱壳环境，则必须依赖运行期 UTG。

---

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、无障碍服务声明及其 accessibility-service XML 配置完整静态可见；但无障碍服务类 com.nnawozvvi.pamwhbawm.UIDNwaidobaWIODb、启动 Activity、注入 Activity 的全部实现类均不在 classes.dex 中（dex 内 com.nnawozvvi 零命中），由 com.honey.wine.g.attachBaseContext 调用 com.honey.wine.a 解密加载 assets/yftggfU/gg8GIauj91.68w（zlib 包裹 262045 字节，熵 7.995，无 dex/PK 魔数）的加密态载荷。因此无障碍引导页文案、ACTION_ACCESSIBILITY_SETTINGS 跳转点、弹窗/遮罩逻辑全部藏于加密载荷内，静态不可还原。",
  "summary_one_liner": "以'QR Code Scanner: Add-On'二维码扫描插件为外壳，声明全量事件监听+读屏+手势的无障碍服务，但服务实现与全部引导页面流转均编译在加密载荷中，启动即由自定义 Application 解密加载，运行期引导方式静态不可见。",
  "disguise_identity": {
    "app_display_name": "QR Code Scanner: Add-On",
    "claimed_brand_or_persona": "QR Code Scanner: Add-On（二维码扫描增强插件，无真实品牌授权，命名空间与实现包 com.honey.wine 完全无关）",
    "a11y_service_label": "无（asclllservizio.xml 未声明 android:description，9 个业务 Activity 的 android:label 均为空字符串，系统无障碍列表中以空名称呈现）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍服务 XML 完全缺失 android:description 与 label，列表项无可读名称与说明；2) 全部 9 个业务 Activity 的 android:label 置为空字符串 \"\"，抹除组件可读名；3) 三套互不相关命名空间并存——桌面名 QR Code Scanner: Add-On、业务包 com.nnawozvvi.pamwhbawm、实现包 com.honey.wine，Application 类置于 com.honey.wine.g；4) 专用注入 Activity inject.uibwduIABuIaw 使用 singleTask+excludeFromRecents+Theme.NoTitleBar，不留最近任务痕迹；5) com.honey.wine.a 用整数 key 异或解密字符串常量表，DEX 字符串表中搜不到 accessibility/settings 等关键 API 明文。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.honey.wine.g（自定义 Application）→ 解密加载器 com.honey.wine.a → 启动 Activity com.nnawozvvi.pamwhbawm.WNiudwabNUDIba（Manifest 唯一 LAUNCHER 入口）",
      "trigger_event": "进程创建时 attachBaseContext(Context) 回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（此阶段为纯解密加载，不涉及界面）",
      "user_action_requested": "无",
      "code_anchor": "com.honey.wine.g#attachBaseContext → com.honey.wine.a#a(Context)"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.nnawozvvi.pamwhbawm.WNiudwabNUDIba（LAUNCHER Activity，Manifest 无 label、无 theme 覆盖）",
      "trigger_event": "onCreate（Activity 实现类在加密载荷内，方法体不可静态取得）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（Activity 类体缺失于 classes.dex，界面与文案不可静态还原）",
      "user_action_requested": "不可静态还原",
      "code_anchor": "#1 manifest:components（activity com.nnawozvvi.pamwhbawm.WNiudwabNUDIba）"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "不可静态还原（预期为加密载荷内 Activity/Dialog；assets 下无本地引导 HTML，仅存在 AR 模型 eyes_close/*.mml、Lottie 配置 JSON、aigames/sConsole.html 控制台页等与引导无关的资源）",
      "trigger_event": "不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（DEX 内未检出任何引导/权限说明文案；唯一相关的 Google Play services 系列字符串来自 com.google.android.gms 通用 SDK 资源，非本应用编写）",
      "user_action_requested": "不可静态还原",
      "code_anchor": "assets/ 目录全量核验（无 guide/instruction/a11y 类 HTML）；classes.dex 无 ACCESSIBILITY_SETTINGS 字符串"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "预期为 android.settings.ACCESSIBILITY_SETTINGS 系统设置页，但发起跳转的代码位于加密载荷内",
      "trigger_event": "不可静态还原",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（classes.dex 中 ACCESSIBILITY_SETTINGS 零命中；唯一 APPLICATION_DETAILS_SETTINGS 出现在第三方 com.facebook.react.modules.intent.IntentModule#openSettings，属 React Native 通用 SDK，不归责本应用）",
      "user_action_requested": "不可静态还原",
      "code_anchor": "com.nnawozvvi.pamwhbawm.UIDNwaidobaWIODb（类体缺失）；res/xml/asclllservizio.xml"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.nnawozvvi.pamwhbawm.inject.uibwduIABuIaw（singleTask、excludeFromRecents=true、Theme.NoTitleBar 的专用注入窗口）",
      "trigger_event": "不可静态还原（预期由无障碍服务事件或 SYSTEM_ALERT_WINDOW 悬浮窗触发）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（Activity 类体缺失，无法取得窗口内容与叠层时序）",
      "user_action_requested": "不可静态还原",
      "code_anchor": "#1 manifest:components（activity com.nnawozvvi.pamwhbawm.inject.uibwduIABuIaw）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.nnawozvvi.pamwhbawm.UIDNwaidobaWIODb（无障碍服务，typeAllMask + canRetrieveWindowContent + canPerformGestures + flagRetrieveInteractiveWindows）+ receiver.AIUbawuidBAWUdi（priority 999 SMS_DELIVER/SMS_RECEIVED）",
      "trigger_event": "onAccessibilityEvent（方法体缺失，不可静态还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（服务实现类缺失；仅能确认其声明具备全量事件监听、读屏与手势模拟能力，以及配套短信拦截/发送能力）",
      "user_action_requested": "不可静态还原",
      "code_anchor": "#1 manifest:components；res/xml/asclllservizio.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：res/xml/asclllservizio.xml 未声明 android:description，服务无任何说明文字，列表中以空名称/无描述呈现（唯一的静态可见呈现位置）",
    "AndroidManifest.xml：9 个业务 Activity（util.AUInawiOBFA、nawIODnaiowdna、util.nidwoanAIOWDbwaiuBa、util.uaiwdBuaiwbdaD、inject.uibwduIABuIaw、ioNWOADnaoidWNaod、util.InioawndOIADNwaiond、opnoPAWNDioaNDW、WNiudwabNUDIba）的 android:label 均为空字符串，组件列表无可见名称",
    "classes.dex：未检出任何自研无障碍引导/权限说明文案（ACCESSIBILITY_SETTINGS 零命中，accessibility 相关 214 处全部来自 com.facebook.* 通用 SDK）",
    "assets/：无本地引导 HTML（aigames/sConsole.html 为 269 字节调试控制台页，非用户引导页）；引导文案预期位于加密载荷内，静态不可定位",
    "运行期预期位置（不可静态证实）：WNiudwabNUDIba 内的原生引导页、inject.uibwduIABuIaw 无标题注入窗口的遮罩叠层、以及 SYSTEM_ALERT_WINDOW 悬浮窗"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "QR Code Scanner: Add-On",
      "text_zh": "二维码扫描器：附加组件",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "%1$s 需要启用 Google Play 服务才能运行。",
      "source_location": "com.google.android.gms 通用 SDK 字符串资源（非本应用自研，不作为引导文案）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Get Google Play services",
      "text_zh": "获取 Google Play 服务",
      "source_location": "com.google.android.gms 通用 SDK 字符串资源（非本应用自研）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "android:accessibilityEventTypes=\"typeAllMask\" android:canRetrieveWindowContent=\"true\" android:canPerformGestures=\"true\" android:accessibilityFlags=\"flagDefault|flagIncludeNotImportantViews|flagReportViewIds|flagRetrieveInteractiveWindows\"",
      "text_zh": "无障碍事件类型：全部掩码；可读取窗口内容：是；可执行手势：是；标志：默认|包含非重要视图|报告视图 ID|检索交互窗口",
      "source_location": "res/xml/asclllservizio.xml（无 android:description，无 android:label）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：拒权反馈逻辑位于加密载荷内，classes.dex 中无 ACCESSIBILITY_SETTINGS 字符串、无相关 Activity 实现，无法判定是否存在 onResume 死循环重跳或定时器拉起",
    "overlay_or_fake_settings": "存在高疑叠层载体但内容不可见：inject.uibwduIABuIaw 为 singleTask + excludeFromRecents + Theme.NoTitleBar 的无标题不驻留最近任务窗口，配合 SYSTEM_ALERT_WINDOW 权限，具备叠放引导遮罩或高仿设置页的能力；实际窗口内容与是否覆盖系统无障碍页不可静态还原",
    "restricted_settings_13plus_coaching": "无静态证据（跳转与教学文案均在加密载荷内，DEX 中无 APPLICATION_DETAILS_SETTINGS 的自研调用）",
    "post_grant_anti_removal": "不可静态还原；但已确认 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED、优先级 999 的 SMS_DELIVER 接收器与 BOOT_COMPLETED/USER_PRESENT/PACKAGE_REMOVED 接收器，具备开机自启与卸载感知的常驻条件",
    "benign_graceful_degradation": "无（无任何降级路径或手动替代模式的静态证据，且不具备良性理由）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到应用进程发起 action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 瞬间立即抓屏（此跳转点位于加密载荷内，只能由运行期 Hook 捕获）；同时冷启动后 0–3 秒内高频连续抓帧，捕获 WNiudwabNUDIba 的引导页；从系统设置页返回后 800ms 内再抓一帧验证是否压栈遮罩或重跳。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导页（一阶段）",
        "page_identifier": "com.nnawozvvi.pamwhbawm.WNiudwabNUDIba，Manifest 无 label 无自定义 theme，实际 UI 由加密载荷构建",
        "why_most_useful": "这是唯一由 Manifest 确证的用户可见入口，其界面文案与按钮数量直接决定是否属于不可取消的强制引导",
        "observable_utg_signals": ["是否存在仅一个确认按钮、无取消/跳过按钮", "是否出现'开启无障碍'类按钮与指向设置页的箭头示意", "是否以'扫描失败/权限不足'类文案作为开启理由", "页面标题是否仍为 QR Code Scanner 或已切换为安全/清理类措辞"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务中，名称为空、无描述、开关关闭的条目（对应 UIDNwaidobaWIODb）",
        "why_most_useful": "asclllservizio.xml 确认无 android:description，此页可直接证实应用刻意剥离可读标识以规避用户判断，是最强的身份规避证据",
        "observable_utg_signals": ["服务项显示名是否为空或仅为包名", "是否缺少描述副标题", "系统是否弹出'此服务可读取屏幕全部内容'的红色警示（Android 12+ 且非 isAccessibilityTool）"]
      },
      {
        "page_role": "跳转设置后压栈的遮罩/引导窗口",
        "page_identifier": "com.nnawozvvi.pamwhbawm.inject.uibwduIABuIaw（singleTask、excludeFromRecents、Theme.NoTitleBar），或 TYPE_APPLICATION_OVERLAY 悬浮窗",
        "why_most_useful": "该 Activity 的 singleTask+excludeFromRecents+NoTitleBar 组合是叠层指引页的强特征；若它确实覆盖在系统无障碍设置页之上，即构成典型的遮罩叠层诱导",
        "observable_utg_signals": ["系统设置页之上是否叠加无标题窗口", "是否出现指向开关位置的手指/GIF/箭头指引", "窗口是否遮挡系统'此服务可读取全部屏幕内容'警示", "最近任务列表中是否确实看不到该窗口"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "显著盲区：一阶段（引导页）与二阶段（获权后读屏/点击/短信外发）全部编译在 assets/yftggfU/gg8GIauj91.68w 加密载荷内，DEX 中不含无障碍服务类、不含 ACCESSIBILITY_SETTINGS 字符串，静态分析无法预览任何引导文案与时序；若引导采用纯图片/GIF 指引（assets 中存在 main_bottombtn_up.9.png 等九宫格图与 Lottie 动画库），UTG 文本提取将为空，必须启用 OCR 与图像比对。另注意本应用为 Android 原生而非 Flutter，但 DEX 内含大量 React Native/Facebook SDK 类，判定时勿将 com.facebook.* 的 openSettings/ACCESSIBILITY 相关代码误归本应用。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "LURE_UTILITY_CLEANER_DISGUISE"
  ],
  "code_anchors": [
    "com.honey.wine.g#attachBaseContext",
    "com.honey.wine.a#a(android.content.Context)",
    "com.nnawozvvi.pamwhbawm.UIDNwaidobaWIODb（Manifest 声明，类体缺失于 classes.dex）",
    "com.nnawozvvi.pamwhbawm.inject.uibwduIABuIaw（singleTask + excludeFromRecents + Theme.NoTitleBar）",
    "res/xml/asclllservizio.xml",
    "assets/yftggfU/gg8GIauj91.68w"
  ]
}
```

</details>

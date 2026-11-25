# MB_120__767c218be4｜TeaBot — QR-Code Scanner: Add-On

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：174.6s

## 1. 一句话核心结论

- **核心申请方式**：壳层 dex 反射注入二阶段载荷后，由不存在的 in.makaek.tezbak.UIDNwaidobaWIODb 无障碍服务配合伪装的“QR-Code Scanner: Add-On”身份在运行期完成无障碍引导，具体引导页文案与跳转时序静态不可还原。
- **静态可见性说明**：classes.dex 仅为壳层：Manifest 声明的全部 in.makaek.tezbak.* 组件（启动 Activity、无障碍服务、SMS 接收器、注入 Activity）在包内唯一 dex 中完全不存在，dex 字符串表无 tezbak/makaek/AccessibilityService/com.android.settings 任何痕迹。真实载荷由 com.stone.observe.IRhBiBuZoUrAiZjMfHtTyRrSzYtBaKuAdXcBwWeYqBlRqAuEr.attachBaseContext 经 getDir 私有目录 + 反射改写 BaseDexClassLoader.pathList 注入（NQlZrBjUpUkOkHnCwSbWaEx.lazyinflict），并在 onCreate 中用反射伪造 Application 替身。无障碍引导的弹窗文案、遮罩、拒绝循环与设置页教学全部位于该二阶段 DEX（或远端下发），静态不可见；assets 内亦无内嵌 dex 或加密引导 HTML。
- **命中的行为模式标签**：`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `767c218be4e7d2c99ee9c8b36128ac932d2dac0e3792ce638b804083f75e1096` |
| 包名 / 年份 | `com.stone.observe` / 2022 |
| 家族 / 品类 | **TeaBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | QR-Code Scanner: Add-On |
| 引导页宣称品牌/身份 | 二维码扫描工具（QR-Code Scanner: Add-On），实为 TeaBot 系银行木马 |
| 系统无障碍列表服务名 | 无标签，系统无障碍列表仅显示裸服务名 in.makaek.tezbak.UIDNwaidobaWIODb（res/xml/asclllservizio.xml 未声明 android:label 与 android:description） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置完全空白：asclllservizio.xml 仅有 accessibilityEventTypes/feedbackType/flags/canRetrieveWindowContent/canPerformGestures，缺失 android:description 与 android:label，系统列表中不显示任何用途说明；所有 Manifest 组件类名使用 in.makaek.tezbak 随机化无意义串（如 UIDNwaidobaWIODb、KAopneaoniAoiasM、uibwduIABuIaw）且包内不存在，配合 Application 类名超长随机串与整包类名逐字母拼接式混淆；4 个 Activity 声明 android:label=""（空白标签）；注入 Activity 声明 excludeFromRecents+singleTask+Theme.NoTitleBar 以无痕覆盖；无 activity-alias、无伪造 isAccessibilityTool 声明。 |
| 无障碍服务类名 | `in.makaek.tezbak.UIDNwaidobaWIODb` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.stone.observe.IRhBiBuZoUrAiZjMfHtTyRrSzYtBaKuAdXcBwWeYqBlRqAuEr（android:name 指定的 Application） | 进程启动即 attachBaseContext(Context) → getDir(ZKoIwZiPsLbPtFwXg,0) → cashkangaroo → NQlZrBjUpUkOkHnCwSbWaEx.lazyinflict 反射注入 dex；随后 onCreate() → decidespirit() 用 Class.forName 实例化替身 Application 并反射 invoke attachBaseContext/onCreate | 不可静态还原 | 无 | 无需用户操作，冷启动即触发 | `com.stone.observe.IRhBiBuZoUrAiZjMfHtTyRrSzYtBaKuAdXcBwWeYqBlRqAuEr.attachBaseContext / .onCreate；com.stone.observe.NQlZrBjUpUkOkHnCwSbWaEx.lazyinflict` |
| 2 | 业务功能触发 | in.makaek.tezbak.KAopneaoniAoiasM（Manifest LAUNCHER Activity，包内无对应类，实际由注入 dex 提供） | 用户点击桌面图标“QR-Code Scanner: Add-On”进入启动 Activity，此时执行的是二阶段注入代码 | 不可静态还原 | **原文**：无（代码不在包内，静态不可见）<br>**译注**：预期为伪装成二维码扫描工具的首页，实际呈现内容无法静态确认 | 不可静态还原 | `AndroidManifest.xml activity in.makaek.tezbak.KAopneaoniAoiasM（intent-filter MAIN/LAUNCHER）` |
| 3 | 跳无障碍设置 | in.makaek.tezbak.UIDNwaidobaWIODb（BIND_ACCESSIBILITY_SERVICE 服务，meta-data 指向 @xml/asclllservizio）+ 系统无障碍服务列表页 | 不可静态还原（壳层 dex 中不存在 ACTION_ACCESSIBILITY_SETTINGS 调用点，跳转逻辑在注入的二阶段 dex 内） | 系统无障碍页 | **原文**：无（asclllservizio.xml 未声明 android:description / android:label，系统列表项无可读说明文字）<br>**译注**：系统无障碍列表中仅呈现服务名 in.makaek.tezbak.UIDNwaidobaWIODb，无任何功能说明供用户判断 | 不可静态还原 | `res/xml/asclllservizio.xml；AndroidManifest.xml service in.makaek.tezbak.UIDNwaidobaWIODb` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 桌面/启动器：应用名 “QR-Code Scanner: Add-On”（AndroidManifest application android:label，为全包唯一可见文案）
- 系统无障碍服务列表：仅显示裸服务名 in.makaek.tezbak.UIDNwaidobaWIODb，res/xml/asclllservizio.xml 未配置 android:description 与 android:label，无任何说明文字
- res/values/strings.xml 仅含 Google Play Services 通用文案（Enable/Install/Update Google Play services），无引导、无恐吓、无隐私承诺类文本
- assets/ 内无本地 HTML/WebView 引导页，仅有 Lynx 引擎与广告相关资源（loader.js、lynx_core.js、omsdk_v1.js、kwLBB.json），未见引导文案
- 四个 Activity（in.makaek.tezbak.util.AUInawiOBFA、nawIODnaiowdna、util.nidwoanAIOWDbwaiuBa、util.uaiwdBuaiwbdaD）及注入 Activity inject.uibwduIABuIaw 均声明 android:label=""，运行时界面文案无法静态确认
- 推测的二阶段引导弹窗/遮罩/设置页教学文本位于运行期注入 dex，静态不可还原

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | QR-Code Scanner: Add-On | 二维码扫描器：附加组件 | `AndroidManifest.xml application android:label（硬编码于清单）` | 良性透明说明 |
| en | in.makaek.tezbak.UIDNwaidobaWIODb | 无意义随机串服务名（系统无障碍列表项显示名） | `AndroidManifest.xml service android:name + res/xml/asclllservizio.xml（无 label/description）` | 未知 |
| en | %1$s won't work unless you enable Google Play services. | 除非启用 Google Play 服务，否则 %1$s 无法运行。 | `res/values/strings.xml common_google_play_services_enable_text（GMS 标准库文案，非自研引导）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：壳层 dex 中无任何无障碍状态检测（isAccessibilityServiceEnabled）、无 ACTION_ACCESSIBILITY_SETTINGS 跳转点，也无 onResume/Timer 重跳逻辑，判定代码位于运行期注入的二阶段 dex 内
- **遮罩叠层 / 高仿系统设置页**：不可静态还原；但 Manifest 已声明 SYSTEM_ALERT_WINDOW、ACTION_MANAGE_OVERLAY_PERMISSION、WRITE_SETTINGS 权限，并内置 excludeFromRecents+singleTask+Theme.NoTitleBar 的注入 Activity（in.makaek.tezbak.inject.uibwduIABuIaw），具备叠层遮罩与无痕覆盖的能力基础，实际使用情况需动态确认
- **Android 13+ 受限设置（Restricted Settings）应对**：不可静态还原（Manifest targetSdkVersion=28，低于 30 的受限设置机制，且引导代码不在包内）
- **获权后即时行为与防撤权机制**：不可静态还原；但已声明 GET_TASKS、DISABLE_KEYGUARD、RECEIVE_BOOT_COMPLETED、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，并含 BOOT_COMPLETED/USER_PRESENT/PACKAGE_REMOVED 等广播接收器（in.makaek.tezbak.receiver.eifbiaFBAUIFB），具备保活与撤权对抗条件
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：应用进程启动并完成 Application.attachBaseContext 注入后，一旦监测到界面切换至系统无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS / 组件名 com.android.settings/.Settings$AccessibilitySettingsActivity），或监测到首个非壳层自绘 Activity（in.makaek.tezbak.KAopneaoniAoiasM）出现的瞬间即拉起 UTG；亦可直接监测 OVERLAY 窗口（TYPE_APPLICATION_OVERLAY/TYPE_SYSTEM_ALERT）创建事件，因遮罩层与设置页常同时出现。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区为一阶段壳：包内 classes.dex 不含任何 Manifest 声明的组件类，全部引导界面由运行期经反射改写 BaseDexClassLoader.pathList 注入的二阶段 dex 提供（亦可能从远端下载），因此纯静态无法获得任何引导文案与跳转时序。运行期 UTG 不受静态加壳阻挡，但需确保 UTG 启动时机晚于 Application.attachBaseContext 注入完成，否则可能仅捕获到壳层空窗口。另需注意 assets 内 Lynx/广告 SDK 资源为残留，非引导载体，勿误判。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项（无说明文本的裸服务名）** | 列表项文本 in.makaek.tezbak.UIDNwaidobaWIODb，无 subtitle/description 文本 | 该条目零说明文本是全包唯一可直接静态确认的“身份空白”证据，可印证 asclllservizio.xml 缺失 label/description 的伪装手法 | 节点文本等于 in.makaek.tezbak.UIDNwaidobaWIODb；该项无 contentDescription/description 子节点；存在开关控件且当前为关闭状态 |
| **跳转前的引导弹窗页（二阶段注入 dex 提供）** | 前台 Activity 非 com.stone.observe.* 与 in.makaek.tezbak.KAopneaoniAoiasM 之外的窗口，或含二维码扫描器品牌文案的 Dialog | 该页承载真正的诱导话术（恐吓/假更新/隐私承诺），是区分“诱导”与“良性说明”的决定性证据，静态完全不可见 | 弹窗无取消/关闭按钮（仅单个“去开启”按钮）；文案含 accessibility/无障碍/权限/开启 等关键词；点击后 intent 目标为 ACCESSIBILITY_SETTINGS |
| **设置页后压栈的半透明遮罩引导层** | 系统无障碍页之上的 TYPE_APPLICATION_OVERLAY 窗口，含箭头/手指指示图或半透明蒙层 | 遮罩叠层是 TeaBot 系教唆用户点开开关的典型手法，可验证 SYSTEM_ALERT_WINDOW 与无障碍跳转的联动 | 无障碍页上层存在其它包名的 overlay 窗口；overlay 内含指示箭头或“打开此开关”类文本；overlay 窗口不含可关闭控件 |
| **拒绝返回后的反馈页/循环重跳** | 从设置页返回后再次出现同一引导页或再次跳转 ACCESSIBILITY_SETTINGS | 确认是否存在不可取消的拒权循环，这是强制性与良性降级的分界 | onResume 后 1-2 秒内重复出现同一引导界面；多次返回仍无法退出到桌面；无“稍后再说/跳过”控件 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.stone.observe.IRhBiBuZoUrAiZjMfHtTyRrSzYtBaKuAdXcBwWeYqBlRqAuEr.attachBaseContext`
- `com.stone.observe.IRhBiBuZoUrAiZjMfHtTyRrSzYtBaKuAdXcBwWeYqBlRqAuEr.decidespirit`
- `com.stone.observe.NQlZrBjUpUkOkHnCwSbWaEx.lazyinflict`
- `res/xml/asclllservizio.xml`
- `AndroidManifest.xml（service in.makaek.tezbak.UIDNwaidobaWIODb / activity in.makaek.tezbak.KAopneaoniAoiasM）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**静态可见性判定：`packed_or_encrypted`（一阶段壳/Dropper，运行期反射注入 DEX）**

- **Manifest 与 DEX 严重不一致**：Manifest 声明的全部组件（`in.makaek.tezbak.KAopneaoniAoiasM` 启动 Activity、无障碍服务 `in.makaek.tezbak.UIDNwaidobaWIODb`、SMS 广播接收器、`in.makaek.tezbak.inject.uibwduIABuIaw` 注入 Activity 等）在包内唯一的 `classes.dex`（2.0 MB，724 类）中**一个都不存在**；`classes.dex` 的字符串表里 `tezbak` / `makaek` / `AccessibilityService` / `com.android.settings` 命中数均为 0，只有 `com.stone.observe.*`（229 类）、`com.mbridge.msdk`、`com.ss`、`com.paytm.pgsdk` 等壳与广告/SDK 残留。
- **壳加载链已还原**（[IRhBiBuZoUrAiZjMfHtTyRrSzYtBaKuAdXcBwWeYqBlRqAuEr.attachBaseContext()](<resource-unit:#1.dex1 code:com.stone.observe.IRhBiBuZoUrAiZjMfHtTyRrSzYtBaKuAdXcBwWeYqBlRqAuEr#attachBaseContext>)）：`getDir(ZKoIwZiPsLbPtFwXg, 0)` 取私有目录 → `gadgetorder(file)` → `conducthundred()` 判定 → `cashkangaroo()` → [NQlZrBjUpUkOkHnCwSbWaEx.lazyinflict()](<resource-unit:#1.dex1 code:com.stone.observe.NQlZrBjUpUkOkHnCwSbWaEx#lazyinflict>) → 反射取 `BaseDexClassLoader` 的 `pathList`/`dexElements` 字段并 `censusindustry()` 注入，即标准**反射式 DexClassLoader 内存加载**；同链在 `onCreate()` 中通过 `decidespirit()` 反射 `Class.forName(...).newInstance()` 伪造 `Application` 并 `invoke(attachBaseContext)`、`onCreate()` 完成替身接管。
- **无障碍引导链不可静态还原**：包内无任何 `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` / `ACTION_MANAGE_OVERLAY_PERMISSION` / `isAccessibilityServiceEnabled` 调用点，无本地 HTML/WebView 教学页（`assets/` 仅 Lynx/广告资源，无 dex、无加密引导页），`res/values/strings.xml` 只有 Google Play Services 文案；`res/xml/asclllservizio.xml` 仅声明 `typeAllMask` + `flagRetrieveInteractiveWindows` + `canPerformGestures`，**无 `android:description`、无 `android:label`**。
- **身份伪装**：桌面名为 `QR-Code Scanner: Add-On`（二维码扫描器），实际权限组合为 `READ_SMS/SEND_SMS/WRITE_SMS/RECEIVE_MMS` + `QUERY_ALL_PACKAGES` + `SYSTEM_ALERT_WINDOW` + `RECORD_AUDIO` + `REQUEST_INSTALL_PACKAGES`，并带 `SMS_DELIVER` 高优先级接收器与 `RESPOND_VIA_MESSAGE` 服务，符合 TeaBot 系银行木马（短信窃取+无障碍覆盖注入）特征。
- **覆盖边界**：真实 UTG 引导页（弹窗文案、遮罩、拒绝循环、13+ 受限设置教学）全部位于运行期从私有目录/远端注入的二阶段 DEX，静态无法取得；须动态脱壳或设备侧抓取。因引导命题证据未闭合，本轮未登记风险条目。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "classes.dex 仅为壳层：Manifest 声明的全部 in.makaek.tezbak.* 组件（启动 Activity、无障碍服务、SMS 接收器、注入 Activity）在包内唯一 dex 中完全不存在，dex 字符串表无 tezbak/makaek/AccessibilityService/com.android.settings 任何痕迹。真实载荷由 com.stone.observe.IRhBiBuZoUrAiZjMfHtTyRrSzYtBaKuAdXcBwWeYqBlRqAuEr.attachBaseContext 经 getDir 私有目录 + 反射改写 BaseDexClassLoader.pathList 注入（NQlZrBjUpUkOkHnCwSbWaEx.lazyinflict），并在 onCreate 中用反射伪造 Application 替身。无障碍引导的弹窗文案、遮罩、拒绝循环与设置页教学全部位于该二阶段 DEX（或远端下发），静态不可见；assets 内亦无内嵌 dex 或加密引导 HTML。",
  "summary_one_liner": "壳层 dex 反射注入二阶段载荷后，由不存在的 in.makaek.tezbak.UIDNwaidobaWIODb 无障碍服务配合伪装的“QR-Code Scanner: Add-On”身份在运行期完成无障碍引导，具体引导页文案与跳转时序静态不可还原。",
  "disguise_identity": {
    "app_display_name": "QR-Code Scanner: Add-On",
    "claimed_brand_or_persona": "二维码扫描工具（QR-Code Scanner: Add-On），实为 TeaBot 系银行木马",
    "a11y_service_label": "无标签，系统无障碍列表仅显示裸服务名 in.makaek.tezbak.UIDNwaidobaWIODb（res/xml/asclllservizio.xml 未声明 android:label 与 android:description）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置完全空白：asclllservizio.xml 仅有 accessibilityEventTypes/feedbackType/flags/canRetrieveWindowContent/canPerformGestures，缺失 android:description 与 android:label，系统列表中不显示任何用途说明；所有 Manifest 组件类名使用 in.makaek.tezbak 随机化无意义串（如 UIDNwaidobaWIODb、KAopneaoniAoiasM、uibwduIABuIaw）且包内不存在，配合 Application 类名超长随机串与整包类名逐字母拼接式混淆；4 个 Activity 声明 android:label=\"\"（空白标签）；注入 Activity 声明 excludeFromRecents+singleTask+Theme.NoTitleBar 以无痕覆盖；无 activity-alias、无伪造 isAccessibilityTool 声明。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.stone.observe.IRhBiBuZoUrAiZjMfHtTyRrSzYtBaKuAdXcBwWeYqBlRqAuEr（android:name 指定的 Application）",
      "trigger_event": "进程启动即 attachBaseContext(Context) → getDir(ZKoIwZiPsLbPtFwXg,0) → cashkangaroo → NQlZrBjUpUkOkHnCwSbWaEx.lazyinflict 反射注入 dex；随后 onCreate() → decidespirit() 用 Class.forName 实例化替身 Application 并反射 invoke attachBaseContext/onCreate",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该阶段无任何界面，仅静默完成载荷解密与 DEX 注入",
      "user_action_requested": "无需用户操作，冷启动即触发",
      "code_anchor": "com.stone.observe.IRhBiBuZoUrAiZjMfHtTyRrSzYtBaKuAdXcBwWeYqBlRqAuEr.attachBaseContext / .onCreate；com.stone.observe.NQlZrBjUpUkOkHnCwSbWaEx.lazyinflict"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "in.makaek.tezbak.KAopneaoniAoiasM（Manifest LAUNCHER Activity，包内无对应类，实际由注入 dex 提供）",
      "trigger_event": "用户点击桌面图标“QR-Code Scanner: Add-On”进入启动 Activity，此时执行的是二阶段注入代码",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（代码不在包内，静态不可见）",
      "shown_text_zh": "预期为伪装成二维码扫描工具的首页，实际呈现内容无法静态确认",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml activity in.makaek.tezbak.KAopneaoniAoiasM（intent-filter MAIN/LAUNCHER）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "in.makaek.tezbak.UIDNwaidobaWIODb（BIND_ACCESSIBILITY_SERVICE 服务，meta-data 指向 @xml/asclllservizio）+ 系统无障碍服务列表页",
      "trigger_event": "不可静态还原（壳层 dex 中不存在 ACTION_ACCESSIBILITY_SETTINGS 调用点，跳转逻辑在注入的二阶段 dex 内）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（asclllservizio.xml 未声明 android:description / android:label，系统列表项无可读说明文字）",
      "shown_text_zh": "系统无障碍列表中仅呈现服务名 in.makaek.tezbak.UIDNwaidobaWIODb，无任何功能说明供用户判断",
      "user_action_requested": "不可静态还原",
      "code_anchor": "res/xml/asclllservizio.xml；AndroidManifest.xml service in.makaek.tezbak.UIDNwaidobaWIODb"
    }
  ],
  "text_presentation_locations": [
    "桌面/启动器：应用名 “QR-Code Scanner: Add-On”（AndroidManifest application android:label，为全包唯一可见文案）",
    "系统无障碍服务列表：仅显示裸服务名 in.makaek.tezbak.UIDNwaidobaWIODb，res/xml/asclllservizio.xml 未配置 android:description 与 android:label，无任何说明文字",
    "res/values/strings.xml 仅含 Google Play Services 通用文案（Enable/Install/Update Google Play services），无引导、无恐吓、无隐私承诺类文本",
    "assets/ 内无本地 HTML/WebView 引导页，仅有 Lynx 引擎与广告相关资源（loader.js、lynx_core.js、omsdk_v1.js、kwLBB.json），未见引导文案",
    "四个 Activity（in.makaek.tezbak.util.AUInawiOBFA、nawIODnaiowdna、util.nidwoanAIOWDbwaiuBa、util.uaiwdBuaiwbdaD）及注入 Activity inject.uibwduIABuIaw 均声明 android:label=\"\"，运行时界面文案无法静态确认",
    "推测的二阶段引导弹窗/遮罩/设置页教学文本位于运行期注入 dex，静态不可还原"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "QR-Code Scanner: Add-On",
      "text_zh": "二维码扫描器：附加组件",
      "source_location": "AndroidManifest.xml application android:label（硬编码于清单）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "in.makaek.tezbak.UIDNwaidobaWIODb",
      "text_zh": "无意义随机串服务名（系统无障碍列表项显示名）",
      "source_location": "AndroidManifest.xml service android:name + res/xml/asclllservizio.xml（无 label/description）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "除非启用 Google Play 服务，否则 %1$s 无法运行。",
      "source_location": "res/values/strings.xml common_google_play_services_enable_text（GMS 标准库文案，非自研引导）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：壳层 dex 中无任何无障碍状态检测（isAccessibilityServiceEnabled）、无 ACTION_ACCESSIBILITY_SETTINGS 跳转点，也无 onResume/Timer 重跳逻辑，判定代码位于运行期注入的二阶段 dex 内",
    "overlay_or_fake_settings": "不可静态还原；但 Manifest 已声明 SYSTEM_ALERT_WINDOW、ACTION_MANAGE_OVERLAY_PERMISSION、WRITE_SETTINGS 权限，并内置 excludeFromRecents+singleTask+Theme.NoTitleBar 的注入 Activity（in.makaek.tezbak.inject.uibwduIABuIaw），具备叠层遮罩与无痕覆盖的能力基础，实际使用情况需动态确认",
    "restricted_settings_13plus_coaching": "不可静态还原（Manifest targetSdkVersion=28，低于 30 的受限设置机制，且引导代码不在包内）",
    "post_grant_anti_removal": "不可静态还原；但已声明 GET_TASKS、DISABLE_KEYGUARD、RECEIVE_BOOT_COMPLETED、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，并含 BOOT_COMPLETED/USER_PRESENT/PACKAGE_REMOVED 等广播接收器（in.makaek.tezbak.receiver.eifbiaFBAUIFB），具备保活与撤权对抗条件",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "应用进程启动并完成 Application.attachBaseContext 注入后，一旦监测到界面切换至系统无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS / 组件名 com.android.settings/.Settings$AccessibilitySettingsActivity），或监测到首个非壳层自绘 Activity（in.makaek.tezbak.KAopneaoniAoiasM）出现的瞬间即拉起 UTG；亦可直接监测 OVERLAY 窗口（TYPE_APPLICATION_OVERLAY/TYPE_SYSTEM_ALERT）创建事件，因遮罩层与设置页常同时出现。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项（无说明文本的裸服务名）",
        "page_identifier": "列表项文本 in.makaek.tezbak.UIDNwaidobaWIODb，无 subtitle/description 文本",
        "why_most_useful": "该条目零说明文本是全包唯一可直接静态确认的“身份空白”证据，可印证 asclllservizio.xml 缺失 label/description 的伪装手法",
        "observable_utg_signals": ["节点文本等于 in.makaek.tezbak.UIDNwaidobaWIODb", "该项无 contentDescription/description 子节点", "存在开关控件且当前为关闭状态"]
      },
      {
        "page_role": "跳转前的引导弹窗页（二阶段注入 dex 提供）",
        "page_identifier": "前台 Activity 非 com.stone.observe.* 与 in.makaek.tezbak.KAopneaoniAoiasM 之外的窗口，或含二维码扫描器品牌文案的 Dialog",
        "why_most_useful": "该页承载真正的诱导话术（恐吓/假更新/隐私承诺），是区分“诱导”与“良性说明”的决定性证据，静态完全不可见",
        "observable_utg_signals": ["弹窗无取消/关闭按钮（仅单个“去开启”按钮）", "文案含 accessibility/无障碍/权限/开启 等关键词", "点击后 intent 目标为 ACCESSIBILITY_SETTINGS"]
      },
      {
        "page_role": "设置页后压栈的半透明遮罩引导层",
        "page_identifier": "系统无障碍页之上的 TYPE_APPLICATION_OVERLAY 窗口，含箭头/手指指示图或半透明蒙层",
        "why_most_useful": "遮罩叠层是 TeaBot 系教唆用户点开开关的典型手法，可验证 SYSTEM_ALERT_WINDOW 与无障碍跳转的联动",
        "observable_utg_signals": ["无障碍页上层存在其它包名的 overlay 窗口", "overlay 内含指示箭头或“打开此开关”类文本", "overlay 窗口不含可关闭控件"]
      },
      {
        "page_role": "拒绝返回后的反馈页/循环重跳",
        "page_identifier": "从设置页返回后再次出现同一引导页或再次跳转 ACCESSIBILITY_SETTINGS",
        "why_most_useful": "确认是否存在不可取消的拒权循环，这是强制性与良性降级的分界",
        "observable_utg_signals": ["onResume 后 1-2 秒内重复出现同一引导界面", "多次返回仍无法退出到桌面", "无“稍后再说/跳过”控件"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区为一阶段壳：包内 classes.dex 不含任何 Manifest 声明的组件类，全部引导界面由运行期经反射改写 BaseDexClassLoader.pathList 注入的二阶段 dex 提供（亦可能从远端下载），因此纯静态无法获得任何引导文案与跳转时序。运行期 UTG 不受静态加壳阻挡，但需确保 UTG 启动时机晚于 Application.attachBaseContext 注入完成，否则可能仅捕获到壳层空窗口。另需注意 assets 内 Lynx/广告 SDK 资源为残留，非引导载体，勿误判。"
  },
  "behavior_pattern_tags": [
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.stone.observe.IRhBiBuZoUrAiZjMfHtTyRrSzYtBaKuAdXcBwWeYqBlRqAuEr.attachBaseContext",
    "com.stone.observe.IRhBiBuZoUrAiZjMfHtTyRrSzYtBaKuAdXcBwWeYqBlRqAuEr.decidespirit",
    "com.stone.observe.NQlZrBjUpUkOkHnCwSbWaEx.lazyinflict",
    "res/xml/asclllservizio.xml",
    "AndroidManifest.xml（service in.makaek.tezbak.UIDNwaidobaWIODb / activity in.makaek.tezbak.KAopneaoniAoiasM）"
  ]
}
```

</details>

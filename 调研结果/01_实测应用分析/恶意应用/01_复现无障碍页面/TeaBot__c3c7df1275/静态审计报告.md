# MB_121__c3c7df1275｜TeaBot — QR-Code Scanner: Add-On

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：143.5s

## 1. 一句话核心结论

- **核心申请方式**：以 TikTok 代码库改名伪装成扫码工具，Manifest 预埋无标签无说明但可读全屏并模拟手势的无障碍服务，真实引导界面藏在加密资产 mitggS.json 经反射 DexClassLoader 注入的二阶段载荷中。
- **静态可见性说明**：Manifest 声明的 in.makaek.tezbak.* 全部组件（无障碍服务 UIDNwaidobaWIODb、启动 Activity KAopneaoniAoiasM、inject 活动、短信接收器、Provider）在 classes.dex 中不存在任何对应类，引导 UI 与跳转逻辑均由运行期二阶段载荷提供；assets/mitggS.json 为 205KB 高熵非明文资产，且被 com.bracket.original.EWwUeLjZkGlCzGhGmBcZzLuLnPhKmFwMiMmEx#gapsuggest 的反射 DexClassLoader 注入骨架配套使用，推断为加密二阶段 Dex。可静态确认的仅有 Manifest 组件声明、无障碍配置 XML 能力项与权限集合。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c3c7df127552aa2594ad335d7cc955cb1274cc322455a89b1856a2adf9f83ded` |
| 包名 / 年份 | `com.bracket.original` / 2022 |
| 家族 / 品类 | **TeaBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | QR-Code Scanner: Add-On |
| 引导页宣称品牌/身份 | QR-Code Scanner: Add-On（二维码扫描工具类应用） |
| 系统无障碍列表服务名 | 服务自身未设 android:label，系统无障碍列表将回落显示应用名 QR-Code Scanner: Add-On 与包名 com.bracket.original，且无任何说明描述 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：5 个 Activity 及无障碍服务使用 android:label="" 空白标签挤出警告文本；无障碍配置缺失 description/label/settingsActivity 使系统列表零说明；Manifest 包名 com.bracket.original 与注入组件包名 in.makaek.tezbak 混用制造归属混淆；真实代码库为 com.ss.android.ugc.* TikTok 模块；资源命名 asclllservizio / nsrlllseclllcfg 与类名 EWwUeLjZkGlCzGhGmBcZzLuLnPhKmFwMiMmEx 长串随机字母混淆；方法内穿插 LMNGMYl/IchAUbM 垃圾算术死代码；加密资产 mitggS.json 全包无明文引用 |
| 无障碍服务类名 | `in.makaek.tezbak.UIDNwaidobaWIODb` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | in.makaek.tezbak.KAopneaoniAoiasM（MAIN/LAUNCHER，label 为空） | 用户点击桌面图标启动 | 不可静态还原 | **原文**：无（该 Activity 的 label 属性为空字符串，实现类不在 classes.dex 内）<br>**译注**：无静态可见文本；界面内容由运行期注入的二阶段代码渲染 | 不可静态确定 | `AndroidManifest.xml 中 activity in.makaek.tezbak.KAopneaoniAoiasM 的 MAIN/LAUNCHER intent-filter` |
| 2 | 引导说明页 | 疑似 in.makaek.tezbak.util.AUInawiOBFA / nawIODnaiowdna / util.nidwoanAIOWDbwaiuBa / util.uaiwdBuaiwbdaD（均 Theme.NoTitleBar、label 为空） | 启动后由二阶段代码按序 startActivity，具体触发点不可静态还原 | 不可静态还原 | 无 | 不可静态确定（是否含取消/跳过按钮需运行期 UTG 捕获） | `AndroidManifest.xml 中 4 个 label="" 且 theme=@android:style/Theme.NoTitleBar 的 activity 声明` |
| 3 | 跳无障碍设置 | 系统 Settings.ACTION_ACCESSIBILITY_SETTINGS 页面（目标服务 in.makaek.tezbak.UIDNwaidobaWIODb） | 二阶段代码发起无障碍设置跳转；DEX 内不含 ACTION_ACCESSIBILITY_SETTINGS 字面量，跳转常量在载荷内 | 系统无障碍页 | **原文**：无（服务未配置 android:description，系统列表项无说明文本）<br>**译注**：系统无障碍列表将显示应用名 QR-Code Scanner: Add-On 与包名，无任何功能说明 | 手动在系统列表中开启该服务开关 | `AndroidManifest.xml 中 service in.makaek.tezbak.UIDNwaidobaWIODb + res/xml/asclllservizio.xml` |
| 4 | 遮罩叠层指引 | in.makaek.tezbak.inject.uibwduIABuIaw（excludeFromRecents + singleTask + Theme.NoTitleBar） | 不可静态还原；该类不在 DEX 内，推测在服务开启回调或设置页压栈时拉起 | 不可静态还原 | 无 | 不可静态确定 | `AndroidManifest.xml 中 activity in.makaek.tezbak.inject.uibwduIABuIaw 的 excludeFromRecents/singleTask 声明` |
| 5 | 获权后动作 | in.makaek.tezbak.UIDNwaidobaWIODb 无障碍服务本体 | 系统绑定服务后 onServiceConnected 回调（实现不可见） | 不可静态还原 | 无 | 无（后台自动执行） | `res/xml/asclllservizio.xml 第 2 行能力属性` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 无障碍服务自身：res/xml/asclllservizio.xml 未声明 android:description 与 android:label，系统无障碍列表项呈现零说明文本，仅回落显示应用名 QR-Code Scanner: Add-On
- 启动 Activity in.makaek.tezbak.KAopneaoniAoiasM 的 android:label 为空字符串，桌面与最近任务不显示应用标题
- 4 个引导/注入类 Activity（AUInawiOBFA、nawIODnaiowdna、nidwoanAIOWDbwaiuBa、uaiwdBuaiwbdaD、inject.uibwduIABuIaw）均 label 为空且 Theme.NoTitleBar，无标题栏承载文本
- 应用级 android:label="QR-Code Scanner: Add-On" 是唯一静态可见的用户面文字，其余引导文案应在二阶段载荷经加密资产 mitggS.json 解密后渲染，静态不可定位
- assets 目录下无本地 HTML 引导页（loader.js / lynx_core.js / medialib.js 属 TikTok 运行时），故不存在本地 WebView 文案资源

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | QR-Code Scanner: Add-On | 二维码扫描器：附加组件 | `AndroidManifest.xml application 的 android:label` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原。Manifest 中 in.makaek.tezbak 全部组件类缺失，拒权后是否 onResume 重跳或定时拉起需运行期 UTG/日志确认；二阶段载荷需先从 mitggS.json 解密注入
- **遮罩叠层 / 高仿系统设置页**：存在高度可疑的注入承载组件 in.makaek.tezbak.inject.uibwduIABuIaw（excludeFromRecents + singleTask + Theme.NoTitleBar），具备设置页压栈遮罩的组件特征，但实现类不在 DEX 内，是否叠放半透明遮罩或高仿系统无障碍开关页无法静态确认；应用已申请 SYSTEM_ALERT_WINDOW 权限
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（DEX 内不含 ACTION_APPLICATION_DETAILS_SETTINGS / REQUEST_INSTALL_PACKAGES 引导文案）；targetSdkVersion=28 本身低于 Android 13 受限设置机制，故该分步教学必要性低
- **获权后即时行为与防撤权机制**：不可静态还原；无障碍配置申请 flagRetrieveInteractiveWindows 与 canPerformGestures，具备在设置页模拟 GLOBAL_ACTION_BACK/HOME 阻止撤权的技术前提，但实际调用位于二阶段载荷内未见实现
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到前台 Activity 切换为系统 Settings 无障碍页（com.android.settings/.Settings$AccessibilitySettings 或 .AccessibilitySettingsActivity）且调用方包为 com.bracket.original 的瞬间立即拉起 UTG；同时应在冷启动 KAopneaoniAoiasM 后 1 秒内预拉一次 UTG，用于捕获可能的直弹引导弹窗
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：本案核心引导逻辑不在静态代码内。Manifest 声明的 in.makaek.tezbak.* 全部类在 classes.dex 中缺失，需由反射 DexClassLoader 骨架从加密资产 mitggS.json（205KB 高熵、全包无明文引用）解密加载，故纯静态分析无法看到任何引导文案与跳转代码；但静态加壳不阻挡运行期 UTG，只要在首次冷启动时持续采集前台页面即可捕获真实引导界面。另需注意 targetSdkVersion=28，Android 13+ 受限设置引导场景可能不存在。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项** | 列表中出现服务名含 com.bracket.original 或 in.makaek.tezbak.UIDNwaidobaWIODb 的条目，且条目下方无任何功能说明副标题 | 该条目无 description 是本案最直接的静态可预期诱导证据：用户只能看到一个扫码工具申请全屏读取与手势控制，系统侧无任何解释文本 | 服务条目文本与包名 com.bracket.original / in.makaek.tezbak.UIDNwaidobaWIODb；条目无 summary/description 子文本；应用名显示为 QR-Code Scanner: Add-On 而非真实品牌 |
| **跳转前引导说明页** | 包 com.bracket.original 的 label 为空、无标题栏的 Activity（KAopneaoniAoiasM 或 util 包下 4 个活动之一） | 确定是否存在说明文案、是否有取消/跳过按钮，以及文案的修辞框架（假更新/故障恐吓/隐私承诺） | 页面所有 TextView 文本全文；是否存在「取消」「跳过」「稍后」按钮节点；是否出现非扫码业务的品牌词（银行、反诈、清理等） |
| **设置页后压栈遮罩页** | in.makaek.tezbak.inject.uibwduIABuIaw（excludeFromRecents、singleTask、无标题栏），表现为无障碍设置页之上叠加的半透明或高仿界面 | 区分「正常跳转」与「遮罩诱导点击/伪造系统开关」的关键，也是判定 COERCE_OVERLAY_STACK_ON_SETTINGS 的直接依据 | 无障碍设置页之上是否出现另一 Activity 窗口；遮罩层是否绘制指向开关位置的箭头/手指/高亮框；遮罩是否含伪造的系统确认按钮或「点击此处开启」提示 |
| **获权后回跳页** | 服务开启后自动回到的应用页面或悬浮窗 | 验证是否存在获权后立即执行敏感动作（读取短信、模拟点击、拉起安装器） | 是否弹出无障碍已开启的确认提示；是否立即出现悬浮窗或覆盖其他应用界面 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `AndroidManifest.xml: service in.makaek.tezbak.UIDNwaidobaWIODb (BIND_ACCESSIBILITY_SERVICE, meta-data @xml/asclllservizio)`
- `res/xml/asclllservizio.xml 第 2 行: typeAllMask + canRetrieveWindowContent + canPerformGestures + flagRetrieveInteractiveWindows，无 description/label`
- `AndroidManifest.xml: activity in.makaek.tezbak.inject.uibwduIABuIaw (excludeFromRecents, singleTask, Theme.NoTitleBar)`
- `com.bracket.original.EWwUeLjZkGlCzGhGmBcZzLuLnPhKmFwMiMmEx#gapsuggest`
- `com.bracket.original.EWwUeLjZkGlCzGhGmBcZzLuLnPhKmFwMiMmEx#madblanket`
- `assets/mitggS.json (205555 字节高熵加密载荷，无明文引用)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（累计 15 次工具调用，已达上限，停止探索）。核心结论如下。

## 一、总体结论

该 APK 的**无障碍引导界面在静态层面完全不可见**：Manifest 声明的所有 `in.makaek.tezbak.*` 组件（含无障碍服务 `UIDNwaidobaWIODb`、启动 Activity `KAopneaoniAoiasM`、短信接收器、Provider）**在 `classes.dex` 中不存在任何对应类**（DEX 实际只含 `com.bracket.*`、`com.ss.*`、`io.*`、`org.*` 共 708 个类）。这是典型的**一阶段宿主 + 二阶段动态投递**结构：

- 宿主代码是**字节跳动/TikTok 代码库**（`plugins.json` 列出 `com.ss.android.ugc.*` 全部 AAB 模块），却被改名为扫码工具 "QR-Code Scanner: Add-On"；
- [com.bracket.original.EWwUeLjZkGlCzGhGmBcZzLuLnPhKmFwMiMmEx#gapsuggest](<resource-unit:#1.dex1 code:com.bracket.original.EWwUeLjZkGlCzGhGmBcZzLuLnPhKmFwMiMmEx#gapsuggest>) 通过反射构造 `DexClassLoader`，并配合 `madblanket` 用 `Field.set` 把加载器塞进父加载器字段，属典型 Dex 注入骨架，穿插大量无意义算术混淆；
- [assets/mitggS.json](<resource-unit:#1 file:assets/mitggS.json>) 为 205KB 高熵非明文资产（首字节 `64 1d 2e 79 96 11 ab d8…`），全包内无任何明文引用，推断即加密的二阶段载荷。

## 二、无障碍相关的可确认静态事实

- 无障碍配置 [res/xml/asclllservizio.xml](<resource-unit:#1 file:res/xml/asclllservizio.xml#L2>)**无 `android:description`、无 `android:label`、无 `android:settingsActivity`**，却申请了 `typeAllMask` + `canRetrieveWindowContent=true` + `canPerformGestures=true` + `flagRetrieveInteractiveWindows`——即「界面上无任何说明文字，能力上可读全屏内容并模拟手势」。
- 启动 Activity `in.makaek.tezbak.KAopneaoniAoiasM` 及另外 4 个 Activity 均 `android:label=""`（空白标签），主题 `Theme.NoTitleBar`；`in.makaek.tezbak.inject.uibwduIABuIaw` 额外带 `excludeFromRecents` + `singleTask`，是典型的注入/遮罩承载页。
- 已声明 `REQUEST_INSTALL_PACKAGES`、`SYSTEM_ALERT_WINDOW`、`WRITE_SETTINGS`、`READ_SMS`/`SEND_SMS`/`RECEIVE_SMS`、`QUERY_ALL_PACKAGES`、`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`，与 TeaBot 家族能力面一致。
- 导出 Provider `com.klone.buratodonner`（`in.makaek.tezbak.util.SomeProvider`）与高优先级短信/开机广播接收器。

## 三、边界说明

引导弹窗、`ACTION_ACCESSIBILITY_SETTINGS` 跳转、遮罩叠层、拒权循环等**运行期页面流转逻辑均位于二阶段载荷内**，静态不可还原，故 `static_visibility="packed_or_encrypted"`；UTG 视角下的最佳取证点是「无障碍服务列表项本身」与「跳转设置瞬间的压栈页」。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest 声明的 in.makaek.tezbak.* 全部组件（无障碍服务 UIDNwaidobaWIODb、启动 Activity KAopneaoniAoiasM、inject 活动、短信接收器、Provider）在 classes.dex 中不存在任何对应类，引导 UI 与跳转逻辑均由运行期二阶段载荷提供；assets/mitggS.json 为 205KB 高熵非明文资产，且被 com.bracket.original.EWwUeLjZkGlCzGhGmBcZzLuLnPhKmFwMiMmEx#gapsuggest 的反射 DexClassLoader 注入骨架配套使用，推断为加密二阶段 Dex。可静态确认的仅有 Manifest 组件声明、无障碍配置 XML 能力项与权限集合。",
  "summary_one_liner": "以 TikTok 代码库改名伪装成扫码工具，Manifest 预埋无标签无说明但可读全屏并模拟手势的无障碍服务，真实引导界面藏在加密资产 mitggS.json 经反射 DexClassLoader 注入的二阶段载荷中。",
  "disguise_identity": {
    "app_display_name": "QR-Code Scanner: Add-On",
    "claimed_brand_or_persona": "QR-Code Scanner: Add-On（二维码扫描工具类应用）",
    "a11y_service_label": "服务自身未设 android:label，系统无障碍列表将回落显示应用名 QR-Code Scanner: Add-On 与包名 com.bracket.original，且无任何说明描述",
    "identity_mismatch": true,
    "obfuscation_tricks": "5 个 Activity 及无障碍服务使用 android:label=\"\" 空白标签挤出警告文本；无障碍配置缺失 description/label/settingsActivity 使系统列表零说明；Manifest 包名 com.bracket.original 与注入组件包名 in.makaek.tezbak 混用制造归属混淆；真实代码库为 com.ss.android.ugc.* TikTok 模块；资源命名 asclllservizio / nsrlllseclllcfg 与类名 EWwUeLjZkGlCzGhGmBcZzLuLnPhKmFwMiMmEx 长串随机字母混淆；方法内穿插 LMNGMYl/IchAUbM 垃圾算术死代码；加密资产 mitggS.json 全包无明文引用"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "in.makaek.tezbak.KAopneaoniAoiasM（MAIN/LAUNCHER，label 为空）",
      "trigger_event": "用户点击桌面图标启动",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（该 Activity 的 label 属性为空字符串，实现类不在 classes.dex 内）",
      "shown_text_zh": "无静态可见文本；界面内容由运行期注入的二阶段代码渲染",
      "user_action_requested": "不可静态确定",
      "code_anchor": "AndroidManifest.xml 中 activity in.makaek.tezbak.KAopneaoniAoiasM 的 MAIN/LAUNCHER intent-filter"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "疑似 in.makaek.tezbak.util.AUInawiOBFA / nawIODnaiowdna / util.nidwoanAIOWDbwaiuBa / util.uaiwdBuaiwbdaD（均 Theme.NoTitleBar、label 为空）",
      "trigger_event": "启动后由二阶段代码按序 startActivity，具体触发点不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无静态可见说明文字；包内 assets 亦无本地 HTML 引导页，仅有 TikTok 素材与字体",
      "user_action_requested": "不可静态确定（是否含取消/跳过按钮需运行期 UTG 捕获）",
      "code_anchor": "AndroidManifest.xml 中 4 个 label=\"\" 且 theme=@android:style/Theme.NoTitleBar 的 activity 声明"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统 Settings.ACTION_ACCESSIBILITY_SETTINGS 页面（目标服务 in.makaek.tezbak.UIDNwaidobaWIODb）",
      "trigger_event": "二阶段代码发起无障碍设置跳转；DEX 内不含 ACTION_ACCESSIBILITY_SETTINGS 字面量，跳转常量在载荷内",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（服务未配置 android:description，系统列表项无说明文本）",
      "shown_text_zh": "系统无障碍列表将显示应用名 QR-Code Scanner: Add-On 与包名，无任何功能说明",
      "user_action_requested": "手动在系统列表中开启该服务开关",
      "code_anchor": "AndroidManifest.xml 中 service in.makaek.tezbak.UIDNwaidobaWIODb + res/xml/asclllservizio.xml"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "in.makaek.tezbak.inject.uibwduIABuIaw（excludeFromRecents + singleTask + Theme.NoTitleBar）",
      "trigger_event": "不可静态还原；该类不在 DEX 内，推测在服务开启回调或设置页压栈时拉起",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无静态可见文本；该组件命名为 inject 且排除最近任务，符合设置页叠层引导/注入页特征，但实现不可见",
      "user_action_requested": "不可静态确定",
      "code_anchor": "AndroidManifest.xml 中 activity in.makaek.tezbak.inject.uibwduIABuIaw 的 excludeFromRecents/singleTask 声明"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "in.makaek.tezbak.UIDNwaidobaWIODb 无障碍服务本体",
      "trigger_event": "系统绑定服务后 onServiceConnected 回调（实现不可见）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无静态可见文本；配置声明 typeAllMask、canRetrieveWindowContent、canPerformGestures、flagRetrieveInteractiveWindows，具备全屏读取与手势模拟能力",
      "user_action_requested": "无（后台自动执行）",
      "code_anchor": "res/xml/asclllservizio.xml 第 2 行能力属性"
    }
  ],
  "text_presentation_locations": [
    "无障碍服务自身：res/xml/asclllservizio.xml 未声明 android:description 与 android:label，系统无障碍列表项呈现零说明文本，仅回落显示应用名 QR-Code Scanner: Add-On",
    "启动 Activity in.makaek.tezbak.KAopneaoniAoiasM 的 android:label 为空字符串，桌面与最近任务不显示应用标题",
    "4 个引导/注入类 Activity（AUInawiOBFA、nawIODnaiowdna、nidwoanAIOWDbwaiuBa、uaiwdBuaiwbdaD、inject.uibwduIABuIaw）均 label 为空且 Theme.NoTitleBar，无标题栏承载文本",
    "应用级 android:label=\"QR-Code Scanner: Add-On\" 是唯一静态可见的用户面文字，其余引导文案应在二阶段载荷经加密资产 mitggS.json 解密后渲染，静态不可定位",
    "assets 目录下无本地 HTML 引导页（loader.js / lynx_core.js / medialib.js 属 TikTok 运行时），故不存在本地 WebView 文案资源"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "QR-Code Scanner: Add-On",
      "text_zh": "二维码扫描器：附加组件",
      "source_location": "AndroidManifest.xml application 的 android:label",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原。Manifest 中 in.makaek.tezbak 全部组件类缺失，拒权后是否 onResume 重跳或定时拉起需运行期 UTG/日志确认；二阶段载荷需先从 mitggS.json 解密注入",
    "overlay_or_fake_settings": "存在高度可疑的注入承载组件 in.makaek.tezbak.inject.uibwduIABuIaw（excludeFromRecents + singleTask + Theme.NoTitleBar），具备设置页压栈遮罩的组件特征，但实现类不在 DEX 内，是否叠放半透明遮罩或高仿系统无障碍开关页无法静态确认；应用已申请 SYSTEM_ALERT_WINDOW 权限",
    "restricted_settings_13plus_coaching": "无静态证据（DEX 内不含 ACTION_APPLICATION_DETAILS_SETTINGS / REQUEST_INSTALL_PACKAGES 引导文案）；targetSdkVersion=28 本身低于 Android 13 受限设置机制，故该分步教学必要性低",
    "post_grant_anti_removal": "不可静态还原；无障碍配置申请 flagRetrieveInteractiveWindows 与 canPerformGestures，具备在设置页模拟 GLOBAL_ACTION_BACK/HOME 阻止撤权的技术前提，但实际调用位于二阶段载荷内未见实现",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到前台 Activity 切换为系统 Settings 无障碍页（com.android.settings/.Settings$AccessibilitySettings 或 .AccessibilitySettingsActivity）且调用方包为 com.bracket.original 的瞬间立即拉起 UTG；同时应在冷启动 KAopneaoniAoiasM 后 1 秒内预拉一次 UTG，用于捕获可能的直弹引导弹窗",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "列表中出现服务名含 com.bracket.original 或 in.makaek.tezbak.UIDNwaidobaWIODb 的条目，且条目下方无任何功能说明副标题",
        "why_most_useful": "该条目无 description 是本案最直接的静态可预期诱导证据：用户只能看到一个扫码工具申请全屏读取与手势控制，系统侧无任何解释文本",
        "observable_utg_signals": [
          "服务条目文本与包名 com.bracket.original / in.makaek.tezbak.UIDNwaidobaWIODb",
          "条目无 summary/description 子文本",
          "应用名显示为 QR-Code Scanner: Add-On 而非真实品牌"
        ]
      },
      {
        "page_role": "跳转前引导说明页",
        "page_identifier": "包 com.bracket.original 的 label 为空、无标题栏的 Activity（KAopneaoniAoiasM 或 util 包下 4 个活动之一）",
        "why_most_useful": "确定是否存在说明文案、是否有取消/跳过按钮，以及文案的修辞框架（假更新/故障恐吓/隐私承诺）",
        "observable_utg_signals": [
          "页面所有 TextView 文本全文",
          "是否存在「取消」「跳过」「稍后」按钮节点",
          "是否出现非扫码业务的品牌词（银行、反诈、清理等）"
        ]
      },
      {
        "page_role": "设置页后压栈遮罩页",
        "page_identifier": "in.makaek.tezbak.inject.uibwduIABuIaw（excludeFromRecents、singleTask、无标题栏），表现为无障碍设置页之上叠加的半透明或高仿界面",
        "why_most_useful": "区分「正常跳转」与「遮罩诱导点击/伪造系统开关」的关键，也是判定 COERCE_OVERLAY_STACK_ON_SETTINGS 的直接依据",
        "observable_utg_signals": [
          "无障碍设置页之上是否出现另一 Activity 窗口",
          "遮罩层是否绘制指向开关位置的箭头/手指/高亮框",
          "遮罩是否含伪造的系统确认按钮或「点击此处开启」提示"
        ]
      },
      {
        "page_role": "获权后回跳页",
        "page_identifier": "服务开启后自动回到的应用页面或悬浮窗",
        "why_most_useful": "验证是否存在获权后立即执行敏感动作（读取短信、模拟点击、拉起安装器）",
        "observable_utg_signals": [
          "是否弹出无障碍已开启的确认提示",
          "是否立即出现悬浮窗或覆盖其他应用界面"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：本案核心引导逻辑不在静态代码内。Manifest 声明的 in.makaek.tezbak.* 全部类在 classes.dex 中缺失，需由反射 DexClassLoader 骨架从加密资产 mitggS.json（205KB 高熵、全包无明文引用）解密加载，故纯静态分析无法看到任何引导文案与跳转代码；但静态加壳不阻挡运行期 UTG，只要在首次冷启动时持续采集前台页面即可捕获真实引导界面。另需注意 targetSdkVersion=28，Android 13+ 受限设置引导场景可能不存在。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "AndroidManifest.xml: service in.makaek.tezbak.UIDNwaidobaWIODb (BIND_ACCESSIBILITY_SERVICE, meta-data @xml/asclllservizio)",
    "res/xml/asclllservizio.xml 第 2 行: typeAllMask + canRetrieveWindowContent + canPerformGestures + flagRetrieveInteractiveWindows，无 description/label",
    "AndroidManifest.xml: activity in.makaek.tezbak.inject.uibwduIABuIaw (excludeFromRecents, singleTask, Theme.NoTitleBar)",
    "com.bracket.original.EWwUeLjZkGlCzGhGmBcZzLuLnPhKmFwMiMmEx#gapsuggest",
    "com.bracket.original.EWwUeLjZkGlCzGhGmBcZzLuLnPhKmFwMiMmEx#madblanket",
    "assets/mitggS.json (205555 字节高熵加密载荷，无明文引用)"
  ]
}
```

</details>

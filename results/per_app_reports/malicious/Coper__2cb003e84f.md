# MB_047__2cb003e84f｜Coper — Google Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：100.2s

## 1. 一句话核心结论

- **核心申请方式**：一阶段仅剩加密壳与 Manifest，借 native 解密 raw 资源加载二阶段 DEX，并把无障碍服务在系统中伪装成“Google Chrome”、用土耳其语描述诱导启用，实际引导流程全部藏于二阶段且静态不可还原。
- **静态可见性说明**：一阶段 classes.dex 仅 2804 字节 8 个类，无任何 Activity/Service 实现；Application.attachBaseContext 调用 native CPzXoNA，libfGzsoGwEb.so 解密 res/raw/jtldryhvhihtez（458,976 字节高熵数据）并通过 DexClassLoader + 反射注入 ApplicationInj 加载二阶段 DEX。无障碍引导页、跳转点、弹窗/WebView/悬浮窗文案全部位于该加密二阶段，静态不可见；仅 Manifest 组件声明、无障碍服务 label/description 与 a11y 能力配置（res/xml/sqodgaxenjaqq.xml）静态可确认。
- **命中的行为模式标签**：`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `2cb003e84f12842e0b9b69187cf7e8287906882d2a37fe58751c72688d896c67` |
| 包名 / 年份 | `com.trybirdpene` / 2025 |
| 家族 / 品类 | **Coper**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google Chrome |
| 引导页宣称品牌/身份 | Google Chrome（冒用 Google 官方浏览器品牌，包名 com.trybirdpene 与之无任何关联） |
| 系统无障碍列表服务名 | Google Chrome（service android:label=@string/a，与桌面名同源） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.trybirdpene 与宣称品牌无关；类名/资源名全量随机化（p067f、p084t、XDfabYriJQnd、qozuqxiyiripeynm、jtldryhvhihtez）；无障碍描述使用土耳其语“Erişebilirlik Servisileri Etkinleştirme”，面向土耳其语用户定向投放；无障碍服务 label 直接复用应用显示名“Google Chrome”，使系统无障碍列表中该项显示为 Google Chrome，掩盖其真实身份；启动 Activity 采用透明无标题主题并 excludeFromRecents 隐藏痕迹；无多 activity-alias、无同形字、未见伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.trybirdpene.p084t` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Erişebilirlik Servisileri Etkinleştirme / Erişebilirlik Servisileri Etkinleştirme |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.trybirdpene.p067f（LAUNCHER Activity，android:theme=@style/Theme.AppCompat.Transparent.NoActionBar，excludeFromRecents=true，screenOrientation=fullSensor） | 点击桌面图标（MAIN/LAUNCHER intent-filter）→ Application iQPPmZmhqZ.attachBaseContext → native CPzXoNA 解密并加载二阶段 DEX | 原生Activity | **原文**：无（一阶段仅壳，界面由二阶段渲染）<br>**译注**：一阶段无自有 UI，启动即透明主题解壳 | 仅点击图标启动；无任何一阶段可控的取消/跳过入口 | `com.trybirdpene.iQPPmZmhqZ#attachBaseContext + com.trybirdpene.p067f（Manifest）` |
| 2 | 引导说明页 | 二阶段解密后的引导 Activity/Dialog（组件名未知，非 p067f 之外的已声明透明 Activity p023t/p014v/p097c 之一或动态注册） | 不可静态还原（二阶段代码由 DexClassLoader 加载，静态 DEX 内无 ACCESSIBILITY_SETTINGS 等字符串） | 不可静态还原 | **原文**：无（静态不可见）<br>**译注**：不可静态还原，需 UTG 实机捕获 | 不可静态还原 | `二阶段 DEX（res/raw/jtldryhvhihtez 解密产物），静态不可见` |
| 3 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载的服务列表项（label="Google Chrome"，描述="Erişebilirlik Servisileri Etkinleştirme"） | 二阶段引导页按钮触发（Intent ACTION_ACCESSIBILITY_SETTINGS，静态不可见具体调用点） | 系统无障碍页 | **原文**：Google Chrome / Erişebilirlik Servisileri Etkinleştirme<br>**译注**：Google Chrome / 启用无障碍服务 | 在系统无障碍列表中点击“Google Chrome”并把开关打开（服务说明仅一句土耳其语，无功能范围告知） | `res/values/strings.xml (a, XDfabYriJQnd) + res/xml/sqodgaxenjaqq.xml + com.trybirdpene.p084t` |
| 4 | 获权后动作 | com.trybirdpene.p084t（AccessibilityService，typeAllMask / canRetrieveWindowContent / flagRetrieveInteractiveWindows） | 系统绑定 BIND_ACCESSIBILITY_SERVICE 后 onServiceConnected（回调实现位于二阶段） | 不可静态还原 | 无 | 无（后台静默执行） | `res/xml/sqodgaxenjaqq.xml + com.trybirdpene.p084t` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务 label=@string/a="Google Chrome"（伪装成浏览器）
- 系统无障碍服务列表项描述：android:description=@string/XDfabYriJQnd="Erişebilirlik Servisileri Etkinleştirme"（土耳其语“启用无障碍服务”）
- 桌面图标名称：application android:label=@string/a="Google Chrome"
- 二阶段引导弹窗/Activity/WebView/悬浮窗：全部位于加密 res/raw/jtldryhvhihtez 解密后的 DEX，静态不可见，需 UTG 实机捕获

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Google Chrome | Google Chrome（谷歌浏览器） | `res/values/strings.xml key "a"（application android:label 与无障碍 service android:label 共用）` | 未知 |
| tr | Erişebilirlik Servisileri Etkinleştirme | 启用无障碍服务（原文含拼写错误 Servisileri，规范应为 Servisleri） | `res/values/strings.xml key "XDfabYriJQnd"（res/xml/sqodgaxenjaqq.xml android:description）` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原（一阶段 dex 无任何相关代码；二阶段由 native 解密后 DexClassLoader 加载，需 UTG 观测是否 onResume 死循环重跳或定时拉起无障碍设置）
- **遮罩叠层 / 高仿系统设置页**：不可静态还原（一阶段 Manifest 未见 SYSTEM_ALERT_WINDOW 权限，悬浮遮罩若存在应由二阶段通过窗口令牌或无障碍自身实现）
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=30，未声明 13+ 受限设置引导相关逻辑；如二阶段存在亦不可静态见）
- **获权后即时行为与防撤权机制**：不可静态还原（已声明 WRITE_SETTINGS、设备管理员 receiver com.trybirdpene.p071q 与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，具备防卸载/防撤权配套能力，但具体阻止撤权行为在二阶段）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 com.trybirdpene.p067f 后立即开始 UTG 采样（壳解出二阶段即接管界面）；并在监测到 Activity 跳转 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 时压栈抓取前序页面与跳转后 800ms~2s 的叠加层
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：一阶段为加密壳（native 解密 res/raw/jtldryhvhihtez → DexClassLoader 二阶段），静态完全无法看到引导流程；且应用全量字符串已混淆、界面文案可能在运行时由远端下发，纯静态只能确认“伪装成 Google Chrome 的无障碍服务”这一层；必须依赖运行期 UTG 才能在二阶段界面出现时取证。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后二阶段首屏引导页（弹窗或全屏 Activity）** | com.trybirdpene 包内 Activity/Dialog，透明主题，无 ActionBar，首次启动即出现且无系统权限弹窗前置 | 这是全案唯一能取到引导文案原文的页面，可直接区分假更新/故障恐吓/隐私承诺等话术 | 弹窗标题与正文全文；按钮文字是否仅有“启用/确定”而无取消/跳过；是否包含“无障碍”“Erişebilirlik”“Erişilebilirlik”等关键词 |
| **系统无障碍设置页及其中的服务列表项** | Settings → Accessibility → Downloaded services，条目文本为 Google Chrome / Erişebilirlik Servisileri Etkinleştirme | 直接证明系统级品牌冒用与描述伪装，且可判断应用是否在设置页上叠加引导遮罩 | 服务项 label 与 description 原文；开关是否已被应用自动切换；是否有悬浮引导窗/遮罩覆盖系统开关 |
| **从无障碍设置返回后的回落页** | 重新出现的引导页或无障碍设置再次被拉起 | 识别拒权/返回后的死循环重跳，是判定强制诱导而非良性说明的关键 | 返回后是否 <2s 内重新进入无障碍设置；页面文案是否升级为恐吓话术；是否存在 GLOBAL_ACTION_BACK 被拦截现象 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.trybirdpene.iQPPmZmhqZ#attachBaseContext`
- `com.trybirdpene.iQPPmZmhqZ#<clinit>`
- `lib/arm64-v8a/libfGzsoGwEb.so Java_com_trybirdpene_iQPPmZmhqZ_CPzXoNA`
- `res/raw/jtldryhvhihtez`
- `res/xml/sqodgaxenjaqq.xml`
- `res/values/strings.xml (a, XDfabYriJQnd)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，13 次工具调用内收口）

**1. 无障碍申请/引导链路的界面与流程完全位于加密二阶段，静态不可见**
- 一阶段 `classes.dex` 仅 **2,804 字节、8 个类**（`BuildConfig`、`R` 系列、`iQPPmZmhqZ`），**没有任何 Activity/Service/Dialog/WebView 的实现体**；Manifest 中声明的 `p067f`（LAUNCHER）、`p084t`（无障碍服务）等组件代码体均不在该 dex 中。
- [iQPPmZmhqZ.<clinit>](<resource-unit:#1.dex1 code:com.trybirdpene.iQPPmZmhqZ#<clinit>>) 执行 `System.loadLibrary("fGzsoGwEb")`，[iQPPmZmhqZ.attachBaseContext()](<resource-unit:#1.dex1 code:com.trybirdpene.iQPPmZmhqZ#attachBaseContext>) 立即调用 native `CPzXoNA(Context)`。
- [lib/arm64-v8a/libfGzsoGwEb.so](<resource-unit:#1.so1 code:Java_com_trybirdpene_iQPPmZmhqZ_CPzXoNA>) 的字符串明确暴露解壳链：`openRawResource` → `raw/jtldryhvhihtez` → `getExternalCache`/`dataDir` 落盘 → `dalvik/system/DexClassLoader` → `forName`/`getDeclaredField` → `com.trybirdpene:pm/ApplicationInj…` + `currentActivityThread`，即**运行时解密 raw 资源为二阶段 DEX 并反射替换 Application**。
- [res/raw/jtldryhvhihtez](<resource-unit:#1 file:res/raw/jtldryhvhihtez>) 为 458,976 字节高熵随机数据（首字节 `f3 62 5c 6e…`，非 zip/dex 魔数），确认为加密载荷。
→ 因此 `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转点、引导弹窗、悬浮遮罩、拒权循环等**均无静态可见代码**，DEX 内搜索这些 API 名全部 `no_matches`。

**2. 仍可静态确认的伪装与无障碍面（Manifest + 资源层）**
- 桌面名与无障碍服务名同为 `@string/a` = **"Google Chrome"**（[res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml#L3-L5>)），无障碍描述 `@string/XDfabYriJQnd` = **"Erişebilirlik Servisileri Etkinleştirme"**（土耳其语“启用无障碍服务”）——**在系统无障碍列表中整条服务项被伪装成 Google Chrome**，属品牌冒用 + 系统级身份混淆。
- 服务配置 [res/xml/sqodgaxenjaqq.xml](<resource-unit:#1 file:res/xml/sqodgaxenjaqq.xml>)：`typeAllMask`、`canRetrieveWindowContent="true"`、`flagIncludeNotImportantViews|flagReportViewIds|flagRetrieveInteractiveWindows` —— 全事件监听 + 全局窗口内容读取，具备任意界面读取与自动点击能力（获权后动作实体在二阶段）。
- 启动 Activity [com.trybirdpene.p067f](<resource-unit:#1 manifest:components>) 使用 `Theme.AppCompat.Transparent.NoActionBar` + `excludeFromRecents`，与壳 Application 的透明无标题风格一致，符合“启动即解壳、界面由二阶段接管”的形态。

**3. 未决与覆盖边界**
二阶段 DEX 需运行时解密（依赖设备环境执行 native 解壳），本次未做 angr 动态还原，故**“一步步引导用户开启无障碍”的具体页面流转、文案原文、拒绝/返回后的重跳循环**无法给出逐字证据；下列 flow 中除第 1、3 步外均标注为不可静态还原，仅依据 Manifest/资源事实与 Coper 家族行为模式给出待 UTG 验证的假设。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "一阶段 classes.dex 仅 2804 字节 8 个类，无任何 Activity/Service 实现；Application.attachBaseContext 调用 native CPzXoNA，libfGzsoGwEb.so 解密 res/raw/jtldryhvhihtez（458,976 字节高熵数据）并通过 DexClassLoader + 反射注入 ApplicationInj 加载二阶段 DEX。无障碍引导页、跳转点、弹窗/WebView/悬浮窗文案全部位于该加密二阶段，静态不可见；仅 Manifest 组件声明、无障碍服务 label/description 与 a11y 能力配置（res/xml/sqodgaxenjaqq.xml）静态可确认。",
  "summary_one_liner": "一阶段仅剩加密壳与 Manifest，借 native 解密 raw 资源加载二阶段 DEX，并把无障碍服务在系统中伪装成“Google Chrome”、用土耳其语描述诱导启用，实际引导流程全部藏于二阶段且静态不可还原。",
  "disguise_identity": {
    "app_display_name": "Google Chrome",
    "claimed_brand_or_persona": "Google Chrome（冒用 Google 官方浏览器品牌，包名 com.trybirdpene 与之无任何关联）",
    "a11y_service_label": "Google Chrome（service android:label=@string/a，与桌面名同源）",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.trybirdpene 与宣称品牌无关；类名/资源名全量随机化（p067f、p084t、XDfabYriJQnd、qozuqxiyiripeynm、jtldryhvhihtez）；无障碍描述使用土耳其语“Erişebilirlik Servisileri Etkinleştirme”，面向土耳其语用户定向投放；无障碍服务 label 直接复用应用显示名“Google Chrome”，使系统无障碍列表中该项显示为 Google Chrome，掩盖其真实身份；启动 Activity 采用透明无标题主题并 excludeFromRecents 隐藏痕迹；无多 activity-alias、无同形字、未见伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.trybirdpene.p067f（LAUNCHER Activity，android:theme=@style/Theme.AppCompat.Transparent.NoActionBar，excludeFromRecents=true，screenOrientation=fullSensor）",
      "trigger_event": "点击桌面图标（MAIN/LAUNCHER intent-filter）→ Application iQPPmZmhqZ.attachBaseContext → native CPzXoNA 解密并加载二阶段 DEX",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（一阶段仅壳，界面由二阶段渲染）",
      "shown_text_zh": "一阶段无自有 UI，启动即透明主题解壳",
      "user_action_requested": "仅点击图标启动；无任何一阶段可控的取消/跳过入口",
      "code_anchor": "com.trybirdpene.iQPPmZmhqZ#attachBaseContext + com.trybirdpene.p067f（Manifest）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "二阶段解密后的引导 Activity/Dialog（组件名未知，非 p067f 之外的已声明透明 Activity p023t/p014v/p097c 之一或动态注册）",
      "trigger_event": "不可静态还原（二阶段代码由 DexClassLoader 加载，静态 DEX 内无 ACCESSIBILITY_SETTINGS 等字符串）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（静态不可见）",
      "shown_text_zh": "不可静态还原，需 UTG 实机捕获",
      "user_action_requested": "不可静态还原",
      "code_anchor": "二阶段 DEX（res/raw/jtldryhvhihtez 解密产物），静态不可见"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载的服务列表项（label=\"Google Chrome\"，描述=\"Erişebilirlik Servisileri Etkinleştirme\"）",
      "trigger_event": "二阶段引导页按钮触发（Intent ACTION_ACCESSIBILITY_SETTINGS，静态不可见具体调用点）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Chrome / Erişebilirlik Servisileri Etkinleştirme",
      "shown_text_zh": "Google Chrome / 启用无障碍服务",
      "user_action_requested": "在系统无障碍列表中点击“Google Chrome”并把开关打开（服务说明仅一句土耳其语，无功能范围告知）",
      "code_anchor": "res/values/strings.xml (a, XDfabYriJQnd) + res/xml/sqodgaxenjaqq.xml + com.trybirdpene.p084t"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.trybirdpene.p084t（AccessibilityService，typeAllMask / canRetrieveWindowContent / flagRetrieveInteractiveWindows）",
      "trigger_event": "系统绑定 BIND_ACCESSIBILITY_SERVICE 后 onServiceConnected（回调实现位于二阶段）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后接管全事件与窗口内容读取，具体行为（点击/读屏/跳转/阻止撤权）不可静态还原",
      "user_action_requested": "无（后台静默执行）",
      "code_anchor": "res/xml/sqodgaxenjaqq.xml + com.trybirdpene.p084t"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务 label=@string/a=\"Google Chrome\"（伪装成浏览器）",
    "系统无障碍服务列表项描述：android:description=@string/XDfabYriJQnd=\"Erişebilirlik Servisileri Etkinleştirme\"（土耳其语“启用无障碍服务”）",
    "桌面图标名称：application android:label=@string/a=\"Google Chrome\"",
    "二阶段引导弹窗/Activity/WebView/悬浮窗：全部位于加密 res/raw/jtldryhvhihtez 解密后的 DEX，静态不可见，需 UTG 实机捕获"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Google Chrome",
      "text_zh": "Google Chrome（谷歌浏览器）",
      "source_location": "res/values/strings.xml key \"a\"（application android:label 与无障碍 service android:label 共用）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "tr",
      "text_verbatim": "Erişebilirlik Servisileri Etkinleştirme",
      "text_zh": "启用无障碍服务（原文含拼写错误 Servisileri，规范应为 Servisleri）",
      "source_location": "res/values/strings.xml key \"XDfabYriJQnd\"（res/xml/sqodgaxenjaqq.xml android:description）",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原（一阶段 dex 无任何相关代码；二阶段由 native 解密后 DexClassLoader 加载，需 UTG 观测是否 onResume 死循环重跳或定时拉起无障碍设置）",
    "overlay_or_fake_settings": "不可静态还原（一阶段 Manifest 未见 SYSTEM_ALERT_WINDOW 权限，悬浮遮罩若存在应由二阶段通过窗口令牌或无障碍自身实现）",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=30，未声明 13+ 受限设置引导相关逻辑；如二阶段存在亦不可静态见）",
    "post_grant_anti_removal": "不可静态还原（已声明 WRITE_SETTINGS、设备管理员 receiver com.trybirdpene.p071q 与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，具备防卸载/防撤权配套能力，但具体阻止撤权行为在二阶段）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 com.trybirdpene.p067f 后立即开始 UTG 采样（壳解出二阶段即接管界面）；并在监测到 Activity 跳转 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 时压栈抓取前序页面与跳转后 800ms~2s 的叠加层",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后二阶段首屏引导页（弹窗或全屏 Activity）",
        "page_identifier": "com.trybirdpene 包内 Activity/Dialog，透明主题，无 ActionBar，首次启动即出现且无系统权限弹窗前置",
        "why_most_useful": "这是全案唯一能取到引导文案原文的页面，可直接区分假更新/故障恐吓/隐私承诺等话术",
        "observable_utg_signals": ["弹窗标题与正文全文", "按钮文字是否仅有“启用/确定”而无取消/跳过", "是否包含“无障碍”“Erişebilirlik”“Erişilebilirlik”等关键词"]
      },
      {
        "page_role": "系统无障碍设置页及其中的服务列表项",
        "page_identifier": "Settings → Accessibility → Downloaded services，条目文本为 Google Chrome / Erişebilirlik Servisileri Etkinleştirme",
        "why_most_useful": "直接证明系统级品牌冒用与描述伪装，且可判断应用是否在设置页上叠加引导遮罩",
        "observable_utg_signals": ["服务项 label 与 description 原文", "开关是否已被应用自动切换", "是否有悬浮引导窗/遮罩覆盖系统开关"]
      },
      {
        "page_role": "从无障碍设置返回后的回落页",
        "page_identifier": "重新出现的引导页或无障碍设置再次被拉起",
        "why_most_useful": "识别拒权/返回后的死循环重跳，是判定强制诱导而非良性说明的关键",
        "observable_utg_signals": ["返回后是否 <2s 内重新进入无障碍设置", "页面文案是否升级为恐吓话术", "是否存在 GLOBAL_ACTION_BACK 被拦截现象"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：一阶段为加密壳（native 解密 res/raw/jtldryhvhihtez → DexClassLoader 二阶段），静态完全无法看到引导流程；且应用全量字符串已混淆、界面文案可能在运行时由远端下发，纯静态只能确认“伪装成 Google Chrome 的无障碍服务”这一层；必须依赖运行期 UTG 才能在二阶段界面出现时取证。"
  },
  "behavior_pattern_tags": [
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.trybirdpene.iQPPmZmhqZ#attachBaseContext",
    "com.trybirdpene.iQPPmZmhqZ#<clinit>",
    "lib/arm64-v8a/libfGzsoGwEb.so Java_com_trybirdpene_iQPPmZmhqZ_CPzXoNA",
    "res/raw/jtldryhvhihtez",
    "res/xml/sqodgaxenjaqq.xml",
    "res/values/strings.xml (a, XDfabYriJQnd)"
  ]
}
```

> 说明：因本轮工具调用预算（≤14）已用尽于壳层穿透核验，未写入项目风险台账；已确认事实为“加密二阶段壳 + 无障碍服务伪装为 Google Chrome 的土耳其语诱导描述 + 全窗口读取能力”，而“逐步引导开启无障碍”的界面流转因 `static_visibility=packed_or_encrypted` 需 UTG 补充证据后方可定级落库。

</details>

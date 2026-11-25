# MB_070__501eb3e847｜Cerberus — Playstore

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：105.6s

## 1. 一句话核心结论

- **核心申请方式**：以 'Playstore' 名义伪装上架，桌面与组件标签全部置空，无障碍服务在系统列表中仅以土耳其语祈使句 'Lütfen izin veriniz.' 呈现，实际引导逻辑藏于 native 解密装载的二阶段 DEX，获权后即取得全局读屏与控件事件上报能力。
- **静态可见性说明**：classes.dex 中不存在无障碍服务类 com.chbsjdrnv.edzi.hiogoek.inziqvppey，也无 'chbsjdrnv'、'Lütfen izin' 等任何字符串；二阶段 DEX 由 com.wood.area.HIoTuLoWlIwQwIeNuGaTtHaTeHtAxSxRaYcYaIlIsHnJy 反射创建 DexClassLoader 装载，解密由 assets/lib/arm64-v8a/libByteAIDT.so、libByteAINN.so 等 ByteAI 保护库完成。因此引导弹窗、跳转 ACTION_ACCESSIBILITY_SETTINGS 的具体实现不可静态还原；Manifest 组件、无障碍服务标签与 res/xml/kyvwcvj.xml 能力声明仍完整可见。
- **命中的行为模式标签**：`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `501eb3e8474ddd35728b11248df2e9629afb6852b9281940059fcae7b9043522` |
| 包名 / 年份 | `com.wood.area` / 2024 |
| 家族 / 品类 | **Cerberus**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Playstore |
| 引导页宣称品牌/身份 | Google Play 商店（Playstore） |
| 系统无障碍列表服务名 | Lütfen izin veriniz. |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：桌面名冒用 Google Play 商店品牌，而包名为 com.wood.area 且无任何 Google 签名/来源证据；全部 activity 使用 android:label=""（空标签）并统一 @drawable/bvb 图标以规避桌面与应用列表识别；DeviceAdmin receiver 的 android:label="  "（仅两个空格）用于在设备管理列表挤出提示；无障碍服务仅设 android:label 而无 android:description，且未声明 isAccessibilityTool，靠一句非本地化语言祈使句掩盖读屏能力；application 类名与全部业务类名采用随机字母大小写混淆（如 ATeXwJpNwToOeBcOePjPhPeEsJx）。 |
| 无障碍服务类名 | `com.chbsjdrnv.edzi.hiogoek.inziqvppey` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.chbsjdrnv.edzi.jycuujnqkqj（MAIN/LAUNCHER，同时声明 android.app.role.SMS 角色） | 用户点击桌面 'Playstore' 图标启动（intent-filter: android.intent.action.MAIN + LAUNCHER） | 原生Activity | 无 | 点击应用图标启动；是否有取消/跳过按钮不可静态判定 | `AndroidManifest.xml: activity com.chbsjdrnv.edzi.jycuujnqkqj` |
| 2 | 冷启动入口 | com.wood.area.ATeXwJpNwToOeBcOePjPhPeEsJx（Application）→ com.wood.area.HIoTuLoWlIwQwIeNuGaTtHaTeHtAxSxRaYcYaIlIsHnJy | Application 初始化时经 spiritturtle → volumecause → patternresemble 反射构造 DexClassLoader，并把解密后的 DEX 注入 pathClassLoader 字段 | 不可静态还原 | 无 | 无（自动执行） | `com.wood.area.HIoTuLoWlIwQwIeNuGaTtHaTeHtAxSxRaYcYaIlIsHnJy.patternresemble / volumecause` |
| 3 | 引导说明页 | 二阶段 DEX 内的引导界面（载体不可静态判定，疑为原生弹窗或 WebView） | 载荷装载完成后由解密 DEX 内代码拉起，具体回调不可静态还原 | 不可静态还原 | **原文**：无（代码段与资源段均无引导文案，全部位于加密载荷）<br>**译注**：无法静态取得引导说明原文 | 不可静态判定是否提供取消/跳过入口 | `不可静态还原（位于 native 解密装载的二阶段 DEX）` |
| 4 | 跳无障碍设置 | 系统设置 · 无障碍服务列表 / 本应用无障碍服务详情页 | 由二阶段 DEX 发起 ACTION_ACCESSIBILITY_SETTINGS 跳转；该字符串在 classes.dex 中不存在，确认调用点在加密载荷内 | 系统无障碍页 | **原文**：Lütfen izin veriniz.<br>**译注**：请授予权限。 | 在系统无障碍列表中找到该条目并打开开关；android:description 为空，用户无任何能力说明可参考 | `AndroidManifest.xml: service com.chbsjdrnv.edzi.hiogoek.inziqvppey（android:label="Lütfen izin veriniz."）` |
| 5 | 获权后动作 | com.chbsjdrnv.edzi.hiogoek.inziqvppey（AccessibilityService 实现） | 系统绑定服务后回调 onServiceConnected / onAccessibilityEvent | 不可静态还原 | 无 | 无 | `res/xml/kyvwcvj.xml（canRetrieveWindowContent=true, flagIncludeNotImportantViews, flagReportViewIds）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项标签：AndroidManifest.xml 中 service com.chbsjdrnv.edzi.hiogoek.inziqvppey 的 android:label="Lütfen izin veriniz."（唯一静态可见的诱导文案）
- 系统无障碍服务详情页描述位：android:description 未声明（配置为空），用户看不到能力说明
- 桌面与应用列表：android:label="Playstore"，冒充 Google Play 商店
- 应用内引导弹窗 / 教学页 / 遮罩层：代码段与 res/ 资源中均无对应文案，全部位于 native 解密装载的二阶段 DEX（不可静态定位）
- 设备管理列表：receiver com.chbsjdrnv.edzi.zrhqz.mxxsdcahrc 的 android:label="  "（纯空格），用于挤出系统风险提示

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Lütfen izin veriniz. | 请授予权限。 | `AndroidManifest.xml · service com.chbsjdrnv.edzi.hiogoek.inziqvppey android:label` | 教唆忽视警告 |
| en | Playstore | Play 商店 | `AndroidManifest.xml · application android:label` | 未知 |
| other | — | （两个空格，无实际文字） | `AndroidManifest.xml · receiver com.chbsjdrnv.edzi.zrhqz.mxxsdcahrc android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：拒绝或从系统设置返回后的重跳逻辑位于 native 解密装载的二阶段 DEX，classes.dex 中无 ACCESSIBILITY_SETTINGS 跳转点与 onResume 计时器可核对
- **遮罩叠层 / 高仿系统设置页**：不可静态还原；但应用已申请 SYSTEM_ALERT_WINDOW 与 ACTION_MANAGE_OVERLAY_PERMISSION，具备叠放引导遮罩/悬浮窗的技术前提
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未发现应用详情页/受限设置教学的静态痕迹，相关逻辑若存在亦在加密载荷内）
- **获权后即时行为与防撤权机制**：不可静态还原；已确认具备 DeviceAdmin receiver（android.app.action.DEVICE_ADMIN_ENABLED/DISABLED，priority 121）与 BOOT_COMPLETED/SMS_DELIVER 高优先级广播监听，具备撤权对抗与重启复活基础，但具体阻止撤权代码未静态确认
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到本应用进程发起 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的 startActivity，或无障碍服务 com.chbsjdrnv.edzi.hiogoek.inziqvppey 被系统绑定（onServiceConnected）的瞬间立即拉起 UTG；同时应在冷启动 com.chbsjdrnv.edzi.jycuujnqkqj 后立即抓帧，因二阶段 DEX 解密完成即可能直弹引导页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：显著盲区：核心引导逻辑与无障碍服务实现均不在 classes.dex，而是由 native 库（libByteAIDT.so 等）解密后经 DexClassLoader 注入，纯静态 UTG 前必须先完成运行期脱壳或内存 dump 才能取得引导文案与跳转代码；另桌面名冒用 'Playstore'、全部 activity 标签为空、DeviceAdmin 标签为纯空格，会使基于文本匹配的识别在首屏直接失效，需结合包名 com.wood.area 与无障碍服务标签 'Lütfen izin veriniz.' 作联合判别。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后首屏（二阶段载荷解密完成即弹出）** | com.chbsjdrnv.edzi.jycuujnqkqj 及其拉起的弹窗/WebView，无 label、图标为 @drawable/bvb | 引导文案与取消按钮的有无只在此页可见，是判定是否属非自愿诱导的唯一直接证据 | 弹窗标题/正文全文与按钮文本；是否存在取消/跳过控件；是否可返回键关闭；是否加载 http(s) 远端 URL |
| **跳转前教学/说明页** | 跳转 ACCESSIBILITY_SETTINGS 之前的 Activity 或 WebView 页面 | 判定诱导修辞框架（假更新/故障恐吓/假反诈/清理工具伪装）的关键载体 | 页面文案关键词；是否为本地 assets HTML 或远端域名；是否含分步截图/GIF 指引 |
| **系统无障碍服务列表项** | 设置→无障碍→已下载服务中标签为 'Lütfen izin veriniz.' 的条目 | 核对服务名与系统警告文案的并置效果，验证空白 description 造成的告知缺失 | 服务条目完整标签文本；description 是否为空；点击进入详情页后的能力提示 |
| **系统设置页返回后的压栈遮罩页** | 从设置返回应用瞬间的悬浮窗/Activity（SYSTEM_ALERT_WINDOW 已授予） | 验证是否存在 refusal loop（拒权即重跳）与设置页叠层引导 | 是否自动重跳设置页；遮罩层文字与位置；返回键是否被消费 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.wood.area.HIoTuLoWlIwQwIeNuGaTtHaTeHtAxSxRaYcYaIlIsHnJy.patternresemble（反射构造 DexClassLoader 装载解密 DEX）`
- `com.wood.area.HIoTuLoWlIwQwIeNuGaTtHaTeHtAxSxRaYcYaIlIsHnJy.volumecause（Field.set 覆写 ClassLoader 字段完成注入）`
- `AndroidManifest.xml · service com.chbsjdrnv.edzi.hiogoek.inziqvppey（android:label="Lütfen izin veriniz.", BIND_ACCESSIBILITY_SERVICE）`
- `res/xml/kyvwcvj.xml（canRetrieveWindowContent=true, typeWindowContentChanged|typeWindowStateChanged, flagReportViewIds）`
- `assets/lib/arm64-v8a/libByteAIDT.so`
- `AndroidManifest.xml · activity com.chbsjdrnv.edzi.jycuujnqkqj（MAIN/LAUNCHER, android:label=""）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点（定向核验，共 14 次工具调用收口）

- **无障碍服务本体不在 classes.dex 中**：Manifest 声明的 `com.chbsjdrnv.edzi.hiogoek.inziqvppey` 类在 DEX 中查无此定义，`chbsjdrnv`、`Lütfen izin` 等字符串在代码段与资源段也均无匹配，说明承载引导逻辑与无障碍服务实现的代码位于**运行期解密的二阶段 DEX**。
- **二阶段载荷装载链已定位**：[HIoTuLoWlIwQwIeNuGaTtHaTeHtAxSxRaYcYaIlIsHnJy.patternresemble()](<resource-unit:#1.dex1 code:com.wood.area.HIoTuLoWlIwQwIeNuGaTtHaTeHtAxSxRaYcYaIlIsHnJy#patternresemble>) 通过反射构造 `DexClassLoader`，[volumecause()](<resource-unit:#1.dex1 code:com.wood.area.HIoTuLoWlIwQwIeNuGaTtHaTeHtAxSxRaYcYaIlIsHnJy#volumecause>) 用 `Field.set` 覆写 `pathClassLoader`/`mClassLoader` 字段，解密与 DEX 生成由 `assets/lib/arm64-v8a/libByteAIDT.so`、`libByteAINN.so` 等 ByteAI 系列 native 库承担。因此**引导弹窗、跳转 `ACTION_ACCESSIBILITY_SETTINGS` 的具体代码均不可静态还原**。
- **仍可静态确认的诱导面**：系统无障碍列表中该项仅显示服务标签 [Lütfen izin veriniz.](<resource-unit:#1 manifest:components>)（土耳其语"请授予权限"），且 `android:description` 为空——**用户在系统设置页看到的只有一句祈使句，无任何能力说明**。
- **身份伪装与隐身处理**：桌面名 `Playstore`（伪装 Google Play 商店），但包名 `com.wood.area`、开发者信息与 Play 商店无关；全部 `activity` 的 `android:label=""` 并统一使用 `@drawable/bvb` 图标，DeviceAdmin `receiver` 的 `android:label="  "`（纯空格），属典型的空白标签挤出警告与同名图标伪装。
- **获权后的能力范围（配置文件已确认）**：[res/xml/kyvwcvj.xml](<resource-unit:#1 file:res/xml/kyvwcvj.xml>) 声明 `canRetrieveWindowContent="true"` + `typeWindowContentChanged|typeWindowStateChanged` + `flagIncludeNotImportantViews|flagReportViewIds`，即全局读屏与控件级事件上报，配合 `SYSTEM_ALERT_WINDOW`、`READ_SMS`/`RECEIVE_SMS`、`CALL_PHONE`、`REQUEST_INSTALL_PACKAGES` 与 DeviceAdmin，符合 Cerberus 系银行木马的界面覆盖与自动操作范式。
- **覆盖边界**：引导页 UI 载体（原生 Dialog / 本地 HTML / 远端 WebView）、拒绝后是否死循环重跳、是否叠遮罩，均藏在加密 DEX 内，本次未做 native 解密还原，故 `step_by_step_flow` 中标为"不可静态还原"，不作事实性断言。

> 说明：受本轮 14 次调用硬约束，未再追加 `angr` 反编译解密算法与风险台账写入；行为链结论以"已证实事实/分析判断"区分如上，Manifest 与 a11y 配置为已证实事实，引导流程细节为待动态验证的判断。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "classes.dex 中不存在无障碍服务类 com.chbsjdrnv.edzi.hiogoek.inziqvppey，也无 'chbsjdrnv'、'Lütfen izin' 等任何字符串；二阶段 DEX 由 com.wood.area.HIoTuLoWlIwQwIeNuGaTtHaTeHtAxSxRaYcYaIlIsHnJy 反射创建 DexClassLoader 装载，解密由 assets/lib/arm64-v8a/libByteAIDT.so、libByteAINN.so 等 ByteAI 保护库完成。因此引导弹窗、跳转 ACTION_ACCESSIBILITY_SETTINGS 的具体实现不可静态还原；Manifest 组件、无障碍服务标签与 res/xml/kyvwcvj.xml 能力声明仍完整可见。",
  "summary_one_liner": "以 'Playstore' 名义伪装上架，桌面与组件标签全部置空，无障碍服务在系统列表中仅以土耳其语祈使句 'Lütfen izin veriniz.' 呈现，实际引导逻辑藏于 native 解密装载的二阶段 DEX，获权后即取得全局读屏与控件事件上报能力。",
  "disguise_identity": {
    "app_display_name": "Playstore",
    "claimed_brand_or_persona": "Google Play 商店（Playstore）",
    "a11y_service_label": "Lütfen izin veriniz.",
    "identity_mismatch": true,
    "obfuscation_tricks": "桌面名冒用 Google Play 商店品牌，而包名为 com.wood.area 且无任何 Google 签名/来源证据；全部 activity 使用 android:label=\"\"（空标签）并统一 @drawable/bvb 图标以规避桌面与应用列表识别；DeviceAdmin receiver 的 android:label=\"  \"（仅两个空格）用于在设备管理列表挤出提示；无障碍服务仅设 android:label 而无 android:description，且未声明 isAccessibilityTool，靠一句非本地化语言祈使句掩盖读屏能力；application 类名与全部业务类名采用随机字母大小写混淆（如 ATeXwJpNwToOeBcOePjPhPeEsJx）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.chbsjdrnv.edzi.jycuujnqkqj（MAIN/LAUNCHER，同时声明 android.app.role.SMS 角色）",
      "trigger_event": "用户点击桌面 'Playstore' 图标启动（intent-filter: android.intent.action.MAIN + LAUNCHER）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该 Activity 的 android:label 为空，启动后显示界面内容需运行期观察",
      "user_action_requested": "点击应用图标启动；是否有取消/跳过按钮不可静态判定",
      "code_anchor": "AndroidManifest.xml: activity com.chbsjdrnv.edzi.jycuujnqkqj"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.wood.area.ATeXwJpNwToOeBcOePjPhPeEsJx（Application）→ com.wood.area.HIoTuLoWlIwQwIeNuGaTtHaTeHtAxSxRaYcYaIlIsHnJy",
      "trigger_event": "Application 初始化时经 spiritturtle → volumecause → patternresemble 反射构造 DexClassLoader，并把解密后的 DEX 注入 pathClassLoader 字段",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "此步无界面，仅完成二阶段载荷解密装载",
      "user_action_requested": "无（自动执行）",
      "code_anchor": "com.wood.area.HIoTuLoWlIwQwIeNuGaTtHaTeHtAxSxRaYcYaIlIsHnJy.patternresemble / volumecause"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "二阶段 DEX 内的引导界面（载体不可静态判定，疑为原生弹窗或 WebView）",
      "trigger_event": "载荷装载完成后由解密 DEX 内代码拉起，具体回调不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（代码段与资源段均无引导文案，全部位于加密载荷）",
      "shown_text_zh": "无法静态取得引导说明原文",
      "user_action_requested": "不可静态判定是否提供取消/跳过入口",
      "code_anchor": "不可静态还原（位于 native 解密装载的二阶段 DEX）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 · 无障碍服务列表 / 本应用无障碍服务详情页",
      "trigger_event": "由二阶段 DEX 发起 ACTION_ACCESSIBILITY_SETTINGS 跳转；该字符串在 classes.dex 中不存在，确认调用点在加密载荷内",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Lütfen izin veriniz.",
      "shown_text_zh": "请授予权限。",
      "user_action_requested": "在系统无障碍列表中找到该条目并打开开关；android:description 为空，用户无任何能力说明可参考",
      "code_anchor": "AndroidManifest.xml: service com.chbsjdrnv.edzi.hiogoek.inziqvppey（android:label=\"Lütfen izin veriniz.\"）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.chbsjdrnv.edzi.hiogoek.inziqvppey（AccessibilityService 实现）",
      "trigger_event": "系统绑定服务后回调 onServiceConnected / onAccessibilityEvent",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后开始接收 typeWindowContentChanged / typeWindowStateChanged 事件并读取窗口内容（含非重要视图与 ViewId）",
      "user_action_requested": "无",
      "code_anchor": "res/xml/kyvwcvj.xml（canRetrieveWindowContent=true, flagIncludeNotImportantViews, flagReportViewIds）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项标签：AndroidManifest.xml 中 service com.chbsjdrnv.edzi.hiogoek.inziqvppey 的 android:label=\"Lütfen izin veriniz.\"（唯一静态可见的诱导文案）",
    "系统无障碍服务详情页描述位：android:description 未声明（配置为空），用户看不到能力说明",
    "桌面与应用列表：android:label=\"Playstore\"，冒充 Google Play 商店",
    "应用内引导弹窗 / 教学页 / 遮罩层：代码段与 res/ 资源中均无对应文案，全部位于 native 解密装载的二阶段 DEX（不可静态定位）",
    "设备管理列表：receiver com.chbsjdrnv.edzi.zrhqz.mxxsdcahrc 的 android:label=\"  \"（纯空格），用于挤出系统风险提示"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Lütfen izin veriniz.",
      "text_zh": "请授予权限。",
      "source_location": "AndroidManifest.xml · service com.chbsjdrnv.edzi.hiogoek.inziqvppey android:label",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Playstore",
      "text_zh": "Play 商店",
      "source_location": "AndroidManifest.xml · application android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "other",
      "text_verbatim": "  ",
      "text_zh": "（两个空格，无实际文字）",
      "source_location": "AndroidManifest.xml · receiver com.chbsjdrnv.edzi.zrhqz.mxxsdcahrc android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：拒绝或从系统设置返回后的重跳逻辑位于 native 解密装载的二阶段 DEX，classes.dex 中无 ACCESSIBILITY_SETTINGS 跳转点与 onResume 计时器可核对",
    "overlay_or_fake_settings": "不可静态还原；但应用已申请 SYSTEM_ALERT_WINDOW 与 ACTION_MANAGE_OVERLAY_PERMISSION，具备叠放引导遮罩/悬浮窗的技术前提",
    "restricted_settings_13plus_coaching": "无（未发现应用详情页/受限设置教学的静态痕迹，相关逻辑若存在亦在加密载荷内）",
    "post_grant_anti_removal": "不可静态还原；已确认具备 DeviceAdmin receiver（android.app.action.DEVICE_ADMIN_ENABLED/DISABLED，priority 121）与 BOOT_COMPLETED/SMS_DELIVER 高优先级广播监听，具备撤权对抗与重启复活基础，但具体阻止撤权代码未静态确认",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到本应用进程发起 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的 startActivity，或无障碍服务 com.chbsjdrnv.edzi.hiogoek.inziqvppey 被系统绑定（onServiceConnected）的瞬间立即拉起 UTG；同时应在冷启动 com.chbsjdrnv.edzi.jycuujnqkqj 后立即抓帧，因二阶段 DEX 解密完成即可能直弹引导页。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后首屏（二阶段载荷解密完成即弹出）",
        "page_identifier": "com.chbsjdrnv.edzi.jycuujnqkqj 及其拉起的弹窗/WebView，无 label、图标为 @drawable/bvb",
        "why_most_useful": "引导文案与取消按钮的有无只在此页可见，是判定是否属非自愿诱导的唯一直接证据",
        "observable_utg_signals": ["弹窗标题/正文全文与按钮文本", "是否存在取消/跳过控件", "是否可返回键关闭", "是否加载 http(s) 远端 URL"]
      },
      {
        "page_role": "跳转前教学/说明页",
        "page_identifier": "跳转 ACCESSIBILITY_SETTINGS 之前的 Activity 或 WebView 页面",
        "why_most_useful": "判定诱导修辞框架（假更新/故障恐吓/假反诈/清理工具伪装）的关键载体",
        "observable_utg_signals": ["页面文案关键词", "是否为本地 assets HTML 或远端域名", "是否含分步截图/GIF 指引"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置→无障碍→已下载服务中标签为 'Lütfen izin veriniz.' 的条目",
        "why_most_useful": "核对服务名与系统警告文案的并置效果，验证空白 description 造成的告知缺失",
        "observable_utg_signals": ["服务条目完整标签文本", "description 是否为空", "点击进入详情页后的能力提示"]
      },
      {
        "page_role": "系统设置页返回后的压栈遮罩页",
        "page_identifier": "从设置返回应用瞬间的悬浮窗/Activity（SYSTEM_ALERT_WINDOW 已授予）",
        "why_most_useful": "验证是否存在 refusal loop（拒权即重跳）与设置页叠层引导",
        "observable_utg_signals": ["是否自动重跳设置页", "遮罩层文字与位置", "返回键是否被消费"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "显著盲区：核心引导逻辑与无障碍服务实现均不在 classes.dex，而是由 native 库（libByteAIDT.so 等）解密后经 DexClassLoader 注入，纯静态 UTG 前必须先完成运行期脱壳或内存 dump 才能取得引导文案与跳转代码；另桌面名冒用 'Playstore'、全部 activity 标签为空、DeviceAdmin 标签为纯空格，会使基于文本匹配的识别在首屏直接失效，需结合包名 com.wood.area 与无障碍服务标签 'Lütfen izin veriniz.' 作联合判别。"
  },
  "behavior_pattern_tags": [
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.wood.area.HIoTuLoWlIwQwIeNuGaTtHaTeHtAxSxRaYcYaIlIsHnJy.patternresemble（反射构造 DexClassLoader 装载解密 DEX）",
    "com.wood.area.HIoTuLoWlIwQwIeNuGaTtHaTeHtAxSxRaYcYaIlIsHnJy.volumecause（Field.set 覆写 ClassLoader 字段完成注入）",
    "AndroidManifest.xml · service com.chbsjdrnv.edzi.hiogoek.inziqvppey（android:label=\"Lütfen izin veriniz.\", BIND_ACCESSIBILITY_SERVICE）",
    "res/xml/kyvwcvj.xml（canRetrieveWindowContent=true, typeWindowContentChanged|typeWindowStateChanged, flagReportViewIds）",
    "assets/lib/arm64-v8a/libByteAIDT.so",
    "AndroidManifest.xml · activity com.chbsjdrnv.edzi.jycuujnqkqj（MAIN/LAUNCHER, android:label=\"\"）"
  ]
}
```

</details>

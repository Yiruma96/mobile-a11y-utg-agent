# MB_107__144cb58bad｜Octo — Google Play

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：143.5s

## 1. 一句话核心结论

- **核心申请方式**：以“Google Play”为应用名与无障碍服务名，用“Enable this service to protect your device.”的安全保护话术诱使开启具备全量窗口读取与手势注入的无障碍服务，但真正的分步引导页面流转藏在 native 解密的高熵载荷中，静态不可见。
- **静态可见性说明**：仅 Manifest 与资源层（无障碍服务声明、android:description 文案、服务标签、权限集）完整可见。classes.dex 仅 7392 字节的加载桩，真实业务代码由 libdkbfWjqXt.so 在 Application.attachBaseContext 中解密 res/raw/pdledcnq（459328 字节、熵 8.0、16 字节分块全不重复）后动态加载；引导弹窗、ACTION_ACCESSIBILITY_SETTINGS/ACTION_APPLICATION_DETAILS_SETTINGS 跳转、拒权循环与获权后动作全部位于该加密载荷内，DEX 中 accessibility/startActivity/com.android.settings 关键字零命中，静态不可还原。
- **命中的行为模式标签**：`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `144cb58badccd0d201ef6b9befef75f7a2860cf6b978b14d9acf9b77a6a3fdfb` |
| 包名 / 年份 | `com.standhave03` / 2023 |
| 家族 / 品类 | **Octo**（同池样本数：9） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google Play |
| 引导页宣称品牌/身份 | Google Play（Google 官方应用商店品牌） |
| 系统无障碍列表服务名 | Google Play |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：应用 android:label 与无障碍服务 android:label 均复用 @string/a="Google Play"，与包名 com.standhave03 及签名主体无任何关联；所有类名/方法名/字段名均为随机字母混淆（p050j、pjFBZs、kJAlXNQffKriviM）；无障碍说明文案仅一句英文泛化安全承诺，不披露任何实际操作（短信读取、手势点击）范围；服务配置请求 flagRetrieveInteractiveWindows + canPerformGestures 但描述中完全不提及，属能力与告知严重不符。未发现空白/换行挤出警告、同形字或伪造 isAccessibilityTool 的静态证据（后者因代码加密不可判定）。 |
| 无障碍服务类名 | `com.standhave03.p050j` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.standhave03.p025i（LAUNCHER Activity，Theme.AppCompat.Transparent.NoActionBar，screenOrientation=fullSensor） | 用户点击桌面图标启动 MAIN/LAUNCHER | 原生Activity | **原文**：无（Activity 主题为透明无标题栏，界面内容由加密载荷内代码绘制，静态不可还原）<br>**译注**：启动页为透明主题，实际呈现内容不可静态还原 | 不可静态还原 | `AndroidManifest.xml application/activity[com.standhave03.p025i]` |
| 2 | 获权前动作（载荷解密与真实入口装载） | com.standhave03.pjFBZs（自定义 Application）→ libdkbfWjqXt.so | attachBaseContext() 回调，在 super 之后立即调用 native 方法 kJAlXNQffKriviM(Context) | 不可静态还原 | 无 | 不可静态还原 | `com.standhave03.pjFBZs.attachBaseContext / com.standhave03.pjFBZs.kJAlXNQffKriviM` |
| 3 | 引导说明页 | 候选载体：com.standhave03.p018b（@android:style/Theme.Dialog）/ com.standhave03.p069f 与 com.standhave03.p091u（Theme.NoTitleBar.Fullscreen + adjustResize，形态符合 WebView 全屏页）/ com.standhave03.p017n（singleTask）；具体归属不可静态判定 | 不可静态还原（无 ACTION_ACCESSIBILITY_SETTINGS / startActivity 静态字符串） | 不可静态还原 | **原文**：无（包内无 assets/ 目录，无本地 HTML；res/values/strings.xml 仅有 2 条字符串，均非引导正文）<br>**译注**：引导正文不在任何静态可见资源中 | 不可静态还原（是否有取消/跳过按钮无法判定） | `AndroidManifest.xml activity[com.standhave03.p018b / p069f / p091u / p017n]` |
| 4 | 跳无障碍设置 | 系统无障碍设置页（Settings.ACTION_ACCESSIBILITY_SETTINGS）→ 列表项“Google Play” | 不可静态还原（跳转 Intent 构造在加密载荷内） | 系统无障碍页 | **原文**：Google Play / Enable this service to protect your device.<br>**译注**：“Google Play” / “启用此服务以保护您的设备。” | 用户在系统无障碍列表中找到“Google Play”并打开开关；系统标准页面本身具备返回能力 | `res/values/strings.xml (a / ZpBZQOCOJEesXG)、res/xml/hgprndxossxcklb.xml android:description` |
| 5 | 拒权反馈循环 | 不可静态还原 | 不可静态还原（无 onResume/Timer 静态证据，相关代码在加密载荷内） | 不可静态还原 | 无 | 不可静态还原 | `不可静态还原（加密载荷）` |
| 6 | 获权后动作 | com.standhave03.p050j（AccessibilityService，typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows + canPerformGestures）；配合 READ_SMS/RECEIVE_SMS/SEND_SMS/CALL_PHONE/WRITE_SETTINGS 与设备管理器 | onServiceConnected / onAccessibilityEvent（事件类型 typeAllMask） | 不可静态还原 | 无 | 不可静态还原 | `AndroidManifest.xml service[com.standhave03.p050j]、res/xml/hgprndxossxcklb.xml、res/xml-v22/hgprndxossxcklb.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统设置 → 无障碍 → 已安装服务列表：服务名“Google Play”（@string/a，与桌面应用名同一资源）
- 系统设置 → 无障碍 → 该服务详情页副标题：android:description = “Enable this service to protect your device.”（res/values/strings.xml key ZpBZQOCOJEesXG，经 res/xml/hgprndxossxcklb.xml 与 res/xml-v22/hgprndxossxcklb.xml 引用）
- 应用内引导弹窗/说明页文字：包内无 assets/ 目录、无 HTML、strings.xml 仅 2 条非引导字符串，全部引导正文由 res/raw/pdledcnq 解密后的代码提供，静态位置不可定位（候选 Activity：p018b Theme.Dialog、p069f/p091u 全屏 NoTitleBar）
- 桌面图标标签：@string/a = “Google Play”

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable this service to protect your device. | 启用此服务以保护您的设备。 | `res/values/strings.xml key ZpBZQOCOJEesXG（被 res/xml/hgprndxossxcklb.xml 的 android:description 引用，显示于系统无障碍服务详情）` | 假反诈安全 |
| en | Google Play | Google Play（Google 官方应用商店） | `res/values/strings.xml key a（同时用于 application android:label 与无障碍服务 android:label）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原。引导与跳转逻辑位于 native 解密后的 DEX，包内无 onResume/Timer/ACTION_ACCESSIBILITY_SETTINGS 静态痕迹，无法确认是良性降级还是死循环重跳。
- **遮罩叠层 / 高仿系统设置页**：不可静态确认。Manifest 存在 Theme.AppCompat.Transparent.NoActionBar、Theme.Dialog、NoTitleBar.Fullscreen 等适合叠层/遮罩的 Activity（p018b、p069f、p091u、p064i、p098d、p015t），但无静态证据表明其用于覆盖系统无障碍页或伪造设置界面。
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（目标 SDK 为 28，低于 Android 13 受限设置机制适用版本；相关教学文案若存在亦在加密载荷内）
- **获权后即时行为与防撤权机制**：不可静态确认。服务具备 canPerformGestures 与全量窗口读取，理论上可执行 GLOBAL_ACTION_BACK/HOME 阻止撤权，但无静态代码证据。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 com.standhave03 进程首次启动后（Application.attachBaseContext 完成解密加载）的任一跳转：以 Activity 启动事件为目标，一旦前台出现 Settings 的 ACCESSIBILITY_SETTINGS 或 APPLICATION_DETAILS_SETTINGS 页面立即抓取前一帧与后一帧；若未捕获跳转，则在 com.standhave03.p025i 冷启动后 1 秒起按 500ms 间隔连续截图直至出现系统无障碍页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两类显著盲区：其一，真实引导 UI 完全位于 native 解密的高熵载荷（res/raw/pdledcnq，熵 8.0）内，纯静态无法给出页面流转，必须运行期 UTG/动态脱壳取证；其二，若载荷内引导页为纯图片或 WebView 远端下发（包内无 assets/、无本地 HTML，远端可能性存在），UTG 节点树将缺少文本，需结合截图 OCR 与抓包补充。静态加壳本身不阻挡运行期 UTG，但需保证设备可正常启动该样本以完成解密。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后的应用内引导页（真身）** | 包名 com.standhave03 的 Activity 且非 launcher p025i：重点观察 p018b（对话框主题）、p069f / p091u（全屏无标题）、p017n（singleTask）；透明主题 Activity 叠加在桌面或上一页之上 | 该页承载真实诱导文案与“去开启”按钮，是判定诱导话术框架（假安全/假更新/教唆忽视警告）的唯一现场 | Activity 类名（p018b/p069f/p091u/p017n）；页面全部文本节点与按钮文案；是否存在取消/跳过控件；是否 WebView（节点树为单一 WebView 容器） |
| **跳转动作与目标 Intent 取证** | 前台从 com.standhave03 切换到 com.android.settings/.Settings$AccessibilitySettingsActivity 或 .applications.AppInfoActivity | 确认“第几步、什么时机”跳到受限设置，以及是否直接跳到本应用详情页为后续受限设置授权铺路 | 跳转目标 Activity 全名；跳转前是否显示倒计时/遮罩；是否连续多次跳转（拒权循环） |
| **系统无障碍服务列表项（伪装身份现场）** | Settings 无障碍列表中出现文本“Google Play”及副标题“Enable this service to protect your device.” | 固定证据证明应用以 Google Play 名义占用系统无障碍列表，且说明文案与实际能力（窗口读取+手势注入）严重不符 | 列表项标题文本 Google Play；副标题原文；同一列表中真实 Google Play 服务是否共存造成混淆 |
| **获权后返回应用的下一步动作页** | 开启开关返回后前台出现的 com.standhave03 Activity（可能为 p069f/p091u 全屏页或直接无界面） | 判断获权后是否立即自操作、跳转权限引导或静默后台运行（对应短信/设备管理器链路） | 返回后首个前台包名；是否出现第二个权限申请（短信/设备管理器）；是否有悬浮窗覆盖 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.standhave03.pjFBZs.attachBaseContext`
- `com.standhave03.pjFBZs.kJAlXNQffKriviM`
- `res/raw/pdledcnq`
- `res/xml/hgprndxossxcklb.xml`
- `res/xml-v22/hgprndxossxcklb.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（受约束定向审计）

**核心判断：纯运行期 UTG 页面流转无法静态还原——无障碍引导逻辑位于 native 解密的加密载荷内。**

已证实的静态事实：

1. **可见代码仅为加载桩**：classes.dex 仅 7,392 字节、31 个类，全部为壳桩（`onCreate`/`onBind`/`onReceive` 空实现）。在 DEX 中检索 `accessibility`、`ACTION_ACCESSIBILITY_SETTINGS`、`startActivity`、`com.android.settings` 等关键字，**没有命中任何结果**。
2. **native 二阶段解密**：[pjFBZs.attachBaseContext()](<resource-unit:#1.dex1 code:com.standhave03.pjFBZs#attachBaseContext>) 在 `super` 后立即调用 native 方法 [kJAlXNQffKriviM()](<resource-unit:#1.dex1 code:com.standhave03.pjFBZs#kJAlXNQffKriviM>)；`libdkbfWjqXt.so` 导出 `Java_com_standhave03_pjFBZs_kJAlXNQffKriviM` 及 `_JNIEnv::CallObjectMethod/NewObject/CallStaticObjectMethod` 等反射建类符号。
3. **加密载荷**：[res/raw/pdledcnq](<resource-unit:#1 file:res/raw/pdledcnq>) 459,328 字节，熵 8.000，256 种字节值全覆盖，28,708 个 16 字节分块**互不重复**——高熵密文/压缩体，非明文资源。
4. **无障碍声明本身清晰可见**（Manifest/资源层）：
   - 服务 [com.standhave03.p050j](<resource-unit:#1 manifest:components>)，`BIND_ACCESSIBILITY_SERVICE`，标签 `@string/a` = **“Google Play”**；
   - 配置 [res/xml/hgprndxossxcklb.xml](<resource-unit:#1 file:res/xml/hgprndxossxcklb.xml>)：`typeAllMask` + `canRetrieveWindowContent` + `flagRetrieveInteractiveWindows` + `flagReportViewIds`；v22 版另加 `canPerformGestures`（全量窗口读取 + 手势注入，等同完全操控）；
   - 说明文案 [res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml>)：**“Enable this service to protect your device.”** —— 伪装成“设备保护”的安全工具话术。
5. **身份伪装**：应用名与服务名同为 **“Google Play”**，而包名 `com.standhave03` 无任何关联；同时声明设备管理器（`wipe-data`/`reset-password`/`force-lock`/`disable-camera`/`watch-login`）、短信读发、`CALL_PHONE`、`WRITE_SETTINGS`、通知监听。

**未能静态确认的部分（覆盖边界）**：引导弹窗/说明页、`ACTION_ACCESSIBILITY_SETTINGS` 与 `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转点、拒权循环、获权后自操作——这些均应在解密后的 DEX 中。Manifest 中可见若干 `Theme.AppCompat.Transparent.NoActionBar` / `Theme.Dialog` / 全屏 `NoTitleBar.Fullscreen` 的 Activity（`p025i` 启动页、`p018b` 对话框、`p069f`/`p091u` 全屏页、`p017n` singleTask），与“透明引导页 + 对话框 + WebView 载体”形态吻合，但**具体哪一个是引导页无法静态判定**，故不臆测。

**已登记风险**：R-001（high / malware_trojan）——native 解密高熵载荷动态加载，无障碍引导逻辑不可静态还原。报告已生成。

---

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "仅 Manifest 与资源层（无障碍服务声明、android:description 文案、服务标签、权限集）完整可见。classes.dex 仅 7392 字节的加载桩，真实业务代码由 libdkbfWjqXt.so 在 Application.attachBaseContext 中解密 res/raw/pdledcnq（459328 字节、熵 8.0、16 字节分块全不重复）后动态加载；引导弹窗、ACTION_ACCESSIBILITY_SETTINGS/ACTION_APPLICATION_DETAILS_SETTINGS 跳转、拒权循环与获权后动作全部位于该加密载荷内，DEX 中 accessibility/startActivity/com.android.settings 关键字零命中，静态不可还原。",
  "summary_one_liner": "以“Google Play”为应用名与无障碍服务名，用“Enable this service to protect your device.”的安全保护话术诱使开启具备全量窗口读取与手势注入的无障碍服务，但真正的分步引导页面流转藏在 native 解密的高熵载荷中，静态不可见。",
  "disguise_identity": {
    "app_display_name": "Google Play",
    "claimed_brand_or_persona": "Google Play（Google 官方应用商店品牌）",
    "a11y_service_label": "Google Play",
    "identity_mismatch": true,
    "obfuscation_tricks": "应用 android:label 与无障碍服务 android:label 均复用 @string/a=\"Google Play\"，与包名 com.standhave03 及签名主体无任何关联；所有类名/方法名/字段名均为随机字母混淆（p050j、pjFBZs、kJAlXNQffKriviM）；无障碍说明文案仅一句英文泛化安全承诺，不披露任何实际操作（短信读取、手势点击）范围；服务配置请求 flagRetrieveInteractiveWindows + canPerformGestures 但描述中完全不提及，属能力与告知严重不符。未发现空白/换行挤出警告、同形字或伪造 isAccessibilityTool 的静态证据（后者因代码加密不可判定）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.standhave03.p025i（LAUNCHER Activity，Theme.AppCompat.Transparent.NoActionBar，screenOrientation=fullSensor）",
      "trigger_event": "用户点击桌面图标启动 MAIN/LAUNCHER",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（Activity 主题为透明无标题栏，界面内容由加密载荷内代码绘制，静态不可还原）",
      "shown_text_zh": "启动页为透明主题，实际呈现内容不可静态还原",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml application/activity[com.standhave03.p025i]"
    },
    {
      "step": 2,
      "stage": "获权前动作（载荷解密与真实入口装载）",
      "screen_or_component": "com.standhave03.pjFBZs（自定义 Application）→ libdkbfWjqXt.so",
      "trigger_event": "attachBaseContext() 回调，在 super 之后立即调用 native 方法 kJAlXNQffKriviM(Context)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "进程启动即解密并加载 res/raw/pdledcnq，随后由解密代码决定 UI 走向",
      "user_action_requested": "不可静态还原",
      "code_anchor": "com.standhave03.pjFBZs.attachBaseContext / com.standhave03.pjFBZs.kJAlXNQffKriviM"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "候选载体：com.standhave03.p018b（@android:style/Theme.Dialog）/ com.standhave03.p069f 与 com.standhave03.p091u（Theme.NoTitleBar.Fullscreen + adjustResize，形态符合 WebView 全屏页）/ com.standhave03.p017n（singleTask）；具体归属不可静态判定",
      "trigger_event": "不可静态还原（无 ACTION_ACCESSIBILITY_SETTINGS / startActivity 静态字符串）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（包内无 assets/ 目录，无本地 HTML；res/values/strings.xml 仅有 2 条字符串，均非引导正文）",
      "shown_text_zh": "引导正文不在任何静态可见资源中",
      "user_action_requested": "不可静态还原（是否有取消/跳过按钮无法判定）",
      "code_anchor": "AndroidManifest.xml activity[com.standhave03.p018b / p069f / p091u / p017n]"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（Settings.ACTION_ACCESSIBILITY_SETTINGS）→ 列表项“Google Play”",
      "trigger_event": "不可静态还原（跳转 Intent 构造在加密载荷内）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Play / Enable this service to protect your device.",
      "shown_text_zh": "“Google Play” / “启用此服务以保护您的设备。”",
      "user_action_requested": "用户在系统无障碍列表中找到“Google Play”并打开开关；系统标准页面本身具备返回能力",
      "code_anchor": "res/values/strings.xml (a / ZpBZQOCOJEesXG)、res/xml/hgprndxossxcklb.xml android:description"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "不可静态还原",
      "trigger_event": "不可静态还原（无 onResume/Timer 静态证据，相关代码在加密载荷内）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "拒绝或返回后是否重跳设置页无法静态判定",
      "user_action_requested": "不可静态还原",
      "code_anchor": "不可静态还原（加密载荷）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.standhave03.p050j（AccessibilityService，typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows + canPerformGestures）；配合 READ_SMS/RECEIVE_SMS/SEND_SMS/CALL_PHONE/WRITE_SETTINGS 与设备管理器",
      "trigger_event": "onServiceConnected / onAccessibilityEvent（事件类型 typeAllMask）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后利用全量窗口读取与手势注入操控界面、读取短信与通话能力，具体实现位于加密载荷内",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml service[com.standhave03.p050j]、res/xml/hgprndxossxcklb.xml、res/xml-v22/hgprndxossxcklb.xml"
    }
  ],
  "text_presentation_locations": [
    "系统设置 → 无障碍 → 已安装服务列表：服务名“Google Play”（@string/a，与桌面应用名同一资源）",
    "系统设置 → 无障碍 → 该服务详情页副标题：android:description = “Enable this service to protect your device.”（res/values/strings.xml key ZpBZQOCOJEesXG，经 res/xml/hgprndxossxcklb.xml 与 res/xml-v22/hgprndxossxcklb.xml 引用）",
    "应用内引导弹窗/说明页文字：包内无 assets/ 目录、无 HTML、strings.xml 仅 2 条非引导字符串，全部引导正文由 res/raw/pdledcnq 解密后的代码提供，静态位置不可定位（候选 Activity：p018b Theme.Dialog、p069f/p091u 全屏 NoTitleBar）",
    "桌面图标标签：@string/a = “Google Play”"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable this service to protect your device.",
      "text_zh": "启用此服务以保护您的设备。",
      "source_location": "res/values/strings.xml key ZpBZQOCOJEesXG（被 res/xml/hgprndxossxcklb.xml 的 android:description 引用，显示于系统无障碍服务详情）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Play",
      "text_zh": "Google Play（Google 官方应用商店）",
      "source_location": "res/values/strings.xml key a（同时用于 application android:label 与无障碍服务 android:label）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原。引导与跳转逻辑位于 native 解密后的 DEX，包内无 onResume/Timer/ACTION_ACCESSIBILITY_SETTINGS 静态痕迹，无法确认是良性降级还是死循环重跳。",
    "overlay_or_fake_settings": "不可静态确认。Manifest 存在 Theme.AppCompat.Transparent.NoActionBar、Theme.Dialog、NoTitleBar.Fullscreen 等适合叠层/遮罩的 Activity（p018b、p069f、p091u、p064i、p098d、p015t），但无静态证据表明其用于覆盖系统无障碍页或伪造设置界面。",
    "restricted_settings_13plus_coaching": "无静态证据（目标 SDK 为 28，低于 Android 13 受限设置机制适用版本；相关教学文案若存在亦在加密载荷内）",
    "post_grant_anti_removal": "不可静态确认。服务具备 canPerformGestures 与全量窗口读取，理论上可执行 GLOBAL_ACTION_BACK/HOME 阻止撤权，但无静态代码证据。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 com.standhave03 进程首次启动后（Application.attachBaseContext 完成解密加载）的任一跳转：以 Activity 启动事件为目标，一旦前台出现 Settings 的 ACCESSIBILITY_SETTINGS 或 APPLICATION_DETAILS_SETTINGS 页面立即抓取前一帧与后一帧；若未捕获跳转，则在 com.standhave03.p025i 冷启动后 1 秒起按 500ms 间隔连续截图直至出现系统无障碍页。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后的应用内引导页（真身）",
        "page_identifier": "包名 com.standhave03 的 Activity 且非 launcher p025i：重点观察 p018b（对话框主题）、p069f / p091u（全屏无标题）、p017n（singleTask）；透明主题 Activity 叠加在桌面或上一页之上",
        "why_most_useful": "该页承载真实诱导文案与“去开启”按钮，是判定诱导话术框架（假安全/假更新/教唆忽视警告）的唯一现场",
        "observable_utg_signals": ["Activity 类名（p018b/p069f/p091u/p017n）", "页面全部文本节点与按钮文案", "是否存在取消/跳过控件", "是否 WebView（节点树为单一 WebView 容器）"]
      },
      {
        "page_role": "跳转动作与目标 Intent 取证",
        "page_identifier": "前台从 com.standhave03 切换到 com.android.settings/.Settings$AccessibilitySettingsActivity 或 .applications.AppInfoActivity",
        "why_most_useful": "确认“第几步、什么时机”跳到受限设置，以及是否直接跳到本应用详情页为后续受限设置授权铺路",
        "observable_utg_signals": ["跳转目标 Activity 全名", "跳转前是否显示倒计时/遮罩", "是否连续多次跳转（拒权循环）"]
      },
      {
        "page_role": "系统无障碍服务列表项（伪装身份现场）",
        "page_identifier": "Settings 无障碍列表中出现文本“Google Play”及副标题“Enable this service to protect your device.”",
        "why_most_useful": "固定证据证明应用以 Google Play 名义占用系统无障碍列表，且说明文案与实际能力（窗口读取+手势注入）严重不符",
        "observable_utg_signals": ["列表项标题文本 Google Play", "副标题原文", "同一列表中真实 Google Play 服务是否共存造成混淆"]
      },
      {
        "page_role": "获权后返回应用的下一步动作页",
        "page_identifier": "开启开关返回后前台出现的 com.standhave03 Activity（可能为 p069f/p091u 全屏页或直接无界面）",
        "why_most_useful": "判断获权后是否立即自操作、跳转权限引导或静默后台运行（对应短信/设备管理器链路）",
        "observable_utg_signals": ["返回后首个前台包名", "是否出现第二个权限申请（短信/设备管理器）", "是否有悬浮窗覆盖"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两类显著盲区：其一，真实引导 UI 完全位于 native 解密的高熵载荷（res/raw/pdledcnq，熵 8.0）内，纯静态无法给出页面流转，必须运行期 UTG/动态脱壳取证；其二，若载荷内引导页为纯图片或 WebView 远端下发（包内无 assets/、无本地 HTML，远端可能性存在），UTG 节点树将缺少文本，需结合截图 OCR 与抓包补充。静态加壳本身不阻挡运行期 UTG，但需保证设备可正常启动该样本以完成解密。"
  },
  "behavior_pattern_tags": [
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "TRIG_COLD_START_BLOCK"
  ],
  "code_anchors": [
    "com.standhave03.pjFBZs.attachBaseContext",
    "com.standhave03.pjFBZs.kJAlXNQffKriviM",
    "res/raw/pdledcnq",
    "res/xml/hgprndxossxcklb.xml",
    "res/xml-v22/hgprndxossxcklb.xml",
    "res/values/strings.xml"
  ]
}
```

</details>

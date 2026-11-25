# MR_088__8ea51f4b8b｜Helper — helpserver

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：159.7s

## 1. 一句话核心结论

- **核心申请方式**：无界面空壳 Activity + 后台服务经 native 解密加密载荷，静默注册 label 为 "Get more money"、typeAllMask/canRetrieveWindowContent 的无障碍服务，不提供任何 description 或前置说明，引导流程全在解密载荷中运行期生成。
- **静态可见性说明**：Manifest、无障碍配置 xml、DEX 外壳与 assets 密文均完整可见，但无障碍开启的引导页面、话术文案、跳转与拒权重试逻辑完全不在 DEX/资源内：全部位于 assets 下两份高熵加密数据（loaddex...data 183857B / cloaddex...data 13620B，无 dex 魔数、可打印率 36.7%、零明文 URL 与文案），由 libloaddex.hb.com.loaddex.psx.so 的 JNI_OnLoad 及 Servicepsx_c/Receiverpsx_r 在 native 层解密执行；全包无 layout、无 HTML、无引导字符串，故运行期页面流转不可静态还原。
- **命中的行为模式标签**：`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `8ea51f4b8b3e8709bccdf9e73d3c8d5099446c1352f0f656a16086ffcb1351ba` |
| 包名 / 年份 | `loaddex.hb.com.loaddex.psx` / 2020 |
| 家族 / 品类 | **Helper**（同池样本数：2） |
| 原始来源标识 | https://securelist.com/unkillable-xhelper-and-a-trojan-matryoshka/96487/ |
| 桌面显示名 | helpserver |
| 引导页宣称品牌/身份 | 无任何页面宣称（应用无可见界面，无 WebView、无弹窗、无文案资源）；唯一对用户可见的身份信息是无障碍服务名 "Get more money" 与通知监听服务名 "SystemSafeguard" |
| 系统无障碍列表服务名 | Get more money |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍 label 为 "Get more money"（直白表达收益诱导），与桌面显示名 helpserver、应用内 strings app_name=apk 三者互不一致；2) 同进程另一服务伪装成系统语义 "SystemSafeguard"；3) 无障碍未声明 android:description，系统列表中无任何能力说明；4) res/xml/accessibility.xml 为空配置、仅 xml-v13 才带 typeAllMask 全量事件与读屏权限，规避低版本检查；5) 全部类名统一加 psx 后缀、无意义单方法 cc.cc() 作 native 桥；6) 唯一 Activity 为 Theme.Translucent + excludeFromRecents + 空 onCreate，启动即消失不留痕。 |
| 无障碍服务类名 | `loaddex.hb.com.loaddex.psx.Accessibilitypsx` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, READ_SMS, RECEIVE_SMS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | loaddex.hb.com.loaddex.psx.Activitypsx（Theme.Translucent，process=:psx，excludeFromRecents=true） | Launcher 点击启动 / onCreate | 原生Activity | 无 | 无（用户看不到任何页面，也无取消/跳过控件） | `loaddex.hb.com.loaddex.psx.Activitypsx.onCreate` |
| 2 | 获权后动作（能力植入） | loaddex.hb.com.loaddex.psx.Servicepsx（process=:psx，exported，action=ServicepsxTil，priority=1000）与 Receiverpsx（BOOT_COMPLETED priority=2147483646 / USER_PRESENT / PACKAGE_ADDED / PACKAGE_REMOVED / CONNECTIVITY_CHANGE） | Service.onCreate / onStartCommand / Receiver.onReceive → cc.cc() → Servicepsx_c(Context,Intent) / Receiverpsx_r(Object,Object) 等 JNI 声明 | 不可静态还原 | 无 | 不可静态还原 | `loaddex.hb.com.loaddex.psx.Servicepsx.onCreate / Servicepsx.Servicepsx_c / Receiverpsx.onReceive` |
| 3 | 跳无障碍设置（运行期，不可静态还原） | 预期由 native 解密载荷拉起 android.settings.ACCESSIBILITY_SETTINGS，或叠加悬浮窗/引导页；静态代码中无对应 Intent 字符串 | 不可静态还原（推测由 JNI_OnLoad 后的解密模块触发） | 不可静态还原 | **原文**：无（DEX 与资源中无任何引导文案、无 ACTION_ACCESSIBILITY_SETTINGS/ACTION_APPLICATION_DETAILS_SETTINGS 字面量）<br>**译注**：无法静态确认；全包检索 accessibility / Settings / http 在代码与资源中零命中 | 不可静态还原 | `#1.so1 JNI_OnLoad@0x31f8（载荷入口）；assets/loaddex.hb.com.loaddex.psx.data、assets/cloaddex.hb.com.loaddex.psx.data（加密载荷）` |
| 4 | 系统无障碍列表（唯一静态可见的用户触点） | 系统设置 → 无障碍 → 已安装服务列表项 loaddex.hb.com.loaddex.psx.Accessibilitypsx | 用户手动进入系统无障碍设置 | 系统无障碍页 | **原文**：Get more money<br>**译注**：“赚更多钱”——系统无障碍列表中显示的服务名，无副标题/说明（未声明 android:description） | 用户需自行点击开关启用；该服务本身不提供任何用途说明、无隐私承诺、无取消按钮概念 | `AndroidManifest.xml service android:label="Get more money" + res/xml-v13/accessibility.xml（typeAllMask, canRetrieveWindowContent=true, notificationTimeout=100）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项标题：AndroidManifest 中 Accessibilitypsx 的 android:label="Get more money"（无 description，故列表内无任何能力说明文字）
- 系统通知使用权列表项标题：Notificationpsx 的 android:label="SystemSafeguard"（伪装系统安全组件语义）
- 应用桌面图标名：android:label="helpserver"（与上述两个服务名均不一致）
- res/values/strings.xml 仅 app_name=apk，无任何引导/说明文案
- 无 layout 目录、无 Dialog、无 assets 内 HTML/WebView 页面、无悬浮窗布局——静态包内不存在任何引导文字呈现位置
- 运行期可能出现的引导弹窗/遮罩/WebView 文案：由 assets 下两份加密 data 在 native 层解密后生成，静态不可见

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Get more money | 赚更多钱 | `AndroidManifest.xml → service loaddex.hb.com.loaddex.psx.Accessibilitypsx android:label` | 未知 |
| en | SystemSafeguard | 系统安全防护（伪装为系统级安全组件） | `AndroidManifest.xml → service loaddex.hb.com.loaddex.psx.Notificationpsx android:label` | 假反诈安全 |
| en | helpserver | 帮助服务器 | `AndroidManifest.xml → application android:label（桌面显示名）` | 清理工具伪装 |
| en | apk | apk（占位式应用名，未本地化） | `res/values/strings.xml → app_name` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：静态代码中不存在 onResume/Timer 重跳逻辑：唯一 Activity 的 onCreate 为空且无生命周期重写，DEX 内无 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 字面量。若存在拒权重试循环，只能由 native 解密载荷在运行期实现，需动态观测确认。
- **遮罩叠层 / 高仿系统设置页**：静态包内无悬浮窗布局、无高仿设置页布局；但已申请 SYSTEM_ALERT_WINDOW 权限，且无障碍配置为 typeAllMask + canRetrieveWindowContent=true，具备在设置页之上叠加遮罩/引导层的技术条件，实际叠层内容在加密载荷内。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=19，无需受限设置授权；静态无相关教学文案）
- **获权后即时行为与防撤权机制**：静态不可确认。可确认的支撑条件：无障碍服务为 typeAllMask 全量事件（可监听设置页交互并执行全局动作）+ SYSTEM_ALERT_WINDOW 悬浮窗 + WRITE_SETTINGS + KILL_BACKGROUND_PROCESSES；但无 GLOBAL_ACTION_BACK/HOME 的静态调用证据，实现位于加密载荷。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：①监听 UI 栈出现 android.settings.ACCESSIBILITY_SETTINGS（com.android.settings/.Settings$AccessibilitySettings 或厂商等价页）的瞬间立即抓取前后两层界面；②应用进程 :psx 启动或收到 BOOT_COMPLETED/USER_PRESENT 后 3~10 秒内出现的首个新 Activity（解密载荷首屏）；③直接进入系统无障碍列表定位 label 为 "Get more money" 的服务项。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：引导文案、弹窗布局、跳转序列与拒权循环 100% 不在静态包内，位于 assets 两份高熵加密 data 且由自研 SO（无商业壳特征，apkid 仅报 dx/r8 无 marker）在 native 层解密；纯静态/纯 UTG-文本 检测在“首次运行前”完全无话术可见。另需注意：无障碍服务 label 为纯收益诱导短语且无 description，若检测规则要求“存在引导文案”才判定，本样本会被漏判，应以“空壳 Translucent Activity + 无 description 的全量读屏服务 + 加密 assets”组合特征作为替代判据。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项（唯一静态可见引导触点）** | com.android.settings 无障碍页中 title="Get more money" 的列表项，无 summary/description 副文本 | 这是用户唯一能看到的“诱导入口”，服务名直白承诺收益且与桌面名不一致，是判定伪装身份的关键静态+运行期双证据 | 列表项文本 Get more money 且 summary 为空；同包另有 SystemSafeguard 出现在通知使用权列表；包名 loaddex.hb.com.loaddex.psx 出现在两个不同权限列表 |
| **跳转前/跳转后的引导页或遮罩层（运行期解密生成）** | 非 com.android.settings 包名的全屏 Activity 或 TYPE_APPLICATION_OVERLAY 窗口，出现在无障碍设置页之上或紧随其后 | 静态包内零文案零布局，该页面是唯一能证明“逐步引导话术”存在的位置；捕获它才能补齐引导链证据 | 窗口层级中同时存在 settings 页与异包 overlay；界面出现 money/earn/enable service/step 等诱导词；出现指向无障碍开关位置的箭头或高亮框 |
| **解密载荷首屏（后台拉起后的可见界面）** | 进程 :psx 下新出现的 Activity 或 WebView 容器，包名 loaddex.hb.com.loaddex.psx | 确认加密载荷落地后是否生成原生 Dialog / 本地 HTML / 远端 WebView，从而确定 ui_carrier 类型 | WebView 节点出现（本地 file:///android_asset 或远端 http）；Dialog 按钮文本与取消按钮是否存在；页面文本语言（该家族常见俄/葡/英多语） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `loaddex.hb.com.loaddex.psx.Activitypsx.onCreate`
- `loaddex.hb.com.loaddex.psx.Servicepsx.onCreate`
- `loaddex.hb.com.loaddex.psx.Servicepsx.Servicepsx_c`
- `loaddex.hb.com.loaddex.psx.Receiverpsx.onReceive`
- `res/xml-v13/accessibility.xml`
- `assets/loaddex.hb.com.loaddex.psx.data`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**核心判断：该样本在静态可见范围内没有任何“逐步引导”页面流转，其无障碍开启引导链整体藏在加密载荷与 native 层，`static_visibility = packed_or_encrypted`。**

已核实的结构事实：

- **无界面外壳**：唯一 Activity [Activitypsx.onCreate()](<resource-unit:#1.dex1 code:loaddex.hb.com.loaddex.psx.Activitypsx#onCreate>) 只调用 `super.onCreate()`，既无 `setContentView`，也无弹窗、无跳转；Manifest 中该 Activity 为 `Theme.Translucent` + `excludeFromRecents`，即启动后立即消失的空壳页。
- **无障碍服务是唯一“门面”**：`Accessibilitypsx` 的 `android:label="Get more money"`，与桌面显示名 `helpserver` 不一致；[res/xml/accessibility.xml](<resource-unit:#1 file:res/xml/accessibility.xml>) 是完全空配置，仅 v13 版本 [res/xml-v13/accessibility.xml](<resource-unit:#1 file:res/xml-v13/accessibility.xml>) 带 `typeAllMask` + `canRetrieveWindowContent="true"` + `notificationTimeout="100"`；Manifest 未设 `android:description`，因此系统无障碍列表中无任何功能说明。同进程另注册 label 为 `SystemSafeguard` 的通知监听服务。
- **全包无引导文案载体**：`res/values/strings.xml` 仅 `app_name=apk`；无 layout、无 HTML/WebView、无 Dialog；DEX 全文检索 `accessibility`、`Settings`、`http` 均无命中，即**不存在 `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 静态跳转点**，也不存在拒权重跳逻辑。
- **入口全部下沉 native**：[Servicepsx.onCreate()](<resource-unit:#1.dex1 code:loaddex.hb.com.loaddex.psx.Servicepsx#onCreate>) 与 `Receiverpsx.onReceive` 均只做 `cc.cc()` 后直调 JNI 声明 [Servicepsx_c()](<resource-unit:#1.dex1 code:loaddex.hb.com.loaddex.psx.Servicepsx#Servicepsx_c>)，实现在 [JNI_OnLoad@0x31f8](<resource-unit:#1.so1 code:JNI_OnLoad@0x31f8>)；广播覆盖 `BOOT_COMPLETED`(priority 2147483646)、`USER_PRESENT`、`PACKAGE_ADDED/REMOVED`、`CONNECTIVITY_CHANGE`，均可后台拉起。
- **载荷加密**：[assets/loaddex.hb.com.loaddex.psx.data](<resource-unit:#1 file:assets/loaddex.hb.com.loaddex.psx.data>)（183857 B）与 [assets/cloaddex.hb.com.loaddex.psx.data](<resource-unit:#1 file:assets/cloaddex.hb.com.loaddex.psx.data>)（13620 B）为高熵二进制，无 `dex\n03` 魔数、可打印字符仅 36.7%、无任何明文文案或 URL；SO 导入表仅 `fopen/fwrite/unlink/access/stat`，与“解密落盘后自行加载”的行为一致。apkid 未识别出商业壳，属自研加密投递器。

**因此**：用户实际接触到的“引导”只有系统无障碍列表里一个语义可疑的服务名（`Get more money`）。真正的话术、弹窗、遮罩与跳转序列由加密载荷运行期解密产生，静态不可还原；UTG 检测必须放在“无障碍设置页被拉起”与“解密后首屏 Activity 出现”两个运行期瞬间。

已登记风险：**R-001**（`malware_trojan` / high，`autonomous_audit`）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、无障碍配置 xml、DEX 外壳与 assets 密文均完整可见，但无障碍开启的引导页面、话术文案、跳转与拒权重试逻辑完全不在 DEX/资源内：全部位于 assets 下两份高熵加密数据（loaddex...data 183857B / cloaddex...data 13620B，无 dex 魔数、可打印率 36.7%、零明文 URL 与文案），由 libloaddex.hb.com.loaddex.psx.so 的 JNI_OnLoad 及 Servicepsx_c/Receiverpsx_r 在 native 层解密执行；全包无 layout、无 HTML、无引导字符串，故运行期页面流转不可静态还原。",
  "summary_one_liner": "无界面空壳 Activity + 后台服务经 native 解密加密载荷，静默注册 label 为 \"Get more money\"、typeAllMask/canRetrieveWindowContent 的无障碍服务，不提供任何 description 或前置说明，引导流程全在解密载荷中运行期生成。",
  "disguise_identity": {
    "app_display_name": "helpserver",
    "claimed_brand_or_persona": "无任何页面宣称（应用无可见界面，无 WebView、无弹窗、无文案资源）；唯一对用户可见的身份信息是无障碍服务名 \"Get more money\" 与通知监听服务名 \"SystemSafeguard\"",
    "a11y_service_label": "Get more money",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍 label 为 \"Get more money\"（直白表达收益诱导），与桌面显示名 helpserver、应用内 strings app_name=apk 三者互不一致；2) 同进程另一服务伪装成系统语义 \"SystemSafeguard\"；3) 无障碍未声明 android:description，系统列表中无任何能力说明；4) res/xml/accessibility.xml 为空配置、仅 xml-v13 才带 typeAllMask 全量事件与读屏权限，规避低版本检查；5) 全部类名统一加 psx 后缀、无意义单方法 cc.cc() 作 native 桥；6) 唯一 Activity 为 Theme.Translucent + excludeFromRecents + 空 onCreate，启动即消失不留痕。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "loaddex.hb.com.loaddex.psx.Activitypsx（Theme.Translucent，process=:psx，excludeFromRecents=true）",
      "trigger_event": "Launcher 点击启动 / onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面内容，仅调用 super.onCreate() 后即结束，无 setContentView、无 Dialog、无跳转",
      "user_action_requested": "无（用户看不到任何页面，也无取消/跳过控件）",
      "code_anchor": "loaddex.hb.com.loaddex.psx.Activitypsx.onCreate"
    },
    {
      "step": 2,
      "stage": "获权后动作（能力植入）",
      "screen_or_component": "loaddex.hb.com.loaddex.psx.Servicepsx（process=:psx，exported，action=ServicepsxTil，priority=1000）与 Receiverpsx（BOOT_COMPLETED priority=2147483646 / USER_PRESENT / PACKAGE_ADDED / PACKAGE_REMOVED / CONNECTIVITY_CHANGE）",
      "trigger_event": "Service.onCreate / onStartCommand / Receiver.onReceive → cc.cc() → Servicepsx_c(Context,Intent) / Receiverpsx_r(Object,Object) 等 JNI 声明",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台服务与广播接收器只做一次 cc.cc() 后直接调用 native 方法，无任何 UI 与文案；具体行为由 SO 解密 assets 密文后决定",
      "user_action_requested": "不可静态还原",
      "code_anchor": "loaddex.hb.com.loaddex.psx.Servicepsx.onCreate / Servicepsx.Servicepsx_c / Receiverpsx.onReceive"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置（运行期，不可静态还原）",
      "screen_or_component": "预期由 native 解密载荷拉起 android.settings.ACCESSIBILITY_SETTINGS，或叠加悬浮窗/引导页；静态代码中无对应 Intent 字符串",
      "trigger_event": "不可静态还原（推测由 JNI_OnLoad 后的解密模块触发）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（DEX 与资源中无任何引导文案、无 ACTION_ACCESSIBILITY_SETTINGS/ACTION_APPLICATION_DETAILS_SETTINGS 字面量）",
      "shown_text_zh": "无法静态确认；全包检索 accessibility / Settings / http 在代码与资源中零命中",
      "user_action_requested": "不可静态还原",
      "code_anchor": "#1.so1 JNI_OnLoad@0x31f8（载荷入口）；assets/loaddex.hb.com.loaddex.psx.data、assets/cloaddex.hb.com.loaddex.psx.data（加密载荷）"
    },
    {
      "step": 4,
      "stage": "系统无障碍列表（唯一静态可见的用户触点）",
      "screen_or_component": "系统设置 → 无障碍 → 已安装服务列表项 loaddex.hb.com.loaddex.psx.Accessibilitypsx",
      "trigger_event": "用户手动进入系统无障碍设置",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Get more money",
      "shown_text_zh": "“赚更多钱”——系统无障碍列表中显示的服务名，无副标题/说明（未声明 android:description）",
      "user_action_requested": "用户需自行点击开关启用；该服务本身不提供任何用途说明、无隐私承诺、无取消按钮概念",
      "code_anchor": "AndroidManifest.xml service android:label=\"Get more money\" + res/xml-v13/accessibility.xml（typeAllMask, canRetrieveWindowContent=true, notificationTimeout=100）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项标题：AndroidManifest 中 Accessibilitypsx 的 android:label=\"Get more money\"（无 description，故列表内无任何能力说明文字）",
    "系统通知使用权列表项标题：Notificationpsx 的 android:label=\"SystemSafeguard\"（伪装系统安全组件语义）",
    "应用桌面图标名：android:label=\"helpserver\"（与上述两个服务名均不一致）",
    "res/values/strings.xml 仅 app_name=apk，无任何引导/说明文案",
    "无 layout 目录、无 Dialog、无 assets 内 HTML/WebView 页面、无悬浮窗布局——静态包内不存在任何引导文字呈现位置",
    "运行期可能出现的引导弹窗/遮罩/WebView 文案：由 assets 下两份加密 data 在 native 层解密后生成，静态不可见"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Get more money",
      "text_zh": "赚更多钱",
      "source_location": "AndroidManifest.xml → service loaddex.hb.com.loaddex.psx.Accessibilitypsx android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "SystemSafeguard",
      "text_zh": "系统安全防护（伪装为系统级安全组件）",
      "source_location": "AndroidManifest.xml → service loaddex.hb.com.loaddex.psx.Notificationpsx android:label",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "helpserver",
      "text_zh": "帮助服务器",
      "source_location": "AndroidManifest.xml → application android:label（桌面显示名）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "apk",
      "text_zh": "apk（占位式应用名，未本地化）",
      "source_location": "res/values/strings.xml → app_name",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "静态代码中不存在 onResume/Timer 重跳逻辑：唯一 Activity 的 onCreate 为空且无生命周期重写，DEX 内无 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 字面量。若存在拒权重试循环，只能由 native 解密载荷在运行期实现，需动态观测确认。",
    "overlay_or_fake_settings": "静态包内无悬浮窗布局、无高仿设置页布局；但已申请 SYSTEM_ALERT_WINDOW 权限，且无障碍配置为 typeAllMask + canRetrieveWindowContent=true，具备在设置页之上叠加遮罩/引导层的技术条件，实际叠层内容在加密载荷内。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=19，无需受限设置授权；静态无相关教学文案）",
    "post_grant_anti_removal": "静态不可确认。可确认的支撑条件：无障碍服务为 typeAllMask 全量事件（可监听设置页交互并执行全局动作）+ SYSTEM_ALERT_WINDOW 悬浮窗 + WRITE_SETTINGS + KILL_BACKGROUND_PROCESSES；但无 GLOBAL_ACTION_BACK/HOME 的静态调用证据，实现位于加密载荷。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "①监听 UI 栈出现 android.settings.ACCESSIBILITY_SETTINGS（com.android.settings/.Settings$AccessibilitySettings 或厂商等价页）的瞬间立即抓取前后两层界面；②应用进程 :psx 启动或收到 BOOT_COMPLETED/USER_PRESENT 后 3~10 秒内出现的首个新 Activity（解密载荷首屏）；③直接进入系统无障碍列表定位 label 为 \"Get more money\" 的服务项。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项（唯一静态可见引导触点）",
        "page_identifier": "com.android.settings 无障碍页中 title=\"Get more money\" 的列表项，无 summary/description 副文本",
        "why_most_useful": "这是用户唯一能看到的“诱导入口”，服务名直白承诺收益且与桌面名不一致，是判定伪装身份的关键静态+运行期双证据",
        "observable_utg_signals": ["列表项文本 Get more money 且 summary 为空", "同包另有 SystemSafeguard 出现在通知使用权列表", "包名 loaddex.hb.com.loaddex.psx 出现在两个不同权限列表"]
      },
      {
        "page_role": "跳转前/跳转后的引导页或遮罩层（运行期解密生成）",
        "page_identifier": "非 com.android.settings 包名的全屏 Activity 或 TYPE_APPLICATION_OVERLAY 窗口，出现在无障碍设置页之上或紧随其后",
        "why_most_useful": "静态包内零文案零布局，该页面是唯一能证明“逐步引导话术”存在的位置；捕获它才能补齐引导链证据",
        "observable_utg_signals": ["窗口层级中同时存在 settings 页与异包 overlay", "界面出现 money/earn/enable service/step 等诱导词", "出现指向无障碍开关位置的箭头或高亮框"]
      },
      {
        "page_role": "解密载荷首屏（后台拉起后的可见界面）",
        "page_identifier": "进程 :psx 下新出现的 Activity 或 WebView 容器，包名 loaddex.hb.com.loaddex.psx",
        "why_most_useful": "确认加密载荷落地后是否生成原生 Dialog / 本地 HTML / 远端 WebView，从而确定 ui_carrier 类型",
        "observable_utg_signals": ["WebView 节点出现（本地 file:///android_asset 或远端 http）", "Dialog 按钮文本与取消按钮是否存在", "页面文本语言（该家族常见俄/葡/英多语）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：引导文案、弹窗布局、跳转序列与拒权循环 100% 不在静态包内，位于 assets 两份高熵加密 data 且由自研 SO（无商业壳特征，apkid 仅报 dx/r8 无 marker）在 native 层解密；纯静态/纯 UTG-文本 检测在“首次运行前”完全无话术可见。另需注意：无障碍服务 label 为纯收益诱导短语且无 description，若检测规则要求“存在引导文案”才判定，本样本会被漏判，应以“空壳 Translucent Activity + 无 description 的全量读屏服务 + 加密 assets”组合特征作为替代判据。"
  },
  "behavior_pattern_tags": [
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "loaddex.hb.com.loaddex.psx.Activitypsx.onCreate",
    "loaddex.hb.com.loaddex.psx.Servicepsx.onCreate",
    "loaddex.hb.com.loaddex.psx.Servicepsx.Servicepsx_c",
    "loaddex.hb.com.loaddex.psx.Receiverpsx.onReceive",
    "res/xml-v13/accessibility.xml",
    "assets/loaddex.hb.com.loaddex.psx.data"
  ]
}
```

</details>

# MR_072__9d4ce9cce7｜Cerberus — Android System Update 

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：97.4s

## 1. 一句话核心结论

- **核心申请方式**：以“Android System Update ”（尾随空格）为桌面名、意大利语“Aggiornamento del sistema”为无障碍服务标签，静默声明可读取全屏窗口内容且无任何用途说明的无障碍服务，实际引导页面与文案藏于加密载荷动态加载阶段，静态不可见。
- **静态可见性说明**：Manifest 与无障碍配置文件可见，但引导实现完全不可静态还原：classes.dex 明文符号表被抹除（ACCESSIBILITY_SETTINGS/Settings/accessibility 等字符串零命中），Manifest 声明的 venue.join.prepare.crqi 无障碍服务类与 ubrjliy 启动 Activity 在 DEX 中不存在（venue 包 0 个类），res/values 无 strings.xml（label_guide/label_success 等文案未解码），assets/jhJfI.json 471KB 为二进制密文，判定为二阶段解密 dex/资源动态加载，引导 UI 与逐字文案需运行期捕获。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9d4ce9cce72ec64761014aecbf1076041a8d790771fa8f8899bd3e2b2758281d` |
| 包名 / 年份 | `tail.curious.matrix` / 2020 |
| 家族 / 品类 | **Cerberus**（同池样本数：8） |
| 原始来源标识 | https://www.secureauth.com/blog/hijacking-2fa-a-look-at-mobile-malware-through-an-identity-lens/ |
| 桌面显示名 | Android System Update |
| 引导页宣称品牌/身份 | Android 系统更新 / Aggiornamento del sistema（伪造系统更新组件） |
| 系统无障碍列表服务名 | Aggiornamento del sistema |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：桌面名与无障碍服务标签均冒充系统更新，且桌面名末尾带尾随空格以在启动器/列表中挤出或错位显示；无障碍服务未设置 android:description（系统无障碍列表内零说明）；全部组件类名 venue.join.prepare.* 与资源键名 label_meat/label_dress/label_guide/label_success 等为无意义随机串，配合 dexlib 2.x 重打包与加密 assets 载荷隐藏真实实现；Manifest 中同时存在多个 android:label="" 且 excludeFromRecents+Theme.NoDisplay 的不可见 Activity（vrkmpd/ocpvniq/dnvkrtd）用于静默中转。 |
| 无障碍服务类名 | `venue.join.prepare.crqi` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | venue.join.prepare.ubrjliy（LAUNCHER 入口 Activity，类体不在 DEX 中） | 点击桌面图标 / android.intent.action.MAIN + LAUNCHER | 不可静态还原 | 无 | 不可静态还原 | `AndroidManifest.xml: activity venue.join.prepare.ubrjliy (MAIN/LAUNCHER)` |
| 2 | 引导说明页 | venue.join.prepare.NIbYyKkDtRmWaBjBpSiUcMbOqCyEtYmInGkPe（android:label="label_guide"）及 label_sure/label_observe/label_naive 等多页引导 Activity | 由入口 Activity 或解密载荷按 label_guide→label_sure→label_observe 顺序拉起 | 不可静态还原 | **原文**：无（label_guide 等字符串未在 res/values 解码，res 中无 strings.xml）<br>**译注**：存在名为“引导/确认/观察/天真”等命名的多步说明页，文案不可静态读取 | 不可静态还原（是否存在取消/跳过按钮需运行期观察） | `AndroidManifest.xml: venue.join.prepare.NIbYyKkDtRmWaBjBpSiUcMbOqCyEtYmInGkPe (label_guide)` |
| 3 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（应用侧发起代码不可见） | 不可静态还原（应用代码中未检出 ACTION_ACCESSIBILITY_SETTINGS 明文字符串，推测由解密载荷动态构造 Intent） | 系统无障碍页 | 无 | 手动在系统无障碍列表中找到并开启“Aggiornamento del sistema” | `res/xml/yfnrigjlmooqrzyx.xml + AndroidManifest.xml: service venue.join.prepare.crqi` |
| 4 | 获权后动作 | venue.join.prepare.crqi（AccessibilityService，canRetrieveWindowContent=true，监听 typeWindowContentChanged\|typeWindowStateChanged） | 系统绑定服务后回调 onServiceConnected/onAccessibilityEvent | 不可静态还原 | 无 | 无 | `res/xml/yfnrigjlmooqrzyx.xml (accessibilityFlags/canRetrieveWindowContent)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目名称：Aggiornamento del sistema（Manifest service android:label），其 android:description 为空 —— 系统授权页对用户零说明
- 桌面启动器名称：Android System Update （application android:label，末尾含尾随空格）
- 应用内多步引导页（label_guide / label_sure / label_observe / label_naive / label_success / label_draft 等 label 资源 Activity）：文案存于未解码资源或运行期解密资源，静态不可见
- res/values 目录内不存在 strings.xml，res/xml 无障碍配置不含任何描述文本；assets/jhJfI.json 为密文，可能承载 HTML/文案资源但不可静态解出

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Android System Update | 安卓系统更新（末尾含一个尾随空格） | `AndroidManifest.xml: <application android:label>` | 假更新 |
| it | Aggiornamento del sistema | 系统更新 | `AndroidManifest.xml: service venue.join.prepare.crqi android:label` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：引导与重跳逻辑位于加密载荷（assets/jhJfI.json 解密 dex），代码中无 ACTION_ACCESSIBILITY_SETTINGS 明文与 onResume 死循环可见证据，需运行期 Hook onResume/startActivity 观测
- **遮罩叠层 / 高仿系统设置页**：不可静态还原；但无障碍配置 flagIncludeNotImportantViews+flagReportViewIds+typeWindowContentChanged 支持精确读取系统设置页控件，具备在真实无障碍页上叠放半透明遮罩/伪造开关页并代为点击开关的技术前提
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=27，未声明 13+ 受限设置相关引导；且无明文文本可证）
- **获权后即时行为与防撤权机制**：不可静态还原；Manifest 同时声明 BIND_DEVICE_ADMIN 设备管理接收器 venue.join.prepare.dsagzeuskgxzqr（res/xml/kaxvruu）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，具备防卸载/保活的静态前提，但 GLOBAL_ACTION_BACK/HOME 阻止撤权行为未见明文
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到系统无障碍设置页（com.android.settings/.Settings$AccessibilitySettings 或 accessibility 相关 Settings Activity）被拉起即开始录屏；或监测到无障碍服务 venue.join.prepare.crqi 被 enable（AccessibilityManager 中服务状态变更）时立即截取当前栈顶页面
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：显著盲区：一阶段为纯外壳，Manifest 声明的入口与无障碍服务类在 DEX 中不存在，明文符号表被抹除、assets/jhJfI.json 为二进制密文，引导 UI 与文案在二阶段解密后才出现；若解密依赖远程下发或设备指纹校验，UTG 冷启动可能只看到空白/闪退外壳，需在联网且真实设备指纹条件下多次冷启动并在无障碍设置页出现时回溯栈。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/引导说明页** | LAUNCHER 入口 venue.join.prepare.ubrjliy 之后的第一个应用内页面，标签资源 label_guide/label_sure | 这是判定“是否零步骤强制引导”与是否提供取消/跳过的唯一直接证据，静态完全不可见 | 是否存在可点击的取消/跳过/稍后按钮；是否只有单一“去开启/继续”按钮；文案是否声称系统更新或安全风险；页面是否为 WebView 承载 |
| **跳转前教学页/遮罩页** | ACCESSIBILITY_SETTINGS 被拉起前 1 个页面；或设置页上叠加的非系统窗口（悬浮窗/半透明遮罩） | 区分“正常引导用户手动开启”与“叠层遮挡真实开关并伪造开关页”的关键；本样本无障碍权限足以读取设置页控件 ID | 设置页之上是否存在非 com.android.settings 包名的窗口节点；是否有与系统开关同位置的自绘开关控件；是否出现指向右上角菜单/应用详情的分步图示 |
| **系统无障碍服务列表项** | 设置→无障碍→已下载的服务中的条目文本 Aggiornamento del sistema | 确证伪装身份与系统授权页零说明（无 description），是身份不符的客观锚点 | 条目名称是否为系统更新类文案；条目下方是否缺少用途说明文本；是否同时出现与桌面名 Android System Update 的错位/尾随空格现象 |
| **获权后动作页** | 无障碍服务 enable 后 800ms 内的栈顶 Activity/悬浮窗（label_success / label_observe 等） | 判断获权后是进入良性功能还是立即启动覆盖层/后台窃取，闭合整条链路 | 是否立即关闭引导页并转入后台；是否出现悬浮窗权限申请或 SYSTEM_ALERT_WINDOW 相关页面；是否出现短信/联系人/通话相关界面或后台服务拉起 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `AndroidManifest.xml: <service android:name="venue.join.prepare.crqi" android:label="Aggiornamento del sistema" android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE">`
- `res/xml/yfnrigjlmooqrzyx.xml（canRetrieveWindowContent=true, flagIncludeNotImportantViews|flagReportViewIds, 无 android:description）`
- `AndroidManifest.xml: <application android:label="Android System Update "> / activity venue.join.prepare.ubrjliy (MAIN/LAUNCHER)`
- `assets/jhJfI.json（471KB 二进制密文载荷）`
- `AndroidManifest.xml: receiver venue.join.prepare.dsagzeuskgxzqr (BIND_DEVICE_ADMIN, res/xml/kaxvruu)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 定向核验结论（UTG 视角）

**一句话**：该样本的无障碍引导链路**无法静态还原**：`classes.dex` 为 4.5MB 且**明文符号表被抹除**（连 `Settings`/`accessibility` 等框架字符串都零命中），Manifest 声明的全部 `venue.join.prepare.*` 组件**在 DEX 中不存在**，实际引导 UI 与文案藏于加密载荷/动态加载阶段。

已核实事实（4 项，均来自包内静态证据）：

1. **无障碍服务真实存在且高权限**：[AndroidManifest.xml（service `venue.join.prepare.crqi`）](<resource-unit:#1 manifest:components>) 声明 `android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE"`，服务标签为意大利语 `Aggiornamento del sistema`（“系统更新”），而桌面名为 `Android System Update `（**末尾含尾随空格**，典型的图标区/列表区名称挤出与撞名手法）。
2. **配置文件无任何用户可见说明**：[res/xml/yfnrigjlmooqrzyx.xml](<resource-unit:#1 file:res/xml/yfnrigjlmooqrzyx.xml>) 只有 `accessibilityEventTypes=typeWindowContentChanged|typeWindowStateChanged`、`flagIncludeNotImportantViews|flagReportViewIds`、`canRetrieveWindowContent="true"`，**无 `android:description`、无 `packageNames` 限定** —— 即申请“读取全屏窗口内容+控件 ID”的全域监听能力，且系统无障碍列表里对用户**不显示任何用途说明**。
3. **引导文案不在资源中**：解包后 `res/values/` 仅有 `attrs/ids/public`，**没有 strings.xml**；Manifest 大量 `label_guide`/`label_success`/`label_sure`/`label_observe` 等标签指向未解码资源，说明多步引导页（说明页→设置→成功页）的文案刻意不可静态获取。
4. **代码层为二阶段载荷**：`assets/jhJfI.json`（471KB）为**二进制密文**（非 JSON 文本）；`search_text_in_app`/`strings` 对 `ACCESSIBILITY_SETTINGS`、`crqi`、`ubrjliy` 全部零命中；`list_codebase` 中 `venue` 包 **0 个类**（实际类分布在 `tail`/`better`/`poem` 等混淆包）。即 Manifest 声明的无障碍服务类与入口 Activity 在运行期由**解密后的 dex 动态注入**。

因此：`static_visibility = packed_or_encrypted`。可确认的仅有“**伪装系统更新的无障碍服务 + 全域窗口读取能力 + 零说明**”这一授权前提，**具体是冷启动弹窗、WebView 教学页还是叠层遮罩指引，静态不可判定**，必须靠 UTG 在运行期抓取。

给 UTG 的关键提示：不要盯冷启动首页（首页可能只是无害外壳），应以**系统无障碍设置页出现 `Aggiornamento del sistema` 条目**为锚点，向前回溯压栈页面，向后捕获获权后的跳转。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest 与无障碍配置文件可见，但引导实现完全不可静态还原：classes.dex 明文符号表被抹除（ACCESSIBILITY_SETTINGS/Settings/accessibility 等字符串零命中），Manifest 声明的 venue.join.prepare.crqi 无障碍服务类与 ubrjliy 启动 Activity 在 DEX 中不存在（venue 包 0 个类），res/values 无 strings.xml（label_guide/label_success 等文案未解码），assets/jhJfI.json 471KB 为二进制密文，判定为二阶段解密 dex/资源动态加载，引导 UI 与逐字文案需运行期捕获。",
  "summary_one_liner": "以“Android System Update ”（尾随空格）为桌面名、意大利语“Aggiornamento del sistema”为无障碍服务标签，静默声明可读取全屏窗口内容且无任何用途说明的无障碍服务，实际引导页面与文案藏于加密载荷动态加载阶段，静态不可见。",
  "disguise_identity": {
    "app_display_name": "Android System Update ",
    "claimed_brand_or_persona": "Android 系统更新 / Aggiornamento del sistema（伪造系统更新组件）",
    "a11y_service_label": "Aggiornamento del sistema",
    "identity_mismatch": true,
    "obfuscation_tricks": "桌面名与无障碍服务标签均冒充系统更新，且桌面名末尾带尾随空格以在启动器/列表中挤出或错位显示；无障碍服务未设置 android:description（系统无障碍列表内零说明）；全部组件类名 venue.join.prepare.* 与资源键名 label_meat/label_dress/label_guide/label_success 等为无意义随机串，配合 dexlib 2.x 重打包与加密 assets 载荷隐藏真实实现；Manifest 中同时存在多个 android:label=\"\" 且 excludeFromRecents+Theme.NoDisplay 的不可见 Activity（vrkmpd/ocpvniq/dnvkrtd）用于静默中转。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "venue.join.prepare.ubrjliy（LAUNCHER 入口 Activity，类体不在 DEX 中）",
      "trigger_event": "点击桌面图标 / android.intent.action.MAIN + LAUNCHER",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "入口界面内容不可静态获取（代码位于加密载荷，运行期解密加载）",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml: activity venue.join.prepare.ubrjliy (MAIN/LAUNCHER)"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "venue.join.prepare.NIbYyKkDtRmWaBjBpSiUcMbOqCyEtYmInGkPe（android:label=\"label_guide\"）及 label_sure/label_observe/label_naive 等多页引导 Activity",
      "trigger_event": "由入口 Activity 或解密载荷按 label_guide→label_sure→label_observe 顺序拉起",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（label_guide 等字符串未在 res/values 解码，res 中无 strings.xml）",
      "shown_text_zh": "存在名为“引导/确认/观察/天真”等命名的多步说明页，文案不可静态读取",
      "user_action_requested": "不可静态还原（是否存在取消/跳过按钮需运行期观察）",
      "code_anchor": "AndroidManifest.xml: venue.join.prepare.NIbYyKkDtRmWaBjBpSiUcMbOqCyEtYmInGkPe (label_guide)"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（应用侧发起代码不可见）",
      "trigger_event": "不可静态还原（应用代码中未检出 ACTION_ACCESSIBILITY_SETTINGS 明文字符串，推测由解密载荷动态构造 Intent）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "跳转至系统“无障碍”设置，列表中服务条目显示“Aggiornamento del sistema”",
      "user_action_requested": "手动在系统无障碍列表中找到并开启“Aggiornamento del sistema”",
      "code_anchor": "res/xml/yfnrigjlmooqrzyx.xml + AndroidManifest.xml: service venue.join.prepare.crqi"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "venue.join.prepare.crqi（AccessibilityService，canRetrieveWindowContent=true，监听 typeWindowContentChanged|typeWindowStateChanged）",
      "trigger_event": "系统绑定服务后回调 onServiceConnected/onAccessibilityEvent",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后读取全屏窗口内容与控件 ID（可用于覆盖层注入与界面内容窃取），无包名白名单限制",
      "user_action_requested": "无",
      "code_anchor": "res/xml/yfnrigjlmooqrzyx.xml (accessibilityFlags/canRetrieveWindowContent)"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目名称：Aggiornamento del sistema（Manifest service android:label），其 android:description 为空 —— 系统授权页对用户零说明",
    "桌面启动器名称：Android System Update （application android:label，末尾含尾随空格）",
    "应用内多步引导页（label_guide / label_sure / label_observe / label_naive / label_success / label_draft 等 label 资源 Activity）：文案存于未解码资源或运行期解密资源，静态不可见",
    "res/values 目录内不存在 strings.xml，res/xml 无障碍配置不含任何描述文本；assets/jhJfI.json 为密文，可能承载 HTML/文案资源但不可静态解出"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Android System Update ",
      "text_zh": "安卓系统更新（末尾含一个尾随空格）",
      "source_location": "AndroidManifest.xml: <application android:label>",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "it",
      "text_verbatim": "Aggiornamento del sistema",
      "text_zh": "系统更新",
      "source_location": "AndroidManifest.xml: service venue.join.prepare.crqi android:label",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：引导与重跳逻辑位于加密载荷（assets/jhJfI.json 解密 dex），代码中无 ACTION_ACCESSIBILITY_SETTINGS 明文与 onResume 死循环可见证据，需运行期 Hook onResume/startActivity 观测",
    "overlay_or_fake_settings": "不可静态还原；但无障碍配置 flagIncludeNotImportantViews+flagReportViewIds+typeWindowContentChanged 支持精确读取系统设置页控件，具备在真实无障碍页上叠放半透明遮罩/伪造开关页并代为点击开关的技术前提",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=27，未声明 13+ 受限设置相关引导；且无明文文本可证）",
    "post_grant_anti_removal": "不可静态还原；Manifest 同时声明 BIND_DEVICE_ADMIN 设备管理接收器 venue.join.prepare.dsagzeuskgxzqr（res/xml/kaxvruu）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，具备防卸载/保活的静态前提，但 GLOBAL_ACTION_BACK/HOME 阻止撤权行为未见明文",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到系统无障碍设置页（com.android.settings/.Settings$AccessibilitySettings 或 accessibility 相关 Settings Activity）被拉起即开始录屏；或监测到无障碍服务 venue.join.prepare.crqi 被 enable（AccessibilityManager 中服务状态变更）时立即截取当前栈顶页面",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/引导说明页",
        "page_identifier": "LAUNCHER 入口 venue.join.prepare.ubrjliy 之后的第一个应用内页面，标签资源 label_guide/label_sure",
        "why_most_useful": "这是判定“是否零步骤强制引导”与是否提供取消/跳过的唯一直接证据，静态完全不可见",
        "observable_utg_signals": ["是否存在可点击的取消/跳过/稍后按钮", "是否只有单一“去开启/继续”按钮", "文案是否声称系统更新或安全风险", "页面是否为 WebView 承载"]
      },
      {
        "page_role": "跳转前教学页/遮罩页",
        "page_identifier": "ACCESSIBILITY_SETTINGS 被拉起前 1 个页面；或设置页上叠加的非系统窗口（悬浮窗/半透明遮罩）",
        "why_most_useful": "区分“正常引导用户手动开启”与“叠层遮挡真实开关并伪造开关页”的关键；本样本无障碍权限足以读取设置页控件 ID",
        "observable_utg_signals": ["设置页之上是否存在非 com.android.settings 包名的窗口节点", "是否有与系统开关同位置的自绘开关控件", "是否出现指向右上角菜单/应用详情的分步图示"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置→无障碍→已下载的服务中的条目文本 Aggiornamento del sistema",
        "why_most_useful": "确证伪装身份与系统授权页零说明（无 description），是身份不符的客观锚点",
        "observable_utg_signals": ["条目名称是否为系统更新类文案", "条目下方是否缺少用途说明文本", "是否同时出现与桌面名 Android System Update 的错位/尾随空格现象"]
      },
      {
        "page_role": "获权后动作页",
        "page_identifier": "无障碍服务 enable 后 800ms 内的栈顶 Activity/悬浮窗（label_success / label_observe 等）",
        "why_most_useful": "判断获权后是进入良性功能还是立即启动覆盖层/后台窃取，闭合整条链路",
        "observable_utg_signals": ["是否立即关闭引导页并转入后台", "是否出现悬浮窗权限申请或 SYSTEM_ALERT_WINDOW 相关页面", "是否出现短信/联系人/通话相关界面或后台服务拉起"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "显著盲区：一阶段为纯外壳，Manifest 声明的入口与无障碍服务类在 DEX 中不存在，明文符号表被抹除、assets/jhJfI.json 为二进制密文，引导 UI 与文案在二阶段解密后才出现；若解密依赖远程下发或设备指纹校验，UTG 冷启动可能只看到空白/闪退外壳，需在联网且真实设备指纹条件下多次冷启动并在无障碍设置页出现时回溯栈。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "AndroidManifest.xml: <service android:name=\"venue.join.prepare.crqi\" android:label=\"Aggiornamento del sistema\" android:permission=\"android.permission.BIND_ACCESSIBILITY_SERVICE\">",
    "res/xml/yfnrigjlmooqrzyx.xml（canRetrieveWindowContent=true, flagIncludeNotImportantViews|flagReportViewIds, 无 android:description）",
    "AndroidManifest.xml: <application android:label=\"Android System Update \"> / activity venue.join.prepare.ubrjliy (MAIN/LAUNCHER)",
    "assets/jhJfI.json（471KB 二进制密文载荷）",
    "AndroidManifest.xml: receiver venue.join.prepare.dsagzeuskgxzqr (BIND_DEVICE_ADMIN, res/xml/kaxvruu)"
  ]
}
```

**覆盖边界与未决问题**：`venue.join.prepare.*` 全部组件在 DEX 中无类体、明文符号表被抹除，本轮的“逐步引导链路”（弹窗→设置跳转→遮罩→拒权循环）属**未证实推断**，仅“伪装系统更新 + 全域窗口读取 + 零说明授权”已由 Manifest 与无障碍配置证实。因本次定向审计工具调用预算（14 次）已用尽，未对 `assets/jhJfI.json` 做解密还原，也未向风险台账写入结论；如继续，应优先尝试解密该载荷并补录“伪装系统更新诱导无障碍授权”风险条目。

</details>

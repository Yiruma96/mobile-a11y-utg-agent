# MB_105__5f3ccbc143｜Octo — Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：174.7s

## 1. 一句话核心结论

- **核心申请方式**：以伪装成 Chrome 的壳应用承载 AES 加密二阶段 DEX，无障碍服务在系统列表中自称“保护设备”却申请读取全屏内容与控件 ID 的最高权限，真正诱导流程藏在加密载荷内。
- **静态可见性说明**：壳 Application siAq.Vm 在 attachBaseContext 中用 AES/ECB(密钥=包名MD5派生) 解密 APK 内 src/ 下两份加密资产，取得配置 JSON 后把加密 DEX 异或落盘并反射注入 dexElements，注入后删除临时文件。明文 classes.dex 中 earlysince27/p085d/accessibilityservice 等关键字 0 命中，无障碍服务实现与全部引导页面流转均位于加密载荷内；仅 Manifest 声明、无障碍配置 XML 与两条字符串（Chrome / Enable this service to protect your device）静态可见。本次按包名 MD5 派生密钥未能解出载荷明文。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `5f3ccbc143370c214b2afcbbb3d54a0f9cdc8e9e09f266800700ea0532353957` |
| 包名 / 年份 | `com.earlysince27` / 2023 |
| 家族 / 品类 | **Octo**（同池样本数：9） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Chrome |
| 引导页宣称品牌/身份 | Chrome（Google 浏览器品牌）+ 设备安全防护工具双重伪装 |
| 系统无障碍列表服务名 | Chrome |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：应用 label 与无障碍服务 label 均指向 @string/a=Chrome；Activity com.earlysince27.p040j 的 android:label 为空串；类名/包名整体混淆为 siAq、QBMyedEjW、com.earlysince27.p085d 等无意义串；加密资产文件名使用 MD5 十六进制（src/AF5EE28C7D99D788F1E2B8A0F6BBB403、src/7F718B2CAAEF2BBB9FCBC32782BFD815） |
| 无障碍服务类名 | `com.earlysince27.p085d` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | Application siAq.Vm（android:name="siAq.Vm"） | 进程启动时 attachBaseContext(Context) | 不可静态还原 | 无 | 无（用户不可见） | `siAq.Vm.attachBaseContext / siAq.Vm.loadDexByVersion` |
| 2 | 业务功能触发 | 解密载荷内真实首屏 Activity（不可静态确定） | 载荷注入完成后由载荷内 application 类接管，具体触发点不可静态还原 | 不可静态还原 | 无 | 不可静态还原 | `siAq.Vm#applcationName（来自解密 JSON 的 application 字段）` |
| 3 | 跳无障碍设置 | 系统无障碍设置页（跳转代码位于加密载荷） | 不可静态还原（预期为 ACTION_ACCESSIBILITY_SETTINGS 显式跳转） | 系统无障碍页 | **原文**：Enable this service to protect your device<br>**译注**：启用此服务以保护你的设备 | 在系统无障碍列表中找到并开启名为 Chrome 的服务（引导文案与开关流程不可静态还原） | `res/xml/xwltivwgv.xml → @string/ByxrYpmUxX；服务 com.earlysince27.p085d` |
| 4 | 获权后动作 | com.earlysince27.p085d（AccessibilityService） | 服务被绑定后 onServiceConnected（实现体在加密载荷内） | 不可静态还原 | 无 | 无 | `com.earlysince27.p085d（Manifest 声明，类体不在明文 DEX）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统设置 → 无障碍 → 已安装服务列表项标题：@string/a = "Chrome"（服务 com.earlysince27.p085d 的 android:label）
- 系统无障碍服务列表项说明文字：res/xml/xwltivwgv.xml 的 android:description = @string/ByxrYpmUxX = "Enable this service to protect your device"
- 桌面/应用列表图标名称：application android:label = @string/a = "Chrome"
- 引导弹窗/Activity/WebView/悬浮窗：实现位于 AES 加密的二阶段 DEX，静态不可见，需运行期捕获

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable this service to protect your device | 启用此服务以保护你的设备 | `res/values/strings.xml key=ByxrYpmUxX（由 res/xml/xwltivwgv.xml 的 android:description 引用）` | 假反诈安全 |
| en | Chrome | Chrome（谷歌浏览器品牌名） | `res/values/strings.xml key=a（application android:label 与无障碍服务 android:label）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：拒绝或返回后的重跳逻辑位于 AES 加密载荷，需运行期监测是否 onResume 死循环拉起无障碍设置
- **遮罩叠层 / 高仿系统设置页**：不可静态还原：Manifest 存在多个 Theme.AppCompat.Transparent.NoActionBar + excludeFromRecents 的透明 Activity（p058l、p057a、p068s、p020o），具备叠放半透明引导遮罩/伪设置页的载体条件，但实际使用方式在加密载荷内
- **Android 13+ 受限设置（Restricted Settings）应对**：无（不可静态还原，明文未见相关文案）
- **获权后即时行为与防撤权机制**：不可静态还原：同时声明 DEVICE_ADMIN 接收器 com.earlysince27.p075v（BIND_DEVICE_ADMIN）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，具备防撤权/防卸载能力，具体实现位于加密载荷
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后立即拉起并全程录屏/抓栈，在监测到跳转 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间抓取前一屏；同时在无障碍设置页停留期间持续采样，捕获 800ms 内可能压栈的透明遮罩 Activity
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：引导弹窗、文案、跳转代码与获权后行为全部位于 AES/ECB 加密的二阶段 DEX，纯静态 UTG 文本抽取只能得到系统无障碍列表中的一条描述；须依赖运行期 UTG + 动态 Hook 补齐。若载荷还从远端下发 HTML/配置，需叠加流量侧取证。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首屏（载荷注入后的真实入口）** | 启动后首个非透明 Activity，包名 com.earlysince27，可能伪装 Chrome 界面 | 确认诱导是冷启动即弹还是功能触发，是判定强制性与否的第一手依据 | 首屏 Activity 类名与包名；是否出现不可取消按钮的弹窗节点；是否已存在跳转 ACCESSIBILITY_SETTINGS 的 intent 记录 |
| **系统无障碍服务列表项** | 设置页中 label=Chrome、描述=Enable this service to protect your device 的条目 | 固化伪装身份与假安全承诺文案，是身份不匹配与诱导的直接证据 | 服务标题文本 Chrome；描述文本 Enable this service to protect your device；对应包名 com.earlysince27 |
| **跳转前引导说明页** | 跳转 ACCESSIBILITY_SETTINGS 前紧邻的 Activity/Dialog/WebView | 区分原生弹窗、本地 HTML、远端 WebView 三种载体，决定后续是否需 OCR 与网络侧取证 | WebView 节点与 URL；按钮文本与是否存在取消/跳过；倒计时或强制点击控件 |
| **设置页后压栈的透明遮罩页** | 回到应用瞬间出现的 Theme.AppCompat.Transparent.NoActionBar 全屏 Activity | 识别 COERCE_OVERLAY_STACK_ON_SETTINGS 类叠层指引，这是区分恶性引导与良性说明的关键 | 半透明覆盖层节点；覆盖层内指向系统开关位置的箭头/高亮；覆盖层是否拦截返回键 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `siAq.Vm.attachBaseContext`
- `siAq.Vm.loadDexByVersion`
- `QBMyedEjW.Pnsp.Decrypt`
- `QBMyedEjW.Jybzxm.getAssetsName`
- `res/xml/xwltivwgv.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（工具调用已用尽，按约束停止继续探索）

**1. 静态可见性：核心逻辑全部加密，无法还原 UTG 流程**
- 应用入口 `android:name="siAq.Vm"` 是壳 Application。[siAq.Vm.attachBaseContext()](<resource-unit:#1.dex1 code:siAq.Vm#attachBaseContext>) 从自身 APK 的 `src/` 读取两份加密资产：先解密配置 JSON（`application` 类名 + `dex` 列表），再用 `xorEncode` 将 DEX 写入 `getDir("ded")`，随后由 [siAq.Vm.loadDexByVersion()](<resource-unit:#1.dex1 code:siAq.Vm#loadDexByVersion>) 反射改写 `pathList.dexElements` 注入，注入后立即删除临时文件。
- 解密算法为 [QBMyedEjW.Pnsp.Decrypt()](<resource-unit:#1.dex1 code:QBMyedEjW.Pnsp#Decrypt>)：`AES/ECB/PKCS5Padding`，密钥由包名经 MD5 派生；资产名用 [QBMyedEjW.Jybzxm.getAssetsName()](<resource-unit:#1.dex1 code:QBMyedEjW.Jybzxm#getAssetsName>) 做 MD5 十六进制混淆。
- 加密资产实体：[src/AF5EE28C7D99D788F1E2B8A0F6BBB403](<resource-unit:#1 file:unknown/src/AF5EE28C7D99D788F1E2B8A0F6BBB403>)（7192B 配置）与 [src/7F718B2CAAEF2BBB9FCBC32782BFD815](<resource-unit:#1 file:unknown/src/7F718B2CAAEF2BBB9FCBC32782BFD815>)（96B）。
- 关键核验：明文 `classes.dex` 中检索 `earlysince27`、`p085d`、`accessibilityservice`、`xwltivwgv`、`ByxrYpmUxX` **全部 0 命中**；`DexClassLoader`/`InMemoryDexClassLoader` 0 命中（用反射注入，而非标准 API）。因此 **无障碍服务实现、引导弹窗、跳转 `ACTION_ACCESSIBILITY_SETTINGS` 的代码一律不在可见 DEX 内**，静态无法给出步骤级页面流转。
- 额外事实：`classes.dex` 内混入 3717 个 `com.walmart.glass` 类及 Braze、ThreatMetrix SDK，属被二次打包的宿主应用代码，与壳共同构成“正常应用外观 + 加密恶意载荷”的结构。

**2. 已确认的 Manifest/资源级诱导线索（唯一静态可见部分）**
- 无障碍服务 [com.earlysince27.p085d](<resource-unit:#1 manifest:components>)：`permission="android.permission.BIND_ACCESSIBILITY_SERVICE"`，`label="@string/a"`。
- 服务描述资源 [res/xml/xwltivwgv.xml](<resource-unit:#1 file:res/xml/xwltivwgv.xml>) 指向 `@string/ByxrYpmUxX` = **"Enable this service to protect your device"**，即系统无障碍列表中呈现的原文；同时申请 `typeAllMask`、`canRetrieveWindowContent`、`flagRetrieveInteractiveWindows`、`flagReportViewIds`——这是读取全屏内容与控件 ID 的最高权限组合，与“保护设备”的表述完全不符。
- [res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml#L1-L4>) 中 `a` = **"Chrome"**：应用桌面名称与无障碍服务名称均伪装为 Chrome；其中一个 Activity `p040j` 的 `android:label` 为空串，属典型的空白/伪装命名手法。
- 权限组合 `READ_SMS/RECEIVE_SMS/SEND_SMS/CALL_PHONE/WRITE_SETTINGS/REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` 与 `SMS_DELIVER`、`WAP_PUSH_DELIVER`、`RESPOND_VIA_MESSAGE`、`DEVICE_ADMIN` 接收器并存，构成无障碍操控 + 短信拦截 + 防卸载组合；这些组件同样在明文 DEX 中无实现。

**3. 未决问题与覆盖边界**
- AES-ECB 密钥派生与配置结构耦合，本次按包名 MD5 派生未能直接解出明文，载荷内 UTG 流程（弹窗载体、是否遮罩叠层、拒绝后是否循环重跳、13+ 受限设置教学）**未能静态证实**，需运行期动态观测（监测 `ACTION_ACCESSIBILITY_SETTINGS` 跳转与冷启动首屏）补齐。
- 已登记风险：R-001（AES 加密二阶段 DEX 载荷隐藏无障碍服务与短信窃取逻辑，malware_trojan/high）。身份伪装（label=Chrome + 空 label Activity + 假安全承诺描述）作为同一载荷结构下的证据已在 R-001 报告中说明，未单独立项。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "壳 Application siAq.Vm 在 attachBaseContext 中用 AES/ECB(密钥=包名MD5派生) 解密 APK 内 src/ 下两份加密资产，取得配置 JSON 后把加密 DEX 异或落盘并反射注入 dexElements，注入后删除临时文件。明文 classes.dex 中 earlysince27/p085d/accessibilityservice 等关键字 0 命中，无障碍服务实现与全部引导页面流转均位于加密载荷内；仅 Manifest 声明、无障碍配置 XML 与两条字符串（Chrome / Enable this service to protect your device）静态可见。本次按包名 MD5 派生密钥未能解出载荷明文。",
  "summary_one_liner": "以伪装成 Chrome 的壳应用承载 AES 加密二阶段 DEX，无障碍服务在系统列表中自称“保护设备”却申请读取全屏内容与控件 ID 的最高权限，真正诱导流程藏在加密载荷内。",
  "disguise_identity": {
    "app_display_name": "Chrome",
    "claimed_brand_or_persona": "Chrome（Google 浏览器品牌）+ 设备安全防护工具双重伪装",
    "a11y_service_label": "Chrome",
    "identity_mismatch": true,
    "obfuscation_tricks": "应用 label 与无障碍服务 label 均指向 @string/a=Chrome；Activity com.earlysince27.p040j 的 android:label 为空串；类名/包名整体混淆为 siAq、QBMyedEjW、com.earlysince27.p085d 等无意义串；加密资产文件名使用 MD5 十六进制（src/AF5EE28C7D99D788F1E2B8A0F6BBB403、src/7F718B2CAAEF2BBB9FCBC32782BFD815）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "Application siAq.Vm（android:name=\"siAq.Vm\"）",
      "trigger_event": "进程启动时 attachBaseContext(Context)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，仅执行解密与 DEX 注入",
      "user_action_requested": "无（用户不可见）",
      "code_anchor": "siAq.Vm.attachBaseContext / siAq.Vm.loadDexByVersion"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "解密载荷内真实首屏 Activity（不可静态确定）",
      "trigger_event": "载荷注入完成后由载荷内 application 类接管，具体触发点不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不可静态还原",
      "user_action_requested": "不可静态还原",
      "code_anchor": "siAq.Vm#applcationName（来自解密 JSON 的 application 字段）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（跳转代码位于加密载荷）",
      "trigger_event": "不可静态还原（预期为 ACTION_ACCESSIBILITY_SETTINGS 显式跳转）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Enable this service to protect your device",
      "shown_text_zh": "启用此服务以保护你的设备",
      "user_action_requested": "在系统无障碍列表中找到并开启名为 Chrome 的服务（引导文案与开关流程不可静态还原）",
      "code_anchor": "res/xml/xwltivwgv.xml → @string/ByxrYpmUxX；服务 com.earlysince27.p085d"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.earlysince27.p085d（AccessibilityService）",
      "trigger_event": "服务被绑定后 onServiceConnected（实现体在加密载荷内）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（结合短信/电话/设备管理权限，预期执行读屏与短信操控）",
      "user_action_requested": "无",
      "code_anchor": "com.earlysince27.p085d（Manifest 声明，类体不在明文 DEX）"
    }
  ],
  "text_presentation_locations": [
    "系统设置 → 无障碍 → 已安装服务列表项标题：@string/a = \"Chrome\"（服务 com.earlysince27.p085d 的 android:label）",
    "系统无障碍服务列表项说明文字：res/xml/xwltivwgv.xml 的 android:description = @string/ByxrYpmUxX = \"Enable this service to protect your device\"",
    "桌面/应用列表图标名称：application android:label = @string/a = \"Chrome\"",
    "引导弹窗/Activity/WebView/悬浮窗：实现位于 AES 加密的二阶段 DEX，静态不可见，需运行期捕获"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable this service to protect your device",
      "text_zh": "启用此服务以保护你的设备",
      "source_location": "res/values/strings.xml key=ByxrYpmUxX（由 res/xml/xwltivwgv.xml 的 android:description 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Chrome",
      "text_zh": "Chrome（谷歌浏览器品牌名）",
      "source_location": "res/values/strings.xml key=a（application android:label 与无障碍服务 android:label）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：拒绝或返回后的重跳逻辑位于 AES 加密载荷，需运行期监测是否 onResume 死循环拉起无障碍设置",
    "overlay_or_fake_settings": "不可静态还原：Manifest 存在多个 Theme.AppCompat.Transparent.NoActionBar + excludeFromRecents 的透明 Activity（p058l、p057a、p068s、p020o），具备叠放半透明引导遮罩/伪设置页的载体条件，但实际使用方式在加密载荷内",
    "restricted_settings_13plus_coaching": "无（不可静态还原，明文未见相关文案）",
    "post_grant_anti_removal": "不可静态还原：同时声明 DEVICE_ADMIN 接收器 com.earlysince27.p075v（BIND_DEVICE_ADMIN）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，具备防撤权/防卸载能力，具体实现位于加密载荷",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后立即拉起并全程录屏/抓栈，在监测到跳转 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间抓取前一屏；同时在无障碍设置页停留期间持续采样，捕获 800ms 内可能压栈的透明遮罩 Activity",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首屏（载荷注入后的真实入口）",
        "page_identifier": "启动后首个非透明 Activity，包名 com.earlysince27，可能伪装 Chrome 界面",
        "why_most_useful": "确认诱导是冷启动即弹还是功能触发，是判定强制性与否的第一手依据",
        "observable_utg_signals": ["首屏 Activity 类名与包名", "是否出现不可取消按钮的弹窗节点", "是否已存在跳转 ACCESSIBILITY_SETTINGS 的 intent 记录"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置页中 label=Chrome、描述=Enable this service to protect your device 的条目",
        "why_most_useful": "固化伪装身份与假安全承诺文案，是身份不匹配与诱导的直接证据",
        "observable_utg_signals": ["服务标题文本 Chrome", "描述文本 Enable this service to protect your device", "对应包名 com.earlysince27"]
      },
      {
        "page_role": "跳转前引导说明页",
        "page_identifier": "跳转 ACCESSIBILITY_SETTINGS 前紧邻的 Activity/Dialog/WebView",
        "why_most_useful": "区分原生弹窗、本地 HTML、远端 WebView 三种载体，决定后续是否需 OCR 与网络侧取证",
        "observable_utg_signals": ["WebView 节点与 URL", "按钮文本与是否存在取消/跳过", "倒计时或强制点击控件"]
      },
      {
        "page_role": "设置页后压栈的透明遮罩页",
        "page_identifier": "回到应用瞬间出现的 Theme.AppCompat.Transparent.NoActionBar 全屏 Activity",
        "why_most_useful": "识别 COERCE_OVERLAY_STACK_ON_SETTINGS 类叠层指引，这是区分恶性引导与良性说明的关键",
        "observable_utg_signals": ["半透明覆盖层节点", "覆盖层内指向系统开关位置的箭头/高亮", "覆盖层是否拦截返回键"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：引导弹窗、文案、跳转代码与获权后行为全部位于 AES/ECB 加密的二阶段 DEX，纯静态 UTG 文本抽取只能得到系统无障碍列表中的一条描述；须依赖运行期 UTG + 动态 Hook 补齐。若载荷还从远端下发 HTML/配置，需叠加流量侧取证。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "siAq.Vm.attachBaseContext",
    "siAq.Vm.loadDexByVersion",
    "QBMyedEjW.Pnsp.Decrypt",
    "QBMyedEjW.Jybzxm.getAssetsName",
    "res/xml/xwltivwgv.xml",
    "res/values/strings.xml"
  ]
}
```

</details>

# MB_012__d65ae353ce｜TeaBot — VLC MediaPlayer

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：147.0s

## 1. 一句话核心结论

- **核心申请方式**：以 VLC MediaPlayer 名义伪装，声明无任何 description 的全能无障碍服务（读窗口内容+执行手势），真实的无障碍引导与跳设置逻辑藏在异或加密的 assets.czl 中经 DexClassLoader 二阶段加载，主 DEX 完全不留引导痕迹。
- **静态可见性说明**：Manifest、无障碍服务配置、权限、DEX 加载器均静态完整可见；但无障碍服务的实现类 myself.smile.river.andaowidnAIObdnaw 在主 DEX 中不存在，ACTION_ACCESSIBILITY_SETTINGS 跳转、引导弹窗/说明页、拒权循环等运行期 UTG 流程位于 assets/assets.czl（2095 字节，逐字节异或混淆，含 com.android.settings 等明文片段）经 DexClassLoader 反射加载的二阶段载荷内，另有 Lynx 动态 UI 脚本 assets/base.bundle 与 1.2MB 配置 assets/aG.json，均未在本轮解密还原，故引导页原文与跳转时序不可静态确认。
- **命中的行为模式标签**：`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d65ae353ce5d975cea85bb0fab578590a90061173657ba2e1a0c1110d9b8eb91` |
| 包名 / 年份 | `donor.mutual.draft` / 2022 |
| 家族 / 品类 | **TeaBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | VLC MediaPlayer |
| 引导页宣称品牌/身份 | VLC MediaPlayer（VLC 播放器品牌，实际包名 donor.mutual.draft，与 org.videolan.vlc 无关） |
| 系统无障碍列表服务名 | 服务自身未声明 android:label，系统无障碍列表将回退显示应用名「VLC MediaPlayer」；且无 android:description/summary，列表中零用途说明 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务缺失 description/summary 造成列表无用途交代；数十个 Activity 使用 android:label="" 空白标签或随机小写字母串标签（如 bfoewynjkhzpjkxzsajrtmsycmqndrftjydut）挤出真实来源；统一 Theme.NoTitleBar 隐藏标题栏；myself.smile.river.inject.AoNaiwndwadA 设 excludeFromRecents 从最近任务隐藏；全部类名/包名随机化混淆；载荷 assets.czl 逐字节异或加密规避静态扫描 |
| 无障碍服务类名 | `myself.smile.river.andaowidnAIObdnaw` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | myself.smile.river.andwioawdnbawuiDa（唯一 MAIN/LAUNCHER + android.app.role.SMS 角色 Activity） | 用户点击桌面「VLC MediaPlayer」图标，onCreate 启动 | 原生Activity | **原文**：无（主 DEX 中该 Activity 无静态可见文案，界面由二阶段载荷渲染）<br>**译注**：冷启动后展示的应用主界面内容不可静态确认 | 无（本步仅承载启动） | `#1 manifest:components（myself.smile.river.andwioawdnbawuiDa，含 MAIN/LAUNCHER 与 role.SMS intent-filter）` |
| 2 | 业务功能触发 | donor.mutual.draft.JNhWuTnFkLjKaRw#believecancel（反射构造 dalvik.system.DexClassLoader） | declinehat 调用 believecancel，从 assets 解密并加载二阶段 dex | 不可静态还原 | 无 | 无 | `#1.dex1 code:donor.mutual.draft.JNhWuTnFkLjKaRw#believecancel` |
| 3 | 引导说明页 | 载荷内未知 Activity / Dialog / Lynx 页面（assets/base.bundle） | 二阶段 dex 加载完成后由载荷代码触发 | 不可静态还原 | **原文**：无（原文位于 assets/assets.czl 加密数据内，本轮未解密）<br>**译注**：引导用户开启无障碍的说明文案不可静态确认 | 不可静态确认（是否有取消/跳过按钮未知） | `#1 file:assets/assets.czl / #1 file:assets/base.bundle` |
| 4 | 跳无障碍设置 | android.settings.ACCESSIBILITY_SETTINGS 系统页（载荷内拼接 intent，主 DEX 无该字符串） | 载荷内点击回调 | 系统无障碍页 | 无 | 不可静态确认 | `#1 file:res/xml/acsakpoaskopaj.xml（服务配置，无 description）` |
| 5 | 获权后动作 | myself.smile.river.andaowidnAIObdnaw（typeAllMask 全能无障碍服务） | 用户在系统设置中开启服务，onServiceConnected 回调 | 不可静态还原 | 无 | 无 | `#1 file:res/xml/acsakpoaskopaj.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：仅回退显示应用名「VLC MediaPlayer」，服务未配置 android:description/summary，无任何用途说明（res/xml/acsakpoaskopaj.xml）
- 引导说明页/弹窗文案：不在主 DEX 与 res/ 任何资源中，位于加密载荷 assets/assets.czl 解密后动态渲染，静态不可见
- Lynx 动态 UI：assets/base.bundle 含 global.__redefineUIManager 等脚本，可能承载运行期下发的页面布局与文案
- 预筛命中的 assets/POLITICAS.html（西班牙语隐私声明）、assets/CertificateWarning.html（仿浏览器证书警告页）、assets/radio1.html（电台播放器）均为伪装外壳素材，非无障碍引导页
- res/values/strings.xml 仅含 Google Play services 样板文案，未发现任何无障碍引导话术

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | %1$s won't work unless you enable Google Play services. | 除非您启用 Google Play 服务，否则 %1$s 将无法工作。 | `res/values/strings.xml key=common_google_play_services_enable_text` | 未知 |
| en | %1$s won't run without Google Play services, which are missing from your device. | 缺少 Google Play 服务，%1$s 无法运行。 | `res/values/strings.xml key=common_google_play_services_install_text` | 未知 |
| en | %1$s is having trouble with Google Play services. Please try again. | %1$s 与 Google Play 服务通信出现问题，请重试。 | `res/values/strings.xml key=common_google_play_services_unknown_issue` | 未知 |
| es | AppModelo Políticas de Privacidad Nos damos cuenta de que la privacidad de su información personal es importante. | AppModelo 隐私政策：我们认识到您个人信息的隐私很重要。 | `assets/POLITICAS.html` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态确认：主 DEX 无 onResume/定时器拉起 ACCESSIBILITY_SETTINGS 的代码，拒权后重跳逻辑应在 assets.czl 解密载荷内
- **遮罩叠层 / 高仿系统设置页**：不可静态确认；但已声明 SYSTEM_ALERT_WINDOW 权限，且存在 excludeFromRecents + Theme.NoTitleBar 的 inject.AoNaiwndwadA 隐藏 Activity，具备叠层遮罩/伪造页面的能力基础
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（载荷内可能包含，未解密）
- **获权后即时行为与防撤权机制**：不可静态确认：主 DEX 无 performGlobalAction/GLOBAL_ACTION_BACK 等阻止撤权调用
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以包名 donor.mutual.draft 启动后监听顶层 Activity 变化：一旦出现 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 页面立即触发 UTG 抓取；同时在冷启动 3 秒内若出现非 MAIN Activity 的弹窗/无标题栏 Activity（尤其 myself.smile.river.inject.AoNaiwndwadA）即视为引导页候选
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：无障碍引导的文案与跳转逻辑完全不在主 DEX，而在 assets/assets.czl 异或加密载荷中经 DexClassLoader 二阶段加载，纯静态无法还原引导原文与时序；assets/base.bundle（Lynx 脚本）还可能在运行期从远端下发页面，导致引导文案随云控变化。因此本样本必须以运行期 UTG 抓取作为主要判定手段。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后的引导说明页** | 非启动器 Activity 的 Dialog/Activity，标题栏缺失（Theme.NoTitleBar），或 Lynx 渲染页面 | 承载诱导用户开启无障碍的全部话术与按钮设计，是判定是否存在诱导的最直接证据 | 弹窗/页面全部可见文本节点；是否存在取消/跳过按钮文本；是否存在「无障碍/辅助功能/开启」类关键词；页面是否为可点击遮罩或高亮箭头指引 |
| **系统无障碍服务列表项** | Settings → 无障碍 → 已下载/已安装的服务，条目名「VLC MediaPlayer」 | 验证服务在系统 UI 中是否零用途说明，确认用户在被引导时无法判断用途 | 服务条目显示名；条目下方是否为空描述；开关控件状态 |
| **跳设置后的压栈遮罩/悬浮引导窗** | SYSTEM_ALERT_WINDOW 悬浮窗（无标题栏、覆盖系统设置页） | 区分是否为教唆式分步教学（在系统页上叠放箭头/手指指引并催促点击），而非良性说明 | 系统设置页之上是否存在另一窗口层；悬浮窗内文本与箭头位置；是否遮挡返回键区域 |
| **拒权返回后的反馈页** | 从系统设置返回后重新出现的引导弹窗 | 确认是否存在拒权死循环重跳（COERCE 类行为） | 返回后重新弹出的页面与原文；重复弹出间隔；是否有任何退出路径 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `donor.mutual.draft.JNhWuTnFkLjKaRw#believecancel`
- `donor.mutual.draft.JNhWuTnFkLjKaRw#declinehat`
- `myself.smile.river.andwioawdnbawuiDa`
- `myself.smile.river.andaowidnAIObdnaw`
- `res/xml/acsakpoaskopaj.xml`
- `assets/assets.czl`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

- **身份伪装已确认**：`AndroidManifest.xml` 中 `android:label="VLC MediaPlayer"`，但包名为 `donor.mutual.draft`、代码命名空间为 `myself.smile.river`/`donor.*`，与 VLC 官方无任何关联；数十个 Activity 使用空白 `android:label=""` 或随机字母串标签 + `Theme.NoTitleBar`，`myself.smile.river.inject.AoNaiwndwadA` 还设置了 `excludeFromRecents`，用于隐藏弹出层来源。
- **无障碍服务声明为“零说明全能型”**：[res/xml/acsakpoaskopaj.xml](<resource-unit:#1 file:res/xml/acsakpoaskopaj.xml>) 声明 `typeAllMask` + `canRetrieveWindowContent="true"` + `canPerformGestures="true"` + `flagRetrieveInteractiveWindows`，但**完全没有 `android:description`/`summary`**，系统无障碍列表对用户零用途交代。
- **引导流程不在主 DEX**：在 `classes.dex` 中检索 `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`performGlobalAction`、`AccessibilityService` 全部无命中，且 `myself.smile.river` 包下的类在主 DEX 中不存在——服务实现类与引导 UI 均不在可静态读取的 DEX 里。
- **二阶段加密载荷已定位**：`assets/assets.czl`（2095 B）为逐字节异或混淆数据，含 `com.android.settings`、`VWD_CW_GmB[BW` 等明文片段；[donor.mutual.draft.JNhWuTnFkLjKaRw#believecancel](<resource-unit:#1.dex1 code:donor.mutual.draft.JNhWuTnFkLjKaRw#believecancel>) 通过反射构造 `dalvik.system.DexClassLoader` 加载外部 dex，调用方为 `declinehat`。另有 Lynx 动态 UI 脚本 `assets/base.bundle` 与 1.2 MB 配置 `assets/aG.json`。
- **预筛 HTML 与本链路无关**：`POLITICAS.html`（西班牙语隐私声明）、`CertificateWarning.html`（仿浏览器证书警告页）、`radio1.html`（电台播放器）均非无障碍引导页；`strings.xml` 仅含 GMS 样板文案，无引导话术。
- **结论**：用户看到的无障碍引导弹窗/说明页/跳设置/拒权重试全部由解密载荷运行期生成，纯静态不可还原；本次在 12 次工具调用内收敛，`static_visibility` 如实标注为部分动态可见。

已登记风险 **R-001**（high / malware_trojan），证据边界为 `assets.czl` 未解密还原。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest、无障碍服务配置、权限、DEX 加载器均静态完整可见；但无障碍服务的实现类 myself.smile.river.andaowidnAIObdnaw 在主 DEX 中不存在，ACTION_ACCESSIBILITY_SETTINGS 跳转、引导弹窗/说明页、拒权循环等运行期 UTG 流程位于 assets/assets.czl（2095 字节，逐字节异或混淆，含 com.android.settings 等明文片段）经 DexClassLoader 反射加载的二阶段载荷内，另有 Lynx 动态 UI 脚本 assets/base.bundle 与 1.2MB 配置 assets/aG.json，均未在本轮解密还原，故引导页原文与跳转时序不可静态确认。",
  "summary_one_liner": "以 VLC MediaPlayer 名义伪装，声明无任何 description 的全能无障碍服务（读窗口内容+执行手势），真实的无障碍引导与跳设置逻辑藏在异或加密的 assets.czl 中经 DexClassLoader 二阶段加载，主 DEX 完全不留引导痕迹。",
  "disguise_identity": {
    "app_display_name": "VLC MediaPlayer",
    "claimed_brand_or_persona": "VLC MediaPlayer（VLC 播放器品牌，实际包名 donor.mutual.draft，与 org.videolan.vlc 无关）",
    "a11y_service_label": "服务自身未声明 android:label，系统无障碍列表将回退显示应用名「VLC MediaPlayer」；且无 android:description/summary，列表中零用途说明",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务缺失 description/summary 造成列表无用途交代；数十个 Activity 使用 android:label=\"\" 空白标签或随机小写字母串标签（如 bfoewynjkhzpjkxzsajrtmsycmqndrftjydut）挤出真实来源；统一 Theme.NoTitleBar 隐藏标题栏；myself.smile.river.inject.AoNaiwndwadA 设 excludeFromRecents 从最近任务隐藏；全部类名/包名随机化混淆；载荷 assets.czl 逐字节异或加密规避静态扫描"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "myself.smile.river.andwioawdnbawuiDa（唯一 MAIN/LAUNCHER + android.app.role.SMS 角色 Activity）",
      "trigger_event": "用户点击桌面「VLC MediaPlayer」图标，onCreate 启动",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（主 DEX 中该 Activity 无静态可见文案，界面由二阶段载荷渲染）",
      "shown_text_zh": "冷启动后展示的应用主界面内容不可静态确认",
      "user_action_requested": "无（本步仅承载启动）",
      "code_anchor": "#1 manifest:components（myself.smile.river.andwioawdnbawuiDa，含 MAIN/LAUNCHER 与 role.SMS intent-filter）"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "donor.mutual.draft.JNhWuTnFkLjKaRw#believecancel（反射构造 dalvik.system.DexClassLoader）",
      "trigger_event": "declinehat 调用 believecancel，从 assets 解密并加载二阶段 dex",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "解密载荷加载阶段无用户界面",
      "user_action_requested": "无",
      "code_anchor": "#1.dex1 code:donor.mutual.draft.JNhWuTnFkLjKaRw#believecancel"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "载荷内未知 Activity / Dialog / Lynx 页面（assets/base.bundle）",
      "trigger_event": "二阶段 dex 加载完成后由载荷代码触发",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（原文位于 assets/assets.czl 加密数据内，本轮未解密）",
      "shown_text_zh": "引导用户开启无障碍的说明文案不可静态确认",
      "user_action_requested": "不可静态确认（是否有取消/跳过按钮未知）",
      "code_anchor": "#1 file:assets/assets.czl / #1 file:assets/base.bundle"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "android.settings.ACCESSIBILITY_SETTINGS 系统页（载荷内拼接 intent，主 DEX 无该字符串）",
      "trigger_event": "载荷内点击回调",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "跳转后系统无障碍服务列表，服务项显示为「VLC MediaPlayer」且无用途说明",
      "user_action_requested": "不可静态确认",
      "code_anchor": "#1 file:res/xml/acsakpoaskopaj.xml（服务配置，无 description）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "myself.smile.river.andaowidnAIObdnaw（typeAllMask 全能无障碍服务）",
      "trigger_event": "用户在系统设置中开启服务，onServiceConnected 回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后可读取全部窗口内容、上报视图 ID、抓取交互窗口并执行手势，具体动作逻辑在载荷内",
      "user_action_requested": "无",
      "code_anchor": "#1 file:res/xml/acsakpoaskopaj.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：仅回退显示应用名「VLC MediaPlayer」，服务未配置 android:description/summary，无任何用途说明（res/xml/acsakpoaskopaj.xml）",
    "引导说明页/弹窗文案：不在主 DEX 与 res/ 任何资源中，位于加密载荷 assets/assets.czl 解密后动态渲染，静态不可见",
    "Lynx 动态 UI：assets/base.bundle 含 global.__redefineUIManager 等脚本，可能承载运行期下发的页面布局与文案",
    "预筛命中的 assets/POLITICAS.html（西班牙语隐私声明）、assets/CertificateWarning.html（仿浏览器证书警告页）、assets/radio1.html（电台播放器）均为伪装外壳素材，非无障碍引导页",
    "res/values/strings.xml 仅含 Google Play services 样板文案，未发现任何无障碍引导话术"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "除非您启用 Google Play 服务，否则 %1$s 将无法工作。",
      "source_location": "res/values/strings.xml key=common_google_play_services_enable_text",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't run without Google Play services, which are missing from your device.",
      "text_zh": "缺少 Google Play 服务，%1$s 无法运行。",
      "source_location": "res/values/strings.xml key=common_google_play_services_install_text",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s is having trouble with Google Play services. Please try again.",
      "text_zh": "%1$s 与 Google Play 服务通信出现问题，请重试。",
      "source_location": "res/values/strings.xml key=common_google_play_services_unknown_issue",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "es",
      "text_verbatim": "AppModelo Políticas de Privacidad Nos damos cuenta de que la privacidad de su información personal es importante.",
      "text_zh": "AppModelo 隐私政策：我们认识到您个人信息的隐私很重要。",
      "source_location": "assets/POLITICAS.html",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态确认：主 DEX 无 onResume/定时器拉起 ACCESSIBILITY_SETTINGS 的代码，拒权后重跳逻辑应在 assets.czl 解密载荷内",
    "overlay_or_fake_settings": "不可静态确认；但已声明 SYSTEM_ALERT_WINDOW 权限，且存在 excludeFromRecents + Theme.NoTitleBar 的 inject.AoNaiwndwadA 隐藏 Activity，具备叠层遮罩/伪造页面的能力基础",
    "restricted_settings_13plus_coaching": "无静态证据（载荷内可能包含，未解密）",
    "post_grant_anti_removal": "不可静态确认：主 DEX 无 performGlobalAction/GLOBAL_ACTION_BACK 等阻止撤权调用",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以包名 donor.mutual.draft 启动后监听顶层 Activity 变化：一旦出现 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 页面立即触发 UTG 抓取；同时在冷启动 3 秒内若出现非 MAIN Activity 的弹窗/无标题栏 Activity（尤其 myself.smile.river.inject.AoNaiwndwadA）即视为引导页候选",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后的引导说明页",
        "page_identifier": "非启动器 Activity 的 Dialog/Activity，标题栏缺失（Theme.NoTitleBar），或 Lynx 渲染页面",
        "why_most_useful": "承载诱导用户开启无障碍的全部话术与按钮设计，是判定是否存在诱导的最直接证据",
        "observable_utg_signals": ["弹窗/页面全部可见文本节点", "是否存在取消/跳过按钮文本", "是否存在「无障碍/辅助功能/开启」类关键词", "页面是否为可点击遮罩或高亮箭头指引"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → 无障碍 → 已下载/已安装的服务，条目名「VLC MediaPlayer」",
        "why_most_useful": "验证服务在系统 UI 中是否零用途说明，确认用户在被引导时无法判断用途",
        "observable_utg_signals": ["服务条目显示名", "条目下方是否为空描述", "开关控件状态"]
      },
      {
        "page_role": "跳设置后的压栈遮罩/悬浮引导窗",
        "page_identifier": "SYSTEM_ALERT_WINDOW 悬浮窗（无标题栏、覆盖系统设置页）",
        "why_most_useful": "区分是否为教唆式分步教学（在系统页上叠放箭头/手指指引并催促点击），而非良性说明",
        "observable_utg_signals": ["系统设置页之上是否存在另一窗口层", "悬浮窗内文本与箭头位置", "是否遮挡返回键区域"]
      },
      {
        "page_role": "拒权返回后的反馈页",
        "page_identifier": "从系统设置返回后重新出现的引导弹窗",
        "why_most_useful": "确认是否存在拒权死循环重跳（COERCE 类行为）",
        "observable_utg_signals": ["返回后重新弹出的页面与原文", "重复弹出间隔", "是否有任何退出路径"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：无障碍引导的文案与跳转逻辑完全不在主 DEX，而在 assets/assets.czl 异或加密载荷中经 DexClassLoader 二阶段加载，纯静态无法还原引导原文与时序；assets/base.bundle（Lynx 脚本）还可能在运行期从远端下发页面，导致引导文案随云控变化。因此本样本必须以运行期 UTG 抓取作为主要判定手段。"
  },
  "behavior_pattern_tags": [
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "CARRIER_OVERLAY_MASK_OR_GUIDE"
  ],
  "code_anchors": [
    "donor.mutual.draft.JNhWuTnFkLjKaRw#believecancel",
    "donor.mutual.draft.JNhWuTnFkLjKaRw#declinehat",
    "myself.smile.river.andwioawdnbawuiDa",
    "myself.smile.river.andaowidnAIObdnaw",
    "res/xml/acsakpoaskopaj.xml",
    "assets/assets.czl"
  ]
}
```

</details>

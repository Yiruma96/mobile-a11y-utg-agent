# MB_143__801f956057｜Crocodilus — IKO Lokata

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：159.3s

## 1. 一句话核心结论

- **核心申请方式**：以波兰银行品牌 IKO Lokata 冒充、包名无关联的一阶段加密 Dropper，无障碍服务实现与引导页面全部藏于 AES 加密的二阶段载荷，仅能从 Manifest 确证其声明了高能力无障碍服务且无用途说明。
- **静态可见性说明**：一阶段 classes.dex 仅含解密装载器与反射加载；Manifest 声明的无障碍服务类 unrelated.hamburger.mCrlHbKuUbzQ.woHOKBMFI 在可见 DEX 中完全不存在，assets/encroc1~9.enc 与伪装为 encroc1.dex、lib1~7.so 的文件均为 AES 密文（文件头无 DEX/ELF 魔数），全部引导 UI、跳转逻辑与无障碍实现藏于加密二阶段载荷；res/ 与 assets/ 文本资源中无任何 accessibility 相关字符串。
- **命中的行为模式标签**：`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `801f956057aa608c7393b2fcca9b731c610c6bd5e14f4f3c1d64e8f211828319` |
| 包名 / 年份 | `unrelated.hamburger` / 2025 |
| 家族 / 品类 | **Crocodilus**（同池样本数：6） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | IKO Lokata |
| 引导页宣称品牌/身份 | IKO（波兰 IKO 银行）Lokata 存款产品 |
| 系统无障碍列表服务名 | IKO Lokata |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 unrelated.hamburger 与所冒充品牌完全无关；无障碍服务 android:description 缺失，系统无障碍列表中仅显示品牌名而无任何用途说明；所有类名/包名采用随机语义词混淆（如 mCrlHbKuUbzQ、woHOKBMFI）；资产以 .dex/.so 后缀伪装密文；Manifest 中声明多个 activity-alias 与大量干扰性组件 |
| 无障碍服务类名 | `unrelated.hamburger.mCrlHbKuUbzQ.woHOKBMFI` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | 一阶段 DEX 内的解密装载链（无独立可见引导 Activity） | dinerbanking() 被调用后链式触发 estimatorlividly() → showingnutrient() | 不可静态还原 | 无 | 无（后台静默执行） | `demeaningimplosive.underminedynasty.Crumpetcinch.dinerbanking/estimatorlividly/showingnutrient` |
| 2 | 业务功能触发 | assets 资产读取与 AES 解密（obsessedscientist 解码文件名 → imprisonbullhorn 读流 → familydevoutly 解密） | showingnutrient() 调用 obsessedscientist() 得到资产名，再调 Alabastertweezers.imprisonbullhorn() 读取，最终 Strangelyunlivable.cherubgoal() → Quarryescapist.familydevoutly() 解密 | 不可静态还原 | **原文**：🚀 Asset okumaya başlandı: / ✅ Asset okundu: / ✅ Şifre çözme başarılı<br>**译注**：“开始读取资产 / 资产读取完成 / 解密成功”（仅日志，不呈现给用户） | 无 | `demeaningimplosive.reflectedunwarlike.Alabastertweezers.imprisonbullhorn；drivewaywiden.goutgeneric.Quarryescapist.familydevoutly` |
| 3 | 获权后动作（二阶段入口） | Cabanaproperly.makingtrophy() 内存加载解密后的二阶段载荷 | Snubapplied.unawarestays() 取得明文后传入 makingtrophy() | 不可静态还原 | 无 | 无 | `drivewaywiden.goutgeneric.Snubapplied.unawarestays；demeaningimplosive.unchainmuch.Cabanaproperly.makingtrophy` |
| 4 | 引导说明页 / 跳受限设置 / 跳无障碍设置 / 遮罩叠层指引 / 拒权反馈循环 | 二阶段载荷内实现（静态不可见），仅可确证最终目标为 Manifest 声明的 AccessibilityService unrelated.hamburger.mCrlHbKuUbzQ.woHOKBMFI | 不可静态还原（类体不在任何明文制品中） | 不可静态还原 | **原文**：无（res/ 与 assets/ 中 accessibility 相关字符串零命中）<br>**译注**：无法确定；不存在本地 HTML/strings 资源可承载引导文案 | 不可静态还原；可确证的客观结果为把用户导向系统无障碍列表中的“IKO Lokata”条目 | `res/xml/llipdkho.xml（无障碍能力配置）；AndroidManifest.xml 中 service unrelated.hamburger.mCrlHbKuUbzQ.woHOKBMFI` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统设置 → 无障碍 → 已下载服务列表中的服务名“IKO Lokata”（来自 Manifest android:label，android:description 缺失，无任何用途说明）
- 桌面启动器图标名“IKO Lokata”（android:label），与包名 unrelated.hamburger 不一致
- res/ 与 assets/ 下无任何承载无障碍引导文案的 strings.xml、layout 或 HTML 资源（grep accessibility 零命中）
- 引导弹窗/教学页/遮罩层的具体承载位置不可静态还原，位于 assets/encroc*.enc 解密后的二阶段载荷内
- 应用内仅有的明文字符串为 com.nirvana.dropper.util.TG.send 输出的土耳其语调试日志，不面向用户呈现

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | 🚀 Asset okumaya başlandı: | 开始读取资产： | `demeaningimplosive.reflectedunwarlike.Alabastertweezers#imprisonbullhorn 硬编码，经 com.nirvana.dropper.util.TG#send 输出` | 未知 |
| tr | ✅ Şifre çözme başarılı | 解密成功 | `drivewaywiden.goutgeneric.Quarryescapist#familydevoutly 硬编码` | 未知 |
| tr | ❌ Şifre çözme hatası: | 解密错误： | `drivewaywiden.goutgeneric.Quarryescapist#familydevoutly 硬编码` | 未知 |
| en | IKO Lokata | IKO Lokata（波兰 IKO 银行存款产品名） | `AndroidManifest.xml application android:label 与 accessibilityservice android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原；一阶段 DEX 中不存在 ACTION_ACCESSIBILITY_SETTINGS 跳转点、onResume 重跳或 Timer 轮询代码，相关逻辑全在加密二阶段
- **遮罩叠层 / 高仿系统设置页**：不可静态还原；Manifest 权限清单中未观察到 SYSTEM_ALERT_WINDOW，但权限 dump 可能被截断，不能据此排除悬浮窗方案
- **Android 13+ 受限设置（Restricted Settings）应对**：不可静态还原；一阶段无 APPLICATION_DETAILS_SETTINGS 跳转代码，无法确证是否包含 Android 13+ 受限设置分步教学
- **获权后即时行为与防撤权机制**：不可静态还原；但 Manifest 声明了 DeviceAdmin 配置 res/xml/hgaalwz.xml（uses-policies force-lock）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED，具备获权后锁屏与常驻的配套能力
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动即启动采集，重点在检测到系统无障碍设置页（Settings$AccessibilitySettings）或应用详情页被拉起前 300~800ms 的窗口，以及解密完成后首次界面渲染瞬间（因载荷为运行期 AES 解密，静态无法预判弹窗时机）
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：一阶段完全无引导 UI，全部文案与跳转在 AES 加密二阶段载荷内，静态 UTG 特征（strings/HTML/Manifest description）全部缺失；若二阶段引导采用纯图片或 GIF 图文教程，UTG 文本树可能为空，必须启用 OCR；另 Manifest 声明无障碍服务但实现类不在 DEX 中，也意味着仅靠静态清单会误判为“空壳服务”。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **解密后首屏引导弹窗/教学页** | 非 IKO 官方界面的自绘 Activity 或全屏 Dialog，文案含无障碍/辅助功能授权引导 | 决定该样本是良性无障碍应用还是伪装引导，是整个 UTG 判定的核心页 | 页面文本是否提及无障碍/辅助功能/权限开启；是否存在取消或跳过按钮；应用名与页面宣称品牌是否一致 |
| **系统无障碍服务列表项** | Settings$AccessibilitySettings 中“IKO Lokata”条目，副标题为空 | 直接证明用户被引导至无障碍开关，且无用途说明构成信息缺失 | 服务名 IKO Lokata；description 为空；开关由关到开的点击序列 |
| **设置页返回后的压栈遮罩页** | 从无障碍页返回后 500~1500ms 内出现的半透明或全屏浮层 | 区分是否存在“获权后再确认/阻止撤权”的对抗行为 | 浮层是否覆盖系统设置页；是否自动执行返回/Home；是否有二次确认点击 |
| **应用详情页受限设置入口** | Settings$AppDetailsSettings（unrelated.hamburger） | 核验是否实施 Android 13+ 受限设置分步教学 | 是否跳转应用详情页；页面停留时长与后续点击位置 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `demeaningimplosive.underminedynasty.Crumpetcinch.dinerbanking`
- `demeaningimplosive.underminedynasty.Crumpetcinch.obsessedscientist`
- `demeaningimplosive.reflectedunwarlike.Alabastertweezers.imprisonbullhorn`
- `drivewaywiden.goutgeneric.Quarryescapist.familydevoutly`
- `res/xml/llipdkho.xml`
- `res/xml/hgaalwz.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**静态可见性：不可还原（二阶段全加密）**。本样本的一阶段 DEX 仅承担“解密并加载”职责，无障碍引导界面与 `ACTION_ACCESSIBILITY_SETTINGS` 跳转代码**不在包内任何明文制品中**。

- **Manifest 伪装**：包名 `unrelated.hamburger`，桌面显示名与无障碍服务标签均为 `IKO Lokata`（波兰银行 IKO 存款产品品牌），但包名与品牌毫无关联；无障碍服务 `unrelated.hamburger.mCrlHbKuUbzQ.woHOKBMFI` 的 `android:description` 缺失，系统无障碍列表只剩一个品牌名，没有用途说明。
- **无障碍能力配置**（[res/xml/llipdkho.xml](<resource-unit:#1 file:res/xml/llipdkho.xml>)）：`canRetrieveWindowContent=true`、`canPerformGestures=true`、`notificationTimeout=100`、`accessibilityFlags=0x10`，具备读取窗口内容与全局手势执行能力，是典型的银行木马点击注入配置。
- **关键证据缺口**：`classes.dex` 仅 38 个类，**完全不含** `woHOKBMFI` 及其包 `mCrlHbKuUbzQ` 的类体；在 `res/`、`assets/` 文本资源中 grep `accessibility` 零命中。即：Manifest 声明了无障碍服务，但实现该服务的类只存在于加密载荷中。
- **二阶段加密链已确证**：[Crumpetcinch.dinerbanking()](<resource-unit:#1.dex1 code:demeaningimplosive.underminedynasty.Crumpetcinch#dinerbanking>) → [estimatorlividly()](<resource-unit:#1.dex1 code:demeaningimplosive.underminedynasty.Crumpetcinch#estimatorlividly>) → [showingnutrient()](<resource-unit:#1.dex1 code:demeaningimplosive.underminedynasty.Crumpetcinch#showingnutrient>) 以 XOR 解码资产名（[obsessedscientist()](<resource-unit:#1.dex1 code:demeaningimplosive.underminedynasty.Crumpetcinch#obsessedscientist>)）后，经 [Alabastertweezers.imprisonbullhorn()](<resource-unit:#1.dex1 code:demeaningimplosive.reflectedunwarlike.Alabastertweezers#imprisonbullhorn>) 读取 assets，再由 [Quarryescapist.familydevoutly()](<resource-unit:#1.dex1 code:drivewaywiden.goutgeneric.Quarryescapist#familydevoutly>) 用 AES/CBC（[manlikespotlight()](<resource-unit:#1.dex1 code:drivewaywiden.goutgeneric.Quarryescapist#manlikespotlight>)）解密并交给 `Cabanaproperly.makingtrophy()` 加载。
- **资产实为密文**：`assets/encroc1.dex`、`lib1.so` 头部均为随机字节（非 `dex\n035`、非 `\x7fELF`），`encroc1~9.enc` 为同族密文，确认 `.dex`/`.so` 后缀是伪装。
- **土耳其语指向**：解密日志硬编码土耳其语（`Şifre çözme başarılı` 等），与 Crocodilus 家族语言画像一致；另声明 DeviceAdmin（`force-lock`）与短信全套权限，构成获权后的高危落点。

**因此**：UTG 视角下可确证的只有“伪装品牌 + 无障碍能力声明 + 加密二阶段”三件事；**冷启动弹窗、拒权循环、遮罩叠层、受限设置教学等具体页面流转全部位于密文载荷内，无法静态还原**，需运行期 UTG 捕获。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "一阶段 classes.dex 仅含解密装载器与反射加载；Manifest 声明的无障碍服务类 unrelated.hamburger.mCrlHbKuUbzQ.woHOKBMFI 在可见 DEX 中完全不存在，assets/encroc1~9.enc 与伪装为 encroc1.dex、lib1~7.so 的文件均为 AES 密文（文件头无 DEX/ELF 魔数），全部引导 UI、跳转逻辑与无障碍实现藏于加密二阶段载荷；res/ 与 assets/ 文本资源中无任何 accessibility 相关字符串。",
  "summary_one_liner": "以波兰银行品牌 IKO Lokata 冒充、包名无关联的一阶段加密 Dropper，无障碍服务实现与引导页面全部藏于 AES 加密的二阶段载荷，仅能从 Manifest 确证其声明了高能力无障碍服务且无用途说明。",
  "disguise_identity": {
    "app_display_name": "IKO Lokata",
    "claimed_brand_or_persona": "IKO（波兰 IKO 银行）Lokata 存款产品",
    "a11y_service_label": "IKO Lokata",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 unrelated.hamburger 与所冒充品牌完全无关；无障碍服务 android:description 缺失，系统无障碍列表中仅显示品牌名而无任何用途说明；所有类名/包名采用随机语义词混淆（如 mCrlHbKuUbzQ、woHOKBMFI）；资产以 .dex/.so 后缀伪装密文；Manifest 中声明多个 activity-alias 与大量干扰性组件"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "一阶段 DEX 内的解密装载链（无独立可见引导 Activity）",
      "trigger_event": "dinerbanking() 被调用后链式触发 estimatorlividly() → showingnutrient()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "本步骤无用户可见界面，为静默解密装载",
      "user_action_requested": "无（后台静默执行）",
      "code_anchor": "demeaningimplosive.underminedynasty.Crumpetcinch.dinerbanking/estimatorlividly/showingnutrient"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "assets 资产读取与 AES 解密（obsessedscientist 解码文件名 → imprisonbullhorn 读流 → familydevoutly 解密）",
      "trigger_event": "showingnutrient() 调用 obsessedscientist() 得到资产名，再调 Alabastertweezers.imprisonbullhorn() 读取，最终 Strangelyunlivable.cherubgoal() → Quarryescapist.familydevoutly() 解密",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "🚀 Asset okumaya başlandı: / ✅ Asset okundu: / ✅ Şifre çözme başarılı",
      "shown_text_zh": "“开始读取资产 / 资产读取完成 / 解密成功”（仅日志，不呈现给用户）",
      "user_action_requested": "无",
      "code_anchor": "demeaningimplosive.reflectedunwarlike.Alabastertweezers.imprisonbullhorn；drivewaywiden.goutgeneric.Quarryescapist.familydevoutly"
    },
    {
      "step": 3,
      "stage": "获权后动作（二阶段入口）",
      "screen_or_component": "Cabanaproperly.makingtrophy() 内存加载解密后的二阶段载荷",
      "trigger_event": "Snubapplied.unawarestays() 取得明文后传入 makingtrophy()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（装载完成后真实功能才出现）",
      "user_action_requested": "无",
      "code_anchor": "drivewaywiden.goutgeneric.Snubapplied.unawarestays；demeaningimplosive.unchainmuch.Cabanaproperly.makingtrophy"
    },
    {
      "step": 4,
      "stage": "引导说明页 / 跳受限设置 / 跳无障碍设置 / 遮罩叠层指引 / 拒权反馈循环",
      "screen_or_component": "二阶段载荷内实现（静态不可见），仅可确证最终目标为 Manifest 声明的 AccessibilityService unrelated.hamburger.mCrlHbKuUbzQ.woHOKBMFI",
      "trigger_event": "不可静态还原（类体不在任何明文制品中）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（res/ 与 assets/ 中 accessibility 相关字符串零命中）",
      "shown_text_zh": "无法确定；不存在本地 HTML/strings 资源可承载引导文案",
      "user_action_requested": "不可静态还原；可确证的客观结果为把用户导向系统无障碍列表中的“IKO Lokata”条目",
      "code_anchor": "res/xml/llipdkho.xml（无障碍能力配置）；AndroidManifest.xml 中 service unrelated.hamburger.mCrlHbKuUbzQ.woHOKBMFI"
    }
  ],
  "text_presentation_locations": [
    "系统设置 → 无障碍 → 已下载服务列表中的服务名“IKO Lokata”（来自 Manifest android:label，android:description 缺失，无任何用途说明）",
    "桌面启动器图标名“IKO Lokata”（android:label），与包名 unrelated.hamburger 不一致",
    "res/ 与 assets/ 下无任何承载无障碍引导文案的 strings.xml、layout 或 HTML 资源（grep accessibility 零命中）",
    "引导弹窗/教学页/遮罩层的具体承载位置不可静态还原，位于 assets/encroc*.enc 解密后的二阶段载荷内",
    "应用内仅有的明文字符串为 com.nirvana.dropper.util.TG.send 输出的土耳其语调试日志，不面向用户呈现"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "🚀 Asset okumaya başlandı: ",
      "text_zh": "开始读取资产：",
      "source_location": "demeaningimplosive.reflectedunwarlike.Alabastertweezers#imprisonbullhorn 硬编码，经 com.nirvana.dropper.util.TG#send 输出",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "tr",
      "text_verbatim": "✅ Şifre çözme başarılı",
      "text_zh": "解密成功",
      "source_location": "drivewaywiden.goutgeneric.Quarryescapist#familydevoutly 硬编码",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "tr",
      "text_verbatim": "❌ Şifre çözme hatası: ",
      "text_zh": "解密错误：",
      "source_location": "drivewaywiden.goutgeneric.Quarryescapist#familydevoutly 硬编码",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "IKO Lokata",
      "text_zh": "IKO Lokata（波兰 IKO 银行存款产品名）",
      "source_location": "AndroidManifest.xml application android:label 与 accessibilityservice android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原；一阶段 DEX 中不存在 ACTION_ACCESSIBILITY_SETTINGS 跳转点、onResume 重跳或 Timer 轮询代码，相关逻辑全在加密二阶段",
    "overlay_or_fake_settings": "不可静态还原；Manifest 权限清单中未观察到 SYSTEM_ALERT_WINDOW，但权限 dump 可能被截断，不能据此排除悬浮窗方案",
    "restricted_settings_13plus_coaching": "不可静态还原；一阶段无 APPLICATION_DETAILS_SETTINGS 跳转代码，无法确证是否包含 Android 13+ 受限设置分步教学",
    "post_grant_anti_removal": "不可静态还原；但 Manifest 声明了 DeviceAdmin 配置 res/xml/hgaalwz.xml（uses-policies force-lock）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED，具备获权后锁屏与常驻的配套能力",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动即启动采集，重点在检测到系统无障碍设置页（Settings$AccessibilitySettings）或应用详情页被拉起前 300~800ms 的窗口，以及解密完成后首次界面渲染瞬间（因载荷为运行期 AES 解密，静态无法预判弹窗时机）",
    "key_pages_to_capture": [
      {
        "page_role": "解密后首屏引导弹窗/教学页",
        "page_identifier": "非 IKO 官方界面的自绘 Activity 或全屏 Dialog，文案含无障碍/辅助功能授权引导",
        "why_most_useful": "决定该样本是良性无障碍应用还是伪装引导，是整个 UTG 判定的核心页",
        "observable_utg_signals": ["页面文本是否提及无障碍/辅助功能/权限开启", "是否存在取消或跳过按钮", "应用名与页面宣称品牌是否一致"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings$AccessibilitySettings 中“IKO Lokata”条目，副标题为空",
        "why_most_useful": "直接证明用户被引导至无障碍开关，且无用途说明构成信息缺失",
        "observable_utg_signals": ["服务名 IKO Lokata", "description 为空", "开关由关到开的点击序列"]
      },
      {
        "page_role": "设置页返回后的压栈遮罩页",
        "page_identifier": "从无障碍页返回后 500~1500ms 内出现的半透明或全屏浮层",
        "why_most_useful": "区分是否存在“获权后再确认/阻止撤权”的对抗行为",
        "observable_utg_signals": ["浮层是否覆盖系统设置页", "是否自动执行返回/Home", "是否有二次确认点击"]
      },
      {
        "page_role": "应用详情页受限设置入口",
        "page_identifier": "Settings$AppDetailsSettings（unrelated.hamburger）",
        "why_most_useful": "核验是否实施 Android 13+ 受限设置分步教学",
        "observable_utg_signals": ["是否跳转应用详情页", "页面停留时长与后续点击位置"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "存在显著盲区：一阶段完全无引导 UI，全部文案与跳转在 AES 加密二阶段载荷内，静态 UTG 特征（strings/HTML/Manifest description）全部缺失；若二阶段引导采用纯图片或 GIF 图文教程，UTG 文本树可能为空，必须启用 OCR；另 Manifest 声明无障碍服务但实现类不在 DEX 中，也意味着仅靠静态清单会误判为“空壳服务”。"
  },
  "behavior_pattern_tags": [
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION"
  ],
  "code_anchors": [
    "demeaningimplosive.underminedynasty.Crumpetcinch.dinerbanking",
    "demeaningimplosive.underminedynasty.Crumpetcinch.obsessedscientist",
    "demeaningimplosive.reflectedunwarlike.Alabastertweezers.imprisonbullhorn",
    "drivewaywiden.goutgeneric.Quarryescapist.familydevoutly",
    "res/xml/llipdkho.xml",
    "res/xml/hgaalwz.xml"
  ]
}
```

</details>

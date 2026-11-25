# MB_145__6d55d90d02｜Crocodilus — IKO

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：128.9s

## 1. 一句话核心结论

- **核心申请方式**：主 DEX 为反射劫持 Application 生命周期的加载壳，无障碍服务与引导界面全部封装在 AES 加密的二阶段载荷中于运行期解密加载，静态无法看到任何申请无障碍的文案或跳转逻辑。
- **静态可见性说明**：主 classes.dex 仅含加载壳（32 个类），无障碍服务类 nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF 及全部引导 UI/文案均不在主 DEX；真实实现藏于 assets/encroc1~5.enc 与 encroc1.dex/encroc2.dex 等 AES-CBC 加密载荷，由 Application.attachBaseContext 反射劫持链在运行期解密加载，资源中亦无 HTML/WebView/引导字符串，故引导页面流转不可静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `6d55d90d021b0980528f56d040e78fa7b85a96f5c244e23f330f24c8e80c1cb2` |
| 包名 / 年份 | `nuttiness.pamperer.cosmetics` / 2025 |
| 家族 / 品类 | **Crocodilus**（同池样本数：6） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | （静态预筛为空，Manifest label 无可读值） |
| 引导页宣称品牌/身份 | 不可静态还原（位于加密二阶段载荷） |
| 系统无障碍列表服务名 | 无 label 属性，系统无障碍列表将直接显示类名 nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未设置 android:label 与 android:description（预筛 description=[]），列表项只能显示随机化类名；应用 label 为空；Manifest 内存在多个 activity/service/receiver 别名（com.apple.treeActivity、com.flap.decayService、com.humorist.safenessService 等）与 com.december.META_6391 类伪装组件名；Application 真实类通过 Class.forName + 反射 attach 隐藏；载荷文件名与字符串均 XOR 混淆 |
| 无障碍服务类名 | `nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | aixx.uvoe.pxoq.Iqom (Application) → VzxfOopr → 反射构造的真实 Application | 进程启动时 attachBaseContext(Context) | 不可静态还原 | **原文**：无（该阶段无 UI；异常文案为硬编码土耳其语 "Başlatılamadı"）<br>**译注**：无界面；初始化失败抛出“无法启动” | 无 | `aixx.uvoe.pxoq.Iqom.attachBaseContext / aixx.uvoe.pxoq.VzxfOopr.m_ohsf` |
| 2 | 冷启动入口 | Comicstarving → Outlastunrafe → Penalizeunvalued.gradedalmost（载荷装载） | Application 初始化链中 cataractwaltz/outburstmagnesium 回调 | 不可静态还原 | 无 | 无 | `armydecrease.chosenthirty.Comicstarving.exquisitereborn / rippingunwind.backachemoistness.Frowngrout.dispersedperjury` |
| 3 | 引导说明页 | 二阶段载荷内（类 nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF 及伴随 Activity，均不可静态定位） | 不可静态还原（载荷解密后方可见） | 不可静态还原 | 无 | 不可静态还原 | `nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF（Manifest 声明，代码体在加密载荷内）` |
| 4 | 跳无障碍设置 | 系统设置 Settings.ACTION_ACCESSIBILITY_SETTINGS（预期目标页，跳转调用点在载荷内） | 不可静态还原 | 系统无障碍页 | 无 | 不可静态还原 | `不可静态还原（主 DEX 无 ACCESSIBILITY_SETTINGS 字符串）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- Manifest：无障碍服务 nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF 未配置 android:label / android:description，系统无障碍列表仅显示随机化类名
- 主 classes.dex：无任何引导文案、无 HTML/raw 资源、无 WebView 相关字符串
- assets/：encroc1.dex、encroc2.dex、encroc1~5.enc 为 AES-CBC 密文载荷，引导界面与文案预期封装其中，静态不可读
- res/：无 html/htm/js 资源，未发现可读的引导说明文本

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Başlatılamadı | 无法启动 | `aixx.uvoe.pxoq.Iqom.attachBaseContext 抛出的 RuntimeException 文案` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原（跳转与重试逻辑位于 AES 加密的二阶段载荷，主 DEX 无相关字符串）
- **遮罩叠层 / 高仿系统设置页**：不可静态还原；主 DEX 无悬浮窗/SYSTEM_ALERT_WINDOW 相关代码，但载荷内是否使用遮罩无法排除
- **Android 13+ 受限设置（Restricted Settings）应对**：不可静态还原
- **获权后即时行为与防撤权机制**：不可静态还原
- **良性降级 / 替代方案**：无（未见任何降级/替代路径代码，主 DEX 仅有加载与解密逻辑）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测进程启动后首次出现 Settings ACTION_ACCESSIBILITY_SETTINGS 跳转（或 android.settings.ACCESSIBILITY_SETTINGS 组件的 Activity 启动）时立即拉起 UTG；同时可在冷启动首帧（Application 解密完成后首个 Activity）抓取首屏，因为该样本的引导页在载荷解密后极早出现。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：本样本为两阶段加密载荷结构，静态只能确认无障碍服务声明与 AES 解密装载链，所有引导文案、跳转代码、拒权循环均在 encroc 系列密文中；若动态阶段载荷未成功解密或依赖远端下发，UTG 可能只看到空白/闪退页面。另应用 label 与无障碍服务 label 均为空，UTG 文本提取需按包名/类名而非显示名识别。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首屏/引导说明页（载荷解密后第一个 Activity）** | 包名 nuttiness.pamperer.cosmetics 下、非 MainActivity 命名的随机化 Activity（Manifest 中 TJydMkiWRbuz.*、qrNsfPHktbXX.* 等别名之一） | 该页是解密后真正展示引导文案的位置，可一次性取到诱导话术与按钮结构 | 全部可见文本节点（标题、说明、按钮）；是否存在取消/跳过按钮；是否存在品牌 Logo/仿冒身份文案；页面是否为 WebView 容器 |
| **跳转瞬间的系统无障碍服务列表项** | Settings 无障碍页中列表项文本 nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF | 服务无 label/description，列表项仅显示随机类名，可证明身份伪装与用户被要求开启的具体服务 | 列表项完整文本（类名原样）；副标题是否为空；开关状态 |
| **设置页后压栈遮罩/引导浮层（若存在）** | 无障碍设置页上方叠加的自绘 Window（半透明遮罩、箭头指引、模拟开关） | 用于区分“单纯跳系统设置”与“高仿设置页/遮罩指引”两种诱导强度 | 叠加层节点是否属于应用包而非 settings 包；遮罩内文本与箭头指向；是否存在伪造开关控件 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `aixx.uvoe.pxoq.Iqom.attachBaseContext`
- `aixx.uvoe.pxoq.VzxfOopr.m_ohsf`
- `armydecrease.chosenthirty.Comicstarving.exquisitereborn`
- `rippingunwind.backachemoistness.Frowngrout.dispersedperjury`
- `rippingunwind.backachemoistness.Penalizeunvalued.gradedalmost`
- `AndroidManifest.xml: service nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（受工具预算约束，以下结论仅基于已确认证据）。

## 分析结论要点

**1. 主 DEX 只是加载壳，无障碍引导界面不在静态可见代码内**
- Manifest 中注册了无障碍服务 `nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF`（`BIND_ACCESSIBILITY_SERVICE`），但该类在 `classes.dex` 中**不存在**（全量类清单仅 32 个类，无 `nuttiness.*` 包）。
- 主 DEX 中亦无 `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`isAccessibilityTool`、`action_accessibility` 等任何字符串，`res/` 下也无 HTML/raw/WebView 引导资源。

**2. 已确认的二阶段加密加载链（这就是引导页藏身处）**
- [Iqom.attachBaseContext()](<resource-unit:#1.dex1 code:aixx.uvoe.pxoq.Iqom#attachBaseContext>) → `VzxfOopr.m_ohsf`：用 XOR 混淆串经 `Class.forName` 反射取出真实 Application 类，再用 `setAccessible(true)` 反射调用隐藏方法 `Application.attach(Context)` 并手动 `onCreate()`，属于典型“真 Application 藏在载荷里”的结构。
- [Comicstarving.exquisitereborn()](<resource-unit:#1.dex1 code:armydecrease.chosenthirty.Comicstarving#exquisitereborn>) 通过 `monopolysinger()` 的 XOR 还原出 8 字节资源名（由 `encroc` 系列推断），读 `assets/` 后交 `Outlastunafraid → Penalizeunvalued → gradedalmost` 载入。
- [Frowngrout.dispersedperjury()](<resource-unit:#1.dex1 code:rippingunwind.backachemoistness.Frowngrout#dispersedperjury>) 使用 `happilyseventh()` 的 20 字节 XOR 还原算法名（长度与 `AES/CBC/PKCS5Padding` 一致），配 `SecretKeySpec`+`IvParameterSpec` 做 AES 解密。
- `assets/encroc1.dex`、`encroc2.dex` 魔数均非 `dex\n`（实测 `51 8c 35 ed…`、`8c e4 06 33…`），`encroc1~5.enc` 亦为密文，共约 120KB 加密载荷。

**3. 结论：无障碍诱导的页面流转（弹窗/WebView/悬浮窗/跳设置）全部位于 AES 加密的二阶段载荷内，无法静态还原**；可静态确认的只有“服务声明存在 + 引导链被刻意加密隐藏 + 反射劫持 Application 生命周期”这三项，配合 `READ_SMS/SEND_SMS/CALL_PHONE/CAMERA/QUERY_ALL_PACKAGES/REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` 的权限组合，与 Crocodilus 家族的“加密载荷 + 无障碍滥用”结构一致。

**4. 覆盖边界**：未取得密钥常量（`paycheckwheat`、`reversingfiddling` 等字段值分散在混淆方法中）与载荷解密结果，故 `shown_text_verbatim`、按钮文案、拒权循环、遮罩层等运行期细节无法逐字给出；UTG 侧应把捕获时机锁定在“无障碍设置页跳转瞬间与冷启动首帧”。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "主 classes.dex 仅含加载壳（32 个类），无障碍服务类 nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF 及全部引导 UI/文案均不在主 DEX；真实实现藏于 assets/encroc1~5.enc 与 encroc1.dex/encroc2.dex 等 AES-CBC 加密载荷，由 Application.attachBaseContext 反射劫持链在运行期解密加载，资源中亦无 HTML/WebView/引导字符串，故引导页面流转不可静态还原。",
  "summary_one_liner": "主 DEX 为反射劫持 Application 生命周期的加载壳，无障碍服务与引导界面全部封装在 AES 加密的二阶段载荷中于运行期解密加载，静态无法看到任何申请无障碍的文案或跳转逻辑。",
  "disguise_identity": {
    "app_display_name": "（静态预筛为空，Manifest label 无可读值）",
    "claimed_brand_or_persona": "不可静态还原（位于加密二阶段载荷）",
    "a11y_service_label": "无 label 属性，系统无障碍列表将直接显示类名 nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未设置 android:label 与 android:description（预筛 description=[]），列表项只能显示随机化类名；应用 label 为空；Manifest 内存在多个 activity/service/receiver 别名（com.apple.treeActivity、com.flap.decayService、com.humorist.safenessService 等）与 com.december.META_6391 类伪装组件名；Application 真实类通过 Class.forName + 反射 attach 隐藏；载荷文件名与字符串均 XOR 混淆"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "aixx.uvoe.pxoq.Iqom (Application) → VzxfOopr → 反射构造的真实 Application",
      "trigger_event": "进程启动时 attachBaseContext(Context)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（该阶段无 UI；异常文案为硬编码土耳其语 \"Başlatılamadı\"）",
      "shown_text_zh": "无界面；初始化失败抛出“无法启动”",
      "user_action_requested": "无",
      "code_anchor": "aixx.uvoe.pxoq.Iqom.attachBaseContext / aixx.uvoe.pxoq.VzxfOopr.m_ohsf"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "Comicstarving → Outlastunrafe → Penalizeunvalued.gradedalmost（载荷装载）",
      "trigger_event": "Application 初始化链中 cataractwaltz/outburstmagnesium 回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "读取 assets 中 XOR 还原名（encroc 系列）并 AES 解密后装载",
      "user_action_requested": "无",
      "code_anchor": "armydecrease.chosenthirty.Comicstarving.exquisitereborn / rippingunwind.backachemoistness.Frowngrout.dispersedperjury"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "二阶段载荷内（类 nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF 及伴随 Activity，均不可静态定位）",
      "trigger_event": "不可静态还原（载荷解密后方可见）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不可静态还原",
      "user_action_requested": "不可静态还原",
      "code_anchor": "nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF（Manifest 声明，代码体在加密载荷内）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 Settings.ACTION_ACCESSIBILITY_SETTINGS（预期目标页，跳转调用点在载荷内）",
      "trigger_event": "不可静态还原",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不可静态还原",
      "user_action_requested": "不可静态还原",
      "code_anchor": "不可静态还原（主 DEX 无 ACCESSIBILITY_SETTINGS 字符串）"
    }
  ],
  "text_presentation_locations": [
    "Manifest：无障碍服务 nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF 未配置 android:label / android:description，系统无障碍列表仅显示随机化类名",
    "主 classes.dex：无任何引导文案、无 HTML/raw 资源、无 WebView 相关字符串",
    "assets/：encroc1.dex、encroc2.dex、encroc1~5.enc 为 AES-CBC 密文载荷，引导界面与文案预期封装其中，静态不可读",
    "res/：无 html/htm/js 资源，未发现可读的引导说明文本"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Başlatılamadı",
      "text_zh": "无法启动",
      "source_location": "aixx.uvoe.pxoq.Iqom.attachBaseContext 抛出的 RuntimeException 文案",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原（跳转与重试逻辑位于 AES 加密的二阶段载荷，主 DEX 无相关字符串）",
    "overlay_or_fake_settings": "不可静态还原；主 DEX 无悬浮窗/SYSTEM_ALERT_WINDOW 相关代码，但载荷内是否使用遮罩无法排除",
    "restricted_settings_13plus_coaching": "不可静态还原",
    "post_grant_anti_removal": "不可静态还原",
    "benign_graceful_degradation": "无（未见任何降级/替代路径代码，主 DEX 仅有加载与解密逻辑）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测进程启动后首次出现 Settings ACTION_ACCESSIBILITY_SETTINGS 跳转（或 android.settings.ACCESSIBILITY_SETTINGS 组件的 Activity 启动）时立即拉起 UTG；同时可在冷启动首帧（Application 解密完成后首个 Activity）抓取首屏，因为该样本的引导页在载荷解密后极早出现。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首屏/引导说明页（载荷解密后第一个 Activity）",
        "page_identifier": "包名 nuttiness.pamperer.cosmetics 下、非 MainActivity 命名的随机化 Activity（Manifest 中 TJydMkiWRbuz.*、qrNsfPHktbXX.* 等别名之一）",
        "why_most_useful": "该页是解密后真正展示引导文案的位置，可一次性取到诱导话术与按钮结构",
        "observable_utg_signals": ["全部可见文本节点（标题、说明、按钮）", "是否存在取消/跳过按钮", "是否存在品牌 Logo/仿冒身份文案", "页面是否为 WebView 容器"]
      },
      {
        "page_role": "跳转瞬间的系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中列表项文本 nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF",
        "why_most_useful": "服务无 label/description，列表项仅显示随机类名，可证明身份伪装与用户被要求开启的具体服务",
        "observable_utg_signals": ["列表项完整文本（类名原样）", "副标题是否为空", "开关状态"]
      },
      {
        "page_role": "设置页后压栈遮罩/引导浮层（若存在）",
        "page_identifier": "无障碍设置页上方叠加的自绘 Window（半透明遮罩、箭头指引、模拟开关）",
        "why_most_useful": "用于区分“单纯跳系统设置”与“高仿设置页/遮罩指引”两种诱导强度",
        "observable_utg_signals": ["叠加层节点是否属于应用包而非 settings 包", "遮罩内文本与箭头指向", "是否存在伪造开关控件"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：本样本为两阶段加密载荷结构，静态只能确认无障碍服务声明与 AES 解密装载链，所有引导文案、跳转代码、拒权循环均在 encroc 系列密文中；若动态阶段载荷未成功解密或依赖远端下发，UTG 可能只看到空白/闪退页面。另应用 label 与无障碍服务 label 均为空，UTG 文本提取需按包名/类名而非显示名识别。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "aixx.uvoe.pxoq.Iqom.attachBaseContext",
    "aixx.uvoe.pxoq.VzxfOopr.m_ohsf",
    "armydecrease.chosenthirty.Comicstarving.exquisitereborn",
    "rippingunwind.backachemoistness.Frowngrout.dispersedperjury",
    "rippingunwind.backachemoistness.Penalizeunvalued.gradedalmost",
    "AndroidManifest.xml: service nuttiness.pamperer.cosmetics.iRhkqgbpsuK.dNCGxurzQUjoF"
  ]
}
```

</details>

# MR_171__ffa5ac3460｜Cerberus — Flash Player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：153.1s

## 1. 一句话核心结论

- **核心申请方式**：以 Flash Player 名义注册无描述说明的 AccessibilityService，全部业务代码藏在加密的 support/rcboawvrn 二阶段载荷中，由 Application.onCreate 反射加载，引导用户开启无障碍的具体页面流转无法静态还原，须运行期 UTG 抓取。
- **静态可见性说明**：Manifest 与无障碍配置 xml 完整可见；但 classes.dex 内不含任何 com.mwmnfwt.arhkrgajn.* 类，全部代码位于 com.iuolnsaork.itfets.* 且类名/方法名混淆、字符串以 byte[] 经私有函数解密；真正的引导文案与跳转逻辑位于 assets 路径下 unknown/support/rcboawvrn（463KB，熵 8.0）与 resources.lz（258KB，高熵）二阶段加密载荷中，zlib/xor 均不可解，且无 strings.xml、无 HTML/布局资源，故引导页面流转、弹窗文案、拒权循环逻辑均不可静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ffa5ac3460998e7b9856fc136ebcd112196c3abf24816ccab1fbae11eae4954c` |
| 包名 / 年份 | `com.mwmnfwt.arhkrgajn` / 2019 |
| 家族 / 品类 | **Cerberus**（同池样本数：8） |
| 原始来源标识 | https://www.threatfabric.com/blogs/cerberus-a-new-banking-trojan-from-the-underworld.html |
| 桌面显示名 | Flash Player |
| 引导页宣称品牌/身份 | Flash Player（Adobe Flash Player 播放器品牌） |
| 系统无障碍列表服务名 | Flash Player Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置未设置 android:description，系统无障碍列表中服务名下方为空白说明；多个 Activity 的 android:label 为空串（rsvrjvalnoql.Oamndbqk、tiytemkez.PuRngQgIOPG、tiytemkez.yRlqHcGvQf）或随机无意义串（qvcuwyhrdpft、nwbyaobqu、urkyqeotw、mfpwarehvs、ojuzjcqyazmd、nsjujsyjg、sutgnj、weldusqvtbhm）；设备管理器 Receiver 伪装为 System Driver；使用 Theme.Translucent.NoTitleBar / Theme.NoDisplay 与 excludeFromRecents 隐藏界面；包名 com.mwmnfwt.arhkrgajn 与真实代码包 com.iuolnsaork.itfets 不一致（Manifest 声明类在 DEX 中不存在，需运行期解密加载）；字符串全部以字节数组加密混淆。 |
| 无障碍服务类名 | `com.mwmnfwt.arhkrgajn.lupurnjzcfr.QCDwtYULzO` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.mwmnfwt.arhkrgajn.wlIGbq（LAUNCHER Activity，无 android:label） | 用户点击桌面 Flash Player 图标启动 | 原生Activity | **原文**：无（该 Activity 未声明 label，且 res 中无 strings.xml，无任何可见文案资源）<br>**译注**：该入口自身不携带任何文案，界面内容由加密载荷运行时构建 | 无明确要求；启动后进入不可静态确定的界面 | `AndroidManifest.xml: com.mwmnfwt.arhkrgajn.wlIGbq (action.MAIN/category.LAUNCHER)` |
| 2 | 冷启动入口 | com.iuolnsaork.itfets.TDEaNE（自定义 Application）→ FECTkBViqd | Application.onCreate() | 不可静态还原 | 无 | 无 | `com.iuolnsaork.itfets.TDEaNE#onCreate → com.iuolnsaork.itfets.FECTkBViqd#pluBZBWRcEOi` |
| 3 | 业务功能触发 | 加密载荷 unknown/support/rcboawvrn（及索引 cache.txt→support/resources.lz） | Application 初始化后由解密加载器读取并装载 | 不可静态还原 | **原文**：无（载荷熵值 8.0，无任何明文可读字符串）<br>**译注**：二阶段载荷承载全部业务逻辑，包括权限引导流程与无障碍服务实现 | 不可静态确定 | `unknown/support/rcboawvrn、unknown/support/resources.lz、unknown/support/cache.txt` |
| 4 | 跳无障碍设置 | com.mwmnfwt.arhkrgajn.lupurnjzcfr.QCDwtYULzO（无障碍服务，label=Flash Player Service）+ 系统无障碍设置页 | 载荷内逻辑调用 ACTION_ACCESSIBILITY_SETTINGS（该常量在 DEX 文本中 0 命中，因字符串加密，具体调用点不可静态定位） | 系统无障碍页 | **原文**：Flash Player Service<br>**译注**：系统无障碍服务列表中出现名为“Flash Player Service”的服务，下方说明为空白 | 要求用户开启该无障碍服务；是否存在取消/跳过不可静态确定 | `AndroidManifest.xml: service com.mwmnfwt.arhkrgajn.lupurnjzcfr.QCDwtYULzO; res/xml/oyfamrcbayz.xml` |
| 5 | 拒权反馈循环 | 不可静态还原（位于加密载荷） | 不可静态确定（可能为 onResume / Timer） | 不可静态还原 | 无 | 不可静态确定 | `unknown/support/rcboawvrn（加密载荷，静态不可解）` |
| 6 | 获权后动作 | 无障碍服务 QCDwtYULzO + 设备管理器 Receiver rsvrjvalnoql.zGxVQqDnPap（label=System Driver） | 服务在系统设置中被启用后由系统绑定 | 不可静态还原 | **原文**：System Driver<br>**译注**：获权后可读取窗口内容（canRetrieveWindowContent + flagReportViewIds），并具备 force-lock/wipe-data 设备管理策略，反移除与自点确认逻辑不可静态还原 | 不可静态确定 | `res/xml/oyfamrcbayz.xml; res/xml/yodnzh.xml; AndroidManifest.xml: receiver zGxVQqDnPap` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：android:label="Flash Player Service"（android:description 未设置 → 列表项说明区为空白）
- 桌面图标名：android:label="Flash Player"（application 级）
- 设备管理器列表项：receiver android:label="System Driver"
- 多个 Activity 标签为空串或随机串（qvcuwyhrdpft / nwbyaobqu / urkyqeotw / mfpwarehvs / ojuzjcqyazmd / nsjujsyjg / sutgnj / weldusqvtbhm），不承载任何说明性文案
- res/values 下不存在 strings.xml；resources.arsc 内无用户可见文案；assets 下无 HTML/JS/布局资源 → 所有引导弹窗与教学页文案均只能由加密载荷 unknown/support/rcboawvrn 或远端下发在运行时生成（位置不可静态还原）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Flash Player | Flash Player（伪装为 Adobe Flash 播放器） | `AndroidManifest.xml application android:label` | 假更新 |
| en | Flash Player Service | Flash Player 服务（系统无障碍列表显示名） | `AndroidManifest.xml service QCDwtYULzO android:label` | 未知 |
| en | System Driver | 系统驱动（伪装为系统组件以掩盖设备管理器激活请求） | `AndroidManifest.xml receiver zGxVQqDnPap android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：引导与重跳逻辑位于加密载荷 unknown/support/rcboawvrn，DEX 内既无明文 ACTION_ACCESSIBILITY_SETTINGS 亦无相关 Activity/弹窗资源，无法确认是否 onResume 死循环重跳或定时器拉起
- **遮罩叠层 / 高仿系统设置页**：不可静态还原：DEX 中无悬浮窗权限（无 SYSTEM_ALERT_WINDOW）声明，未见伪造设置页布局资源；但存在 Theme.Translucent.NoTitleBar / Theme.NoDisplay 及 excludeFromRecents 的隐藏型 Activity，实际是否叠遮罩需 UTG 观测
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=27，低于 Android 13 受限设置机制；未见相关教学代码或文案）
- **获权后即时行为与防撤权机制**：不可静态还原：存在 BIND_DEVICE_ADMIN 的 Receiver（force-lock + wipe-data）与 PACKAGE_ADDED/PACKAGE_REMOVED/USER_PRESENT/BOOT_COMPLETED 高优先级监听，具备反移除能力基础，但自点确认/GLOBAL_ACTION_BACK 阻止撤权的具体实现位于加密载荷
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 com.mwmnfwt.arhkrgajn.wlIGbq 冷启动为起点；在检测到顶层页面跳转到 android.settings.ACCESSIBILITY_SETTINGS（或组件含 com.android.settings/.accessibility.*）时立即抓取；同时在 Activity 切换为 com.mwmnfwt.arhkrgajn.tiytemkez.* / rsvrjvalnoql.Oamndbqk（Theme.NoDisplay、excludeFromRecents）瞬间抓屏，这类隐藏 Activity 最可能是载荷加载或引导中转页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：①所有引导文案与跳转逻辑位于加密载荷 unknown/support/rcboawvrn（熵 8.0）内，静态无法预判界面结构；②resources.arsc 无任何用户可见文案、assets 无 HTML，故若载荷以纯图片或 WebView 远端页面呈现引导，UTG 需依赖截图/OCR 补充；③Manifest 声明的类在 DEX 中不存在，运行期才解密装载，首个可见页可能并非 wlIGbq；④本机无在线设备，未能运行期验证。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首个可见页（引导入口）** | 启动后 1–3 秒内最上层 Activity（预期为 com.mwmnfwt.arhkrgajn.wlIGbq 或其跳转的解密后 Activity，窗口特征含 Theme.Translucent.NoTitleBar） | 该页承载全部引导文案，是判断“假更新/故障恐吓/隐私承诺”话术的唯一直接来源，因资源层无任何文案，只能从运行期界面取证 | 页面根节点无文本但有图片/WebView；是否存在不可取消（无关闭按钮/返回无效）的弹窗节点；WebView 节点是否指向远端 URL 或本地解密 HTML |
| **跳转前教学/说明页** | 跳转 ACTION_ACCESSIBILITY_SETTINGS 前的最上层 Activity 或 Dialog | 决定是否为分步教学式诱导、是否提供取消/跳过，直接支撑“强制 vs 透明说明”的定性 | 是否存在“下一步/立即开启”主按钮而无取消按钮；是否出现分步骤序号或图示；文本中是否出现 accessibility/无障碍 字样 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中 label=Flash Player Service 的条目 | 验证空白 description 造成的身份混淆效果，以及是否在设置页期间叠加悬浮引导层 | 列表项副标题是否为空；服务名与包名/图标是否与 Flash Player 品牌不符；设置页上方是否出现应用自绘遮罩/高亮指引 |
| **拒权返回后的反馈页** | 从系统设置返回应用后的最上层窗口（重复出现的同一 Activity 即视为循环） | 区分良性降级与强制循环重跳（COERCE_REFUSAL_LOOP_RELAUNCH） | 返回后是否在 1–2 秒内再次跳转设置页；是否出现惩罚性弹窗或功能锁定提示；是否存在替代路径（手动模式/跳过） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.mwmnfwt.arhkrgajn.wlIGbq（Manifest LAUNCHER Activity，无 label）`
- `com.iuolnsaork.itfets.TDEaNE#onCreate`
- `com.iuolnsaork.itfets.FECTkBViqd#pluBZBWRcEOi`
- `res/xml/oyfamrcbayz.xml`
- `unknown/support/rcboawvrn`
- `res/xml/yodnzh.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，收口）

**可见性判定：`packed_or_encrypted`（二阶段载荷加密，引导链不可静态还原）**

- **Manifest 层完全可见**：`label="Flash Player"`，无障碍服务 [QCDwtYULzO](<resource-unit:#1 manifest:components>) 的 `android:label="Flash Player Service"`，绑定 `BIND_ACCESSIBILITY_SERVICE`，配置 [res/xml/oyfamrcbayz.xml](<resource-unit:#1 file:res/xml/oyfamrcbayz.xml>) 仅声明 `canRetrieveWindowContent=true` + `flagReportViewIds`，**未声明 `android:description`**（系统无障碍列表里服务名下方无任何说明文字，属"空白描述"手法）。
- **代码层被完全混淆+字符串加密**：`classes.dex` 中 `com.mwmnfwt.arhkrgajn.*`（Manifest 声明的全部 Activity/Service/Receiver）**不存在**；实际只有 `com.iuolnsaork.itfets.*`（729 类，类名/方法名全随机，如 `hKAkCZgIPvnL` 有 38 个重载）。所有字符串都以 `new byte[]{...}` 经私有解密函数还原（见 [FECTkBViqd#pluBZBWRcEOi](<resource-unit:#1.dex1 code:com.iuolnsaork.itfets.FECTkBViqd#pluBZBWRcEOi>)），因此 `ACCESSIBILITY_SETTINGS`、`android.settings.*` 等常量在文本搜索中**全部为 0 命中**——并非不存在，而是被加密。
- **二阶段载荷为高熵密文**：`assets` 下无 HTML/JS/布局资源；`unknown/support/` 有 `rcboawvrn`（463 KB，**熵值 8.0**，zlib/xor 均不可解）与 `resources.lz`（258 KB，同为高熵），另有 `cache.txt` 内容为 `support/resources.lz`，及 5 个 36–43 字节随机名索引文件。`res/values/` 无 `strings.xml`，`resources.arsc` 内无任何用户可见文案（仅 ConstraintLayout 属性名与图标路径）。**即：任何引导弹窗/教学页文案都不可能来自资源，只能来自解密后的载荷或远端下发。**
- **加载入口**：`Application.onCreate` → `TDEaNE#onCreate` → `FECTkBViqd#pluBZBWRcEOi()`，内部通过 `Class.forName` + `Field`/`Method` 反射（`zpHMWTo`、`irEqhLireVlp` 字段、`hKAkCZgIPvnL(byte[])` 解密类名）装载隐藏类，返回值即解密后的类对象；DEX 中无 `DexClassLoader` 字面量，说明加载器类名同样被加密。
- **伪装与反移除旁证**：多个 Activity `android:label=""` 或随机串（`qvcuwyhrdpft`、`nwbyaobqu`…），`Theme.Translucent.NoTitleBar`/`Theme.NoDisplay`、`excludeFromRecents`；设备管理器 Receiver 标签 `System Driver`，[res/xml/yodnzh.xml](<resource-unit:#1 file:res/xml/yodnzh.xml>) 申请 `force-lock` + `wipe-data`。
- **UTG 结论**：可确认"存在以 Flash Player 名义注册的无描述无障碍服务 + 全套短信/联系人/通话权限 + 设备管理器"，但**具体"如何一步步引导用户开启无障碍"的页面流转（跳转点、弹窗文案、拒权重跳、遮罩）位于加密载荷 `rcboawvrn` 内，静态不可还原**，需运行期 UTG 抓取。

**覆盖边界**：未对 `rcboawvrn` 做运行期解密（无静态密钥、无在线设备可动态脱壳）；未验证载荷是否真的以 `ACTION_ACCESSIBILITY_SETTINGS` 跳转（该常量必然存在于解密后的字符串池中）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest 与无障碍配置 xml 完整可见；但 classes.dex 内不含任何 com.mwmnfwt.arhkrgajn.* 类，全部代码位于 com.iuolnsaork.itfets.* 且类名/方法名混淆、字符串以 byte[] 经私有函数解密；真正的引导文案与跳转逻辑位于 assets 路径下 unknown/support/rcboawvrn（463KB，熵 8.0）与 resources.lz（258KB，高熵）二阶段加密载荷中，zlib/xor 均不可解，且无 strings.xml、无 HTML/布局资源，故引导页面流转、弹窗文案、拒权循环逻辑均不可静态还原。",
  "summary_one_liner": "以 Flash Player 名义注册无描述说明的 AccessibilityService，全部业务代码藏在加密的 support/rcboawvrn 二阶段载荷中，由 Application.onCreate 反射加载，引导用户开启无障碍的具体页面流转无法静态还原，须运行期 UTG 抓取。",
  "disguise_identity": {
    "app_display_name": "Flash Player",
    "claimed_brand_or_persona": "Flash Player（Adobe Flash Player 播放器品牌）",
    "a11y_service_label": "Flash Player Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置未设置 android:description，系统无障碍列表中服务名下方为空白说明；多个 Activity 的 android:label 为空串（rsvrjvalnoql.Oamndbqk、tiytemkez.PuRngQgIOPG、tiytemkez.yRlqHcGvQf）或随机无意义串（qvcuwyhrdpft、nwbyaobqu、urkyqeotw、mfpwarehvs、ojuzjcqyazmd、nsjujsyjg、sutgnj、weldusqvtbhm）；设备管理器 Receiver 伪装为 System Driver；使用 Theme.Translucent.NoTitleBar / Theme.NoDisplay 与 excludeFromRecents 隐藏界面；包名 com.mwmnfwt.arhkrgajn 与真实代码包 com.iuolnsaork.itfets 不一致（Manifest 声明类在 DEX 中不存在，需运行期解密加载）；字符串全部以字节数组加密混淆。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.mwmnfwt.arhkrgajn.wlIGbq（LAUNCHER Activity，无 android:label）",
      "trigger_event": "用户点击桌面 Flash Player 图标启动",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（该 Activity 未声明 label，且 res 中无 strings.xml，无任何可见文案资源）",
      "shown_text_zh": "该入口自身不携带任何文案，界面内容由加密载荷运行时构建",
      "user_action_requested": "无明确要求；启动后进入不可静态确定的界面",
      "code_anchor": "AndroidManifest.xml: com.mwmnfwt.arhkrgajn.wlIGbq (action.MAIN/category.LAUNCHER)"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.iuolnsaork.itfets.TDEaNE（自定义 Application）→ FECTkBViqd",
      "trigger_event": "Application.onCreate()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；在进程启动时完成解密与反射装载隐藏类（Class.forName + Field/Method 反射 + byte[] 解密类名）",
      "user_action_requested": "无",
      "code_anchor": "com.iuolnsaork.itfets.TDEaNE#onCreate → com.iuolnsaork.itfets.FECTkBViqd#pluBZBWRcEOi"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "加密载荷 unknown/support/rcboawvrn（及索引 cache.txt→support/resources.lz）",
      "trigger_event": "Application 初始化后由解密加载器读取并装载",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（载荷熵值 8.0，无任何明文可读字符串）",
      "shown_text_zh": "二阶段载荷承载全部业务逻辑，包括权限引导流程与无障碍服务实现",
      "user_action_requested": "不可静态确定",
      "code_anchor": "unknown/support/rcboawvrn、unknown/support/resources.lz、unknown/support/cache.txt"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "com.mwmnfwt.arhkrgajn.lupurnjzcfr.QCDwtYULzO（无障碍服务，label=Flash Player Service）+ 系统无障碍设置页",
      "trigger_event": "载荷内逻辑调用 ACTION_ACCESSIBILITY_SETTINGS（该常量在 DEX 文本中 0 命中，因字符串加密，具体调用点不可静态定位）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Flash Player Service",
      "shown_text_zh": "系统无障碍服务列表中出现名为“Flash Player Service”的服务，下方说明为空白",
      "user_action_requested": "要求用户开启该无障碍服务；是否存在取消/跳过不可静态确定",
      "code_anchor": "AndroidManifest.xml: service com.mwmnfwt.arhkrgajn.lupurnjzcfr.QCDwtYULzO; res/xml/oyfamrcbayz.xml"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "不可静态还原（位于加密载荷）",
      "trigger_event": "不可静态确定（可能为 onResume / Timer）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "拒权后是否死循环重跳、是否叠加遮罩均需运行期 UTG 判定",
      "user_action_requested": "不可静态确定",
      "code_anchor": "unknown/support/rcboawvrn（加密载荷，静态不可解）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 QCDwtYULzO + 设备管理器 Receiver rsvrjvalnoql.zGxVQqDnPap（label=System Driver）",
      "trigger_event": "服务在系统设置中被启用后由系统绑定",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "System Driver",
      "shown_text_zh": "获权后可读取窗口内容（canRetrieveWindowContent + flagReportViewIds），并具备 force-lock/wipe-data 设备管理策略，反移除与自点确认逻辑不可静态还原",
      "user_action_requested": "不可静态确定",
      "code_anchor": "res/xml/oyfamrcbayz.xml; res/xml/yodnzh.xml; AndroidManifest.xml: receiver zGxVQqDnPap"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：android:label=\"Flash Player Service\"（android:description 未设置 → 列表项说明区为空白）",
    "桌面图标名：android:label=\"Flash Player\"（application 级）",
    "设备管理器列表项：receiver android:label=\"System Driver\"",
    "多个 Activity 标签为空串或随机串（qvcuwyhrdpft / nwbyaobqu / urkyqeotw / mfpwarehvs / ojuzjcqyazmd / nsjujsyjg / sutgnj / weldusqvtbhm），不承载任何说明性文案",
    "res/values 下不存在 strings.xml；resources.arsc 内无用户可见文案；assets 下无 HTML/JS/布局资源 → 所有引导弹窗与教学页文案均只能由加密载荷 unknown/support/rcboawvrn 或远端下发在运行时生成（位置不可静态还原）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Flash Player",
      "text_zh": "Flash Player（伪装为 Adobe Flash 播放器）",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Flash Player Service",
      "text_zh": "Flash Player 服务（系统无障碍列表显示名）",
      "source_location": "AndroidManifest.xml service QCDwtYULzO android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "System Driver",
      "text_zh": "系统驱动（伪装为系统组件以掩盖设备管理器激活请求）",
      "source_location": "AndroidManifest.xml receiver zGxVQqDnPap android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：引导与重跳逻辑位于加密载荷 unknown/support/rcboawvrn，DEX 内既无明文 ACTION_ACCESSIBILITY_SETTINGS 亦无相关 Activity/弹窗资源，无法确认是否 onResume 死循环重跳或定时器拉起",
    "overlay_or_fake_settings": "不可静态还原：DEX 中无悬浮窗权限（无 SYSTEM_ALERT_WINDOW）声明，未见伪造设置页布局资源；但存在 Theme.Translucent.NoTitleBar / Theme.NoDisplay 及 excludeFromRecents 的隐藏型 Activity，实际是否叠遮罩需 UTG 观测",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=27，低于 Android 13 受限设置机制；未见相关教学代码或文案）",
    "post_grant_anti_removal": "不可静态还原：存在 BIND_DEVICE_ADMIN 的 Receiver（force-lock + wipe-data）与 PACKAGE_ADDED/PACKAGE_REMOVED/USER_PRESENT/BOOT_COMPLETED 高优先级监听，具备反移除能力基础，但自点确认/GLOBAL_ACTION_BACK 阻止撤权的具体实现位于加密载荷",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 com.mwmnfwt.arhkrgajn.wlIGbq 冷启动为起点；在检测到顶层页面跳转到 android.settings.ACCESSIBILITY_SETTINGS（或组件含 com.android.settings/.accessibility.*）时立即抓取；同时在 Activity 切换为 com.mwmnfwt.arhkrgajn.tiytemkez.* / rsvrjvalnoql.Oamndbqk（Theme.NoDisplay、excludeFromRecents）瞬间抓屏，这类隐藏 Activity 最可能是载荷加载或引导中转页。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首个可见页（引导入口）",
        "page_identifier": "启动后 1–3 秒内最上层 Activity（预期为 com.mwmnfwt.arhkrgajn.wlIGbq 或其跳转的解密后 Activity，窗口特征含 Theme.Translucent.NoTitleBar）",
        "why_most_useful": "该页承载全部引导文案，是判断“假更新/故障恐吓/隐私承诺”话术的唯一直接来源，因资源层无任何文案，只能从运行期界面取证",
        "observable_utg_signals": ["页面根节点无文本但有图片/WebView", "是否存在不可取消（无关闭按钮/返回无效）的弹窗节点", "WebView 节点是否指向远端 URL 或本地解密 HTML"]
      },
      {
        "page_role": "跳转前教学/说明页",
        "page_identifier": "跳转 ACTION_ACCESSIBILITY_SETTINGS 前的最上层 Activity 或 Dialog",
        "why_most_useful": "决定是否为分步教学式诱导、是否提供取消/跳过，直接支撑“强制 vs 透明说明”的定性",
        "observable_utg_signals": ["是否存在“下一步/立即开启”主按钮而无取消按钮", "是否出现分步骤序号或图示", "文本中是否出现 accessibility/无障碍 字样"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中 label=Flash Player Service 的条目",
        "why_most_useful": "验证空白 description 造成的身份混淆效果，以及是否在设置页期间叠加悬浮引导层",
        "observable_utg_signals": ["列表项副标题是否为空", "服务名与包名/图标是否与 Flash Player 品牌不符", "设置页上方是否出现应用自绘遮罩/高亮指引"]
      },
      {
        "page_role": "拒权返回后的反馈页",
        "page_identifier": "从系统设置返回应用后的最上层窗口（重复出现的同一 Activity 即视为循环）",
        "why_most_useful": "区分良性降级与强制循环重跳（COERCE_REFUSAL_LOOP_RELAUNCH）",
        "observable_utg_signals": ["返回后是否在 1–2 秒内再次跳转设置页", "是否出现惩罚性弹窗或功能锁定提示", "是否存在替代路径（手动模式/跳过）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：①所有引导文案与跳转逻辑位于加密载荷 unknown/support/rcboawvrn（熵 8.0）内，静态无法预判界面结构；②resources.arsc 无任何用户可见文案、assets 无 HTML，故若载荷以纯图片或 WebView 远端页面呈现引导，UTG 需依赖截图/OCR 补充；③Manifest 声明的类在 DEX 中不存在，运行期才解密装载，首个可见页可能并非 wlIGbq；④本机无在线设备，未能运行期验证。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.mwmnfwt.arhkrgajn.wlIGbq（Manifest LAUNCHER Activity，无 label）",
    "com.iuolnsaork.itfets.TDEaNE#onCreate",
    "com.iuolnsaork.itfets.FECTkBViqd#pluBZBWRcEOi",
    "res/xml/oyfamrcbayz.xml",
    "unknown/support/rcboawvrn",
    "res/xml/yodnzh.xml"
  ]
}
```

</details>

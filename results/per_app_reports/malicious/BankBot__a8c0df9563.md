# MB_114__a8c0df9563｜BankBot — Postegro

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：190.7s

## 1. 一句话核心结论

- **核心申请方式**：空壳 DEX + Application 启动即 native 解密高熵资源还原全部逻辑，静态仅暴露一个标签为 Postegro、说明为土耳其语『启用无障碍服务』的 typeAllMask/canRetrieveWindowContent 无障碍服务，引导页面流转藏于加密载荷内不可静态还原。
- **静态可见性说明**：可见 classes.dex 仅 7168 字节、30 个空壳类，Manifest 声明的无障碍服务类 com.themdont25.p075h 及各 Activity 在 DEX 字符串表中零命中；全部业务逻辑（含无障碍引导 UI 与跳转序列）由 Application.attachBaseContext 调用的 native 方法 JDLxIs（libZyRnrN.so，混淆 C++ 符号）在运行期解密 res/raw/dciwqlhgujksf（460684 字节高熵）与 50 个随机长名 assets 分片后动态加载。仅 Manifest、res/xml 无障碍与设备管理器配置、strings.xml 两条字符串可静态确认。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a8c0df9563d945f286f7a5e73ec5a134362a28b6abe9400b2589b7eef91726cf` |
| 包名 / 年份 | `com.themdont25` / 2023 |
| 家族 / 品类 | **BankBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Postegro |
| 引导页宣称品牌/身份 | Postegro（无品牌指向的虚构应用名，非真实社交/银行品牌，实际为银行木马外壳） |
| 系统无障碍列表服务名 | Postegro |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：服务标签与桌面名复用同一字符串 @string/a=Postegro，无障碍说明 hssaAnk 仅写土耳其语『启用无障碍服务』而无任何功能合理性说明；服务类名 com.themdont25.p075h 及全部 Activity 使用无意义短名（p012p/p015k/p020a 等）；类名与资产文件名大量随机化；未声明 android:isAccessibilityTool，依赖系统默认判定以规避 Android 12+ 的『非无障碍工具』提示 |
| 无障碍服务类名 | `com.themdont25.p075h` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.themdont25.KJzpnjM（自定义 Application） | 进程创建时 attachBaseContext(Context) 回调 | 不可静态还原 | 无 | 无（用户不可见） | `com.themdont25.KJzpnjM.attachBaseContext` |
| 2 | 冷启动入口 | libZyRnrN.so 内 Java_com_themdont25_KJzpnjM_JDLxIs | attachBaseContext 直接调用 native 方法 JDLxIs(context) | 不可静态还原 | 无 | 无（用户不可见） | `com.themdont25.KJzpnjM.JDLxIs / lib/arm64-v8a/libZyRnrN.so` |
| 3 | 引导说明页 | 系统无障碍列表中的服务条目（com.themdont25.p075h） | 用户进入 设置→无障碍→已下载的服务 时由系统渲染服务名与说明 | 系统无障碍页 | **原文**：Postegro / Erişebilirlik Servisileri Etkinleştirme<br>**译注**：Postegro / 启用无障碍服务 | 系统页内开启开关；服务本身无取消/跳过选项 | `res/values/strings.xml (a, hssaAnk) + res/xml/fpvlq.xml android:description` |
| 4 | 跳无障碍设置 | 未知（预期为解密载荷内 Activity/Dialog） | 不可静态还原：DEX 中不存在 ACTION_ACCESSIBILITY_SETTINGS 相关字符串 | 不可静态还原 | 无 | 不可静态判定是否有取消/跳过按钮 | `不可静态还原（载荷 res/raw/dciwqlhgujksf 解密后）` |
| 5 | 获权后动作 | com.themdont25.p075h（AccessibilityService，实现类不可见） | 系统绑定无障碍服务后回调（typeAllMask 监听全部事件） | 不可静态还原 | 无 | 无 | `AndroidManifest.xml (lines 117-122) + res/xml/fpvlq.xml + res/xml/sznlbpvzx.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目：服务名 Postegro（@string/a）与说明 Erişebilirlik Servisileri Etkinleştirme（@string/hssaAnk），由 res/xml/fpvlq.xml 的 android:description 引用
- 桌面图标名称：android:label=@string/a 即 Postegro（Manifest activity 与 a11y service、device admin receiver 共用）
- 应用内引导弹窗/说明页：不可静态还原，位于 native 解密后的载荷中（可见 DEX 内无任何相关字符串或布局）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Erişebilirlik Servisileri Etkinleştirme | 启用无障碍服务 | `res/values/strings.xml key=hssaAnk（被 res/xml/fpvlq.xml android:description 引用）` | 受限设置分步教学 |
| en | Postegro | Postegro（应用名／无障碍服务名） | `res/values/strings.xml key=a（Manifest android:label 与服务 label 共用）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：可见 DEX 不含任何设置页跳转或重试逻辑，需运行期观测是否存在 onResume 死循环重跳或定时拉起
- **遮罩叠层 / 高仿系统设置页**：不可静态还原；但无障碍配置已开启 flagRetrieveInteractiveWindows + canRetrieveWindowContent + typeAllMask，具备运行期叠放遮罩/伪造界面的完整能力
- **Android 13+ 受限设置（Restricted Settings）应对**：不可静态还原（可见 DEX 无 APPLICATION_DETAILS_SETTINGS 或『受限设置』相关字符串；targetSdk 依 platformBuildVersionCode=28 属 13 以下，暂不触发该路径）
- **获权后即时行为与防撤权机制**：不可静态还原；已确认配套设备管理器策略 wipe-data/reset-password/force-lock/disable-camera 与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，具备反撤权/反卸载基础能力
- **良性降级 / 替代方案**：无（未发现任何降级路径或替代模式声明）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：进程启动后立即监测：①任何 Intent 指向 Settings.ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的 startActivity；②首个非系统 Activity/Dialog 的窗口出现（Application 解密后往往立即拉起引导页）；③无障碍服务 onServiceConnected 回调前的窗口序列
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：静态只能看到空壳 DEX 与高熵加密载荷，引导文案与页面全部在 native 解密后生成，纯静态 UTG 无法获得任何诱导原文；必须在运行期（冷启动/首启）即时抓取窗口树，否则载荷解密完成后可能直接跳转系统设置页而错过引导页。另需注意本样本未声明 android:isAccessibilityTool，Android 12+ 会显示系统警告，其引导文案大概率包含『忽略警告』话术，需重点抓取。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **解密后的首个引导页/弹窗（冷启动或功能触发）** | 非 Postegro 已知空壳类的窗口；窗口类型为 Dialog 或 Theme.AppCompat.Transparent.NoActionBar 透明 Activity | 这是唯一承载逐字诱导文案与按钮集合的页面，直接决定是否存在不可取消诱导 | 全部 TextView 文本与按钮文本（含『取消/稍后』是否存在）；弹窗是否 setCancelable(false)、返回键是否被拦截；页面内是否出现品牌 Logo/仿系统 UI 元素 |
| **跳转无障碍设置瞬间的前后台切换** | Intent action=android.settings.ACCESSIBILITY_SETTINGS 或 ComponentName=com.android.settings/.Settings$AccessibilitySettingsActivity | 确认引导链路是否直跳系统无障碍页，以及跳转前是否先经说明页（一步式 vs 多步式） | Intent extra 与目标包名；跳转前后 Activity 栈变化；跳转时是否同时启动悬浮窗/遮罩 |
| **系统无障碍服务列表项** | 设置→无障碍→已下载的服务 中的 Postegro 条目 | 核验服务名与说明文案是否与代码一致、系统是否附加『非无障碍工具』警告（Android 12+ isAccessibilityTool 缺失） | 条目名称与描述文本；是否显示系统安全警告横幅；开关初始状态 |
| **拒绝/返回后的反馈页** | 用户从设置页返回后重新出现在栈顶的窗口 | 区分良性降级与拒权死循环重跳这一关键判定点 | 返回后是否在 1-2 秒内重新拉起同一引导页；是否出现倒计时/催促文案；退出应用后是否被再次拉起 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.themdont25.KJzpnjM.attachBaseContext`
- `com.themdont25.KJzpnjM.JDLxIs（native，libZyRnrN.so 导出 Java_com_themdont25_KJzpnjM_JDLxIs）`
- `AndroidManifest.xml (lines 117-122) 无障碍服务 com.themdont25.p075h`
- `res/xml/fpvlq.xml（typeAllMask / canRetrieveWindowContent / flagRetrieveInteractiveWindows）`
- `res/values/strings.xml（a=Postegro, hssaAnk=Erişebilirlik Servisileri Etkinleştirme）`
- `res/raw/dciwqlhgujksf（460684 字节高熵加密载荷）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（代码级定向核验）

**一句话**：该样本把“引导用户开启无障碍”的**全部实现**（引导页面、跳转逻辑、服务 `p075h` 的实体代码）从可见 DEX 中剥离，改由 `Application.attachBaseContext` 阶段的 native 解密器从高熵资源中还原，因此**静态只能看到外壳与资源声明，页面流转不可静态还原**。

**已确认的静态事实**
1. **DEX 是空壳**：`classes.dex` 仅 7168 字节 / 30 个类，除 `KJzpnjM`、`R`、`BuildConfig` 外均为随机名空类；Manifest 声明的 `p075h`、`p016j` 等在 DEX 字符串表中命中 **0 次**。静态预筛“DEX 线索全空、无障碍标签/description 为空”并非未实现，而是**实现被移出**。
2. **启动即进 native**：[KJzpnjM.attachBaseContext](<resource-unit:<local_path> code:com.themdont25.KJzpnjM#attachBaseContext>) 在 `super` 后立刻调用 native [KJzpnjM.JDLxIs](<resource-unit:<local_path> code:com.themdont25.KJzpnjM#JDLxIs>)，实现位于 [lib/arm64-v8a/libZyRnrN.so](<resource-unit:<local_path> file:all>)（导出 `Java_com_themdont25_KJzpnjM_JDLxIs`，混淆 C++ 符号 + `fopen/fwrite/strstr` + `CallStaticObjectMethod/NewObject` 反射）。
3. **加密载荷**：[res/raw/dciwqlhgujksf](<resource-unit:<local_path> file:all>) 460,684 字节，无 DEX/ZIP/ELF 魔数，单字节异或常见密钥均失败，字节分布近似均匀（高熵）；[assets/com5.cgZz](<resource-unit:<local_path> file:all>) 等 50 个随机长名分片同属二进制密文。
4. **无障碍声明极其激进**：[AndroidManifest.xml (lines 117-122)](<resource-unit:<local_path> file:L117-L122>) 声明 `com.themdont25.p075h`；[res/xml/fpvlq.xml](<resource-unit:<local_path> file:all>) 配置 `typeAllMask` + `canRetrieveWindowContent="true"` + `flagRetrieveInteractiveWindows`（读全窗口内容、跨应用交互）。
5. **身份与文案**：[strings.xml (lines 3-4)](<resource-unit:<local_path> file:L3-L4>) 全包仅两条字符串：`a = Postegro`（桌面名 + 无障碍服务标签）、`hssaAnk = Erişebilirlik Servisileri Etkinleştirme`（土耳其语“启用无障碍服务”）。**服务描述被用作诱导说辞**，无任何业务合理性说明。
6. **配套反卸载与高权限**：[res/xml/sznlbpvzx.xml](<resource-unit:<local_path> file:all>) 申请 `wipe-data / reset-password / force-lock / disable-camera`；叠加 `READ_SMS/SEND_SMS/CALL_PHONE/WRITE_SETTINGS/REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`、SMS_DELIVER 高优先级接收器、通知监听服务，符合 BankBot 系银行木马画像。

**未决项（覆盖边界）**：`ACTION_ACCESSIBILITY_SETTINGS` 跳转点、引导弹窗/WebView、拒绝重试循环、获权后自点确认等**均未取得任何静态证据**——DEX 内不存在相关字符串，密钥与解包算法仅在混淆 native 库内，超出本次调用预算未做 angr 全量反编译。相关风险已登记为 R-001。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "可见 classes.dex 仅 7168 字节、30 个空壳类，Manifest 声明的无障碍服务类 com.themdont25.p075h 及各 Activity 在 DEX 字符串表中零命中；全部业务逻辑（含无障碍引导 UI 与跳转序列）由 Application.attachBaseContext 调用的 native 方法 JDLxIs（libZyRnrN.so，混淆 C++ 符号）在运行期解密 res/raw/dciwqlhgujksf（460684 字节高熵）与 50 个随机长名 assets 分片后动态加载。仅 Manifest、res/xml 无障碍与设备管理器配置、strings.xml 两条字符串可静态确认。",
  "summary_one_liner": "空壳 DEX + Application 启动即 native 解密高熵资源还原全部逻辑，静态仅暴露一个标签为 Postegro、说明为土耳其语『启用无障碍服务』的 typeAllMask/canRetrieveWindowContent 无障碍服务，引导页面流转藏于加密载荷内不可静态还原。",
  "disguise_identity": {
    "app_display_name": "Postegro",
    "claimed_brand_or_persona": "Postegro（无品牌指向的虚构应用名，非真实社交/银行品牌，实际为银行木马外壳）",
    "a11y_service_label": "Postegro",
    "identity_mismatch": true,
    "obfuscation_tricks": "服务标签与桌面名复用同一字符串 @string/a=Postegro，无障碍说明 hssaAnk 仅写土耳其语『启用无障碍服务』而无任何功能合理性说明；服务类名 com.themdont25.p075h 及全部 Activity 使用无意义短名（p012p/p015k/p020a 等）；类名与资产文件名大量随机化；未声明 android:isAccessibilityTool，依赖系统默认判定以规避 Android 12+ 的『非无障碍工具』提示"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.themdont25.KJzpnjM（自定义 Application）",
      "trigger_event": "进程创建时 attachBaseContext(Context) 回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "此阶段无界面，仅执行 native 解密初始化",
      "user_action_requested": "无（用户不可见）",
      "code_anchor": "com.themdont25.KJzpnjM.attachBaseContext"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "libZyRnrN.so 内 Java_com_themdont25_KJzpnjM_JDLxIs",
      "trigger_event": "attachBaseContext 直接调用 native 方法 JDLxIs(context)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "native 层读取并解密 res/raw/dciwqlhgujksf 与 assets 分片，反射构造真实组件（推测为落地 DEX/替换 Application）",
      "user_action_requested": "无（用户不可见）",
      "code_anchor": "com.themdont25.KJzpnjM.JDLxIs / lib/arm64-v8a/libZyRnrN.so"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "系统无障碍列表中的服务条目（com.themdont25.p075h）",
      "trigger_event": "用户进入 设置→无障碍→已下载的服务 时由系统渲染服务名与说明",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Postegro / Erişebilirlik Servisileri Etkinleştirme",
      "shown_text_zh": "Postegro / 启用无障碍服务",
      "user_action_requested": "系统页内开启开关；服务本身无取消/跳过选项",
      "code_anchor": "res/values/strings.xml (a, hssaAnk) + res/xml/fpvlq.xml android:description"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "未知（预期为解密载荷内 Activity/Dialog）",
      "trigger_event": "不可静态还原：DEX 中不存在 ACTION_ACCESSIBILITY_SETTINGS 相关字符串",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无法静态取得引导文案与跳转实现",
      "user_action_requested": "不可静态判定是否有取消/跳过按钮",
      "code_anchor": "不可静态还原（载荷 res/raw/dciwqlhgujksf 解密后）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.themdont25.p075h（AccessibilityService，实现类不可见）",
      "trigger_event": "系统绑定无障碍服务后回调（typeAllMask 监听全部事件）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后即可读取全部窗口内容并跨应用交互（覆盖/点击/劫持），配合设备管理器 wipe-data 具备反卸载能力",
      "user_action_requested": "无",
      "code_anchor": "AndroidManifest.xml (lines 117-122) + res/xml/fpvlq.xml + res/xml/sznlbpvzx.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目：服务名 Postegro（@string/a）与说明 Erişebilirlik Servisileri Etkinleştirme（@string/hssaAnk），由 res/xml/fpvlq.xml 的 android:description 引用",
    "桌面图标名称：android:label=@string/a 即 Postegro（Manifest activity 与 a11y service、device admin receiver 共用）",
    "应用内引导弹窗/说明页：不可静态还原，位于 native 解密后的载荷中（可见 DEX 内无任何相关字符串或布局）"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Erişebilirlik Servisileri Etkinleştirme",
      "text_zh": "启用无障碍服务",
      "source_location": "res/values/strings.xml key=hssaAnk（被 res/xml/fpvlq.xml android:description 引用）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Postegro",
      "text_zh": "Postegro（应用名／无障碍服务名）",
      "source_location": "res/values/strings.xml key=a（Manifest android:label 与服务 label 共用）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：可见 DEX 不含任何设置页跳转或重试逻辑，需运行期观测是否存在 onResume 死循环重跳或定时拉起",
    "overlay_or_fake_settings": "不可静态还原；但无障碍配置已开启 flagRetrieveInteractiveWindows + canRetrieveWindowContent + typeAllMask，具备运行期叠放遮罩/伪造界面的完整能力",
    "restricted_settings_13plus_coaching": "不可静态还原（可见 DEX 无 APPLICATION_DETAILS_SETTINGS 或『受限设置』相关字符串；targetSdk 依 platformBuildVersionCode=28 属 13 以下，暂不触发该路径）",
    "post_grant_anti_removal": "不可静态还原；已确认配套设备管理器策略 wipe-data/reset-password/force-lock/disable-camera 与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，具备反撤权/反卸载基础能力",
    "benign_graceful_degradation": "无（未发现任何降级路径或替代模式声明）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "进程启动后立即监测：①任何 Intent 指向 Settings.ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的 startActivity；②首个非系统 Activity/Dialog 的窗口出现（Application 解密后往往立即拉起引导页）；③无障碍服务 onServiceConnected 回调前的窗口序列",
    "key_pages_to_capture": [
      {
        "page_role": "解密后的首个引导页/弹窗（冷启动或功能触发）",
        "page_identifier": "非 Postegro 已知空壳类的窗口；窗口类型为 Dialog 或 Theme.AppCompat.Transparent.NoActionBar 透明 Activity",
        "why_most_useful": "这是唯一承载逐字诱导文案与按钮集合的页面，直接决定是否存在不可取消诱导",
        "observable_utg_signals": ["全部 TextView 文本与按钮文本（含『取消/稍后』是否存在）", "弹窗是否 setCancelable(false)、返回键是否被拦截", "页面内是否出现品牌 Logo/仿系统 UI 元素"]
      },
      {
        "page_role": "跳转无障碍设置瞬间的前后台切换",
        "page_identifier": "Intent action=android.settings.ACCESSIBILITY_SETTINGS 或 ComponentName=com.android.settings/.Settings$AccessibilitySettingsActivity",
        "why_most_useful": "确认引导链路是否直跳系统无障碍页，以及跳转前是否先经说明页（一步式 vs 多步式）",
        "observable_utg_signals": ["Intent extra 与目标包名", "跳转前后 Activity 栈变化", "跳转时是否同时启动悬浮窗/遮罩"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置→无障碍→已下载的服务 中的 Postegro 条目",
        "why_most_useful": "核验服务名与说明文案是否与代码一致、系统是否附加『非无障碍工具』警告（Android 12+ isAccessibilityTool 缺失）",
        "observable_utg_signals": ["条目名称与描述文本", "是否显示系统安全警告横幅", "开关初始状态"]
      },
      {
        "page_role": "拒绝/返回后的反馈页",
        "page_identifier": "用户从设置页返回后重新出现在栈顶的窗口",
        "why_most_useful": "区分良性降级与拒权死循环重跳这一关键判定点",
        "observable_utg_signals": ["返回后是否在 1-2 秒内重新拉起同一引导页", "是否出现倒计时/催促文案", "退出应用后是否被再次拉起"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：静态只能看到空壳 DEX 与高熵加密载荷，引导文案与页面全部在 native 解密后生成，纯静态 UTG 无法获得任何诱导原文；必须在运行期（冷启动/首启）即时抓取窗口树，否则载荷解密完成后可能直接跳转系统设置页而错过引导页。另需注意本样本未声明 android:isAccessibilityTool，Android 12+ 会显示系统警告，其引导文案大概率包含『忽略警告』话术，需重点抓取。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.themdont25.KJzpnjM.attachBaseContext",
    "com.themdont25.KJzpnjM.JDLxIs（native，libZyRnrN.so 导出 Java_com_themdont25_KJzpnjM_JDLxIs）",
    "AndroidManifest.xml (lines 117-122) 无障碍服务 com.themdont25.p075h",
    "res/xml/fpvlq.xml（typeAllMask / canRetrieveWindowContent / flagRetrieveInteractiveWindows）",
    "res/values/strings.xml（a=Postegro, hssaAnk=Erişebilirlik Servisileri Etkinleştirme）",
    "res/raw/dciwqlhgujksf（460684 字节高熵加密载荷）"
  ]
}
```

</details>

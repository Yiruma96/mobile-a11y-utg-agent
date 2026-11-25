# MB_082__fd7e7e23db｜Ermac — QR CreatorScanner

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：203.7s

## 1. 一句话核心结论

- **核心申请方式**：以 QR CreatorScanner 二维码工具为外壳，无障碍服务与全部业务逻辑藏于 6.2MB 加密资产经 DexClassLoader 反射加载，静态看不到任何诱导页面，仅留下无描述的无障碍服务声明与'Accessibility settings'等孤儿文案资源。
- **静态可见性说明**：仅壳层可见：classes.dex 只有 Application 反射引导器与 Lottie/GMS 依赖，Manifest 声明的无障碍服务 com.tulecazopabi.banewo.tebojatuci.xefetune 及全部 com.tulecazopabi.banewo.* 组件实现均不在 DEX 中；二阶段代码位于加密资产 assets/CbWXQU.json（6.2MB 非文本密文），由 Application.onCreate/attachBaseContext 经 XOR 解密字符串 + DexClassLoader 反射注入 pathClassLoader 后执行。引导弹窗、跳转顺序、文案均无法静态还原。
- **命中的行为模式标签**：`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `fd7e7e23db5f645db9ed47a5d36e7cf57ca2dbdf46a37484eafa1e04f657bf02` |
| 包名 / 年份 | `com.tag.right` / 2022 |
| 家族 / 品类 | **Ermac**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | QR CreatorScanner |
| 引导页宣称品牌/身份 | 二维码扫描/创建工具（QR CreatorScanner），实际无任何扫码业务实现 |
| 系统无障碍列表服务名 | QR CreatorScanner |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未声明 android:description，系统无障碍列表无任何功能说明；无障碍服务名与桌面名完全一致以冒充正常工具；大量 Activity 的 label 为随机小写串（papqnkmarfmphne、sunittdioldpnl...）；cevuna/nemuyahelu/pavu 使用 android:label="" 且 excludeFromRecents + Theme.NoDisplay 隐身；taskAffinity 伪装为 ...toast / ...perm / ...main 多套别名；包名与类名（com.tag.right / com.tulecazopabi.banewo）完全无意义随机化；关键类名/方法名/字段名以字节数组 XOR 常量表运行时还原 |
| 无障碍服务类名 | `com.tulecazopabi.banewo.tebojatuci.xefetune` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.tulecazopabi.banewo.zamosa（exported=true，MAIN/LAUNCHER，taskAffinity=com.tulecazopabi.banewo.main） | 用户点击桌面图标启动；进程随后触发 Application.onCreate/attachBaseContext | 不可静态还原 | 无 | 不可静态还原 | `AndroidManifest.xml: com.tulecazopabi.banewo.zamosa（MAIN/LAUNCHER）；实现类缺失` |
| 2 | 冷启动入口 | com.tag.right.GEyFfPkBdBiDgQpRiYcCkZaBz（Application）→ OZdBuNiNdLuMdNjWePcTnGpGdBxOuIwBnIjNqSgQtAiNcTuIqEkJaSa（加载器） | Application.attachBaseContext → wordventure → roundexhaust；Application.onCreate → wininput → DexClassLoader 注入 | 不可静态还原 | **原文**：无（无任何用户界面，纯后台解密注入）<br>**译注**：无界面；XOR 还原类名/方法名后反射构造 DexClassLoader 并替换父加载器字段 | 无需用户操作，进程启动即发生 | `GEyFfPkBdBiDgQpRiYcCkZaBz#onCreate / #wininput / #wordventure；OZdBuNiNdLuMdNjWePcTnGpGdBxOuIwBnIjNqSgQtAiNcTuIqEkJaSa#roundexhaust / #fatramp / #impactglory` |
| 3 | 跳无障碍设置 | 系统设置 → 无障碍 → 已安装服务列表项（服务 com.tulecazopabi.banewo.tebojatuci.xefetune，label=QR CreatorScanner） | 不可静态还原；相关跳转代码位于加密载荷内（DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 调用点） | 系统无障碍页 | **原文**：Accessibility settings / Accessibility（strings.xml: spec_settings / spec_settings2，DEX 中无引用点）<br>**译注**：无障碍设置 / 无障碍（疑为跳转入口按钮文案，消费代码在载荷内） | 不可静态还原；服务项无 android:description，用户看不到任何功能说明 | `res/values/strings.xml#spec_settings / #spec_settings2；res/xml/mugi.xml；AndroidManifest.xml service tebojatuci.xefetune` |
| 4 | 跳受限设置 | 应用详情页（清缓存/卸载/权限页）相关资源已就位 | 不可静态还原 | 不可静态还原 | **原文**：Clear data / Storage: / Clear cache / Uninstall / Setting<br>**译注**：清除数据 / 存储 / 清除缓存 / 卸载 / 设置（DEX 中均无引用点，消费代码在载荷内） | 不可静态还原；存在诱导用户前往应用详情页卸载/清理类页面的资源准备迹象 | `res/values/strings.xml#clear_data / #app_info_storage / #harmful_app_warning_uninstall / #menu_setting` |
| 5 | 获权后动作 | com.tulecazopabi.banewo.tebojatuci.xefetune（BIND_ACCESSIBILITY_SERVICE，绑定 res/xml/mugi.xml） | 系统绑定无障碍服务后回调（服务实现不在 DEX 中） | 不可静态还原 | 无 | 不可静态还原 | `res/xml/mugi.xml（canRetrieveWindowContent=true、flagRetrieveInteractiveWindows、typeWindowContentChanged/typeViewTextChanged）；AndroidManifest.xml 设备管理 receiver xarenu.tayokigeduwoti` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表：服务 label 直接使用应用名 'QR CreatorScanner'，且 android:description 完全缺失，呈现为无说明条目
- strings.xml 资源中预留 'Accessibility settings' / 'Accessibility' 两条跳转入口文案，但 DEX 内无任何引用点，实际呈现在加密载荷控制的界面中（不可静态定位）
- strings.xml 预留 'Clear data' / 'Storage:' / 'Clear cache' / 'Uninstall' / 'Setting' 等应用详情页相关文案，同样无 DEX 引用点
- 预筛所列 Google Play services 提示文案均为 com.google.android.gms 自带默认资源，未发现被任何应用自身代码或界面用作诱导话术
- 所有引导弹窗/Activity/WebView/悬浮窗的具体承载位置均无法静态定位：相关组件类不在 classes.dex 中

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Accessibility settings | 无障碍设置 | `res/values/strings.xml key=spec_settings（DEX 无引用点）` | 未知 |
| en | Accessibility | 无障碍 | `res/values/strings.xml key=spec_settings2（DEX 无引用点）` | 未知 |
| en | Clear data | 清除数据 | `res/values/strings.xml key=clear_data（DEX 无引用点）` | 未知 |
| en | Uninstall | 卸载 | `res/values/strings.xml key=harmful_app_warning_uninstall（DEX 无引用点）` | 未知 |
| en | %1$s won't work unless you enable Google Play services. | %1$s 在启用 Google Play 服务前无法运行。 | `res/values/strings.xml key=common_google_play_services_enable_text（GMS SDK 默认资源）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：DEX 中不存在 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 调用点，也无 onResume 权限轮询逻辑，全部跳转与重试代码位于加密载荷内
- **遮罩叠层 / 高仿系统设置页**：不可静态还原；但已声明 SYSTEM_ALERT_WINDOW 权限与 canRequestTouchExplorationMode，具备叠放悬浮引导层与触摸探索劫持的完整能力基础
- **Android 13+ 受限设置（Restricted Settings）应对**：不可静态还原（targetSdk=28，低于 Android 13 受限设置门控阈值；未发现 Session 安装器或应用详情右上角菜单引导代码）
- **获权后即时行为与防撤权机制**：不可静态还原；已声明设备管理 Receiver（xarenu.tayokigeduwoti，BIND_DEVICE_ADMIN，监听 DEVICE_ADMIN_DISABLE_REQUESTED）与 REQUEST_DELETE_PACKAGES，具备撤权/卸载对抗能力基础
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 com.tag.right 进程拉起（launcher com.tulecazopabi.banewo.zamosa 出现）后立即开始录制，并在任何跳转至 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间压栈截图；由于跳转时机完全由加密载荷决定，建议冷启动后持续 60 秒以上全程 UTG 采样而非单点触发
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：全部引导界面与跳转逻辑位于 assets/CbWXQU.json 加密二阶段载荷内，静态完全不可见，需依赖运行期 UTG 全程录制补齐；若载荷按环境门控（模拟器/地域/安装时长）不激活，则运行期亦可能观察不到任何诱导页面。此外服务无 android:description，纯文本 UTG 在该条目上只能取到名称，需结合空白说明判定。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首屏/引导页（载荷解密完成后的第一个界面）** | 包名 com.tag.right、activity 组件名 com.tulecazopabi.banewo.zamosa 或 xexerexejeko.cevuna，界面文案非二维码扫描相关 | 这是二阶段载荷解密成功后唯一能直接观察到的入口界面，用于确认诱导是冷启动直弹还是功能触发 | 首个非系统 Activity 的组件名与 taskAffinity；界面文本是否提及无障碍/权限/更新；是否存在全屏或半透明遮罩层节点；是否出现按钮但无取消/跳过控件 |
| **系统无障碍服务列表项（QR CreatorScanner 条目）** | 设置包 com.android.settings，页面含 'QR CreatorScanner' 文本且说明行为空 | 直接验证无 android:description 造成的空白说明这一身份掩护手法，是区分恶意与良性无障碍工具的最强单点证据 | 服务条目名称与描述是否为空；该条目是否由应用自动滚动/高亮定位；跳转发生前应用是否在前台 |
| **跳转设置页后的压栈遮罩/引导层** | SYSTEM_ALERT_WINDOW 类型悬浮窗或高仿设置页（组件名含 xexerexejeko.*，taskAffinity 为 ...toast / ...perm） | 确认是否在系统设置页之上叠放半透明指引遮罩或伪造开关页，属典型诱导升级手法 | 窗口层级是否为 TYPE_APPLICATION_OVERLAY；遮罩内是否含箭头/手指指向无障碍开关；是否有定时重复拉起的窗口重建 |
| **应用详情页（受限设置/卸载引导）** | 设置包 com.android.settings 的应用详情页，含 'Clear data' / 'Uninstall' 文案页 | 核实是否教用户前往应用详情页操作，以及是否伴随卸载对抗 | 是否从应用内跳转至应用详情页；页面停留时长与返回行为；是否触发设备管理激活弹窗 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.tag.right.GEyFfPkBdBiDgQpRiYcCkZaBz#onCreate`
- `com.tag.right.GEyFfPkBdBiDgQpRiYcCkZaBz#wininput`
- `com.tag.right.OZdBuNiNdLuMdNjWePcTnGpGdBxOuIwBnIjNqSgQtAiNcTuIqEkJaSa#fatramp`
- `com.tag.right.OZdBuNiNdLuMdNjWePcTnGpGdBxOuIwBnIjNqSgQtAiNcTuIqEkJaSa#roundexhaust`
- `res/xml/mugi.xml`
- `assets/CbWXQU.json`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 核验结论

**核心判断：静态可见的只有一层壳，无障碍诱导的页面流转全部位于加密二阶段载荷内，本次无法给出页面级 UTG 文案与跳转序列。**

已核实的链路：

- **Manifest 声明的无障碍服务类在 DEX 中不存在。** `com.tulecazopabi.banewo.tebojatuci.xefetune`（label=`QR CreatorScanner`，绑定 `@xml/mugi`）以及 40 余个 `com.tulecazopabi.banewo.*` Activity、Service、Receiver 均无法在 `classes.dex`（446 类，仅 `com.tag.*` + `com.airbnb.lottie`）中解析到，说明这些组件实现全部位于二阶段载荷。
- **启动即解密注入。** [Application.onCreate()](<resource-unit:#1.dex1 code:com.tag.right.GEyFfPkBdBiDgQpRiYcCkZaBz#onCreate>) 调 [wininput()](<resource-unit:#1.dex1 code:com.tag.right.GEyFfPkBdBiDgQpRiYcCkZaBz#wininput>)；`attachBaseContext` 经 [wordventure()](<resource-unit:#1.dex1 code:com.tag.right.GEyFfPkBdBiDgQpRiYcCkZaBz#wordventure>) 进入装载。类名/方法名由 `wheelticket()`/`alcoholmarch()` 用字节数组异或还原（如 `{81,116,32,...} ^ {48,26,68}`），以规避字符串检索。
- **反射构造 DexClassLoader 并替换父加载器字段。** [fatramp()](<resource-unit:#1.dex1 code:com.tag.right.OZdBuNiNdLuMdNjWePcTnGpGdBxOuIwBnIjNqSgQtAiNcTuIqEkJaSa#fatramp>) 用 `getConstructor(...).newInstance()` 构造加载器，[roundexhaust()](<resource-unit:#1.dex1 code:com.tag.right.OZdBuNiNdLuMdNjWePcTnGpGdBxOuIwBnIjNqSgQtAiNcTuIqEkJaSa#roundexhaust>) → [impactglory()](<resource-unit:#1.dex1 code:com.tag.right.GEyFfPkBdBiDgQpRiYcCkZaBz#wordventure>) 以 `Field.set` 写入 `pathClassLoader`。
- **载荷载体：** [assets/CbWXQU.json](<resource-unit:#1 file:assets/CbWXQU.json>) 6,235,800 字节，非文本二进制密文，是包内唯一可疑的大体积加密资产。
- **无障碍能力已声明且极宽：** [res/xml/mugi.xml](<resource-unit:#1 file:res/xml/mugi.xml>) 含 `canRetrieveWindowContent`、`canRequestTouchExplorationMode`、`flagRetrieveInteractiveWindows`，监听 `typeWindowContentChanged/typeViewTextChanged/typeNotificationStateChanged` 等全事件，且**未声明 `android:description`**，系统无障碍列表中将呈现空白说明。
- **引导文案资源存在但引用方缺失：** [res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml>) 中 `spec_settings="Accessibility settings"`、`spec_settings2="Accessibility"`、`clear_data`、`menu_setting`、`harmful_app_warning_uninstall` 等字符串在 DEX 中无任何引用点，与其消费代码同处载荷内。预筛列的 Google Play services 文案全部为 GMS SDK 自带默认资源，**未发现被用作诱导话术**。
- **身份掩护：** 桌面名与无障碍服务名同为 `QR CreatorScanner`，但应用无任何扫码业务实现；大量 Activity label 为随机小写串（`papqnkmarfmphne`、`sunittdioldpnl...`），另有 `cevuna`/`nemuyahelu`/`pavu` 的 `android:label=""` 且 `excludeFromRecents`+`Theme.NoDisplay`，`taskAffinity` 分别伪装为 `...toast`、`...perm`。

已登记风险 **R-001**（malware_trojan / high）。覆盖缺口：`CbWXQU.json` 的解密算法与密钥未能静态还原，故"如何一步步引导开启无障碍"的具体弹窗/Activity/跳转顺序属 `packed_or_encrypted`，只能确认引导文案资源的存在与无障碍能力的完整声明。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "仅壳层可见：classes.dex 只有 Application 反射引导器与 Lottie/GMS 依赖，Manifest 声明的无障碍服务 com.tulecazopabi.banewo.tebojatuci.xefetune 及全部 com.tulecazopabi.banewo.* 组件实现均不在 DEX 中；二阶段代码位于加密资产 assets/CbWXQU.json（6.2MB 非文本密文），由 Application.onCreate/attachBaseContext 经 XOR 解密字符串 + DexClassLoader 反射注入 pathClassLoader 后执行。引导弹窗、跳转顺序、文案均无法静态还原。",
  "summary_one_liner": "以 QR CreatorScanner 二维码工具为外壳，无障碍服务与全部业务逻辑藏于 6.2MB 加密资产经 DexClassLoader 反射加载，静态看不到任何诱导页面，仅留下无描述的无障碍服务声明与'Accessibility settings'等孤儿文案资源。",
  "disguise_identity": {
    "app_display_name": "QR CreatorScanner",
    "claimed_brand_or_persona": "二维码扫描/创建工具（QR CreatorScanner），实际无任何扫码业务实现",
    "a11y_service_label": "QR CreatorScanner",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未声明 android:description，系统无障碍列表无任何功能说明；无障碍服务名与桌面名完全一致以冒充正常工具；大量 Activity 的 label 为随机小写串（papqnkmarfmphne、sunittdioldpnl...）；cevuna/nemuyahelu/pavu 使用 android:label=\"\" 且 excludeFromRecents + Theme.NoDisplay 隐身；taskAffinity 伪装为 ...toast / ...perm / ...main 多套别名；包名与类名（com.tag.right / com.tulecazopabi.banewo）完全无意义随机化；关键类名/方法名/字段名以字节数组 XOR 常量表运行时还原"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.tulecazopabi.banewo.zamosa（exported=true，MAIN/LAUNCHER，taskAffinity=com.tulecazopabi.banewo.main）",
      "trigger_event": "用户点击桌面图标启动；进程随后触发 Application.onCreate/attachBaseContext",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "首屏内容不可静态获取（Activity 类不在 DEX 中）",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml: com.tulecazopabi.banewo.zamosa（MAIN/LAUNCHER）；实现类缺失"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.tag.right.GEyFfPkBdBiDgQpRiYcCkZaBz（Application）→ OZdBuNiNdLuMdNjWePcTnGpGdBxOuIwBnIjNqSgQtAiNcTuIqEkJaSa（加载器）",
      "trigger_event": "Application.attachBaseContext → wordventure → roundexhaust；Application.onCreate → wininput → DexClassLoader 注入",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（无任何用户界面，纯后台解密注入）",
      "shown_text_zh": "无界面；XOR 还原类名/方法名后反射构造 DexClassLoader 并替换父加载器字段",
      "user_action_requested": "无需用户操作，进程启动即发生",
      "code_anchor": "GEyFfPkBdBiDgQpRiYcCkZaBz#onCreate / #wininput / #wordventure；OZdBuNiNdLuMdNjWePcTnGpGdBxOuIwBnIjNqSgQtAiNcTuIqEkJaSa#roundexhaust / #fatramp / #impactglory"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已安装服务列表项（服务 com.tulecazopabi.banewo.tebojatuci.xefetune，label=QR CreatorScanner）",
      "trigger_event": "不可静态还原；相关跳转代码位于加密载荷内（DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 调用点）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Accessibility settings / Accessibility（strings.xml: spec_settings / spec_settings2，DEX 中无引用点）",
      "shown_text_zh": "无障碍设置 / 无障碍（疑为跳转入口按钮文案，消费代码在载荷内）",
      "user_action_requested": "不可静态还原；服务项无 android:description，用户看不到任何功能说明",
      "code_anchor": "res/values/strings.xml#spec_settings / #spec_settings2；res/xml/mugi.xml；AndroidManifest.xml service tebojatuci.xefetune"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "应用详情页（清缓存/卸载/权限页）相关资源已就位",
      "trigger_event": "不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Clear data / Storage: / Clear cache / Uninstall / Setting",
      "shown_text_zh": "清除数据 / 存储 / 清除缓存 / 卸载 / 设置（DEX 中均无引用点，消费代码在载荷内）",
      "user_action_requested": "不可静态还原；存在诱导用户前往应用详情页卸载/清理类页面的资源准备迹象",
      "code_anchor": "res/values/strings.xml#clear_data / #app_info_storage / #harmful_app_warning_uninstall / #menu_setting"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.tulecazopabi.banewo.tebojatuci.xefetune（BIND_ACCESSIBILITY_SERVICE，绑定 res/xml/mugi.xml）",
      "trigger_event": "系统绑定无障碍服务后回调（服务实现不在 DEX 中）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "具备读取全部窗口文本、触摸探索、监听窗口/文本/通知变化的能力；配合 READ_SMS/RECEIVE_SMS/SEND_SMS、设备管理 Receiver、SYSTEM_ALERT_WINDOW、REQUEST_INSTALL_PACKAGES",
      "user_action_requested": "不可静态还原",
      "code_anchor": "res/xml/mugi.xml（canRetrieveWindowContent=true、flagRetrieveInteractiveWindows、typeWindowContentChanged/typeViewTextChanged）；AndroidManifest.xml 设备管理 receiver xarenu.tayokigeduwoti"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表：服务 label 直接使用应用名 'QR CreatorScanner'，且 android:description 完全缺失，呈现为无说明条目",
    "strings.xml 资源中预留 'Accessibility settings' / 'Accessibility' 两条跳转入口文案，但 DEX 内无任何引用点，实际呈现在加密载荷控制的界面中（不可静态定位）",
    "strings.xml 预留 'Clear data' / 'Storage:' / 'Clear cache' / 'Uninstall' / 'Setting' 等应用详情页相关文案，同样无 DEX 引用点",
    "预筛所列 Google Play services 提示文案均为 com.google.android.gms 自带默认资源，未发现被任何应用自身代码或界面用作诱导话术",
    "所有引导弹窗/Activity/WebView/悬浮窗的具体承载位置均无法静态定位：相关组件类不在 classes.dex 中"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Accessibility settings",
      "text_zh": "无障碍设置",
      "source_location": "res/values/strings.xml key=spec_settings（DEX 无引用点）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility",
      "text_zh": "无障碍",
      "source_location": "res/values/strings.xml key=spec_settings2（DEX 无引用点）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Clear data",
      "text_zh": "清除数据",
      "source_location": "res/values/strings.xml key=clear_data（DEX 无引用点）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Uninstall",
      "text_zh": "卸载",
      "source_location": "res/values/strings.xml key=harmful_app_warning_uninstall（DEX 无引用点）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "%1$s 在启用 Google Play 服务前无法运行。",
      "source_location": "res/values/strings.xml key=common_google_play_services_enable_text（GMS SDK 默认资源）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：DEX 中不存在 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 调用点，也无 onResume 权限轮询逻辑，全部跳转与重试代码位于加密载荷内",
    "overlay_or_fake_settings": "不可静态还原；但已声明 SYSTEM_ALERT_WINDOW 权限与 canRequestTouchExplorationMode，具备叠放悬浮引导层与触摸探索劫持的完整能力基础",
    "restricted_settings_13plus_coaching": "不可静态还原（targetSdk=28，低于 Android 13 受限设置门控阈值；未发现 Session 安装器或应用详情右上角菜单引导代码）",
    "post_grant_anti_removal": "不可静态还原；已声明设备管理 Receiver（xarenu.tayokigeduwoti，BIND_DEVICE_ADMIN，监听 DEVICE_ADMIN_DISABLE_REQUESTED）与 REQUEST_DELETE_PACKAGES，具备撤权/卸载对抗能力基础",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 com.tag.right 进程拉起（launcher com.tulecazopabi.banewo.zamosa 出现）后立即开始录制，并在任何跳转至 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间压栈截图；由于跳转时机完全由加密载荷决定，建议冷启动后持续 60 秒以上全程 UTG 采样而非单点触发",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首屏/引导页（载荷解密完成后的第一个界面）",
        "page_identifier": "包名 com.tag.right、activity 组件名 com.tulecazopabi.banewo.zamosa 或 xexerexejeko.cevuna，界面文案非二维码扫描相关",
        "why_most_useful": "这是二阶段载荷解密成功后唯一能直接观察到的入口界面，用于确认诱导是冷启动直弹还是功能触发",
        "observable_utg_signals": ["首个非系统 Activity 的组件名与 taskAffinity", "界面文本是否提及无障碍/权限/更新", "是否存在全屏或半透明遮罩层节点", "是否出现按钮但无取消/跳过控件"]
      },
      {
        "page_role": "系统无障碍服务列表项（QR CreatorScanner 条目）",
        "page_identifier": "设置包 com.android.settings，页面含 'QR CreatorScanner' 文本且说明行为空",
        "why_most_useful": "直接验证无 android:description 造成的空白说明这一身份掩护手法，是区分恶意与良性无障碍工具的最强单点证据",
        "observable_utg_signals": ["服务条目名称与描述是否为空", "该条目是否由应用自动滚动/高亮定位", "跳转发生前应用是否在前台"]
      },
      {
        "page_role": "跳转设置页后的压栈遮罩/引导层",
        "page_identifier": "SYSTEM_ALERT_WINDOW 类型悬浮窗或高仿设置页（组件名含 xexerexejeko.*，taskAffinity 为 ...toast / ...perm）",
        "why_most_useful": "确认是否在系统设置页之上叠放半透明指引遮罩或伪造开关页，属典型诱导升级手法",
        "observable_utg_signals": ["窗口层级是否为 TYPE_APPLICATION_OVERLAY", "遮罩内是否含箭头/手指指向无障碍开关", "是否有定时重复拉起的窗口重建"]
      },
      {
        "page_role": "应用详情页（受限设置/卸载引导）",
        "page_identifier": "设置包 com.android.settings 的应用详情页，含 'Clear data' / 'Uninstall' 文案页",
        "why_most_useful": "核实是否教用户前往应用详情页操作，以及是否伴随卸载对抗",
        "observable_utg_signals": ["是否从应用内跳转至应用详情页", "页面停留时长与返回行为", "是否触发设备管理激活弹窗"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "存在显著盲区：全部引导界面与跳转逻辑位于 assets/CbWXQU.json 加密二阶段载荷内，静态完全不可见，需依赖运行期 UTG 全程录制补齐；若载荷按环境门控（模拟器/地域/安装时长）不激活，则运行期亦可能观察不到任何诱导页面。此外服务无 android:description，纯文本 UTG 在该条目上只能取到名称，需结合空白说明判定。"
  },
  "behavior_pattern_tags": [
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION"
  ],
  "code_anchors": [
    "com.tag.right.GEyFfPkBdBiDgQpRiYcCkZaBz#onCreate",
    "com.tag.right.GEyFfPkBdBiDgQpRiYcCkZaBz#wininput",
    "com.tag.right.OZdBuNiNdLuMdNjWePcTnGpGdBxOuIwBnIjNqSgQtAiNcTuIqEkJaSa#fatramp",
    "com.tag.right.OZdBuNiNdLuMdNjWePcTnGpGdBxOuIwBnIjNqSgQtAiNcTuIqEkJaSa#roundexhaust",
    "res/xml/mugi.xml",
    "assets/CbWXQU.json"
  ]
}
```

</details>

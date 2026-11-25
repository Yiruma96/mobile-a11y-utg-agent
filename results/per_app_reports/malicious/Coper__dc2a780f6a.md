# MB_050__dc2a780f6a｜Coper — Google Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：170.8s

## 1. 一句话核心结论

- **核心申请方式**：以 Google Chrome 名义注册无障碍服务并内置土耳其语『启用无障碍服务』文案，采用透明无标题 Activity + 伪造系统设置项身份，实际引导与操控代码全部封装在加密载荷与自定义 SO 中，静态无法还原具体弹窗与跳转序列。
- **静态可见性说明**：清单与资源层完整可见：无障碍服务 com.pagethan10.p068s、label=@string/a(Google Chrome)、土耳其语引导文案、全部高危权限与组件声明均可读。但所有 com.pagethan10.* 实现类在 classes.dex 中缺失（该类计数为 0，DEX 仅含 Unity Ads 与 com.rail.dignity），真实引导流程与无障碍操作逻辑位于随包高熵载荷 assets/DDlfO.json（1,060,765B）、AndroidManifest.xml/raw/vkicna（1,000,028B）与自定义原生库 libMJnWUXJ.so 中，须运行期由 SO 解密释放；assets 下另有 Vue 打包前端资源作为 Hybrid 承载层，但为构建产物而非可读引导页。
- **命中的行为模式标签**：`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `dc2a780f6abb9f0ec0a6675f20acb91ebe2a8748297682a59daf9164fbea2ee8` |
| 包名 / 年份 | `com.pagethan10` / 2026 |
| 家族 / 品类 | **Coper**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google Chrome |
| 引导页宣称品牌/身份 | Google Chrome（谷歌官方浏览器） |
| 系统无障碍列表服务名 | Google Chrome |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:description 留空，系统设置页不展示任何权限用途说明；应用显示名、无障碍服务标签、设备管理员 receiver 标签统一复用同一字符串 @string/a 指向 Google Chrome；启动 Activity 额外注册 com.android.settings.action.IA_SETTINGS 与 android.app.action.ANGLE_FOR_ANDROID、QS_TILE_PREFERENCES，冒充系统设置项/系统组件身份；主入口使用 MAIN + category.INFO 而非 LAUNCHER 以弱化桌面图标存在感；多数 Activity 采用 Theme.AppCompat.Transparent.NoActionBar 透明无标题主题便于叠层；APK 内条目路径被改写成 classes.dex/xml/...、AndroidManifest.xml/raw/vkicna 等畸形结构并对 ZIP 标志位做手脚，使常规解包工具解析失败。 |
| 无障碍服务类名 | `com.pagethan10.p068s` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.pagethan10 主 Activity（清单中 label=@string/a 的启动项，声明 MAIN + category.INFO，并叠加 ANGLE_FOR_ANDROID / QS_TILE_PREFERENCES / IA_SETTINGS 过滤器） | 系统或外部 intent 启动主 Activity；类实现体不在 classes.dex 中，具体 onCreate 逻辑需解密载荷后确认 | 不可静态还原 | **原文**：Google Chrome<br>**译注**：谷歌 Chrome（应用与界面标题显示名） | 无明确要求；静态不可确认首屏是否直接弹出引导或先呈现空壳界面 | `AndroidManifest.xml 启动 activity 节点（label=@string/a）` |
| 2 | 引导说明页 | 清单声明的多个 Theme.AppCompat.Transparent.NoActionBar Activity（com.pagethan10.p054i / p084c / p020f 等）与 Theme.Dialog Activity（com.pagethan10.p024i），以及 assets 下 Vue 打包前端（index.*.js/css、emailRegister、emailVerify） | 不可静态还原（类实现缺失，需载荷解密后确认点击/定时器/onResume 触发） | 不可静态还原 | **原文**：Erişebilirlik Servisileri Etkinleştirme<br>**译注**：启用无障碍服务（仅确证该文案存在于 strings.xml 资源中，绑定到具体界面需运行期验证） | 预期为引导用户前往系统无障碍设置开启服务；是否提供取消/跳过按钮静态不可确认 | `res/values/strings.xml (name=sAnOHdpofdirBCE)` |
| 3 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS，列表中显示服务项 Google Chrome | 不可静态还原（DEX 中不存在 startActivity 调用点；字符串表无 accessibility_settings 相关常量） | 系统无障碍页 | **原文**：Google Chrome<br>**译注**：系统无障碍服务列表中显示的服务名称为『Google Chrome』，且无用途说明文字 | 要求用户在该系统页面手动将『Google Chrome』开关打开；用户可自行返回，返回后应用如何反应静态不可确认 | `AndroidManifest.xml service com.pagethan10.p068s (BIND_ACCESSIBILITY_SERVICE, label=@string/a)` |
| 4 | 获权后动作 | com.pagethan10.p068s（AccessibilityService 实现，类体缺失）、通知监听服务 com.pagethan10.p014j、设备管理员 receiver com.pagethan10.p080k、短信/开机/屏幕状态 receiver com.pagethan10.p010r | onServiceConnected 等回调不可静态还原；获得无障碍后与 READ_SMS/SEND_SMS/CALL_PHONE/QUERY_ALL_PACKAGES/WRITE_SETTINGS 权限面组合 | 不可静态还原 | 无 | 不可静态确认；是否存在自点确认、阻止撤权、GLOBAL_ACTION_BACK 拦截均待运行期取证 | `AndroidManifest.xml service/receiver 声明集合` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml: @string/a = "Google Chrome"，同时被应用显示名、无障碍服务 label、设备管理员 receiver label 引用，呈现于桌面图标名与系统无障碍服务列表项
- res/values/strings.xml: sAnOHdpofdirBCE = "Erişebilirlik Servisileri Etkinleştirme"（土耳其语启用无障碍服务引导语），具体绑定界面因类实现缺失无法静态定位，预期由加密载荷释放的页面承载
- 无障碍服务 android:description 为空：系统无障碍详情页不呈现任何用途说明，用户只能看到服务名 Google Chrome
- assets/ 下 Vue 打包前端资源（index.*.js/css、emailRegister.*、emailVerify.*、countdown.*）构成 Hybrid 页面承载层，但为构建产物，无可读引导文案
- 清单声明的透明无标题 Activity（Theme.AppCompat.Transparent.NoActionBar）与 Theme.Dialog Activity 为潜在的弹窗/压栈引导载体，实际文本需运行期捕获

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Google Chrome | 谷歌 Chrome | `res/values/strings.xml, key=a（被应用 label 与无障碍服务 label 引用）` | 未知 |
| tr | Erişebilirlik Servisileri Etkinleştirme | 启用无障碍服务 | `res/values/strings.xml, key=sAnOHdpofdirBCE` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：静态不可确认。类实现位于加密载荷，DEX 中无对应 Activity/Service 字节码，无法判定是否存在 onResume 重跳或定时器轮询拉起系统设置页；须运行期 UTG 观测从设置页返回后的界面变化。
- **遮罩叠层 / 高仿系统设置页**：静态不可确认是否存在半透明引导遮罩。可确认的载体条件：清单内多个 Activity 使用 Theme.AppCompat.Transparent.NoActionBar 透明无标题主题，另有一个 Theme.Dialog Activity 与 Theme.NoTitleBar.Fullscreen（excludeFromRecents）Activity，具备叠层与全屏引导的承载能力；assets 中无高仿系统无障碍开关页的 HTML 证据。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未发现 RELATED_TO 受限设置教学或 Session 安装器相关代码；实现类缺失，若有亦在加密载荷内）
- **获权后即时行为与防撤权机制**：静态不可确认。可确认的加固条件为：声明设备管理员 receiver（BIND_DEVICE_ADMIN + DEVICE_ADMIN_ENABLED 过滤器）、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、REQUEST_COMPANION_RUN_IN_BACKGROUND 与 BOOT_COMPLETED/SCREEN_ON/USER_PRESENT 高优先级 receiver，具备反卸载与自启保活基础；是否在无障碍设置页自点确认或用 GLOBAL_ACTION_BACK 阻止撤权需运行期取证。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在两个瞬间拉起：一是应用进程启动后立刻抓取首屏（清单主入口为非 LAUNCHER 的 MAIN+INFO Activity，冷启动即可能直接弹透明引导层）；二是 Hook Context.startActivity / Activity 切换，监测 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的瞬间，并在跳转前 500ms 与返回后 800ms 各抓一帧。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：全部 com.pagethan10.* 实现类不在 classes.dex 中，引导 UI 与无障碍操控逻辑由加密载荷（assets/DDlfO.json、raw/vkicna）经自定义 libMJnWUXJ.so 在运行期释放，纯静态分析无法取得任何引导页文本与跳转代码；另需注意应用显示名与无障碍服务名同为 Google Chrome 且 description 为空，纯静态只看到『一个无说明的 Chrome 无障碍服务』，容易被误判为普通仿冒；运行期 UTG 是本样本唯一可靠的引导链路取证手段。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | 首帧即出现、无标题栏、背景为下层界面透出的弹窗或全屏页，文本含土耳其语『Erişebilirlik Servisileri Etkinleştirme』或其变体 | 直接验证引导是否零步直达、是否有取消/跳过按钮，是判定 TRIG_COLD_START_BLOCK 与 COERCE_NO_SKIP_NON_CANCELABLE 的唯一现场 | 是否存在取消/关闭按钮节点；土耳其语引导文案的完整原文；是否含指向无障碍设置的按钮文案；弹窗是否可被返回键关闭 |
| **系统无障碍服务列表项** | Settings 无障碍页中名为『Google Chrome』的服务条目及其详情页（description 为空） | 确认伪装名在系统界面上的实际呈现，以及是否存在描述为空的异常信号 | 服务显示名是否为 Google Chrome；服务描述是否为空；开关初始状态 |
| **设置页后压栈遮罩页** | 从无障碍设置返回应用后 800ms 内出现的透明 Activity 或悬浮层 | 区分『温和引导』与『遮罩叠压系统设置逼迫点击』，并可验证拒权后的重跳循环 | 返回后是否立即重新跳转设置页；是否出现悬浮窗/遮罩层；遮罩上是否有指向开关位置的指示箭头或高亮 |
| **获权后首屏变化** | 无障碍开关开启后应用界面是否切换为功能页、空白页或直接退至后台 | 判断获权即转入隐蔽运行（无可见 UI）还是继续展示外壳，区分壳应用与功能应用 | 开启后是否立即启动前台服务通知；界面是否变为空白/白屏；是否出现短信或联系人相关界面 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `AndroidManifest.xml service com.pagethan10.p068s (android.permission.BIND_ACCESSIBILITY_SERVICE, label=@string/a)`
- `res/values/strings.xml key=a / key=sAnOHdpofdirBCE`
- `classes.dex（com.pagethan10.* 实现类计数为 0，仅含 com.unity3d.* 与 com.rail.dignity）`
- `assets/DDlfO.json`
- `lib/arm64-v8a/libMJnWUXJ.so`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（要点）

**核心判断：静态可见性不足，引导流程无法静态还原，但伪装与诱导要素已确证。**

1. **解包受阻的原因**：APK 中多个 `assets/*` 条目设置了 ZIP 通用标志位 0x800/0x807/0x808（UTF-8 名称标志），工具误判为"加密需密码"；并且条目路径被篡改出 `classes.dex/xml/...`、`AndroidManifest.xml/raw/vkicna`、`resources.arsc/xml/...` 等畸形路径，导致 apktool 解码的 Manifest XML 结构损坏（`read_manifest` 报 not well-formed）。经手工重打包后，才获得可读的清单与 DEX。

2. **身份伪装已确证**：无障碍服务 [com.pagethan10.p068s](<resource-unit:<local_path> file:all>) 持有 `BIND_ACCESSIBILITY_SERVICE` 与 `android.accessibilityservice.AccessibilityService` action，其 `android:label` 引用 `@string/a`，值为 **`Google Chrome`**，与桌面显示名一致；`android:description` 为空，未作任何权限说明。同一 [strings.xml](<resource-unit:<local_path> file:all>) 内置土耳其语 `sAnOHdpofdirBCE = "Erişebilirlik Servisileri Etkinleştirme"`（"启用无障碍服务"），即引导文案已备好。

3. **引导链路全部落在 DEX 之外**：唯一 [classes.dex](<resource-unit:<local_path> file:all>) 反编译后只有 `com.unity3d.*`（Unity Ads）与 `com.rail.dignity` 共 1427 个类，**`com.pagethan10.*` 实现类计数为 0**，字符串表仅残留一次 `com.pagethan10.oRTfZSIUCvvuDmj`。清单声明的全部 Activity/Service/Receiver 均无对应字节码，故 `ACTION_ACCESSIBILITY_SETTINGS` 跳转点、弹窗/WebView 载体、拒权重跳逻辑**均不可静态定位**。

4. **二阶段载荷定位**：[DDlfO.json](<resource-unit:<local_path> file:all>)（1,060,765 B）与 `AndroidManifest.xml/raw/vkicna`（1,000,028 B）均为高熵非明文，四 ABI 携带 `libMJnWUXJ.so`（17–22 KB，自定义小型壳/解密器规模）。另有完整 Vue 打包前端资源（`index.*.js/css`、`emailRegister`、`emailVerify`、`countdown`、`apmplus.hybrid.cn.js`），指向 Hybrid 页面承载层——但 HTML 文本本身也是打包产物而非可读引导页。

5. **辅助伪装手法**：启动 Activity 同时注册 `android.app.action.ANGLE_FOR_ANDROID`、`android.service.quicksettings.action.QS_TILE_PREFERENCES`、`com.android.settings.action.IA_SETTINGS`（伪造"系统设置项"身份），主入口使用 `MAIN` + `category.INFO` 而非 `LAUNCHER`；多数 Activity 用 `Theme.AppCompat.Transparent.NoActionBar`（透明无标题），符合"点开即压半透明引导层"的载体特征，但具体呈现内容需运行期取证。

6. **已登记风险**：R-001（high / malware_trojan）——伪装 Google Chrome 的无障碍服务与诱导文案，实现藏于加密载荷。

**未决边界**：本轮严格控制在效率上限内，未对 `libMJnWUXJ.so` 做 angr 函数级还原、未解密 `DDlfO.json`/`vkicna`，因此"第几步弹出什么文案、是否 onResume 死循环重跳、是否获权后 `GLOBAL_ACTION_BACK` 阻止撤权"等**运行期 UTG 细节均无静态证据**，仅能给出取证指引（见下）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "清单与资源层完整可见：无障碍服务 com.pagethan10.p068s、label=@string/a(Google Chrome)、土耳其语引导文案、全部高危权限与组件声明均可读。但所有 com.pagethan10.* 实现类在 classes.dex 中缺失（该类计数为 0，DEX 仅含 Unity Ads 与 com.rail.dignity），真实引导流程与无障碍操作逻辑位于随包高熵载荷 assets/DDlfO.json（1,060,765B）、AndroidManifest.xml/raw/vkicna（1,000,028B）与自定义原生库 libMJnWUXJ.so 中，须运行期由 SO 解密释放；assets 下另有 Vue 打包前端资源作为 Hybrid 承载层，但为构建产物而非可读引导页。",
  "summary_one_liner": "以 Google Chrome 名义注册无障碍服务并内置土耳其语『启用无障碍服务』文案，采用透明无标题 Activity + 伪造系统设置项身份，实际引导与操控代码全部封装在加密载荷与自定义 SO 中，静态无法还原具体弹窗与跳转序列。",
  "disguise_identity": {
    "app_display_name": "Google Chrome",
    "claimed_brand_or_persona": "Google Chrome（谷歌官方浏览器）",
    "a11y_service_label": "Google Chrome",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:description 留空，系统设置页不展示任何权限用途说明；应用显示名、无障碍服务标签、设备管理员 receiver 标签统一复用同一字符串 @string/a 指向 Google Chrome；启动 Activity 额外注册 com.android.settings.action.IA_SETTINGS 与 android.app.action.ANGLE_FOR_ANDROID、QS_TILE_PREFERENCES，冒充系统设置项/系统组件身份；主入口使用 MAIN + category.INFO 而非 LAUNCHER 以弱化桌面图标存在感；多数 Activity 采用 Theme.AppCompat.Transparent.NoActionBar 透明无标题主题便于叠层；APK 内条目路径被改写成 classes.dex/xml/...、AndroidManifest.xml/raw/vkicna 等畸形结构并对 ZIP 标志位做手脚，使常规解包工具解析失败。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.pagethan10 主 Activity（清单中 label=@string/a 的启动项，声明 MAIN + category.INFO，并叠加 ANGLE_FOR_ANDROID / QS_TILE_PREFERENCES / IA_SETTINGS 过滤器）",
      "trigger_event": "系统或外部 intent 启动主 Activity；类实现体不在 classes.dex 中，具体 onCreate 逻辑需解密载荷后确认",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Google Chrome",
      "shown_text_zh": "谷歌 Chrome（应用与界面标题显示名）",
      "user_action_requested": "无明确要求；静态不可确认首屏是否直接弹出引导或先呈现空壳界面",
      "code_anchor": "AndroidManifest.xml 启动 activity 节点（label=@string/a）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "清单声明的多个 Theme.AppCompat.Transparent.NoActionBar Activity（com.pagethan10.p054i / p084c / p020f 等）与 Theme.Dialog Activity（com.pagethan10.p024i），以及 assets 下 Vue 打包前端（index.*.js/css、emailRegister、emailVerify）",
      "trigger_event": "不可静态还原（类实现缺失，需载荷解密后确认点击/定时器/onResume 触发）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Erişebilirlik Servisileri Etkinleştirme",
      "shown_text_zh": "启用无障碍服务（仅确证该文案存在于 strings.xml 资源中，绑定到具体界面需运行期验证）",
      "user_action_requested": "预期为引导用户前往系统无障碍设置开启服务；是否提供取消/跳过按钮静态不可确认",
      "code_anchor": "res/values/strings.xml (name=sAnOHdpofdirBCE)"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS，列表中显示服务项 Google Chrome",
      "trigger_event": "不可静态还原（DEX 中不存在 startActivity 调用点；字符串表无 accessibility_settings 相关常量）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Chrome",
      "shown_text_zh": "系统无障碍服务列表中显示的服务名称为『Google Chrome』，且无用途说明文字",
      "user_action_requested": "要求用户在该系统页面手动将『Google Chrome』开关打开；用户可自行返回，返回后应用如何反应静态不可确认",
      "code_anchor": "AndroidManifest.xml service com.pagethan10.p068s (BIND_ACCESSIBILITY_SERVICE, label=@string/a)"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.pagethan10.p068s（AccessibilityService 实现，类体缺失）、通知监听服务 com.pagethan10.p014j、设备管理员 receiver com.pagethan10.p080k、短信/开机/屏幕状态 receiver com.pagethan10.p010r",
      "trigger_event": "onServiceConnected 等回调不可静态还原；获得无障碍后与 READ_SMS/SEND_SMS/CALL_PHONE/QUERY_ALL_PACKAGES/WRITE_SETTINGS 权限面组合",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（静态不可见任何获权后的界面文案）",
      "user_action_requested": "不可静态确认；是否存在自点确认、阻止撤权、GLOBAL_ACTION_BACK 拦截均待运行期取证",
      "code_anchor": "AndroidManifest.xml service/receiver 声明集合"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml: @string/a = \"Google Chrome\"，同时被应用显示名、无障碍服务 label、设备管理员 receiver label 引用，呈现于桌面图标名与系统无障碍服务列表项",
    "res/values/strings.xml: sAnOHdpofdirBCE = \"Erişebilirlik Servisileri Etkinleştirme\"（土耳其语启用无障碍服务引导语），具体绑定界面因类实现缺失无法静态定位，预期由加密载荷释放的页面承载",
    "无障碍服务 android:description 为空：系统无障碍详情页不呈现任何用途说明，用户只能看到服务名 Google Chrome",
    "assets/ 下 Vue 打包前端资源（index.*.js/css、emailRegister.*、emailVerify.*、countdown.*）构成 Hybrid 页面承载层，但为构建产物，无可读引导文案",
    "清单声明的透明无标题 Activity（Theme.AppCompat.Transparent.NoActionBar）与 Theme.Dialog Activity 为潜在的弹窗/压栈引导载体，实际文本需运行期捕获"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Google Chrome",
      "text_zh": "谷歌 Chrome",
      "source_location": "res/values/strings.xml, key=a（被应用 label 与无障碍服务 label 引用）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "tr",
      "text_verbatim": "Erişebilirlik Servisileri Etkinleştirme",
      "text_zh": "启用无障碍服务",
      "source_location": "res/values/strings.xml, key=sAnOHdpofdirBCE",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "静态不可确认。类实现位于加密载荷，DEX 中无对应 Activity/Service 字节码，无法判定是否存在 onResume 重跳或定时器轮询拉起系统设置页；须运行期 UTG 观测从设置页返回后的界面变化。",
    "overlay_or_fake_settings": "静态不可确认是否存在半透明引导遮罩。可确认的载体条件：清单内多个 Activity 使用 Theme.AppCompat.Transparent.NoActionBar 透明无标题主题，另有一个 Theme.Dialog Activity 与 Theme.NoTitleBar.Fullscreen（excludeFromRecents）Activity，具备叠层与全屏引导的承载能力；assets 中无高仿系统无障碍开关页的 HTML 证据。",
    "restricted_settings_13plus_coaching": "无（未发现 RELATED_TO 受限设置教学或 Session 安装器相关代码；实现类缺失，若有亦在加密载荷内）",
    "post_grant_anti_removal": "静态不可确认。可确认的加固条件为：声明设备管理员 receiver（BIND_DEVICE_ADMIN + DEVICE_ADMIN_ENABLED 过滤器）、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、REQUEST_COMPANION_RUN_IN_BACKGROUND 与 BOOT_COMPLETED/SCREEN_ON/USER_PRESENT 高优先级 receiver，具备反卸载与自启保活基础；是否在无障碍设置页自点确认或用 GLOBAL_ACTION_BACK 阻止撤权需运行期取证。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在两个瞬间拉起：一是应用进程启动后立刻抓取首屏（清单主入口为非 LAUNCHER 的 MAIN+INFO Activity，冷启动即可能直接弹透明引导层）；二是 Hook Context.startActivity / Activity 切换，监测 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的瞬间，并在跳转前 500ms 与返回后 800ms 各抓一帧。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "首帧即出现、无标题栏、背景为下层界面透出的弹窗或全屏页，文本含土耳其语『Erişebilirlik Servisileri Etkinleştirme』或其变体",
        "why_most_useful": "直接验证引导是否零步直达、是否有取消/跳过按钮，是判定 TRIG_COLD_START_BLOCK 与 COERCE_NO_SKIP_NON_CANCELABLE 的唯一现场",
        "observable_utg_signals": ["是否存在取消/关闭按钮节点", "土耳其语引导文案的完整原文", "是否含指向无障碍设置的按钮文案", "弹窗是否可被返回键关闭"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中名为『Google Chrome』的服务条目及其详情页（description 为空）",
        "why_most_useful": "确认伪装名在系统界面上的实际呈现，以及是否存在描述为空的异常信号",
        "observable_utg_signals": ["服务显示名是否为 Google Chrome", "服务描述是否为空", "开关初始状态"]
      },
      {
        "page_role": "设置页后压栈遮罩页",
        "page_identifier": "从无障碍设置返回应用后 800ms 内出现的透明 Activity 或悬浮层",
        "why_most_useful": "区分『温和引导』与『遮罩叠压系统设置逼迫点击』，并可验证拒权后的重跳循环",
        "observable_utg_signals": ["返回后是否立即重新跳转设置页", "是否出现悬浮窗/遮罩层", "遮罩上是否有指向开关位置的指示箭头或高亮"]
      },
      {
        "page_role": "获权后首屏变化",
        "page_identifier": "无障碍开关开启后应用界面是否切换为功能页、空白页或直接退至后台",
        "why_most_useful": "判断获权即转入隐蔽运行（无可见 UI）还是继续展示外壳，区分壳应用与功能应用",
        "observable_utg_signals": ["开启后是否立即启动前台服务通知", "界面是否变为空白/白屏", "是否出现短信或联系人相关界面"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：全部 com.pagethan10.* 实现类不在 classes.dex 中，引导 UI 与无障碍操控逻辑由加密载荷（assets/DDlfO.json、raw/vkicna）经自定义 libMJnWUXJ.so 在运行期释放，纯静态分析无法取得任何引导页文本与跳转代码；另需注意应用显示名与无障碍服务名同为 Google Chrome 且 description 为空，纯静态只看到『一个无说明的 Chrome 无障碍服务』，容易被误判为普通仿冒；运行期 UTG 是本样本唯一可靠的引导链路取证手段。"
  },
  "behavior_pattern_tags": [
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "AndroidManifest.xml service com.pagethan10.p068s (android.permission.BIND_ACCESSIBILITY_SERVICE, label=@string/a)",
    "res/values/strings.xml key=a / key=sAnOHdpofdirBCE",
    "classes.dex（com.pagethan10.* 实现类计数为 0，仅含 com.unity3d.* 与 com.rail.dignity）",
    "assets/DDlfO.json",
    "lib/arm64-v8a/libMJnWUXJ.so"
  ]
}
```

</details>

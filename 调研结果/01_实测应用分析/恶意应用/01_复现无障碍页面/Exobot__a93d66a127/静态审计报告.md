# MB_152__a93d66a127｜Exobot — BAWAG PSK Security

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：155.0s

## 1. 一句话核心结论

- **核心申请方式**：伪装为 BAWAG PSK Security 银行的 Exobot 系木马，壳 Application 在 attachBaseContext 中经 native 解密内嵌载荷后动态注入无障碍服务，引导文案与跳转逻辑全部藏于加密载荷，仅无障碍列表暴露一句 'Service must be enabled.'。
- **静态可见性说明**：classes.dex 仅为壳（33 个类：R$*、Application bgYohrrP、空壳组件）。Manifest 声明的无障碍服务 com.bypressfo.p050a、启动页 p076r、全屏透明 Activity p010t/p093v、Dialog 主题 p061c 均不在 DEX 中，真实逻辑位于 res/raw/wqhehnzhagnblw（163340 字节，熵 7.9989，魔数 87aec54e）的加密载荷，由 libURisRK.so 的 JNI oCetXE 解密后动态加载。因此无障碍引导弹窗、ACTION_ACCESSIBILITY_SETTINGS 跳转、悬浮窗遮罩等运行期流程不可静态还原；仅 Manifest、无障碍 XML 配置与 strings.xml 两句文案完整可见。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a93d66a127091d11090f544514d7e677c24db69d361008e60fffc5200331a1fe` |
| 包名 / 年份 | `com.bypressfo` / 2022 |
| 家族 / 品类 | **Exobot**（同池样本数：3） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | BAWAG PSK Security |
| 引导页宣称品牌/身份 | BAWAG PSK（奥地利 BAWAG P.S.K. 银行）官方安全组件 |
| 系统无障碍列表服务名 | BAWAG PSK Security |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名为随机串 com.bypressfo 与品牌无关联；Manifest 批量声明 com.bypressfo.vdcityomnnlsiko/ugbbrjbodhptytm/wdcdmvvyoot 等随机名组件用于填充清单；真实组件类不在 DEX 中（运行期注入）；大量 excludeFromRecents+noHistory+Theme.AppCompat.Transparent.NoActionBar 的透明 Activity（p017y、p078u、p088f）及 Theme.NoTitleBar.Fullscreen 的 p010t/p093v，便于无感弹出；无障碍描述压缩为一句 'Service must be enabled.' 以弱化系统警告的观感；targetSdk=28 规避 Android 12+ isAccessibilityTool 声明要求。 |
| 无障碍服务类名 | `com.bypressfo.p050a` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Service must be enabled. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.bypressfo.bgYohrrP（Application）→ com.bypressfo.p076r（LAUNCHER Activity） | 进程创建时 attachBaseContext() → 反射调用 native oCetXE(Context)；随后启动 p076r | 不可静态还原 | **原文**：BAWAG PSK Security<br>**译注**：应用/页面标识显示为“BAWAG PSK Security” | 打开应用（点击桌面图标，图标名为 BAWAG PSK Security） | `com.bypressfo.bgYohrrP.attachBaseContext / com.bypressfo.bgYohrrP.<clinit> / AndroidManifest.xml activity com.bypressfo.p076r` |
| 2 | 引导说明页 | p076r 或 p010t/p093v（Theme.NoTitleBar.Fullscreen 全屏页）、p061c（Theme.Dialog 弹窗页）——具体承载页由加密载荷决定 | 启动页 onCreate/onResume 后加载解密载荷并展示引导（静态不可见） | 不可静态还原 | **原文**：无（classes.dex 与 res/ 中不存在除 'Service must be enabled.' 与 'BAWAG PSK Security' 之外的应用自有文案）<br>**译注**：静态资源中无引导说明文案，文案应由加密载荷内嵌的 HTML/字符串提供 | 不可静态还原（无法确认是否存在取消/跳过按钮） | `com.bypressfo.p076r / com.bypressfo.p010t / com.bypressfo.p093v / com.bypressfo.p061c（Manifest 声明，类体缺失）` |
| 3 | 跳受限设置 | 系统“使用情况访问权限”“悬浮窗/显示在其他应用上层”“修改系统设置”页（PACKAGE_USAGE_STATS / SYSTEM_ALERT_WINDOW / WRITE_SETTINGS 均已申请） | 不可静态还原；DEX 内检索 ACTION_MANAGE_OVERLAY / APPLICATION_DETAILS_SETTINGS 无命中，跳转实现位于加密载荷 | 不可静态还原 | 无 | 不可静态还原 | `AndroidManifest.xml uses-permission SYSTEM_ALERT_WINDOW / PACKAGE_USAGE_STATS / WRITE_SETTINGS` |
| 4 | 跳无障碍设置 | 系统无障碍服务列表中的 “BAWAG PSK Security” 条目（Settings.ACTION_ACCESSIBILITY_SETTINGS 目标页） | 不可静态还原；ACTION_ACCESSIBILITY_SETTINGS 字符串不在 classes.dex，跳转代码在加密载荷中 | 系统无障碍页 | **原文**：BAWAG PSK Security / Service must be enabled.<br>**译注**：条目名“BAWAG PSK Security”；服务说明“服务必须被启用。” | 在系统无障碍列表中点开该服务并打开开关（用户需自行确认系统风险提示） | `res/xml/khxzxermtqafd.xml（android:description=@string/IasapxKu）；res/values/strings.xml#L3-L4；Manifest service com.bypressfo.p050a` |
| 5 | 遮罩叠层指引 | 疑为悬浮窗/透明 Activity 叠层（已具备 SYSTEM_ALERT_WINDOW 权限与多个透明 noHistory Activity） | 不可静态还原 | 悬浮窗Overlay | 无 | 不可静态还原 | `AndroidManifest.xml activity com.bypressfo.p017y / p078u（excludeFromRecents+noHistory+Transparent）` |
| 6 | 获权后动作 | com.bypressfo.p050a（无障碍服务，typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows）；SMS 接收/发送、通知监听 p057a、DeviceAdmin p058z | 系统绑定无障碍服务后 onServiceConnected（实现位于加密载荷，不可静态还原） | 不可静态还原 | 无 | 无需用户操作（服务后台运行） | `res/xml/khxzxermtqafd.xml；Manifest service com.bypressfo.p050a / com.bypressfo.p057a / receiver com.bypressfo.p058z` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统设置 → 无障碍 → 已下载/已安装的服务列表：条目名 “BAWAG PSK Security”（service android:label=@string/a，与桌面名一致）
- 同一系统无障碍列表条目的服务说明副标题：“Service must be enabled.”（android:description=@string/IasapxKu，仅此一句，无任何功能说明）
- 桌面图标名：“BAWAG PSK Security”（application android:label=@string/a）
- 应用内引导页/弹窗/WebView 文案：静态不可见，应位于 res/raw/wqhehnzhagnblw 加密载荷内（strings.xml 中无任何引导类文案，仅两条应用自有字符串）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Service must be enabled. | 服务必须被启用。 | `res/values/strings.xml key=IasapxKu（被 res/xml/khxzxermtqafd.xml 的 android:description 引用）` | 教唆忽视警告 |
| en | BAWAG PSK Security | BAWAG PSK 安全（组件） | `res/values/strings.xml key=a（application/android:label、无障碍 service android:label、DeviceAdmin receiver android:label 共用）` | 假反诈安全 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：跳转与重试逻辑位于加密载荷 res/raw/wqhehnzhagnblw（libURisRK.so 解密后动态加载），classes.dex 中无 ACTION_ACCESSIBILITY_SETTINGS 引用，无法确认是否存在 onResume 死循环重跳或定时拉起。
- **遮罩叠层 / 高仿系统设置页**：不可静态确认具体实现；但已具备 SYSTEM_ALERT_WINDOW 与 ACTION_MANAGE_OVERLAY_PERMISSION 声明、多个 excludeFromRecents+noHistory 的 Theme.AppCompat.Transparent.NoActionBar 透明 Activity（p017y、p078u、p088f），以及 fullSensor+Theme.NoTitleBar.Fullscreen 的全屏页（p010t、p093v），具备设置页压栈遮罩/伪造开关页的结构条件。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdk=28，Manifest 与静态资源中无“应用详情→右上角菜单→允许受限设置”相关文案，也未使用 Session 安装器绕过；但不排除该文案存在于加密载荷内）
- **获权后即时行为与防撤权机制**：不可静态确认。已确认具备的对抗能力：DeviceAdmin receiver com.bypressfo.p058z（res/xml/yrraw）、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED/QUICKBOOT_POWERON/USER_PRESENT/SCREEN_ON 高优先级 receiver p038l、REQUEST_DELETE_PACKAGES、USES_POLICY_FORCE_LOCK；是否使用 GLOBAL_ACTION_BACK/HOME 阻止撤权因载荷加密无法核实。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到前台 Activity 切换至 Settings$AccessibilitySettings / Settings$AccessibilityDetailsSettings，或首个非启动页 Activity（p010t、p093v、p061c、p017y、p078u）在冷启动 3 秒内被拉起时立即抓取；另可在 oCetXE 解密完成后（进程启动即触发）开始连续截屏。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：全部引导文案与跳转逻辑位于 res/raw/wqhehnzhagnblw（163KB 高熵加密载荷，熵 7.9989），由 libURisRK.so 的 JNI oCetXE 在 attachBaseContext 解密后动态加载，静态侧仅能看到 Manifest 与两条字符串。若设备上解密失败（如依赖签名/环境校验），应用可能表现为空白页，此时 UTG 无文本可采；静态加壳本身不阻挡运行期 UTG 截屏，需在解密成功、p076r 之后的前台窗口出现时立即抓取。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导/说明页（真身 UI）** | com.bypressfo.p076r 之后出现的 p010t / p093v 全屏页，或 p061c（Theme.Dialog）弹窗 | 该页文案完全不在静态资源中，只有运行期才能看到实际诱导话术与是否存在取消按钮 | 页面文本节点全文（识别假银行安全/假更新话术）；是否存在“取消/稍后/跳过”按钮节点；是否 WebView 容器（class=android.webkit.WebView）及加载 URL |
| **跳转前教学页 / 设置页后压栈遮罩页** | p017y、p078u、p088f 等透明 noHistory Activity，或 TYPE_APPLICATION_OVERLAY 悬浮窗（系统权限 SYSTEM_ALERT_WINDOW 已授予时） | 区分“合规说明”与“覆盖系统界面的高仿引导”，是判定 COERCE_OVERLAY_STACK_ON_SETTINGS 的唯一直接证据 | 叠层窗口 package=com.bypressfo 且覆盖 Settings 包；叠层内是否绘制高仿无障碍开关控件；叠层内箭头/手指图标指向的真实系统开关位置 |
| **系统无障碍服务列表项** | Settings 无障碍列表中 label=BAWAG PSK Security、summary=Service must be enabled. 的条目 | 确认伪装名在系统级暴露，且描述被压缩为一句无信息量文案，用于固定 ID_SYSTEM_OR_BRAND_IMPERSONATION 证据 | 条目标题文本 'BAWAG PSK Security'；条目副标题 'Service must be enabled.'；同列表是否存在重复/多别名条目 |
| **获权后返回应用页** | 获权瞬间从 Settings 返回后的前台界面（可能是空白透明页或直接回桌面） | 判断获权后是否立即静默执行（无任何 UI 反馈）与是否触发自撤权对抗 | 是否出现全局返回/Home 自动操作；是否出现无障碍自点击（节点 click 无用户输入）；前台是否变空（无 UI 直接后台驻留） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.bypressfo.bgYohrrP.attachBaseContext`
- `com.bypressfo.bgYohrrP.oCetXE（native，libURisRK.so）`
- `res/xml/khxzxermtqafd.xml`
- `res/raw/wqhehnzhagnblw`
- `res/values/strings.xml#L3-L4`
- `com.bypressfo.p050a（无障碍服务，类体缺失于 classes.dex）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（代码级定向核验）

**核心事实：该样本的第二阶段载荷以整体加密方式内嵌，所有与无障碍引导相关的代码都位于加密载荷中；静态可见的只有壳 Application、Manifest 声明和资源。**

1. **壳层入口**：[bgYohrrP.attachBaseContext()](<resource-unit:#1.dex1 code:com.bypressfo.bgYohrrP#attachBaseContext>) 通过反射调用 `native oCetXE(Context)`，`<clinit>` 加载 [libURisRK.so](<resource-unit:#1.so1 byte:0x12d0+0x1000>)。`classes.dex` 只有 33 个类，全部是 `R$*`、Application 和空壳组件（仅有 `onCreate/onReceive/onStartCommand`）。
2. **加密载荷已定位**：[res/raw/wqhehnzhagnblw](<resource-unit:#1 file:res/raw/wqhehnzhagnblw>) 为 163,340 字节、熵 7.9989、魔数 `87ae c54e`（非 zip/dex），与 .so 中导出的 `EBYTdDoXtFunc::McTzBrEYdi / epRupIwvTcjLZboE / anggYlkUKBff` + `fopen/fwrite/strstr` 组合高度吻合“解密 → 落盘 → 动态加载”的链路。
3. **Manifest 声明的真实组件在 classes.dex 中全部缺失**：无障碍服务 [com.bypressfo.p050a](<resource-unit:#1 manifest:components>)、启动 Activity `p076r`、全屏透明 Activity `p010t/p093v`、`Theme.Dialog` 的 `p061c`、`singleTask` 的 `p050e` 均未出现在 DEX 中，确认由运行期解密注入。
4. **无障碍配置本身已具备高危能力**：[res/xml/khxzxermtqafd.xml](<resource-unit:#1 file:res/xml/khxzxermtqafd.xml>) 声明 `typeAllMask`、`flagRetrieveInteractiveWindows`、`flagReportViewIds`、`canRetrieveWindowContent="true"`，且 `android:description="@string/IasapxKu"` 仅有一句 `Service must be enabled.`（[strings.xml](<resource-unit:#1 file:res/values/strings.xml#L3-L4>)）。
5. **身份伪装成立**：桌面名、无障碍服务 label、DeviceAdmin receiver label 统一为 `BAWAG PSK Security`（奥地利 BAWAG PSK 银行），但包名为随机串 `com.bypressfo`，`minSdk=21 / targetSdk=28`，`usesCleartextTraffic=true`，与真实银行 App 完全不符。
6. **UTG 关键盲区**：`classes.dex` 中检索 `ACTION_ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`ACTION_MANAGE_OVERLAY` 均无命中，引导弹窗文案除上面两句外不存在于任何静态资源；**跳转逻辑与引导页面文本位于加密载荷内，无法静态还原**。因此 `static_visibility="packed_or_encrypted"`，下文流程中未证实的环节如实标注为不可静态还原。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "classes.dex 仅为壳（33 个类：R$*、Application bgYohrrP、空壳组件）。Manifest 声明的无障碍服务 com.bypressfo.p050a、启动页 p076r、全屏透明 Activity p010t/p093v、Dialog 主题 p061c 均不在 DEX 中，真实逻辑位于 res/raw/wqhehnzhagnblw（163340 字节，熵 7.9989，魔数 87aec54e）的加密载荷，由 libURisRK.so 的 JNI oCetXE 解密后动态加载。因此无障碍引导弹窗、ACTION_ACCESSIBILITY_SETTINGS 跳转、悬浮窗遮罩等运行期流程不可静态还原；仅 Manifest、无障碍 XML 配置与 strings.xml 两句文案完整可见。",
  "summary_one_liner": "伪装为 BAWAG PSK Security 银行的 Exobot 系木马，壳 Application 在 attachBaseContext 中经 native 解密内嵌载荷后动态注入无障碍服务，引导文案与跳转逻辑全部藏于加密载荷，仅无障碍列表暴露一句 'Service must be enabled.'。",
  "disguise_identity": {
    "app_display_name": "BAWAG PSK Security",
    "claimed_brand_or_persona": "BAWAG PSK（奥地利 BAWAG P.S.K. 银行）官方安全组件",
    "a11y_service_label": "BAWAG PSK Security",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名为随机串 com.bypressfo 与品牌无关联；Manifest 批量声明 com.bypressfo.vdcityomnnlsiko/ugbbrjbodhptytm/wdcdmvvyoot 等随机名组件用于填充清单；真实组件类不在 DEX 中（运行期注入）；大量 excludeFromRecents+noHistory+Theme.AppCompat.Transparent.NoActionBar 的透明 Activity（p017y、p078u、p088f）及 Theme.NoTitleBar.Fullscreen 的 p010t/p093v，便于无感弹出；无障碍描述压缩为一句 'Service must be enabled.' 以弱化系统警告的观感；targetSdk=28 规避 Android 12+ isAccessibilityTool 声明要求。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.bypressfo.bgYohrrP（Application）→ com.bypressfo.p076r（LAUNCHER Activity）",
      "trigger_event": "进程创建时 attachBaseContext() → 反射调用 native oCetXE(Context)；随后启动 p076r",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "BAWAG PSK Security",
      "shown_text_zh": "应用/页面标识显示为“BAWAG PSK Security”",
      "user_action_requested": "打开应用（点击桌面图标，图标名为 BAWAG PSK Security）",
      "code_anchor": "com.bypressfo.bgYohrrP.attachBaseContext / com.bypressfo.bgYohrrP.<clinit> / AndroidManifest.xml activity com.bypressfo.p076r"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "p076r 或 p010t/p093v（Theme.NoTitleBar.Fullscreen 全屏页）、p061c（Theme.Dialog 弹窗页）——具体承载页由加密载荷决定",
      "trigger_event": "启动页 onCreate/onResume 后加载解密载荷并展示引导（静态不可见）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（classes.dex 与 res/ 中不存在除 'Service must be enabled.' 与 'BAWAG PSK Security' 之外的应用自有文案）",
      "shown_text_zh": "静态资源中无引导说明文案，文案应由加密载荷内嵌的 HTML/字符串提供",
      "user_action_requested": "不可静态还原（无法确认是否存在取消/跳过按钮）",
      "code_anchor": "com.bypressfo.p076r / com.bypressfo.p010t / com.bypressfo.p093v / com.bypressfo.p061c（Manifest 声明，类体缺失）"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统“使用情况访问权限”“悬浮窗/显示在其他应用上层”“修改系统设置”页（PACKAGE_USAGE_STATS / SYSTEM_ALERT_WINDOW / WRITE_SETTINGS 均已申请）",
      "trigger_event": "不可静态还原；DEX 内检索 ACTION_MANAGE_OVERLAY / APPLICATION_DETAILS_SETTINGS 无命中，跳转实现位于加密载荷",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无静态可见文案",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml uses-permission SYSTEM_ALERT_WINDOW / PACKAGE_USAGE_STATS / WRITE_SETTINGS"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍服务列表中的 “BAWAG PSK Security” 条目（Settings.ACTION_ACCESSIBILITY_SETTINGS 目标页）",
      "trigger_event": "不可静态还原；ACTION_ACCESSIBILITY_SETTINGS 字符串不在 classes.dex，跳转代码在加密载荷中",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "BAWAG PSK Security / Service must be enabled.",
      "shown_text_zh": "条目名“BAWAG PSK Security”；服务说明“服务必须被启用。”",
      "user_action_requested": "在系统无障碍列表中点开该服务并打开开关（用户需自行确认系统风险提示）",
      "code_anchor": "res/xml/khxzxermtqafd.xml（android:description=@string/IasapxKu）；res/values/strings.xml#L3-L4；Manifest service com.bypressfo.p050a"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "疑为悬浮窗/透明 Activity 叠层（已具备 SYSTEM_ALERT_WINDOW 权限与多个透明 noHistory Activity）",
      "trigger_event": "不可静态还原",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静态资源中无遮罩指引文案；实现位置在加密载荷内",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml activity com.bypressfo.p017y / p078u（excludeFromRecents+noHistory+Transparent）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.bypressfo.p050a（无障碍服务，typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows）；SMS 接收/发送、通知监听 p057a、DeviceAdmin p058z",
      "trigger_event": "系统绑定无障碍服务后 onServiceConnected（实现位于加密载荷，不可静态还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后行为不可静态还原；Manifest 表明同时具备读发短信、通知监听、设备管理员、忽略电池优化等能力",
      "user_action_requested": "无需用户操作（服务后台运行）",
      "code_anchor": "res/xml/khxzxermtqafd.xml；Manifest service com.bypressfo.p050a / com.bypressfo.p057a / receiver com.bypressfo.p058z"
    }
  ],
  "text_presentation_locations": [
    "系统设置 → 无障碍 → 已下载/已安装的服务列表：条目名 “BAWAG PSK Security”（service android:label=@string/a，与桌面名一致）",
    "同一系统无障碍列表条目的服务说明副标题：“Service must be enabled.”（android:description=@string/IasapxKu，仅此一句，无任何功能说明）",
    "桌面图标名：“BAWAG PSK Security”（application android:label=@string/a）",
    "应用内引导页/弹窗/WebView 文案：静态不可见，应位于 res/raw/wqhehnzhagnblw 加密载荷内（strings.xml 中无任何引导类文案，仅两条应用自有字符串）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Service must be enabled.",
      "text_zh": "服务必须被启用。",
      "source_location": "res/values/strings.xml key=IasapxKu（被 res/xml/khxzxermtqafd.xml 的 android:description 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "BAWAG PSK Security",
      "text_zh": "BAWAG PSK 安全（组件）",
      "source_location": "res/values/strings.xml key=a（application/android:label、无障碍 service android:label、DeviceAdmin receiver android:label 共用）",
      "rhetorical_frame": "假反诈安全"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：跳转与重试逻辑位于加密载荷 res/raw/wqhehnzhagnblw（libURisRK.so 解密后动态加载），classes.dex 中无 ACTION_ACCESSIBILITY_SETTINGS 引用，无法确认是否存在 onResume 死循环重跳或定时拉起。",
    "overlay_or_fake_settings": "不可静态确认具体实现；但已具备 SYSTEM_ALERT_WINDOW 与 ACTION_MANAGE_OVERLAY_PERMISSION 声明、多个 excludeFromRecents+noHistory 的 Theme.AppCompat.Transparent.NoActionBar 透明 Activity（p017y、p078u、p088f），以及 fullSensor+Theme.NoTitleBar.Fullscreen 的全屏页（p010t、p093v），具备设置页压栈遮罩/伪造开关页的结构条件。",
    "restricted_settings_13plus_coaching": "无（targetSdk=28，Manifest 与静态资源中无“应用详情→右上角菜单→允许受限设置”相关文案，也未使用 Session 安装器绕过；但不排除该文案存在于加密载荷内）",
    "post_grant_anti_removal": "不可静态确认。已确认具备的对抗能力：DeviceAdmin receiver com.bypressfo.p058z（res/xml/yrraw）、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED/QUICKBOOT_POWERON/USER_PRESENT/SCREEN_ON 高优先级 receiver p038l、REQUEST_DELETE_PACKAGES、USES_POLICY_FORCE_LOCK；是否使用 GLOBAL_ACTION_BACK/HOME 阻止撤权因载荷加密无法核实。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到前台 Activity 切换至 Settings$AccessibilitySettings / Settings$AccessibilityDetailsSettings，或首个非启动页 Activity（p010t、p093v、p061c、p017y、p078u）在冷启动 3 秒内被拉起时立即抓取；另可在 oCetXE 解密完成后（进程启动即触发）开始连续截屏。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导/说明页（真身 UI）",
        "page_identifier": "com.bypressfo.p076r 之后出现的 p010t / p093v 全屏页，或 p061c（Theme.Dialog）弹窗",
        "why_most_useful": "该页文案完全不在静态资源中，只有运行期才能看到实际诱导话术与是否存在取消按钮",
        "observable_utg_signals": ["页面文本节点全文（识别假银行安全/假更新话术）", "是否存在“取消/稍后/跳过”按钮节点", "是否 WebView 容器（class=android.webkit.WebView）及加载 URL"]
      },
      {
        "page_role": "跳转前教学页 / 设置页后压栈遮罩页",
        "page_identifier": "p017y、p078u、p088f 等透明 noHistory Activity，或 TYPE_APPLICATION_OVERLAY 悬浮窗（系统权限 SYSTEM_ALERT_WINDOW 已授予时）",
        "why_most_useful": "区分“合规说明”与“覆盖系统界面的高仿引导”，是判定 COERCE_OVERLAY_STACK_ON_SETTINGS 的唯一直接证据",
        "observable_utg_signals": ["叠层窗口 package=com.bypressfo 且覆盖 Settings 包", "叠层内是否绘制高仿无障碍开关控件", "叠层内箭头/手指图标指向的真实系统开关位置"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中 label=BAWAG PSK Security、summary=Service must be enabled. 的条目",
        "why_most_useful": "确认伪装名在系统级暴露，且描述被压缩为一句无信息量文案，用于固定 ID_SYSTEM_OR_BRAND_IMPERSONATION 证据",
        "observable_utg_signals": ["条目标题文本 'BAWAG PSK Security'", "条目副标题 'Service must be enabled.'", "同列表是否存在重复/多别名条目"]
      },
      {
        "page_role": "获权后返回应用页",
        "page_identifier": "获权瞬间从 Settings 返回后的前台界面（可能是空白透明页或直接回桌面）",
        "why_most_useful": "判断获权后是否立即静默执行（无任何 UI 反馈）与是否触发自撤权对抗",
        "observable_utg_signals": ["是否出现全局返回/Home 自动操作", "是否出现无障碍自点击（节点 click 无用户输入）", "前台是否变空（无 UI 直接后台驻留）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：全部引导文案与跳转逻辑位于 res/raw/wqhehnzhagnblw（163KB 高熵加密载荷，熵 7.9989），由 libURisRK.so 的 JNI oCetXE 在 attachBaseContext 解密后动态加载，静态侧仅能看到 Manifest 与两条字符串。若设备上解密失败（如依赖签名/环境校验），应用可能表现为空白页，此时 UTG 无文本可采；静态加壳本身不阻挡运行期 UTG 截屏，需在解密成功、p076r 之后的前台窗口出现时立即抓取。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.bypressfo.bgYohrrP.attachBaseContext",
    "com.bypressfo.bgYohrrP.oCetXE（native，libURisRK.so）",
    "res/xml/khxzxermtqafd.xml",
    "res/raw/wqhehnzhagnblw",
    "res/values/strings.xml#L3-L4",
    "com.bypressfo.p050a（无障碍服务，类体缺失于 classes.dex）"
  ]
}
```

**边界说明**：因关键流程位于加密载荷，本次未做风险台账写入；如需闭环，下一步应对 `libURisRK.so` 的 `oCetXE` 做 angr 逆向或 dump 解密后的 DEX，再核对 `ACTION_ACCESSIBILITY_SETTINGS` 跳转与遮罩实现。

</details>

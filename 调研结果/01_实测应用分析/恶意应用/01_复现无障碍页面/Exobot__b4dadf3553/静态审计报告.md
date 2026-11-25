# MB_153__b4dadf3553｜Exobot — BAWAG PSK Security

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：165.8s

## 1. 一句话核心结论

- **核心申请方式**：伪装成 BAWAG PSK 银行安全组件的 Exobot 家族样本，用一句空泛的 'Service must be enabled.' 作无障碍说明，请求 typeAllMask + 窗口内容读取的无障碍服务，真实引导与跳转逻辑藏在 native 解密的 res/raw 二阶段中。
- **静态可见性说明**：首阶段 classes.dex 仅 38 个桩类，Manifest 声明的无障碍服务 com.gotbutcv.p051s、启动 Activity com.gotbutcv.p043i 及全部业务类在 DEX 中不存在；真实代码由 AXbOQB.attachBaseContext 加载 libUgSqgXbMi.so 并从 res/raw/kshpyoex（163140 字节高熵密文）解密出二阶段。ACTION_ACCESSIBILITY_SETTINGS 跳转实现、引导弹窗文案、是否叠层/拒权循环均不可静态还原；仅 Manifest、res/xml/qbhernyn.xml、res/values/strings.xml 层可见。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b4dadf3553bb82499c4d0b6be96c47c46abc6904b611376d75c844ffb83725c6` |
| 包名 / 年份 | `com.gotbutcv` / 2022 |
| 家族 / 品类 | **Exobot**（同池样本数：3） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | BAWAG PSK Security |
| 引导页宣称品牌/身份 | BAWAG PSK（奥地利 BAWAG P.S.K. 银行）安全组件 |
| 系统无障碍列表服务名 | BAWAG PSK Security |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.gotbutcv 与宣称品牌无关；全部业务类被混淆为 p051s/p043i 等两字符短名并置于加密二阶段；20 余个随机字符串命名的 Activity/Receiver/Service（tvrdossfnhazz、zfrfmtrrvrizdi、ppjdzsjwawxdvxf 等）掩盖真实入口；application 主题为 Theme.AppCompat.Transparent.NoActionBar；无障碍说明仅一句 'Service must be enabled.'，不告知任何功能范围 |
| 无障碍服务类名 | `com.gotbutcv.p051s` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Service must be enabled. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.gotbutcv.p043i（android.intent.action.MAIN / LAUNCHER，label=BAWAG PSK Security，theme=Theme.AppCompat.Transparent.NoActionBar） | 用户点击桌面图标启动（onCreate/onResume 实现位于加密二阶段，不可见） | 不可静态还原 | **原文**：BAWAG PSK Security<br>**译注**：BAWAG PSK 安全（桌面图标与启动页标题） | 启动应用；是否可取消/跳过不可静态确认 | `AndroidManifest.xml 中 com.gotbutcv.p043i（实现体在加密二阶段 res/raw/kshpyoex）` |
| 2 | 跳无障碍设置 | 系统「设置 → 无障碍 → 已下载的服务」列表项 com.gotbutcv.p051s | 由二阶段代码发起的 ACTION_ACCESSIBILITY_SETTINGS 跳转（DEX 中无该字符串，跳转实现不可静态还原） | 系统无障碍页 | **原文**：BAWAG PSK Security / Service must be enabled.<br>**译注**：BAWAG PSK 安全 / 服务必须启用。 | 用户需在系统无障碍列表中手动找到并开启该服务 | `AndroidManifest.xml service com.gotbutcv.p051s；res/xml/qbhernyn.xml；res/values/strings.xml#OJWvDjwIjUMYT` |
| 3 | 获权后动作 | com.gotbutcv.p051s（AccessibilityService，typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows） | 系统绑定服务后回调 onServiceConnected / onAccessibilityEvent（实现体在加密二阶段） | 不可静态还原 | 无 | 无需用户操作；后续可能叠加 SYSTEM_ALERT_WINDOW 悬浮窗与短信拦截行为 | `res/xml/qbhernyn.xml；AndroidManifest.xml com.gotbutcv.p051s` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 桌面/启动器：android:label=@string/a → 'BAWAG PSK Security'（AndroidManifest application 与 activity com.gotbutcv.p043i）
- 系统无障碍服务列表项标题：service com.gotbutcv.p051s 的 android:label=@string/a → 'BAWAG PSK Security'
- 系统无障碍服务列表项描述：res/xml/qbhernyn.xml 的 android:description=@string/OJWvDjwIjUMYT → 'Service must be enabled.'（res/values/strings.xml）
- 包内未发现任何引导 HTML、assets 资源或自定义引导布局（assets 目录为空，res/layout 仅 AppCompat 模板），引导弹窗/遮罩文字若存在则来自加密二阶段，位置不可静态确定

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | BAWAG PSK Security | BAWAG PSK 安全 | `res/values/strings.xml 中 <string name="a">，被 application、com.gotbutcv.p043i、无障碍服务 com.gotbutcv.p051s 共同引用` | 假反诈安全 |
| en | Service must be enabled. | 服务必须启用。 | `res/values/strings.xml 中 <string name="OJWvDjwIjUMYT">，经 res/xml/qbhernyn.xml 的 android:description 呈现于系统无障碍列表` | 教唆忽视警告 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：拒权/返回系统设置后的处理逻辑位于 libUgSqgXbMi.so 解密出的二阶段载荷（res/raw/kshpyoex），首阶段 DEX 无 onResume/跳转相关实现，无法确认是否存在循环重跳
- **遮罩叠层 / 高仿系统设置页**：不可静态还原；已声明 SYSTEM_ALERT_WINDOW 与 Theme.AppCompat.Transparent.NoActionBar 透明无标题主题，具备叠层/伪设置页能力基础，但叠层代码不在可见范围内
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=28，未在可见资源中检索到应用详情页/受限设置教学文案；二阶段内是否存在不可静态确认）
- **获权后即时行为与防撤权机制**：不可静态还原；已声明设备管理员（res/xml/qmpgfadf.xml 含 wipe-data/reset-password/force-lock）、RECEIVE_BOOT_COMPLETED 自启与 PACKAGE_USAGE_STATS，具备防卸载/自启驻留底座，但无障碍服务内的 GLOBAL_ACTION_BACK 阻止撤权代码位于加密二阶段
- **良性降级 / 替代方案**：无（未见任何替代路径、手动模式或功能降级说明；无障碍说明仅为命令式一句话）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 ActivityManager/无障碍事件监测到顶层组件切至 com.android.settings/.accessibility.AccessibilitySettings 或 AccessibilityDetailsSettings 的瞬间立即拉起 UTG；若冷启动后 3 秒内未跳设置页，则改为以 com.gotbutcv.p043i 进入前台为触发点抓首屏弹窗
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：首阶段 DEX 为壳，全部引导文案、跳转代码与拒权循环逻辑在 libUgSqgXbMi.so 解密的 res/raw/kshpyoex 二阶段内，静态无法还原；若二阶段引导采用纯图/无文本空文本节点，UTG 文本节点可能为空，需结合截图比对。运行期 UTG 不受静态加壳影响，仍可正常捕获页面。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首屏（伪装银行安全组件）** | 包名 com.gotbutcv + 组件 com.gotbutcv.p043i，透明无 ActionBar 主题 | 确认诱导是从冷启动直接发起还是由某个功能按钮触发，并记录是否存在不可取消弹窗与取消按钮缺失 | 首屏是否直接出现引导文案/按钮；是否存在'取消/稍后'控件；是否出现系统设置跳转的前置说明文本 |
| **系统无障碍服务列表项** | Settings → Accessibility → 已下载的服务，条目文本 'BAWAG PSK Security' / 'Service must be enabled.' | 固定证据：服务名冒充银行、说明为空泛命令句，可直接量化身份不一致与说明缺失 | 服务列表项 label 文本；服务列表项 description 文本；是否存在同名良性应用混淆项 |
| **跳设置后压栈的引导遮罩/悬浮窗** | SYSTEM_ALERT_WINDOW 类型悬浮窗，或无障碍详情页之上叠加的透明 Activity | 判定是否存在遮挡系统开关位置、手把手指引点击的叠层诱导 | 无障碍详情页之上是否出现非系统窗口节点；遮罩是否覆盖开关区域并带箭头/文案；返回后是否被立刻重新拉起 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.gotbutcv.p051s（AndroidManifest 无障碍服务，label=BAWAG PSK Security，meta-data=@xml/qbhernyn）`
- `com.gotbutcv.p043i（LAUNCHER Activity，label=BAWAG PSK Security，Theme.AppCompat.Transparent.NoActionBar）`
- `com.gotbutcv.AXbOQB.attachBaseContext / OxOncUfELGC（加载 libUgSqgXbMi.so 并解密二阶段）`
- `res/xml/qbhernyn.xml（typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows）`
- `res/values/strings.xml#OJWvDjwIjUMYT（android:description = 'Service must be enabled.'）`
- `res/raw/kshpyoex（163140 字节加密二阶段载荷）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**静态可见性：加密二阶段（packed_or_encrypted）。引导页面的代码与文字全部不在首阶段 DEX 中，无法逐行还原 UTG 流转，但 Manifest、无障碍配置和服务名可以确认伪装与诱导结构。**

已核实事实：
- 首阶段 `classes.dex` 仅 38 个类，全部是 `Application`/`R`/AppCompat 桩与空壳组件；**Manifest 中声明的无障碍服务 `com.gotbutcv.p051s` 与启动 Activity `com.gotbutcv.p043i` 在 DEX 内均不存在**（`get_class_structure` 返回 Class not found，`search_function_definitions` 对 `p051s`/`AccessibilityService`/`onAccessibilityEvent` 全部 no_matches），`ACTION_ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`Service must be enabled.` 在 DEX 文本中均无命中。
- 真正的业务代码通过 [AXbOQB.attachBaseContext()](<resource-unit:#1.dex1 code:com.gotbutcv.AXbOQB#attachBaseContext>) 加载 [libUgSqgXbMi.so](<resource-unit:#1 file:lib/arm64-v8a/libUgSqgXbMi.so>)，该 `.so` 导出 `Java_com_gotbutcv_AXbOQB_OxOncUfELGC` 与一组混淆 C++ 符号（`DEveEjGgEsEPVYT`/`aasljqzkUpOiWR` 类），对应 [AXbOQB.OxOncUfELGC()](<resource-unit:#1.dex1 code:com.gotbutcv.AXbOQB#OxOncUfELGC>) 的 native 声明。
- 包内唯一可疑大体积资产是 [res/raw/kshpyoex](<resource-unit:#1 file:res/raw/kshpyoex>)（163,140 字节，首部 `87 95 0a 90 01 e7 9e 2c …` 高熵、无任何可打印头），即被加密的第二阶段载荷；`assets/` 为空，`res/layout` 仅 AppCompat 资源，无 HTML、无引导文案资源。

可确认的诱导结构（Manifest/资源层）：
- 桌面名称与无障碍服务标签同为 `BAWAG PSK Security`（`@string/a`），伪装奥地利 BAWAG PSK 银行安全组件；包名 `com.gotbutcv` 与之毫无关系。
- [res/xml/qbhernyn.xml](<resource-unit:#1 file:res/xml/qbhernyn.xml>) 声明 `typeAllMask` + `canRetrieveWindowContent="true"` + `flagRetrieveInteractiveWindows`，即全量窗口内容读取能力（典型窃取短信/覆盖页能力底座）。
- 无障碍说明仅为 [@string/OJWvDjwIjUMYT](<resource-unit:#1 file:res/values/strings.xml#L3>) = `Service must be enabled.`——一句命令式空话，不含任何功能用途告知，属于“教唆用户直接开启”的最小化说明。
- 配套高风险权限与组件：`READ_SMS`/`RECEIVE_SMS`/`SEND_SMS`、`CALL_PHONE`、`SYSTEM_ALERT_WINDOW`、`WRITE_SETTINGS`、`PACKAGE_USAGE_STATS`、设备管理员（[res/xml/qmpgfadf.xml](<resource-unit:#1 file:res/xml/qmpgfadf.xml>) 含 `wipe-data`/`reset-password`/`force-lock`）、`SMS_DELIVER` 高优先级接收器、`BOOT_COMPLETED` 自启，以及 20 余个随机命名的混淆 Activity/Receiver/Service（`tvrdossfnhazz`、`zfrfmtrrvrizdi` 等），用于隐藏真实入口。

未决边界：跳转 `ACTION_ACCESSIBILITY_SETTINGS` 的具体代码、是否 `onResume` 死循环重跳、是否叠放悬浮引导遮罩、13+ 受限设置教学，均在加密二阶段内，本次未做脱壳还原（超出 14 次工具预算），因此 flow 中相关步骤标记为不可静态还原，不做断言。

---

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "首阶段 classes.dex 仅 38 个桩类，Manifest 声明的无障碍服务 com.gotbutcv.p051s、启动 Activity com.gotbutcv.p043i 及全部业务类在 DEX 中不存在；真实代码由 AXbOQB.attachBaseContext 加载 libUgSqgXbMi.so 并从 res/raw/kshpyoex（163140 字节高熵密文）解密出二阶段。ACTION_ACCESSIBILITY_SETTINGS 跳转实现、引导弹窗文案、是否叠层/拒权循环均不可静态还原；仅 Manifest、res/xml/qbhernyn.xml、res/values/strings.xml 层可见。",
  "summary_one_liner": "伪装成 BAWAG PSK 银行安全组件的 Exobot 家族样本，用一句空泛的 'Service must be enabled.' 作无障碍说明，请求 typeAllMask + 窗口内容读取的无障碍服务，真实引导与跳转逻辑藏在 native 解密的 res/raw 二阶段中。",
  "disguise_identity": {
    "app_display_name": "BAWAG PSK Security",
    "claimed_brand_or_persona": "BAWAG PSK（奥地利 BAWAG P.S.K. 银行）安全组件",
    "a11y_service_label": "BAWAG PSK Security",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.gotbutcv 与宣称品牌无关；全部业务类被混淆为 p051s/p043i 等两字符短名并置于加密二阶段；20 余个随机字符串命名的 Activity/Receiver/Service（tvrdossfnhazz、zfrfmtrrvrizdi、ppjdzsjwawxdvxf 等）掩盖真实入口；application 主题为 Theme.AppCompat.Transparent.NoActionBar；无障碍说明仅一句 'Service must be enabled.'，不告知任何功能范围"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.gotbutcv.p043i（android.intent.action.MAIN / LAUNCHER，label=BAWAG PSK Security，theme=Theme.AppCompat.Transparent.NoActionBar）",
      "trigger_event": "用户点击桌面图标启动（onCreate/onResume 实现位于加密二阶段，不可见）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "BAWAG PSK Security",
      "shown_text_zh": "BAWAG PSK 安全（桌面图标与启动页标题）",
      "user_action_requested": "启动应用；是否可取消/跳过不可静态确认",
      "code_anchor": "AndroidManifest.xml 中 com.gotbutcv.p043i（实现体在加密二阶段 res/raw/kshpyoex）"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「设置 → 无障碍 → 已下载的服务」列表项 com.gotbutcv.p051s",
      "trigger_event": "由二阶段代码发起的 ACTION_ACCESSIBILITY_SETTINGS 跳转（DEX 中无该字符串，跳转实现不可静态还原）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "BAWAG PSK Security / Service must be enabled.",
      "shown_text_zh": "BAWAG PSK 安全 / 服务必须启用。",
      "user_action_requested": "用户需在系统无障碍列表中手动找到并开启该服务",
      "code_anchor": "AndroidManifest.xml service com.gotbutcv.p051s；res/xml/qbhernyn.xml；res/values/strings.xml#OJWvDjwIjUMYT"
    },
    {
      "step": 3,
      "stage": "获权后动作",
      "screen_or_component": "com.gotbutcv.p051s（AccessibilityService，typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows）",
      "trigger_event": "系统绑定服务后回调 onServiceConnected / onAccessibilityEvent（实现体在加密二阶段）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（获权后进入后台窗口内容读取与自动化操作，界面表现不可静态还原）",
      "user_action_requested": "无需用户操作；后续可能叠加 SYSTEM_ALERT_WINDOW 悬浮窗与短信拦截行为",
      "code_anchor": "res/xml/qbhernyn.xml；AndroidManifest.xml com.gotbutcv.p051s"
    }
  ],
  "text_presentation_locations": [
    "桌面/启动器：android:label=@string/a → 'BAWAG PSK Security'（AndroidManifest application 与 activity com.gotbutcv.p043i）",
    "系统无障碍服务列表项标题：service com.gotbutcv.p051s 的 android:label=@string/a → 'BAWAG PSK Security'",
    "系统无障碍服务列表项描述：res/xml/qbhernyn.xml 的 android:description=@string/OJWvDjwIjUMYT → 'Service must be enabled.'（res/values/strings.xml）",
    "包内未发现任何引导 HTML、assets 资源或自定义引导布局（assets 目录为空，res/layout 仅 AppCompat 模板），引导弹窗/遮罩文字若存在则来自加密二阶段，位置不可静态确定"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "BAWAG PSK Security",
      "text_zh": "BAWAG PSK 安全",
      "source_location": "res/values/strings.xml 中 <string name=\"a\">，被 application、com.gotbutcv.p043i、无障碍服务 com.gotbutcv.p051s 共同引用",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Service must be enabled.",
      "text_zh": "服务必须启用。",
      "source_location": "res/values/strings.xml 中 <string name=\"OJWvDjwIjUMYT\">，经 res/xml/qbhernyn.xml 的 android:description 呈现于系统无障碍列表",
      "rhetorical_frame": "教唆忽视警告"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：拒权/返回系统设置后的处理逻辑位于 libUgSqgXbMi.so 解密出的二阶段载荷（res/raw/kshpyoex），首阶段 DEX 无 onResume/跳转相关实现，无法确认是否存在循环重跳",
    "overlay_or_fake_settings": "不可静态还原；已声明 SYSTEM_ALERT_WINDOW 与 Theme.AppCompat.Transparent.NoActionBar 透明无标题主题，具备叠层/伪设置页能力基础，但叠层代码不在可见范围内",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=28，未在可见资源中检索到应用详情页/受限设置教学文案；二阶段内是否存在不可静态确认）",
    "post_grant_anti_removal": "不可静态还原；已声明设备管理员（res/xml/qmpgfadf.xml 含 wipe-data/reset-password/force-lock）、RECEIVE_BOOT_COMPLETED 自启与 PACKAGE_USAGE_STATS，具备防卸载/自启驻留底座，但无障碍服务内的 GLOBAL_ACTION_BACK 阻止撤权代码位于加密二阶段",
    "benign_graceful_degradation": "无（未见任何替代路径、手动模式或功能降级说明；无障碍说明仅为命令式一句话）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 ActivityManager/无障碍事件监测到顶层组件切至 com.android.settings/.accessibility.AccessibilitySettings 或 AccessibilityDetailsSettings 的瞬间立即拉起 UTG；若冷启动后 3 秒内未跳设置页，则改为以 com.gotbutcv.p043i 进入前台为触发点抓首屏弹窗",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首屏（伪装银行安全组件）",
        "page_identifier": "包名 com.gotbutcv + 组件 com.gotbutcv.p043i，透明无 ActionBar 主题",
        "why_most_useful": "确认诱导是从冷启动直接发起还是由某个功能按钮触发，并记录是否存在不可取消弹窗与取消按钮缺失",
        "observable_utg_signals": ["首屏是否直接出现引导文案/按钮", "是否存在'取消/稍后'控件", "是否出现系统设置跳转的前置说明文本"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility → 已下载的服务，条目文本 'BAWAG PSK Security' / 'Service must be enabled.'",
        "why_most_useful": "固定证据：服务名冒充银行、说明为空泛命令句，可直接量化身份不一致与说明缺失",
        "observable_utg_signals": ["服务列表项 label 文本", "服务列表项 description 文本", "是否存在同名良性应用混淆项"]
      },
      {
        "page_role": "跳设置后压栈的引导遮罩/悬浮窗",
        "page_identifier": "SYSTEM_ALERT_WINDOW 类型悬浮窗，或无障碍详情页之上叠加的透明 Activity",
        "why_most_useful": "判定是否存在遮挡系统开关位置、手把手指引点击的叠层诱导",
        "observable_utg_signals": ["无障碍详情页之上是否出现非系统窗口节点", "遮罩是否覆盖开关区域并带箭头/文案", "返回后是否被立刻重新拉起"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：首阶段 DEX 为壳，全部引导文案、跳转代码与拒权循环逻辑在 libUgSqgXbMi.so 解密的 res/raw/kshpyoex 二阶段内，静态无法还原；若二阶段引导采用纯图/无文本空文本节点，UTG 文本节点可能为空，需结合截图比对。运行期 UTG 不受静态加壳影响，仍可正常捕获页面。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.gotbutcv.p051s（AndroidManifest 无障碍服务，label=BAWAG PSK Security，meta-data=@xml/qbhernyn）",
    "com.gotbutcv.p043i（LAUNCHER Activity，label=BAWAG PSK Security，Theme.AppCompat.Transparent.NoActionBar）",
    "com.gotbutcv.AXbOQB.attachBaseContext / OxOncUfELGC（加载 libUgSqgXbMi.so 并解密二阶段）",
    "res/xml/qbhernyn.xml（typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows）",
    "res/values/strings.xml#OJWvDjwIjUMYT（android:description = 'Service must be enabled.'）",
    "res/raw/kshpyoex（163140 字节加密二阶段载荷）"
  ]
}
```

</details>

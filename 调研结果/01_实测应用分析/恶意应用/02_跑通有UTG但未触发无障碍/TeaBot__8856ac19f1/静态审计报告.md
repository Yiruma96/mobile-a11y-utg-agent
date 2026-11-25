# MB_115__8856ac19f1｜TeaBot — QR Code Scanner: Add-On

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：160.2s

## 1. 一句话核心结论

- **核心申请方式**：扫码工具外壳 + 无标签无说明的无障碍服务 + Tinker 加密载荷：真实引导流程藏于二阶段 dex，静态只能确认其无障碍服务以空白名称静默出现在系统列表并具备读屏与手势能力。
- **静态可见性说明**：真实业务代码（com.akbjmrnec.wiuvhfydb.* 含无障碍服务与全部 Activity）不在 classes.dex 中；Application 类 com.honey.wine.e 通过 attachBaseContext -> com.honey.wine.f.a(Context) 实现 Tinker 式热补丁装载（反射向 BaseDexClassLoader.pathList 注入 dex），载荷为 assets/TUIGGay/hetGedjgF1.ff7（zlib 78 9c，解压 262633 字节，熵 7.995，解压后仍为高熵密文，未还原出 DEX）。因此无障碍引导弹窗、跳转 Settings 的 Intent 构造、遮罩层与全部诱导文案均无法静态取得，仅 Manifest 声明、无障碍配置 XML 与权限/组件结构静态可见。
- **命中的行为模式标签**：`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `8856ac19f179461c4008249c342c8dadbd17118f80f43ce0229ddb1cda33bd67` |
| 包名 / 年份 | `com.akbjmrnec.wiuvhfydb` / 2022 |
| 家族 / 品类 | **TeaBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | QR Code Scanner: Add-On |
| 引导页宣称品牌/身份 | 二维码扫描工具（QR Code Scanner 加装插件） |
| 系统无障碍列表服务名 | 无（asclllservizio.xml 未声明 android:description，服务无 label，系统无障碍列表将显示由类名 com.akbjmrnec.wiuvhfydb.UIDNwaidobaWIODb 派生的空白/无意义条目） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：服务无 description 与 settingsActivity，用户在系统无障碍列表中看不到任何用途说明；全部类名/包名为随机大小写拼接（UIDNwaidobaWIODb、iaoWNDoianwdoIAWND、nawIODnaiowdna）；核心代码整体移出主 dex，由 Tinker 补丁机制在 Application.attachBaseContext 阶段从 assets 解密装载，规避主 DEX 静态特征扫描；多个 Theme.NoTitleBar 且 android:label="" 的空名 Activity（含 singleTask + excludeFromRecents 的 inject.uibwduIABuIaw）可承载无标题遮罩/注入页；assets/aigames/sConsole.html 为 <script src="%s"> 远程脚本注入壳。 |
| 无障碍服务类名 | `com.akbjmrnec.wiuvhfydb.UIDNwaidobaWIODb` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | android.app.Application 子类 com.honey.wine.e（attachBaseContext / onCreate） | 进程启动时 attachBaseContext 回调 | 不可静态还原 | 无 | 无（用户无感知） | `com.honey.wine.e#attachBaseContext / com.honey.wine.e#onCreate / com.honey.wine.f#a(Context)` |
| 2 | 引导说明页 | 候选：com.akbjmrnec.wiuvhfydb.WNiudwabNUDIba（LAUNCHER）或 util.AUInawiOBFA / nawIODnaiowdna / util.nidwoanAIOWDbwaiuBa / util.uaiwdBuaiwbdaD（Theme.NoTitleBar、android:label=""） | 不可静态还原（类体位于加密补丁 dex，onCreate 逻辑与文案均不可见） | 不可静态还原 | **原文**：无（代码体未还原；主 dex 内不存在 com.akbjmrnec.* 类实体）<br>**译注**：推测为扫码工具外壳或无障碍用途说明页，但内容无法静态确认 | 不可静态还原（是否有取消/跳过按钮无法确认） | `AndroidManifest.xml 中 com.akbjmrnec.wiuvhfydb.WNiudwabNUDIba / util.AUInawiOBFA 等 activity 声明` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS 页面（预期） | 不可静态还原：主 dex 中不存在 ACTION_ACCESSIBILITY_SETTINGS / android.settings.* 相关字符串引用 | 不可静态还原 | 无 | 不可静态还原 | `res/xml/asclllservizio.xml（服务在系统列表中的呈现依据）` |
| 4 | 获权后动作 | com.akbjmrnec.wiuvhfydb.UIDNwaidobaWIODb（AccessibilityService，typeAllMask / canRetrieveWindowContent / canPerformGestures / flagRetrieveInteractiveWindows） | 系统绑定服务后 onServiceConnected / onAccessibilityEvent（方法体位于加密载荷，不可见） | 不可静态还原 | 无 | 无（后台持续运行） | `res/xml/asclllservizio.xml / AndroidManifest.xml 中 service UIDNwaidobaWIODb 声明` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表：服务无 android:description 与 label，条目名称只能由类名 com.akbjmrnec.wiuvhfydb.UIDNwaidobaWIODb 派生（res/xml/asclllservizio.xml 未定义任何说明文本）
- 桌面图标名称：AndroidManifest.xml application android:label="QR Code Scanner: Add-On"（唯一静态可见的身份文本）
- 预筛命中的 Google Play services 系列文案位于 res/values/strings.xml（common_google_play_services_*），属 GMS SDK 自带资源，非本应用诱导话术
- assets/aigames/sConsole.html：仅含 <script src="%s"> 占位，为远程脚本注入壳，无静态文案
- 预期但不可静态确认的载体：5 个 Theme.NoTitleBar 空标签 Activity（util.AUInawiOBFA、nawIODnaiowdna、util.nidwoanAIOWDbwaiuBa、util.uaiwdBuaiwbdaD、inject.uibwduIABuIaw）与 SYSTEM_ALERT_WINDOW 悬浮窗，其 UI 文案随加密载荷下发

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | QR Code Scanner: Add-On | 二维码扫描器：附加组件 | `AndroidManifest.xml <application android:label>` | 清理工具伪装 |
| en | android:accessibilityEventTypes="typeAllMask" android:accessibilityFeedbackType="feedbackVisual" android:accessibilityFlags="flagDefault\|flagIncludeNotImportantViews\|flagReportViewIds\|flagRetrieveInteractiveWindows" android:canRetrieveWindowContent="true" android:canPerformGestures="true" | （无障碍服务能力声明，非用户可见文案）接收全部事件类型、可读取窗口内容、可执行手势、可获取交互窗口 | `res/xml/asclllservizio.xml` | 未知 |
| en | %1$s won't work unless you enable Google Play services. | %1$s 在您启用 Google Play 服务之前无法工作。 | `res/values/strings.xml common_google_play_services_enable_text（GMS SDK 资源）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：引导与重跳逻辑位于 assets/TUIGGay/hetGedjgF1.ff7 解密后的补丁 dex 中，主 dex 无任何 settings Intent 引用，无法确认是否 onResume 死循环重跳或定时器拉起
- **遮罩叠层 / 高仿系统设置页**：不可静态还原；但已具备叠加遮罩的客观条件：SYSTEM_ALERT_WINDOW 权限 + 5 个 Theme.NoTitleBar 空标签 Activity + singleTask/excludeFromRecents 的 inject.uibwduIABuIaw 注入页
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（targetSdk 28，主 dex 无 ACTION_APPLICATION_DETAILS_SETTINGS 引用；相关教学文案若存在亦在加密载荷内）
- **获权后即时行为与防撤权机制**：不可静态还原；服务声明 canPerformGestures 与 flagRetrieveInteractiveWindows，具备用 GLOBAL_ACTION_BACK/HOME 干扰撤权的技术前提，但无静态证据
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以冷启动后首个 Activity 拉起为起点，在系统 Activity 栈出现 com.android.settings/.Settings$AccessibilitySettings（或 SubSettings）的瞬间定格抓取；同时对所有 Theme.NoTitleBar 空标签 Activity 的 onResume 与 WindowManager 新增悬浮窗（TYPE_APPLICATION_OVERLAY）事件设触发点
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：一阶段 dex 内不含任何业务/引导代码（无 com.akbjmrnec.* 类实体、无 settings Intent 字符串），真实 UI 全部由 assets/TUIGGay/hetGedjgF1.ff7 经 Tinker 机制在 attachBaseContext 阶段解密装载；若该载荷校验运行环境（模拟器/UTG 沙箱）或依赖远端下发参数才启用诱导页，纯 UTG 可能只看到空白外壳。注意静态加壳本身不阻挡运行期 UTG，应以运行期行为为准。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首屏/工具外壳页** | com.akbjmrnec.wiuvhfydb.WNiudwbaNUDIba 或 util.AUInawiOBFA / nawIODnaiowdna 等 NoTitleBar Activity 的窗口内容 | 确认是否在无任何业务操作的情况下立即弹出无障碍引导（TRIG_COLD_START_BLOCK），以及外壳页是否仅为扫码工具假象 | 首屏文本与按钮文案；是否出现无取消按钮的对话框；是否存在一次性跳过入口；页面停留时长与是否阻塞业务 |
| **跳转前的说明/教学页** | 引导文案载体（原生 Dialog / 本地或远程 WebView），可通过窗口类名与是否含 WebView 区分 | 区分 CARRIER_NATIVE_DIALOG_OR_ACTIVITY / CARRIER_WEBVIEW_LOCAL_HTML / CARRIER_WEBVIEW_REMOTE_URL，并提取诱导话术（假更新、故障恐吓、隐私承诺等） | 文案逐字提取；是否存在取消/关闭控件；是否宣称安全或隐私承诺；WebView 加载的是 assets 还是远端 URL |
| **系统无障碍服务列表项** | Settings$AccessibilitySettings 中标签为空白或类名派生文本的服务条目 | 直接证明诱导指向的是无说明的 UIDNwaidobaWIODb 服务，而非任何具名辅助功能 | 服务条目显示名称（空白/类名）；是否存在用途说明副标题；开关被点击时的系统警告弹窗文案；该条目是否为列表唯一可操作项 |
| **设置页之上的遮罩/悬浮引导层** | TYPE_APPLICATION_OVERLAY 悬浮窗或压栈的 NoTitleBar Activity（inject.uibwduIABuIaw） | 判定 COERCE_OVERLAY_STACK_ON_SETTINGS：是否用高亮手指/箭头/伪造开关页覆盖系统无障碍页，把用户引向特定条目 | 遮罩是否覆盖系统设置；是否绘制指向开关的箭头或高亮框；遮罩是否屏蔽返回键/不可关闭；遮罩透明度与位置 |
| **返回设置后的反馈页** | 从系统设置返回后立即重建的引导弹窗或再次跳转 | 判定 COERCE_REFUSAL_LOOP_RELAUNCH：未授权即回弹重跳的循环机制与周期 | 返回后重新跳转的时延；连续重跳次数；文案是否升级为恐吓/惩罚性提示；是否出现强制停留无法退出 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.honey.wine.e#attachBaseContext`
- `com.honey.wine.e#onCreate`
- `com.honey.wine.f#a(Context)`
- `assets/TUIGGay/hetGedjgF1.ff7`
- `res/xml/asclllservizio.xml`
- `AndroidManifest.xml service com.akbjmrnec.wiuvhfydb.UIDNwaidobaWIODb`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**关键判断：UTG 页面流转无法通过静态分析还原——真实的无障碍诱导代码不在 `classes.dex` 中，而在经 Tinker 热修复机制加载的加密载荷内。**

已证实的静态事实：

1. **Manifest 声明了一个没有标签的无障碍服务**
   [UIDNwaidobaWIODb](<resource-unit:#1 manifest:components>) 声明 `BIND_ACCESSIBILITY_SERVICE`，导出的 meta-data 指向 [res/xml/asclllservizio.xml](<resource-unit:#1 file:res/xml/asclllservizio.xml>)，配置为 `typeAllMask` + `canRetrieveWindowContent=true` + `canPerformGestures=true` + `flagRetrieveInteractiveWindows`，**既没有 `android:description`，也没有 `android:settingsActivity`，更没有 `android:isAccessibilityTool`**（targetSdk 28 本身也低于 31）。因此，系统无障碍列表只能显示由类名派生或为空的条目，用户看不到任何用途说明。

2. **应用身份与权限能力严重不符**
   桌面显示名为 `QR Code Scanner: Add-On`（扫码工具），但同时持有 `READ_SMS`/`RECEIVE_SMS`/`SEND_SMS`/`WRITE_SMS`/`RECEIVE_MMS`、`SYSTEM_ALERT_WINDOW`、`QUERY_ALL_PACKAGES`、`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`、`USE_FULL_SCREEN_INTENT`、`REQUEST_PASSWORD_COMPLEXITY`，并注册了优先级 999 的 `SMS_RECEIVED/SMS_DELIVER` 接收器，这与 TeaBot 家族以短信窃取 + 无障碍注入为核心的行为特征一致。

3. **真实业务代码被整体抽走**：在 DEX 字符串中搜不到任何 `com.akbjmrnec.*` 类描述符，MCP 也无法定位 `UIDNwaidobaWIODb`、`WNiudwabNUDIba` 等类，这说明这些类的实体不在 `classes.dex` 中。

4. **加载链已还原**：`android:name=com.honey.wine.e` → [attachBaseContext](<resource-unit:#1.dex1 code:com.honey.wine.e#attachBaseContext>) 调用 [f.a(Context)](<resource-unit:#1.dex1 code:com.honey.wine.f#a>)，这是一套完整复刻 Tinker 的热补丁装载逻辑（通过反射向 `BaseDexClassLoader.pathList` 注入 dex，并使用 `RandomAccessFile`/`FileLock`、`patch_time`/`unzip_time`/`patchUrl` 字段）；[onCreate](<resource-unit:#1.dex1 code:com.honey.wine.e#onCreate>) 再切换到 `com.mi.MiApplication`。载荷文件为 [assets/TUIGGay/hetGedjgF1.ff7](<resource-unit:#1 file:assets/TUIGGay/hetGedjgF1.ff7>)（262681 B，`78 9c` zlib 头，解压 262633 B，熵 7.995），解压后仍是高熵密文，尚未还原出 DEX。

5. **无法确认的 UI 载体**：5 个 `Theme.NoTitleBar` 空标签 Activity（`util.AUInawiOBFA`、`nawIODnaiowdna`、`util.nidwoanAIOWDbwaiuBa`、`util.uaiwdBuaiwbdaD`、`inject.uibwduIABuIaw`）以及 `assets/aigames/sConsole.html`（`<script src="%s">` 远程脚本注入壳）是典型的诱导页/遮罩页/注入页候选，但它们的 onCreate 逻辑与文案都在加密载荷内，**没有任何一处可以静态引用到 `ACTION_ACCESSIBILITY_SETTINGS` 跳转或引导弹窗文本**。

6. 预筛给出的 Google Play services 系列字符串全部来自 `res/values/strings.xml` 的 GMS SDK 资源，属于误报，与本应用的诱导话术无关。

边界：本次在 14 次工具调用内停止，未执行 UTG 动态抓取，也未写入项目风险记录。要判定"是否强制、是否循环重跳、是否叠加遮罩"，需要在运行期观测；本报告的 JSON 已给出捕获策略。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "真实业务代码（com.akbjmrnec.wiuvhfydb.* 含无障碍服务与全部 Activity）不在 classes.dex 中；Application 类 com.honey.wine.e 通过 attachBaseContext -> com.honey.wine.f.a(Context) 实现 Tinker 式热补丁装载（反射向 BaseDexClassLoader.pathList 注入 dex），载荷为 assets/TUIGGay/hetGedjgF1.ff7（zlib 78 9c，解压 262633 字节，熵 7.995，解压后仍为高熵密文，未还原出 DEX）。因此无障碍引导弹窗、跳转 Settings 的 Intent 构造、遮罩层与全部诱导文案均无法静态取得，仅 Manifest 声明、无障碍配置 XML 与权限/组件结构静态可见。",
  "summary_one_liner": "扫码工具外壳 + 无标签无说明的无障碍服务 + Tinker 加密载荷：真实引导流程藏于二阶段 dex，静态只能确认其无障碍服务以空白名称静默出现在系统列表并具备读屏与手势能力。",
  "disguise_identity": {
    "app_display_name": "QR Code Scanner: Add-On",
    "claimed_brand_or_persona": "二维码扫描工具（QR Code Scanner 加装插件）",
    "a11y_service_label": "无（asclllservizio.xml 未声明 android:description，服务无 label，系统无障碍列表将显示由类名 com.akbjmrnec.wiuvhfydb.UIDNwaidobaWIODb 派生的空白/无意义条目）",
    "identity_mismatch": true,
    "obfuscation_tricks": "服务无 description 与 settingsActivity，用户在系统无障碍列表中看不到任何用途说明；全部类名/包名为随机大小写拼接（UIDNwaidobaWIODb、iaoWNDoianwdoIAWND、nawIODnaiowdna）；核心代码整体移出主 dex，由 Tinker 补丁机制在 Application.attachBaseContext 阶段从 assets 解密装载，规避主 DEX 静态特征扫描；多个 Theme.NoTitleBar 且 android:label=\"\" 的空名 Activity（含 singleTask + excludeFromRecents 的 inject.uibwduIABuIaw）可承载无标题遮罩/注入页；assets/aigames/sConsole.html 为 <script src=\"%s\"> 远程脚本注入壳。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "android.app.Application 子类 com.honey.wine.e（attachBaseContext / onCreate）",
      "trigger_event": "进程启动时 attachBaseContext 回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "此步无界面；负责在进程启动阶段装载 Tinker 补丁 dex，使后续所有诱导页面代码生效",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "com.honey.wine.e#attachBaseContext / com.honey.wine.e#onCreate / com.honey.wine.f#a(Context)"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "候选：com.akbjmrnec.wiuvhfydb.WNiudwabNUDIba（LAUNCHER）或 util.AUInawiOBFA / nawIODnaiowdna / util.nidwoanAIOWDbwaiuBa / util.uaiwdBuaiwbdaD（Theme.NoTitleBar、android:label=\"\"）",
      "trigger_event": "不可静态还原（类体位于加密补丁 dex，onCreate 逻辑与文案均不可见）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（代码体未还原；主 dex 内不存在 com.akbjmrnec.* 类实体）",
      "shown_text_zh": "推测为扫码工具外壳或无障碍用途说明页，但内容无法静态确认",
      "user_action_requested": "不可静态还原（是否有取消/跳过按钮无法确认）",
      "code_anchor": "AndroidManifest.xml 中 com.akbjmrnec.wiuvhfydb.WNiudwabNUDIba / util.AUInawiOBFA 等 activity 声明"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS 页面（预期）",
      "trigger_event": "不可静态还原：主 dex 中不存在 ACTION_ACCESSIBILITY_SETTINGS / android.settings.* 相关字符串引用",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "预期跳转到系统无障碍列表，列表项名称为空白/类名派生文本",
      "user_action_requested": "不可静态还原",
      "code_anchor": "res/xml/asclllservizio.xml（服务在系统列表中的呈现依据）"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.akbjmrnec.wiuvhfydb.UIDNwaidobaWIODb（AccessibilityService，typeAllMask / canRetrieveWindowContent / canPerformGestures / flagRetrieveInteractiveWindows）",
      "trigger_event": "系统绑定服务后 onServiceConnected / onAccessibilityEvent（方法体位于加密载荷，不可见）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后可读取全部窗口内容并执行手势，配合短信全套权限可对银行/即时通讯界面进行读屏与自动操作",
      "user_action_requested": "无（后台持续运行）",
      "code_anchor": "res/xml/asclllservizio.xml / AndroidManifest.xml 中 service UIDNwaidobaWIODb 声明"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表：服务无 android:description 与 label，条目名称只能由类名 com.akbjmrnec.wiuvhfydb.UIDNwaidobaWIODb 派生（res/xml/asclllservizio.xml 未定义任何说明文本）",
    "桌面图标名称：AndroidManifest.xml application android:label=\"QR Code Scanner: Add-On\"（唯一静态可见的身份文本）",
    "预筛命中的 Google Play services 系列文案位于 res/values/strings.xml（common_google_play_services_*），属 GMS SDK 自带资源，非本应用诱导话术",
    "assets/aigames/sConsole.html：仅含 <script src=\"%s\"> 占位，为远程脚本注入壳，无静态文案",
    "预期但不可静态确认的载体：5 个 Theme.NoTitleBar 空标签 Activity（util.AUInawiOBFA、nawIODnaiowdna、util.nidwoanAIOWDbwaiuBa、util.uaiwdBuaiwbdaD、inject.uibwduIABuIaw）与 SYSTEM_ALERT_WINDOW 悬浮窗，其 UI 文案随加密载荷下发"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "QR Code Scanner: Add-On",
      "text_zh": "二维码扫描器：附加组件",
      "source_location": "AndroidManifest.xml <application android:label>",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "android:accessibilityEventTypes=\"typeAllMask\" android:accessibilityFeedbackType=\"feedbackVisual\" android:accessibilityFlags=\"flagDefault|flagIncludeNotImportantViews|flagReportViewIds|flagRetrieveInteractiveWindows\" android:canRetrieveWindowContent=\"true\" android:canPerformGestures=\"true\"",
      "text_zh": "（无障碍服务能力声明，非用户可见文案）接收全部事件类型、可读取窗口内容、可执行手势、可获取交互窗口",
      "source_location": "res/xml/asclllservizio.xml",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "%1$s 在您启用 Google Play 服务之前无法工作。",
      "source_location": "res/values/strings.xml common_google_play_services_enable_text（GMS SDK 资源）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：引导与重跳逻辑位于 assets/TUIGGay/hetGedjgF1.ff7 解密后的补丁 dex 中，主 dex 无任何 settings Intent 引用，无法确认是否 onResume 死循环重跳或定时器拉起",
    "overlay_or_fake_settings": "不可静态还原；但已具备叠加遮罩的客观条件：SYSTEM_ALERT_WINDOW 权限 + 5 个 Theme.NoTitleBar 空标签 Activity + singleTask/excludeFromRecents 的 inject.uibwduIABuIaw 注入页",
    "restricted_settings_13plus_coaching": "无静态证据（targetSdk 28，主 dex 无 ACTION_APPLICATION_DETAILS_SETTINGS 引用；相关教学文案若存在亦在加密载荷内）",
    "post_grant_anti_removal": "不可静态还原；服务声明 canPerformGestures 与 flagRetrieveInteractiveWindows，具备用 GLOBAL_ACTION_BACK/HOME 干扰撤权的技术前提，但无静态证据",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以冷启动后首个 Activity 拉起为起点，在系统 Activity 栈出现 com.android.settings/.Settings$AccessibilitySettings（或 SubSettings）的瞬间定格抓取；同时对所有 Theme.NoTitleBar 空标签 Activity 的 onResume 与 WindowManager 新增悬浮窗（TYPE_APPLICATION_OVERLAY）事件设触发点",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首屏/工具外壳页",
        "page_identifier": "com.akbjmrnec.wiuvhfydb.WNiudwbaNUDIba 或 util.AUInawiOBFA / nawIODnaiowdna 等 NoTitleBar Activity 的窗口内容",
        "why_most_useful": "确认是否在无任何业务操作的情况下立即弹出无障碍引导（TRIG_COLD_START_BLOCK），以及外壳页是否仅为扫码工具假象",
        "observable_utg_signals": ["首屏文本与按钮文案", "是否出现无取消按钮的对话框", "是否存在一次性跳过入口", "页面停留时长与是否阻塞业务"]
      },
      {
        "page_role": "跳转前的说明/教学页",
        "page_identifier": "引导文案载体（原生 Dialog / 本地或远程 WebView），可通过窗口类名与是否含 WebView 区分",
        "why_most_useful": "区分 CARRIER_NATIVE_DIALOG_OR_ACTIVITY / CARRIER_WEBVIEW_LOCAL_HTML / CARRIER_WEBVIEW_REMOTE_URL，并提取诱导话术（假更新、故障恐吓、隐私承诺等）",
        "observable_utg_signals": ["文案逐字提取", "是否存在取消/关闭控件", "是否宣称安全或隐私承诺", "WebView 加载的是 assets 还是远端 URL"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings$AccessibilitySettings 中标签为空白或类名派生文本的服务条目",
        "why_most_useful": "直接证明诱导指向的是无说明的 UIDNwaidobaWIODb 服务，而非任何具名辅助功能",
        "observable_utg_signals": ["服务条目显示名称（空白/类名）", "是否存在用途说明副标题", "开关被点击时的系统警告弹窗文案", "该条目是否为列表唯一可操作项"]
      },
      {
        "page_role": "设置页之上的遮罩/悬浮引导层",
        "page_identifier": "TYPE_APPLICATION_OVERLAY 悬浮窗或压栈的 NoTitleBar Activity（inject.uibwduIABuIaw）",
        "why_most_useful": "判定 COERCE_OVERLAY_STACK_ON_SETTINGS：是否用高亮手指/箭头/伪造开关页覆盖系统无障碍页，把用户引向特定条目",
        "observable_utg_signals": ["遮罩是否覆盖系统设置", "是否绘制指向开关的箭头或高亮框", "遮罩是否屏蔽返回键/不可关闭", "遮罩透明度与位置"]
      },
      {
        "page_role": "返回设置后的反馈页",
        "page_identifier": "从系统设置返回后立即重建的引导弹窗或再次跳转",
        "why_most_useful": "判定 COERCE_REFUSAL_LOOP_RELAUNCH：未授权即回弹重跳的循环机制与周期",
        "observable_utg_signals": ["返回后重新跳转的时延", "连续重跳次数", "文案是否升级为恐吓/惩罚性提示", "是否出现强制停留无法退出"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：一阶段 dex 内不含任何业务/引导代码（无 com.akbjmrnec.* 类实体、无 settings Intent 字符串），真实 UI 全部由 assets/TUIGGay/hetGedjgF1.ff7 经 Tinker 机制在 attachBaseContext 阶段解密装载；若该载荷校验运行环境（模拟器/UTG 沙箱）或依赖远端下发参数才启用诱导页，纯 UTG 可能只看到空白外壳。注意静态加壳本身不阻挡运行期 UTG，应以运行期行为为准。"
  },
  "behavior_pattern_tags": [
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE"
  ],
  "code_anchors": [
    "com.honey.wine.e#attachBaseContext",
    "com.honey.wine.e#onCreate",
    "com.honey.wine.f#a(Context)",
    "assets/TUIGGay/hetGedjgF1.ff7",
    "res/xml/asclllservizio.xml",
    "AndroidManifest.xml service com.akbjmrnec.wiuvhfydb.UIDNwaidobaWIODb"
  ]
}
```

</details>

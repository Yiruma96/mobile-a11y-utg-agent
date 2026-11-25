# MB_083__ae502f6778｜Ermac — HookAPP

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：94.9s

## 1. 一句话核心结论

- **核心申请方式**：以伪 Chrome 更新页全屏悬浮窗 WebView 覆盖界面，配合 onResume 反复重弹与伪造 isAccessibilityTool 的 HookAPPService，诱导 CIS 地区用户开启无障碍权限。
- **静态可见性说明**：DEX 代码、Manifest、无障碍配置与 strings 完整可读，引导流程逻辑静态清晰；但诱导页 HTML 正文经 Base64 编码后由 m3.e(G.a()) 取值并仅替换 %Enable_Accessibility_Service% 占位符后 loadDataWithBaseURL 渲染，正文文案与页面内按钮行为不在静态资源中，需动态捕获。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ae502f67782e9cc2a6e33b868f14467f3dabf126e868a8e10a68aa2ddd4092e1` |
| 包名 / 年份 | `com.rekezapayojekubu.kebi` / 2024 |
| 家族 / 品类 | **Ermac**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | HookAPP |
| 引导页宣称品牌/身份 | Chrome Update Service（伪造的 Chrome 浏览器更新服务）；另备 Facebook/Google Play/Gmail/WhatsApp/YouTube/Instagram/TikTok/Telegram/Chrome/Contacts 共 10 个 activity-alias 供运行期切换 |
| 系统无障碍列表服务名 | HookAPPService |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 运行期 setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED) 禁用自身启动器组件隐藏图标（k3.d.c）；2) 10 个 activity-alias 伪装主流应用图标与名称，静态 enabled=false 由服务端指令切换；3) 无障碍配置伪造 android:isAccessibilityTool="true" 使系统不再弹出高风险提示；4) 系统无障碍描述写成 "若无障碍已开启请先关闭再开启" 的反常话术；5) 类名与包名全量随机化（com.hakojogerewaya.cidu.*、k3.d、v1.a 等） |
| 无障碍服务类名 | `com.hakojogerewaya.cidu.pitowulalu.ducehejimu` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.rekezapayojekubu.kebi.rapu（LAUNCHER，Theme.Translucent.NoTitleBar，noHistory） | onCreate：先执行 k3.d.a(this) 国家白名单判定，命中后 k3.d.c(this) 禁用启动器组件并 finish()；未命中则 setContentView(单空格 TextView) 后进入 noziba 分支 | 原生Activity | **原文**：textView.setText(" ");<br>**译注**：仅设置一个空格文本作为界面内容，界面本身不可见（透明无标题主题） | 无需操作，自动跳转；无取消/跳过入口 | `com.rekezapayojekubu.kebi.rapu.onCreate / k3.d.a / k3.d.c` |
| 2 | 引导说明页 | com.hakojogerewaya.cidu.noziba（透明 Activity，getWindow().setType(2006) 系统悬浮窗类型） | onCreate → onResume → s() | 悬浮窗Overlay | **原文**：无（窗口本身透明，内容由 WebView 覆盖层承载）<br>**译注**：透明宿主窗口，作为全屏悬浮遮罩的容器 | 无直接要求，遮罩随后压栈 | `com.hakojogerewaya.cidu.noziba.onCreate（setType(2006)）` |
| 3 | 遮罩叠层指引 | WindowManager 全屏 WebView 覆盖层（addView(new WindowManager$LayoutParams(-1,-1,2,262144,-2))，JS 桥 "Android"） | noziba.s() 中 v1.a.a(this)==false（未在 enabled_accessibility_services 中检测到 ducehejimu）且 this.z 为真时构建并 addView | 远端WebView | **原文**：Base64.decode((String) G.a(), 0) 后 f4.i.F0(html, "%Enable_Accessibility_Service%", "Chrome Update Service")，并以 loadDataWithBaseURL(null, html, "text/html", "UTF-8", null) 渲染（正文非明文静态资源）<br>**译注**：页面以「Chrome 更新服务 / Chrome Update Service」名义呈现，实际目的为要求开启无障碍；HTML 正文来自 Base64 配置下发，静态不可见 | 按页面指引开启无障碍服务（页面内含 JS 桥 Android 供点击回调），无取消/跳过按钮 | `com.hakojogerewaya.cidu.noziba.s（WebView + addJavascriptInterface(noziba$g, "Android") + addView）` |
| 4 | 跳无障碍设置 | WebView 内按钮经 JS 桥 com.hakojogerewaya.cidu.noziba$g 触发（推测跳系统无障碍设置页） | 页面按钮点击 → JS 桥回调 | 远端WebView | **原文**：无（按钮文案位于 Base64 HTML 内，静态不可读）<br>**译注**：页面内引导按钮，指向系统无障碍服务列表 | 在系统无障碍列表中勾选 HookAPPService | `com.hakojogerewaya.cidu.noziba$g（JS 接口，loadUrl/addJavascriptInterface）` |
| 5 | 拒权反馈循环 | noziba.onResume → s() 重入 | 用户从系统设置页返回、未开启无障碍 → onResume 无条件调用 s()，重新判定并再次 addView 遮罩 | 悬浮窗Overlay | **原文**：无（复用同一 Base64 HTML 页面）<br>**译注**：返回即重新覆盖，无跳过路径 | 只能反复面对遮罩，或强制停止应用 | `com.hakojogerewaya.cidu.noziba.onResume` |
| 6 | 获权后动作 | ducehejimu 无障碍服务（HookAPPService）+ noziba.s() 权限申请分支 | v1.a.a(this)==true 后：j3.a.t() 上报、h3.a.a() 取设备信息、检查 14 项运行时权限与悬浮窗/Doze 白名单（k3.c.a、noziba$d.d），随后进入业务逻辑 | 系统无障碍页 | **原文**：If accessibility permission has been on, please turn off then turn on.<br>**译注**：若无障碍权限已开启，请先关闭再重新开启。 | 按提示反复关闭/开启服务，以使新配置生效 | `v1.a.a / noziba.s / res/xml/hajose.xml / res/values/strings.xml#L49` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 全屏 WindowManager 悬浮窗 WebView（noziba.s 中 addView，LayoutParams(-1,-1,2,262144,-2)），承载 Base64 配置下发的伪「Chrome Update Service」HTML 引导页
- 系统无障碍服务列表项：服务标签 "HookAPPService"，应用名 "HookAPP"
- 系统无障碍服务详情描述：res/values/strings.xml 中 text_accessibility_service_description = "If accessibility permission has been on, please turn off then turn on."（经 res/xml/hajose.xml 的 android:description 引用）
- 桌面图标名称：默认 "HookAPP"，另有 10 个 activity-alias 标签 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram
- 应用运行时 Toast 提示（androidx.activity.b#run）："need accessibility service"
- rapu 的透明宿主窗口仅显示单个空格 TextView（无可读文案）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | If accessibility permission has been on, please turn off then turn on. | 如果无障碍权限已经开启，请先关闭再重新开启。 | `res/values/strings.xml#text_accessibility_service_description（被 res/xml/hajose.xml android:description 引用）` | 教唆忽视警告 |
| en | Chrome Update Service | Chrome 更新服务 | `com.hakojogerewaya.cidu.noziba.s 中 f4.i.F0(html, "%Enable_Accessibility_Service%", "Chrome Update Service") 硬编码替换值` | 假更新 |
| en | need accessibility service | 需要无障碍服务 | `androidx.activity.b#run 中的 Toast.makeText 硬编码` | 未知 |
| en | HookAPPService | HookAPP 服务 | `AndroidManifest.xml 无障碍 service android:label` | 未知 |
| en | HookAPP | HookAPP（应用显示名） | `AndroidManifest.xml application android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：noziba.onResume() 无条件调用 s()，每次从系统设置页返回都会重新读取 enabled_accessibility_services；未检测到本服务即重新创建 WebView 并以 WindowManager.addView 全屏压栈覆盖，形成死循环；同时 rapu 通过 k3.d.c() 禁用自身启动器组件，用户难以从桌面重新定位并卸载。
- **遮罩叠层 / 高仿系统设置页**：全屏半透明系统级悬浮窗（WindowManager$LayoutParams 宽高 -1、type 2、flags 262144），内容为 WebView 渲染的伪「Chrome Update Service」HTML 页面，覆盖在系统设置页之上形成遮罩式分步指引；未发现高仿系统无障碍开关的原生仿制页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=29，未针对 Android 13+ 受限设置做「应用详情→右上角菜单→允许受限设置」教学）
- **获权后即时行为与防撤权机制**：获权后通过系统描述文本 "If accessibility permission has been on, please turn off then turn on." 要求用户反复关闭再开启服务（重置服务实例/规避已授权检测）；同时具备 BIND_DEVICE_ADMIN 设备管理器与 notification listener，但未在静态代码中确认用 GLOBAL_ACTION_BACK/HOME 阻止撤权。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到进程 com.rekezapayojekubu.kebi 启动后约 1–2 秒内出现 WindowManager.addView 的全屏 TYPE_APPLICATION_OVERLAY 覆盖层，或 UTG 中检测到无障碍设置相关页面被悬浮层覆盖时立即抓取；另可在 noziba Activity onResume 触发后立即抓屏。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导页 HTML 正文经 Base64 编码且内容来自配置下发，静态不可见；若下发 HTML 采用纯图片/空文本渲染，则 UTG 文本信号可能为空，需 OCR 与截图补充。静态本身未加壳，运行期 UTG 不受影响。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后全屏伪更新引导遮罩页（最关键）** | 覆盖整个屏幕的 WebView 容器，无系统标题栏，宿主为透明 Activity；页面标题/正文含「Chrome」「Update」字样 | 该页是唯一的诱导入口，同时证明「伪造 Chrome 更新身份 + 覆盖式引导 + 无取消按钮」三要素 | 页面文本节点中 Chrome / Update / Service 等品牌词；无「取消/跳过/稍后」按钮节点；按钮节点点击目标为无障碍设置相关文案（如 Accessibility / Aksesibilitas）；覆盖层下方仍可见系统设置页或桌面节点 |
| **系统无障碍服务列表项** | Settings 无障碍页中名为 HookAPPService 的条目 | 确认服务标签与真实身份不符（HookAPP/HookAPPService vs 引导页宣称 Chrome），并核对 isAccessibilityTool 伪造导致无风险提示 | 服务条目文本 HookAPPService；条目无系统高风险警告提示；勾选后服务立即启动的日志/状态变化 |
| **从设置页返回后的遮罩重弹页** | noziba.onResume 触发的第二次 addView 覆盖层 | 证明拒权循环（无良性降级），区分「一次性引导」与「强制胁迫」 | 同一遮罩页面在 1–2 秒内重复出现；无任何可关闭控件；宿主 Activity 仍为 noziba 透明窗口 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.hakojogerewaya.cidu.noziba.s`
- `com.hakojogerewaya.cidu.noziba.onResume`
- `com.hakojogerewaya.cidu.noziba.onCreate`
- `v1.a.a`
- `com.rekezapayojekubu.kebi.rapu.onCreate`
- `res/xml/hajose.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

分析已完成。为避免超出工具调用预算，我基于已核实证据直接给出结论。

## 结论要点

**核心机制（已证实）**：无障碍引导不依赖 `ACTION_ACCESSIBILITY_SETTINGS` 跳转。该样本改为通过**全屏悬浮窗 WebView（伪 "Chrome Update Service" 页面）**在任意界面之上强行覆盖，并配合 `onResume` 反复重新拉起，从而形成拒权循环。

1. **启动链**：桌面入口 [rapu.onCreate()](<resource-unit:#1.dex1 code:com.rekezapayojekubu.kebi.rapu#onCreate>) 先做国家白名单判定 [k3.d.a()](<resource-unit:#1.dex1 code:k3.d#a>)（`[ua][ru][by][tj][uz][tm][az][am][kz][kg][md]`，仅 CIS 地区生效）；命中后调用 [k3.d.c()](<resource-unit:#1.dex1 code:k3.d#c>) 执行 `setComponentEnabledSetting(..., 2, 1)`，**在运行期禁用自身启动器组件（隐藏图标）** 并 `finish()`，随后转入 `noziba`。
2. **遮罩载体**：[noziba.onCreate()](<resource-unit:#1.dex1 code:com.hakojogerewaya.cidu.noziba#onCreate>) 把窗口类型设为 `2006`（TYPE_SYSTEM_ALERT 系统级悬浮窗），并设置 `0x40000` 标志。
3. **诱导页**：[noziba.s()](<resource-unit:#1.dex1 code:com.hakojogerewaya.cidu.noziba#s>) 通过 [v1.a.a()](<resource-unit:#1.dex1 code:v1.a#a>) 读取 `Settings.Secure.enabled_accessibility_services` 判定无障碍是否开启；未开启时新建 `WebView`（JS 开启、注入 `Android` JS 桥 `noziba$g`、`loadDataWithBaseURL(null,...)`），把远端/配置下发的 Base64 HTML 中 `%Enable_Accessibility_Service%` 占位符**替换为 "Chrome Update Service"**，再用 `WindowManager.addView(-1,-1)` 全屏压栈。
4. **拒权循环**：[noziba.onResume()](<resource-unit:#1.dex1 code:com.hakojogerewaya.cidu.noziba#onResume>) 无条件调用 `s()`，用户从设置页返回即重新判定并重弹遮罩。
5. **身份伪装**：`android:label="HookAPP"`、服务标签 `HookAPPService`，另有 10 个 `activity-alias`（Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome/Instagram/TikTok/Telegram，均 `enabled="false"` 待运行期切换）；无障碍配置 [hajose.xml](<resource-unit:#1 file:res/xml/hajose.xml>) 伪造 `android:isAccessibilityTool="true"`，且申请 `canTakeScreenshot`/`canPerformGestures`/`canRetrieveWindowContent` 等全量能力。
6. **描述话术**：[strings.xml 第49行](<resource-unit:#1 file:res/values/strings.xml#L49>) 的系统无障碍说明为 "If accessibility permission has been on, please turn off then turn on." —— 教唆用户**先关闭再开启**，用于规避已授权检测/重置服务状态。

**未决边界**：引导 HTML 正文来自 Base64 编码的 `m3.e`（`G.a()`）取值，非明文静态资源，其按钮文案与点击后是否再调 `ACTION_ACCESSIBILITY_SETTINGS` 需动态捕获确认。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "DEX 代码、Manifest、无障碍配置与 strings 完整可读，引导流程逻辑静态清晰；但诱导页 HTML 正文经 Base64 编码后由 m3.e(G.a()) 取值并仅替换 %Enable_Accessibility_Service% 占位符后 loadDataWithBaseURL 渲染，正文文案与页面内按钮行为不在静态资源中，需动态捕获。",
  "summary_one_liner": "以伪 Chrome 更新页全屏悬浮窗 WebView 覆盖界面，配合 onResume 反复重弹与伪造 isAccessibilityTool 的 HookAPPService，诱导 CIS 地区用户开启无障碍权限。",
  "disguise_identity": {
    "app_display_name": "HookAPP",
    "claimed_brand_or_persona": "Chrome Update Service（伪造的 Chrome 浏览器更新服务）；另备 Facebook/Google Play/Gmail/WhatsApp/YouTube/Instagram/TikTok/Telegram/Chrome/Contacts 共 10 个 activity-alias 供运行期切换",
    "a11y_service_label": "HookAPPService",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 运行期 setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED) 禁用自身启动器组件隐藏图标（k3.d.c）；2) 10 个 activity-alias 伪装主流应用图标与名称，静态 enabled=false 由服务端指令切换；3) 无障碍配置伪造 android:isAccessibilityTool=\"true\" 使系统不再弹出高风险提示；4) 系统无障碍描述写成 \"若无障碍已开启请先关闭再开启\" 的反常话术；5) 类名与包名全量随机化（com.hakojogerewaya.cidu.*、k3.d、v1.a 等）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.rekezapayojekubu.kebi.rapu（LAUNCHER，Theme.Translucent.NoTitleBar，noHistory）",
      "trigger_event": "onCreate：先执行 k3.d.a(this) 国家白名单判定，命中后 k3.d.c(this) 禁用启动器组件并 finish()；未命中则 setContentView(单空格 TextView) 后进入 noziba 分支",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "textView.setText(\" \");",
      "shown_text_zh": "仅设置一个空格文本作为界面内容，界面本身不可见（透明无标题主题）",
      "user_action_requested": "无需操作，自动跳转；无取消/跳过入口",
      "code_anchor": "com.rekezapayojekubu.kebi.rapu.onCreate / k3.d.a / k3.d.c"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.hakojogerewaya.cidu.noziba（透明 Activity，getWindow().setType(2006) 系统悬浮窗类型）",
      "trigger_event": "onCreate → onResume → s()",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（窗口本身透明，内容由 WebView 覆盖层承载）",
      "shown_text_zh": "透明宿主窗口，作为全屏悬浮遮罩的容器",
      "user_action_requested": "无直接要求，遮罩随后压栈",
      "code_anchor": "com.hakojogerewaya.cidu.noziba.onCreate（setType(2006)）"
    },
    {
      "step": 3,
      "stage": "遮罩叠层指引",
      "screen_or_component": "WindowManager 全屏 WebView 覆盖层（addView(new WindowManager$LayoutParams(-1,-1,2,262144,-2))，JS 桥 \"Android\"）",
      "trigger_event": "noziba.s() 中 v1.a.a(this)==false（未在 enabled_accessibility_services 中检测到 ducehejimu）且 this.z 为真时构建并 addView",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "Base64.decode((String) G.a(), 0) 后 f4.i.F0(html, \"%Enable_Accessibility_Service%\", \"Chrome Update Service\")，并以 loadDataWithBaseURL(null, html, \"text/html\", \"UTF-8\", null) 渲染（正文非明文静态资源）",
      "shown_text_zh": "页面以「Chrome 更新服务 / Chrome Update Service」名义呈现，实际目的为要求开启无障碍；HTML 正文来自 Base64 配置下发，静态不可见",
      "user_action_requested": "按页面指引开启无障碍服务（页面内含 JS 桥 Android 供点击回调），无取消/跳过按钮",
      "code_anchor": "com.hakojogerewaya.cidu.noziba.s（WebView + addJavascriptInterface(noziba$g, \"Android\") + addView）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "WebView 内按钮经 JS 桥 com.hakojogerewaya.cidu.noziba$g 触发（推测跳系统无障碍设置页）",
      "trigger_event": "页面按钮点击 → JS 桥回调",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "无（按钮文案位于 Base64 HTML 内，静态不可读）",
      "shown_text_zh": "页面内引导按钮，指向系统无障碍服务列表",
      "user_action_requested": "在系统无障碍列表中勾选 HookAPPService",
      "code_anchor": "com.hakojogerewaya.cidu.noziba$g（JS 接口，loadUrl/addJavascriptInterface）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "noziba.onResume → s() 重入",
      "trigger_event": "用户从系统设置页返回、未开启无障碍 → onResume 无条件调用 s()，重新判定并再次 addView 遮罩",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（复用同一 Base64 HTML 页面）",
      "shown_text_zh": "返回即重新覆盖，无跳过路径",
      "user_action_requested": "只能反复面对遮罩，或强制停止应用",
      "code_anchor": "com.hakojogerewaya.cidu.noziba.onResume"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "ducehejimu 无障碍服务（HookAPPService）+ noziba.s() 权限申请分支",
      "trigger_event": "v1.a.a(this)==true 后：j3.a.t() 上报、h3.a.a() 取设备信息、检查 14 项运行时权限与悬浮窗/Doze 白名单（k3.c.a、noziba$d.d），随后进入业务逻辑",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "shown_text_zh": "若无障碍权限已开启，请先关闭再重新开启。",
      "user_action_requested": "按提示反复关闭/开启服务，以使新配置生效",
      "code_anchor": "v1.a.a / noziba.s / res/xml/hajose.xml / res/values/strings.xml#L49"
    }
  ],
  "text_presentation_locations": [
    "全屏 WindowManager 悬浮窗 WebView（noziba.s 中 addView，LayoutParams(-1,-1,2,262144,-2)），承载 Base64 配置下发的伪「Chrome Update Service」HTML 引导页",
    "系统无障碍服务列表项：服务标签 \"HookAPPService\"，应用名 \"HookAPP\"",
    "系统无障碍服务详情描述：res/values/strings.xml 中 text_accessibility_service_description = \"If accessibility permission has been on, please turn off then turn on.\"（经 res/xml/hajose.xml 的 android:description 引用）",
    "桌面图标名称：默认 \"HookAPP\"，另有 10 个 activity-alias 标签 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram",
    "应用运行时 Toast 提示（androidx.activity.b#run）：\"need accessibility service\"",
    "rapu 的透明宿主窗口仅显示单个空格 TextView（无可读文案）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "text_zh": "如果无障碍权限已经开启，请先关闭再重新开启。",
      "source_location": "res/values/strings.xml#text_accessibility_service_description（被 res/xml/hajose.xml android:description 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Chrome Update Service",
      "text_zh": "Chrome 更新服务",
      "source_location": "com.hakojogerewaya.cidu.noziba.s 中 f4.i.F0(html, \"%Enable_Accessibility_Service%\", \"Chrome Update Service\") 硬编码替换值",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "need accessibility service",
      "text_zh": "需要无障碍服务",
      "source_location": "androidx.activity.b#run 中的 Toast.makeText 硬编码",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "HookAPPService",
      "text_zh": "HookAPP 服务",
      "source_location": "AndroidManifest.xml 无障碍 service android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "HookAPP",
      "text_zh": "HookAPP（应用显示名）",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "noziba.onResume() 无条件调用 s()，每次从系统设置页返回都会重新读取 enabled_accessibility_services；未检测到本服务即重新创建 WebView 并以 WindowManager.addView 全屏压栈覆盖，形成死循环；同时 rapu 通过 k3.d.c() 禁用自身启动器组件，用户难以从桌面重新定位并卸载。",
    "overlay_or_fake_settings": "全屏半透明系统级悬浮窗（WindowManager$LayoutParams 宽高 -1、type 2、flags 262144），内容为 WebView 渲染的伪「Chrome Update Service」HTML 页面，覆盖在系统设置页之上形成遮罩式分步指引；未发现高仿系统无障碍开关的原生仿制页。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=29，未针对 Android 13+ 受限设置做「应用详情→右上角菜单→允许受限设置」教学）",
    "post_grant_anti_removal": "获权后通过系统描述文本 \"If accessibility permission has been on, please turn off then turn on.\" 要求用户反复关闭再开启服务（重置服务实例/规避已授权检测）；同时具备 BIND_DEVICE_ADMIN 设备管理器与 notification listener，但未在静态代码中确认用 GLOBAL_ACTION_BACK/HOME 阻止撤权。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到进程 com.rekezapayojekubu.kebi 启动后约 1–2 秒内出现 WindowManager.addView 的全屏 TYPE_APPLICATION_OVERLAY 覆盖层，或 UTG 中检测到无障碍设置相关页面被悬浮层覆盖时立即抓取；另可在 noziba Activity onResume 触发后立即抓屏。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后全屏伪更新引导遮罩页（最关键）",
        "page_identifier": "覆盖整个屏幕的 WebView 容器，无系统标题栏，宿主为透明 Activity；页面标题/正文含「Chrome」「Update」字样",
        "why_most_useful": "该页是唯一的诱导入口，同时证明「伪造 Chrome 更新身份 + 覆盖式引导 + 无取消按钮」三要素",
        "observable_utg_signals": ["页面文本节点中 Chrome / Update / Service 等品牌词", "无「取消/跳过/稍后」按钮节点", "按钮节点点击目标为无障碍设置相关文案（如 Accessibility / Aksesibilitas）", "覆盖层下方仍可见系统设置页或桌面节点"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中名为 HookAPPService 的条目",
        "why_most_useful": "确认服务标签与真实身份不符（HookAPP/HookAPPService vs 引导页宣称 Chrome），并核对 isAccessibilityTool 伪造导致无风险提示",
        "observable_utg_signals": ["服务条目文本 HookAPPService", "条目无系统高风险警告提示", "勾选后服务立即启动的日志/状态变化"]
      },
      {
        "page_role": "从设置页返回后的遮罩重弹页",
        "page_identifier": "noziba.onResume 触发的第二次 addView 覆盖层",
        "why_most_useful": "证明拒权循环（无良性降级），区分「一次性引导」与「强制胁迫」",
        "observable_utg_signals": ["同一遮罩页面在 1–2 秒内重复出现", "无任何可关闭控件", "宿主 Activity 仍为 noziba 透明窗口"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导页 HTML 正文经 Base64 编码且内容来自配置下发，静态不可见；若下发 HTML 采用纯图片/空文本渲染，则 UTG 文本信号可能为空，需 OCR 与截图补充。静态本身未加壳，运行期 UTG 不受影响。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL"
  ],
  "code_anchors": [
    "com.hakojogerewaya.cidu.noziba.s",
    "com.hakojogerewaya.cidu.noziba.onResume",
    "com.hakojogerewaya.cidu.noziba.onCreate",
    "v1.a.a",
    "com.rekezapayojekubu.kebi.rapu.onCreate",
    "res/xml/hajose.xml"
  ]
}
```

</details>

# MB_131__ceea4208d5｜TrickMo — Google services

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：196.1s

## 1. 一句话核心结论

- **核心申请方式**：该应用把自身与无障碍服务同时伪装成“Google services”，用“必须启用否则无法正常运行 + 杀毒软件会误报”的文案在冷启动即引导用户进入系统无障碍页开启全量监听服务，并以 isAccessibilityTool=true 伪造辅助工具属性规避系统警告，真实引导页面与载荷藏于加密资产与运行期投放类中。
- **静态可见性说明**：Manifest、无障碍配置 XML、resources.arsc 文案与 Application 桩代码静态可见；但真正执行引导的类 nilheart.ptur744.lens.gi5qN5xht_SWOTMtcfj 不在 classes.dex 中（Class.forName 后异常被吞），且全部 81 个 assets 条目（含 assets/www/index.html、inject.js、YgIheO.json、googleinfo.txt）以 PKZIP 传统加密存储，DEX 内不存在 ACTION_ACCESSIBILITY_SETTINGS 跳转字符串，故无障碍设置跳转、引导页与遮罩逻辑均无法静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ceea4208d55b4de89279633183dae164e57aa03d729ade7d39a75c7d1e583078` |
| 包名 / 年份 | `nilheart.ptur744.lens` / 2025 |
| 家族 / 品类 | **TrickMo**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google services |
| 引导页宣称品牌/身份 | Google Play services / Google services（Google 官方服务组件） |
| 系统无障碍列表服务名 | Google services |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:isAccessibilityTool="true" 伪造“辅助工具类”以在 Android 14+ 隐藏警告并归入“已下载的应用”；服务名与类名完全无关（V_mhElDCXAww9C）；Application 桩类通过反射替换 ContextImpl.mOuterContext / LoadedApk.mApplication 劫持 Application 实例；多个 noHistory+excludeFromRecents+launchMode=singleInstance 的隐形 Activity（c9XPJ2hRrGd0Ax3hb、o9PA、Zbm8h84T8NFeyVIbTm1、K03QONwX6QdSwTYY）与 StubActivity 作跳板；宿主为被二次打包的 MediaConverter 应用，包名 nilheart.ptur744.lens 与“Google”无任何关联。 |
| 无障碍服务类名 | `nilheart.ptur744.lens.V_mhElDCXAww9C` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | This option shall be enabled. This is very important for the correct and steady operation of the application. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.dynamic.human.Jfetchbarrel（android:name 指向的 Application） | Application.onCreate() | 不可静态还原 | 无 | 无 | `com.dynamic.human.Jfetchbarrel#onCreate` |
| 2 | 冷启动入口 | Jfetchbarrel.bambooprocess(String) 反射链：Class.forName("nilheart.ptur744.lens.gi5qN5xht_SWOTMtcfj") → 改写 ContextImpl.mOuterContext / LoadedApk.mApplication → application.onCreate() | onCreate 内调用 bambooprocess，且无条件 return true（异常被 catch 吞掉） | 不可静态还原 | 无 | 无 | `com.dynamic.human.Jfetchbarrel#bambooprocess` |
| 3 | 引导说明页 | 冷启动后立即弹出的无障碍开启说明（推测为 assets/www/index.html WebView 或原生 Dialog，资产加密不可读） | 按文案“Immediately after running the application”即冷启动后立即触发 | 不可静态还原 | **原文**：Immediately after running the application, the Accessibility aid menu will open. To prevent the steady operation of this application from interfering with other third-party applications (for example, malware or too strict antivirus policy), a special option shall be enabled that will help avoid conflicts.<br>**译注**：运行本应用后无障碍辅助菜单将立即打开。为防止本应用的稳定运行受到其他第三方应用干扰（例如恶意软件或过于严格的杀毒策略），需要启用一个特殊选项以避免冲突。 | 按提示前往无障碍菜单开启服务，并忽略可能出现的安全警告；无可见取消/跳过路径 | `resources.arsc 字符串（无障碍引导说明）；assets/www/index.html（PKZIP 加密）` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载的服务 → “Google services” | 运行期载荷发起 ACTION_ACCESSIBILITY_SETTINGS（DEX 内无该字符串，由投放类执行） | 系统无障碍页 | **原文**：Google services<br>**译注**：无障碍服务列表中显示条目名“Google services” | 点选该条目进入开关页并打开开关 | `AndroidManifest.xml service nilheart.ptur744.lens.V_mhElDCXAww9C label=@7F0E001C` |
| 5 | 跳无障碍设置 | 服务详情/开关页下方说明文本（android:description） | 用户在列表中展开或进入服务详情 | 系统无障碍页 | **原文**：This option shall be enabled. This is very important for the correct and steady operation of the application.<br>**译注**：必须启用此选项。这对本应用的正确与稳定运行非常重要。 | 开启开关；文案只强调“必须启用”，未提供拒绝或替代方案 | `res/xml/accessibilityservice.xml android:description=@7F0E001B` |
| 6 | 拒权反馈循环 | 未静态可见（引导与重试逻辑在加密资产/运行期投放类中） | 不可静态还原 | 不可静态还原 | 无 | 不可静态还原 | `无（受加密资产阻断）` |
| 7 | 获权后动作 | 无障碍服务 V_mhElDCXAww9C（全事件监听 + 窗口内容读取 + 手势注入 + 截图）及 DeviceAdmin/输入法/通知监听/VPN 组件 | 服务 onServiceConnected 后由投放载荷驱动（不可静态还原） | 不可静态还原 | 无 | 不可静态还原 | `res/xml/accessibilityservice.xml；res/xml/device_admin.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目名：AndroidManifest.xml 中 service V_mhElDCXAww9C 的 android:label=@7F0E001C → “Google services”
- 系统无障碍服务详情/开关页说明文本：res/xml/accessibilityservice.xml 的 android:description=@7F0E001B → “This option shall be enabled. This is very important for the correct and steady operation of the application.”
- 冷启动引导说明（预期为本地 WebView 或原生 Dialog）：resources.arsc 中 “Immediately after running the application, the Accessibility aid menu will open...”（对应 assets/www/index.html，PKZIP 加密不可读）
- 伪装为系统/Google 组件的弹窗文案：Google Play services 库资源字符串（“Enable Google Play services”、“%1$s won't work unless you enable Google Play services.”、“New version of Google Play services needed. It will update itself shortly.”）
- 桌面图标名称：AndroidManifest.xml application android:label=@7F0E0021 → “Google services”

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | This option shall be enabled. This is very important for the correct and steady operation of the application. | 必须启用此选项。这对本应用的正确与稳定运行非常重要。 | `res/xml/accessibilityservice.xml android:description → resources.arsc @7F0E001B` | 故障恐吓 |
| en | Immediately after running the application, the Accessibility aid menu will open. To prevent the steady operation of this application from interfering with other third-party applications (for example, malware or too strict antivirus policy), a special option shall be enabled that will help avoid conflicts. | 运行本应用后无障碍辅助菜单将立即打开。为防止本应用的稳定运行受到其他第三方应用干扰（例如恶意软件或过于严格的杀毒策略），需要启用一个特殊选项以避免冲突。 | `resources.arsc 字符串（无障碍引导说明）` | 教唆忽视警告 |
| en | Google services | Google 服务 | `AndroidManifest.xml application android:label=@7F0E0021；service V_mhElDCXAww9C android:label=@7F0E001C` | 假更新 |
| en | %1$s won't work unless you enable Google Play services. | 除非启用 Google Play 服务，否则 %1$s 无法工作。 | `resources.arsc（Google Play services 库字符串）` | 故障恐吓 |
| en | New version of Google Play services needed. It will update itself shortly. | 需要新版本的 Google Play 服务，它将很快自行更新。 | `resources.arsc（Google Play services 库字符串）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：引导与重试逻辑位于加密资产与运行期投放类（nilheart.ptur744.lens.gi5qN5xht_SWOTMtcfj）中，DEX 内无 ACTION_ACCESSIBILITY_SETTINGS 及 onResume 重跳代码，无法确认是否死循环拉起；但服务声明 noHistory/excludeFromRecents 的多个隐形 Activity 与 StubActivity 具备反复拉起条件。
- **遮罩叠层 / 高仿系统设置页**：静态不可见：DEX 内无 SYSTEM_ALERT_WINDOW 使用点与遮罩布局调用；overlay 线索初筛为空，遮罩/高仿设置页（若存在）在加密资产或投放类中。
- **Android 13+ 受限设置（Restricted Settings）应对**：无直接证据：DEX 中仅宿主遗留代码使用 ACTION_APPLICATION_DETAILS_SETTINGS（com.fundevs.app.mediaconverter.BaseActivity#L、MediaActivity#G0），是否用于引导“允许受限设置”无法确认；无障碍开启路径的受限设置教学不可静态还原。
- **获权后即时行为与防撤权机制**：具备条件但未静态闭环：同时申请 DeviceAdmin（wipe-data、reset-password、force-lock、disable-camera 等）与无障碍全量事件/手势注入，具备阻止撤权能力；具体自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权代码在加密载荷中，不可静态确认。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后监测到当前 Activity 变为 com.android.settings/.Settings$AccessibilitySettings 或 AccessibilityDetailsSettings（即 ACTION_ACCESSIBILITY_SETTINGS 触发瞬间）时立刻抓取；其次在 Application 初始化完成后的首帧（Jfetchbarrel.onCreate 之后）开始连续抓取，以捕获其前置引导页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区：全部 81 个 assets（含 assets/www/index.html、inject.js、YgIheO.json、googleinfo.txt）为 PKZIP 加密存储，DEX 内真实业务类缺失且无 ACTION_ACCESSIBILITY_SETTINGS 字符串，静态无法还原引导页与遮罩；此外存在被二次打包的良性宿主（MediaConverter）代码与 Google Play services 库资源，易造成“看似正常”的误判。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项** | Settings → 无障碍 → 已下载的服务 中出现名称“Google services”的条目（对应 nilheart.ptur744.lens.V_mhElDCXAww9C） | 这是品牌冒充与 isAccessibilityTool 伪造的最终呈现点，UTG 可同时取到应用名、服务名与说明文本三者一致伪装的证据 | 服务条目文本 “Google services”；服务条目对应的包名 nilheart.ptur744.lens 与显示名不一致；条目未出现系统高危警告横幅（isAccessibilityTool=true 生效） |
| **冷启动引导弹窗页 / 跳转前教学页** | 冷启动后首个非宿主业务页面，内容含“Accessibility aid menu will open”“very important for the correct and steady operation” | 决定是否存在冷启动 0 步阻断式诱导，以及话术是否教唆忽视杀毒软件警告；该页面在静态层被加密资产隐藏，只能靠 UTG 获取 | 弹窗/页面文本是否含 accessibility 与 antivirus/malware 话术；是否存在取消/跳过按钮；承载控件类型为 WebView 还是原生 Dialog |
| **设置页后压栈遮罩页** | 跳转系统无障碍页后 500–1000ms 内出现的悬浮窗或高仿开关页（SYSTEM_ALERT_WINDOW 已声明） | 用于判定是否存在遮罩叠层指引或伪造系统开关页，这是静态层完全缺失的一环 | 窗口是否属于 nilheart.ptur744.lens 且覆盖在 settings 之上；遮罩文本是否为指引箭头/“点击此处开启”；返回键后是否再次压栈 |
| **拒权返回后的反馈页** | 从无障碍页返回宿主 App 时立刻出现的页面或再次跳转动作 | 判定拒权循环强度（死循环重跳 / 定时拉起 / 良性降级） | 返回后 N 秒内是否再次进入 settings 包名页面；是否出现“必须开启”类阻断文案；是否存在退出应用的唯一出路 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.dynamic.human.Jfetchbarrel#onCreate`
- `com.dynamic.human.Jfetchbarrel#bambooprocess`
- `res/xml/accessibilityservice.xml（android:isAccessibilityTool="true"，canTakeScreenshot/canPerformGestures/canRetrieveWindowContent）`
- `AndroidManifest.xml（service nilheart.ptur744.lens.V_mhElDCXAww9C label=@7F0E001C；application label=@7F0E0021 “Google services”）`
- `resources.arsc（android:description @7F0E001B 与无障碍冷启动引导文案）`
- `assets/www/index.html、assets/YgIheO.json、assets/googleinfo.txt（PKZIP 加密，未解密）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（受 14 次工具调用上限约束，已完成定向核验）

**静态可见性：核心引导链不可静态还原（`packed_or_encrypted`）**

1. **Manifest 层证据完整且高度可疑**
   - 应用显示名与无障碍服务标签均为 **“Google services”**（`label=@7F0E0021` / `@7F0E001C`），属系统性品牌冒充。
   - 无障碍服务 `nilheart.ptur744.lens.V_mhElDCXAww9C` 绑定 `BIND_ACCESSIBILITY_SERVICE`，其配置文件 [res/xml/accessibilityservice.xml](<resource-unit:#1 file:res/xml/accessibilityservice.xml>) 声明了 **`android:isAccessibilityTool="true"`**，并开启 `canRetrieveWindowContent`、`canPerformGestures`、`canTakeScreenshot`、`canRequestFilterKeyEvents` 与全事件类型 `0xFFFFFFFF`——即伪装成"辅助工具类"以规避 Android 14+ 的系统警告，实际权限为全量屏幕读取与手势注入。
   - 同时声明 DeviceAdmin（`wipe-data`/`reset-password`/`disable-camera` 等）、输入法、通知监听、VPN 服务，具备典型 TrickMo 式"撤权抵抗 + 全通道监听"能力。

2. **引导文案真实存在，且直接教唆忽视安全警告**
   - `android:description` = “This option shall be enabled. This is very important for the correct and steady operation of the application.”
   - `resources.arsc` 中另有一句冷启动引导原文：“**Immediately after running the application, the Accessibility aid menu will open.** To prevent the steady operation ... from interfering with other third-party applications (for example, **malware or too strict antivirus policy**), a special option shall be enabled...” —— 明确说明**安装后立即拉起无障碍设置**，并预置"杀毒软件误报"话术。
   - 另有 Google Play services 库原生文案（“%1$s won't work unless you enable Google Play services.” 等）配合品牌伪装。

3. **跳转与页面载体藏在加密资产中**
   - 整个 DEX 内 **不存在 `ACTION_ACCESSIBILITY_SETTINGS`**；唯一跳转点为宿主 App（`com.fundevs.app.mediaconverter`）遗留的 `APPLICATION_DETAILS_SETTINGS`。
   - APK 的 **81 个 assets 条目为 PKZIP 加密**，包括 `assets/www/index.html`(239KB)、`assets/www/inject.js`、`assets/YgIheO.json`(5.4MB)、`assets/googleinfo.txt`——WebView 教学页与载荷配置均不可静态读取。
   - Application 类 [com.dynamic.human.Jfetchbarrel#onCreate](<resource-unit:#1.dex1 code:com.dynamic.human.Jfetchbarrel#onCreate>) 通过 `bambooprocess()` 反射改写 `ContextImpl.mOuterContext` 与 `LoadedApk.mApplication`，再 `Class.forName("nilheart.ptur744.lens.gi5qN5xht_SWOTMtcfj")` 实例化并回调其 `onCreate()`；**该类不在 classes.dex 中**，说明真实业务与引导逻辑由运行期投放，异常被静默吞掉。
   - `libtool-checker.so` 仅 10KB，为环境检测桩，非加载器。

4. **UTG 视角要点**：最佳钩子是冷启动 Application 初始化后、系统无障碍设置页被拉起前；最有判别力的页面是**系统无障碍服务列表中的 “Google services” 条目**（标签 + description 双伪装 + 无警告横幅），以及紧随其后的引导说明页。

> 因硬性调用上限，本轮未写入风险台账（结论与证据已在上文与 JSON 中完整给出）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、无障碍配置 XML、resources.arsc 文案与 Application 桩代码静态可见；但真正执行引导的类 nilheart.ptur744.lens.gi5qN5xht_SWOTMtcfj 不在 classes.dex 中（Class.forName 后异常被吞），且全部 81 个 assets 条目（含 assets/www/index.html、inject.js、YgIheO.json、googleinfo.txt）以 PKZIP 传统加密存储，DEX 内不存在 ACTION_ACCESSIBILITY_SETTINGS 跳转字符串，故无障碍设置跳转、引导页与遮罩逻辑均无法静态还原。",
  "summary_one_liner": "该应用把自身与无障碍服务同时伪装成“Google services”，用“必须启用否则无法正常运行 + 杀毒软件会误报”的文案在冷启动即引导用户进入系统无障碍页开启全量监听服务，并以 isAccessibilityTool=true 伪造辅助工具属性规避系统警告，真实引导页面与载荷藏于加密资产与运行期投放类中。",
  "disguise_identity": {
    "app_display_name": "Google services",
    "claimed_brand_or_persona": "Google Play services / Google services（Google 官方服务组件）",
    "a11y_service_label": "Google services",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:isAccessibilityTool=\"true\" 伪造“辅助工具类”以在 Android 14+ 隐藏警告并归入“已下载的应用”；服务名与类名完全无关（V_mhElDCXAww9C）；Application 桩类通过反射替换 ContextImpl.mOuterContext / LoadedApk.mApplication 劫持 Application 实例；多个 noHistory+excludeFromRecents+launchMode=singleInstance 的隐形 Activity（c9XPJ2hRrGd0Ax3hb、o9PA、Zbm8h84T8NFeyVIbTm1、K03QONwX6QdSwTYY）与 StubActivity 作跳板；宿主为被二次打包的 MediaConverter 应用，包名 nilheart.ptur744.lens 与“Google”无任何关联。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.dynamic.human.Jfetchbarrel（android:name 指向的 Application）",
      "trigger_event": "Application.onCreate()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，仅执行初始化",
      "user_action_requested": "无",
      "code_anchor": "com.dynamic.human.Jfetchbarrel#onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "Jfetchbarrel.bambooprocess(String) 反射链：Class.forName(\"nilheart.ptur744.lens.gi5qN5xht_SWOTMtcfj\") → 改写 ContextImpl.mOuterContext / LoadedApk.mApplication → application.onCreate()",
      "trigger_event": "onCreate 内调用 bambooprocess，且无条件 return true（异常被 catch 吞掉）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "目标类不在 classes.dex 中，真实业务与引导流程由运行期投放后接管",
      "user_action_requested": "无",
      "code_anchor": "com.dynamic.human.Jfetchbarrel#bambooprocess"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "冷启动后立即弹出的无障碍开启说明（推测为 assets/www/index.html WebView 或原生 Dialog，资产加密不可读）",
      "trigger_event": "按文案“Immediately after running the application”即冷启动后立即触发",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Immediately after running the application, the Accessibility aid menu will open. To prevent the steady operation of this application from interfering with other third-party applications (for example, malware or too strict antivirus policy), a special option shall be enabled that will help avoid conflicts.",
      "shown_text_zh": "运行本应用后无障碍辅助菜单将立即打开。为防止本应用的稳定运行受到其他第三方应用干扰（例如恶意软件或过于严格的杀毒策略），需要启用一个特殊选项以避免冲突。",
      "user_action_requested": "按提示前往无障碍菜单开启服务，并忽略可能出现的安全警告；无可见取消/跳过路径",
      "code_anchor": "resources.arsc 字符串（无障碍引导说明）；assets/www/index.html（PKZIP 加密）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载的服务 → “Google services”",
      "trigger_event": "运行期载荷发起 ACTION_ACCESSIBILITY_SETTINGS（DEX 内无该字符串，由投放类执行）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google services",
      "shown_text_zh": "无障碍服务列表中显示条目名“Google services”",
      "user_action_requested": "点选该条目进入开关页并打开开关",
      "code_anchor": "AndroidManifest.xml service nilheart.ptur744.lens.V_mhElDCXAww9C label=@7F0E001C"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "服务详情/开关页下方说明文本（android:description）",
      "trigger_event": "用户在列表中展开或进入服务详情",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "This option shall be enabled. This is very important for the correct and steady operation of the application.",
      "shown_text_zh": "必须启用此选项。这对本应用的正确与稳定运行非常重要。",
      "user_action_requested": "开启开关；文案只强调“必须启用”，未提供拒绝或替代方案",
      "code_anchor": "res/xml/accessibilityservice.xml android:description=@7F0E001B"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "未静态可见（引导与重试逻辑在加密资产/运行期投放类中）",
      "trigger_event": "不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无法确认是否 onResume 死循环重跳或定时拉起",
      "user_action_requested": "不可静态还原",
      "code_anchor": "无（受加密资产阻断）"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 V_mhElDCXAww9C（全事件监听 + 窗口内容读取 + 手势注入 + 截图）及 DeviceAdmin/输入法/通知监听/VPN 组件",
      "trigger_event": "服务 onServiceConnected 后由投放载荷驱动（不可静态还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后具备读取任意界面文本、模拟点击与截图能力，配合 DeviceAdmin 具备撤权抵抗条件",
      "user_action_requested": "不可静态还原",
      "code_anchor": "res/xml/accessibilityservice.xml；res/xml/device_admin.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目名：AndroidManifest.xml 中 service V_mhElDCXAww9C 的 android:label=@7F0E001C → “Google services”",
    "系统无障碍服务详情/开关页说明文本：res/xml/accessibilityservice.xml 的 android:description=@7F0E001B → “This option shall be enabled. This is very important for the correct and steady operation of the application.”",
    "冷启动引导说明（预期为本地 WebView 或原生 Dialog）：resources.arsc 中 “Immediately after running the application, the Accessibility aid menu will open...”（对应 assets/www/index.html，PKZIP 加密不可读）",
    "伪装为系统/Google 组件的弹窗文案：Google Play services 库资源字符串（“Enable Google Play services”、“%1$s won't work unless you enable Google Play services.”、“New version of Google Play services needed. It will update itself shortly.”）",
    "桌面图标名称：AndroidManifest.xml application android:label=@7F0E0021 → “Google services”"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "This option shall be enabled. This is very important for the correct and steady operation of the application.",
      "text_zh": "必须启用此选项。这对本应用的正确与稳定运行非常重要。",
      "source_location": "res/xml/accessibilityservice.xml android:description → resources.arsc @7F0E001B",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Immediately after running the application, the Accessibility aid menu will open. To prevent the steady operation of this application from interfering with other third-party applications (for example, malware or too strict antivirus policy), a special option shall be enabled that will help avoid conflicts.",
      "text_zh": "运行本应用后无障碍辅助菜单将立即打开。为防止本应用的稳定运行受到其他第三方应用干扰（例如恶意软件或过于严格的杀毒策略），需要启用一个特殊选项以避免冲突。",
      "source_location": "resources.arsc 字符串（无障碍引导说明）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Google services",
      "text_zh": "Google 服务",
      "source_location": "AndroidManifest.xml application android:label=@7F0E0021；service V_mhElDCXAww9C android:label=@7F0E001C",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "除非启用 Google Play 服务，否则 %1$s 无法工作。",
      "source_location": "resources.arsc（Google Play services 库字符串）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "New version of Google Play services needed. It will update itself shortly.",
      "text_zh": "需要新版本的 Google Play 服务，它将很快自行更新。",
      "source_location": "resources.arsc（Google Play services 库字符串）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：引导与重试逻辑位于加密资产与运行期投放类（nilheart.ptur744.lens.gi5qN5xht_SWOTMtcfj）中，DEX 内无 ACTION_ACCESSIBILITY_SETTINGS 及 onResume 重跳代码，无法确认是否死循环拉起；但服务声明 noHistory/excludeFromRecents 的多个隐形 Activity 与 StubActivity 具备反复拉起条件。",
    "overlay_or_fake_settings": "静态不可见：DEX 内无 SYSTEM_ALERT_WINDOW 使用点与遮罩布局调用；overlay 线索初筛为空，遮罩/高仿设置页（若存在）在加密资产或投放类中。",
    "restricted_settings_13plus_coaching": "无直接证据：DEX 中仅宿主遗留代码使用 ACTION_APPLICATION_DETAILS_SETTINGS（com.fundevs.app.mediaconverter.BaseActivity#L、MediaActivity#G0），是否用于引导“允许受限设置”无法确认；无障碍开启路径的受限设置教学不可静态还原。",
    "post_grant_anti_removal": "具备条件但未静态闭环：同时申请 DeviceAdmin（wipe-data、reset-password、force-lock、disable-camera 等）与无障碍全量事件/手势注入，具备阻止撤权能力；具体自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权代码在加密载荷中，不可静态确认。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后监测到当前 Activity 变为 com.android.settings/.Settings$AccessibilitySettings 或 AccessibilityDetailsSettings（即 ACTION_ACCESSIBILITY_SETTINGS 触发瞬间）时立刻抓取；其次在 Application 初始化完成后的首帧（Jfetchbarrel.onCreate 之后）开始连续抓取，以捕获其前置引导页。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → 无障碍 → 已下载的服务 中出现名称“Google services”的条目（对应 nilheart.ptur744.lens.V_mhElDCXAww9C）",
        "why_most_useful": "这是品牌冒充与 isAccessibilityTool 伪造的最终呈现点，UTG 可同时取到应用名、服务名与说明文本三者一致伪装的证据",
        "observable_utg_signals": ["服务条目文本 “Google services”", "服务条目对应的包名 nilheart.ptur744.lens 与显示名不一致", "条目未出现系统高危警告横幅（isAccessibilityTool=true 生效）"]
      },
      {
        "page_role": "冷启动引导弹窗页 / 跳转前教学页",
        "page_identifier": "冷启动后首个非宿主业务页面，内容含“Accessibility aid menu will open”“very important for the correct and steady operation”",
        "why_most_useful": "决定是否存在冷启动 0 步阻断式诱导，以及话术是否教唆忽视杀毒软件警告；该页面在静态层被加密资产隐藏，只能靠 UTG 获取",
        "observable_utg_signals": ["弹窗/页面文本是否含 accessibility 与 antivirus/malware 话术", "是否存在取消/跳过按钮", "承载控件类型为 WebView 还是原生 Dialog"]
      },
      {
        "page_role": "设置页后压栈遮罩页",
        "page_identifier": "跳转系统无障碍页后 500–1000ms 内出现的悬浮窗或高仿开关页（SYSTEM_ALERT_WINDOW 已声明）",
        "why_most_useful": "用于判定是否存在遮罩叠层指引或伪造系统开关页，这是静态层完全缺失的一环",
        "observable_utg_signals": ["窗口是否属于 nilheart.ptur744.lens 且覆盖在 settings 之上", "遮罩文本是否为指引箭头/“点击此处开启”", "返回键后是否再次压栈"]
      },
      {
        "page_role": "拒权返回后的反馈页",
        "page_identifier": "从无障碍页返回宿主 App 时立刻出现的页面或再次跳转动作",
        "why_most_useful": "判定拒权循环强度（死循环重跳 / 定时拉起 / 良性降级）",
        "observable_utg_signals": ["返回后 N 秒内是否再次进入 settings 包名页面", "是否出现“必须开启”类阻断文案", "是否存在退出应用的唯一出路"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区：全部 81 个 assets（含 assets/www/index.html、inject.js、YgIheO.json、googleinfo.txt）为 PKZIP 加密存储，DEX 内真实业务类缺失且无 ACTION_ACCESSIBILITY_SETTINGS 字符串，静态无法还原引导页与遮罩；此外存在被二次打包的良性宿主（MediaConverter）代码与 Google Play services 库资源，易造成“看似正常”的误判。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.dynamic.human.Jfetchbarrel#onCreate",
    "com.dynamic.human.Jfetchbarrel#bambooprocess",
    "res/xml/accessibilityservice.xml（android:isAccessibilityTool=\"true\"，canTakeScreenshot/canPerformGestures/canRetrieveWindowContent）",
    "AndroidManifest.xml（service nilheart.ptur744.lens.V_mhElDCXAww9C label=@7F0E001C；application label=@7F0E0021 “Google services”）",
    "resources.arsc（android:description @7F0E001B 与无障碍冷启动引导文案）",
    "assets/www/index.html、assets/YgIheO.json、assets/googleinfo.txt（PKZIP 加密，未解密）"
  ]
}
```

</details>

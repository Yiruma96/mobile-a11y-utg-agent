# MR_152__4dd7e249e5｜GhostClicker — Assistive Touch

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：179.9s

## 1. 一句话核心结论

- **核心申请方式**：该样本不存在无障碍权限引导链——Manifest 无 accessibilityservice，ACTION_ACCESSIBILITY_SETTINGS 只是工具类'设置快捷方式'网格中的一项；其真实诱导对象是冷启动强制跳转的 SYSTEM_ALERT_WINDOW 悬浮窗授权（拒绝后无限重跳），真正的恶意部分在伪装 com.google.android.gms 的 DeviceAdmin 后台组件与加密 DexClassLoader 载荷。
- **静态可见性说明**：应用自身逻辑（Manifest、全部 Activity/Service、strings、布局）完整静态可见且已确认无无障碍服务；但 com.google.android.gms.b.w#l 通过 I.a() 解密字节流写入 cache 临时 .jar 后由 DexClassLoader 加载 13 个类并反射调用，其真实内容为密文/远端下发，静态不可还原；com.google.android.gms.logs 的 Logger 逻辑大量使用 Base64 混淆键，故无法在静态侧完全排除二阶段载荷运行期注入无障碍引导 UI。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `4dd7e249e5202c8fa6b53f3674547982adfaf773035d38beea45f39f9bdd4e77` |
| 包名 / 年份 | `dto.assistivetouch.touch` / 2017 |
| 家族 / 品类 | **GhostClicker**（同池样本数：4） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/h/ghostclicker-adware-is-a-phantomlike-android-click-fraud.html |
| 桌面显示名 | Assistive Touch |
| 引导页宣称品牌/身份 | Assistive Touch（iOS 风格悬浮球辅助工具）；同时内部代码伪装为 Google Mobile Services（com.google.android.gms.logs / com.google.android.gms.ads / Plus Service） |
| 系统无障碍列表服务名 | 无（未声明任何 AccessibilityService，系统无障碍列表中不会出现本应用条目） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：应用自身业务包名为 zxc.studio.assistivetouch，但恶意组件被放在 com.google.android.gms.logs 包下冒充 GMS；DeviceAdminReceiver 的 android:label 写作 'Plus Service' 且复用 abc_scrubber_control_to_pressed_mtrl_005 图标；DeviceAdmin 策略文件 res/xml/admin.xml 中 <uses-policies/> 为空，无实际策略，说明申请设备管理员仅用于反卸载持久化；字符串与 AlarmManager tag 均用 Base64 编码（如 Y3hYRHpjSjNHaFJ3Sm1EVXhzYWQ= / Y3hYRHpjSjNHaFJ3Sm1EVXN0YXR1cw==）；另存在一个以 android:name=com.google.android.gms.logs.Logger 命名的 Activity 冒充 SDK 日志组件。 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | zxc.studio.assistivetouch.ui.activity.MainActivity | onCreate(Bundle) | 原生Activity | **原文**：无（仅初始化界面与 AdView，无权限说明文案）<br>**译注**：无说明文字，直接进入主界面并触发权限流程 | 无（自动触发下一步） | `zxc.studio.assistivetouch.ui.activity.MainActivity#onCreate` |
| 2 | 业务功能触发 | MainActivity#a(Activity) → 系统 CAMERA 权限对话框 | onCreate 内调用 a(Activity)，Build.VERSION.SDK_INT>=23 且未授予 CAMERA 时 | 系统权限对话框 | **原文**：无自定义文案（系统标准相机权限弹窗）<br>**译注**：系统标准「是否允许访问相机」弹窗 | 允许/拒绝相机权限（系统原生按钮，可取消） | `zxc.studio.assistivetouch.ui.activity.MainActivity#a(android.app.Activity)` |
| 3 | 跳受限设置 | 系统「显示在其他应用上层」页（android.settings.action.MANAGE_OVERLAY_PERMISSION，package:dto.assistivetouch.touch） | onCreate 内 SDK_INT>=23 且 Settings.canDrawOverlays(this)==false 时调用 k() | 系统设置页 | **原文**：无自定义引导文案<br>**译注**：直接跳系统悬浮窗授权页，无前置解释弹窗 | 手动打开「允许显示在其他应用上层」开关（可返回取消） | `zxc.studio.assistivetouch.ui.activity.MainActivity#k` |
| 4 | 拒权反馈循环 | MainActivity.onActivityResult → 再次进入系统悬浮窗授权页 | onActivityResult 回调中 resultCode != RESULT_OK 时无条件调用 k() | 系统设置页（重复拉起） | **原文**：无提示文案<br>**译注**：用户拒绝或返回后立即再次跳转同一授权页，无提示、无跳过入口 | 只能再次面对授权页，无取消/跳过选项，形成弱拒绝循环 | `zxc.studio.assistivetouch.ui.activity.MainActivity#onActivityResult` |
| 5 | 获权后动作 | ChatHeadVirtualService / ChatHeadService / BubblesService（悬浮球） | onActivityResult 中 resultCode==RESULT_OK 且 canDrawOverlays() 为真时调用 p() → startService | 悬浮窗Overlay | **原文**：Start / Stop<br>**译注**：启动悬浮球服务，界面按钮文字变为 Stop | 无（自动启动），用户可点 Stop 停止 | `zxc.studio.assistivetouch.ui.activity.MainActivity#p` |
| 6 | 业务功能触发 | SettingsActivity 快捷设置网格 → 系统「无障碍」设置页 | 用户在快捷项列表中点击「Accessibility」项（onItemClick → startActivityForResult） | 系统无障碍页 | **原文**：Accessibility<br>**译注**：「无障碍」——仅作为用户可自定义的 40 余项系统设置快捷入口之一，点击后打开系统无障碍设置页，应用自身不在此页出现任何服务条目 | 用户自行选择（非应用强制、无引导文案、无服务可开启） | `zxc.studio.assistivetouch.ui.activity.SettingsActivity#k` |
| 7 | 获权后动作 | com.google.android.gms.logs.b（DeviceAdminReceiver，label='Plus Service'）→ AlarmManager → com.google.android.gms.logs.c | CONNECTIVITY_CHANGE / DEVICE_ADMIN_ENABLED 广播触发 onReceive，且距上次执行超过 21600000ms（6 小时） | 不可静态还原 | **原文**：To use lock screen feature go to advanced settings and ACTIVE Device Admin<br>**译注**：「要使用锁屏功能，请进入高级设置并激活设备管理员」——这是应用内唯一的设备管理员引导文案，与无障碍无关 | 要求用户前往系统高级设置激活设备管理员（用于反卸载持久化），激活后 onEnabled 写入 Base64 混淆键 Y3hYRHpjSjNHaFJ3Sm1EVXhzYWQ= | `com.google.android.gms.logs.b#onReceive` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- SettingsActivity 快捷设置网格项「Accessibility」（res/values/strings.xml:25，key=accessibility_settings，value='Accessibility'），仅作为系统设置快捷入口标题，非权限说明
- res/values/strings.xml:63（key=err_do_not_have_admin）：'To use lock screen feature go to advanced settings and ACTIVE Device Admin' —— 唯一的'去系统设置开启'类引导文案，指向设备管理员而非无障碍
- Toast 短提示（SettingsActivity.a(String)）：'App has no permission to access call phone.' / 'Your phone does not have this setting.' / 'Flashlight not available' 等，功能失败时弹出，无恐吓/假更新话术
- MainActivity 主界面 Start/Stop 按钮文字（硬编码 setText("Start")/setText("Stop")），无权限说明
- 系统标准 CAMERA 运行时权限弹窗（无自定义 rationale 文案，未调用 shouldShowRequestPermissionRationale）
- 系统标准 MANAGE_OVERLAY_PERMISSION 悬浮窗授权页（应用不叠加任何遮罩/引导悬浮窗，无高仿系统页）
- Google Ads SDK 内置字符串（'%1$s is having trouble with Google Play services...'、'Allow Ad to create a calendar event?'）位于三方广告 SDK 资源，与本应用权限引导无关

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Accessibility | 无障碍 | `res/values/strings.xml key=accessibility_settings (id 0x7f080016)` | 良性透明说明 |
| en | To use lock screen feature go to advanced settings and ACTIVE Device Admin | 要使用锁屏功能，请进入高级设置并激活设备管理员 | `res/values/strings.xml key=err_do_not_have_admin (id 0x7f080041)，由 LockActivity/AdminReceiver 相关流程引用` | 受限设置分步教学 |
| en | App has no permission to access call phone. | 应用没有拨打电话的权限。 | `res/values/strings.xml（Toast 文案，SettingsActivity.a(String) 调用）` | 良性透明说明 |
| en | Your phone does not have this setting. | 您的手机没有此设置项。 | `res/values/strings.xml（Toast 文案，SettingsActivity.a(String) 调用）` | 良性透明说明 |
| en | Plus Service | Plus 服务 | `AndroidManifest.xml 中 receiver com.google.android.gms.logs.b 的 android:label` | 未知 |
| en | %1$s is having trouble with Google Play services. If the problem persists, please contact the developer for assistance. | %1$s 使用 Google Play 服务时遇到问题。若问题持续，请联系开发者获取帮助。 | `Google Ads SDK 资源（com.google.android.gms.ads，三方 SDK）` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：针对 SYSTEM_ALERT_WINDOW：MainActivity.onActivityResult 中只要 resultCode != RESULT_OK 就无条件再次调用 k() 拉起 MANAGE_OVERLAY_PERMISSION，用户返回/拒绝即被立刻重新跳转，无 Toast 说明、无跳过按钮，形成弱死循环（可通过按 Home 键脱离）。针对无障碍：不存在任何循环或重跳逻辑，因为应用根本没有无障碍引导流程。
- **遮罩叠层 / 高仿系统设置页**：无。全包未发现半透明引导遮罩、全屏悬浮窗模拟系统无障碍开关页或高仿系统设置页；SYSTEM_ALERT_WINDOW 仅用于 Assistive Touch 悬浮球（ChatHeadService/BubblesService）与广告浮层。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全包唯一的 APPLICATION_DETAILS_SETTINGS 跳转位于 Google Ads SDK（com.google.android.gms.common.internal.z#a），属 SDK 通用错误引导，不含「点右上角菜单允许受限设置」类文案；无 SESSION_INSTALLER 绕过实现（预筛 restricted 标记与本轮代码核验不一致）。
- **获权后即时行为与防撤权机制**：针对无障碍：无（无 GLOBAL_ACTION_BACK/HOME 撤权阻断，无无障碍服务故无从谈起）。但存在等效反移除机制：伪装为 'Plus Service' 的 DeviceAdminReceiver com.google.android.gms.logs.b 通过空策略 admin.xml 申请设备管理员，onDisabled 仅改写 Base64 键 Y3hYRHpjSjNHaFJ3Sm1EVXhzYWQ= 标记状态，配合每 6 小时 AlarmManager 拉起的 c 服务实现卸载阻力与自恢复。
- **良性降级 / 替代方案**：无。悬浮窗授权被拒后不提供手动模式、ADB 指引或只读降级路径，而是立即重跳系统授权页。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：纯 UTG 检测不应以无障碍为触发点（本样本无该能力）。应监测两类瞬间：① 冷启动后首次出现 MANAGE_OVERLAY_PERMISSION 系统页（package:dto.assistivetouch.touch）——这是唯一的强制授权跳转；② 该页返回后 0~1s 内是否再次出现同一页面（拒绝循环判定）。如需验证二阶段载荷是否注入无障碍引导，则在 DexClassLoader 加载完成后（cache 目录出现 ads*.jar/.dex）再持续监听 ACCESSIBILITY_SETTINGS 跳转。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：① 应用自身无无障碍组件，若检测策略只按'无障碍引导'维度建模，将完全漏判本样本真实的悬浮窗强制授权 + 伪装 GMS 的 DeviceAdmin 持久化行为；② com.google.android.gms.b.w#l 的 DexClassLoader 载荷为密文（I.a 解密），二阶段是否在运行期注入无障碍引导/悬浮窗诱导 UI 无法静态确认，需 UTG 结合 cache 目录落盘的 ads*.jar 与后续页面流转观测；③ com.google.android.gms.logs 的 Logger 大量 Base64 混淆，其远控下发内容不可静态还原，属部分动态可见。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动强制跳转的悬浮窗授权页（唯一强制权限页）** | 系统页标题含「显示在其他应用上层」/Draw over other apps，且包名为 dto.assistivetouch.touch | 该页是应用唯一的强制权限跳转，且无前置说明弹窗，可直接判定是否存在'裸跳受限设置'行为 | packageName=dto.assistivetouch.touch 出现在设置页目标中；页面无任何应用自绘的说明浮层（区别于诱导型样本的遮罩）；开关初始状态为关闭 |
| **拒绝后二次/三次跳转的同一授权页（拒绝循环判定）** | 返回键或拒绝开关后 ≤1s 内再次出现同一 MANAGE_OVERLAY_PERMISSION 页面 | onActivityResult 无条件重跳是本样本唯一的强制性设计证据，UTG 时序可直观量化循环次数 | 同一 Activity 在返回后立即重新压栈；全程无 Toast/对话框解释；无'跳过'或'稍后'控件 |
| **SettingsActivity 快捷设置网格（'Accessibility' 条目所在页）** | 顶部 Toolbar 为 Assistive Touch 的 GridView 网格，包含 Settings/APN/Accessibility/Battery saver 等条目 | 用于证明 ACCESSIBILITY_SETTINGS 只是用户可编辑的快捷方式项，而非权限诱导入口，是排除误判的关键反证页面 | 网格内同时存在 40+ 个系统设置快捷项；点击'Accessibility'仅打开系统无障碍设置页，页面内无本应用服务条目；页面提供自定义/编辑快捷项能力（长按或编辑按钮） |
| **设备管理员激活页（真实'去系统设置'引导文案所在处）** | 系统「激活设备管理员」页，显示应用名 Assistive Touch，触发源为 label='Plus Service' 的 receiver | 该页是本样本唯一的'引导用户去系统设置开启高危权限'行为，替代无障碍成为真正的诱导判定对象 | 系统页标题含「设备管理员」/Device admin；应用内前置 Toast 文案 'To use lock screen feature go to advanced settings and ACTIVE Device Admin'；激活后应用缓存中 Base64 键 xsd 状态被置 true |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `zxc.studio.assistivetouch.ui.activity.MainActivity#k`
- `zxc.studio.assistivetouch.ui.activity.MainActivity#onActivityResult`
- `zxc.studio.assistivetouch.ui.activity.SettingsActivity#k`
- `com.google.android.gms.logs.b#onReceive`
- `com.google.android.gms.b.w#l`
- `res/values/strings.xml key=err_do_not_have_admin / res/xml/admin.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**核心判断：该样本不存在无障碍（Accessibility）权限引导链，纯运行期 UTG 视角下“引导开启无障碍”的假设不成立。**

1. **Manifest 层无任何无障碍组件**：没有 `android.accessibilityservice` service 声明，没有 `BIND_ACCESSIBILITY_SERVICE` 权限，没有 `accessibility-service` 元数据 XML；`app_label="Assistive Touch"`，与显示名一致，无空白/同形字伪装。
2. **`ACCESSIBILITY_SETTINGS` 仅是一处“设置快捷方式”条目**：在 [SettingsActivity.k()](<resource-unit:#1.dex1 code:zxc.studio.assistivetouch.ui.activity.SettingsActivity#k>) 中，它与 `SETTINGS`、`APN_SETTINGS`、`BATTERY_SAVER_SETTINGS` 等 40 余项一起被塞进可自定义的网格快捷列表；点击后只是普通 `startActivityForResult` 打开系统设置页，属工具类“快捷开关”功能，非权限诱导。
3. **`APPLICATION_DETAILS_SETTINGS` 的唯一引用位于 Google Ads SDK 内部**（`com.google.android.gms.common.internal.z#a`），与无障碍/受限设置教学无关，属三方 SDK 通用跳转，不构成 `RESTRICTED_SETTINGS` 教学链。
4. **真正的权限引导对象是悬浮窗而非无障碍**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:zxc.studio.assistivetouch.ui.activity.MainActivity#onCreate>) → [MainActivity.k()](<resource-unit:#1.dex1 code:zxc.studio.assistivetouch.ui.activity.MainActivity#k>) 在 `SDK_INT>=23` 且 `!Settings.canDrawOverlays()` 时直接拉起 `ACTION_MANAGE_OVERLAY_PERMISSION`；[onActivityResult()](<resource-unit:#1.dex1 code:zxc.studio.assistivetouch.ui.activity.MainActivity#onActivityResult>) 在用户拒绝（`resultCode != -1`）时**无条件再次调用 `k()` 重跳**，形成弱拒绝循环。文案仅 Toast（"App has no permission to access call phone." 等），无恐吓/假更新话术。
5. **高危发现不在无障碍，而在伪装 GMS 的后台组件**：`com.google.android.gms.logs.b` 是 `DeviceAdminReceiver`，标签写作 `Plus Service`（图标复用 `abc_scrubber_control_to_pressed_mtrl_005`），`onReceive` 用 Base64 混淆键（如 `Y3hYRHpjSjNHaFJ3Sm1EVXhzYWQ=`）记录状态，并以 `AlarmManager` 每 6 小时拉起 `c` 服务；`com.google.android.gms.b.w#l` 通过 `I.a(...)` 解密字节、写临时 jar 后用 `DexClassLoader` 加载 13 个类并反射取 13 个方法——**载荷内容为远端/密文，静态不可还原**。
6. **局限**：解密后的 dex 与 `Logger` 的真实远控/下载逻辑不可静态获取，故“无障碍是否由二阶段载荷在运行期注入”只能在 UTG 层验证，无法在静态侧否定到 100%。

---

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "应用自身逻辑（Manifest、全部 Activity/Service、strings、布局）完整静态可见且已确认无无障碍服务；但 com.google.android.gms.b.w#l 通过 I.a() 解密字节流写入 cache 临时 .jar 后由 DexClassLoader 加载 13 个类并反射调用，其真实内容为密文/远端下发，静态不可还原；com.google.android.gms.logs 的 Logger 逻辑大量使用 Base64 混淆键，故无法在静态侧完全排除二阶段载荷运行期注入无障碍引导 UI。",
  "summary_one_liner": "该样本不存在无障碍权限引导链——Manifest 无 accessibilityservice，ACTION_ACCESSIBILITY_SETTINGS 只是工具类'设置快捷方式'网格中的一项；其真实诱导对象是冷启动强制跳转的 SYSTEM_ALERT_WINDOW 悬浮窗授权（拒绝后无限重跳），真正的恶意部分在伪装 com.google.android.gms 的 DeviceAdmin 后台组件与加密 DexClassLoader 载荷。",
  "disguise_identity": {
    "app_display_name": "Assistive Touch",
    "claimed_brand_or_persona": "Assistive Touch（iOS 风格悬浮球辅助工具）；同时内部代码伪装为 Google Mobile Services（com.google.android.gms.logs / com.google.android.gms.ads / Plus Service）",
    "a11y_service_label": "无（未声明任何 AccessibilityService，系统无障碍列表中不会出现本应用条目）",
    "identity_mismatch": true,
    "obfuscation_tricks": "应用自身业务包名为 zxc.studio.assistivetouch，但恶意组件被放在 com.google.android.gms.logs 包下冒充 GMS；DeviceAdminReceiver 的 android:label 写作 'Plus Service' 且复用 abc_scrubber_control_to_pressed_mtrl_005 图标；DeviceAdmin 策略文件 res/xml/admin.xml 中 <uses-policies/> 为空，无实际策略，说明申请设备管理员仅用于反卸载持久化；字符串与 AlarmManager tag 均用 Base64 编码（如 Y3hYRHpjSjNHaFJ3Sm1EVXhzYWQ= / Y3hYRHpjSjNHaFJ3Sm1EVXN0YXR1cw==）；另存在一个以 android:name=com.google.android.gms.logs.Logger 命名的 Activity 冒充 SDK 日志组件。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "zxc.studio.assistivetouch.ui.activity.MainActivity",
      "trigger_event": "onCreate(Bundle)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（仅初始化界面与 AdView，无权限说明文案）",
      "shown_text_zh": "无说明文字，直接进入主界面并触发权限流程",
      "user_action_requested": "无（自动触发下一步）",
      "code_anchor": "zxc.studio.assistivetouch.ui.activity.MainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity#a(Activity) → 系统 CAMERA 权限对话框",
      "trigger_event": "onCreate 内调用 a(Activity)，Build.VERSION.SDK_INT>=23 且未授予 CAMERA 时",
      "ui_carrier": "系统权限对话框",
      "shown_text_verbatim": "无自定义文案（系统标准相机权限弹窗）",
      "shown_text_zh": "系统标准「是否允许访问相机」弹窗",
      "user_action_requested": "允许/拒绝相机权限（系统原生按钮，可取消）",
      "code_anchor": "zxc.studio.assistivetouch.ui.activity.MainActivity#a(android.app.Activity)"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统「显示在其他应用上层」页（android.settings.action.MANAGE_OVERLAY_PERMISSION，package:dto.assistivetouch.touch）",
      "trigger_event": "onCreate 内 SDK_INT>=23 且 Settings.canDrawOverlays(this)==false 时调用 k()",
      "ui_carrier": "系统设置页",
      "shown_text_verbatim": "无自定义引导文案",
      "shown_text_zh": "直接跳系统悬浮窗授权页，无前置解释弹窗",
      "user_action_requested": "手动打开「允许显示在其他应用上层」开关（可返回取消）",
      "code_anchor": "zxc.studio.assistivetouch.ui.activity.MainActivity#k"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity.onActivityResult → 再次进入系统悬浮窗授权页",
      "trigger_event": "onActivityResult 回调中 resultCode != RESULT_OK 时无条件调用 k()",
      "ui_carrier": "系统设置页（重复拉起）",
      "shown_text_verbatim": "无提示文案",
      "shown_text_zh": "用户拒绝或返回后立即再次跳转同一授权页，无提示、无跳过入口",
      "user_action_requested": "只能再次面对授权页，无取消/跳过选项，形成弱拒绝循环",
      "code_anchor": "zxc.studio.assistivetouch.ui.activity.MainActivity#onActivityResult"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "ChatHeadVirtualService / ChatHeadService / BubblesService（悬浮球）",
      "trigger_event": "onActivityResult 中 resultCode==RESULT_OK 且 canDrawOverlays() 为真时调用 p() → startService",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Start / Stop",
      "shown_text_zh": "启动悬浮球服务，界面按钮文字变为 Stop",
      "user_action_requested": "无（自动启动），用户可点 Stop 停止",
      "code_anchor": "zxc.studio.assistivetouch.ui.activity.MainActivity#p"
    },
    {
      "step": 6,
      "stage": "业务功能触发",
      "screen_or_component": "SettingsActivity 快捷设置网格 → 系统「无障碍」设置页",
      "trigger_event": "用户在快捷项列表中点击「Accessibility」项（onItemClick → startActivityForResult）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Accessibility",
      "shown_text_zh": "「无障碍」——仅作为用户可自定义的 40 余项系统设置快捷入口之一，点击后打开系统无障碍设置页，应用自身不在此页出现任何服务条目",
      "user_action_requested": "用户自行选择（非应用强制、无引导文案、无服务可开启）",
      "code_anchor": "zxc.studio.assistivetouch.ui.activity.SettingsActivity#k"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.google.android.gms.logs.b（DeviceAdminReceiver，label='Plus Service'）→ AlarmManager → com.google.android.gms.logs.c",
      "trigger_event": "CONNECTIVITY_CHANGE / DEVICE_ADMIN_ENABLED 广播触发 onReceive，且距上次执行超过 21600000ms（6 小时）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "To use lock screen feature go to advanced settings and ACTIVE Device Admin",
      "shown_text_zh": "「要使用锁屏功能，请进入高级设置并激活设备管理员」——这是应用内唯一的设备管理员引导文案，与无障碍无关",
      "user_action_requested": "要求用户前往系统高级设置激活设备管理员（用于反卸载持久化），激活后 onEnabled 写入 Base64 混淆键 Y3hYRHpjSjNHaFJ3Sm1EVXhzYWQ=",
      "code_anchor": "com.google.android.gms.logs.b#onReceive"
    }
  ],
  "text_presentation_locations": [
    "SettingsActivity 快捷设置网格项「Accessibility」（res/values/strings.xml:25，key=accessibility_settings，value='Accessibility'），仅作为系统设置快捷入口标题，非权限说明",
    "res/values/strings.xml:63（key=err_do_not_have_admin）：'To use lock screen feature go to advanced settings and ACTIVE Device Admin' —— 唯一的'去系统设置开启'类引导文案，指向设备管理员而非无障碍",
    "Toast 短提示（SettingsActivity.a(String)）：'App has no permission to access call phone.' / 'Your phone does not have this setting.' / 'Flashlight not available' 等，功能失败时弹出，无恐吓/假更新话术",
    "MainActivity 主界面 Start/Stop 按钮文字（硬编码 setText(\"Start\")/setText(\"Stop\")），无权限说明",
    "系统标准 CAMERA 运行时权限弹窗（无自定义 rationale 文案，未调用 shouldShowRequestPermissionRationale）",
    "系统标准 MANAGE_OVERLAY_PERMISSION 悬浮窗授权页（应用不叠加任何遮罩/引导悬浮窗，无高仿系统页）",
    "Google Ads SDK 内置字符串（'%1$s is having trouble with Google Play services...'、'Allow Ad to create a calendar event?'）位于三方广告 SDK 资源，与本应用权限引导无关"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Accessibility",
      "text_zh": "无障碍",
      "source_location": "res/values/strings.xml key=accessibility_settings (id 0x7f080016)",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "To use lock screen feature go to advanced settings and ACTIVE Device Admin",
      "text_zh": "要使用锁屏功能，请进入高级设置并激活设备管理员",
      "source_location": "res/values/strings.xml key=err_do_not_have_admin (id 0x7f080041)，由 LockActivity/AdminReceiver 相关流程引用",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "App has no permission to access call phone.",
      "text_zh": "应用没有拨打电话的权限。",
      "source_location": "res/values/strings.xml（Toast 文案，SettingsActivity.a(String) 调用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Your phone does not have this setting.",
      "text_zh": "您的手机没有此设置项。",
      "source_location": "res/values/strings.xml（Toast 文案，SettingsActivity.a(String) 调用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Plus Service",
      "text_zh": "Plus 服务",
      "source_location": "AndroidManifest.xml 中 receiver com.google.android.gms.logs.b 的 android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s is having trouble with Google Play services. If the problem persists, please contact the developer for assistance.",
      "text_zh": "%1$s 使用 Google Play 服务时遇到问题。若问题持续，请联系开发者获取帮助。",
      "source_location": "Google Ads SDK 资源（com.google.android.gms.ads，三方 SDK）",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "针对 SYSTEM_ALERT_WINDOW：MainActivity.onActivityResult 中只要 resultCode != RESULT_OK 就无条件再次调用 k() 拉起 MANAGE_OVERLAY_PERMISSION，用户返回/拒绝即被立刻重新跳转，无 Toast 说明、无跳过按钮，形成弱死循环（可通过按 Home 键脱离）。针对无障碍：不存在任何循环或重跳逻辑，因为应用根本没有无障碍引导流程。",
    "overlay_or_fake_settings": "无。全包未发现半透明引导遮罩、全屏悬浮窗模拟系统无障碍开关页或高仿系统设置页；SYSTEM_ALERT_WINDOW 仅用于 Assistive Touch 悬浮球（ChatHeadService/BubblesService）与广告浮层。",
    "restricted_settings_13plus_coaching": "无。全包唯一的 APPLICATION_DETAILS_SETTINGS 跳转位于 Google Ads SDK（com.google.android.gms.common.internal.z#a），属 SDK 通用错误引导，不含「点右上角菜单允许受限设置」类文案；无 SESSION_INSTALLER 绕过实现（预筛 restricted 标记与本轮代码核验不一致）。",
    "post_grant_anti_removal": "针对无障碍：无（无 GLOBAL_ACTION_BACK/HOME 撤权阻断，无无障碍服务故无从谈起）。但存在等效反移除机制：伪装为 'Plus Service' 的 DeviceAdminReceiver com.google.android.gms.logs.b 通过空策略 admin.xml 申请设备管理员，onDisabled 仅改写 Base64 键 Y3hYRHpjSjNHaFJ3Sm1EVXhzYWQ= 标记状态，配合每 6 小时 AlarmManager 拉起的 c 服务实现卸载阻力与自恢复。",
    "benign_graceful_degradation": "无。悬浮窗授权被拒后不提供手动模式、ADB 指引或只读降级路径，而是立即重跳系统授权页。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "纯 UTG 检测不应以无障碍为触发点（本样本无该能力）。应监测两类瞬间：① 冷启动后首次出现 MANAGE_OVERLAY_PERMISSION 系统页（package:dto.assistivetouch.touch）——这是唯一的强制授权跳转；② 该页返回后 0~1s 内是否再次出现同一页面（拒绝循环判定）。如需验证二阶段载荷是否注入无障碍引导，则在 DexClassLoader 加载完成后（cache 目录出现 ads*.jar/.dex）再持续监听 ACCESSIBILITY_SETTINGS 跳转。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动强制跳转的悬浮窗授权页（唯一强制权限页）",
        "page_identifier": "系统页标题含「显示在其他应用上层」/Draw over other apps，且包名为 dto.assistivetouch.touch",
        "why_most_useful": "该页是应用唯一的强制权限跳转，且无前置说明弹窗，可直接判定是否存在'裸跳受限设置'行为",
        "observable_utg_signals": [
          "packageName=dto.assistivetouch.touch 出现在设置页目标中",
          "页面无任何应用自绘的说明浮层（区别于诱导型样本的遮罩）",
          "开关初始状态为关闭"
        ]
      },
      {
        "page_role": "拒绝后二次/三次跳转的同一授权页（拒绝循环判定）",
        "page_identifier": "返回键或拒绝开关后 ≤1s 内再次出现同一 MANAGE_OVERLAY_PERMISSION 页面",
        "why_most_useful": "onActivityResult 无条件重跳是本样本唯一的强制性设计证据，UTG 时序可直观量化循环次数",
        "observable_utg_signals": [
          "同一 Activity 在返回后立即重新压栈",
          "全程无 Toast/对话框解释",
          "无'跳过'或'稍后'控件"
        ]
      },
      {
        "page_role": "SettingsActivity 快捷设置网格（'Accessibility' 条目所在页）",
        "page_identifier": "顶部 Toolbar 为 Assistive Touch 的 GridView 网格，包含 Settings/APN/Accessibility/Battery saver 等条目",
        "why_most_useful": "用于证明 ACCESSIBILITY_SETTINGS 只是用户可编辑的快捷方式项，而非权限诱导入口，是排除误判的关键反证页面",
        "observable_utg_signals": [
          "网格内同时存在 40+ 个系统设置快捷项",
          "点击'Accessibility'仅打开系统无障碍设置页，页面内无本应用服务条目",
          "页面提供自定义/编辑快捷项能力（长按或编辑按钮）"
        ]
      },
      {
        "page_role": "设备管理员激活页（真实'去系统设置'引导文案所在处）",
        "page_identifier": "系统「激活设备管理员」页，显示应用名 Assistive Touch，触发源为 label='Plus Service' 的 receiver",
        "why_most_useful": "该页是本样本唯一的'引导用户去系统设置开启高危权限'行为，替代无障碍成为真正的诱导判定对象",
        "observable_utg_signals": [
          "系统页标题含「设备管理员」/Device admin",
          "应用内前置 Toast 文案 'To use lock screen feature go to advanced settings and ACTIVE Device Admin'",
          "激活后应用缓存中 Base64 键 xsd 状态被置 true"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：① 应用自身无无障碍组件，若检测策略只按'无障碍引导'维度建模，将完全漏判本样本真实的悬浮窗强制授权 + 伪装 GMS 的 DeviceAdmin 持久化行为；② com.google.android.gms.b.w#l 的 DexClassLoader 载荷为密文（I.a 解密），二阶段是否在运行期注入无障碍引导/悬浮窗诱导 UI 无法静态确认，需 UTG 结合 cache 目录落盘的 ads*.jar 与后续页面流转观测；③ com.google.android.gms.logs 的 Logger 大量 Base64 混淆，其远控下发内容不可静态还原，属部分动态可见。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_FEATURE_ON_DEMAND",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "zxc.studio.assistivetouch.ui.activity.MainActivity#k",
    "zxc.studio.assistivetouch.ui.activity.MainActivity#onActivityResult",
    "zxc.studio.assistivetouch.ui.activity.SettingsActivity#k",
    "com.google.android.gms.logs.b#onReceive",
    "com.google.android.gms.b.w#l",
    "res/values/strings.xml key=err_do_not_have_admin / res/xml/admin.xml"
  ]
}
```

</details>

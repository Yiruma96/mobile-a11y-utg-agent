# MR_051__57881f388f｜MonitorMinor — Google Service

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：104.3s

## 1. 一句话核心结论

- **核心申请方式**：该应用冒充“Google Service”，先以红绿清单式权限页强制申请 9 项危险权限并跳悬浮窗授权，再在“Settings”偏好页以勾选项引导用户跳转系统无障碍设置开启名为 Google Service、描述为 Receiver 的无障碍服务，返回未开启即被线程反复拉回。
- **静态可见性说明**：全流程静态可见：APK 未加壳，classes.dex 可正常反编译，无 AES 载荷、无 assets HTML、无 WebView、无远端配置参与权限引导；仅部分偏好项标题通过 d.a(int) 从资源 id 取串（如 2131099666、2131099728），字面值未逐条还原，但跳转目标（ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / MANAGE_OVERLAY_PERMISSION）与判定条件全部在字节码中明确可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `57881f388f12f7f07e2f42dec5d1c965a83045b16d2ea418a6316ee30888ec19` |
| 包名 / 年份 | `com.udxlbuno.plwnnhop` / 2020 |
| 家族 / 品类 | **MonitorMinor**（同池样本数：1） |
| 原始来源标识 | https://securelist.com/monitorminor-vicious-stalkerware/95575/ |
| 桌面显示名 | Google Service |
| 引导页宣称品牌/身份 | Google Service / Google Play 服务（并自称 Settings、Permission Request 等系统组件） |
| 系统无障碍列表服务名 | Google Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 label 冒用 Google Service、android:description 仅为空洞的 “Receiver”，掩盖真实监听能力；多入口伪装：activity-alias “WiFi”（targetActivity com.udxlbuno.plwnnhop.QaOUNIFQMU，Theme.Transparent）与多个 label 为 “Log in”“Register user”“Alert Ring”“Alert Message” 的透明/对话框主题 Activity；设备管理器 label 使用土耳其语 “Sistem Yöneticisi”；字符串资源大量以 nnhop. 前缀密文形式存放以规避静态检索；包名 com.udxlbuno.plwnnhop 与展示名完全无关。 |
| 无障碍服务类名 | `com.udxlbuno.plwnnhop.core.listener.YwdgjvZpkx` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `BIND_DEVICE_ADMIN, CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Receiver |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.udxlbuno.plwnnhop.xAnOvZoepF（LAUNCHER，label @string/xwVURbAqup = Google Service） | onCreate（点击桌面图标） | 原生Activity | **原文**：setContentView(2130968580)；this.c.setText(Html.fromHtml(d.a(2131099662, strA, m.b, m.b, strA, m.e)))<br>**译注**：首屏为一段经 Html.fromHtml 渲染的富文本说明（含占位符，具体文案由资源 2131099662 拼装），配一个“继续”按钮 | 点击按钮 2131361815 继续，无跳过逻辑 | `com.udxlbuno.plwnnhop.xAnOvZoepF#onCreate / #onClick` |
| 2 | 业务功能触发 | com.udxlbuno.plwnnhop.cECkPSKOZf → com.udxlbuno.plwnnhop.rOWwpgcisL / psnYfunHuu（label “Log in”/“Register user”） | xAnOvZoepF.onClick 跳转 | 原生Activity | **原文**：I'm new User / I'm already a Registered User<br>**译注**：“我是新用户 / 我已是注册用户”注册登录分流页（资源 OYsKJompCx、bPMmODzXrI） | 选择注册或登录，进入主设置页 | `com.udxlbuno.plwnnhop.xAnOvZoepF#onClick；res/values/strings.xml#OYsKJompCx` |
| 3 | 引导说明页 | com.udxlbuno.plwnnhop.wcBSKjPZDV（PreferenceActivity，label @string/XIoSdIbBKq = Settings）onCreate 首判 | onCreate 中 if (AllowPermissionActivity.a(this)) → 立即 startActivity(AllowPermissionActivity.class) 并 finish | 原生Activity | **原文**：Please provide permission for the app to best use of this application.<br>**译注**：“请授予权限以便最佳使用本应用”——未授权时不允许进入设置页，直接强制跳到权限页 | 被迫进入权限申请页，无取消路径 | `com.udxlbuno.plwnnhop.wcBSKjPZDV#onCreate；res/values/strings.xml#wTBjSvYaOk` |
| 4 | 引导说明页 | com.udxlbuno.plwnnhop.AllowPermissionActivity（label @string/KAURCoXraN = Permission Request） | onCreate 末尾直接调用 onClick(this.a) 弹系统权限框；onResume 每次刷新红/绿图标 | 原生Activity | **原文**：Click on Settings, Go to Permissions and make sure you have enabled all the permissions for this application. / Make sure you choose all the features enabled.<br>**译注**：“点击设置→权限，确保为本应用开启全部权限”“请确保把所有功能都开启”——以清单式图标逐项展示通话状态、存储、通讯录、通话记录、短信、相机、定位、日历、录音的授予状态 | 逐个点“允许”；按钮 2131361808 直接跳应用详情页自行开权限 | `com.udxlbuno.plwnnhop.AllowPermissionActivity#onCreate / #onClick / #a()；res/values/strings.xml#yUyTSMQitY, #etGGbVVbqX` |
| 5 | 跳受限设置 | 系统“显示在其他应用上层”授权页（android.settings.action.MANAGE_OVERLAY_PERMISSION） | onClick 中 arrayList 为空且 !Settings.canDrawOverlays(this) → c()；onActivityResult(108) 返回后再进 b() | 系统无障碍页 | **原文**：无（系统页面）<br>**译注**：跳转悬浮窗/上层显示权限页，为后续遮罩与叠层做能力准备 | 在系统页打开“允许显示在其他应用上层” | `com.udxlbuno.plwnnhop.AllowPermissionActivity#c()` |
| 6 | 跳无障碍设置 | com.udxlbuno.plwnnhop.wcBSKjPZDV#onPreferenceClick → 系统无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS） | 点击 key=c 的无障碍 CheckBoxPreference（或 key=p 项），执行 startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), this.ah/this.al) | 系统无障碍页 | **原文**：无（跳转系统页；偏好项标题由 d.a(2131099666) 取串，开关点击后 setChecked(false)）<br>**译注**：点击后进入系统无障碍设置列表，界面上的勾选状态被立刻置回未勾选，造成“未开启”的错觉 | 在系统无障碍列表中找到并手动开启“Google Service”服务 | `com.udxlbuno.plwnnhop.wcBSKjPZDV#onPreferenceClick` |
| 7 | 拒权反馈循环 | AllowPermissionActivity.onStop 启动的 AllowPermissionActivity$1 线程 → b() 重新拉起 wcBSKjPZDV | onStop 中 new Thread(new AllowPermissionActivity$1(this)).start()；b() 以 FLAG_ACTIVITY_NEW_TASK 启动 wcBSKjPZDV | 原生Activity | **原文**：无（后台线程重跳）<br>**译注**：离开权限页即启动后台线程重新把用户拉回设置/权限页，形成返回即重跳的循环 | 无法通过返回键退出流程 | `com.udxlbuno.plwnnhop.AllowPermissionActivity#onStop / #b()` |
| 8 | 获权后动作 | com.udxlbuno.plwnnhop.core.listener.YwdgjvZpkx（无障碍服务）+ wcBSKjPZDV.onActivityResult 状态回填 | onActivityResult(requestCode=ah) 中 YwdgjvZpkx.a(this) && !YwdgjvZpkx.b(this) 回填开关；onResume 同样校验 | 系统无障碍页 | **原文**：无（服务已启用后静默运行）<br>**译注**：返回设置页后静默校验无障碍服务是否真正启用，并同步显示勾选状态，之后由该服务接管窗口内容监听 | 无需再操作（服务已在后台运行） | `com.udxlbuno.plwnnhop.wcBSKjPZDV#onActivityResult / #onResume；com.udxlbuno.plwnnhop.core.listener.YwdgjvZpkx` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- xAnOvZoepF 首屏：TextView 通过 Html.fromHtml(d.a(2131099662, ...)) 渲染的富文本说明 + 一个继续按钮（layout 资源 2130968580）
- AllowPermissionActivity 权限清单页：9 个 ImageView 红/绿图标 + TextView 2131361806 提示语 + “Request/OK”按钮 2131361807 与跳详情页按钮 2131361808（layout 2130968576）
- wcBSKjPZDV 偏好页：PreferenceCategory 标题与各 CheckBoxPreference 的 title/summary（由 d.a(资源 id) 从 res/values/strings.xml 取串），如“Make sure you choose all the features enabled.”
- 系统无障碍列表：服务项名称取自 android:label=@string/hclEUCJUDl（Google Service），说明文字取自 res/xml/ssecca.xml 的 android:description=@string/YdOeNKmeod（Receiver）
- 设备管理器说明：receiver com.udxlbuno.plwnnhop.core.uKKtwYdAnp 的 android:label="Sistem Yöneticisi"、android:description=@string/ZOCdUxwgCE（Monitors attempts to disable or uninstall.）
- strings.xml 中 ljEsEGAHhG：以“★ Open \"Google Settings\" application on your phone …”分步条目呈现的反安全扫描教学文本
- 无 assets/ HTML、无 WebView、无悬浮引导遮罩文本（浮层仅由系统 MANAGE_OVERLAY_PERMISSION 能力准备，未见引导性 Overlay 视图代码）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Google Service | 谷歌服务 | `res/values/strings.xml key=hclEUCJUDl / xwVURbAqup（application label、无障碍服务 label、Activity label）` | 假更新 |
| en | Receiver | 接收器 | `res/values/strings.xml key=YdOeNKmeod，经 res/xml/ssecca.xml 的 android:description 呈现于系统无障碍列表` | 良性透明说明 |
| en | Please provide permission for the app to best use of this application. | 请提供权限，以便最佳使用本应用。 | `res/values/strings.xml key=wTBjSvYaOk` | 故障恐吓 |
| en | Click on Settings, Go to Permissions and make sure you have enabled all the permissions for this application. | 点击设置，进入权限，确保你已为本应用开启所有权限。 | `res/values/strings.xml key=yUyTSMQitY（AllowPermissionActivity 提示语）` | 受限设置分步教学 |
| en | Make sure you choose all the features enabled. | 请确保把所有功能都选择开启。 | `res/values/strings.xml key=etGGbVVbqX` | 受限设置分步教学 |
| en | ★ Open "Google Settings" application on your phone ★ Go to Security ★ Disable "Scan device for security threats" ★ Disable "Improve harmful app detection" | ★ 打开手机上的“Google 设置”应用 ★ 进入安全 ★ 关闭“扫描设备以防范安全威胁” ★ 关闭“改进有害应用检测” | `res/values/strings.xml key=ljEsEGAHhG（含 \n 换行分段）` | 教唆忽视警告 |
| en | Monitors attempts to disable or uninstall. | 监控卸载或停用的尝试。 | `res/values/strings.xml key=ZOCdUxwgCE（设备管理器 receiver android:description）` | 假反诈安全 |
| en | Permission Request | 权限请求 | `res/values/strings.xml key=KAURCoXraN（AllowPermissionActivity label）` | 良性透明说明 |
| tr | Sistem Yöneticisi | 系统管理员 | `AndroidManifest.xml：receiver com.udxlbuno.plwnnhop.core.uKKtwYdAnp android:label` | 假反诈安全 |
| en | I'm new User / I'm already a Registered User | 我是新用户 / 我已是注册用户 | `res/values/strings.xml key=OYsKJompCx / bPMmODzXrI` | 未知 |
| zh | %1$s无法访问 Google Play 服务，请重试。 | 同原文 | `res/values-zh-rCN/strings.xml（Google Play services 框架串，佐证 Google 品牌借用语境）` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：AllowPermissionActivity.onStop 启动后台线程 AllowPermissionActivity$1，其 run 调用 b() 以 FLAG_ACTIVITY_NEW_TASK 再次 startActivity(wcBSKjPZDV) 并 finish 自身；wcBSKjPZDV.onCreate 又因 AllowPermissionActivity.a(this) 为真立刻跳回 AllowPermissionActivity，形成离开即重跳的闭环。无障碍偏好项在跳转时先 setChecked(false)，onActivityResult/onResume 才按 YwdgjvZpkx.a()/b() 回填真实状态。
- **遮罩叠层 / 高仿系统设置页**：未发现自绘的高仿系统设置页或半透明引导遮罩视图；但流程强制申请 SYSTEM_ALERT_WINDOW（MANAGE_OVERLAY_PERMISSION）以取得悬浮叠层能力，为后续叠层提供条件。
- **Android 13+ 受限设置（Restricted Settings）应对**：无针对 Android 13+“受限设置”右上角菜单的专门引导；但存在等效手法：AllowPermissionActivity 按钮 2131361808 直接 startActivity(ACTION_APPLICATION_DETAILS_SETTINGS) 让用户进入应用详情页手动改权限，并配合“Click on Settings, Go to Permissions…”分步教学。
- **获权后即时行为与防撤权机制**：获权后未见 GLOBAL_ACTION_BACK/HOME 阻止撤权或自点确认的实现；但注册了设备管理器 receiver core.uKKtwYdAnp（BIND_DEVICE_ADMIN，描述“Monitors attempts to disable or uninstall.”），且字符串 ljEsEGAHhG 教用户关闭 Play Protect 的“扫描设备以防范安全威胁/改进有害应用检测”，具备抗卸载与抗安全软件的现实意图。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以“监测到 startActivity/startActivityForResult 目标为 android.settings.ACCESSIBILITY_SETTINGS”为第一触发点（同时命中 key=c 与 key=p 两处调用）；第二触发点为“冷启动后首次出现 com.udxlbuno.plwnnhop.AllowPermissionActivity 且 200ms 内弹出系统权限框”，第三触发点为“监测到 android.settings.ACTION_APPLICATION_DETAILS_SETTINGS 跳转”。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无静态加壳，无远端 HTML，无图片诱导，UTG 文本可完整提取；唯一盲区是偏好项标题与首屏富文本由 d.a(资源 id) 与 Html.fromHtml 拼装（部分为 nnhop. 前缀密文资源），需在运行期读取渲染后文本，纯静态 strings.xml 中对应字面值不可直接检索。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动强制权限清单页（红绿图标逐项展示）** | Activity 名 AllowPermissionActivity，标题“Permission Request”，页面含 9 个权限图标 + 提示 TextView + 两个按钮 | 该页是整条诱导链的闸门，App 在此处拒绝进入主功能直到全部危险权限授予，最能证明“无取消/无降级”的强制属性 | 页面标题 Permission Request 与包名/Google Service 身份不一致；同一屏出现通话状态/短信/通讯录/录音等 9 项权限图标；无返回键可用的退出路径（onStop 触发重跳线程） |
| **跳转前设置页（无障碍勾选项）** | PreferenceActivity wcBSKjPZDV，label“Settings”，含无障碍 CheckBoxPreference（key=c、key=p） | 捕获点击瞬间可确认“点击 → 立即置回未勾选 → 跳系统无障碍页”的诱导时序，这是区分正当引导与诱导开启的关键 | 点击后开关状态瞬间回弹为未选中；紧接着出现 android.settings.ACCESSIBILITY_SETTINGS 页面；偏好项摘要含“Make sure you choose all the features enabled.” |
| **系统无障碍服务列表项** | 系统设置 → 无障碍 → 已下载的服务，条目名“Google Service”，副标题“Receiver” | 直接呈现品牌冒用与描述空洞化的证据：服务名冒充 Google，说明文字仅为无意义的“Receiver” | 条目名 Google Service 与真实包名 com.udxlbuno.plwnnhop 无关；description 文本为 Receiver；返回设置页后该开关被静默回填为已勾选 |
| **返回系统设置后的重跳页** | 从无障碍页返回后重新出现的 AllowPermissionActivity 或 wcBSKjPZDV | 验证拒权循环：用户返回即被重新拉起，证明非良性降级 | 未开启服务情况下重复出现同一权限/设置页；短时间多次 Activity 切换记录 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.udxlbuno.plwnnhop.wcBSKjPZDV#onPreferenceClick`
- `com.udxlbuno.plwnnhop.wcBSKjPZDV#onCreate`
- `com.udxlbuno.plwnnhop.AllowPermissionActivity#onClick`
- `com.udxlbuno.plwnnhop.AllowPermissionActivity#onStop`
- `com.udxlbuno.plwnnhop.core.listener.YwdgjvZpkx`
- `res/xml/ssecca.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **静态完全可见**：无加壳，无加密载荷，无远端 HTML，也无 WebView。引导全部由原生 Activity、PreferenceActivity 和 Toast 完成。
- **入口链**：`xAnOvZoepF`（LAUNCHER，label 取自 `@string/xwVURbAqup`=“Google Service”）→ 内置 HTML 文本欢迎页 → `cECkPSZKOZf` → `wcBSKjPZDV`（label “Settings”，PreferenceActivity）。
- **前置权限诱导**：`AllowPermissionActivity`（label “Permission Request”）用红/绿图标清单逐项展示 9 项危险权限（通话状态、通讯录、通话记录、短信、相机、定位、日历、录音等），`onCreate` 末尾直接调用 `onClick(this.a)` 弹出系统授权框；全部授权后跳转 `ACTION_MANAGE_OVERLAY_PERMISSION`；副按钮跳转 `ACTION_APPLICATION_DETAILS_SETTINGS`（教用户进应用详情页手动开权限）。
- **无障碍跳转点**：`wcBSKjPZDV.onPreferenceClick` 中 key=`c` 的 `CheckBoxPreference` 与 key=`p` 的项均执行 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), ...)`，并把开关立即置回 false（视觉上“未开启”），`onActivityResult` 再用 `YwdgjvZpkx.a/b` 回填真实状态。
- **身份伪装**：无障碍服务 `core.listener.YwdgjvZpkx` 的 `android:label` = “Google Service”，`android:description` = “Receiver”（`res/xml/ssecca.xml` → `@string/YdOeNKmeod`）；设备管理器 label “Sistem Yöneticisi”、描述 “Monitors attempts to disable or uninstall.”；另有 `activity-alias` “WiFi” 指向 `QaOUNIFQMU`。
- **拒权循环**：`AllowPermissionActivity.onStop` 启动 `AllowPermissionActivity$1` 线程，`b()` 反复以 `FLAG_ACTIVITY_NEW_TASK` 拉回 `wcBSKjPZDV`；未授权则 `onCreate` 直接回到权限页，构成返回即重跳。
- **反安全软件**：字符串 `ljEsEGAHhG` 明示教用户进入 “Google Settings” 关闭 “Scan device for security threats”“Improve harmful app detection”（即关闭 Play Protect 扫描），属于典型的教唆忽略系统警告。
- 未决：`d.a(int)` 对资源 id（如 2131099666/2131099728）的解密式取串未逐条还原，偏好项标题原文以资源 id 记录；`PnsrYByfLo`（伪造输入法 `IRemoteService` action）与无障碍服务内部动作未在本轮展开。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全流程静态可见：APK 未加壳，classes.dex 可正常反编译，无 AES 载荷、无 assets HTML、无 WebView、无远端配置参与权限引导；仅部分偏好项标题通过 d.a(int) 从资源 id 取串（如 2131099666、2131099728），字面值未逐条还原，但跳转目标（ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / MANAGE_OVERLAY_PERMISSION）与判定条件全部在字节码中明确可见。",
  "summary_one_liner": "该应用冒充“Google Service”，先以红绿清单式权限页强制申请 9 项危险权限并跳悬浮窗授权，再在“Settings”偏好页以勾选项引导用户跳转系统无障碍设置开启名为 Google Service、描述为 Receiver 的无障碍服务，返回未开启即被线程反复拉回。",
  "disguise_identity": {
    "app_display_name": "Google Service",
    "claimed_brand_or_persona": "Google Service / Google Play 服务（并自称 Settings、Permission Request 等系统组件）",
    "a11y_service_label": "Google Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 label 冒用 Google Service、android:description 仅为空洞的 “Receiver”，掩盖真实监听能力；多入口伪装：activity-alias “WiFi”（targetActivity com.udxlbuno.plwnnhop.QaOUNIFQMU，Theme.Transparent）与多个 label 为 “Log in”“Register user”“Alert Ring”“Alert Message” 的透明/对话框主题 Activity；设备管理器 label 使用土耳其语 “Sistem Yöneticisi”；字符串资源大量以 nnhop. 前缀密文形式存放以规避静态检索；包名 com.udxlbuno.plwnnhop 与展示名完全无关。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.udxlbuno.plwnnhop.xAnOvZoepF（LAUNCHER，label @string/xwVURbAqup = Google Service）",
      "trigger_event": "onCreate（点击桌面图标）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "setContentView(2130968580)；this.c.setText(Html.fromHtml(d.a(2131099662, strA, m.b, m.b, strA, m.e)))",
      "shown_text_zh": "首屏为一段经 Html.fromHtml 渲染的富文本说明（含占位符，具体文案由资源 2131099662 拼装），配一个“继续”按钮",
      "user_action_requested": "点击按钮 2131361815 继续，无跳过逻辑",
      "code_anchor": "com.udxlbuno.plwnnhop.xAnOvZoepF#onCreate / #onClick"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.udxlbuno.plwnnhop.cECkPSKOZf → com.udxlbuno.plwnnhop.rOWwpgcisL / psnYfunHuu（label “Log in”/“Register user”）",
      "trigger_event": "xAnOvZoepF.onClick 跳转",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "I'm new User / I'm already a Registered User",
      "shown_text_zh": "“我是新用户 / 我已是注册用户”注册登录分流页（资源 OYsKJompCx、bPMmODzXrI）",
      "user_action_requested": "选择注册或登录，进入主设置页",
      "code_anchor": "com.udxlbuno.plwnnhop.xAnOvZoepF#onClick；res/values/strings.xml#OYsKJompCx"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.udxlbuno.plwnnhop.wcBSKjPZDV（PreferenceActivity，label @string/XIoSdIbBKq = Settings）onCreate 首判",
      "trigger_event": "onCreate 中 if (AllowPermissionActivity.a(this)) → 立即 startActivity(AllowPermissionActivity.class) 并 finish",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Please provide permission for the app to best use of this application.",
      "shown_text_zh": "“请授予权限以便最佳使用本应用”——未授权时不允许进入设置页，直接强制跳到权限页",
      "user_action_requested": "被迫进入权限申请页，无取消路径",
      "code_anchor": "com.udxlbuno.plwnnhop.wcBSKjPZDV#onCreate；res/values/strings.xml#wTBjSvYaOk"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "com.udxlbuno.plwnnhop.AllowPermissionActivity（label @string/KAURCoXraN = Permission Request）",
      "trigger_event": "onCreate 末尾直接调用 onClick(this.a) 弹系统权限框；onResume 每次刷新红/绿图标",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Click on Settings, Go to Permissions and make sure you have enabled all the permissions for this application. / Make sure you choose all the features enabled.",
      "shown_text_zh": "“点击设置→权限，确保为本应用开启全部权限”“请确保把所有功能都开启”——以清单式图标逐项展示通话状态、存储、通讯录、通话记录、短信、相机、定位、日历、录音的授予状态",
      "user_action_requested": "逐个点“允许”；按钮 2131361808 直接跳应用详情页自行开权限",
      "code_anchor": "com.udxlbuno.plwnnhop.AllowPermissionActivity#onCreate / #onClick / #a()；res/values/strings.xml#yUyTSMQitY, #etGGbVVbqX"
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "系统“显示在其他应用上层”授权页（android.settings.action.MANAGE_OVERLAY_PERMISSION）",
      "trigger_event": "onClick 中 arrayList 为空且 !Settings.canDrawOverlays(this) → c()；onActivityResult(108) 返回后再进 b()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统页面）",
      "shown_text_zh": "跳转悬浮窗/上层显示权限页，为后续遮罩与叠层做能力准备",
      "user_action_requested": "在系统页打开“允许显示在其他应用上层”",
      "code_anchor": "com.udxlbuno.plwnnhop.AllowPermissionActivity#c()"
    },
    {
      "step": 6,
      "stage": "跳无障碍设置",
      "screen_or_component": "com.udxlbuno.plwnnhop.wcBSKjPZDV#onPreferenceClick → 系统无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "点击 key=c 的无障碍 CheckBoxPreference（或 key=p 项），执行 startActivityForResult(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"), this.ah/this.al)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（跳转系统页；偏好项标题由 d.a(2131099666) 取串，开关点击后 setChecked(false)）",
      "shown_text_zh": "点击后进入系统无障碍设置列表，界面上的勾选状态被立刻置回未勾选，造成“未开启”的错觉",
      "user_action_requested": "在系统无障碍列表中找到并手动开启“Google Service”服务",
      "code_anchor": "com.udxlbuno.plwnnhop.wcBSKjPZDV#onPreferenceClick"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "AllowPermissionActivity.onStop 启动的 AllowPermissionActivity$1 线程 → b() 重新拉起 wcBSKjPZDV",
      "trigger_event": "onStop 中 new Thread(new AllowPermissionActivity$1(this)).start()；b() 以 FLAG_ACTIVITY_NEW_TASK 启动 wcBSKjPZDV",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（后台线程重跳）",
      "shown_text_zh": "离开权限页即启动后台线程重新把用户拉回设置/权限页，形成返回即重跳的循环",
      "user_action_requested": "无法通过返回键退出流程",
      "code_anchor": "com.udxlbuno.plwnnhop.AllowPermissionActivity#onStop / #b()"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "com.udxlbuno.plwnnhop.core.listener.YwdgjvZpkx（无障碍服务）+ wcBSKjPZDV.onActivityResult 状态回填",
      "trigger_event": "onActivityResult(requestCode=ah) 中 YwdgjvZpkx.a(this) && !YwdgjvZpkx.b(this) 回填开关；onResume 同样校验",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（服务已启用后静默运行）",
      "shown_text_zh": "返回设置页后静默校验无障碍服务是否真正启用，并同步显示勾选状态，之后由该服务接管窗口内容监听",
      "user_action_requested": "无需再操作（服务已在后台运行）",
      "code_anchor": "com.udxlbuno.plwnnhop.wcBSKjPZDV#onActivityResult / #onResume；com.udxlbuno.plwnnhop.core.listener.YwdgjvZpkx"
    }
  ],
  "text_presentation_locations": [
    "xAnOvZoepF 首屏：TextView 通过 Html.fromHtml(d.a(2131099662, ...)) 渲染的富文本说明 + 一个继续按钮（layout 资源 2130968580）",
    "AllowPermissionActivity 权限清单页：9 个 ImageView 红/绿图标 + TextView 2131361806 提示语 + “Request/OK”按钮 2131361807 与跳详情页按钮 2131361808（layout 2130968576）",
    "wcBSKjPZDV 偏好页：PreferenceCategory 标题与各 CheckBoxPreference 的 title/summary（由 d.a(资源 id) 从 res/values/strings.xml 取串），如“Make sure you choose all the features enabled.”",
    "系统无障碍列表：服务项名称取自 android:label=@string/hclEUCJUDl（Google Service），说明文字取自 res/xml/ssecca.xml 的 android:description=@string/YdOeNKmeod（Receiver）",
    "设备管理器说明：receiver com.udxlbuno.plwnnhop.core.uKKtwYdAnp 的 android:label=\"Sistem Yöneticisi\"、android:description=@string/ZOCdUxwgCE（Monitors attempts to disable or uninstall.）",
    "strings.xml 中 ljEsEGAHhG：以“★ Open \\\"Google Settings\\\" application on your phone …”分步条目呈现的反安全扫描教学文本",
    "无 assets/ HTML、无 WebView、无悬浮引导遮罩文本（浮层仅由系统 MANAGE_OVERLAY_PERMISSION 能力准备，未见引导性 Overlay 视图代码）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Google Service",
      "text_zh": "谷歌服务",
      "source_location": "res/values/strings.xml key=hclEUCJUDl / xwVURbAqup（application label、无障碍服务 label、Activity label）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Receiver",
      "text_zh": "接收器",
      "source_location": "res/values/strings.xml key=YdOeNKmeod，经 res/xml/ssecca.xml 的 android:description 呈现于系统无障碍列表",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Please provide permission for the app to best use of this application.",
      "text_zh": "请提供权限，以便最佳使用本应用。",
      "source_location": "res/values/strings.xml key=wTBjSvYaOk",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Click on Settings, Go to Permissions and make sure you have enabled all the permissions for this application.",
      "text_zh": "点击设置，进入权限，确保你已为本应用开启所有权限。",
      "source_location": "res/values/strings.xml key=yUyTSMQitY（AllowPermissionActivity 提示语）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Make sure you choose all the features enabled.",
      "text_zh": "请确保把所有功能都选择开启。",
      "source_location": "res/values/strings.xml key=etGGbVVbqX",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "★ Open \"Google Settings\" application on your phone ★ Go to Security ★ Disable \"Scan device for security threats\" ★ Disable \"Improve harmful app detection\"",
      "text_zh": "★ 打开手机上的“Google 设置”应用 ★ 进入安全 ★ 关闭“扫描设备以防范安全威胁” ★ 关闭“改进有害应用检测”",
      "source_location": "res/values/strings.xml key=ljEsEGAHhG（含 \\n 换行分段）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Monitors attempts to disable or uninstall.",
      "text_zh": "监控卸载或停用的尝试。",
      "source_location": "res/values/strings.xml key=ZOCdUxwgCE（设备管理器 receiver android:description）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Permission Request",
      "text_zh": "权限请求",
      "source_location": "res/values/strings.xml key=KAURCoXraN（AllowPermissionActivity label）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "tr",
      "text_verbatim": "Sistem Yöneticisi",
      "text_zh": "系统管理员",
      "source_location": "AndroidManifest.xml：receiver com.udxlbuno.plwnnhop.core.uKKtwYdAnp android:label",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "I'm new User / I'm already a Registered User",
      "text_zh": "我是新用户 / 我已是注册用户",
      "source_location": "res/values/strings.xml key=OYsKJompCx / bPMmODzXrI",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "%1$s无法访问 Google Play 服务，请重试。",
      "text_zh": "同原文",
      "source_location": "res/values-zh-rCN/strings.xml（Google Play services 框架串，佐证 Google 品牌借用语境）",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "AllowPermissionActivity.onStop 启动后台线程 AllowPermissionActivity$1，其 run 调用 b() 以 FLAG_ACTIVITY_NEW_TASK 再次 startActivity(wcBSKjPZDV) 并 finish 自身；wcBSKjPZDV.onCreate 又因 AllowPermissionActivity.a(this) 为真立刻跳回 AllowPermissionActivity，形成离开即重跳的闭环。无障碍偏好项在跳转时先 setChecked(false)，onActivityResult/onResume 才按 YwdgjvZpkx.a()/b() 回填真实状态。",
    "overlay_or_fake_settings": "未发现自绘的高仿系统设置页或半透明引导遮罩视图；但流程强制申请 SYSTEM_ALERT_WINDOW（MANAGE_OVERLAY_PERMISSION）以取得悬浮叠层能力，为后续叠层提供条件。",
    "restricted_settings_13plus_coaching": "无针对 Android 13+“受限设置”右上角菜单的专门引导；但存在等效手法：AllowPermissionActivity 按钮 2131361808 直接 startActivity(ACTION_APPLICATION_DETAILS_SETTINGS) 让用户进入应用详情页手动改权限，并配合“Click on Settings, Go to Permissions…”分步教学。",
    "post_grant_anti_removal": "获权后未见 GLOBAL_ACTION_BACK/HOME 阻止撤权或自点确认的实现；但注册了设备管理器 receiver core.uKKtwYdAnp（BIND_DEVICE_ADMIN，描述“Monitors attempts to disable or uninstall.”），且字符串 ljEsEGAHhG 教用户关闭 Play Protect 的“扫描设备以防范安全威胁/改进有害应用检测”，具备抗卸载与抗安全软件的现实意图。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以“监测到 startActivity/startActivityForResult 目标为 android.settings.ACCESSIBILITY_SETTINGS”为第一触发点（同时命中 key=c 与 key=p 两处调用）；第二触发点为“冷启动后首次出现 com.udxlbuno.plwnnhop.AllowPermissionActivity 且 200ms 内弹出系统权限框”，第三触发点为“监测到 android.settings.ACTION_APPLICATION_DETAILS_SETTINGS 跳转”。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动强制权限清单页（红绿图标逐项展示）",
        "page_identifier": "Activity 名 AllowPermissionActivity，标题“Permission Request”，页面含 9 个权限图标 + 提示 TextView + 两个按钮",
        "why_most_useful": "该页是整条诱导链的闸门，App 在此处拒绝进入主功能直到全部危险权限授予，最能证明“无取消/无降级”的强制属性",
        "observable_utg_signals": ["页面标题 Permission Request 与包名/Google Service 身份不一致", "同一屏出现通话状态/短信/通讯录/录音等 9 项权限图标", "无返回键可用的退出路径（onStop 触发重跳线程）"]
      },
      {
        "page_role": "跳转前设置页（无障碍勾选项）",
        "page_identifier": "PreferenceActivity wcBSKjPZDV，label“Settings”，含无障碍 CheckBoxPreference（key=c、key=p）",
        "why_most_useful": "捕获点击瞬间可确认“点击 → 立即置回未勾选 → 跳系统无障碍页”的诱导时序，这是区分正当引导与诱导开启的关键",
        "observable_utg_signals": ["点击后开关状态瞬间回弹为未选中", "紧接着出现 android.settings.ACCESSIBILITY_SETTINGS 页面", "偏好项摘要含“Make sure you choose all the features enabled.”"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已下载的服务，条目名“Google Service”，副标题“Receiver”",
        "why_most_useful": "直接呈现品牌冒用与描述空洞化的证据：服务名冒充 Google，说明文字仅为无意义的“Receiver”",
        "observable_utg_signals": ["条目名 Google Service 与真实包名 com.udxlbuno.plwnnhop 无关", "description 文本为 Receiver", "返回设置页后该开关被静默回填为已勾选"]
      },
      {
        "page_role": "返回系统设置后的重跳页",
        "page_identifier": "从无障碍页返回后重新出现的 AllowPermissionActivity 或 wcBSKjPZDV",
        "why_most_useful": "验证拒权循环：用户返回即被重新拉起，证明非良性降级",
        "observable_utg_signals": ["未开启服务情况下重复出现同一权限/设置页", "短时间多次 Activity 切换记录"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无静态加壳，无远端 HTML，无图片诱导，UTG 文本可完整提取；唯一盲区是偏好项标题与首屏富文本由 d.a(资源 id) 与 Html.fromHtml 拼装（部分为 nnhop. 前缀密文资源），需在运行期读取渲染后文本，纯静态 strings.xml 中对应字面值不可直接检索。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.udxlbuno.plwnnhop.wcBSKjPZDV#onPreferenceClick",
    "com.udxlbuno.plwnnhop.wcBSKjPZDV#onCreate",
    "com.udxlbuno.plwnnhop.AllowPermissionActivity#onClick",
    "com.udxlbuno.plwnnhop.AllowPermissionActivity#onStop",
    "com.udxlbuno.plwnnhop.core.listener.YwdgjvZpkx",
    "res/xml/ssecca.xml"
  ]
}
```

</details>

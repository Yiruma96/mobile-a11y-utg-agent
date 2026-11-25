# MR_025__38acf26161｜CallerSpy — GSERVICES

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：90.1s

## 1. 一句话核心结论

- **核心申请方式**：应用以 GSERVICES（冒用 Google Play 服务）身份冷启动即批量索权，并用原生弹窗与 APPLecation_DETAILS/OPPO 悬浮窗设置跳转把用户推向受限设置，而无障碍服务本身以无 label、无 description 的裸项出现在系统列表中，缺少任何应用内用途说明或专门引导页。
- **静态可见性说明**：DEX 未加壳、无密文动态加载，Manifest、无障碍配置、布局与跳转代码均静态可见。但应用内不存在 ACTION_ACCESSIBILITY_SETTINGS 跳转，也不存在无障碍说明页/教学 WebView，故“引导开启无障碍”的界面环节在代码中确实缺失，而非被隐藏；ACCESSIBILITY.notifications 的事件处理体与可能的远端引导内容未在本次预算内完全展开。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `38acf26161a2c6429ee40d9b70d8419a9bd00eaa8740d221f943cea3229372dd` |
| 包名 / 年份 | `com.sas.gservices.accesibility` / 2019 |
| 家族 / 品类 | **CallerSpy**（同池样本数：4） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/19/l/mobile-cyberespionage-campaign-distributed-through-callerspy-mounts-initial-phase-of-a-targeted-attack.html |
| 桌面显示名 | GSERVICES |
| 引导页宣称品牌/身份 | Google Play services（Google Play 服务） |
| 系统无障碍列表服务名 | GSERVICES（服务未声明 android:label，回退为应用名；android:description 为空，无障碍列表中无任何用途说明） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务不设 android:label 与 android:description，系统列表中只剩应用名、无解释；资源内植入大量 Google Play services 假故障/假更新话术冒充官方组件；accessibility_service_config 的 packageNames 仍为模板值 com.example.abdullah.accesibility_service，与本包名不符；应用详情跳转弹窗按钮文案拼写为 Canel。 |
| 无障碍服务类名 | `com.sas.gservices.accesibility.ACCESSIBILITY.notifications` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.example.abdullah.accesibility_service |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECORD_AUDIO` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.sas.gservices.accesibility.MainActivity（LAUNCHER，portrait） | onCreate：setContentView(activity_main) 后立即 startForegroundService(AirddService) 并 ActivityCompat.requestPermissions(13 项权限, requestCode=1) | 原生Activity | **原文**：Please wait setting up application!<br>**译注**：请稍候，正在设置应用！ | 面对系统权限弹窗需逐项点击“允许”；界面本身无取消/跳过入口，用户只能等待或离开 | `com.sas.gservices.accesibility.MainActivity.onCreate / res/layout/activity_main.xml` |
| 2 | 跳受限设置 | com.oppo.safe.permission.floatwindow.FloatWindowListActivity → com.coloros.safecenter…FloatWindowListActivity（厂商悬浮窗权限页） | onCreate 内 initOPPO() 逐级 try/catch 拉起 OPPO/ColorOS 悬浮窗权限页 | 系统无障碍页 | 无 | 要求用户在该厂商页面为 GSERVICES 打开悬浮窗（叠层）权限；无跳过按钮 | `com.sas.gservices.accesibility.MainActivity.initOPPO` |
| 3 | 拒权反馈循环 | android.support.v7.app.AlertDialog（MainActivity 内） | onRequestPermissionsResult(requestCode=1/2) 检测到拒绝或 shouldShowRequestPermissionRationale 为真 | 原生Dialog | **原文**：You need to grant read contacts permission to use read contacts feature. Retry and grant it ! / You denied read contacts permission. So, the feature will be disabled. To enable it, go on settings and grant read phone state permission for the application<br>**译注**：你需要授予读取通讯录权限才能使用读取通讯录功能。请重试并授予！/ 你拒绝了读取通讯录权限，功能将被禁用。要启用它，请到设置中为应用授予读取电话状态权限 | 点击 OK 跳应用详情页重新授权，或点击 Canel（原文拼写）取消 | `com.sas.gservices.accesibility.MainActivity.onRequestPermissionsResult` |
| 4 | 跳受限设置 | 系统“应用详情”页（android.settings.APPLICATION_DETAILS_SETTINGS + package:com.sas.gservices.accesibility） | 上述弹窗 OK 按钮（MainActivity$6.onClick）回调 openSettingToGetPermission() | 系统无障碍页 | 无 | 要求用户手动进入权限列表重新授予被拒权限；无应用内取消机制，返回后不再重弹（onResume 为空实现） | `com.sas.gservices.accesibility.MainActivity.openSettingToGetPermission` |
| 5 | 获权后动作 | MainActivity$1 / MainActivity$1$1 / MainActivity$insertUserDataLocally → 系统设备管理器授权页（ADD_DEVICE_ADMIN） | Handler 每 500ms 轮询 hasPermissions 直到全量授权，随后 runOnUiThread 读取短信/通讯录/通话记录/jpg 列表并落库上传；AsyncTask onPostExecute 调 makeDeviceAdministator() 拉起设备管理器激活页 | 原生Activity | 无 | 在系统设备管理器页点击“激活”；采集与上传过程用户无感知、无法取消 | `com.sas.gservices.accesibility.MainActivity$1.run / MainActivity.makeDeviceAdministator` |
| 6 | 引导说明页 | 无（系统设置 → 无障碍 → 已安装服务列表中的 com.sas.gservices.accesibility.ACCESSIBILITY.notifications 裸项） | 无应用内触发；需用户自行进入系统无障碍列表，或由外部投放方引导 | 系统无障碍页 | 无 | 由用户手动找到并打开该服务开关；应用内无任何跳转、弹窗、WebView 或悬浮引导指向无障碍设置 | `res/xml/accessibility_service_config.xml / AndroidManifest.xml(service ACCESSIBILITY.notifications)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 布局 activity_main.xml 单行 TextView：“Please wait setting up application!”（唯一可见的应用自身界面文案）
- MainActivity.onRequestPermissionsResult 内的原生不可取消 AlertDialog：标题 “Read Contacts permission”/“Read Contacts permission denied”，正文要求“Retry and grant it !”并指示“go on settings and grant … permission”
- 同一弹窗第二个分支（requestCode=2）：“Read Phone State permission denied … go on settings and grant read phone state permission for the application”，按钮 OK / Cancel
- res/values/strings.xml 等资源中的 Google Play services 伪装文案：“%1$s won't work unless you enable Google Play services.”、“Get Google Play services”、“Update Google Play services”、“%1$s is having trouble with Google Play services. Please try again.”（属于 GMS 模板资源，未见由本应用自有 UI 引用）
- 系统无障碍服务列表项：仅显示 GSERVICES，无 android:label / android:description 说明
- 无 assets 内本地 HTML 引导页、无 WebView 教学页、无悬浮窗引导遮罩（initOPPO 仅打开厂商悬浮窗权限页，未发现自有 Overlay 引导实现）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please wait setting up application! | 请稍候，正在设置应用！ | `res/layout/activity_main.xml（TextView android:text）` | 良性透明说明 |
| en | You need to grant read contacts permission to use read contacts feature. Retry and grant it ! | 你需要授予读取通讯录权限才能使用读取通讯录功能。请重试并授予！ | `MainActivity.onRequestPermissionsResult 硬编码` | 受限设置分步教学 |
| en | You denied read contacts permission. So, the feature will be disabled. To enable it, go on settings and grant read phone state permission for the application | 你拒绝了读取通讯录权限，功能将被禁用。要启用它，请到设置中为应用授予读取电话状态权限 | `MainActivity.onRequestPermissionsResult 硬编码` | 受限设置分步教学 |
| en | You denied read phone state permission. So, the feature will be disabled. To enable it, go on settings and grant read phone state permission for the application | 你拒绝了读取电话状态权限，功能将被禁用。要启用它，请到设置中为应用授予读取电话状态权限 | `MainActivity.onRequestPermissionsResult 硬编码（requestCode=2）` | 受限设置分步教学 |
| en | %1$s won't work unless you enable Google Play services. | %1$s 需要启用 Google Play 服务才能运行。 | `res/values/strings.xml（GMS 资源，假借官方身份）` | 假更新 |
| en | Update Google Play services | 更新 Google Play 服务 | `res/values/strings.xml` | 假更新 |
| en | %1$s is having trouble with Google Play services. Please try again. | %1$s 与 Google Play 服务通信出现问题，请重试。 | `res/values/strings.xml` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：权限轮询死循环：MainActivity$1.run 每 500ms 检查 hasPermissions，未齐备即 postDelayed 自我重排；onResume 为空实现，未做返回后重跳，故无设置页重跳死循环，仅表现为静默持续轮询与拒权弹窗反复提示。
- **遮罩叠层 / 高仿系统设置页**：未见自有半透明引导遮罩或高仿无障碍开关页；仅在冷启动时 initOPPO() 拉起 OPPO/ColorOS 悬浮窗权限列表（为后续叠层铺路），并跳转系统应用详情页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。仅以通用文案“go on settings and grant … permission”引导到应用详情页，未提供 Android 13+ 应用详情页右上角菜单“允许受限设置”的具体点击教学，也未使用 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：获权后由 AsyncTask onPostExecute 调 makeDeviceAdministator() 拉起 android.app.action.ADD_DEVICE_ADMIN 引导激活设备管理员，配合 BOOT_COMPLETED / restart_service / TimerCheckReceiver / AirddService 守护链防停止；未发现通过无障碍自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码。
- **良性降级 / 替代方案**：无。拒权后仅提示“功能将被禁用”，但代码仍持续轮询并在齐备后静默采集上传，无手动模式或降级路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 MainActivity.onCreate 完成后（launch 后约 1s，Handler.postDelayed 1000ms 到点）与 initOPPO() 触发瞬间拉起；以及监测 Intent 到 android.settings.APPLICATION_DETAILS_SETTINGS / com.oppo.safe|com.coloros.safecenter 悬浮窗页、android.app.action.ADD_DEVICE_ADMIN 时立即抓栈。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：应用内根本不存在 ACTION_ACCESSIBILITY_SETTINGS 跳转与任何无障碍说明 UI，因此纯 UTG 只能观察到系统无障碍列表中的裸服务项，无法捕获“引导开启无障碍”的应用侧页面；真正的诱导若存在，只能来自远端下发或投放方外部分发渠道，静态与本地 UTG 均不可见。此外 initOPPO 的悬浮窗页跳转可能因机型不存在对应组件而静默失败（try/catch 吞异常），导致该步不可观测。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首屏（唯一自有界面）** | GSERVICES 应用主界面，居中单行文本 Please wait setting up application! | 确认应用无任何业务功能与无障碍用途说明，属纯采集外壳 | 界面控件树仅 1 个 TextView 且文本固定；无 WebView 节点；无按钮/开关可交互 |
| **拒权引导弹窗页** | AlertDialog 标题 Read Contacts permission denied，按钮 OK / Canel | 区分是否以“功能被禁用”恐吓+教用户进设置重授权，是诱导受限设置的关键证据 | 对话框是否可取消（点击外部/返回键）；按钮文案拼写 Canel；OK 后是否跳 APPLICATION_DETAILS_SETTINGS |
| **设置页后厂商悬浮窗权限页** | com.oppo.safe.permission.floatwindow.FloatWindowListActivity 或 com.coloros.safecenter 悬浮窗列表，含 GSERVICES 条目 | 证明冷启动即把用户推向叠层类受限设置，为后续覆盖其它应用/系统页做准备 | 包名 com.oppo.safe / com.coloros.safecenter；列表中 GSERVICES 悬浮窗开关初始为关；无应用内引导文案 |
| **系统无障碍服务列表项** | 设置→无障碍→已下载服务中的 GSERVICES 条目（无副标题/无描述） | 核实无障碍服务以无说明裸项呈现，判定其缺失告知义务与身份伪装 | 服务项仅有标题 GSERVICES、无 description 文本；开关默认关闭；点击后弹系统风险确认框 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.sas.gservices.accesibility.MainActivity.onCreate`
- `com.sas.gservices.accesibility.MainActivity.onRequestPermissionsResult`
- `com.sas.gservices.accesibility.MainActivity.openSettingToGetPermission`
- `com.sas.gservices.accesibility.MainActivity.initOPPO`
- `res/xml/accessibility_service_config.xml`
- `res/layout/activity_main.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，静态视角）

**1. 无障碍能力声明存在，但没有“跳转无障碍设置”的引导代码**
- 服务 [ACCESSIBILITY.notifications](<resource-unit:#1 manifest:components>) 已在 Manifest 中注册，`android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE"`，并且**没有 `android:label`，也没有 `android:description`**；因此在系统无障碍列表中只会显示应用名 `GSERVICES`，没有任何用途说明。
- 配置 [accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml#L2>) 中 `android:settingsActivity=""`，`packageNames="com.example.abdullah.accesibility_service"`；这与本应用包名不符，属于模板残留，`canRetrieveWindowContent="true"`、`typeContextClicked|typeViewClicked`。
- 全包检索 `android.settings.ACCESSIBILITY_SETTINGS`、`enabled_accessibility_services`、`ACTION_ACCESSIBILITY_SETTINGS` 均**没有命中**，因此应用内不存在由代码拉起系统无障碍页的逻辑；无障碍开关依赖用户自行开启，或由外部（投放者、引导页）开启。

**2. 实际存在的“引导跳设置”路径都指向其它受限设置**
- 冷启动 [MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.sas.gservices.accesibility.MainActivity#onCreate>)：一次性申请 13 项运行时权限（通讯录、短信、录音、相机、通话记录、定位），随后调用 `initOPPO()` **直接拉起 OPPO/ColorOS 悬浮窗权限页**（`com.oppo.safe…FloatWindowListActivity` / `com.coloros.safecenter…`），为后续叠层做准备。
- 拒绝权限后弹出的原生 AlertDialog（[onRequestPermissionsResult()](<resource-unit:#1.dex1 code:com.sas.gservices.accesibility.MainActivity#onRequestPermissionsResult>)）中，`OK` 按钮会调用 [openSettingToGetPermission()](<resource-unit:#1.dex1 code:com.sas.gservices.accesibility.MainActivity#openSettingToGetPermission>)，通过 `ACTION_APPLICATION_DETAILS_SETTINGS` 跳到应用详情页（教用户手动到设置中打开权限），`Cancel` 按钮文案被拼错为 `Canel`。
- 另有 `ADD_DEVICE_ADMIN` 跳转（[makeDeviceAdministator()](<resource-unit:#1.dex1 code:com.sas.gservices.accesibility.MainActivity#makeDeviceAdministator>)，requestCode 47），属于设备管理器授权引导，而不是无障碍。
- 主界面布局只有一行文本 `Please wait setting up application!`（[activity_main.xml](<resource-unit:#1 file:res/layout/activity_main.xml#L4>)），没有业务界面，也没有任何“无障碍用途说明”页面或 WebView 教学页。

**3. 获取权限后的动作闭环（说明无障碍是采集链路的一环）**
`onCreate` 以 500 ms 间隔轮询权限就绪（`MainActivity$1.run`），就绪后立即读取短信、通讯录、通话记录、外置存储 jpg 列表并落库上传（`MainActivity$1$1.run`），并有 `StoreDataToRemoteServer`、录音、截屏、通话录音等 7 个采集服务与 BOOT 自启/守护链。无障碍服务在此架构中用于窗口内容/点击事件捕获（`canRetrieveWindowContent=true`）。

**4. 身份伪装**
应用名 `GSERVICES`、包名 `com.sas.gservices.accesibility`，资源中混入大量 Google Play services 错误/更新提示字符串（`%1$s won't work unless you enable Google Play services.` 等），构成对 Google Play 服务的品牌冒用，用于“假故障/假更新”话术。无障碍列表无 label/description，属于“空白标签不解释用途”的规避手法。

**边界说明**：本次未发现任何指向无障碍设置的 Intent 或引导 UI，因此“如何一步步引导开启无障碍”这一问题的静态答案只是“没有应用内引导，只有系统列表中的裸服务项 + 其它受限设置跳转”；`ACCESSIBILITY.notifications` 的事件处理体与是否存在远端下发的引导页，未在预算内展开，属未决项。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳、无密文动态加载，Manifest、无障碍配置、布局与跳转代码均静态可见。但应用内不存在 ACTION_ACCESSIBILITY_SETTINGS 跳转，也不存在无障碍说明页/教学 WebView，故“引导开启无障碍”的界面环节在代码中确实缺失，而非被隐藏；ACCESSIBILITY.notifications 的事件处理体与可能的远端引导内容未在本次预算内完全展开。",
  "summary_one_liner": "应用以 GSERVICES（冒用 Google Play 服务）身份冷启动即批量索权，并用原生弹窗与 APPLecation_DETAILS/OPPO 悬浮窗设置跳转把用户推向受限设置，而无障碍服务本身以无 label、无 description 的裸项出现在系统列表中，缺少任何应用内用途说明或专门引导页。",
  "disguise_identity": {
    "app_display_name": "GSERVICES",
    "claimed_brand_or_persona": "Google Play services（Google Play 服务）",
    "a11y_service_label": "GSERVICES（服务未声明 android:label，回退为应用名；android:description 为空，无障碍列表中无任何用途说明）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务不设 android:label 与 android:description，系统列表中只剩应用名、无解释；资源内植入大量 Google Play services 假故障/假更新话术冒充官方组件；accessibility_service_config 的 packageNames 仍为模板值 com.example.abdullah.accesibility_service，与本包名不符；应用详情跳转弹窗按钮文案拼写为 Canel。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.sas.gservices.accesibility.MainActivity（LAUNCHER，portrait）",
      "trigger_event": "onCreate：setContentView(activity_main) 后立即 startForegroundService(AirddService) 并 ActivityCompat.requestPermissions(13 项权限, requestCode=1)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Please wait setting up application!",
      "shown_text_zh": "请稍候，正在设置应用！",
      "user_action_requested": "面对系统权限弹窗需逐项点击“允许”；界面本身无取消/跳过入口，用户只能等待或离开",
      "code_anchor": "com.sas.gservices.accesibility.MainActivity.onCreate / res/layout/activity_main.xml"
    },
    {
      "step": 2,
      "stage": "跳受限设置",
      "screen_or_component": "com.oppo.safe.permission.floatwindow.FloatWindowListActivity → com.coloros.safecenter…FloatWindowListActivity（厂商悬浮窗权限页）",
      "trigger_event": "onCreate 内 initOPPO() 逐级 try/catch 拉起 OPPO/ColorOS 悬浮窗权限页",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接跳转 ColorOS/OPPO 安全中心的悬浮窗权限列表，无任何应用内说明",
      "user_action_requested": "要求用户在该厂商页面为 GSERVICES 打开悬浮窗（叠层）权限；无跳过按钮",
      "code_anchor": "com.sas.gservices.accesibility.MainActivity.initOPPO"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "android.support.v7.app.AlertDialog（MainActivity 内）",
      "trigger_event": "onRequestPermissionsResult(requestCode=1/2) 检测到拒绝或 shouldShowRequestPermissionRationale 为真",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "You need to grant read contacts permission to use read contacts feature. Retry and grant it ! / You denied read contacts permission. So, the feature will be disabled. To enable it, go on settings and grant read phone state permission for the application",
      "shown_text_zh": "你需要授予读取通讯录权限才能使用读取通讯录功能。请重试并授予！/ 你拒绝了读取通讯录权限，功能将被禁用。要启用它，请到设置中为应用授予读取电话状态权限",
      "user_action_requested": "点击 OK 跳应用详情页重新授权，或点击 Canel（原文拼写）取消",
      "code_anchor": "com.sas.gservices.accesibility.MainActivity.onRequestPermissionsResult"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统“应用详情”页（android.settings.APPLICATION_DETAILS_SETTINGS + package:com.sas.gservices.accesibility）",
      "trigger_event": "上述弹窗 OK 按钮（MainActivity$6.onClick）回调 openSettingToGetPermission()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接打开本应用的系统详情页，让用户手动去开权限（未提供 13+ 受限设置的具体点击教学文案）",
      "user_action_requested": "要求用户手动进入权限列表重新授予被拒权限；无应用内取消机制，返回后不再重弹（onResume 为空实现）",
      "code_anchor": "com.sas.gservices.accesibility.MainActivity.openSettingToGetPermission"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "MainActivity$1 / MainActivity$1$1 / MainActivity$insertUserDataLocally → 系统设备管理器授权页（ADD_DEVICE_ADMIN）",
      "trigger_event": "Handler 每 500ms 轮询 hasPermissions 直到全量授权，随后 runOnUiThread 读取短信/通讯录/通话记录/jpg 列表并落库上传；AsyncTask onPostExecute 调 makeDeviceAdministator() 拉起设备管理器激活页",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "权限齐备后静默采集并上传数据，再引导用户激活设备管理员（防卸载）；全程无可见业务界面与告知",
      "user_action_requested": "在系统设备管理器页点击“激活”；采集与上传过程用户无感知、无法取消",
      "code_anchor": "com.sas.gservices.accesibility.MainActivity$1.run / MainActivity.makeDeviceAdministator"
    },
    {
      "step": 6,
      "stage": "引导说明页",
      "screen_or_component": "无（系统设置 → 无障碍 → 已安装服务列表中的 com.sas.gservices.accesibility.ACCESSIBILITY.notifications 裸项）",
      "trigger_event": "无应用内触发；需用户自行进入系统无障碍列表，或由外部投放方引导",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无障碍列表仅显示应用名 GSERVICES，无 label、无 description，不解释为何需要读取窗口内容与点击事件",
      "user_action_requested": "由用户手动找到并打开该服务开关；应用内无任何跳转、弹窗、WebView 或悬浮引导指向无障碍设置",
      "code_anchor": "res/xml/accessibility_service_config.xml / AndroidManifest.xml(service ACCESSIBILITY.notifications)"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 布局 activity_main.xml 单行 TextView：“Please wait setting up application!”（唯一可见的应用自身界面文案）",
    "MainActivity.onRequestPermissionsResult 内的原生不可取消 AlertDialog：标题 “Read Contacts permission”/“Read Contacts permission denied”，正文要求“Retry and grant it !”并指示“go on settings and grant … permission”",
    "同一弹窗第二个分支（requestCode=2）：“Read Phone State permission denied … go on settings and grant read phone state permission for the application”，按钮 OK / Cancel",
    "res/values/strings.xml 等资源中的 Google Play services 伪装文案：“%1$s won't work unless you enable Google Play services.”、“Get Google Play services”、“Update Google Play services”、“%1$s is having trouble with Google Play services. Please try again.”（属于 GMS 模板资源，未见由本应用自有 UI 引用）",
    "系统无障碍服务列表项：仅显示 GSERVICES，无 android:label / android:description 说明",
    "无 assets 内本地 HTML 引导页、无 WebView 教学页、无悬浮窗引导遮罩（initOPPO 仅打开厂商悬浮窗权限页，未发现自有 Overlay 引导实现）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please wait setting up application!",
      "text_zh": "请稍候，正在设置应用！",
      "source_location": "res/layout/activity_main.xml（TextView android:text）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "You need to grant read contacts permission to use read contacts feature. Retry and grant it !",
      "text_zh": "你需要授予读取通讯录权限才能使用读取通讯录功能。请重试并授予！",
      "source_location": "MainActivity.onRequestPermissionsResult 硬编码",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "You denied read contacts permission. So, the feature will be disabled. To enable it, go on settings and grant read phone state permission for the application",
      "text_zh": "你拒绝了读取通讯录权限，功能将被禁用。要启用它，请到设置中为应用授予读取电话状态权限",
      "source_location": "MainActivity.onRequestPermissionsResult 硬编码",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "You denied read phone state permission. So, the feature will be disabled. To enable it, go on settings and grant read phone state permission for the application",
      "text_zh": "你拒绝了读取电话状态权限，功能将被禁用。要启用它，请到设置中为应用授予读取电话状态权限",
      "source_location": "MainActivity.onRequestPermissionsResult 硬编码（requestCode=2）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "%1$s 需要启用 Google Play 服务才能运行。",
      "source_location": "res/values/strings.xml（GMS 资源，假借官方身份）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Update Google Play services",
      "text_zh": "更新 Google Play 服务",
      "source_location": "res/values/strings.xml",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s is having trouble with Google Play services. Please try again.",
      "text_zh": "%1$s 与 Google Play 服务通信出现问题，请重试。",
      "source_location": "res/values/strings.xml",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "权限轮询死循环：MainActivity$1.run 每 500ms 检查 hasPermissions，未齐备即 postDelayed 自我重排；onResume 为空实现，未做返回后重跳，故无设置页重跳死循环，仅表现为静默持续轮询与拒权弹窗反复提示。",
    "overlay_or_fake_settings": "未见自有半透明引导遮罩或高仿无障碍开关页；仅在冷启动时 initOPPO() 拉起 OPPO/ColorOS 悬浮窗权限列表（为后续叠层铺路），并跳转系统应用详情页。",
    "restricted_settings_13plus_coaching": "无。仅以通用文案“go on settings and grant … permission”引导到应用详情页，未提供 Android 13+ 应用详情页右上角菜单“允许受限设置”的具体点击教学，也未使用 Session 安装器绕过。",
    "post_grant_anti_removal": "获权后由 AsyncTask onPostExecute 调 makeDeviceAdministator() 拉起 android.app.action.ADD_DEVICE_ADMIN 引导激活设备管理员，配合 BOOT_COMPLETED / restart_service / TimerCheckReceiver / AirddService 守护链防停止；未发现通过无障碍自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码。",
    "benign_graceful_degradation": "无。拒权后仅提示“功能将被禁用”，但代码仍持续轮询并在齐备后静默采集上传，无手动模式或降级路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 MainActivity.onCreate 完成后（launch 后约 1s，Handler.postDelayed 1000ms 到点）与 initOPPO() 触发瞬间拉起；以及监测 Intent 到 android.settings.APPLICATION_DETAILS_SETTINGS / com.oppo.safe|com.coloros.safecenter 悬浮窗页、android.app.action.ADD_DEVICE_ADMIN 时立即抓栈。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首屏（唯一自有界面）",
        "page_identifier": "GSERVICES 应用主界面，居中单行文本 Please wait setting up application!",
        "why_most_useful": "确认应用无任何业务功能与无障碍用途说明，属纯采集外壳",
        "observable_utg_signals": ["界面控件树仅 1 个 TextView 且文本固定", "无 WebView 节点", "无按钮/开关可交互"]
      },
      {
        "page_role": "拒权引导弹窗页",
        "page_identifier": "AlertDialog 标题 Read Contacts permission denied，按钮 OK / Canel",
        "why_most_useful": "区分是否以“功能被禁用”恐吓+教用户进设置重授权，是诱导受限设置的关键证据",
        "observable_utg_signals": ["对话框是否可取消（点击外部/返回键）", "按钮文案拼写 Canel", "OK 后是否跳 APPLICATION_DETAILS_SETTINGS"]
      },
      {
        "page_role": "设置页后厂商悬浮窗权限页",
        "page_identifier": "com.oppo.safe.permission.floatwindow.FloatWindowListActivity 或 com.coloros.safecenter 悬浮窗列表，含 GSERVICES 条目",
        "why_most_useful": "证明冷启动即把用户推向叠层类受限设置，为后续覆盖其它应用/系统页做准备",
        "observable_utg_signals": ["包名 com.oppo.safe / com.coloros.safecenter", "列表中 GSERVICES 悬浮窗开关初始为关", "无应用内引导文案"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置→无障碍→已下载服务中的 GSERVICES 条目（无副标题/无描述）",
        "why_most_useful": "核实无障碍服务以无说明裸项呈现，判定其缺失告知义务与身份伪装",
        "observable_utg_signals": ["服务项仅有标题 GSERVICES、无 description 文本", "开关默认关闭", "点击后弹系统风险确认框"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：应用内根本不存在 ACTION_ACCESSIBILITY_SETTINGS 跳转与任何无障碍说明 UI，因此纯 UTG 只能观察到系统无障碍列表中的裸服务项，无法捕获“引导开启无障碍”的应用侧页面；真正的诱导若存在，只能来自远端下发或投放方外部分发渠道，静态与本地 UTG 均不可见。此外 initOPPO 的悬浮窗页跳转可能因机型不存在对应组件而静默失败（try/catch 吞异常），导致该步不可观测。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "LURE_RESTRICTED_SETTINGS_COACHING"
  ],
  "code_anchors": [
    "com.sas.gservices.accesibility.MainActivity.onCreate",
    "com.sas.gservices.accesibility.MainActivity.onRequestPermissionsResult",
    "com.sas.gservices.accesibility.MainActivity.openSettingToGetPermission",
    "com.sas.gservices.accesibility.MainActivity.initOPPO",
    "res/xml/accessibility_service_config.xml",
    "res/layout/activity_main.xml"
  ]
}
```

</details>

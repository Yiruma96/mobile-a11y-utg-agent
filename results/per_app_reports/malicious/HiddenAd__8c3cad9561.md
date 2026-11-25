# MR_165__8c3cad9561｜HiddenAd — Clean Master

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：151.6s

## 1. 一句话核心结论

- **核心申请方式**：以知名清理工具 Clean Master 之名，用通知栏与悬浮窗的『手机异常缓慢/垃圾堆积』恐吓把用户引向后台拉起的透明权限引导页，再以『点右上角按钮』式教学加『绝不收集任何个人数据』承诺诱导开启具备读屏取词与按键过滤能力的无障碍服务，真实引导逻辑由运行期下发的 moduleshell 模块执行。
- **静态可见性说明**：Manifest 无障碍服务声明、res/xml/sa__detection_service_config.xml 能力配置、res/values/strings.xml 全部引导文案、透明入口 Activity 均静态完整可见；但无障碍服务的真实业务实现（RTemplateAccessibilityService.onAccessibilityEvent 为空壳）以及 PermissionProxyActivity/UsageProxyActivity/SettingTipsActivity 的页面构建与跳转逻辑，全部通过 moduleshell 模板框架反射委托到运行期下发的模块实现，两处 dex 中不存在 ACTION_ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / MANAGE_OVERLAY_PERMISSION 字面量，跳转目标与弹窗载体不可静态还原。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `8c3cad9561d3f0f0e86d53ab5cb75936ff611296a85993b72411a5aa89d014d3` |
| 包名 / 年份 | `com.sstfsk.cleanmaster` / 2020 |
| 家族 / 品类 | **HiddenAd**（同池样本数：12） |
| 原始来源标识 | https://blog.malwarebytes.com/android/2020/07/we-found-yet-another-phone-with-pre-installed-malware-via-the-lifeline-assistance-program/ |
| 桌面显示名 | Clean Master |
| 引导页宣称品牌/身份 | Clean Master（知名手机清理/加速工具品牌，官方包名为 com.cleanmaster.mguard） |
| 系统无障碍列表服务名 | Clean Master |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.sstfsk.cleanmaster 与声明类命名空间 com.superman.moduleshell.*、com.sthnsqqwel.cleanmaster.*、com.android.impl.* 相互割裂；无 LAUNCHER 主入口，仅保留自定义 action com.sthnsqqwel.cleanmaster.act 的透明 Activity 作为隐蔽入口；无障碍说明以换行分段方式把教学句与隐私承诺混排在系统服务描述中；大量 Activity 复用同一 taskAffinity（com.superman.moduleshell.nhk.install.SettingTipsActivity）并使用 Translucent.NoTitleBar.Fullscreen 主题规避可见界面。 |
| 无障碍服务类名 | `com.superman.moduleshell.cleanmaster.AccessibilityDetectService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Please turn on the button in the top-right corner. <br><br>Powerful clean the background apps that use memory.<br><br>Notice: We will NOT collect any personal data. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.sthnsqqwel.cleanmaster.aa（透明主题 Activity）→ com.sthnsqqwel.cleanmaster.MainService | 外部 Intent action=com.sthnsqqwel.cleanmaster.act 或 MainService 被守护进程拉起；aa.onCreate 内 startService 后立即 finish() | 原生Activity | 无 | 无（无需用户操作，也无可取消界面） | `com.sthnsqqwel.cleanmaster.aa#onCreate` |
| 2 | 业务功能触发 | 通知栏/悬浮提示：BoostTempActivity、BoostProcessingMonitorActivity、BoostFinishTempActivity（均 Translucent.NoTitleBar、excludeFromRecents、singleInstance/singleTask） | 后台任务（BoostEventReceiver / CleanMasterReceiver / ModuleXTaskReceiver 定时或 BOOT_COMPLETED）下发通知点击或直接 startActivity | 通知栏 | **原文**：Your phone is abnormally slow / Click here to clean up the background apps / Found a lot of junk files in the phone,<font color=#ff0606>Clean up now! </font> / Excessive phone memory usage<br>**译注**：您的手机异常缓慢 / 点击此处清理后台应用 / 手机中发现大量垃圾文件，立即清理！ / 手机内存占用过高 | 点击通知进入清理/加速流程（无跳过清理的选项，仅『Boost』『Clean』动作按钮） | `res/values/strings.xml#L4-L16、L31` |
| 3 | 引导说明页 | com.superman.moduleshell.cleanmaster.PermissionProxyActivity（index=6）/ UsageProxyActivity（index=9）/ SettingTipsActivity，均为 RTemplateActivity 壳，页面内容运行期下发 | 权限检测失败后由模块框架反射调起（RTemplateActivity.onCreate → mFActivity 委托） | 不可静态还原 | **原文**：Please turn on permission / Please authorized to %1$s / Granting permissions<br>**译注**：请开启权限 / 请授权给 %1$s / 正在授予权限 | 点击进入权限设置（Cancel/Continue 字符串存在，但取消路径是否可用不可静态确认） | `com.superman.moduleshell.cleanmaster.PermissionProxyActivity#getIndex、res/values/strings.xml#L38、L56-L57` |
| 4 | 跳受限设置 | 系统『使用情况访问权限』页（UsageProxyActivity 对应）；SYSTEM_ALERT_WINDOW 悬浮窗授权页 | 引导页按钮点击 → 模块实现发起 Settings Intent（静态 dex 无该字面量，运行期拼接/下发） | 系统无障碍页 | **原文**：Please turn on usage rights / Grant Floating Window permission / Floating Window<br>**译注**：请开启使用情况访问权限 / 授予悬浮窗权限 / 悬浮窗 | 在系统页手动打开『使用情况访问权限』与『显示在其他应用上层』开关 | `com.superman.moduleshell.cleanmaster.UsageProxyActivity#getIndex、res/values/strings.xml#L35、L37、L42` |
| 5 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载的服务 → 「Clean Master」条目；服务描述来自 sa__detection_service_config.xml | 『Enable Accessibility』按钮点击后跳转（跳转代码在运行期模块中） | 系统无障碍页 | **原文**：Enable Accessibility / Please turn on the button in the top-right corner. <br><br>Powerful clean the background apps that use memory.<br><br>Notice: We will NOT collect any personal data.<br>**译注**：启用无障碍 / 请打开右上角的按钮。强大的清理占用内存的后台应用。注意：我们不会收集任何个人数据。 | 在系统无障碍列表中点击「Clean Master」并开启开关（该页由系统渲染，应用无法插入取消按钮） | `res/xml/sa__detection_service_config.xml、res/values/strings.xml#L23-L27、L36` |
| 6 | 遮罩叠层指引 | 悬浮窗叠层（SYSTEM_ALERT_WINDOW + flagIncludeNotImportantViews/flagReportViewIds 支持按视图 ID 定位系统设置控件） | 跳转系统设置后由后台服务叠加悬浮引导（具体绘制代码在运行期模块，静态不可还原） | 悬浮窗Overlay | **原文**：Please turn on the button in the top-right corner.<br>**译注**：请打开右上角的按钮（即在系统设置页上叠一层指向右上角开关的指引） | 按遮罩指引点击系统设置页右上角/开关位置 | `res/values/strings.xml#L23、res/xml/sa__detection_service_config.xml` |
| 7 | 获权后动作 | com.superman.moduleshell.cleanmaster.AccessibilityDetectService（index=10，进程 :lsb_e）→ 运行期下发模块 | onServiceConnected 后模块框架接管；RTemplateAccessibilityService.onAccessibilityEvent 空实现，实际事件处理在动态模块 | 不可静态还原 | 无 | 无（静默运行） | `com.superman.moduleshell.cleanmaster.AccessibilityDetectService#getIndex、com.superman.module.api.template.RTemplateAccessibilityService#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目描述（android:description=@string/sa__detection_service_des，res/xml/sa__detection_service_config.xml 引用）：『Please turn on the button in the top-right corner...We will NOT collect any personal data.』
- 通知栏通知标题/正文（sa__boost_phone_slow_title / sa__boost_phone_slow_description / sa__junk_clean_notification_desc2 / sa__boost_notification_desc，红字 #ff0606 渲染）
- 权限引导 Activity 内的文案（sa__permission_title『Please turn on permission』、sa__permission_open_accessibility『Enable Accessibility』、sa__permission_float_window『Grant Floating Window permission』、sa__usage_stat_permission_title『Please turn on usage rights』），承载组件运行期下发
- 透明/无标题全屏主题的临时 Activity（BoostTempActivity、BoostProcessingMonitorActivity、SettingTipsActivity、NhkRSDActivity）作为跳转中转与弹窗宿主
- 悬浮窗叠层（SYSTEM_ALERT_WINDOW 已申请，配合 flagIncludeNotImportantViews/flagReportViewIds 在系统设置页上定位控件绘制指引）
- 安装/更新诱导文案『Please click to install』『Download completed』（sa__click_to_install、sa__download_completed）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please turn on the button in the top-right corner. <br><br>Powerful clean the background apps that use memory.<br><br>Notice: We will NOT collect any personal data. | 请打开右上角的按钮。强大的清理占用内存的后台应用。注意：我们不会收集任何个人数据。 | `res/values/strings.xml key=sa__detection_service_des（经 res/xml/sa__detection_service_config.xml android:description 呈现于系统无障碍列表）` | 隐私承诺 |
| en | Enable Accessibility | 启用无障碍 | `res/values/strings.xml key=sa__permission_open_accessibility` | 受限设置分步教学 |
| en | Please turn on permission | 请开启权限 | `res/values/strings.xml key=sa__permission_title` | 受限设置分步教学 |
| en | Grant Floating Window permission | 授予悬浮窗权限 | `res/values/strings.xml key=sa__permission_float_window` | 受限设置分步教学 |
| en | Please turn on usage rights | 请开启使用情况访问权限 | `res/values/strings.xml key=sa__usage_stat_permission_title` | 受限设置分步教学 |
| en | Your phone is abnormally slow | 您的手机异常缓慢 | `res/values/strings.xml key=sa__boost_phone_slow_title` | 故障恐吓 |
| en | Click here to clean up the background apps | 点击此处清理后台应用 | `res/values/strings.xml key=sa__boost_phone_slow_description` | 清理工具伪装 |
| en | Found a lot of junk files in the phone,<font color=#ff0606>Clean up now! </font> | 手机中发现大量垃圾文件，立即清理！ | `res/values/strings.xml key=sa__junk_clean_notification_desc2` | 故障恐吓 |
| en | Please click to install | 请点击安装 | `res/values/strings.xml key=sa__click_to_install` | 假更新 |
| en | Excessive phone memory usage / Press for instant speed increase, and free memory | 手机内存占用过高 / 按下立即提速并释放内存 | `res/values/strings.xml key=sa__boost_memory_usage_high_title / sa__boost_memory_usage_high_description` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：静态不可完全还原：拒绝/返回后由后台服务与定时 Receiver（ModuleXTaskReceiver、BoostEventReceiver、CleanMasterReceiver、FlightTaskReceiver/HearingTaskReceiver 等）再次拉起 PermissionProxyActivity/UsageProxyActivity/SettingTipsActivity 并重新弹通知，形成循环；循环间隔与次数由运行期下发模块控制，未在静态代码中确认。
- **遮罩叠层 / 高仿系统设置页**：已申请 SYSTEM_ALERT_WINDOW，无障碍服务配置开启 flagIncludeNotImportantViews/flagReportViewIds/flagRequestFilterKeyEvents 并按视图 ID 定位控件，具备在系统无障碍设置页上叠加半透明指引遮罩的技术条件；遮罩绘制代码在运行期下发模块中，未见高仿系统开关页资源。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=22，安装包为 2020 年样本，未针对 Android 13+ 受限设置/会话安装器做教学，跳转仍走传统设置页）。
- **获权后即时行为与防撤权机制**：静态不可确认：无障碍事件类型含 typeWindowStateChanged/typeWindowContentChanged 且可读取窗口内容，具备监听设置页并执行返回/Home 阻止撤权的条件，但 GLOBAL_ACTION_BACK/HOME 调用点位于运行期下发模块，未在静态代码中确认。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到当前焦点为系统无障碍设置页（com.android.settings/.accessibility.AccessibilitySettings 或 Settings$AccessibilitySettingsActivity）或应用详情页，且同时存在来自 com.sstfsk.cleanmaster 的悬浮窗窗口时拉起 UTG；另在冷启动后收到该包通知点击（Boost/Clean 通知）瞬间同步抓取，以捕获跳转前的引导弹窗。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：无障碍服务的真实业务逻辑（RTemplateAccessibilityService 为空壳，getIndex 仅返回 10）与所有页面构建/设置跳转/遮罩绘制均由 moduleshell 运行期下发模块执行，静态 dex 内无 ACTION_ACCESSIBILITY_SETTINGS 等字面量，属一阶段 Dropper/模块化外壳结构；因此『拒绝后重跳循环、获权后是否阻止撤权』等动态细节必须依赖运行期 UTG/Hook 才能定性，静态侧仅能确认服务声明、能力配置与全部诱导文案。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前引导弹窗页（权限总引导）** | com.superman.moduleshell.cleanmaster.PermissionProxyActivity / UsageProxyActivity / SettingTipsActivity 的窗口，含『Please turn on permission』『Enable Accessibility』『Please turn on usage rights』文本与 Continue/Cancel 按钮 | 这是唯一能证明『应用主动引导开无障碍』的界面，可验证是否存在可取消路径以及文案是否为清理工具伪装的假安全理由 | 文本节点『Enable Accessibility』/『Please turn on permission』；按钮节点是否仅有一个 Continue（无 Cancel/跳过）；窗口包名 com.sstfsk.cleanmaster 与 Activity 类名 |
| **系统无障碍服务列表项** | Settings 无障碍列表中 label 为『Clean Master』的服务条目及其描述展开 | 核对系统层面呈现的服务名与说明是否与真实品牌一致，以及描述中的隐私承诺与能力声明矛盾 | 条目文本『Clean Master』；描述文本『We will NOT collect any personal data.』；开关 checked 状态变化 |
| **设置页后压栈遮罩页** | 系统设置 Activity 之上叠加的 TYPE_APPLICATION_OVERLAY/TYPE_SYSTEM_ALERT 窗口（来源包 com.sstfsk.cleanmaster） | 判定是否使用悬浮窗在系统页上做『点右上角』指引遮罩，是区别于良性应用的关键特征 | window 层存在非 Settings 包的全屏/半透明 overlay；overlay 内文本『Please turn on the button in the top-right corner.』；overlay 覆盖的坐标是否指向无障碍开关位置 |
| **通知栏诱导入口** | 通知标题『Your phone is abnormally slow』/『Clean notification』/红字『Clean up now!』，点击后跳转链路 | 确认冷启动/后台唤起路径是通知而非用户主动打开图标（应用无 LAUNCHER 入口） | 通知文本与包名；点击后落地的 Activity 类名；落地是否直接为权限引导页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.superman.moduleshell.cleanmaster.AccessibilityDetectService#getIndex`
- `com.superman.module.api.template.RTemplateAccessibilityService#onAccessibilityEvent`
- `com.sthnsqqwel.cleanmaster.aa#onCreate`
- `com.superman.moduleshell.cleanmaster.PermissionProxyActivity#getIndex`
- `res/xml/sa__detection_service_config.xml`
- `res/values/strings.xml#L23-L27`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（工具调用已到上限，停止探索）。以下为结论。

## 关键发现

**1. 静态可见性：引导流程的“执行体”不在静态代码里**
- 无障碍服务声明完整可见：[AndroidManifest.xml](<resource-unit:#1 manifest:components>) 中 `com.superman.moduleshell.cleanmaster.AccessibilityDetectService`，`android:label="@string/app_name"`（= `Clean Master`），绑定 `BIND_ACCESSIBILITY_SERVICE`，配置文件 [res/xml/sa__detection_service_config.xml](<resource-unit:#1 file:res/xml/sa__detection_service_config.xml>) 声明 `canRetrieveWindowContent="true"`、`flagRequestFilterKeyEvents`、`flagReportViewIds`、监听通知/窗口内容变化。
- 但 [AccessibilityDetectService#getIndex()](<resource-unit:#1.dex2 code:com.superman.moduleshell.cleanmaster.AccessibilityDetectService#getIndex>) 仅返回 `10`，父类 [RTemplateAccessibilityService#onAccessibilityEvent()](<resource-unit:#1.dex2 code:com.superman.module.api.template.RTemplateAccessibilityService#onAccessibilityEvent>) 是**空实现**；`PermissionProxyActivity`、`UsageProxyActivity`、`SettingTipsActivity` 均为 `RTemplateActivity` 壳（index 6/9），`onCreate/onResume` 通过反射委托给 `mFActivity`。
- 全包 `classes.dex` + `assets/core.dex` 的字符串中**不存在** `ACTION_ACCESSIBILITY_SETTINGS` / `android.settings.ACCESSIBILITY_SETTINGS` / `APPLICATION_DETAILS_SETTINGS` / `MANAGE_OVERLAY_PERMISSION` 字面量 —— 跳转 Intent 由 moduleshell 插件框架运行期解析下发，静态不可还原。故 `static_visibility = partial_dynamic_or_remote`。

**2. 伪装身份**
- 桌面名 `Clean Master`、无障碍服务名同为一个知名清理工具品牌（官方包为 `com.cleanmaster.mguard`，本包为 `com.sstfsk.cleanmaster`），属品牌冒用。
- 无障碍说明文本用 `Please turn on the button in the top-right corner` 的教学式引导 + `We will NOT collect any personal data` 隐私承诺（[strings.xml L23-L27](<resource-unit:#1 file:res/values/strings.xml#L23-L27>)），与服务实际声明的读屏内容/按键过滤能力矛盾。

**3. 隐蔽入口**
- 全 Manifest 无 `android.intent.category.LAUNCHER` 主入口；唯一外部入口是 `com.sthnsqqwel.cleanmaster.act` → [aa#onCreate()](<resource-unit:#1.dex1 code:com.sthnsqqwel.cleanmaster.aa#onCreate>)，透明主题、`startService(MainService)` 后立即 `finish()`，无任何 UI —— 说明 UI（含授权引导）由后台服务/通知/悬浮窗拉起，非用户主动点图标。

**4. 可确认的引导物料（文本层）**
- 清理工具伪装：`Your phone is abnormally slow` / `Click here to clean up the background apps` / 红字 `Found a lot of junk files in the phone,Clean up now!`
- 分步权限教学：`Please turn on permission`、`Enable Accessibility`、`Grant Floating Window permission`、`Please turn on usage rights`
- 安装诱导：`Please click to install`、`Download completed`

**未决/覆盖边界**：各步骤的具体承载组件（Dialog / 全屏遮罩 / WebView）与拒绝后的重跳循环逻辑位于运行期下发的模块实现中，静态不可判定；`.so`（libdaemon/libleomodule/libleoyahfa）经字符串初筛未见设置页跳转或引导文本，属守护/引擎类库，未深挖。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest 无障碍服务声明、res/xml/sa__detection_service_config.xml 能力配置、res/values/strings.xml 全部引导文案、透明入口 Activity 均静态完整可见；但无障碍服务的真实业务实现（RTemplateAccessibilityService.onAccessibilityEvent 为空壳）以及 PermissionProxyActivity/UsageProxyActivity/SettingTipsActivity 的页面构建与跳转逻辑，全部通过 moduleshell 模板框架反射委托到运行期下发的模块实现，两处 dex 中不存在 ACTION_ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / MANAGE_OVERLAY_PERMISSION 字面量，跳转目标与弹窗载体不可静态还原。",
  "summary_one_liner": "以知名清理工具 Clean Master 之名，用通知栏与悬浮窗的『手机异常缓慢/垃圾堆积』恐吓把用户引向后台拉起的透明权限引导页，再以『点右上角按钮』式教学加『绝不收集任何个人数据』承诺诱导开启具备读屏取词与按键过滤能力的无障碍服务，真实引导逻辑由运行期下发的 moduleshell 模块执行。",
  "disguise_identity": {
    "app_display_name": "Clean Master",
    "claimed_brand_or_persona": "Clean Master（知名手机清理/加速工具品牌，官方包名为 com.cleanmaster.mguard）",
    "a11y_service_label": "Clean Master",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.sstfsk.cleanmaster 与声明类命名空间 com.superman.moduleshell.*、com.sthnsqqwel.cleanmaster.*、com.android.impl.* 相互割裂；无 LAUNCHER 主入口，仅保留自定义 action com.sthnsqqwel.cleanmaster.act 的透明 Activity 作为隐蔽入口；无障碍说明以换行分段方式把教学句与隐私承诺混排在系统服务描述中；大量 Activity 复用同一 taskAffinity（com.superman.moduleshell.nhk.install.SettingTipsActivity）并使用 Translucent.NoTitleBar.Fullscreen 主题规避可见界面。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.sthnsqqwel.cleanmaster.aa（透明主题 Activity）→ com.sthnsqqwel.cleanmaster.MainService",
      "trigger_event": "外部 Intent action=com.sthnsqqwel.cleanmaster.act 或 MainService 被守护进程拉起；aa.onCreate 内 startService 后立即 finish()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，瞬间透明退出，用户不可感知",
      "user_action_requested": "无（无需用户操作，也无可取消界面）",
      "code_anchor": "com.sthnsqqwel.cleanmaster.aa#onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "通知栏/悬浮提示：BoostTempActivity、BoostProcessingMonitorActivity、BoostFinishTempActivity（均 Translucent.NoTitleBar、excludeFromRecents、singleInstance/singleTask）",
      "trigger_event": "后台任务（BoostEventReceiver / CleanMasterReceiver / ModuleXTaskReceiver 定时或 BOOT_COMPLETED）下发通知点击或直接 startActivity",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Your phone is abnormally slow / Click here to clean up the background apps / Found a lot of junk files in the phone,<font color=#ff0606>Clean up now! </font> / Excessive phone memory usage",
      "shown_text_zh": "您的手机异常缓慢 / 点击此处清理后台应用 / 手机中发现大量垃圾文件，立即清理！ / 手机内存占用过高",
      "user_action_requested": "点击通知进入清理/加速流程（无跳过清理的选项，仅『Boost』『Clean』动作按钮）",
      "code_anchor": "res/values/strings.xml#L4-L16、L31"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.superman.moduleshell.cleanmaster.PermissionProxyActivity（index=6）/ UsageProxyActivity（index=9）/ SettingTipsActivity，均为 RTemplateActivity 壳，页面内容运行期下发",
      "trigger_event": "权限检测失败后由模块框架反射调起（RTemplateActivity.onCreate → mFActivity 委托）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Please turn on permission / Please authorized to %1$s / Granting permissions",
      "shown_text_zh": "请开启权限 / 请授权给 %1$s / 正在授予权限",
      "user_action_requested": "点击进入权限设置（Cancel/Continue 字符串存在，但取消路径是否可用不可静态确认）",
      "code_anchor": "com.superman.moduleshell.cleanmaster.PermissionProxyActivity#getIndex、res/values/strings.xml#L38、L56-L57"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统『使用情况访问权限』页（UsageProxyActivity 对应）；SYSTEM_ALERT_WINDOW 悬浮窗授权页",
      "trigger_event": "引导页按钮点击 → 模块实现发起 Settings Intent（静态 dex 无该字面量，运行期拼接/下发）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Please turn on usage rights / Grant Floating Window permission / Floating Window",
      "shown_text_zh": "请开启使用情况访问权限 / 授予悬浮窗权限 / 悬浮窗",
      "user_action_requested": "在系统页手动打开『使用情况访问权限』与『显示在其他应用上层』开关",
      "code_anchor": "com.superman.moduleshell.cleanmaster.UsageProxyActivity#getIndex、res/values/strings.xml#L35、L37、L42"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载的服务 → 「Clean Master」条目；服务描述来自 sa__detection_service_config.xml",
      "trigger_event": "『Enable Accessibility』按钮点击后跳转（跳转代码在运行期模块中）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Enable Accessibility / Please turn on the button in the top-right corner. \n\nPowerful clean the background apps that use memory.\n\nNotice: We will NOT collect any personal data.",
      "shown_text_zh": "启用无障碍 / 请打开右上角的按钮。强大的清理占用内存的后台应用。注意：我们不会收集任何个人数据。",
      "user_action_requested": "在系统无障碍列表中点击「Clean Master」并开启开关（该页由系统渲染，应用无法插入取消按钮）",
      "code_anchor": "res/xml/sa__detection_service_config.xml、res/values/strings.xml#L23-L27、L36"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "悬浮窗叠层（SYSTEM_ALERT_WINDOW + flagIncludeNotImportantViews/flagReportViewIds 支持按视图 ID 定位系统设置控件）",
      "trigger_event": "跳转系统设置后由后台服务叠加悬浮引导（具体绘制代码在运行期模块，静态不可还原）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Please turn on the button in the top-right corner.",
      "shown_text_zh": "请打开右上角的按钮（即在系统设置页上叠一层指向右上角开关的指引）",
      "user_action_requested": "按遮罩指引点击系统设置页右上角/开关位置",
      "code_anchor": "res/values/strings.xml#L23、res/xml/sa__detection_service_config.xml"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.superman.moduleshell.cleanmaster.AccessibilityDetectService（index=10，进程 :lsb_e）→ 运行期下发模块",
      "trigger_event": "onServiceConnected 后模块框架接管；RTemplateAccessibilityService.onAccessibilityEvent 空实现，实际事件处理在动态模块",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；服务以 canRetrieveWindowContent + 按键过滤能力静默读取窗口内容",
      "user_action_requested": "无（静默运行）",
      "code_anchor": "com.superman.moduleshell.cleanmaster.AccessibilityDetectService#getIndex、com.superman.module.api.template.RTemplateAccessibilityService#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目描述（android:description=@string/sa__detection_service_des，res/xml/sa__detection_service_config.xml 引用）：『Please turn on the button in the top-right corner...We will NOT collect any personal data.』",
    "通知栏通知标题/正文（sa__boost_phone_slow_title / sa__boost_phone_slow_description / sa__junk_clean_notification_desc2 / sa__boost_notification_desc，红字 #ff0606 渲染）",
    "权限引导 Activity 内的文案（sa__permission_title『Please turn on permission』、sa__permission_open_accessibility『Enable Accessibility』、sa__permission_float_window『Grant Floating Window permission』、sa__usage_stat_permission_title『Please turn on usage rights』），承载组件运行期下发",
    "透明/无标题全屏主题的临时 Activity（BoostTempActivity、BoostProcessingMonitorActivity、SettingTipsActivity、NhkRSDActivity）作为跳转中转与弹窗宿主",
    "悬浮窗叠层（SYSTEM_ALERT_WINDOW 已申请，配合 flagIncludeNotImportantViews/flagReportViewIds 在系统设置页上定位控件绘制指引）",
    "安装/更新诱导文案『Please click to install』『Download completed』（sa__click_to_install、sa__download_completed）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please turn on the button in the top-right corner. \n\nPowerful clean the background apps that use memory.\n\nNotice: We will NOT collect any personal data.",
      "text_zh": "请打开右上角的按钮。强大的清理占用内存的后台应用。注意：我们不会收集任何个人数据。",
      "source_location": "res/values/strings.xml key=sa__detection_service_des（经 res/xml/sa__detection_service_config.xml android:description 呈现于系统无障碍列表）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility",
      "text_zh": "启用无障碍",
      "source_location": "res/values/strings.xml key=sa__permission_open_accessibility",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please turn on permission",
      "text_zh": "请开启权限",
      "source_location": "res/values/strings.xml key=sa__permission_title",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant Floating Window permission",
      "text_zh": "授予悬浮窗权限",
      "source_location": "res/values/strings.xml key=sa__permission_float_window",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please turn on usage rights",
      "text_zh": "请开启使用情况访问权限",
      "source_location": "res/values/strings.xml key=sa__usage_stat_permission_title",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Your phone is abnormally slow",
      "text_zh": "您的手机异常缓慢",
      "source_location": "res/values/strings.xml key=sa__boost_phone_slow_title",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Click here to clean up the background apps",
      "text_zh": "点击此处清理后台应用",
      "source_location": "res/values/strings.xml key=sa__boost_phone_slow_description",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Found a lot of junk files in the phone,<font color=#ff0606>Clean up now! </font>",
      "text_zh": "手机中发现大量垃圾文件，立即清理！",
      "source_location": "res/values/strings.xml key=sa__junk_clean_notification_desc2",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Please click to install",
      "text_zh": "请点击安装",
      "source_location": "res/values/strings.xml key=sa__click_to_install",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Excessive phone memory usage / Press for instant speed increase, and free memory",
      "text_zh": "手机内存占用过高 / 按下立即提速并释放内存",
      "source_location": "res/values/strings.xml key=sa__boost_memory_usage_high_title / sa__boost_memory_usage_high_description",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "静态不可完全还原：拒绝/返回后由后台服务与定时 Receiver（ModuleXTaskReceiver、BoostEventReceiver、CleanMasterReceiver、FlightTaskReceiver/HearingTaskReceiver 等）再次拉起 PermissionProxyActivity/UsageProxyActivity/SettingTipsActivity 并重新弹通知，形成循环；循环间隔与次数由运行期下发模块控制，未在静态代码中确认。",
    "overlay_or_fake_settings": "已申请 SYSTEM_ALERT_WINDOW，无障碍服务配置开启 flagIncludeNotImportantViews/flagReportViewIds/flagRequestFilterKeyEvents 并按视图 ID 定位控件，具备在系统无障碍设置页上叠加半透明指引遮罩的技术条件；遮罩绘制代码在运行期下发模块中，未见高仿系统开关页资源。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=22，安装包为 2020 年样本，未针对 Android 13+ 受限设置/会话安装器做教学，跳转仍走传统设置页）。",
    "post_grant_anti_removal": "静态不可确认：无障碍事件类型含 typeWindowStateChanged/typeWindowContentChanged 且可读取窗口内容，具备监听设置页并执行返回/Home 阻止撤权的条件，但 GLOBAL_ACTION_BACK/HOME 调用点位于运行期下发模块，未在静态代码中确认。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到当前焦点为系统无障碍设置页（com.android.settings/.accessibility.AccessibilitySettings 或 Settings$AccessibilitySettingsActivity）或应用详情页，且同时存在来自 com.sstfsk.cleanmaster 的悬浮窗窗口时拉起 UTG；另在冷启动后收到该包通知点击（Boost/Clean 通知）瞬间同步抓取，以捕获跳转前的引导弹窗。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前引导弹窗页（权限总引导）",
        "page_identifier": "com.superman.moduleshell.cleanmaster.PermissionProxyActivity / UsageProxyActivity / SettingTipsActivity 的窗口，含『Please turn on permission』『Enable Accessibility』『Please turn on usage rights』文本与 Continue/Cancel 按钮",
        "why_most_useful": "这是唯一能证明『应用主动引导开无障碍』的界面，可验证是否存在可取消路径以及文案是否为清理工具伪装的假安全理由",
        "observable_utg_signals": ["文本节点『Enable Accessibility』/『Please turn on permission』", "按钮节点是否仅有一个 Continue（无 Cancel/跳过）", "窗口包名 com.sstfsk.cleanmaster 与 Activity 类名"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中 label 为『Clean Master』的服务条目及其描述展开",
        "why_most_useful": "核对系统层面呈现的服务名与说明是否与真实品牌一致，以及描述中的隐私承诺与能力声明矛盾",
        "observable_utg_signals": ["条目文本『Clean Master』", "描述文本『We will NOT collect any personal data.』", "开关 checked 状态变化"]
      },
      {
        "page_role": "设置页后压栈遮罩页",
        "page_identifier": "系统设置 Activity 之上叠加的 TYPE_APPLICATION_OVERLAY/TYPE_SYSTEM_ALERT 窗口（来源包 com.sstfsk.cleanmaster）",
        "why_most_useful": "判定是否使用悬浮窗在系统页上做『点右上角』指引遮罩，是区别于良性应用的关键特征",
        "observable_utg_signals": ["window 层存在非 Settings 包的全屏/半透明 overlay", "overlay 内文本『Please turn on the button in the top-right corner.』", "overlay 覆盖的坐标是否指向无障碍开关位置"]
      },
      {
        "page_role": "通知栏诱导入口",
        "page_identifier": "通知标题『Your phone is abnormally slow』/『Clean notification』/红字『Clean up now!』，点击后跳转链路",
        "why_most_useful": "确认冷启动/后台唤起路径是通知而非用户主动打开图标（应用无 LAUNCHER 入口）",
        "observable_utg_signals": ["通知文本与包名", "点击后落地的 Activity 类名", "落地是否直接为权限引导页"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：无障碍服务的真实业务逻辑（RTemplateAccessibilityService 为空壳，getIndex 仅返回 10）与所有页面构建/设置跳转/遮罩绘制均由 moduleshell 运行期下发模块执行，静态 dex 内无 ACTION_ACCESSIBILITY_SETTINGS 等字面量，属一阶段 Dropper/模块化外壳结构；因此『拒绝后重跳循环、获权后是否阻止撤权』等动态细节必须依赖运行期 UTG/Hook 才能定性，静态侧仅能确认服务声明、能力配置与全部诱导文案。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.superman.moduleshell.cleanmaster.AccessibilityDetectService#getIndex",
    "com.superman.module.api.template.RTemplateAccessibilityService#onAccessibilityEvent",
    "com.sthnsqqwel.cleanmaster.aa#onCreate",
    "com.superman.moduleshell.cleanmaster.PermissionProxyActivity#getIndex",
    "res/xml/sa__detection_service_config.xml",
    "res/values/strings.xml#L23-L27"
  ]
}
```

</details>

# MR_030__745fdbf7c7｜StealJob — Update Service

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：124.0s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即以不可取消的『Checking <机型> Compatibility』伪兼容检测弹窗开局，3.5 秒后把同一弹窗改成索要无障碍权限的文案并一键跳转 ACCESSIBILITY_SETTINGS；无论用户是否授权，返回后一律进入『机型不支持、正在自动卸载』的假卸载页，并在 2 秒后禁用自身启动组件抹掉桌面图标，实现『已卸载』假象下继续由无障碍服务窃取输入事件。
- **静态可见性说明**：全流程静态完整可见：Manifest、res/xml/myserviceconfig.xml、res/layout/dialog_one.xml、dialog_two.xml、activity_unkown.xml、res/values/strings.xml 与 MainActivity/Activity_Unknown/CoreAccessibilityService 及 4 个匿名内部类的反编译方法体均已还原；无加壳、无 VMP、无 AES 加密载荷、无 WebView 远端 HTML、无动态下发文案。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `745fdbf7c78d971e0e82ee22861fc6279301aaae1683b7f5c06babc5bafd94ac` |
| 包名 / 年份 | `com.update.android.v2.test3` / 2019 |
| 家族 / 品类 | **StealJob**（同池样本数：4） |
| 原始来源标识 | https://ti.360.net/blog/articles/stealjob-new-android-malware-used-by-donot-apt-group-en/ |
| 桌面显示名 | Update Service |
| 引导页宣称品牌/身份 | 冒充系统/厂商的『更新服务』与设备兼容性检测程序，并在索权文案中以自身名 Update Service 作为需要无障碍权限的系统组件 |
| 系统无障碍列表服务名 | Update Service（CoreAccessibilityService 未配置 android:label，系统无障碍列表回落显示 application android:label=@string/app_name 即 'Update Service'；亦无 android:description） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务故意不配置 android:label/android:description，使系统无障碍列表只显示与系统更新服务同名的 'Update Service'；strings.xml 中写好却从未被 myserviceconfig 引用的隐私承诺 'We use this service to access notifications intended for this App. We DONT collect any other info.' 因此永不展示；跳转设置后以 PackageManager.setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP) 禁用 MainActivity 与 Activity_Unknown 组件，抹除桌面图标与入口，制造『应用已卸载』假象 |
| 无障碍服务类名 | `com.simpleapp.accessibility.CoreAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.simpleapp.activities.MainActivity（LAUNCHER 入口）+ 原生 Dialog（res/layout/dialog_one.xml） | onCreate() 内直接调用 showDialog() | 原生Dialog | **原文**：INFORMATION / Checking <Build.MODEL> Compatibility / Please Wait..<br>**译注**：『信息』标题；正在检查 <机型> 兼容性；请稍候……（配不确定进度条，伪装系统兼容性自检） | 无任何可操作控件：dialog.setCancelable(false)，返回键/点击外部无效，Okay 按钮此时 visibility=gone，唯一出路是等待 | `com.simpleapp.activities.MainActivity#showDialog` |
| 2 | 引导说明页 | 同一个 dialogone（dialog_one.xml 内 accmsgtv / checkdvtv / pv2 / plztv / okay 控件切换可见性） | new Handler().postDelayed(new MainActivity$2(this), 3500L) 延时回调 | 原生Dialog | **原文**：You must enable Accessiblity for 'Update Service' to use this application properly<br>**译注**：你必须为『Update Service』启用无障碍功能，才能正常使用本应用 | 只能点击唯一的 Okay 按钮（无取消、无稍后、无跳过） | `com.simpleapp.activities.MainActivity$2#run` |
| 3 | 跳无障碍设置 | 系统『无障碍 / 已安装的服务』设置页（android.settings.ACCESSIBILITY_SETTINGS） | MainActivity$3.onClick() 点击 Okay：startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))，同时置 acccheck=true | 系统无障碍页 | **原文**：无（由系统设置页呈现，列表项名称为 'Update Service'）<br>**译注**：系统无障碍服务列表，用户在列表中需自行找到并开启名为 Update Service 的服务（无 description 说明） | 在系统列表中开启 'Update Service' 开关（应用侧无引导高亮、无遮罩、无假开关页） | `com.simpleapp.activities.MainActivity$3#onClick` |
| 4 | 拒权反馈循环 | MainActivity.onStop + com.simpleapp.util.ActivityUtil.removeMainActivityFromLauncher / removeShortcutFromHomeScreen | 用户按返回或 Home 离开（onStop），若未点 Okay 跳设置则 acccheck=false → 走 else 分支 | 无界面（静默执行） | 无 | 无交互，用户只会看到桌面图标凭空消失 | `com.simpleapp.activities.MainActivity#onStop` |
| 5 | 拒权反馈循环 | 原生 Dialog（res/layout/dialog_two.xml）+ Activity_Unknown（activity_unkown.xml 假卸载页） | 两条路径：①onResume 第二次进入（从系统无障碍设置返回，无论是否真正开启服务）→ showDialogTwo() + launchnow()；②onCreate 后 15 秒 Handler(MainActivity$1) 兜底触发 | 原生Dialog | **原文**：<Build.MODEL> Does not support this application. Don't worry application will uninstall automatically. / Note : Don't switch to any other application. / Application Not Supported By Your Device. Uninstall in Progress..<br>**译注**：『<机型> 不支持本应用。别担心，应用将自动卸载。』『注意：不要切换到任何其他应用。』并 Toast『你的设备不支持本应用，正在卸载……』 | 只能点 Okay（setCancelable(false)，无取消），被要求『不要切换到其他应用』以阻止用户去撤销权限或查看系统设置 | `com.simpleapp.activities.MainActivity#onResume / com.simpleapp.activities.MainActivity#launchnow / com.simpleapp.activities.MainActivity#showDialogTwo` |
| 6 | 获权后动作 | com.simpleapp.activities.Activity_Unknown（假卸载进度页）+ PackageManager 组件禁用 + com.simpleapp.accessibility.CoreAccessibilityService | Activity_Unknown.onCreate 后 2 秒 Activity_Unknown$1.run；或点击 DONE（Activity_Unknown$2.onClick） | 原生Activity | **原文**：Uninstalling... / App Uninstalled / CANCEL / DONE<br>**译注**：『正在卸载……』『应用已卸载』，CANCEL / DONE 两个按钮（两者实际都只是禁用组件，并不会真的卸载） | 点 DONE 或等待自动完成；用户以为卸载成功，实际仅 Activity 被 setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP) 禁用，进程与无障碍服务继续运行并持续上报 KEY_LOG 事件 | `com.simpleapp.activities.Activity_Unknown$1#run / com.simpleapp.activities.Activity_Unknown$2#onClick / com.simpleapp.accessibility.CoreAccessibilityService#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity.onCreate → showDialog()：不可取消（setCancelable(false)）、无标题、透明底 CardView 原生 Dialog，res/layout/dialog_one.xml，正文含 'INFORMATION' 表头、动态拼接 'Checking <Build.MODEL> Compatibility'、'Please Wait..' 与不确定进度条
- 同一 dialog_one 内 accmsgtv（初始 gone，3.5 秒后由 MainActivity$2 显示）：'You must enable Accessiblity for 'Update Service' to use this application properly'，同时显示 okay 按钮
- MainActivity.onResume → showDialogTwo()：不可取消原生 Dialog，res/layout/dialog_two.xml，两行 TextView 分别为 '<MODEL> Does not support this application. Don't worry application will uninstall automatically.' 与 'Note : Don't switch to any other application. '，配 Okay 按钮
- Toast（launchnow 与 MainActivity$1.run）：'Application Not Supported By Your Device. Uninstall in Progress..'
- Activity_Unknown 假卸载 Activity（res/layout/activity_unkown.xml）：顶部卡片 ic_launcher + TextView 文本 'Goawy'（布局默认值，运行时被 setText(getString(2131427357)) 覆盖为 app_name 'Update Service'）、'Uninstalling...'、CANCEL、'App Uninstalled'、DONE
- 系统无障碍列表项：CoreAccessibilityService 未设 android:label/android:description，仅显示 'Update Service'；res/xml/myserviceconfig.xml 无 description 属性
- res/values/strings.xml 的 description_accessibility_service（隐私承诺文案）未被任何无障碍配置或界面引用，属死文案，实际从不呈现
- MainActivity$4.onClick（dialog_two 的 Okay）：仅 Toast 'Please wait..'

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Checking %s Compatibility（代码中为 "Checking " + Build.MODEL + " Compatibility"） | 正在检查 <机型> 兼容性 | `com.simpleapp.activities.MainActivity#showDialog 硬编码字符串 / res/layout/dialog_one.xml@id/checkdvtv` | 假更新 |
| en | You must enable Accessiblity for 'Update Service' to use this application properly | 你必须为『Update Service』启用无障碍功能，才能正常使用本应用 | `com.simpleapp.activities.MainActivity$2#run 硬编码字符串 / res/layout/dialog_one.xml@id/accmsgtv` | 故障恐吓 |
| en | Please Wait.. | 请稍候…… | `res/layout/dialog_one.xml@id/plztv` | 假更新 |
| en | %s Does not support this application. Don't worry application will uninstall automatically.（代码中为 Build.MODEL + " Does not support this application. Don't worry application will uninstall automatically."） | <机型> 不支持本应用。别担心，应用将自动卸载。 | `com.simpleapp.activities.MainActivity#showDialogTwo 硬编码字符串 / res/layout/dialog_two.xml@id/twocheckdvtv` | 故障恐吓 |
| en | Note : Don't switch to any other application. | 注意：不要切换到任何其他应用。 | `com.simpleapp.activities.MainActivity#showDialogTwo 硬编码字符串 / res/layout/dialog_two.xml@id/twochtv` | 教唆忽视警告 |
| en | Application Not Supported By Your Device. Uninstall in Progress.. | 你的设备不支持本应用，正在卸载…… | `com.simpleapp.activities.MainActivity#launchnow 与 MainActivity$1#run 硬编码 Toast` | 故障恐吓 |
| en | Uninstalling... / App Uninstalled | 正在卸载…… / 应用已卸载 | `res/layout/activity_unkown.xml@id/un 与 com.simpleapp.activities.Activity_Unknown$1#run 中 setText("App Uninstalled")` | 未知 |
| en | Update Service | 更新服务（伪装系统更新组件名，同时作为桌面名与无障碍服务显示名） | `res/values/strings.xml@string/app_name` | 假更新 |
| en | We use this service to access notifications intended for this App. We DONT collect any other info. | 我们使用此服务访问本应用的专属通知，我们不收集任何其他信息。 | `res/values/strings.xml@string/description_accessibility_service（未被 res/xml/myserviceconfig.xml 引用，实际不展示）` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：两级闭环：①onResume 第二次进入（从系统无障碍设置返回后）不做任何服务启用状态校验（全包无 ENABLED_ACCESSIBILITY_SERVICES / isAccessibilityEnabled 检查），直接弹不可取消的『机型不支持、将自动卸载』对话框并 Toast 后跳 Activity_Unknown 假卸载页；②若用户始终不点 Okay、不离开，onCreate 中 postDelayed 15 秒的 MainActivity$1 会以 scheck=true 兜底弹同样 Toast 并跳假卸载页；③若用户按返回/Home 拒绝，onStop 的 else 分支静默调用 ActivityUtil.removeMainActivityFromLauncher + removeShortcutFromHomeScreen 抹掉桌面入口，再启动应用只能看到入口消失
- **遮罩叠层 / 高仿系统设置页**：无遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；仅使用两个透明底、不可取消的 300dip CardView 原生 Dialog（伪装成系统 INFORMATION 提示框）
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=22（minSdk 15），远早于 Android 13 受限设置机制，代码中不存在 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、也不存在 Session 安装器绕过逻辑
- **获权后即时行为与防撤权机制**：获权/返回后立即进入 Activity_Unknown 假卸载页，2 秒后 Activity_Unknown$1.run 与 DONE 按钮均执行 PackageManager.setComponentEnabledSetting(getComponentName(), COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP)，禁用 MainActivity 与 Activity_Unknown 组件使图标与入口消失，使用户无法再从桌面进入应用去关闭无障碍；未发现用 GLOBAL_ACTION_BACK/HOME 主动阻止撤权的代码（CoreAccessibilityService.onAccessibilityEvent 仅转发点击/文本变化/窗口变化事件为 KEY_LOG 广播）
- **良性降级 / 替代方案**：无。不存在手动模式、ADB 说明或仅观看模式等降级路径；未授权与已授权在 UI 上被同等对待，一律导向『自动卸载』假象

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在冷启动 MainActivity 出现后立即开始 UTG 采集（第 0 步即弹框，无前置交互）；并在监测到 startActivity 的 Intent action = android.settings.ACCESSIBILITY_SETTINGS 时打点，把设置页与返回后压栈的『机型不支持』对话框作为同一会话连续捕获，避免漏掉从系统设置返回的瞬时切换
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无图文诱饵，全部关键文案为纯文本，UTG 可直接提取。需注意两点时序盲区：①首屏弹窗与 3.5 秒后的索权文案是同一窗口的内容替换，若仅在启动瞬间截取一次会只看到『Checking 兼容性』而误判为良性自检，须做时间序列采样；②最后一步依赖组件禁用后图标消失，纯界面 UTG 无法观察『进程仍存活』，需配合 ps/无障碍服务状态查询才能证明恶意持续性。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动伪兼容检测弹窗页（0 步触发、不可取消）** | 透明底圆角卡片弹窗，表头 'INFORMATION'，正文 'Checking <机型> Compatibility' + 不确定进度条 + 'Please Wait..'，无任何可点控件 | 这是全流程唯一的第一现场，能在用户做任何操作前就固定『伪装系统提示框索要无障碍』的证据；文本可纯 UTG 提取，无需 OCR | 包名 com.update.android.v2.test3 下的 Dialog 窗口（非 Activity 全屏）；可见文本 'INFORMATION' / 'Checking ... Compatibility' / 'Please Wait..'；无可点击节点且返回键无效（不可取消特征） |
| **索权说明页（同一弹窗 3.5 秒后变脸）** | 同一 Dialog 内出现文本 'You must enable Accessiblity for 'Update Service' to use this application properly' 与唯一 Okay 按钮 | 直接给出『为 Update Service 开启无障碍』的逐字话术，是判定诱导与身份冒充的关键文本证据 | 文本节点包含 'enable Accessiblity' 与 'Update Service'；仅一个可点击节点（Okay），无取消/跳过节点；与上一步为同一窗口 ID，体现文案二次替换 |
| **系统无障碍服务列表项** | 系统设置 ACTION_ACCESSIBILITY_SETTINGS 页面中名为 'Update Service' 的服务条目，无副标题说明 | 证明跳转目标确为真实系统无障碍页（非伪造页面），并记录列表项显示名与缺失 description 造成的身份混淆 | 系统包 com.android.settings 的窗口；列表项文本 'Update Service' 且无描述文本；开关初始为关闭状态 |
| **返回后压栈的『机型不支持/自动卸载』恐吓弹窗页** | Dialog 内两行文本 '<机型> Does not support this application. Don't worry application will uninstall automatically.' 与 'Note : Don't switch to any other application. ' | 这是拒权/返回后的反馈循环证据：无论是否真正开启服务都会出现，可判定为无校验的软强制而非良性降级 | 返回系统设置后约 0–1 秒内出现的 Dialog；文本包含 'Does not support this application' 与 'uninstall automatically'；同一时刻出现 Toast 'Application Not Supported By Your Device. Uninstall in Progress..' |
| **假卸载页 + 桌面图标消失** | Activity_Unknown：'Uninstalling...' 进度条、'App Uninstalled'、CANCEL/DONE；随后桌面该应用图标消失但进程存活 | 证明『卸载假象』与组件自禁用，是用户以为已卸载而恶意服务继续运行的关键现场 | 页面文本 'Uninstalling...' / 'App Uninstalled' / 'DONE'；返回桌面后 LAUNCHER 中不再有 Update Service 条目；adb shell ps 仍可见 com.update.android.v2.test3 进程与无障碍服务运行 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.simpleapp.activities.MainActivity#showDialog`
- `com.simpleapp.activities.MainActivity$2#run`
- `com.simpleapp.activities.MainActivity$3#onClick`
- `com.simpleapp.activities.MainActivity#onResume`
- `com.simpleapp.activities.MainActivity#onStop`
- `res/layout/dialog_one.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**静态可见性：完全可见（clear）**。全流程均为原生 Java 代码与本地 layout/strings，无加壳、无 WebView、无远端 HTML、无悬浮窗遮罩。

**引导链（冷启动 0 步触发，全程不可取消）**

1. **冷启动即弹框**：`MainActivity.onCreate` 直接 `showDialog()`，`setCancelable(false)`、无标题、透明底 `CardView` 弹窗，标题 "INFORMATION"，正文 `"Checking <Build.MODEL> Compatibility"` + 转圈进度条 + `"Please Wait.."` —— 伪装成系统/厂商兼容性检测。无任何取消/跳过按钮（`dialog_one.xml` 中 `okay` 按钮初始 `visibility=gone`）。
2. **3.5 秒后变脸为索权文案**：`MainActivity$2.run` 隐藏检测文本与进度条，显示 `"You must enable Accessiblity for 'Update Service' to use this application properly"` 与 `Okay` 按钮（原文拼写错误 "Accessiblity"）。
3. **点击 Okay 直跳系统无障碍页**：`MainActivity$3.onClick` → `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，并置 `acccheck=true`。这是**全应用唯一一处跳无障碍设置**，未使用 `ACTION_APPLICATION_DETAILS_SETTINGS`，无受限设置分步教学（targetSdk 22，早于 Android 13 限制）。
4. **离场即隐藏图标（反卸载/反侦查）**：`onStop` 中若 `acccheck` 为真则 `scheck=true`；若用户没去设置而是按返回/Home，则 `scheck=false` 且 `ActivityUtil.removeMainActivityFromLauncher()` + `removeShortcutFromHomeScreen()`，桌面图标被抹掉。
5. **返回即"假卸载"恐吓页**：`onResume` 第二次进入（从系统设置返回）**不校验无障碍是否真的开启**（未查 `ENABLED_ACCESSIBILITY_SERVICES`），直接 `showDialogTwo()`（同样 `setCancelable(false)`）：`"<MODEL> Does not support this application. Don't worry application will uninstall automatically."` + `"Note : Don't switch to any other application. "`，随即 `launchnow()` Toast `"Application Not Supported By Your Device. Uninstall in Progress.."` 并跳 `Activity_Unknown`。
6. **15 秒兜底重跳**：`onCreate` 中 `new Handler().postDelayed(new MainActivity$1(this), 15000L)`，若用户始终未离开（`scheck` 为真）同样弹出假卸载 Toast 并进 `Activity_Unknown`，形成"不给权就走到卸载页"的软强制闭环。
7. **假卸载页完成隐身**：`Activity_Unknown` 展示 `"Uninstalling..."` 进度（60%）、`CANCEL`/`DONE`；2 秒后 `Activity_Unknown$1.run` 调用 `PackageManager.setComponentEnabledSetting(getComponentName(), COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP)` 禁用自身 Activity 组件，`DONE` 按钮同样只做这件事 —— 用户以为已卸载，进程与无障碍服务仍在后台（`CoreAccessibilityService.onAccessibilityEvent` 持续把 `TYPE_VIEW_CLICKED/TEXT_CHANGED/WINDOW_STATE_CHANGED` 事件外发为 `KEY_LOG` 广播）。

**身份不一致**：桌面名 `Update Service`（仿系统更新服务），无障碍服务无 `android:label`、无 `android:description`，系统无障碍列表里只显示应用名 "Update Service"；`strings.xml` 中那条 `"We use this service to access notifications intended for this App. We DONT collect any other info."`（`description_accessibility_service`）**并未被 `myserviceconfig.xml` 引用**，即隐私承诺文案根本不会展示给用户；`myserviceconfig.xml` 只声明 `typeAllMask` + `canRetrieveWindowContent="true"`（可读取全屏控件内容）。strings 里那批 "Google Play services" 文案来自 GMS 库，属良性 SDK 残留，非本应用话术。

**未发现**：叠加半透明引导遮罩、伪造系统无障碍开关页、获权后 `GLOBAL_ACTION_BACK` 阻止撤权、WebView/远端 HTML、Session 安装器绕过。`MainActivity$4`（假卸载弹窗的 Okay）仅弹 "Please wait.." Toast。

> 说明：本轮为遵守 ≤14 次调用的硬性预算，未再调用 `record_risk` 写入项目风险台账；以下结论均由已读取的 Manifest、layout、strings 与反编译方法体直接支撑。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全流程静态完整可见：Manifest、res/xml/myserviceconfig.xml、res/layout/dialog_one.xml、dialog_two.xml、activity_unkown.xml、res/values/strings.xml 与 MainActivity/Activity_Unknown/CoreAccessibilityService 及 4 个匿名内部类的反编译方法体均已还原；无加壳、无 VMP、无 AES 加密载荷、无 WebView 远端 HTML、无动态下发文案。",
  "summary_one_liner": "冷启动即以不可取消的『Checking <机型> Compatibility』伪兼容检测弹窗开局，3.5 秒后把同一弹窗改成索要无障碍权限的文案并一键跳转 ACCESSIBILITY_SETTINGS；无论用户是否授权，返回后一律进入『机型不支持、正在自动卸载』的假卸载页，并在 2 秒后禁用自身启动组件抹掉桌面图标，实现『已卸载』假象下继续由无障碍服务窃取输入事件。",
  "disguise_identity": {
    "app_display_name": "Update Service",
    "claimed_brand_or_persona": "冒充系统/厂商的『更新服务』与设备兼容性检测程序，并在索权文案中以自身名 Update Service 作为需要无障碍权限的系统组件",
    "a11y_service_label": "Update Service（CoreAccessibilityService 未配置 android:label，系统无障碍列表回落显示 application android:label=@string/app_name 即 'Update Service'；亦无 android:description）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务故意不配置 android:label/android:description，使系统无障碍列表只显示与系统更新服务同名的 'Update Service'；strings.xml 中写好却从未被 myserviceconfig 引用的隐私承诺 'We use this service to access notifications intended for this App. We DONT collect any other info.' 因此永不展示；跳转设置后以 PackageManager.setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP) 禁用 MainActivity 与 Activity_Unknown 组件，抹除桌面图标与入口，制造『应用已卸载』假象"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.simpleapp.activities.MainActivity（LAUNCHER 入口）+ 原生 Dialog（res/layout/dialog_one.xml）",
      "trigger_event": "onCreate() 内直接调用 showDialog()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "INFORMATION / Checking <Build.MODEL> Compatibility / Please Wait..",
      "shown_text_zh": "『信息』标题；正在检查 <机型> 兼容性；请稍候……（配不确定进度条，伪装系统兼容性自检）",
      "user_action_requested": "无任何可操作控件：dialog.setCancelable(false)，返回键/点击外部无效，Okay 按钮此时 visibility=gone，唯一出路是等待",
      "code_anchor": "com.simpleapp.activities.MainActivity#showDialog"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "同一个 dialogone（dialog_one.xml 内 accmsgtv / checkdvtv / pv2 / plztv / okay 控件切换可见性）",
      "trigger_event": "new Handler().postDelayed(new MainActivity$2(this), 3500L) 延时回调",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "You must enable Accessiblity for 'Update Service' to use this application properly",
      "shown_text_zh": "你必须为『Update Service』启用无障碍功能，才能正常使用本应用",
      "user_action_requested": "只能点击唯一的 Okay 按钮（无取消、无稍后、无跳过）",
      "code_anchor": "com.simpleapp.activities.MainActivity$2#run"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统『无障碍 / 已安装的服务』设置页（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "MainActivity$3.onClick() 点击 Okay：startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))，同时置 acccheck=true",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（由系统设置页呈现，列表项名称为 'Update Service'）",
      "shown_text_zh": "系统无障碍服务列表，用户在列表中需自行找到并开启名为 Update Service 的服务（无 description 说明）",
      "user_action_requested": "在系统列表中开启 'Update Service' 开关（应用侧无引导高亮、无遮罩、无假开关页）",
      "code_anchor": "com.simpleapp.activities.MainActivity$3#onClick"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity.onStop + com.simpleapp.util.ActivityUtil.removeMainActivityFromLauncher / removeShortcutFromHomeScreen",
      "trigger_event": "用户按返回或 Home 离开（onStop），若未点 Okay 跳设置则 acccheck=false → 走 else 分支",
      "ui_carrier": "无界面（静默执行）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无提示，静默把 MainActivity 组件从桌面移除并删除桌面快捷方式，应用图标消失",
      "user_action_requested": "无交互，用户只会看到桌面图标凭空消失",
      "code_anchor": "com.simpleapp.activities.MainActivity#onStop"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "原生 Dialog（res/layout/dialog_two.xml）+ Activity_Unknown（activity_unkown.xml 假卸载页）",
      "trigger_event": "两条路径：①onResume 第二次进入（从系统无障碍设置返回，无论是否真正开启服务）→ showDialogTwo() + launchnow()；②onCreate 后 15 秒 Handler(MainActivity$1) 兜底触发",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "<Build.MODEL> Does not support this application. Don't worry application will uninstall automatically. / Note : Don't switch to any other application. / Application Not Supported By Your Device. Uninstall in Progress..",
      "shown_text_zh": "『<机型> 不支持本应用。别担心，应用将自动卸载。』『注意：不要切换到任何其他应用。』并 Toast『你的设备不支持本应用，正在卸载……』",
      "user_action_requested": "只能点 Okay（setCancelable(false)，无取消），被要求『不要切换到其他应用』以阻止用户去撤销权限或查看系统设置",
      "code_anchor": "com.simpleapp.activities.MainActivity#onResume / com.simpleapp.activities.MainActivity#launchnow / com.simpleapp.activities.MainActivity#showDialogTwo"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.simpleapp.activities.Activity_Unknown（假卸载进度页）+ PackageManager 组件禁用 + com.simpleapp.accessibility.CoreAccessibilityService",
      "trigger_event": "Activity_Unknown.onCreate 后 2 秒 Activity_Unknown$1.run；或点击 DONE（Activity_Unknown$2.onClick）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Uninstalling... / App Uninstalled / CANCEL / DONE",
      "shown_text_zh": "『正在卸载……』『应用已卸载』，CANCEL / DONE 两个按钮（两者实际都只是禁用组件，并不会真的卸载）",
      "user_action_requested": "点 DONE 或等待自动完成；用户以为卸载成功，实际仅 Activity 被 setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP) 禁用，进程与无障碍服务继续运行并持续上报 KEY_LOG 事件",
      "code_anchor": "com.simpleapp.activities.Activity_Unknown$1#run / com.simpleapp.activities.Activity_Unknown$2#onClick / com.simpleapp.accessibility.CoreAccessibilityService#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "MainActivity.onCreate → showDialog()：不可取消（setCancelable(false)）、无标题、透明底 CardView 原生 Dialog，res/layout/dialog_one.xml，正文含 'INFORMATION' 表头、动态拼接 'Checking <Build.MODEL> Compatibility'、'Please Wait..' 与不确定进度条",
    "同一 dialog_one 内 accmsgtv（初始 gone，3.5 秒后由 MainActivity$2 显示）：'You must enable Accessiblity for 'Update Service' to use this application properly'，同时显示 okay 按钮",
    "MainActivity.onResume → showDialogTwo()：不可取消原生 Dialog，res/layout/dialog_two.xml，两行 TextView 分别为 '<MODEL> Does not support this application. Don't worry application will uninstall automatically.' 与 'Note : Don't switch to any other application. '，配 Okay 按钮",
    "Toast（launchnow 与 MainActivity$1.run）：'Application Not Supported By Your Device. Uninstall in Progress..'",
    "Activity_Unknown 假卸载 Activity（res/layout/activity_unkown.xml）：顶部卡片 ic_launcher + TextView 文本 'Goawy'（布局默认值，运行时被 setText(getString(2131427357)) 覆盖为 app_name 'Update Service'）、'Uninstalling...'、CANCEL、'App Uninstalled'、DONE",
    "系统无障碍列表项：CoreAccessibilityService 未设 android:label/android:description，仅显示 'Update Service'；res/xml/myserviceconfig.xml 无 description 属性",
    "res/values/strings.xml 的 description_accessibility_service（隐私承诺文案）未被任何无障碍配置或界面引用，属死文案，实际从不呈现",
    "MainActivity$4.onClick（dialog_two 的 Okay）：仅 Toast 'Please wait..'"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Checking %s Compatibility（代码中为 \"Checking \" + Build.MODEL + \" Compatibility\"）",
      "text_zh": "正在检查 <机型> 兼容性",
      "source_location": "com.simpleapp.activities.MainActivity#showDialog 硬编码字符串 / res/layout/dialog_one.xml@id/checkdvtv",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "You must enable Accessiblity for 'Update Service' to use this application properly",
      "text_zh": "你必须为『Update Service』启用无障碍功能，才能正常使用本应用",
      "source_location": "com.simpleapp.activities.MainActivity$2#run 硬编码字符串 / res/layout/dialog_one.xml@id/accmsgtv",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Please Wait..",
      "text_zh": "请稍候……",
      "source_location": "res/layout/dialog_one.xml@id/plztv",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "%s Does not support this application. Don't worry application will uninstall automatically.（代码中为 Build.MODEL + \" Does not support this application. Don't worry application will uninstall automatically.\"）",
      "text_zh": "<机型> 不支持本应用。别担心，应用将自动卸载。",
      "source_location": "com.simpleapp.activities.MainActivity#showDialogTwo 硬编码字符串 / res/layout/dialog_two.xml@id/twocheckdvtv",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Note : Don't switch to any other application. ",
      "text_zh": "注意：不要切换到任何其他应用。",
      "source_location": "com.simpleapp.activities.MainActivity#showDialogTwo 硬编码字符串 / res/layout/dialog_two.xml@id/twochtv",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Application Not Supported By Your Device. Uninstall in Progress..",
      "text_zh": "你的设备不支持本应用，正在卸载……",
      "source_location": "com.simpleapp.activities.MainActivity#launchnow 与 MainActivity$1#run 硬编码 Toast",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Uninstalling... / App Uninstalled",
      "text_zh": "正在卸载…… / 应用已卸载",
      "source_location": "res/layout/activity_unkown.xml@id/un 与 com.simpleapp.activities.Activity_Unknown$1#run 中 setText(\"App Uninstalled\")",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Update Service",
      "text_zh": "更新服务（伪装系统更新组件名，同时作为桌面名与无障碍服务显示名）",
      "source_location": "res/values/strings.xml@string/app_name",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "We use this service to access notifications intended for this App. We DONT collect any other info.",
      "text_zh": "我们使用此服务访问本应用的专属通知，我们不收集任何其他信息。",
      "source_location": "res/values/strings.xml@string/description_accessibility_service（未被 res/xml/myserviceconfig.xml 引用，实际不展示）",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "两级闭环：①onResume 第二次进入（从系统无障碍设置返回后）不做任何服务启用状态校验（全包无 ENABLED_ACCESSIBILITY_SERVICES / isAccessibilityEnabled 检查），直接弹不可取消的『机型不支持、将自动卸载』对话框并 Toast 后跳 Activity_Unknown 假卸载页；②若用户始终不点 Okay、不离开，onCreate 中 postDelayed 15 秒的 MainActivity$1 会以 scheck=true 兜底弹同样 Toast 并跳假卸载页；③若用户按返回/Home 拒绝，onStop 的 else 分支静默调用 ActivityUtil.removeMainActivityFromLauncher + removeShortcutFromHomeScreen 抹掉桌面入口，再启动应用只能看到入口消失",
    "overlay_or_fake_settings": "无遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；仅使用两个透明底、不可取消的 300dip CardView 原生 Dialog（伪装成系统 INFORMATION 提示框）",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=22（minSdk 15），远早于 Android 13 受限设置机制，代码中不存在 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、也不存在 Session 安装器绕过逻辑",
    "post_grant_anti_removal": "获权/返回后立即进入 Activity_Unknown 假卸载页，2 秒后 Activity_Unknown$1.run 与 DONE 按钮均执行 PackageManager.setComponentEnabledSetting(getComponentName(), COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP)，禁用 MainActivity 与 Activity_Unknown 组件使图标与入口消失，使用户无法再从桌面进入应用去关闭无障碍；未发现用 GLOBAL_ACTION_BACK/HOME 主动阻止撤权的代码（CoreAccessibilityService.onAccessibilityEvent 仅转发点击/文本变化/窗口变化事件为 KEY_LOG 广播）",
    "benign_graceful_degradation": "无。不存在手动模式、ADB 说明或仅观看模式等降级路径；未授权与已授权在 UI 上被同等对待，一律导向『自动卸载』假象"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在冷启动 MainActivity 出现后立即开始 UTG 采集（第 0 步即弹框，无前置交互）；并在监测到 startActivity 的 Intent action = android.settings.ACCESSIBILITY_SETTINGS 时打点，把设置页与返回后压栈的『机型不支持』对话框作为同一会话连续捕获，避免漏掉从系统设置返回的瞬时切换",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动伪兼容检测弹窗页（0 步触发、不可取消）",
        "page_identifier": "透明底圆角卡片弹窗，表头 'INFORMATION'，正文 'Checking <机型> Compatibility' + 不确定进度条 + 'Please Wait..'，无任何可点控件",
        "why_most_useful": "这是全流程唯一的第一现场，能在用户做任何操作前就固定『伪装系统提示框索要无障碍』的证据；文本可纯 UTG 提取，无需 OCR",
        "observable_utg_signals": ["包名 com.update.android.v2.test3 下的 Dialog 窗口（非 Activity 全屏）", "可见文本 'INFORMATION' / 'Checking ... Compatibility' / 'Please Wait..'", "无可点击节点且返回键无效（不可取消特征）"]
      },
      {
        "page_role": "索权说明页（同一弹窗 3.5 秒后变脸）",
        "page_identifier": "同一 Dialog 内出现文本 'You must enable Accessiblity for 'Update Service' to use this application properly' 与唯一 Okay 按钮",
        "why_most_useful": "直接给出『为 Update Service 开启无障碍』的逐字话术，是判定诱导与身份冒充的关键文本证据",
        "observable_utg_signals": ["文本节点包含 'enable Accessiblity' 与 'Update Service'", "仅一个可点击节点（Okay），无取消/跳过节点", "与上一步为同一窗口 ID，体现文案二次替换"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 ACTION_ACCESSIBILITY_SETTINGS 页面中名为 'Update Service' 的服务条目，无副标题说明",
        "why_most_useful": "证明跳转目标确为真实系统无障碍页（非伪造页面），并记录列表项显示名与缺失 description 造成的身份混淆",
        "observable_utg_signals": ["系统包 com.android.settings 的窗口", "列表项文本 'Update Service' 且无描述文本", "开关初始为关闭状态"]
      },
      {
        "page_role": "返回后压栈的『机型不支持/自动卸载』恐吓弹窗页",
        "page_identifier": "Dialog 内两行文本 '<机型> Does not support this application. Don't worry application will uninstall automatically.' 与 'Note : Don't switch to any other application. '",
        "why_most_useful": "这是拒权/返回后的反馈循环证据：无论是否真正开启服务都会出现，可判定为无校验的软强制而非良性降级",
        "observable_utg_signals": ["返回系统设置后约 0–1 秒内出现的 Dialog", "文本包含 'Does not support this application' 与 'uninstall automatically'", "同一时刻出现 Toast 'Application Not Supported By Your Device. Uninstall in Progress..'"]
      },
      {
        "page_role": "假卸载页 + 桌面图标消失",
        "page_identifier": "Activity_Unknown：'Uninstalling...' 进度条、'App Uninstalled'、CANCEL/DONE；随后桌面该应用图标消失但进程存活",
        "why_most_useful": "证明『卸载假象』与组件自禁用，是用户以为已卸载而恶意服务继续运行的关键现场",
        "observable_utg_signals": ["页面文本 'Uninstalling...' / 'App Uninstalled' / 'DONE'", "返回桌面后 LAUNCHER 中不再有 Update Service 条目", "adb shell ps 仍可见 com.update.android.v2.test3 进程与无障碍服务运行"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无图文诱饵，全部关键文案为纯文本，UTG 可直接提取。需注意两点时序盲区：①首屏弹窗与 3.5 秒后的索权文案是同一窗口的内容替换，若仅在启动瞬间截取一次会只看到『Checking 兼容性』而误判为良性自检，须做时间序列采样；②最后一步依赖组件禁用后图标消失，纯界面 UTG 无法观察『进程仍存活』，需配合 ps/无障碍服务状态查询才能证明恶意持续性。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "com.simpleapp.activities.MainActivity#showDialog",
    "com.simpleapp.activities.MainActivity$2#run",
    "com.simpleapp.activities.MainActivity$3#onClick",
    "com.simpleapp.activities.MainActivity#onResume",
    "com.simpleapp.activities.MainActivity#onStop",
    "res/layout/dialog_one.xml"
  ]
}
```

</details>

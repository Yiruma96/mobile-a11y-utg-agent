# MR_136__0277b5385b｜SpyAgent — كشف رقم واسم المتصل المجهول

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：124.4s

## 1. 一句话核心结论

- **核心申请方式**：该应用无任何引导文案，靠阿拉伯语“识别未知来电”名称伪装，冷启动在透明空白页先索取空说明的设备管理器权限，随后无论同意与否都直接 startActivity 跳转 android.settings.ACCESSIBILITY_SETTINGS，并同步把自身桌面组件禁用隐藏，获权后即成为全量输入监听键盘记录器。
- **静态可见性说明**：全部引导逻辑静态可见：M.onCreate/M.a/M.onActivityResult 与 strings.xml 配置串即完整流程；应用不含壳、不含 AES 密文资源、不含远端 HTML/WebView 引导页，res/raw 仅含内嵌二阶段 APK。唯一不可静态还原的是 C2 samire.ddns.net:2020 下发的后续指令内容（属获权后行为，不影响无障碍引导链判定）。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `0277b5385bcc033e01966990d356dc643814828e23c4a51be3bc7d1629545c5c` |
| 包名 / 年份 | `yps.eton.application` / 2018 |
| 家族 / 品类 | **SpyAgent**（同池样本数：12） |
| 原始来源标识 | https://www.fortinet.com/blog/threat-research/android-spyware-now-dropping-legit-apps- |
| 桌面显示名 | كشف رقم واسم المتصل المجهول |
| 引导页宣称品牌/身份 | 未知来电号码/姓名识别工具（Caller ID，伪装为可显示陌生来电者身份的实用工具，字符串中另出现第三方下载站命名“كشف المتصل المجهول_8.0_apk-dl.com”） |
| 系统无障碍列表服务名 | كشف رقم واسم المتصل المجهول |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未声明 android:description 且无 accessibility-service 配置 XML，系统列表中不展示任何能力说明；服务名与桌面名完全相同，无法从系统页区分“来电识别”与“全量输入监听”；主 Activity 使用 Theme.Translucent.NoTitleBar 且不 setContentView，启动即空白无可读内容；首次运行后通过 setComponentEnabledSetting(M, DISABLED) 自隐藏桌面入口；设备管理器请求 ADD_EXPLANATION 传入空字符串；另设透明、excludeFromRecents、transparent 图标的远端控制 Activity h 隐藏于最近任务之外。 |
| 无障碍服务类名 | `yps.eton.application.k` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | yps.eton.application.M（LAUNCHER Activity，主题 @android:style/Theme.Translucent.NoTitleBar） | 用户点击桌面图标 → M.onCreate | 原生Activity | 无 | 无提示；用户只能看到一闪而过的空白或直接被带到后续系统页面，无取消/跳过按钮 | `yps.eton.application.M#onCreate` |
| 2 | 业务功能触发 | 内嵌载荷释放线程 yps.eton.application.M$1（由 M.b() 启动） | onCreate 中 merge_file="1" 且 charAt(0)=='1' → 检测 package_file 指定包是否已安装，未安装则 b() → new Thread(M$1).start() | 不可静态还原 | 无 | 由系统安装器弹窗要求用户安装内嵌的第二个 APK（本步界面为系统安装器，非应用自绘） | `yps.eton.application.M#b / yps.eton.application.M$1#run` |
| 3 | 跳受限设置 | 系统设备管理器激活页（android.app.action.ADD_DEVICE_ADMIN，由 yps.eton.application.i 提供 DeviceAdminReceiver 组件） | onCreate 中 group_properties.charAt(4) 非 '0' 走 else 分支 → startActivityForResult(intent, 100) | 原生Activity | **原文**：android.app.extra.ADD_EXPLANATION = ""<br>**译注**：系统弹窗中“说明”区域为空字符串，用户看不到任何申请设备管理器权限的理由 | 系统弹窗要求点击“激活/取消”，应用侧无自定义取消或跳过入口 | `yps.eton.application.M#onCreate` |
| 4 | 拒权反馈循环 | yps.eton.application.M#onActivityResult → M#a() | onActivityResult(100, resultCode, intent)：if (resultCode == -1) a(); else a(); —— 两个分支完全相同，无论激活还是拒绝都继续 | 不可静态还原 | 无 | 无选择空间：拒绝设备管理器不会阻止流程，也不会出现任何反馈文案 | `yps.eton.application.M#onActivityResult / yps.eton.application.M#a` |
| 5 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表） | M#a() 中 group_properties.charAt(6)=='1' → Intent.setAction("android.settings.ACCESSIBILITY_SETTINGS") + FLAG_ACTIVITY_NEW_TASK → startActivity | 系统无障碍页 | **原文**：كشف رقم واسم المتصل المجهول<br>**译注**：系统无障碍服务列表中出现与桌面应用同名的一项“识别未知来电号码与姓名”，无任何能力说明（无 android:description） | 要求用户在该系统页手动找到同名条目并打开开关（应用不提供跳转到本服务条目的锚点，需用户自行查找） | `yps.eton.application.M#a / AndroidManifest.xml: yps.eton.application.k` |
| 6 | 获权后动作 | yps.eton.application.k（AccessibilityService） | 用户在系统页开启开关 → onServiceConnected；此后每次 onAccessibilityEvent | 不可静态还原 | **原文**：Package Name:= %s c0c1c3a2c0c1c Text:= %s c0c1c3a2c0c1c Time:= %s c0c1c3a2c0c1c###--- End ---###<br>**译注**：无界面提示；静默把每个应用（含输入法、聊天、短信界面）的控件文本与时间戳拼接上报，另在 A.i 为真时输出 key_logger 关键日志到 host=samire.ddns.net,2020 | 无；用户无感知，且桌面图标此时已被隐藏，难以回到应用撤销授权 | `yps.eton.application.k#onServiceConnected / yps.eton.application.k#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 应用自身：无任何引导/说明文字载体——M.onCreate 未调用 setContentView，全包未检索到 AlertDialog、WebView、WindowManager 悬浮窗调用；strings.xml 仅含 app_name/service_name/client_name 等名称与配置串
- 系统无障碍列表项名称：res/values/strings.xml 的 service_name（= app_name = كشف رقم واسم المتصل المجهول），由 Manifest 中 yps.eton.application.k 的 android:label 引用；服务未声明 android:description，列表内无能力说明文本
- 系统设备管理器弹窗：android.app.extra.ADD_EXPLANATION 传入空字符串 ""（yps.eton.application.M#onCreate），弹窗说明区留白
- 系统安装器：内嵌 res/raw APK 以 ACTION_VIEW 方式拉起的安装确认页（yps.eton.application.M$1#run）
- res/values/strings.xml 的 host（samire.ddns.net,2020）、package_file（كشف المتصل المجهول_8.0_apk-dl.com）、group_properties（11111110）为纯配置串，不呈现给用户

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ar | كشف رقم واسم المتصل المجهول | 识别未知来电的号码与姓名 | `res/values/strings.xml → app_name / service_name / client_name（0x7f080021、0x7f080027）` | 清理工具伪装 |
| ar | كشف المتصل المجهول_8.0_apk-dl.com | 识别未知来电者_8.0_apk-dl.com（第三方 APK 下载站命名痕迹） | `res/values/strings.xml → package_file（0x7f080026），被 M.onCreate 用于检测是否已安装同名包` | 未知 |
| en | Package Name:= %s c0c1c3a2c0c1c Text:= %s c0c1c3a2c0c1c Time:= %s c0c1c3a2c0c1c###--- End ---### | 包名、控件文本、时间戳三者拼接的键盘记录上报格式（仅内部日志/上报，不呈现给用户） | `yps.eton.application.k#onAccessibilityEvent（硬编码拼接）` | 未知 |
| en | key_loggerfxf0x4x4x0fxfonlinec0c1c3a2c0c1c | 自命名为 key_logger（键盘记录器）的在线日志标记 | `yps.eton.application.k#onAccessibilityEvent（硬编码）` | 未知 |
| en | samire.ddns.net,2020 | 动态 DNS 形式的 C2 主机与端口配置（不呈现给用户） | `res/values/strings.xml → host（0x7f080024）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无显式循环，但拒绝无效：M.onActivityResult 中 resultCode 为 -1 与其它值均调用同一个 a()，即设备管理器被拒绝后仍立即跳转 ACCESSIBILITY_SETTINGS；同时 M 在跳转前已被 setComponentEnabledSetting(..., 2, 1) 禁用并从桌面移除，用户无法再次从图标进入，只能由 BOOT_COMPLETED 接收器 B / AlarmManager 定时器 Z 或远端广播拉起后台逻辑
- **遮罩叠层 / 高仿系统设置页**：无。全包未检索到 WindowManager/悬浮窗或自绘高仿设置页；仅有一个透明、excludeFromRecents 的远端控制 Activity h（由广播 com.xxx.broadcast.xxx 驱动，用于远端聊天/回传，非无障碍引导遮罩）
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=22，跳转直接使用 android.settings.ACCESSIBILITY_SETTINGS，未出现 ACTION_APPLICATION_DETAILS_SETTINGS、未教用户打开“受限设置”菜单，也无 Session 安装器绕过
- **获权后即时行为与防撤权机制**：未见 GLOBAL_ACTION_BACK/HOME 或自点确认逻辑（未检索到 performGlobalAction/GLOBAL_ACTION）；但通过首次运行即禁用桌面组件 + 申请设备管理器权限，使应用在授权后从桌面消失并具备卸载阻力
- **良性降级 / 替代方案**：无。既无手动模式、也无 ADB 说明或“仅观看”降级路径，拒绝授权不会有任何替代功能或提示

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：Hook Activity 启动：一旦监测到 startActivity 目标 action 为 android.settings.ACCESSIBILITY_SETTINGS，立即回拉 UTG；或在冷启动 yps.eton.application.M 出现（1 秒内无任何控件、无文本）后紧接着监测 ADD_DEVICE_ADMIN 弹窗，即可完整覆盖 0 步跳转链
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在三处盲区：一是全流程零文案、零图片，纯靠名称与空白页，基于文本/OCR 的诱导识别会漏检；二是引导发生在系统设置页，应用自身 UI 无痕迹，若仅录屏应用界面会看不到无障碍页；三是应用首跑即禁用自身桌面组件，二次运行需靠 BOOT_COMPLETED 接收器 B 或 AlarmManager 定时器 Z 拉起，纯手工复现可能找不到入口。另有内嵌 res/raw APK 二阶段载荷，其安装后行为需单独捕获。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动透明跳板页** | yps.eton.application.M，Theme.Translucent.NoTitleBar，无布局、无控件、无文本 | 该页为空文本是此家族最关键判别信号：无任何说明却立即走向系统设置，可直接排除良性透明说明型应用 | Activity 名称为混淆短名 M 且主题为 Translucent.NoTitleBar；页面无任何节点文本或可点击控件；停留时间极短（小于 1 秒）后直接离开应用界面 |
| **设备管理器空说明弹窗** | 系统对话框，标题含激活设备管理，说明区为空 | ADD_EXPLANATION 为空是“无理由索取高权限”的直接证据，且其后无论同意与否都跳无障碍页 | 弹窗说明文本为空或仅系统默认语句；弹窗由 yps.eton.application.i 提供的 DeviceAdminReceiver 触发；关闭/拒绝该弹窗后紧接着出现系统无障碍设置页 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务中条目文本为 كشف رقم واسم المتصل المجهول，无副标题说明 | 证明诱导终点即系统无障碍开关，且服务名与来电识别应用同名、零能力说明，构成身份与能力不匹配 | 列表项文本与桌面应用名完全一致；条目下无 description 副文本；上一跳来源包名为 yps.eton.application |
| **获权后静默采集验证页** | 无界面；通过流量侧观测 samire.ddns.net:2020 连接及含 c0c1c3a2c0c1c 分隔符的文本上报 | 确认授权后的真实目的是全量输入监听而非来电识别，为“诱导”提供危害落点 | 开启开关后前台界面无变化、无功能页；网络侧出现 DNS 域名 samire.ddns.net 的 2020 端口连接；上报体包含包名+控件文本+时间戳三段结构 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `yps.eton.application.M#onCreate`
- `yps.eton.application.M#a`
- `yps.eton.application.M#onActivityResult`
- `yps.eton.application.k#onServiceConnected`
- `yps.eton.application.k#onAccessibilityEvent`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验结果）

**核心发现：该样本在无障碍权限获取环节几乎不呈现任何文字引导：它没有任何引导页、弹窗、WebView 或悬浮遮罩，只依赖桌面名称和一个未加说明的设备管理器请求，强制把用户推送到系统无障碍列表页。**

1. **入口是一个“透明跳板”**：`M`（唯一 LAUNCHER Activity）在 Manifest 中继承 `@android:style/Theme.Translucent.NoTitleBar`，其 `onCreate` 不调用 `setContentView`，因此启动时界面空白，没有任何说明文案；`res/values/strings.xml` 里也**没有**任何引导语句（仅 app_name/service_name/client_name 等阿拉伯语名称与配置串）。
2. **执行顺序由配置字符串驱动**：`group_properties="11111110"` 按位控制行为：`charAt(0)=='1'` 时先 `setComponentEnabledSetting(M, DISABLED)` 把桌面图标移除（用完即隐藏），`charAt(6)=='1'` 时才 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`；`merge_file="1"` 触发内嵌 APK 释放安装。
3. **跳无障碍页之前先索取设备管理器权限**：`charAt(4)` 分支走 `android.app.action.ADD_DEVICE_ADMIN`，且 `ADD_EXPLANATION` 传入**空字符串**，系统弹窗中不会出现任何用途说明；`onActivityResult` 无论用户同意还是拒绝，都会进入 `a()` 并跳转到无障碍设置页，也就是说拒绝后仍会被推去授权，且没有取消、跳过或降级路径。
4. **系统无障碍列表中的服务名与应用名相同**：`service_name` 与 `app_name` 都是 `كشف رقم واسم المتصل المجهول`（“识别未知来电号码与姓名”），系统列表里看不出这是“全量输入监听”能力；`k` 未声明 `android:description`，也**没有** `accessibility-service` 配置 XML（即预筛得到的 `description` 为空，因此系统页没有能力说明）。
5. **获得权限后即为全量键盘记录器**：`k.onServiceConnected` 设置 `eventTypes=-1`（监听全部事件）、`flags=89`、`A.h=true`；`onAccessibilityEvent` 把每个包名的控件文本按 `c0c1c3a2c0c1c` 分隔拼接（含 `key_loggerfxf0x4x4x0fxfon...` 关键字日志），随后上报到 `host=samire.ddns.net,2020` 的 C2。
6. **附带二阶段载荷与远端控制窗口**：`M$1.run` 把 `res/raw` 内嵌 APK 写到 `/sdcard/<service_name>/base.apk`，再以 `VIEW` 动作安装（配置串 `package_file` 指向一个 `_8.0_apk-dl.com` 的下载站包名，安装成功后直接拉起）；`h` 是透明、不在最近任务中显示、由广播 `com.xxx.broadcast.xxx` 驱动的远端聊天、控制悬浮 Activity，与无障碍引导无关。

**结论**：该样本的无障碍诱导属于“零文案冷启动直跳系统设置”型，不存在假更新、假反诈、清理工具等任何诱饵话术载体；判别只能依赖“透明空白启动页 → 设备管理器空说明弹窗 → 无结果判断直接跳 ACCESSIBILITY_SETTINGS → 图标自隐藏”这条调用链。静态可见性完整（无壳、无加密资源、无远端 HTML）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑静态可见：M.onCreate/M.a/M.onActivityResult 与 strings.xml 配置串即完整流程；应用不含壳、不含 AES 密文资源、不含远端 HTML/WebView 引导页，res/raw 仅含内嵌二阶段 APK。唯一不可静态还原的是 C2 samire.ddns.net:2020 下发的后续指令内容（属获权后行为，不影响无障碍引导链判定）。",
  "summary_one_liner": "该应用无任何引导文案，靠阿拉伯语“识别未知来电”名称伪装，冷启动在透明空白页先索取空说明的设备管理器权限，随后无论同意与否都直接 startActivity 跳转 android.settings.ACCESSIBILITY_SETTINGS，并同步把自身桌面组件禁用隐藏，获权后即成为全量输入监听键盘记录器。",
  "disguise_identity": {
    "app_display_name": "كشف رقم واسم المتصل المجهول",
    "claimed_brand_or_persona": "未知来电号码/姓名识别工具（Caller ID，伪装为可显示陌生来电者身份的实用工具，字符串中另出现第三方下载站命名“كشف المتصل المجهول_8.0_apk-dl.com”）",
    "a11y_service_label": "كشف رقم واسم المتصل المجهول",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未声明 android:description 且无 accessibility-service 配置 XML，系统列表中不展示任何能力说明；服务名与桌面名完全相同，无法从系统页区分“来电识别”与“全量输入监听”；主 Activity 使用 Theme.Translucent.NoTitleBar 且不 setContentView，启动即空白无可读内容；首次运行后通过 setComponentEnabledSetting(M, DISABLED) 自隐藏桌面入口；设备管理器请求 ADD_EXPLANATION 传入空字符串；另设透明、excludeFromRecents、transparent 图标的远端控制 Activity h 隐藏于最近任务之外。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "yps.eton.application.M（LAUNCHER Activity，主题 @android:style/Theme.Translucent.NoTitleBar）",
      "trigger_event": "用户点击桌面图标 → M.onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "透明空白页面，不加载任何布局，屏幕无任何文字或控件（onCreate 中无 setContentView 调用）",
      "user_action_requested": "无提示；用户只能看到一闪而过的空白或直接被带到后续系统页面，无取消/跳过按钮",
      "code_anchor": "yps.eton.application.M#onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "内嵌载荷释放线程 yps.eton.application.M$1（由 M.b() 启动）",
      "trigger_event": "onCreate 中 merge_file=\"1\" 且 charAt(0)=='1' → 检测 package_file 指定包是否已安装，未安装则 b() → new Thread(M$1).start()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台把 res/raw 中的 base.apk 写入 /sdcard/<service_name>/base.apk，再以 android.intent.action.VIEW + application/vnd.android.package-archive 拉起安装器（二阶段 APK）",
      "user_action_requested": "由系统安装器弹窗要求用户安装内嵌的第二个 APK（本步界面为系统安装器，非应用自绘）",
      "code_anchor": "yps.eton.application.M#b / yps.eton.application.M$1#run"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统设备管理器激活页（android.app.action.ADD_DEVICE_ADMIN，由 yps.eton.application.i 提供 DeviceAdminReceiver 组件）",
      "trigger_event": "onCreate 中 group_properties.charAt(4) 非 '0' 走 else 分支 → startActivityForResult(intent, 100)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "android.app.extra.ADD_EXPLANATION = \"\"",
      "shown_text_zh": "系统弹窗中“说明”区域为空字符串，用户看不到任何申请设备管理器权限的理由",
      "user_action_requested": "系统弹窗要求点击“激活/取消”，应用侧无自定义取消或跳过入口",
      "code_anchor": "yps.eton.application.M#onCreate"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "yps.eton.application.M#onActivityResult → M#a()",
      "trigger_event": "onActivityResult(100, resultCode, intent)：if (resultCode == -1) a(); else a(); —— 两个分支完全相同，无论激活还是拒绝都继续",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何提示或解释，直接执行下一步；同时把自身桌面组件禁用（setComponentEnabledSetting(new ComponentName(this, M.class), 2, 1)）并 finish",
      "user_action_requested": "无选择空间：拒绝设备管理器不会阻止流程，也不会出现任何反馈文案",
      "code_anchor": "yps.eton.application.M#onActivityResult / yps.eton.application.M#a"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表）",
      "trigger_event": "M#a() 中 group_properties.charAt(6)=='1' → Intent.setAction(\"android.settings.ACCESSIBILITY_SETTINGS\") + FLAG_ACTIVITY_NEW_TASK → startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "كشف رقم واسم المتصل المجهول",
      "shown_text_zh": "系统无障碍服务列表中出现与桌面应用同名的一项“识别未知来电号码与姓名”，无任何能力说明（无 android:description）",
      "user_action_requested": "要求用户在该系统页手动找到同名条目并打开开关（应用不提供跳转到本服务条目的锚点，需用户自行查找）",
      "code_anchor": "yps.eton.application.M#a / AndroidManifest.xml: yps.eton.application.k"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "yps.eton.application.k（AccessibilityService）",
      "trigger_event": "用户在系统页开启开关 → onServiceConnected；此后每次 onAccessibilityEvent",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Package Name:= %s c0c1c3a2c0c1c Text:= %s c0c1c3a2c0c1c Time:= %s c0c1c3a2c0c1c###--- End ---###",
      "shown_text_zh": "无界面提示；静默把每个应用（含输入法、聊天、短信界面）的控件文本与时间戳拼接上报，另在 A.i 为真时输出 key_logger 关键日志到 host=samire.ddns.net,2020",
      "user_action_requested": "无；用户无感知，且桌面图标此时已被隐藏，难以回到应用撤销授权",
      "code_anchor": "yps.eton.application.k#onServiceConnected / yps.eton.application.k#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "应用自身：无任何引导/说明文字载体——M.onCreate 未调用 setContentView，全包未检索到 AlertDialog、WebView、WindowManager 悬浮窗调用；strings.xml 仅含 app_name/service_name/client_name 等名称与配置串",
    "系统无障碍列表项名称：res/values/strings.xml 的 service_name（= app_name = كشف رقم واسم المتصل المجهول），由 Manifest 中 yps.eton.application.k 的 android:label 引用；服务未声明 android:description，列表内无能力说明文本",
    "系统设备管理器弹窗：android.app.extra.ADD_EXPLANATION 传入空字符串 \"\"（yps.eton.application.M#onCreate），弹窗说明区留白",
    "系统安装器：内嵌 res/raw APK 以 ACTION_VIEW 方式拉起的安装确认页（yps.eton.application.M$1#run）",
    "res/values/strings.xml 的 host（samire.ddns.net,2020）、package_file（كشف المتصل المجهول_8.0_apk-dl.com）、group_properties（11111110）为纯配置串，不呈现给用户"
  ],
  "verbatim_texts": [
    {
      "lang": "ar",
      "text_verbatim": "كشف رقم واسم المتصل المجهول",
      "text_zh": "识别未知来电的号码与姓名",
      "source_location": "res/values/strings.xml → app_name / service_name / client_name（0x7f080021、0x7f080027）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "ar",
      "text_verbatim": "كشف المتصل المجهول_8.0_apk-dl.com",
      "text_zh": "识别未知来电者_8.0_apk-dl.com（第三方 APK 下载站命名痕迹）",
      "source_location": "res/values/strings.xml → package_file（0x7f080026），被 M.onCreate 用于检测是否已安装同名包",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Package Name:= %s c0c1c3a2c0c1c Text:= %s c0c1c3a2c0c1c Time:= %s c0c1c3a2c0c1c###--- End ---###",
      "source_location": "yps.eton.application.k#onAccessibilityEvent（硬编码拼接）",
      "text_zh": "包名、控件文本、时间戳三者拼接的键盘记录上报格式（仅内部日志/上报，不呈现给用户）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "key_loggerfxf0x4x4x0fxfonlinec0c1c3a2c0c1c",
      "text_zh": "自命名为 key_logger（键盘记录器）的在线日志标记",
      "source_location": "yps.eton.application.k#onAccessibilityEvent（硬编码）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "samire.ddns.net,2020",
      "text_zh": "动态 DNS 形式的 C2 主机与端口配置（不呈现给用户）",
      "source_location": "res/values/strings.xml → host（0x7f080024）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无显式循环，但拒绝无效：M.onActivityResult 中 resultCode 为 -1 与其它值均调用同一个 a()，即设备管理器被拒绝后仍立即跳转 ACCESSIBILITY_SETTINGS；同时 M 在跳转前已被 setComponentEnabledSetting(..., 2, 1) 禁用并从桌面移除，用户无法再次从图标进入，只能由 BOOT_COMPLETED 接收器 B / AlarmManager 定时器 Z 或远端广播拉起后台逻辑",
    "overlay_or_fake_settings": "无。全包未检索到 WindowManager/悬浮窗或自绘高仿设置页；仅有一个透明、excludeFromRecents 的远端控制 Activity h（由广播 com.xxx.broadcast.xxx 驱动，用于远端聊天/回传，非无障碍引导遮罩）",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=22，跳转直接使用 android.settings.ACCESSIBILITY_SETTINGS，未出现 ACTION_APPLICATION_DETAILS_SETTINGS、未教用户打开“受限设置”菜单，也无 Session 安装器绕过",
    "post_grant_anti_removal": "未见 GLOBAL_ACTION_BACK/HOME 或自点确认逻辑（未检索到 performGlobalAction/GLOBAL_ACTION）；但通过首次运行即禁用桌面组件 + 申请设备管理器权限，使应用在授权后从桌面消失并具备卸载阻力",
    "benign_graceful_degradation": "无。既无手动模式、也无 ADB 说明或“仅观看”降级路径，拒绝授权不会有任何替代功能或提示"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "Hook Activity 启动：一旦监测到 startActivity 目标 action 为 android.settings.ACCESSIBILITY_SETTINGS，立即回拉 UTG；或在冷启动 yps.eton.application.M 出现（1 秒内无任何控件、无文本）后紧接着监测 ADD_DEVICE_ADMIN 弹窗，即可完整覆盖 0 步跳转链",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动透明跳板页",
        "page_identifier": "yps.eton.application.M，Theme.Translucent.NoTitleBar，无布局、无控件、无文本",
        "why_most_useful": "该页为空文本是此家族最关键判别信号：无任何说明却立即走向系统设置，可直接排除良性透明说明型应用",
        "observable_utg_signals": [
          "Activity 名称为混淆短名 M 且主题为 Translucent.NoTitleBar",
          "页面无任何节点文本或可点击控件",
          "停留时间极短（小于 1 秒）后直接离开应用界面"
        ]
      },
      {
        "page_role": "设备管理器空说明弹窗",
        "page_identifier": "系统对话框，标题含激活设备管理，说明区为空",
        "why_most_useful": "ADD_EXPLANATION 为空是“无理由索取高权限”的直接证据，且其后无论同意与否都跳无障碍页",
        "observable_utg_signals": [
          "弹窗说明文本为空或仅系统默认语句",
          "弹窗由 yps.eton.application.i 提供的 DeviceAdminReceiver 触发",
          "关闭/拒绝该弹窗后紧接着出现系统无障碍设置页"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务中条目文本为 كشف رقم واسم المتصل المجهول，无副标题说明",
        "why_most_useful": "证明诱导终点即系统无障碍开关，且服务名与来电识别应用同名、零能力说明，构成身份与能力不匹配",
        "observable_utg_signals": [
          "列表项文本与桌面应用名完全一致",
          "条目下无 description 副文本",
          "上一跳来源包名为 yps.eton.application"
        ]
      },
      {
        "page_role": "获权后静默采集验证页",
        "page_identifier": "无界面；通过流量侧观测 samire.ddns.net:2020 连接及含 c0c1c3a2c0c1c 分隔符的文本上报",
        "why_most_useful": "确认授权后的真实目的是全量输入监听而非来电识别，为“诱导”提供危害落点",
        "observable_utg_signals": [
          "开启开关后前台界面无变化、无功能页",
          "网络侧出现 DNS 域名 samire.ddns.net 的 2020 端口连接",
          "上报体包含包名+控件文本+时间戳三段结构"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在三处盲区：一是全流程零文案、零图片，纯靠名称与空白页，基于文本/OCR 的诱导识别会漏检；二是引导发生在系统设置页，应用自身 UI 无痕迹，若仅录屏应用界面会看不到无障碍页；三是应用首跑即禁用自身桌面组件，二次运行需靠 BOOT_COMPLETED 接收器 B 或 AlarmManager 定时器 Z 拉起，纯手工复现可能找不到入口。另有内嵌 res/raw APK 二阶段载荷，其安装后行为需单独捕获。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "yps.eton.application.M#onCreate",
    "yps.eton.application.M#a",
    "yps.eton.application.M#onActivityResult",
    "yps.eton.application.k#onServiceConnected",
    "yps.eton.application.k#onAccessibilityEvent",
    "res/values/strings.xml"
  ]
}
```

</details>

# MR_128__8cc9ceaefc｜SpyNote — System Android

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：95.9s

## 1. 一句话核心结论

- **核心申请方式**：透明无 UI 的 Launcher Activity 依据本地字符串 gp="11111" 在冷启动时直接 startActivity 跳转系统无障碍设置页，并在 onResume 中无限重跳直至授权，全程无任何说明文字、无取消按钮、无引导遮罩
- **静态可见性说明**：全部跳转与开关逻辑均在 classes.dex 中以明文常量（android.settings.ACCESSIBILITY_SETTINGS、android.app.action.ADD_DEVICE_ADMIN）实现，无加壳、无 AES 载荷、无远端 HTML，静态完全可见；仅 C11 后续 C2 通信部分使用字符串混淆（C11.a(str, long) 偏移取值），不影响无障碍引导链判定
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `8cc9ceaefc3a9aac5b1e1a7e482e92ba67d3dfc37fea6709e2c176a87a9adc61` |
| 包名 / 年份 | `cmf0.c3b5bm90zq.patch` / 2020 |
| 家族 / 品类 | **SpyNote**（同池样本数：59） |
| 原始来源标识 | https://blog.lookout.com/nation-state-mobile-malware-targets-syrians-with-covid-19-lures |
| 桌面显示名 | System Android |
| 引导页宣称品牌/身份 | 冒充 Android 系统组件（System Android），实际为 SpyNote 系远程控制木马 |
| 系统无障碍列表服务名 | System Android（C1 未声明 android:label，系统回落至 @string/app_name / @string/s 同为 System Android；无 android:description） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无空白/换行挤出、无同形字、无多 activity-alias、无伪造 isAccessibilityTool；混淆手法为：①包名/类名全混淆（cmf0.c3b5bm90zq.patch.C1~C15）；②以系统级通用名称 "System Android" 同时作为应用名与服务名，冒充系统组件；③无障碍服务不声明 label/description，使系统设置页无法展示真实用途；④授权成功后调用 setComponentEnabledSetting(C7, 2, 1) 禁用自身桌面图标实现隐身 |
| 无障碍服务类名 | `cmf0.c3b5bm90zq.patch.C1` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | cmf0.c3b5bm90zq.patch.C7（LAUNCHER，Theme.Translucent.NoTitleBar，excludeFromRecents=true） | 用户点击桌面图标启动，onCreate()/onResume() 均直接调用 c() | 原生Activity | 无 | 无提示；用户无任何可点击对象，也无取消/跳过入口 | `cmf0.c3b5bm90zq.patch.C7#onCreate / cmf0.c3b5bm90zq.patch.C7#onResume / cmf0.c3b5bm90zq.patch.C7#c` |
| 2 | 业务功能触发 | 本地控制串 @string/gp（res/values/strings.xml，id 0x7f0c0021） | C7.c() 读取 gp="11111" 并按字符位分派：charAt(1)=无障碍、charAt(3)=设备管理员、charAt(0)=隐藏图标、charAt(4)=su 探测、charAt(2)=图标抓取 | 不可静态还原 | **原文**：11111<br>**译注**：五位开关串，当前全部为 1，即所有恶意子功能默认启用 | 无 | `res/values/strings.xml#L36 (gp) / cmf0.c3b5bm90zq.patch.C7#c` |
| 3 | 引导说明页 | 不存在——无引导 Activity / Dialog / WebView / HTML | 无 | 不可静态还原 | 无 | 无 | `search_text_in_app: WebView/Toast/ACCESSIBILITY_SETTINGS 均无引导类调用点` |
| 4 | 跳受限设置 | 系统设备管理员激活页（android.app.action.ADD_DEVICE_ADMIN，requestCode=100） | C7$1.run() 中 gp.charAt(3)=='1' 且 c.a()（未激活）时 startActivityForResult | 系统无障碍页 | **原文**：android.app.extra.ADD_EXPLANATION = ""<br>**译注**：设备管理员激活页的“说明”字段被置为空字符串，用户看不到任何申请理由 | 点击“激活”授予设备管理员（含 wipe-data、reset-password、disable-camera 等策略）；系统页自带取消 | `cmf0.c3b5bm90zq.patch.C7$1#run / res/xml/device_admin.xml` |
| 5 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载服务列表（android.settings.ACCESSIBILITY_SETTINGS） | C7$1.run() 中 gp.charAt(1)=='1' 且 C11.j==false 时，new Intent().setAction("android.settings.ACCESSIBILITY_SETTINGS").setFlags(268435456) 后 startActivity | 系统无障碍页 | **原文**：System Android<br>**译注**：系统无障碍列表中出现名为“System Android”的服务项，无副标题、无功能描述，用户无法判断其真实用途 | 点击“System Android”并打开开关（系统页无本应用提供的任何解释或取消引导） | `cmf0.c3b5bm90zq.patch.C7$1#run / AndroidManifest.xml service cmf0.c3b5bm90zq.patch.C1` |
| 6 | 拒权反馈循环 | C7（透明 Activity）→ 系统无障碍页 反复切换 | 用户从无障碍页按返回 → C7.onResume() → c() → C11.j 仍为 false → b() → 新线程 C7$1.run() → 再次 startActivity(ACCESSIBILITY_SETTINGS) | 系统无障碍页 | 无 | 只能被迫开启无障碍开关（或强制停止应用） | `cmf0.c3b5bm90zq.patch.C7#onResume / cmf0.c3b5bm90zq.patch.C7#b / cmf0.c3b5bm90zq.patch.C7$1#run` |
| 7 | 获权后动作 | cmf0.c3b5bm90zq.patch.C1（AccessibilityService） | onServiceConnected()：flags=89、eventTypes=-1、feedbackType=16，置 C11.j=true；onAccessibilityEvent 逐条抓取前台包名与界面文本 | 不可静态还原 | 无 | 无 | `cmf0.c3b5bm90zq.patch.C1#onServiceConnected / cmf0.c3b5bm90zq.patch.C1#onAccessibilityEvent / cmf0.c3b5bm90zq.patch.C7#a()` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 无任何应用自绘的引导/说明文字（全包无 WebView、无引导 Dialog、无 HTML 资源、无悬浮窗）
- 系统无障碍服务列表项名称：'System Android'（来自 @string/app_name / @string/s，C1 未声明 android:label）
- 系统无障碍服务描述：缺失（Manifest 中 C1 无 android:description、无 accessibilityservice meta-data），故系统只能显示通用警告与空白描述
- 设备管理员激活页说明文本：显式置空（Intent extra android.app.extra.ADD_EXPLANATION = ""）
- 本地控制串 res/values/strings.xml#L36 gp="11111"（不可见，仅驱动跳转分支）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | System Android | 系统 Android | `res/values/strings.xml key app_name / s；同时作为无障碍服务在系统列表中的显示名` | 未知 |
| en | android.settings.ACCESSIBILITY_SETTINGS | （跳转目标）系统无障碍设置页 | `cmf0.c3b5bm90zq.patch.C7$1#run 硬编码 Intent action` | 受限设置分步教学 |
| en | android.app.extra.ADD_EXPLANATION = "" | 设备管理员申请说明留空 | `cmf0.c3b5bm90zq.patch.C7$1#run 硬编码` | 教唆忽视警告 |
| en | 11111 | 11111（五位功能开关，全开） | `res/values/strings.xml key gp (0x7f0c0021)` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：C7.onResume() 无条件再次执行 c()，只要 C11.j 仍为 false 就经 b() 起线程 C7$1.run() 重新 startActivity("android.settings.ACCESSIBILITY_SETTINGS")；用户从无障碍页返回即被立即弹回，形成无提示死循环，直到开关被打开（或应用被强制停止/卸载）
- **遮罩叠层 / 高仿系统设置页**：无。不使用悬浮窗遮罩，也不伪造高仿系统无障碍开关页；直接借用真实系统设置页作为唯一界面
- **Android 13+ 受限设置（Restricted Settings）应对**：无。目标 SDK 22（Android 5.1），未包含 Android 13 受限设置（应用详情→右上角菜单）教学，也无 Session 安装器绕过逻辑
- **获权后即时行为与防撤权机制**：获权后不主动监听设置页阻止撤权（未发现 GLOBAL_ACTION_BACK/HOME 拦截逻辑）；但会通过 setComponentEnabledSetting(C7, 2, 1) 禁用自身 Launcher 图标，使应用从桌面消失、增加用户定位与卸载难度；另已提前申请设备管理员（含 wipe-data）作为二次持久化
- **良性降级 / 替代方案**：无。未授权则无限重跳，不存在手动模式、ADB 说明或仅观看模式等降级路径

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 Launcher Activity 后立即监控 Intent：一旦出现 action="android.settings.ACCESSIBILITY_SETTINGS"（或 android.app.action.ADD_DEVICE_ADMIN）即拉起 UTG；同时因存在 onResume 重跳循环，可在系统无障碍页驻留期间持续抓取，返回瞬间会立即被重新压入
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在一处显著盲区：本样本全程零自绘文本、零图片诱饵，纯 UTG 只能看到系统设置页与一个透明 Activity，若检测策略仅以“应用自绘引导文案/悬浮窗”为特征将漏报；应改用“Launcher Activity 无 UI + 立即跳 ACCESSIBILITY_SETTINGS + 返回后重跳”的行为序列特征。另外 C11 的通信部分使用字符串偏移混淆（C11.a(str,long)），但其不承载无障碍引导逻辑，不影响本判定

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后首屏（透明 Activity 落地瞬间）** | 包名 cmf0.c3b5bm90zq.patch、Activity cmf0.c3b5bm90zq.patch.C7、Theme.Translucent.NoTitleBar、无任何可交互控件 | 证实零提示直接跳转：捕获到该页为空且随后立即切到设置页，即证明不存在任何说明/征询环节 | 空白透明窗口无控件节点；Activity 名 C7；停留时长极短（<1s）随即跳系统设置 |
| **设备管理员激活页** | 系统 DeviceAdminAdd 页，应用名 System Android，说明区域为空 | 空 ADD_EXPLANATION 是典型的隐瞒真实权限诉求信号，且设备管理员含 wipe-data 高危策略 | 说明/描述文本为空；权限策略列表含 wipe data / disable camera；激活按钮 vs 取消按钮 |
| **系统无障碍服务列表项** | Settings → Accessibility → Downloaded services，条目文本 'System Android'，无副标题描述 | 区分是否诱导的关键：服务名冒充系统组件、且无 description，用户无法知情同意 | 条目名称为 System Android；无 description 文本；开关初始为关闭 |
| **返回后重跳（拒权循环）** | 从无障碍页按返回 → 再次出现同一 AccessibilitySettings 页面 | 直接证明拒绝反馈死循环，是诱导/胁迫开启无障碍的决定性运行期证据 | 返回后 <2s 内页面被重新压入；重复出现次数递增；始终无跳过/取消控件 |
| **获权后桌面图标消失** | Launcher 中 'System Android' 图标消失，无障碍列表开关变为开启 | 证明授权后主动隐身，配合无障碍全事件监听形成完整危害闭环 | 桌面无该应用图标；无障碍开关为开启状态；无前台 UI 但持续后台活动 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `cmf0.c3b5bm90zq.patch.C7#onCreate`
- `cmf0.c3b5bm90zq.patch.C7#onResume`
- `cmf0.c3b5bm90zq.patch.C7#c`
- `cmf0.c3b5bm90zq.patch.C7$1#run`
- `cmf0.c3b5bm90zq.patch.C1#onServiceConnected`
- `res/values/strings.xml#L36`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，11 次工具调用）

**核心事实：该样本完全没有“引导页面”，采用的是“无任何提示的一步直达 + 返回后重新跳转”的方式。**

1. **入口伪装**：Launcher 入口 [C7](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7>) 使用 `Theme.Translucent.NoTitleBar` + `excludeFromRecents="true"`，没有任何可见 UI（`onCreate` 仅调用 `c()`），且没有 `setContentView`。
2. **开关来自本地字符串 `gp`**：[C7.c()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7#c>) 读取 `getString(0x7f0c0021)`，即 [strings.xml 的 `gp` = "11111"](<resource-unit:#1.dex1 file:res/values/strings.xml#L36>)，并按字符位控制流程：`charAt(1)`→跳无障碍设置、`charAt(3)`→申请设备管理员、`charAt(0)`→隐藏图标、`charAt(4)`→`su` root 探测、`charAt(2)`→抓取图标。当前值 `"11111"` 使全部开关打开。
3. **直接跳转点**：[C7$1.run()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7$1#run>) 在后台线程中构造 `new Intent().setAction("android.settings.ACCESSIBILITY_SETTINGS")` + `FLAG_ACTIVITY_NEW_TASK`，直接 `startActivity`；同一段代码还用 `android.app.action.ADD_DEVICE_ADMIN` 申请设备管理员，且 **`ADD_EXPLANATION` 传入空串**。
4. **没有教学载体**：全包无 `WebView`、无 `AlertDialog` 引导、无悬浮窗遮罩、无 HTML 资源；无障碍服务 [C1](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C1>) 在 Manifest 中**既无 `android:label` 也无 `android:description`/`meta-data` 配置**，系统无障碍列表只能回落到应用名 `System Android`，因此用户看不到任何用途说明。
5. **拒权循环**：`C7.onResume()` 同样调用 `c()`；由于 `C11.j` 仍为 false，流程走到 `b()` → 再次拉起 `ACCESSIBILITY_SETTINGS`。用户从设置页返回后立即被重新推进无障碍页，形成**死循环**，且因 Activity 为透明且无取消控件，用户既无法看到“取消/跳过”选项，也无法停留在本页。
6. **获权后**：`C1.onServiceConnected` 设置 `flags=89`、`eventTypes=-1`（监听全部事件），把前台应用文本写文件并回传 `82.137.218.185`；同时 `charAt(0)=='1'` 触发 `setComponentEnabledSetting(C7, 2, 1)` **禁用自身 Launcher 图标**，实现授权后“隐身”。

> 结论：该样本的“引导”实质是**利用系统设置页本身作为唯一界面**，通过透明 Activity 反复跳转逼迫用户开启无障碍，属于典型的 SpyNote 系无障碍滥用型恶意软件；无任何说明文字、无取消路径、无降级机制。

---

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部跳转与开关逻辑均在 classes.dex 中以明文常量（android.settings.ACCESSIBILITY_SETTINGS、android.app.action.ADD_DEVICE_ADMIN）实现，无加壳、无 AES 载荷、无远端 HTML，静态完全可见；仅 C11 后续 C2 通信部分使用字符串混淆（C11.a(str, long) 偏移取值），不影响无障碍引导链判定",
  "summary_one_liner": "透明无 UI 的 Launcher Activity 依据本地字符串 gp=\"11111\" 在冷启动时直接 startActivity 跳转系统无障碍设置页，并在 onResume 中无限重跳直至授权，全程无任何说明文字、无取消按钮、无引导遮罩",
  "disguise_identity": {
    "app_display_name": "System Android",
    "claimed_brand_or_persona": "冒充 Android 系统组件（System Android），实际为 SpyNote 系远程控制木马",
    "a11y_service_label": "System Android（C1 未声明 android:label，系统回落至 @string/app_name / @string/s 同为 System Android；无 android:description）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无空白/换行挤出、无同形字、无多 activity-alias、无伪造 isAccessibilityTool；混淆手法为：①包名/类名全混淆（cmf0.c3b5bm90zq.patch.C1~C15）；②以系统级通用名称 \"System Android\" 同时作为应用名与服务名，冒充系统组件；③无障碍服务不声明 label/description，使系统设置页无法展示真实用途；④授权成功后调用 setComponentEnabledSetting(C7, 2, 1) 禁用自身桌面图标实现隐身"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "cmf0.c3b5bm90zq.patch.C7（LAUNCHER，Theme.Translucent.NoTitleBar，excludeFromRecents=true）",
      "trigger_event": "用户点击桌面图标启动，onCreate()/onResume() 均直接调用 c()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "全透明、无标题、不进入最近任务列表的空白 Activity，用户几乎看不到任何界面",
      "user_action_requested": "无提示；用户无任何可点击对象，也无取消/跳过入口",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7#onCreate / cmf0.c3b5bm90zq.patch.C7#onResume / cmf0.c3b5bm90zq.patch.C7#c"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "本地控制串 @string/gp（res/values/strings.xml，id 0x7f0c0021）",
      "trigger_event": "C7.c() 读取 gp=\"11111\" 并按字符位分派：charAt(1)=无障碍、charAt(3)=设备管理员、charAt(0)=隐藏图标、charAt(4)=su 探测、charAt(2)=图标抓取",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "11111",
      "shown_text_zh": "五位开关串，当前全部为 1，即所有恶意子功能默认启用",
      "user_action_requested": "无",
      "code_anchor": "res/values/strings.xml#L36 (gp) / cmf0.c3b5bm90zq.patch.C7#c"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "不存在——无引导 Activity / Dialog / WebView / HTML",
      "trigger_event": "无",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "全包搜索无 WebView、无 AlertDialog 引导、无 assets HTML、无悬浮窗说明页；从透明 Activity 直接跳到系统设置",
      "user_action_requested": "无",
      "code_anchor": "search_text_in_app: WebView/Toast/ACCESSIBILITY_SETTINGS 均无引导类调用点"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统设备管理员激活页（android.app.action.ADD_DEVICE_ADMIN，requestCode=100）",
      "trigger_event": "C7$1.run() 中 gp.charAt(3)=='1' 且 c.a()（未激活）时 startActivityForResult",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.app.extra.ADD_EXPLANATION = \"\"",
      "shown_text_zh": "设备管理员激活页的“说明”字段被置为空字符串，用户看不到任何申请理由",
      "user_action_requested": "点击“激活”授予设备管理员（含 wipe-data、reset-password、disable-camera 等策略）；系统页自带取消",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7$1#run / res/xml/device_admin.xml"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载服务列表（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "C7$1.run() 中 gp.charAt(1)=='1' 且 C11.j==false 时，new Intent().setAction(\"android.settings.ACCESSIBILITY_SETTINGS\").setFlags(268435456) 后 startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "System Android",
      "shown_text_zh": "系统无障碍列表中出现名为“System Android”的服务项，无副标题、无功能描述，用户无法判断其真实用途",
      "user_action_requested": "点击“System Android”并打开开关（系统页无本应用提供的任何解释或取消引导）",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7$1#run / AndroidManifest.xml service cmf0.c3b5bm90zq.patch.C1"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "C7（透明 Activity）→ 系统无障碍页 反复切换",
      "trigger_event": "用户从无障碍页按返回 → C7.onResume() → c() → C11.j 仍为 false → b() → 新线程 C7$1.run() → 再次 startActivity(ACCESSIBILITY_SETTINGS)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何提示的静默重跳；用户返回即被立即弹回无障碍设置页，无法退出，也看不到“稍后再说/跳过”",
      "user_action_requested": "只能被迫开启无障碍开关（或强制停止应用）",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7#onResume / cmf0.c3b5bm90zq.patch.C7#b / cmf0.c3b5bm90zq.patch.C7$1#run"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "cmf0.c3b5bm90zq.patch.C1（AccessibilityService）",
      "trigger_event": "onServiceConnected()：flags=89、eventTypes=-1、feedbackType=16，置 C11.j=true；onAccessibilityEvent 逐条抓取前台包名与界面文本",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静默记录所有应用界面文本（键盘输入、聊天内容）写入外部存储并回传 82.137.218.185；同时 C7.a() 执行 setComponentEnabledSetting(C7,2,1) 禁用自身桌面图标使应用从桌面消失",
      "user_action_requested": "无",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C1#onServiceConnected / cmf0.c3b5bm90zq.patch.C1#onAccessibilityEvent / cmf0.c3b5bm90zq.patch.C7#a()"
    }
  ],
  "text_presentation_locations": [
    "无任何应用自绘的引导/说明文字（全包无 WebView、无引导 Dialog、无 HTML 资源、无悬浮窗）",
    "系统无障碍服务列表项名称：'System Android'（来自 @string/app_name / @string/s，C1 未声明 android:label）",
    "系统无障碍服务描述：缺失（Manifest 中 C1 无 android:description、无 accessibilityservice meta-data），故系统只能显示通用警告与空白描述",
    "设备管理员激活页说明文本：显式置空（Intent extra android.app.extra.ADD_EXPLANATION = \"\"）",
    "本地控制串 res/values/strings.xml#L36 gp=\"11111\"（不可见，仅驱动跳转分支）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "System Android",
      "text_zh": "系统 Android",
      "source_location": "res/values/strings.xml key app_name / s；同时作为无障碍服务在系统列表中的显示名",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "text_zh": "（跳转目标）系统无障碍设置页",
      "source_location": "cmf0.c3b5bm90zq.patch.C7$1#run 硬编码 Intent action",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "android.app.extra.ADD_EXPLANATION = \"\"",
      "text_zh": "设备管理员申请说明留空",
      "source_location": "cmf0.c3b5bm90zq.patch.C7$1#run 硬编码",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "11111",
      "text_zh": "11111（五位功能开关，全开）",
      "source_location": "res/values/strings.xml key gp (0x7f0c0021)",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "C7.onResume() 无条件再次执行 c()，只要 C11.j 仍为 false 就经 b() 起线程 C7$1.run() 重新 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\")；用户从无障碍页返回即被立即弹回，形成无提示死循环，直到开关被打开（或应用被强制停止/卸载）",
    "overlay_or_fake_settings": "无。不使用悬浮窗遮罩，也不伪造高仿系统无障碍开关页；直接借用真实系统设置页作为唯一界面",
    "restricted_settings_13plus_coaching": "无。目标 SDK 22（Android 5.1），未包含 Android 13 受限设置（应用详情→右上角菜单）教学，也无 Session 安装器绕过逻辑",
    "post_grant_anti_removal": "获权后不主动监听设置页阻止撤权（未发现 GLOBAL_ACTION_BACK/HOME 拦截逻辑）；但会通过 setComponentEnabledSetting(C7, 2, 1) 禁用自身 Launcher 图标，使应用从桌面消失、增加用户定位与卸载难度；另已提前申请设备管理员（含 wipe-data）作为二次持久化",
    "benign_graceful_degradation": "无。未授权则无限重跳，不存在手动模式、ADB 说明或仅观看模式等降级路径"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 Launcher Activity 后立即监控 Intent：一旦出现 action=\"android.settings.ACCESSIBILITY_SETTINGS\"（或 android.app.action.ADD_DEVICE_ADMIN）即拉起 UTG；同时因存在 onResume 重跳循环，可在系统无障碍页驻留期间持续抓取，返回瞬间会立即被重新压入",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后首屏（透明 Activity 落地瞬间）",
        "page_identifier": "包名 cmf0.c3b5bm90zq.patch、Activity cmf0.c3b5bm90zq.patch.C7、Theme.Translucent.NoTitleBar、无任何可交互控件",
        "why_most_useful": "证实零提示直接跳转：捕获到该页为空且随后立即切到设置页，即证明不存在任何说明/征询环节",
        "observable_utg_signals": ["空白透明窗口无控件节点", "Activity 名 C7", "停留时长极短（<1s）随即跳系统设置"]
      },
      {
        "page_role": "设备管理员激活页",
        "page_identifier": "系统 DeviceAdminAdd 页，应用名 System Android，说明区域为空",
        "why_most_useful": "空 ADD_EXPLANATION 是典型的隐瞒真实权限诉求信号，且设备管理员含 wipe-data 高危策略",
        "observable_utg_signals": ["说明/描述文本为空", "权限策略列表含 wipe data / disable camera", "激活按钮 vs 取消按钮"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility → Downloaded services，条目文本 'System Android'，无副标题描述",
        "why_most_useful": "区分是否诱导的关键：服务名冒充系统组件、且无 description，用户无法知情同意",
        "observable_utg_signals": ["条目名称为 System Android", "无 description 文本", "开关初始为关闭"]
      },
      {
        "page_role": "返回后重跳（拒权循环）",
        "page_identifier": "从无障碍页按返回 → 再次出现同一 AccessibilitySettings 页面",
        "why_most_useful": "直接证明拒绝反馈死循环，是诱导/胁迫开启无障碍的决定性运行期证据",
        "observable_utg_signals": ["返回后 <2s 内页面被重新压入", "重复出现次数递增", "始终无跳过/取消控件"]
      },
      {
        "page_role": "获权后桌面图标消失",
        "page_identifier": "Launcher 中 'System Android' 图标消失，无障碍列表开关变为开启",
        "why_most_useful": "证明授权后主动隐身，配合无障碍全事件监听形成完整危害闭环",
        "observable_utg_signals": ["桌面无该应用图标", "无障碍开关为开启状态", "无前台 UI 但持续后台活动"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在一处显著盲区：本样本全程零自绘文本、零图片诱饵，纯 UTG 只能看到系统设置页与一个透明 Activity，若检测策略仅以“应用自绘引导文案/悬浮窗”为特征将漏报；应改用“Launcher Activity 无 UI + 立即跳 ACCESSIBILITY_SETTINGS + 返回后重跳”的行为序列特征。另外 C11 的通信部分使用字符串偏移混淆（C11.a(str,long)），但其不承载无障碍引导逻辑，不影响本判定"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "LURE_DISMISS_SYSTEM_WARNING",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "cmf0.c3b5bm90zq.patch.C7#onCreate",
    "cmf0.c3b5bm90zq.patch.C7#onResume",
    "cmf0.c3b5bm90zq.patch.C7#c",
    "cmf0.c3b5bm90zq.patch.C7$1#run",
    "cmf0.c3b5bm90zq.patch.C1#onServiceConnected",
    "res/values/strings.xml#L36"
  ]
}
```

</details>

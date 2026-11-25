# MR_147__579fe1f6a9｜Hqwar — Servis Güncellemesi

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：104.8s

## 1. 一句话核心结论

- **核心申请方式**：以土耳其语“Servis Güncellemesi（服务更新）”为统一身份伪装，声明一个无任何 description、可读取窗口内容并上报控件 ID 的无障碍服务，真实引导页与跳转逻辑全部封装在加密载荷 templates/main.tpl 中、由脱壳桩类动态释放，静态仅能确认诱导的落点与能力面。
- **静态可见性说明**：可见 classes.dex 仅 26 个类的脱壳/解密桩（com.ertinsit.lcipdp.iemSotG.onCreate 为无效字符串与 switch 混淆），Manifest 声明的全部 com.xhqlob.doscby.* 业务类（无障碍服务 qxRjxBp、启动 Activity AKrheIcrC、uprtknrhf.* 隐藏 Activity）均不在可见 DEX 中；引导页/弹窗/跳转代码与全部文案藏于高熵加密载荷 unknown/templates/main.tpl（233208 字节，由 templates/.config 指向）。仅 Manifest、res/xml/vyklwvyuouh.xml 与权限声明可静态确认，无 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / DexClassLoader / Cipher 等明文串可用于静态串联。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `579fe1f6a9991a9257fe0ca27692bf84286eeb4a9ba26c73ef9e8841390ca5d5` |
| 包名 / 年份 | `com.xhqlob.doscby` / 2019 |
| 家族 / 品类 | **Hqwar**（同池样本数：4） |
| 原始来源标识 | https://blog.zimperium.com/how-zimperiums-z9-detected-unknown-mobile-malware-overlooked-by-the-av-industry/ |
| 桌面显示名 | Servis Güncellemesi |
| 引导页宣称品牌/身份 | 系统/运营商“服务更新”（Servis Güncellemesi） |
| 系统无障碍列表服务名 | Servis Güncellemesi |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置无 android:description（系统列表中零功能说明）；settingsActivity 遗留模板值 com.example.root.myapplication.MainActivity 与真实包名不符；十余个 android:label="" 且共用 @drawable/aujepehe 图标、excludeFromRecents、Theme.NoDisplay 的隐藏 Activity；服务类名/包名全随机混淆（qxRjxBp、uprtknrhf.*、ynstfaipm.*）；核心载荷以高熵 main.tpl 加密存放，明文中无任何敏感 API 字符串。 |
| 无障碍服务类名 | `com.xhqlob.doscby.qxRjxBp` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.xhqlob.doscby.uprtknrhf.AKrheIcrC（MAIN/LAUNCHER，实现类体不在可见 DEX） | 用户点击桌面图标冷启动 | 不可静态还原 | 无 | 不可静态确认（是否可取消/跳过无法判断） | `AndroidManifest.xml: activity com.xhqlob.doscby.uprtknrhf.AKrheIcrC（LAUNCHER）` |
| 2 | 引导说明页 | 加密载荷 templates/main.tpl 内释放的引导 Activity/弹窗（类名不在可见 DEX） | Application com.ertinsit.lcipdp.iemSotG.onCreate 中的脱壳桩 FVMTRPjXwtPN.GNiTtOAS 释放并加载真实代码后触发 | 不可静态还原 | 无 | 不可静态确认 | `com.ertinsit.lcipdp.iemSotG.onCreate / com.ertinsit.lcipdp.FVMTRPjXwtPN.GNiTtOAS` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS，列表项显示为 Servis Güncellemesi | 真实代码中的 Intent 跳转（可见 DEX 内无该字符串，判定由加密载荷内代码发起） | 系统无障碍页 | **原文**：Servis Güncellemesi<br>**译注**：“服务更新”——用户在系统无障碍服务列表中看到的就是这一名称，且无任何功能说明文字 | 用户需在系统无障碍列表中点选并确认开启该服务（系统确认弹窗由 OS 提供） | `AndroidManifest.xml: service com.xhqlob.doscby.qxRjxBp android:label="Servis Güncellemesi"; res/xml/vyklwvyuouh.xml（无 android:description）` |
| 4 | 遮罩叠层指引 | 可能的悬浮窗/遮罩引导层（应用已声明 SYSTEM_ALERT_WINDOW） | 不可静态确认（跳转设置后是否压栈遮罩需运行期验证） | 悬浮窗Overlay | 无 | 不可静态确认 | `AndroidManifest.xml: uses-permission android.permission.SYSTEM_ALERT_WINDOW / application android:theme=@android:style/Theme.Translucent.NoTitleBar` |
| 5 | 获权后动作 | com.xhqlob.doscby.qxRjxBp（AccessibilityService，读取窗口内容+控件ID）；短信/联系人/录音/通话等后续链路由 svzikosxo.* 接收器与多个常驻 Service 承载 | onServiceConnected 后监听 typeWindowContentChanged / typeWindowStateChanged | 不可静态还原 | 无 | 不可静态确认（是否自点确认、阻止撤权需运行期验证） | `res/xml/vyklwvyuouh.xml（canRetrieveWindowContent=true, flagReportViewIds）; AndroidManifest.xml: receiver com.xhqlob.doscby.svzikosxo.XFywTLdKTA (SMS_DELIVER)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项名称：AndroidManifest.xml 中 service com.xhqlob.doscby.qxRjxBp 的 android:label="Servis Güncellemesi"（系统列表原样展示）
- 系统无障碍列表的说明区：res/xml/vyklwvyuouh.xml 未声明 android:description，故此处为空白——用户看不到任何用途说明
- 桌面图标名称：application android:label="Servis Güncellemesi"
- 其余引导/说明文字（原生弹窗、Activity 布局、WebView HTML）均随真实代码封装于加密载荷 unknown/templates/main.tpl，静态不可读

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Servis Güncellemesi | 服务更新 | `AndroidManifest.xml: application android:label 与 service com.xhqlob.doscby.qxRjxBp android:label` | 假更新 |
| java | com.example.root.myapplication.MainActivity | 无障碍配置中残留的模板 settingsActivity 值（与本应用真实包名 com.xhqlob.doscby 不符） | `res/xml/vyklwvyuouh.xml android:settingsActivity` | 未知 |
| und | templates/main.tpl | 加密载荷文件路径清单（载荷本体为高熵二进制，静态不可解密） | `unknown/templates/.config` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：可见 DEX 中无跳转与 onResume 逻辑，返回设置页后的重跳/死循环需动态验证
- **遮罩叠层 / 高仿系统设置页**：不可静态确认是否叠放半透明遮罩或高仿系统开关页；但应用已具备 SYSTEM_ALERT_WINDOW 权限与全透明无标题主题，具备该能力条件
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据；应用 targetSdkVersion=27（低于 Android 13 受限设置机制），未见相关教学代码
- **获权后即时行为与防撤权机制**：不可静态确认；Manifest 中存在 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、BOOT_COMPLETED/SCREEN_ON/USER_PRESENT 高优接收器与多个常驻 Service，具备常驻与自动重启能力，但是否阻止撤权需动态验证
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到前台 Activity 为 com.xhqlob.doscby.uprtknrhf.AKrheIcrC（冷启动首屏）时立即开始录屏；并在任意时刻检测到 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的瞬间打标记并连拍屏幕，随后捕获设置页返回后 0.5–2 秒内的屏幕状态以确认是否压入遮罩/重跳
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：真实引导文案与跳转逻辑全部在加密载荷 templates/main.tpl 中，静态无任何敏感字符串，纯静态分析只能看到伪装名称与无障碍能力面；此外应用使用全透明无标题主题与 label="" 的隐藏 Activity，UTG 若仅按 Activity 名与可见文本判定，可能把空标签透明页视为噪声而漏掉遮罩层；无障碍 description 为空也使“系统页文本特征”类信号失效，需依赖 Intent 跳转与悬浮窗层级信号。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导页/弹窗页** | com.xhqlob.doscby.uprtknrhf.AKrheIcrC 或其拉起的透明无标题 Activity/原生 Dialog | 该页承载唯一的说辞文案与是否可取消的关键判定，是区分“假更新诱导”与良性说明的分界点 | 界面文案与语种（土耳其语“服务更新”类说辞）；是否存在取消/跳过控件（不可取消则强诱导）；页面是否为 WebView（可看 URL 是否指向远端） |
| **跳转后的系统无障碍服务列表项** | 设置 > 无障碍 列表中的 “Servis Güncellemesi” 条目及其说明区（说明区应为空白） | 直接证明用户被引导到的目标即该服务，且无功能说明、名称与真实能力不符 | 服务显示名与桌面名一致性；description 为空；跳转由应用自身发起（调用栈/Intent 记录） |
| **设置页后压栈的遮罩/引导层** | SYSTEM_ALERT_WINDOW 类型悬浮窗或半透明 Activity（Theme.Translucent.NoTitleBar） | 叠层遮罩与分步指引是“教唆用户在系统页操作”的最强证据，也决定是否构成遮罩诱导 | 悬浮窗是否覆盖系统设置页并含步骤文字/箭头；遮罩是否拦截返回键；从设置返回后是否立即重跳 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `AndroidManifest.xml: service com.xhqlob.doscby.qxRjxBp (android:label="Servis Güncellemesi", BIND_ACCESSIBILITY_SERVICE)`
- `res/xml/vyklwvyuouh.xml (canRetrieveWindowContent=true, flagReportViewIds, 无 android:description, settingsActivity 模板残留)`
- `com.ertinsit.lcipdp.iemSotG.onCreate`
- `com.ertinsit.lcipdp.FVMTRPjXwtPN.GNiTtOAS`
- `unknown/templates/main.tpl`
- `unknown/templates/.config`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**1. 静态可见性：核心 UI 与跳转逻辑全部藏在加密载荷中，可见部分只剩外壳**
- `classes.dex` 极小：全包仅 **26 个类 / 2 个包**（`com.ertinsit.lcipdp`、`android.support.fohwytzktyn`），且 `Application` 类 [iemSotG.onCreate()](<resource-unit:#1.dex1 code:com.ertinsit.lcipdp.iemSotG#onCreate>) 只做无意义的字符串拼接、switch 跳转和字段写入，反编译结果为典型的**解密/脱壳桩**。
- 在 `classes.dex` 内全文检索 `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`android.settings.*`、`BIND_ACCESSIBILITY_SERVICE`、`DexClassLoader`、`Cipher`、`main.tpl` **全部零命中**；只有 `android.support.*` 提供的 `setAccessibilityDelegate`/`sendAccessibilityEvent`（AppCompat 库自带），说明真正的无障碍服务类、引导 Activity、弹窗文案均不在可见 DEX 中。
- 包内存在 [templates/main.tpl](<resource-unit:#1 file:unknown/templates/main.tpl>)（233 208 字节，头部 `78 C7 01 00 00 4B C0 9E CF …` 高熵，非 UTF-8、无明文可读串）与 [templates/.config](<resource-unit:#1 file:unknown/templates/.config>)（内容为 `templates/main.tpl`），符合“加密二阶段 DEX/资源 + 装载清单”的结构；`apktool.yml` 将其列为 `unknownFiles`。
- 因此 Manifest 中声明的 `com.xhqlob.doscby.*` 全部业务类（含无障碍服务 `qxRjxBp`、启动 Activity `AKrheIcrC`、`odkmbqvfw` 等十几个 `uprtknrhf.*` 透明/无标题 Activity）在静态 DEX 中**均不存在**，无法读取其 `onCreate/onResume`、Intent 跳转与弹窗代码。

**2. 仍可确认的诱导相关事实**
- 无障碍服务声明：[AndroidManifest.xml 中的 service](<resource-unit:#1 manifest:components>) `com.xhqlob.doscby.qxRjxBp`，`android:label="Servis Güncellemesi"`（与桌面名相同，土耳其语“服务更新”），`BIND_ACCESSIBILITY_SERVICE` + `android.accessibilityservice` intent-filter。
- 无障碍配置 [res/xml/vyklwvyuouh.xml](<resource-unit:#1 file:res/xml/vyklwvyuouh.xml>)：**无 `android:description`**（系统无障碍列表内无任何功能说明，用户无从判断用途）；`canRetrieveWindowContent="true"`、事件类型 `typeWindowContentChanged|typeWindowStateChanged`、flags `flagDefault|flagIncludeNotImportantViews|flagReportViewIds`——这是**为读取任意应用界面内容并精确定位控件**而配置的（典型的短信/银行界面读取与自动点击能力），远超“服务更新”所需。
- 配置里的 `android:settingsActivity="com.example.root.myapplication.MainActivity"` 是模板残留（真实包名为 `com.xhqlob.doscby`），说明该无障碍配置为批量生成/复用模板，并非为某一真实功能定制。
- 应用整体身份：桌面名“Servis Güncellemesi”（服务更新），实际申请 `READ_SMS/RECEIVE_SMS/SEND_SMS/WRITE_SMS`、`READ_CONTACTS`、`RECORD_AUDIO`、`CALL_PHONE`、`PACKAGE_USAGE_STATS`、`SYSTEM_ALERT_WINDOW`、`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`，与“系统服务更新”宣称完全不符——**名称即伪装**。
- 大量 `android:label=""`、`android:icon="@drawable/aujepehe"`、`excludeFromRecents`、`Theme.NoDisplay` 的隐藏 Activity（`uprtknrhf.*`），以及 `SMS_DELIVER`/`WAP_PUSH_DELIVER` 高优接收器与 `BOOT_COMPLETED/SCREEN_ON/USER_PRESENT` 复活链，属获权后的常驻与短信接管结构；但其具体 UI 文案不可静态还原。

**3. UTG 视角的抓取建议（在可见证据范围内）**
最可靠的做法是不依赖文案：**监测到 `Intent` 目标为 `android.settings.ACCESSIBILITY_SETTINGS`（或 `ACTION_APPLICATION_DETAILS_SETTINGS`）的瞬间**以及**冷启动首个前台 Activity 为 `com.xhqlob.doscby.uprtknrhf.AKrheIcrC` 时**立即录屏 + 抓栈，随后重点看：①启动 Activity 是否是不可取消的原生弹窗/全屏“更新”页；②跳系统设置后是否压入 `SYSTEM_ALERT_WINDOW` 悬浮遮罩（该应用已持有悬浮窗权限）；③从设置页返回后是否 `onResume` 循环重跳。

**4. 覆盖边界**
`main.tpl` 为加密载荷，无可见解密入口（桩代码字符串已混淆/加密），静态无法还原引导页文案与分步教学；本报告未做动态运行（未启动设备侧验证），因此 `step_by_step_flow` 中除 Manifest/配置可确认的节点外均标注为不可静态还原，不做臆测填充。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "可见 classes.dex 仅 26 个类的脱壳/解密桩（com.ertinsit.lcipdp.iemSotG.onCreate 为无效字符串与 switch 混淆），Manifest 声明的全部 com.xhqlob.doscby.* 业务类（无障碍服务 qxRjxBp、启动 Activity AKrheIcrC、uprtknrhf.* 隐藏 Activity）均不在可见 DEX 中；引导页/弹窗/跳转代码与全部文案藏于高熵加密载荷 unknown/templates/main.tpl（233208 字节，由 templates/.config 指向）。仅 Manifest、res/xml/vyklwvyuouh.xml 与权限声明可静态确认，无 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / DexClassLoader / Cipher 等明文串可用于静态串联。",
  "summary_one_liner": "以土耳其语“Servis Güncellemesi（服务更新）”为统一身份伪装，声明一个无任何 description、可读取窗口内容并上报控件 ID 的无障碍服务，真实引导页与跳转逻辑全部封装在加密载荷 templates/main.tpl 中、由脱壳桩类动态释放，静态仅能确认诱导的落点与能力面。",
  "disguise_identity": {
    "app_display_name": "Servis Güncellemesi",
    "claimed_brand_or_persona": "系统/运营商“服务更新”（Servis Güncellemesi）",
    "a11y_service_label": "Servis Güncellemesi",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置无 android:description（系统列表中零功能说明）；settingsActivity 遗留模板值 com.example.root.myapplication.MainActivity 与真实包名不符；十余个 android:label=\"\" 且共用 @drawable/aujepehe 图标、excludeFromRecents、Theme.NoDisplay 的隐藏 Activity；服务类名/包名全随机混淆（qxRjxBp、uprtknrhf.*、ynstfaipm.*）；核心载荷以高熵 main.tpl 加密存放，明文中无任何敏感 API 字符串。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.xhqlob.doscby.uprtknrhf.AKrheIcrC（MAIN/LAUNCHER，实现类体不在可见 DEX）",
      "trigger_event": "用户点击桌面图标冷启动",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该 Activity 的具体界面文案位于加密载荷 templates/main.tpl，静态不可读；应用主题为 Theme.Translucent.NoTitleBar",
      "user_action_requested": "不可静态确认（是否可取消/跳过无法判断）",
      "code_anchor": "AndroidManifest.xml: activity com.xhqlob.doscby.uprtknrhf.AKrheIcrC（LAUNCHER）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "加密载荷 templates/main.tpl 内释放的引导 Activity/弹窗（类名不在可见 DEX）",
      "trigger_event": "Application com.ertinsit.lcipdp.iemSotG.onCreate 中的脱壳桩 FVMTRPjXwtPN.GNiTtOAS 释放并加载真实代码后触发",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不可静态还原；结合应用名推测以“服务更新/需开启辅助服务”为说辞，但无代码证据，不作断言",
      "user_action_requested": "不可静态确认",
      "code_anchor": "com.ertinsit.lcipdp.iemSotG.onCreate / com.ertinsit.lcipdp.FVMTRPjXwtPN.GNiTtOAS"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS，列表项显示为 Servis Güncellemesi",
      "trigger_event": "真实代码中的 Intent 跳转（可见 DEX 内无该字符串，判定由加密载荷内代码发起）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Servis Güncellemesi",
      "shown_text_zh": "“服务更新”——用户在系统无障碍服务列表中看到的就是这一名称，且无任何功能说明文字",
      "user_action_requested": "用户需在系统无障碍列表中点选并确认开启该服务（系统确认弹窗由 OS 提供）",
      "code_anchor": "AndroidManifest.xml: service com.xhqlob.doscby.qxRjxBp android:label=\"Servis Güncellemesi\"; res/xml/vyklwvyuouh.xml（无 android:description）"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "可能的悬浮窗/遮罩引导层（应用已声明 SYSTEM_ALERT_WINDOW）",
      "trigger_event": "不可静态确认（跳转设置后是否压栈遮罩需运行期验证）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不可静态还原；仅能确认具备悬浮窗权限与 Theme.Translucent 无标题主题，具备叠层指引的技术条件",
      "user_action_requested": "不可静态确认",
      "code_anchor": "AndroidManifest.xml: uses-permission android.permission.SYSTEM_ALERT_WINDOW / application android:theme=@android:style/Theme.Translucent.NoTitleBar"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.xhqlob.doscby.qxRjxBp（AccessibilityService，读取窗口内容+控件ID）；短信/联系人/录音/通话等后续链路由 svzikosxo.* 接收器与多个常驻 Service 承载",
      "trigger_event": "onServiceConnected 后监听 typeWindowContentChanged / typeWindowStateChanged",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务被配置为可读取任意应用窗口内容并上报 viewId，具备静默读取界面与自动点击的能力面；具体操作逻辑在加密载荷中",
      "user_action_requested": "不可静态确认（是否自点确认、阻止撤权需运行期验证）",
      "code_anchor": "res/xml/vyklwvyuouh.xml（canRetrieveWindowContent=true, flagReportViewIds）; AndroidManifest.xml: receiver com.xhqlob.doscby.svzikosxo.XFywTLdKTA (SMS_DELIVER)"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项名称：AndroidManifest.xml 中 service com.xhqlob.doscby.qxRjxBp 的 android:label=\"Servis Güncellemesi\"（系统列表原样展示）",
    "系统无障碍列表的说明区：res/xml/vyklwvyuouh.xml 未声明 android:description，故此处为空白——用户看不到任何用途说明",
    "桌面图标名称：application android:label=\"Servis Güncellemesi\"",
    "其余引导/说明文字（原生弹窗、Activity 布局、WebView HTML）均随真实代码封装于加密载荷 unknown/templates/main.tpl，静态不可读"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Servis Güncellemesi",
      "text_zh": "服务更新",
      "source_location": "AndroidManifest.xml: application android:label 与 service com.xhqlob.doscby.qxRjxBp android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "java",
      "text_verbatim": "com.example.root.myapplication.MainActivity",
      "text_zh": "无障碍配置中残留的模板 settingsActivity 值（与本应用真实包名 com.xhqlob.doscby 不符）",
      "source_location": "res/xml/vyklwvyuouh.xml android:settingsActivity",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "und",
      "text_verbatim": "templates/main.tpl",
      "text_zh": "加密载荷文件路径清单（载荷本体为高熵二进制，静态不可解密）",
      "source_location": "unknown/templates/.config",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：可见 DEX 中无跳转与 onResume 逻辑，返回设置页后的重跳/死循环需动态验证",
    "overlay_or_fake_settings": "不可静态确认是否叠放半透明遮罩或高仿系统开关页；但应用已具备 SYSTEM_ALERT_WINDOW 权限与全透明无标题主题，具备该能力条件",
    "restricted_settings_13plus_coaching": "无静态证据；应用 targetSdkVersion=27（低于 Android 13 受限设置机制），未见相关教学代码",
    "post_grant_anti_removal": "不可静态确认；Manifest 中存在 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、BOOT_COMPLETED/SCREEN_ON/USER_PRESENT 高优接收器与多个常驻 Service，具备常驻与自动重启能力，但是否阻止撤权需动态验证",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到前台 Activity 为 com.xhqlob.doscby.uprtknrhf.AKrheIcrC（冷启动首屏）时立即开始录屏；并在任意时刻检测到 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的瞬间打标记并连拍屏幕，随后捕获设置页返回后 0.5–2 秒内的屏幕状态以确认是否压入遮罩/重跳",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导页/弹窗页",
        "page_identifier": "com.xhqlob.doscby.uprtknrhf.AKrheIcrC 或其拉起的透明无标题 Activity/原生 Dialog",
        "why_most_useful": "该页承载唯一的说辞文案与是否可取消的关键判定，是区分“假更新诱导”与良性说明的分界点",
        "observable_utg_signals": ["界面文案与语种（土耳其语“服务更新”类说辞）", "是否存在取消/跳过控件（不可取消则强诱导）", "页面是否为 WebView（可看 URL 是否指向远端）"]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表项",
        "page_identifier": "设置 > 无障碍 列表中的 “Servis Güncellemesi” 条目及其说明区（说明区应为空白）",
        "why_most_useful": "直接证明用户被引导到的目标即该服务，且无功能说明、名称与真实能力不符",
        "observable_utg_signals": ["服务显示名与桌面名一致性", "description 为空", "跳转由应用自身发起（调用栈/Intent 记录）"]
      },
      {
        "page_role": "设置页后压栈的遮罩/引导层",
        "page_identifier": "SYSTEM_ALERT_WINDOW 类型悬浮窗或半透明 Activity（Theme.Translucent.NoTitleBar）",
        "why_most_useful": "叠层遮罩与分步指引是“教唆用户在系统页操作”的最强证据，也决定是否构成遮罩诱导",
        "observable_utg_signals": ["悬浮窗是否覆盖系统设置页并含步骤文字/箭头", "遮罩是否拦截返回键", "从设置返回后是否立即重跳"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：真实引导文案与跳转逻辑全部在加密载荷 templates/main.tpl 中，静态无任何敏感字符串，纯静态分析只能看到伪装名称与无障碍能力面；此外应用使用全透明无标题主题与 label=\"\" 的隐藏 Activity，UTG 若仅按 Activity 名与可见文本判定，可能把空标签透明页视为噪声而漏掉遮罩层；无障碍 description 为空也使“系统页文本特征”类信号失效，需依赖 Intent 跳转与悬浮窗层级信号。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "AndroidManifest.xml: service com.xhqlob.doscby.qxRjxBp (android:label=\"Servis Güncellemesi\", BIND_ACCESSIBILITY_SERVICE)",
    "res/xml/vyklwvyuouh.xml (canRetrieveWindowContent=true, flagReportViewIds, 无 android:description, settingsActivity 模板残留)",
    "com.ertinsit.lcipdp.iemSotG.onCreate",
    "com.ertinsit.lcipdp.FVMTRPjXwtPN.GNiTtOAS",
    "unknown/templates/main.tpl",
    "unknown/templates/.config"
  ]
}
```

</details>

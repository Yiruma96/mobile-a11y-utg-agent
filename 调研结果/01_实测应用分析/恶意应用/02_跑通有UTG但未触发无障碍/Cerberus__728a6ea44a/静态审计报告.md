# MR_144__728a6ea44a｜Cerberus — Flash Player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：112.8s

## 1. 一句话核心结论

- **核心申请方式**：以 Flash Player 品牌伪装、静默声明一个无用途说明但可读取窗口内容并监听界面变化的无障碍服务，真实引导流程藏于加密载荷，运行期通过隐藏 Activity 与系统设置跳转逼迫用户开启后实施窗口内容窃取（Cerberus 家族形态）。
- **静态可见性说明**：明文 DEX 仅为引导壳：Application.onCreate 走字符串解密与方法名混淆的空壳分支，全包无 ACTION_ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / android.settings 明文引用，无 DexClassLoader/getAssets 明文加载点。真实引导 UI、跳转逻辑与文案位于 unknown/support/resources.lz(258KB) 与 unknown/support/jkvzdnuoq(602KB 高熵密文) 加密载荷中，由 support/cache.txt 索引，静态不可还原；可确认的仅为 Manifest 无障碍服务声明、res/xml/vmwbef.xml 能力配置、设备管理器与隐藏 Activity 结构。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `728a6ea44aab94a2d0ebbccbf0c1b4a93fbd9efa8813c19a88d368d6a46b4f4f` |
| 包名 / 年份 | `com.uxlgtsvfdc.zipvwntdy` / 2019 |
| 家族 / 品类 | **Cerberus**（同池样本数：8） |
| 原始来源标识 | https://www.threatfabric.com/blogs/cerberus-a-new-banking-trojan-from-the-underworld.html |
| 桌面显示名 | Flash Player |
| 引导页宣称品牌/身份 | Adobe Flash Player（伪造知名播放器品牌） |
| 系统无障碍列表服务名 | Flash Player Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未声明 android:description，系统列表中不显示任何用途说明；服务名与桌面名统一冒用 Flash Player；另有多个 label="" 且 excludeFromRecents/noHistory/Theme.NoDisplay 的隐藏 Activity（ybcdvfwxpn.GrlQupux、ybcdvfwxpn.uYnhSVcns、dvbTumHTyOA）用于遮罩跳板；设备管理器 receiver 伪装为 System Driver；类名/方法名与字符串全量混淆加密 |
| 无障碍服务类名 | `com.uxlgtsvfdc.zipvwntdy.zksemxfl.RAKGxUYWGpo` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.uxlgtsvfdc.zipvwntdy.ZCQefkpkSqO（LAUNCHER，label 继承 Flash Player） | 用户点击桌面 Flash Player 图标，onCreate 触发 | 原生Activity | **原文**：无（该 Activity 未声明 label/文案，界面内容由加密载荷决定）<br>**译注**：界面文案不可静态还原 | 不可静态还原 | `com.uxlgtsvfdc.zipvwntdy.ZCQefkpkSqO（Manifest LAUNCHER）；com.eramtetinr.gcsehxroyn.SHfnEU.onCreate` |
| 2 | 冷启动入口 | Application 初始化：com.eramtetinr.gcsehxroyn.SHfnEU.onCreate → com.jwrqmzaum.jwrqmzaum.TSgtmhIs.qaiNbK 解密链 | Application.onCreate 在进程启动时无条件执行，先解密字符串与载荷索引再判定 | 不可静态还原 | **原文**：无（明文中仅见混淆占位串 "tmtvul kmealsp"、"cmieoncei chaj"、"semscs mkbptsc tucrm"、"sgptdlutinqnc rhuez"、"slanonelnwc"）<br>**译注**：无意义占位串，解密后语义不可静态取得 | 无用户交互，后台完成解密与载荷准备 | `com.eramtetinr.gcsehxroyn.SHfnEU.onCreate / TRwVWPI / KWbjUpDysNY；unknown/support/resources.lz` |
| 3 | 引导说明页 | 加密载荷内的引导 UI（弹窗或 WebView，具体载体不可静态还原） | 载荷解密加载后由载荷代码控制，疑似冷启动即触发 | 不可静态还原 | 无 | 不可静态还原（恶意样本通常无可取消或跳过按钮） | `unknown/support/resources.lz；unknown/support/jkvzdnuoq` |
| 4 | 跳无障碍设置 | 系统无障碍服务列表中的 "Flash Player Service" 条目（配置 res/xml/vmwbef.xml） | 载荷代码发起 ACTION_ACCESSIBILITY_SETTINGS 跳转（跳转指令位于密文，明文 DEX 无该字符串） | 系统无障碍页 | **原文**：Flash Player Service<br>**译注**：系统无障碍列表中显示的服务名，无用途说明文字 | 要求用户在该列表中手动找到并开启该服务；是否有取消路径取决于密文内 UI | `#1 manifest:components；res/xml/vmwbef.xml` |
| 5 | 获权后动作 | com.uxlgtsvfdc.zipvwntdy.zksemxfl.RAKGxUYWGpo（无障碍服务本体，另含 HJGykA/MUSPcOURejIN/vOxlPEKl/HBOxMrf/QbhgNqIB/kjqHTlQgl 等配套 Service） | 系统回调 onAccessibilityEvent(typeWindowContentChanged\|typeWindowStateChanged) | 不可静态还原 | 无 | 无（获权后静默读取窗口内容） | `res/xml/vmwbef.xml；com.uxlgtsvfdc.zipvwntdy.zksemxfl.RAKGxUYWGpo` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目：服务名 "Flash Player Service"（Manifest service android:label），android:description 缺失，列表中无任何用途说明
- 应用桌面/最近任务名称："Flash Player"（application android:label）
- 设备管理器说明中的伪装名："System Driver"（receiver com.uxlgtsvfdc.zipvwntdy.nmhzcosgyedf.yaMEmAPT 的 label）
- 加密载荷 unknown/support/resources.lz 与 unknown/support/jkvzdnuoq 内的引导弹窗/WebView/悬浮层文案（静态不可还原）
- 明文 DEX 中仅存无意义混淆占位串（SHfnEU.onCreate 内 "tmtvul kmealsp" 等），不构成面向用户的文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Flash Player | Flash 播放器（伪造 Adobe Flash Player 品牌） | `AndroidManifest.xml application/@android:label` | 未知 |
| en | Flash Player Service | Flash 播放器服务（无障碍列表中的服务名，冒用播放器身份掩盖读屏与窗口读取能力） | `AndroidManifest.xml service com.uxlgtsvfdc.zipvwntdy.zksemxfl.RAKGxUYWGpo/@android:label` | 未知 |
| en | System Driver | 系统驱动（设备管理器 receiver 伪装名，配合防卸载） | `AndroidManifest.xml receiver com.uxlgtsvfdc.zipvwntdy.nmhzcosgyedf.yaMEmAPT/@android:label` | 未知 |
| unknown | （加密载荷内引导文案，静态不可取得） | 无法翻译：文案位于 resources.lz / jkvzdnuoq 密文中 | `unknown/support/resources.lz；unknown/support/jkvzdnuoq` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：明文 DEX 内无设置页回跳判定逻辑（未出现 isAccessibilityEnabled、Settings$Secure 相关判定，仅见 com.jwrqmzaum.jwrqmzaum.xXGbetr 的 Settings$Secure.reloadStatus 无关调用），实际拒绝后行为由加密载荷决定；结合该家族形态高度疑似 onResume 或定时器循环重跳
- **遮罩叠层 / 高仿系统设置页**：不可静态还原（疑似）：包内已存在多个 label=""、excludeFromRecents、noHistory、Theme.NoDisplay 的隐藏 Activity（ybcdvfwxpn.GrlQupux、ybcdvfwxpn.uYnhSVcns、dvbTumHTyOA）及高权限无障碍读取配置，具备叠层遮罩与高仿开关页所需组件，但绘制代码在密文内
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=27，早于 Android 13 受限设置机制，无需该项教学）
- **获权后即时行为与防撤权机制**：不可静态还原；已确认的对抗设施为设备管理器 receiver（BIND_DEVICE_ADMIN + @xml/uvu + 高优先级 DEVICE_ADMIN_DISABLED/ACTION_DEVICE_ADMIN_DISABLE_REQUESTED 监听），用于提高卸载/停用难度
- **良性降级 / 替代方案**：无（未见任何降级路径；无描述的无障碍服务 + 设备管理器 + 隐藏 Activity 组合不存在良性替代模式）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测任意 Activity 启动或 intent 指向 com.android.settings 的 AccessibilitySettings/Settings$AccessibilitySettingsActivity，或点击图标进入 ZCQefkpkSqO 后 0–3 秒内出现的任意自有弹窗/WebView；同时监听 RAKGxUYWGpo 服务被启用事件作为获权确认点
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：明文 DEX 为引导壳，全部引导文案与跳转逻辑位于 unknown/support/resources.lz 与 jkvzdnuoq 加密载荷内，静态侧无法给出逐字文本与拒绝循环机制；载荷若为纯图片/GIF 引导还需 OCR；应用本身无静态加壳特征但采用载荷级加密，静态不可见不阻碍运行期 UTG 捕获，动态执行是必要补充手段。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | ZCQefkpkSqO 启动后出现的 Dialog 或全屏 Activity，标题/正文含 Flash Player 与“启用服务/权限”语义 | 这是唯一能取得逐字诱导文案的位置，静态密文无法替代 | 弹窗文本全文与按钮文案；是否存在取消/跳过按钮；弹窗是否覆盖返回键（不可取消） |
| **跳转前 WebView 教学页** | 含 WebView 组件的 Activity（可能为 label="" 的隐藏 Activity），URL 为 file:///android_asset 或远端 http(s) | 区分本地 HTML 教学与远端云控页面，决定是否属云控变脸 | WebView URL 与加载来源；页面内步骤编号文本（如“第1步/第2步”）；是否内嵌图片引导 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中的 "Flash Player Service" 条目 | 确认服务无 description、名称冒用播放器品牌，是身份不一致的直接运行期证据 | 列表项标题文本；说明/摘要区域是否为空；应用图标是否为伪造 Flash 图标 |
| **设置页返回后遮罩/循环重跳页** | 从设置页返回时立即压栈的透明或全屏 Activity，或再次弹出的引导弹窗 | 证明拒绝后的强制循环与遮罩叠层，是“非自愿授权”定性的关键 | 返回后 0–2 秒内是否自动重跳设置页；是否出现悬浮窗/遮罩层节点；返回键是否被拦截 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.eramtetinr.gcsehxroyn.SHfnEU.onCreate`
- `com.uxlgtsvfdc.zipvwntdy.ZCQefkpkSqO`
- `com.uxlgtsvfdc.zipvwntdy.zksemxfl.RAKGxUYWGpo`
- `res/xml/vmwbef.xml`
- `unknown/support/resources.lz`
- `com.uxlgtsvfdc.zipvwntdy.nmhzcosgyedf.yaMEmAPT`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 定向核验结论（围绕“无障碍权限引导流程”）

**核实到的静态事实**

- 启动入口：[ZCQefkpkSqO](<resource-unit:#1 manifest:components>) 是唯一的 LAUNCHER Activity，并且没有声明 `android:label`，因此继承应用名 `Flash Player`；Application 类为 [com.eramtetinr.gcsehxroyn.SHfnEU](<resource-unit:#1.dex1 code:com.eramtetinr.gcsehxroyn.SHfnEU>)。
- 无障碍服务：`com.uxlgtsvfdc.zipvwntdy.zksemxfl.RAKGxUYWGpo`，label 为 `Flash Player Service`，**没有 `android:description`**；配置 [res/xml/vmwbef.xml](<resource-unit:#1 file:res/xml/vmwbef.xml>) 只开启 `canRetrieveWindowContent="true"`，并启用 `flagIncludeNotImportantViews|flagReportViewIds`，事件类型为 `typeWindowContentChanged|typeWindowStateChanged`。这是典型的“读取窗口内容并监听界面变化”的凭证窃取配置，而系统列表中的用途说明为空。
- 同时存在的辅助伪装点：设备管理器 receiver 的 label 为 `System Driver`，绑定 `@xml/uvu`，用于提高卸载难度；多个 `label=""`、`excludeFromRecents`、`noHistory`、`Theme.NoDisplay` 的隐藏 Activity，例如 `ybcdvfwxpn.GrlQupux`、`dvbTumHTyOA`，可用于遮罩或跳板。
- **关键引导代码不在明文 DEX 中**：全包搜索 `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`android.settings`、`isAccessibilityTool`、`DexClassLoader` 和 `getAssets` 都没有命中；`SHfnEU.onCreate()` 只做字符串解密和方法名混淆的空壳调用，其中 `TRwVWPI()` 和 `KWbjUpDysNY()` 都是空实现，switch 分支恒不成立。
- 真正的载荷在 [unknown/support/resources.lz](<resource-unit:#1 file:unknown/support/resources.lz>)（258,236 字节，头 `2bfc0000`）、[unknown/support/jkvzdnuoq](<resource-unit:#1 file:unknown/support/jkvzdnuoq>)（601,998 字节，高熵密文）以及 [unknown/support/cache.txt](<resource-unit:#1 file:unknown/support/cache.txt>) 的 `support/resources.lz` 索引中。另有多个字母乱序文件名，内容为等长随机串。

**判定**

无障碍引导所依赖的**跳转点、弹窗或 WebView 文案、拒绝后的循环重跳逻辑全部位于加密载荷内**，在当前工具调用预算内无法静态还原；`onCreate` 的解密链路已被字符串混淆和方法名替换彻底遮蔽。因此，纯运行期 UTG 视角只能给出**可捕获的触发点与判据**，不能给出逐字文案。已确认的恶意事实是：以 `Flash Player` 品牌伪装，提供一个无描述、高读取权限的无障碍服务，并搭配设备管理器和隐藏 Activity。这与 Cerberus 系列样本的银行木马形态一致。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "明文 DEX 仅为引导壳：Application.onCreate 走字符串解密与方法名混淆的空壳分支，全包无 ACTION_ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / android.settings 明文引用，无 DexClassLoader/getAssets 明文加载点。真实引导 UI、跳转逻辑与文案位于 unknown/support/resources.lz(258KB) 与 unknown/support/jkvzdnuoq(602KB 高熵密文) 加密载荷中，由 support/cache.txt 索引，静态不可还原；可确认的仅为 Manifest 无障碍服务声明、res/xml/vmwbef.xml 能力配置、设备管理器与隐藏 Activity 结构。",
  "summary_one_liner": "以 Flash Player 品牌伪装、静默声明一个无用途说明但可读取窗口内容并监听界面变化的无障碍服务，真实引导流程藏于加密载荷，运行期通过隐藏 Activity 与系统设置跳转逼迫用户开启后实施窗口内容窃取（Cerberus 家族形态）。",
  "disguise_identity": {
    "app_display_name": "Flash Player",
    "claimed_brand_or_persona": "Adobe Flash Player（伪造知名播放器品牌）",
    "a11y_service_label": "Flash Player Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未声明 android:description，系统列表中不显示任何用途说明；服务名与桌面名统一冒用 Flash Player；另有多个 label=\"\" 且 excludeFromRecents/noHistory/Theme.NoDisplay 的隐藏 Activity（ybcdvfwxpn.GrlQupux、ybcdvfwxpn.uYnhSVcns、dvbTumHTyOA）用于遮罩跳板；设备管理器 receiver 伪装为 System Driver；类名/方法名与字符串全量混淆加密"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.uxlgtsvfdc.zipvwntdy.ZCQefkpkSqO（LAUNCHER，label 继承 Flash Player）",
      "trigger_event": "用户点击桌面 Flash Player 图标，onCreate 触发",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（该 Activity 未声明 label/文案，界面内容由加密载荷决定）",
      "shown_text_zh": "界面文案不可静态还原",
      "user_action_requested": "不可静态还原",
      "code_anchor": "com.uxlgtsvfdc.zipvwntdy.ZCQefkpkSqO（Manifest LAUNCHER）；com.eramtetinr.gcsehxroyn.SHfnEU.onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "Application 初始化：com.eramtetinr.gcsehxroyn.SHfnEU.onCreate → com.jwrqmzaum.jwrqmzaum.TSgtmhIs.qaiNbK 解密链",
      "trigger_event": "Application.onCreate 在进程启动时无条件执行，先解密字符串与载荷索引再判定",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（明文中仅见混淆占位串 \"tmtvul kmealsp\"、\"cmieoncei chaj\"、\"semscs mkbptsc tucrm\"、\"sgptdlutinqnc rhuez\"、\"slanonelnwc\"）",
      "shown_text_zh": "无意义占位串，解密后语义不可静态取得",
      "user_action_requested": "无用户交互，后台完成解密与载荷准备",
      "code_anchor": "com.eramtetinr.gcsehxroyn.SHfnEU.onCreate / TRwVWPI / KWbjUpDysNY；unknown/support/resources.lz"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "加密载荷内的引导 UI（弹窗或 WebView，具体载体不可静态还原）",
      "trigger_event": "载荷解密加载后由载荷代码控制，疑似冷启动即触发",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "引导文案全部位于 resources.lz / jkvzdnuoq 密文中，静态不可见",
      "user_action_requested": "不可静态还原（恶意样本通常无可取消或跳过按钮）",
      "code_anchor": "unknown/support/resources.lz；unknown/support/jkvzdnuoq"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍服务列表中的 \"Flash Player Service\" 条目（配置 res/xml/vmwbef.xml）",
      "trigger_event": "载荷代码发起 ACTION_ACCESSIBILITY_SETTINGS 跳转（跳转指令位于密文，明文 DEX 无该字符串）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Flash Player Service",
      "shown_text_zh": "系统无障碍列表中显示的服务名，无用途说明文字",
      "user_action_requested": "要求用户在该列表中手动找到并开启该服务；是否有取消路径取决于密文内 UI",
      "code_anchor": "#1 manifest:components；res/xml/vmwbef.xml"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.uxlgtsvfdc.zipvwntdy.zksemxfl.RAKGxUYWGpo（无障碍服务本体，另含 HJGykA/MUSPcOURejIN/vOxlPEKl/HBOxMrf/QbhgNqIB/kjqHTlQgl 等配套 Service）",
      "trigger_event": "系统回调 onAccessibilityEvent(typeWindowContentChanged|typeWindowStateChanged)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务能力：canRetrieveWindowContent=true、flagIncludeNotImportantViews、flagReportViewIds，即读取全窗口节点并含非重要视图与控件 ID，供后续叠加与自动填表窃取使用",
      "user_action_requested": "无（获权后静默读取窗口内容）",
      "code_anchor": "res/xml/vmwbef.xml；com.uxlgtsvfdc.zipvwntdy.zksemxfl.RAKGxUYWGpo"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目：服务名 \"Flash Player Service\"（Manifest service android:label），android:description 缺失，列表中无任何用途说明",
    "应用桌面/最近任务名称：\"Flash Player\"（application android:label）",
    "设备管理器说明中的伪装名：\"System Driver\"（receiver com.uxlgtsvfdc.zipvwntdy.nmhzcosgyedf.yaMEmAPT 的 label）",
    "加密载荷 unknown/support/resources.lz 与 unknown/support/jkvzdnuoq 内的引导弹窗/WebView/悬浮层文案（静态不可还原）",
    "明文 DEX 中仅存无意义混淆占位串（SHfnEU.onCreate 内 \"tmtvul kmealsp\" 等），不构成面向用户的文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Flash Player",
      "text_zh": "Flash 播放器（伪造 Adobe Flash Player 品牌）",
      "source_location": "AndroidManifest.xml application/@android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Flash Player Service",
      "text_zh": "Flash 播放器服务（无障碍列表中的服务名，冒用播放器身份掩盖读屏与窗口读取能力）",
      "source_location": "AndroidManifest.xml service com.uxlgtsvfdc.zipvwntdy.zksemxfl.RAKGxUYWGpo/@android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "System Driver",
      "text_zh": "系统驱动（设备管理器 receiver 伪装名，配合防卸载）",
      "source_location": "AndroidManifest.xml receiver com.uxlgtsvfdc.zipvwntdy.nmhzcosgyedf.yaMEmAPT/@android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "unknown",
      "text_verbatim": "（加密载荷内引导文案，静态不可取得）",
      "text_zh": "无法翻译：文案位于 resources.lz / jkvzdnuoq 密文中",
      "source_location": "unknown/support/resources.lz；unknown/support/jkvzdnuoq",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：明文 DEX 内无设置页回跳判定逻辑（未出现 isAccessibilityEnabled、Settings$Secure 相关判定，仅见 com.jwrqmzaum.jwrqmzaum.xXGbetr 的 Settings$Secure.reloadStatus 无关调用），实际拒绝后行为由加密载荷决定；结合该家族形态高度疑似 onResume 或定时器循环重跳",
    "overlay_or_fake_settings": "不可静态还原（疑似）：包内已存在多个 label=\"\"、excludeFromRecents、noHistory、Theme.NoDisplay 的隐藏 Activity（ybcdvfwxpn.GrlQupux、ybcdvfwxpn.uYnhSVcns、dvbTumHTyOA）及高权限无障碍读取配置，具备叠层遮罩与高仿开关页所需组件，但绘制代码在密文内",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=27，早于 Android 13 受限设置机制，无需该项教学）",
    "post_grant_anti_removal": "不可静态还原；已确认的对抗设施为设备管理器 receiver（BIND_DEVICE_ADMIN + @xml/uvu + 高优先级 DEVICE_ADMIN_DISABLED/ACTION_DEVICE_ADMIN_DISABLE_REQUESTED 监听），用于提高卸载/停用难度",
    "benign_graceful_degradation": "无（未见任何降级路径；无描述的无障碍服务 + 设备管理器 + 隐藏 Activity 组合不存在良性替代模式）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测任意 Activity 启动或 intent 指向 com.android.settings 的 AccessibilitySettings/Settings$AccessibilitySettingsActivity，或点击图标进入 ZCQefkpkSqO 后 0–3 秒内出现的任意自有弹窗/WebView；同时监听 RAKGxUYWGpo 服务被启用事件作为获权确认点",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "ZCQefkpkSqO 启动后出现的 Dialog 或全屏 Activity，标题/正文含 Flash Player 与“启用服务/权限”语义",
        "why_most_useful": "这是唯一能取得逐字诱导文案的位置，静态密文无法替代",
        "observable_utg_signals": ["弹窗文本全文与按钮文案", "是否存在取消/跳过按钮", "弹窗是否覆盖返回键（不可取消）"]
      },
      {
        "page_role": "跳转前 WebView 教学页",
        "page_identifier": "含 WebView 组件的 Activity（可能为 label=\"\" 的隐藏 Activity），URL 为 file:///android_asset 或远端 http(s)",
        "why_most_useful": "区分本地 HTML 教学与远端云控页面，决定是否属云控变脸",
        "observable_utg_signals": ["WebView URL 与加载来源", "页面内步骤编号文本（如“第1步/第2步”）", "是否内嵌图片引导"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中的 \"Flash Player Service\" 条目",
        "why_most_useful": "确认服务无 description、名称冒用播放器品牌，是身份不一致的直接运行期证据",
        "observable_utg_signals": ["列表项标题文本", "说明/摘要区域是否为空", "应用图标是否为伪造 Flash 图标"]
      },
      {
        "page_role": "设置页返回后遮罩/循环重跳页",
        "page_identifier": "从设置页返回时立即压栈的透明或全屏 Activity，或再次弹出的引导弹窗",
        "why_most_useful": "证明拒绝后的强制循环与遮罩叠层，是“非自愿授权”定性的关键",
        "observable_utg_signals": ["返回后 0–2 秒内是否自动重跳设置页", "是否出现悬浮窗/遮罩层节点", "返回键是否被拦截"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "存在显著盲区：明文 DEX 为引导壳，全部引导文案与跳转逻辑位于 unknown/support/resources.lz 与 jkvzdnuoq 加密载荷内，静态侧无法给出逐字文本与拒绝循环机制；载荷若为纯图片/GIF 引导还需 OCR；应用本身无静态加壳特征但采用载荷级加密，静态不可见不阻碍运行期 UTG 捕获，动态执行是必要补充手段。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.eramtetinr.gcsehxroyn.SHfnEU.onCreate",
    "com.uxlgtsvfdc.zipvwntdy.ZCQefkpkSqO",
    "com.uxlgtsvfdc.zipvwntdy.zksemxfl.RAKGxUYWGpo",
    "res/xml/vmwbef.xml",
    "unknown/support/resources.lz",
    "com.uxlgtsvfdc.zipvwntdy.nmhzcosgyedf.yaMEmAPT"
  ]
}
```

</details>

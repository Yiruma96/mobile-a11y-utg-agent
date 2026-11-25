# MB_072__5362c4101f｜Cerberus — Player Sistem Güncelleme

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：183.6s

## 1. 一句话核心结论

- **核心申请方式**：伪装成土耳其语“Player 系统更新”的 Cerberus 系银行木马，冷启动即由 Application 解密加载二阶段 dex，再以无 description、仅显示为“Player Güncellemesi”的静默无障碍服务诱导用户开启全局读屏权限，全部引导文案藏在加密载荷内。
- **静态可见性说明**：无障碍服务类 hirmriumcrggxxcgwjox.jsainzbmudc.qia.xjnebkglqnohbb、Launcher Activity tjhrxdtsttubyve 及全部引导 UI 类均不在 classes.dex 中（对 21 个 qia.* 类名做全文/定义/结构查询全部 no_matches），仅存在于 assets/mUQtlh.json（660KB，gzip 1f8b 加密容器），由 Aunhappyprogram.attachBaseContext 经 Obringrate.casegreen 反射构造 DexClassLoader 解密加载。res/values 无 strings.xml，除两条土耳其语 label 外无任何界面原文；assets 下 HTML 均为 MoPub/UnityAds SDK 自带资源，与本应用引导无关。因此纯 UTG 视角的弹窗文案、取消按钮、拒绝后重跳逻辑均无法静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `5362c4101f153eedaca5344cdec4897af155b364dd1609ad19a495af745fcc50` |
| 包名 / 年份 | `foztfoooubzwjwkapdthkpmw.zifgisscqs.gylqexbgzbysbeituofejtazcwh` / 2023 |
| 家族 / 品类 | **Cerberus**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Player Sistem Güncelleme |
| 引导页宣称品牌/身份 | 泛化的“Player 播放器系统更新/升级包”（无真实品牌主体，包名为随机乱码串，不指向任何已知厂商） |
| 系统无障碍列表服务名 | Player Güncellemesi |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 桌面名与无障碍服务名仅差一个词（Sistem Güncelleme vs Güncellemesi），规避同名/同串检测；2) 无障碍服务完全不声明 android:description，系统列表中无任何用途说明；3) 大量 Activity 使用 android:label="" 与 Theme.NoDisplay / Translucent.NoTitleBar / excludeFromRecents，页面名空白且不进入最近任务；4) 其余 Activity 的 label 指向 label_barely/label_vacuum 等字符串资源，包内未解码出 strings.xml，运行时呈空或占位；5) 类名/包名全量随机词拼接混淆（qia、hgztointzudgq 等），并伴随大量无意义算术指令与字符混淆常量；6) 二阶段 dex 以 gzip+加密容器 assets/mUQtlh.json 形式落地，用反射 DexClassLoader 加载，规避静态特征；7) 未声明 isAccessibilityTool，依赖 targetSdk 29 在低版本系统上规避 Android 11+ 的无障碍权限警告。 |
| 无障碍服务类名 | `hirmriumcrggxxcgwjox.jsainzbmudc.qia.xjnebkglqnohbb` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | Application foztfoooubzwjwkapdthkpmw.zifgisscqs.gylqexbgzbysbeituofejtazcwh.Aunhappyprogram → 反射 DexClassLoader 加载 assets/mUQtlh.json | 进程启动 attachBaseContext() 回调（早于任何 Activity onCreate） | 不可静态还原 | 无 | 无需用户操作 | `foztfoooubzwjwkapdthkpmw.zifgisscqs.gylqexbgzbysbeituofejtazcwh.Aunhappyprogram#attachBaseContext / Obringrate#casegreen` |
| 2 | 冷启动入口 | Launcher Activity hirmriumcrggxxcgwjox.jsainzbmudc.qia.tjhrxdtsttubyve（MAIN + LAUNCHER + android.app.role.SMS），运行于解密后的二阶段 dex | 用户点击桌面图标「Player Sistem Güncelleme」 | 不可静态还原 | **原文**：Player Sistem Güncelleme<br>**译注**：桌面图标名称：Player 系统更新 | 点击图标启动（唯一可见入口，无其他正常业务入口） | `AndroidManifest.xml activity android:name="hirmriumcrggxxcgwjox.jsainzbmudc.qia.tjhrxdtsttubyve"` |
| 3 | 引导说明页 | 二阶段 dex 内的引导 Activity / Dialog（类名与文案均被加密，静态不可见） | 不可静态还原（推测为 Launcher Activity onCreate/onResume 或首次运行标记判定后触发） | 不可静态还原 | 无 | 不可静态还原 | `二阶段 assets/mUQtlh.json 解密后 dex（静态不可达）` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS，落点为服务项「Player Güncellemesi」 | 不可静态还原（Intent 构造代码位于二阶段 dex） | 系统无障碍页 | **原文**：Player Güncellemesi<br>**译注**：系统无障碍服务列表中显示的服务名：Player 更新 | 用户在系统无障碍列表中手动开启该服务（无 description，系统列表内不展示任何用途说明） | `AndroidManifest.xml service hirmriumcrggxxcgwjox.jsainzbmudc.qia.xjnebkglqnohbb + res/xml/dcbyuo.xml` |
| 5 | 获权后动作 | 无障碍服务 hirmriumcrggxxcgwjox.jsainzbmudc.qia.xjnebkglqnohbb#onServiceConnected / onAccessibilityEvent | 用户在系统设置中启用服务后系统绑定回调 | 不可静态还原 | 无 | 无需操作；服务按 typeWindowContentChanged\|typeWindowStateChanged 持续抓取前台界面 | `res/xml/dcbyuo.xml（canRetrieveWindowContent=true, flagReportViewIds）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 桌面启动器图标名称：application@android:label = "Player Sistem Güncelleme"（AndroidManifest.xml application 节点）
- 系统无障碍服务列表条目：service@android:label = "Player Güncellemesi"（AndroidManifest.xml service 节点）；该服务无 android:description，故系统列表内除服务名外不呈现任何用途说明
- 多个 Activity 标题为空字符串 android:label=""（如 nlnoqordql、wfhxquzg、kpdfpah），配合 Theme.NoDisplay / Translucent.NoTitleBar / excludeFromRecents，页面无标题且不进最近任务
- 其余 Activity 的 label 指向 label_barely、label_vacuum、label_position 等字符串资源，包内 res/values 未解码出 strings.xml，运行时呈空或占位符
- assets/*.html 与 assets/lpc/*.json 经核验为 MoPub/UnityAds 广告 SDK 自带资源（apn_vastvideo.html、LivePersonaCardStrings.*），不承载本应用引导文案
- 真正面向用户的引导弹窗/说明页/跳转按钮文案：全部位于加密二阶段 dex（assets/mUQtlh.json），静态不可见，须运行期 UTG/截图捕获

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Player Sistem Güncelleme | Player 系统更新 | `AndroidManifest.xml <application android:label>` | 假更新 |
| tr | Player Güncellemesi | Player 更新 | `AndroidManifest.xml <service android:name="...xjnebkglqnohbb" android:label>` | 假更新 |
| tr | wjjvubqd | （无意义随机串，非可读文案） | `AndroidManifest.xml 通知监听 service android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：引导与重跳逻辑位于加密二阶段 dex（assets/mUQtlh.json），无任何静态可见的 onResume 重跳或定时器代码；从样本性质（Cerberus 系银行木马、targetSdk 29、仅一个 Launcher 入口且无真实业务界面）判断极可能为获权前阻断式循环，但须 UTG 抓取确认
- **遮罩叠层 / 高仿系统设置页**：无悬浮窗通道：权限清单不含 SYSTEM_ALERT_WINDOW，无法叠放半透明遮罩或全屏悬浮窗；但声明了 Theme.Translucent.NoTitleBar 与多个 Theme.NoDisplay + excludeFromRecents 的空白标题 Activity，具备以透明 Activity 模拟“设置引导层”的能力（具体实现不可静态还原）
- **Android 13+ 受限设置（Restricted Settings）应对**：无：targetSdkVersion=29，不触发 Android 13+ 的受限设置（Restricted Settings）流程；包内无任何应用详情页/右上角菜单相关引导文本
- **获权后即时行为与防撤权机制**：不可静态还原：静态未发现 GLOBAL_ACTION_BACK/HOME 或自点确认代码（相关实现只可能在二阶段 dex）；但样本另行申请 DEVICE_ADMIN 广播接收器（BIND_DEVICE_ADMIN + res/xml/whhhlxfkse）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，构成独立于无障碍的防卸载/保活能力
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以“监测到 Activity 跳转 android.settings.ACCESSIBILITY_SETTINGS（或系统无障碍设置包 com.android.settings/.Settings$AccessibilitySettings）”为第一触发点；同时以“冷启动首帧出现非 Launcher 的第二个 Activity/Dialog（尤其 Theme.Translucent 透明页）”为第二触发点，因本样本 Launcher 本身运行在解密后的二阶段 dex，弹窗可能在首帧即出现
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在明确盲区：无障碍服务类与全部引导 UI 位于加密二阶段 dex（assets/mUQtlh.json，gzip+加密容器，660KB），静态零可见，只能靠运行期 UTG/截图补齐文案与拒绝循环逻辑；另 res/values 缺 strings.xml，Activity label 指向的资源值缺失，静态无法判断页面标题。注意静态加壳/加密本身不阻挡运行期 UTG 捕获。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后首个引导页（透明/空白标题 Activity 或 Dialog）** | Activity hirmriumcrggxxcgwjox.jsainzbmudc.qia.tjhrxdtsttubyve 之后新压栈的非系统 Activity；标题为空、可能背景透明、不出现在最近任务 | 这是全包唯一静态不可见的关键节点：本样本除广告 SDK 外无任何本地文案资源，所有诱导措辞只存在于该页，UTG 提取的文本即为判定“假更新/恐吓/教唆忽视警告”的唯一直接证据 | 页面上出现的土耳其语/英语诱导文案（如 güncelleme、erişilebilirlik、izin、etkinleştir）；是否存在“开启/İzin Ver”主按钮而缺少“取消/İptal/跳过”次级按钮；页面是否为空白标题 + 半透明背景（Activity 名称与桌面名不一致） |
| **跳转系统无障碍设置后的服务列表项** | 系统 Settings 无障碍列表中名为「Player Güncellemesi」的条目，其下方无任何 description 描述行 | 可实证“服务名伪装 + 零说明”的最终呈现形态：条目只有名称、无用途说明，用户无法判断其真实权限范围，是最强的身份欺骗证据 | 服务条目文本 Player Güncellemesi；条目下方 description 为空（与桌面名 Player Sistem Güncelleme 仅一词之差）；系统是否弹出“此服务可读取全部内容”类警告（targetSdk 29 在 Android 10 及以下通常不弹） |
| **拒绝/返回后的反馈循环页** | 用户从系统设置返回后重新出现的前台 Activity，或每 N 秒重复弹出的同一引导 Activity | 区分“良性降级”与“阻断式强制”：本样本无真实业务功能，若返回后立即重跳设置页，即可定性为 COERCE_REFUSAL_LOOP_RELAUNCH | 返回应用后 1~3 秒内 Activity 栈是否再次跳转 ACCESSIBILITY_SETTINGS；是否出现倒计时/进度条式的等待引导；是否存在任何可关闭引导的按钮 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `foztfoooubzwjwkapdthkpmw.zifgisscqs.gylqexbgzbysbeituofejtazcwh.Aunhappyprogram#attachBaseContext`
- `foztfoooubzwjwkapdthkpmw.zifgisscqs.gylqexbgzbysbeituofejtazcwh.Obringrate#casegreen`
- `res/xml/dcbyuo.xml`
- `AndroidManifest.xml service hirmriumcrggxxcgwjox.jsainzbmudc.qia.xjnebkglqnohbb`
- `AndroidManifest.xml activity hirmriumcrggxxcgwjox.jsainzbmudc.qia.tjhrxdtsttubyve`
- `assets/mUQtlh.json`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 定向核验结论（14 次工具调用内收口）

**核心判定：无障碍引导流程整体位于加密二阶段载荷内，静态不可见；但 Manifest 与一阶段壳已能确认“假更新诱导 + 无障碍服务隐藏式声明 + DexClassLoader 二阶段解密加载”的完整框架。**

已确认事实：

1. **应用身份伪装为“播放器系统更新”**：`application@android:label` = `Player Sistem Güncelleme`（土耳其语“Player 系统更新”），而包名为随机乱码串 `foztfoooubzwjwkapdthkpmw.zifgisscqs.gylqexbgzbysbeituofejtazcwh`，无任何品牌一致信息。见 [AndroidManifest.xml 应用声明](<resource-unit:#1 manifest:basic_info>)。
2. **无障碍服务声明刻意极简、无说明**：`hirmriumcrggxxcgwjox.jsainzbmudc.qia.xjnebkglqnohbb`，`android:label="Player Güncellemesi"`（与桌面名仅差一词，规避同名检测），**无 `android:description`**，`BIND_ACCESSIBILITY_SERVICE` 保护，meta-data 指向 [res/xml/dcbyuo.xml](<resource-unit:#1 file:res/xml/dcbyuo.xml>)，其中 `canRetrieveWindowContent="true"`、事件类型 `typeWindowContentChanged|typeWindowStateChanged`、`flagIncludeNotImportantViews|flagReportViewIds`——典型读屏/抓取输入框与控件 ID 的银行木马配置，但**不声明 `isAccessibilityTool`**，也不给出任何面向用户的用途说明。
3. **无障碍服务类与启动 Activity 均不在 classes.dex 中**：`search_text_in_app` / `search_function_definitions` / `get_class_structure` 对 `hirmriumcrggxxcgwjox.jsainzbmudc.qia.*` 全部 `no_matches`，`list_codebase` 只列出 3 个壳包（`hgztointzudgq`/`ifllkexo`/`ldfxpkwseu`，共 50 类）。即**连 Launcher Activity（`tjhrxdtsttubyve`，MAIN+LAUNCHER+SMS role）都在二阶段 dex 里**，应用冷启动第一步就是先解密加载。
4. **二阶段载荷 = 加密资产 + 反射 DexClassLoader**：[Aunhappyprogram#attachBaseContext()](<resource-unit:#1.dex1 code:foztfoooubzwjwkapdthkpmw.zifgisscqs.gylqexbgzbysbeituofejtazcwh.Aunhappyprogram#attachBaseContext>) 在 `super.attachBaseContext` 之后立即执行 `agentlobster → frogribbon → erodewire → pairdigital → rugquestion` 链，配合 [Obringrate#casegreen()](<resource-unit:#1.dex1 code:foztfoooubzwjwkapdthkpmw.zifgisscqs.gylqexbgzbysbeituofejtazcwh.Obringrate#casegreen>) 通过反射构造 `DexClassLoader`（`getConstructor` + `newInstance` + `setAccessible`），载荷取自 [assets/mUQtlh.json](<resource-unit:#1 file:assets/mUQtlh.json>)（660,116 字节，偏移 4 起为 `1f 8b` gzip 流，压缩后长度大于原始长度，说明为加密/混淆容器）。
5. **无悬浮窗通道**：权限表**不含 `SYSTEM_ALERT_WINDOW`**，因此“半透明遮罩/全屏悬浮引导”在本样本中只能以 Activity/Dialog 形式实现；同时声明了 `Theme.Translucent.NoTitleBar` 与多个 `label=""` / `Theme.NoDisplay` / `excludeFromRecents` Activity，具备“无痕透明页 + 空白标题”隐藏页面名的能力。
6. **引导文案 100% 静态不可见**：`res/values` 下无 `strings.xml`，Activity 的 `android:label` 全部指向 `label_barely`、`label_vacuum` 等字符串资源（包内未解码出对应值），故除两条土耳其语 label 外**没有任何可引用的界面原文**；`assets/*.html` 经核验全部为 Twitter MoPub/UnityAds 广告 SDK 资源（`apn_omsdk.js`、`apn_vastvideo.html`、`lpc/LivePersonaCardStrings.*`），`AppInfos.xml` 为 MoPub 应用启动器清单，`sourcePath.txt` 内容为 `\appwarmup\android\trigger\src`——**均为第三方 SDK 自带，与本应用无障碍引导无关**。

**判定**：`static_visibility = packed_or_encrypted`。引导弹窗/说明页/跳转 `ACTION_ACCESSIBILITY_SETTINGS` 的代码全部位于加密二阶段 dex，静态仅能给出 Manifest 级与壳级证据；运行期 UTG 应在“冷启动后首帧/透明页弹出”与“跳系统无障碍列表”两个瞬间抓取。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "无障碍服务类 hirmriumcrggxxcgwjox.jsainzbmudc.qia.xjnebkglqnohbb、Launcher Activity tjhrxdtsttubyve 及全部引导 UI 类均不在 classes.dex 中（对 21 个 qia.* 类名做全文/定义/结构查询全部 no_matches），仅存在于 assets/mUQtlh.json（660KB，gzip 1f8b 加密容器），由 Aunhappyprogram.attachBaseContext 经 Obringrate.casegreen 反射构造 DexClassLoader 解密加载。res/values 无 strings.xml，除两条土耳其语 label 外无任何界面原文；assets 下 HTML 均为 MoPub/UnityAds SDK 自带资源，与本应用引导无关。因此纯 UTG 视角的弹窗文案、取消按钮、拒绝后重跳逻辑均无法静态还原。",
  "summary_one_liner": "伪装成土耳其语“Player 系统更新”的 Cerberus 系银行木马，冷启动即由 Application 解密加载二阶段 dex，再以无 description、仅显示为“Player Güncellemesi”的静默无障碍服务诱导用户开启全局读屏权限，全部引导文案藏在加密载荷内。",
  "disguise_identity": {
    "app_display_name": "Player Sistem Güncelleme",
    "claimed_brand_or_persona": "泛化的“Player 播放器系统更新/升级包”（无真实品牌主体，包名为随机乱码串，不指向任何已知厂商）",
    "a11y_service_label": "Player Güncellemesi",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 桌面名与无障碍服务名仅差一个词（Sistem Güncelleme vs Güncellemesi），规避同名/同串检测；2) 无障碍服务完全不声明 android:description，系统列表中无任何用途说明；3) 大量 Activity 使用 android:label=\"\" 与 Theme.NoDisplay / Translucent.NoTitleBar / excludeFromRecents，页面名空白且不进入最近任务；4) 其余 Activity 的 label 指向 label_barely/label_vacuum 等字符串资源，包内未解码出 strings.xml，运行时呈空或占位；5) 类名/包名全量随机词拼接混淆（qia、hgztointzudgq 等），并伴随大量无意义算术指令与字符混淆常量；6) 二阶段 dex 以 gzip+加密容器 assets/mUQtlh.json 形式落地，用反射 DexClassLoader 加载，规避静态特征；7) 未声明 isAccessibilityTool，依赖 targetSdk 29 在低版本系统上规避 Android 11+ 的无障碍权限警告。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "Application foztfoooubzwjwkapdthkpmw.zifgisscqs.gylqexbgzbysbeituofejtazcwh.Aunhappyprogram → 反射 DexClassLoader 加载 assets/mUQtlh.json",
      "trigger_event": "进程启动 attachBaseContext() 回调（早于任何 Activity onCreate）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "此阶段无界面，仅完成二阶段 dex 解密与类加载",
      "user_action_requested": "无需用户操作",
      "code_anchor": "foztfoooubzwjwkapdthkpmw.zifgisscqs.gylqexbgzbysbeituofejtazcwh.Aunhappyprogram#attachBaseContext / Obringrate#casegreen"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "Launcher Activity hirmriumcrggxxcgwjox.jsainzbmudc.qia.tjhrxdtsttubyve（MAIN + LAUNCHER + android.app.role.SMS），运行于解密后的二阶段 dex",
      "trigger_event": "用户点击桌面图标「Player Sistem Güncelleme」",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Player Sistem Güncelleme",
      "shown_text_zh": "桌面图标名称：Player 系统更新",
      "user_action_requested": "点击图标启动（唯一可见入口，无其他正常业务入口）",
      "code_anchor": "AndroidManifest.xml activity android:name=\"hirmriumcrggxxcgwjox.jsainzbmudc.qia.tjhrxdtsttubyve\""
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "二阶段 dex 内的引导 Activity / Dialog（类名与文案均被加密，静态不可见）",
      "trigger_event": "不可静态还原（推测为 Launcher Activity onCreate/onResume 或首次运行标记判定后触发）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（文案在加密载荷内，需运行期 UTG 抓取）",
      "user_action_requested": "不可静态还原",
      "code_anchor": "二阶段 assets/mUQtlh.json 解密后 dex（静态不可达）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS，落点为服务项「Player Güncellemesi」",
      "trigger_event": "不可静态还原（Intent 构造代码位于二阶段 dex）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Player Güncellemesi",
      "shown_text_zh": "系统无障碍服务列表中显示的服务名：Player 更新",
      "user_action_requested": "用户在系统无障碍列表中手动开启该服务（无 description，系统列表内不展示任何用途说明）",
      "code_anchor": "AndroidManifest.xml service hirmriumcrggxxcgwjox.jsainzbmudc.qia.xjnebkglqnohbb + res/xml/dcbyuo.xml"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 hirmriumcrggxxcgwjox.jsainzbmudc.qia.xjnebkglqnohbb#onServiceConnected / onAccessibilityEvent",
      "trigger_event": "用户在系统设置中启用服务后系统绑定回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后无提示，静默读取窗口内容与控件 ID",
      "user_action_requested": "无需操作；服务按 typeWindowContentChanged|typeWindowStateChanged 持续抓取前台界面",
      "code_anchor": "res/xml/dcbyuo.xml（canRetrieveWindowContent=true, flagReportViewIds）"
    }
  ],
  "text_presentation_locations": [
    "桌面启动器图标名称：application@android:label = \"Player Sistem Güncelleme\"（AndroidManifest.xml application 节点）",
    "系统无障碍服务列表条目：service@android:label = \"Player Güncellemesi\"（AndroidManifest.xml service 节点）；该服务无 android:description，故系统列表内除服务名外不呈现任何用途说明",
    "多个 Activity 标题为空字符串 android:label=\"\"（如 nlnoqordql、wfhxquzg、kpdfpah），配合 Theme.NoDisplay / Translucent.NoTitleBar / excludeFromRecents，页面无标题且不进最近任务",
    "其余 Activity 的 label 指向 label_barely、label_vacuum、label_position 等字符串资源，包内 res/values 未解码出 strings.xml，运行时呈空或占位符",
    "assets/*.html 与 assets/lpc/*.json 经核验为 MoPub/UnityAds 广告 SDK 自带资源（apn_vastvideo.html、LivePersonaCardStrings.*），不承载本应用引导文案",
    "真正面向用户的引导弹窗/说明页/跳转按钮文案：全部位于加密二阶段 dex（assets/mUQtlh.json），静态不可见，须运行期 UTG/截图捕获"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Player Sistem Güncelleme",
      "text_zh": "Player 系统更新",
      "source_location": "AndroidManifest.xml <application android:label>",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "tr",
      "text_verbatim": "Player Güncellemesi",
      "text_zh": "Player 更新",
      "source_location": "AndroidManifest.xml <service android:name=\"...xjnebkglqnohbb\" android:label>",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "tr",
      "text_verbatim": "wjjvubqd",
      "text_zh": "（无意义随机串，非可读文案）",
      "source_location": "AndroidManifest.xml 通知监听 service android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：引导与重跳逻辑位于加密二阶段 dex（assets/mUQtlh.json），无任何静态可见的 onResume 重跳或定时器代码；从样本性质（Cerberus 系银行木马、targetSdk 29、仅一个 Launcher 入口且无真实业务界面）判断极可能为获权前阻断式循环，但须 UTG 抓取确认",
    "overlay_or_fake_settings": "无悬浮窗通道：权限清单不含 SYSTEM_ALERT_WINDOW，无法叠放半透明遮罩或全屏悬浮窗；但声明了 Theme.Translucent.NoTitleBar 与多个 Theme.NoDisplay + excludeFromRecents 的空白标题 Activity，具备以透明 Activity 模拟“设置引导层”的能力（具体实现不可静态还原）",
    "restricted_settings_13plus_coaching": "无：targetSdkVersion=29，不触发 Android 13+ 的受限设置（Restricted Settings）流程；包内无任何应用详情页/右上角菜单相关引导文本",
    "post_grant_anti_removal": "不可静态还原：静态未发现 GLOBAL_ACTION_BACK/HOME 或自点确认代码（相关实现只可能在二阶段 dex）；但样本另行申请 DEVICE_ADMIN 广播接收器（BIND_DEVICE_ADMIN + res/xml/whhhlxfkse）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，构成独立于无障碍的防卸载/保活能力",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以“监测到 Activity 跳转 android.settings.ACCESSIBILITY_SETTINGS（或系统无障碍设置包 com.android.settings/.Settings$AccessibilitySettings）”为第一触发点；同时以“冷启动首帧出现非 Launcher 的第二个 Activity/Dialog（尤其 Theme.Translucent 透明页）”为第二触发点，因本样本 Launcher 本身运行在解密后的二阶段 dex，弹窗可能在首帧即出现",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后首个引导页（透明/空白标题 Activity 或 Dialog）",
        "page_identifier": "Activity hirmriumcrggxxcgwjox.jsainzbmudc.qia.tjhrxdtsttubyve 之后新压栈的非系统 Activity；标题为空、可能背景透明、不出现在最近任务",
        "why_most_useful": "这是全包唯一静态不可见的关键节点：本样本除广告 SDK 外无任何本地文案资源，所有诱导措辞只存在于该页，UTG 提取的文本即为判定“假更新/恐吓/教唆忽视警告”的唯一直接证据",
        "observable_utg_signals": [
          "页面上出现的土耳其语/英语诱导文案（如 güncelleme、erişilebilirlik、izin、etkinleştir）",
          "是否存在“开启/İzin Ver”主按钮而缺少“取消/İptal/跳过”次级按钮",
          "页面是否为空白标题 + 半透明背景（Activity 名称与桌面名不一致）"
        ]
      },
      {
        "page_role": "跳转系统无障碍设置后的服务列表项",
        "page_identifier": "系统 Settings 无障碍列表中名为「Player Güncellemesi」的条目，其下方无任何 description 描述行",
        "why_most_useful": "可实证“服务名伪装 + 零说明”的最终呈现形态：条目只有名称、无用途说明，用户无法判断其真实权限范围，是最强的身份欺骗证据",
        "observable_utg_signals": [
          "服务条目文本 Player Güncellemesi",
          "条目下方 description 为空（与桌面名 Player Sistem Güncelleme 仅一词之差）",
          "系统是否弹出“此服务可读取全部内容”类警告（targetSdk 29 在 Android 10 及以下通常不弹）"
        ]
      },
      {
        "page_role": "拒绝/返回后的反馈循环页",
        "page_identifier": "用户从系统设置返回后重新出现的前台 Activity，或每 N 秒重复弹出的同一引导 Activity",
        "why_most_useful": "区分“良性降级”与“阻断式强制”：本样本无真实业务功能，若返回后立即重跳设置页，即可定性为 COERCE_REFUSAL_LOOP_RELAUNCH",
        "observable_utg_signals": [
          "返回应用后 1~3 秒内 Activity 栈是否再次跳转 ACCESSIBILITY_SETTINGS",
          "是否出现倒计时/进度条式的等待引导",
          "是否存在任何可关闭引导的按钮"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在明确盲区：无障碍服务类与全部引导 UI 位于加密二阶段 dex（assets/mUQtlh.json，gzip+加密容器，660KB），静态零可见，只能靠运行期 UTG/截图补齐文案与拒绝循环逻辑；另 res/values 缺 strings.xml，Activity label 指向的资源值缺失，静态无法判断页面标题。注意静态加壳/加密本身不阻挡运行期 UTG 捕获。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "foztfoooubzwjwkapdthkpmw.zifgisscqs.gylqexbgzbysbeituofejtazcwh.Aunhappyprogram#attachBaseContext",
    "foztfoooubzwjwkapdthkpmw.zifgisscqs.gylqexbgzbysbeituofejtazcwh.Obringrate#casegreen",
    "res/xml/dcbyuo.xml",
    "AndroidManifest.xml service hirmriumcrggxxcgwjox.jsainzbmudc.qia.xjnebkglqnohbb",
    "AndroidManifest.xml activity hirmriumcrggxxcgwjox.jsainzbmudc.qia.tjhrxdtsttubyve",
    "assets/mUQtlh.json"
  ]
}
```

说明：受本轮 14 次工具调用硬约束，未再执行 `register_evidence_graph` / `record_risk` 写入风险台账，上述结论与证据均来自已核实的 Manifest、`res/xml/dcbyuo.xml`、`Aunhappyprogram#attachBaseContext`、`Obringrate#casegreen` 与 `assets/mUQtlh.json` 文件特征；无障碍引导的文案与拒绝循环属未决项，需运行期 UTG 补齐。

</details>

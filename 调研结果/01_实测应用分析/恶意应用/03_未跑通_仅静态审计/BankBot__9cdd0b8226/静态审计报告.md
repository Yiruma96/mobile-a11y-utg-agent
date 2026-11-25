# MB_113__9cdd0b8226｜BankBot — e-Devlet Kapısı

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：185.2s

## 1. 一句话核心结论

- **核心申请方式**：冒充土耳其 e-Devlet 政务门户、以「Google Play Hizmetleri」名义注册可读取窗口内容的无障碍服务，其诱导流程整体藏于 attachBaseContext 还原的加密二阶段载荷中，静态不可见。
- **静态可见性说明**：Manifest、无障碍配置 XML、权限声明完整可见；但 Manifest 声明的全部 bag.beach.arrive.* 组件（含无障碍服务 wxbiwojccp 与 LAUNCHER Activity dqanxgzxd）在 classes.dex 中均无实现，由 Application.attachBaseContext 中 talentenhance/escapeenergy/sicksolve + ZPuZnDqSbQgFgGeZfMyWeMcKzJzDcEjIqQtUfOuHcGbLjMkTgGfHl.vibrantvictory 组成的加密二阶段装载器还原。引导文案、ACTION_ACCESSIBILITY_SETTINGS 跳转点、遮罩与拒权循环逻辑全部位于该载荷内，DEX 中不存在相关字符串与函数，静态不可还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9cdd0b8226d5612ac6ca5be00e013a67a6f1f376cbc8558332a986c5f16b51b0` |
| 包名 / 年份 | `frog.chalk.balance` / 2024 |
| 家族 / 品类 | **BankBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | e-Devlet Kapısı |
| 引导页宣称品牌/身份 | 土耳其政府电子政务门户 e-Devlet Kapısı + 系统级 Google Play Hizmetleri（Google Play 服务） |
| 系统无障碍列表服务名 | Google Play Hizmetleri |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：应用名冒用政府门户、无障碍服务名冒用系统品牌「Google Play Hizmetleri」；android:description 完全缺失以规避用户对用途的怀疑；组件类名使用 bag.beach.arrive 伪包且实现体不在包内（二阶段载荷动态注册）；Application 内大量无效算术循环作反分析填充；设备管理员 Receiver 的 android:label 置空；多个 Activity 设置 android:label="" 与 Theme.NoDisplay/excludeFromRecents 隐藏界面 |
| 无障碍服务类名 | `bag.beach.arrive.wxbiwojccp` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | Application frog.chalk.balance.UEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb（attachBaseContext → onCreate） | 进程启动即执行 attachBaseContext，super 调用前先执行 Application.class.getClassUEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb() 与载荷解密 | 不可静态还原 | 无 | 无（自动执行） | `frog.chalk.balance.UEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb.attachBaseContext / trymargin` |
| 2 | 冷启动入口 | bag.beach.arrive.dqanxgzxd（Manifest 声明的 LAUNCHER Activity，含 android.app.role.SMS 类别） | 用户点击桌面图标（android.intent.action.MAIN + LAUNCHER） | 不可静态还原 | 无 | 不可静态判定 | `#1 manifest:components（bag.beach.arrive.dqanxgzxd）` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS，列表项显示「Google Play Hizmetleri」 | 由二阶段载荷内的跳转逻辑触发（DEX 中无 ACCESSIBILITY_SETTINGS 字符串，调用点不可静态定位） | 系统无障碍页 | **原文**：Google Play Hizmetleri<br>**译注**：系统无障碍服务列表中显示为「Google Play 服务」，无用途说明（description 缺失） | 打开该条目开关；关闭/跳过入口由系统提供，应用侧是否附加拦截不可静态判定 | `#1 manifest:components（service bag.beach.arrive.wxbiwojccp android:label）` |
| 4 | 获权后动作 | bag.beach.arrive.wxbiwojccp（AccessibilityService，canRetrieveWindowContent=true，typeWindowContentChanged/StateChanged，flagReportViewIds） | 系统绑定服务后回调 onAccessibilityEvent（实现体在二阶段载荷中，静态不存在） | 不可静态还原 | 无 | 无 | `res/xml/zujmpglksjqznp.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项名称：AndroidManifest.xml 中 service bag.beach.arrive.wxbiwojccp 的 android:label="Google Play Hizmetleri"（唯一静态可见的引导性文案载体）
- 系统无障碍列表项说明：android:description 缺失，列表内无任何用途说明文字
- 桌面应用名：AndroidManifest.xml application android:label="e-Devlet Kapısı"
- 应用内引导弹窗 / WebView / 悬浮遮罩：未在 DEX 与 assets 中找到对应实现或土耳其语无障碍引导文案，全部位于 attachBaseContext 还原的二阶段加密载荷内，静态不可定位
- assets 内虽有 onboarding_web.html、fail.html、offline.html、imageView.html、ffdkkxckdsdindex.html 等 HTML，但均无无障碍权限引导相关内容

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | e-Devlet Kapısı | 土耳其电子政务门户（e-Devlet 门户） | `AndroidManifest.xml application@android:label` | 未知 |
| tr | Google Play Hizmetleri | Google Play 服务 | `AndroidManifest.xml service bag.beach.arrive.wxbiwojccp@android:label` | 未知 |
| xx | wlvvxhvey | 无意义随机字符串（通知监听服务标签） | `AndroidManifest.xml service bag.beach.arrive.ipniwwosfp@android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态判定：DEX 中无 ACCESSIBILITY_SETTINGS 字符串、无 onResume/Timer 重跳实现，拒权反馈循环代码位于 attachBaseContext 还原的二阶段载荷内
- **遮罩叠层 / 高仿系统设置页**：不可静态判定：DEX 中无悬浮窗相关应用自身实现（WindowManager.addView / SYSTEM_ALERT_WINDOW 权限均未声明），遮罩或高仿设置页若存在则来自二阶段载荷
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=29，低于 Android 13 受限设置机制，静态未见 APPLICATION_DETAILS_SETTINGS 相关字符串）
- **获权后即时行为与防撤权机制**：不可静态判定：DEX 中无 performGlobalAction/GLOBAL_ACTION_BACK 调用；但声明了 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、设备管理员 Receiver（@xml/sfmztp）与 FOREGROUND_SERVICE，具备反移除基础能力，具体逻辑在二阶段载荷内
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动即拉起：装载在 Application.attachBaseContext 完成，引导流程可能先于首个 Activity 出现；同时在系统无障碍设置页（ACCESSIBILITY_SETTINGS）打开瞬间与从该页返回应用的 onResume 时刻重点采集，以捕获可能的叠层或重跳
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：无障碍引导全部实现位于 attachBaseContext 还原的加密二阶段载荷，静态零可见；若引导界面以纯图片（assets 内含 andorid-en_1.jpg / andorid-chs_1.jpg 等图片资源）或远端下发 HTML 呈现，UTG 文本提取会失效，需 OCR 与网络流量旁证。此外 assets 内 UOXMi.json（425KB）等大体积二进制/JSON 资产亦可能为后续指令源。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首个界面（LAUNCHER Activity 或二阶段载荷拉起的引导弹窗）** | bag.beach.arrive.dqanxgzxd 或透明主题全屏 Dialog（application theme 为 Theme.Translucent.NoTitleBar） | 该页承载全部引导文案，是判定诱导话术与是否有取消/跳过按钮的唯一来源，静态完全缺失 | 无障碍用途说明与「必须开启才能使用」类强制话术；是否存在取消/跳过/稍后按钮；是否出现 e-Devlet 或 Google Play 品牌图标与文案 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务，条目名「Google Play Hizmetleri」 | 直接确认服务名冒用系统品牌且无 description，是身份不一致的铁证 | 条目文本 Google Play Hizmetleri；条目下方用途说明为空；开关状态（是否已开启） |
| **跳设置后返回/叠层页** | 从设置页返回后重新出现的 Activity 或悬浮遮罩 | 区分良性降级与拒权死循环重跳，是判定强制性的关键 | 返回后是否立即重新弹出同一引导页；是否叠放半透明遮罩覆盖无障碍开关位置；引导文案是否变化（升级为恐吓或故障提示） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `frog.chalk.balance.UEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb.attachBaseContext`
- `frog.chalk.balance.UEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb.trymargin`
- `frog.chalk.balance.ZPuZnDqSbQgFgGeZfMyWeMcKzJzDcEjIqQtUfOuHcGbLjMkTgGfHl.vibrantvictory`
- `res/xml/zujmpglksjqznp.xml`
- `AndroidManifest.xml (service bag.beach.arrive.wxbiwojccp / activity bag.beach.arrive.dqanxgzxd)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

- **身份伪装**：`android:label="e-Devlet Kapısı"`（土耳其电子政务门户），包名 `frog.chalk.balance`，无开发者/机构信息；无障碍服务却以 `android:label="Google Play Hizmetleri"`（Google Play 服务）注册，形成双重品牌冒用。
- **无障碍能力配置**：[res/xml/zujmpglksjqznp.xml](<resource-unit:#1 file:res/xml/zujmpglksjqznp.xml>) 开启 `canRetrieveWindowContent="true"` + `flagReportViewIds` + `typeWindowContentChanged/StateChanged`，即具备读取任意前台界面文本与控件 ID 的完整能力；`android:description` 缺失，系统列表中无任何用途说明。
- **关键发现：服务实现不在包内**。Manifest 声明的 `bag.beach.arrive.*` 全部组件（含无障碍服务 `wxbiwojccp`、启动 Activity `dqanxgzxd`）在 classes.dex 类表中**完全不存在**；反编译仅见 `com`/`frog`/`inspire`/`deputy`/`waste` 包。
- **二阶段加密装载**：[UEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb.attachBaseContext()](<resource-unit:#1.dex1 code:frog.chalk.balance.UEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb#attachBaseContext>) 在 `super.attachBaseContext` 之前执行 `Application.class.getClassUEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb()`，经 `talentenhance/escapeenergy/sicksolve` 解密资产后由 [trymargin()](<resource-unit:#1.dex1 code:frog.chalk.balance.UEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb#trymargin>) 调用 [vibrantvictory()](<resource-unit:#1.dex1 code:frog.chalk.balance.ZPuZnDqSbQgFgGeZfMyWeMcKzJzDcEjIqQtUfOuHcGbLjMkTgGfHl#vibrantvictory>) 装载还原，`onCreate` 中大量无意义算术循环为反分析填充。静态加壳初判 `False` 属误判——属**运行时载荷还原**而非传统壳。
- **纯 UTG 页面流转不可静态还原**：DEX 内无 `ACCESSIBILITY_SETTINGS`/`APPLICATION_DETAILS_SETTINGS` 字符串、无 `onAccessibilityEvent`/`performGlobalAction` 定义、无土耳其语引导文案，跳转点与引导弹窗均在还原后的二阶段载荷中。
- **配套高敏权限**：SMS 读写/发送、通讯录、录音、拨号、忽略电池优化、通知监听、设备管理员 Receiver（`@xml/sfmztp`）、开机自启——典型银行木马能力面。

**UTG 采集建议**：冷启动即拉起（装载在 `attachBaseContext` 完成），优先捕获系统无障碍列表中 `Google Play Hizmetleri` 条目页与任何跳转设置页后的叠层。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、无障碍配置 XML、权限声明完整可见；但 Manifest 声明的全部 bag.beach.arrive.* 组件（含无障碍服务 wxbiwojccp 与 LAUNCHER Activity dqanxgzxd）在 classes.dex 中均无实现，由 Application.attachBaseContext 中 talentenhance/escapeenergy/sicksolve + ZPuZnDqSbQgFgGeZfMyWeMcKzJzDcEjIqQtUfOuHcGbLjMkTgGfHl.vibrantvictory 组成的加密二阶段装载器还原。引导文案、ACTION_ACCESSIBILITY_SETTINGS 跳转点、遮罩与拒权循环逻辑全部位于该载荷内，DEX 中不存在相关字符串与函数，静态不可还原。",
  "summary_one_liner": "冒充土耳其 e-Devlet 政务门户、以「Google Play Hizmetleri」名义注册可读取窗口内容的无障碍服务，其诱导流程整体藏于 attachBaseContext 还原的加密二阶段载荷中，静态不可见。",
  "disguise_identity": {
    "app_display_name": "e-Devlet Kapısı",
    "claimed_brand_or_persona": "土耳其政府电子政务门户 e-Devlet Kapısı + 系统级 Google Play Hizmetleri（Google Play 服务）",
    "a11y_service_label": "Google Play Hizmetleri",
    "identity_mismatch": true,
    "obfuscation_tricks": "应用名冒用政府门户、无障碍服务名冒用系统品牌「Google Play Hizmetleri」；android:description 完全缺失以规避用户对用途的怀疑；组件类名使用 bag.beach.arrive 伪包且实现体不在包内（二阶段载荷动态注册）；Application 内大量无效算术循环作反分析填充；设备管理员 Receiver 的 android:label 置空；多个 Activity 设置 android:label=\"\" 与 Theme.NoDisplay/excludeFromRecents 隐藏界面"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "Application frog.chalk.balance.UEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb（attachBaseContext → onCreate）",
      "trigger_event": "进程启动即执行 attachBaseContext，super 调用前先执行 Application.class.getClassUEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb() 与载荷解密",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该阶段无界面，仅完成加密二阶段载荷的解密与装载",
      "user_action_requested": "无（自动执行）",
      "code_anchor": "frog.chalk.balance.UEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb.attachBaseContext / trymargin"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "bag.beach.arrive.dqanxgzxd（Manifest 声明的 LAUNCHER Activity，含 android.app.role.SMS 类别）",
      "trigger_event": "用户点击桌面图标（android.intent.action.MAIN + LAUNCHER）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "启动页实现类不在 DEX 中，无法静态获取界面内容",
      "user_action_requested": "不可静态判定",
      "code_anchor": "#1 manifest:components（bag.beach.arrive.dqanxgzxd）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS，列表项显示「Google Play Hizmetleri」",
      "trigger_event": "由二阶段载荷内的跳转逻辑触发（DEX 中无 ACCESSIBILITY_SETTINGS 字符串，调用点不可静态定位）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Play Hizmetleri",
      "shown_text_zh": "系统无障碍服务列表中显示为「Google Play 服务」，无用途说明（description 缺失）",
      "user_action_requested": "打开该条目开关；关闭/跳过入口由系统提供，应用侧是否附加拦截不可静态判定",
      "code_anchor": "#1 manifest:components（service bag.beach.arrive.wxbiwojccp android:label）"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "bag.beach.arrive.wxbiwojccp（AccessibilityService，canRetrieveWindowContent=true，typeWindowContentChanged/StateChanged，flagReportViewIds）",
      "trigger_event": "系统绑定服务后回调 onAccessibilityEvent（实现体在二阶段载荷中，静态不存在）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后读取前台窗口文本与控件 ID，具体窃取/覆盖行为不可静态还原",
      "user_action_requested": "无",
      "code_anchor": "res/xml/zujmpglksjqznp.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项名称：AndroidManifest.xml 中 service bag.beach.arrive.wxbiwojccp 的 android:label=\"Google Play Hizmetleri\"（唯一静态可见的引导性文案载体）",
    "系统无障碍列表项说明：android:description 缺失，列表内无任何用途说明文字",
    "桌面应用名：AndroidManifest.xml application android:label=\"e-Devlet Kapısı\"",
    "应用内引导弹窗 / WebView / 悬浮遮罩：未在 DEX 与 assets 中找到对应实现或土耳其语无障碍引导文案，全部位于 attachBaseContext 还原的二阶段加密载荷内，静态不可定位",
    "assets 内虽有 onboarding_web.html、fail.html、offline.html、imageView.html、ffdkkxckdsdindex.html 等 HTML，但均无无障碍权限引导相关内容"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "e-Devlet Kapısı",
      "text_zh": "土耳其电子政务门户（e-Devlet 门户）",
      "source_location": "AndroidManifest.xml application@android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "tr",
      "text_verbatim": "Google Play Hizmetleri",
      "text_zh": "Google Play 服务",
      "source_location": "AndroidManifest.xml service bag.beach.arrive.wxbiwojccp@android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "xx",
      "text_verbatim": "wlvvxhvey",
      "text_zh": "无意义随机字符串（通知监听服务标签）",
      "source_location": "AndroidManifest.xml service bag.beach.arrive.ipniwwosfp@android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态判定：DEX 中无 ACCESSIBILITY_SETTINGS 字符串、无 onResume/Timer 重跳实现，拒权反馈循环代码位于 attachBaseContext 还原的二阶段载荷内",
    "overlay_or_fake_settings": "不可静态判定：DEX 中无悬浮窗相关应用自身实现（WindowManager.addView / SYSTEM_ALERT_WINDOW 权限均未声明），遮罩或高仿设置页若存在则来自二阶段载荷",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=29，低于 Android 13 受限设置机制，静态未见 APPLICATION_DETAILS_SETTINGS 相关字符串）",
    "post_grant_anti_removal": "不可静态判定：DEX 中无 performGlobalAction/GLOBAL_ACTION_BACK 调用；但声明了 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、设备管理员 Receiver（@xml/sfmztp）与 FOREGROUND_SERVICE，具备反移除基础能力，具体逻辑在二阶段载荷内",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动即拉起：装载在 Application.attachBaseContext 完成，引导流程可能先于首个 Activity 出现；同时在系统无障碍设置页（ACCESSIBILITY_SETTINGS）打开瞬间与从该页返回应用的 onResume 时刻重点采集，以捕获可能的叠层或重跳",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首个界面（LAUNCHER Activity 或二阶段载荷拉起的引导弹窗）",
        "page_identifier": "bag.beach.arrive.dqanxgzxd 或透明主题全屏 Dialog（application theme 为 Theme.Translucent.NoTitleBar）",
        "why_most_useful": "该页承载全部引导文案，是判定诱导话术与是否有取消/跳过按钮的唯一来源，静态完全缺失",
        "observable_utg_signals": [
          "无障碍用途说明与「必须开启才能使用」类强制话术",
          "是否存在取消/跳过/稍后按钮",
          "是否出现 e-Devlet 或 Google Play 品牌图标与文案"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务，条目名「Google Play Hizmetleri」",
        "why_most_useful": "直接确认服务名冒用系统品牌且无 description，是身份不一致的铁证",
        "observable_utg_signals": [
          "条目文本 Google Play Hizmetleri",
          "条目下方用途说明为空",
          "开关状态（是否已开启）"
        ]
      },
      {
        "page_role": "跳设置后返回/叠层页",
        "page_identifier": "从设置页返回后重新出现的 Activity 或悬浮遮罩",
        "why_most_useful": "区分良性降级与拒权死循环重跳，是判定强制性的关键",
        "observable_utg_signals": [
          "返回后是否立即重新弹出同一引导页",
          "是否叠放半透明遮罩覆盖无障碍开关位置",
          "引导文案是否变化（升级为恐吓或故障提示）"
        ]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "存在显著盲区：无障碍引导全部实现位于 attachBaseContext 还原的加密二阶段载荷，静态零可见；若引导界面以纯图片（assets 内含 andorid-en_1.jpg / andorid-chs_1.jpg 等图片资源）或远端下发 HTML 呈现，UTG 文本提取会失效，需 OCR 与网络流量旁证。此外 assets 内 UOXMi.json（425KB）等大体积二进制/JSON 资产亦可能为后续指令源。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "COERCE_NO_SKIP_NON_CANCELABLE"
  ],
  "code_anchors": [
    "frog.chalk.balance.UEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb.attachBaseContext",
    "frog.chalk.balance.UEjPxPwPpFnRjCtBnUdPdJmDrLcEpIb.trymargin",
    "frog.chalk.balance.ZPuZnDqSbQgFgGeZfMyWeMcKzJzDcEjIqQtUfOuHcGbLjMkTgGfHl.vibrantvictory",
    "res/xml/zujmpglksjqznp.xml",
    "AndroidManifest.xml (service bag.beach.arrive.wxbiwojccp / activity bag.beach.arrive.dqanxgzxd)"
  ]
}
```

已登记风险 **R-001**（high / malware_trojan）：伪装「Google Play Hizmetleri」的无障碍服务由加密二阶段载荷还原。工具调用共 14 次，按约束收口。

</details>

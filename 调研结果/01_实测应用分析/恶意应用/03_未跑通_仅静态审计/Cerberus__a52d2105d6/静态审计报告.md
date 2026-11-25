# MB_067__a52d2105d6｜Cerberus — Google Update

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：100.6s

## 1. 一句话核心结论

- **核心申请方式**：以“Google Update”名义申报可读全屏文本且无任何用途说明的无障碍服务，但服务类与入口类体均不在 DEX 中，引导流程纯运行期、静态不可见。
- **静态可见性说明**：Manifest 与 res/xml 无障碍配置完整可见，但无障碍服务类 com.hmxuxgdngpi.bkqrlzkuwzuj.zWPzgfI 及 LAUNCHER 入口 OzGUhRlf 等全部 com.hmxuxgdngpi.* 组件在唯一 classes.dex 中均无对应类（APKiD 未检出加壳）；全包检索无 ACTION_ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / AccessibilityService 及任何引导文案或 HTML 资源，引导页面流转与拒绝反馈逻辑静态不可还原，推测由运行期/远端提供。
- **命中的行为模式标签**：`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a52d2105d680d029f9cc5c9c77f639e47ae520e41ce7294bbad77b8f2931796a` |
| 包名 / 年份 | `com.hmxuxgdngpi.bkqrlzkuwzuj` / 2025 |
| 家族 / 品类 | **Cerberus**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google Update |
| 引导页宣称品牌/身份 | Google Update（冒充 Google 系统更新） |
| 系统无障碍列表服务名 | Google Update |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名与类名随机化（com.hmxuxgdngpi.bkqrlzkuwzuj / zWPzgfI），实际代码包为 com.tsrdeaem.stcbmi 与 com.ridjujclcyrc.ridjujclcyrc；无障碍服务未设置 android:description 与 settingsActivity，系统列表中无可读说明；声明类体缺失，实现与清单脱钩 |
| 无障碍服务类名 | `com.hmxuxgdngpi.bkqrlzkuwzuj.zWPzgfI` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.hmxuxgdngpi.bkqrlzkuwzuj.OzGUhRlf（MAIN/LAUNCHER，附带 android.app.role.SMS） | 用户点击桌面图标（ACTION_MAIN + LAUNCHER），另有多入口 activity 如 krizifujrzi、ecovmewcxvmd、oPiZdfH(NoDisplay) | 不可静态还原 | 无 | 不可静态还原 | `com.hmxuxgdngpi.bkqrlzkuwzuj.OzGUhRlf（Manifest 声明，DEX 中无类体）` |
| 2 | 跳无障碍设置 | com.hmxuxgdngpi.bkqrlzkuwzuj.zWPzgfI（无障碍服务，label=Google Update） | 不可静态还原；全包无 ACTION_ACCESSIBILITY_SETTINGS 跳转点 | 系统无障碍页 | **原文**：Google Update<br>**译注**：系统无障碍服务列表中显示为“Google Update”，无功能说明描述 | 不可静态还原（需用户在系统列表中手动开启该服务开关） | `#1 manifest:components / res/xml/lhwubrqbaic.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：service android:label="Google Update"，无 android:description 说明文字
- 桌面应用图标名：application android:label="Google Update"
- res/xml/lhwubrqbaic.xml 无障碍能力配置中未声明 description/summary，故无系统级说明页
- 未发现本地 HTML/WebView 引导资产、strings 引导文案、原生 Dialog 文案或悬浮窗布局（res/ 下无 accessib 相关字符串）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Google Update | Google 更新 | `AndroidManifest.xml: application@android:label 与 service(zWPzgfI)@android:label` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：包内无无障碍设置跳转与 onResume 重跳逻辑的可见代码
- **遮罩叠层 / 高仿系统设置页**：不可静态还原：未发现 SYSTEM_ALERT_WINDOW 权限、悬浮窗布局或高仿设置页资源
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=27，且无应用详情/受限设置相关跳转字符串）
- **获权后即时行为与防撤权机制**：不可静态还原：未发现 GLOBAL_ACTION_BACK/HOME 相关调用（AccessibilityService 相关符号在 DEX 中不存在）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动点击 LAUNCHER 后立即开始 UTG；并在监测到当前焦点为 com.android.settings 且 accessibility 相关页面（/accessibility 或 /accessibility_settings）时锁定截取，因静态无跳转点，必须以运行期页面栈为准
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：无障碍服务类、LAUNCHER 入口等所有清单组件的类体均不在唯一 DEX 中，静态无法看到任何引导文案、跳转与拒绝循环逻辑，纯静态判定会漏掉全部运行期引导行为；需以 UTG 页面栈+截图作为唯一可靠判据。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首个界面** | packageName=com.hmxuxgdngpi.bkqrlzkuwzuj 的首个 Activity（预期 OzGUhRlf 或 krizifujrzi/ecovmewcxvmd） | 静态无任何引导文案，首个界面的真实形态（原生/WebView/无界面直跳）只能运行期确定 | 首屏是否立即无交互跳转；是否存在无法取消的弹窗/无按钮遮罩；是否出现 WebView 控件与远端 URL |
| **系统无障碍服务列表项** | com.android.settings accessibility 页面中的“Google Update”条目 | 确认该服务是否真正注册成功并暴露在列表、以及是否有说明文字缺失造成的辨识困难 | 条目名 Google Update；无 description 文本；开关状态变化 |
| **跳转设置后返回的反馈页** | 从 settings 返回后重新出现的应用界面（若存在遮罩则为悬浮窗层级） | 判断拒绝开启后是否形成重跳循环或遮罩压栈 | 返回后是否立刻再次拉起 settings；是否出现悬浮窗/遮罩层级；页面重复出现次数与时间间隔 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `AndroidManifest.xml: service com.hmxuxgdngpi.bkqrlzkuwzuj.zWPzgfI (android:label="Google Update", BIND_ACCESSIBILITY_SERVICE)`
- `AndroidManifest.xml: application android:label="Google Update"`
- `res/xml/lhwubrqbaic.xml (canRetrieveWindowContent=true, flagIncludeNotImportantViews, 无 android:description)`
- `AndroidManifest.xml: activity com.hmxuxgdngpi.bkqrlzkuwzuj.OzGUhRlf (MAIN/LAUNCHER，DEX 中无类体)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向静态核验）

**核心事实：无障碍服务的声明齐全，但实现类整体缺失，因此引导页面流转无法静态还原。**

- **Manifest 声明**：`service android:name="com.hmxuxgdngpi.bkqrlzkuwzuj.zWPzgfI"`，`android:label="Google Update"`，绑定 `BIND_ACCESSIBILITY_SERVICE`，action 为 `android.accessibilityservice.AccessibilityService`；应用 `application@android:label` 同为 `Google Update`。
- **能力配置**：[res/xml/lhwubrqbaic.xml](<resource-unit:#1 file:res/xml/lhwubrqbaic.xml#L2-L3>) 只设置了 `typeWindowContentChanged|typeWindowStateChanged`、`flagIncludeNotImportantViews|flagReportViewIds`、`canRetrieveWindowContent="true"`；**没有 `android:description`，也没有 `android:settingsActivity`**，所以系统无障碍列表项不会提供任何用途说明，也没有二级说明页入口。
- **类体缺失**：唯一 `classes.dex`（APKiD：`dexlib 2.x`，未检出加壳/混淆壳）中，`com.hmxuxgdngpi.*` 全部组件（含无障碍服务 `zWPzgfI`、LAUNCHER 入口 `OzGUhRlf`、通知监听 `lMRsnYoHNo`、设备管理器 receiver）**都没有对应类**；`list_codebase` 只列出 `com.tsrdeaem.stcbmi`（417 类）与 `com.ridjujclcyrc`（7 类）。
- **跳转点缺失**：全量文本检索 `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`AccessibilityService`、`performGlobalAction`、`getRootInActiveWindow`、`hmxuxgdngpi`、`lhwubrqbaic` **均无命中**；`res/` 下也无任何与 `accessib` 相关的字符串或说明资源，没有 HTML/WebView 引导资产。
- **可确认的诱导特征**：桌面名与无障碍服务名均冒充“Google Update”（系统/品牌冒充 + 假更新外壳），并且该服务具备读取全屏文本的能力，但**没有说明文案**，属于用户无法形成知情同意的读屏服务申报；配合同包 `READ_SMS`/`SEND_SMS`/`CALL_PHONE`/`RECORD_AUDIO`/设备管理器/通知监听，形成典型 Cerberus 系银行木马的能力面。
- **不可确认部分**：冷启动弹窗、UTG 遮罩、拒绝后重跳循环、`ACTION_ACCESSIBILITY_SETTINGS` 拉起时机等**均无静态证据**；因入口类与无障碍类体不在包内静态可见代码中，这些行为只能靠运行期 UTG 捕获，本次不作推测性断言。

已登记风险：R-001（high，malware_trojan，`autonomous_audit`）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest 与 res/xml 无障碍配置完整可见，但无障碍服务类 com.hmxuxgdngpi.bkqrlzkuwzuj.zWPzgfI 及 LAUNCHER 入口 OzGUhRlf 等全部 com.hmxuxgdngpi.* 组件在唯一 classes.dex 中均无对应类（APKiD 未检出加壳）；全包检索无 ACTION_ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / AccessibilityService 及任何引导文案或 HTML 资源，引导页面流转与拒绝反馈逻辑静态不可还原，推测由运行期/远端提供。",
  "summary_one_liner": "以“Google Update”名义申报可读全屏文本且无任何用途说明的无障碍服务，但服务类与入口类体均不在 DEX 中，引导流程纯运行期、静态不可见。",
  "disguise_identity": {
    "app_display_name": "Google Update",
    "claimed_brand_or_persona": "Google Update（冒充 Google 系统更新）",
    "a11y_service_label": "Google Update",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名与类名随机化（com.hmxuxgdngpi.bkqrlzkuwzuj / zWPzgfI），实际代码包为 com.tsrdeaem.stcbmi 与 com.ridjujclcyrc.ridjujclcyrc；无障碍服务未设置 android:description 与 settingsActivity，系统列表中无可读说明；声明类体缺失，实现与清单脱钩"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.hmxuxgdngpi.bkqrlzkuwzuj.OzGUhRlf（MAIN/LAUNCHER，附带 android.app.role.SMS）",
      "trigger_event": "用户点击桌面图标（ACTION_MAIN + LAUNCHER），另有多入口 activity 如 krizifujrzi、ecovmewcxvmd、oPiZdfH(NoDisplay)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（入口类不在 DEX 中，界面文案无法静态提取）",
      "user_action_requested": "不可静态还原",
      "code_anchor": "com.hmxuxgdngpi.bkqrlzkuwzuj.OzGUhRlf（Manifest 声明，DEX 中无类体）"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "com.hmxuxgdngpi.bkqrlzkuwzuj.zWPzgfI（无障碍服务，label=Google Update）",
      "trigger_event": "不可静态还原；全包无 ACTION_ACCESSIBILITY_SETTINGS 跳转点",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Update",
      "shown_text_zh": "系统无障碍服务列表中显示为“Google Update”，无功能说明描述",
      "user_action_requested": "不可静态还原（需用户在系统列表中手动开启该服务开关）",
      "code_anchor": "#1 manifest:components / res/xml/lhwubrqbaic.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：service android:label=\"Google Update\"，无 android:description 说明文字",
    "桌面应用图标名：application android:label=\"Google Update\"",
    "res/xml/lhwubrqbaic.xml 无障碍能力配置中未声明 description/summary，故无系统级说明页",
    "未发现本地 HTML/WebView 引导资产、strings 引导文案、原生 Dialog 文案或悬浮窗布局（res/ 下无 accessib 相关字符串）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Google Update",
      "text_zh": "Google 更新",
      "source_location": "AndroidManifest.xml: application@android:label 与 service(zWPzgfI)@android:label",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：包内无无障碍设置跳转与 onResume 重跳逻辑的可见代码",
    "overlay_or_fake_settings": "不可静态还原：未发现 SYSTEM_ALERT_WINDOW 权限、悬浮窗布局或高仿设置页资源",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=27，且无应用详情/受限设置相关跳转字符串）",
    "post_grant_anti_removal": "不可静态还原：未发现 GLOBAL_ACTION_BACK/HOME 相关调用（AccessibilityService 相关符号在 DEX 中不存在）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动点击 LAUNCHER 后立即开始 UTG；并在监测到当前焦点为 com.android.settings 且 accessibility 相关页面（/accessibility 或 /accessibility_settings）时锁定截取，因静态无跳转点，必须以运行期页面栈为准",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首个界面",
        "page_identifier": "packageName=com.hmxuxgdngpi.bkqrlzkuwzuj 的首个 Activity（预期 OzGUhRlf 或 krizifujrzi/ecovmewcxvmd）",
        "why_most_useful": "静态无任何引导文案，首个界面的真实形态（原生/WebView/无界面直跳）只能运行期确定",
        "observable_utg_signals": ["首屏是否立即无交互跳转", "是否存在无法取消的弹窗/无按钮遮罩", "是否出现 WebView 控件与远端 URL"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings accessibility 页面中的“Google Update”条目",
        "why_most_useful": "确认该服务是否真正注册成功并暴露在列表、以及是否有说明文字缺失造成的辨识困难",
        "observable_utg_signals": ["条目名 Google Update", "无 description 文本", "开关状态变化"]
      },
      {
        "page_role": "跳转设置后返回的反馈页",
        "page_identifier": "从 settings 返回后重新出现的应用界面（若存在遮罩则为悬浮窗层级）",
        "why_most_useful": "判断拒绝开启后是否形成重跳循环或遮罩压栈",
        "observable_utg_signals": ["返回后是否立刻再次拉起 settings", "是否出现悬浮窗/遮罩层级", "页面重复出现次数与时间间隔"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：无障碍服务类、LAUNCHER 入口等所有清单组件的类体均不在唯一 DEX 中，静态无法看到任何引导文案、跳转与拒绝循环逻辑，纯静态判定会漏掉全部运行期引导行为；需以 UTG 页面栈+截图作为唯一可靠判据。"
  },
  "behavior_pattern_tags": [
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "LURE_FAKE_UPDATE_OR_INSTALL"
  ],
  "code_anchors": [
    "AndroidManifest.xml: service com.hmxuxgdngpi.bkqrlzkuwzuj.zWPzgfI (android:label=\"Google Update\", BIND_ACCESSIBILITY_SERVICE)",
    "AndroidManifest.xml: application android:label=\"Google Update\"",
    "res/xml/lhwubrqbaic.xml (canRetrieveWindowContent=true, flagIncludeNotImportantViews, 无 android:description)",
    "AndroidManifest.xml: activity com.hmxuxgdngpi.bkqrlzkuwzuj.OzGUhRlf (MAIN/LAUNCHER，DEX 中无类体)"
  ]
}
```

</details>

# MR_170__f9dc40a7dd｜Brata — GreatVault

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：169.8s

## 1. 一句话核心结论

- **核心申请方式**：保险库外观的 GreatVault 静默注册名为「协助服务」、无任何能力说明却具备全局读屏+手势注入的无障碍服务，其分步图文引导页与跳转逻辑全部封在 AppSealing 加密载荷中，需运行期 UTG 捕获。
- **静态可见性说明**：应用使用 AppSealing/WhiteCryption 加固，classes.dex 仅含 28 个 com.inka.appsealing.* 壳类；业务与全部引导逻辑封于加密资产 assets/sealed1.dex、assets/borlam、assets/eidask（头部为随机密文，strings 无任何可读标识）。在 dex1/dex2/dex3 中检索 accessibility_settings、ACTION_ACCESSIBILITY_SETTINGS、APPLICATION_DETAILS_SETTINGS、PesphoService 均无命中，故无障碍跳转代码、引导文案、拒绝后行为均静态不可见。仅 Manifest 声明、无障碍配置 xml、5 个自有布局骨架、引导插图与 strings 可确认。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `f9dc40a7dd2a875344721834e7d80bf7dbfa1bf08f29b7209deb0decad77e992` |
| 包名 / 年份 | `com.greatvault.mobile` / 2021 |
| 家族 / 品类 | **Brata**（同池样本数：8） |
| 原始来源标识 | https://www.mcafee.com/blogs/other-blogs/mcafee-labs/brata-keeps-sneaking-into-google-play-now-targeting-usa-and-spain/?hilite=%27Android%27%2C%27Malware%27 |
| 桌面显示名 | GreatVault |
| 引导页宣称品牌/身份 | GreatVault（保险库/密码管理类安全工具外观，包名 com.greatvault.mobile） |
| 系统无障碍列表服务名 | Serviço de Assistência（葡语默认）/ Assistance Service（英文） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未声明 android:description（系统列表中无任何能力说明）；服务名为中性的「协助/辅助服务」，与 GreatVault 保险库语义及实际全局读屏+手势能力均不匹配；6 个 Activity 与全部字符串资源使用无意义混淆名（Ucaphy/Heaski/Axicam/Grovea/Relitz/Abrimu、murial/tikily/wwilla、aalind/miperl/sappoo 等），布局中 TextView 无 text 属性改由运行期注入；未见空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool（加固层内无法排除） |
| 无障碍服务类名 | `com.greatvault.PesphoService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.greatvault.MainActivity（LAUNCHER，无自定义布局，推断为壳/分发页） | 用户点击桌面图标启动（onCreate） | 不可静态还原 | 无 | 不可静态还原 | `#1 manifest:components（com.greatvault.MainActivity）` |
| 2 | 引导说明页 | com.greatvault.AxicamActivity（竖屏锁定，配套 activity_verazz.xml / activity_spudid.xml 类布局） | 冷启动或功能入口跳转（onCreate/onResume 注入文案） | 原生Activity | **原文**：无（布局 TextView 均无 android:text，文案由 setText 运行期写入）<br>**译注**：整屏白底，居中显示加粗标题 + 说明文字 + 128dp 引导插图 + 单个按钮，构成单向前进的分步教学页 | 点击单个 Button 继续（布局中仅一个按钮，未见取消/跳过控件） | `#1 file:res/layout/activity_verazz.xml；#1 file:res/layout/activity_spudid.xml` |
| 3 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载/已安装的服务列表项 Serviço de Assistência | 上一步按钮点击后 startActivity(ACTION_ACCESSIBILITY_SETTINGS)（调用点位于加密载荷，静态不可见） | 系统无障碍页 | **原文**：Serviço de Assistência<br>**译注**：系统无障碍列表中显示的服务名「协助服务」，无描述文字说明其读屏与手势能力 | 在系统列表中手动找到并开启该服务开关 | `#1 file:res/values/strings.xml#L35；#1 manifest:components（PesphoService android:label）` |
| 4 | 获权后动作 | com.greatvault.PesphoService（无障碍服务，canRetrieveWindowContent + canPerformGestures） | 用户在系统设置中开启服务后系统回调 onServiceConnected | 不可静态还原 | 无 | 无需再操作；服务在后台对任意前台应用生效 | `#1 file:res/xml/pespho_service_cfg.xml；#1 manifest:components` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项名称：res/values/strings.xml#L35 的 service_name = Serviço de Assistência（英文资源为 Assistance Service）；该服务无 android:description，列表项下无任何能力说明文字
- 原生 Activity 整屏教学页：res/layout/activity_verazz.xml、activity_spudid.xml、activity_sosted.xml、activity_drimez.xml、activity_ukenae.xml，标题/说明 TextView 无 text 属性，实际文案由加密 DEX 运行期 setText() 注入，静态不可见
- 引导插图（图片即教学载体，非文字）：res/drawable-*/murial.png、wwilla.png、tikily.png 三套多密度分步教学图
- 不存在本地 HTML/WebView 教学页：assets/ 下仅有 AppSealing 加固资产（sealed1.dex、borlam、eidask、AppSealing/*），无 html 文件；亦未发现远端 WebView 的本地痕迹
- 加密资产内可能的悬浮遮罩/引导层：assets/sealed1.dex 等为密文，静态不可确认

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | Serviço de Assistência | 协助服务（辅助服务） | `res/values/strings.xml#L35 key=service_name` | 未知 |
| en | Assistance Service | 协助服务（辅助服务） | `res/values-en-rUS/strings.xml#L4 key=service_name` | 未知 |
| en | GreatVault | GreatVault（大保险库，密码/资产管理语义） | `res/values/strings.xml#L31 key=app_name` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：拒绝或从系统设置返回后的重跳逻辑位于 AppSealing 加密载荷（assets/sealed1.dex），需 UTG 监测 Activity 重启与 startActivity(ACTION_ACCESSIBILITY_SETTINGS) 频次确认是否为 onResume 死循环或定时器重拉
- **遮罩叠层 / 高仿系统设置页**：静态未发现本地悬浮窗权限声明或高仿系统开关页布局（无对应 drawable/layout 特征）；加密载荷内是否叠放半透明引导遮罩不可确认
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=29，未触及 Android 13 受限设置机制；包内亦无 ACTION_APPLICATION_DETAILS_SETTINGS 静态痕迹）
- **获权后即时行为与防撤权机制**：不可静态还原（未见本地 GLOBAL_ACTION_BACK/HOME 字符串，相关行为可能在加密载荷内）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间为最佳拉起时机；同时在应用冷启动（com.greatvault.MainActivity onCreate）后即开始逐帧抓取，防止引导页早于跳转出现
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导文案与跳转逻辑全部位于 AppSealing/WhiteCryption 加密载荷（assets/sealed1.dex、borlam、eidask），静态无法确认具体话术、是否可取消、拒绝后是否循环重跳及获权后是否阻止撤权；若加密载荷在运行期解密后仍以自定义 View 直接绘制文字（而非标准 TextView），UTG 可能取不到文本，此时需对 murial/wwilla/tikily 三套引导插图启用 OCR 兜底。静态加固本身不阻挡运行期 UTG 捕获。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页/教学页** | com.greatvault.AxicamActivity / UcaphyActivity / HeaskiActivity / GroveaActivity / RelitzActivity / AbrimuActivity，白底整屏、居中加粗标题+说明文本+128dp 插图+单按钮 | 这是唯一承载诱导话术的界面，直接决定其修辞框架（假更新/故障恐吓/安全承诺/分步教学）与是否可取消 | 标题与说明正文的完整文本；按钮数量与文案（是否存在取消/跳过）；页面栈中 Activity 类名与出现顺序；插图是否为教学分步图 |
| **跳转前引导/遮罩页** | 跳转 ACCESSIBILITY_SETTINGS 前最后停留的应用内 Activity；或跳转后 500-1500ms 出现在系统设置之上的半透明悬浮层 | 区分是原生教学页引导，还是压栈遮罩式指引（后者属高强度强制引导） | 是否存在非系统包名的顶层窗口；窗口类型是否为 TYPE_ACCESSIBILITY_OVERLAY/TYPE_APPLICATION_OVERLAY；遮罩透明度与箭头/手指指示位置 |
| **系统无障碍服务列表项** | Settings 无障碍页中 label 为 Serviço de Assistência / Assistance Service 的条目，开关初始为关闭 | 确认系统侧展示给用户的唯一信息就是「协助服务」这一中性名且无描述，构成身份淡化证据 | 列表项标题文本；条目下方描述区域是否为空；开关控件坐标与当前状态 |
| **拒权/返回后的反馈页** | 从系统设置返回后重新出现的应用内 Activity 或其重启次数 | 判定是否存在拒绝循环重跳，是区分强制诱导与良性降级的关键 | 返回后 Activity 重启时间间隔；同一 Activity 反复出现次数；是否再次出现跳转系统设置的窗口切换 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.greatvault.PesphoService（AndroidManifest.xml 声明，android:label=@string/service_name，无 android:description，priority=999）`
- `res/xml/pespho_service_cfg.xml（canRetrieveWindowContent=true、canPerformGestures=true，无 packageNames 限定）`
- `res/values/strings.xml#L31-L35（app_name=GreatVault、service_name=Serviço de Assistência）`
- `res/layout/activity_verazz.xml / activity_spudid.xml / activity_sosted.xml / activity_drimez.xml / activity_ukenae.xml（标题+说明+插图+单按钮引导骨架，TextView 无 text）`
- `com.inka.appsealing.AppSealingApplication（壳入口，com.inka.appsealing.AppSealingService/AppSealingIPService）`
- `assets/sealed1.dex / assets/borlam / assets/eidask（加密业务与引导载荷，静态不可读）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 视角）

**静态可见度：整体加固遮蔽。** 应用使用 AppSealing / WhiteCryption 加固，`classes.dex` 只有 28 个 `com.inka.appsealing.*` 壳类，业务与引导逻辑全部封在 `assets/sealed1.dex`、`assets/borlam`、`assets/eidask`（头部均为随机密文、`strings` 零可读标识）。三个 DEX 中检索 `accessibility_settings` / `ACTION_ACCESSIBILITY_SETTINGS` / `PesphoService` / `APPLICATION_DETAILS_SETTINGS` 均无命中，因此**具体跳转调用点无法静态定位**。

**仍可确认的引导骨架（资源层）：**
- 无障碍服务 [PesphoService](<resource-unit:#1 manifest:components>) 在系统列表只显示 `Serviço de Assistência` / `Assistance Service`，**`android:description` 缺失**，`priority=999`。
- 能力配置 [pespho_service_cfg.xml](<resource-unit:#1 file:res/xml/pespho_service_cfg.xml>) 仅两项：`canRetrieveWindowContent="true"` + `canPerformGestures="true"`，无包名/事件类型限定 → 全局读屏 + 全局手势注入。
- 6 个混淆 Activity 配套 5 个自有布局（[activity_spudid.xml](<resource-unit:#1 file:res/layout/activity_spudid.xml>)、[activity_verazz.xml](<resource-unit:#1 file:res/layout/activity_verazz.xml>) 等），结构统一为「加粗标题 + 说明文本 + 128dp 引导插图 + 单个 Button」，**TextView 全部无 `text` 属性** → 文案由加密 DEX 运行期 `setText()` 注入。
- 引导插图 [murial.png](<resource-unit:#1 file:res/drawable-xxhdpi/murial.png>)、`wwilla.png`、`tikily.png` 为多套分步教学图。
- 包内**无任何 HTML/WebView 资源**，`assets/` 下只有加固资产，故不存在本地 HTML 教学页；远端 WebView 亦无本地痕迹。

**引导路径推断：** 冷启动 → 保险库外观主页 → 单按钮图文教学页（标题/说明/插图）→ 跳系统无障碍列表 → 开启后 `PesphoService` 获得全屏读屏与代点击能力。该推断的每一步界面文案、是否有取消按钮、拒绝后是否循环重跳，**必须由 UTG 运行期捕获**，本次不做断言。

**身份伪装：** 显示名 `GreatVault`（保险库/密码管理语义）与"协助服务"中性名及其实质全局读屏+手势权限严重不匹配，属对系统无障碍列表的审查淡化；未发现空白/换行挤出、同形字、多 alias 或伪造 `isAccessibilityTool` 的迹象（这些需在解密后确认）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "应用使用 AppSealing/WhiteCryption 加固，classes.dex 仅含 28 个 com.inka.appsealing.* 壳类；业务与全部引导逻辑封于加密资产 assets/sealed1.dex、assets/borlam、assets/eidask（头部为随机密文，strings 无任何可读标识）。在 dex1/dex2/dex3 中检索 accessibility_settings、ACTION_ACCESSIBILITY_SETTINGS、APPLICATION_DETAILS_SETTINGS、PesphoService 均无命中，故无障碍跳转代码、引导文案、拒绝后行为均静态不可见。仅 Manifest 声明、无障碍配置 xml、5 个自有布局骨架、引导插图与 strings 可确认。",
  "summary_one_liner": "保险库外观的 GreatVault 静默注册名为「协助服务」、无任何能力说明却具备全局读屏+手势注入的无障碍服务，其分步图文引导页与跳转逻辑全部封在 AppSealing 加密载荷中，需运行期 UTG 捕获。",
  "disguise_identity": {
    "app_display_name": "GreatVault",
    "claimed_brand_or_persona": "GreatVault（保险库/密码管理类安全工具外观，包名 com.greatvault.mobile）",
    "a11y_service_label": "Serviço de Assistência（葡语默认）/ Assistance Service（英文）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未声明 android:description（系统列表中无任何能力说明）；服务名为中性的「协助/辅助服务」，与 GreatVault 保险库语义及实际全局读屏+手势能力均不匹配；6 个 Activity 与全部字符串资源使用无意义混淆名（Ucaphy/Heaski/Axicam/Grovea/Relitz/Abrimu、murial/tikily/wwilla、aalind/miperl/sappoo 等），布局中 TextView 无 text 属性改由运行期注入；未见空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool（加固层内无法排除）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.greatvault.MainActivity（LAUNCHER，无自定义布局，推断为壳/分发页）",
      "trigger_event": "用户点击桌面图标启动（onCreate）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "启动入口界面，文案由加密 DEX 运行期注入，静态不可见",
      "user_action_requested": "不可静态还原",
      "code_anchor": "#1 manifest:components（com.greatvault.MainActivity）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.greatvault.AxicamActivity（竖屏锁定，配套 activity_verazz.xml / activity_spudid.xml 类布局）",
      "trigger_event": "冷启动或功能入口跳转（onCreate/onResume 注入文案）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（布局 TextView 均无 android:text，文案由 setText 运行期写入）",
      "shown_text_zh": "整屏白底，居中显示加粗标题 + 说明文字 + 128dp 引导插图 + 单个按钮，构成单向前进的分步教学页",
      "user_action_requested": "点击单个 Button 继续（布局中仅一个按钮，未见取消/跳过控件）",
      "code_anchor": "#1 file:res/layout/activity_verazz.xml；#1 file:res/layout/activity_spudid.xml"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载/已安装的服务列表项 Serviço de Assistência",
      "trigger_event": "上一步按钮点击后 startActivity(ACTION_ACCESSIBILITY_SETTINGS)（调用点位于加密载荷，静态不可见）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Serviço de Assistência",
      "shown_text_zh": "系统无障碍列表中显示的服务名「协助服务」，无描述文字说明其读屏与手势能力",
      "user_action_requested": "在系统列表中手动找到并开启该服务开关",
      "code_anchor": "#1 file:res/values/strings.xml#L35；#1 manifest:components（PesphoService android:label）"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.greatvault.PesphoService（无障碍服务，canRetrieveWindowContent + canPerformGestures）",
      "trigger_event": "用户在系统设置中开启服务后系统回调 onServiceConnected",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务获得全局界面内容读取与模拟手势能力，后续自动化行为位于加密载荷",
      "user_action_requested": "无需再操作；服务在后台对任意前台应用生效",
      "code_anchor": "#1 file:res/xml/pespho_service_cfg.xml；#1 manifest:components"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项名称：res/values/strings.xml#L35 的 service_name = Serviço de Assistência（英文资源为 Assistance Service）；该服务无 android:description，列表项下无任何能力说明文字",
    "原生 Activity 整屏教学页：res/layout/activity_verazz.xml、activity_spudid.xml、activity_sosted.xml、activity_drimez.xml、activity_ukenae.xml，标题/说明 TextView 无 text 属性，实际文案由加密 DEX 运行期 setText() 注入，静态不可见",
    "引导插图（图片即教学载体，非文字）：res/drawable-*/murial.png、wwilla.png、tikily.png 三套多密度分步教学图",
    "不存在本地 HTML/WebView 教学页：assets/ 下仅有 AppSealing 加固资产（sealed1.dex、borlam、eidask、AppSealing/*），无 html 文件；亦未发现远端 WebView 的本地痕迹",
    "加密资产内可能的悬浮遮罩/引导层：assets/sealed1.dex 等为密文，静态不可确认"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "Serviço de Assistência",
      "text_zh": "协助服务（辅助服务）",
      "source_location": "res/values/strings.xml#L35 key=service_name",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Assistance Service",
      "text_zh": "协助服务（辅助服务）",
      "source_location": "res/values-en-rUS/strings.xml#L4 key=service_name",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "GreatVault",
      "text_zh": "GreatVault（大保险库，密码/资产管理语义）",
      "source_location": "res/values/strings.xml#L31 key=app_name",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：拒绝或从系统设置返回后的重跳逻辑位于 AppSealing 加密载荷（assets/sealed1.dex），需 UTG 监测 Activity 重启与 startActivity(ACTION_ACCESSIBILITY_SETTINGS) 频次确认是否为 onResume 死循环或定时器重拉",
    "overlay_or_fake_settings": "静态未发现本地悬浮窗权限声明或高仿系统开关页布局（无对应 drawable/layout 特征）；加密载荷内是否叠放半透明引导遮罩不可确认",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=29，未触及 Android 13 受限设置机制；包内亦无 ACTION_APPLICATION_DETAILS_SETTINGS 静态痕迹）",
    "post_grant_anti_removal": "不可静态还原（未见本地 GLOBAL_ACTION_BACK/HOME 字符串，相关行为可能在加密载荷内）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间为最佳拉起时机；同时在应用冷启动（com.greatvault.MainActivity onCreate）后即开始逐帧抓取，防止引导页早于跳转出现",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页/教学页",
        "page_identifier": "com.greatvault.AxicamActivity / UcaphyActivity / HeaskiActivity / GroveaActivity / RelitzActivity / AbrimuActivity，白底整屏、居中加粗标题+说明文本+128dp 插图+单按钮",
        "why_most_useful": "这是唯一承载诱导话术的界面，直接决定其修辞框架（假更新/故障恐吓/安全承诺/分步教学）与是否可取消",
        "observable_utg_signals": ["标题与说明正文的完整文本", "按钮数量与文案（是否存在取消/跳过）", "页面栈中 Activity 类名与出现顺序", "插图是否为教学分步图"]
      },
      {
        "page_role": "跳转前引导/遮罩页",
        "page_identifier": "跳转 ACCESSIBILITY_SETTINGS 前最后停留的应用内 Activity；或跳转后 500-1500ms 出现在系统设置之上的半透明悬浮层",
        "why_most_useful": "区分是原生教学页引导，还是压栈遮罩式指引（后者属高强度强制引导）",
        "observable_utg_signals": ["是否存在非系统包名的顶层窗口", "窗口类型是否为 TYPE_ACCESSIBILITY_OVERLAY/TYPE_APPLICATION_OVERLAY", "遮罩透明度与箭头/手指指示位置"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中 label 为 Serviço de Assistência / Assistance Service 的条目，开关初始为关闭",
        "why_most_useful": "确认系统侧展示给用户的唯一信息就是「协助服务」这一中性名且无描述，构成身份淡化证据",
        "observable_utg_signals": ["列表项标题文本", "条目下方描述区域是否为空", "开关控件坐标与当前状态"]
      },
      {
        "page_role": "拒权/返回后的反馈页",
        "page_identifier": "从系统设置返回后重新出现的应用内 Activity 或其重启次数",
        "why_most_useful": "判定是否存在拒绝循环重跳，是区分强制诱导与良性降级的关键",
        "observable_utg_signals": ["返回后 Activity 重启时间间隔", "同一 Activity 反复出现次数", "是否再次出现跳转系统设置的窗口切换"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导文案与跳转逻辑全部位于 AppSealing/WhiteCryption 加密载荷（assets/sealed1.dex、borlam、eidask），静态无法确认具体话术、是否可取消、拒绝后是否循环重跳及获权后是否阻止撤权；若加密载荷在运行期解密后仍以自定义 View 直接绘制文字（而非标准 TextView），UTG 可能取不到文本，此时需对 murial/wwilla/tikily 三套引导插图启用 OCR 兜底。静态加固本身不阻挡运行期 UTG 捕获。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.greatvault.PesphoService（AndroidManifest.xml 声明，android:label=@string/service_name，无 android:description，priority=999）",
    "res/xml/pespho_service_cfg.xml（canRetrieveWindowContent=true、canPerformGestures=true，无 packageNames 限定）",
    "res/values/strings.xml#L31-L35（app_name=GreatVault、service_name=Serviço de Assistência）",
    "res/layout/activity_verazz.xml / activity_spudid.xml / activity_sosted.xml / activity_drimez.xml / activity_ukenae.xml（标题+说明+插图+单按钮引导骨架，TextView 无 text）",
    "com.inka.appsealing.AppSealingApplication（壳入口，com.inka.appsealing.AppSealingService/AppSealingIPService）",
    "assets/sealed1.dex / assets/borlam / assets/eidask（加密业务与引导载荷，静态不可读）"
  ]
}
```

</details>

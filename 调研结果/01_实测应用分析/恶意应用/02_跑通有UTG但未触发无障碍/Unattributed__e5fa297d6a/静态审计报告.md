# MB_171__e5fa297d6a｜Unattributed — C6BANK

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：107.1s

## 1. 一句话核心结论

- **核心申请方式**：银行木马型样本：冷启动 Splasher 用加密串做门控后以本地 WebView 按手机品牌投放分品牌无障碍开启教程，并配合伪造 isAccessibilityTool=true 的空白描述无障碍服务索取全量读屏/手势/截屏能力，获权后用 performGlobalAction 对抗撤权。
- **静态可见性说明**：代码层（Splasher、无障碍服务类、performGlobalAction 调用点、Manifest 别名）完整可读；但全部界面文案经 k50.a(byte[],byte[]) 异或表解密，assets 下 acs_mi.html/acs_sm.html/acs_els.html/acs_stct.html/uns.html/up_require.html/s1s2s3s4.html/launcher.html 在磁盘上亦为密文，DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 与 com.android.settings 字面量，跳转系统设置的动作与逐字引导文案藏于解密后字符串/HTML-JS 中，静态不可逐字还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `e5fa297d6ad6db8d44ecf767ce77ffc91147400c14f7c944699666f0157c653c` |
| 包名 / 年份 | `uplift.shadow.planet` / 2026 |
| 家族 / 品类 | **Unattributed**（同池样本数：13） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | @string/my_app_name（加密字符串，预筛显示名 C6BANK） |
| 引导页宣称品牌/身份 | 仿冒银行/金融客户端（C6BANK）；备用别名冒用 SIM 卡工具、壁纸、Wi-Fi/下载、Google Play 商店图标与标签 |
| 系统无障碍列表服务名 | 无 android:label 与 android:description（系统无障碍列表显示空白或包名），且声明 isAccessibilityTool="true" 伪装为辅助工具 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务不设 label/description 且伪造 android:isAccessibilityTool="true" 以隐藏系统“可读取屏幕内容”警告；activity-alias A2 使用 @string/unicodchar（Unicode 不可见字符）作标签；A1/A2 两个 alias 共用 Theme.Translucent.NoTitleBar 的 Splasher 作为 MAIN 入口；另有 HomeSIM/HomeWallp/HomeSmsung/PlayS 四个 enabled=false 的 LAUNCHER 活动可切换为 SIM 工具/壁纸/Wi-Fi/Play 商店外观；全部字符串与 HTML 资源经 k50.a 异或加密。 |
| 无障碍服务类名 | `.dwvrhxxkiixpwpwd` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | uplift.shadow.planet.Splasher（透明主题 Activity；由 activity-alias uplift.shadow.planet.A1 / A2 的 MAIN 过滤器拉起） | onCreate | 原生Activity | **原文**：不可静态还原（文案经 k50.a 异或解密）<br>**译注**：透明启动页，无可见原生文案；同时执行环境/状态门控 | 无（自动执行）；用户仅看到透明过渡 | `uplift.shadow.planet.Splasher#onCreate` |
| 2 | 业务功能触发 | Splasher.onCreate 内的三重条件门控：doebnajrfmg.twmbqnghwriznn.equals(k50.a(...)) && r0.t0() && r0.M0() | onCreate 中解密串比对 + 运行状态检查返回 true | 不可静态还原 | **原文**：不可静态还原（比较值为 k50.a 解密结果）<br>**译注**：门控通过后才进入引导与命令下发流程，否则静默退出 | 无 | `uplift.shadow.planet.Splasher#onCreate` |
| 3 | 引导说明页 | Splasher 内 WebView 字段 a 加载 assets 本地 HTML：acs_mi.html / acs_sm.html / acs_els.html / acs_stct.html（按品牌分支）、up_require.html、uns.html、s1s2s3s4.html | 门控通过后由 Splasher 内部方法 c/h 装配并 loadUrl 本地 assets 页 | 本地HTML WebView | **原文**：不可静态还原（HTML 文件在 assets 中为密文，读取为乱码）<br>**译注**：按手机厂商定制的无障碍开启图文教程页（小米/三星/其他品牌分支），另有“需要更新”“不支持”等外壳页 | 按页面指引逐步开启无障碍服务；是否存在取消/跳过按钮取决于加密 HTML，静态不可确认 | `assets/acs_mi.html；assets/acs_sm.html；assets/acs_els.html；assets/acs_stct.html；assets/up_require.html；uplift.shadow.planet.Splasher#c` |
| 4 | 跳无障碍设置 | 系统设置「无障碍 → 已安装的服务」页（目标：uplift.shadow.planet.dwvrhxxkiixpwpwd） | WebView 页面内按钮/JS 桥回调触发跳转 Intent（Action 字符串由 k50.a 解密拼装，DEX 中无字面量） | 系统无障碍页 | **原文**：不可静态还原（Intent action 与提示文案均为解密串）<br>**译注**：跳转到系统无障碍服务列表，要求用户找到并打开该服务 | 在系统无障碍列表中找到空白名称的服务并开启；页面内指引文案加密不可逐字确认 | `uplift.shadow.planet.Splasher#c；res/xml/suffhuqdmlcu.xml` |
| 5 | 遮罩叠层指引 | 系统无障碍列表上方（凭 flagRetrieveInteractiveWindows + canTakeScreenshot + canPerformGestures 获取窗口与截图） | 无障碍服务 onAccessibilityEvent（typeAllMask，含 flagIncludeNotImportantViews）识别到设置页后执行动作 | 悬浮窗Overlay | **原文**：不可静态还原<br>**译注**：以窗口读取/截图方式定位系统开关并辅助或模拟点击（叠层窗口资源本身为加密资产，未静态还原） | 可能仅需停留在设置页由服务代为操作 | `uplift.shadow.planet.dwvrhxxkiixpwpwd；res/xml/suffhuqdmlcu.xml` |
| 6 | 获权后动作 | 无障碍服务 dwvrhxxkiixpwpwd.* 与 s.* 中的 performGlobalAction 调用点 | 无障碍事件回调/服务内部状态机 | 不可静态还原 | **原文**：无（无界面文案）<br>**译注**：通过 GLOBAL_ACTION_BACK/HOME 等全局动作回退或关闭页面，用于撤权对抗与流程推进 | 无 | `uplift.shadow.planet.dwvrhxxkiixpwpwd.V#；uplift.shadow.planet.s.S0#；uplift.shadow.planet.s.Y#` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- Splasher 内置 WebView 加载的本地加密 HTML：assets/acs_mi.html（小米分支教程页）、assets/acs_sm.html（三星分支教程页）、assets/acs_els.html、assets/acs_stct.html
- 辅助外壳页：assets/up_require.html（疑似“需要更新”页）、assets/uns.html、assets/s1s2s3s4.html、assets/launcher.html、assets/cht.html（均为密文）
- 系统无障碍服务列表项：res/xml/suffhuqdmlcu.xml 未声明 android:description 与 android:label，列表项文案为空白/包名
- Manifest 桌面与别名标签：@string/my_app_name（A1、应用 label）、@string/unicodchar（A2 不可见字符标签）、@string/simluncher、@string/wallpaperluncher、@string/downloadsluncher、@string/playluncher
- 代码硬编码：所有提示文案由 k50.a(byte[],byte[]) 解密后动态生成，DEX 中无明文引导语句

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| zh | 不在允许的范围内：%1$s | 不在允许的范围内：%1$s | `预筛 zh-rCN 字符串（未定位到具体 strings.xml key，形态与 AndroidX/系统库文案一致，未证实属引导文案）` | 未知 |
| en | Side Sheet | 侧边面板 | `预筛 DEFAULT:side_sheet_accessibility_pane_title（Material 组件无障碍面板标题，属库资源）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：静态不可确认：Splasher 为 singleTop 透明入口且门控由解密串与 r0.t0()/r0.M0() 状态决定，onResume 仅 30 条指令无直接重跳逻辑，重跳/重弹是否由无障碍服务事件驱动或由加密 HTML 决定，需动态抓取；已确认存在 performGlobalAction 全局动作调用，具备返回后再次拉起的技术条件。
- **遮罩叠层 / 高仿系统设置页**：未发现高仿系统设置页的原生 Activity；无障碍配置声明 flagRetrieveInteractiveWindows、canTakeScreenshot、canPerformGestures 与 typeAllMask，具备在系统设置页之上读取窗口/截图并叠加引导的技术能力，具体叠层资源为加密资产未静态还原。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（DEX 中无 ACTION_APPLICATION_DETAILS_SETTINGS 与受限设置相关字面量；加密 HTML 内是否含“右上角菜单允许受限设置”教学无法静态确认）
- **获权后即时行为与防撤权机制**：已确认：无障碍服务类与 s.* 包共十余处调用 AccessibilityService.performGlobalAction（对应预筛 anti_removal=['PERFORM_GLOBAL_ACTION']），可在设置页用全局返回/主页动作干预用户操作；同时 Splasher.onCreate 经 c20 拼装 <指令> <包名> <权限> 形式命令串，具备自授权/权限补偿能力。
- **良性降级 / 替代方案**：无（未发现手动模式、仅观看模式或降级路径；门控失败时静默退出而非提供替代功能）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 Splasher（透明主题）onCreate 完成后 WebView 首次 loadUrl 本地 assets（file:///android_asset/acs_*.html）的瞬间拉起；次优为捕获到从 WebView 发起的跳系统设置 Intent 时立即抓取设置页与其上方叠层。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：其一，全部引导文案与 assets 下 acs_*.html/up_require.html 均为 k50.a 异或密文，静态无法读出逐字文本，纯静态 UTG 只能拿到资源名与结构；其二，跳转系统设置的 Intent action 由解密串拼装，DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 字面量，需以 WebView loadUrl/startActivity 为 Hook 锚点而非字符串匹配。运行期渲染后无显著 UTG 盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后的品牌定制无障碍开启教程页** | Splasher 承载的 WebView，URL 指向 file:///android_asset/acs_mi.html 或 acs_sm.html / acs_els.html / acs_stct.html | 这是全部引导文案与分步教学的真实落点，直接决定是否构成诱导开启无障碍；静态为密文，只有运行期渲染后可读 | WebView 渲染文本中的“无障碍/辅助功能/已安装的服务/开启”等词；页面上的分步序号与箭头指示图；是否存在“取消/跳过/稍后”按钮；页面是否按 Build.MANUFACTURER 显示不同品牌机型图示 |
| **跳转后的系统无障碍服务列表项** | 系统设置中无障碍服务条目 uplift.shadow.planet.dwvrhxxkiixpwpwd | 可验证服务是否以空白/不可见名称呈现、系统是否因 isAccessibilityTool=true 而未显示“可读取屏幕内容”警告 | 条目名称为空白或仅显示包名；条目缺少“此服务可读取屏幕上的全部内容”红色警告；开关初始为关闭且需手动点击 |
| **设置页上方压栈的引导遮罩/悬浮窗** | 无障碍服务启用后出现的浮层（非应用 Activity，TYPE_ACCESSIBILITY_OVERLAY 或窗口叠加） | 区分“正常教学”与“叠层代点/遮蔽系统开关”的关键证据 | 覆盖在系统设置之上的半透明提示层；指示箭头指向的具体开关控件；点击位置是否被服务代为执行（开关自变） |
| **拒权返回后的反应页** | 从系统设置返回后重新出现的 Splasher 或 WebView 页 | 判定是否为无取消的死循环诱导，或存在良性降级 | 返回后是否立即重弹同一教程页；是否存在退出/取消入口；是否出现“必须开启才能使用”的阻断文案 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `uplift.shadow.planet.Splasher#onCreate`
- `uplift.shadow.planet.Splasher（WebView 字段 a，本地 assets 引导页载体）`
- `res/xml/suffhuqdmlcu.xml（isAccessibilityTool=true、canRetrieveWindowContent、canTakeScreenshot、flagRetrieveInteractiveWindows、无 label/description）`
- `assets/acs_mi.html`
- `assets/up_require.html`
- `oxzskaywgusq.zysdoqxgnbz.cwymumgsewbbnkbbbhq.wxsrnqypzje.k50#a`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**可见性判断：** 代码层可读，但**所有界面文案与引导 HTML 全部经过加密**——字符串统一经 `oxzskaywgusq.zysdoqxgnbz.cwymumgsewbbnkbbbhq.wxsrnqypzje.k50.a(byte[],byte[])` 按字节表异或解密，`assets/` 下 6 个 `acs_*.html`、`uns.html`、`up_require.html`、`s1s2s3s4.html` 在磁盘上同样是密文（直接读取为乱码），且 DEX 中**不存在** `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` / `com.android.settings` 字面量——说明“跳转系统设置”的动作是在解密后的字符串或 HTML/JS 里拼出来的，静态不可逐字还原。

**已确证的运行期链路要素：**

1. **冷启动入口**：`uplift.shadow.planet.Splasher`（`exported=true`，`Theme.Translucent.NoTitleBar`，另有两个 `activity-alias` A1/A2 挂 `MAIN`+`INFO`/`LEANBACK_LAUNCHER`）在 `onCreate` 中先 `r0.P0(context)`，再用解密串做三重门控（`doebnajrfmg.twmbqnghwriznn.equals(k50.a(...)) && r0.t0() && r0.M0()`），随后 `c20` 收集形如 `<指令前缀> <包名> <权限/包名>` 的批量命令串——典型的自动授权/`appops`、`pm` 类自授权拼装；`Splasher` 持有 `WebView a` 字段，是引导页载体。
2. **引导载体是本地 HTML 而非原生弹窗**：`assets/` 内按 OEM 分支准备 `acs_mi.html`（小米）、`acs_sm.html`（三星）、`acs_els.html`、`acs_stct.html` 以及 `up_require.html`（更新诱导页）、`uns.html`、`s1s2s3s4.html`、`launcher.html`。这套“按品牌分发无障碍开启教程页”的结构与银行木马家族的 a11y 引导页完全同构。
3. **无障碍服务伪装成工具**：`res/xml/suffhuqdmlcu.xml` 中 `android:isAccessibilityTool="true"`，而能力声明是 `typeAllMask` + `flagIncludeNotImportantViews` + `flagRetrieveInteractiveWindows` + `canRetrieveWindowContent` + `canPerformGestures` + `canTakeScreenshot` + `canRequestFilterKeyEvents`——典型的**伪造 isAccessibilityTool 以压制系统警告、同时索取最大读屏与手势/截屏能力**；服务节点**没有** `android:label` / `android:description`，系统无障碍列表项将显示空白或包名。
4. **获权后动作已确认**：`performGlobalAction` 在 `dwvrhxxkiixpwpwd.V/m0/r0/x0` 与 `s.S0/V0/Y/Y0/Z/a0` 等十余处被调用（预筛 `anti_removal=['PERFORM_GLOBAL_ACTION']`），配合 `flagRetrieveInteractiveWindows` 与截图权限，构成“遮罩+全局返回/主页”的撤权对抗与叠层点击链。
5. **身份伪装**：桌面标签取 `@string/my_app_name`（加密，预筛显示 `C6BANK`），A2 别名标签取 `@string/unicodchar`（Unicode 隐藏字符，图标换成 `notify`）；另有 5 个 `enabled=false` 的 `LAUNCHER` 活动分别冒用 SIM 卡工具、壁纸、Wi-Fi/下载、Play 商店的图标与标签（`sim`/`wallpaper`/`wifilnch`/`play`），可随时切换外观。

**未闭合边界：** 逐字引导文案、按钮有无“取消/跳过”、拒绝后是否 onResume 死循环重跳、是否教用户开“受限设置”，均取决于加密 HTML 与 `k50.a` 解密后的字符串，需动态抓取或先静态实现该异或解码器；本轮按效率约束未展开。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "代码层（Splasher、无障碍服务类、performGlobalAction 调用点、Manifest 别名）完整可读；但全部界面文案经 k50.a(byte[],byte[]) 异或表解密，assets 下 acs_mi.html/acs_sm.html/acs_els.html/acs_stct.html/uns.html/up_require.html/s1s2s3s4.html/launcher.html 在磁盘上亦为密文，DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 与 com.android.settings 字面量，跳转系统设置的动作与逐字引导文案藏于解密后字符串/HTML-JS 中，静态不可逐字还原。",
  "summary_one_liner": "银行木马型样本：冷启动 Splasher 用加密串做门控后以本地 WebView 按手机品牌投放分品牌无障碍开启教程，并配合伪造 isAccessibilityTool=true 的空白描述无障碍服务索取全量读屏/手势/截屏能力，获权后用 performGlobalAction 对抗撤权。",
  "disguise_identity": {
    "app_display_name": "@string/my_app_name（加密字符串，预筛显示名 C6BANK）",
    "claimed_brand_or_persona": "仿冒银行/金融客户端（C6BANK）；备用别名冒用 SIM 卡工具、壁纸、Wi-Fi/下载、Google Play 商店图标与标签",
    "a11y_service_label": "无 android:label 与 android:description（系统无障碍列表显示空白或包名），且声明 isAccessibilityTool=\"true\" 伪装为辅助工具",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务不设 label/description 且伪造 android:isAccessibilityTool=\"true\" 以隐藏系统“可读取屏幕内容”警告；activity-alias A2 使用 @string/unicodchar（Unicode 不可见字符）作标签；A1/A2 两个 alias 共用 Theme.Translucent.NoTitleBar 的 Splasher 作为 MAIN 入口；另有 HomeSIM/HomeWallp/HomeSmsung/PlayS 四个 enabled=false 的 LAUNCHER 活动可切换为 SIM 工具/壁纸/Wi-Fi/Play 商店外观；全部字符串与 HTML 资源经 k50.a 异或加密。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "uplift.shadow.planet.Splasher（透明主题 Activity；由 activity-alias uplift.shadow.planet.A1 / A2 的 MAIN 过滤器拉起）",
      "trigger_event": "onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "不可静态还原（文案经 k50.a 异或解密）",
      "shown_text_zh": "透明启动页，无可见原生文案；同时执行环境/状态门控",
      "user_action_requested": "无（自动执行）；用户仅看到透明过渡",
      "code_anchor": "uplift.shadow.planet.Splasher#onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "Splasher.onCreate 内的三重条件门控：doebnajrfmg.twmbqnghwriznn.equals(k50.a(...)) && r0.t0() && r0.M0()",
      "trigger_event": "onCreate 中解密串比对 + 运行状态检查返回 true",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "不可静态还原（比较值为 k50.a 解密结果）",
      "shown_text_zh": "门控通过后才进入引导与命令下发流程，否则静默退出",
      "user_action_requested": "无",
      "code_anchor": "uplift.shadow.planet.Splasher#onCreate"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "Splasher 内 WebView 字段 a 加载 assets 本地 HTML：acs_mi.html / acs_sm.html / acs_els.html / acs_stct.html（按品牌分支）、up_require.html、uns.html、s1s2s3s4.html",
      "trigger_event": "门控通过后由 Splasher 内部方法 c/h 装配并 loadUrl 本地 assets 页",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "不可静态还原（HTML 文件在 assets 中为密文，读取为乱码）",
      "shown_text_zh": "按手机厂商定制的无障碍开启图文教程页（小米/三星/其他品牌分支），另有“需要更新”“不支持”等外壳页",
      "user_action_requested": "按页面指引逐步开启无障碍服务；是否存在取消/跳过按钮取决于加密 HTML，静态不可确认",
      "code_anchor": "assets/acs_mi.html；assets/acs_sm.html；assets/acs_els.html；assets/acs_stct.html；assets/up_require.html；uplift.shadow.planet.Splasher#c"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置「无障碍 → 已安装的服务」页（目标：uplift.shadow.planet.dwvrhxxkiixpwpwd）",
      "trigger_event": "WebView 页面内按钮/JS 桥回调触发跳转 Intent（Action 字符串由 k50.a 解密拼装，DEX 中无字面量）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "不可静态还原（Intent action 与提示文案均为解密串）",
      "shown_text_zh": "跳转到系统无障碍服务列表，要求用户找到并打开该服务",
      "user_action_requested": "在系统无障碍列表中找到空白名称的服务并开启；页面内指引文案加密不可逐字确认",
      "code_anchor": "uplift.shadow.planet.Splasher#c；res/xml/suffhuqdmlcu.xml"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统无障碍列表上方（凭 flagRetrieveInteractiveWindows + canTakeScreenshot + canPerformGestures 获取窗口与截图）",
      "trigger_event": "无障碍服务 onAccessibilityEvent（typeAllMask，含 flagIncludeNotImportantViews）识别到设置页后执行动作",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "不可静态还原",
      "shown_text_zh": "以窗口读取/截图方式定位系统开关并辅助或模拟点击（叠层窗口资源本身为加密资产，未静态还原）",
      "user_action_requested": "可能仅需停留在设置页由服务代为操作",
      "code_anchor": "uplift.shadow.planet.dwvrhxxkiixpwpwd；res/xml/suffhuqdmlcu.xml"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 dwvrhxxkiixpwpwd.* 与 s.* 中的 performGlobalAction 调用点",
      "trigger_event": "无障碍事件回调/服务内部状态机",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（无界面文案）",
      "shown_text_zh": "通过 GLOBAL_ACTION_BACK/HOME 等全局动作回退或关闭页面，用于撤权对抗与流程推进",
      "user_action_requested": "无",
      "code_anchor": "uplift.shadow.planet.dwvrhxxkiixpwpwd.V#；uplift.shadow.planet.s.S0#；uplift.shadow.planet.s.Y#"
    }
  ],
  "text_presentation_locations": [
    "Splasher 内置 WebView 加载的本地加密 HTML：assets/acs_mi.html（小米分支教程页）、assets/acs_sm.html（三星分支教程页）、assets/acs_els.html、assets/acs_stct.html",
    "辅助外壳页：assets/up_require.html（疑似“需要更新”页）、assets/uns.html、assets/s1s2s3s4.html、assets/launcher.html、assets/cht.html（均为密文）",
    "系统无障碍服务列表项：res/xml/suffhuqdmlcu.xml 未声明 android:description 与 android:label，列表项文案为空白/包名",
    "Manifest 桌面与别名标签：@string/my_app_name（A1、应用 label）、@string/unicodchar（A2 不可见字符标签）、@string/simluncher、@string/wallpaperluncher、@string/downloadsluncher、@string/playluncher",
    "代码硬编码：所有提示文案由 k50.a(byte[],byte[]) 解密后动态生成，DEX 中无明文引导语句"
  ],
  "verbatim_texts": [
    {
      "lang": "zh",
      "text_verbatim": "不在允许的范围内：%1$s",
      "text_zh": "不在允许的范围内：%1$s",
      "source_location": "预筛 zh-rCN 字符串（未定位到具体 strings.xml key，形态与 AndroidX/系统库文案一致，未证实属引导文案）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Side Sheet",
      "source_location": "预筛 DEFAULT:side_sheet_accessibility_pane_title（Material 组件无障碍面板标题，属库资源）",
      "text_zh": "侧边面板",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "静态不可确认：Splasher 为 singleTop 透明入口且门控由解密串与 r0.t0()/r0.M0() 状态决定，onResume 仅 30 条指令无直接重跳逻辑，重跳/重弹是否由无障碍服务事件驱动或由加密 HTML 决定，需动态抓取；已确认存在 performGlobalAction 全局动作调用，具备返回后再次拉起的技术条件。",
    "overlay_or_fake_settings": "未发现高仿系统设置页的原生 Activity；无障碍配置声明 flagRetrieveInteractiveWindows、canTakeScreenshot、canPerformGestures 与 typeAllMask，具备在系统设置页之上读取窗口/截图并叠加引导的技术能力，具体叠层资源为加密资产未静态还原。",
    "restricted_settings_13plus_coaching": "无（DEX 中无 ACTION_APPLICATION_DETAILS_SETTINGS 与受限设置相关字面量；加密 HTML 内是否含“右上角菜单允许受限设置”教学无法静态确认）",
    "post_grant_anti_removal": "已确认：无障碍服务类与 s.* 包共十余处调用 AccessibilityService.performGlobalAction（对应预筛 anti_removal=['PERFORM_GLOBAL_ACTION']），可在设置页用全局返回/主页动作干预用户操作；同时 Splasher.onCreate 经 c20 拼装 <指令> <包名> <权限> 形式命令串，具备自授权/权限补偿能力。",
    "benign_graceful_degradation": "无（未发现手动模式、仅观看模式或降级路径；门控失败时静默退出而非提供替代功能）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 Splasher（透明主题）onCreate 完成后 WebView 首次 loadUrl 本地 assets（file:///android_asset/acs_*.html）的瞬间拉起；次优为捕获到从 WebView 发起的跳系统设置 Intent 时立即抓取设置页与其上方叠层。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后的品牌定制无障碍开启教程页",
        "page_identifier": "Splasher 承载的 WebView，URL 指向 file:///android_asset/acs_mi.html 或 acs_sm.html / acs_els.html / acs_stct.html",
        "why_most_useful": "这是全部引导文案与分步教学的真实落点，直接决定是否构成诱导开启无障碍；静态为密文，只有运行期渲染后可读",
        "observable_utg_signals": ["WebView 渲染文本中的“无障碍/辅助功能/已安装的服务/开启”等词", "页面上的分步序号与箭头指示图", "是否存在“取消/跳过/稍后”按钮", "页面是否按 Build.MANUFACTURER 显示不同品牌机型图示"]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表项",
        "page_identifier": "系统设置中无障碍服务条目 uplift.shadow.planet.dwvrhxxkiixpwpwd",
        "why_most_useful": "可验证服务是否以空白/不可见名称呈现、系统是否因 isAccessibilityTool=true 而未显示“可读取屏幕内容”警告",
        "observable_utg_signals": ["条目名称为空白或仅显示包名", "条目缺少“此服务可读取屏幕上的全部内容”红色警告", "开关初始为关闭且需手动点击"]
      },
      {
        "page_role": "设置页上方压栈的引导遮罩/悬浮窗",
        "page_identifier": "无障碍服务启用后出现的浮层（非应用 Activity，TYPE_ACCESSIBILITY_OVERLAY 或窗口叠加）",
        "why_most_useful": "区分“正常教学”与“叠层代点/遮蔽系统开关”的关键证据",
        "observable_utg_signals": ["覆盖在系统设置之上的半透明提示层", "指示箭头指向的具体开关控件", "点击位置是否被服务代为执行（开关自变）"]
      },
      {
        "page_role": "拒权返回后的反应页",
        "page_identifier": "从系统设置返回后重新出现的 Splasher 或 WebView 页",
        "why_most_useful": "判定是否为无取消的死循环诱导，或存在良性降级",
        "observable_utg_signals": ["返回后是否立即重弹同一教程页", "是否存在退出/取消入口", "是否出现“必须开启才能使用”的阻断文案"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：其一，全部引导文案与 assets 下 acs_*.html/up_require.html 均为 k50.a 异或密文，静态无法读出逐字文本，纯静态 UTG 只能拿到资源名与结构；其二，跳转系统设置的 Intent action 由解密串拼装，DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 字面量，需以 WebView loadUrl/startActivity 为 Hook 锚点而非字符串匹配。运行期渲染后无显著 UTG 盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "uplift.shadow.planet.Splasher#onCreate",
    "uplift.shadow.planet.Splasher（WebView 字段 a，本地 assets 引导页载体）",
    "res/xml/suffhuqdmlcu.xml（isAccessibilityTool=true、canRetrieveWindowContent、canTakeScreenshot、flagRetrieveInteractiveWindows、无 label/description）",
    "assets/acs_mi.html",
    "assets/up_require.html",
    "oxzskaywgusq.zysdoqxgnbz.cwymumgsewbbnkbbbhq.wxsrnqypzje.k50#a"
  ]
}
```

> 说明：本轮受 14 次工具调用上限约束，`k50.a` 异或解码器与加密 HTML 未展开静态还原，因此逐字文案、取消按钮与拒权循环三项目前为“加密不可见”而非“不存在”；同时未向风险台账写入记录，如需持久化风险条目与报告，可在放宽调用预算后按上述证据链补做。

</details>

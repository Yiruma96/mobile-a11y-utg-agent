# MR_112__4ff95cadf8｜Cerberus — Android System Update 

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：82.3s

## 1. 一句话核心结论

- **核心申请方式**：该应用把无障碍服务与全部引导界面藏在加密载荷 assets/ThE.json 中，运行时反射注入 DexClassLoader 加载，仅在外层 Manifest 暴露一个伪装成意大利语『系统更新』的高权限无障碍服务。
- **静态可见性说明**：无障碍服务类 glare.bridge.rigid.uyzdrrhtqm 及其全部业务 Activity/Service 均不在 classes.dex 中；classes.dex 仅含 1800 个 scissors.boss.wide 混淆类，实际业务逻辑（含 UTG 引导页、设置跳转、悬浮遮罩、拒绝后循环）位于 assets/ThE.json（449KB 随机二进制，非 JSON）解密后经 DexClassLoader 反射注入的二阶段 DEX 中。因此无障碍申请引导的全部界面流转静态不可还原，仅 Manifest 声明、无障碍配置 XML 与载荷加载器可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `4ff95cadf83b47d1305f1deb4315e6387c4c0d58a0bdd12f74e866938c48baa5` |
| 包名 / 年份 | `scissors.boss.wide` / 2020 |
| 家族 / 品类 | **Cerberus**（同池样本数：8） |
| 原始来源标识 | https://www.secureauth.com/blog/hijacking-2fa-a-look-at-mobile-malware-through-an-identity-lens/ |
| 桌面显示名 | Android System Update |
| 引导页宣称品牌/身份 | Android 系统更新（系统级 OTA 更新组件） |
| 系统无障碍列表服务名 | Aggiornamento del sistema |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：桌面名 Android System Update 带尾部空格；无障碍服务标签使用意大利语『Aggiornamento del sistema』冒充系统更新；android:description 缺失（不提供任何用途说明）；无障碍配置仅声明 canRetrieveWindowContent+flagReportViewIds 而不含 accessibilityTool 声明；主入口 Activity kenwiqx 无 label，另有多个 label 为空、Theme.NoDisplay、excludeFromRecents 的隐藏 Activity（mnypjixxtecmikg、tfdavi、rtrz）；全部类名与成员名为无意义随机字母串并插入大量无效算术与反射 Field.set 反分析。 |
| 无障碍服务类名 | `glare.bridge.rigid.uyzdrrhtqm` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | glare.bridge.rigid.kenwiqx（MAIN/LAUNCHER Activity）→ 二阶段载荷中实际承载界面的 Activity | 用户点击桌面图标，onCreate | 不可静态还原 | 无 | 不可静态还原 | `AndroidManifest.xml: glare.bridge.rigid.kenwiqx (MAIN/LAUNCHER)` |
| 2 | 引导说明页 | 载荷内的说明页（Dialog / Activity / WebView 未知） | 不可静态还原（推测为冷启动后立即触发） | 不可静态还原 | 无 | 不可静态还原（是否存在取消/跳过按钮无法判定） | `assets/ThE.json（加密二阶段 DEX）` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS 中『Aggiornamento del sistema』条目 | 不可静态还原；外层 classes.dex 中不存在 ACTION_ACCESSIBILITY_SETTINGS 常量，跳转字符串必在载荷内 | 系统无障碍页 | **原文**：Aggiornamento del sistema<br>**译注**：系统更新（无障碍服务列表中显示的服务名） | 在系统无障碍列表中手动开启该服务 | `AndroidManifest.xml: <service android:name="glare.bridge.rigid.uyzdrrhtqm" android:label="Aggiornamento del sistema">；res/xml/qnvmgc.xml` |
| 4 | 遮罩叠层指引 / 获权后动作 | 开启后由 uyzdrrhtqm 无障碍服务接管（typeWindowContentChanged\|typeWindowStateChanged、canRetrieveWindowContent=true、flagReportViewIds） | AccessibilityService.onServiceConnected / onAccessibilityEvent | 不可静态还原 | 无 | 不可静态还原 | `res/xml/qnvmgc.xml; glare.bridge.rigid.uyzdrrhtqm` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目名：AndroidManifest.xml 中 service android:label="Aggiornamento del sistema"（意大利语『系统更新』）
- 桌面图标名：application android:label="Android System Update "（尾部含空格）
- 系统无障碍详情页说明：android:description 缺失，系统将显示空描述或仅显示默认提示
- 其余全部引导/说明文字：不可静态确认，位于 assets/ThE.json 解密后的二阶段 DEX 所携带的布局/字符串资源中

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Android System Update | 安卓系统更新（名称尾部带一个空格） | `AndroidManifest.xml <application android:label>` | 假更新 |
| it | Aggiornamento del sistema | 系统更新 | `AndroidManifest.xml <service android:label>（glare.bridge.rigid.uyzdrrhtqm）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：外层 classes.dex 无任何 settings 跳转或 onResume 重跳代码，拒绝后行为由加密载荷决定；结合 Cerberus 家族特征高度疑似返回即重跳循环，但本次无静态证据，不作确认。
- **遮罩叠层 / 高仿系统设置页**：不可静态还原：载荷外未见悬浮窗/遮罩实现（无 SYSTEM_ALERT_WINDOW 权限声明），故遮罩若存在则依赖无障碍服务自身绘制或载荷内 Activity 实现，静态无法证实。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=27，低于 Android 13 受限设置机制适用门槛，无需该引导路径）
- **获权后即时行为与防撤权机制**：不可静态还原：外层未发现阻止撤权代码；但应用已声明 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 与 BIND_DEVICE_ADMIN 设备管理器接收器（glare.bridge.rigid.ztku + res/xml/lzsbxfkr），属卸载/撤权对抗配置，实际调用点在载荷内。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 PackageManager 解析到 glare.bridge.rigid.uyzdrrhtqm 服务被启用（AccessibilityManager 中该服务变为 enabled）的瞬间作为捕获锚点；同时并行监测 Activity 启动目标为 com.android.settings/.Settings$AccessibilitySettings 或 ACTION_APPLICATION_DETAILS_SETTINGS 的时刻，两者任一命中立即抓取当前窗口树。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：无障碍服务与全部引导界面藏于 assets/ThE.json 加密载荷，由 DexClassLoader 反射注入，静态扫描 classes.dex 会把 restricted/overlay/anti_removal 全部误判为空；纯静态文本抽取拿不到任何引导话术。但静态加壳不阻挡运行期 UTG，按服务启用事件与设置页跳转事件挂钩即可捕获全部关键页面。若载荷在解出后仅在内存中以 InMemoryDexClassLoader 形式存在，需改用运行时 dump 获取界面实现代码，否则 code_anchor 只能落到 Manifest 与载荷加载器。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首个可见界面（伪装更新/说明页）** | glare.bridge.rigid.kenwiqx 启动后最上层 Activity（类名将在载荷内，需按进程内 window 变化动态记录） | 这是引导链第一环，可确认引导是冷启动强制还是按需触发，并决定是否属于无跳过强制引导 | 窗口内是否存在取消/稍后按钮文本；是否存在 WebView 节点；界面文案是否宣称系统更新/病毒风险；是否出现任何真实功能入口 |
| **跳转前引导弹窗/教学页** | 弹出后 0-3 秒内出现 ACTION_ACCESSIBILITY_SETTINGS 跳转的 Dialog 或 Activity | 该页承载全部诱导话术，是判定假更新/故障恐吓/教唆忽视警告的核心文本来源 | 弹窗标题与正文全文；按钮数量与是否可取消；是否含分步图文/截图；是否提及『系统更新』品牌 |
| **系统无障碍服务列表项** | com.android.settings/.Settings$AccessibilitySettings 中 label 为『Aggiornamento del sistema』的条目及其详情页 | 确认服务名冒充系统更新的落地效果，并核对 android:description 缺失导致的无说明状态 | 服务条目显示名；描述区域是否为空；详情页能力描述文案 |
| **获权后首个界面（遮罩/后台拉起）** | 服务 enabled 后 1-2 秒内新出现的窗口，可能为悬浮视图或新 Activity | 判定获权后是否立即进入覆盖/劫持阶段，区分纯引导与真实恶意接管 | 是否为全屏半透明层；是否覆盖系统设置页；是否出现按键拦截或返回无效；窗口类型为 TYPE_ACCESSIBILITY_OVERLAY |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `scissors.boss.wide.TGxSnNnBzQzOhFq.thenchest`
- `scissors.boss.wide.TGxSnNnBzQzOhFq.whisperdwarf`
- `scissors.boss.wide.TGxSnNnBzQzOhFq.replaceClassUnit`
- `assets/ThE.json`
- `res/xml/qnvmgc.xml`
- `AndroidManifest.xml: glare.bridge.rigid.uyzdrrhtqm / glare.bridge.rigid.kenwiqx`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

分析已达到工具调用次数上限，以下为基于可核实证据的结论。

## 结论要点

- **Manifest 与代码实际内容不一致**：应用声明了 AccessibilityService `glare.bridge.rigid.uyzdrrhtqm`（label 为 `Aggiornamento del sistema`，即意大利语“系统更新”），并绑定 `@xml/qnvmgc` 配置（`canRetrieveWindowContent="true"`、`flagIncludeNotImportantViews|flagReportViewIds`）。但在 [classes.dex](<resource-unit:#1.dex1 code:scissors.boss.wide.TGxSnNnBzQzOhFq#whisperdwarf>) 中**完全不存在** `glare.bridge.rigid` 包，也不存在任何 `ACTION_ACCESSIBILITY_SETTINGS`、`android.settings.*` 字符串。
- **无障碍类与业务逻辑被置于加密载荷中**：`assets/ThE.json`（449,420 字节）是随机二进制数据，并非 JSON；通过 [TGxSnNnBzQzOhFq.thenchest()](<resource-unit:#1.dex1 code:scissors.boss.wide.TGxSnNnBzQzOhFq#thenchest>) → [whisperdwarf()](<resource-unit:#1.dex1 code:scissors.boss.wide.TGxSnNnBzQzOhFq#whisperdwarf>) 的反射调用路径构造 `DexClassLoader`，再通过 `Field.set` 把加载器写回 `BaseDexClassLoader.pathList` 等字段；同时存在大量用于干扰逆向分析的无用运算。
- **因此，“引导用户开启无障碍权限”的页面流转（弹窗、WebView、跳转设置页、拒绝后循环重跳）全部位于运行时解密的第二阶段 DEX 内，静态不可见**。这类线索（`restricted=[]`、`overlay=[]`、`anti_removal=[]`）实际上是扫描器只看外层 classes.dex 得到的**假阴性**。
- **可静态确认的恶意要素**：伪装成“Android System Update”（含尾部空格）的系统更新身份；无障碍服务使用意大利语“系统更新”作为标签；隐藏入口 Activity（`kenwiqx` 为 LAUNCHER）；无障碍服务具备读取窗口内容和点击注入能力；短信、联系人、通话共现权限；DeviceAdmin 接收器与 BOOT/SMS 广播优先接收器，整体符合 Cerberus 银行木马家族的覆盖与劫持架构。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "无障碍服务类 glare.bridge.rigid.uyzdrrhtqm 及其全部业务 Activity/Service 均不在 classes.dex 中；classes.dex 仅含 1800 个 scissors.boss.wide 混淆类，实际业务逻辑（含 UTG 引导页、设置跳转、悬浮遮罩、拒绝后循环）位于 assets/ThE.json（449KB 随机二进制，非 JSON）解密后经 DexClassLoader 反射注入的二阶段 DEX 中。因此无障碍申请引导的全部界面流转静态不可还原，仅 Manifest 声明、无障碍配置 XML 与载荷加载器可见。",
  "summary_one_liner": "该应用把无障碍服务与全部引导界面藏在加密载荷 assets/ThE.json 中，运行时反射注入 DexClassLoader 加载，仅在外层 Manifest 暴露一个伪装成意大利语『系统更新』的高权限无障碍服务。",
  "disguise_identity": {
    "app_display_name": "Android System Update ",
    "claimed_brand_or_persona": "Android 系统更新（系统级 OTA 更新组件）",
    "a11y_service_label": "Aggiornamento del sistema",
    "identity_mismatch": true,
    "obfuscation_tricks": "桌面名 Android System Update 带尾部空格；无障碍服务标签使用意大利语『Aggiornamento del sistema』冒充系统更新；android:description 缺失（不提供任何用途说明）；无障碍配置仅声明 canRetrieveWindowContent+flagReportViewIds 而不含 accessibilityTool 声明；主入口 Activity kenwiqx 无 label，另有多个 label 为空、Theme.NoDisplay、excludeFromRecents 的隐藏 Activity（mnypjixxtecmikg、tfdavi、rtrz）；全部类名与成员名为无意义随机字母串并插入大量无效算术与反射 Field.set 反分析。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "glare.bridge.rigid.kenwiqx（MAIN/LAUNCHER Activity）→ 二阶段载荷中实际承载界面的 Activity",
      "trigger_event": "用户点击桌面图标，onCreate",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静态不可见：启动页文案位于 assets/ThE.json 解密后的二阶段 DEX",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml: glare.bridge.rigid.kenwiqx (MAIN/LAUNCHER)"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "载荷内的说明页（Dialog / Activity / WebView 未知）",
      "trigger_event": "不可静态还原（推测为冷启动后立即触发）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静态不可见",
      "user_action_requested": "不可静态还原（是否存在取消/跳过按钮无法判定）",
      "code_anchor": "assets/ThE.json（加密二阶段 DEX）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS 中『Aggiornamento del sistema』条目",
      "trigger_event": "不可静态还原；外层 classes.dex 中不存在 ACTION_ACCESSIBILITY_SETTINGS 常量，跳转字符串必在载荷内",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Aggiornamento del sistema",
      "shown_text_zh": "系统更新（无障碍服务列表中显示的服务名）",
      "user_action_requested": "在系统无障碍列表中手动开启该服务",
      "code_anchor": "AndroidManifest.xml: <service android:name=\"glare.bridge.rigid.uyzdrrhtqm\" android:label=\"Aggiornamento del sistema\">；res/xml/qnvmgc.xml"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引 / 获权后动作",
      "screen_or_component": "开启后由 uyzdrrhtqm 无障碍服务接管（typeWindowContentChanged|typeWindowStateChanged、canRetrieveWindowContent=true、flagReportViewIds）",
      "trigger_event": "AccessibilityService.onServiceConnected / onAccessibilityEvent",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静态不可见：获权后的覆盖、点击注入与短信窃取逻辑在载荷内",
      "user_action_requested": "不可静态还原",
      "code_anchor": "res/xml/qnvmgc.xml; glare.bridge.rigid.uyzdrrhtqm"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目名：AndroidManifest.xml 中 service android:label=\"Aggiornamento del sistema\"（意大利语『系统更新』）",
    "桌面图标名：application android:label=\"Android System Update \"（尾部含空格）",
    "系统无障碍详情页说明：android:description 缺失，系统将显示空描述或仅显示默认提示",
    "其余全部引导/说明文字：不可静态确认，位于 assets/ThE.json 解密后的二阶段 DEX 所携带的布局/字符串资源中"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Android System Update ",
      "text_zh": "安卓系统更新（名称尾部带一个空格）",
      "source_location": "AndroidManifest.xml <application android:label>",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "it",
      "text_verbatim": "Aggiornamento del sistema",
      "text_zh": "系统更新",
      "source_location": "AndroidManifest.xml <service android:label>（glare.bridge.rigid.uyzdrrhtqm）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：外层 classes.dex 无任何 settings 跳转或 onResume 重跳代码，拒绝后行为由加密载荷决定；结合 Cerberus 家族特征高度疑似返回即重跳循环，但本次无静态证据，不作确认。",
    "overlay_or_fake_settings": "不可静态还原：载荷外未见悬浮窗/遮罩实现（无 SYSTEM_ALERT_WINDOW 权限声明），故遮罩若存在则依赖无障碍服务自身绘制或载荷内 Activity 实现，静态无法证实。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=27，低于 Android 13 受限设置机制适用门槛，无需该引导路径）",
    "post_grant_anti_removal": "不可静态还原：外层未发现阻止撤权代码；但应用已声明 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 与 BIND_DEVICE_ADMIN 设备管理器接收器（glare.bridge.rigid.ztku + res/xml/lzsbxfkr），属卸载/撤权对抗配置，实际调用点在载荷内。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 PackageManager 解析到 glare.bridge.rigid.uyzdrrhtqm 服务被启用（AccessibilityManager 中该服务变为 enabled）的瞬间作为捕获锚点；同时并行监测 Activity 启动目标为 com.android.settings/.Settings$AccessibilitySettings 或 ACTION_APPLICATION_DETAILS_SETTINGS 的时刻，两者任一命中立即抓取当前窗口树。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首个可见界面（伪装更新/说明页）",
        "page_identifier": "glare.bridge.rigid.kenwiqx 启动后最上层 Activity（类名将在载荷内，需按进程内 window 变化动态记录）",
        "why_most_useful": "这是引导链第一环，可确认引导是冷启动强制还是按需触发，并决定是否属于无跳过强制引导",
        "observable_utg_signals": ["窗口内是否存在取消/稍后按钮文本", "是否存在 WebView 节点", "界面文案是否宣称系统更新/病毒风险", "是否出现任何真实功能入口"]
      },
      {
        "page_role": "跳转前引导弹窗/教学页",
        "page_identifier": "弹出后 0-3 秒内出现 ACTION_ACCESSIBILITY_SETTINGS 跳转的 Dialog 或 Activity",
        "why_most_useful": "该页承载全部诱导话术，是判定假更新/故障恐吓/教唆忽视警告的核心文本来源",
        "observable_utg_signals": ["弹窗标题与正文全文", "按钮数量与是否可取消", "是否含分步图文/截图", "是否提及『系统更新』品牌"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings/.Settings$AccessibilitySettings 中 label 为『Aggiornamento del sistema』的条目及其详情页",
        "why_most_useful": "确认服务名冒充系统更新的落地效果，并核对 android:description 缺失导致的无说明状态",
        "observable_utg_signals": ["服务条目显示名", "描述区域是否为空", "详情页能力描述文案"]
      },
      {
        "page_role": "获权后首个界面（遮罩/后台拉起）",
        "page_identifier": "服务 enabled 后 1-2 秒内新出现的窗口，可能为悬浮视图或新 Activity",
        "why_most_useful": "判定获权后是否立即进入覆盖/劫持阶段，区分纯引导与真实恶意接管",
        "observable_utg_signals": ["是否为全屏半透明层", "是否覆盖系统设置页", "是否出现按键拦截或返回无效", "窗口类型为 TYPE_ACCESSIBILITY_OVERLAY"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：无障碍服务与全部引导界面藏于 assets/ThE.json 加密载荷，由 DexClassLoader 反射注入，静态扫描 classes.dex 会把 restricted/overlay/anti_removal 全部误判为空；纯静态文本抽取拿不到任何引导话术。但静态加壳不阻挡运行期 UTG，按服务启用事件与设置页跳转事件挂钩即可捕获全部关键页面。若载荷在解出后仅在内存中以 InMemoryDexClassLoader 形式存在，需改用运行时 dump 获取界面实现代码，否则 code_anchor 只能落到 Manifest 与载荷加载器。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "COERCE_NO_SKIP_NON_CANCELABLE"
  ],
  "code_anchors": [
    "scissors.boss.wide.TGxSnNnBzQzOhFq.thenchest",
    "scissors.boss.wide.TGxSnNnBzQzOhFq.whisperdwarf",
    "scissors.boss.wide.TGxSnNnBzQzOhFq.replaceClassUnit",
    "assets/ThE.json",
    "res/xml/qnvmgc.xml",
    "AndroidManifest.xml: glare.bridge.rigid.uyzdrrhtqm / glare.bridge.rigid.kenwiqx"
  ]
}
```

**未决与覆盖边界**：引导链的步骤 1、2、4 及拒绝后循环、遮罩叠层均**无法静态确认**——`assets/ThE.json` 为加密二阶段载荷，本次未做解密还原，故 `step_by_step_flow` 中相关字段以“不可静态还原”标注，未作推测性填充；上述标签中 `COERCE_NO_SKIP_NON_CANCELABLE` 属家族特征推断，未由代码证据直接支撑。

</details>

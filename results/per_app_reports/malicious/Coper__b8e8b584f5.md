# MB_045__b8e8b584f5｜Coper — Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：186.1s

## 1. 一句话核心结论

- **核心申请方式**：以“Chrome”名义注册同名无障碍服务（无说明文字）并由动态加载载荷在运行期推送引导与跳转，明文包内仅剩组件壳与加密资产。
- **静态可见性说明**：仅 Manifest 组件布局、应用/服务显示名（Chrome）与资源表残桩字符串可静态确认；classes.dex 内不存在 com.involve.* 与 com.upon.front.* 实现，无障碍服务、启动 Activity、设置跳转与引导 UI 代码全部缺失；无障碍配置 XML（res/xml/dyruxlcc.xml、lfdqvgts.xml）及 assets/data.json、AFWfEd.json、BhF39pvP.js、v1-boot_loader.jsa、AW/AU/AX/AZ/AR.json 均为加密条目；resources.arsc 被替换为 1.7KB 残桩（APKEditor EDIT_TYPE=PROTECTED）；解密与落地由混淆 JNI 的 libvixt.so 承担。
- **命中的行为模式标签**：`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b8e8b584f5de2f13818e7068fb5e2063c18c644667a9909d79bb7ddec76a0468` |
| 包名 / 年份 | `com.upon.front` / 2025 |
| 家族 / 品类 | **Coper**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Chrome |
| 引导页宣称品牌/身份 | Google Chrome（系统浏览器品牌冒名） |
| 系统无障碍列表服务名 | Chrome |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务与启动 Activity 共用同一 label 资源 @7F030001（值为 Chrome）实现品牌冒名；无障碍服务 android:description 完全缺失，系统列表内无任何权限用途说明；LAUNCHER Activity 设 excludeFromRecents=true 隐藏最近任务；资源表被裁剪为残桩、DEX 无对应实现，形成“声明的组件静态不可见”的规避效果 |
| 无障碍服务类名 | `com.involve.p024l` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.involve.p045l（唯一 LAUNCHER Activity，label=Chrome，screenOrientation=10，excludeFromRecents=true） | 桌面图标点击 ACTION_MAIN/CATEGORY_LAUNCHER 冷启动 | 不可静态还原 | 无 | 不可静态还原 | `AndroidManifest.xml: activity com.involve.p045l` |
| 2 | 引导说明页 | 预期为加密资产驱动的页面（assets/BhF39pvP.js、assets/data.json、assets/AFWfEd.json 之一），载体无法确认 | 不可静态还原 | 不可静态还原 | **原文**：Erişebilirlik Servisileri Etkinleştirme<br>**译注**：启用无障碍服务（土耳其语；该字符串仅残留于被裁剪的 resources.arsc 字符串池，说明原应用存在“启用无障碍服务”引导文案） | 不可静态还原（原文提示为引导用户启用无障碍服务） | `resources.arsc 残桩字符串池（原 string 资源）` |
| 3 | 跳无障碍设置 | 系统设置无障碍页（android.settings.ACCESSIBILITY_SETTINGS） | 不可静态还原（明文 DEX 无 ACTION_ACCESSIBILITY_SETTINGS 引用，跳转由动态加载代码发起） | 系统无障碍页 | 无 | 在系统无障碍列表中打开“Chrome”服务开关（推断） | `AndroidManifest.xml: service com.involve.p024l` |
| 4 | 获权后动作 | com.involve.p024l 无障碍服务 + com.involve.p092o 通知监听服务 + com.involve.p083p 短信接管服务 | 服务在系统设置中被启用后由系统绑定 | 不可静态还原 | 无 | 无 | `AndroidManifest.xml: services com.involve.p024l / p092o / p083p` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务名显示为 “Chrome”（label 资源 @7F030001），且无 android:description，故不展示任何用途说明
- 应用桌面/最近任务显示名：@7F030001 = “Chrome”（application 与 LAUNCHER Activity com.involve.p045l 共用）
- 被裁剪 resources.arsc 中残留的引导文案 “Erişebilirlik Servisileri Etkinleştirme”，原属应用字符串资源，实际渲染位置由加密资产（data.json / AFWfEd.json / BhF39pvP.js）在运行期决定，静态不可见
- 加密资产 assets/data.json、AFWfEd.json、BhF39pvP.js、v1-boot_loader.jsa 为最可能的本地 HTML/JS 引导页或说明弹窗内容载体（不可解密读取）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Erişebilirlik Servisileri Etkinleştirme | 启用无障碍服务 | `resources.arsc 残桩字符串池（原 res/values 字符串，键不可恢复）` | 受限设置分步教学 |
| en | Chrome | Chrome（浏览器品牌名） | `resources.arsc 字符串池，被 application、LAUNCHER Activity 与无障碍服务共用的 label @7F030001` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：拒权/返回逻辑位于动态加载载荷，明文 DEX 无相关 Activity 生命周期回调实现
- **遮罩叠层 / 高仿系统设置页**：不可静态还原（资源表残桩中残留 Theme.AppCompat.Transparent.NoActionBar，提示原应用存在透明主题页面，可能用于遮罩式引导，但无代码证据确认）
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：不可静态还原
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动进入唯一 LAUNCHER com.involve.p045l 后立即开始连续截屏；并以 Activity 栈出现 Settings$AccessibilitySettings / Settings$InstalledAccessibilityServiceDetail 或 ApplicationDetailsSettingsActivity 的时刻作为关键锚点，随后继续抓取 1–2 秒内的叠层与返回重跳
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：无障碍配置 XML 与全部引导资产（data.json、AFWfEd.json、BhF39pvP.js、v1-boot_loader.jsa 等）为加密条目，classes.dex 中无 com.involve.* 实现，跳转与拒权循环完全依赖 libvixt.so 解密落地后反射加载；若首屏仅展示图片/GIF 引导，UTG 需 OCR。静态加壳不阻挡运行期 UTG，故必须依赖运行期抓取才能给出逐步流程。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首屏（唯一入口 Activity）** | com.involve.p045l 窗口，label 显示 Chrome，横屏（screenOrientation=10），不出现在最近任务 | 明文 DEX 无该类实现，首屏必为动态加载载荷渲染，是判定引导文案载体（原生/WebView/远端）的唯一入口 | 窗口标题/状态栏是否显示 Chrome；首屏是否含“启用无障碍服务”类文案及语言（土耳其语）；是否存在 WebView 特征（滚动容器、URL 栏、外链） |
| **系统无障碍服务列表项** | Settings 无障碍页中名为 Chrome 的服务项，副标题为空 | 直接证明品牌冒名与无用途说明，是“系统列表内身份混淆”的客观证据 | 服务名文本 = Chrome；描述文本为空/缺失；是否伴随遮罩或悬浮层覆盖 |
| **跳转前引导/教学页** | 设置跳转前的原生 Dialog 或 WebView 页，文案含“启用无障碍服务”指引 | 区分“良性透明说明”与“分步教唆开启高危权限”的关键页面 | 是否提供取消/跳过按钮；是否出现“点右上角菜单/允许受限设置”类步骤；文案是否使用故障/风险恐吓或隐私承诺 |
| **返回设置页后的叠层与重跳** | 从系统设置返回后立即出现的 Activity 或悬浮窗，可能是透明主题页面 | 验证拒权循环与遮罩压栈，这是恶意诱导与良性降级的核心分界 | 返回后是否自动重跳设置页及间隔；是否有半透明遮罩/悬浮窗叠在设置页上；是否有自点确认或阻止撤权行为 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `AndroidManifest.xml: service com.involve.p024l（BIND_ACCESSIBILITY_SERVICE，label=@7F030001=Chrome，meta-data android.accessibilityservice=@7F050001，无 description）`
- `AndroidManifest.xml: activity com.involve.p045l（唯一 LAUNCHER，excludeFromRecents=true，screenOrientation=10）`
- `AndroidManifest.xml: services com.involve.p092o（NotificationListenerService）、com.involve.p083p（导出 RESPOND_VIA_MESSAGE，短信接管）`
- `resources.arsc（1780B 残桩，含 Chrome 与 Erişebilirlik Servisileri Etkinleştirme、Theme.AppCompat.Transparent.NoActionBar、EDIT_TYPE=PROTECTED）`
- `lib/arm64-v8a/libvixt.so（混淆 JNI Java_com_nameown12_…、fopen/fwrite、jbyteArray 解密落地桩）`
- `assets/BhF39pvP.js、assets/AFWfEd.json、assets/data.json、assets/v1-boot_loader.jsa（加密，不可静态读取）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（已到工具调用上限，基于已核实证据停止）

**核心事实**

1. **Manifest 声明了完整的“无障碍家族”，但代码主体不在包内。** 无障碍服务为 `com.involve.p024l`（`BIND_ACCESSIBILITY_SERVICE`，`android:label="@7F030001"` 即“Chrome”，`meta-data android.accessibilityservice=@7F050001`，**无 `android:description`**）；唯一 LAUNCHER 入口为 `com.involve.p045l`（同样 label=Chrome，`excludeFromRecents="true"`、`screenOrientation="10"`）；另有 `com.involve.p092o`（NotificationListenerService）、`com.involve.p083p`（导出且 `RESPOND_VIA_MESSAGE`，可接管短信）、`LogSrv` 等。见 [Manifest 组件声明](<resource-unit:#1 manifest:components>)。
2. **`classes.dex`（6.2 MB）中不存在任何 `com.involve.*` / `com.upon.front.*` 类。** 反编译可见的全部是 bitmovin/gigya/grindr/intercom 等第三方 SDK 与 `com.upon.become.*` 混淆类（例如 [Aoilsteak](<resource-unit:#1.dex1 code:com.upon.become.Aoilsteak>)）。也就是说，Manifest 声明的启动 Activity 与无障碍服务在可读 DEX 中**无实现**，只能由运行期动态加载补入。
3. **资源表被替换为 1.7 KB 的残桩。** `resources.arsc` 只剩字符串池残片，含 `Chrome`、`Erişebilirlik Servisileri Etkinleştirme`（土耳其语“启用无障碍服务”）、`Theme.AppCompat.Transparent.NoActionBar`，以及 `EDIT_TYPE=PROTECTED`、`APKEditor VERSION=1.3.9` 的加工痕迹；无障碍配置 XML（`res/xml/dyruxlcc.xml`、`lfdqvgts.xml`）在包内是加密条目。
4. **全部引导用资产为加密条目**：`assets/data.json`、`assets/AFWfEd.json`、`assets/BhF39pvP.js`、`assets/v1-boot_loader.jsa`、`assets/AW.json/AU.json/AX.json/AZ.json/AR.json` 均带加密标志位，无法静态读取——即“引导页/说明文案/跳转脚本”最可能就藏在这里。
5. **解密/落地桩在原生层**：`libvixt.so` 仅 51 KB，导出 `Java_com_nameown12_…` 混淆 JNI 与 `MFZjJcBGPkzc`/`rrYAVdWrImnRdwJ` 混淆符号，并导入 `fopen/fwrite/strstr/strncpy` 与 `jbyteArray` 方法，符合“解密 + 写文件 + 反射加载”的 loader 特征。见 [libvixt.so](<resource-unit:#1 file:lib/arm64-v8a/libvixt.so>)。
6. 可读 DEX 内**搜不到 `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` / `DexClassLoader`**，跳转与加载逻辑不在明文层，无法给出静态可证的逐步页面流转。

**因此**：该样本属于**强动态加载 + 资产加密 + 资源表残桩**形态（静态预筛“未加壳”判断不成立）。可确认的是伪装身份与组件布局（`Chrome` 显示名 + 无障碍服务名同为 `Chrome` 且无说明文字，属系统/品牌冒名），但“如何一步步引导开启无障碍”的具体 UI 载体、文案与拒权循环**无法静态还原**，需以 UTG 在运行期抓取。

**UTG 建议触发点**：冷启动进入唯一 LAUNCHER `com.involve.p045l` 后，监测到系统无障碍设置页（`Settings$AccessibilitySettings` / `InstalledAccessibilityServiceDetail`）或应用详情页压栈瞬间，以及随后返回时的 Activity 重跳。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "仅 Manifest 组件布局、应用/服务显示名（Chrome）与资源表残桩字符串可静态确认；classes.dex 内不存在 com.involve.* 与 com.upon.front.* 实现，无障碍服务、启动 Activity、设置跳转与引导 UI 代码全部缺失；无障碍配置 XML（res/xml/dyruxlcc.xml、lfdqvgts.xml）及 assets/data.json、AFWfEd.json、BhF39pvP.js、v1-boot_loader.jsa、AW/AU/AX/AZ/AR.json 均为加密条目；resources.arsc 被替换为 1.7KB 残桩（APKEditor EDIT_TYPE=PROTECTED）；解密与落地由混淆 JNI 的 libvixt.so 承担。",
  "summary_one_liner": "以“Chrome”名义注册同名无障碍服务（无说明文字）并由动态加载载荷在运行期推送引导与跳转，明文包内仅剩组件壳与加密资产。",
  "disguise_identity": {
    "app_display_name": "Chrome",
    "claimed_brand_or_persona": "Google Chrome（系统浏览器品牌冒名）",
    "a11y_service_label": "Chrome",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务与启动 Activity 共用同一 label 资源 @7F030001（值为 Chrome）实现品牌冒名；无障碍服务 android:description 完全缺失，系统列表内无任何权限用途说明；LAUNCHER Activity 设 excludeFromRecents=true 隐藏最近任务；资源表被裁剪为残桩、DEX 无对应实现，形成“声明的组件静态不可见”的规避效果"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.involve.p045l（唯一 LAUNCHER Activity，label=Chrome，screenOrientation=10，excludeFromRecents=true）",
      "trigger_event": "桌面图标点击 ACTION_MAIN/CATEGORY_LAUNCHER 冷启动",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该 Activity 的实现类不在 classes.dex 中，界面内容需运行期由加密资产加载后渲染",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml: activity com.involve.p045l"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "预期为加密资产驱动的页面（assets/BhF39pvP.js、assets/data.json、assets/AFWfEd.json 之一），载体无法确认",
      "trigger_event": "不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Erişebilirlik Servisileri Etkinleştirme",
      "shown_text_zh": "启用无障碍服务（土耳其语；该字符串仅残留于被裁剪的 resources.arsc 字符串池，说明原应用存在“启用无障碍服务”引导文案）",
      "user_action_requested": "不可静态还原（原文提示为引导用户启用无障碍服务）",
      "code_anchor": "resources.arsc 残桩字符串池（原 string 资源）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置无障碍页（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "不可静态还原（明文 DEX 无 ACTION_ACCESSIBILITY_SETTINGS 引用，跳转由动态加载代码发起）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "跳转代码不在明文层，仅能从 Manifest 声明的无障碍服务推断其目标页",
      "user_action_requested": "在系统无障碍列表中打开“Chrome”服务开关（推断）",
      "code_anchor": "AndroidManifest.xml: service com.involve.p024l"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.involve.p024l 无障碍服务 + com.involve.p092o 通知监听服务 + com.involve.p083p 短信接管服务",
      "trigger_event": "服务在系统设置中被启用后由系统绑定",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后行为实现不在明文 DEX，需运行期 Hook/UTG 观测",
      "user_action_requested": "无",
      "code_anchor": "AndroidManifest.xml: services com.involve.p024l / p092o / p083p"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务名显示为 “Chrome”（label 资源 @7F030001），且无 android:description，故不展示任何用途说明",
    "应用桌面/最近任务显示名：@7F030001 = “Chrome”（application 与 LAUNCHER Activity com.involve.p045l 共用）",
    "被裁剪 resources.arsc 中残留的引导文案 “Erişebilirlik Servisileri Etkinleştirme”，原属应用字符串资源，实际渲染位置由加密资产（data.json / AFWfEd.json / BhF39pvP.js）在运行期决定，静态不可见",
    "加密资产 assets/data.json、AFWfEd.json、BhF39pvP.js、v1-boot_loader.jsa 为最可能的本地 HTML/JS 引导页或说明弹窗内容载体（不可解密读取）"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Erişebilirlik Servisileri Etkinleştirme",
      "text_zh": "启用无障碍服务",
      "source_location": "resources.arsc 残桩字符串池（原 res/values 字符串，键不可恢复）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Chrome",
      "text_zh": "Chrome（浏览器品牌名）",
      "source_location": "resources.arsc 字符串池，被 application、LAUNCHER Activity 与无障碍服务共用的 label @7F030001",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：拒权/返回逻辑位于动态加载载荷，明文 DEX 无相关 Activity 生命周期回调实现",
    "overlay_or_fake_settings": "不可静态还原（资源表残桩中残留 Theme.AppCompat.Transparent.NoActionBar，提示原应用存在透明主题页面，可能用于遮罩式引导，但无代码证据确认）",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "不可静态还原",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动进入唯一 LAUNCHER com.involve.p045l 后立即开始连续截屏；并以 Activity 栈出现 Settings$AccessibilitySettings / Settings$InstalledAccessibilityServiceDetail 或 ApplicationDetailsSettingsActivity 的时刻作为关键锚点，随后继续抓取 1–2 秒内的叠层与返回重跳",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首屏（唯一入口 Activity）",
        "page_identifier": "com.involve.p045l 窗口，label 显示 Chrome，横屏（screenOrientation=10），不出现在最近任务",
        "why_most_useful": "明文 DEX 无该类实现，首屏必为动态加载载荷渲染，是判定引导文案载体（原生/WebView/远端）的唯一入口",
        "observable_utg_signals": ["窗口标题/状态栏是否显示 Chrome", "首屏是否含“启用无障碍服务”类文案及语言（土耳其语）", "是否存在 WebView 特征（滚动容器、URL 栏、外链）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中名为 Chrome 的服务项，副标题为空",
        "why_most_useful": "直接证明品牌冒名与无用途说明，是“系统列表内身份混淆”的客观证据",
        "observable_utg_signals": ["服务名文本 = Chrome", "描述文本为空/缺失", "是否伴随遮罩或悬浮层覆盖"]
      },
      {
        "page_role": "跳转前引导/教学页",
        "page_identifier": "设置跳转前的原生 Dialog 或 WebView 页，文案含“启用无障碍服务”指引",
        "why_most_useful": "区分“良性透明说明”与“分步教唆开启高危权限”的关键页面",
        "observable_utg_signals": ["是否提供取消/跳过按钮", "是否出现“点右上角菜单/允许受限设置”类步骤", "文案是否使用故障/风险恐吓或隐私承诺"]
      },
      {
        "page_role": "返回设置页后的叠层与重跳",
        "page_identifier": "从系统设置返回后立即出现的 Activity 或悬浮窗，可能是透明主题页面",
        "why_most_useful": "验证拒权循环与遮罩压栈，这是恶意诱导与良性降级的核心分界",
        "observable_utg_signals": ["返回后是否自动重跳设置页及间隔", "是否有半透明遮罩/悬浮窗叠在设置页上", "是否有自点确认或阻止撤权行为"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "存在显著盲区：无障碍配置 XML 与全部引导资产（data.json、AFWfEd.json、BhF39pvP.js、v1-boot_loader.jsa 等）为加密条目，classes.dex 中无 com.involve.* 实现，跳转与拒权循环完全依赖 libvixt.so 解密落地后反射加载；若首屏仅展示图片/GIF 引导，UTG 需 OCR。静态加壳不阻挡运行期 UTG，故必须依赖运行期抓取才能给出逐步流程。"
  },
  "behavior_pattern_tags": [
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "TRIG_COLD_START_BLOCK"
  ],
  "code_anchors": [
    "AndroidManifest.xml: service com.involve.p024l（BIND_ACCESSIBILITY_SERVICE，label=@7F030001=Chrome，meta-data android.accessibilityservice=@7F050001，无 description）",
    "AndroidManifest.xml: activity com.involve.p045l（唯一 LAUNCHER，excludeFromRecents=true，screenOrientation=10）",
    "AndroidManifest.xml: services com.involve.p092o（NotificationListenerService）、com.involve.p083p（导出 RESPOND_VIA_MESSAGE，短信接管）",
    "resources.arsc（1780B 残桩，含 Chrome 与 Erişebilirlik Servisileri Etkinleştirme、Theme.AppCompat.Transparent.NoActionBar、EDIT_TYPE=PROTECTED）",
    "lib/arm64-v8a/libvixt.so（混淆 JNI Java_com_nameown12_…、fopen/fwrite、jbyteArray 解密落地桩）",
    "assets/BhF39pvP.js、assets/AFWfEd.json、assets/data.json、assets/v1-boot_loader.jsa（加密，不可静态读取）"
  ]
}
```

**覆盖边界说明**：本次未写入 `record_risk` —— 该样本的引导流程关键证据（跳转代码、引导 UI、拒权循环）全部位于加密资产与动态加载载荷中，证据链未闭合，不符合“确认成立即登记”的条件；已确认的客观事实为“Chrome 同名无障碍服务 + 无说明文字 + 组件实现缺失 + 全量加密资产 + 混淆 loader”，可作为运行期 UTG 复核的定向基线。建议后续以动态分析补齐 `ACTION_ACCESSIBILITY_SETTINGS` 跳转与遮罩层证据后再定性。

</details>

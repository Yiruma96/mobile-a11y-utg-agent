# MB_043__28ffffe619｜SpyNote — NextGen mParivahan

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：132.8s

## 1. 一句话核心结论

- **核心申请方式**：以 com.tencent.mm 包名、'NextGen mParivahan' 显示名伪装，声明 priority=999 的无障碍服务并把系统列表描述资源留成 '...'，用透明无标题 Activity 承载 VMP 加密后的分步引导逻辑，把用户一步步带进系统无障碍页开启全量窗口读取权限。
- **静态可见性说明**：Manifest、无障碍服务配置(res/xml/۠ۡ.xml)、字符串与资源命名可静态还原；但包内不存在 classes.dex，业务 DEX 由 Apk-VM 3.1.16 VMP 整体加密（assets/protected_by_np/ApkvVmProtect_9b957f0d97344a659af2f44c851ab63a.txt），引导弹窗文案、ACTION_ACCESSIBILITY_SETTINGS 跳转、拒权重跳等运行期页面流转逻辑完全不可静态读取。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `28ffffe619b6ad1f6e023d90ee5e630b3a59cfb33179836e82a6c9fb729a10ec` |
| 包名 / 年份 | `com.tencent.mm` / 2026 |
| 家族 / 品类 | **SpyNote**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | NextGen mParivahan |
| 引导页宣称品牌/身份 | NextGen mParivahan（伪装为印度 mParivahan 政务应用），同时以 com.tencent.mm 冒充微信包名，字符串体系源自 WhatsApp |
| 系统无障碍列表服务名 | NextGen mParivahan（@string/APKTOOL_DUPLICATE_string_0x7f0c0043），系统列表描述为 '...' |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍 description 资源内容仅为 '...'，系统授权页不披露真实用途；2) 无障碍配置与字符串资源被统一改名为 GOOGLE_PLAY_SERVICES_VERSION_PROTECTION 假名，res/xml 文件名改用阿拉伯-印度数字同形字（۠ۡ.xml 等）；3) 大量 Activity 使用 android:label=" "（单个空格）与 Theme.Translucent.NoTitleBar + excludeFromRecents 隐藏界面；4) 存在标签为 'Play Store' 的 Activity 作诱饵；5) 无障碍配置内 settingsActivity 与 Manifest 声明的服务类不一致（套壳模板）；6) strings.xml 由 WhatsApp 全套字符串批量替换品牌词生成。 |
| 无障碍服务类名 | `com.tencent.xyuoexeixbmkhdiuwzzlkywraiijxbakemzouyxxqvwoqzzkwd2.ujbuxlwemwmejnfvhvumwzemklwolnrhcpffedvodubensvuhx6nSsAP24` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.tencent.xyuoexeixbmkhdiuwzzlkywraiijxbakemzouyxxqvwoqzzkwd2.ujbuxlwemwmejnfvhvumwzemklwolnrhcpffedvodubensvuhx6SJTMB87（MAIN/LAUNCHER，label=NextGen mParivahan，taskAffinity=app.one，Theme.Translucent.NoTitleBar） | 用户点击桌面图标触发 android.intent.action.MAIN（onCreate/onResume 后的具体分支不可静态还原） | 原生Activity | **原文**：NextGen mParivahan<br>**译注**：启动页以“NextGen mParivahan”品牌呈现，本身为透明无标题主题，页面内容不可静态还原 | 不可静态还原（壳内逻辑决定是否直接弹出授权引导） | `#1 manifest:components / ujbuxlwemwmejnfvhvumwzemklwolnrhcpffedvodubensvuhx6SJTMB87` |
| 2 | 引导说明页 | 无障碍服务配置指定的 settingsActivity（com.tencent...bnwqcbfdivrgyhtohmxkqtkoovtsrlnobopruetttrjjmtigvz3.mkkvwjwhlrbuijfrrxsledyrzkrtwhnzdoaidnvwmmejnwozjz17，与 Manifest 声明服务类不一致） | 由壳内引导逻辑调用，具体触发点（onCreate 直弹 / 定时器 / 功能触发）不可静态还原 | 不可静态还原 | **原文**：无（壳内文案未落盘明文）<br>**译注**：不可静态还原；工程内仅存 WhatsApp 改词后的权限说辞模板（如“NextGen mParivahan can send and receive SMS”） | 不可静态还原（是否提供取消/跳过按钮无法从资源层确认） | `#1 file:unknown/۠ۡ.xml（accessibility-service 配置）` |
| 3 | 跳无障碍设置 | 系统 Settings → Accessibility → 已安装服务列表（条目显示 “NextGen mParivahan / ...”） | 壳内代码调用 android.settings.ACCESSIBILITY_SETTINGS（字符串位于加密 DEX，静态不可见） | 系统无障碍页 | **原文**：NextGen mParivahan ...<br>**译注**：系统无障碍列表条目：服务名“NextGen mParivahan”，说明仅三个点，用户无从判断真实用途 | 用户手动进入设置并打开该服务开关（是否强制、是否可返回无法静态确认） | `#1 manifest:components（service android:label=@string/0x7f0c0043）/ #1 file:res/values/strings.xml` |
| 4 | 获权后动作 | 无障碍服务 ujbuxlwemwmejnfvhvumwzemklwolnrhcpffedvodubensvuhx6nSsAP24（accessibilityFlags + canRetrieveWindowContent=true，监听 packageNames） | 服务被系统绑定后 onServiceConnected / onAccessibilityEvent 回调（实现体在 VMP 内） | 不可静态还原 | 无 | 无需用户操作（后台静默执行） | `#1 file:unknown/۠ۡ.xml（canRetrieveWindowContent / accessibilityFlags）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目：android:label=@string/APKTOOL_DUPLICATE_string_0x7f0c0043 → "NextGen mParivahan"；android:description 引用 @string 0x7f0c0000，内容仅为 "..."（res/values/strings.xml）
- 桌面/最近任务：启动 Activity 标签 "NextGen mParivahan"，另有多个 Activity 标签为单个空格 " "，theme=@android:style/Theme.Translucent.NoTitleBar，excludeFromRecents=true
- 诱饵入口：一个 Activity 标签写作 "Play Store"（showForAllUsers=true，intent-filter com.tencent.mm.xyz）
- 字符串资源层：res/values/strings.xml 为 WhatsApp 全套文案替换品牌词后的版本（权限/账号/设备管理类说辞），无独立“无障碍引导”专属文案落盘
- 壳内引导页/弹窗/WebView 文案：位于 Apk-VM 3.1.16 加密 DEX，包内无 classes.dex，静态不可见

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | ... | 三个点（空白说明，故意不披露服务用途） | `res/values/strings.xml → GOOGLE_PLAY_SERVICES_VERSION_PROTECTION（id 0x7f0c0000，被无障碍 description 引用）` | 未知 |
| en | NextGen mParivahan | “NextGen mParivahan”（伪装为 mParivahan 政务应用品牌名） | `res/values/strings.xml → APKTOOL_DUPLICATE_string_0x7f0c0043（application/android:label 与无障碍 service android:label）` | 未知 |
| en | NextGen mParivahan can send and receive SMS | “NextGen mParivahan 可以发送和接收短信”（WhatsApp 原文按品牌词替换而来，用于权限说辞） | `res/values/strings.xml → APKTOOL_DUPLICATE_string_0x7f0c002d` | 隐私承诺 |
| en | Allow NextGen mParivahan for device admin | “允许 NextGen mParivahan 使用设备管理器”（诱导授予设备管理权限的文案模板） | `res/values/strings.xml → APKTOOL_DUPLICATE_string_0x7f0c0337` | 受限设置分步教学 |
| en | Secured by Apk Manager From Rizki Rizaldi Copyright 2022 :) | “由 Apk Manager（Rizki Rizaldi）加固，2022 年版权”（重打包工具残留声明） | `assets/classes.dex.dat` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态确认（引导与重跳逻辑位于 Apk-VM 3.1.16 加密 DEX，包内无 classes.dex）；Manifest 侧可见无障碍服务 stopWithTask=false、监听 BOOT_COMPLETED/REBOOT 且 priority=999，具备开机/重启后重新拉起诱导流程的结构条件。
- **遮罩叠层 / 高仿系统设置页**：未见高仿无障碍开关页资源；但应用持有 SYSTEM_ALERT_WINDOW 权限，且多个 Activity 使用 Theme.Translucent.NoTitleBar + showForAllUsers + turnScreenOn，具备在系统设置页上叠放透明引导层/悬浮窗的能力（具体叠层代码不可静态还原）。
- **Android 13+ 受限设置（Restricted Settings）应对**：不可静态还原（targetSdkVersion=29，包内未见针对 Android 13+ 受限设置的静态文案；若存在则在加密 DEX 内）。
- **获权后即时行为与防撤权机制**：不可静态确认；Manifest 显示无障碍服务 stopWithTask=false，并有 FOREGROUND_SERVICE、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、设备管理说辞字符串，具备抗撤权/常驻的结构条件，但 GLOBAL_ACTION_BACK/HOME 阻止撤权代码位于加密 DEX。
- **良性降级 / 替代方案**：无（未发现任何降级或替代路径说明）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：静态无法定位跳转点，纯 UTG 检测应在两个瞬间拉起：① 启动 Activity（…6SJTMB87）onResume 后首次出现非空节点树/弹窗时；② 监测到当前 Activity 变为 com.android.settings/.Settings$AccessibilitySettings（或 AccessibilityDetailsSettings）时立即抓取返回栈与遮罩层。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：一阶段即为 VMP（Apk-VM 3.1.16）整体加密，包内无 classes.dex，跳转与话术代码静态完全不可见；应用主题为 Theme.Translucent.NoTitleBar，截图可能呈黑屏/空白，必须以 UTG 节点树而非截图判读；另有标签为单个空格的 Activity 与 'Play Store' 诱饵入口，易被当作正常组件忽略；未见纯图空文本诱饵证据（unknown/ 下 jpg 未解密）。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗/说明页** | 透明主题 Activity（…6SJTMB87 或 settingsActivity 指向的混淆类）之上出现的 Dialog/全屏说明节点 | 此处是唯一的“话术层”，决定判定其属于诱导说明还是纯静默跳转 | 节点文本与按钮文案（是否含“启用/允许/去设置/下一步”）；是否存在取消/跳过按钮（isClickable 节点数量）；窗口是否为 translucent 覆盖层（activity 名 + 是否 fullscreen opaque=false） |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中条目文本 'NextGen mParivahan' 与说明 '...' | 直接证实系统侧零披露（空白 description），是身份混淆与知情缺失的关键证据 | 条目摘要文本是否仅 '...'；包名 com.tencent.mm 与显示名 NextGen mParivahan 的错位；服务开关切换前后的 UTG 节点变化 |
| **跳设置后叠加的遮罩/悬浮引导页** | SYSTEM_ALERT_WINDOW 类型的悬浮窗节点或 AccessibilitySettings 之上的非 settings 窗口 | 区分“教用户自己点开关”与“遮罩指引/伪造设置页”，是 UTG 最容易漏检的高危形态 | 窗口包名为 com.tencent.mm 但叠加在 settings 之上；手指引导动画/箭头/高亮遮罩节点；返回键行为是否被拦截（返回后仍在设置页） |
| **拒权返回后的反馈循环页** | 从设置页返回后重新出现的同一引导弹窗或再次跳转 ACCESSIBILITY_SETTINGS | 验证是否存在拒权死循环重跳，决定是否构成强制授权 | 返回后 1~3 秒内 activity 再次切到 settings 无障碍页；弹窗重复出现次数与是否有 dismiss 通道 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.tencent.xyuoexeixbmkhdiuwzzlkywraiijxbakemzouyxxqvwoqzzkwd2.ujbuxlwemwmejnfvhvumwzemklwolnrhcpffedvodubensvuhx6nSsAP24（Manifest 无障碍服务，priority=999）`
- `com.tencent.xyuoexeixbmkhdiuwzzlkywraiijxbakemzouyxxqvwoqzzkwd2.ujbuxlwemwmejnfvhvumwzemklwolnrhcpffedvodubensvuhx6SJTMB87（MAIN 启动 Activity，label=NextGen mParivahan）`
- `unknown/۠ۡ.xml（@xml/GOOGLE_PLAY_SERVICES_VERSION_PROTECTION 无障碍配置：canRetrieveWindowContent、packageNames、settingsActivity）`
- `res/values/strings.xml（0x7f0c0000='...' 空白描述；0x7f0c0043='NextGen mParivahan'；WhatsApp 改词文案）`
- `assets/protected_by_np/ApkvVmProtect_9b957f0d97344a659af2f44c851ab63a.txt（Apk-VM 3.1.16 加壳声明）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**核心事实（可静态确认）**

- **身份三重错位**：包名为 `com.tencent.mm`，应用标签与启动 Activity 标签均为 **"NextGen mParivahan"**，而 `assets/classes.dex.dat` 明文写着 `Secured by Apk Manager From Rizki Rizaldi Copyright 2022 :)`；`res/values/strings.xml` 是**整套 WhatsApp 字符串**，只是把品牌词统一替换成 "NextGen mParivahan"（如 "NextGen mParivahan can send and receive SMS"、"Allow NextGen mParivahan for device admin"），说明该包由第三方工具重打包。
- **无障碍服务声明**：`com.tencent...x6nSsAP24` 带有 `BIND_ACCESSIBILITY_SERVICE` 和 `intent-filter android:priority="999"`，配置指向伪装资源名 `@xml/GOOGLE_PLAY_SERVICES_VERSION_PROTECTION`（实际文件为同形字命名的 `۠ۡ.xml`）。解析该二进制 XML 后可见属性集：`description / settingsActivity / accessibilityEventTypes / packageNames / accessibilityFeedbackType / notificationTimeout / accessibilityFlags / canRetrieveWindowContent`，即具备**窗口内容抓取 + 全包名监听**能力。
- **系统无障碍列表文案被刻意留空**：`description` 属性引用 `0x7f0c0000`，而该字符串资源实际内容仅为 **"..."**（三个点）；服务 `android:label` 引用 `0x7f0c0043` = "NextGen mParivahan"。用户在被要求授权时，系统页只显示"NextGen mParivahan / ..."，不披露真实用途。
- **界面层伪装手段**：多数 Activity 使用 `android:label=" "`（单个空格）和 `@android:style/Theme.Translucent.NoTitleBar` 隐藏自身；`excludeFromRecents`、`showForAllUsers`、`turnScreenOn` 频繁使用；另有一个 Activity 标签写作 **"Play Store"**。无障碍配置里的 `settingsActivity` 指向一个与 Manifest 声明服务不同的混淆类，属于套壳模板特征。
- **业务代码整体不可见**：包内**没有任何 classes.dex**，`assets/protected_by_np/ApkvVmProtect_*.txt` 记录 `Function: Apk-VM / Version: 3.1.16 / ProtectTime: 2025-04-02`，全部 Java 逻辑（含引导文案、跳 `ACCESSIBILITY_SETTINGS` 的代码、拒权重跳逻辑）位于 VMP 加密体，无法静态还原。`res/xml`、`res/values` 资源名被阿拉伯-印度数字同形字与 `GOOGLE_PLAY_SERVICES_VERSION_PROTECTION` 等假名系统性替换。

**判断**：应用具备完整的无障碍诱导攻击结构（高优先级服务 + 空白 description + 透明页 + 品牌冒充），但**"如何一步步引导用户开启"的 UI 流程代码全部在 VMP 壳内**，只能给出 Manifest 与资源层可证的骨架，运行期页面流转必须靠 UTG 动态捕获。既有风险 [R-001](<resource-unit:#1 manifest:components>) 已登记该家族判定。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、无障碍服务配置(res/xml/۠ۡ.xml)、字符串与资源命名可静态还原；但包内不存在 classes.dex，业务 DEX 由 Apk-VM 3.1.16 VMP 整体加密（assets/protected_by_np/ApkvVmProtect_9b957f0d97344a659af2f44c851ab63a.txt），引导弹窗文案、ACTION_ACCESSIBILITY_SETTINGS 跳转、拒权重跳等运行期页面流转逻辑完全不可静态读取。",
  "summary_one_liner": "以 com.tencent.mm 包名、'NextGen mParivahan' 显示名伪装，声明 priority=999 的无障碍服务并把系统列表描述资源留成 '...'，用透明无标题 Activity 承载 VMP 加密后的分步引导逻辑，把用户一步步带进系统无障碍页开启全量窗口读取权限。",
  "disguise_identity": {
    "app_display_name": "NextGen mParivahan",
    "claimed_brand_or_persona": "NextGen mParivahan（伪装为印度 mParivahan 政务应用），同时以 com.tencent.mm 冒充微信包名，字符串体系源自 WhatsApp",
    "a11y_service_label": "NextGen mParivahan（@string/APKTOOL_DUPLICATE_string_0x7f0c0043），系统列表描述为 '...'",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍 description 资源内容仅为 '...'，系统授权页不披露真实用途；2) 无障碍配置与字符串资源被统一改名为 GOOGLE_PLAY_SERVICES_VERSION_PROTECTION 假名，res/xml 文件名改用阿拉伯-印度数字同形字（۠ۡ.xml 等）；3) 大量 Activity 使用 android:label=\" \"（单个空格）与 Theme.Translucent.NoTitleBar + excludeFromRecents 隐藏界面；4) 存在标签为 'Play Store' 的 Activity 作诱饵；5) 无障碍配置内 settingsActivity 与 Manifest 声明的服务类不一致（套壳模板）；6) strings.xml 由 WhatsApp 全套字符串批量替换品牌词生成。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.tencent.xyuoexeixbmkhdiuwzzlkywraiijxbakemzouyxxqvwoqzzkwd2.ujbuxlwemwmejnfvhvumwzemklwolnrhcpffedvodubensvuhx6SJTMB87（MAIN/LAUNCHER，label=NextGen mParivahan，taskAffinity=app.one，Theme.Translucent.NoTitleBar）",
      "trigger_event": "用户点击桌面图标触发 android.intent.action.MAIN（onCreate/onResume 后的具体分支不可静态还原）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "NextGen mParivahan",
      "shown_text_zh": "启动页以“NextGen mParivahan”品牌呈现，本身为透明无标题主题，页面内容不可静态还原",
      "user_action_requested": "不可静态还原（壳内逻辑决定是否直接弹出授权引导）",
      "code_anchor": "#1 manifest:components / ujbuxlwemwmejnfvhvumwzemklwolnrhcpffedvodubensvuhx6SJTMB87"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "无障碍服务配置指定的 settingsActivity（com.tencent...bnwqcbfdivrgyhtohmxkqtkoovtsrlnobopruetttrjjmtigvz3.mkkvwjwhlrbuijfrrxsledyrzkrtwhnzdoaidnvwmmejnwozjz17，与 Manifest 声明服务类不一致）",
      "trigger_event": "由壳内引导逻辑调用，具体触发点（onCreate 直弹 / 定时器 / 功能触发）不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（壳内文案未落盘明文）",
      "shown_text_zh": "不可静态还原；工程内仅存 WhatsApp 改词后的权限说辞模板（如“NextGen mParivahan can send and receive SMS”）",
      "user_action_requested": "不可静态还原（是否提供取消/跳过按钮无法从资源层确认）",
      "code_anchor": "#1 file:unknown/۠ۡ.xml（accessibility-service 配置）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统 Settings → Accessibility → 已安装服务列表（条目显示 “NextGen mParivahan / ...”）",
      "trigger_event": "壳内代码调用 android.settings.ACCESSIBILITY_SETTINGS（字符串位于加密 DEX，静态不可见）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "NextGen mParivahan ...",
      "shown_text_zh": "系统无障碍列表条目：服务名“NextGen mParivahan”，说明仅三个点，用户无从判断真实用途",
      "user_action_requested": "用户手动进入设置并打开该服务开关（是否强制、是否可返回无法静态确认）",
      "code_anchor": "#1 manifest:components（service android:label=@string/0x7f0c0043）/ #1 file:res/values/strings.xml"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 ujbuxlwemwmejnfvhvumwzemklwolnrhcpffedvodubensvuhx6nSsAP24（accessibilityFlags + canRetrieveWindowContent=true，监听 packageNames）",
      "trigger_event": "服务被系统绑定后 onServiceConnected / onAccessibilityEvent 回调（实现体在 VMP 内）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后读取全屏窗口内容并执行模拟点击/窃取等动作，具体行为不可静态还原",
      "user_action_requested": "无需用户操作（后台静默执行）",
      "code_anchor": "#1 file:unknown/۠ۡ.xml（canRetrieveWindowContent / accessibilityFlags）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目：android:label=@string/APKTOOL_DUPLICATE_string_0x7f0c0043 → \"NextGen mParivahan\"；android:description 引用 @string 0x7f0c0000，内容仅为 \"...\"（res/values/strings.xml）",
    "桌面/最近任务：启动 Activity 标签 \"NextGen mParivahan\"，另有多个 Activity 标签为单个空格 \" \"，theme=@android:style/Theme.Translucent.NoTitleBar，excludeFromRecents=true",
    "诱饵入口：一个 Activity 标签写作 \"Play Store\"（showForAllUsers=true，intent-filter com.tencent.mm.xyz）",
    "字符串资源层：res/values/strings.xml 为 WhatsApp 全套文案替换品牌词后的版本（权限/账号/设备管理类说辞），无独立“无障碍引导”专属文案落盘",
    "壳内引导页/弹窗/WebView 文案：位于 Apk-VM 3.1.16 加密 DEX，包内无 classes.dex，静态不可见"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "...",
      "text_zh": "三个点（空白说明，故意不披露服务用途）",
      "source_location": "res/values/strings.xml → GOOGLE_PLAY_SERVICES_VERSION_PROTECTION（id 0x7f0c0000，被无障碍 description 引用）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "NextGen mParivahan",
      "text_zh": "“NextGen mParivahan”（伪装为 mParivahan 政务应用品牌名）",
      "source_location": "res/values/strings.xml → APKTOOL_DUPLICATE_string_0x7f0c0043（application/android:label 与无障碍 service android:label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "NextGen mParivahan can send and receive SMS",
      "text_zh": "“NextGen mParivahan 可以发送和接收短信”（WhatsApp 原文按品牌词替换而来，用于权限说辞）",
      "source_location": "res/values/strings.xml → APKTOOL_DUPLICATE_string_0x7f0c002d",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow NextGen mParivahan for device admin",
      "text_zh": "“允许 NextGen mParivahan 使用设备管理器”（诱导授予设备管理权限的文案模板）",
      "source_location": "res/values/strings.xml → APKTOOL_DUPLICATE_string_0x7f0c0337",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Secured by Apk Manager From Rizki Rizaldi Copyright 2022 :)",
      "text_zh": "“由 Apk Manager（Rizki Rizaldi）加固，2022 年版权”（重打包工具残留声明）",
      "source_location": "assets/classes.dex.dat",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态确认（引导与重跳逻辑位于 Apk-VM 3.1.16 加密 DEX，包内无 classes.dex）；Manifest 侧可见无障碍服务 stopWithTask=false、监听 BOOT_COMPLETED/REBOOT 且 priority=999，具备开机/重启后重新拉起诱导流程的结构条件。",
    "overlay_or_fake_settings": "未见高仿无障碍开关页资源；但应用持有 SYSTEM_ALERT_WINDOW 权限，且多个 Activity 使用 Theme.Translucent.NoTitleBar + showForAllUsers + turnScreenOn，具备在系统设置页上叠放透明引导层/悬浮窗的能力（具体叠层代码不可静态还原）。",
    "restricted_settings_13plus_coaching": "不可静态还原（targetSdkVersion=29，包内未见针对 Android 13+ 受限设置的静态文案；若存在则在加密 DEX 内）。",
    "post_grant_anti_removal": "不可静态确认；Manifest 显示无障碍服务 stopWithTask=false，并有 FOREGROUND_SERVICE、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、设备管理说辞字符串，具备抗撤权/常驻的结构条件，但 GLOBAL_ACTION_BACK/HOME 阻止撤权代码位于加密 DEX。",
    "benign_graceful_degradation": "无（未发现任何降级或替代路径说明）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "静态无法定位跳转点，纯 UTG 检测应在两个瞬间拉起：① 启动 Activity（…6SJTMB87）onResume 后首次出现非空节点树/弹窗时；② 监测到当前 Activity 变为 com.android.settings/.Settings$AccessibilitySettings（或 AccessibilityDetailsSettings）时立即抓取返回栈与遮罩层。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗/说明页",
        "page_identifier": "透明主题 Activity（…6SJTMB87 或 settingsActivity 指向的混淆类）之上出现的 Dialog/全屏说明节点",
        "why_most_useful": "此处是唯一的“话术层”，决定判定其属于诱导说明还是纯静默跳转",
        "observable_utg_signals": ["节点文本与按钮文案（是否含“启用/允许/去设置/下一步”）", "是否存在取消/跳过按钮（isClickable 节点数量）", "窗口是否为 translucent 覆盖层（activity 名 + 是否 fullscreen opaque=false）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中条目文本 'NextGen mParivahan' 与说明 '...'",
        "why_most_useful": "直接证实系统侧零披露（空白 description），是身份混淆与知情缺失的关键证据",
        "observable_utg_signals": ["条目摘要文本是否仅 '...'", "包名 com.tencent.mm 与显示名 NextGen mParivahan 的错位", "服务开关切换前后的 UTG 节点变化"]
      },
      {
        "page_role": "跳设置后叠加的遮罩/悬浮引导页",
        "page_identifier": "SYSTEM_ALERT_WINDOW 类型的悬浮窗节点或 AccessibilitySettings 之上的非 settings 窗口",
        "why_most_useful": "区分“教用户自己点开关”与“遮罩指引/伪造设置页”，是 UTG 最容易漏检的高危形态",
        "observable_utg_signals": ["窗口包名为 com.tencent.mm 但叠加在 settings 之上", "手指引导动画/箭头/高亮遮罩节点", "返回键行为是否被拦截（返回后仍在设置页）"]
      },
      {
        "page_role": "拒权返回后的反馈循环页",
        "page_identifier": "从设置页返回后重新出现的同一引导弹窗或再次跳转 ACCESSIBILITY_SETTINGS",
        "why_most_useful": "验证是否存在拒权死循环重跳，决定是否构成强制授权",
        "observable_utg_signals": ["返回后 1~3 秒内 activity 再次切到 settings 无障碍页", "弹窗重复出现次数与是否有 dismiss 通道"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "一阶段即为 VMP（Apk-VM 3.1.16）整体加密，包内无 classes.dex，跳转与话术代码静态完全不可见；应用主题为 Theme.Translucent.NoTitleBar，截图可能呈黑屏/空白，必须以 UTG 节点树而非截图判读；另有标签为单个空格的 Activity 与 'Play Store' 诱饵入口，易被当作正常组件忽略；未见纯图空文本诱饵证据（unknown/ 下 jpg 未解密）。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.tencent.xyuoexeixbmkhdiuwzzlkywraiijxbakemzouyxxqvwoqzzkwd2.ujbuxlwemwmejnfvhvumwzemklwolnrhcpffedvodubensvuhx6nSsAP24（Manifest 无障碍服务，priority=999）",
    "com.tencent.xyuoexeixbmkhdiuwzzlkywraiijxbakemzouyxxqvwoqzzkwd2.ujbuxlwemwmejnfvhvumwzemklwolnrhcpffedvodubensvuhx6SJTMB87（MAIN 启动 Activity，label=NextGen mParivahan）",
    "unknown/۠ۡ.xml（@xml/GOOGLE_PLAY_SERVICES_VERSION_PROTECTION 无障碍配置：canRetrieveWindowContent、packageNames、settingsActivity）",
    "res/values/strings.xml（0x7f0c0000='...' 空白描述；0x7f0c0043='NextGen mParivahan'；WhatsApp 改词文案）",
    "assets/protected_by_np/ApkvVmProtect_9b957f0d97344a659af2f44c851ab63a.txt（Apk-VM 3.1.16 加壳声明）"
  ]
}
```

</details>

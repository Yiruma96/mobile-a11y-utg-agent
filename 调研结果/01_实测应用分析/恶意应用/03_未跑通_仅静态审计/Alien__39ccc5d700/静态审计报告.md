# MB_027__39ccc5d700｜Alien — video

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：207.5s

## 1. 一句话核心结论

- **核心申请方式**：以中性名 video 声明的无障碍服务实现体完全藏于 assets/Rk.json 加密载荷、由 Application.attachBaseContext 动态装载，系统列表无任何用途描述，上层代码中不含无障碍设置跳转实现。
- **静态可见性说明**：Manifest、无障碍服务配置 XML、桌面/服务名、权限与引导素材（assets/qidao、notify_p、xintiao）静态可见；但无障碍服务实现类 com.mhiauaqmlacl.ypmsfwbkjhsbeoz.ojfiq 及全部 com.mhiauaqmlacl.* 组件在 classes.dex 中无任何定义，DEX 检索 AccessibilityService / ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / 无障碍 均为 0 命中。Application 类 attachBaseContext 经混淆方法链解密 244KB 非 JSON 密文 assets/Rk.json 并配合 DexClassLoader 动态装载，引导弹窗文案、跳转点与拒权循环逻辑全部位于该加密二阶段载荷内，静态不可还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `39ccc5d7009aefac18891c70a16b857b98481d6f69800075e31900c4dc9ef000` |
| 包名 / 年份 | `com.escape.glad` / 2023 |
| 家族 / 品类 | **Alien**（同池样本数：1） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | video |
| 引导页宣称品牌/身份 | video（中性词伪装，内部残留 GBWhatsApp / com.plutus.market 金融行情命名素材） |
| 系统无障碍列表服务名 | video |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务无 android:description（系统列表零说明）；服务标签与桌面名同为通用词 video；包名 com.escape.glad 与全部类名为随机字母串（如 NXsLiObTjHxMbOhSzWdEbDiAsNrMuDzPp）；attachBaseContext 内填充大量无副作用算术与循环垃圾指令对抗反编译；含 label="" 且 Theme.NoDisplay / excludeFromRecents 的不可见 Activity（gwsbwjljwqx、lwmcrlixkvo、gtzkggpuaqjntiao）；服务实现类整体从可见 DEX 移除并加密动态装载 |
| 无障碍服务类名 | `com.mhiauaqmlacl.ypmsfwbkjhsbeoz.ojfiq` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | Application com.escape.glad.NXsLiObTjHxMbOhSzWdEbDiAsNrMuDzPp（attachBaseContext） | 进程启动时 attachBaseContext 回调 | 不可静态还原 | 无 | 无 | `com.escape.glad.NXsLiObTjHxMbOhSzWdEbDiAsNrMuDzPp.attachBaseContext → centuryculture / inputarm / antennarubber / gaugepear` |
| 2 | 引导说明页 | 解密载荷内的引导界面（疑似原生弹窗，布局标识 notify_permission_layout / notify_permission_title_name / notify_permission_tv_allow / notify_permission_tv_cancel / notify_permission_tv_info） | 无法静态确认（载荷解密后动态注册） | 不可静态还原 | **原文**：无（DEX 中仅存布局字段名 notify_permission_title_name、notify_permission_tv_allow、notify_permission_tv_cancel，具体文案随载荷下发）<br>**译注**：布局命名表明存在「标题 + 允许 / 取消 / 说明」结构的权限引导弹窗，含取消按钮 | 疑似点击「允许」进入系统无障碍设置；存在取消项但实际行为不可静态确认 | `assets/Rk.json（解密载荷） + 布局字符串 notify_permission_layout / notify_permission_tv_allow / notify_permission_tv_cancel` |
| 3 | 引导说明页 | 分步图文引导素材 assets/qidao/img_0.png ~ img_11.png（另含 xintiao、notify_p 系列） | 无法静态确认（由载荷内界面加载） | 不可静态还原 | **原文**：无（素材为纯图片，无对应文本资源）<br>**译注**：12 张分步示意图，用途为逐屏演示操作步骤（据命名与体量判断为权限/功能开启教学图） | 引导用户按图逐步操作 | `assets/qidao/img_0.png … img_11.png` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（预期） | 无法静态确认 | 系统无障碍页 | **原文**：无（DEX 中不存在 ACCESSIBILITY_SETTINGS 常量）<br>**译注**：系统无障碍设置列表中将显示服务项「video」，且无任何用途描述 | 用户需在列表中手动找到「video」并打开开关 | `res/xml/kxtxfwkalotsegdc.xml + AndroidManifest.xml（service android:label="video"，无 android:description）` |
| 5 | 获权后动作 | 无障碍服务 com.mhiauaqmlacl.ypmsfwbkjhsbeoz.ojfiq（实现体在加密载荷内） | 服务被系统绑定后 onServiceConnected / onAccessibilityEvent（typeWindowStateChanged、typeWindowContentChanged） | 不可静态还原 | 无 | 无 | `res/xml/kxtxfwkalotsegdc.xml（canRetrieveWindowContent=true, flagReportViewIds）+ 载荷内 com.mhiauaqmlacl.ypmsfwbkjhsbeoz.ojfiq` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表：服务项名称「video」（AndroidManifest.xml 中 service android:label="video"），android:description 缺失，列表内无任何用途说明文字
- 载荷内原生权限引导弹窗：布局资源标识 notify_permission_layout / notify_permission_title_name / notify_permission_tv_allow / notify_permission_tv_cancel / notify_permission_tv_info（DEX 仅保留字段名，文案随 assets/Rk.json 解密载荷下发）
- 分步图文教学：assets/qidao/img_0.png ~ img_11.png（纯图片、无文本资源，需 OCR 才能读取内容）
- 辅助素材目录：assets/xintiao/（img_0~img_5.png）、assets/notify_p/（img_0~img_1.png）
- 本地 WebView 前端：assets/2.f93ccaa4.chunk.js（297KB React/jQuery 打包，其中无 accessibility/permission 相关文案）
- 桌面图标名称「video」（application android:label="video"，无其他 activity-alias 伪装）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | video | 视频 | `AndroidManifest.xml：application android:label 与 service android:label` | 清理工具伪装 |
| en | notify_permission_title_name / notify_permission_tv_allow / notify_permission_tv_cancel / notify_permission_tv_info | 通知权限标题 / 允许 / 取消 / 说明（仅字段名，实际文案位于加密载荷） | `classes.dex 资源字段名（布局标识）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无法静态确认：拒绝或返回系统设置后的重跳逻辑位于 assets/Rk.json 解密载荷内，可见 DEX 中不存在 ACCESSIBILITY_SETTINGS 跳转与 onResume 轮询实现
- **遮罩叠层 / 高仿系统设置页**：无法静态确认：已声明 SYSTEM_ALERT_WINDOW 权限且存在 Theme.NoDisplay 的 excludeFromRecents 不可见 Activity，具备叠加悬浮引导层与伪造设置页的能力，但具体实现不在可见代码中
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=29，低于 Android 13 受限设置门槛；可见 DEX 中亦无 APPLICATION_DETAILS_SETTINGS 跳转实现）
- **获权后即时行为与防撤权机制**：无法静态确认：载荷内是否自点确认或监听设置页阻止撤权不可见；Manifest 另行注册了 BIND_DEVICE_ADMIN 设备管理器 receiver（res/xml/ozjbjkrbn）与通知监听服务，具备抗卸载/抗撤权的组件基础
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后立即开始 UTG 轮询（应用自带引导素材 assets/qidao 12 张图与 notify_permission_* 弹窗布局，提示引导发生在启动早期）；同时在检测到顶层包名从 com.escape.glad 切换为 com.android.settings 时以 200~800ms 间隔连续抓取，覆盖跳转前的弹窗页与跳转后的系统无障碍列表
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：存在三重盲区：①无障碍服务实现类与全部引导逻辑经 assets/Rk.json（244KB 密文）解密后动态装载，静态完全不可见，无法预知文案与跳转方式；②引导素材 assets/qidao/img_*.png 为纯图片无文本资源，UTG 文本通道取不到内容，必须 OCR；③存在 label="" + Theme.NoDisplay + excludeFromRecents 的不可见 Activity 与 SYSTEM_ALERT_WINDOW 权限，若引导以透明悬浮层叠加在系统设置页之上，UTG 可能同时抓到应用悬浮窗与系统页两个 window，需按 window 层级区分。（注：本样本无静态加壳，Manifest/资源层完整可见，运行期 UTG 不受加壳阻挡。）

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后首次出现的权限引导弹窗页** | com.escape.glad 进程内的 Dialog/Activity，含标题 + 允许 + 取消 三段文本结构（布局对应 notify_permission_title_name / notify_permission_tv_allow / notify_permission_tv_cancel） | 这是判定「是否以欺骗性理由诱导开启无障碍」的唯一文案来源，静态完全缺失，必须运行期取证 | 弹窗全部文本（标题、正文、按钮）；是否存在取消/跳过按钮及其可见性；弹窗是否不可取消（无返回响应）；弹窗背景是否为应用界面或系统设置仿真图 |
| **跳转前分步图文教学页** | 承载 assets/qidao/img_0~img_11.png 的界面（ImageView/WebView 轮播） | 图片内含具体操作指引文字，是纯图空文本诱导的关键证据，UTG 无法直接取文本时必须截图 OCR | 界面是否为纯图片无文本节点；是否有「下一步」推进按钮；图片内容是否复刻系统无障碍设置界面 |
| **跳转后的系统无障碍服务列表项** | com.android.settings 无障碍页面中 label 为「video」的列表项 | 确认服务项显示名无任何用途描述，且确认应用确实跳转至该页而非伪造页面 | 列表项文本是否仅「video」而无 description 副标题；页面包名是否为 com.android.settings（排除高仿页）；开关切换后是否自动返回应用 |
| **返回/拒权后的反馈页** | 用户按返回键离开系统设置后应用重新显示的界面 | 判定是否构成拒权死循环（onResume 重跳或定时器拉起），这是强制引导的核心特征 | 返回后是否再次弹出同一引导弹窗；弹窗重现的时间间隔；是否出现「必须开启才能使用」类阻断文案 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.escape.glad.NXsLiObTjHxMbOhSzWdEbDiAsNrMuDzPp.attachBaseContext`
- `com.escape.glad.NXsLiObTjHxMbOhSzWdEbDiAsNrMuDzPp.gaugepear / centuryculture / antennarubber`
- `res/xml/kxtxfwkalotsegdc.xml`
- `AndroidManifest.xml（service com.mhiauaqmlacl.ypmsfwbkjhsbeoz.ojfiq，label="video"，无 android:description）`
- `assets/Rk.json`
- `assets/qidao/img_0.png ~ img_11.png`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，13 次工具调用内收口）

**核心发现：无障碍引导链在静态层面被完整切断，引导流程位于加密二阶段载荷内。**

1. **Manifest 层可确认的引导前置条件**
   - 无障碍服务 `com.mhiauaqmlacl.ypmsfwbkjhsbeoz.ojfiq`，`android:label="video"`（与桌面显示名 `video` 完全一致），`BIND_ACCESSIBILITY_SERVICE` 权限，配置为 [kxtxfwkalotsegdc.xml](<resource-unit:#1 file:res/xml/kxtxfwkalotsegdc.xml>)：仅 `typeWindowContentChanged|typeWindowStateChanged` + `canRetrieveWindowContent="true"` + `flagReportViewIds`，即"读全屏内容+按 viewId 定位控件"的自动化操作型能力，**未声明 `android:description`**——系统无障碍列表中将没有任何用途说明文字。
   - 同时声明 `SYSTEM_ALERT_WINDOW`、`REQUEST_INSTALL_PACKAGES`、`READ_SMS`/`RECEIVE_SMS`/`SEND_SMS`、`READ_CONTACTS`、`RECORD_AUDIO`、`QUERY_ALL_PACKAGES`，并抢注 `android.app.role.SMS` 默认短信角色；还有设备管理器 receiver、`Theme.NoDisplay` 无界面 Activity（`gwsbwjljwqx`、`lwmcrlixkvo`）、通知监听服务。该组合指向 Alien 家族的短信拦截 + 无障碍自动化 + 假应用投递能力。

2. **服务实现类在可见 DEX 中根本不存在（关键判定）**
   - 对 `classes.dex` 原始字节检索：`com/mhiauaqmlacl`、`ypmsfwb`、`ojfiq`、`AccessibilityService`、`kxtxfwkalotsegdc` 命中次数**均为 0**；DEX 内只有 `com.escape.*`、`com.cow.*`、`com.gbwhatsapp.*` 三组包。
   - 应用类 [NXsLiObTjHxMbOhSzWdEbDiAsNrMuDzPp#attachBaseContext](<resource-unit:#1.dex1 code:com.escape.glad.NXsLiObTjHxMbOhSzWdEbDiAsNrMuDzPp#attachBaseContext>) 填充大量无副作用算术/循环垃圾指令，并在 `super.attachBaseContext` 前后串接 `toiletbecome → husbandmaster → centuryculture → inputarm → antennarubber → gaugepear` 混淆方法链（读取资源→解密→落盘→装载），DEX 内存在 `DexClassLoader` 引用；`assets/Rk.json` 244392 字节、文件头 `3d e2 ff da`，非 JSON 明文，即加密载荷。
   - 结论：`ojfiq` 及 Manifest 中其余 `com.mhiauaqmlacl.*` 组件均由 `Rk.json` 解密后动态装载。

3. **跳转点与引导文案在上层代码中检索为空**
   - `android.settings.ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`ACTION_MANAGE_OVERLAY_PERMISSION`、`isAccessibilityServiceEnabled`、`无障碍`、`辅助功能`、`开启`、`授权` 在 DEX 中命中**均为 0**；唯一 `android.settings` 常量是 `INTERNAL_STORAGE_SETTINGS`（SDK 内部残留）。
   - 但**引导素材已备齐**：`assets/qidao/img_0~img_11.png`（12 张分步图文）、`assets/xintiao/`、`assets/notify_p/`、`assets/npci/npci_otp_rules.json`；布局字符串 `notify_permission_layout`、`notify_permission_title_name`、`notify_permission_tv_allow`、`notify_permission_tv_cancel`、`notify_permission_tv_info` 说明存在"标题+允许/取消"的原生权限引导弹窗（带取消按钮），`assets/2.f93ccaa4.chunk.js`（297KB，jQuery/React 打包）为本地 WebView 前端，但其中无 accessibility/permission 相关文案，权限引导文案随远程/解密载荷下发。

4. **身份伪装**：桌面名 `video`、无障碍服务标签 `video`，均为中性词；包名 `com.escape.glad` 与类名全为随机字母串；内部残留 `com.gbwhatsapp`、`Share/GBWhatsApp.apk`、`com.plutus.market` 等金融/通讯应用命名，属冒名素材残留。

5. **覆盖边界**：引导弹窗具体文案、跳转触发时机（冷启动/功能触发）、拒权后重跳逻辑、获权后滥用行为，均位于 `Rk.json` 解密载荷内，静态不可还原；本次未启动动态分析（未验证在线设备），标注 `packed_or_encrypted`。

**已登记风险**：R-001（medium，malware_trojan）——无障碍服务实现类由加密资源动态加载，引导流程不可静态还原。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、无障碍服务配置 XML、桌面/服务名、权限与引导素材（assets/qidao、notify_p、xintiao）静态可见；但无障碍服务实现类 com.mhiauaqmlacl.ypmsfwbkjhsbeoz.ojfiq 及全部 com.mhiauaqmlacl.* 组件在 classes.dex 中无任何定义，DEX 检索 AccessibilityService / ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / 无障碍 均为 0 命中。Application 类 attachBaseContext 经混淆方法链解密 244KB 非 JSON 密文 assets/Rk.json 并配合 DexClassLoader 动态装载，引导弹窗文案、跳转点与拒权循环逻辑全部位于该加密二阶段载荷内，静态不可还原。",
  "summary_one_liner": "以中性名 video 声明的无障碍服务实现体完全藏于 assets/Rk.json 加密载荷、由 Application.attachBaseContext 动态装载，系统列表无任何用途描述，上层代码中不含无障碍设置跳转实现。",
  "disguise_identity": {
    "app_display_name": "video",
    "claimed_brand_or_persona": "video（中性词伪装，内部残留 GBWhatsApp / com.plutus.market 金融行情命名素材）",
    "a11y_service_label": "video",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务无 android:description（系统列表零说明）；服务标签与桌面名同为通用词 video；包名 com.escape.glad 与全部类名为随机字母串（如 NXsLiObTjHxMbOhSzWdEbDiAsNrMuDzPp）；attachBaseContext 内填充大量无副作用算术与循环垃圾指令对抗反编译；含 label=\"\" 且 Theme.NoDisplay / excludeFromRecents 的不可见 Activity（gwsbwjljwqx、lwmcrlixkvo、gtzkggpuaqjntiao）；服务实现类整体从可见 DEX 移除并加密动态装载"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "Application com.escape.glad.NXsLiObTjHxMbOhSzWdEbDiAsNrMuDzPp（attachBaseContext）",
      "trigger_event": "进程启动时 attachBaseContext 回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该阶段无界面输出，仅执行资源读取、解密与二阶段代码装载",
      "user_action_requested": "无",
      "code_anchor": "com.escape.glad.NXsLiObTjHxMbOhSzWdEbDiAsNrMuDzPp.attachBaseContext → centuryculture / inputarm / antennarubber / gaugepear"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "解密载荷内的引导界面（疑似原生弹窗，布局标识 notify_permission_layout / notify_permission_title_name / notify_permission_tv_allow / notify_permission_tv_cancel / notify_permission_tv_info）",
      "trigger_event": "无法静态确认（载荷解密后动态注册）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（DEX 中仅存布局字段名 notify_permission_title_name、notify_permission_tv_allow、notify_permission_tv_cancel，具体文案随载荷下发）",
      "shown_text_zh": "布局命名表明存在「标题 + 允许 / 取消 / 说明」结构的权限引导弹窗，含取消按钮",
      "user_action_requested": "疑似点击「允许」进入系统无障碍设置；存在取消项但实际行为不可静态确认",
      "code_anchor": "assets/Rk.json（解密载荷） + 布局字符串 notify_permission_layout / notify_permission_tv_allow / notify_permission_tv_cancel"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "分步图文引导素材 assets/qidao/img_0.png ~ img_11.png（另含 xintiao、notify_p 系列）",
      "trigger_event": "无法静态确认（由载荷内界面加载）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（素材为纯图片，无对应文本资源）",
      "shown_text_zh": "12 张分步示意图，用途为逐屏演示操作步骤（据命名与体量判断为权限/功能开启教学图）",
      "user_action_requested": "引导用户按图逐步操作",
      "code_anchor": "assets/qidao/img_0.png … img_11.png"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（预期）",
      "trigger_event": "无法静态确认",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（DEX 中不存在 ACCESSIBILITY_SETTINGS 常量）",
      "shown_text_zh": "系统无障碍设置列表中将显示服务项「video」，且无任何用途描述",
      "user_action_requested": "用户需在列表中手动找到「video」并打开开关",
      "code_anchor": "res/xml/kxtxfwkalotsegdc.xml + AndroidManifest.xml（service android:label=\"video\"，无 android:description）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 com.mhiauaqmlacl.ypmsfwbkjhsbeoz.ojfiq（实现体在加密载荷内）",
      "trigger_event": "服务被系统绑定后 onServiceConnected / onAccessibilityEvent（typeWindowStateChanged、typeWindowContentChanged）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务具备读取全屏窗口内容与按 viewId 定位控件的能力，可实施跨应用自动点击与短信/凭据读取，具体行为不可静态还原",
      "user_action_requested": "无",
      "code_anchor": "res/xml/kxtxfwkalotsegdc.xml（canRetrieveWindowContent=true, flagReportViewIds）+ 载荷内 com.mhiauaqmlacl.ypmsfwbkjhsbeoz.ojfiq"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表：服务项名称「video」（AndroidManifest.xml 中 service android:label=\"video\"），android:description 缺失，列表内无任何用途说明文字",
    "载荷内原生权限引导弹窗：布局资源标识 notify_permission_layout / notify_permission_title_name / notify_permission_tv_allow / notify_permission_tv_cancel / notify_permission_tv_info（DEX 仅保留字段名，文案随 assets/Rk.json 解密载荷下发）",
    "分步图文教学：assets/qidao/img_0.png ~ img_11.png（纯图片、无文本资源，需 OCR 才能读取内容）",
    "辅助素材目录：assets/xintiao/（img_0~img_5.png）、assets/notify_p/（img_0~img_1.png）",
    "本地 WebView 前端：assets/2.f93ccaa4.chunk.js（297KB React/jQuery 打包，其中无 accessibility/permission 相关文案）",
    "桌面图标名称「video」（application android:label=\"video\"，无其他 activity-alias 伪装）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "video",
      "text_zh": "视频",
      "source_location": "AndroidManifest.xml：application android:label 与 service android:label",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "notify_permission_title_name / notify_permission_tv_allow / notify_permission_tv_cancel / notify_permission_tv_info",
      "text_zh": "通知权限标题 / 允许 / 取消 / 说明（仅字段名，实际文案位于加密载荷）",
      "source_location": "classes.dex 资源字段名（布局标识）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无法静态确认：拒绝或返回系统设置后的重跳逻辑位于 assets/Rk.json 解密载荷内，可见 DEX 中不存在 ACCESSIBILITY_SETTINGS 跳转与 onResume 轮询实现",
    "overlay_or_fake_settings": "无法静态确认：已声明 SYSTEM_ALERT_WINDOW 权限且存在 Theme.NoDisplay 的 excludeFromRecents 不可见 Activity，具备叠加悬浮引导层与伪造设置页的能力，但具体实现不在可见代码中",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=29，低于 Android 13 受限设置门槛；可见 DEX 中亦无 APPLICATION_DETAILS_SETTINGS 跳转实现）",
    "post_grant_anti_removal": "无法静态确认：载荷内是否自点确认或监听设置页阻止撤权不可见；Manifest 另行注册了 BIND_DEVICE_ADMIN 设备管理器 receiver（res/xml/ozjbjkrbn）与通知监听服务，具备抗卸载/抗撤权的组件基础",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后立即开始 UTG 轮询（应用自带引导素材 assets/qidao 12 张图与 notify_permission_* 弹窗布局，提示引导发生在启动早期）；同时在检测到顶层包名从 com.escape.glad 切换为 com.android.settings 时以 200~800ms 间隔连续抓取，覆盖跳转前的弹窗页与跳转后的系统无障碍列表",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后首次出现的权限引导弹窗页",
        "page_identifier": "com.escape.glad 进程内的 Dialog/Activity，含标题 + 允许 + 取消 三段文本结构（布局对应 notify_permission_title_name / notify_permission_tv_allow / notify_permission_tv_cancel）",
        "why_most_useful": "这是判定「是否以欺骗性理由诱导开启无障碍」的唯一文案来源，静态完全缺失，必须运行期取证",
        "observable_utg_signals": ["弹窗全部文本（标题、正文、按钮）", "是否存在取消/跳过按钮及其可见性", "弹窗是否不可取消（无返回响应）", "弹窗背景是否为应用界面或系统设置仿真图"]
      },
      {
        "page_role": "跳转前分步图文教学页",
        "page_identifier": "承载 assets/qidao/img_0~img_11.png 的界面（ImageView/WebView 轮播）",
        "why_most_useful": "图片内含具体操作指引文字，是纯图空文本诱导的关键证据，UTG 无法直接取文本时必须截图 OCR",
        "observable_utg_signals": ["界面是否为纯图片无文本节点", "是否有「下一步」推进按钮", "图片内容是否复刻系统无障碍设置界面"]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页面中 label 为「video」的列表项",
        "why_most_useful": "确认服务项显示名无任何用途描述，且确认应用确实跳转至该页而非伪造页面",
        "observable_utg_signals": ["列表项文本是否仅「video」而无 description 副标题", "页面包名是否为 com.android.settings（排除高仿页）", "开关切换后是否自动返回应用"]
      },
      {
        "page_role": "返回/拒权后的反馈页",
        "page_identifier": "用户按返回键离开系统设置后应用重新显示的界面",
        "why_most_useful": "判定是否构成拒权死循环（onResume 重跳或定时器拉起），这是强制引导的核心特征",
        "observable_utg_signals": ["返回后是否再次弹出同一引导弹窗", "弹窗重现的时间间隔", "是否出现「必须开启才能使用」类阻断文案"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "存在三重盲区：①无障碍服务实现类与全部引导逻辑经 assets/Rk.json（244KB 密文）解密后动态装载，静态完全不可见，无法预知文案与跳转方式；②引导素材 assets/qidao/img_*.png 为纯图片无文本资源，UTG 文本通道取不到内容，必须 OCR；③存在 label=\"\" + Theme.NoDisplay + excludeFromRecents 的不可见 Activity 与 SYSTEM_ALERT_WINDOW 权限，若引导以透明悬浮层叠加在系统设置页之上，UTG 可能同时抓到应用悬浮窗与系统页两个 window，需按 window 层级区分。（注：本样本无静态加壳，Manifest/资源层完整可见，运行期 UTG 不受加壳阻挡。）"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.escape.glad.NXsLiObTjHxMbOhSzWdEbDiAsNrMuDzPp.attachBaseContext",
    "com.escape.glad.NXsLiObTjHxMbOhSzWdEbDiAsNrMuDzPp.gaugepear / centuryculture / antennarubber",
    "res/xml/kxtxfwkalotsegdc.xml",
    "AndroidManifest.xml（service com.mhiauaqmlacl.ypmsfwbkjhsbeoz.ojfiq，label=\"video\"，无 android:description）",
    "assets/Rk.json",
    "assets/qidao/img_0.png ~ img_11.png"
  ]
}
```

</details>

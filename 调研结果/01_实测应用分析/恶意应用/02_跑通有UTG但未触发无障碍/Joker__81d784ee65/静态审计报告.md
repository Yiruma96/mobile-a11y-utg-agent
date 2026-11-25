# MR_027__81d784ee65｜Joker — Reward Clean

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：119.8s

## 1. 一句话核心结论

- **核心申请方式**：以『清理加速需要权限』为名，在清理/加速功能被点击时弹出原生对话框宣称『绝对安全』，点 Enable 后裸跳系统无障碍设置页，并用无障碍服务描述文字教用户打开右上角开关，获权后实际只在 Play 商店页自动点星打 5 分、点 SUBMIT/ACCEPT/INSTALL。
- **静态可见性说明**：无障碍引导与点击机器逻辑全部位于 classes.dex 明文 Java（com.starlight.cleaner.*），无加壳、无加密资产、无远端 HTML 引导页；assets/full_licenses.html 仅为 OpenVPN 开源许可文本，与引导链路无关。仅 fmu 埋点上报端点未在本轮追至服务端。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `81d784ee65a8dc113683cd7cc271a36da275a500621cefa187095951af3a5114` |
| 包名 / 年份 | `com.building.castle.bster` / 2019 |
| 家族 / 品类 | **Joker**（同池样本数：4） |
| 原始来源标识 | https://medium.com/csis-techblog/analysis-of-joker-a-spy-premium-subscription-bot-on-googleplay-9ad24f044451 |
| 桌面显示名 | Reward Clean |
| 引导页宣称品牌/身份 | Reward Clean（手机垃圾清理/内存加速/省电工具） |
| 系统无障碍列表服务名 | Reward Clean |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名为 com.building.castle.bster，与清理工具品牌无关联；Manifest 内并行存在多别名入口 GameLauncher（android:label="Solitaire"，Gdx 游戏壳）与 StarActivity（android:label="Promotion"，excludeFromRecents 广告页），构成多 activity-alias 换脸；无障碍服务本身未使用空白/同形字或伪造 isAccessibilityTool（代码中未出现该 API）。 |
| 无障碍服务类名 | `com.starlight.cleaner.device.ram.AccessibilityFroceService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.android.settings,com.android.vending |
| 共现高危权限 | `PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Tap the top right slider to enable Reward Clean Cleaning.<br><br>Enable to use:<br>1) Thorough Reward Clean junk and cache files cleaning<br>2) Effective phone boosting<br>3) Battery life extending<br><br>Attention: you may receive warnings about privacy - it is a standard Android OS procedure when enabling Accessibility Services. (Reward Clean does NOT collect any personal data) |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.starlight.cleaner.ui.activity.AliasLauncher（MAIN/LAUNCHER，桌面显示 Reward Clean）→ StartActivity → MainActivity | 用户点击桌面图标启动 | 原生Activity | **原文**：Reward Clean<br>**译注**：桌面图标名「Reward Clean」，呈现为手机清理/加速工具 | 点击图标启动应用（无权限请求） | `AndroidManifest.xml: AliasLauncher / StartActivity / MainActivity` |
| 2 | 业务功能触发 | com.starlight.cleaner.ui.fragment.CleanFragment（深度清理页）/ SpeedUpFragment2（加速页） | 点击清理/加速按钮 → cleanCache() / boost() 调用 fms.c.ac() / fms.a.ac() 判定未获无障碍权限 | 原生Activity | **原文**：Deep clean / Optimizing applications<br>**译注**：页面按钮分别为「深度清理」「优化应用」，功能看似普通清理工具 | 点击清理/加速按钮（功能本身不执行，先转权限引导） | `com.starlight.cleaner.ui.fragment.CleanFragment#cleanCache；SpeedUpFragment2#boost` |
| 3 | 引导说明页 | com.starlight.cleaner.fnm（自定义 DialogFragment，布局含 txt_title/txt_content/btn_positive/btn_close） | CleanFragment#a(fms) / SpeedUpFragment2#a(fms) 组装 fnm$a 后 fnm.a(...).a(getChildFragmentManager(), ...) 显示 | 原生Dialog | **原文**：Optimizing applications / Android %s user, we need your permission to clean %s more of RAM memory. It is entirely safe. / Enable<br>**译注**：标题「优化应用」（清理页为「深度清理」）；正文「Android %s 用户，我们需要您的授权才能再清理 %s 的内存。这完全安全。」；主按钮「Enable（启用）」；另有 btn_close 关闭按钮 | 点「Enable」继续（存在 btn_close 可关闭/放弃，但关闭后下次点功能仍会重弹） | `com.starlight.cleaner.fnm#onViewCreated；res/values/strings.xml#L650-L655` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | fnm 的 btn_positive onClick → 按 fms 枚举分支 case 2（ACCESSIBILITY）执行 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))，前后写入 fmu 埋点 fmj("ACCESSIBILITY","SCREEN_POSITIVE"/"SCREEN_SHOWN") | 系统无障碍页 | **原文**：无（应用侧无自定义文案，直接打开系统无障碍服务列表）<br>**译注**：跳到系统「无障碍 → 已下载的服务」列表，用户需自行找到 Reward Clean 并开启 | 在系统列表中点击 Reward Clean 并打开开关（应用未提供任何高仿开关页或遮罩） | `com.starlight.cleaner.ui.fragment.CleanFragment#a(fms,View)；SpeedUpFragment2#a(fms,View)` |
| 5 | 遮罩叠层指引 | 系统无障碍列表条目 com.starlight.cleaner.device.ram.AccessibilityFroceService（android:description） | 用户进入系统无障碍服务详情页时系统渲染该服务的 description | 系统无障碍页 | **原文**：Tap the top right slider to enable Reward Clean Cleaning.<br><br>Enable to use:<br>1) Thorough Reward Clean junk and cache files cleaning<br>2) Effective phone boosting<br>3) Battery life extending<br><br>Attention: you may receive warnings about privacy - it is a standard Android OS procedure when enabling Accessibility Services. (Reward Clean does NOT collect any personal data)<br>**译注**：「点右上角滑块即可开启 Reward Clean 清理。开启后可使用：1) 彻底的垃圾与缓存清理 2) 有效提速 3) 延长电池续航。注意：开启无障碍服务时你可能会看到隐私警告——这是 Android 系统的标准流程。（Reward Clean 不收集任何个人数据）」 | 按文字指引点右上角滑块开启；并被告知忽略系统隐私警告 | `res/xml/accessibilityconfig.xml: android:description=@string/accessibility_service_description；res/values/strings.xml#L67` |
| 6 | 拒权反馈循环 | com.starlight.cleaner.ui.fragment.MainFragment#onMessageEvent(com.starlight.cleaner.fnc)；SpeedUpFragment2#onCreate | EventBus 事件 fnc.yw==true 时再次 startActivity("android.settings.ACCESSIBILITY_SETTINGS")；SpeedUpFragment2.onCreate 检测服务未运行则 startService(AccessibilityFroceService) 预拉起 | 原生Activity / 系统无障碍页 | 无 | 重复开启或再次面对同一弹窗（每次点清理/加速功能都会重弹引导框） | `com.starlight.cleaner.ui.fragment.MainFragment#onMessageEvent；SpeedUpFragment2#onCreate` |
| 7 | 获权后动作 | com.starlight.cleaner.device.ram.AccessibilityFroceService（:accessibility 独立进程，packageNames 仅 com.android.settings 与 com.android.vending） | onAccessibilityEvent 收到 com.android.vending 的窗口内容变化事件 | 不可静态还原（后台服务行为，无界面） | **原文**：Contains ads / Rate this app / com.android.vending:id/star5 / com.android.vending:id/post_review_button / SUBMIT / ACCEPT / INSTALL<br>**译注**：在 Play 商店页面自动展开「包含广告」、自动点第 5 颗星（打 5 星好评）、自动点「提交评价」、自动点「接受」与「安装」按钮 | 无（后台静默模拟点击，用户界面在 Play 商店内被自动操作） | `com.starlight.cleaner.device.ram.AccessibilityFroceService#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 业务功能页：CleanFragment（Deep clean）/ SpeedUpFragment2（Optimizing applications）按钮文案，暗示普通清理加速功能
- 原生不可取消风险提示框：自定义 DialogFragment com.starlight.cleaner.fnm，标题 permission_dialog_title_boost/cache、正文 permission_dialog_content_boost/cache、主按钮 permission_dialog_enable_boost/cache（Enable），含 btn_close 关闭按钮
- 系统无障碍设置页：应用无自定义 UI，直接 startActivity("android.settings.ACCESSIBILITY_SETTINGS") 裸跳
- 系统无障碍列表/详情页 android:description：res/xml/accessibilityconfig.xml → @string/accessibility_service_description（『Tap the top right slider…』分步教学 + 忽视隐私警告 + 不收集数据承诺）
- 系统无障碍服务名：android:label=@string/app_name（Reward Clean），与桌面名一致
- Manifest 其他入口标签：GameLauncher（Solitaire）、StarActivity（Promotion）——与清理工具身份无关的换脸入口

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Optimizing applications | 优化应用 | `res/values/strings.xml key=permission_dialog_title_boost` | 清理工具伪装 |
| en | Deep clean | 深度清理 | `res/values/strings.xml key=permission_dialog_title_cache` | 清理工具伪装 |
| en | Android %s user, we need your permission to clean %s more of RAM memory. It is entirely safe. | Android %s 用户，我们需要您的授权，才能再多清理 %s 的内存。这完全安全。 | `res/values/strings.xml key=permission_dialog_content_boost / permission_dialog_content_cache（CleanFragment#a、SpeedUpFragment2#a 以 SDK 版本与剩余空间填充）` | 隐私承诺 |
| en | Enable | 启用 | `res/values/strings.xml key=permission_dialog_enable_boost / permission_dialog_enable_cache` | 清理工具伪装 |
| en | Tap the top right slider to enable Reward Clean Cleaning.<br><br>Enable to use:<br>1) Thorough Reward Clean junk and cache files cleaning<br>2) Effective phone boosting<br>3) Battery life extending<br><br>Attention: you may receive warnings about privacy - it is a standard Android OS procedure when enabling Accessibility Services. (Reward Clean does NOT collect any personal data) | 点右上角滑块即可开启 Reward Clean 清理。开启后可使用：1) 彻底的 Reward Clean 垃圾与缓存清理 2) 有效的手机提速 3) 延长电池续航。注意：开启无障碍服务时你可能会收到隐私警告——这是 Android 系统的标准流程。（Reward Clean 不收集任何个人数据） | `res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibilityconfig.xml 的 android:description 引用）` | 教唆忽视警告 |
| en | Solitaire | 纸牌（接龙游戏） | `AndroidManifest.xml: activity com.starlight.cleaner.GameLauncher android:label="Solitaire"` | 未知 |
| en | Promotion | 推广 | `AndroidManifest.xml: activity com.starlight.cleaner.ui.activity.StarActivity android:label="Promotion"` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无 onResume 死循环重跳证据；但存在两条复跳路径：(1) EventBus 事件 fnc.yw==true 时 MainFragment#onMessageEvent 再次 startActivity(ACCESSIBILITY_SETTINGS)；(2) 用户每次点击清理/加速功能都会重新走 cleanCache()/boost() 的权限判定并重弹同一个 fnm 引导框。跳转前后以 fmu.a(new fmj("ACCESSIBILITY","SCREEN_POSITIVE"/"SCREEN_SHOWN")) 埋点记录引导转化。
- **遮罩叠层 / 高仿系统设置页**：无。既不叠半透明引导遮罩，也不做高仿系统无障碍开关页，直接裸跳 android.settings.ACCESSIBILITY_SETTINGS；教学文字改放在系统无障碍服务的 android:description 内。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未发现『应用详情 → 右上角菜单 → 允许受限设置』的分步教学，本轮亦未定位到 SESSION_INSTALLER 相关引导代码；APPLICATION_DETAILS_SETTINGS 跳转仅用于 OosterService/CleanCacheService 动画结束后的应用详情页跳转与商店详情页）
- **获权后即时行为与防撤权机制**：本轮未证实自点确认或 GLOBAL_ACTION_BACK/HOME 撤权对抗；但无障碍配置的 packageNames 明确包含 com.android.settings，且 AccessibilityFroceService 含 onKeyEvent 与多个广播接收器，具备监听设置页的能力，属待验证项。
- **良性降级 / 替代方案**：无。未获无障碍权限时功能路径直接转权限引导，不存在手动清理/ADB/仅观看等替代降级路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（由 fnm 弹窗 Enable 点击触发），以及随后系统无障碍详情页渲染 com.starlight.cleaner.device.ram.AccessibilityFroceService 的 description 时；另可在冷启动后点击清理/加速按钮时前置抓取 fnm 弹窗。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无图空文本盲区：全部引导文字均为可读文本。需注意两点：(1) 跳转系统设置后应用侧不提供任何自定义 UI，若仅抓应用自身界面会漏掉『教学』其实位于 android:description 中，需专门抓系统无障碍详情页；(2) 获权后行为发生在 :accessibility 独立进程且作用于 Play 商店，需在商店页同时抓取无障碍点击事件才能与『清理功能』区分。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **功能触发的引导弹窗页** | DialogFragment 类名 com.starlight.cleaner.fnm，标题『Optimizing applications』或『Deep clean』，含 Enable 与关闭按钮 | 这是应用唯一自有的说明载体，可直接判定文案框架（清理伪装 + 完全安全承诺）与是否可取消 | 标题/正文/按钮文本全量可读；同一弹窗是否覆盖清理与加速两个不同功能；是否存在关闭按钮（btn_close） |
| **跳转前埋点与跳转动作** | CleanFragment/SpeedUpFragment2 内 fmj("ACCESSIBILITY","SCREEN_POSITIVE") 与随后的系统无障碍页 | 确认『点 Enable 即跳设置』的强绑定关系，并排除高仿页面可能 | 跳转目标包名为 com.android.settings 且 action 为 ACCESSIBILITY_SETTINGS；跳转后应用未叠加任何悬浮窗 |
| **系统无障碍服务列表项/详情页** | 服务名 Reward Clean，描述以『Tap the top right slider to enable Reward Clean Cleaning』开头 | 这是本案最关键的诱导点：把系统 description 当作教学页，并主动要求用户忽略隐私警告 | description 全文含『standard Android OS procedure』与『does NOT collect any personal data』；服务名与桌面名一致但包名 com.building.castle.bster 不一致；配置仅声明 com.android.settings/com.android.vending 两个包名 |
| **获权后 Play 商店自动点击页** | com.android.vending 评价页出现 star5 高亮、post_review_button/SUBMIT 被自动点击、INSTALL/ACCEPT 被自动点击 | 证明所申请的无障碍权限实际用于刷好评与自动确认安装，而非所述清理功能 | 星级从 0 跳到 5 且无用户触摸事件；评价提交按钮在无人操作下被触发；安装确认框被自动点 ACCEPT/INSTALL |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.starlight.cleaner.ui.fragment.CleanFragment#cleanCache`
- `com.starlight.cleaner.ui.fragment.CleanFragment#a(fms,View)`
- `com.starlight.cleaner.fnm#onViewCreated`
- `res/xml/accessibilityconfig.xml`
- `res/values/strings.xml#L650-L655`
- `com.starlight.cleaner.device.ram.AccessibilityFroceService#onAccessibilityEvent`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（运行期 UTG 视角，工具调用已收口）

**可见性**：纯 Java/DEX 实现，无障碍引导链路完整静态可见，无壳、无 AES/远端 HTML；`assets/full_licenses.html` 仅为 OpenVPN 开源许可文本，与引导无关。

**引导链路（三步）**
1. **业务功能触发**：用户在“深度清理/加速”页点击清理或加速按钮 → `cleanCache()` / `boost()` 先做权限判定 `fms.c.ac()` / `fms.a.ac()`，未获权则直接弹引导框。
2. **原生引导弹窗**：统一由 `fnm`（自定义 DialogFragment，布局 `txt_title/txt_content/btn_positive/btn_close`）呈现，标题「Optimizing applications」/「Deep clean」，正文「Android %s user, we need your permission to clean %s more of RAM memory. It is entirely safe.」，主按钮「Enable」，另有 `btn_close` 可关闭。文案框架是**清理工具伪装 + 隐私/安全承诺**（"It is entirely safe."）。
3. **跳受限设置**：`Enable` 的 onClick 按 `fms` 枚举分支：`ACCESSIBILITY` → `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，并在跳转前后埋点 `fmu.a(new fmj("ACCESSIBILITY","SCREEN_POSITIVE"/"SCREEN_SHOWN"))`；同一方法还处理 `OVERLAY` → `MANAGE_OVERLAY_PERMISSION`。**注意：直接裸跳系统无障碍列表，无高仿页面、无遮罩叠层、无分步截图教学。**

**设置页内的“教学”落在 android:description 上**：`res/xml/accessibilityconfig.xml` 的 `android:description` 直接写「Tap the top right slider to enable Reward Clean Cleaning…」，即把系统无障碍列表条目本身当作教学载体；同时声明 `packageNames="com.android.settings,com.android.vending"`、`canRetrieveWindowContent=true`、`flagRequestFilterKeyEvents` —— 只盯设置页和 Play 商店两个包名，功能上与“清理加速”无关。

**拒权/复跳**：未发现 onResume 死循环重跳或定时器强制拉起；但 `MainFragment.onMessageEvent(fnc)` 在 `fnc.yw==true` 时会**再跳一次** `ACCESSIBILITY_SETTINGS`（事件驱动二次拉起），且每次点功能按钮都会重弹对话框。`SpeedUpFragment2.onCreate` 还会 `startService(AccessibilityFroceService)`（对未授权无障碍服务无效，属探测/预拉起）。

**获权后的真实动作（与“清理”完全不符）**：`AccessibilityFroceService.onAccessibilityEvent` 只在 `com.android.vending` 事件里工作——展开 “Contains ads”、点 `com.android.vending:id/star5`（**自动打 5 星**）、点 `post_review_button`/`SUBMIT`、点 `ACCEPT`、点 `INSTALL`，并带 `removeMessages` 防抖与 1000/2000ms 延迟连点。这是刷好评/自动确认安装的点击机器人，而非 RAM 清理。

**身份伪装**：桌面名 `Reward Clean`、无障碍服务 label 同为 `Reward Clean`（一致），但包名 `com.building.castle.bster` 与“清理工具”无关；Manifest 另设 `GameLauncher`（label **Solitaire**）与 `StarActivity`（label **Promotion**）多别名入口，属多 alias 换脸。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导与点击机器逻辑全部位于 classes.dex 明文 Java（com.starlight.cleaner.*），无加壳、无加密资产、无远端 HTML 引导页；assets/full_licenses.html 仅为 OpenVPN 开源许可文本，与引导链路无关。仅 fmu 埋点上报端点未在本轮追至服务端。",
  "summary_one_liner": "以『清理加速需要权限』为名，在清理/加速功能被点击时弹出原生对话框宣称『绝对安全』，点 Enable 后裸跳系统无障碍设置页，并用无障碍服务描述文字教用户打开右上角开关，获权后实际只在 Play 商店页自动点星打 5 分、点 SUBMIT/ACCEPT/INSTALL。",
  "disguise_identity": {
    "app_display_name": "Reward Clean",
    "claimed_brand_or_persona": "Reward Clean（手机垃圾清理/内存加速/省电工具）",
    "a11y_service_label": "Reward Clean",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名为 com.building.castle.bster，与清理工具品牌无关联；Manifest 内并行存在多别名入口 GameLauncher（android:label=\"Solitaire\"，Gdx 游戏壳）与 StarActivity（android:label=\"Promotion\"，excludeFromRecents 广告页），构成多 activity-alias 换脸；无障碍服务本身未使用空白/同形字或伪造 isAccessibilityTool（代码中未出现该 API）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.starlight.cleaner.ui.activity.AliasLauncher（MAIN/LAUNCHER，桌面显示 Reward Clean）→ StartActivity → MainActivity",
      "trigger_event": "用户点击桌面图标启动",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Reward Clean",
      "shown_text_zh": "桌面图标名「Reward Clean」，呈现为手机清理/加速工具",
      "user_action_requested": "点击图标启动应用（无权限请求）",
      "code_anchor": "AndroidManifest.xml: AliasLauncher / StartActivity / MainActivity"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.starlight.cleaner.ui.fragment.CleanFragment（深度清理页）/ SpeedUpFragment2（加速页）",
      "trigger_event": "点击清理/加速按钮 → cleanCache() / boost() 调用 fms.c.ac() / fms.a.ac() 判定未获无障碍权限",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Deep clean / Optimizing applications",
      "shown_text_zh": "页面按钮分别为「深度清理」「优化应用」，功能看似普通清理工具",
      "user_action_requested": "点击清理/加速按钮（功能本身不执行，先转权限引导）",
      "code_anchor": "com.starlight.cleaner.ui.fragment.CleanFragment#cleanCache；SpeedUpFragment2#boost"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.starlight.cleaner.fnm（自定义 DialogFragment，布局含 txt_title/txt_content/btn_positive/btn_close）",
      "trigger_event": "CleanFragment#a(fms) / SpeedUpFragment2#a(fms) 组装 fnm$a 后 fnm.a(...).a(getChildFragmentManager(), ...) 显示",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Optimizing applications / Android %s user, we need your permission to clean %s more of RAM memory. It is entirely safe. / Enable",
      "shown_text_zh": "标题「优化应用」（清理页为「深度清理」）；正文「Android %s 用户，我们需要您的授权才能再清理 %s 的内存。这完全安全。」；主按钮「Enable（启用）」；另有 btn_close 关闭按钮",
      "user_action_requested": "点「Enable」继续（存在 btn_close 可关闭/放弃，但关闭后下次点功能仍会重弹）",
      "code_anchor": "com.starlight.cleaner.fnm#onViewCreated；res/values/strings.xml#L650-L655"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "fnm 的 btn_positive onClick → 按 fms 枚举分支 case 2（ACCESSIBILITY）执行 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))，前后写入 fmu 埋点 fmj(\"ACCESSIBILITY\",\"SCREEN_POSITIVE\"/\"SCREEN_SHOWN\")",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧无自定义文案，直接打开系统无障碍服务列表）",
      "shown_text_zh": "跳到系统「无障碍 → 已下载的服务」列表，用户需自行找到 Reward Clean 并开启",
      "user_action_requested": "在系统列表中点击 Reward Clean 并打开开关（应用未提供任何高仿开关页或遮罩）",
      "code_anchor": "com.starlight.cleaner.ui.fragment.CleanFragment#a(fms,View)；SpeedUpFragment2#a(fms,View)"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统无障碍列表条目 com.starlight.cleaner.device.ram.AccessibilityFroceService（android:description）",
      "trigger_event": "用户进入系统无障碍服务详情页时系统渲染该服务的 description",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Tap the top right slider to enable Reward Clean Cleaning.\n\nEnable to use:\n1) Thorough Reward Clean junk and cache files cleaning\n2) Effective phone boosting\n3) Battery life extending\n\nAttention: you may receive warnings about privacy - it is a standard Android OS procedure when enabling Accessibility Services. (Reward Clean does NOT collect any personal data)",
      "shown_text_zh": "「点右上角滑块即可开启 Reward Clean 清理。开启后可使用：1) 彻底的垃圾与缓存清理 2) 有效提速 3) 延长电池续航。注意：开启无障碍服务时你可能会看到隐私警告——这是 Android 系统的标准流程。（Reward Clean 不收集任何个人数据）」",
      "user_action_requested": "按文字指引点右上角滑块开启；并被告知忽略系统隐私警告",
      "code_anchor": "res/xml/accessibilityconfig.xml: android:description=@string/accessibility_service_description；res/values/strings.xml#L67"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.starlight.cleaner.ui.fragment.MainFragment#onMessageEvent(com.starlight.cleaner.fnc)；SpeedUpFragment2#onCreate",
      "trigger_event": "EventBus 事件 fnc.yw==true 时再次 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\")；SpeedUpFragment2.onCreate 检测服务未运行则 startService(AccessibilityFroceService) 预拉起",
      "ui_carrier": "原生Activity / 系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "用户返回后，事件驱动可再次把用户拉回无障碍设置页；未发现 onResume 死循环或定时器强制重跳",
      "user_action_requested": "重复开启或再次面对同一弹窗（每次点清理/加速功能都会重弹引导框）",
      "code_anchor": "com.starlight.cleaner.ui.fragment.MainFragment#onMessageEvent；SpeedUpFragment2#onCreate"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.starlight.cleaner.device.ram.AccessibilityFroceService（:accessibility 独立进程，packageNames 仅 com.android.settings 与 com.android.vending）",
      "trigger_event": "onAccessibilityEvent 收到 com.android.vending 的窗口内容变化事件",
      "ui_carrier": "不可静态还原（后台服务行为，无界面）",
      "shown_text_verbatim": "Contains ads / Rate this app / com.android.vending:id/star5 / com.android.vending:id/post_review_button / SUBMIT / ACCEPT / INSTALL",
      "shown_text_zh": "在 Play 商店页面自动展开「包含广告」、自动点第 5 颗星（打 5 星好评）、自动点「提交评价」、自动点「接受」与「安装」按钮",
      "user_action_requested": "无（后台静默模拟点击，用户界面在 Play 商店内被自动操作）",
      "code_anchor": "com.starlight.cleaner.device.ram.AccessibilityFroceService#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "业务功能页：CleanFragment（Deep clean）/ SpeedUpFragment2（Optimizing applications）按钮文案，暗示普通清理加速功能",
    "原生不可取消风险提示框：自定义 DialogFragment com.starlight.cleaner.fnm，标题 permission_dialog_title_boost/cache、正文 permission_dialog_content_boost/cache、主按钮 permission_dialog_enable_boost/cache（Enable），含 btn_close 关闭按钮",
    "系统无障碍设置页：应用无自定义 UI，直接 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\") 裸跳",
    "系统无障碍列表/详情页 android:description：res/xml/accessibilityconfig.xml → @string/accessibility_service_description（『Tap the top right slider…』分步教学 + 忽视隐私警告 + 不收集数据承诺）",
    "系统无障碍服务名：android:label=@string/app_name（Reward Clean），与桌面名一致",
    "Manifest 其他入口标签：GameLauncher（Solitaire）、StarActivity（Promotion）——与清理工具身份无关的换脸入口"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Optimizing applications",
      "text_zh": "优化应用",
      "source_location": "res/values/strings.xml key=permission_dialog_title_boost",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Deep clean",
      "text_zh": "深度清理",
      "source_location": "res/values/strings.xml key=permission_dialog_title_cache",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Android %s user, we need your permission to clean %s more of RAM memory. It is entirely safe.",
      "text_zh": "Android %s 用户，我们需要您的授权，才能再多清理 %s 的内存。这完全安全。",
      "source_location": "res/values/strings.xml key=permission_dialog_content_boost / permission_dialog_content_cache（CleanFragment#a、SpeedUpFragment2#a 以 SDK 版本与剩余空间填充）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable",
      "text_zh": "启用",
      "source_location": "res/values/strings.xml key=permission_dialog_enable_boost / permission_dialog_enable_cache",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Tap the top right slider to enable Reward Clean Cleaning.\n\nEnable to use:\n1) Thorough Reward Clean junk and cache files cleaning\n2) Effective phone boosting\n3) Battery life extending\n\nAttention: you may receive warnings about privacy - it is a standard Android OS procedure when enabling Accessibility Services. (Reward Clean does NOT collect any personal data)",
      "text_zh": "点右上角滑块即可开启 Reward Clean 清理。开启后可使用：1) 彻底的 Reward Clean 垃圾与缓存清理 2) 有效的手机提速 3) 延长电池续航。注意：开启无障碍服务时你可能会收到隐私警告——这是 Android 系统的标准流程。（Reward Clean 不收集任何个人数据）",
      "source_location": "res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibilityconfig.xml 的 android:description 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Solitaire",
      "text_zh": "纸牌（接龙游戏）",
      "source_location": "AndroidManifest.xml: activity com.starlight.cleaner.GameLauncher android:label=\"Solitaire\"",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Promotion",
      "text_zh": "推广",
      "source_location": "AndroidManifest.xml: activity com.starlight.cleaner.ui.activity.StarActivity android:label=\"Promotion\"",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无 onResume 死循环重跳证据；但存在两条复跳路径：(1) EventBus 事件 fnc.yw==true 时 MainFragment#onMessageEvent 再次 startActivity(ACCESSIBILITY_SETTINGS)；(2) 用户每次点击清理/加速功能都会重新走 cleanCache()/boost() 的权限判定并重弹同一个 fnm 引导框。跳转前后以 fmu.a(new fmj(\"ACCESSIBILITY\",\"SCREEN_POSITIVE\"/\"SCREEN_SHOWN\")) 埋点记录引导转化。",
    "overlay_or_fake_settings": "无。既不叠半透明引导遮罩，也不做高仿系统无障碍开关页，直接裸跳 android.settings.ACCESSIBILITY_SETTINGS；教学文字改放在系统无障碍服务的 android:description 内。",
    "restricted_settings_13plus_coaching": "无（未发现『应用详情 → 右上角菜单 → 允许受限设置』的分步教学，本轮亦未定位到 SESSION_INSTALLER 相关引导代码；APPLICATION_DETAILS_SETTINGS 跳转仅用于 OosterService/CleanCacheService 动画结束后的应用详情页跳转与商店详情页）",
    "post_grant_anti_removal": "本轮未证实自点确认或 GLOBAL_ACTION_BACK/HOME 撤权对抗；但无障碍配置的 packageNames 明确包含 com.android.settings，且 AccessibilityFroceService 含 onKeyEvent 与多个广播接收器，具备监听设置页的能力，属待验证项。",
    "benign_graceful_degradation": "无。未获无障碍权限时功能路径直接转权限引导，不存在手动清理/ADB/仅观看等替代降级路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（由 fnm 弹窗 Enable 点击触发），以及随后系统无障碍详情页渲染 com.starlight.cleaner.device.ram.AccessibilityFroceService 的 description 时；另可在冷启动后点击清理/加速按钮时前置抓取 fnm 弹窗。",
    "key_pages_to_capture": [
      {
        "page_role": "功能触发的引导弹窗页",
        "page_identifier": "DialogFragment 类名 com.starlight.cleaner.fnm，标题『Optimizing applications』或『Deep clean』，含 Enable 与关闭按钮",
        "why_most_useful": "这是应用唯一自有的说明载体，可直接判定文案框架（清理伪装 + 完全安全承诺）与是否可取消",
        "observable_utg_signals": ["标题/正文/按钮文本全量可读", "同一弹窗是否覆盖清理与加速两个不同功能", "是否存在关闭按钮（btn_close）"]
      },
      {
        "page_role": "跳转前埋点与跳转动作",
        "page_identifier": "CleanFragment/SpeedUpFragment2 内 fmj(\"ACCESSIBILITY\",\"SCREEN_POSITIVE\") 与随后的系统无障碍页",
        "why_most_useful": "确认『点 Enable 即跳设置』的强绑定关系，并排除高仿页面可能",
        "observable_utg_signals": ["跳转目标包名为 com.android.settings 且 action 为 ACCESSIBILITY_SETTINGS", "跳转后应用未叠加任何悬浮窗"]
      },
      {
        "page_role": "系统无障碍服务列表项/详情页",
        "page_identifier": "服务名 Reward Clean，描述以『Tap the top right slider to enable Reward Clean Cleaning』开头",
        "why_most_useful": "这是本案最关键的诱导点：把系统 description 当作教学页，并主动要求用户忽略隐私警告",
        "observable_utg_signals": ["description 全文含『standard Android OS procedure』与『does NOT collect any personal data』", "服务名与桌面名一致但包名 com.building.castle.bster 不一致", "配置仅声明 com.android.settings/com.android.vending 两个包名"]
      },
      {
        "page_role": "获权后 Play 商店自动点击页",
        "page_identifier": "com.android.vending 评价页出现 star5 高亮、post_review_button/SUBMIT 被自动点击、INSTALL/ACCEPT 被自动点击",
        "why_most_useful": "证明所申请的无障碍权限实际用于刷好评与自动确认安装，而非所述清理功能",
        "observable_utg_signals": ["星级从 0 跳到 5 且无用户触摸事件", "评价提交按钮在无人操作下被触发", "安装确认框被自动点 ACCEPT/INSTALL"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无图空文本盲区：全部引导文字均为可读文本。需注意两点：(1) 跳转系统设置后应用侧不提供任何自定义 UI，若仅抓应用自身界面会漏掉『教学』其实位于 android:description 中，需专门抓系统无障碍详情页；(2) 获权后行为发生在 :accessibility 独立进程且作用于 Play 商店，需在商店页同时抓取无障碍点击事件才能与『清理功能』区分。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_DISMISS_SYSTEM_WARNING",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.starlight.cleaner.ui.fragment.CleanFragment#cleanCache",
    "com.starlight.cleaner.ui.fragment.CleanFragment#a(fms,View)",
    "com.starlight.cleaner.fnm#onViewCreated",
    "res/xml/accessibilityconfig.xml",
    "res/values/strings.xml#L650-L655",
    "com.starlight.cleaner.device.ram.AccessibilityFroceService#onAccessibilityEvent"
  ]
}
```

补充边界说明：`fmu` 埋点上报的目标地址与本轮未追的服务端下发未核验（不影响上述引导链结论）；`post_grant_anti_removal` 中针对 `com.android.settings` 的监听能力（`onKeyEvent`、`PERFORM_GLOBAL_ACTION` 预筛线索）尚需在后续针对 `AccessibilityFroceService` 的 `nI/nJ/onKeyEvent` 单独闭环。

</details>

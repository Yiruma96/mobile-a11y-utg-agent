# BN_056__72efd84eec｜自动化与跳广告 — Buddy

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：145.3s

## 1. 一句话核心结论

- **核心申请方式**：Buddy 在首次冷启动的 6 步引导向导第 2 步，以原生页面如实说明无障碍用途与数据流向，经一次可拒绝的 BottomSheet 同意弹窗后才跳转系统无障碍设置，并在 Android 13+ 如实教学'允许受限设置'，全程保留 Skip setup 跳过与返回降级。
- **静态可见性说明**：无障碍引导全链路（MainActivity 冷启动分流、OnboardingActivity 6 步向导、Ui.openAccessibilitySettings 同意弹窗、restrictedHelp 受限设置教学、CheckActivity 诊断入口）均由 DEX 明文 Java 代码与 res/values/strings.xml 明文文案完整静态可见；无加壳、无 WebView/HTML 承载、无远端下发文案。唯一未闭合处为 BuddyService 内 PERFORM_GLOBAL_ACTION/WATCH_SETTINGS 的具体使用点，与本次引导流程无直接依赖。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `72efd84eec1363297275647560889f9be9ef4f7337fbf97cff284e3e039b9665` |
| 包名 / 年份 | `app.buddy.assistant` / 2025-2026 |
| 家族 / 品类 | **自动化与跳广告**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/app.buddy.assistant_212.apk |
| 桌面显示名 | Buddy |
| 引导页宣称品牌/身份 | Buddy（F-Droid 开源，Claude Code / Codex / OpenCode / Antigravity / Grok 手机内本地运行容器） |
| 系统无障碍列表服务名 | Buddy assistant |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。未在 DEX 检索到 isAccessibilityTool 伪造声明；无空白/换行挤出警告、无同形字、无多 activity-alias 伪装；无障碍项标签与桌面名同为 Buddy 品牌，说明文案与 Manifest android:description 一致。 |
| 无障碍服务类名 | `app.buddy.assistant.BuddyService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES` |
| 系统设置项说明 (`android:description`) | Shows the Buddy chat bubble and lets the agent you choose (Claude Code, Codex, OpenCode, Antigravity or Grok), running inside Buddy on this phone, read the screen and tap, type and scroll for you. Nothing leaves the phone except what the agent itself sends to its AI service (Anthropic, OpenAI, Google, xAI or your OpenCode model's provider). |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | app.buddy.assistant.MainActivity → app.buddy.assistant.OnboardingActivity | MainActivity.onCreate：!Prefs.onboarded(this) 且 SetupState.count() < 3 时 startActivity(OnboardingActivity) | 原生Activity | **原文**：无（纯页面跳转，无提示文案）<br>**译注**：首次安装启动时进入分步设置向导，不弹出任何权限索要弹窗 | 无强制操作，可继续向导或使用右上角 Skip setup 跳过 | `app.buddy.assistant.MainActivity#onCreate` |
| 2 | 引导说明页 | OnboardingActivity 第 0/1 步：welcome() / brain()（选择 AI 代理） | OnboardingActivity.onResume → render()，step=0/1 | 原生Activity | **原文**：Choose your agent / Who answers your chats. You can add others later in Settings.<br>**译注**：选择代理（Claude Code / Codex / OpenCode / Antigravity / Grok / 本地模型），说明可后续在设置中添加 | 选择代理后点击 Get started / Continue；右上角 Skip setup 可跳过整个向导 | `app.buddy.assistant.OnboardingActivity#render / #brain / #welcome` |
| 3 | 引导说明页 | OnboardingActivity 第 2 步 ACCESS：header + note + primary 按钮 | render() case ACCESS(2)，未授权（done()==false）时构建该页 | 原生Activity | **原文**：Let Buddy see and tap — Buddy's accessibility service shows the bubble and lets the agent read the screen, tap and type, only when you ask it to do something. / Nothing leaves the phone except what %1$s sends to %2$s to answer you. Sending, posting, buying and deleting always ask for your OK first. / In the list: Downloaded apps → Buddy assistant → turn it on.<br>**译注**：「让 Buddy 看见并点击」——说明无障碍服务用于显示悬浮气泡、按你的指令读屏/点击/输入；隐私说明：除你所选代理发往其 AI 服务商（Anthropic/OpenAI/Google/xAI 等）的内容外，数据不出手机；发送、发布、购买、删除前必先征得你同意；并给出系统列表中的路径：已下载的应用 → Buddy assistant → 打开 | 点击主按钮 Open accessibility settings；页面下方另有无障碍开关置灰说明与 App info 按钮；Skip setup 仍可用 | `app.buddy.assistant.OnboardingActivity#render（case ACCESS）/ res/values/strings.xml onboarding_access_title\|onboarding_access_text\|onboarding_access_privacy\|onboarding_access_list_hint` |
| 4 | 引导说明页 | Ui.openAccessibilitySettings 弹出的原生 BottomSheet 同意弹窗（仅首次，Prefs.a11yConsent()==false 时） | OnboardingActivity.lambda$render$2（点击 Open accessibility settings）→ accessTries++ → Ui.openAccessibilitySettings(this) | 原生Dialog | **原文**：How Buddy uses accessibility — Buddy uses Android's accessibility service to do what you ask in other apps: it reads what's on the screen and taps, types and scrolls for you. It also shows the floating bubble. / While a task runs, the screen content, which can include personal information such as messages, names or addresses, is sent to the AI service of the agent you choose (Anthropic for Claude Code, OpenAI for Codex, Google for Antigravity, xAI for Grok, or your OpenCode model's provider), only to carry out your request. / Buddy has no servers of its own. It doesn't collect, sell or share this data, and doesn't use it for ads. / Before anything that sends, posts, buys or deletes, Buddy asks for your OK. You can turn the service off anytime in Android's accessibility settings. / Privacy policy — No thanks / Agree and continue<br>**译注**：「Buddy 如何使用无障碍」透明说明：用于代你在其他应用中读屏、点击、输入、滚动并显示悬浮气泡；任务运行时屏幕内容（可能含消息、姓名、地址等个人信息）仅发送给你所选代理的 AI 服务商以完成请求；Buddy 无自有服务器，不收集/出售/共享数据、不用于广告；任何发送、发布、购买、删除前都会征得同意；可随时在系统无障碍设置中关闭。提供「隐私政策」链接与「不，谢谢」「同意并继续」两个按钮 | 二选一：No thanks（关闭弹窗、不跳转）/ Agree and continue（记录同意并跳转系统页）；存在明确取消按钮 | `app.buddy.assistant.Ui#openAccessibilitySettings / app.buddy.assistant.Ui#lambda$openAccessibilitySettings$14 / res/values/strings.xml ui_a11y_title\|ui_a11y_what\|ui_a11y_data\|ui_a11y_no_servers\|ui_a11y_asks\|ui_no_thanks\|ui_agree_continue` |
| 5 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表） | Ui.lambda$openAccessibilitySettings$14 中 Prefs.setA11yConsent(activity) → dialog.dismiss() → runnable.run() → Ui$$ExternalSyntheticLambda0.run → startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：无（应用侧不注入任何文案，直接打开系统原生无障碍列表）<br>**译注**：进入系统无障碍设置，用户在列表中自行找到「已下载的应用 → Buddy assistant」并手动开启开关 | 用户需在系统页手动打开 Buddy assistant 开关（应用无法代点、无遮罩、无高仿页面） | `app.buddy.assistant.Ui$$ExternalSyntheticLambda0#run` |
| 6 | 拒权反馈循环 | OnboardingActivity 第 2 步 + restrictedHelp 卡片（SDK≥33 且 accessTries>0 时出现） | onResume → render()；若开关被系统置灰，accessTries>0 时渲染 restrictedHelp；提供 secondary 按钮 App info | 原生Activity | **原文**：Switch greyed out? — Android blocks this for apps installed from a file. Tap App info (below), then ⋮ in the top right → Allow restricted settings, and try again. / 1. Tap App info below. 2. Tap ⋮ in the top right → Allow restricted settings. 3. Come back and open accessibility settings again.<br>**译注**：「开关变灰？」——如实解释：从文件安装的应用会被 Android 拦截；请点下方 App info，右上角 ⋮ → 允许受限设置，再回来重试（三步分步教学） | 可点 App info（跳 ACTION_APPLICATION_DETAILS_SETTINGS，package:app.buddy.assistant）按步骤允许受限设置后返回；未授权时页面停留本页，不自动重复拉起设置页，无定时器死循环；Skip setup 仍可退出 | `app.buddy.assistant.OnboardingActivity#restrictedHelp / #render（SDK≥33 分支）/ #openAppInfo / res/values/strings.xml onboarding_access_greyed_title\|onboarding_access_greyed_text\|onboarding_access_restricted_steps` |
| 7 | 获权后动作 | OnboardingActivity → 自动进入第 3 步 AGENTS（安装并登录 AI 代理）→ … → 第 6 步 TRY | onResume → checkAdvance()：done(this, ACCESS)==true（SetupState.accessibilityEnabled 读 Settings.Secure enabled_accessibility_services 含本包）时 body.postDelayed(900ms) → go(step+1) | 原生Activity | **原文**：Accessibility is on. / Continue<br>**译注**：「无障碍已开启」，900ms 后自动前进到安装代理步骤（获权后不自动关闭服务、不监听设置页、不阻止撤权） | 无需操作，自动前进；亦可用 Continue 手动推进，或用 Skip setup 直接结束向导进入聊天列表 | `app.buddy.assistant.OnboardingActivity#checkAdvance / #done / #lambda$checkAdvance$1$app-buddy-assistant-OnboardingActivity / res/values/strings.xml onboarding_access_done` |
| 8 | 业务功能触发 | app.buddy.assistant.CheckActivity（体检/诊断页）中的无障碍检查项 | CheckActivity#checks 中无障碍项失败时点击修复按钮 → Ui.openAccessibilitySettings(CheckActivity) | 原生Dialog | **原文**：How Buddy uses accessibility（复用同一同意弹窗文案，含 No thanks / Agree and continue）<br>**译注**：用户在体检页按需手动触发，同样先弹透明说明同意弹窗，可拒绝；非后台自动弹出 | 点击体检项修复按钮后二选一（同意跳转 / 不谢谢），属用户按需触发 | `app.buddy.assistant.CheckActivity#checks / app.buddy.assistant.CheckActivity#lambda$checks$3$app-buddy-assistant-CheckActivity` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- OnboardingActivity 第 2 步原生页面（LinearLayout 动态拼接）：标题「Let Buddy see and tap」、用途说明、隐私承诺 note、系统列表路径提示、主按钮「Open accessibility settings」
- Ui.openAccessibilitySettings 弹出的原生 BottomSheet Dialog（透明说明 + 隐私政策链接 + No thanks / Agree and continue）
- OnboardingActivity 第 2 步下方 restrictedHelp 卡片（SDK≥33 且 accessTries>0）：「Switch greyed out?」+ 三步「App info → ⋮ → Allow restricted settings」教学 + App info 按钮
- OnboardingActivity 顶部栏右上角常驻「Skip setup」按钮（点击后走 Ui.confirmSheet 二次确认）
- OnboardingActivity 第 6 步 tryIt 页的示例提示语（onboarding_try_prompt 等，与无障碍无直接关系）
- 系统无障碍列表中的服务条目文案：android:label="Buddy assistant" + android:description 全文（Manifest 静态声明）
- CheckActivity 体检页无障碍检查项（按需复用同一同意弹窗）
- 全部文案来自 res/values/strings.xml（另有 ar/de/es/fr/hi/in/it/ja/ko/nl/pl/pt/ru/tr/uk/vi/zh-rCN 共 17 个语言包），无 HTML/WebView 承载、无远端下发

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Let Buddy see and tap | 让 Buddy 看见并点击 | `res/values/strings.xml key=onboarding_access_title（OnboardingActivity#render case ACCESS）` | 良性透明说明 |
| en | Buddy's accessibility service shows the bubble and lets the agent read the screen, tap and type, only when you ask it to do something. | Buddy 的无障碍服务用于显示悬浮气泡，并让你选择的代理在你要求它做事时读取屏幕、点击与输入。 | `res/values/strings.xml key=onboarding_access_text` | 良性透明说明 |
| en | Nothing leaves the phone except what %1$s sends to %2$s to answer you. Sending, posting, buying and deleting always ask for your OK first. | 除了 %1$s 为回答你而发送给 %2$s 的内容外，任何数据都不离开手机。发送、发布、购买与删除操作都会先征得你的同意。 | `res/values/strings.xml key=onboarding_access_privacy（及 _both/_local/_opencode 变体）` | 隐私承诺 |
| en | In the list: Downloaded apps → Buddy assistant → turn it on. | 在列表中依次进入：已下载的应用 → Buddy assistant → 打开开关。 | `res/values/strings.xml key=onboarding_access_list_hint` | 受限设置分步教学 |
| en | How Buddy uses accessibility | Buddy 如何使用无障碍功能 | `res/values/strings.xml key=ui_a11y_title（Ui#openAccessibilitySettings BottomSheet 标题）` | 良性透明说明 |
| en | While a task runs, the screen content, which can include personal information such as messages, names or addresses, is sent to the AI service of the agent you choose (Anthropic for Claude Code, OpenAI for Codex, Google for Antigravity, xAI for Grok, or your OpenCode model's provider), only to carry out your request. | 任务运行期间，屏幕内容（可能包含消息、姓名或地址等个人信息）会被发送给你所选代理的 AI 服务（Claude Code→Anthropic，Codex→OpenAI，Antigravity→Google，Grok→xAI，或你的 OpenCode 模型服务商），仅用于执行你的请求。 | `res/values/strings.xml key=ui_a11y_data` | 良性透明说明 |
| en | Buddy has no servers of its own. It doesn't collect, sell or share this data, and doesn't use it for ads. | Buddy 没有自有服务器，不收集、不出售、不共享这些数据，也不用于广告。 | `res/values/strings.xml key=ui_a11y_no_servers` | 隐私承诺 |
| en | Before anything that sends, posts, buys or deletes, Buddy asks for your OK. You can turn the service off anytime in Android's accessibility settings. | 在发送、发布、购买或删除任何内容前，Buddy 会征求你的同意。你随时可以在 Android 无障碍设置中关闭该服务。 | `res/values/strings.xml key=ui_a11y_asks` | 良性透明说明 |
| en | No thanks | 不，谢谢 | `res/values/strings.xml key=ui_no_thanks（BottomSheet 取消按钮）` | 良性透明说明 |
| en | Agree and continue | 同意并继续 | `res/values/strings.xml key=ui_agree_continue（BottomSheet 确认按钮，点击后才跳系统无障碍页）` | 良性透明说明 |
| en | Switch greyed out? | 开关变灰了？ | `res/values/strings.xml key=onboarding_access_greyed_title（restrictedHelp 卡片）` | 受限设置分步教学 |
| en | Android blocks this for apps installed from a file. Tap App info (below), then ⋮ in the top right → Allow restricted settings, and try again. | Android 会拦截从文件安装的应用开启此权限。请点击下方 App info，再点右上角 ⋮ → 允许受限设置，然后重试。 | `res/values/strings.xml key=onboarding_access_greyed_text` | 受限设置分步教学 |
| en | 1. Tap App info below.<br>2. Tap ⋮ in the top right → Allow restricted settings.<br>3. Come back and open accessibility settings again. | 1. 点击下方 App info。2. 点右上角 ⋮ → 允许受限设置。3. 返回后再次打开无障碍设置。 | `res/values/strings.xml key=onboarding_access_restricted_steps（OnboardingActivity#restrictedHelp）` | 受限设置分步教学 |
| en | Accessibility is on. | 无障碍已开启。 | `res/values/strings.xml key=onboarding_access_done（获权后状态文案）` | 良性透明说明 |
| en | Shows the Buddy chat bubble and lets the agent you choose (Claude Code, Codex, OpenCode, Antigravity or Grok), running inside Buddy on this phone, read the screen and tap, type and scroll for you. Nothing leaves the phone except what the agent itself sends to its AI service (Anthropic, OpenAI, Google, xAI or your OpenCode model's provider). | 显示 Buddy 聊天气泡，并让你选择的代理（Claude Code、Codex、OpenCode、Antigravity 或 Grok，均在本机 Buddy 内运行）替你读屏、点击、输入与滚动。除代理自身发往其 AI 服务的内容外，任何数据都不离开手机。 | `AndroidManifest.xml <service android:name=".BuddyService"> 的 android:description（系统无障碍列表展示）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`shallow_1_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无死循环：onResume → render() + checkAdvance()，仅当 SetupState.accessibilityEnabled() 为真（Settings.Secure enabled_accessibility_services 含本包）才 postDelayed(900ms) 自动前进；用户拒绝或从系统页返回而未开启时，停留在第 2 步页面等待，不重复拉起 ACCESSIBILITY_SETTINGS，无定时器轮询、无 onResume 强跳；返回键仅按步后退（noAutoAdvance=true），顶部 Skip setup 经确认弹窗后 finishGuide() 直接进入 MainActivity。
- **遮罩叠层 / 高仿系统设置页**：无。跳转后应用侧不绘制任何遮罩、全屏悬浮窗或高仿系统开关页；悬浮气泡（Bubble）为应用自身聊天入口功能，非设置页引导叠层。
- **Android 13+ 受限设置（Restricted Settings）应对**：有，且为如实复述：SDK≥33 且 accessTries>0 时 restrictedHelp() 教学「App info → 右上角 ⋮ → Allow restricted settings → 返回再开无障碍设置」，并提供 App info 按钮跳 ACTION_APPLICATION_DETAILS_SETTINGS（package:app.buddy.assistant）。未使用 Session 安装器、无伪造系统弹窗。
- **获权后即时行为与防撤权机制**：无。获权后仅读取 enabled_accessibility_services 判断状态并前进到下一步，未见自点确认、自授权或监听设置页后用 GLOBAL_ACTION_BACK/HOME 阻止撤权；文案明确告知「可随时在系统无障碍设置中关闭」。
- **良性降级 / 替代方案**：有：向导全程可 Skip setup 跳过（二次确认后进入主界面聊天列表）；任一未完成步骤均可停留而不阻塞其他功能；隐私说明中提供「本地模型」路径（Ollama/LM Studio/llama.cpp，屏幕内容仅发往用户自有服务器）；BottomSheet 明确提供 No thanks 取消。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在首次冷启动进入 OnboardingActivity 且 step==2（出现「Open accessibility settings」按钮）时开始连续抓栈；随后监听 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间拍页，并在 900ms 后（checkAdvance 自动前进）与从系统页 onResume 返回时各补抓一帧；若系统开关置灰，则在同一页出现「Switch greyed out?」卡片并伴随 ACTION_APPLICATION_DETAILS_SETTINGS 跳转时再抓。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图空文本诱导、无温和外壳、无 Dropper 二阶段、无静态加壳（静态可见性 clear）。需注意的边界：①BuddyService 内 PERFORM_GLOBAL_ACTION / WATCH_SETTINGS 的具体使用点本轮未追到，若存在对系统无障碍设置页的自动化操作，属 UTG 难以直接判定的运行期行为，建议结合 Hook AccessibilityService#performGlobalAction 与 Settings 页 Activity 监控补充；②Background.launch 中通过本机无线 adb 执行 pm grant WRITE_SECURE_SETTINGS 的自授权链，UTG 仅能看到 dev options 页面跳转，需 adb/日志侧佐证；③引导文案随设备语言本地化（17 语言），多语言环境抓取时应按语言包对齐文本。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动向导第 2 步说明页（跳转前）** | app.buddy.assistant.OnboardingActivity，标题「Let Buddy see and tap」，含主按钮「Open accessibility settings」与右上角「Skip setup」 | 该页决定是否构成「无说明直接索权」——此处有完整用途与数据流向披露，是良性判定的核心页面 | 标题与正文文本「Let Buddy see and tap」/「only when you ask it to do something」；按钮文本「Open accessibility settings」；存在「Skip setup」与「No thanks」类可取消控件；页面为原生 LinearLayout 拼接，无 WebView 节点 |
| **跳转前同意弹窗（BottomSheet）** | Ui.bottomSheet 生成的原生 Dialog，标题「How Buddy uses accessibility」，底部两按钮 No thanks / Agree and continue | 这是唯一的显式同意门；捕获它可区分「一次点击即跳系统页」与「二次确认后才跳」 | Dialog 节点文本「How Buddy uses accessibility」；同时存在「No thanks」与「Agree and continue」两个按钮；含「Privacy policy」可点击链接；点击 Agree 后才出现系统 Settings 包 Activity |
| **系统无障碍设置页（跳转后）** | com.android.settings 的 AccessibilitySettings，列表项含「Buddy assistant」 | 确认跳转目标为真实系统设置而非高仿页，并核对系统条目名称/说明与应用身份一致 | 窗口包名为 com.android.settings（非 app.buddy.assistant）；列表项文本「Buddy assistant」；无应用侧 overlay/悬浮窗覆盖层（windows 列表不含 app.buddy.assistant 的 TYPE_APPLICATION_OVERLAY）；开关需用户手动点击，应用未代点 |
| **受限设置教学卡片页（Android 13+ 开关置灰时）** | OnboardingActivity 第 2 步内嵌卡片「Switch greyed out?」+ 三步编号说明 + 「App info」按钮 | 区分「如实复述官方受限设置流程」与「伪造系统弹窗/教唆绕过安全警告」 | 文本「⋮ in the top right → Allow restricted settings」；按钮「App info」点击后跳 android.settings.APPLICATION_DETAILS_SETTINGS 且 data=package:app.buddy.assistant；目标页为系统「应用信息」而非自绘仿冒页；无 Session-based 安装器界面 |
| **获权后状态页 / 后续步骤** | OnboardingActivity step=3（Install and sign in）或 step=6（tryIt），出现「Accessibility is on.」 | 验证获权后无自点确认、无阻止撤权、无隐藏二次权限拉升（如立刻索要 WRITE_SECURE_SETTINGS 的 adb 授权） | 文本「Accessibility is on.」；未出现系统无障碍页被再次拉起的循环；未出现 GLOBAL_ACTION_BACK/HOME 触发的设置页回退；后续步骤为代理安装/登录，非权限索取 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `app.buddy.assistant.OnboardingActivity#render（case ACCESS 分支，构建第 2 步说明页与 Open accessibility settings 按钮）`
- `app.buddy.assistant.OnboardingActivity#lambda$render$2$app-buddy-assistant-OnboardingActivity（accessTries++ 后调用 Ui.openAccessibilitySettings）`
- `app.buddy.assistant.Ui#openAccessibilitySettings / app.buddy.assistant.Ui#lambda$openAccessibilitySettings$14（同意弹窗 → setA11yConsent → startActivity ACCESSIBILITY_SETTINGS）`
- `app.buddy.assistant.Ui$$ExternalSyntheticLambda0#run（startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))）`
- `app.buddy.assistant.OnboardingActivity#restrictedHelp / #openAppInfo（受限设置三步教学与 ACTION_APPLICATION_DETAILS_SETTINGS 跳转）`
- `res/values/strings.xml（onboarding_access_title|onboarding_access_text|onboarding_access_privacy|onboarding_access_list_hint|onboarding_access_greyed_title|onboarding_access_restricted_steps|ui_a11y_title|ui_a11y_data|ui_a11y_no_servers|ui_a11y_asks|ui_no_thanks|ui_agree_continue）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（Buddy / app.buddy.assistant，纯运行期 UTG 视角）

**总体判定：良性、透明，无障碍申请全程由用户主动点击触发，存在明确取消与跳过路径，无遮罩/假设置页/拒权循环。**

- **冷启动入口链**：`MainActivity.onCreate` 在 `!Prefs.onboarded()` 时直接 `startActivity(OnboardingActivity)`；引导为 0~6 步分步向导（WELCOME→BRAIN→**ACCESS(2)**→AGENTS→BACKGROUND→SAFETY→TRY），无障碍位于第 2 步，不是首屏强插。
- **两次确认才跳系统页**：第 2 步页内主按钮"Open accessibility settings" → `OnboardingActivity.lambda$render$2` → `Ui.openAccessibilitySettings()`。该方法先查 `Prefs.a11yConsent()`，未同意则弹**原生 BottomSheet 透明说明**（`ui_a11y_title/what/data/no_servers/asks` + Privacy policy 链接），按钮为 **"No thanks" / "Agree and continue"**；点同意才 `Prefs.setA11yConsent()` 并 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`。说明文字如实披露"屏幕内容（可能含消息、姓名、地址）会发给你选择的 AI 服务商"。
- **13+ 受限设置教学属实但标准且透明**：`accessTries>0 && SDK>=33` 时 `restrictedHelp()` 显示"Switch greyed out?"与三步（App info → ⋮ → Allow restricted settings → 回来再开），并提供 "App info" 按钮 → `ACTION_APPLICATION_DETAILS_SETTINGS`。这是 Google 官方受限设置流程的如实复述，无伪造、无 Session 安装器绕过。
- **无拒绝死循环**：`onResume → render() + checkAdvance()`，仅当 `done(step)`（`SetupState.accessibilityEnabled` 读 `enabled_accessibility_services` 为真）才 `postDelayed(900ms)` 自动前进；未授权则停留本页等待，不重复拉起设置页。
- **取消/降级完备**：顶部常驻 "Skip setup" → `Ui.confirmSheet(onboarding_skip_title/text/action)` → `finishGuide()` 直入 `MainActivity`；`onBackPressed` 逐步后退。
- **身份一致**：桌面名 Buddy，无障碍项 `Buddy assistant`，说明为 `android:description` 全文，DEX 中**未检索到** `isAccessibilityTool` 伪造痕迹；无 WebView 承载引导（引导全为原生 View 拼接）。
- **边界说明**：`BuddyService` 的 `PERFORM_GLOBAL_ACTION`/`WATCH_SETTINGS` 属预筛共现，本轮未追到"设置页自点确认/阻止撤权"的具体调用点，不构成已证实诱导行为；`Background.launch` 中通过无线 adb `pm grant WRITE_SECURE_SETTINGS` 属另一条自授权链，不在本轮无障碍引导范围，建议另立命题核查。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（MainActivity 冷启动分流、OnboardingActivity 6 步向导、Ui.openAccessibilitySettings 同意弹窗、restrictedHelp 受限设置教学、CheckActivity 诊断入口）均由 DEX 明文 Java 代码与 res/values/strings.xml 明文文案完整静态可见；无加壳、无 WebView/HTML 承载、无远端下发文案。唯一未闭合处为 BuddyService 内 PERFORM_GLOBAL_ACTION/WATCH_SETTINGS 的具体使用点，与本次引导流程无直接依赖。",
  "summary_one_liner": "Buddy 在首次冷启动的 6 步引导向导第 2 步，以原生页面如实说明无障碍用途与数据流向，经一次可拒绝的 BottomSheet 同意弹窗后才跳转系统无障碍设置，并在 Android 13+ 如实教学'允许受限设置'，全程保留 Skip setup 跳过与返回降级。",
  "disguise_identity": {
    "app_display_name": "Buddy",
    "claimed_brand_or_persona": "Buddy（F-Droid 开源，Claude Code / Codex / OpenCode / Antigravity / Grok 手机内本地运行容器）",
    "a11y_service_label": "Buddy assistant",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。未在 DEX 检索到 isAccessibilityTool 伪造声明；无空白/换行挤出警告、无同形字、无多 activity-alias 伪装；无障碍项标签与桌面名同为 Buddy 品牌，说明文案与 Manifest android:description 一致。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "app.buddy.assistant.MainActivity → app.buddy.assistant.OnboardingActivity",
      "trigger_event": "MainActivity.onCreate：!Prefs.onboarded(this) 且 SetupState.count() < 3 时 startActivity(OnboardingActivity)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（纯页面跳转，无提示文案）",
      "shown_text_zh": "首次安装启动时进入分步设置向导，不弹出任何权限索要弹窗",
      "user_action_requested": "无强制操作，可继续向导或使用右上角 Skip setup 跳过",
      "code_anchor": "app.buddy.assistant.MainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "OnboardingActivity 第 0/1 步：welcome() / brain()（选择 AI 代理）",
      "trigger_event": "OnboardingActivity.onResume → render()，step=0/1",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Choose your agent / Who answers your chats. You can add others later in Settings.",
      "shown_text_zh": "选择代理（Claude Code / Codex / OpenCode / Antigravity / Grok / 本地模型），说明可后续在设置中添加",
      "user_action_requested": "选择代理后点击 Get started / Continue；右上角 Skip setup 可跳过整个向导",
      "code_anchor": "app.buddy.assistant.OnboardingActivity#render / #brain / #welcome"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "OnboardingActivity 第 2 步 ACCESS：header + note + primary 按钮",
      "trigger_event": "render() case ACCESS(2)，未授权（done()==false）时构建该页",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Let Buddy see and tap — Buddy's accessibility service shows the bubble and lets the agent read the screen, tap and type, only when you ask it to do something. / Nothing leaves the phone except what %1$s sends to %2$s to answer you. Sending, posting, buying and deleting always ask for your OK first. / In the list: Downloaded apps → Buddy assistant → turn it on.",
      "shown_text_zh": "「让 Buddy 看见并点击」——说明无障碍服务用于显示悬浮气泡、按你的指令读屏/点击/输入；隐私说明：除你所选代理发往其 AI 服务商（Anthropic/OpenAI/Google/xAI 等）的内容外，数据不出手机；发送、发布、购买、删除前必先征得你同意；并给出系统列表中的路径：已下载的应用 → Buddy assistant → 打开",
      "user_action_requested": "点击主按钮 Open accessibility settings；页面下方另有无障碍开关置灰说明与 App info 按钮；Skip setup 仍可用",
      "code_anchor": "app.buddy.assistant.OnboardingActivity#render（case ACCESS）/ res/values/strings.xml onboarding_access_title|onboarding_access_text|onboarding_access_privacy|onboarding_access_list_hint"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "Ui.openAccessibilitySettings 弹出的原生 BottomSheet 同意弹窗（仅首次，Prefs.a11yConsent()==false 时）",
      "trigger_event": "OnboardingActivity.lambda$render$2（点击 Open accessibility settings）→ accessTries++ → Ui.openAccessibilitySettings(this)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "How Buddy uses accessibility — Buddy uses Android's accessibility service to do what you ask in other apps: it reads what's on the screen and taps, types and scrolls for you. It also shows the floating bubble. / While a task runs, the screen content, which can include personal information such as messages, names or addresses, is sent to the AI service of the agent you choose (Anthropic for Claude Code, OpenAI for Codex, Google for Antigravity, xAI for Grok, or your OpenCode model's provider), only to carry out your request. / Buddy has no servers of its own. It doesn't collect, sell or share this data, and doesn't use it for ads. / Before anything that sends, posts, buys or deletes, Buddy asks for your OK. You can turn the service off anytime in Android's accessibility settings. / Privacy policy — No thanks / Agree and continue",
      "shown_text_zh": "「Buddy 如何使用无障碍」透明说明：用于代你在其他应用中读屏、点击、输入、滚动并显示悬浮气泡；任务运行时屏幕内容（可能含消息、姓名、地址等个人信息）仅发送给你所选代理的 AI 服务商以完成请求；Buddy 无自有服务器，不收集/出售/共享数据、不用于广告；任何发送、发布、购买、删除前都会征得同意；可随时在系统无障碍设置中关闭。提供「隐私政策」链接与「不，谢谢」「同意并继续」两个按钮",
      "user_action_requested": "二选一：No thanks（关闭弹窗、不跳转）/ Agree and continue（记录同意并跳转系统页）；存在明确取消按钮",
      "code_anchor": "app.buddy.assistant.Ui#openAccessibilitySettings / app.buddy.assistant.Ui#lambda$openAccessibilitySettings$14 / res/values/strings.xml ui_a11y_title|ui_a11y_what|ui_a11y_data|ui_a11y_no_servers|ui_a11y_asks|ui_no_thanks|ui_agree_continue"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表）",
      "trigger_event": "Ui.lambda$openAccessibilitySettings$14 中 Prefs.setA11yConsent(activity) → dialog.dismiss() → runnable.run() → Ui$$ExternalSyntheticLambda0.run → startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧不注入任何文案，直接打开系统原生无障碍列表）",
      "shown_text_zh": "进入系统无障碍设置，用户在列表中自行找到「已下载的应用 → Buddy assistant」并手动开启开关",
      "user_action_requested": "用户需在系统页手动打开 Buddy assistant 开关（应用无法代点、无遮罩、无高仿页面）",
      "code_anchor": "app.buddy.assistant.Ui$$ExternalSyntheticLambda0#run"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "OnboardingActivity 第 2 步 + restrictedHelp 卡片（SDK≥33 且 accessTries>0 时出现）",
      "trigger_event": "onResume → render()；若开关被系统置灰，accessTries>0 时渲染 restrictedHelp；提供 secondary 按钮 App info",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Switch greyed out? — Android blocks this for apps installed from a file. Tap App info (below), then ⋮ in the top right → Allow restricted settings, and try again. / 1. Tap App info below. 2. Tap ⋮ in the top right → Allow restricted settings. 3. Come back and open accessibility settings again.",
      "shown_text_zh": "「开关变灰？」——如实解释：从文件安装的应用会被 Android 拦截；请点下方 App info，右上角 ⋮ → 允许受限设置，再回来重试（三步分步教学）",
      "user_action_requested": "可点 App info（跳 ACTION_APPLICATION_DETAILS_SETTINGS，package:app.buddy.assistant）按步骤允许受限设置后返回；未授权时页面停留本页，不自动重复拉起设置页，无定时器死循环；Skip setup 仍可退出",
      "code_anchor": "app.buddy.assistant.OnboardingActivity#restrictedHelp / #render（SDK≥33 分支）/ #openAppInfo / res/values/strings.xml onboarding_access_greyed_title|onboarding_access_greyed_text|onboarding_access_restricted_steps"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "OnboardingActivity → 自动进入第 3 步 AGENTS（安装并登录 AI 代理）→ … → 第 6 步 TRY",
      "trigger_event": "onResume → checkAdvance()：done(this, ACCESS)==true（SetupState.accessibilityEnabled 读 Settings.Secure enabled_accessibility_services 含本包）时 body.postDelayed(900ms) → go(step+1)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility is on. / Continue",
      "shown_text_zh": "「无障碍已开启」，900ms 后自动前进到安装代理步骤（获权后不自动关闭服务、不监听设置页、不阻止撤权）",
      "user_action_requested": "无需操作，自动前进；亦可用 Continue 手动推进，或用 Skip setup 直接结束向导进入聊天列表",
      "code_anchor": "app.buddy.assistant.OnboardingActivity#checkAdvance / #done / #lambda$checkAdvance$1$app-buddy-assistant-OnboardingActivity / res/values/strings.xml onboarding_access_done"
    },
    {
      "step": 8,
      "stage": "业务功能触发",
      "screen_or_component": "app.buddy.assistant.CheckActivity（体检/诊断页）中的无障碍检查项",
      "trigger_event": "CheckActivity#checks 中无障碍项失败时点击修复按钮 → Ui.openAccessibilitySettings(CheckActivity)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "How Buddy uses accessibility（复用同一同意弹窗文案，含 No thanks / Agree and continue）",
      "shown_text_zh": "用户在体检页按需手动触发，同样先弹透明说明同意弹窗，可拒绝；非后台自动弹出",
      "user_action_requested": "点击体检项修复按钮后二选一（同意跳转 / 不谢谢），属用户按需触发",
      "code_anchor": "app.buddy.assistant.CheckActivity#checks / app.buddy.assistant.CheckActivity#lambda$checks$3$app-buddy-assistant-CheckActivity"
    }
  ],
  "text_presentation_locations": [
    "OnboardingActivity 第 2 步原生页面（LinearLayout 动态拼接）：标题「Let Buddy see and tap」、用途说明、隐私承诺 note、系统列表路径提示、主按钮「Open accessibility settings」",
    "Ui.openAccessibilitySettings 弹出的原生 BottomSheet Dialog（透明说明 + 隐私政策链接 + No thanks / Agree and continue）",
    "OnboardingActivity 第 2 步下方 restrictedHelp 卡片（SDK≥33 且 accessTries>0）：「Switch greyed out?」+ 三步「App info → ⋮ → Allow restricted settings」教学 + App info 按钮",
    "OnboardingActivity 顶部栏右上角常驻「Skip setup」按钮（点击后走 Ui.confirmSheet 二次确认）",
    "OnboardingActivity 第 6 步 tryIt 页的示例提示语（onboarding_try_prompt 等，与无障碍无直接关系）",
    "系统无障碍列表中的服务条目文案：android:label=\"Buddy assistant\" + android:description 全文（Manifest 静态声明）",
    "CheckActivity 体检页无障碍检查项（按需复用同一同意弹窗）",
    "全部文案来自 res/values/strings.xml（另有 ar/de/es/fr/hi/in/it/ja/ko/nl/pl/pt/ru/tr/uk/vi/zh-rCN 共 17 个语言包），无 HTML/WebView 承载、无远端下发"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Let Buddy see and tap",
      "text_zh": "让 Buddy 看见并点击",
      "source_location": "res/values/strings.xml key=onboarding_access_title（OnboardingActivity#render case ACCESS）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Buddy's accessibility service shows the bubble and lets the agent read the screen, tap and type, only when you ask it to do something.",
      "text_zh": "Buddy 的无障碍服务用于显示悬浮气泡，并让你选择的代理在你要求它做事时读取屏幕、点击与输入。",
      "source_location": "res/values/strings.xml key=onboarding_access_text",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Nothing leaves the phone except what %1$s sends to %2$s to answer you. Sending, posting, buying and deleting always ask for your OK first.",
      "text_zh": "除了 %1$s 为回答你而发送给 %2$s 的内容外，任何数据都不离开手机。发送、发布、购买与删除操作都会先征得你的同意。",
      "source_location": "res/values/strings.xml key=onboarding_access_privacy（及 _both/_local/_opencode 变体）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "In the list: Downloaded apps → Buddy assistant → turn it on.",
      "text_zh": "在列表中依次进入：已下载的应用 → Buddy assistant → 打开开关。",
      "source_location": "res/values/strings.xml key=onboarding_access_list_hint",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "How Buddy uses accessibility",
      "text_zh": "Buddy 如何使用无障碍功能",
      "source_location": "res/values/strings.xml key=ui_a11y_title（Ui#openAccessibilitySettings BottomSheet 标题）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "While a task runs, the screen content, which can include personal information such as messages, names or addresses, is sent to the AI service of the agent you choose (Anthropic for Claude Code, OpenAI for Codex, Google for Antigravity, xAI for Grok, or your OpenCode model's provider), only to carry out your request.",
      "text_zh": "任务运行期间，屏幕内容（可能包含消息、姓名或地址等个人信息）会被发送给你所选代理的 AI 服务（Claude Code→Anthropic，Codex→OpenAI，Antigravity→Google，Grok→xAI，或你的 OpenCode 模型服务商），仅用于执行你的请求。",
      "source_location": "res/values/strings.xml key=ui_a11y_data",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Buddy has no servers of its own. It doesn't collect, sell or share this data, and doesn't use it for ads.",
      "text_zh": "Buddy 没有自有服务器，不收集、不出售、不共享这些数据，也不用于广告。",
      "source_location": "res/values/strings.xml key=ui_a11y_no_servers",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Before anything that sends, posts, buys or deletes, Buddy asks for your OK. You can turn the service off anytime in Android's accessibility settings.",
      "text_zh": "在发送、发布、购买或删除任何内容前，Buddy 会征求你的同意。你随时可以在 Android 无障碍设置中关闭该服务。",
      "source_location": "res/values/strings.xml key=ui_a11y_asks",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "No thanks",
      "text_zh": "不，谢谢",
      "source_location": "res/values/strings.xml key=ui_no_thanks（BottomSheet 取消按钮）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Agree and continue",
      "text_zh": "同意并继续",
      "source_location": "res/values/strings.xml key=ui_agree_continue（BottomSheet 确认按钮，点击后才跳系统无障碍页）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Switch greyed out?",
      "text_zh": "开关变灰了？",
      "source_location": "res/values/strings.xml key=onboarding_access_greyed_title（restrictedHelp 卡片）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Android blocks this for apps installed from a file. Tap App info (below), then ⋮ in the top right → Allow restricted settings, and try again.",
      "text_zh": "Android 会拦截从文件安装的应用开启此权限。请点击下方 App info，再点右上角 ⋮ → 允许受限设置，然后重试。",
      "source_location": "res/values/strings.xml key=onboarding_access_greyed_text",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "1. Tap App info below.\n2. Tap ⋮ in the top right → Allow restricted settings.\n3. Come back and open accessibility settings again.",
      "text_zh": "1. 点击下方 App info。2. 点右上角 ⋮ → 允许受限设置。3. 返回后再次打开无障碍设置。",
      "source_location": "res/values/strings.xml key=onboarding_access_restricted_steps（OnboardingActivity#restrictedHelp）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility is on.",
      "text_zh": "无障碍已开启。",
      "source_location": "res/values/strings.xml key=onboarding_access_done（获权后状态文案）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Shows the Buddy chat bubble and lets the agent you choose (Claude Code, Codex, OpenCode, Antigravity or Grok), running inside Buddy on this phone, read the screen and tap, type and scroll for you. Nothing leaves the phone except what the agent itself sends to its AI service (Anthropic, OpenAI, Google, xAI or your OpenCode model's provider).",
      "text_zh": "显示 Buddy 聊天气泡，并让你选择的代理（Claude Code、Codex、OpenCode、Antigravity 或 Grok，均在本机 Buddy 内运行）替你读屏、点击、输入与滚动。除代理自身发往其 AI 服务的内容外，任何数据都不离开手机。",
      "source_location": "AndroidManifest.xml <service android:name=\".BuddyService\"> 的 android:description（系统无障碍列表展示）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "shallow_1_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无死循环：onResume → render() + checkAdvance()，仅当 SetupState.accessibilityEnabled() 为真（Settings.Secure enabled_accessibility_services 含本包）才 postDelayed(900ms) 自动前进；用户拒绝或从系统页返回而未开启时，停留在第 2 步页面等待，不重复拉起 ACCESSIBILITY_SETTINGS，无定时器轮询、无 onResume 强跳；返回键仅按步后退（noAutoAdvance=true），顶部 Skip setup 经确认弹窗后 finishGuide() 直接进入 MainActivity。",
    "overlay_or_fake_settings": "无。跳转后应用侧不绘制任何遮罩、全屏悬浮窗或高仿系统开关页；悬浮气泡（Bubble）为应用自身聊天入口功能，非设置页引导叠层。",
    "restricted_settings_13plus_coaching": "有，且为如实复述：SDK≥33 且 accessTries>0 时 restrictedHelp() 教学「App info → 右上角 ⋮ → Allow restricted settings → 返回再开无障碍设置」，并提供 App info 按钮跳 ACTION_APPLICATION_DETAILS_SETTINGS（package:app.buddy.assistant）。未使用 Session 安装器、无伪造系统弹窗。",
    "post_grant_anti_removal": "无。获权后仅读取 enabled_accessibility_services 判断状态并前进到下一步，未见自点确认、自授权或监听设置页后用 GLOBAL_ACTION_BACK/HOME 阻止撤权；文案明确告知「可随时在系统无障碍设置中关闭」。",
    "benign_graceful_degradation": "有：向导全程可 Skip setup 跳过（二次确认后进入主界面聊天列表）；任一未完成步骤均可停留而不阻塞其他功能；隐私说明中提供「本地模型」路径（Ollama/LM Studio/llama.cpp，屏幕内容仅发往用户自有服务器）；BottomSheet 明确提供 No thanks 取消。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在首次冷启动进入 OnboardingActivity 且 step==2（出现「Open accessibility settings」按钮）时开始连续抓栈；随后监听 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间拍页，并在 900ms 后（checkAdvance 自动前进）与从系统页 onResume 返回时各补抓一帧；若系统开关置灰，则在同一页出现「Switch greyed out?」卡片并伴随 ACTION_APPLICATION_DETAILS_SETTINGS 跳转时再抓。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动向导第 2 步说明页（跳转前）",
        "page_identifier": "app.buddy.assistant.OnboardingActivity，标题「Let Buddy see and tap」，含主按钮「Open accessibility settings」与右上角「Skip setup」",
        "why_most_useful": "该页决定是否构成「无说明直接索权」——此处有完整用途与数据流向披露，是良性判定的核心页面",
        "observable_utg_signals": ["标题与正文文本「Let Buddy see and tap」/「only when you ask it to do something」", "按钮文本「Open accessibility settings」", "存在「Skip setup」与「No thanks」类可取消控件", "页面为原生 LinearLayout 拼接，无 WebView 节点"]
      },
      {
        "page_role": "跳转前同意弹窗（BottomSheet）",
        "page_identifier": "Ui.bottomSheet 生成的原生 Dialog，标题「How Buddy uses accessibility」，底部两按钮 No thanks / Agree and continue",
        "why_most_useful": "这是唯一的显式同意门；捕获它可区分「一次点击即跳系统页」与「二次确认后才跳」",
        "observable_utg_signals": ["Dialog 节点文本「How Buddy uses accessibility」", "同时存在「No thanks」与「Agree and continue」两个按钮", "含「Privacy policy」可点击链接", "点击 Agree 后才出现系统 Settings 包 Activity"]
      },
      {
        "page_role": "系统无障碍设置页（跳转后）",
        "page_identifier": "com.android.settings 的 AccessibilitySettings，列表项含「Buddy assistant」",
        "why_most_useful": "确认跳转目标为真实系统设置而非高仿页，并核对系统条目名称/说明与应用身份一致",
        "observable_utg_signals": ["窗口包名为 com.android.settings（非 app.buddy.assistant）", "列表项文本「Buddy assistant」", "无应用侧 overlay/悬浮窗覆盖层（windows 列表不含 app.buddy.assistant 的 TYPE_APPLICATION_OVERLAY）", "开关需用户手动点击，应用未代点"]
      },
      {
        "page_role": "受限设置教学卡片页（Android 13+ 开关置灰时）",
        "page_identifier": "OnboardingActivity 第 2 步内嵌卡片「Switch greyed out?」+ 三步编号说明 + 「App info」按钮",
        "why_most_useful": "区分「如实复述官方受限设置流程」与「伪造系统弹窗/教唆绕过安全警告」",
        "observable_utg_signals": ["文本「⋮ in the top right → Allow restricted settings」", "按钮「App info」点击后跳 android.settings.APPLICATION_DETAILS_SETTINGS 且 data=package:app.buddy.assistant", "目标页为系统「应用信息」而非自绘仿冒页", "无 Session-based 安装器界面"]
      },
      {
        "page_role": "获权后状态页 / 后续步骤",
        "page_identifier": "OnboardingActivity step=3（Install and sign in）或 step=6（tryIt），出现「Accessibility is on.」",
        "why_most_useful": "验证获权后无自点确认、无阻止撤权、无隐藏二次权限拉升（如立刻索要 WRITE_SECURE_SETTINGS 的 adb 授权）",
        "observable_utg_signals": ["文本「Accessibility is on.」", "未出现系统无障碍页被再次拉起的循环", "未出现 GLOBAL_ACTION_BACK/HOME 触发的设置页回退", "后续步骤为代理安装/登录，非权限索取"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图空文本诱导、无温和外壳、无 Dropper 二阶段、无静态加壳（静态可见性 clear）。需注意的边界：①BuddyService 内 PERFORM_GLOBAL_ACTION / WATCH_SETTINGS 的具体使用点本轮未追到，若存在对系统无障碍设置页的自动化操作，属 UTG 难以直接判定的运行期行为，建议结合 Hook AccessibilityService#performGlobalAction 与 Settings 页 Activity 监控补充；②Background.launch 中通过本机无线 adb 执行 pm grant WRITE_SECURE_SETTINGS 的自授权链，UTG 仅能看到 dev options 页面跳转，需 adb/日志侧佐证；③引导文案随设备语言本地化（17 语言），多语言环境抓取时应按语言包对齐文本。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "app.buddy.assistant.OnboardingActivity#render（case ACCESS 分支，构建第 2 步说明页与 Open accessibility settings 按钮）",
    "app.buddy.assistant.OnboardingActivity#lambda$render$2$app-buddy-assistant-OnboardingActivity（accessTries++ 后调用 Ui.openAccessibilitySettings）",
    "app.buddy.assistant.Ui#openAccessibilitySettings / app.buddy.assistant.Ui#lambda$openAccessibilitySettings$14（同意弹窗 → setA11yConsent → startActivity ACCESSIBILITY_SETTINGS）",
    "app.buddy.assistant.Ui$$ExternalSyntheticLambda0#run（startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))）",
    "app.buddy.assistant.OnboardingActivity#restrictedHelp / #openAppInfo（受限设置三步教学与 ACTION_APPLICATION_DETAILS_SETTINGS 跳转）",
    "res/values/strings.xml（onboarding_access_title|onboarding_access_text|onboarding_access_privacy|onboarding_access_list_hint|onboarding_access_greyed_title|onboarding_access_restricted_steps|ui_a11y_title|ui_a11y_data|ui_a11y_no_servers|ui_a11y_asks|ui_no_thanks|ui_agree_continue）"
  ]
}
```

**未登记风险**：本次定向核验未发现可单独定级的诱导/欺诈/隐私违规命题，故未调用 `record_risk`；上述两处边界（`PERFORM_GLOBAL_ACTION` 具体使用点、无线 adb `pm grant` 自授权链）建议另立命题专项核查后再定性。

</details>

# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:58:33
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`app.buddy.assistant`（静态标签：`benign` / `自动化与跳广告` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 5 步，UTG 唯一节点 `7` 个，有向边 `9` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 5 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_05_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`app.buddy.assistant/app.buddy.assistant.OnboardingActivity` | hooks=`[]` | overlays=`0` | texts=`step 2 of 6 / Skip setup / Let Buddy see and tap / Buddy's accessibility service shows the bubble and lets the agent read the screen, tap and type, only when you ask it to do something. / Nothing leaves the phone except what Claude Code sends to Anthropic to answer you. Sending, posting, buying and deleting always ask for your OK first.`
- **Back 后 +5.5s**：`app.buddy.assistant/app.buddy.assistant.OnboardingActivity` | hooks=`[]` | overlays=`0` | texts=`step 2 of 6 / Skip setup / Let Buddy see and tap / Buddy's accessibility service shows the bubble and lets the agent read the screen, tap and type, only when you ask it to do something. / Nothing leaves the phone except what Claude Code sends to Anthropic to answer you. Sending, posting, buying and deleting always ask for your OK first.`
- **Back 后 +10.5s**：`app.buddy.assistant/app.buddy.assistant.OnboardingActivity` | hooks=`[]` | overlays=`0` | texts=`step 2 of 6 / Skip setup / Let Buddy see and tap / Buddy's accessibility service shows the bubble and lets the agent read the screen, tap and type, only when you ask it to do something. / Nothing leaves the phone except what Claude Code sends to Anthropic to answer you. Sending, posting, buying and deleting always ask for your OK first.`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `app.buddy.assistant` / `OnboardingActivity` | `-` | 11 | 453 / 否 | `click` → [11] Button text="Get started" (click) center=(540,2032 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `app.buddy.assistant` / `OnboardingActivity` | `-` | 30 | 408 / 否 | `click` → [30] Button text="Continue" (click) center=(540,2032) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `app.buddy.assistant` / `OnboardingActivity` | `-` | 7 | 413 / 否 | `click` → [7] Button text="Open accessibility settings" (click) c | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `app.buddy.assistant` / `OnboardingActivity` | `-` | 8 | 818 / 否 | `click` → [8] Button text="Agree and continue" (click) center=(78 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 214 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_05_layout.xml` + `step_05_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`app.buddy.assistant/OnboardingActivity`)**: `Skip setup` | `Meet Buddy` | `A chat bubble that can use your phone for you.` | `Ask in plain words` | `"Reply to Sam that I'm late", "add milk to my basket".` | `Your own plan, no API key` | `Runs Claude Code from your Claude subscription. Codex w` | `You stay in control` | `Sending, posting, buying and deleting always ask first.` | `setup takes about 5 minutes`
- **Step 2 (`app.buddy.assistant/OnboardingActivity`)**: `step 1 of 6` | `Skip setup` | `Choose your agent` | `Who answers your chats. You can add others later in Set` | `CC` | `Claude Code` | `recommended` | `Uses your Claude subscription (Pro or Max).` | `CX` | `Codex`
- **Step 3 (`app.buddy.assistant/OnboardingActivity`)**: `step 2 of 6` | `Skip setup` | `Let Buddy see and tap` | `Buddy's accessibility service shows the bubble and lets` | `Nothing leaves the phone except what Claude Code sends ` | `In the list: Downloaded apps → Buddy assistant → turn i` | `Open accessibility settings`
- **Step 4 (`app.buddy.assistant/OnboardingActivity`)**: `How Buddy uses accessibility` | `Buddy uses Android's accessibility service to do what y` | `While a task runs, the screen content, which can includ` | `Buddy has no servers of its own. It doesn't collect, se` | `Before anything that sends, posts, buys or deletes, Bud` | `Privacy policy` | `No thanks` | `Agree and continue`
- **Step 5 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Buddy assistant` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以「聊天泡泡替你操作手机」为卖点，经六步引导（选代理→应用内隐私同意弹层）把用户引至系统无障碍设置，最终弹出「完全控制设备」的系统高危授权警告；拒绝授权后返回应用仍停在第2步，并反复重新拉起诱导弹层施压。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 「认识Buddy：一个能替你操作手机的聊天泡泡」（引导首屏）
- 英文 -> 「用大白话下指令即可，如『回复Sam说我迟到了』『把牛奶加进购物车』」（引导首屏）
- 英文 -> 「用你自己的订阅，无需 API Key」（引导首屏）
- 英文 -> 「你始终掌控：发送、发帖、购买、删除前都会先询问」（引导首屏、第2步）
- 英文 -> 「除所选代理发给AI服务商的内容外，其他都不离开手机」（第2步、服务详情页）
- 英文 -> 「Buddy没有自己的服务器，不收集、不出售、不共享这些数据，也不用于广告」（应用内隐私同意弹层）
- 英文 -> 「设置大约只需5分钟」（引导首屏，降低心理门槛）
- 英文 -> 「OpenCode：免费·限量」（第1步，低价诱饵选项）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: OnboardingActivity** | 引导首屏介绍「Meet Buddy」聊天泡泡可代你操作手机，强调用现有订阅无需API Key、敏感操作前会询问；点击「Get started」进入六步向导。 | `step_01_action.png` |
| 2 | **Step 2: OnboardingActivity** | 向导第1步「选择代理」，列出Claude Code（推荐）、Codex、OpenCode（免费限量）三张卡片；保留默认代理后点击「Continue」进入下一步。 | `step_02_action.png` |
| 3 | **Step 3: OnboardingActivity** | 向导第2步索取无障碍权限，称仅在用户要求时读屏、点击、输入，数据只发给所选AI；点击「Open accessibility settings」跳转系统设置。 | `step_03_action.png` |
| 4 | **Step 4: OnboardingActivity** | 应用内隐私同意弹层，说明读屏代操作、屏幕内容含个人信息将发往第三方AI、无自有服务器；点击「Agree and continue」进入系统无障碍列表。 | `step_04_action.png` |
| 5 | **Step 5: [无障碍列表页]** | 跳至系统无障碍设置页，「已下载应用」中Buddy assistant显示为关闭；探针在此捕获无障碍页钩子后自动终止，尚未真正授权。 | `step_05_screen.png` |
| 6 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留系统无障碍设置列表页，无弹窗、无遮罩，未出现二次引导或跳回应用。 | `step_05_probe_800ms_screen.png` |
| 7 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍在系统无障碍列表页，遮罩数为0，页面文本为空，未出现系统警告或诱导覆盖层。 | `step_05_probe_2000ms_screen.png` |
| 8 | **服务详情页** | 无障碍服务详情页：显示「使用Buddy assistant」开关与快捷键选项，长文描述读屏代操作及数据仅发往所选AI服务商；本步仅查看未开启。 | `step_05_service_detail_screen.png` |
| 9 | **系统警告弹窗(点Deny)** | 系统原生高危警告弹窗：询问是否允许完全控制设备，列明可读取全部屏幕、覆盖显示、代替用户操作等风险，含「允许/拒绝」；仅查看未授权。 | `step_05_system_warning_screen.png` |
| 10 | **拒权返回 +2.0s** | 拒绝授权返回后2秒：应用仍停在第2步无障碍引导页，并再次自动拉起同类诱导弹层（RELAUNCHED_LURE_DIALOG），持续施压。 | `step_05_refusal_2000ms_screen.png` |
| 11 | **拒权返回 +10.5s** | 拒权后10.5秒：再次回到同一无障碍引导页并重新拉起诱导弹层，未提供有效降级或放弃路径，形成循环引导。 | `step_05_refusal_10500ms_screen.png` |

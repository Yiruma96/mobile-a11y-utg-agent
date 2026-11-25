# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:27:56
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`yzl.nctvmzbwcbmjrzxpfibmjvptielpyasykfpprzz.rhiefdziwmvbmueyvbfcbbmehxbtzcutjjgmb`（静态标签：`malicious` / `Svpeng` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `3` 个，有向边 `2` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / The Services are provided by Google Inc. (“Google”), located at 1600 Amphitheatre Parkway, Mountain View, CA 94043, United States. 

 By using our Services, you are agreeing to these terms: 

 Our Services are very diverse, so sometimes additional terms or product requirements (including age requirements) may apply. Additional terms will be available with the relevant Services, and those additional terms become part of your agreement with us if you use those Services. 

 You must follow any policies made available to you within the Services. 

 Don’t misuse our Services. For example, don’t interfere with our Services or try to access them using a method other than the interface and the instructions that we provide. You may use our Services only as permitted by law, including applicable export and re-export control laws and regulations. We may suspend or stop providing our Services to you if you do not comply with our terms or policies or if we are investigating suspected misconduct. 

 Using our Services does not give you ownership of any intellectual property rights in our Services or the content you access. You may not use content from our Services unless you obtain permission from its owner or are otherwise permitted by law. These terms do not grant you the right to use any branding or logos used in our Services. Don’t remove, obscure, or alter any legal notices displayed in or along with our Services. 

 Our Services display some content that is not Google’s. This content is the sole responsibility of the entity that makes it available. We may review content to determine whether it is illegal or violates our policies, and we may remove or refuse to display content that we reasonably believe violates our policies or the law. But that does not necessarily mean that we review content, so please don’t assume that we do. 

 In connection with your use of the Services, we may send you service announcements, administrative messages, and other information. You may opt out of some of those communications. 

 Some of our Services are available on mobile devices. Do not use such Services in a way that distracts you and prevents you from obeying traffic or safety laws.`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 23 | 251 / 否 | `click` → [23] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 3 | 149 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Adobe Flash Player to access` | `Call logs` | `read and write phone call log` | `Contacts` | `access your contacts` | `Files and media` | `access photos, media, and files on your device` | `Phone` | `make and manage phone calls` | `SMS`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Adobe Flash Player` | `This app was built for an older version of Android and ` | `OK`

## 中文逐页引导链路解读

> **全链路总结**：应用先以“Adobe Flash Player”名义诱导用户接受通话记录、联系人、文件媒体、电话和短信等敏感权限，随后跳转无障碍设置并触发钩子与探针；拒权返回后仍重新拉起无障碍设置，且页面混入大段Google服务条款文本，符合Svpeng滥用权限与无障碍诱导特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许Adobe Flash Player访问哪些内容”（Step 1 权限审核页，借Adobe Flash Player名义诱导接受敏感权限）
- 英文 -> “此应用针对旧版Android构建，可能无法正常运行；请检查更新或联系开发者”（Step 2 无障碍列表页，以兼容性提示降低警惕）
- 英文 -> “服务由Google Inc.提供……使用服务即表示同意这些条款”（拒权返回页，以Google服务条款长文本伪装或填充页面）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 权限审核页：伪装Adobe Flash Player，索要通话记录、联系人、文件、电话及短信权限；点“继续”推进，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 无障碍列表页：显示Adobe Flash Player与旧版Android警告；捕获无障碍钩子及探针后自动终止，无通知或遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍停留在无障碍设置页，界面无文本；未出现通知横幅或遮罩，仅等待观察。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒探针：仍为无障碍设置页，界面文本为空；无通知横幅、无遮罩，继续等待。 | `step_02_probe_2000ms_screen.png` |
| 5 | **拒权返回 +2.0s** | 拒权返回后2秒：无障碍设置页显示“已下载应用”，并混入大段Google条款；拒权后仍重新拉起无障碍设置，无通知或遮罩。 | `step_02_refusal_2000ms_screen.png` |

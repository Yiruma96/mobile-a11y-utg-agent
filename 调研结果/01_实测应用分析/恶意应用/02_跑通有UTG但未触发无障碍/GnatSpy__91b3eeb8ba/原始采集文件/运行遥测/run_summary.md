# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:47:02
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.facebookupdate`（静态标签：`malicious` / `GnatSpy` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 6 | 75 / 否 | `click` → [4] Button text="While using the app" id=permission_all | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 55 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 62 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 81 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 61 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.facebookupdate` / `FacebookUpdate` | `-` | 4 | 62 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.facebookupdate` / `FacebookUpdate` | `-` | 4 | 62 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.facebookupdate` / `FacebookUpdate` | `-` | 4 | 62 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Facebook Update to record audio?` | `While using the app` | `Only this time` | `Deny`
- **Step 2 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Facebook Update to access your contacts?` | `Allow` | `Deny`
- **Step 3 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Facebook Update to make and manage phone calls?` | `Allow` | `Deny`
- **Step 4 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Facebook Update to access photos, media, and file` | `Allow` | `Deny`
- **Step 5 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Facebook Update to send and view SMS messages?` | `Allow` | `Deny`
- **Step 6 (`com.facebookupdate/FacebookUpdate`)**: `Facebook` | `© 2017–2018 Facebook Inc.` | `All rights reserved` | `Updating …`
- **Step 7 (`com.facebookupdate/FacebookUpdate`)**: `Facebook` | `© 2017–2018 Facebook Inc.` | `All rights reserved` | `Updating …`
- **Step 8 (`com.facebookupdate/FacebookUpdate`)**: `Facebook` | `© 2017–2018 Facebook Inc.` | `All rights reserved` | `Updating …`

## 中文逐页引导链路解读

> **全链路总结**：该 GnatSpy 样本以“Facebook Update”为伪装名，连续索取麦克风、联系人、电话、存储媒体和短信权限，随后展示仿冒 Facebook 的“Updating …”页面，并静态跳转至无障碍服务设置及录音/接收器组件，呈现强制授权与品牌仿冒链路。本轮观测未见通知横幅或悬浮遮罩，拒权分支未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “允许 Facebook Update 录制音频？”（Step 1 麦克风授权页）
- 英语 -> “仅在使用应用时”（Step 1 授权选项）
- 英语 -> “允许 Facebook Update 访问联系人？”（Step 2 联系人授权页）
- 英语 -> “允许 Facebook Update 拨打和管理电话？”（Step 3 电话授权页）
- 英语 -> “允许 Facebook Update 访问照片、媒体和文件？”（Step 4 存储媒体授权页）
- 英语 -> “允许 Facebook Update 发送和查看短信？”（Step 5 短信授权页）
- 英语 -> “Facebook / © 2017–2018 Facebook Inc. / 版权所有 / 正在更新…”（Step 6–8 仿冒 Facebook 更新页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: GrantPermissionsActivity** | 系统麦克风授权弹窗，询问是否允许“Facebook Update”录音；点击“仅在使用时”，授予前台麦克风权限，无通知横幅/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: GrantPermissionsActivity** | 系统联系人授权弹窗，英文询问是否允许“Facebook Update”访问联系人；点击“允许”，授予联系人权限，无通知横幅/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: GrantPermissionsActivity** | 系统电话授权弹窗，询问是否允许“Facebook Update”拨打和管理电话；点击“允许”，授予电话权限，无通知横幅/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: GrantPermissionsActivity** | 系统存储/媒体授权弹窗，询问是否允许访问照片、媒体和文件；点击“允许”，授予存储媒体权限，无通知横幅/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: GrantPermissionsActivity** | 系统短信授权弹窗，询问是否允许“Facebook Update”发送和查看短信；点击“允许”，授予短信权限，无通知横幅/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: FacebookUpdate** | 仿冒 Facebook 的启动/更新页，显示“正在更新…”及 2017–2018 版权；探针静态跳转至无障碍服务设置 Activity，无通知/遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: FacebookUpdate** | 仍为仿冒 Facebook 更新页，保留“正在更新…”与版权字样；探针静态跳转至应用内 .activities.FacebookUpdate，无通知/遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: FacebookUpdate** | 重复仿冒 Facebook 更新页，显示“正在更新…”和版权；探针静态跳转至 .Receivers.CallRecorderReceiver（通话录音接收器），无通知/遮罩。 | `step_08_screen.png` |

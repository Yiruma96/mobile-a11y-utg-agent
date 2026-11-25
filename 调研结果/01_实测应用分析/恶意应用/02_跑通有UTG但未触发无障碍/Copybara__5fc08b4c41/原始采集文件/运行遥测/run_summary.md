# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:48:11
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.ilmybnlapp.apk`（静态标签：`malicious` / `Copybara` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.ilmybnlapp.apk` / `main` | `-` | 1 | 0 / 是 | `swipe` → [540, 1800] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.ilmybnlapp.apk` / `main` | `-` | 10 | 617 / 否 | `click` → [10] Button text="Continue" (click) center=(540,2084) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.ilmybnlapp.apk` / `main` | `-` | 3 | 63 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,121 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.ilmybnlapp.apk` / `main` | `-` | 3 | 63 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,121 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.ilmybnlapp.apk` / `main` | `-` | 10 | 617 / 否 | `click` → [10] Button text="Continue" (click) center=(540,2084) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.ilmybnlapp.apk` / `main` | `-` | 3 | 63 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.ilmybnlapp.apk` / `main` | `-` | 3 | 63 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.ilmybnlapp.apk` / `main` | `-` | 3 | 63 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.ilmybnlapp.apk/main`)**: (空文本)
- **Step 2 (`com.ilmybnlapp.apk/main`)**: `IgUZCQFSnEDVRQvzrjDBCU5wO0xBLpqRcFeY98Fyus` | `Shizuku LP Integration` | `Required to edit other apps memory with ADB/Shizuku aft` | `Click the "Continue" button and follow the steps to ena` | `1 Open settings` | `2 In Accessibility, open the "Downloaded Services" or "` | `3 Activate the "Star Patcher" option.` | `Continue`
- **Step 3 (`com.ilmybnlapp.apk/main`)**: `No internet` | `Please make sure you are connected to the internet` | `OK`
- **Step 4 (`com.ilmybnlapp.apk/main`)**: `No internet` | `Please make sure you are connected to the internet` | `OK`
- **Step 5 (`com.ilmybnlapp.apk/main`)**: `IgUZCQFSnEDVRQvzrjDBCU5wO0xBLpqRcFeY98Fyus` | `Shizuku LP Integration` | `Required to edit other apps memory with ADB/Shizuku aft` | `Click the "Continue" button and follow the steps to ena` | `1 Open settings` | `2 In Accessibility, open the "Downloaded Services" or "` | `3 Activate the "Star Patcher" option.` | `Continue`
- **Step 6 (`com.ilmybnlapp.apk/main`)**: `No internet` | `Please make sure you are connected to the internet` | `OK`
- **Step 7 (`com.ilmybnlapp.apk/main`)**: `No internet` | `Please make sure you are connected to the internet` | `OK`
- **Step 8 (`com.ilmybnlapp.apk/main`)**: `No internet` | `Please make sure you are connected to the internet` | `OK`

## 中文逐页引导链路解读

> **全链路总结**：应用从主WebView入口下滑露出“Shizuku LP集成”说明页，借“修改他应用/系统应用需启用无障碍Star Patcher”话术诱导点击Continue；随后反复弹出“No internet”阻断框，并以静态跳转探针指向service与AdminReceiver，未实际完成授权/拒权测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “Shizuku LP Integration…Required to edit other apps memory with ADB/Shizuku…Also needed to edit system apps like the Google Playstore”核心意译：声称需用ADB/Shizuku修改其他应用内存，甚至系统应用与Play商店（Step2、Step5）。
- 英文 -> “Click the ‘Continue’ button…The normal functions…not used…but the service must exist…”核心意译：诱导点击Continue并按步骤启用服务，谎称读屏与模拟点击不被使用但服务必须存在（Step2、Step5）。
- 英文 -> “1 Open settings / 2 In Accessibility… / 3 Activate the ‘Star Patcher’ option.”核心意译：手把手引导进入设置、无障碍已下载/已安装服务并激活Star Patcher（Step2、Step5）。
- 英文 -> “No internet / Please make sure you are connected to the internet / OK”核心意译：以未联网阻断弹窗催促仅点OK，制造无法继续的假象（Step3、Step4、Step6-Step8）。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: main** | 第1页为主WebView空白页，无可见文案；向下滑动以露出疑似Continue按钮，未见通知、遮罩或取消键。 | `step_01_action.png` |
| 2 | **Step 2: main** | 第2页为Shizuku LP集成诱导页，称需ADB/Shizuku修改他应用内存与系统应用；点击Continue引导开启无障碍Star Patcher，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: main** | 第3页弹出“No internet/请确保联网”阻断弹窗，仅有OK按钮，无取消键、通知或遮罩；点击OK试图继续引导流程。 | `step_03_action.png` |
| 4 | **Step 4: main** | 第4页仍为“No internet”联网阻断弹窗，仅OK无取消；因上次点击未生效再次点击OK，未见通知横幅或遮罩。 | `step_04_action.png` |
| 5 | **Step 5: main** | 第5页回到Shizuku LP集成说明页，重复要求点击Continue并按步骤激活Star Patcher无障碍服务；无通知、遮罩或取消键。 | `step_05_action.png` |
| 6 | **Step 6: main** | 第6页仍显示“No internet”联网阻断弹窗，仅有OK；探针执行静态Activity跳转至service2_BR，未注册点击，无通知或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: main** | 第7页继续停留“No internet”弹窗，仅OK无取消；探针静态跳转AdminReceiver2，疑似设备管理/管理员接收器，无通知或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: main** | 第8页仍为“No internet”阻断弹窗，仅OK；探针静态跳转service1_BR，未完成授权交互，无通知横幅与遮罩。 | `step_08_screen.png` |

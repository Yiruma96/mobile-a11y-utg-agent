# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:11:51
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.demo.testing`（静态标签：`malicious` / `hawkshaw` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.demo.testing` / `HawkshawMainActivity` | `-` | 5 | 42 / 否 | `click` → [2] EditText text="Username" id=username (click) center | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.demo.testing` / `HawkshawMainActivity` | `-` | 5 | 42 / 否 | `type` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.demo.testing` / `HawkshawMainActivity` | `-` | 5 | 41 / 否 | `click` → [3] EditText text="Password" id=password (click) center | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.demo.testing` / `HawkshawMainActivity` | `-` | 5 | 41 / 否 | `type` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.demo.testing` / `HawkshawMainActivity` | `-` | 5 | 41 / 否 | `click` → [5] Button text="LOGIN" id=login (click) center=(825,83 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.demo.testing` / `HawkshawMainActivity` | `-` | 5 | 41 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.demo.testing` / `HawkshawMainActivity` | `-` | 5 | 41 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.demo.testing` / `HawkshawMainActivity` | `-` | 5 | 41 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.demo.testing/HawkshawMainActivity`)**: `Idea Security` | `Username` | `Password` | `REGISTER` | `LOGIN`
- **Step 2 (`com.demo.testing/HawkshawMainActivity`)**: `Idea Security` | `Username` | `Password` | `REGISTER` | `LOGIN`
- **Step 3 (`com.demo.testing/HawkshawMainActivity`)**: `Idea Security` | `user123` | `Password` | `REGISTER` | `LOGIN`
- **Step 4 (`com.demo.testing/HawkshawMainActivity`)**: `Idea Security` | `user123` | `Password` | `REGISTER` | `LOGIN`
- **Step 5 (`com.demo.testing/HawkshawMainActivity`)**: `Idea Security` | `user123` | `••••••••` | `REGISTER` | `LOGIN`
- **Step 6 (`com.demo.testing/HawkshawMainActivity`)**: `Idea Security` | `user123` | `••••••••` | `REGISTER` | `LOGIN`
- **Step 7 (`com.demo.testing/HawkshawMainActivity`)**: `Idea Security` | `user123` | `••••••••` | `REGISTER` | `LOGIN`
- **Step 8 (`com.demo.testing/HawkshawMainActivity`)**: `Idea Security` | `user123` | `••••••••` | `REGISTER` | `LOGIN`

## 中文逐页引导链路解读

> **全链路总结**：应用从“Idea Security”登录页采集用户名与密码，点击 LOGIN 后未出现可见授权弹窗或通知，随后静态探针依次跳转无障碍、秘密拨号盘码接收器、设备管理接收器；本轮拒权结果未测试。核心特征是伪装安全品牌收集凭据并探测高危组件。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Idea Security（英文） -> “理念安全/创意安全”（登录页），以安全品牌名包装登录入口
- REGISTER/LOGIN（英文） -> 注册/登录（登录页按钮），推动用户完成账号密码提交

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: HawkshawMainActivity** | 登录页显示“Idea Security”、用户名/密码、注册/登录；本步点击用户名框，无通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: HawkshawMainActivity** | 仍为登录页，用户名框已聚焦；探针在框内输入用户名，页面无新增提示，也无通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: HawkshawMainActivity** | 登录页用户名已填为 user123；本步点击密码框以准备输入密码，仍无通知横幅或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: HawkshawMainActivity** | 用户名保持 user123，密码框聚焦；探针输入密码，界面未弹出说明或权限提示，无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: HawkshawMainActivity** | 密码显示为八个圆点，凭据已填；本步点击 LOGIN/登录，未出现弹窗或通知，仍为登录页。 | `step_05_action.png` |
| 6 | **Step 6: HawkshawMainActivity** | 界面仍为已填凭据的登录页；静态引导跳转探针指向 Accessibility/无障碍组件，未见授权弹窗或通知。 | `step_06_screen.png` |
| 7 | **Step 7: HawkshawMainActivity** | 登录页未变；静态探针跳转 SecretDialPadCodeReceiver/秘密拨号盘码接收器，无可见界面、通知或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: HawkshawMainActivity** | 登录页未变；静态探针跳转 MyDeviceAdminReceiver/设备管理接收器，试图触发设备管理授权路径，无可见提示。 | `step_08_screen.png` |

# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:16:53
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.stub`（静态标签：`malicious` / `Chameleon` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.stub` / `MainActivity` | `-` | 1 | 0 / 是 | `click` → [241, 1256] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.stub` / `MainActivity` | `-` | 4 | 26 / 否 | `type` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.stub` / `MainActivity` | `-` | 4 | 33 / 否 | `click` → [4] Button text="Next" (click) center=(903,1215) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.stub` / `MainActivity` | `-` | 6 | 49 / 否 | `click` → [3] EditText text="EMP1001" (click) center=(443,871) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.stub` / `MainActivity` | `-` | 6 | 49 / 否 | `click` → [4] Button text="Next" (click) center=(903,1215) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.stub` / `MainActivity` | `-` | 1 | 8 / 是 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.stub` / `MainActivity` | `-` | 6 | 42 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.stub` / `MainActivity` | `-` | 6 | 42 / 否 | `click` → [3] EditText (click) center=(443,1215) | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.stub/MainActivity`)**: (空文本)
- **Step 2 (`com.stub/MainActivity`)**: `Document` | `Hey, Login Now` | `Next`
- **Step 3 (`com.stub/MainActivity`)**: `Document` | `Hey, Login Now` | `EMP1001` | `Next`
- **Step 4 (`com.stub/MainActivity`)**: `Document` | `Hey, Login Now` | `EMP1001` | `Next` | `Forgot password?`
- **Step 5 (`com.stub/MainActivity`)**: `Document` | `Hey, Login Now` | `EMP1001` | `Next` | `Forgot password?`
- **Step 6 (`com.stub/MainActivity`)**: `Document`
- **Step 7 (`com.stub/MainActivity`)**: `Document` | `Hey, Login Now` | `Next` | `Forgot password?`
- **Step 8 (`com.stub/MainActivity`)**: `Document` | `Hey, Login Now` | `Next` | `Forgot password?`

## 中文逐页引导链路解读

> **全链路总结**：该应用以MainActivity承载假CRM WebView登录页，用“Hey, Login Now”“Next”“Forgot password?”及EMP1001占位员工ID诱导提交；随后静态跳转至MyJavaScriptInterface/WebView主活动，未触发系统授权或拒权（not_tested），元数据标记malicious/Chameleon。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Hey, Login Now -> 嘿，立即登录（假CRM登录页，Step 2-5、7-8）
- Next -> 下一步（假CRM登录页，Step 2-5、7）
- Forgot password? -> 忘记密码？（假CRM登录页，Step 4-5、7-8）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 假CRM WebView登录页，界面无可见文案；点击坐标[241,1256]疑似“员工ID”输入框，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 同一假CRM登录页显示“Hey, Login Now（嘿，立即登录）”“Next（下一步）”；向聚焦输入框键入占位员工ID。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 登录页显示EMP1001与“Next（下一步）”；点击下一步提交员工ID推进虚假登录，无通知横幅或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 登录页出现“Forgot password?（忘记密码？）”；回点员工ID输入框，界面仍仅见占位EMP1001，无系统弹窗。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 员工ID已填EMP1001；再次点击“Next（下一步）”提交，页面无通知横幅、无遮罩，也未出现取消入口。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 界面仅剩“Document（文档）”标题；静态跳转至MyJavaScriptInterface，疑似WebView JS桥接口，无通知/遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: MainActivity** | 回到假CRM登录页，显示“Hey, Login Now（嘿，立即登录）”；静态跳转至WebView主活动，无通知/遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: MainActivity** | 再点员工ID输入框重填；登录页仍显示“Hey, Login Now（嘿，立即登录）”“Next”“Forgot password?”，无通知/遮罩。 | `step_08_action.png` |

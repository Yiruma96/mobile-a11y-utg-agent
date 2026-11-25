# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:56:59
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.bean.cousin`（静态标签：`malicious` / `Sova` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`success`（共执行 2 步，UTG 唯一节点 `1` 个，有向边 `1` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.bean.cousin` / `AccessibilityGuideActivity` | `-` | 5 | 109 / 否 | `click` → [5] TextView text="OK" id=ok_button (click) center=(540 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.bean.cousin` / `AccessibilityGuideActivity` | `-` | 5 | 109 / 否 | `terminate` → App flow reached the guide dialog while System Accessib | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.bean.cousin/AccessibilityGuideActivity`)**: `Chrome` | `1. Open the Accessibility settings` | `2. Select Enable Accessibility Service` | `3. Slide the switch to enable` | `OK`
- **Step 2 (`com.bean.cousin/AccessibilityGuideActivity`)**: `Chrome` | `1. Open the Accessibility settings` | `2. Select Enable Accessibility Service` | `3. Slide the switch to enable` | `OK`

## 中文逐页引导链路解读

> **全链路总结**：应用入口即弹出仿Chrome的无障碍引导弹窗，并以通知横幅催促“为Chrome启用访问”，点击OK诱导跳转系统无障碍设置；流程在Chrome开关关闭时终止，未实际授权，拒权路径未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “Chrome”（第1/2步引导弹窗，冒充浏览器身份）
- 英文 -> “1. 打开无障碍设置；2. 选择启用无障碍服务；3. 滑动开关以启用”（第1/2步引导弹窗，分步诱导授权）
- 英文 -> “OK”（第1/2步引导弹窗，仅确认键，无取消键）
- 英文通知 -> 标题“更新应用访问权限”、正文“为‘Chrome’启用访问权限”（第1/2步通知横幅，催促开启无障碍）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: AccessibilityGuideActivity** | 应用弹出仿Chrome无障碍引导，英文三步要求打开设置并启用服务；通知称“为Chrome启用访问”，点OK转向系统设置，无取消键。 | `step_01_action.png` |
| 2 | **Step 2: AccessibilityGuideActivity** | 本步仍显示同一仿Chrome引导，通知继续催促为Chrome开启访问；探针在系统无障碍设置Chrome开关关闭时终止，未完成授权。 | `step_02_action.png` |

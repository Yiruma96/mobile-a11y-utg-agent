# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:24:33
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.sdfabfnf.efpkfohw`（静态标签：`malicious` / `TeaBot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`success`（共执行 1 步，UTG 唯一节点 `1` 个，有向边 `0` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.sdfabfnf.efpkfohw` / `KoRErkHpuBNWucj` | `-` | 12 | 562 / 否 | `terminate` → App launched via its loader Activity and presented the  | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.sdfabfnf.efpkfohw/KoRErkHpuBNWucj`)**: `PDF AI: TEXT RECOGNISER` | `Accessibility` | `Screen readerGet spoken audio guidance and special cont` | `Visibility enhancementsChange size, contrast, and colou` | `Hearing enhancementsAdjust the audio to help your heari` | `Interaction and dexterityEnhance or replace touch inter` | `Advanced settingsManage Direct access and other advance` | `Installed services5 services` | `About Accessibility` | `Contact Us`

## 中文逐页引导链路解读

> **全链路总结**：应用通过加载器 Activity 启动后，立即跳转到系统“无障碍”设置页，并以英文提示诱导用户启用无障碍服务；本次轨迹未实际完成授权或拒权测试即终止，核心特征是伪装成 PDF AI 文字识别器并借用系统设置页骗取高权限。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- PDF AI: TEXT RECOGNISER -> PDF AI：文字识别器（Step 1 无障碍设置页，应用伪装名称）
- You need enable Accessibility -> 你需要启用无障碍功能（Step 1 无障碍设置页提示气泡）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: KoRErkHpuBNWucj** | 系统无障碍设置页，顶部伪装名“PDF AI：文字识别器”，英文提示“需启用无障碍”；本步终止，无通知、无遮罩。 | `step_01_action.png` |

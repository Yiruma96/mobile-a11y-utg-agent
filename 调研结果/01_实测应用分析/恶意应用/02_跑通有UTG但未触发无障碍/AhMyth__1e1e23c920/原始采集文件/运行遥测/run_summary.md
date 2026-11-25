# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:35:39
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.android.vendng`（静态标签：`malicious` / `AhMyth` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 4 | 184 / 否 | `click` → [4] Button text="Allow" id=button1 (click) center=(887, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 6 | 88 / 否 | `click` → [4] Button text="While using the app" id=permission_all | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 6 | 87 / 否 | `click` → [4] Button text="While using the app" id=permission_all | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 6 | 70 / 否 | `click` → [4] Button text="While using the app" id=permission_all | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 50 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 57 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 57 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 57 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Let app always run in background?` | `Allowing Flashlight to always run in the background may` | `Deny` | `Allow`
- **Step 2 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Flashlight to take pictures and record video?` | `While using the app` | `Only this time` | `Deny`
- **Step 3 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Flashlight to access this device’s location?` | `While using the app` | `Only this time` | `Deny`
- **Step 4 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Flashlight to record audio?` | `While using the app` | `Only this time` | `Deny`
- **Step 5 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Flashlight to access your contacts?` | `Allow` | `Deny`
- **Step 6 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Flashlight to make and manage phone calls?` | `Allow` | `Deny`
- **Step 7 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Flashlight to make and manage phone calls?` | `Allow` | `Deny`
- **Step 8 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Flashlight to make and manage phone calls?` | `Allow` | `Deny`

## 中文逐页引导链路解读

> **全链路总结**：应用借“手电筒”名义先引导开启电池后台豁免，再连续索取相机、定位、麦克风、联系人和电话权限，随后静态跳转至无障碍服务及包/屏幕接收器，呈现AhMyth式远控与持久化特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Let app always run in background?（英文）-> 让应用始终在后台运行？（Step 1 电池优化豁免页）
- Allowing Flashlight to always run in the background may reduce battery life...（英文）-> 允许“手电筒”始终后台运行可能缩短电池续航，可稍后在设置中更改（Step 1 电池优化豁免页）
- Allow Flashlight to take pictures and record video?（英文）-> 允许“手电筒”拍照和录像？（Step 2 相机权限页）
- Allow Flashlight to access this device’s location?（英文）-> 允许“手电筒”访问本机位置？（Step 3 定位权限页）
- Allow Flashlight to record audio?（英文）-> 允许“手电筒”录制音频？（Step 4 录音权限页）
- Allow Flashlight to access your contacts?（英文）-> 允许“手电筒”访问联系人？（Step 5 联系人权限页）
- Allow Flashlight to make and manage phone calls?（英文）-> 允许“手电筒”拨打电话和管理通话？（Step 6-8 电话权限页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: RequestIgnoreBatteryOptimi** | 电池优化豁免页，英文询问是否让“手电筒”始终后台运行；有vendng空通知、无遮罩，本步点Allow。 | `step_01_action.png` |
| 2 | **Step 2: GrantPermissionsActivity** | 相机权限页，英文请求允许“手电筒”拍照和录像；有vendng空通知、无遮罩，本步点“仅使用时允许”。 | `step_02_action.png` |
| 3 | **Step 3: GrantPermissionsActivity** | 定位权限页，英文请求允许“手电筒”访问本机位置；有vendng空通知、无遮罩，本步点“仅使用时允许”。 | `step_03_action.png` |
| 4 | **Step 4: GrantPermissionsActivity** | 录音权限页，英文请求允许“手电筒”录制音频；有vendng空通知、无遮罩，本步点“仅使用时允许”。 | `step_04_action.png` |
| 5 | **Step 5: GrantPermissionsActivity** | 联系人权限页，英文请求允许“手电筒”访问联系人；有vendng空通知、无遮罩，本步点Allow。 | `step_05_action.png` |
| 6 | **Step 6: GrantPermissionsActivity** | 电话权限页，英文请求允许“手电筒”拨打电话和管理通话；有vendng空通知、无遮罩，未点按钮，静态跳转无障碍服务。 | `step_06_screen.png` |
| 7 | **Step 7: GrantPermissionsActivity** | 电话权限页，英文请求允许“手电筒”拨打电话和管理通话；有vendng空通知、无遮罩，未点按钮，静态跳转包监听接收器。 | `step_07_screen.png` |
| 8 | **Step 8: GrantPermissionsActivity** | 电话权限页，英文请求允许“手电筒”拨打电话和管理通话；有vendng空通知、无遮罩，未点按钮，静态跳转屏幕接收器。 | `step_08_screen.png` |

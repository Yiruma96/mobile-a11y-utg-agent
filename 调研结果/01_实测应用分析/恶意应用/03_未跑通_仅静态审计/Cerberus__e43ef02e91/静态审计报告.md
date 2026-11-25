# MR_021__e43ef02e91｜Cerberus — com.whatsapp

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：162.8s

## 1. 一句话核心结论

- **核心申请方式**：以 com.whatsapp 为应用名与无障碍服务标签，将无障碍服务实现藏入 Avast VPS 加密载荷、由 Application 启动即解密注入，且无障碍配置刻意不写 description，属典型诱骗授权型（UTG）无障碍投递框架。
- **静态可见性说明**：Manifest、无障碍配置 xml 与 base64 字符串资源静态可见；但 Manifest 声明的无障碍服务类 seqydttlpalajgmhmj.sdortecrxqaqiwsl.cluuac.znxuix 在 classes.dex（472 类、6 个包）中完全不存在，其真实实现与引导跳转逻辑均位于加密二阶段载荷 assets/db_dex.nmp、db_evoapk.dat、db_crt.dat（头部为 AvastVpsAC1+/AvastVpsEA1+ 私有格式），由 Application 类 Amuffinpromote.attachBaseContext 解密落地后加载，故 UTG 页面流转与文案无法静态还原。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `e43ef02e91e34cc255d2d76b681e8b021532d00ad7fbbff7f8b2e3a1df843243` |
| 包名 / 年份 | `xpmwjinzd.qzcwcqqkimadlxdk.hsomeub` / 2020 |
| 家族 / 品类 | **Cerberus**（同池样本数：8） |
| 原始来源标识 | https://www.secureauth.com/blog/hijacking-2fa-a-look-at-mobile-malware-through-an-identity-lens/ |
| 桌面显示名 | com.whatsapp |
| 引导页宣称品牌/身份 | WhatsApp（未获授权的品牌冒用） |
| 系统无障碍列表服务名 | com.whatsapp |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置 res/xml/logvhecjds.xml 仅含 canRetrieveWindowContent/事件类型/Flags，未声明 android:description 与 android:summary，使系统无障碍列表项描述为空、警告文本被挤空；应用 android:label 与无障碍 service android:label 同为 com.whatsapp 形成品牌同形；另设 android:label="" + Theme.NoDisplay + excludeFromRecents 的隐身 Activity（ktxezfmbeebjga、upkaszm）；包名与类名均为随机字母串，全部业务类名做无意义词义混淆。 |
| 无障碍服务类名 | `seqydttlpalajgmhmj.sdortecrxqaqiwsl.cluuac.znxuix` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | 自定义 Application：xpmwjinzd.qzcwcqqkimadlxdk.hsomeub.Amuffinpromote（AndroidManifest android:name） | 进程启动时系统回调 attachBaseContext(Context)，随后 onCreate() | 不可静态还原 | 无 | 无（用户无感知） | `Amuffinpromote.attachBaseContext / Amuffinpromote.onCreate → noblehope / chargemansion / alreadyfamily / girlmyth / gatemotion / enrichcase` |
| 2 | 冷启动入口 | 解密落地文件加载的二阶段 DEX（源 assets/db_dex.nmp、db_evoapk.dat、db_crt.dat） | attachBaseContext 中 gatemotion(...) 返回 true 后调用 enrichcase(...) 完成装载；onCreate 再次调用 enrichcase | 不可静态还原 | **原文**：无（载荷加密，字符串不可读）<br>**译注**：载荷内应包含无障碍服务 znxuix 实现及后续引导/跳转代码，当前不可读 | 不可静态还原 | `Amuffinpromote.attachBaseContext（enrichcase 调用点）` |
| 3 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（预期目标页） | 预期由加密载荷内代码通过 Intent 拉起；classes.dex 中无任何 ACTION_ACCESSIBILITY_SETTINGS 字符串或调用点 | 系统无障碍页 | **原文**：无（classes.dex 未出现 android.settings.ACCESSIBILITY_SETTINGS 字面量）<br>**译注**：系统无障碍服务列表中会显示名为 com.whatsapp、描述为空白的服务项 | 不可静态还原（推测为要求用户点开该服务并开启开关） | `不可静态还原；对应列表项由 AndroidManifest service znxuix + res/xml/logvhecjds.xml 决定` |
| 4 | 引导说明页 | base64 密文字符串资源（actionSettingInection、LogSMS、autoClick、app_inject、base6401 等） | 运行期由解密载荷读取并 base64 解码后展示 | 不可静态还原 | **原文**：N2JjNA== / NmJjNw== / NmJjMg== / NmljNg== / NmNkNTk3NzkyMTQ1Y2JhM2JhYmNmYzQzNWQ2ZTBkNTY4MzgyNWVmMWM1MmFiYmNmZmIzMzgyZGIxNjk1NGVkMjE3MzhjMWNhYTk2NmFhODgyMmU0Njk2NzJjMWNiZmNjMDUxOTNjOTUyYTZiYjhjOTFlZmI1YmEwNzQ3NzY0YTUzZTIyYzczNDI3OWQ0ZTFkMmE2ODlkNjA1NjFmYmQ2ZDBhMzA4N2VmMTYxMWY0NmZlYWVhZDM2ZmJjYjJiZDg1YTJjMzBhYjU3MzUzYjBlNGYzMjA5Y2U4NzljOWU4MmU3NDI4MTg5ZWViZjFiZjdkY2M2OTMxNzg1Mzk2NjI5NjIxYzJkMDA1OGI4YjJiNjc0NjYzYTE4YTZjNGQ3ZDQyOGFlNDI4MzUyMDQzODNiNGU1NTUwZTM3MGJhYTU3MzE2YmE4YjIyZDIzYmI3MjkxMTFjZDVhYTljYTBmNjI2YzZiYTAxMmI3ZTllMmUwMmVlZDQwMzI2YmVhZDczNzY4NWY4YzBlZWRiMDAxMGVjYTRjNThiNTFjOTcxN2ZiN2Y2ZWRiZmFjNDdkZTMyN2E5NmQyMTQ2OGY4OGVmOWIxNjllNDYzNTgyZTcwODI1MDNlMTgwM2ZjMzc0MTJhNDM4OGZmMGMzYjdhNjM0YjIwZTA3OWQ1NmUwMzM0OTVjM2E5NTQzMWVhMjBiNTkxNGUxZDRlNjlhYmNlNWY2OGFjNWI4NzIzZDc2OTZiYTExOWJhNWE5NjU4MDFkNTk4ZGY5Y2U0ZjEyMTc2OTFkNmQ5ODZiZWQ1OGZmMDc0NWRkZGNiNTMxYTZlZGUyYTg1NDNlOWJhZGZmNDBhMjg0NzU2MGZhMjA3MDU4OWNjNmM2YTFhODE3MWFkMGNkYTA2OTIyODQ5NjIwZGU5NDI2MzgxNjRkNTIxY2E5YmRmMWI0YjY2YjcxOTZmN2I4NjQzOGRjZTVkYmRiMzAxNjU1Y2Q2Nzk3MWFlZmZkMGE5ZWU2MjE3ZWZhOGFkOTc3ODM2MjU1NTJkNDNlNmJiMDUwYTFiN2FjMzQ4NjM0NTM2YmE2N2ExZTdiNTNlMmZjY2Y5YjljMTBhMDkwMzRhYmI2OTA4Yjc0YWFkMjk1YmMwZTg4MTdmYzU1ZGYzMzQ1ZGMyNDRmMGMzZjRmZmYyZGMxYThiODQxNDNmMzg1M2RjNTZiYjEzMjk0MzU2NDNmOTZhNTQxNThjZGQ3ZTFlODcyMzJkMTRkOTM2ZGIzYzk2MGRiNWU4NTMyOTBjYzNiNzhmZTBjN2QzNGNhNzg1M2NlZTMwZDNjODhlNDllYTcwNTUzMjViNDcwMGM5YTBiMzVhMDUwOWJkMDMyYmRmOGJhNDhjNmY5ZDUyNzRkMDVmZTE4YjA4OTZmNTQyYWU1ZjU3MGJjNzM5NTYzYmFhYjdkMDI1YzBkY2IyZWQ4ZmMyZGMzZDc1NDFmZTEyZDhmY2MyMTMzYmEwMWIwNzAzZTU0OTFjMWY2ZTMxMjUzYzkxZGJmMzU5NmI4NmE2OWE1MWM0ZmRiODkyMjJkYWMwYzUwYWNjOWVkY2ZiZjY0OTNhZDAyMmU4Y2UwYWJhZWUzMjgyZmIzOTRjNDAzZGM3ZTg1YjQ4ODg5OWUyYjMzYjg5NzVjZWJhNDE5MWJlZDU3ZDEyNjk0ZGY1OTBiOGMxNDI4ZDI4MGE4OTNkZDFlNDA3OWNhMzFlMGU3MTUwZjQzOTE5MDQzMjAzY2YwZDhmNjZmZDZlZGIzYTUzNzgyM2U4ZDUzMjM4Y2JkYjA2MDgwNjg0MzNjMTczNTg4MWYwODc3MjgwYjE5NWFmMDk5Y2Y4MjZlMzQ2ZTQxOTVjMmMwMjYyYzMzYjA1NDM4NjE4NjJhNTQzMTIzMzc2MWU0MjBhMDFjMDIxZjljZDIxNzJiNjFmZDljZWIyYWViZDE3YWYxODJjMjBkYTI3NDFjNTE4NjlmMmNiZGQwZDQwNTY0NmU5ZDk1ZTk2Yjc5NTk1MDU1Mzk4YzM1NDU1NTZiMTMzNTYyOTJmNmQ4NDMzYmU0NWFjYWQ4MjNhMjg3MGRjODE1YWYyMTBkNTQ1M2UzYzQ5MGY2YzAxOGEyYzY0NjBhNDRhMGQ0MDY5N2FhNjVlMzIzYTEyYzY3ZmJkZjIxZTZhODdiMjMyMTMxNzIwMjhhZWM3Y2RhYWQ2NmUyMjVkN2E1MzkyNTM4Y2NkNzI5NzUwNzAyYzFkZjNiYzY3ZWExMmY3NjI2ODQzYTM0Yjg0ODAxMzRiYzc1MTNlYjc5NGM5MTZmODYzNmJkZTMyOTBhOWU1YjYyOGUzZmQ1NjhmYmI0ZWFiNTY1NmRjYmFlNDUxM2Y4NTFjZjlhMDViODJlNjE1OGRiNDA0YjliMzdjMDBjZDkxZjhhYTBhYWI1NmY0ZTNmZDc4YTEyMzVhMjEzMjQ3NjNiMzY2ODU1M2ZhYzFiN2Q5NTY3OTcxOWYwYmMyMTk2OTNjNDlmYWIwMmQ3OWY0YTRhMGZhMTA1YmRlMGFkYjdjMjEyMWY1MzJhNTI5Mzc1NmY3YmZhOTZiNjkwYTUyYzNkMzk0MGUxMjRkOGY4NDQzYTdiODQwOGY3MjkzNTA3ZGNmNTRhMDY0ZTFiZmQwYzIxMjBiZDcwMmI2NjdhOWRjNzE5NDBiYjViZmY0MWE3NzBlNzA2OTE0YzU2MTM1Y2EwMGIzYWJhZjg0YzM5NzdmNGNmNDQ2YmEzOGJlZWIwZmU4OWQzOWUyNzYxZmI5NDYxYTQzNDFkYWU0NjNkNjZiOTZhYmYyMzZlNDY0ZmE1NzNkY2Q4YzAzZGNlYzIzYjQzMWM0NmU3MGI5NWNhMTY0MWIwYzNlNjhmOWRhMzU2ZWZjZjdmNWEzMjRmNDhhZjVkYTY5YjJjNDg3Y2IwMWYxNTkxNmQ3MmE4MmEyN2ZiODBiMTdhZTM4ZjJmMjQyMjI0MDBkMjE0OWMxNWMyMTFiN2M3NDM4YWZiMjYzZDg2NDU3YTJhOWEzYzg1NzMyZmI0MDAyODQ1YmVhYTg4MTFjMzNjYzUzOTgyYjMyMDExMzdjMjJmNjNlZmIyNDE0ZDc1YzE0NjA5ZjQ4YmY5Mzc3YmMxMTY2YzUxOWY5MDhkYWRkNGYwZDNkYTMxOGE0ZmEwODRlZWY0ZGRjNjVkNjZjOTMxYmVlNTAxZTEyNDQyM2YxYzkxYzU2OTI4MjJjMDNjNzdiZTk4YWFiZDZhMmQ1NGI5NmJjZmI0YjRhOWExNjNlNTg3ZjhiNWY3NDQxYjhhZjg0MWJiMGJkZjRhMWY0ZDhhOTAzZmVmODNlYjAzYWQyMGMzMTZhMTQwOWRhN2E2MjU5OTg1YWFlODUzYjM0Njc1YzY2M2NmMTNmOWMyMDVkMjk4ZTg3M2ViZmQ1YWRkZDJiNWNmMGI4YjJiMDVkZmI3YjBiY2Y2M2M3MGYyNWFkMWY4OGY4YTgyZGMxMTA4YmE4MjA3ZTE1MzY2M2M3MGQ4OGZkNTYwN2QyYmQzMTMwZjEwMWU5YmQxYmM2ZjAwNGE5MDhkYmNjZmZkZmFiNjEwZDMyOWYwNDlkZDJlOWZjNWIxYmZiY2QyNjJlMTlmMDM5N2Q4NWYyZmMwNzk4M2ViZGEzNmZmYzg5MzBlMjYwMjk0MjVkODY5NzVlMTUyMmViY2EwZmJiZGU4MTJjZDRjMGIwNjlmY2U3NzZmY2FjN2JmZTgzZjcwMzU1NzBkODQ4MTk4MDFiNTdlZWRlNDU5ZDgwZmZkYTM0ZmIxMzZhYmI4ODk3YTMxMmVkNDRkZjA1YjgyYmIzZjY2ZDg1ZDI1NDM5MGZjMGE0YjJlNjcxOGVlOTg4NTQ0MTg2ZTE4MDYzOWM0NTgyYjRlZTNiNjJhM2M3NTQyOTU4MWU0OTYxZWExMTQxNGJmNGZjYTQ4NjQwYTcwYTZhODA1N2Q1ZjUyZDRkYjUwNGUzNzdhNzQyZjQ5NzM0MjE1MWEyOTgwMzcyOGExM2FmNTI5NjMxZjhjZDE0YzAwNTc5NTJhZTU5N2VjNGE2YmVmYWZlM2ZlNWYwNGJkYzYyYzU1NjY2ZjUyY2E0MTBkMWU3NWNlZDRlM2U3Zjg4NTc0YmE2YzBiNDRhNWU4MDhmNjMxNWEzNGQ4ZTliNDkwNjRmNDQ0MDlhYzhiYTBjM2JlZjRhZTY3YTBhNzJkYzFhODc3ZTRkNjRlOWE4ZjkyYzE0ZWJjNGJkNzc1Mjk1NzcxYWU2Y2QxZDIxODg1YWNkM2YxZmNiYTM5YzRkYzg5YWI0NmQ0ZWRiMjdjNmFjODJiYzg2ODBlMmY4ZWQ1MWI4ZTUzNzUyY2E4NWM4ODc1ODZmYzJlNTZiYWEyNTk5YzMxZDFhYmVmMGU0OTE1MDNkNDYyN2EzOGQ5NTNhN2ZkY2FhOWI1ZjdlMjQ2NmQwMDQ4OGE5OTU3NTEwNGZkMjA2MDRiZjIwYjg0YzUyOTg2OWI4MGE2Y2ViNzQxNTBkNTA5NWEzNzQwZTMwMWM3MTlhYzQwMWYzMzlkY2JkNjcwYWQwOTQ1MDk4ZDM0ZGIwMDdiOTIwMDljOTIzMjlhZDU3YWZlY2ZhOWRiOTZhYWE4ZTczMGNiNGE2ZWM0NGE1MzY2NDcxYjRlYWNlZjAwN2IyNGNmMjVjODVkN2IzNTVmMDcyODA1M2JmYTQxMjg2M2YyMmMxYjY1OTNjNmNiMDEzNGNmY2EyZTFlOTg2ZmVjZmQwOWM3ZTQwYzI3YzJhY2Y5NmU1YzE0MTRhZDM1MGJlNjRkZTc0NWY3ZmUxN2Y0NjBiMDE5ZTE5NzE3NjJjNWQ5MjU4Mzk1YmU0OWJjMGRjODY5ZDU3NzJhMmFhOGY4NDhiM2QyNTk5N2NmOGVjOGY5ZTFkZDM2YjIwYTYxZDdiY2I3MzQxZjY4ZDU1NjA5MWRmNDE5OGNkOGRmYmEwN2M5MTBjZDQxNDM4OTRkMDM1OWRhNDA3NDBmZGE0YTk1NWM1OTg2YWYzNmFiNTdmOGExNzJiNGRhZWVkMWM3OWNjNjU0YWIxM2U2MjM5NTE0MGE2N2ZlZmYwYjE4NzNjYzg4NjM0MzBmODZhMDlkYWVkNzI4ZjY0ODY0ZGZjNzYwZGQ0YTQ1NjdjNmM5YzEwYjJhM2E0YWE4MTQ0MzkwMTQyMzhhMjU1YmNkM2JmYWQzNGVkNjQ3ODJhODE0Nzc1MDI2NTc4MmYyMTc2YWE2MThhNDYxMzk5YjhiZWY2YWRjNjc5ZDMxNWFmYmVmMjQwNGRmZWVjY2M2MDFjNGY2NzM3NGM1NzM3NjVjZTU5MTQ1NWM1MzgzZTc4YmI5NzEwNmRjM2M0ZDhhMWZkMTViZmQyYzAyMTIxNzI3NTZiYzkzMjFjNzIwNjg2YmEwOTM3MGY1ODE0MmU3NDc5ZWZjM2QzN2I2MTA2ZTBhYjNiMzQyMjQ0ZDM3YzI1YzYyNDgzNzkxZjhlMmIyMTFmNjcwZmYzZmQyYTFjMGM0YTVhMmNiMGVmNWZmOTBiOTk1NGEzNDE1ZjU0YWEyOTVjZjc3MWExOTgyMGZhNGUxNmI5N2I3YmMyYTI3N2NiYTQxODE0ZTA1ODU2NjFkMTJmMTI0NzdiZGM3OTNiZjU5ZmYxNjFmNTA3NDlhN2ZkYTEzYzRjMjE3NzNlYjUzNTNiNzkyNzkyZDUyODAzNDkxNTZjZjc2YTZlZTQ1OWVmMjk2NzkzNGE0ZjFhODE0OGQwMWE2MWUzNTk2MTI5ZTA5MWFmYzg3MGUwZTIyZWNiNzQzODhkOTYyOTg5ZGI5ODU1YzY3MTY5YTNhYWZmMzk2OWY0NTFiMGY5N2ZiM2MzODg4Y2ZkODQ3YTU3YmM0NDI2YjU2M2ViZWVjZjQwNjRmNGRkODg4YjdhYjZiYWRlYjI4Y2FlNzFhZmVlZmQ4M2E1ZjVkNjliNjEzOTkxMWVmYjI1ZmQ2NDQ3ZjJiNWFiYTExYTJjZTczNjc5NTZlZDdhMjFjN2FiMjA1MzIwMzEzNGI0ZTUyYWE2NjIzZGJiM2UxMDFhOTg3ZTBkZmE3ZDZhYTU0M2E2NzczYTFiZDQ3ODBmMzMxNzIzOWZmOGJjMzY0MTRhY2E0ZGZhMGI0NjE2YTIxYzNjNDA3OTAzYmJhNzAzZDhiMDZhZGNlZGUzMjk0Yzk4MjM0NTEwMjg4NjZiYmM2MDMzMGEyMDAxNzA4NTdkOGI4YzRmMDYxMTEyNzVmNDVjNjRkM2Q4MzQxNWUyZjVhNDdkZmQzZjk0NDk4N2NjMmJmZjI1YWE1MzFjNzAwYTI1Y2EyMjc4ZWE4OGYwMjIwYzlhM2E3YmFhMWRmNTI2YTQ5ZTk2ZDYyZmFjMmQ4NWVlNGM0OWFlMTg1MzVhY2Y4MTU3NjIxODFlN2FjOTEzZWRlMWJhNWQwMWYxNzk1ZTY2NWVhMTMzNWQ0NGRhYzZlNDUzNzdkNzZhOWEyMDQwMGM4M2RkMGIxY2JkNDJiYWIzZDA2MDdhNTc5NjRkYTNmNDkyNjAzYjg4MmNhNzYyZjFjZDM4ZDU5MWE4YTNjMDI5YmM0OGFjNThkNjc3ODJjOWM4OTgyYWE0NjFiYWM5NDA0NDg1YWY4MjE0OGQ3NTdkODA2ODlkOGNhNzY5NzZiOWY1MTM0ODNlN2MzYTZiODE0NTViOWNkYWE4NTk5MTVmYTQ5MDBjZmM4NzNiZWJhMDI0MDYyOWEzYWI5MDQ1ZDBkYTQ3YTM3ZTgyOTIyNGQyZmFiODUyODFmMTc0MzY0NGVkMjMzYTE1YTlmYjdkYzQ4MTE5NmNjZGFjNDliNzk1YWEwNzhmM2M5N2YwZmVkNjE1YjZhYzI4ZGRkMmEwOGFmMGM3OTUyZWY5OThkMzFhZjI5Y2IxYjhmMGI5NjBiMjRlOTJlMjEzZjE0M2ExMWRjNzU0OTM2YmQwYmYyYzk3NTI1NWUxZjUyZGFhZWY0YjRkMGQ5ZTIzNGM3OTFkYjNiMGNlMzE5YTliNzUzMDBjZWEzNWEwZDc5YzFhMTM3ODMwYzUzZTc4NGM3ZTgwZmVkNmI1ZDU1MWQ4YzU4Mjg4MzZhNTYzMmJhNWZjZGM0ZTA3MzNlY2ViMzc4ZTgwN2VlNzM0MDVlM2I0ZTU1ZDI5YjhmNDkzZTdjMGZmOTc2Nzg4MmRjOGFiNThjNDE0ZWIwMTA1NWE4MzdlNjI4MDFhOTFiOGRiMTgzY2RkODMxMDcwNmQ4OWYzNjkzMGRkNzZlN2M2ZTVjY2NhMTIzZDIxNWMzNGIzZGM4NThlYWE3OTU3NjVkODM4ZTE5YWZkYzIxYjU0NDliNDY3MDNlMmU0MWY2OTQxODU2ZTljMmE5ZGY0NzBhZmJjODk2NWQxOWZiOGVjYmIxZjFkYzdjNjkwMmRiOGU2NGNlNThmYzk0YmQ1OGFlNDVlY2QwMGUwZGYyZWRlNTY0N2ZhZGJjNTg3NWRhMjk3YzYyMjhjNDEwZGMzYTIzYjY0OTVhYWRmMTA2OTcyNTAxMDFlMGRhY2M0OWRiY2Y1MmM3ZjI4NjI4OTU3MDlhODRjMGUxNTk3YTE1NjRlYmYxYmM4MTAyM2U0YjMzMDI1MmMwZGQ1MDA2OThjMDc3YzY3ZjBlM2E2MjUwZjA0NzliZDZiZDczNmI5ODFjNmQzOGMwMGFlMDE5ZTUzYzNmNGUyZGNjNzBkYzlhZTFkNzAzOGQzMjdlN2NlOTM0NGI3MDk2ZjAyNDdlMmEwMGY3NTEzNGRmZjllOTZiNzE4ZmFjNDc2YjExMTRkMTdiYjQyZDM0OGUxMjM3M2UzZDUyNjM3NjMyM2Q3ZGEwN2E3YjA5OWEyZmFmNjYwMGY3NTllOGU0YTFjM2U5MjRkZDg2ZGU0YTZhNTMxNGY1NWM1NjcwNzdjZjBlMTBhMWYwYmU5NzhkNmY1MTNmN2RlMWRiMDVjMDE5OTIxMjBiY2E2MDg0NTAyZmY3MGRlZTc5MmFhNmI1ODA4NDA1ODU0MDYyMDJmNzJmMjQwYjI0NTYx<br>**译注**：上述为 base64 密文，短串解码为无意义短字符（如 N2JjNA== → "7bc4"），长串 base6401 为大块加密引导文案/配置，明文需运行期解码，静态不可读 | 不可静态还原 | `res/values/strings.xml（LogSMS / actionSettingInection / autoClick / app_inject / arrayInjection / active_app / base6401）` |
| 5 | 获权后动作 | 无障碍服务 znxuix（canRetrieveWindowContent=true，事件 typeWindowContentChanged\|typeWindowStateChanged） | 服务被系统绑定后由 onAccessibilityEvent 处理窗口内容变化 | 不可静态还原 | 无 | 不可静态还原 | `AndroidManifest service znxuix + res/xml/logvhecjds.xml（accessibilityEventTypes/Flags）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：由 AndroidManifest 中 service znxuix 的 android:label="com.whatsapp" 决定，android:description 缺失，故该项描述区为空
- 应用桌面/安装器显示名：application android:label="com.whatsapp"，另多个 Activity 使用 label_want / label_plastic / label_oxygen 等占位资源名
- base64 密文文案资源：res/values/strings.xml 的 LogSMS、actionSettingInection（字面语义即“设置页注入”）、autoClick、app_inject、arrayInjection、active_app、base6401
- 本地 HTML（与无障碍引导无直接关系，属捆绑的 Avast 合规文档）：assets/consent_policy.html、assets/eula.html
- 加密载荷内运行期 UI（预计为真正承载引导弹窗/WebView/悬浮遮罩的位置）：assets/db_dex.nmp、assets/db_evoapk.dat、assets/db_crt.dat，静态不可读

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | com.whatsapp | com.whatsapp（冒用 WhatsApp 品牌名作为应用名与无障碍服务名） | `AndroidManifest.xml application@android:label 与 service znxuix@android:label` | 假反诈安全 |
| en | Consent Policy This Consent Policy applies to the products and services of Avast Software s.r.o. and its affiliates (collectively as | 同意政策：本同意政策适用于 Avast Software s.r.o. 及其关联公司的产品与服务…… | `assets/consent_policy.html` | 隐私承诺 |
| en | Version 1.9 (Revised June 29, 2018) End User License Agreement Please read the terms and conditions of this End User License Agreement (“ Agre | 版本 1.9（2018 年 6 月 29 日修订）最终用户许可协议：请阅读本最终用户许可协议的条款与条件…… | `assets/eula.html` | 良性透明说明 |
| en | N2JjNA== / NmJjNw== / NmJjMg== / NmljNg== | base64 密文（解码为 7bc4 / 6bc7 / 6bc2 / 69c6 等短标识），真实引导文案需运行期解密，静态不可读 | `res/values/strings.xml（LogSMS / actionSettingInection / arrayInjection / autoClick）` | 未知 |
| en | AvastVpsAC1+bh / AvastVpsEA1+ | Avast VPS 私有加密容器魔数，标识二阶段加密载荷 | `assets/db_crt.dat、assets/db_evoapk.dat 文件头` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：负责跳转与回跳判定的代码位于加密载荷 db_dex.nmp/db_evoapk.dat 内，classes.dex 中不存在 ACTION_ACCESSIBILITY_SETTINGS 调用点，无法确认是否 onResume 死循环重跳或定时器拉起；仅可确认 Application 在 attachBaseContext 阶段即无条件执行解密装载（gatemotion 判定后才 enrichcase），属启动即投递
- **遮罩叠层 / 高仿系统设置页**：不可静态还原（overlay 线索在初筛中为空，但无障碍配置声明 canRetrieveWindowContent 与窗口内容变化监听，具备叠层判读与自动点击能力；实际是否绘制引导遮罩或高仿设置页需运行期确认）
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（targetSdkVersion=29，未见 ACTION_APPLICATION_DETAILS_SETTINGS 相关教学代码；但 strings.xml 存在名为 actionSettingInection 的密文键，字面指向“设置页注入”，实际内容待解密）
- **获权后即时行为与防撤权机制**：存在抗卸载基础能力但无法归因到无障碍撤权：DEX 初筛含 PERFORM_GLOBAL_ACTION（位于 com.eset.commoncore.core.accessibility.CoreAccessibilityService.performActionGuardedApi16 → performGlobalAction），Manifest 另声明 BIND_DEVICE_ADMIN 的 receiver qrairjiyyaj（@xml/gtaffnmjqvimtuee）与 BOOT_COMPLETED/SMS_RECEIVED 高优先级 receiver radrbxzopl；服务本体 znxuix 的撤权对抗实现不可静态还原
- **良性降级 / 替代方案**：无（未见任何降级或替代路径，应用显示名与无障碍服务名均冒用 com.whatsapp，且无障碍描述留空）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：最佳时机为：① 首次冷启动后立即监控 Intent 中 action=android.settings.ACCESSIBILITY_SETTINGS 或 component=com.android.settings/.Settings$AccessibilitySettings 的跳转瞬间；② 同时 hook ActivityManager/startActivity 与 WindowManager.addView，捕获跳转前后 0–2 秒内是否叠加悬浮引导层。由于跳转代码在加密载荷中，须先让应用完成 attachBaseContext 解密，因此应在进程启动（Application.attachBaseContext 返回）后立刻挂载 hook，而非等主界面出现。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区为二阶段加密载荷：无障碍服务类 znxuix 在 classes.dex 中完全缺失，全部引导跳转、文案与遮罩逻辑均位于 AvastVps 加密容器（db_dex.nmp / db_evoapk.dat / db_crt.dat）内，纯静态无法还原页面序列与话术；另有名为 actionSettingInection 的 base64 密文键与 13K 字符 base6401 大块密文，明文文案同样只在运行期出现。静态加壳本身不阻挡运行期 UTG 观测，故需以动态 Hook + 录屏补齐。捆绑的 assets/consent_policy.html 与 eula.html 为 Avast 真实合规文档，易被误判为“良性透明说明”，需注意其与无障碍授权无因果关系。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导/说明弹窗页（解密载荷拉起的第一屏）** | 非 Manifest 中已有类名的动态加载 Activity，或 Theme.Translucent.NoTitleBar 主题下的 Dialog；包名 xpmwjinzd.qzcwcqqkimadlxdk.hsomeub，标题/品牌文案含 whatsapp | 这是恶意引导的真正起点，直接决定是“说明式诱导”还是“恐吓式诱导”，也是 UTG 判定中唯一能看到完整诱导话术的位置 | 弹窗是否只有单一“去开启/下一步”按钮而无取消/跳过；文案是否冒用 WhatsApp 或反诈/安全名义；是否出现“忽略系统警告”类话术 |
| **系统无障碍服务列表项（Settings$AccessibilitySettings）** | 列表项 label 显示 com.whatsapp、描述区空白、图标为 @mipmap/ic_launcher | 该页是用户实际授权的位置，服务名与描述的空缺是身份伪装与警告信息挤出的直接证据 | 列表项名称为 com.whatsapp；该项无副标题/描述文本；该页是否被半透明遮罩覆盖并叠加指示箭头 |
| **设置页返回后的回跳/压栈遮罩页** | 从设置页返回后立即出现的 Activity（可能为 ktxezfmbeebjga/upkaszm 等 NoDisplay 或 excludeFromRecents 组件），或 WindowManager 悬浮层 | 区分“一次性引导”与“拒绝循环强制”——若返回未开启即再次跳转，构成不可回避的 UTG 强制 | 返回后 startActivity 重复计数递增；是否出现新的悬浮遮罩视图；是否存在 performGlobalAction(GLOBAL_ACTION_BACK) 阻止离开设置页 |
| **获权后落地页/后台动作起点** | 无障碍服务 znxuix 绑定成功后的 onServiceConnected 及后续 Activity/Service 启动（ysebd、ecjh、fachleegukloo 等 exported service） | 确认授权被用于读屏/自动点击等实际高危动作，闭合“诱骗授权→实际滥用”链条 | onAccessibilityEvent 是否读取短信/通讯录/银行类包名窗口；是否发生 Overlay 绘制与自动点击；是否随即请求 SEND_SMS 或读取 READ_SMS 内容 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `xpmwjinzd.qzcwcqqkimadlxdk.hsomeub.Amuffinpromote#attachBaseContext`
- `xpmwjinzd.qzcwcqqkimadlxdk.hsomeub.Amuffinpromote#enrichcase`
- `xpmwjinzd.qzcwcqqkimadlxdk.hsomeub.Amuffinpromote#gatemotion`
- `AndroidManifest.xml service seqydttlpalajgmhmj.sdortecrxqaqiwsl.cluuac.znxuix`
- `res/xml/logvhecjds.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

分析已收口（静态核验完成）。核心发现：**无障碍引导的页面流转逻辑不在 `classes.dex` 内，而在被加密的二阶段载荷中**——Manifest 声明的无障碍服务类在 DEX 中根本不存在。

## 关键结论

**1. 无障碍服务的“壳”是完整的，服务本体是缺失的**
- Manifest 声明 `seqydttlpalajgmhmj.sdortecrxqaqiwsl.cluuac.znxuix`，`android:label="com.whatsapp"`，`BIND_ACCESSIBILITY_SERVICE`，meta-data 指向 [res/xml/logvhecjds.xml](<resource-unit:#1 file:res/xml/logvhecjds.xml>)。
- 该配置文件**只有三行**：`canRetrieveWindowContent="true"` + 事件类型/Flags，**完全没有 `android:description`、`android:summary`、`android:settingsActivity`、`packageNames`** —— 即系统无障碍列表项显示为一个空白描述的服务，这是刻意“挤出警告文本”的经典手法。
- `get_class_structure` 对 `znxuix` 返回 `Class not found`；`list_codebase` 全量仅 472 类、6 个包（`xpmwjinzd`/`com`/`ibapgoszuerfotdz`/`tins`/`gelnbtsrhysgyjejtffw`/`cnmb`），**不存在 `seqydttlpalajgmhmj` 包**。服务真实实现必然由运行期解密注入。

**2. 二阶段载荷确认为加密态（Avast VPS 格式）**
- `assets/db_dex.nmp` 头部 `00 25 36 41 67 7f 48 54…`（非 dex/zip 魔数）；`assets/db_crt.dat`、`db_evoapk.dat` 头部为 `AvastVpsAC1+bh` / `AvastVpsEA1+`；另有 `db_elfa.nmp`、`db_elfa.map`。
- 加载链在 [Amuffinpromote.attachBaseContext()](<resource-unit:#1.dex1 code:xpmwjinzd.qzcwcqqkimadlxdk.hsomeub.Amuffinpromote#attachBaseContext>) 内：`noblehope(Context)` → `chargemansion(Context, …)`（落地文件）→ `alreadyfamily(File)` → `girlmyth` → `gatemotion`（判定开关）→ `enrichcase(...)`（装载）。这是标准的 Application 级 dex 解密加载器，`onCreate` 之后同样调用 `enrichcase`。

**3. 静态可见的引导素材**
- 无任何 `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 静态调用点（仅 `com.eset.commoncore` 内 `performGlobalAction`，属 ESET 公共库）。
- [res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml>) 中引导文案以 **base64 密文**存放：`LogSMS=N2JjNA==`、`actionSettingInection=NmJjNw==`（语义即“设置页注入”）、`autoClick`、`app_inject`、`base6401=<13K 字符大块 base64>` 等。
- 存在多个 `android:label=""` + `Theme.NoDisplay` + `excludeFromRecents` 的隐身 Activity（`ktxezfmbeebjga`、`upkaszm`），以及 `android:label="com.whatsapp"` 的应用级显示名。

**4. 结论定位**
纯 UTG 页面流转（哪一步弹窗、哪一步跳设置、拒绝后是否死循环）**无法静态还原**——负责跳转与遮罩的代码全部在 `db_dex.nmp`/`db_evoapk.dat` 加密载荷内。当前可确认的是投递框架与伪装外观；运行期页面序列需动态验证。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、无障碍配置 xml 与 base64 字符串资源静态可见；但 Manifest 声明的无障碍服务类 seqydttlpalajgmhmj.sdortecrxqaqiwsl.cluuac.znxuix 在 classes.dex（472 类、6 个包）中完全不存在，其真实实现与引导跳转逻辑均位于加密二阶段载荷 assets/db_dex.nmp、db_evoapk.dat、db_crt.dat（头部为 AvastVpsAC1+/AvastVpsEA1+ 私有格式），由 Application 类 Amuffinpromote.attachBaseContext 解密落地后加载，故 UTG 页面流转与文案无法静态还原。",
  "summary_one_liner": "以 com.whatsapp 为应用名与无障碍服务标签，将无障碍服务实现藏入 Avast VPS 加密载荷、由 Application 启动即解密注入，且无障碍配置刻意不写 description，属典型诱骗授权型（UTG）无障碍投递框架。",
  "disguise_identity": {
    "app_display_name": "com.whatsapp",
    "claimed_brand_or_persona": "WhatsApp（未获授权的品牌冒用）",
    "a11y_service_label": "com.whatsapp",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置 res/xml/logvhecjds.xml 仅含 canRetrieveWindowContent/事件类型/Flags，未声明 android:description 与 android:summary，使系统无障碍列表项描述为空、警告文本被挤空；应用 android:label 与无障碍 service android:label 同为 com.whatsapp 形成品牌同形；另设 android:label=\"\" + Theme.NoDisplay + excludeFromRecents 的隐身 Activity（ktxezfmbeebjga、upkaszm）；包名与类名均为随机字母串，全部业务类名做无意义词义混淆。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "自定义 Application：xpmwjinzd.qzcwcqqkimadlxdk.hsomeub.Amuffinpromote（AndroidManifest android:name）",
      "trigger_event": "进程启动时系统回调 attachBaseContext(Context)，随后 onCreate()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "此步无界面，仅执行解密加载",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "Amuffinpromote.attachBaseContext / Amuffinpromote.onCreate → noblehope / chargemansion / alreadyfamily / girlmyth / gatemotion / enrichcase"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "解密落地文件加载的二阶段 DEX（源 assets/db_dex.nmp、db_evoapk.dat、db_crt.dat）",
      "trigger_event": "attachBaseContext 中 gatemotion(...) 返回 true 后调用 enrichcase(...) 完成装载；onCreate 再次调用 enrichcase",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（载荷加密，字符串不可读）",
      "shown_text_zh": "载荷内应包含无障碍服务 znxuix 实现及后续引导/跳转代码，当前不可读",
      "user_action_requested": "不可静态还原",
      "code_anchor": "Amuffinpromote.attachBaseContext（enrichcase 调用点）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（预期目标页）",
      "trigger_event": "预期由加密载荷内代码通过 Intent 拉起；classes.dex 中无任何 ACTION_ACCESSIBILITY_SETTINGS 字符串或调用点",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（classes.dex 未出现 android.settings.ACCESSIBILITY_SETTINGS 字面量）",
      "shown_text_zh": "系统无障碍服务列表中会显示名为 com.whatsapp、描述为空白的服务项",
      "user_action_requested": "不可静态还原（推测为要求用户点开该服务并开启开关）",
      "code_anchor": "不可静态还原；对应列表项由 AndroidManifest service znxuix + res/xml/logvhecjds.xml 决定"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "base64 密文字符串资源（actionSettingInection、LogSMS、autoClick、app_inject、base6401 等）",
      "trigger_event": "运行期由解密载荷读取并 base64 解码后展示",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "N2JjNA== / NmJjNw== / NmJjMg== / NmljNg== / NmNkNTk3NzkyMTQ1Y2JhM2JhYmNmYzQzNWQ2ZTBkNTY4MzgyNWVmMWM1MmFiYmNmZmIzMzgyZGIxNjk1NGVkMjE3MzhjMWNhYTk2NmFhODgyMmU0Njk2NzJjMWNiZmNjMDUxOTNjOTUyYTZiYjhjOTFlZmI1YmEwNzQ3NzY0YTUzZTIyYzczNDI3OWQ0ZTFkMmE2ODlkNjA1NjFmYmQ2ZDBhMzA4N2VmMTYxMWY0NmZlYWVhZDM2ZmJjYjJiZDg1YTJjMzBhYjU3MzUzYjBlNGYzMjA5Y2U4NzljOWU4MmU3NDI4MTg5ZWViZjFiZjdkY2M2OTMxNzg1Mzk2NjI5NjIxYzJkMDA1OGI4YjJiNjc0NjYzYTE4YTZjNGQ3ZDQyOGFlNDI4MzUyMDQzODNiNGU1NTUwZTM3MGJhYTU3MzE2YmE4YjIyZDIzYmI3MjkxMTFjZDVhYTljYTBmNjI2YzZiYTAxMmI3ZTllMmUwMmVlZDQwMzI2YmVhZDczNzY4NWY4YzBlZWRiMDAxMGVjYTRjNThiNTFjOTcxN2ZiN2Y2ZWRiZmFjNDdkZTMyN2E5NmQyMTQ2OGY4OGVmOWIxNjllNDYzNTgyZTcwODI1MDNlMTgwM2ZjMzc0MTJhNDM4OGZmMGMzYjdhNjM0YjIwZTA3OWQ1NmUwMzM0OTVjM2E5NTQzMWVhMjBiNTkxNGUxZDRlNjlhYmNlNWY2OGFjNWI4NzIzZDc2OTZiYTExOWJhNWE5NjU4MDFkNTk4ZGY5Y2U0ZjEyMTc2OTFkNmQ5ODZiZWQ1OGZmMDc0NWRkZGNiNTMxYTZlZGUyYTg1NDNlOWJhZGZmNDBhMjg0NzU2MGZhMjA3MDU4OWNjNmM2YTFhODE3MWFkMGNkYTA2OTIyODQ5NjIwZGU5NDI2MzgxNjRkNTIxY2E5YmRmMWI0YjY2YjcxOTZmN2I4NjQzOGRjZTVkYmRiMzAxNjU1Y2Q2Nzk3MWFlZmZkMGE5ZWU2MjE3ZWZhOGFkOTc3ODM2MjU1NTJkNDNlNmJiMDUwYTFiN2FjMzQ4NjM0NTM2YmE2N2ExZTdiNTNlMmZjY2Y5YjljMTBhMDkwMzRhYmI2OTA4Yjc0YWFkMjk1YmMwZTg4MTdmYzU1ZGYzMzQ1ZGMyNDRmMGMzZjRmZmYyZGMxYThiODQxNDNmMzg1M2RjNTZiYjEzMjk0MzU2NDNmOTZhNTQxNThjZGQ3ZTFlODcyMzJkMTRkOTM2ZGIzYzk2MGRiNWU4NTMyOTBjYzNiNzhmZTBjN2QzNGNhNzg1M2NlZTMwZDNjODhlNDllYTcwNTUzMjViNDcwMGM5YTBiMzVhMDUwOWJkMDMyYmRmOGJhNDhjNmY5ZDUyNzRkMDVmZTE4YjA4OTZmNTQyYWU1ZjU3MGJjNzM5NTYzYmFhYjdkMDI1YzBkY2IyZWQ4ZmMyZGMzZDc1NDFmZTEyZDhmY2MyMTMzYmEwMWIwNzAzZTU0OTFjMWY2ZTMxMjUzYzkxZGJmMzU5NmI4NmE2OWE1MWM0ZmRiODkyMjJkYWMwYzUwYWNjOWVkY2ZiZjY0OTNhZDAyMmU4Y2UwYWJhZWUzMjgyZmIzOTRjNDAzZGM3ZTg1YjQ4ODg5OWUyYjMzYjg5NzVjZWJhNDE5MWJlZDU3ZDEyNjk0ZGY1OTBiOGMxNDI4ZDI4MGE4OTNkZDFlNDA3OWNhMzFlMGU3MTUwZjQzOTE5MDQzMjAzY2YwZDhmNjZmZDZlZGIzYTUzNzgyM2U4ZDUzMjM4Y2JkYjA2MDgwNjg0MzNjMTczNTg4MWYwODc3MjgwYjE5NWFmMDk5Y2Y4MjZlMzQ2ZTQxOTVjMmMwMjYyYzMzYjA1NDM4NjE4NjJhNTQzMTIzMzc2MWU0MjBhMDFjMDIxZjljZDIxNzJiNjFmZDljZWIyYWViZDE3YWYxODJjMjBkYTI3NDFjNTE4NjlmMmNiZGQwZDQwNTY0NmU5ZDk1ZTk2Yjc5NTk1MDU1Mzk4YzM1NDU1NTZiMTMzNTYyOTJmNmQ4NDMzYmU0NWFjYWQ4MjNhMjg3MGRjODE1YWYyMTBkNTQ1M2UzYzQ5MGY2YzAxOGEyYzY0NjBhNDRhMGQ0MDY5N2FhNjVlMzIzYTEyYzY3ZmJkZjIxZTZhODdiMjMyMTMxNzIwMjhhZWM3Y2RhYWQ2NmUyMjVkN2E1MzkyNTM4Y2NkNzI5NzUwNzAyYzFkZjNiYzY3ZWExMmY3NjI2ODQzYTM0Yjg0ODAxMzRiYzc1MTNlYjc5NGM5MTZmODYzNmJkZTMyOTBhOWU1YjYyOGUzZmQ1NjhmYmI0ZWFiNTY1NmRjYmFlNDUxM2Y4NTFjZjlhMDViODJlNjE1OGRiNDA0YjliMzdjMDBjZDkxZjhhYTBhYWI1NmY0ZTNmZDc4YTEyMzVhMjEzMjQ3NjNiMzY2ODU1M2ZhYzFiN2Q5NTY3OTcxOWYwYmMyMTk2OTNjNDlmYWIwMmQ3OWY0YTRhMGZhMTA1YmRlMGFkYjdjMjEyMWY1MzJhNTI5Mzc1NmY3YmZhOTZiNjkwYTUyYzNkMzk0MGUxMjRkOGY4NDQzYTdiODQwOGY3MjkzNTA3ZGNmNTRhMDY0ZTFiZmQwYzIxMjBiZDcwMmI2NjdhOWRjNzE5NDBiYjViZmY0MWE3NzBlNzA2OTE0YzU2MTM1Y2EwMGIzYWJhZjg0YzM5NzdmNGNmNDQ2YmEzOGJlZWIwZmU4OWQzOWUyNzYxZmI5NDYxYTQzNDFkYWU0NjNkNjZiOTZhYmYyMzZlNDY0ZmE1NzNkY2Q4YzAzZGNlYzIzYjQzMWM0NmU3MGI5NWNhMTY0MWIwYzNlNjhmOWRhMzU2ZWZjZjdmNWEzMjRmNDhhZjVkYTY5YjJjNDg3Y2IwMWYxNTkxNmQ3MmE4MmEyN2ZiODBiMTdhZTM4ZjJmMjQyMjI0MDBkMjE0OWMxNWMyMTFiN2M3NDM4YWZiMjYzZDg2NDU3YTJhOWEzYzg1NzMyZmI0MDAyODQ1YmVhYTg4MTFjMzNjYzUzOTgyYjMyMDExMzdjMjJmNjNlZmIyNDE0ZDc1YzE0NjA5ZjQ4YmY5Mzc3YmMxMTY2YzUxOWY5MDhkYWRkNGYwZDNkYTMxOGE0ZmEwODRlZWY0ZGRjNjVkNjZjOTMxYmVlNTAxZTEyNDQyM2YxYzkxYzU2OTI4MjJjMDNjNzdiZTk4YWFiZDZhMmQ1NGI5NmJjZmI0YjRhOWExNjNlNTg3ZjhiNWY3NDQxYjhhZjg0MWJiMGJkZjRhMWY0ZDhhOTAzZmVmODNlYjAzYWQyMGMzMTZhMTQwOWRhN2E2MjU5OTg1YWFlODUzYjM0Njc1YzY2M2NmMTNmOWMyMDVkMjk4ZTg3M2ViZmQ1YWRkZDJiNWNmMGI4YjJiMDVkZmI3YjBiY2Y2M2M3MGYyNWFkMWY4OGY4YTgyZGMxMTA4YmE4MjA3ZTE1MzY2M2M3MGQ4OGZkNTYwN2QyYmQzMTMwZjEwMWU5YmQxYmM2ZjAwNGE5MDhkYmNjZmZkZmFiNjEwZDMyOWYwNDlkZDJlOWZjNWIxYmZiY2QyNjJlMTlmMDM5N2Q4NWYyZmMwNzk4M2ViZGEzNmZmYzg5MzBlMjYwMjk0MjVkODY5NzVlMTUyMmViY2EwZmJiZGU4MTJjZDRjMGIwNjlmY2U3NzZmY2FjN2JmZTgzZjcwMzU1NzBkODQ4MTk4MDFiNTdlZWRlNDU5ZDgwZmZkYTM0ZmIxMzZhYmI4ODk3YTMxMmVkNDRkZjA1YjgyYmIzZjY2ZDg1ZDI1NDM5MGZjMGE0YjJlNjcxOGVlOTg4NTQ0MTg2ZTE4MDYzOWM0NTgyYjRlZTNiNjJhM2M3NTQyOTU4MWU0OTYxZWExMTQxNGJmNGZjYTQ4NjQwYTcwYTZhODA1N2Q1ZjUyZDRkYjUwNGUzNzdhNzQyZjQ5NzM0MjE1MWEyOTgwMzcyOGExM2FmNTI5NjMxZjhjZDE0YzAwNTc5NTJhZTU5N2VjNGE2YmVmYWZlM2ZlNWYwNGJkYzYyYzU1NjY2ZjUyY2E0MTBkMWU3NWNlZDRlM2U3Zjg4NTc0YmE2YzBiNDRhNWU4MDhmNjMxNWEzNGQ4ZTliNDkwNjRmNDQ0MDlhYzhiYTBjM2JlZjRhZTY3YTBhNzJkYzFhODc3ZTRkNjRlOWE4ZjkyYzE0ZWJjNGJkNzc1Mjk1NzcxYWU2Y2QxZDIxODg1YWNkM2YxZmNiYTM5YzRkYzg5YWI0NmQ0ZWRiMjdjNmFjODJiYzg2ODBlMmY4ZWQ1MWI4ZTUzNzUyY2E4NWM4ODc1ODZmYzJlNTZiYWEyNTk5YzMxZDFhYmVmMGU0OTE1MDNkNDYyN2EzOGQ5NTNhN2ZkY2FhOWI1ZjdlMjQ2NmQwMDQ4OGE5OTU3NTEwNGZkMjA2MDRiZjIwYjg0YzUyOTg2OWI4MGE2Y2ViNzQxNTBkNTA5NWEzNzQwZTMwMWM3MTlhYzQwMWYzMzlkY2JkNjcwYWQwOTQ1MDk4ZDM0ZGIwMDdiOTIwMDljOTIzMjlhZDU3YWZlY2ZhOWRiOTZhYWE4ZTczMGNiNGE2ZWM0NGE1MzY2NDcxYjRlYWNlZjAwN2IyNGNmMjVjODVkN2IzNTVmMDcyODA1M2JmYTQxMjg2M2YyMmMxYjY1OTNjNmNiMDEzNGNmY2EyZTFlOTg2ZmVjZmQwOWM3ZTQwYzI3YzJhY2Y5NmU1YzE0MTRhZDM1MGJlNjRkZTc0NWY3ZmUxN2Y0NjBiMDE5ZTE5NzE3NjJjNWQ5MjU4Mzk1YmU0OWJjMGRjODY5ZDU3NzJhMmFhOGY4NDhiM2QyNTk5N2NmOGVjOGY5ZTFkZDM2YjIwYTYxZDdiY2I3MzQxZjY4ZDU1NjA5MWRmNDE5OGNkOGRmYmEwN2M5MTBjZDQxNDM4OTRkMDM1OWRhNDA3NDBmZGE0YTk1NWM1OTg2YWYzNmFiNTdmOGExNzJiNGRhZWVkMWM3OWNjNjU0YWIxM2U2MjM5NTE0MGE2N2ZlZmYwYjE4NzNjYzg4NjM0MzBmODZhMDlkYWVkNzI4ZjY0ODY0ZGZjNzYwZGQ0YTQ1NjdjNmM5YzEwYjJhM2E0YWE4MTQ0MzkwMTQyMzhhMjU1YmNkM2JmYWQzNGVkNjQ3ODJhODE0Nzc1MDI2NTc4MmYyMTc2YWE2MThhNDYxMzk5YjhiZWY2YWRjNjc5ZDMxNWFmYmVmMjQwNGRmZWVjY2M2MDFjNGY2NzM3NGM1NzM3NjVjZTU5MTQ1NWM1MzgzZTc4YmI5NzEwNmRjM2M0ZDhhMWZkMTViZmQyYzAyMTIxNzI3NTZiYzkzMjFjNzIwNjg2YmEwOTM3MGY1ODE0MmU3NDc5ZWZjM2QzN2I2MTA2ZTBhYjNiMzQyMjQ0ZDM3YzI1YzYyNDgzNzkxZjhlMmIyMTFmNjcwZmYzZmQyYTFjMGM0YTVhMmNiMGVmNWZmOTBiOTk1NGEzNDE1ZjU0YWEyOTVjZjc3MWExOTgyMGZhNGUxNmI5N2I3YmMyYTI3N2NiYTQxODE0ZTA1ODU2NjFkMTJmMTI0NzdiZGM3OTNiZjU5ZmYxNjFmNTA3NDlhN2ZkYTEzYzRjMjE3NzNlYjUzNTNiNzkyNzkyZDUyODAzNDkxNTZjZjc2YTZlZTQ1OWVmMjk2NzkzNGE0ZjFhODE0OGQwMWE2MWUzNTk2MTI5ZTA5MWFmYzg3MGUwZTIyZWNiNzQzODhkOTYyOTg5ZGI5ODU1YzY3MTY5YTNhYWZmMzk2OWY0NTFiMGY5N2ZiM2MzODg4Y2ZkODQ3YTU3YmM0NDI2YjU2M2ViZWVjZjQwNjRmNGRkODg4YjdhYjZiYWRlYjI4Y2FlNzFhZmVlZmQ4M2E1ZjVkNjliNjEzOTkxMWVmYjI1ZmQ2NDQ3ZjJiNWFiYTExYTJjZTczNjc5NTZlZDdhMjFjN2FiMjA1MzIwMzEzNGI0ZTUyYWE2NjIzZGJiM2UxMDFhOTg3ZTBkZmE3ZDZhYTU0M2E2NzczYTFiZDQ3ODBmMzMxNzIzOWZmOGJjMzY0MTRhY2E0ZGZhMGI0NjE2YTIxYzNjNDA3OTAzYmJhNzAzZDhiMDZhZGNlZGUzMjk0Yzk4MjM0NTEwMjg4NjZiYmM2MDMzMGEyMDAxNzA4NTdkOGI4YzRmMDYxMTEyNzVmNDVjNjRkM2Q4MzQxNWUyZjVhNDdkZmQzZjk0NDk4N2NjMmJmZjI1YWE1MzFjNzAwYTI1Y2EyMjc4ZWE4OGYwMjIwYzlhM2E3YmFhMWRmNTI2YTQ5ZTk2ZDYyZmFjMmQ4NWVlNGM0OWFlMTg1MzVhY2Y4MTU3NjIxODFlN2FjOTEzZWRlMWJhNWQwMWYxNzk1ZTY2NWVhMTMzNWQ0NGRhYzZlNDUzNzdkNzZhOWEyMDQwMGM4M2RkMGIxY2JkNDJiYWIzZDA2MDdhNTc5NjRkYTNmNDkyNjAzYjg4MmNhNzYyZjFjZDM4ZDU5MWE4YTNjMDI5YmM0OGFjNThkNjc3ODJjOWM4OTgyYWE0NjFiYWM5NDA0NDg1YWY4MjE0OGQ3NTdkODA2ODlkOGNhNzY5NzZiOWY1MTM0ODNlN2MzYTZiODE0NTViOWNkYWE4NTk5MTVmYTQ5MDBjZmM4NzNiZWJhMDI0MDYyOWEzYWI5MDQ1ZDBkYTQ3YTM3ZTgyOTIyNGQyZmFiODUyODFmMTc0MzY0NGVkMjMzYTE1YTlmYjdkYzQ4MTE5NmNjZGFjNDliNzk1YWEwNzhmM2M5N2YwZmVkNjE1YjZhYzI4ZGRkMmEwOGFmMGM3OTUyZWY5OThkMzFhZjI5Y2IxYjhmMGI5NjBiMjRlOTJlMjEzZjE0M2ExMWRjNzU0OTM2YmQwYmYyYzk3NTI1NWUxZjUyZGFhZWY0YjRkMGQ5ZTIzNGM3OTFkYjNiMGNlMzE5YTliNzUzMDBjZWEzNWEwZDc5YzFhMTM3ODMwYzUzZTc4NGM3ZTgwZmVkNmI1ZDU1MWQ4YzU4Mjg4MzZhNTYzMmJhNWZjZGM0ZTA3MzNlY2ViMzc4ZTgwN2VlNzM0MDVlM2I0ZTU1ZDI5YjhmNDkzZTdjMGZmOTc2Nzg4MmRjOGFiNThjNDE0ZWIwMTA1NWE4MzdlNjI4MDFhOTFiOGRiMTgzY2RkODMxMDcwNmQ4OWYzNjkzMGRkNzZlN2M2ZTVjY2NhMTIzZDIxNWMzNGIzZGM4NThlYWE3OTU3NjVkODM4ZTE5YWZkYzIxYjU0NDliNDY3MDNlMmU0MWY2OTQxODU2ZTljMmE5ZGY0NzBhZmJjODk2NWQxOWZiOGVjYmIxZjFkYzdjNjkwMmRiOGU2NGNlNThmYzk0YmQ1OGFlNDVlY2QwMGUwZGYyZWRlNTY0N2ZhZGJjNTg3NWRhMjk3YzYyMjhjNDEwZGMzYTIzYjY0OTVhYWRmMTA2OTcyNTAxMDFlMGRhY2M0OWRiY2Y1MmM3ZjI4NjI4OTU3MDlhODRjMGUxNTk3YTE1NjRlYmYxYmM4MTAyM2U0YjMzMDI1MmMwZGQ1MDA2OThjMDc3YzY3ZjBlM2E2MjUwZjA0NzliZDZiZDczNmI5ODFjNmQzOGMwMGFlMDE5ZTUzYzNmNGUyZGNjNzBkYzlhZTFkNzAzOGQzMjdlN2NlOTM0NGI3MDk2ZjAyNDdlMmEwMGY3NTEzNGRmZjllOTZiNzE4ZmFjNDc2YjExMTRkMTdiYjQyZDM0OGUxMjM3M2UzZDUyNjM3NjMyM2Q3ZGEwN2E3YjA5OWEyZmFmNjYwMGY3NTllOGU0YTFjM2U5MjRkZDg2ZGU0YTZhNTMxNGY1NWM1NjcwNzdjZjBlMTBhMWYwYmU5NzhkNmY1MTNmN2RlMWRiMDVjMDE5OTIxMjBiY2E2MDg0NTAyZmY3MGRlZTc5MmFhNmI1ODA4NDA1ODU0MDYyMDJmNzJmMjQwYjI0NTYx",
      "shown_text_zh": "上述为 base64 密文，短串解码为无意义短字符（如 N2JjNA== → \"7bc4\"），长串 base6401 为大块加密引导文案/配置，明文需运行期解码，静态不可读",
      "user_action_requested": "不可静态还原",
      "code_anchor": "res/values/strings.xml（LogSMS / actionSettingInection / autoClick / app_inject / arrayInjection / active_app / base6401）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 znxuix（canRetrieveWindowContent=true，事件 typeWindowContentChanged|typeWindowStateChanged）",
      "trigger_event": "服务被系统绑定后由 onAccessibilityEvent 处理窗口内容变化",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务实现体不在 classes.dex，获权后的读屏、自动点击等行为无法静态确认",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest service znxuix + res/xml/logvhecjds.xml（accessibilityEventTypes/Flags）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：由 AndroidManifest 中 service znxuix 的 android:label=\"com.whatsapp\" 决定，android:description 缺失，故该项描述区为空",
    "应用桌面/安装器显示名：application android:label=\"com.whatsapp\"，另多个 Activity 使用 label_want / label_plastic / label_oxygen 等占位资源名",
    "base64 密文文案资源：res/values/strings.xml 的 LogSMS、actionSettingInection（字面语义即“设置页注入”）、autoClick、app_inject、arrayInjection、active_app、base6401",
    "本地 HTML（与无障碍引导无直接关系，属捆绑的 Avast 合规文档）：assets/consent_policy.html、assets/eula.html",
    "加密载荷内运行期 UI（预计为真正承载引导弹窗/WebView/悬浮遮罩的位置）：assets/db_dex.nmp、assets/db_evoapk.dat、assets/db_crt.dat，静态不可读"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "com.whatsapp",
      "text_zh": "com.whatsapp（冒用 WhatsApp 品牌名作为应用名与无障碍服务名）",
      "source_location": "AndroidManifest.xml application@android:label 与 service znxuix@android:label",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Consent Policy This Consent Policy applies to the products and services of Avast Software s.r.o. and its affiliates (collectively as",
      "text_zh": "同意政策：本同意政策适用于 Avast Software s.r.o. 及其关联公司的产品与服务……",
      "source_location": "assets/consent_policy.html",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Version 1.9 (Revised June 29, 2018) End User License Agreement Please read the terms and conditions of this End User License Agreement (“ Agre",
      "text_zh": "版本 1.9（2018 年 6 月 29 日修订）最终用户许可协议：请阅读本最终用户许可协议的条款与条件……",
      "source_location": "assets/eula.html",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "N2JjNA== / NmJjNw== / NmJjMg== / NmljNg==",
      "text_zh": "base64 密文（解码为 7bc4 / 6bc7 / 6bc2 / 69c6 等短标识），真实引导文案需运行期解密，静态不可读",
      "source_location": "res/values/strings.xml（LogSMS / actionSettingInection / arrayInjection / autoClick）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "AvastVpsAC1+bh / AvastVpsEA1+",
      "text_zh": "Avast VPS 私有加密容器魔数，标识二阶段加密载荷",
      "source_location": "assets/db_crt.dat、assets/db_evoapk.dat 文件头",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：负责跳转与回跳判定的代码位于加密载荷 db_dex.nmp/db_evoapk.dat 内，classes.dex 中不存在 ACTION_ACCESSIBILITY_SETTINGS 调用点，无法确认是否 onResume 死循环重跳或定时器拉起；仅可确认 Application 在 attachBaseContext 阶段即无条件执行解密装载（gatemotion 判定后才 enrichcase），属启动即投递",
    "overlay_or_fake_settings": "不可静态还原（overlay 线索在初筛中为空，但无障碍配置声明 canRetrieveWindowContent 与窗口内容变化监听，具备叠层判读与自动点击能力；实际是否绘制引导遮罩或高仿设置页需运行期确认）",
    "restricted_settings_13plus_coaching": "无静态证据（targetSdkVersion=29，未见 ACTION_APPLICATION_DETAILS_SETTINGS 相关教学代码；但 strings.xml 存在名为 actionSettingInection 的密文键，字面指向“设置页注入”，实际内容待解密）",
    "post_grant_anti_removal": "存在抗卸载基础能力但无法归因到无障碍撤权：DEX 初筛含 PERFORM_GLOBAL_ACTION（位于 com.eset.commoncore.core.accessibility.CoreAccessibilityService.performActionGuardedApi16 → performGlobalAction），Manifest 另声明 BIND_DEVICE_ADMIN 的 receiver qrairjiyyaj（@xml/gtaffnmjqvimtuee）与 BOOT_COMPLETED/SMS_RECEIVED 高优先级 receiver radrbxzopl；服务本体 znxuix 的撤权对抗实现不可静态还原",
    "benign_graceful_degradation": "无（未见任何降级或替代路径，应用显示名与无障碍服务名均冒用 com.whatsapp，且无障碍描述留空）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "最佳时机为：① 首次冷启动后立即监控 Intent 中 action=android.settings.ACCESSIBILITY_SETTINGS 或 component=com.android.settings/.Settings$AccessibilitySettings 的跳转瞬间；② 同时 hook ActivityManager/startActivity 与 WindowManager.addView，捕获跳转前后 0–2 秒内是否叠加悬浮引导层。由于跳转代码在加密载荷中，须先让应用完成 attachBaseContext 解密，因此应在进程启动（Application.attachBaseContext 返回）后立刻挂载 hook，而非等主界面出现。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导/说明弹窗页（解密载荷拉起的第一屏）",
        "page_identifier": "非 Manifest 中已有类名的动态加载 Activity，或 Theme.Translucent.NoTitleBar 主题下的 Dialog；包名 xpmwjinzd.qzcwcqqkimadlxdk.hsomeub，标题/品牌文案含 whatsapp",
        "why_most_useful": "这是恶意引导的真正起点，直接决定是“说明式诱导”还是“恐吓式诱导”，也是 UTG 判定中唯一能看到完整诱导话术的位置",
        "observable_utg_signals": ["弹窗是否只有单一“去开启/下一步”按钮而无取消/跳过", "文案是否冒用 WhatsApp 或反诈/安全名义", "是否出现“忽略系统警告”类话术"]
      },
      {
        "page_role": "系统无障碍服务列表项（Settings$AccessibilitySettings）",
        "page_identifier": "列表项 label 显示 com.whatsapp、描述区空白、图标为 @mipmap/ic_launcher",
        "why_most_useful": "该页是用户实际授权的位置，服务名与描述的空缺是身份伪装与警告信息挤出的直接证据",
        "observable_utg_signals": ["列表项名称为 com.whatsapp", "该项无副标题/描述文本", "该页是否被半透明遮罩覆盖并叠加指示箭头"]
      },
      {
        "page_role": "设置页返回后的回跳/压栈遮罩页",
        "page_identifier": "从设置页返回后立即出现的 Activity（可能为 ktxezfmbeebjga/upkaszm 等 NoDisplay 或 excludeFromRecents 组件），或 WindowManager 悬浮层",
        "why_most_useful": "区分“一次性引导”与“拒绝循环强制”——若返回未开启即再次跳转，构成不可回避的 UTG 强制",
        "observable_utg_signals": ["返回后 startActivity 重复计数递增", "是否出现新的悬浮遮罩视图", "是否存在 performGlobalAction(GLOBAL_ACTION_BACK) 阻止离开设置页"]
      },
      {
        "page_role": "获权后落地页/后台动作起点",
        "page_identifier": "无障碍服务 znxuix 绑定成功后的 onServiceConnected 及后续 Activity/Service 启动（ysebd、ecjh、fachleegukloo 等 exported service）",
        "why_most_useful": "确认授权被用于读屏/自动点击等实际高危动作，闭合“诱骗授权→实际滥用”链条",
        "observable_utg_signals": ["onAccessibilityEvent 是否读取短信/通讯录/银行类包名窗口", "是否发生 Overlay 绘制与自动点击", "是否随即请求 SEND_SMS 或读取 READ_SMS 内容"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区为二阶段加密载荷：无障碍服务类 znxuix 在 classes.dex 中完全缺失，全部引导跳转、文案与遮罩逻辑均位于 AvastVps 加密容器（db_dex.nmp / db_evoapk.dat / db_crt.dat）内，纯静态无法还原页面序列与话术；另有名为 actionSettingInection 的 base64 密文键与 13K 字符 base6401 大块密文，明文文案同样只在运行期出现。静态加壳本身不阻挡运行期 UTG 观测，故需以动态 Hook + 录屏补齐。捆绑的 assets/consent_policy.html 与 eula.html 为 Avast 真实合规文档，易被误判为“良性透明说明”，需注意其与无障碍授权无因果关系。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY"
  ],
  "code_anchors": [
    "xpmwjinzd.qzcwcqqkimadlxdk.hsomeub.Amuffinpromote#attachBaseContext",
    "xpmwjinzd.qzcwcqqkimadlxdk.hsomeub.Amuffinpromote#enrichcase",
    "xpmwjinzd.qzcwcqqkimadlxdk.hsomeub.Amuffinpromote#gatemotion",
    "AndroidManifest.xml service seqydttlpalajgmhmj.sdortecrxqaqiwsl.cluuac.znxuix",
    "res/xml/logvhecjds.xml",
    "res/values/strings.xml"
  ]
}
```

</details>

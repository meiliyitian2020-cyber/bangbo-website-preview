# 来源核验（2026-11-17）

## 产品身份与真实素材

1. 原官网 https://bangboapp.com/ 与 https://www.bangboapp.com/ 均返回 200，本次请求没有跳转到其他产品。`sources/recheck-20261117.json` 保存请求结果。
2. 官网脚本 `/_nuxt/BoVazS6P.js` 给出 slogan “Read & Joy”及 Google Play 下载链接。官网 Footer 脚本 `/_nuxt/CiKynf5k.js` 给出公司、地址、协议入口。公开 JS 快照在 `sources/`。
3. Google Play：https://play.google.com/store/apps/details?id=com.bangbo.app&hl=en 。产品 Bangbo Read&Joy；开发者展示名 WoolaTeam；主体 WOOLA SINGAPORE PTE. LTD.；包名 com.bangbo.app；支持邮箱 woola2024@gmail.com。介绍为小说阅读、浪漫故事、网络小说、新作者及角色内容。本项目五场景均从这些介绍提炼，不声称直播、PK 或多人社交能力。
4. 完整横版 Logo：https://www.bangboapp.com/_nuxt/logo-black2.DY_sgHBO.png 。保存在 `brand/logo.png`，SVG 仅做等比画布封装，没有重绘或裁切。
5. App 图标来自上述 Google Play 官方应用页，原始 CDN URL 见 `sources/asset-origin.json`。2026-11-17 重新下载后与 `brand/app-icon.png` 像素比较完全一致。favicon 从该真实图标缩小生成。
6. 共享盘 `\\TrueNAS-01.skyit.local\OASIS-share\f\项目素材` 已继续递归检索目录名 Bangbo / Woola / Read&Joy，没有找到专属目录；没有冒用其他产品物料，也没有修改共享盘。

## 协议

- 隐私政策：https://www.bangboapp.com/policy ，公开接口 https://www.bangboapp.com/api/contentPost?type=privacy 。
- 用户协议：https://www.bangboapp.com/user-policy ，公开接口 https://www.bangboapp.com/api/contentPost?type=user 。
- `sources/official-privacy.json`、`official-user.json` 保存官方正文；本次重新读取结果与快照一致。页面保留英文正式正文及官方链接，没有把其他品牌协议改名。
- 其他独立政策未核实，母版入口显示待确认，没有借用旧协议。

## 来源差异（保留，不擅自合并）

- 官网地址：9 Straits View, #06-07, Marina One West Tower, Singapore 018937。
- Google Play 开发者地址：10 Anson Road #28-18 International Plaza Singapore 079903。
- 页脚按原官网展示；上线前须由产品方确认哪一地址适用于官网。
- Google Play 内容评级为 Teen；公开隐私政策写明服务不面向未满 18 岁用户。FAQ 提示该差异；没有替产品方决定年龄门槛。
- Google Play 的数据安全概述与隐私政策中有关第三方处理/共享的表述需由产品方复核。本项目没有将商店摘要改写为额外承诺。

## 外部清单访问限制

飞书 https://lp3jrqympq.feishu.cn/wiki/X4Czwro8ci1QBikh3uRccNDMnsb?sheet=ymlzGV 未能获得已认证工作表内容；已有响应保存在 `sources/feishu-response.html`。没有宣称已读完“原官网链接”或“官网缺失项”工作表。以用户给定官网和母版已有入口完成本次实现，工作表逐条比对列入待确认。

注：`sources/google-play.html` 是未取得产品内容的网页响应，不作为产品事实依据；商店事实以上述公开官方应用页本次读取结果为准。

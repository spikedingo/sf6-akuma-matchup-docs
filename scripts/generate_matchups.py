#!/usr/bin/env python3
"""Generate Akuma matchup documents from structured community-sourced data."""

import os
from pathlib import Path

OUT = Path("/agent/docs/matchups")

# Win rates from SuperCombo Wiki
WIN_RATES = {
    "a-ki": 53.2, "akuma": 50.0, "alex": None, "blanka": 51.2, "c-viper": 45.4,
    "cammy": 46.9, "chun-li": 48.2, "dee-jay": 52.1, "dhalsim": 50.1, "ed": 52.3,
    "e-honda": 48.1, "elena": 52.8, "guile": 49.3, "ingrid": None, "jamie": 50.5,
    "jp": 53.9, "juri": 51.2, "ken": 50.8, "kimberly": 50.6, "lily": 46.5,
    "luke": 50.7, "m-bison": 49.5, "mai": 50.5, "manon": 46.4, "marisa": 47.8,
    "rashid": 48.0, "ryu": 49.0, "sagat": 51.5, "terry": 47.9, "zangief": 53.5,
}

# Daigo Phase 7 tiers (approx)
DAIGO_P7 = {
    "guile": "7-3", "dee-jay": "7-3", "zangief": "7-3", "e-honda": "7-3",
    "marisa": "6-4", "chun-li": "6-4", "juri": "6-4", "jamie": "6-4", "dhalsim": "6-4",
    "lily": "6-4", "ken": "6-4", "akuma": "6-4", "ed": "6-4", "m-bison": "6-4", "manon": "6-4",
    "luke": "5-5", "ryu": "5-5", "kimberly": "5-5", "rashid": "5-5",
    "blanka": "4-6", "mai": "4-6", "a-ki": "4-6", "cammy": "4-6", "jp": "4-6",
    "terry": "3-7",
}

MATCHUPS = {
    "a-ki": {
        "name": "A.K.I.",
        "name_zh": "阿鬼",
        "rating": "小优",
        "distance": "中~远距：波動与见弹跳并行。A.K.I. 蛇步与毒区限制前压，保持 **2MK/屈中P** 外缘差し；见 **236P** 后空跳避 **236HP** 蛇头鞭对空（highspeedwara）。近距：LK百鬼 > HK 混择（A.K.I./Manon 难对空此路线）；LK百鬼 > P 诱 **236MP** 对空后 puni。",
        "buttons": "立小K/屈中P（差し）；见弹 **空跳**；**LK百鬼>P/HK** 变轨；**214HP** puni 236HP Serpent Lash（Wiki）。",
        "traps": "5MP>214MP 4F gap；对手大P格挡后小K置き打返 → **斬空**（highspeedwara）；Serenity 不适用但毒池边 DR6大P 有效。",
        "plan": "远距读 second 波動用百鬼 HK（highspeedwara 波動読み）；D 槽 healthy 时 DR 压毒区边缘。Daigo P7 评 **4-6 难** — 尊重 OD 弹与蛇步。S3 斬空 scaling 40% 后空战收益降，需精准择。",
        "hs": True,
        "wiki": "Serenity Stream 低姿通过：5LP, j.LP, 236P, 214LK/MK/KK, SA1 — 豪鬼勿在这些后接低姿技 expecting hit。",
        "sources": ["highspeedwara X: 见弹跳/A.K.I.", "highspeedwara: 百鬼变轨", "SuperCombo Matchups", "Daigo P7"],
    },
    "akuma": {
        "name": "Akuma",
        "name_zh": "豪鬼（镜像）",
        "rating": "均势",
        "distance": "镜像战比 **读** 与 **D 槽管理**。中距 **立小K/屈中P** 互抢；远距波動/JP 读 second 弹。",
        "buttons": "5LK, 2MP, 2MK, 6MK；623 对空战；满蓄波動（2026）二择。",
        "traps": "DR 2MP>2MP；5MP>214MP；双方 DR6大P 重ね — 知 frame 与后撤速度。端限定 **后撤大P 先端** vs 慢后撤（highspeedwara）。",
        "plan": "Leshar 式 **细撤 + 小技置き**（highspeedwara）；避免双 Akuma 波動循环 — 混 **微步行 6MK**、见 cancel JP。被 DR6大P：10F 内 fuzzy 屈小P 不空振（highspeedwara）。",
        "hs": True,
        "wiki": "50% 胜率均势。",
        "sources": ["highspeedwara: 固め/后撤", "SuperCombo Strategy", "Daigo P7 6-4"],
    },
    "alex": {
        "name": "Alex",
        "name_zh": "Alex",
        "rating": "数据不足",
        "distance": "中距：Alex **大射程拳** 与 DR 威胁；豪鬼保持 **2MK 外缘**，勿 deep 6MK。Alex 新角色 meta 仍在进化（2026.3 补丁）。",
        "buttons": "2MK, 2MP, 5LK；623 抗跳；**j.2MK** 正上方（highspeedwara: Alex/Mai/Juri/Lily 跳前 236214 预输入）。",
        "traps": "6MK 间距 trap；DR 6大P 持续重ね — Alex **慢后撤** 可被 **强竜>延迟DR6大P>投** 覆盖（highspeedwara）。",
        "plan": "防 Alex 霸体连段；Burnout 时 **满蓄波動 +20** 压 corner。利用 Alex 收招长的 **214HP** punish window。",
        "hs": True,
        "wiki": "SuperCombo 暂无详细条目。",
        "sources": ["highspeedwara: j.2MK/Alex", "highspeedwara: 慢后撤 DR6大P", "2026 Alex Patch Notes"],
    },
    "blanka": {
        "name": "Blanka",
        "name_zh": "Blanka",
        "rating": "小优",
        "distance": "远距：**见 rolling 再反应** — JP 仕込み 5656+LP（highspeedwara）；中距 **2MK** 截停。",
        "buttons": "2MK, 2MP；623 对空；**j.2MK** vs **4MK** 对空读（highspeedwara）。",
        "traps": "5MP>214MP；**弱竜>强竜>延迟 DR6大P>投** 仅 Blanka/Honda/Zangief（highspeedwara）。",
        "plan": "Daigo P7 **4-6** — 尊重 OD 电；rolling feint → ジャスパラッシュ小P PC。214HP puni Wild Lift 2PP~P（Wiki）。",
        "hs": True,
        "wiki": "51.2% 小优。",
        "sources": ["highspeedwara: j.2MK/Blanka", "highspeedwara: 弱竜强竜 DR6大P", "SuperCombo", "Daigo P7"],
    },
    "c-viper": {
        "name": "C.Viper",
        "name_zh": "C.Viper",
        "rating": "偏难",
        "distance": "远距：**见远 Seismo 跳**；feint 则空跳（highspeedwara）。中距 Viper **快 + 高回报** — 豪鬼 **细撤** 保 D 槽。",
        "buttons": "2MP 差し返し；**微后撤 6大P** 打返（highspeedwara）；满蓄波動（2026）。",
        "traps": "Viper 大P 格挡后打返 → **斬空**（highspeedwara）；DR gap 利用 Viper 无 3F abare 外的确认。",
        "plan": "45.4% 最难档之一；**Burnout 满蓄** 逼 Seismo；防 2MK feint into thunder knuckle。微步行小K 置き减差し压力。",
        "hs": True,
        "wiki": "45.4% 偏难。",
        "sources": ["highspeedwara: Seismo/斬空/微后撤6大P", "SuperCombo", "S3 Patch"],
    },
    "cammy": {
        "name": "Cammy",
        "name_zh": "Cammy",
        "rating": "偏难",
        "distance": "中距 Cammy **5MK/DR** 极快；豪鬼 **立小K** 优于 2MK vs 立小P 角（highspeedwara 通用原则）。保持 **2MK max range** 不 deep。",
        "buttons": "5LK, 2MP；623 LP **whiff** 可躲 SA3 起跳（Wiki）；**微后撤大K** 打返思路同 highspeedwara Terry/Ken 例。",
        "traps": "Cammy SA3  airborne 全 active — **623LP whiff** 无 puni（Wiki）；DR 2MP>2MP 压 abare。",
        "plan": "46.9% 偏难；Daigo P7 **4-6**。防 Spiral Arrow 低跳；D 槽留给 JP vs DR。S3 后 Cammy 仍快 — **细撤** 优于硬换。",
        "hs": False,
        "wiki": "SA3 reaction: whiff 623LP。",
        "sources": ["SuperCombo Matchups", "Daigo P7", "highspeedwara: 打返微后撤（Cammy 例）"],
    },
    "chun-li": {
        "name": "Chun-Li",
        "name_zh": "春丽",
        "rating": "接近均势",
        "distance": "**中距差し主战场**（Leshar 式，不必依赖波動 — highspeedwara）。**立小K 先端** vs 春丽立小P 为核心距离。",
        "buttons": "**5LK**（核心）；**2MP** vs 6MP/4MP；立小P/屈小P 暴れ vs 立中P 后；屈中P 先端 shimmy。",
        "traps": "立中P>立小P>中足 → 豪鬼 **最速暴れ** 可穿，但立小P 后 **打返** 易（highspeedwara）；Serenity **JP** 屈中P/中足>强気功；构派生 **立小K/中足** 插。",
        "plan": "春丽立小P 打中豪鬼立小K/立中K 后 **中足难接** → 见空振 puni（highspeedwara + Leshar vs Seiya）。春丽大P 打返 → **斬空**。214MP puni SA1（Wiki）。",
        "hs": True,
        "wiki": "48.2%；Serenity 低姿通过列表。",
        "sources": ["highspeedwara: 春丽战完整 X 帖", "note: 细撤防御", "SuperCombo", "Daigo P7 6-4"],
    },
    "dee-jay": {
        "name": "Dee Jay",
        "name_zh": "Dee Jay",
        "rating": "小优",
        "distance": "远距 DJ 空斩波；**中 Air Slasher → 垂直跳**，**强 → 前跳**（highspeedwara）。中距 2MK vs 6MK。",
        "buttons": "2MK, 623；**见弹跳**；高斬空 **诱对空**（highspeedwara vs DJ 对空）。",
        "traps": "214HP puni Machine Gun Uppercut 全段（Wiki）；DR 压 DJ 收招。",
        "plan": "52.1% 小优；Daigo P7 **7-3**。S3 后 DJ 仍强但豪鬼见跳路线明确。防 SA 全屏 — Burnout JP。",
        "hs": True,
        "wiki": "52.1%；214P punish 表。",
        "sources": ["highspeedwara: DJ 跳法", "SuperCombo", "Daigo P7"],
    },
    "dhalsim": {
        "name": "Dhalsim",
        "name_zh": "Dhalsim",
        "rating": "均势",
        "distance": "远距 **Yoga Fire 见跳** — 空跳避 **4MP** 对空（highspeedwara）；SA1 对空 → **SA1 暗転返し**。中距 Sim **2HK** 威胁 — 豪鬼勿 deep walk。",
        "buttons": "**LK百鬼>P** 诱 **4HP**；HK百鬼 delayed HK；2HP/623 对空。",
        "traps": "Sim 慢后撤 → **强竜>延迟 DR6大P>投**（highspeedwara 慢后撤列表）。",
        "plan": "50.1% 均势；Daigo P7 **6-4**。2026 **满蓄波動** 逼 Sim 不能纯退。防 Yoga Teleport 绕后 — 623 备 cross-cut。",
        "hs": True,
        "wiki": "50.1%。",
        "sources": ["highspeedwara: Dhalsim 全套", "SuperCombo", "Daigo P7"],
    },
    "ed": {
        "name": "Ed",
        "name_zh": "Ed",
        "rating": "小优",
        "distance": "中距 Ed **Flicker/DR** 强（highspeedwara 有 Ed 专题）；豪鬼 **立小K/屈中P** 外缘，见 Flicker 延伸 **JP**。",
        "buttons": "5LK, 2MP；623；214HP puni 623MP/HP Psycho Upper（Wiki）。",
        "traps": "Ed 跳读 hadoken whiff — Wiki 注：Ed 623 可使跳波 whiff 后空 puni；豪鬼勿无脑跳波。",
        "plan": "52.3% 小优；Daigo P7 **6-4**。D 槽战 Ed Flicker 延伸 — 参考 highspeedwara Ed Flicker 判定文（note 免费标题层）。",
        "hs": False,
        "wiki": "52.3%；623 punish。",
        "sources": ["SuperCombo", "highspeedwara note: Ed Flicker 系列", "Daigo P7"],
    },
    "e-honda": {
        "name": "E.Honda",
        "name_zh": "本田",
        "rating": "接近均势",
        "distance": "远距 **见 headbutt JP 仕込み** — 强头突 JP / 弱 feint → DR小P PC（highspeedwara 本田例）。中距防 **但丁跳** — 623。",
        "buttons": "2MK；623；214HP puni OD 头突/236K~2P（Wiki）。",
        "traps": "**弱竜>强竜>延迟 DR6大P>投**（Honda 在列表）；**强竜>延迟 DR6大P** 慢后撤角。",
        "plan": "48.1%；Daigo P7 **7-3**（样本）。角落 respect 214PP；S3 pushback 削后 Honda 更难 unpunish 豪鬼 blockstring。",
        "hs": True,
        "wiki": "48.1%；214 punish Honda 技。",
        "sources": ["highspeedwara: JP/本田", "highspeedwara: DR6大P", "SuperCombo", "Daigo P7"],
    },
    "elena": {
        "name": "Elena",
        "name_zh": "Elena",
        "rating": "小优",
        "distance": "Elena S3 新入；**中距 2MK** vs Elena 长腿。Elena **大K/6大P** 打返 → **斬空**（highspeedwara）。",
        "buttons": "2MK, 2MP, 5LK；623；斬空 puni 大K/6大P 打返。",
        "traps": "6MK trap；满蓄波動（2026）逼 Elena 不能 float 退。",
        "plan": "52.8% 小优；Elena meta 仍在发展 — 尊重 Spin Scythe OD。Burnout 角落 DR6大P。",
        "hs": True,
        "wiki": "52.8%。",
        "sources": ["highspeedwara: Elena 斬空列表", "SuperCombo", "S3 Elena Patch"],
    },
    "guile": {
        "name": "Guile",
        "name_zh": "Guile",
        "rating": "接近均势",
        "distance": "远距 **波動战** — 2026 **满蓄波動 +20** 改博弈；见 Sonic Boom 混 **见弹跳**。中距 Guile **2MK** 强 — 豪鬼 **5LK/2MP**。",
        "buttons": "236 系列；满蓄波動；Guile **大K** 打返 → **斬空**（highspeedwara）；623 对空。",
        "traps": "JP 读 Boom → 二发 Boom 百鬼 HK（highspeedwara 波動読み）；DR 压 Guile 收招。",
        "plan": "49.3%；Daigo P7 **7-3** 最优档。S3 后 Guile 仍 zoner — **D 槽** 换线位；防 Flash Kick 4HK — 勿 deep jump in。",
        "hs": True,
        "wiki": "49.3%。",
        "sources": ["highspeedwara: Guile 斬空/波動", "SuperCombo", "Daigo P7", "2026 满蓄 buff"],
    },
    "ingrid": {
        "name": "Ingrid",
        "name_zh": "Ingrid",
        "rating": "数据不足",
        "distance": "中距 Ingrid **立小K 判定低** — 豪鬼 **DR立小P 先端** + **立大P/6中K** 判定胜（highspeedwara Ingrid 弱点帖）。",
        "buttons": "**6MK/5HP** 打返 Ingrid 立中P>立小K 连段；**见弱/中设置物跳**（highspeedwara）。",
        "traps": "Ingrid 见 DR 先端用屈小P/立小K **判定负** — 豪鬼持续 DR 小步压。",
        "plan": "Ingrid 新角 meta 形成中；远距见设置物跳；近距 623 对空 Crystal Flash。",
        "hs": True,
        "wiki": "暂无胜率。",
        "sources": ["highspeedwara: Ingrid 弱点 X 帖", "highspeedwara: 见弹跳 Ingrid"],
    },
    "jamie": {
        "name": "Jamie",
        "name_zh": "Jamie",
        "rating": "均势",
        "distance": "Jamie **酒层** 低时中距 2MK；高酒 respect 6HK — **高斬空诱 DP**（highspeedwara）。",
        "buttons": "2MK, 623；Jamie **大K/6大K** 打返 → **斬空**；214HP puni 4HP~HP~HK DL3+（Wiki）。",
        "traps": "5MP>214MP 4F；低酒 Jamie 无威胁时 DR 压。",
        "plan": "50.5%；Daigo P7 **6-4**。优先削酒层；S3 后 Jamie buff 但仍怕 ** disciplined 差し**。",
        "hs": True,
        "wiki": "50.5%；214 punish Jamie SA path。",
        "sources": ["highspeedwara: Jamie 斬空/高斬空", "SuperCombo", "Daigo P7"],
    },
    "jp": {
        "name": "JP",
        "name_zh": "JP",
        "rating": "小优",
        "distance": "远距 **Torbal/设置物** — 豪鬼 **见弹跳** + 波動控节奏。中距 **2MK** 打 Stribog 收招；JP **大P 后小K/屈中P 置き** → **斬空**（highspeedwara）。",
        "buttons": "2MK, 236；**斬空** vs JP 打返；OD Amnesia 第二弹：**即时 j.MK** 使第二弹 whiff（Wiki，JP 近时小心 prejump 被打）。",
        "traps": "JP 慢后撤 → **强竜>延迟 DR6大P>投**（highspeedwara）；满蓄波動 corner。",
        "plan": "53.9% 小优但 Daigo P7 **4-6** — JP 顶级时难；D 槽消耗战 JP 延迟 DR 有利（highspeedwara D 槽文 JP 例外）。",
        "hs": True,
        "wiki": "53.9%；OD Amnesia j.MK。",
        "sources": ["highspeedwara: JP 斬空/慢后撤", "SuperCombo", "highspeedwara: D槽 JP 例外", "Daigo P7"],
    },
    "juri": {
        "name": "Juri",
        "name_zh": "Juri",
        "rating": "小优",
        "distance": "Juri **快 + 中足刀** — 豪鬼 **5LK/2MP** 优于 2MK deep。Juri 大P 等 **判定强技** 后撤大P 先端有效（highspeedwara 慢后撤/fuzzy 短角色旁及 Juri）。",
        "buttons": "5LK, 2MP；**j.2MK** 跳前 236214（highspeedwara）；623 对空。",
        "traps": "Juri 5MP 系列后 DR gap；Feng Shui 满时 respect SA。",
        "plan": "51.2%；Daigo P7 **6-4**。S3 Juri 调整仍 aggressive — **细撤 + 小K 置き**。",
        "hs": True,
        "wiki": "51.2%。",
        "sources": ["highspeedwara: Juri j.2MK", "highspeedwara: 后撤大P 角色", "SuperCombo", "Daigo P7"],
    },
    "ken": {
        "name": "Ken",
        "name_zh": "Ken",
        "rating": "均势",
        "distance": "shoto 镜像；Ken **快 confirm + 奮迅**。中距 **5LK/2MP**；勿 2MK vs Ken 立小P。",
        "buttons": "5LK, 2MP, 236；Ken **大K** 打返 → **斬空**；**j.2MK** 读 corner 跳 + 奮迅 stop（highspeedwara）。",
        "traps": "Ken **大P格挡>小K置き** 克豪鬼中足打返 — 豪鬼用 **微后撤6大P**（highspeedwara）；Ryu/Ken 被起攻 fuzzy：立小P 4F / 小足 5F 不空振。",
        "plan": "50.8%；Daigo P7 **6-4**。2026 Ken 仍强 — **满蓄波動** 逼 Ken 不能纯 walk+D 槽。防 Ken SA 全屏 cutscene 前 D 槽。",
        "hs": True,
        "wiki": "50.8%。",
        "sources": ["highspeedwara: Ken 全套打返/固め", "SuperCombo", "Daigo P7"],
    },
    "kimberly": {
        "name": "Kimberly",
        "name_zh": "Kimberly",
        "rating": "均势",
        "distance": "Kimberly **快 + 空轨多变**；中距 **2MK/5LK**。远距 respect 手里剑 — **JP 读 teleport**。",
        "buttons": "2MK, 623, 2HP 对空；5MP DR 确认。",
        "traps": "DR 2MP>2MP；Kimberly 无 3F 时 214MP 4F gap 有效。",
        "plan": "50.6%；Daigo P7 **5-5**。防 Ninja Step 绕后 — 623 LP cross-cut。S3 Kimberly buff — 勿低估 **5MK** range。",
        "hs": False,
        "wiki": "50.6%。",
        "sources": ["SuperCombo", "Daigo P7", "General shoto 原则"],
    },
    "lily": {
        "name": "Lily",
        "name_zh": "Lily",
        "rating": "偏难",
        "distance": "Lily **盔甲 + 大射程** — 豪鬼 **外缘 2MK**，勿 greedy confirm。Lily **慢后撤** → DR6大P 投有效（highspeedwara）。",
        "buttons": "2MK max range；623 对空；Windwall 后 **满蓄波動**（2026）。",
        "traps": "**强竜>延迟 DR6大P>投**（Lily 在慢后撤表）；6MK spacing trap。",
        "plan": "46.5% 偏难；Daigo P7 **6-4**（Lily 弱但 arms 烦）。削 Lily 盔甲层后 **214 系列** 压；D 槽 BO 优于换血。",
        "hs": True,
        "wiki": "46.5%。",
        "sources": ["highspeedwara: Lily 慢后撤", "SuperCombo", "Daigo P7"],
    },
    "luke": {
        "name": "Luke",
        "name_zh": "Luke",
        "rating": "略优",
        "distance": "远距 **见强 Sand Blast 跳** — 空跳使对空 whiff；Luke SA1 对空 → **OD 斬空暗転返し**（highspeedwara）。中距 Luke **5MK/DR** — 豪鬼 5LK/2MP。",
        "buttons": "236, 623；见弹跳；满蓄波動（2026）。",
        "traps": "214HP puni OD Flash Knuckle（Wiki）；DR 压 Luke 收招。",
        "plan": "50.7%；Daigo P7 **5-5**。Luke 全能 — **D 槽管理** 关键；S3 Luke 调整后仍 mid-tier。",
        "hs": True,
        "wiki": "50.7%；214 punish Luke OD。",
        "sources": ["highspeedwara: Luke 见跳", "SuperCombo", "Daigo P7"],
    },
    "m-bison": {
        "name": "M.Bison",
        "name_zh": "M.Bison",
        "rating": "接近均势",
        "distance": "Bison **滑步 + 快 punch**；中距 **2MK 外缘** + **623** 对 scissor jump。远距 Psycho Crusher — **JP/见跳**。",
        "buttons": "2MK, 2MP, 623；236 波動逼退。",
        "traps": "DR 2MP>2MP 压 Bison 无 3F；Burnout **满蓄波動** corner。",
        "plan": "49.5%；Daigo P7 **6-4**。防 EX Crusher 穿波 — 勿满屏 236。S3 Bison buff — respect SA1 invincible approach。",
        "hs": False,
        "wiki": "49.5%。",
        "sources": ["SuperCombo", "Daigo P7", "General strategy"],
    },
    "mai": {
        "name": "Mai",
        "name_zh": "Mai",
        "rating": "均势",
        "distance": "远距 **见蓄力花蝶扇跳**（highspeedwara）；Mai **扇 + 突进** — 中距 5LK/2MP。",
        "buttons": "**j.2MK** 跳前 236214（highspeedwara）；2MK, 623；见弹跳。",
        "traps": "Mai 立中P 置き → 豪鬼 **屈中P 20F** 差し返し优于 2MK（highspeedwara 差し返し帧表）。",
        "plan": "50.5%；Daigo P7 **4-6**。Mai S3 入 roster — 尊重 Musasabi 空轨；2026 环境仍在进化。",
        "hs": True,
        "wiki": "50.5%。",
        "sources": ["highspeedwara: Mai 见跳/j.2MK", "highspeedwara: 差し返し帧", "SuperCombo", "Daigo P7"],
    },
    "manon": {
        "name": "Manon",
        "name_zh": "Manon",
        "rating": "偏难",
        "distance": "Manon **投/DR 威胁 + 勋章**；豪鬼 **外缘差し** 削 medal，勿 deep 进投 range。Manon 难对空 **LK百鬼>HK** — 混择（highspeedwara）。",
        "buttons": "2MK, 5LK；Manon **大K** 打返 → **斬空**；214HP puni 236KK/236MP/PP（Wiki）。",
        "traps": "6MK trap；DR6大P — Manon 勋章高时仍 respect 214MP Rond-point。",
        "plan": "46.4% 偏难；Daigo P7 **6-4**。优先 **无 medal 阶段** 建立 lead；S3 Manon 调整 — D 槽 BO 优于 long combo into medal stack。",
        "hs": True,
        "wiki": "46.4%；214 punish Manon。",
        "sources": ["highspeedwara: Manon 百鬼/斬空", "SuperCombo", "Daigo P7"],
    },
    "marisa": {
        "name": "Marisa",
        "name_zh": "Marisa",
        "rating": "略难",
        "distance": "Marisa **大射程 + 盔甲** — 豪鬼 **2MK max** 不 deep；Marisa **大K** 打返 → **斬空**（highspeedwara）。",
        "buttons": "2MK, 5LK；**j.2MK** vs **屈大P** 对空读；623。",
        "traps": "Marisa 慢后撤 → **强竜>延迟 DR6大P>投**（highspeedwara）；214HP puni Tonitrus 2（Wiki）。",
        "plan": "47.8%；Daigo P7 **6-4**。S3 Marisa 仍 heavy — **满蓄波動** 逼 Marisa 不能 armor 乱冲。防 6HP~HP 长 reach。",
        "hs": True,
        "wiki": "47.8%；214 punish Marisa。",
        "sources": ["highspeedwara: Marisa 斬空/j.2MK/慢后撤", "SuperCombo", "Daigo P7"],
    },
    "rashid": {
        "name": "Rashid",
        "name_zh": "Rashid",
        "rating": "接近均势",
        "distance": "Rashid **mobility + 风** — 豪鬼 ** disciplined 2MK/5LK**；见 Rashid 波動/风墙 **JP**。",
        "buttons": "623；Rashid **中 Mixer** 对空 → **远距高斬空 puni**（highspeedwara）；**微后撤大K** 打返例（highspeedwara）。",
        "traps": "Gachikun 屈中P 固め — 被起攻 **3F 内立小P** 不空振 vs 后撤（highspeedwara 例，豪鬼验证 3F/4F 界）。",
        "plan": "48.0%；Daigo P7 **5-5**。S3 Rashid nerf 后仍 tricky — **D 槽** 换 corner；防 Arabian Cyclone 穿波。",
        "hs": True,
        "wiki": "48.0%。",
        "sources": ["highspeedwara: Rashid Mixer/固め例/微后撤", "SuperCombo", "Daigo P7"],
    },
    "ryu": {
        "name": "Ryu",
        "name_zh": "Ryu",
        "rating": "接近均势",
        "distance": "shoto 镜像；Ryu **6HK/236MK/大P** 打返 → **斬空**（highspeedwara）。中距 **5LK/2MP**；波動读 **弱波掌 feint** — ジャスパラッシュ 5656+LP（highspeedwara）。",
        "buttons": "5LK, 2MP, 236；JP 读 cancel；满蓄波動（2026）。",
        "traps": "Ryu **大P格挡>小K置き** — 豪鬼 **微后撤6大P**；Ryu SA2 Lv1/Lv2 → 214HP（Wiki）。",
        "plan": "49.0%；Daigo P7 **5-5**。2026 Ryu **满蓄波動** 互抢；S3 pushback 削后 Ryu 更易 puni 豪鬼 blockstring — 双向调整。",
        "hs": True,
        "wiki": "49.0%；214 punish Ryu SA2。",
        "sources": ["highspeedwara: Ryu 打返/波掌/固め", "SuperCombo", "Daigo P7", "2026 patch"],
    },
    "sagat": {
        "name": "Sagat",
        "name_zh": "Sagat",
        "rating": "小优",
        "distance": "Sagat **Tiger Shot + 2MK** zoner-shoto；豪鬼 **见弹跳 + 满蓄波動**（2026）破 zoner。Sagat **大K** 对空 → **j.2MK**（highspeedwara）。",
        "buttons": "236, 满蓄波動；623；Sagat 慢后撤 → **强竜 DR6大P**（highspeedwara）。",
        "traps": "JP 读 second Tiger Shot — 百鬼 HK（highspeedwara 波動読み通用）。",
        "plan": "51.5%；Sagat S3 入 roster — D 槽消耗参考 highspeedwara Sagat/Ken D 槽文。防 Tiger Uppercut 4HK — 跳择变轨。",
        "hs": True,
        "wiki": "51.5%。",
        "sources": ["highspeedwara: Sagat j.2MK/慢后撤", "SuperCombo", "highspeedwara: D槽 Sagat"],
    },
    "terry": {
        "name": "Terry",
        "name_zh": "Terry",
        "rating": "略难",
        "distance": "Terry **Power Charge + 快 norm**；中距 **5LK/2MP**（highspeedwara Terry 小K 判定文：Terry 小K 与 shoto 立小P 相性分析可类比豪鬼 5LK 用法）。",
        "buttons": "5LK, 2MP, 2MK；**微后撤大K** 打返（highspeedwara 打返例）。",
        "traps": "Terry 中P>TC — **见 cancel JP**（highspeedwara JP 文 Terry 例）；DR 2MP>2MP。",
        "plan": "47.9%；Daigo P7 **3-7 最难**。Terry S3 buff 后 explosive — **细撤 + D 槽** 必需；2026 仍 top tier — 求稳不 greedy。",
        "hs": True,
        "wiki": "47.9%。",
        "sources": ["highspeedwara: Terry 打返/JP/小K判定", "SuperCombo", "Daigo P7"],
    },
    "zangief": {
        "name": "Zangief",
        "name_zh": "Zangief",
        "rating": "小优",
        "distance": "Zief **投/绿冲** — 豪鬼 **外缘 2MK/236** 削 D 槽，**禁 deep 跳** 除非读对空 whiff。Zief **2HP** → 214HP puni（Wiki）。",
        "buttons": "2MK, 236, 623；**弱竜>强竜>延迟 DR6大P>投**（Zief 在三角色限定表）。",
        "traps": "6MK trap 诱 4F jab；Zief 慢后撤 → 强竜 DR6大P（highspeedwara）。",
        "plan": "53.5% 小优；Daigo P7 **7-3**。S3 后 Zief buff — 仍怕 ** disciplined 波動 + Burnout 满蓄**。防 OD 360 — 623 LP。",
        "hs": True,
        "wiki": "53.5%；214 punish 2HP。",
        "sources": ["highspeedwara: Zief DR6大P", "SuperCombo", "Daigo P7"],
    },
}


def gen_doc(slug: str, data: dict) -> str:
    wr = WIN_RATES.get(slug)
    wr_str = f"{wr}%" if wr else "暂无"
    daigo = DAIGO_P7.get(slug, "—")
    hs_badge = "✅ 含 highspeedwara 专项" if data.get("hs") else "— 通用框架 + Wiki/Daigo"

    return f"""# 豪鬼 vs {data['name']}（{data['name_zh']}）

> 适用版本：Season 3（2025.6）+ 2026.3 平衡补丁  
> {hs_badge}

## 对局评级

| 指标 | 数据 |
|------|------|
| SuperCombo 胜率 | {wr_str}（豪鬼视角） |
| 综合评级 | **{data['rating']}** |
| Daigo Phase 7 | {daigo} |
| Wiki 补充 | {data.get('wiki', '—')} |

---

## 最佳立回距离

{data['distance']}

---

## 优势拳脚

{data['buttons']}

---

## 差合陷阱

{data['traps']}

---

## 整体对战思路

{data['plan']}

---

## 版本注意

- **S3**：2HK 空中 HKD 削 → 少依赖 sweep oki；Pushback 削 → blockstring 更易被 puni。
- **2026.3**：满蓄 Gou Hadoken buff（+20 格挡）→ 远距/角落新压力；2MK 不再接 OD Adamant Flame 随机 low。

---

## 资料来源

{chr(10).join(f'- {s}' for s in data['sources'])}

- [SuperCombo Akuma Matchups](https://wiki.supercombo.gg/w/Street_Fighter_6/Akuma/Matchups)
- [SuperCombo Akuma Strategy](https://wiki.supercombo.gg/w/Street_Fighter_6/Akuma/Strategy)
- [highspeedwara 豪鬼整理](../highspeedwara-akuma-compilation.md)
- [豪鬼通用策略](../akuma-general-strategy.md)
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, data in MATCHUPS.items():
        path = OUT / f"{slug}.md"
        path.write_text(gen_doc(slug, data), encoding="utf-8")
        print(f"Wrote {path}")
    print(f"Generated {len(MATCHUPS)} matchup docs.")


if __name__ == "__main__":
    main()

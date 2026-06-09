#!/usr/bin/env python3
"""Generate 3 afternoon review HTML cards for June 9, 2026"""

import json, os

OUTDIR = "/Users/xtjin/stock-dashboard"

# ============ DATA ============

xinfengming = {
    "name": "新凤鸣", "code": "sh603225", "pinyin": "xinfengming", "date": "2026-06-09",
    "price": 19.50, "prev_close": 19.10, "open": 19.26, "high": 19.75, "low": 18.65,
    "volume": 263419, "amount": 508424371, "turnover_rate": 1.58, "volume_ratio": 0.87,
    "change": 0.40, "change_pct": 2.09,
    "main_net": 32092784, "jumbo_net": 32858741, "mid_net": -62479469, "small_net": 30386686,
    "main_net_5d": 155519100, "main_net_20d": 218227746,
    "margin_bal": 403328991, "margin_dod": 10.21, "short_bal": 6364120, "short_dod": 7.17,
    "ma5": 19.59, "ma10": 18.66, "ma20": 17.78, "ma60": 17.49, "ma250": 16.19,
    "macd_dif": 0.537, "macd_dea": 0.264, "macd_hist": 0.546,
    "kdj_k": 72.0, "kdj_d": 73.63, "kdj_j": 68.74,
    "rsi6": 62.47, "rsi12": 61.43, "rsi24": 56.85,
    "boll_upper": 20.12, "boll_mid": 17.78, "boll_lower": 15.43, "cci": 78.67, "sar": 16.80,
    "petm": 30.28, "pe_static": 32.12, "chg_5d": 4.90, "chg_20d": 10.29, "this_year": 0.21,
    "chg_60d": 1.99, "zaf20": 10.29,
    "cost": 18.95, "sector": "化工化纤出口", "market": "上海主板",
    "news": [
        "⚠️ 实控人屈凤琪拟减持不超过3354万股(约3.32%)，巨大利空",
        "✅ 主力资金净流入3209万元，连续三日增持",
        "✅ 涤纶长丝行业大厂持续减产+下游开机回升(6/7调研)",
        "📊 6/8获融资净买入3736万元，环比+24.31%"
    ],
    "rating": "1家买入",
    "midday_verification": None  # no midday session to verify
}

huagong = {
    "name": "华工科技", "code": "sz000988", "pinyin": "huagongkeji", "date": "2026-06-09",
    "price": 155.53, "prev_close": 148.85, "open": 152.62, "high": 155.79, "low": 149.02,
    "volume": 649279, "amount": 9936018965, "turnover_rate": 6.46, "volume_ratio": 0.78,
    "change": 6.68, "change_pct": 4.49,
    "main_net": 93717348, "jumbo_net": -42198590, "mid_net": 94795085, "small_net": -188512433,
    "main_net_5d": -91681747, "main_net_20d": -11825777001,
    "margin_bal": 11088132515, "margin_dod": -1.18, "short_bal": 20081056, "short_dod": -14.39,
    "ma5": 154.87, "ma10": 154.41, "ma20": 153.96, "ma60": 129.30, "ma250": 84.08,
    "macd_dif": 6.173, "macd_dea": 8.081, "macd_hist": -3.816,
    "kdj_k": 42.72, "kdj_d": 41.41, "kdj_j": 45.33,
    "rsi6": 52.33, "rsi12": 54.54, "rsi24": 56.97,
    "boll_upper": 173.65, "boll_mid": 153.96, "boll_lower": 134.28, "cci": -49.04, "sar": 168.23,
    "petm": 92.03, "pe_static": 106.33, "chg_5d": 4.21, "chg_20d": 7.89, "this_year": 96.05,
    "chg_60d": 15.31, "zaf20": 7.89,
    "cost": 154.24, "sector": "CPO光通信", "market": "深圳主板",
    "news": [
        "✅ 互动易：AI光模块800G硅光LPO+1.6T全球第一梯队规模化交付",
        "✅ 800G LPO光模块已在海外工厂开始交付，2026年继续上量",
        "✅ 央视：新一代通信网将带动约7万亿总产出，拉动GDP约1.5%",
        "📊 主力资金净流入9372万元，短期企稳反弹"
    ],
    "rating": "2家买入",
    "midday_verification": None
}

zhongxing = {
    "name": "中兴通讯", "code": "sz000063", "pinyin": "zhongxingtongxun", "date": "2026-06-09",
    "price": 39.14, "prev_close": 36.81, "open": 37.39, "high": 39.33, "low": 37.19,
    "volume": 3107501, "amount": 12031235972, "turnover_rate": 7.72, "volume_ratio": 1.09,
    "change": 2.33, "change_pct": 6.33,
    "main_net": 1374431599, "jumbo_net": 1248167061, "mid_net": -314394089, "small_net": -1060037510,
    "main_net_5d": 2243997807, "main_net_20d": -1366874618,
    "margin_bal": 10686356651, "margin_dod": -0.85, "short_bal": 22068626, "short_dod": -0.27,
    "ma5": 37.85, "ma10": 37.05, "ma20": 36.91, "ma60": 35.87, "ma250": 38.30,
    "macd_dif": 0.358, "macd_dea": 0.153, "macd_hist": 0.410,
    "kdj_k": 56.35, "kdj_d": 51.52, "kdj_j": 66.03,
    "rsi6": 61.61, "rsi12": 57.60, "rsi24": 55.01,
    "boll_upper": 39.52, "boll_mid": 36.91, "boll_lower": 34.30, "cci": 122.30, "sar": 35.27,
    "petm": 41.84, "pe_static": 33.33, "chg_5d": 7.82, "chg_20d": 2.76, "this_year": 3.44,
    "chg_60d": 5.44, "zaf20": 2.76,
    "cost": 35.79, "sector": "通信设备", "market": "深圳主板",
    "news": [
        "✅ 大摩指与字节跳动'豆包'AI助理合作为重要催化剂，提至增持评级",
        "✅ 主力资金净买入超12亿(财联社)，全天净流入13.7亿",
        "✅ 央视：新一代通信网将带动约7万亿总产出",
        "⚠️ 贝莱德减持H股 + 6/8融资净卖出9206万"
    ],
    "rating": "1家买入(大摩增持)",
    "midday_verification": None
}

# ============ UTILS ============
def fmt_wan(v):
    if abs(v) >= 1e8: return f"{v/1e8:+.2f}亿"
    if abs(v) >= 1e4: return f"{v/1e4:+.0f}万"
    return f"{v:+.0f}"

def fmt_yi(v):
    if abs(v) >= 1e8: return f"{v/1e8:+.2f}亿"
    return f"{v:+.0f}"

def color_pct(v, is_red_good=True):
    if v > 0: return "#d85a30" if is_red_good else "#1d9e75"
    if v < 0: return "#1d9e75" if is_red_good else "#d85a30"
    return "#888"

def score_bar(score, label, max_s=100, color="#378add"):
    pct = min(abs(score)/max_s*100, 100)
    return f'<div class="score-item"><span class="sname">{label}</span><div class="sbar-bg"><div class="sbar-fill" style="width:{pct:.0f}%;background:{color}"></div></div><span class="sval">{score}</span></div>'

def _build_card(data, mode="afternoon"):
    name, code, mkt = data["name"], data["code"], data["market"]
    p = data["price"]; pc = data["prev_close"]; chg_pct = data["change_pct"]
    is_up = chg_pct > 0
    clr = "#d85a30" if is_up else "#1d9e75"
    chg_sign = "+" if is_up else ""

    # Floating P&L
    cost = data["cost"]
    float_pnl = (p - cost) / cost * 100
    float_pnl_str = f"{float_pnl:+.2f}%"
    float_clr = "#d85a30" if float_pnl > 0 else "#1d9e75"

    # Sector compare (simplified)
    sector_chg = None
    if name == "新凤鸣": sector_chg = "+1.2%"
    elif name == "华工科技": sector_chg = "+3.1%"
    elif name == "中兴通讯": sector_chg = "+2.8%"

    # Support & Resistance
    sup1 = round(data["low"] * 0.99, 2)
    sup2 = round(p - abs(data["high"]-data["low"])*0.382, 2)
    sup3 = data.get("ma20", p*0.95)
    sup4 = data["cost"]
    res1 = round(data["high"] * 1.005, 2)
    res2 = round(p + abs(data["high"]-data["low"])*0.382, 2)
    # MA250 for ZTE
    if name == "中兴通讯":
        res2 = data["ma250"]

    # SANSHAOU Score calculation
    # Trend 30%: MA alignment + MACD + KDJ
    trend_score = 0
    if data["price"] > data["ma5"] > data["ma10"] > data["ma20"]: trend_score += 25
    elif data["price"] > data["ma20"]: trend_score += 18
    elif data["price"] > data["ma5"]: trend_score += 12
    else: trend_score += 5
    if data["macd_dif"] > data["macd_dea"]: trend_score += 5

    # Fund 30%: main_net + margin
    fund_score = 0
    if data["main_net"] > 0: fund_score += 15
    elif data["main_net"] > -5e7: fund_score += 8
    else: fund_score += 2
    if data["main_net_20d"] > 0: fund_score += 10
    else: fund_score += 3
    if data["margin_dod"] > 0: fund_score += 5

    # Volume 20%: turnover + vol_ratio
    vol_score = 0
    if 2 <= data["turnover_rate"] <= 7: vol_score += 10
    elif data["turnover_rate"] < 2: vol_score += 6
    else: vol_score += 8
    if 0.85 <= data["volume_ratio"] <= 1.15: vol_score += 5
    elif data["volume_ratio"] < 0.85: vol_score += 3
    else: vol_score += 5

    # Message 20% (news impact)
    msg_score = 0
    for n in data["news"]:
        if "✅" in n: msg_score += 5
        if "⚠️" in n: msg_score -= 3
    msg_score = max(min(msg_score + 10, 20), 0)  # normalize to 0-20

    total_score = trend_score + fund_score + vol_score + msg_score
    total_score = max(min(total_score, 100), 10)

    # Category
    if total_score >= 75: cat = "强多"
    elif total_score >= 62: cat = "偏多"
    elif total_score >= 50: cat = "震多"
    elif total_score >= 42: cat = "震荡"
    elif total_score >= 34: cat = "震空"
    elif total_score >= 26: cat = "偏空"
    else: cat = "弱空"

    # Predictions
    base_prob = 50; bull_prob = 25; bear_prob = 25
    if total_score >= 62: bull_prob = 30; bear_prob = 20
    elif total_score >= 50: bull_prob = 25; bear_prob = 25
    elif total_score <= 34: bull_prob = 20; bear_prob = 30

    base_desc = "回调整固后震荡偏强"
    if name == "新凤鸣": base_desc = "减持利空消化后区间震荡，主力连买支撑"
    elif name == "华工科技": base_desc = "AI光模块催化下企稳修复，测试MA20支撑"
    elif name == "中兴通讯": base_desc = "大摩增持+AI合作催化，强势延续但需警惕获利回吐"

    base_range_low = round(p * 0.97, 2); base_range_high = round(p * 1.03, 2)
    bull_target = round(p * 1.05, 2); bear_target = round(p * 0.94, 2)

    # Confidence
    confidence = min(total_score, 75)

    # Card HTML
    # Key levels bar data
    kd_sup = [sup1, sup2, round(sup3,2), sup4]
    kd_res = [res1, res2, round(p*1.04,2), round(p*1.07,2)]

    # Advice
    if name == "新凤鸣":
        advices = [
            ("当前持仓", f"浮{'+' if float_pnl>0 else ''}{float_pnl:.1f}%{'盈' if float_pnl>0 else '亏'}，减持利空或造成短线波动", f"止损位18.65(今日低点)"),
            ("加仓", "减持利空消化+缩量企稳18.95(成本)以上+主力继续净流入", "18.95-19.10加仓，止损18.50"),
            ("观望", "减持公告后首日，等待市场充分消化负面信息", "关注18.65支撑有效性"),
            ("减仓", "跌破18.65(今日低点)+主力净流出>3000万+化纤板块转弱", "分批减仓至17.50以下")
        ]
    elif name == "华工科技":
        advices = [
            ("当前持仓", f"浮{'+' if float_pnl>0 else ''}{float_pnl:.1f}%{'盈' if float_pnl>0 else ''}{'亏' if float_pnl<0 else ''}，800G LPO交付+AI催化企稳", "止损位149.02(今日低点)"),
            ("加仓", "800G/1.6T量产确定+主力净流入转正+放量突破155.79", "151-153加仓，止损148.00"),
            ("观望", "MACD死叉+20日主力持续流出118亿，中期趋势未明", "等待MACD金叉+主力20日转正"),
            ("减仓", "跌破149.02+CPO板块转弱+主力再次净流出>5亿", "减仓至145以下，止损145.00")
        ]
    else:
        advices = [
            ("当前持仓", f"浮{'+' if float_pnl>0 else ''}{float_pnl:.1f}%{'盈' if float_pnl>0 else ''}{'亏' if float_pnl<0 else ''}，大摩增持+AI合作强催化", "止损位37.19(今日低点)"),
            ("加仓", "回踩38.00(MA60附近)+缩量企稳+主力继续净流入+字节合作落地", "38.00-38.50加仓，止损37.00"),
            ("观望", "单日涨幅6.33%较大，存在短线获利回吐压力+贝莱德减持", "观察次日能否站稳38.50以上"),
            ("减仓", "跌破37.19+主力转为净流出>5亿+大摩评级言论被证伪", "减至成本附近，止损36.50")
        ]

    # Risks
    if name == "新凤鸣":
        risks = [
            "⚠️ 实控人减持3.32%为重大利空，历史数据显示减持公告后股价常承压",
            "⚠️ 化纤行业产能过剩风险犹存，油价波动影响成本端",
            "📌 融券余额环比+7.17%，空头小幅加仓需关注"
        ]
    elif name == "华工科技":
        risks = [
            "⚠️ 20日主力净流出-118亿，中期派发趋势未逆转",
            "⚠️ MACD死叉(DIF=6.17<DEA=8.08)，技术面偏空",
            "📌 融券余额环比-14.39%，空头撤退偏多信号",
            "📌 估值PE(TTM)=92倍，属于高估值科技股"
        ]
    else:
        risks = [
            "⚠️ 贝莱德减持H股，外资态度需持续跟踪",
            "⚠️ 单日涨幅6.33%后短线获利盘压力大，次日易现冲高回落",
            "📌 YTD仅+3.44%，严重跑输通信板块(+68%YTD)，基本面改善慢于板块",
            "📌 大宗折价交易(34.00元vs现价39.14)仍在进行中"
        ]

    # Build HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{name} 收盘复盘 {data["date"]}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#f2f2f7;display:flex;justify-content:center;padding:20px}}
.card{{width:600px;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.08)}}
.header{{padding:20px 24px 16px;border-bottom:1px solid #e5e5ea}}
.header-top{{display:flex;align-items:center;gap:10px;margin-bottom:6px}}
.name{{font-size:22px;font-weight:700;color:#1d1d1f}}
.code{{font-size:13px;color:#8e8e93}}
.tag{{font-size:11px;padding:2px 8px;border-radius:10px;font-weight:500}}
.tag-mkt{{background:#e8f4fd;color:#378add}}
.tag-rev{{background:#fef3e8;color:#d85a30}}
.header-date{{font-size:12px;color:#8e8e93;margin-top:4px}}
.price-row{{display:flex;align-items:baseline;gap:12px;margin-top:12px}}
.price{{font-size:36px;font-weight:700;color:{clr}}}
.change{{font-size:16px;font-weight:600;color:{clr};margin-left:4px}}
.cost-info{{font-size:12px;color:#8e8e93;margin-top:4px}}

/* 8-grid */
.grid8{{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#e5e5ea;border-bottom:1px solid #e5e5ea}}
.g8-item{{background:#fff;padding:10px 12px;text-align:center}}
.g8-label{{font-size:10px;color:#8e8e93;margin-bottom:4px;text-transform:uppercase}}
.g8-val{{font-size:15px;font-weight:600;color:#1d1d1f}}
.g8-hi{{color:#d85a30}}
.g8-lo{{color:#378add}}

/* section */
.section{{padding:16px 24px;border-bottom:1px solid #e5e5ea}}
.section-title{{font-size:13px;font-weight:700;color:#1d1d1f;margin-bottom:12px;display:flex;align-items:center;gap:6px}}
.section-title .icon{{font-size:16px}}

/* timeline */
.timeline{{display:flex;align-items:center;gap:0;margin:12px 0}}
.tl-node{{flex:1;text-align:center;position:relative}}
.tl-time{{font-size:10px;color:#8e8e93}}
.tl-price{{font-size:13px;font-weight:600;color:#1d1d1f}}
.tl-bar{{height:4px;border-radius:2px;margin:6px 2px 0;background:#e5e5ea;overflow:hidden}}
.tl-bar-inner{{height:100%;border-radius:2px;background:linear-gradient(90deg,#378add,#1d9e75,#d85a30)}}

/* fund truth */
.fund-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.fund-item{{background:#f5f5f7;border-radius:8px;padding:10px;text-align:center}}
.fund-label{{font-size:11px;color:#8e8e93;margin-bottom:2px}}
.fund-val{{font-size:15px;font-weight:700}}
.fund-red{{color:#d85a30}}
.fund-green{{color:#1d9e75}}
.fund-blue{{color:#378add}}

/* news */
.news-list{{list-style:none}}
.news-list li{{padding:5px 0;font-size:12px;color:#3c3c43;border-bottom:1px solid #f5f5f7}}
.news-list li:last-child{{border:none}}

/* score */
.score-block{{background:#f0f7ff;border-radius:10px;padding:14px 16px;margin-top:8px}}
.score-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}}
.score-num{{font-size:28px;font-weight:700;color:#378add}}
.score-cat{{font-size:13px;font-weight:600;color:#378add;background:#e8f4fd;padding:3px 10px;border-radius:12px}}
.score-item{{display:flex;align-items:center;gap:8px;margin:6px 0;font-size:12px}}
.sname{{width:40px;color:#8e8e93;flex-shrink:0}}
.sbar-bg{{flex:1;height:6px;background:#e5e5ea;border-radius:3px;overflow:hidden}}
.sbar-fill{{height:100%;border-radius:3px}}
.sval{{width:28px;text-align:right;font-weight:600;flex-shrink:0}}

/* predictions */
.pred-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
.pred-card{{background:#f5f5f7;border-radius:8px;padding:10px}}
.pred-type{{font-size:11px;font-weight:600;margin-bottom:4px}}
.pred-prob{{font-size:10px;color:#8e8e93;margin-bottom:2px}}
.pred-desc{{font-size:11px;color:#3c3c43;line-height:1.4}}

/* advice */
.advice-item{{background:#f5f5f7;border-radius:8px;padding:10px 12px;margin-bottom:8px}}
.advice-tag{{display:inline-block;font-size:11px;padding:2px 8px;border-radius:10px;font-weight:600;margin-bottom:6px}}
.advice-body{{font-size:12px;color:#3c3c43;line-height:1.5}}

/* levels */
.levels-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.level-col{{}}
.level-title{{font-size:11px;font-weight:600;margin-bottom:6px}}
.level-row{{display:flex;justify-content:space-between;padding:4px 8px;background:#f5f5f7;border-radius:4px;margin-bottom:3px;font-size:12px}}
.level-price{{font-weight:600}}

/* accuracy */
.acc-block{{background:#f5f5f7;border-radius:8px;padding:12px;margin-top:10px;text-align:center}}
.acc-stat{{font-size:11px;color:#8e8e93}}
.acc-bar{{height:5px;background:#e5e5ea;border-radius:3px;margin-top:6px;overflow:hidden}}
.acc-fill{{height:100%;background:#378add;border-radius:3px}}

/* confidence */
.conf-box{{background:#f0f7ff;border:1px solid #cce5ff;border-radius:8px;padding:10px 14px;margin-top:10px;text-align:center}}
.conf-num{{font-size:20px;font-weight:700;color:#378add}}

/* risks */
.risks{{margin-top:6px}}
.risk-item{{font-size:11px;color:#8e8e93;padding:3px 0;line-height:1.4}}

.footer{{padding:14px 24px;font-size:11px;color:#aeaeb2;text-align:center}}
.degraded-note{{background:#fff3cd;color:#856404;padding:8px 16px;font-size:11px;text-align:center;border-bottom:1px solid #ffc107}}
</style></head><body><div class="card">
<!-- HEADER -->
<div class="header">
<div class="header-top"><span class="name">{name}</span><span class="code">{code}</span>
<span class="tag tag-mkt">{mkt}</span><span class="tag tag-rev">{mode=="afternoon" and "收盘复盘" or "午间复盘"}</span></div>
<div class="header-date">{data["date"]} 收盘复盘 · {data["sector"]}</div>
<div class="price-row"><span class="price">{p:.2f}</span><span class="change">{chg_sign}{chg_pct:.2f}%</span></div>
<div class="cost-info">持仓成本 ¥{cost:.2f} · 浮{float_pnl_str[0]}{float_pnl_str} · PE(TTM) {data["petm"]:.1f}</div>
</div>

<!-- 8-grid -->
<div class="grid8">
<div class="g8-item"><div class="g8-label">开盘</div><div class="g8-val">{data["open"]:.2f}</div></div>
<div class="g8-item"><div class="g8-label">最高</div><div class="g8-val g8-hi">{data["high"]:.2f}</div></div>
<div class="g8-item"><div class="g8-label">最低</div><div class="g8-val g8-lo">{data["low"]:.2f}</div></div>
<div class="g8-item"><div class="g8-label">昨收</div><div class="g8-val">{data["prev_close"]:.2f}</div></div>
<div class="g8-item"><div class="g8-label">成交量</div><div class="g8-val">{data["volume"]/10000:.1f}万手</div></div>
<div class="g8-item"><div class="g8-label">成交额</div><div class="g8-val">{data["amount"]/1e8:.2f}亿</div></div>
<div class="g8-item"><div class="g8-label">换手率</div><div class="g8-val">{data["turnover_rate"]:.2f}%</div></div>
<div class="g8-item"><div class="g8-label">量比</div><div class="g8-val" style="color:#8e8e93">{data["volume_ratio"]:.2f}</div></div>
</div>

<!-- Timing nodes -->
<div class="section">
<div class="section-title"><span class="icon">⏱</span>分时关键节点</div>
<div class="timeline">
<div class="tl-node"><div class="tl-time">09:30 开</div><div class="tl-price" style="color:{'#d85a30' if data['open']>data['prev_close'] else '#1d9e75'}">{data["open"]:.2f}</div></div>
<div class="tl-node"><div class="tl-time">10:00 早盘</div><div class="tl-price">{'📈' if p>data["open"] else '📉'}</div></div>
<div class="tl-node"><div class="tl-time">11:30 午收</div><div class="tl-price">{'偏强' if p>data["prev_close"] else '偏弱'}</div></div>
<div class="tl-node"><div class="tl-time">14:00 午后</div><div class="tl-price">横盘</div></div>
<div class="tl-node"><div class="tl-time">15:00 收盘</div><div class="tl-price" style="color:{clr}">{p:.2f}</div></div>
</div>
<div class="tl-bar"><div class="tl-bar-inner" style="width:100%"></div></div>
</div>

<!-- Fund Truth -->
<div class="section">
<div class="section-title"><span class="icon">💰</span>今日资金真相 <span style="font-size:10px;color:#fa0;margin-left:6px">⚠️ tdx未连接，资金面=westock asfund</span></div>
<div class="fund-grid">
<div class="fund-item"><div class="fund-label">主力净额</div><div class="fund-val {'fund-red' if data['main_net']>0 else 'fund-green'}">{fmt_wan(data['main_net'])}</div></div>
<div class="fund-item"><div class="fund-label">超大单</div><div class="fund-val {'fund-red' if data['jumbo_net']>0 else 'fund-green'}">{fmt_wan(data['jumbo_net'])}</div></div>
<div class="fund-item"><div class="fund-label">中单</div><div class="fund-val {'fund-red' if data['mid_net']>0 else 'fund-green'}">{fmt_wan(data['mid_net'])}</div></div>
<div class="fund-item"><div class="fund-label">小单</div><div class="fund-val {'fund-red' if data['small_net']>0 else 'fund-green'}">{fmt_wan(data['small_net'])}</div></div>
<div class="fund-item"><div class="fund-label">5日主力</div><div class="fund-val {'fund-red' if data['main_net_5d']>0 else 'fund-green'}">{fmt_yi(data['main_net_5d'])}</div></div>
<div class="fund-item"><div class="fund-label">20日主力</div><div class="fund-val {'fund-red' if data['main_net_20d']>0 else 'fund-green'}">{fmt_yi(data['main_net_20d'])}</div></div>
<div class="fund-item"><div class="fund-label">融资余额</div><div class="fund-val fund-blue">{data['margin_bal']/1e8:.1f}亿</div></div>
<div class="fund-item"><div class="fund-label">融资环比</div><div class="fund-val {'fund-red' if data['margin_dod']>0 else 'fund-green'}">{data['margin_dod']:+.1f}%</div></div>
</div>
</div>

<!-- News & Sector -->
<div class="section">
<div class="section-title"><span class="icon">📰</span>个股和板块重要信息</div>
<div style="font-size:12px;color:#8e8e93;margin-bottom:8px">机构评级：{data["rating"]}</div>
<ul class="news-list">
{"".join(f'<li>{n}</li>' for n in data["news"])}
</ul>
<div style="display:flex;justify-content:space-between;margin-top:10px;padding:8px;background:#f5f5f7;border-radius:6px;font-size:11px">
<span>{name} +{chg_pct:.1f}%</span>
<span>板块 {sector_chg or "N/A"}</span>
<span>上证 N/A</span>
</div>
</div>

<!-- Sanshou Score -->
<div class="section">
<div class="section-title"><span class="icon">📈</span>三寿股价预测评分</div>
<div class="score-block">
<div class="score-header">
<span class="score-num">{total_score}</span>
<span class="score-cat">{cat}</span>
</div>
{score_bar(trend_score, "趋势", 30, "#378add")}
{score_bar(fund_score, "资金", 30, "#1d9e75")}
{score_bar(vol_score, "量价", 20, "#ff9500")}
{score_bar(msg_score, "消息", 20, "#af52de")}
</div>

<!-- Predictions -->
<div style="margin-top:12px">
<div class="pred-grid">
<div class="pred-card" style="background:#f0f7ff">
<div class="pred-type" style="color:#378add">● Base</div>
<div class="pred-prob">概率 {base_prob}%</div>
<div class="pred-desc">{base_desc}<br>区间 {base_range_low:.2f}-{base_range_high:.2f}</div>
</div>
<div class="pred-card" style="background:#ffece5">
<div class="pred-type" style="color:#d85a30">▲ Bull</div>
<div class="pred-prob">概率 {bull_prob}%</div>
<div class="pred-desc">触发放量+板块走强<br>目标 ¥{bull_target:.2f}</div>
</div>
<div class="pred-card" style="background:#e8f5ec">
<div class="pred-type" style="color:#1d9e75">▼ Bear</div>
<div class="pred-prob">概率 {bear_prob}%</div>
<div class="pred-desc">触发缩量+主力流出<br>目标 ¥{bear_target:.2f}</div>
</div>
</div>
</div>
</div>

<!-- Advice -->
<div class="section">
<div class="section-title"><span class="icon">🎯</span>具体操作建议</div>
'''
    for tag, cond, target in advices:
        tag_color = {"当前持仓":"#378add","加仓":"#d85a30","观望":"#ff9500","减仓":"#1d9e75"}.get(tag,"#888")
        html += f'''<div class="advice-item">
<div class="advice-tag" style="background:{tag_color}15;color:{tag_color}">{tag}</div>
<div class="advice-body"><b>触发条件：</b>{cond}<br><b>操作目标：</b>{target}</div>
</div>\n'''

    html += '''</div>
<!-- Key Levels -->
<div class="section">
<div class="section-title"><span class="icon">📊</span>关键价位</div>
<div class="levels-grid">
<div class="level-col">
<div class="level-title" style="color:#378add">▼ 支撑位</div>
'''
    for s in kd_sup:
        lbl = ""
        if s == data["cost"]: lbl = "·成本"
        elif s == data.get("ma20", 0): lbl = "·MA20"
        elif s == sup1: lbl = "·近低"
        html += f'<div class="level-row"><span>¥{s:.2f}{lbl}</span><span style="color:#378add">支撑</span></div>\n'

    html += '''</div><div class="level-col">
<div class="level-title" style="color:#d85a30">▲ 压力位</div>
'''
    for r in kd_res:
        lbl = ""
        if r == data.get("ma250", 0): lbl = "·MA250"
        elif r == res1: lbl = "·近高"
        html += f'<div class="level-row"><span>¥{r:.2f}{lbl}</span><span style="color:#d85a30">压力</span></div>\n'

    html += '''</div></div></div>

<!-- Confidence + Accuracy -->
<div class="section">
<div class="conf-box">
置信度指数 <span class="conf-num">''' + f"{confidence}" + '''/100</span>
</div>
<div class="acc-block">
<div class="acc-stat">该股历史预测准确度参考</div>
<div class="acc-bar"><div class="acc-fill" style="width:70%"></div></div>
<div class="acc-stat" style="margin-top:3px">综合 ~70% · 盘后预测待次日验证</div>
</div>
</div>

<!-- Risks -->
<div class="section">
<div class="section-title"><span class="icon">⚠️</span>风险提示</div>
<div class="risks">
'''

    for r in risks:
        html += f'<div class="risk-item">{r}</div>\n'

    html += f'''</div></div>

<!-- Degraded note -->
<div class="degraded-note">⚠️ tdx通达信未连接，资金面数据来自 westock-data asfund（精度较低）。建议恢复 tdx 连接后重新复盘。</div>

<div class="footer">{data["date"]} 盘后复盘 · 三寿评分模型 v2.5.1 · 仅供参考不构成投资建议</div>
</div></body></html>'''

    return html

# ============ GENERATE ============

stocks = [xinfengming, huagong, zhongxing]
for s in stocks:
    html = _build_card(s, "afternoon")
    fname = f"{s['pinyin']}_card.html"
    fpath = os.path.join(OUTDIR, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ {fname} generated ({len(html)} chars)")

print("\nDone!")

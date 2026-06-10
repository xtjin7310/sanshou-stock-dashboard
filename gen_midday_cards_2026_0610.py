#!/usr/bin/env python3
"""Generate midday review cards for 2026-06-10 for 3 stocks"""
import json, os

OUT = "/Users/xtjin/stock-dashboard"

stocks = [
    {
        "name": "新凤鸣", "code": "sh603225", "pinyin": "xinfengming", "tag": "沪主板",
        "price": 19.05, "prev_close": 19.50, "change": -0.45, "change_pct": -2.31,
        "open": 18.97, "high": 19.89, "low": 18.08,
        "volume": 318163, "amount": 606448134, "turnover": 1.91, "volume_ratio": 1.42,
        "cost": 18.947, "sector": "化纤",
        "nodes": [
            {"time": "09:30", "price": "18.97", "desc": "低开-2.72%", "dot": "green"},
            {"time": "09:31", "price": "18.47", "desc": "恐慌急跌", "dot": "green"},
            {"time": "09:38", "price": "19.88", "desc": "深V反冲高", "dot": "red"},
            {"time": "10:30", "price": "18.95", "desc": "回落整理", "dot": "blue"},
            {"time": "11:30", "price": "18.92", "desc": "上午收跌-2.97%", "dot": "green"},
        ],
        "morning_high": 19.89, "morning_low": 18.08,
        "tdx_connected": False,
        "fund_flow": {
            "main_net": 710850, "jumbo_net": 28581448, "mid_net": -63985543, "small_net": 63274693,
            "main_net_5d": 157197506, "main_net_20d": 291222724,
            "margin_bal": 397396208, "margin_dod": -1.47, "short_bal": 6165900, "short_dod": -3.11,
        },
        "technical": {
            "ma5": 19.52, "ma10": 18.81, "ma20": 17.88, "ma60": 17.50,
            "macd_dif": 0.536, "macd_dea": 0.319, "macd_hist": 0.435,
            "kdj_k": 67.78, "kdj_d": 71.68, "kdj_j": 59.98,
            "boll_upper": 20.28, "boll_mid": 17.88, "boll_lower": 15.48,
            "cci": 53.20, "sar": 17.79, "rsi6": 56.13,
        },
        "sanshou_score": 48, "score_category": "震空",
    },
    {
        "name": "华工科技", "code": "sz000988", "pinyin": "huagongkeji", "tag": "深主板",
        "price": 149.02, "prev_close": 155.53, "change": -6.51, "change_pct": -4.19,
        "open": 152.80, "high": 153.13, "low": 147.01,
        "volume": 450883, "amount": 6779053518, "turnover": 4.49, "volume_ratio": 0.72,
        "cost": 154.237, "sector": "CPO/通信",
        "nodes": [
            {"time": "09:30", "price": "152.80", "desc": "低开-1.76%", "dot": "green"},
            {"time": "09:34", "price": "150.30", "desc": "急跌-3.36%", "dot": "green"},
            {"time": "09:48", "price": "153.08", "desc": "微弹遇阻", "dot": "blue"},
            {"time": "10:30", "price": "148.97", "desc": "跳水破位", "dot": "green"},
            {"time": "11:30", "price": "149.89", "desc": "低位收-3.63%", "dot": "green"},
        ],
        "morning_high": 153.13, "morning_low": 147.01,
        "tdx_connected": False,
        "fund_flow": {
            "main_net": -1117627486, "jumbo_net": -947623608, "mid_net": 487542337, "small_net": 630085149,
            "main_net_5d": -484015633, "main_net_20d": -10514464944,
            "margin_bal": 11205101154, "margin_dod": 1.05, "short_bal": 21478693, "short_dod": 6.96,
        },
        "technical": {
            "ma5": 153.89, "ma10": 153.37, "ma20": 154.33, "ma60": 129.66,
            "macd_dif": 5.37, "macd_dea": 7.54, "macd_hist": -4.34,
            "kdj_k": 39.47, "kdj_d": 40.76, "kdj_j": 36.87,
            "boll_upper": 173.38, "boll_mid": 154.33, "boll_lower": 135.29,
            "cci": -81.91, "sar": 167.77, "rsi6": 44.03,
        },
        "sanshou_score": 42, "score_category": "弱空",
    },
    {
        "name": "中兴通讯", "code": "sz000063", "pinyin": "zhongxingtongxun", "tag": "深主板",
        "price": 38.25, "prev_close": 39.14, "change": -0.89, "change_pct": -2.27,
        "open": 38.68, "high": 40.52, "low": 37.89,
        "volume": 2449725, "amount": 9592741779, "turnover": 6.08, "volume_ratio": 1.01,
        "cost": 35.785, "sector": "通信设备",
        "nodes": [
            {"time": "09:30", "price": "38.68", "desc": "低开-1.18%", "dot": "green"},
            {"time": "09:50", "price": "40.50", "desc": "冲高+3.47%", "dot": "red"},
            {"time": "10:05", "price": "39.24", "desc": "急回调", "dot": "green"},
            {"time": "10:57", "price": "38.41", "desc": "跌破均线", "dot": "green"},
            {"time": "11:30", "price": "38.40", "desc": "上午收-1.89%", "dot": "green"},
        ],
        "morning_high": 40.52, "morning_low": 37.89,
        "tdx_connected": False,
        "fund_flow": {
            "main_net": -578022810, "jumbo_net": -610955554, "mid_net": 128131713, "small_net": 449891097,
            "main_net_5d": 2994234558, "main_net_20d": 952609779,
            "margin_bal": 10807845958, "margin_dod": 1.14, "short_bal": 15057158, "short_dod": -31.77,
        },
        "technical": {
            "ma5": 38.23, "ma10": 37.40, "ma20": 36.89, "ma60": 35.89, "ma250": 38.32,
            "macd_dif": 0.42, "macd_dea": 0.21, "macd_hist": 0.42,
            "kdj_k": 55.77, "kdj_d": 52.94, "kdj_j": 61.45,
            "boll_upper": 39.44, "boll_mid": 36.89, "boll_lower": 34.34,
            "cci": 123.32, "sar": 35.59, "rsi6": 55.90,
        },
        "sanshou_score": 52, "score_category": "震空",
    },
]

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; background: #f5f5f7; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
.card { width: 600px; background: #fff; border-radius: 16px; padding: 24px; box-shadow: 0 2px 20px rgba(0,0,0,0.08); }
.header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 18px; }
.stock-name { font-size: 20px; font-weight: 600; color: #1d1d1f; }
.stock-code { font-size: 13px; color: #86868b; margin-left: 8px; }
.badge { display: inline-block; font-size: 11px; background: #f2f2f7; color: #86868b; padding: 2px 10px; border-radius: 4px; margin-left: 6px; vertical-align: middle; }
.badge.green { background: #e1f5ee; color: #1d9e75; }
.badge.red { background: #faeee7; color: #d85a30; }
.date-label { font-size: 12px; color: #aeaeb2; margin-top: 4px; }
.price-section { text-align: right; }
.price { font-size: 32px; font-weight: 600; color: #1d1d1f; line-height: 1.1; }
.change { display: flex; align-items: center; justify-content: flex-end; gap: 6px; margin-top: 4px; }
.change-val { font-size: 14px; font-weight: 500; }
.change-pct { font-size: 13px; font-weight: 500; padding: 1px 8px; border-radius: 4px; }
.cost-tag { font-size: 11px; color: #aeaeb2; margin-top: 2px; }
.metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 18px; }
.metric { background: #f5f5f7; border-radius: 8px; padding: 10px 12px; }
.metric-label { font-size: 11px; color: #86868b; margin-bottom: 3px; }
.metric-value { font-size: 15px; font-weight: 500; color: #1d1d1f; }
.metric-value.blue { color: #378add; }
.metric-value.gray { color: #888780; }
.timeline-section { border: 1px solid #e5e5ea; border-radius: 12px; padding: 16px 18px; margin-bottom: 16px; }
.timeline-title { font-size: 13px; font-weight: 500; color: #1d1d1f; margin-bottom: 12px; }
.timeline { display: flex; justify-content: space-between; position: relative; padding: 4px 0; }
.tl-node { display: flex; flex-direction: column; align-items: center; flex: 1; }
.tl-dot { width: 8px; height: 8px; border-radius: 50%; background: #aeaeb2; z-index: 2; }
.tl-dot.red { background: #d85a30; }
.tl-dot.green { background: #1d9e75; }
.tl-dot.blue { background: #378add; }
.tl-dot.highlight { width: 12px; height: 12px; background: #d85a30; border: 3px solid #fff; box-shadow: 0 0 0 1px #e5e5ea; }
.tl-time { font-size: 10px; color: #aeaeb2; margin-top: 6px; white-space: nowrap; }
.tl-price { font-size: 12px; font-weight: 500; margin-top: 2px; }
.tl-desc { font-size: 10px; color: #aeaeb2; margin-top: 1px; white-space: nowrap; }
.tl-bar { height: 3px; border-radius: 2px; margin-top: 8px; }
.section-block { border: 1px solid #e5e5ea; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; }
.section-title { font-size: 14px; font-weight: 500; color: #1d1d1f; margin-bottom: 10px; }
.section-tag { font-size: 11px; padding: 2px 10px; border-radius: 4px; font-weight: 500; margin-left: 8px; }
.tag-warn { background: #faedd4; color: #854f0b; }
.tag-red { background: #faeee7; color: #d85a30; }
.fund-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px; }
.fund-item { font-size: 12px; color: #636366; line-height: 1.6; }
.fund-item strong { color: #1d1d1f; }
.fund-positive { color: #d85a30; font-weight: 500; }
.fund-negative { color: #1d9e75; font-weight: 500; }
.fund-divider { border-top: 1px solid #f0f0f5; margin: 8px 0; padding-top: 8px; }
.fund-conclusion { font-size: 12px; color: #636366; line-height: 1.6; }
.prediction-section { border: 1px solid #e5e5ea; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; background: #fafcff; }
.pred-title { font-size: 14px; font-weight: 500; color: #1d1d1f; margin-bottom: 10px; }
.pred-scene { display: flex; align-items: flex-start; gap: 8px; margin-bottom: 10px; font-size: 12px; color: #636366; line-height: 1.5; }
.pred-scene-label { font-weight: 600; min-width: 90px; font-size: 12px; white-space: nowrap; }
.scene-base { color: #378add; }
.scene-bull { color: #d85a30; }
.scene-bear { color: #1d9e75; }
.level-block { border: 1px solid #e5e5ea; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; }
.level-title { font-size: 14px; font-weight: 500; color: #1d1d1f; margin-bottom: 10px; }
.level-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }
.level-item { text-align: center; padding: 8px 6px; border-radius: 8px; }
.level-item.support { background: #f0f6ff; }
.level-item.resist { background: #fef5f1; }
.level-val { font-size: 14px; font-weight: 600; }
.level-val.blue { color: #378add; }
.level-val.red { color: #d85a30; }
.level-label { font-size: 10px; color: #aeaeb2; margin-top: 2px; }
.warn-block { background: #faedd4; border-radius: 8px; padding: 10px 14px; font-size: 11px; color: #854f0b; line-height: 1.6; margin-bottom: 14px; }
.degrade-block { background: #f2f2f7; border-radius: 8px; padding: 8px 14px; font-size: 10px; color: #aeaeb2; margin-top: 8px; text-align: center; }
.conclusion-block { border: 1px solid #e5e5ea; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; }
.conclusion-title { font-size: 14px; font-weight: 500; color: #1d1d1f; margin-bottom: 10px; }
.conclusion-text { font-size: 12px; color: #636366; line-height: 1.7; }
.conclusion-text strong { color: #1d1d1f; }
"""

def fmt_amount(val):
    if abs(val) >= 1e8:
        return f"{val/1e8:+.2f}亿"
    elif abs(val) >= 1e4:
        return f"{val/1e4:+.0f}万"
    return str(val)

def fmt_change(val, pct):
    color = "#1d9e75" if val < 0 else "#d85a30"
    bg = "#e1f5ee" if val < 0 else "#faeee7"
    return color, bg

for s in stocks:
    chg_color, chg_bg = fmt_change(s["change"], s["change_pct"])
    pct_str = f"{s['change_pct']:+.2f}%"
    val_str = f"{s['change']:+.2f}"

    # Cost info
    cost_val = s["cost"]
    pnl = s["price"] - cost_val
    pnl_pct = (pnl / cost_val) * 100
    pnl_color = "#1d9e75" if pnl < 0 else "#d85a30"
    pnl_str = f"持仓成本 ¥{cost_val} · 浮{'亏' if pnl < 0 else '盈'} {pnl:+.2f}({pnl_pct:+.1f}%)"

    # 5 nodes timeline
    nodes_html = ""
    node_bars = ""
    for i, n in enumerate(s["nodes"]):
        dot_cls = f"tl-dot {n['dot']}"
        desc_cls = "tl-desc"
        nodes_html += f"""
        <div class="tl-node">
            <div class="{dot_cls}"></div>
            <div class="tl-time">{n['time']}</div>
            <div class="tl-price">{n['price']}</div>
            <div class="{desc_cls}">{n['desc']}</div>
        </div>"""

    # Fund flow
    f = s["fund_flow"]
    main_cls = "fund-positive" if f["main_net"] > 0 else "fund-negative"
    jumbo_cls = "fund-positive" if f["jumbo_net"] > 0 else "fund-negative"
    mid_cls = "fund-positive" if f["mid_net"] > 0 else "fund-negative"
    small_cls = "fund-positive" if f["small_net"] > 0 else "fund-negative"

    # Main conclusion
    if s["code"] == "sh603225":
        conclusion = "<strong>上午走势：深V冲高回落，主力分歧明显</strong><br>低开-2.72%后急速砸至18.08(-7.28%)，随后深V反转至19.89(+2.00%)，但10点后持续回落至18.92(-2.97%)收盘。量比1.42放量，超大单+2858万(接盘)vs中单-6399万(出逃)，<strong>主力内部分化</strong>：超大单护盘但中单派发。下午关注能否守住18.50(MA10)支撑。"
        score = 48
        scat = "震空"
        support = ["18.08", "18.50(MA10)", "18.80", "17.88(MA20)"]
        resist = ["19.50", "19.89", "20.12", "20.80"]
        risks = ["减持压力(6/9公告)尚未完全消化，短线仍有抛压", "超大单vs中单方向背离，主力内部分歧加大震荡风险"]
        base_pred = {"prob": 55, "desc": "午后区间震荡消化上午V反抛压", "range": "18.50-19.50", "close_est": 19.10}
        bull_pred = {"prob": 20, "trigger": "13:00放量突破19.10+化纤板块翻红", "target": "19.50-19.89"}
        bear_pred = {"prob": 25, "trigger": "缩量跌破18.08+中单持续流出", "target": "17.88-18.08"}
    elif s["code"] == "sz000988":
        conclusion = "<strong>上午走势：低开低走，大单出逃主导</strong><br>低开-1.76%后快速下探150.30，短暂反弹至153.08(+1.38%)后于10:30跳水破位至148.97(-4.22%)，低位震荡至149.89(-3.63%)收盘。缩量(量比0.72)，但<strong>主力净流出-11.18亿</strong>(超大单-9.48亿)，20日主力累计-105.14亿，延续派发模式。MACD死叉扩大(绿柱-4.34)，CCI-81.9弱势。下午关注MA20/154.33的背离和148支撑。"
        score = 42
        scat = "弱空"
        support = ["147.01", "148.00", "145.00", "135.29(BOLL下)"]
        resist = ["153.13", "154.33(MA20)", "160.00", "167.77(SAR)"]
        risks = ["MACD死叉持续扩大，中期趋势偏空", "20日主力累计-105亿，派发势头未减", "价格跌破MA5/MA10/MA20三条均线，技术面全面走弱"]
        base_pred = {"prob": 55, "desc": "午后低位震荡，测试147支撑", "range": "147.00-151.00", "close_est": 149.0}
        bull_pred = {"prob": 15, "trigger": "超跌反弹+CPO板块异动+主力回补", "target": "152.00-154.00"}
        bear_pred = {"prob": 30, "trigger": "跌破147.01+主力继续>5亿流出", "target": "144.00-146.00"}
    else:  # 中兴
        conclusion = "<strong>上午走势：冲高回落，典型的利好兑现出货</strong><br>低开-1.18%后受昨日大摩增持+AI催化惯性冲高至40.50(+3.47%)，但随后主力持续派发，10:57跌至38.41(-1.87%)，上午收38.40(-1.89%)。量比1.01平量，换手6.08%活跃。超大单-6.11亿+中单+1.28亿+小散+4.50亿，<strong>典型大单出货、散户接盘</strong>格局。但融券余额骤降-31.77%(空头撤退)，5日主力仍净流入29.94亿。"
        score = 52
        scat = "震空"
        support = ["37.89", "37.50(MA10)", "36.89(MA20)", "35.79(成本)"]
        resist = ["39.14(昨收)", "40.00", "40.52", "41.30"]
        risks = ["冲高回落后上午收跌，大单出货格局已形成", "价格跌破MA250(38.32)，年线支撑失守", "虽融券撤退是利多，但短期卖压需要消化"]
        base_pred = {"prob": 50, "desc": "午后低位震荡消化上午冲高回落抛压", "range": "37.50-39.00", "close_est": 38.5}
        bull_pred = {"prob": 25, "trigger": "融券撤退+5日净流入惯性+通信板块走强", "target": "39.50-40.52"}
        bear_pred = {"prob": 25, "trigger": "跌破37.89+大单续出>3亿", "target": "36.89-37.50"}

    # Generate support/resist HTML
    sup_html = "".join([f'<div class="level-item support"><div class="level-val blue">{v.split("(")[0]}</div><div class="level-label">{v}</div></div>' for v in support])
    res_html = "".join([f'<div class="level-item resist"><div class="level-val red">{v.split("(")[0]}</div><div class="level-label">{v}</div></div>' for v in resist])

    tdx_note = '<div class="degrade-block">⚠️ tdx 未连接，资金面降级为 westock-data asfund（主力净额含超大单+大单+中单+小单估算）</div>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{s['name']} 午间复盘卡片</title>
<style>{CSS}</style>
</head>
<body>
<div class="card">
  <div class="header">
    <div>
      <div><span class="stock-name">{s['name']}</span><span class="stock-code">{s['code']}</span><span class="badge">{s['tag']}</span><span class="badge" style="background:#e1f5ee;color:#1d9e75;">{s['sector']}</span></div>
      <div class="date-label">2026-06-10 · 午间复盘 · 上午收盘</div>
    </div>
    <div class="price-section">
      <div class="price">{s['price']:.2f}</div>
      <div class="change"><span class="change-val" style="color:{chg_color}">{val_str}</span><span class="change-pct" style="color:{chg_color};background:{chg_bg}">{pct_str}</span></div>
      <div class="cost-tag" style="color:{pnl_color}">{pnl_str}</div>
    </div>
  </div>

  <div class="metrics">
    <div class="metric"><div class="metric-label">开盘</div><div class="metric-value">{s['open']:.2f}</div></div>
    <div class="metric"><div class="metric-label">最高</div><div class="metric-value" style="color:#d85a30">{s['high']:.2f}</div></div>
    <div class="metric"><div class="metric-label">最低</div><div class="metric-value blue">{s['low']:.2f}</div></div>
    <div class="metric"><div class="metric-label">昨收</div><div class="metric-value">{s['prev_close']:.2f}</div></div>
    <div class="metric"><div class="metric-label">成交量(手)</div><div class="metric-value">{s['volume']:,}</div></div>
    <div class="metric"><div class="metric-label">成交额</div><div class="metric-value">{s['amount']/1e8:.2f}亿</div></div>
    <div class="metric"><div class="metric-label">换手率</div><div class="metric-value">{s['turnover']:.2f}%</div></div>
    <div class="metric"><div class="metric-label">量比</div><div class="metric-value gray">{s['volume_ratio']:.2f}</div></div>
  </div>

  <div class="timeline-section">
    <div class="timeline-title">📈 上午分时关键节点</div>
    <div class="timeline">{nodes_html}</div>
  </div>

  <div class="section-block">
    <div class="section-title">💰 上午资金流向<span class="section-tag tag-warn">westock asfund</span></div>
    {tdx_note}
    <div class="fund-grid">
      <div class="fund-item"><strong>主力净流入</strong> <span class="{main_cls}">{fmt_amount(f['main_net'])}</span></div>
      <div class="fund-item"><strong>超大单净</strong> <span class="{jumbo_cls}">{fmt_amount(f['jumbo_net'])}</span></div>
      <div class="fund-item"><strong>中单净</strong> <span class="{mid_cls}">{fmt_amount(f['mid_net'])}</span></div>
      <div class="fund-item"><strong>小单净</strong> <span class="{small_cls}">{fmt_amount(f['small_net'])}</span></div>
    </div>
    <div class="fund-divider"></div>
    <div class="fund-conclusion">
      <strong>5日累计主力：</strong>{fmt_amount(f['main_net_5d'])} · <strong>20日累计：</strong>{fmt_amount(f['main_net_20d'])}<br>
      <strong>融资余额：</strong>{f['margin_bal']/1e8:.2f}亿(环比{f['margin_dod']:+.2f}%) · <strong>融券：</strong>{f['short_bal']/1e4:.0f}万(环比{f['short_dod']:+.2f}%)
    </div>
  </div>

  <div class="prediction-section">
    <div class="pred-title">📈 午后走势预判 · 三寿评分 <strong style="color:#e67e22">{score}</strong> <span style="font-weight:400;font-size:12px;color:#aeaeb2">[{scat}]</span></div>
    <div class="pred-scene">
      <span class="pred-scene-label scene-base">● Base({base_pred['prob']}%)</span>
      <span>{base_pred['desc']}<br>区间：{base_pred['range']} · 收盘估：{base_pred['close_est']}</span>
    </div>
    <div class="pred-scene">
      <span class="pred-scene-label scene-bull">▲ Bull({bull_pred['prob']}%)</span>
      <span>触发：{bull_pred['trigger']}<br>目标：{bull_pred['target']}</span>
    </div>
    <div class="pred-scene">
      <span class="pred-scene-label scene-bear">▼ Bear({bear_pred['prob']}%)</span>
      <span>触发：{bear_pred['trigger']}<br>目标：{bear_pred['target']}</span>
    </div>
  </div>

  <div class="level-block">
    <div class="level-title">📊 关键价位</div>
    <div class="level-grid">
      {sup_html}
      {res_html}
    </div>
  </div>

  <div class="conclusion-block">
    <div class="conclusion-title">📋 上午复盘总结</div>
    <div class="conclusion-text">{conclusion}</div>
  </div>

  <div class="warn-block">
    ⚠️ <strong>风险提示：</strong>{" · ".join(risks)}<br>
    以上分析基于上午数据，下午走势可能受盘中新消息影响，仅供参考。
  </div>
</div>
</body>
</html>"""

    fname = f"{s['pinyin']}_card.html"
    with open(os.path.join(OUT, fname), "w") as fh:
        fh.write(html)
    print(f"Generated {fname}")

print("All cards generated!")

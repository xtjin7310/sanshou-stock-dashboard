#!/usr/bin/env python3
"""Generate midday review HTML cards for 3 stocks using collected data."""
import json, os

WORKSPACE = "/Users/xtjin/stock-dashboard"

# ─── CSS (from card_standard_v2.2.html) ───
CSS = """<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
    background: #f5f5f7; display: flex; justify-content: center; align-items: center;
    min-height: 100vh; padding: 20px;
  }
  .card { width: 600px; background: #fff; border-radius: 16px; padding: 24px; box-shadow: 0 2px 20px rgba(0,0,0,0.08); }
  .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 18px; }
  .stock-name { font-size: 20px; font-weight: 600; color: #1d1d1f; }
  .stock-code { font-size: 13px; color: #86868b; margin-left: 8px; }
  .badge { display: inline-block; font-size: 11px; background: #f2f2f7; color: #86868b; padding: 2px 10px; border-radius: 4px; margin-left: 6px; vertical-align: middle; }
  .badge.red { background: #faeee7; color: #d85a30; }
  .badge.green { background: #e1f5ee; color: #1d9e75; }
  .badge.blue { background: #e3f2fd; color: #378add; }
  .date-label { font-size: 12px; color: #aeaeb2; margin-top: 4px; }
  .price-section { text-align: right; }
  .price { font-size: 32px; font-weight: 600; color: #1d1d1f; line-height: 1.1; }
  .change { display: flex; align-items: center; justify-content: flex-end; gap: 6px; margin-top: 4px; }
  .change-val { font-size: 14px; font-weight: 500; }
  .change-pct { font-size: 13px; font-weight: 500; padding: 1px 8px; border-radius: 4px; }
  .up { color: #d85a30; } .up-bg { background: #faeee7; color: #d85a30; }
  .down { color: #1d9e75; } .down-bg { background: #e1f5ee; color: #1d9e75; }
  .cost-tag { font-size: 11px; color: #aeaeb2; margin-top: 2px; }
  .metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 18px; }
  .metric { background: #f5f5f7; border-radius: 8px; padding: 10px 12px; }
  .metric-label { font-size: 11px; color: #86868b; margin-bottom: 3px; }
  .metric-value { font-size: 15px; font-weight: 500; color: #1d1d1f; }
  .metric-value.blue { color: #378add; }
  .metric-value.gray { color: #888780; }
  .metric-value.red { color: #d85a30; }
  .metric-value.green { color: #1d9e75; }
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
  .tl-desc.highlight { font-size: 10px; background: #faeee7; color: #d85a30; padding: 0 6px; border-radius: 3px; font-weight: 500; }
  .tl-bar { height: 3px; border-radius: 2px; margin-top: 8px; }
  .section-block { border: 1px solid #e5e5ea; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; }
  .section-title { font-size: 14px; font-weight: 500; color: #1d1d1f; margin-bottom: 10px; }
  .section-tag { font-size: 11px; padding: 2px 10px; border-radius: 4px; font-weight: 500; margin-left: 8px; }
  .tag-warn { background: #faedd4; color: #854f0b; }
  .tag-red { background: #faeee7; color: #d85a30; }
  .tag-green { background: #e1f5ee; color: #1d9e75; }
  .fund-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px; }
  .fund-item { font-size: 12px; color: #636366; line-height: 1.6; }
  .fund-item strong { color: #1d1d1f; }
  .fund-positive { color: #d85a30; font-weight: 500; }
  .fund-negative { color: #1d9e75; font-weight: 500; }
  .fund-divider { border-top: 1px solid #f0f0f5; margin: 8px 0; padding-top: 8px; }
  .fund-conclusion { font-size: 12px; color: #636366; line-height: 1.6; }
  .prediction-model-block { border: 1px solid #e5e5ea; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; background: #fafcff; }
  .factor-bar { display: flex; gap: 2px; height: 20px; margin-bottom: 10px; border-radius: 4px; overflow: hidden; }
  .factor-seg { }
  .factor-table { display: grid; grid-template-columns: 48px 1fr 40px 48px; gap: 4px 8px; align-items: center; font-size: 11px; color: #636366; margin-bottom: 8px; }
  .factor-table .fname { font-weight: 500; color: #1d1d1f; }
  .factor-table .fweight { color: #aeaeb2; }
  .factor-table .fscore { text-align: right; font-weight: 600; }
  .factor-table .ftag { font-size: 10px; padding: 1px 6px; border-radius: 3px; text-align: center; white-space: nowrap; }
  .ftag-high { background: #faeee7; color: #d85a30; }
  .ftag-mid { background: #faedd4; color: #854f0b; }
  .ftag-low { background: #f5f5f7; color: #aeaeb2; }
  .score-summary { display: flex; align-items: center; gap: 10px; padding: 10px 0; border-top: 1px solid #f0f0f5; }
  .score-big { font-size: 28px; font-weight: 700; }
  .score-legend { display: grid; grid-template-columns: 6px 40px 42px 1fr; gap: 1px 6px; align-items: center; font-size: 9px; color: #636366; line-height: 1.4; margin-top: 8px; border: 1px solid #f0f0f5; border-radius: 6px; padding: 6px 10px; background: #fafafa; }
  .score-legend .dot { width: 6px; height: 6px; border-radius: 2px; display: inline-block; }
  .score-legend .active { font-weight: 600; color: #e67e22; }
  .advice-section { border: 1px solid #e5e5ea; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; }
  .advice-row { display: flex; align-items: flex-start; gap: 10px; padding: 8px 0; border-bottom: 1px solid #f0f0f5; }
  .advice-row:last-child { border-bottom: none; }
  .advice-tag { font-size: 11px; padding: 2px 10px; border-radius: 4px; font-weight: 500; white-space: nowrap; min-width: 72px; text-align: center; }
  .tag-hold { background: #fafcff; color: #636366; border: 1px solid #e5e5ea; }
  .tag-buy { background: #e1f5ee; color: #1d9e75; }
  .tag-sell { background: #faeee7; color: #d85a30; }
  .level-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .level-box { background: #f5f5f7; border-radius: 8px; padding: 10px 12px; }
  .level-label { font-size: 11px; color: #86868b; margin-bottom: 3px; }
  .level-value { font-size: 15px; font-weight: 500; }
  .level-value.support { color: #378add; }
  .level-value.resistance { color: #d85a30; }
  .level-value.cost { color: #1d1d1f; }
  .confidence-block { background: #fafcff; border: 1px solid #e3f2fd; border-radius: 12px; padding: 14px 18px; margin-bottom: 14px; }
  .prediction-row { display: flex; align-items: flex-start; gap: 8px; padding: 6px 0; font-size: 12px; color: #636366; line-height: 1.5; }
  .pred-dot { font-size: 14px; min-width: 16px; }
  .risk-block { background: #fafafa; border: 1px solid #f0f0f5; border-radius: 10px; padding: 12px 16px; margin-bottom: 14px; }
  .risk-title { font-size: 12px; font-weight: 500; color: #854f0b; margin-bottom: 6px; }
  .risk-item { font-size: 11px; color: #aeaeb2; line-height: 1.6; padding-left: 8px; border-left: 2px solid #faedd4; margin-bottom: 4px; }
  .tdx-banner { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 6px; padding: 6px 12px; font-size: 11px; color: #15803d; margin-bottom: 14px; }
  .tdx-banner.warn { background: #fffbeb; border: 1px solid #fde68a; color: #92400e; }
</style>"""

def fmt_amount(amt):
    """Format amount in yuan to readable string."""
    if amt is None: return "—"
    abs_amt = abs(amt)
    if abs_amt >= 1e8:
        return f"{amt/1e8:+.2f}亿"
    elif abs_amt >= 1e4:
        return f"{amt/1e4:+.0f}万"
    else:
        return f"{amt:+.0f}"

def fmt_volume(vol):
    if vol is None: return "—"
    if vol >= 10000:
        return f"{vol/10000:.1f}万"
    return str(vol)

def build_8cell_metrics(data):
    """Build 8-cell metrics grid HTML."""
    pct = data['change_pct']
    color_class = 'green' if pct < 0 else 'red'
    cells = [
        ('开盘', f"{data['open']:.2f}", ''),
        ('最高', f"{data['high']:.2f}", ''),
        ('最低', f"{data['low']:.2f}", 'blue'),
        ('昨收', f"{data['prev_close']:.2f}", ''),
        ('成交量', fmt_volume(data['volume']), ''),
        ('成交额', f"{data['amount']/1e8:.2f}亿", ''),
        ('换手率', f"{data['turnover']:.2f}%", ''),
        ('量比', f"{data['vol_ratio']:.2f}", 'gray'),
    ]
    html = '<div class="metrics">\n'
    for label, val, cls in cells:
        cls_attr = f' class="{cls}"' if cls else ''
        html += f'  <div class="metric"><div class="metric-label">{label}</div><div class="metric-value{cls_attr}">{val}</div></div>\n'
    html += '</div>\n'
    return html

def fmt_pct(val):
    if val is None: return "—"
    return f"{val:+.2f}%"

def build_fund_section(data):
    """Build fund flow section."""
    f = data['fund']
    lines = '<div class="section-block">\n'
    lines += '  <div class="section-title">💰 今日资金真相（上午） <span class="section-tag tag-red">tdx-已连接</span></div>\n'
    lines += '  <div class="fund-grid">\n'
    # tdx data (primary)
    tdx_inout = f.get('tdx_inout', 0)
    tdx_inout_hb = f.get('tdx_inout_hb', 0)
    tdx_wtb = f.get('tdx_wtb', 0)
    inside = f.get('inside', 0)
    outside = f.get('outside', 0)
    
    lines += f'    <div class="fund-item"><strong>📊 tdx主力净额</strong><br><span class="{"fund-positive" if tdx_inout >= 0 else "fund-negative"}">{fmt_amount(tdx_inout)}</span></div>\n'
    lines += f'    <div class="fund-item"><strong>📊 含北向</strong><br><span class="{"fund-positive" if tdx_inout_hb >= 0 else "fund-negative"}">{fmt_amount(tdx_inout_hb)}</span></div>\n'
    lines += f'    <div class="fund-item"><strong>📊 委比</strong><br>{tdx_wtb:+.2f}%</div>\n'
    lines += f'    <div class="fund-item"><strong>📊 外盘/内盘</strong><br><span class="fund-positive">外 {fmt_volume(outside)}</span> / <span class="fund-negative">内 {fmt_volume(inside)}</span></div>\n'
    lines += '  </div>\n'
    
    # Westock asfund supplementary
    jumbo = f.get('jumbo', 0)
    mid = f.get('mid', 0)
    small = f.get('small', 0)
    main_net = f.get('main_net', 0)
    main_5d = f.get('main_5d', 0)
    main_20d = f.get('main_20d', 0)
    
    lines += '  <div class="fund-grid">\n'
    lines += f'    <div class="fund-item"><strong>超大单</strong><br><span class="{"fund-positive" if jumbo >= 0 else "fund-negative"}">{fmt_amount(jumbo)}</span></div>\n'
    lines += f'    <div class="fund-item"><strong>中单</strong><br><span class="{"fund-positive" if mid >= 0 else "fund-negative"}">{fmt_amount(mid)}</span></div>\n'
    lines += f'    <div class="fund-item"><strong>小单(散户)</strong><br><span class="{"fund-positive" if small >= 0 else "fund-negative"}">{fmt_amount(small)}</span></div>\n'
    lines += f'    <div class="fund-item"><strong>主力净额(westock)</strong><br><span class="{"fund-positive" if main_net >= 0 else "fund-negative"}">{fmt_amount(main_net)}</span></div>\n'
    lines += '  </div>\n'
    
    lines += '  <div class="fund-divider"></div>\n'
    lines += f'  <div class="fund-item">5日主力累计: <span class="{"fund-positive" if main_5d >= 0 else "fund-negative"}">{fmt_amount(main_5d)}</span> | 20日: <span class="{"fund-positive" if main_20d >= 0 else "fund-negative"}">{fmt_amount(main_20d)}</span></div>\n'
    
    # Core contradiction analysis
    conclusion = data.get('fund_conclusion', '')
    if conclusion:
        lines += f'  <div class="fund-conclusion" style="margin-top:8px; font-weight:500; color:#1d1d1f;">{conclusion}</div>\n'
    
    lines += '</div>\n'
    return lines

def build_levels(data):
    """Build key levels grid."""
    levels = data.get('key_levels', {})
    supports = levels.get('support', [])
    resistances = levels.get('resistance', [])
    cost = levels.get('cost', 0)
    sar = levels.get('sar', 0)
    html = '<div class="section-block">\n'
    html += '  <div class="section-title">📊 关键价位</div>\n'
    html += '  <div class="level-grid">\n'
    
    # Support column
    sup_html = '<div class="level-box">\n'
    sup_html += '    <div class="level-label">🛡️ 支撑位</div>\n'
    for i, s in enumerate(supports[:4]):
        sup_html += f'    <div class="level-value support">{s:.2f}</div>\n'
    sup_html += '  </div>\n'
    
    # Resistance column
    res_html = '<div class="level-box">\n'
    res_html += '    <div class="level-label">⚔️ 压力位</div>\n'
    for i, r in enumerate(resistances[:4]):
        res_html += f'    <div class="level-value resistance">{r:.2f}</div>\n'
    res_html += '  </div>\n'
    
    html += sup_html + res_html + '  </div>\n'
    
    # Extra: cost, SAR, BOLL
    if cost:
        html += f'  <div style="font-size:11px; color:#86868b; margin-top:8px; text-align:center;">'
        html += f'持仓成本 <strong style="color:#1d1d1f;">¥{cost:.2f}</strong>'
        if sar:
            html += f' | SAR <strong>{sar:.2f}</strong>'
        boll_mid = levels.get('boll_mid', 0)
        if boll_mid:
            html += f' | BOLL中轨 <strong>{boll_mid:.2f}</strong>'
        html += '</div>\n'
    
    html += '</div>\n'
    return html

def build_prediction(data):
    """Build prediction section for midday mode."""
    pred = data.get('prediction', {})
    html = '<div class="prediction-model-block">\n'
    html += '  <div class="section-title">📈 下午走势预判</div>\n'
    
    # Base
    base = pred.get('base', {})
    html += f'  <div class="prediction-row"><div class="pred-dot">●</div><div><strong>基准场景</strong>（概率 {base.get("prob", 50)}%）<br>{base.get("desc", "")}<br>区间: {base.get("range", "")} | 收盘预估: ¥{base.get("close", 0):.2f}</div></div>\n'
    
    # Bull
    bull = pred.get('bull', {})
    html += f'  <div class="prediction-row"><div class="pred-dot" style="color:#d85a30">▲</div><div><strong>偏多场景</strong>（概率 {bull.get("prob", 20)}%）<br>触发: {bull.get("trigger", "")}<br>目标: {bull.get("target", "")}</div></div>\n'
    
    # Bear
    bear = pred.get('bear', {})
    html += f'  <div class="prediction-row"><div class="pred-dot" style="color:#1d9e75">▼</div><div><strong>偏空场景</strong>（概率 {bear.get("prob", 20)}%）<br>触发: {bear.get("trigger", "")}<br>目标: {bear.get("target", "")}</div></div>\n'
    
    # Confidence
    conf = data.get('confidence', 50)
    html += f'  <div style="margin-top:10px; padding-top:8px; border-top:1px solid #f0f0f5; font-size:11px; color:#636366;">置信度: <strong>{conf}/100</strong> {"▓" * (conf // 10)}{"░" * (10 - conf // 10)}</div>\n'
    html += '</div>\n'
    return html

def build_timeline(data):
    """Build 5-node timeline for midday."""
    nodes = data.get('timeline', [])
    html = '<div class="timeline-section">\n'
    html += '  <div class="timeline-title">⏱️ 上午分时关键节点</div>\n'
    html += '  <div class="timeline">\n'
    for node in nodes:
        dot_cls = node.get('dot_class', '')
        price_cls = node.get('price_class', '')
        desc_cls = node.get('desc_class', '')
        html += f'    <div class="tl-node">\n'
        html += f'      <div class="tl-dot {dot_cls}"></div>\n'
        html += f'      <div class="tl-time">{node["time"]}</div>\n'
        html += f'      <div class="tl-price {price_cls}">{node["price"]}</div>\n'
        html += f'      <div class="tl-desc {desc_cls}">{node["desc"]}</div>\n'
        html += f'    </div>\n'
    html += '  </div>\n'
    # Add trend bar
    bar_colors = [n.get('bar_color', '#aeaeb2') for n in nodes]
    bar_html = '  <div class="tl-bar" style="display:flex;gap:2px;">'
    for i, bc in enumerate(bar_colors):
        w = '20%'
        bar_html += f'<div style="flex:1;height:3px;background:{bc};border-radius:2px;"></div>'
    bar_html += '</div>\n'
    html += bar_html
    html += '</div>\n'
    return html

def build_analysis(data):
    """Build analysis text block."""
    analysis = data.get('analysis', '')
    html = '<div class="section-block">\n'
    html += '  <div class="section-title">🔍 上午走势复盘</div>\n'
    html += f'  <div style="font-size:12px;color:#636366;line-height:1.8;">{analysis}</div>\n'
    html += '</div>\n'
    return html

def build_risk(data):
    risks = data.get('risks', [])
    if not risks: return ''
    html = '<div class="risk-block">\n'
    html += '  <div class="risk-title">⚠️ 风险提示</div>\n'
    for r in risks:
        html += f'  <div class="risk-item">{r}</div>\n'
    html += '</div>\n'
    return html

def build_tdx_banner(connected=True):
    if connected:
        return '<div class="tdx-banner">✅ tdx-已连接 · 资金面数据来自通达信 ProInfo.InOut/Wtb</div>\n'
    else:
        return '<div class="tdx-banner warn">⚠️ tdx 未连接 · 资金面降级为 westock-data asfund</div>\n'

def build_card(data):
    """Build complete midday card HTML."""
    pct = data['change_pct']
    color_class = 'up' if pct >= 0 else 'down'
    bg_class = 'up-bg' if pct >= 0 else 'down-bg'
    mode_label = '午间复盘 · 上午收盘'
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{data['name']} 午间复盘</title>
{CSS}
</head>
<body>
<div class="card">
  {build_tdx_banner(data.get('tdx_connected', True))}
  <div class="header">
    <div>
      <div>
        <span class="stock-name">{data['name']}</span>
        <span class="stock-code">{data['code']}</span>
        <span class="badge blue">{data['market']}</span>
        <span class="badge {bg_class}">{mode_label}</span>
      </div>
      <div class="date-label">{data['date']}</div>
    </div>
    <div class="price-section">
      <div class="price">{data['price']:.2f}</div>
      <div class="change">
        <span class="change-val {color_class}">{data['change']:+.2f}</span>
        <span class="change-pct {bg_class}">{data['change_pct']:+.2f}%</span>
      </div>
      <div class="cost-tag">持仓成本 ¥{data['cost']:.3f} | 盈亏 {data['pnl']:+.1f}%</div>
    </div>
  </div>
  
  {build_8cell_metrics(data)}
  {build_timeline(data)}
  {build_fund_section(data)}
  {build_analysis(data)}
  {build_prediction(data)}
  {build_levels(data)}
  {build_risk(data)}
  
  <div class="confidence-block">
    <div style="font-size:11px;color:#aeaeb2;">模型自评 · {data['name']}历史预测 {data.get('accuracy', {}).get('total', 0)}次 | 方向准确率 {data.get('accuracy', {}).get('direction', 0)}% | 综合 {data.get('accuracy', {}).get('composite', 0)}%</div>
  </div>
</div>
</body>
</html>"""
    return html

# ─── STOCK DATA ───

stocks = []

# --- 新凤鸣 ---
xfm = {
    'name': '新凤鸣', 'code': 'sh603225', 'market': '上海主板',
    'date': '2026-06-11',
    'price': 18.39, 'change': -1.06, 'change_pct': -5.45,
    'open': 19.17, 'high': 19.63, 'low': 17.90, 'prev_close': 19.45,
    'volume': 220584, 'amount': 404424309, 'turnover': 1.32, 'vol_ratio': 1.49,
    'cost': 18.947, 'pnl': -2.94,
    'tdx_connected': True,
    'fund': {
        'tdx_inout': 63979920, 'tdx_inout_hb': -27072160, 'tdx_wtb': -55.66,
        'inside': 94469, 'outside': 126115,
        'jumbo': -18795525, 'mid': -35750532, 'small': 59895665,
        'main_net': -24145133, 'main_5d': 143136095, 'main_20d': 313209626,
    },
    'fund_conclusion': '⚠️ 矛盾信号：tdx主力+6398万 vs westock主力-2414万 + 委比-55.66%。以tdx外盘>内盘为准，偏多解读。中单-3575万出逃、散户+5990万接盘，低位承接结构。',
    'timeline': [
        {'time': '09:30', 'price': '¥19.17', 'desc': '低开', 'dot_class': 'green', 'bar_color': '#1d9e75'},
        {'time': '09:33', 'price': '¥18.94', 'desc': '急跌', 'dot_class': 'green', 'bar_color': '#1d9e75'},
        {'time': '10:24', 'price': '¥17.94', 'desc': '日低点', 'dot_class': 'highlight', 'desc_class': 'highlight', 'bar_color': '#ae3940'},
        {'time': '11:15', 'price': '¥18.50', 'desc': 'V反冲高', 'dot_class': 'red', 'bar_color': '#d85a30'},
        {'time': '11:30', 'price': '¥18.39', 'desc': '午间收盘', 'dot_class': 'blue', 'bar_color': '#378add'},
    ],
    'analysis': '<strong>形态：低开→砸盘深跌→深V反弹→尾盘回落。</strong><br><br>'
                '开盘¥19.17（低开-1.44%）后迅速跳水，09:33跌至¥18.94，随后持续下行，10:24触及日低¥17.94（-7.76%）。'
                '10:25后出现深V反弹，11:13-11:16拉升至¥18.50附近，尾盘小幅回落至¥18.39。<br><br>'
                '<strong>量能：</strong>量比1.49放量下跌，上午成交4.04亿。散户+5990万大幅接盘。<br><br>'
                '<strong>核心判断：</strong>减持利空引发的恐慌性抛售，但10:25后V反显示低位有承接。超大单-1879万偏空但体量不大，散户接盘说明恐慌盘在释放。'
                '减持消息消化中，下午关注能否站稳¥18.39上方、量能变化。',
    'prediction': {
        'base': {'prob': 55, 'desc': '恐慌消化区间震荡，测试¥18.39-18.50支撑', 'range': '¥17.90-¥18.80', 'close': 18.35},
        'bull': {'prob': 20, 'trigger': '13:00放量站稳¥18.50+化纤板块翻红+减持不启动', 'target': '¥18.80-¥19.17'},
        'bear': {'prob': 25, 'trigger': '缩量跌破¥17.90+减持消息持续发酵', 'target': '¥17.50-¥17.80'},
    },
    'confidence': 55,
    'key_levels': {
        'support': [17.90, 17.78, 17.50, 16.80],
        'resistance': [18.50, 18.80, 19.17, 19.45],
        'cost': 18.95, 'sar': 17.79, 'boll_mid': 17.96,
    },
    'risks': [
        '实控人减持计划尚未执行，后续减持可能继续压制股价',
        '委比-55.66%显示卖盘压力依然较大，V反后尾盘回落需警惕',
        '化纤板块整体偏弱，板块拖累可能持续',
    ],
    'accuracy': {'total': 9, 'direction': 75, 'composite': 76},
}
stocks.append(('xinfengming', xfm))

# --- 华工科技 ---
hgkj = {
    'name': '华工科技', 'code': 'sz000988', 'market': '深圳主板',
    'date': '2026-06-11',
    'price': 148.60, 'change': -0.40, 'change_pct': -0.27,
    'open': 148.01, 'high': 152.50, 'low': 148.01, 'prev_close': 149.00,
    'volume': 291346, 'amount': 4387903936, 'turnover': 2.90, 'vol_ratio': 0.82,
    'cost': 154.237, 'pnl': -3.66,
    'tdx_connected': True,
    'fund': {
        'tdx_inout': 9828864, 'tdx_inout_hb': -200351616, 'tdx_wtb': 52.60,
        'inside': 142811, 'outside': 148535,
        'jumbo': -159455193, 'mid': 72029289, 'small': 106110802,
        'main_net': -178140091, 'main_5d': -1547130165, 'main_20d': -10607357849,
    },
    'fund_conclusion': '⚠️ 矛盾信号：tdx+983万微流入 vs westock主力-1.78亿 vs 含北向-2.00亿。超大单-1.59亿出货 vs 中单+7202万/散户+1.06亿接盘。20日累计-106亿派发格局未改。委比+52.60%挂单偏多但实际成交偏空，典型\"挂多卖空\"。',
    'timeline': [
        {'time': '09:30', 'price': '¥148.01', 'desc': '微低开', 'dot_class': 'green', 'bar_color': '#1d9e75'},
        {'time': '09:47', 'price': '¥152.25', 'desc': '早盘冲高', 'dot_class': 'red', 'bar_color': '#d85a30'},
        {'time': '10:01', 'price': '¥149.90', 'desc': '回落', 'dot_class': 'green', 'bar_color': '#1d9e75'},
        {'time': '11:18', 'price': '¥148.61', 'desc': '上午低点', 'dot_class': 'highlight', 'desc_class': 'highlight', 'bar_color': '#ae3940'},
        {'time': '11:30', 'price': '¥148.60', 'desc': '午间收盘', 'dot_class': 'blue', 'bar_color': '#378add'},
    ],
    'analysis': '<strong>形态：微低开→早盘冲高→震荡回落→尾盘收低。</strong><br><br>'
                '开盘¥148.01微幅低开，09:31快速拉升至¥150.39，09:47冲高至¥152.25（+2.17%）后开始回落。'
                '10:00后主要在¥149-151区间窄幅震荡，11:18跌至上午最低¥148.61，尾盘微弹收¥148.60。<br><br>'
                '<strong>量能：</strong>量比0.82缩量，上午成交43.88亿。缩量冲高回落是典型的弱势信号。<br><br>'
                '<strong>核心判断：</strong>早盘拉高诱多后持续派发。缩量+冲高回落=多头无力。20日累计-106亿派发格局下，'
                '每一次反弹都是出货窗口。下午关注能否守住¥148.01（开盘价），若跌破则测试¥147.01（昨日前低）。',
    'prediction': {
        'base': {'prob': 55, 'desc': '低位震荡，测试¥147.01支撑', 'range': '¥147.00-¥150.00', 'close': 148.00},
        'bull': {'prob': 15, 'trigger': '13:00放量突破¥150.39+CPO板块止跌', 'target': '¥150.00-¥152.50'},
        'bear': {'prob': 30, 'trigger': '缩量跌破¥147.01+超大单持续出货', 'target': '¥145.00-¥147.00'},
    },
    'confidence': 48,
    'key_levels': {
        'support': [147.01, 145.00, 140.00, 137.21],
        'resistance': [150.39, 152.50, 154.87, 160.00],
        'cost': 154.24, 'sar': 167.77, 'boll_mid': 154.87,
    },
    'risks': [
        '20日主力累计-106亿派发格局未改，超大单持续卖出主动性高',
        '委比+52.60%但实际成交偏空，挂单虚多实空警惕诱多',
        'MACD死叉持续，DIF(4.58)<DEA(6.94)，技术面偏空',
    ],
    'accuracy': {'total': 6, 'direction': 60, 'composite': 64},
}
stocks.append(('huagongkeji', hgkj))

# --- 中兴通讯 ---
zxtx = {
    'name': '中兴通讯', 'code': 'sz000063', 'market': '深圳主板',
    'date': '2026-06-11',
    'price': 38.07, 'change': -0.35, 'change_pct': -0.91,
    'open': 37.91, 'high': 39.50, 'low': 37.62, 'prev_close': 38.42,
    'volume': 1488525, 'amount': 5754204555, 'turnover': 3.70, 'vol_ratio': 0.93,
    'cost': 35.785, 'pnl': +6.39,
    'tdx_connected': True,
    'fund': {
        'tdx_inout': -58002176, 'tdx_inout_hb': 58347520, 'tdx_wtb': 41.18,
        'inside': 749035, 'outside': 739490,
        'jumbo': 128567049, 'mid': -60965270, 'small': 14278459,
        'main_net': 46686811, 'main_5d': 2465409285, 'main_20d': 140545631,
    },
    'fund_conclusion': '矛盾信号：tdx主力-5800万 vs westock主力+4669万 vs 含北向+5835万。超大单+1.29亿吸筹 vs 中单-6097万出货。北向资金持续买入（InOutHB正值）是关键多头支撑。委比+41.18%偏多。整体偏多但力度减弱。',
    'timeline': [
        {'time': '09:30', 'price': '¥37.91', 'desc': '低开', 'dot_class': 'green', 'bar_color': '#1d9e75'},
        {'time': '09:34', 'price': '¥37.69', 'desc': '日低点', 'dot_class': 'highlight', 'desc_class': 'highlight', 'bar_color': '#ae3940'},
        {'time': '09:49', 'price': '¥39.49', 'desc': 'V反冲高', 'dot_class': 'red', 'bar_color': '#d85a30'},
        {'time': '10:55', 'price': '¥38.43', 'desc': '持续回落', 'dot_class': 'green', 'bar_color': '#1d9e75'},
        {'time': '11:30', 'price': '¥38.07', 'desc': '午间收盘', 'dot_class': 'blue', 'bar_color': '#378add'},
    ],
    'analysis': '<strong>形态：低开→深V反弹→冲高回落。</strong><br><br>'
                '开盘¥37.91（低开-1.33%），09:34探底¥37.69（日低-1.90%），随后V反爆发，09:49冲至¥39.49（日高+2.78%），'
                '半小时振幅达4.69%。但冲高后持续回落，10:00后主要在¥38.50-39.00震荡，11:18加速回落至¥38.07。<br><br>'
                '<strong>量能：</strong>量比0.93平量，上午成交57.54亿。V反后量能未持续放大，冲高回落验证量价配合不足。<br><br>'
                '<strong>核心判断：</strong>与6/4、6/9类似的低开V反→冲高回落模式。超大单+1.29亿吸筹但tdx主力-5800万，方向分歧说明'
                '下午方向不确定性高。5日主力+24.65亿显示中期偏多但短期有获利回吐压力。融券-4.06%空头撤退偏多。',
    'prediction': {
        'base': {'prob': 50, 'desc': '区间窄幅震荡消化上午冲高回落抛压', 'range': '¥37.60-¥38.50', 'close': 38.10},
        'bull': {'prob': 25, 'trigger': '13:00放量突破¥38.50+通信板块走强+北向续买', 'target': '¥38.80-¥39.50'},
        'bear': {'prob': 25, 'trigger': '跌破¥37.62+超大单转向流出+通信板块走弱', 'target': '¥36.91-¥37.50'},
    },
    'confidence': 50,
    'key_levels': {
        'support': [37.62, 36.91, 35.86, 35.79],
        'resistance': [38.50, 39.00, 39.49, 40.00],
        'cost': 35.79, 'sar': 35.59, 'boll_mid': 36.92,
    },
    'risks': [
        '冲高回落模式已重复3次（6/4、6/9、6/11），下午延续回调概率偏高',
        'tdx主力-5800万与超大单+1.29亿方向矛盾，需验证下午主力真实意图',
        'MACD金叉延续但KDJ-K(54.19)≈KDJ-D(53.44)，超买风险不大但方向不明',
    ],
    'accuracy': {'total': 13, 'direction': 75, 'composite': 72},
}
stocks.append(('zhongxingtongxun', zxtx))

# ─── GENERATE ───
for pinyin, data in stocks:
    html_path = os.path.join(WORKSPACE, f'{pinyin}_card.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(build_card(data))
    print(f'✅ {data["name"]}: {html_path}')

# ─── UPDATE JSON ───
def update_index_json(pinyin, data, folder):
    """Append a new session to the index.json."""
    idx_path = os.path.join(WORKSPACE, 'data', folder, 'index.json')
    with open(idx_path, 'r', encoding='utf-8') as f:
        idx = json.load(f)
    
    # Check if session already exists
    for s in idx['sessions']:
        if s['date'] == '2026-06-11' and s['session'] == 'morning':
            print(f'  ⚠️ {data["name"]} 午间已存在，跳过')
            return idx_path
    
    f = data['fund']
    session = {
        'date': '2026-06-11',
        'session': 'morning',
        'price': data['price'],
        'prev_close': data['prev_close'],
        'change': data['change'],
        'change_percent': data['change_pct'],
        'open': data['open'],
        'high': data['high'],
        'low': data['low'],
        'volume': data['volume'],
        'amount': data['amount'],
        'turnover_rate': data['turnover'],
        'volume_ratio': data['vol_ratio'],
        'fund_flow': {
            'tdx_inout': f['tdx_inout'],
            'tdx_inout_hb': f['tdx_inout_hb'],
            'tdx_wtb': f['tdx_wtb'],
            'inside': f['inside'],
            'outside': f['outside'],
            'main_net_flow': f['main_net'],
            'jumbo_net_flow': f['jumbo'],
            'mid_net_flow': f['mid'],
            'small_net_flow': f['small'],
            'main_net_5d': f['main_5d'],
            'main_net_20d': f['main_20d'],
        },
        'sanshou_score': data.get('score', 50),
        'score_category': data.get('score_category', '震荡'),
        'predictions': {
            'base': {
                'probability': data['prediction']['base']['prob'],
                'description': data['prediction']['base']['desc'],
                'range': data['prediction']['base']['range'],
                'close_estimate': data['prediction']['base']['close'],
            },
            'bull': {
                'probability': data['prediction']['bull']['prob'],
                'trigger': data['prediction']['bull']['trigger'],
                'target': data['prediction']['bull']['target'],
            },
            'bear': {
                'probability': data['prediction']['bear']['prob'],
                'trigger': data['prediction']['bear']['trigger'],
                'target': data['prediction']['bear']['target'],
            },
        },
        'confidence': data['confidence'],
        'key_levels': {
            'support': data['key_levels']['support'],
            'resistance': data['key_levels']['resistance'],
            'cost': data['key_levels']['cost'],
        },
        'card_html': f"cards/2026-06-11-midday.html",
        'card_screenshot': f"cards/2026-06-11-midday.png",
        'tdx_connected': True,
    }
    
    # Remove midday_verification if exists (not applicable for morning)
    idx['sessions'].append(session)
    
    # Update accuracy
    acc = idx.get('accuracy', {})
    acc['total_predictions'] = acc.get('total_predictions', 0) + 1
    idx['accuracy'] = acc
    
    with open(idx_path, 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    
    print(f'✅ JSON updated: {idx_path}')
    return idx_path

folders = {'xinfengming': 'xinfengming', 'huagongkeji': 'huagongkeji', 'zhongxingtongxun': 'zhongxingtongxun'}
for pinyin, data in stocks:
    update_index_json(pinyin, data, folders[pinyin])

print('\nDone! All 3 midday cards generated.')

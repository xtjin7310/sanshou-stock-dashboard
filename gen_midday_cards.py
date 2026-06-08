#!/usr/bin/env python3
"""Generate midday review HTML cards for all 3 stocks: 新凤鸣, 中兴通讯, 华工科技"""

import json, os

# ========== Data collected from tdx_quotes + westock-data ==========

stocks = {
    "xinfengming": {
        "name": "新凤鸣",
        "code": "603225",
        "market": "SH",
        "sector": "化学纤维",
        "date": "2026-06-08",
        "time": "11:30",
        "label": "午间",
        "session": "午间复盘 · 上午收盘",
        "price": 19.54,
        "prev_close": 20.33,
        "open": 19.61,
        "high": 20.25,
        "low": 19.45,
        "volume_hands": 112051,
        "amount_yuan": 221022327,
        "turnover": 0.67,
        "volume_ratio": 0.66,
        "change": -0.79,
        "change_pct": -3.89,
        "cost": 18.947,
        "profit_pct": 3.13,
        "tdx_inout": 1913,        # 万元
        "tdx_inout_hb": 3546,     # 万元
        "tdx_wtb": 3.98,
        "inside": 52063,
        "outside": 59988,
        "pe_static": 32.19,
        "pe_ttm": 30.35,
        "zaf20": 6.89,
        "this_year": 0.41,
        "hy_zaf": -1.92,
        "outliers_removed": [],
        "asfund_main": 3111,      # 万元
        "asfund_jumbo": 2827,     # 万元
        "asfund_mid": -3484,      # 万元
        "asfund_small": 374,      # 万元
        "asfund_5d": 14674,
        "asfund_20d": 20138,
        "margin_value": 36597,    # 万元
        "margin_dod": 8.95,
        "security_value": 594,    # 万元
        "security_dod": 33.91,
        "is_red": False,          # price down
        "nodes": [
            {"time": "09:30", "price": 19.61, "desc": "低开-3.54%", "dot": "green"},
            {"time": "09:32", "price": 20.01, "desc": "快速拉升", "dot": "red"},
            {"time": "09:56", "price": 19.86, "desc": "二次冲高", "dot": "red"},
            {"time": "10:53", "price": 19.85, "desc": "震荡高位", "dot": "grey"},
            {"time": "11:30", "price": 19.54, "desc": "尾盘回落", "dot": "blue"},
        ],
        "support": [19.45, 19.23, 18.95, 17.54],
        "resistance": [20.25, 20.33, 20.80, 21.12],
        "score": 48,
        "score_category": "震空",
        "confidence": 55,
        "pred_base_range": "19.20-19.80",
        "pred_base_close": 19.50,
        "pred_bull_target": "20.00-20.25",
        "pred_bull_trigger": "13:00放量站稳19.80+化纤板块翻红",
        "pred_bear_target": "19.00-19.23",
        "pred_bear_trigger": "缩量跌破19.45+化纤继续走弱",
        "trend_summary": "低开冲高震荡后尾盘回落。开盘大幅低开-3.54%后急速拉升至20.01（+1.33%振幅），但量能不足（量比0.66缩量），10:00后震荡重心下移，尾盘小幅跳水。",
        "core_judge": "缩量低开反弹乏力，主力小幅流入（+1913万）但Wtb仅3.98%委比弱势，下午大概率在19.20-20.00区间震荡。关注化纤板块能否企稳带动个股修复。",
        "risk": ["量比0.66缩量，反弹持续性存疑", "融券余额环比+33.91%，空头加仓信号", "化纤板块跌1.92%，板块压制明显"],
        "purity_note": "超大单纯度44.8%(LOW)，大单主导，主力信号需打折"
    },
    "zhongxingtongxun": {
        "name": "中兴通讯",
        "code": "000063",
        "market": "SZ",
        "sector": "通信设备",
        "date": "2026-06-08",
        "time": "11:30",
        "label": "午间",
        "session": "午间复盘 · 上午收盘",
        "price": 37.12,
        "prev_close": 39.13,
        "open": 38.02,
        "high": 39.00,
        "low": 37.08,
        "volume_hands": 2035433,
        "amount_yuan": 7750210198,
        "turnover": 5.05,
        "volume_ratio": 1.58,
        "change": -2.01,
        "change_pct": -5.14,
        "cost": 35.785,
        "profit_pct": 3.73,
        "tdx_inout": -137566,      # 万元
        "tdx_inout_hb": -106302,   # 万元
        "tdx_wtb": 88.55,
        "inside": 1142963,
        "outside": 892470,
        "pe_static": 31.61,
        "pe_ttm": 39.68,
        "zaf20": -5.09,
        "this_year": -1.90,
        "hy_zaf": -2.73,
        "asfund_main": -122201,    # 万元
        "asfund_jumbo": -121665,   # 万元
        "asfund_mid": 16900,       # 万元
        "asfund_small": 105300,    # 万元
        "asfund_5d": 318634,
        "asfund_20d": 7768,
        "block_trade": "协议交易 34.00（折价-6.64%）",
        "margin_value": 1077842,   # 万元
        "margin_dod": 4.09,
        "is_red": False,
        "nodes": [
            {"time": "09:30", "price": 38.02, "desc": "低开-2.84%", "dot": "green"},
            {"time": "09:32", "price": 38.97, "desc": "急拉翻红", "dot": "red"},
            {"time": "10:05", "price": 37.90, "desc": "跌破38", "dot": "blue"},
            {"time": "10:32", "price": 38.03, "desc": "V反回弹", "dot": "red"},
            {"time": "11:30", "price": 37.12, "desc": "尾盘砸低", "dot": "green"},
        ],
        "support": [37.08, 36.50, 35.79, 35.50],
        "resistance": [38.50, 39.00, 39.13, 41.30],
        "score": 38,
        "score_category": "偏空",
        "confidence": 65,
        "pred_base_range": "36.50-38.00",
        "pred_base_close": 37.20,
        "pred_bull_target": "38.50-39.00",
        "pred_bull_trigger": "13:00-13:30放量站稳37.50+通信板块反弹",
        "pred_bear_target": "36.00-36.50",
        "pred_bear_trigger": "缩量跌破37.08+主力继续净流出>5亿",
        "trend_summary": "低开后急拉翻红（38.02→38.97），但10:05后一路单边下行，从38.90跌至37.08日内新低，尾盘微反弹至37.12。Wtb高达88.55但资金净流出13.76亿，盘口虚多实空信号明显。",
        "core_judge": "主力上午净流出13.76亿（超大单-12.17亿），Wtb高挂88.55%但实际成交外盘<内盘，典型诱多出货。换手5.05%放量下跌，下午大概率继续下探37.00-36.50支撑区。",
        "risk": ["主力上午净流出13.76亿，抛压巨大", "Wtb 88.55%与价格-5.14%严重背离（虚多实空）", "换手5.05%放量下跌，空头趋势明确", "大宗交易折价6.64%（34.00 vs 37.12）"],
        "purity_note": "超大单纯度70.1%(HIGH)，主力信号可信"
    },
    "huagongkeji": {
        "name": "华工科技",
        "code": "000988",
        "market": "SZ",
        "sector": "CPO/通信",
        "date": "2026-06-08",
        "time": "11:30",
        "label": "午间",
        "session": "午间复盘 · 上午收盘",
        "price": 150.51,
        "prev_close": 157.20,
        "open": 146.00,
        "high": 154.78,
        "low": 146.00,
        "volume_hands": 444146,
        "amount_yuan": 6657604839,
        "turnover": 4.42,
        "volume_ratio": 1.03,
        "change": -6.69,
        "change_pct": -4.26,
        "cost": 154.237,
        "profit_pct": -2.42,
        "tdx_inout": -35631,       # 万元
        "tdx_inout_hb": -52262,    # 万元
        "tdx_wtb": 41.59,
        "inside": 227011,
        "outside": 217135,
        "pe_static": 102.90,
        "pe_ttm": 89.06,
        "zaf20": 2.0,
        "this_year": 89.73,
        "hy_zaf": -0.83,
        "asfund_main": -55200,     # 万元
        "asfund_jumbo": -43796,    # 万元
        "asfund_mid": 25850,       # 万元
        "asfund_small": 29350,     # 万元
        "asfund_5d": -25308,
        "asfund_20d": -1075896,
        "block_trade": "协议交易 156.31（机构买入，折价0%）",
        "margin_value": 1122094,   # 万元
        "margin_dod": 1.29,
        "security_value": 2346,    # 万元
        "security_dod": 11.19,
        "is_red": False,
        "nodes": [
            {"time": "09:30", "price": 146.00, "desc": "巨幅低开-7.12%", "dot": "green"},
            {"time": "09:52", "price": 150.53, "desc": "V反冲破150", "dot": "red"},
            {"time": "10:07", "price": 152.90, "desc": "强势拉涨", "dot": "red"},
            {"time": "10:40", "price": 154.50, "desc": "日内高点", "dot": "red"},
            {"time": "11:30", "price": 150.51, "desc": "冲高回落", "dot": "blue"},
        ],
        "support": [150.00, 146.00, 152.00, 154.24],
        "resistance": [154.78, 157.20, 165.87, 175.80],
        "score": 45,
        "score_category": "震空",
        "confidence": 52,
        "pred_base_range": "148.00-153.00",
        "pred_base_close": 150.00,
        "pred_bull_target": "154.00-155.00",
        "pred_bull_trigger": "13:00放量站稳151.50+CPO板块翻红",
        "pred_bear_target": "145.00-147.00",
        "pred_bear_trigger": "缩量跌破150+主力继续净流出>3亿",
        "trend_summary": "巨幅低开-7.12%后抄底资金涌入，0931-1040从146强势V反至154.78（振幅+6%），但冲高后持续回落至150.51。10:07-10:40冲高后持续回撤2.7%，典型的'利好出货'V反形态。",
        "core_judge": "主力上午净流出3.56亿（超大单-4.38亿），虽然低开后V反但资金面不支持持续走强。Wtb 41.59%但内盘>外盘，下午大概率在148-154区间震荡走弱。20日主力累计-107.59亿是最大隐患。",
        "risk": ["20日主力累计净流出107.59亿，中长期空头主导", "上午V反后冲高回落，抄底盘获利回吐压力", "融券余额环比+11.19%，空头持续加仓", "内盘>外盘（227011 vs 217135），实际卖压大于买盘"],
        "purity_note": "超大单纯度75.3%(HIGH)，主力信号可信度高"
    },
}

def format_amount(yuan):
    """Format amount in readable form"""
    if abs(yuan) >= 1e8:
        return f"{yuan/1e8:.2f}亿"
    elif abs(yuan) >= 1e4:
        return f"{yuan/1e4:.0f}万"
    else:
        return f"{yuan:.0f}"

def format_vol(hands):
    if hands >= 10000:
        return f"{hands/10000:.1f}万手"
    else:
        return f"{hands}手"

def get_color_cls(is_red):
    return "red" if is_red else "green"

def get_color_hex(is_red):
    return "#d85a30" if is_red else "#1d9e75"

def gen_card(s):
    is_red = s['is_red']
    color_cls = "red" if is_red else "green"
    color_hex = "#d85a30" if is_red else "#1d9e75"
    bg_color = "#faeee7" if is_red else "#e1f5ee"
    chg_sign = "+" if is_red else ""
    
    profit_pct = s['profit_pct']
    profit_str = f"浮盈 +{profit_pct:.1f}%" if profit_pct >= 0 else f"浮亏 {profit_pct:.1f}%"
    
    # Fund flow
    tdx_in = s['tdx_inout']
    tdx_in_str = f"+{tdx_in/10000:.2f}亿" if tdx_in >= 0 else f"{tdx_in/10000:.2f}亿"
    tdx_hb_str = f"+{s['tdx_inout_hb']/10000:.2f}亿" if s['tdx_inout_hb'] >= 0 else f"{s['tdx_inout_hb']/10000:.2f}亿"
    
    jumbo_str = f"+{s['asfund_jumbo']/10000:.2f}亿" if s['asfund_jumbo'] >= 0 else f"{s['asfund_jumbo']/10000:.2f}亿"
    mid_str = f"+{s['asfund_mid']/10000:.2f}亿" if s['asfund_mid'] >= 0 else f"{s['asfund_mid']/10000:.2f}亿"
    small_str = f"+{s['asfund_small']/10000:.2f}亿" if s['asfund_small'] >= 0 else f"{s['asfund_small']/10000:.2f}亿"
    main_str = f"+{s['asfund_main']/10000:.2f}亿" if s['asfund_main'] >= 0 else f"{s['asfund_main']/10000:.2f}亿"
    
    asfund_5d = f"+{s['asfund_5d']/10000:.2f}亿" if s['asfund_5d'] >= 0 else f"{s['asfund_5d']/10000:.2f}亿"
    asfund_20d = f"+{s['asfund_20d']/10000:.2f}亿" if s['asfund_20d'] >= 0 else f"{s['asfund_20d']/10000:.2f}亿"
    
    margin_val = f"{s['margin_value']/10000:.2f}亿"
    
    # Nodes
    nodes_html = ""
    n = len(s['nodes'])
    for i, node in enumerate(s['nodes']):
        dot_cls = node['dot']
        if dot_cls == 'red':
            dot_style = 'style="background:#d85a30;"'
        elif dot_cls == 'green':
            dot_style = 'style="background:#1d9e75;"'
        elif dot_cls == 'blue':
            dot_style = 'style="background:#378add;"'
        else:
            dot_style = 'style="background:#aeaeb2;"'
        
        desc_cls = 'highlight' if i == n-1 else ''
        nodes_html += f'''
        <div class="tl-node">
          <div class="tl-dot" {dot_style}></div>
          <div class="tl-time">{node['time']}</div>
          <div class="tl-price">{node['price']}</div>
          <div class="tl-desc{' highlight' if i == n-1 else ''}">{node['desc']}</div>
        </div>'''
    
    # Score bar
    score = s['score']
    score_color = "#1d9e75" if score >= 60 else ("#e67e22" if score >= 40 else "#d85a30")
    score_bar_w = score
    
    # Support/Resistance
    sup_html = ""
    for lv in s['support'][:4]:
        sup_html += f'<div class="level-box"><div class="level-label">支撑位</div><div class="level-value support">{lv}</div></div>'
    for lv in s['resistance'][:4]:
        sup_html += f'<div class="level-box"><div class="level-label">压力位</div><div class="level-value resistance">{lv}</div></div>'
    
    # Risks
    risk_html = ""
    for r in s['risk']:
        risk_html += f'<div style="font-size:11px;color:#d85a30;margin-bottom:4px;">⚠️ {r}</div>'
    
    # Wtb note
    wtb_note = ""
    if s.get('tdx_wtb') and s['tdx_wtb'] > 50 and s['change_pct'] < -3:
        wtb_note = f'<div style="font-size:10px;color:#d85a30;margin-top:4px;">⚠ Wtb {s["tdx_wtb"]:.1f}%与价格{s["change_pct"]:.1f}%严重背离——盘口虚多实空</div>'
    
    # Block trade
    block_html = ""
    if s.get('block_trade'):
        block_html = f'<div style="font-size:11px;color:#636366;margin-top:4px;">📋 大宗交易: {s["block_trade"]}</div>'
    
    # Security note
    sec = ""
    if s.get('security_value') and s['security_value'] > 0:
        sec_val = f"{s['security_value']/10000:.0f}万"
        sec_dod = s.get('security_dod', 0)
        if sec_dod > 20:
            sec = f' | 融券{sec_val}(环比+{sec_dod:.1f}%⚠)'
        else:
            sec = f' | 融券{sec_val}(环比+{sec_dod:.1f}%)'
    
    purity_html = f'<div style="font-size:10px;color:#aeaeb2;margin-top:2px;">📊 {s["purity_note"]}</div>'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{s['name']} 午间复盘卡片</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
    background: #f5f5f7;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
  }}
  .card {{ width: 600px; background: #fff; border-radius: 16px; padding: 24px; box-shadow: 0 2px 20px rgba(0,0,0,0.08); }}
  .header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 18px; }}
  .stock-name {{ font-size: 20px; font-weight: 600; color: #1d1d1f; }}
  .stock-code {{ font-size: 13px; color: #86868b; margin-left: 8px; }}
  .badge {{ display: inline-block; font-size: 11px; background: #f2f2f7; color: #86868b; padding: 2px 10px; border-radius: 4px; margin-left: 6px; vertical-align: middle; }}
  .badge.red {{ background: #faeee7; color: #d85a30; }}
  .badge.green {{ background: #e1f5ee; color: #1d9e75; }}
  .date-label {{ font-size: 12px; color: #aeaeb2; margin-top: 4px; }}
  .price-section {{ text-align: right; }}
  .price {{ font-size: 32px; font-weight: 600; color: #1d1d1f; line-height: 1.1; }}
  .change {{ display: flex; align-items: center; justify-content: flex-end; gap: 6px; margin-top: 4px; }}
  .change-val {{ font-size: 14px; font-weight: 500; color: {color_hex}; }}
  .change-pct {{ font-size: 13px; font-weight: 500; color: {color_hex}; background: {bg_color}; padding: 1px 8px; border-radius: 4px; }}
  .cost-tag {{ font-size: 11px; color: #aeaeb2; margin-top: 2px; }}
  .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 18px; }}
  .metric {{ background: #f5f5f7; border-radius: 8px; padding: 10px 12px; }}
  .metric-label {{ font-size: 11px; color: #86868b; margin-bottom: 3px; }}
  .metric-value {{ font-size: 15px; font-weight: 500; color: #1d1d1f; }}
  .metric-value.blue {{ color: #378add; }}
  .metric-value.gray {{ color: #888780; }}
  .metric-value.red {{ color: #d85a30; }}
  .metric-value.green {{ color: #1d9e75; }}
  .timeline-section {{ border: 1px solid #e5e5ea; border-radius: 12px; padding: 16px 18px; margin-bottom: 16px; }}
  .timeline-title {{ font-size: 13px; font-weight: 500; color: #1d1d1f; margin-bottom: 12px; }}
  .timeline {{ display: flex; justify-content: space-between; position: relative; padding: 4px 0; }}
  .tl-node {{ display: flex; flex-direction: column; align-items: center; flex: 1; }}
  .tl-dot {{ width: 8px; height: 8px; border-radius: 50%; background: #aeaeb2; z-index: 2; }}
  .tl-time {{ font-size: 10px; color: #aeaeb2; margin-top: 6px; white-space: nowrap; }}
  .tl-price {{ font-size: 12px; font-weight: 500; margin-top: 2px; }}
  .tl-desc {{ font-size: 10px; color: #aeaeb2; margin-top: 1px; white-space: nowrap; }}
  .tl-desc.highlight {{ font-size: 10px; background: #faeee7; color: #d85a30; padding: 0 6px; border-radius: 3px; font-weight: 500; }}
  .section-block {{ border: 1px solid #e5e5ea; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; }}
  .section-title {{ font-size: 14px; font-weight: 500; color: #1d1d1f; margin-bottom: 10px; }}
  .section-tag {{ font-size: 11px; padding: 2px 10px; border-radius: 4px; font-weight: 500; margin-left: 8px; }}
  .tag-warn {{ background: #faedd4; color: #854f0b; }}
  .tag-red {{ background: #faeee7; color: #d85a30; }}
  .tag-green {{ background: #e1f5ee; color: #1d9e75; }}
  .fund-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px; }}
  .fund-item {{ font-size: 12px; color: #636366; line-height: 1.6; }}
  .fund-item strong {{ color: #1d1d1f; }}
  .fund-positive {{ color: #d85a30; font-weight: 500; }}
  .fund-negative {{ color: #1d9e75; font-weight: 500; }}
  .fund-divider {{ border-top: 1px solid #f0f0f5; margin: 8px 0; padding-top: 8px; }}
  .fund-conclusion {{ font-size: 12px; color: #636366; line-height: 1.6; }}
  .prediction-model-block {{ border: 1px solid #e5e5ea; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; background: #fafcff; }}
  .factor-bar {{ display: flex; gap: 2px; height: 20px; margin-bottom: 10px; }}
  .factor-seg {{ border-radius: 3px; }}
  .factor-table {{ display: grid; grid-template-columns: 48px 1fr 40px 48px; gap: 4px 8px; align-items: center; font-size: 11px; color: #636366; margin-bottom: 8px; }}
  .factor-table .fname {{ font-weight: 500; color: #1d1d1f; }}
  .factor-table .fweight {{ color: #aeaeb2; }}
  .factor-table .fscore {{ text-align: right; font-weight: 600; }}
  .factor-table .ftag {{ font-size: 10px; padding: 1px 6px; border-radius: 3px; text-align: center; white-space: nowrap; }}
  .ftag-high {{ background: #faeee7; color: #d85a30; }}
  .ftag-mid {{ background: #faedd4; color: #854f0b; }}
  .ftag-low {{ background: #f5f5f7; color: #aeaeb2; }}
  .score-summary {{ display: flex; align-items: center; gap: 10px; padding: 10px 0; border-top: 1px solid #f0f0f5; }}
  .score-big {{ font-size: 28px; font-weight: 700; color: {score_color}; }}
  .score-label {{ font-size: 12px; color: #636366; line-height: 1.4; }}
  .score-legend {{ display: grid; grid-template-columns: 6px 40px 42px 1fr; gap: 1px 6px; align-items: center; font-size: 9px; color: #636366; line-height: 1.4; margin-top: 8px; border: 1px solid #f0f0f5; border-radius: 6px; padding: 6px 10px; background: #fafafa; }}
  .score-legend .dot {{ width: 6px; height: 6px; border-radius: 2px; display: inline-block; }}
  .score-legend .active {{ font-weight: 600; }}
  .advice-section {{ border: 1px solid #e5e5ea; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; }}
  .advice-row {{ display: flex; align-items: flex-start; gap: 10px; padding: 8px 0; border-bottom: 1px solid #f0f0f5; }}
  .advice-row:last-child {{ border-bottom: none; }}
  .advice-tag {{ font-size: 11px; padding: 2px 10px; border-radius: 4px; font-weight: 500; white-space: nowrap; min-width: 72px; text-align: center; }}
  .tag-hold {{ background: #fafcff; color: #636366; border: 1px solid #e5e5ea; }}
  .tag-buy {{ background: #e1f5ee; color: #1d9e75; }}
  .tag-sell {{ background: #faeee7; color: #d85a30; }}
  .level-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
  .level-box {{ background: #f5f5f7; border-radius: 8px; padding: 10px 12px; }}
  .level-label {{ font-size: 11px; color: #86868b; margin-bottom: 3px; }}
  .level-value {{ font-size: 15px; font-weight: 500; }}
  .level-value.support {{ color: #378add; }}
  .level-value.resistance {{ color: #d85a30; }}
  .level-value.cost {{ color: #1d1d1f; }}
  .confidence-block {{ background: #fafcff; border: 1px solid #e3f2fd; border-radius: 12px; padding: 14px 18px; margin-bottom: 14px; }}
  .conf-title {{ font-size: 13px; font-weight: 500; color: #1d1d1f; margin-bottom: 6px; }}
  .conf-row {{ font-size: 12px; color: #636366; line-height: 1.6; }}
  .tdx-src {{ font-size: 9px; background: #e1f5ee; color: #1d9e75; padding: 1px 5px; border-radius: 3px; margin-left: 4px; vertical-align: middle; }}
  .risk-block {{ border: 1px solid #faedd4; border-radius: 12px; padding: 14px 18px; margin-bottom: 14px; background: #fffbf0; }}
  .risk-title {{ font-size: 13px; font-weight: 500; color: #854f0b; margin-bottom: 8px; }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <div>
      <div>
        <span class="stock-name">{s['name']}</span>
        <span class="stock-code">{s['code']}.{s['market']}</span>
        <span class="badge {color_cls}">{s['label']}</span>
        <span class="badge" style="background:#f5f5f7;color:#636366;">{s['sector']}</span>
      </div>
      <div class="date-label">{s['date']} {s['time']} · {s['session']}<span class="tdx-src">✅ tdx-已连接</span></div>
    </div>
    <div class="price-section">
      <div class="price">{s['price']}</div>
      <div class="change">
        <span class="change-val">{chg_sign}{s['change']}</span>
        <span class="change-pct">{chg_sign}{s['change_pct']}%</span>
      </div>
      <div class="cost-tag">持仓成本 {s['cost']} · {profit_str}</div>
    </div>
  </div>

  <div class="metrics">
    <div class="metric"><div class="metric-label">开盘</div><div class="metric-value">{s['open']}</div></div>
    <div class="metric"><div class="metric-label">最高</div><div class="metric-value red">{s['high']}</div></div>
    <div class="metric"><div class="metric-label">最低</div><div class="metric-value blue">{s['low']}</div></div>
    <div class="metric"><div class="metric-label">昨收</div><div class="metric-value gray">{s['prev_close']}</div></div>
    <div class="metric"><div class="metric-label">成交量</div><div class="metric-value">{format_vol(s['volume_hands'])}</div></div>
    <div class="metric"><div class="metric-label">成交额</div><div class="metric-value">{format_amount(s['amount_yuan'])}</div></div>
    <div class="metric"><div class="metric-label">换手率</div><div class="metric-value">{s['turnover']}%</div></div>
    <div class="metric"><div class="metric-label">量比</div><div class="metric-value gray">{s['volume_ratio']}</div></div>
  </div>

  <div class="timeline-section">
    <div class="timeline-title">上午分时走势关键节点</div>
    <div class="timeline">
      {nodes_html}
    </div>
    <div style="margin-top:10px;font-size:12px;color:#636366;line-height:1.5;">
      {s['trend_summary']}
    </div>
  </div>

  <div class="section-block">
    <div class="section-title">💰 上午资金真相 <span class="section-tag tag-red">以tdx为准</span></div>
    <div class="fund-grid">
      <div class="fund-item"><strong>主力净额(tdx InOut):</strong> <span class="{'fund-positive' if tdx_in >= 0 else 'fund-negative'}">{tdx_in_str}</span></div>
      <div class="fund-item"><strong>含北向 InOutHB:</strong> <span class="fund-negative">{tdx_hb_str}</span></div>
      <div class="fund-item"><strong>超大单净额:</strong> <span class="{'fund-positive' if s['asfund_jumbo'] >= 0 else 'fund-negative'}">{jumbo_str}</span></div>
      <div class="fund-item"><strong>中单净额:</strong> <span class="{'fund-positive' if s['asfund_mid'] >= 0 else 'fund-negative'}">{mid_str}</span></div>
      <div class="fund-item"><strong>小单净额:</strong> <span class="{'fund-positive' if s['asfund_small'] >= 0 else 'fund-negative'}">{small_str}</span></div>
      <div class="fund-item"><strong>5日/20日主力:</strong> {asfund_5d} / {asfund_20d}</div>
      <div class="fund-item"><strong>外盘/内盘:</strong> {format_vol(s['outside'])} / {format_vol(s['inside'])}</div>
      <div class="fund-item"><strong>融资余额:</strong> {margin_val} (环比+{s['margin_dod']}%){sec}</div>
    </div>
    {block_html}
    {wtb_note}
    {purity_html}
    <div class="fund-divider"></div>
    <div class="fund-conclusion">
      <strong>核心判断：</strong>{s['core_judge']}
    </div>
  </div>

  <div class="prediction-model-block">
    <div class="section-title">📈 三寿股价预测评分 v2.5.1 <span class="section-tag tag-warn">{s['score_category']}</span></div>
    <div class="factor-bar">
      <div class="factor-seg" style="width:{min(25,100)}%;background:#86868b;"></div>
      <div class="factor-seg" style="width:{min(20,100)}%;background:#a0a0a0;"></div>
      <div class="factor-seg" style="width:{min(20,100)}%;background:#b0b0b0;"></div>
      <div class="factor-seg" style="width:{min(15,100)}%;background:#c0c0c0;"></div>
      <div class="factor-seg" style="width:{min(10,100)}%;background:#d0d0d0;"></div>
      <div class="factor-seg" style="width:{min(8,100)}%;background:#e0e0e0;"></div>
      <div class="factor-seg" style="width:{min(2,100)}%;background:#f0f0f0;"></div>
    </div>
    <div class="factor-table">
      <span class="fname">技术面</span><span>MA5-10-20趋势偏空</span><span class="fweight">25%</span><span class="fscore">12</span><span class="ftag ftag-low">弱</span>
      <span class="fname">量价</span><span>缩量下跌</span><span class="fweight">20%</span><span class="fscore">10</span><span class="ftag ftag-low">弱</span>
      <span class="fname">资金</span><span>主力小幅流入/流出</span><span class="fweight">20%</span><span class="fscore">{14 if tdx_in >= 0 else 6}</span><span class="ftag ftag-{'mid' if tdx_in >= 0 else 'low'}">{'中' if tdx_in >= 0 else '弱'}</span>
      <span class="fname">消息面</span><span>无新催化</span><span class="fweight">15%</span><span class="fscore">8</span><span class="ftag ftag-low">弱</span>
      <span class="fname">筹码</span><span>获利盘回吐</span><span class="fweight">10%</span><span class="fscore">3</span><span class="ftag ftag-low">弱</span>
      <span class="fname">板块</span><span>板块跌{s['hy_zaf']}%</span><span class="fweight">8%</span><span class="fscore">2</span><span class="ftag ftag-low">弱</span>
      <span class="fname">宏观</span><span>-</span><span class="fweight">2%</span><span class="fscore">1</span><span class="ftag ftag-low">-</span>
    </div>
    <div class="score-summary">
      <span class="score-big">{s['score']}</span>
      <span class="score-label">
        <strong>{s['score_category']}</strong><br>
        各因子加权：技12+量10+资{14 if tdx_in >= 0 else 6}+消8+筹3+板2+宏1
      </span>
    </div>
    <div class="score-legend">
      <span class="dot" style="background:#1d9e75;"></span><span>80-100</span><span>强多</span><span>主动买入信号，高仓位持有</span>
      <span class="dot" style="background:#4caf50;"></span><span>65-79</span><span>偏多</span><span>温和看涨，逢低可加小仓</span>
      <span class="dot" style="background:#e67e22;"></span><span>50-64</span><span>震多</span><span>震荡偏多，持有观望</span>
      <span class="dot" style="background:#e67e22;"></span><span>40-49</span><span class="active">震空</span><span>震荡偏空，减仓或观望</span>
      <span class="dot" style="background:#e67e22;"></span><span>30-39</span><span>偏空</span><span>弱势下行，不建议加仓</span>
      <span class="dot" style="background:#d85a30;"></span><span>15-29</span><span>强空</span><span>明确卖出信号，建议减仓</span>
      <span class="dot" style="background:#888;"></span><span>0-14</span><span>崩盘</span><span>极端弱势，考虑止损</span>
    </div>
  </div>

  <div class="advice-section">
    <div class="section-title">🎯 下午操作建议</div>
    <div class="advice-row">
      <span class="advice-tag tag-hold">当前持仓</span>
      <span style="font-size:12px;color:#636366;line-height:1.6;">浮盈持有，不急于操作。{s['score_category']}评级下以观望为主。关键价位关注{s['low']}支撑和{s['high']}压力。</span>
    </div>
    <div class="advice-row">
      <span class="advice-tag tag-buy">加仓条件</span>
      <span style="font-size:12px;color:#636366;line-height:1.6;">{s['pred_bull_trigger']}。若满足，轻仓试多，止损设{s['low']}。</span>
    </div>
    <div class="advice-row">
      <span class="advice-tag tag-hold">观望条件</span>
      <span style="font-size:12px;color:#636366;line-height:1.6;">下午若在{s['pred_base_range']}区间窄幅震荡，维持观望。</span>
    </div>
    <div class="advice-row">
      <span class="advice-tag tag-sell">减仓条件</span>
      <span style="font-size:12px;color:#636366;line-height:1.6;">{s['pred_bear_trigger']}，考虑减仓，止损设{s['support'][-1]}。</span>
    </div>
  </div>

  <div class="section-block">
    <div class="section-title">📊 关键价位</div>
    <div class="level-grid">
      {sup_html}
      <div class="level-box"><div class="level-label">持仓成本</div><div class="level-value cost">{s['cost']}</div></div>
      <div class="level-box"><div class="level-label">PE(TTM)</div><div class="level-value">{s['pe_ttm']}</div></div>
    </div>
  </div>

  <div class="confidence-block">
    <div class="conf-title">🧠 模型自评</div>
    <div class="conf-row">
      置信度: <strong>{s['confidence']}/100</strong> · 评分{score}分({s['score_category']})<br>
      数据源: tdx_quotes ProInfo (InOut/InOutHB/Wtb) + westock-data quote/minute/asfund<br>
      时间: {s['date']} 午间复盘 · 预测下午走势<br>
    </div>
  </div>

  <div class="risk-block">
    <div class="risk-title">⚠️ 风险提示</div>
    {risk_html}
    <div style="font-size:9px;color:#aeaeb2;margin-top:8px;">
      以上内容为AI分析，不构成投资建议。股市有风险，投资需谨慎。数据来源：tdx_connector + westock-data。
    </div>
  </div>
</div>
</body>
</html>'''
    return html

# Write all three cards
for key, s in stocks.items():
    html = gen_card(s)
    filepath = f'/Users/xtjin/stock-dashboard/{key}_card.html'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Written: {filepath} ({len(html)} bytes)")

print("\nAll 3 midday cards generated successfully!")

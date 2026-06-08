#!/usr/bin/env python3
"""Update index.json for all 3 stocks with 2026-06-08 morning session data"""
import json

stocks = [
    {
        "file": "/Users/xtjin/stock-dashboard/data/xinfengming/index.json",
        "card_html": "cards/2026-06-08-midday.html",
        "card_screenshot": "cards/2026-06-08-midday.png",
        "session": {
            "date": "2026-06-08",
            "session": "morning",
            "price": 19.54,
            "prev_close": 20.33,
            "change": -0.79,
            "change_percent": -3.89,
            "open": 19.61,
            "high": 20.25,
            "low": 19.45,
            "volume": 112051,
            "amount": 221022327,
            "turnover_rate": 0.67,
            "volume_ratio": 0.66,
            "fund_flow": {
                "tdx_inout": 19131696,
                "tdx_inout_hb": 35460820,
                "tdx_wtb": 3.98,
                "inside": 52063,
                "outside": 59988,
                "main_net_flow": 31005812,
                "jumbo_net_flow": 28269898,
                "mid_net_flow": -34843536,
                "small_net_flow": 3737724,
                "main_net_5d": 146744901,
                "main_net_20d": 201383811,
                "margin_balance": 365967128,
                "margin_dod": 8.95,
                "short_balance": 5938393,
                "short_dod": 33.91
            },
            "sanshou_score": 48,
            "score_category": "震空",
            "predictions": {
                "base": {
                    "probability": 55,
                    "description": "缩量区间震荡消化低开",
                    "range": "19.20-19.80",
                    "close_estimate": 19.50
                },
                "bull": {
                    "probability": 20,
                    "trigger": "13:00放量站稳19.80+化纤板块翻红",
                    "target": "20.00-20.25"
                },
                "bear": {
                    "probability": 25,
                    "trigger": "缩量跌破19.45+化纤继续走弱",
                    "target": "19.00-19.23"
                }
            },
            "confidence": 55,
            "key_levels": {
                "support": [19.45, 19.23, 18.95, 17.54],
                "resistance": [20.25, 20.33, 20.80, 21.12],
                "cost": 18.95
            },
            "card_html": "cards/2026-06-08-midday.html",
            "card_screenshot": "cards/2026-06-08-midday.png",
            "tdx_connected": True
        }
    },
    {
        "file": "/Users/xtjin/stock-dashboard/data/zhongxingtongxun/index.json",
        "card_html": "cards/2026-06-08-midday.html",
        "card_screenshot": "cards/2026-06-08-midday.png",
        "session": {
            "date": "2026-06-08",
            "session": "morning",
            "price": 37.12,
            "prev_close": 39.13,
            "change": -2.01,
            "change_percent": -5.14,
            "open": 38.02,
            "high": 39.00,
            "low": 37.08,
            "volume": 2035433,
            "amount": 7750210198,
            "turnover_rate": 5.05,
            "volume_ratio": 1.58,
            "fund_flow": {
                "tdx_inout": -1375662080,
                "tdx_inout_hb": -1063018750,
                "tdx_wtb": 88.55,
                "inside": 1142963,
                "outside": 892470,
                "main_net_flow": -1222005694,
                "jumbo_net_flow": -1216650272,
                "mid_net_flow": 169003020,
                "small_net_flow": 1053002674,
                "main_net_5d": 3186337124,
                "main_net_20d": 77682698,
                "margin_balance": 10778422446,
                "margin_dod": 4.09,
                "block_trade": {
                    "type": "协议交易",
                    "price": 34.00,
                    "value": 3400000,
                    "discount": 6.64,
                    "buy_dept": "国泰海通东营府前大街",
                    "sell_dept": "中信建投北京朝外大街"
                }
            },
            "sanshou_score": 38,
            "score_category": "偏空",
            "predictions": {
                "base": {
                    "probability": 50,
                    "description": "放量下跌后低位震荡",
                    "range": "36.50-38.00",
                    "close_estimate": 37.20
                },
                "bull": {
                    "probability": 20,
                    "trigger": "13:00放量站稳37.50+通信板块反弹",
                    "target": "38.50-39.00"
                },
                "bear": {
                    "probability": 30,
                    "trigger": "缩量跌破37.08+主力继续净流出>5亿",
                    "target": "36.00-36.50"
                }
            },
            "confidence": 65,
            "key_levels": {
                "support": [37.08, 36.50, 35.79, 35.50],
                "resistance": [38.50, 39.00, 39.13, 41.30],
                "cost": 35.79
            },
            "card_html": "cards/2026-06-08-midday.html",
            "card_screenshot": "cards/2026-06-08-midday.png",
            "tdx_connected": True
        }
    },
    {
        "file": "/Users/xtjin/stock-dashboard/data/huagongkeji/index.json",
        "card_html": "cards/2026-06-08-midday.html",
        "card_screenshot": "cards/2026-06-08-midday.png",
        "session": {
            "date": "2026-06-08",
            "session": "morning",
            "price": 150.51,
            "prev_close": 157.20,
            "change": -6.69,
            "change_percent": -4.26,
            "open": 146.00,
            "high": 154.78,
            "low": 146.00,
            "volume": 444146,
            "amount": 6657604839,
            "turnover_rate": 4.42,
            "volume_ratio": 1.03,
            "fund_flow": {
                "tdx_inout": -356314624,
                "tdx_inout_hb": -522622208,
                "tdx_wtb": 41.59,
                "inside": 227011,
                "outside": 217135,
                "main_net_flow": -552002741,
                "jumbo_net_flow": -437959699,
                "mid_net_flow": 258498427,
                "small_net_flow": 293504313,
                "main_net_5d": -253083292,
                "main_net_20d": -10758959487,
                "margin_balance": 11220943604,
                "margin_dod": 1.29,
                "short_balance": 23455498,
                "short_dod": 11.19,
                "block_trade": {
                    "type": "协议交易",
                    "price": 156.31,
                    "value": 6533800,
                    "discount": 0.0,
                    "buy_dept": "机构专用",
                    "sell_dept": "华泰证券福建分公司"
                }
            },
            "sanshou_score": 45,
            "score_category": "震空",
            "predictions": {
                "base": {
                    "probability": 50,
                    "description": "V反后回落震荡整理",
                    "range": "148.00-153.00",
                    "close_estimate": 150.00
                },
                "bull": {
                    "probability": 20,
                    "trigger": "13:00放量站稳151.50+CPO板块翻红",
                    "target": "154.00-155.00"
                },
                "bear": {
                    "probability": 30,
                    "trigger": "缩量跌破150+主力继续净流出>3亿",
                    "target": "145.00-147.00"
                }
            },
            "confidence": 52,
            "key_levels": {
                "support": [150.00, 146.00, 152.00, 154.24],
                "resistance": [154.78, 157.20, 165.87, 175.80],
                "cost": 154.24
            },
            "card_html": "cards/2026-06-08-midday.html",
            "card_screenshot": "cards/2026-06-08-midday.png",
            "tdx_connected": True
        }
    }
]

for stock in stocks:
    with open(stock['file'], 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check if session already exists
    session_exists = False
    for s in data['sessions']:
        if s['date'] == '2026-06-08' and s['session'] == 'morning':
            session_exists = True
            break
    
    if not session_exists:
        data['sessions'].append(stock['session'])
        with open(stock['file'], 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated: {stock['file']} (added morning session)")
    else:
        print(f"Skipped: {stock['file']} (morning session already exists)")

# Also copy HTML cards to data dirs
import shutil
shutil.copy2('/Users/xtjin/stock-dashboard/xinfengming_card.html', '/Users/xtjin/stock-dashboard/data/xinfengming/cards/2026-06-08-midday.html')
shutil.copy2('/Users/xtjin/stock-dashboard/zhongxingtongxun_card.html', '/Users/xtjin/stock-dashboard/data/zhongxingtongxun/cards/2026-06-08-midday.html')
shutil.copy2('/Users/xtjin/stock-dashboard/huagongkeji_card.html', '/Users/xtjin/stock-dashboard/data/huagongkeji/cards/2026-06-08-midday.html')
print("HTML cards copied to data dirs.")

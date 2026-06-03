/* ============================================================
   main.js — 首页仪表盘逻辑
   ============================================================ */

(function () {
  'use strict';

  // 三只股票配置
  var STOCKS = [
    { key: 'xinfengming', name: '新凤鸣', code: 'sh603225', page: 'pages/xinfengming.html' },
    { key: 'huagongkeji', name: '华工科技', code: 'sz000988', page: 'pages/huagongkeji.html' },
    { key: 'zhongxing', name: '中兴通讯', code: 'sz000063', page: 'pages/zhongxing.html' }
  ];

  /**
   * 设置今日日期
   */
  function setTodayDate() {
    var now = new Date();
    var yyyy = now.getFullYear();
    var mm = String(now.getMonth() + 1).padStart(2, '0');
    var dd = String(now.getDate()).padStart(2, '0');
    var weekdays = ['日', '一', '二', '三', '四', '五', '六'];
    var weekday = weekdays[now.getDay()];
    var dateStr = yyyy + '年' + mm + '月' + dd + '日 星期' + weekday;

    var el = document.getElementById('today-date');
    if (el) el.textContent = dateStr;
  }

  /**
   * 加载并渲染单个股票概览卡片
   */
  function loadStockCard(stockConfig, containerId) {
    var container = document.getElementById(containerId);
    if (!container) return;

    // 显示加载状态
    container.innerHTML = '<div class="no-data" style="min-height:120px;">加载中...</div>';

    getLatestData(stockConfig.key).then(function (data) {
      if (!data || !data.latest) {
        container.innerHTML = '<div class="no-data" style="min-height:120px;">暂无数据</div>';
        return;
      }

      var latest = data.latest;
      var price = latest.price;
      var score = latest.sanshou_score;
      var flow = latest.fund_flow;

      var changeClass = 'change-flat';
      var changeSign = '';
      if (price.change_pct > 0) {
        changeClass = 'change-up';
        changeSign = '+';
      } else if (price.change_pct < 0) {
        changeClass = 'change-down';
      }

      var mainNetSign = flow.main_net >= 0 ? '流入' : '流出';
      var mainNetAbs = Math.abs(flow.main_net);
      var mainNetStr;
      if (mainNetAbs >= 100000000) {
        mainNetStr = (mainNetAbs / 100000000).toFixed(2) + '亿';
      } else {
        mainNetStr = (mainNetAbs / 10000).toFixed(0) + '万';
      }

      var html = '<div class="stock-card" onclick="window.location.href=\'' + stockConfig.page + '\'">' +
        '<div class="stock-name">' + data.stock + '</div>' +
        '<div class="stock-code">' + data.code + '</div>' +
        '<div class="stock-price">' + price.close.toFixed(2) + '</div>' +
        '<div class="stock-change ' + changeClass + '">' + changeSign + price.change_pct.toFixed(2) + '%</div>' +
        '<div class="stock-meta">' +
          '<span>📊 三寿评分: <strong>' + score.total + '</strong> (' + (score.signal || '-') + ')</span>' +
          '<span>💰 主力' + mainNetSign + ': <strong>' + mainNetStr + '</strong></span>' +
        '</div>' +
        '<div class="stock-meta" style="margin-top:4px;">' +
          '<span>📅 ' + latest.date + '</span>' +
          '<span>📈 准确率: ' + (data.accuracy.composite_rate || 0) + '%</span>' +
        '</div>' +
      '</div>';

      container.innerHTML = html;
    }).catch(function () {
      container.innerHTML = '<div class="no-data" style="min-height:120px;">暂无数据</div>';
    });
  }

  /**
   * 初始化首页
   */
  function initHomepage() {
    // 加载三只股票卡片
    loadStockCard(STOCKS[0], 'stock-card-0');
    loadStockCard(STOCKS[1], 'stock-card-1');
    loadStockCard(STOCKS[2], 'stock-card-2');

    // 启动实时行情轮询
    if (typeof startQuotePolling === 'function') {
      startQuotePolling(10000);
    }

    // 每5秒更新卡片价格
    setInterval(updateHomeCardPrices, 5000);
  }

  function updateHomeCardPrices() {
    if (typeof LIVE_QUOTES === 'undefined') return;
    var cards = document.querySelectorAll('.stock-card');
    if (cards.length < 3) return;

    STOCKS.forEach(function(stock, i) {
      var q = LIVE_QUOTES[stock.key];
      if (!q || q.price === null) return;
      var priceEl = cards[i].querySelector('.stock-price');
      var chgEl = cards[i].querySelector('.stock-change');
      if (priceEl) priceEl.textContent = q.price.toFixed(2);
      if (chgEl) {
        var sign = q.change >= 0 ? '+' : '';
        chgEl.textContent = sign + q.change.toFixed(2) + '%';
        chgEl.className = 'stock-change ' + (q.change >= 0 ? 'change-up' : 'change-down');
      }
    });
  }

  // DOM 加载完成后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHomepage);
  } else {
    initHomepage();
  }
})();

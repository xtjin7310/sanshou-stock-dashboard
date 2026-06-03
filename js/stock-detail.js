/* ============================================================
   stock-detail.js — 个股详情页逻辑
   依赖: charts.js, data-loader.js
   ============================================================ */

// 个股配置（页面内定义）
var STOCK_CONFIG = {
  xinfengming: { key: 'xinfengming', stock: '新凤鸣', code: 'sh603225' },
  huagongkeji: { key: 'huagongkeji', stock: '华工科技', code: 'sz000988' },
  zhongxing: { key: 'zhongxing', stock: '中兴通讯', code: 'sz000063' }
};

/**
 * 获取当前股票标识
 */
function getCurrentStock() {
  // 从 body data 属性读取
  var bodyStock = document.body.getAttribute('data-stock');
  if (bodyStock) return bodyStock;

  // 从 URL 路径推断
  var path = window.location.pathname;
  if (path.indexOf('xinfengming') !== -1) return 'xinfengming';
  if (path.indexOf('huagongkeji') !== -1) return 'huagongkeji';
  if (path.indexOf('zhongxing') !== -1) return 'zhongxing';

  return 'xinfengming';
}

/**
 * 获取默认日期范围（最近30天）
 */
function getDefaultDateRange() {
  var end = new Date();
  var start = new Date();
  start.setDate(start.getDate() - 30);

  var fmt = function (d) {
    var yyyy = d.getFullYear();
    var mm = String(d.getMonth() + 1).padStart(2, '0');
    var dd = String(d.getDate()).padStart(2, '0');
    return yyyy + '-' + mm + '-' + dd;
  };

  return {
    start: fmt(start),
    end: fmt(end)
  };
}

/**
 * 初始化个股页面
 */
function initStockDetail() {
  var stock = getCurrentStock();
  var config = STOCK_CONFIG[stock];
  if (!config) return;

  // 设置页面标题
  document.title = config.stock + '(' + config.code + ') - 三股复盘';

  // 设置股票信息
  var nameEl = document.getElementById('stock-name');
  var codeEl = document.getElementById('stock-code');
  if (nameEl) nameEl.textContent = config.stock;
  if (codeEl) codeEl.textContent = config.code;

  // 默认日期范围
  var range = getDefaultDateRange();
  var startInput = document.getElementById('date-start');
  var endInput = document.getElementById('date-end');
  if (startInput) startInput.value = range.start;
  if (endInput) endInput.value = range.end;

  // 默认 session = all（显示所有时段）
  var currentSession = 'all';

  // 首次加载
  updateAllCharts(stock, range.start, range.end, currentSession);

  // 午间/盘后切换按钮
  var btnAll = document.getElementById('btn-session-all');
  var btnMorning = document.getElementById('btn-session-morning');
  var btnAfternoon = document.getElementById('btn-session-afternoon');

  function setActiveSessionBtn(activeBtn) {
    [btnAll, btnMorning, btnAfternoon].forEach(function (btn) {
      if (btn) btn.classList.remove('btn-active');
    });
    if (activeBtn) activeBtn.classList.add('btn-active');
  }

  if (btnAll) {
    btnAll.addEventListener('click', function () {
      currentSession = 'all';
      setActiveSessionBtn(btnAll);
      updateAllCharts(stock, startInput.value, endInput.value, currentSession);
    });
  }
  if (btnMorning) {
    btnMorning.addEventListener('click', function () {
      currentSession = 'morning';
      setActiveSessionBtn(btnMorning);
      updateAllCharts(stock, startInput.value, endInput.value, currentSession);
    });
  }
  if (btnAfternoon) {
    btnAfternoon.addEventListener('click', function () {
      currentSession = 'afternoon';
      setActiveSessionBtn(btnAfternoon);
      updateAllCharts(stock, startInput.value, endInput.value, currentSession);
    });
  }

  // 默认激活"全部"
  if (btnAll) btnAll.classList.add('btn-active');

  // 日期范围「应用」按钮
  var applyBtn = document.getElementById('btn-apply-date');
  if (applyBtn) {
    applyBtn.addEventListener('click', function () {
      var startVal = startInput ? startInput.value : '';
      var endVal = endInput ? endInput.value : '';
      destroyAllCharts();
      updateAllCharts(stock, startVal, endVal, currentSession);
    });
  }

  // 底部导航（移动端）
  initBottomNav(stock);
}

/**
 * 底部导航（移动端）
 */
function initBottomNav(currentStock) {
  var stocks = ['xinfengming', 'huagongkeji', 'zhongxing'];
  var pages = {
    xinfengming: 'xinfengming.html',
    huagongkeji: 'huagongkeji.html',
    zhongxing: 'zhongxing.html'
  };
  var names = {
    xinfengming: '新凤鸣',
    huagongkeji: '华工科技',
    zhongxing: '中兴通讯'
  };

  var nav = document.getElementById('bottom-nav');
  if (!nav) return;

  var html = '<div class="bottom-nav-inner">';
  stocks.forEach(function (s) {
    var activeClass = s === currentStock ? ' active' : '';
    html += '<button class="bottom-nav-item' + activeClass + '" onclick="window.location.href=\'' + pages[s] + '\'">' +
      '<span class="nav-icon">📈</span>' +
      '<span>' + names[s] + '</span>' +
    '</button>';
  });
  html += '</div>';

  nav.innerHTML = html;
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function () {
  initStockDetail();
});

// 暴露 getCurrentStock 到全局
window.getCurrentStock = getCurrentStock;

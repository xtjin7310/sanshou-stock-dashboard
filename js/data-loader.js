/* ============================================================
   data-loader.js — 数据加载与图表更新
   依赖: charts.js (需要先加载)
   ============================================================ */

/**
 * 获取数据目录的基础路径
 * 自动检测当前页面位置（根目录 / pages/）
 */
function getDataBasePath() {
  var path = window.location.pathname;
  if (path.indexOf('/pages/') !== -1) {
    return '../data/';
  }
  return 'data/';
}

/**
 * 加载股票数据
 * @param {string} stock - 股票标识 (xinfengming|huagongkeji|zhongxing)
 * @param {string} startDate - 起始日期 YYYY-MM-DD
 * @param {string} endDate - 结束日期 YYYY-MM-DD
 * @returns {Promise<Object>} { stock, code, sessions, accuracy }
 */
function loadStockData(stock, startDate, endDate) {
  var url = getDataBasePath() + stock + '/index.json';

  return fetch(url)
    .then(function (response) {
      if (!response.ok) {
        throw new Error('数据加载失败: HTTP ' + response.status);
      }
      return response.json();
    })
    .then(function (data) {
      // 按日期范围过滤
      var filteredSessions = data.sessions.filter(function (s) {
        if (!s.date) return false;
        if (startDate && s.date < startDate) return false;
        if (endDate && s.date > endDate) return false;
        return true;
      });

      // 按日期排序
      filteredSessions.sort(function (a, b) {
        if (a.date < b.date) return -1;
        if (a.date > b.date) return 1;
        return 0;
      });

      return {
        stock: data.stock,
        code: data.code,
        sessions: filteredSessions,
        accuracy: data.accuracy || {}
      };
    })
    .catch(function (err) {
      console.error('加载数据失败:', stock, err);
      return {
        stock: '',
        code: '',
        sessions: [],
        accuracy: {},
        error: err.message
      };
    });
}

/**
 * 获取最新一条数据（用于首页概览卡片）
 * @param {string} stock - 股票标识
 * @returns {Promise<Object|null>}
 */
function getLatestData(stock) {
  var url = getDataBasePath() + stock + '/index.json';

  return fetch(url)
    .then(function (response) {
      if (!response.ok) throw new Error('数据加载失败');
      return response.json();
    })
    .then(function (data) {
      if (!data.sessions || data.sessions.length === 0) return null;

      // 按日期降序排列，取最新
      var sorted = data.sessions.slice().sort(function (a, b) {
        if (a.date < b.date) return 1;
        if (a.date > b.date) return -1;
        return 0;
      });

      return {
        stock: data.stock,
        code: data.code,
        latest: sorted[0],
        accuracy: data.accuracy || {}
      };
    })
    .catch(function (err) {
      console.error('getLatestData error:', stock, err);
      return null;
    });
}

/**
 * 更新所有图表
 * @param {string} stock - 股票标识
 * @param {string} startDate - 起始日期
 * @param {string} endDate - 结束日期
 * @param {string} sessionFilter - 时段筛选 'all'|'morning'|'afternoon'
 */
function updateAllCharts(stock, startDate, endDate, sessionFilter) {
  sessionFilter = sessionFilter || 'all';

  loadStockData(stock, startDate, endDate).then(function (data) {
    if (data.error || data.sessions.length === 0) {
      showChartError('数据加载失败或无数据');
      return;
    }

    // 按 session 过滤
    var filtered = data.sessions;
    if (sessionFilter !== 'all') {
      filtered = data.sessions.filter(function (s) {
        return s.session === sessionFilter;
      });
    }

    if (filtered.length === 0) {
      showChartError('所选时段无数据');
      return;
    }

    // 清除错误状态
    clearChartErrors();

    // 更新各图表
    createPriceChart('chart-price', filtered);
    createChangeChart('chart-change', filtered);
    createVolumeChart('chart-volume', filtered);
    // 从复选框读取选中维度
    var fundDims = {};
    var cbs = document.querySelectorAll('.fund-cb');
    if (cbs.length > 0) { cbs.forEach(function(cb){ fundDims[cb.value] = cb.checked; }); }
    else { fundDims = { main: true, super: true, large: false, medium: false, small: false, margin: false, short: false }; }
    createFundFlowChart('chart-fundflow', filtered, fundDims);
    createScoreChart('chart-score', filtered);
    createKeyLevelChart('chart-keylevel', filtered);

    // 更新三寿因子条形图
    updateFactorBars(filtered[filtered.length - 1]);

    // 更新预测准确度
    updateAccuracyTracking(data.accuracy);

    // 更新卡片画廊
    updateCardGallery(filtered);

    // 更新顶部价格信息
    updateTopBarPrice(filtered[filtered.length - 1]);
  });
}

/**
 * 显示图表错误信息
 */
function showChartError(msg) {
  var containers = document.querySelectorAll('.chart-container');
  containers.forEach(function (container) {
    // 清除 canvas
    var canvas = container.querySelector('canvas');
    if (canvas) {
      var ctx = canvas.getContext('2d');
      if (ctx) ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    // 添加错误提示
    var existing = container.querySelector('.chart-error');
    if (!existing) {
      var errEl = document.createElement('div');
      errEl.className = 'chart-error';
      errEl.textContent = msg;
      container.appendChild(errEl);
    }
  });
}

/**
 * 清除图表错误状态
 */
function clearChartErrors() {
  var errors = document.querySelectorAll('.chart-error');
  errors.forEach(function (el) { el.remove(); });
}

/**
 * 更新三寿7因子水平条形图
 */
function updateFactorBars(latestSession) {
  var container = document.getElementById('factor-bars');
  if (!container || !latestSession) return;

  var factors = latestSession.sanshou_score;
  var factorNames = {
    technical: '技术',
    volume_price: '量价',
    fund: '资金',
    news: '消息',
    chip: '筹码',
    sector: '板块',
    macro: '宏观'
  };

  var getFactorColor = function (score) {
    if (score >= 85) return '#0F6E56';
    if (score >= 70) return '#1d9e75';
    if (score >= 55) return '#378add';
    if (score >= 40) return '#aeaeb2';
    if (score >= 25) return '#e8923f';
    return '#d85a30';
  };

  var html = '';
  var order = ['technical', 'volume_price', 'fund', 'news', 'chip', 'sector', 'macro'];
  order.forEach(function (key) {
    var val = factors[key] || 0;
    var name = factorNames[key] || key;
    html += '<div class="factor-bar-row">' +
      '<span class="factor-bar-label">' + name + '</span>' +
      '<div class="factor-bar-track">' +
        '<div class="factor-bar-fill" style="width:' + val + '%; background:' + getFactorColor(val) + ';"></div>' +
      '</div>' +
      '<span class="factor-bar-value">' + val + '</span>' +
    '</div>';
  });

  container.innerHTML = html;
}

/**
 * 更新预测准确度追踪
 */
function updateAccuracyTracking(accuracy) {
  if (!accuracy) return;

  var totalEl = document.getElementById('acc-total');
  var directionEl = document.getElementById('acc-direction');
  var compositeEl = document.getElementById('acc-composite');
  var progressEl = document.getElementById('acc-progress');
  var tableBody = document.getElementById('prediction-table-body');

  if (totalEl) totalEl.textContent = accuracy.total || 0;
  if (directionEl) directionEl.textContent = accuracy.direction_correct || 0;

  var compositeRate = accuracy.composite_rate || 0;
  if (compositeEl) compositeEl.textContent = compositeRate + '%';
  if (progressEl) progressEl.style.width = compositeRate + '%';

  // 最近预测记录表格
  if (tableBody && accuracy.recent_predictions) {
    var rows = '';
    var preds = accuracy.recent_predictions.slice().reverse();
    preds.forEach(function (p) {
      rows += '<tr>' +
        '<td>' + p.date + '</td>' +
        '<td>' + p.direction_pred + '</td>' +
        '<td>' + p.direction_actual + '</td>' +
        '<td class="' + (p.correct ? 'correct' : 'incorrect') + '">' + (p.correct ? '✓' : '✗') + '</td>' +
      '</tr>';
    });
    tableBody.innerHTML = rows;
  }
}

/**
 * 更新卡片画廊
 */
function updateCardGallery(sessions) {
  var gallery = document.getElementById('card-gallery');
  if (!gallery) return;

  // 按日期分组，倒序
  var dateMap = {};
  sessions.forEach(function (s) {
    if (!dateMap[s.date]) dateMap[s.date] = [];
    dateMap[s.date].push(s);
  });

  var dates = Object.keys(dateMap).sort().reverse();

  if (dates.length === 0) {
    gallery.innerHTML = '<div class="no-data">暂无复盘卡片</div>';
    return;
  }

  var html = '';
  dates.forEach(function (date) {
    var daySessions = dateMap[date];
    html += '<div class="card-gallery-row">';
    html += '<div class="card-gallery-date">' + date.slice(5) + '</div>';
    html += '<div class="card-gallery-thumbs">';

    daySessions.forEach(function (s) {
      var imgSrc = getDataBasePath() + getCurrentStock() + '/' + (s.card_screenshot || '');
      var label = s.session === 'morning' ? '午间' : '盘后';
      html += '<img class="card-thumb" ' +
        'src="' + imgSrc + '" ' +
        'alt="' + date + ' ' + label + '" ' +
        'title="' + date + ' ' + label + '" ' +
        'onerror="this.style.display=\'none\'" ' +
        'onclick="openImageModal(\'' + imgSrc + '\', \'' + date + ' ' + label + '\')" ' +
        'loading="lazy">';
    });

    html += '</div></div>';
  });

  gallery.innerHTML = html;
}

/**
 * 更新顶部栏价格
 */
function updateTopBarPrice(latestSession) {
  if (!latestSession) return;
  var priceEl = document.getElementById('top-price');
  var changeEl = document.getElementById('top-change');
  if (priceEl) priceEl.textContent = latestSession.price.close.toFixed(2);
  if (changeEl) {
    var pct = latestSession.price.change_pct;
    changeEl.textContent = (pct >= 0 ? '+' : '') + pct.toFixed(2) + '%';
    changeEl.className = 'change-display ' + (pct >= 0 ? 'change-up' : 'change-down');
  }
}

/**
 * Modal 弹窗
 */
function openImageModal(src, title) {
  var overlay = document.getElementById('image-modal');
  var img = document.getElementById('modal-image');
  if (!overlay || !img) return;

  img.src = src;
  img.alt = title;
  overlay.classList.add('active');
}

function closeImageModal() {
  var overlay = document.getElementById('image-modal');
  if (overlay) overlay.classList.remove('active');
}

// 点击遮罩关闭
document.addEventListener('DOMContentLoaded', function () {
  var modal = document.getElementById('image-modal');
  if (modal) {
    modal.addEventListener('click', function (e) {
      if (e.target === modal) {
        closeImageModal();
      }
    });
  }

  // ESC 关闭
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeImageModal();
    }
  });
});

// 全局函数暴露
window.openImageModal = openImageModal;
window.closeImageModal = closeImageModal;

/* ============================================================
   charts.js — Chart.js 图表封装工厂
   依赖: Chart.js v4 (CDN)
   ============================================================ */

// 全局图表实例管理
var chartInstances = {};

/**
 * 销毁指定 key 下的旧图表实例
 * @param {string} key - 图表标识
 */
function destroyChart(key) {
  if (chartInstances[key]) {
    chartInstances[key].destroy();
    delete chartInstances[key];
  }
}

/**
 * 销毁所有图表实例
 */
function destroyAllCharts() {
  Object.keys(chartInstances).forEach(function (key) {
    if (chartInstances[key]) {
      chartInstances[key].destroy();
    }
  });
  chartInstances = {};
}

/**
 * 统一默认配置
 */
function getDefaultOptions() {
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 400
    },
    plugins: {
      legend: {
        labels: {
          font: { family: getComputedStyle(document.body).fontFamily, size: 12 },
          usePointStyle: true,
          pointStyleWidth: 8,
          padding: 16
        }
      },
      tooltip: {
        titleFont: { family: getComputedStyle(document.body).fontFamily, size: 13 },
        bodyFont: { family: getComputedStyle(document.body).fontFamily, size: 12 },
        backgroundColor: 'rgba(29, 29, 31, 0.92)',
        titleColor: '#ffffff',
        bodyColor: '#e5e5ea',
        cornerRadius: 8,
        padding: 12,
        displayColors: true,
        usePointStyle: true
      }
    },
    scales: {
      x: {
        ticks: {
          font: { family: getComputedStyle(document.body).fontFamily, size: 11 },
          color: '#6e6e73'
        },
        grid: {
          color: '#f0f0f2',
          drawBorder: false
        }
      },
      y: {
        ticks: {
          font: { family: getComputedStyle(document.body).fontFamily, size: 11 },
          color: '#6e6e73'
        },
        grid: {
          color: '#f0f0f2',
          drawBorder: false
        }
      }
    },
    interaction: {
      mode: 'index',
      intersect: false
    }
  };
}

/**
 * 格式化金额为中文单位
 */
function formatAmountCN(value) {
  if (Math.abs(value) >= 100000000) {
    return (value / 100000000).toFixed(2) + '亿';
  }
  if (Math.abs(value) >= 10000) {
    return (value / 10000).toFixed(0) + '万';
  }
  return value.toString();
}

/**
 * 区块1：价格走势图
 * @param {string} canvasId - canvas 元素 ID
 * @param {Array} sessions - 数据数组
 */
function createPriceChart(canvasId, sessions) {
  destroyChart('price');

  var canvas = document.getElementById(canvasId);
  if (!canvas) return;

  var ctx = canvas.getContext('2d');
  var dates = sessions.map(function (s) { return s.date.slice(5); }); // MM-DD
  var afternoonPrices = sessions.map(function (s) { return s.session === 'afternoon' ? s.price.close : null; });
  var morningPrices = sessions.map(function (s) { return s.session === 'morning' ? s.price.close : null; });

  var datasets = [];

  // 盘后：实线
  if (afternoonPrices.some(function (v) { return v !== null; })) {
    datasets.push({
      label: '盘后收盘价',
      data: afternoonPrices,
      borderColor: '#378add',
      backgroundColor: 'rgba(55, 138, 221, 0.08)',
      borderWidth: 2,
      pointRadius: 3,
      pointBackgroundColor: '#378add',
      tension: 0.3,
      fill: false,
      spanGaps: false
    });
  }

  // 午间：虚线
  if (morningPrices.some(function (v) { return v !== null; })) {
    datasets.push({
      label: '午间收盘价',
      data: morningPrices,
      borderColor: '#378add',
      backgroundColor: 'rgba(55, 138, 221, 0.04)',
      borderWidth: 2,
      borderDash: [6, 3],
      pointRadius: 3,
      pointBackgroundColor: '#378add',
      tension: 0.3,
      fill: false,
      spanGaps: false
    });
  }

  var options = getDefaultOptions();
  options.scales = Object.assign({}, options.scales, {
    y: {
      title: { display: true, text: '元', font: { size: 12 } },
      ticks: { callback: function (v) { return v.toFixed(2); } }
    }
  });

  chartInstances['price'] = new Chart(ctx, {
    type: 'line',
    data: { labels: dates, datasets: datasets },
    options: options
  });
}

/**
 * 区块2：涨跌幅走势图
 * @param {string} canvasId
 * @param {Array} sessions
 */
function createChangeChart(canvasId, sessions) {
  destroyChart('change');

  var canvas = document.getElementById(canvasId);
  if (!canvas) return;

  var ctx = canvas.getContext('2d');
  var dates = sessions.map(function (s) { return s.date.slice(5); });
  var afternoonChanges = sessions.map(function (s) {
    return s.session === 'afternoon' ? parseFloat(s.price.change_pct.toFixed(2)) : null;
  });
  var morningChanges = sessions.map(function (s) {
    return s.session === 'morning' ? parseFloat(s.price.change_pct.toFixed(2)) : null;
  });

  function changeColor(val) {
    if (val === null) return 'transparent';
    return val >= 0 ? '#d85a30' : '#1d9e75';
  }

  var datasets = [
    {
      label: '盘后涨跌幅',
      data: afternoonChanges,
      backgroundColor: afternoonChanges.map(changeColor),
      borderColor: afternoonChanges.map(changeColor),
      borderWidth: 0,
      borderRadius: 4,
      order: 2
    },
    {
      label: '午间涨跌幅',
      data: morningChanges,
      backgroundColor: morningChanges.map(changeColor),
      borderColor: morningChanges.map(changeColor),
      borderWidth: 0,
      borderRadius: 4,
      order: 2
    }
  ];

  var options = getDefaultOptions();
  options.scales = Object.assign({}, options.scales, {
    y: {
      title: { display: true, text: '%', font: { size: 12 } },
      ticks: { callback: function (v) { return v.toFixed(1) + '%'; } }
    }
  });
  options.plugins.tooltip.callbacks = {
    label: function (ctx) {
      var val = ctx.raw;
      if (val === null) return ctx.dataset.label + ': 无数据';
      return ctx.dataset.label + ': ' + (val >= 0 ? '+' : '') + val.toFixed(2) + '%';
    }
  };

  chartInstances['change'] = new Chart(ctx, {
    type: 'bar',
    data: { labels: dates, datasets: datasets },
    options: options
  });
}

/**
 * 区块3：量能走势图（双Y轴）
 * @param {string} canvasId
 * @param {Array} sessions
 */
function createVolumeChart(canvasId, sessions) {
  destroyChart('volume');

  var canvas = document.getElementById(canvasId);
  if (!canvas) return;

  var ctx = canvas.getContext('2d');
  var dates = sessions.map(function (s) { return s.date.slice(5); });
  var volumes = sessions.map(function (s) {
    return parseFloat((s.volume.volume_hands / 10000).toFixed(1));
  });
  var amounts = sessions.map(function (s) {
    return parseFloat((s.volume.amount / 100000000).toFixed(2));
  });

  var options = getDefaultOptions();
  options.scales = {
    x: {
      ticks: { font: { size: 11 }, color: '#6e6e73' },
      grid: { color: '#f0f0f2', drawBorder: false }
    },
    y: {
      type: 'linear',
      position: 'left',
      title: { display: true, text: '成交量(万手)', font: { size: 12 } },
      ticks: { callback: function (v) { return v.toFixed(0) + '万'; } },
      grid: { color: '#f0f0f2', drawBorder: false }
    },
    y1: {
      type: 'linear',
      position: 'right',
      title: { display: true, text: '成交额(亿元)', font: { size: 12 } },
      ticks: { callback: function (v) { return v.toFixed(1) + '亿'; } },
      grid: { drawOnChartArea: false }
    }
  };

  chartInstances['volume'] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: dates,
      datasets: [
        {
          label: '成交量(万手)',
          data: volumes,
          backgroundColor: 'rgba(55, 138, 221, 0.35)',
          borderColor: 'rgba(55, 138, 221, 0.7)',
          borderWidth: 1,
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          label: '成交额(亿元)',
          data: amounts,
          type: 'line',
          borderColor: '#e8923f',
          backgroundColor: 'transparent',
          borderWidth: 2,
          pointRadius: 3,
          pointBackgroundColor: '#e8923f',
          tension: 0.3,
          yAxisID: 'y1',
          order: 1
        }
      ]
    },
    options: options
  });
}

/**
 * 区块4：资金流向堆叠柱状图
 * @param {string} canvasId
 * @param {Array} sessions
 */
function createFundFlowChart(canvasId, sessions) {
  destroyChart('fundflow');

  var canvas = document.getElementById(canvasId);
  if (!canvas) return;

  var ctx = canvas.getContext('2d');
  var dates = sessions.map(function (s) { return s.date.slice(5); });

  var superLarge = sessions.map(function (s) { return parseFloat((s.fund_flow.super_large_net / 10000).toFixed(0)); });
  var large = sessions.map(function (s) { return parseFloat((s.fund_flow.large_net / 10000).toFixed(0)); });
  var medium = sessions.map(function (s) { return parseFloat((s.fund_flow.medium_net / 10000).toFixed(0)); });
  var small = sessions.map(function (s) { return parseFloat((s.fund_flow.small_net / 10000).toFixed(0)); });

  var options = getDefaultOptions();
  options.scales = Object.assign({}, options.scales, {
    y: {
      title: { display: true, text: '万元', font: { size: 12 } },
      stacked: true,
      ticks: { callback: function (v) { return (v / 10000).toFixed(1) + '亿'; } }
    },
    x: { stacked: true }
  });

  chartInstances['fundflow'] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: dates,
      datasets: [
        {
          label: '超大单净',
          data: superLarge,
          backgroundColor: '#0F6E56',
          borderWidth: 0,
          borderRadius: { topLeft: 4, topRight: 4, bottomLeft: 0, bottomRight: 0 },
          stack: 'main'
        },
        {
          label: '大单净',
          data: large,
          backgroundColor: '#1D9E75',
          borderWidth: 0,
          borderRadius: { topLeft: 4, topRight: 4, bottomLeft: 0, bottomRight: 0 },
          stack: 'main'
        },
        {
          label: '中单净',
          data: medium,
          backgroundColor: '#F0997B',
          borderWidth: 0,
          borderRadius: { topLeft: 0, topRight: 0, bottomLeft: 4, bottomRight: 4 },
          stack: 'main'
        },
        {
          label: '小单净',
          data: small,
          backgroundColor: '#D85A30',
          borderWidth: 0,
          borderRadius: { topLeft: 0, topRight: 0, bottomLeft: 4, bottomRight: 4 },
          stack: 'main'
        }
      ]
    },
    options: options
  });
}

/**
 * 区块5：三寿评分趋势图
 * @param {string} canvasId
 * @param {Array} sessions
 */
function createScoreChart(canvasId, sessions) {
  destroyChart('score');

  var canvas = document.getElementById(canvasId);
  if (!canvas) return;

  var ctx = canvas.getContext('2d');
  var dates = sessions.map(function (s) { return s.date.slice(5); });
  var scores = sessions.map(function (s) { return s.sanshou_score.total; });

  var options = getDefaultOptions();
  options.scales = Object.assign({}, options.scales, {
    y: {
      min: 0,
      max: 100,
      title: { display: true, text: '评分', font: { size: 12 } },
      ticks: {
        stepSize: 10,
        callback: function (v) { return v; }
      }
    }
  });

  // 添加色带背景（通过 annotation 或自定义插件）
  options.plugins = Object.assign({}, options.plugins);

  var getScoreColor = function (score) {
    if (score >= 85) return '#0F6E56';
    if (score >= 70) return '#1d9e75';
    if (score >= 55) return '#378add';
    if (score >= 40) return '#aeaeb2';
    if (score >= 25) return '#e8923f';
    return '#d85a30';
  };

  chartInstances['score'] = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dates,
      datasets: [{
        label: '三寿总分',
        data: scores,
        borderColor: '#378add',
        backgroundColor: 'rgba(55, 138, 221, 0.1)',
        borderWidth: 2.5,
        pointRadius: 5,
        pointBackgroundColor: scores.map(getScoreColor),
        pointBorderColor: scores.map(getScoreColor),
        tension: 0.3,
        fill: true
      }]
    },
    options: options
  });
}

/**
 * 区块6：关键价位带
 * @param {string} canvasId
 * @param {Array} sessions
 */
function createKeyLevelChart(canvasId, sessions) {
  destroyChart('keylevel');

  var canvas = document.getElementById(canvasId);
  if (!canvas) return;

  var ctx = canvas.getContext('2d');
  var dates = sessions.map(function (s) { return s.date.slice(5); });
  var closes = sessions.map(function (s) { return s.price.close; });

  // 用最新的 key_levels
  var latest = sessions[sessions.length - 1];
  var support1 = latest.key_levels.support[0];
  var resistance1 = latest.key_levels.resistance[0];
  var costBasis = latest.key_levels.cost_basis;

  var datasets = [{
    label: '收盘价',
    data: closes,
    borderColor: '#1d1d1f',
    backgroundColor: 'transparent',
    borderWidth: 2,
    pointRadius: 3,
    tension: 0.3
  }, {
    label: '支撑位(' + support1 + ')',
    data: dates.map(function () { return support1; }),
    borderColor: '#378add',
    backgroundColor: 'transparent',
    borderWidth: 1.5,
    borderDash: [8, 4],
    pointRadius: 0,
    fill: false
  }, {
    label: '压力位(' + resistance1 + ')',
    data: dates.map(function () { return resistance1; }),
    borderColor: '#e8923f',
    backgroundColor: 'transparent',
    borderWidth: 1.5,
    borderDash: [8, 4],
    pointRadius: 0,
    fill: false
  }, {
    label: '持仓成本(' + costBasis + ')',
    data: dates.map(function () { return costBasis; }),
    borderColor: '#aeaeb2',
    backgroundColor: 'transparent',
    borderWidth: 1.5,
    borderDash: [3, 3],
    pointRadius: 0,
    fill: false
  }];

  var options = getDefaultOptions();
  options.scales = Object.assign({}, options.scales, {
    y: {
      title: { display: true, text: '元', font: { size: 12 } },
      ticks: { callback: function (v) { return v.toFixed(2); } }
    }
  });

  chartInstances['keylevel'] = new Chart(ctx, {
    type: 'line',
    data: { labels: dates, datasets: datasets },
    options: options
  });
}

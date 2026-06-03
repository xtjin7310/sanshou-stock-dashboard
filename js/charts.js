/* ============================================================
   charts.js — Chart.js v4 金融暗色主题 + 资金走势折线
   ============================================================ */
var chartInstances = {};
var currentFundData = [];

function destroyChart(key) {
  if (chartInstances[key]) { chartInstances[key].destroy(); delete chartInstances[key]; }
}
function destroyAllCharts() {
  Object.keys(chartInstances).forEach(function(k) { if(chartInstances[k]) chartInstances[k].destroy(); });
  chartInstances = {};
}

var DARK_THEME = {
  text: '#8890a4', grid: '#1e2430', bg: '#141820',
  rise: '#f0434a', fall: '#22c55e', blue: '#3b82f6',
  cyan: '#06b6d4', orange: '#f59e0b', purple: '#8b5cf6',
  white: '#e1e4ea'
};

function getDefaultOptions() {
  return {
    responsive: true, maintainAspectRatio: false,
    animation: { duration: 300 },
    plugins: {
      legend: { labels: { color: DARK_THEME.text, font: { size: 11 }, usePointStyle: true, pointStyleWidth: 6, padding: 14 } },
      tooltip: {
        backgroundColor: 'rgba(20,24,32,0.96)', titleColor: DARK_THEME.white, bodyColor: DARK_THEME.text,
        borderColor: DARK_THEME.grid, borderWidth: 1, cornerRadius: 6, padding: 10,
        titleFont: { size: 12 }, bodyFont: { size: 11 }
      }
    },
    scales: {
      x: { ticks: { color: DARK_THEME.text, font: { size: 10 } }, grid: { color: DARK_THEME.grid, drawBorder: false } },
      y: { ticks: { color: DARK_THEME.text, font: { size: 10 } }, grid: { color: DARK_THEME.grid, drawBorder: false } }
    },
    interaction: { mode: 'index', intersect: false }
  };
}

function createPriceChart(canvasId, sessions) {
  destroyChart('price');
  var canvas = document.getElementById(canvasId); if(!canvas) return;
  var ctx = canvas.getContext('2d');
  var dates = sessions.map(function(s){return s.date.slice(5);});
  var am = sessions.map(function(s){return s.session==='morning'?s.price.close:null;});
  var pm = sessions.map(function(s){return s.session==='afternoon'?s.price.close:null;});
  var ds = [];
  if(pm.some(function(v){return v!==null;})) ds.push({label:'盘后收盘',data:pm,borderColor:DARK_THEME.blue,borderWidth:2,pointRadius:3,pointBg:DARK_THEME.blue,tension:0.25,fill:false,spanGaps:false});
  if(am.some(function(v){return v!==null;})) ds.push({label:'午间收盘',data:am,borderColor:DARK_THEME.blue,borderWidth:1.5,borderDash:[5,3],pointRadius:2,pointBg:DARK_THEME.blue,tension:0.25,fill:false,spanGaps:false});
  var opt = getDefaultOptions();
  opt.scales.y = { ticks: { color: DARK_THEME.text, callback: function(v){return v.toFixed(2);} }, grid: { color: DARK_THEME.grid }, title: { display: true, text: '元', color: DARK_THEME.text } };
  chartInstances['price'] = new Chart(ctx, { type: 'line', data: { labels: dates, datasets: ds }, options: opt });
}

function createChangeChart(canvasId, sessions) {
  destroyChart('change');
  var canvas = document.getElementById(canvasId); if(!canvas) return;
  var ctx = canvas.getContext('2d');
  var dates = sessions.map(function(s){return s.date.slice(5);});
  var pm = sessions.map(function(s){return s.session==='afternoon'?parseFloat(s.price.change_pct.toFixed(2)):null;});
  var am = sessions.map(function(s){return s.session==='morning'?parseFloat(s.price.change_pct.toFixed(2)):null;});
  function cc(v){if(v===null)return'transparent';return v>=0?DARK_THEME.rise:DARK_THEME.fall;}
  var ds = [
    {label:'盘后',data:pm,backgroundColor:pm.map(cc),borderRadius:3,order:2},
    {label:'午间',data:am,backgroundColor:am.map(cc),borderRadius:3,order:2}
  ];
  var opt = getDefaultOptions();
  opt.scales.y = { ticks: { color: DARK_THEME.text, callback: function(v){return v.toFixed(1)+'%';} }, grid: { color: DARK_THEME.grid }, title: { display: true, text: '%', color: DARK_THEME.text } };
  chartInstances['change'] = new Chart(ctx, { type: 'bar', data: { labels: dates, datasets: ds }, options: opt });
}

function createVolumeChart(canvasId, sessions) {
  destroyChart('volume');
  var canvas = document.getElementById(canvasId); if(!canvas) return;
  var ctx = canvas.getContext('2d');
  var dates = sessions.map(function(s){return s.date.slice(5);});
  var vols = sessions.map(function(s){return parseFloat((s.volume.volume_hands/10000).toFixed(1));});
  var amts = sessions.map(function(s){return parseFloat((s.volume.amount/100000000).toFixed(2));});
  var opt = getDefaultOptions();
  opt.scales = {
    x: { ticks: { color: DARK_THEME.text, font: { size: 10 } }, grid: { color: DARK_THEME.grid } },
    y: { type: 'linear', position: 'left', title: { display: true, text: '成交量(万手)', color: DARK_THEME.text }, ticks: { color: DARK_THEME.text, callback: function(v){return v.toFixed(0)+'万';} }, grid: { color: DARK_THEME.grid } },
    y1: { type: 'linear', position: 'right', title: { display: true, text: '成交额(亿元)', color: DARK_THEME.orange }, ticks: { color: DARK_THEME.orange, callback: function(v){return v.toFixed(1)+'亿';} }, grid: { drawOnChartArea: false } }
  };
  chartInstances['volume'] = new Chart(ctx, { type: 'bar', data: { labels: dates, datasets: [
    { label: '成交量(万手)', data: vols, backgroundColor: 'rgba(59,130,246,0.3)', borderColor: 'rgba(59,130,246,0.6)', borderWidth: 1, borderRadius: 3, yAxisID: 'y', order: 2 },
    { label: '成交额(亿元)', data: amts, type: 'line', borderColor: DARK_THEME.orange, backgroundColor: 'transparent', borderWidth: 2, pointRadius: 3, pointBg: DARK_THEME.orange, tension: 0.25, yAxisID: 'y1', order: 1 }
  ]}, options: opt });
}

/* ========== 资金流向：折线趋势 + 多维度勾选 ========== */
var FUND_DIMENSIONS = {
  main:     { key:'main_net',    label:'主力净额',    color:'#e1e4ea', w:2.5, dash:null, visible:true,  axis:'y', order:1, unit:10000 },
  super:    { key:'super_large_net', label:'超大单',  color:'#06b6d4', w:1.5, dash:[4,2], visible:true, axis:'y', order:2, unit:10000 },
  large:    { key:'large_net',   label:'大单净',    color:'#3b82f6', w:1.5, dash:[4,2], visible:false, axis:'y', order:3, unit:10000 },
  medium:   { key:'medium_net',  label:'中单净',    color:'#f59e0b', w:1.5, dash:null, visible:false, axis:'y', order:4, unit:10000 },
  small:    { key:'small_net',   label:'小单净',    color:'#ef4444', w:1.5, dash:null, visible:false, axis:'y', order:5, unit:10000 },
  margin:   { key:'margin_balance', label:'融资余额', color:'#f59e0b', w:1.5, dash:null, visible:false, axis:'y1', order:6, unit:100000000, suffix:'亿' },
  short:    { key:'short_balance',  label:'融券余额', color:'#8b5cf6', w:1.5, dash:[3,3], visible:false, axis:'y1', order:7, unit:10000, suffix:'万' }
};

function createFundFlowChart(canvasId, sessions, visibleDims) {
  destroyChart('fundflow');
  var canvas = document.getElementById(canvasId); if(!canvas) return;
  var ctx = canvas.getContext('2d');
  var dates = sessions.map(function(s){return s.date.slice(5);});
  currentFundData = sessions;

  // Default visible dimensions from checkboxes, or fallback
  if (!visibleDims) {
    visibleDims = {};
    var cbs = document.querySelectorAll('.fund-cb');
    if (cbs.length > 0) {
      cbs.forEach(function(cb){ visibleDims[cb.value] = cb.checked; });
    } else {
      visibleDims = { main: true, super: true, large: false, medium: false, small: false, margin: false, short: false };
    }
  }

  var datasets = [];
  var hasY1 = false;

  Object.keys(FUND_DIMENSIONS).forEach(function(dimKey){
    var dim = FUND_DIMENSIONS[dimKey];
    if (!visibleDims[dimKey] && visibleDims.hasOwnProperty(dimKey)) return;
    if (!dim.visible && !visibleDims[dimKey]) return;

    var data = sessions.map(function(s){
      var v = s.fund_flow[dim.key];
      if (v === undefined || v === null) return null;
      return parseFloat((v / dim.unit).toFixed(dim.unit >= 100000000 ? 2 : 0));
    });

    if (dim.axis === 'y1') hasY1 = true;

    datasets.push({
      label: dim.label + (dim.suffix ? '('+dim.suffix+')' : ''),
      data: data,
      borderColor: dim.color, backgroundColor: 'transparent',
      borderWidth: dim.w, pointRadius: dim.order === 1 ? 4 : 2, pointBg: dim.color,
      borderDash: dim.dash || undefined,
      tension: 0.3, yAxisID: dim.axis, order: dim.order
    });
  });

  var opt = getDefaultOptions();
  opt.scales = {
    x: { ticks: { color: DARK_THEME.text, font: { size: 10 } }, grid: { color: DARK_THEME.grid } },
    y: {
      type: 'linear', position: 'left',
      title: { display: true, text: '净额(万元)', color: DARK_THEME.text },
      ticks: { color: DARK_THEME.text, callback: function(v){ if(Math.abs(v)>=10000) return (v/10000).toFixed(1)+'亿'; return v+'万'; } },
      grid: { color: DARK_THEME.grid }
    }
  };
  if (hasY1) {
    opt.scales.y1 = {
      type: 'linear', position: 'right',
      title: { display: true, text: '余额', color: DARK_THEME.orange },
      ticks: { color: DARK_THEME.orange },
      grid: { drawOnChartArea: false }
    };
  }

  opt.onClick = function(e, elements) {
    if (elements.length > 0) { var idx = elements[0].index; showFundSummary(idx, sessions); }
  };

  chartInstances['fundflow'] = new Chart(ctx, {
    type: 'line', data: { labels: dates, datasets: datasets }, options: opt
  });
}

/* Show fund summary for clicked date */
function showFundSummary(idx, sessions) {
  if (idx < 0 || idx >= sessions.length) return;
  var s = sessions[idx];
  var panel = document.getElementById('fund-summary');
  if (!panel) return;
  panel.classList.add('active');

  var ff = s.fund_flow;
  var main = ff.main_net || 0;
  var supL = ff.super_large_net || 0;
  var lrg = ff.large_net || 0;
  var med = ff.medium_net || 0;
  var sml = ff.small_net || 0;

  document.getElementById('fs-date').textContent = s.date + ' ' + (s.session === 'morning' ? '午间' : '盘后');
  document.getElementById('fs-main').textContent = formatAmt(main);
  document.getElementById('fs-main').className = 'fs-val ' + (main >= 0 ? 'rise' : 'fall');
  document.getElementById('fs-super').textContent = formatAmt(supL);
  document.getElementById('fs-super').className = 'fs-val ' + (supL >= 0 ? 'rise' : 'fall');
  document.getElementById('fs-large').textContent = formatAmt(lrg);
  document.getElementById('fs-large').className = 'fs-val ' + (lrg >= 0 ? 'rise' : 'fall');
  document.getElementById('fs-med').textContent = formatAmt(med);
  document.getElementById('fs-med').className = 'fs-val ' + (med >= 0 ? 'rise' : 'fall');
  document.getElementById('fs-small').textContent = formatAmt(sml);
  document.getElementById('fs-small').className = 'fs-val ' + (sml >= 0 ? 'rise' : 'fall');
  document.getElementById('fs-margin').textContent = ff.margin_balance ? (ff.margin_balance/100000000).toFixed(2)+'亿' : '--';
  document.getElementById('fs-short').textContent = ff.short_balance ? (ff.short_balance/10000).toFixed(1)+'万' : '--';
  document.getElementById('fs-turnover').textContent = s.volume.turnover_rate.toFixed(2)+'%';
  document.getElementById('fs-vratio').textContent = s.volume.volume_ratio.toFixed(2);
}

function formatAmt(v) {
  var abs = Math.abs(v);
  var sign = v >= 0 ? '+' : '-';
  if (abs >= 100000000) return sign + (abs/100000000).toFixed(2) + '亿';
  if (abs >= 10000) return sign + (abs/10000).toFixed(0) + '万';
  return sign + abs.toFixed(0);
}

function createScoreChart(canvasId, sessions) {
  destroyChart('score');
  var canvas = document.getElementById(canvasId); if(!canvas) return;
  var ctx = canvas.getContext('2d');
  var dates = sessions.map(function(s){return s.date.slice(5);});
  var scores = sessions.map(function(s){return s.sanshou_score.total;});
  function sc(v){if(v>=85)return'#06b6d4';if(v>=70)return'#22c55e';if(v>=55)return'#3b82f6';if(v>=40)return'#7e8494';if(v>=25)return'#f59e0b';return'#ef4444';}
  var opt = getDefaultOptions();
  opt.scales.y = { min: 0, max: 100, title: { display: true, text: '评分', color: DARK_THEME.text }, ticks: { color: DARK_THEME.text, stepSize: 10 }, grid: { color: DARK_THEME.grid } };
  chartInstances['score'] = new Chart(ctx, { type: 'line', data: { labels: dates, datasets: [{
    label: '三寿总分', data: scores, borderColor: DARK_THEME.blue, backgroundColor: 'rgba(59,130,246,0.08)',
    borderWidth: 2.5, pointRadius: 5, pointBg: scores.map(sc), pointBorderColor: scores.map(sc),
    tension: 0.3, fill: true
  }]}, options: opt });
}

function createKeyLevelChart(canvasId, sessions) {
  destroyChart('keylevel');
  var canvas = document.getElementById(canvasId); if(!canvas) return;
  var ctx = canvas.getContext('2d');
  var dates = sessions.map(function(s){return s.date.slice(5);});
  var closes = sessions.map(function(s){return s.price.close;});
  var latest = sessions[sessions.length-1];
  var s1 = latest.key_levels.support[0], r1 = latest.key_levels.resistance[0], cb = latest.key_levels.cost_basis;
  var ds = [
    { label: '收盘价', data: closes, borderColor: DARK_THEME.white, backgroundColor: 'transparent', borderWidth: 2, pointRadius: 3, tension: 0.3 },
    { label: '支撑('+s1+')', data: dates.map(function(){return s1;}), borderColor: DARK_THEME.blue, borderWidth: 1.5, borderDash: [6,3], pointRadius: 0, fill: false },
    { label: '压力('+r1+')', data: dates.map(function(){return r1;}), borderColor: DARK_THEME.orange, borderWidth: 1.5, borderDash: [6,3], pointRadius: 0, fill: false },
    { label: '成本('+cb+')', data: dates.map(function(){return cb;}), borderColor: DARK_THEME.text, borderWidth: 1, borderDash: [2,2], pointRadius: 0, fill: false }
  ];
  var opt = getDefaultOptions();
  opt.scales.y = { title: { display: true, text: '元', color: DARK_THEME.text }, ticks: { color: DARK_THEME.text, callback: function(v){return v.toFixed(2);} }, grid: { color: DARK_THEME.grid } };
  chartInstances['keylevel'] = new Chart(ctx, { type: 'line', data: { labels: dates, datasets: ds }, options: opt });
}

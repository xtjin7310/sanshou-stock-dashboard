/* ============================================================
   live-quote.js — 实时行情轮询（东方财富API）
   ============================================================ */
var LIVE_QUOTES = {
  xinfengming: { secid: '1.603225', price: null, change: null },
  huagongkeji: { secid: '0.000988', price: null, change: null },
  zhongxing:   { secid: '0.000063', price: null, change: null }
};
var QUOTE_TIMER = null;

function fetchLiveQuotes(callback) {
  var secids = ['1.603225','0.000988','0.000063'].join(',');
  var url = 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f14,f15,f17&secids=' + secids;

  fetch(url).then(function(r){return r.json();}).then(function(d){
    if (!d.data || !d.data.diff) return;
    d.data.diff.forEach(function(item){
      var key;
      if (item.f14 === '新凤鸣') key = 'xinfengming';
      else if (item.f14 === '华工科技') key = 'huagongkeji';
      else if (item.f14 === '中兴通讯') key = 'zhongxing';
      else return;

      var f2 = item.f2; var f3 = item.f3; var f4 = item.f4; var f15 = item.f15; var f17 = item.f17;
      LIVE_QUOTES[key].price = f2 / 100;
      LIVE_QUOTES[key].change = f3 / 100;
      LIVE_QUOTES[key].high = f15 / 100;
      LIVE_QUOTES[key].low = f16 ? f16 / 100 : null;
      LIVE_QUOTES[key].open = f17 / 100;
    });
    if (callback) callback(LIVE_QUOTES);
  }).catch(function(e){ console.warn('实时行情获取失败', e); });
}

function startQuotePolling(intervalMs) {
  intervalMs = intervalMs || 10000;
  fetchLiveQuotes();
  if (QUOTE_TIMER) clearInterval(QUOTE_TIMER);
  QUOTE_TIMER = setInterval(function(){ fetchLiveQuotes(); }, intervalMs);
}

function updateTopBarLive(stock) {
  var q = LIVE_QUOTES[stock];
  if (!q || q.price === null) return;
  var pEl = document.getElementById('top-price');
  var cEl = document.getElementById('top-change');
  if (pEl) pEl.textContent = q.price.toFixed(2);
  if (cEl) {
    var sign = q.change >= 0 ? '+' : '';
    cEl.textContent = sign + q.change.toFixed(2) + '%';
    cEl.className = 'change-display ' + (q.change >= 0 ? 'change-up' : 'change-down');
  }
}

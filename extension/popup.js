// Popup logic
var stocks = ['新凤鸣', '华工科技', '中兴通讯'];

function checkStatus() {
  var dot = document.getElementById('status-dot');
  var text = document.getElementById('status-text');

  chrome.runtime.sendMessage({ type: 'HEARTBEAT' }, function (resp) {
    if (chrome.runtime.lastError || !resp || !resp.alive) {
      dot.className = 'dot off';
      text.textContent = 'Native Host 未连接';
    } else {
      dot.className = 'dot on';
      text.textContent = '已连接，可以触发';
    }
  });
}

function sendCatchup(session) {
  var label = session === 'morning' ? '午间复盘' : '盘后复盘';
  if (!confirm('确认触发全部三股' + label + '？')) return;

  stocks.forEach(function (name) {
    var instruction = '请帮我补跑 ' + name + ' 的' + label;
    chrome.runtime.sendMessage({
      type: 'TRIGGER_CATCHUP',
      payload: { instruction: instruction, stock: name, session: session }
    });
  });

  alert('已发送三股' + label + '指令！');
}

document.getElementById('btn-noon').addEventListener('click', function () { sendCatchup('morning'); });
document.getElementById('btn-eod').addEventListener('click', function () { sendCatchup('afternoon'); });

checkStatus();

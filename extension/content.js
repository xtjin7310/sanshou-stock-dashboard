(function () {
  'use strict';

  // Intercept catchup button clicks on stock pages
  function interceptCatchupButtons() {
    // Find all catchup buttons (morning/afternoon)
    var buttons = document.querySelectorAll('[onclick*="triggerCatchup"]');
    buttons.forEach(function (btn) {
      // Remove old onclick
      var newBtn = btn.cloneNode(true);
      btn.parentNode.replaceChild(newBtn, btn);

      newBtn.addEventListener('click', function () {
        var session = this.textContent.includes('午间') ? 'morning' : 'afternoon';
        var stockEl = document.body.getAttribute('data-stock');
        var stock = stockEl || 'xinfengming';

        var symbol = document.getElementById('stock-code');
        var code = symbol ? symbol.textContent.trim() : '';
        var nameEl = document.getElementById('stock-name');
        var name = nameEl ? nameEl.textContent.trim() : '';

        var instruction = '请帮我补跑 ' + (name || stock) + ' 的' + (session === 'morning' ? '午间复盘' : '盘后复盘');

        // Send via native messaging
        chrome.runtime.sendMessage({
          type: 'TRIGGER_CATCHUP',
          payload: {
            instruction: instruction,
            stock: stock,
            session: session,
            code: code,
            name: name
          }
        }, function (response) {
          if (chrome.runtime.lastError) {
            console.warn('Native host not available:', chrome.runtime.lastError.message);
            // Fallback: copy to clipboard
            navigator.clipboard.writeText(instruction).then(function () {
              alert('指令已复制到剪贴板并尝试发送！\n\n' + instruction + '\n\n（如 WorkBuddy 未反应，请手动粘贴）');
            });
          } else {
            // Show success feedback on button
            newBtn.textContent = '已发送!';
            newBtn.style.background = '#22c55e';
            newBtn.style.color = '#fff';
            setTimeout(function () {
              newBtn.textContent = session === 'morning' ? '午间补漏' : '盘后补漏';
              newBtn.style.background = '';
              newBtn.style.color = '';
            }, 2000);
          }
        });
      });
    });
  }

  // Run on load and on DOM changes
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', interceptCatchupButtons);
  } else {
    interceptCatchupButtons();
  }

  // Re-run when navigation changes (SPA-like)
  var observer = new MutationObserver(function () {
    interceptCatchupButtons();
  });
  observer.observe(document.body, { childList: true, subtree: true });
})();

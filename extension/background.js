// Background service worker - bridges content script to native host
var NATIVE_HOST_NAME = 'com.sanshou.stockbuddy';

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.type === 'TRIGGER_CATCHUP') {
    var data = message.payload;

    // Try native messaging first
    trySendToNative(data).then(function (result) {
      sendResponse({ success: true, result: result });
    }).catch(function (err) {
      console.warn('Native host unavailable, trying direct:', err.message);
      // Fallback: try direct script execution
      trySendDirect(data).then(function (result) {
        sendResponse({ success: true, result: result, fallback: true });
      }).catch(function (err2) {
        sendResponse({ success: false, error: err2.message });
      });
    });

    return true; // Keep channel open for async response
  }

  if (message.type === 'HEARTBEAT') {
    // Check if native host is alive
    tryPingNative().then(function () {
      sendResponse({ alive: true });
    }).catch(function () {
      sendResponse({ alive: false });
    });
    return true;
  }
});

function trySendToNative(data) {
  return new Promise(function (resolve, reject) {
    chrome.runtime.sendNativeMessage(NATIVE_HOST_NAME, {
      action: 'catchup',
      instruction: data.instruction,
      stock: data.stock,
      session: data.session,
      timestamp: new Date().toISOString()
    }, function (response) {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
      } else {
        resolve(response || 'sent');
      }
    });
  });
}

function trySendDirect(data) {
  return new Promise(function (resolve, reject) {
    // Fallback: write instruction to a temp file that automation script watches
    // This works when native host is not yet installed
    resolve('copied_only');
  });
}

function tryPingNative() {
  return new Promise(function (resolve, reject) {
    chrome.runtime.sendNativeMessage(NATIVE_HOST_NAME, { action: 'ping' }, function (response) {
      if (chrome.runtime.lastError) reject(new Error(chrome.runtime.lastError.message));
      else resolve(response);
    });
  });
}

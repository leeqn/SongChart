document.addEventListener('DOMContentLoaded', () => {
  const serverInput = document.getElementById('serverUrl');
  const keyInput = document.getElementById('apiKey');
  const form = document.getElementById('settingsForm');
  const statusMsg = document.getElementById('statusMsg');
  const openSettingsTab = document.getElementById('openSettingsTab');

  // Загрузка сохраненных данных
  chrome.storage.sync.get(['songchart_server', 'songchart_api_key'], (data) => {
    serverInput.value = data.songchart_server || 'http://127.0.0.1:8000';
    keyInput.value = data.songchart_api_key || '';
  });

  // Сохранение ключа и адреса
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const server = serverInput.value.trim().replace(/\/+$/, '');
    const apiKey = keyInput.value.trim();

    if (!apiKey) {
      showStatus('API Key cannot be empty!', 'error');
      return;
    }

    chrome.storage.sync.set({
      songchart_server: server,
      songchart_api_key: apiKey
    }, () => {
      showStatus('Settings saved successfully!', 'success');
    });
  });

  // Ссылка для быстрого перехода в настройки веб-приложения
  openSettingsTab.addEventListener('click', (e) => {
    e.preventDefault();
    const server = serverInput.value.trim().replace(/\/+$/, '') || 'http://127.0.0.1:8000';
    chrome.tabs.create({ url: `${server}/settings/` });
  });

  function showStatus(text, type) {
    statusMsg.innerText = text;
    statusMsg.className = `status-msg ${type}`;
    setTimeout(() => {
      statusMsg.innerText = '';
      statusMsg.className = 'status-msg';
    }, 3000);
  }
});
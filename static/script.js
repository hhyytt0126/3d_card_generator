// script.js

const baseInput      = document.getElementById('base');
const targetInput    = document.getElementById('target');
const previewBase    = document.getElementById('preview-base');
const previewTarget  = document.getElementById('preview-target');
const form           = document.getElementById('form');
const progressBar    = document.getElementById('progress');
const progressLabel  = document.getElementById('progress-label');
const progContainer  = document.getElementById('progress-container');

// 画像プレビュー
function previewImage(input, previewEl) {
  const file = input.files[0];
  if (!file) {
    previewEl.src = '';
    previewEl.classList.remove('show');
    return;
  }
  const reader = new FileReader();
  reader.onload = e => {
    previewEl.src = e.target.result;
    previewEl.classList.add('show');
  };
  reader.readAsDataURL(file);
}

baseInput.addEventListener('change', () => previewImage(baseInput, previewBase));
targetInput.addEventListener('change', () => previewImage(targetInput, previewTarget));

// フォーム送信 + プログレスバー
form.addEventListener('submit', e => {
  e.preventDefault();

  const fd  = new FormData(form);
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/generate');
  xhr.responseType = 'blob';

  // アップロード進捗
  xhr.upload.onprogress = e => {
    if (e.lengthComputable) {
      const pct = Math.round((e.loaded / e.total) * 100);
      progContainer.classList.remove('hidden');
      progressBar.value       = pct;
      progressLabel.textContent = `${pct}%`;
    }
  };

  // 完了時の処理
  xhr.onload = () => {
    if (xhr.status === 200) {
      const blob = xhr.response;
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement('a');
      a.href     = url;
      a.download = '3d_card.stl';
      a.click();
      URL.revokeObjectURL(url);
    } else {
      alert(`Error: ${xhr.statusText}`);
    }
    // リセット
    progressBar.value       = 0;
    progressLabel.textContent = '0%';
    progContainer.classList.add('hidden');
  };

  xhr.send(fd);
});

// ドラッグ＆ドロップ設定
['base-wrapper', 'target-wrapper'].forEach(id => {
  const wrapper = document.getElementById(id);
  const input   = wrapper.querySelector('input[type="file"]');

  wrapper.addEventListener('dragover', e => {
    e.preventDefault();
    wrapper.style.borderColor = '#667eea';
    wrapper.style.background  = '#f1f5f9';
  });

  wrapper.addEventListener('dragleave', e => {
    e.preventDefault();
    if (!wrapper.classList.contains('has-file')) {
      wrapper.style.borderColor = '#e2e8f0';
      wrapper.style.background  = '#f8fafc';
    }
  });

  wrapper.addEventListener('drop', e => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      input.files = files;
      input.dispatchEvent(new Event('change'));
      wrapper.classList.add('has-file');
    }
  });
});

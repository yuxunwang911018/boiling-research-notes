document.querySelectorAll('.menu-toggle').forEach((button) => {
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(open));
    document.getElementById('site-nav').classList.toggle('is-open', open);
    button.innerHTML = open ? '關閉導覽 <span aria-hidden="true">−</span>' : '開啟導覽 <span aria-hidden="true">＋</span>';
  });
});

document.querySelectorAll('.media-viewer').forEach((viewer) => {
  const choices = [...viewer.querySelectorAll('.media-choice')];
  const image = viewer.querySelector('.field-image');
  const caption = viewer.querySelector('.media-caption');
  const original = viewer.querySelector('.original-link');
  const play = viewer.querySelector('.play-button');
  const status = viewer.querySelector('.media-status');
  let selected = choices[0];
  let playing = false;

  function update() {
    image.src = playing ? selected.dataset.animation : selected.dataset.poster;
    image.alt = selected.dataset.alt + (playing ? '目前播放驗證快照動畫。' : '');
    caption.textContent = selected.dataset.caption;
    original.href = image.getAttribute('src');
    play.setAttribute('aria-pressed', String(playing));
    play.innerHTML = playing ? '停止動畫 <span aria-hidden="true">Ⅱ</span>' : '播放動畫 <span aria-hidden="true">▷</span>';
    status.textContent = playing ? '動畫播放中' : '靜態快照';
    choices.forEach((choice) => choice.setAttribute('aria-pressed', String(choice === selected)));
  }

  choices.forEach((choice) => choice.addEventListener('click', () => {
    selected = choice;
    playing = false;
    update();
  }));
  play.addEventListener('click', () => {
    playing = !playing;
    update();
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && playing) {
      playing = false;
      update();
    }
  });
});

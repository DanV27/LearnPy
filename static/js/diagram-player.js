/**
 * DiagramPlayer — step-through animated diagram component.
 *
 * Reads a JSON array from <script id="diagram-sequence-data"> injected by
 * Jinja and replaces the #diagram-player-mount container with a navigable
 * frame-by-frame player.
 *
 * No dependencies — plain vanilla JS, no build step, no npm.
 *
 * Noscript fallback: the server renders <noscript> inside the mount
 * containing step-1 as a static image, so the diagram is always visible
 * even without JS.
 */
(function () {
  const dataEl = document.getElementById('diagram-sequence-data');
  const mount  = document.getElementById('diagram-player-mount');

  if (!dataEl || !mount) return;

  let steps;
  try {
    steps = JSON.parse(dataEl.textContent.trim());
  } catch (e) {
    return;
  }

  if (!Array.isArray(steps) || steps.length === 0) return;

  let current = 0;

  // -------------------------------------------------------------------------
  // Build DOM
  // -------------------------------------------------------------------------

  const card = document.createElement('div');
  card.className = 'bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-lg';

  // Header
  const header = document.createElement('div');
  header.className = 'flex items-center justify-between px-md py-sm border-b border-outline-variant bg-surface-container-low';
  header.innerHTML =
    '<div class="flex items-center gap-xs">'
    + '<span class="material-symbols-outlined text-secondary shrink-0" style="font-size:18px;">view_carousel</span>'
    + '<span class="font-headline-md text-headline-md text-primary">Step-by-step diagram</span>'
    + '</div>';

  const counter = document.createElement('span');
  counter.className = 'font-code text-[12px] text-on-surface-variant shrink-0';
  header.appendChild(counter);
  card.appendChild(header);

  // Image
  const imgWrap = document.createElement('div');
  imgWrap.className = 'flex justify-center items-center bg-surface-container p-md min-h-[200px]';
  const img = document.createElement('img');
  img.className = 'max-w-full max-h-[480px] object-contain rounded-lg';
  img.alt = '';
  imgWrap.appendChild(img);
  card.appendChild(imgWrap);

  // Caption
  const caption = document.createElement('p');
  caption.className = 'px-lg py-sm font-body-md text-body-md text-on-surface-variant text-center';
  card.appendChild(caption);

  // Controls
  const controls = document.createElement('div');
  controls.className = 'flex items-center justify-between px-md py-sm border-t border-outline-variant bg-surface-container-low';

  const prevBtn = document.createElement('button');
  prevBtn.className =
    'flex items-center gap-xs font-label-md text-label-md px-md py-xs rounded-lg '
    + 'bg-surface-container border border-outline-variant '
    + 'hover:border-primary hover:bg-surface-container-high transition-colors '
    + 'disabled:opacity-30 disabled:cursor-not-allowed';
  prevBtn.innerHTML =
    '<span class="material-symbols-outlined" style="font-size:16px;">arrow_back</span>Prev';

  const dots = document.createElement('div');
  dots.className = 'flex items-center gap-xs';

  const nextBtn = document.createElement('button');
  nextBtn.className =
    'flex items-center gap-xs font-label-md text-label-md px-md py-xs rounded-lg '
    + 'bg-secondary-container text-primary font-bold '
    + 'hover:brightness-110 transition-all '
    + 'disabled:opacity-30 disabled:cursor-not-allowed';
  nextBtn.innerHTML =
    'Next<span class="material-symbols-outlined" style="font-size:16px;">arrow_forward</span>';

  controls.appendChild(prevBtn);
  controls.appendChild(dots);
  controls.appendChild(nextBtn);
  card.appendChild(controls);

  // Dot indicators
  steps.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.className = 'w-[8px] h-[8px] rounded-full transition-colors';
    dot.setAttribute('aria-label', 'Step ' + (i + 1));
    dot.addEventListener('click', () => goTo(i));
    dots.appendChild(dot);
  });

  // -------------------------------------------------------------------------
  // Navigation
  // -------------------------------------------------------------------------

  function goTo(index) {
    current = index;
    const step = steps[current];

    img.src  = '/static/' + step.src;
    img.alt  = step.caption || '';
    caption.textContent = step.caption || '';
    counter.textContent = 'Step ' + (current + 1) + ' of ' + steps.length;

    prevBtn.disabled = current === 0;
    nextBtn.disabled = current === steps.length - 1;

    dots.querySelectorAll('button').forEach((dot, i) => {
      dot.className = 'w-[8px] h-[8px] rounded-full transition-colors '
        + (i === current ? 'bg-secondary' : 'bg-outline-variant hover:bg-outline');
    });
  }

  prevBtn.addEventListener('click', () => { if (current > 0) goTo(current - 1); });
  nextBtn.addEventListener('click', () => { if (current < steps.length - 1) goTo(current + 1); });

  // Left/right arrow keys when player is focused
  card.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft'  && current > 0)               goTo(current - 1);
    if (e.key === 'ArrowRight' && current < steps.length - 1) goTo(current + 1);
  });
  card.setAttribute('tabindex', '0');

  goTo(0);

  mount.innerHTML = '';
  mount.appendChild(card);
})();

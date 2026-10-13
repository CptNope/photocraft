(() => {
  const css = document.createElement('style');
  css.textContent = '#pc-install{position:fixed;right:8px;bottom:calc(env(safe-area-inset-bottom,0px) + 9px);z-index:9999;background:#1d3550;color:#fff;border:1px solid #62bbcf;border-radius:9px;font:13px system-ui;padding:9px 12px;box-shadow:0 2px 9px #0009}#pc-install-tip{position:fixed;right:8px;bottom:calc(env(safe-area-inset-bottom,0px) + 55px);z-index:9999;max-width:260px;background:#1d3550;border:1px solid #62bbcf;color:#fff;padding:12px;border-radius:8px;font:13px/1.45 system-ui}';
  document.head.append(css);
  const button=document.createElement('button');
  button.id='pc-install';
  button.type='button';
  button.textContent='Install PhotoCraft';
  const info=document.createElement('div');
  info.id='pc-install-tip';
  info.hidden=true;
  info.setAttribute('role','status');
  info.textContent=/iPad|iPhone|iPod/.test(navigator.userAgent)
    ? 'In Safari, tap Share and choose Add to Home Screen.'
    : 'In your browser menu, choose Install app or Add to Home screen.';
  document.body.append(button,info);
  let installEvent;
  window.addEventListener('beforeinstallprompt', event=>{
    event.preventDefault();
    installEvent=event;
  });
  button.addEventListener('click',()=>{
    if (installEvent) {
      const e=installEvent;
      installEvent=null;
      e.prompt();
    } else {
      info.hidden=!info.hidden;
    }
  });
  window.addEventListener('appinstalled',()=>{
    button.remove();
    info.remove();
  });
})();

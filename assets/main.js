(function () {
  const current = document.body.dataset.page;
  if (!current) return;
  const links = document.querySelectorAll('.nav a');
  links.forEach((link) => {
    if (link.dataset.page === current) {
      link.classList.add('active');
    }
  });
})();

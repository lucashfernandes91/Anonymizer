window.addEventListener('DOMContentLoaded', () => {

	// Fecha menu mobile e corrige scroll offset da navbar fixa
	document.querySelectorAll('nav a[href^="#"]').forEach(link => {
		link.addEventListener('click', (e) => {
			document.getElementById('nav-links').classList.remove('open');

			const href = link.getAttribute('href');
			if (!href || !href.startsWith('#')) return;

			const target = document.querySelector(href);
			if (!target) return;

			e.preventDefault();
			const navHeight = document.querySelector('nav').offsetHeight;
			const top = target.getBoundingClientRect().top + window.scrollY - navHeight - 8;
			window.scrollTo({ top, behavior: 'smooth' });
		});
	});

	const dropArea = document.getElementById('drop-area');

	dropArea.addEventListener('dragover', (e) => {
		e.preventDefault();
		dropArea.classList.add('dragover');
	});

	dropArea.addEventListener('dragleave', () => {
		dropArea.classList.remove('dragover');
	});

	// Scroll reveal
	const observer = new IntersectionObserver((entries) => {
		entries.forEach(e => {
			if (e.isIntersecting) {
				e.target.style.opacity = '1';
				e.target.style.transform = 'translateY(0)';
			}
		});
	}, { threshold: 0.1 });

	document.querySelectorAll('.meta-card, .step, .benefit, .flow-step').forEach(el => {
		el.style.opacity = '0';
		el.style.transform = 'translateY(20px)';
		el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
		observer.observe(el);
	});

});

// Scroll para resultado APÓS tudo carregar (imagens base64 incluídas)
window.addEventListener('load', () => {
	const resultArea = document.getElementById('result-area');
	const hasResult = resultArea && resultArea.dataset.hasResult === 'true';
	if (!hasResult) return;

	const navHeight = document.querySelector('nav').offsetHeight;
	const scrollTarget = document.querySelector('.gps-block') || resultArea;
	const top = scrollTarget.getBoundingClientRect().top + window.scrollY - navHeight - 16;
	window.scrollTo({ top, behavior: 'smooth' });
});

// Back to top
const backToTop = document.getElementById('back-to-top');
if (backToTop) {
	window.addEventListener('scroll', () => {
		backToTop.classList.toggle('visible', window.scrollY > 300);
	}, { passive: true });
}

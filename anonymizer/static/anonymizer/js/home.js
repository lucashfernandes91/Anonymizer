window.addEventListener('DOMContentLoaded', () => {

	// Scroll para resultado quando existir
	const resultArea = document.getElementById('result-area');
	const hasResult = resultArea && resultArea.dataset.hasResult === 'true';
	if (hasResult) {
		const navHeight = document.querySelector('nav').offsetHeight;
		const top = resultArea.getBoundingClientRect().top + window.scrollY - navHeight - 16;
		window.scrollTo({ top, behavior: 'smooth' });
	}

	// Fecha menu mobile e corrige scroll offset da navbar fixa
	document.querySelectorAll('nav a[href^="#"], #nav-links .nav-link').forEach(link => {
		link.addEventListener('click', (e) => {
			document.getElementById('nav-links').classList.remove('open');

			const href = link.getAttribute('href');
			if (!href || !href.startsWith('#')) return;

			const target = document.querySelector(href);
			if (!target) return;

			e.preventDefault();
			const navHeight = document.querySelector('nav').offsetHeight;
			const top = target.getBoundingClientRect().top + window.scrollY - navHeight - 16;
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

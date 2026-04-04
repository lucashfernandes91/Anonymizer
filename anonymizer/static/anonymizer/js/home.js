		// Scroll para resultado quando existir
		window.addEventListener('DOMContentLoaded', () => {
			const resultArea = document.getElementById('result-area');
			const hasResult = resultArea && resultArea.dataset.hasResult === 'true';
			if (hasResult) {
				const navHeight = document.querySelector('nav').offsetHeight;
				const top = resultArea.getBoundingClientRect().top + window.scrollY - navHeight - 16;
				window.scrollTo({ top, behavior: 'smooth' });
			}
		});

		// Fecha menu mobile ao clicar em link
		document.querySelectorAll('#nav-links .nav-link').forEach(link => {
			link.addEventListener('click', () => {
				document.getElementById('nav-links').classList.remove('open');
			});
		});

		const dropArea = document.getElementById("drop-area");
		const fileInput = document.getElementById("fileInput");
		const fileElem = document.getElementById("fileElem");
		const form = document.getElementById("uploadForm");

		fileElem.addEventListener("change", (e) => handleFiles(e.target.files));

		dropArea.addEventListener("click", (e) => {
			// Avoid double-trigger when clicking the inner button
			if (e.target.closest('button')) return;
			fileElem.click();
		});

		dropArea.addEventListener("dragover", (e) => {
			e.preventDefault();
			dropArea.classList.add("dragover");
		});

		dropArea.addEventListener("dragleave", () => {
			dropArea.classList.remove("dragover");
		});

		dropArea.addEventListener("drop", (e) => {
			e.preventDefault();
			dropArea.classList.remove("dragover");
			handleFiles(e.dataTransfer.files);
		});

		function handleFiles(files) {
			if (!files.length) return;
			const dt = new DataTransfer();
			dt.items.add(files[0]);
			fileInput.files = dt.files;
			form.submit();
		}

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

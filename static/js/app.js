document.addEventListener('DOMContentLoaded', function () {
    initMarkdownRendering();
    initAnimations();
    initFormEnhancements();
});

function initMarkdownRendering() {
    marked.setOptions({
        breaks: true,
        gfm: true,
        sanitize: false
    });


    const markdownElements = document.querySelectorAll('[data-markdown]');
    markdownElements.forEach(element => {
        const markdownText = element.getAttribute('data-markdown');
        if (markdownText) {
            element.innerHTML = marked.parse(markdownText);
        }
    });
}

function initAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.bg-white\\/80, .bg-white\\/60');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';

        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * index);
    });

    // Add hover effects to interactive elements
    const interactiveElements = document.querySelectorAll('button, .hover\\:scale-105');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function () {
            this.style.transform = 'scale(1.05)';
        });

        element.addEventListener('mouseleave', function () {
            this.style.transform = 'scale(1)';
        });
    });
}

function initFormEnhancements() {
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function () {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<i class="ph ph-spinner animate-spin mr-2"></i>Processing...';
                submitButton.disabled = true;

                setTimeout(() => {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }, 10000);
            }
        });
    });
}

function createWeatherAnimation(weatherType) {
    const animations = {
        'sunny': '☀️',
        'cloudy': '☁️',
        'rainy': '🌧️',
        'stormy': '⛈️',
        'snowy': '❄️',
        'misty': '🌫️'
    };

    return animations[weatherType] || '🌤️';
}

function smoothScrollTo(element) {
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.innerHTML = '';

    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}

function formatTimeAgo(timestamp) {
    const now = new Date();
    const time = new Date(timestamp);
    const diff = Math.floor((now - time) / 1000);

    if (diff < 60) return 'just now';
    if (diff < 3600) return `${Math.floor(diff / 60)} minutes ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)} hours ago`;
    return `${Math.floor(diff / 86400)} days ago`;
}

const SoulWeatherStorage = {
    save: function (key, data) {
        try {
            localStorage.setItem(`soulweather_${key}`, JSON.stringify(data));
        } catch (e) {
            console.warn('Could not save to localStorage:', e);
        }
    },

    load: function (key) {
        try {
            const data = localStorage.getItem(`soulweather_${key}`);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.warn('Could not load from localStorage:', e);
            return null;
        }
    },

    remove: function (key) {
        try {
            localStorage.removeItem(`soulweather_${key}`);
        } catch (e) {
            console.warn('Could not remove from localStorage:', e);
        }
    }
};

window.SoulWeather = {
    createWeatherAnimation,
    smoothScrollTo,
    typeWriter,
    formatTimeAgo,
    Storage: SoulWeatherStorage
};

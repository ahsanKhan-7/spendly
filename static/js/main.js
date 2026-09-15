// main.js — students will add JavaScript here as features are built

document.addEventListener('DOMContentLoaded', function () {
    var trigger = document.getElementById('how-it-works-btn');
    var modal = document.getElementById('video-modal');
    var closeBtn = document.getElementById('video-modal-close');
    var iframe = document.getElementById('video-modal-iframe');
    var videoUrl = 'https://www.youtube.com/embed/dQw4w9WgXcQ';

    if (!trigger || !modal || !closeBtn || !iframe) {
        return;
    }

    function openModal() {
        iframe.src = videoUrl + '?autoplay=1';
        modal.classList.add('is-open');
    }

    function closeModal() {
        modal.classList.remove('is-open');
        iframe.src = '';
    }

    trigger.addEventListener('click', function (e) {
        e.preventDefault();
        openModal();
    });

    closeBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('is-open')) {
            closeModal();
        }
    });
});

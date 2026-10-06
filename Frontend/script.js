const API = "https://room-zero-website-seven.vercel.app";
document.addEventListener('DOMContentLoaded', function () {

    // ---------- Single-page navigation ----------
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');

    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                // Only handle internal section navigation
                e.preventDefault();
                const targetId = href.substring(1);
                sections.forEach(section => section.classList.remove('active'));
                const targetSection = document.getElementById(targetId);
                if (targetSection) targetSection.classList.add('active');

                navLinks.forEach(nav => nav.classList.remove('active'));
                this.classList.add('active');
            }
            // Otherwise, let the browser navigate to another page
        });
    });

    // ---------- Booking modal ----------
    const modal = document.getElementById('booking-modal');
    const form = document.getElementById('booking-form');

    // about.html and reviews.html have no booking modal, so stop here on those pages
    if (!modal || !form) return;

    const closeBtn = document.querySelector('.close');
    const bookBtns = document.querySelectorAll('.book-btn');
    const successMsg = document.getElementById('success-message');
    const modalTitle = document.getElementById('modal-title');
    const errorBox = document.getElementById('error-message');
    let selectedRoomId = null;

    // Open the modal for the clicked room
    bookBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const card = this.closest('.room-card');
            selectedRoomId = parseInt(card.getAttribute('data-room-id'));
            modalTitle.textContent = `Room: ${card.getAttribute('data-room')}`;
            errorBox.textContent = '';
            successMsg.classList.add('hidden');
            form.style.display = 'flex';
            modal.style.display = 'block';
        });
    });

    // Close the modal
    closeBtn.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function (e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Submit the booking to the API
    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        errorBox.textContent = '';

        const data = {
            room_id: selectedRoomId,
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            date: document.getElementById('date').value,
            time_slot: document.getElementById('time').value,
            players: parseInt(document.getElementById('players').value),
        };

        try {
            const res = await fetch(`${API}/bookings`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            const result = await res.json();

            if (res.ok) {
                successMsg.textContent = `BOOKING INITIATED! ID: ${result.id}`;
                form.style.display = 'none';
                successMsg.classList.remove('hidden');
                form.reset();
                setTimeout(() => {
                    modal.style.display = 'none';
                }, 2500);
            } if (Array.isArray(result.detail)) {
    errorBox.textContent = result.detail
        .map(d => `${d.loc[d.loc.length - 1]}: ${d.msg}`)
        .join(' | ');
} else {
    errorBox.textContent = result.detail || 'Booking failed';
}
        } catch (err) {
            errorBox.textContent = 'Cannot reach the server. Is the API running?';
        }
    });
});
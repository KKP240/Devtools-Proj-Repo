// frontend/public/js/write_review.js
document.addEventListener('DOMContentLoaded', async () => {
    const form = document.getElementById('review-form');
    const messageDiv = document.getElementById('form-message');
    const targetP = document.getElementById('review-target');
    const token = localStorage.getItem('accessToken');
    if (!token) { window.location.href = '/login.html'; return; }

    const urlParams = new URLSearchParams(window.location.search);
    const bookingId = urlParams.get('booking_id');
    if (!bookingId) {
        messageDiv.textContent = 'Booking ID not found in URL.';
        return;
    }

    // ดึงข้อมูล booking มาแสดงว่ารีวิวใคร
    try {
        const response = await fetch(`http://localhost:8003/api/bookings/${bookingId}/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const booking = await response.json();
        targetP.textContent = `You are reviewing the service for Booking ID: ${booking.id} provided by Caregiver ID: ${booking.caregiver_id}`;
    } catch(e) {
        targetP.textContent = 'Could not load booking details.';
    }

    // จัดการระบบดาว
    const stars = document.querySelectorAll('#rating-stars span');
    const ratingInput = document.getElementById('rating-input');
    stars.forEach(star => {
        star.addEventListener('click', () => {
            const value = star.getAttribute('data-value');
            ratingInput.value = value;
            stars.forEach(s => {
                s.textContent = s.getAttribute('data-value') <= value ? '★' : '☆';
            });
        });
    });
    
    // จัดการการ Submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        messageDiv.textContent = 'Submitting...';

        const data = {
            booking_id: bookingId,
            rating: form.rating.value,
            comment: form.comment.value,
        };
        
        if (!data.rating) {
            messageDiv.textContent = 'Please select a rating.';
            messageDiv.className = 'text-red-500';
            return;
        }

        try {
            const response = await fetch(`http://localhost:8003/api/reviews/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                messageDiv.textContent = 'Review submitted successfully!';
                messageDiv.className = 'text-green-500';
                setTimeout(() => window.location.href = '/my_bookings.html', 2000);
            } else {
                 const error = await response.json();
                 messageDiv.textContent = `Error: ${JSON.stringify(error)}`;
                 messageDiv.className = 'text-red-500';
            }
        } catch (e) {
             messageDiv.textContent = 'An error occurred.';
             messageDiv.className = 'text-red-500';
        }
    });
});
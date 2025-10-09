// frontend/public/js/booking_list.js
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('caregiver-bookings-container');
    const token = localStorage.getItem('accessToken');

    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    try {
        // ยิง API ไปยัง booking_service เพื่อขอดูงานของตัวเอง
        const response = await fetch('http://localhost:8003/api/bookings/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const bookings = await response.json();

        container.innerHTML = ''; // เคลียร์ "Loading..."

        if (bookings.length === 0) {
            container.innerHTML = '<p>You have no assigned jobs.</p>';
            return;
        }

        bookings.forEach(booking => {
            const bookingCard = document.createElement('div');
            bookingCard.className = 'bg-white p-4 shadow rounded mb-4';

            // เราไม่สามารถรู้ชื่อ Job หรือ Pet ได้จาก API นี้
            // เราต้องยิง API ไปถาม Service อื่นๆ เพิ่มเติม
            // แต่เบื้องต้น เราจะแสดงแค่ ID ไปก่อน
            bookingCard.innerHTML = `
                <p><strong>Booking ID:</strong> ${booking.id}</p>
                <p><strong>Pet ID:</strong> ${booking.pet_id}</p>
                <p><strong>Owner ID:</strong> ${booking.owner_id}</p>
                <p><strong>Status:</strong> ${booking.status}</p>
                `;
            container.appendChild(bookingCard);
        });

    } catch (error) {
        console.error('Failed to fetch jobs:', error);
        container.innerHTML = '<p class="text-red-500">Error loading your jobs.</p>';
    }
});
// frontend/public/js/booking_detail.js
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('booking-detail-container');
    const token = localStorage.getItem('accessToken');

    // 1. ดึง booking ID มาจาก URL (เช่น .../booking_detail.html?id=5)
    const urlParams = new URLSearchParams(window.location.search);
    const bookingId = urlParams.get('id');

    if (!bookingId) {
        container.innerHTML = '<p class="text-red-500">Booking ID not found in URL.</p>';
        return;
    }

    try {
        // 2. ยิง API ไปขอข้อมูล Booking เฉพาะ ID นี้
        const response = await fetch(`http://localhost:8003/api/bookings/${bookingId}/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const booking = await response.json();

        // 3. นำข้อมูลที่ได้มาสร้างเป็น HTML
        // (ในระบบจริง เราจะต้องยิง API ไป service อื่นๆ เพื่อเอาชื่อ caregiver, pet, job title มาเพิ่ม)
        container.innerHTML = `
            <h2 class="text-2xl font-semibold mb-4">Booking Details (ID: ${booking.id})</h2>
            <p class="text-gray-600 mb-2"><strong>Caregiver ID:</strong> ${booking.caregiver_id}</p>
            <p class="text-gray-600 mb-2"><strong>Pet ID:</strong> ${booking.pet_id}</p>
            <p class="text-gray-600 mb-2"><strong>Status:</strong> ${booking.status}</p>
            <p class="text-gray-600 mb-2"><strong>Start:</strong> ${new Date(booking.start).toLocaleString()}</p>
            <p class="text-gray-600 mb-4"><strong>End:</strong> ${new Date(booking.end).toLocaleString()}</p>
        `;
    } catch (error) {
        console.error('Failed to fetch booking details:', error);
        container.innerHTML = '<p class="text-red-500">Error loading booking details.</p>';
    }
});
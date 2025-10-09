// frontend/public/js/my_bookings.js
document.addEventListener('DOMContentLoaded', async () => {
    const ownerContainer = document.getElementById('owner-bookings-container');
    const caregiverContainer = document.getElementById('caregiver-bookings-container');
    const token = localStorage.getItem('accessToken');
    if (!token) { window.location.href = '/login.html'; return; }

    const headers = { 'Authorization': `Bearer ${token}` };

    try {
        // 1. ดึงข้อมูล User ID ปัจจุบัน
        const meResponse = await fetch('http://localhost:8001/api/me/', { headers });
        const currentUser = await meResponse.json();
        const currentUserId = currentUser.id;

        // 2. ดึงข้อมูล Booking ทั้งหมดที่เกี่ยวข้อง
        const bookingsResponse = await fetch('http://localhost:8003/api/bookings/', { headers });
        const bookings = await bookingsResponse.json();

        ownerContainer.innerHTML = '';
        caregiverContainer.innerHTML = '';

        const ownerBookings = bookings.filter(b => b.owner_id === currentUserId);
        const caregiverBookings = bookings.filter(b => b.caregiver_id === currentUserId);

        // 3. แสดงผลส่วนของ Owner
        if (ownerBookings.length === 0) {
            ownerContainer.innerHTML = '<p>You have no bookings as a pet owner.</p>';
        } else {
            ownerBookings.forEach(booking => {
                const item = document.createElement('div');
                item.className = 'bg-white shadow rounded p-4';
                item.innerHTML = `
                    <p><strong>Booking ID:</strong> ${booking.id}</p>
                    <p><strong>Caregiver ID:</strong> ${booking.caregiver_id}</p>
                    <p><strong>Pet ID:</strong> ${booking.pet_id}</p>
                    <p><strong>Status:</strong> ${booking.status}</p>
                    ${booking.status === 'D' ? `<a href="/write_review.html?booking_id=${booking.id}" class="text-blue-500">Write a Review</a>` : ''}
                `;
                ownerContainer.appendChild(item);
            });
        }
        
        // 4. แสดงผลส่วนของ Caregiver
        if (caregiverBookings.length === 0) {
            caregiverContainer.innerHTML = '<p>You have no jobs as a caregiver.</p>';
        } else {
            caregiverBookings.forEach(booking => {
                 const item = document.createElement('div');
                item.className = 'bg-white shadow rounded p-4';
                item.innerHTML = `
                    <p><strong>Booking ID:</strong> ${booking.id}</p>
                    <p><strong>Owner ID:</strong> ${booking.owner_id}</p>
                    <p><strong>Pet ID:</strong> ${booking.pet_id}</p>
                    <p><strong>Status:</strong> ${booking.status}</p>
                `;
                caregiverContainer.appendChild(item);
            });
        }

    } catch (e) {
        console.error("Error fetching bookings:", e);
        ownerContainer.innerHTML = '<p class="text-red-500">Error loading data.</p>';
        caregiverContainer.innerHTML = '<p class="text-red-500">Error loading data.</p>';
    }
});
// frontend/public/js/booking_history.js
document.addEventListener('DOMContentLoaded', async () => {
    const tableBody = document.getElementById('booking-history-table-body');
    const token = localStorage.getItem('accessToken'); // ดึง Token ที่เก็บไว้ตอน Login

    if (!token) {
        window.location.href = '/login.html'; // ถ้ายังไม่ Login ให้ไปหน้า Login
        return;
    }

    try {
        const response = await fetch('http://localhost:8003/api/bookings/', { // ยิงไปที่ booking_service
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const bookings = await response.json();

        tableBody.innerHTML = ''; // เคลียร์ "Loading..."

        bookings.forEach(booking => {
            const row = document.createElement('tr');
            row.className = 'border-b border-gray-200';
            row.innerHTML = `
                <td class="p-4 text-sm text-gray-700">${booking.id}</td>
                <td class="p-4 text-sm text-gray-700">${booking.caregiver_id}</td>
                <td class="p-4 text-sm text-gray-700">${booking.pet_id}</td>
                <td class="p-4 text-sm text-gray-700">${new Date(booking.start).toLocaleString()}</td>
                <td class="p-4 text-sm text-gray-700">${new Date(booking.end).toLocaleString()}</td>
                <td class="p-4 text-sm text-gray-700">${booking.status}</td>
                <td class="p-4 text-sm text-gray-700">
                    </td>
            `;
            tableBody.appendChild(row);
        });

    } catch (error) {
        console.error('Failed to fetch booking history:', error);
        tableBody.innerHTML = '<tr><td colspan="7" class="text-center p-4 text-red-500">Error loading data.</td></tr>';
    }
});
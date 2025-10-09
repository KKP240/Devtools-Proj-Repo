// frontend/public/js/caregiver_list.js
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('caregiver-list-container');
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');

    // ฟังก์ชันสำหรับดึงและแสดงข้อมูล Caregiver
    async function fetchAndDisplayCaregivers(searchQuery = '') {
        container.innerHTML = '<li class="p-4 bg-white rounded shadow text-gray-500">Loading caregivers...</li>';
        
        try {
            // 1. ยิง API ไปที่ user_service เพื่อขอข้อมูล User ทั้งหมด
            // ถ้ามีการค้นหา ให้ส่ง query parameter ไปด้วย
            const apiUrl = `http://localhost:8001/api/users/?search=${searchQuery}`;
            const response = await fetch(apiUrl);
            const users = await response.json();

            // 2. กรองเฉพาะ User ที่มีโปรไฟล์ Caregiver
            const caregivers = users.filter(user => user.caregiver_profile);
            
            container.innerHTML = ''; // เคลียร์ Loading...

            if (caregivers.length === 0) {
                container.innerHTML = '<li>No caregivers found.</li>';
                return;
            }

            // 3. วนลูปและสร้าง HTML สำหรับแต่ละ Caregiver
            caregivers.forEach(user => {
                const caregiver = user.caregiver_profile;
                const li = document.createElement('li');
                li.className = 'p-4 bg-white rounded shadow';
                li.innerHTML = `
                    <a href="/caregiver_detail.html?id=${user.id}" class="text-lg font-medium text-indigo-600 hover:underline">${user.username}</a>
                    <div class="text-sm text-gray-500">Area: ${caregiver.area || 'N/A'} — Rate ฿${caregiver.hourly_rate || '0.00'}</div>
                `;
                container.appendChild(li);
            });

        } catch (error) {
            console.error('Failed to fetch caregivers:', error);
            container.innerHTML = '<li class="text-red-500">Error loading caregivers.</li>';
        }
    }

    // จัดการการค้นหา
    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        fetchAndDisplayCaregivers(searchInput.value);
    });

    // โหลดข้อมูลทั้งหมดในครั้งแรก
    fetchAndDisplayCaregivers();
});
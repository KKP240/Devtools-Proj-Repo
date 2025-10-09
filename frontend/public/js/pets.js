// frontend/public/js/my_pets.js
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('pets-container');
    const token = localStorage.getItem('accessToken');

    // ตรวจสอบว่าล็อกอินแล้วหรือยัง
    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    try {
        // 1. ยิง API ไปที่ pet_service เพื่อขอข้อมูลสัตว์เลี้ยงของ user ที่ล็อกอินอยู่
        const response = await fetch('http://localhost:8002/api/pets/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const pets = await response.json();

        container.innerHTML = ''; // เคลียร์ข้อความ "Loading..."

        if (pets.length === 0) {
            container.innerHTML = '<p>You have not added any pets yet.</p>';
            return;
        }

        // 2. วนลูปข้อมูลที่ได้มา แล้วสร้าง HTML สำหรับการ์ดแต่ละใบ
        pets.forEach(pet => {
            const card = document.createElement('div');
            card.className = 'bg-white rounded-lg shadow-md overflow-hidden';
            
            card.innerHTML = `
                <div class="h-48 bg-gray-100 flex items-center justify-center">
                    ${pet.photo ? 
                        `<img src="${pet.photo}" alt="${pet.name}" class="h-full w-full object-cover">` : 
                        '<span class="text-gray-400">No Photo</span>'
                    }
                </div>
                <div class="p-4">
                    <h2 class="text-lg font-semibold text-gray-800">${pet.name}</h2>
                    <p class="text-sm text-gray-500">Species: ${pet.species}</p>
                    ${pet.age ? `<p class="text-sm text-gray-500">Age: ${pet.age} year(s)</p>` : ''}
                    <p class="text-gray-600 text-sm mt-2">${pet.notes || 'No notes.'}</p>
                </div>
                <div class="p-4 bg-gray-50 border-t">
                    <a href="#" class="text-sm text-blue-500 hover:underline">Edit</a>
                </div>
            `;
            container.appendChild(card);
        });

    } catch (error) {
        console.error('Failed to fetch pets:', error);
        container.innerHTML = '<p class="text-red-500">Error loading your pets.</p>';
    }
});
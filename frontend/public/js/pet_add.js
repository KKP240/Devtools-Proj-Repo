// frontend/public/js/pet_add.js
document.addEventListener('DOMContentLoaded', () => {
    const petForm = document.getElementById('pet-form');
    const messageDiv = document.getElementById('form-message');
    const token = localStorage.getItem('accessToken');

    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    petForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        messageDiv.textContent = 'Saving pet...';
        messageDiv.className = 'text-blue-500';

        // รวบรวมข้อมูลจากฟอร์ม
        const formData = new FormData(petForm);
        const data = {
            name: formData.get('name'),
            species: formData.get('species'),
            age: formData.get('age') || null,
            notes: formData.get('notes'),
            photo: formData.get('photo'),
        };

        try {
            // ยิง API แบบ POST ไปที่ pet_service
            const response = await fetch('http://localhost:8002/api/pets/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                messageDiv.textContent = 'Pet added successfully! Redirecting...';
                messageDiv.className = 'text-green-500';
                setTimeout(() => {
                    window.location.href = '/my_pets.html'; // กลับไปหน้าแสดงรายการสัตว์เลี้ยง
                }, 2000);
            } else {
                const errorData = await response.json();
                messageDiv.textContent = `Error: ${JSON.stringify(errorData)}`;
                messageDiv.className = 'text-red-500';
            }
        } catch (error) {
            console.error('Failed to add pet:', error);
            messageDiv.textContent = 'An unexpected error occurred.';
            messageDiv.className = 'text-red-500';
        }
    });
});
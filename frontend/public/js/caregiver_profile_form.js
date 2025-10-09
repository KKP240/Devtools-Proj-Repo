// frontend/public/js/caregiver_profile_form.js
document.addEventListener('DOMContentLoaded', async () => {
    const form = document.getElementById('caregiver-form');
    const formMessage = document.getElementById('form-message');
    const token = localStorage.getItem('accessToken');

    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    const weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const checkboxContainer = document.getElementById('available-days-checkboxes');
    weekdays.forEach(day => {
        checkboxContainer.innerHTML += `
            <label class="inline-flex items-center">
                <input type="checkbox" name="available_days" value="${day}" class="rounded">
                <span class="ml-2">${day}</span>
            </label>
        `;
    });

    // 1. ดึงข้อมูลโปรไฟล์เดิมมาแสดงในฟอร์ม
    try {
        const response = await fetch('http://localhost:8001/api/me/', {
             headers: { 'Authorization': `Bearer ${token}` }
        });
        const userData = await response.json();
        
        if (userData.caregiver_profile) {
            const profile = userData.caregiver_profile;
            document.getElementById('bio').value = profile.bio || '';
            document.getElementById('hourly_rate').value = profile.hourly_rate || '';
            document.getElementById('area').value = profile.area || '';
            
            // ติ๊ก checkbox ตามข้อมูลเดิม
            document.querySelectorAll('input[name="available_days"]').forEach(checkbox => {
                if (profile.available_days.includes(checkbox.value)) {
                    checkbox.checked = true;
                }
            });
        }
    } catch (e) {
        console.error("Could not fetch existing profile", e);
    }


    // 2. จัดการตอนกด Submit
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        formMessage.textContent = 'Saving...';

        const formData = new FormData(form);
        const data = {
            bio: formData.get('bio'),
            hourly_rate: formData.get('hourly_rate'),
            area: formData.get('area'),
            available_days: formData.getAll('available_days') // ดึงค่าจาก checkbox ทั้งหมด
        };
        
        // เราต้องส่งข้อมูลทั้งหมดของ user ไปด้วย
        const requestBody = {
            caregiver_profile: data
        };

        try {
            // ยิง API แบบ PUT ไปที่ user_service เพื่ออัปเดตโปรไฟล์
            const response = await fetch('http://localhost:8001/api/me/', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(requestBody)
            });

            if (response.ok) {
                formMessage.textContent = 'Profile saved successfully!';
                formMessage.className = 'text-green-500';
            } else {
                const errorData = await response.json();
                formMessage.textContent = `Error: ${JSON.stringify(errorData)}`;
                formMessage.className = 'text-red-500';
            }
        } catch (error) {
            console.error('Failed to save profile:', error);
            formMessage.textContent = 'An unexpected error occurred.';
            formMessage.className = 'text-red-500';
        }
    });
});
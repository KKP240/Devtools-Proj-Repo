document.addEventListener('DOMContentLoaded', async () => {
    // 1. หา Element ที่จำเป็นทั้งหมด
    const profileForm = document.getElementById('profile-form');
    const formMessage = document.getElementById('form-message');
    const caregiverSection = document.getElementById('caregiver-section');

    // 2. ตรวจสอบการล็อกอิน
    const token = localStorage.getItem('accessToken');
    if (!token) {
        // ถ้ายังไม่ล็อกอิน, ให้กลับไปหน้า login ทันที
        window.location.href = '/login.html';
        return;
    }

    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };

    // --- ส่วนของการดึงข้อมูลเก่ามาแสดง ---
    try {
        // 3. ยิง GET request ไปที่ /api/me/ เพื่อดึงข้อมูลโปรไฟล์ปัจจุบัน
        const response = await fetch('http://localhost:8001/api/me/', { headers });
        if (!response.ok) {
            throw new Error('Could not fetch profile data.');
        }
        const user = await response.json();

        // 4. นำข้อมูล User หลักมาใส่ในฟอร์ม
        document.getElementById('username').value = user.username || '';
        document.getElementById('email').value = user.email || '';
        // สามารถเพิ่ม first_name, last_name ได้ถ้ามีในฟอร์ม

        // 5. ตรวจสอบว่ามีโปรไฟล์ Caregiver หรือไม่
        if (user.caregiver_profile) {
            const profile = user.caregiver_profile;
            // สร้างฟอร์มสำหรับ Caregiver ขึ้นมา
            caregiverSection.innerHTML = `
                <legend class="font-semibold px-2">Caregiver Profile</legend>
                <div class="space-y-4 mt-2">
                    <div>
                        <label for="bio" class="block text-sm">Bio / About Me</label>
                        <textarea id="bio" name="bio" rows="4" class="mt-1 w-full border rounded-md px-3 py-2">${profile.bio || ''}</textarea>
                    </div>
                    <div>
                        <label for="hourly_rate" class="block text-sm">Hourly Rate (฿)</label>
                        <input type="number" id="hourly_rate" name="hourly_rate" value="${profile.hourly_rate || ''}" step="0.01" class="mt-1 w-full border rounded-md px-3 py-2">
                    </div>
                    <div>
                        <label for="area" class="block text-sm">Area</label>
                        <input type="text" id="area" name="area" value="${profile.area || ''}" class="mt-1 w-full border rounded-md px-3 py-2">
                    </div>
                </div>
            `;
        } else {
            // ถ้ายังไม่มีโปรไฟล์ Caregiver, อาจจะแสดงปุ่มให้สมัคร
            caregiverSection.innerHTML = `
                <legend class="font-semibold px-2">Caregiver Profile</legend>
                <p class="text-gray-500 mt-2">You are not registered as a caregiver yet.</p>
                <a href="/caregiver_profile_form.html" class="text-blue-500 hover:underline">Become a Caregiver</a>
            `;
        }

    } catch (error) {
        console.error("Error loading profile:", error);
        formMessage.textContent = 'Failed to load your profile data.';
        formMessage.className = 'text-red-500';
    }

    // --- ส่วนของการส่งข้อมูลที่แก้ไขแล้ว ---
    profileForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        formMessage.textContent = 'Saving changes...';
        formMessage.className = 'text-blue-500';

        // 6. รวบรวมข้อมูลจากฟอร์มทั้งหมด
        const formData = new FormData(profileForm);
        
        // ข้อมูลหลักของ User
        const userData = {
            username: formData.get('username'),
            email: formData.get('email'),
            // สามารถเพิ่ม first_name, last_name ได้
        };

        // ข้อมูลของ Caregiver (ถ้ามี)
        const caregiverData = {
            bio: formData.get('bio'),
            hourly_rate: formData.get('hourly_rate'),
            area: formData.get('area'),
        };

        // 7. สร้าง Body ที่จะส่งไป API ให้ตรงกับที่ Serializer ต้องการ
        const requestBody = {
            ...userData,
            caregiver_profile: caregiverData
        };

        try {
            // 8. ยิง PUT request ไปที่ /api/me/ เพื่ออัปเดตข้อมูล
            const response = await fetch('http://localhost:8001/api/me/', {
                method: 'PUT',
                headers: headers,
                body: JSON.stringify(requestBody)
            });

            if (response.ok) {
                formMessage.textContent = 'Profile updated successfully!';
                formMessage.className = 'text-green-500';
            } else {
                const errorData = await response.json();
                let errorMessage = 'Failed to save. ';
                for (const key in errorData) {
                    errorMessage += ` ${key}: ${errorData[key]}`;
                }
                formMessage.textContent = errorMessage;
                formMessage.className = 'text-red-500';
            }
        } catch (error) {
            console.error("Error saving profile:", error);
            formMessage.textContent = 'An unexpected error occurred while saving.';
            formMessage.className = 'text-red-500';
        }
    });
});
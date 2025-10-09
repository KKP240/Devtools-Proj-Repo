// frontend/public/js/job_post_create.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('job-post-form');
    const messageDiv = document.getElementById('form-message');
    const token = localStorage.getItem('accessToken');

    if (!token) {
        window.location.href = '/login.html';
        return;
    }
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        messageDiv.textContent = 'Submitting...';
        messageDiv.className = 'text-blue-500';
        messageDiv.classList.remove('hidden');

        try {
            // --- ขั้นตอนที่ 1: สร้าง Pet ก่อน ---
            const petData = {
                name: form.pet_name.value,
                species: form.pet_species.value,
                age: form.pet_age.value || null,
            };

            const petResponse = await fetch('http://localhost:8002/api/pets/', {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(petData)
            });

            if (!petResponse.ok) throw new Error('Failed to create pet.');
            
            const newPet = await petResponse.json();
            const newPetId = newPet.id;

            // --- ขั้นตอนที่ 2: สร้าง Job Post โดยใช้ ID ของ Pet ที่เพิ่งสร้าง ---
            const jobData = {
                pet_id: newPetId,
                title: form.job_title.value,
                description: form.job_description.value,
                start: form.job_start.value,
                end: form.job_end.value,
            };
            
            const jobResponse = await fetch('http://localhost:8004/api/job-posts/', {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(jobData)
            });

            if (!jobResponse.ok) throw new Error('Failed to create job post.');

            messageDiv.textContent = 'Job post created successfully! Redirecting...';
            messageDiv.className = 'text-green-500';

            setTimeout(() => {
                window.location.href = '/'; // กลับไปหน้าแรก
            }, 2000);

        } catch (error) {
            console.error('Error creating job post:', error);
            messageDiv.textContent = error.message;
            messageDiv.className = 'text-red-500';
        }
    });
});
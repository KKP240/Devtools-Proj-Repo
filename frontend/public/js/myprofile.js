// frontend/public/js/myprofile.js
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    const headers = { 'Authorization': `Bearer ${token}` };

    // 1. ดึงข้อมูล User หลัก
    fetch('http://localhost:8001/api/me/', { headers })
        .then(res => res.json())
        .then(user => {
            const header = document.getElementById('profile-header');
            header.innerHTML = `
                <h1 class="text-2xl font-semibold">${user.username}</h1>
                <p class="text-gray-600">${user.email}</p>
                <a href="/edit_profile.html" class="text-sm text-blue-500 hover:underline">Edit Profile</a>
            `;
        });
    
    // 2. ดึงข้อมูลสัตว์เลี้ยง
    fetch('http://localhost:8002/api/pets/', { headers })
        .then(res => res.json())
        .then(pets => {
            const section = document.getElementById('my-pets-section');
            section.innerHTML = '<h3 class="text-lg font-semibold text-gray-800 mb-2">My Pets</h3>';
            if (pets.length > 0) {
                const list = document.createElement('ul');
                pets.forEach(pet => {
                    const item = document.createElement('li');
                    item.textContent = `${pet.name} (${pet.species})`;
                    list.appendChild(item);
                });
                section.appendChild(list);
            } else {
                section.innerHTML += '<p>You have no pets.</p>';
            }
        });

    // 3. ดึงข้อมูล Job Posts (ต้องสร้าง API endpoint เพิ่ม)
    // สมมติว่า job_post_service มี /api/job-posts/mine/
    fetch('http://localhost:8004/api/job-posts/mine/', { headers })
        .then(res => res.json())
        .then(posts => {
            const section = document.getElementById('my-posts-section');
            section.innerHTML = '<h3 class="text-lg font-semibold text-gray-800 mb-2">My Job Posts</h3>';
            if (posts.length > 0) {
                 const list = document.createElement('ul');
                posts.forEach(post => {
                    const item = document.createElement('li');
                    item.textContent = post.title;
                    list.appendChild(item);
                });
                section.appendChild(list);
            } else {
                section.innerHTML += '<p>You have no job posts.</p>';
            }
        });
});
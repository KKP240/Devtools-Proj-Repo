// frontend/public/js/myposts.js
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('my-posts-container');
    const token = localStorage.getItem('accessToken');
    if (!token) { window.location.href = '/login.html'; return; }

    try {
        // API นี้ต้องสร้างเพิ่มใน job_post_service เพื่อ filter เฉพาะ post ของ user ที่ login
        const response = await fetch('http://localhost:8004/api/job-posts/mine/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const posts = await response.json();

        container.innerHTML = '';
        if (posts.length === 0) {
            container.innerHTML = '<p>You have no job posts yet.</p>';
            return;
        }

        posts.forEach(post => {
            const item = document.createElement('div');
            item.className = 'bg-white shadow rounded-lg p-6';
            item.innerHTML = `
                <div class="flex justify-between items-start">
                    <div>
                        <h2 class="text-xl font-semibold">${post.title}</h2>
                        <p class="text-sm text-gray-600">Status: ${post.status}</p>
                    </div>
                    <div class="space-x-2">
                        <a href="/job_post_edit.html?id=${post.id}" class="px-3 py-1.5 bg-blue-500 text-white rounded text-sm">Edit</a>
                        <button data-id="${post.id}" class="delete-btn px-3 py-1.5 bg-red-500 text-white rounded text-sm">Delete</button>
                    </div>
                </div>
            `;
            container.appendChild(item);
        });
    } catch (e) {
        container.innerHTML = '<p class="text-red-500">Error loading your posts.</p>';
    }
});
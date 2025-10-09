// frontend/public/js/index.js

// ฟังก์ชันหลักของหน้านี้
function initIndexPage() {
    const container = document.getElementById('job-posts-container');
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');

    if (!container) return; // ถ้าไม่เจอ container ให้หยุดทำงาน

    async function fetchJobs(query = '') {
        container.innerHTML = '<p>Loading...</p>';
        try {
            const response = await fetch(`/api/job-posts/?search=${query}`); // URL ผ่าน Gateway
            const posts = await response.json();

            container.innerHTML = '';
            if (posts.length === 0) {
                container.innerHTML = '<p>No job posts found.</p>';
                return;
            }

            posts.forEach(post => {
                const card = document.createElement('div');
                card.className = 'bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow';
                card.innerHTML = `
                    <a href="/job_post_detail.html?id=${post.id}">
                        <div class="h-48 bg-gray-100 flex items-center justify-center">
                            <span class="text-gray-400">Pet Photo</span>
                        </div>
                        <div class="p-4">
                            <h3 class="text-lg font-semibold text-gray-800">${post.title}</h3>
                            <p class="text-sm text-gray-500">Pet ID: ${post.pet_id}</p>
                            <p class="text-sm text-gray-500">Owner ID: ${post.owner_id}</p>
                        </div>
                    </a>
                `;
                container.appendChild(card);
            });
        } catch (error) {
            container.innerHTML = '<p class="text-red-500">Error loading job posts.</p>';
        }
    }

    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            fetchJobs(searchInput.value);
        });
    }

    fetchJobs(); // โหลดครั้งแรก
}

// รอให้ DOMContentLoaded ทำงานก่อนค่อยเรียกฟังก์ชันหลัก
document.addEventListener('DOMContentLoaded', initIndexPage);
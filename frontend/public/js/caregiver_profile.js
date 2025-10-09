// frontend/public/js/caregiver_profile.js
document.addEventListener('DOMContentLoaded', async () => {
    const profileHeader = document.getElementById('profile-header');
    const bioSection = document.getElementById('profile-bio-section');
    const petsSection = document.getElementById('profile-pets-section');
    const reviewsSection = document.getElementById('profile-reviews-section');

    // 1. ดึง User ID ของโปรไฟล์ที่ต้องการดูจาก URL
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('id');

    if (!userId) {
        if (profileHeader) profileHeader.innerHTML = '<p class="text-red-500">User ID not found in URL.</p>';
        return;
    }

    // --- Fetch ข้อมูลหลัก (User + Caregiver Profile) ---
    try {
        const userResponse = await fetch(`/api/users/${userId}/`);
        if (!userResponse.ok) throw new Error('User not found');
        const user = await userResponse.json();

        if (!user.caregiver_profile) {
            if (profileHeader) profileHeader.innerHTML = `<h1 class="text-2xl font-semibold">${user.username} is not a caregiver.</h1>`;
            if (bioSection) bioSection.style.display = 'none';
            if (petsSection) petsSection.style.display = 'none';
            if (reviewsSection) reviewsSection.style.display = 'none';
            return;
        }
        
        const caregiver = user.caregiver_profile;

        // แสดงผลข้อมูล Header
        if (profileHeader) {
            profileHeader.innerHTML = `
                <div class="flex items-center gap-6">
                    <div class="w-28 h-28 rounded-full ring-4 ring-white bg-gray-300 flex-shrink-0"></div>
                    <div>
                        <h1 class="text-2xl font-semibold">${user.username}</h1>
                        <p class="text-gray-600">Area: ${caregiver.area || 'N/A'}</p>
                        <p class="text-gray-600">Rate: ฿${caregiver.hourly_rate || '0.00'}/hr</p>
                    </div>
                </div>
            `;
        }

        // แสดงผลข้อมูล Bio
        if (bioSection) {
            bioSection.innerHTML = `
                <h3 class="text-lg font-semibold text-gray-800 mb-2">About Me</h3>
                <p class="text-gray-600">${caregiver.bio || 'No bio provided.'}</p>
            `;
        }

        // หลังจากโหลดข้อมูลหลักเสร็จ ให้ไปดึงข้อมูลส่วนอื่นๆ ต่อ
        fetchUserPets(userId);
        fetchCaregiverReviews(userId);

    } catch (error) {
        console.error('Failed to fetch main profile:', error);
        if (profileHeader) profileHeader.innerHTML = '<p class="text-red-500">Error loading profile.</p>';
    }
});

// --- ฟังก์ชันสำหรับ Fetch ข้อมูลสัตว์เลี้ยง ---
async function fetchUserPets(ownerId) {
    const petsSection = document.getElementById('profile-pets-section');
    if (!petsSection) return;
    try {
        const response = await fetch(`/api/pets/?owner_id=${ownerId}`);
        const pets = await response.json();
        
        petsSection.innerHTML = '<h3 class="text-lg font-semibold text-gray-800 mb-2">My Pets</h3>';
        if (pets.length === 0) {
            petsSection.innerHTML += '<p class="text-gray-600">This user has not added any pets.</p>';
            return;
        }

        const petList = document.createElement('div');
        petList.className = 'grid grid-cols-2 md:grid-cols-4 gap-4';
        pets.forEach(pet => {
            petList.innerHTML += `<div class="border rounded p-2 text-center"><p class="font-semibold">${pet.name}</p><p class="text-sm text-gray-500">${pet.species}</p></div>`;
        });
        petsSection.appendChild(petList);

    } catch (error) {
        petsSection.innerHTML += '<p class="text-red-500">Could not load pets.</p>';
    }
}

// --- ฟังก์ชันสำหรับ Fetch ข้อมูลรีวิว ---
async function fetchCaregiverReviews(caregiverId) {
    const reviewsSection = document.getElementById('profile-reviews-section');
    if (!reviewsSection) return;
    try {
        const response = await fetch(`/api/reviews/?reviewee_id=${caregiverId}`);
        const reviews = await response.json();

        reviewsSection.innerHTML = '<h3 class="text-lg font-semibold text-gray-800 mb-2">Reviews</h3>';
        if (reviews.length === 0) {
            reviewsSection.innerHTML += '<p class="text-gray-600">No reviews yet.</p>';
            return;
        }

        const reviewList = document.createElement('div');
        reviewList.className = 'space-y-4';
        reviews.forEach(review => {
            reviewList.innerHTML += `<div class="border-t pt-4"><p class="font-bold">Rating: ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p><p class="text-gray-600 italic">"${review.comment}"</p></div>`;
        });
        reviewsSection.appendChild(reviewList);
        
    } catch (error) {
        reviewsSection.innerHTML += '<p class="text-red-500">Could not load reviews.</p>';
    }
}
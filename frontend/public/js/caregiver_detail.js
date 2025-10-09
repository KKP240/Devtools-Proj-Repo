// frontend/public/js/caregiver_detail.js
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('caregiver-detail-container');

    // 1. ดึง caregiver ID มาจาก URL (เช่น ...?id=5)
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('id');

    if (!userId) {
        container.innerHTML = '<p class="text-red-500">Caregiver ID not found in URL.</p>';
        return;
    }

    try {
        // 2. ยิง API ไปขอข้อมูล User (ที่มี profile) จาก user_service
        const userResponse = await fetch(`http://localhost:8001/api/users/${userId}/`);
        if (!userResponse.ok) throw new Error('User not found');
        const user = await userResponse.json();
        const caregiver = user.caregiver_profile;

        if (!caregiver) {
             container.innerHTML = '<p class="text-red-500">This user is not a caregiver.</p>';
             return;
        }

        // 3. นำข้อมูลที่ได้มาสร้างเป็น HTML
        container.innerHTML = `
            <h2 class="text-2xl font-semibold mb-2">${user.username}</h2>
            <p class="text-sm text-gray-500 mb-4">Area: ${caregiver.area || 'N/A'} — Rate: ฿${caregiver.hourly_rate || '0.00'}</p>
            <div class="mb-4">
              <h3 class="font-semibold">About</h3>
              <p class="text-gray-700">${caregiver.bio || 'No description provided.'}</p>
            </div>
            <div class="mb-6">
                <h3 class="font-semibold">Available Days</h3>
                <p class="text-gray-700">${caregiver.available_days.join(', ') || 'Not specified'}</p>
            </div>
            
            <div id="reviews-section">
                <h3 class="font-semibold mt-6">Reviews</h3>
                <p>Loading reviews...</p>
            </div>
        `;

        // 4. (ขั้นสูง) ยิง API ไปที่ booking_service เพื่อดึงรีวิว
        fetchReviews(userId);

    } catch (error) {
        console.error('Failed to fetch caregiver details:', error);
        container.innerHTML = '<p class="text-red-500">Error loading profile.</p>';
    }
});

async function fetchReviews(caregiverId) {
    const reviewsContainer = document.getElementById('reviews-section');
    try {
        // API นี้จะต้องถูกสร้างขึ้นใน booking_service เพื่อให้สามารถ query รีวิวจาก reviewee_id ได้
        const response = await fetch(`http://localhost:8003/api/reviews/?reviewee_id=${caregiverId}`);
        const reviews = await response.json();
        
        if(reviews.length > 0) {
            reviewsContainer.innerHTML = '<h3 class="font-semibold mt-6">Reviews</h3>';
            reviews.forEach(review => {
                const reviewEl = document.createElement('div');
                reviewEl.className = 'border-t mt-4 pt-4';
                reviewEl.innerHTML = `
                    <p class="font-bold">Rating: ${review.rating} / 5</p>
                    <p class="text-gray-600">"${review.comment}"</p>
                `;
                reviewsContainer.appendChild(reviewEl);
            });
        } else {
            reviewsContainer.innerHTML = '<h3 class="font-semibold mt-6">Reviews</h3><p>No reviews yet.</p>';
        }
    } catch(e) {
        reviewsContainer.innerHTML = '<h3 class="font-semibold mt-6">Reviews</h3><p>Could not load reviews.</p>';
    }
}
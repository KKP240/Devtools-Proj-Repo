// frontend/public/js/my_proposals.js
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('proposals-container');
    const token = localStorage.getItem('accessToken');
    if (!token) { window.location.href = '/login.html'; return; }

    try {
        // 1. ยิง API ไปที่ proposal_service
        const response = await fetch('http://localhost:8005/api/proposals/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const proposals = await response.json();

        container.innerHTML = '';
        if (proposals.length === 0) {
            container.innerHTML = '<p>You have not submitted any proposals yet.</p>';
            return;
        }

        // 2. วนลูปเพื่อแสดงผลแต่ละ Proposal
        for (const proposal of proposals) {
            const item = document.createElement('div');
            item.className = 'bg-white p-4 shadow rounded';
            
            // สร้าง HTML เริ่มต้น
            item.innerHTML = `
                <p><strong>Job Post ID:</strong> <a href="/job_post_detail.html?id=${proposal.job_post_id}" class="text-blue-600">${proposal.job_post_id}</a></p>
                <p><strong>Job Title:</strong> <span id="job-title-${proposal.id}">Loading...</span></p>
                <p><strong>Status:</strong> ${proposal.status}</p>
                <p><strong>Your Rate:</strong> ฿${proposal.proposed_rate}</p>
                <p><strong>Message:</strong> ${proposal.message}</p>
            `;
            container.appendChild(item);

            // 3. (ขั้นสูง) ยิง API ไปที่ job_post_service อีกครั้งเพื่อดึงชื่อ Job
            fetch(`http://localhost:8004/api/job-posts/${proposal.job_post_id}/`)
                .then(res => res.json())
                .then(jobPost => {
                    document.getElementById(`job-title-${proposal.id}`).textContent = jobPost.title;
                });
        }

    } catch (e) {
        console.error("Error fetching proposals:", e);
        container.innerHTML = '<p class="text-red-500">Error loading your proposals.</p>';
    }
});
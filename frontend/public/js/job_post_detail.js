// frontend/public/js/job_post_detail.js
document.addEventListener('DOMContentLoaded', async () => {
    const jobContainer = document.getElementById('job-detail-container');
    
    // ดึง Job ID จาก URL
    const urlParams = new URLSearchParams(window.location.search);
    const jobId = urlParams.get('id');

    if (!jobId) {
        jobContainer.innerHTML = '<p class="text-red-500">Job ID not found.</p>';
        return;
    }

    try {
        // --- API Call 1: ดึงข้อมูล Job Post หลัก ---
        const jobResponse = await fetch(`http://localhost:8004/api/job-posts/${jobId}/`);
        if (!jobResponse.ok) throw new Error('Job post not found.');
        const jobPost = await jobResponse.json();
        
        // แสดงข้อมูลเบื้องต้นก่อน
        jobContainer.innerHTML = `
            <h2 class="text-2xl font-semibold mb-4">${jobPost.title}</h2>
            <p class="text-gray-600 mb-4">${jobPost.description}</p>
            <div class="text-sm">
                <p><strong>Owner:</strong> <span id="owner-name">Loading...</span></p>
                <p><strong>Pet:</strong> <span id="pet-name">Loading...</span></p>
                <p><strong>Period:</strong> ${new Date(jobPost.start).toLocaleString()} to ${new Date(jobPost.end).toLocaleString()}</p>
                <p><strong>Status:</strong> ${jobPost.status}</p>
            </div>
        `;

        // --- API Call 2: ดึงข้อมูล Owner จาก user_service ---
        fetch(`http://localhost:8001/api/users/${jobPost.owner_id}/`)
            .then(res => res.json())
            .then(owner => {
                document.getElementById('owner-name').textContent = owner.username;
            });
            
        // --- API Call 3: ดึงข้อมูล Pet จาก pet_service ---
        // หมายเหตุ: API ของ pet_service ต้องอนุญาตให้ดูข้อมูล pet ของคนอื่นได้ด้วย ID
        fetch(`http://localhost:8002/api/pets/${jobPost.pet_id}/`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('accessToken')}` } // ต้อง Login
        })
            .then(res => res.json())
            .then(pet => {
                document.getElementById('pet-name').textContent = `${pet.name} (${pet.species})`;
            });

        // --- API Call 4: ดึงข้อมูล Proposals จาก proposal_service ---
        fetchProposals(jobId);
        
        // --- จัดการฟอร์มส่ง Proposal ---
        setupProposalForm(jobId);

    } catch (error) {
        console.error('Error fetching job details:', error);
        jobContainer.innerHTML = `<p class="text-red-500">${error.message}</p>`;
    }
});

async function fetchProposals(jobId) {
    const proposalsContainer = document.getElementById('proposals-section');
    try {
        // API นี้ต้องถูกสร้างใน proposal_service เพื่อให้ filter จาก job_post_id ได้
        const response = await fetch(`http://localhost:8005/api/proposals/?job_post_id=${jobId}`);
        const proposals = await response.json();
        
        proposalsContainer.innerHTML = '<h3 class="text-xl font-semibold mb-4">Proposals for this Job</h3>';
        if (proposals.length === 0) {
            proposalsContainer.innerHTML += '<p>No proposals yet.</p>';
            return;
        }

        proposals.forEach(proposal => {
            // ในระบบจริง อาจจะต้องยิง API ไปถามชื่อ Caregiver จาก ID อีกที
            proposalsContainer.innerHTML += `
                <div class="border-t py-2">
                    <p>From Caregiver ID: ${proposal.caregiver_id}</p>
                    <p>Rate: ฿${proposal.proposed_rate}</p>
                    <p><em>"${proposal.message}"</em></p>
                </div>
            `;
        });
    } catch (e) {
        proposalsContainer.innerHTML += '<p class="text-red-500">Could not load proposals.</p>';
    }
}

function setupProposalForm(jobId) {
    const form = document.getElementById('proposal-form');
    const messageDiv = document.getElementById('proposal-form-message');
    const token = localStorage.getItem('accessToken');

    if (!token) {
        form.innerHTML = '<p>Please <a href="/login.html" class="text-blue-500">login</a> to submit a proposal.</p>';
        return;
    }
    
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        messageDiv.textContent = 'Submitting...';

        const data = {
            job_post_id: jobId,
            message: form.message.value,
            proposed_rate: form.proposed_rate.value,
        };

        const response = await fetch('http://localhost:8005/api/proposals/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            messageDiv.textContent = 'Proposal submitted successfully!';
            messageDiv.className = 'text-green-500';
            form.reset();
            fetchProposals(jobId); // Refresh list
        } else {
            messageDiv.textContent = 'Failed to submit proposal.';
            messageDiv.className = 'text-red-500';
        }
    });
}
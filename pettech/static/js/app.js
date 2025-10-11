// Basic client-side rendering utilities for PetTech

(function(){
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrfToken = getCookie('csrftoken');

  async function api(path, options={}){
    const headers = options.headers || {};
    if (options.method && options.method.toUpperCase() !== 'GET'){
      headers['Content-Type'] = headers['Content-Type'] || 'application/json';
      headers['X-CSRFToken'] = csrfToken;
    }
    const res = await fetch(path, {credentials: 'same-origin', ...options, headers});
    if (!res.ok){
      let errText;
      try{errText = await res.text();}catch(e){errText = res.statusText}
      throw new Error(errText || ('HTTP '+res.status));
    }
    const contentType = res.headers.get('content-type') || '';
    if (contentType.includes('application/json')) return res.json();
    return res.text();
  }

  function formatDate(dtStr){
    try{ return new Date(dtStr).toLocaleString(); }catch(e){ return dtStr; }
  }

  // Index page renderer
  async function renderHome(){
    const container = document.getElementById('job-posts-grid');
    if (!container) return;
    const params = new URLSearchParams(window.location.search);
    const search = params.get('search') || '';
    const data = await api(`/api/job-posts/?status=open${search?`&search=${encodeURIComponent(search)}`:''}`);
    container.innerHTML = data.map(job => `
      <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300">
        <a href="/job-posts/${job.id}/">
          <div class="h-48 bg-gray-100 flex items-center justify-center">
            ${job.pet && job.pet.photo ? `<img src="${job.pet.photo}" alt="${job.pet.name}" class="h-full w-full object-cover">` : '<span class="text-gray-400">Pet Photo</span>'}
          </div>
          <div class="p-4">
            <h3 class="text-lg font-semibold text-gray-800">${job.title}</h3>
            <p class="text-sm text-gray-500 mb-1">สัตว์เลี้ยง: ${job.pet?.name || ''} (${job.pet?.species || ''})</p>
            <p class="text-sm text-gray-500 mb-1">วันที่: ${formatDate(job.start)} - ${formatDate(job.end)}</p>
            <p class="text-sm text-gray-500 mb-1">งบประมาณ: ${job.budget ? '฿'+job.budget : 'ไม่ระบุ'}</p>
            <p class="text-gray-600 text-sm">${(job.description||'').slice(0,120)}${(job.description||'').length>120?'...':''}</p>
          </div>
        </a>
      </div>
    `).join('');
  }

  // Job post detail renderer
  async function renderJobPostDetail(){
    const container = document.getElementById('job-post-detail');
    if (!container) return;
    const m = location.pathname.match(/job-posts\/(\d+)\//);
    if (!m) return;
    const id = m[1];
    const detail = await api(`/api/job-posts/${id}/`);
    const job = detail.job_post;
    const proposals = detail.proposals || [];

    container.innerHTML = `
      <h2 class="text-2xl font-semibold mb-4">${job.title}</h2>
      <p class="text-gray-600 mb-2">สัตว์เลี้ยง: ${job.pet?.name} (${job.pet?.species})</p>
      <p class="text-gray-600 mb-2">วันที่: ${formatDate(job.start)} - ${formatDate(job.end)}</p>
      <p class="text-gray-600 mb-2">สถานที่: ${job.location || ''}</p>
      <p class="text-gray-600 mb-4">งบประมาณ: ${job.budget ? '฿'+job.budget : 'ไม่ระบุ'}</p>
      <p class="text-gray-800 mb-6">${job.description || ''}</p>
      <div id="proposal-owner"></div>
      <div id="proposal-form" class="mt-8 border-t pt-6"></div>
    `;

    // owner proposal list or caregiver form
    try{
      const me = await api('/api/me/');
      const isOwner = me && me.user && job.owner && me.user.id === job.owner.id;
      if (isOwner){
        // Owner edit/delete controls (same placement intent as SSR using absolute container)
        const controls = document.createElement('div');
        controls.className = 'mb-4 absolute top-[20px] right-[10px] flex gap-2';
        controls.innerHTML = `
          <a href="/job-posts/${job.id}/edit/" class="inline-block bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600">แก้ไขงาน</a>
          <form method="post" action="/job-posts/${job.id}/delete/" onsubmit="return confirm('แน่ใจจะลบงานนี้หรือไม่?');">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken || ''}" />
            <button type="submit" class="inline-block bg-red-500 text-white px-4 py-2 rounded hover:bg-red-700">ลบงาน</button>
          </form>
        `;
        container.prepend(controls);

        document.getElementById('proposal-owner').innerHTML = `
          <h3 class="text-xl font-semibold mb-4 text-green-600">ข้อเสนอที่ได้รับ</h3>
          ${proposals.length ? `<ul class="space-y-4">${proposals.map(p=>`
            <li class="border p-4 rounded ${p.status==='accepted'?'bg-green-50':(p.status==='rejected'?'bg-gray-50':'')}">
              <p class="text-gray-800"><strong>ผู้ดูแล:</strong> ${p.caregiver_profile_id ? `<a class="text-green-700" href="/caregiver-profile/${p.caregiver_profile_id}/">${p.caregiver?.username || '—'}</a>` : (p.caregiver?.username || '—')}</p>
              <p class="text-gray-800"><strong>ข้อความ:</strong> ${p.message || ''}</p>
              <p class="text-gray-800"><strong>อัตราที่เสนอ:</strong> ฿${p.proposed_rate}</p>
              <p class="text-gray-800"><strong>วันที่ส่ง:</strong> ${formatDate(p.created_at)}</p>
              <p class="text-gray-800"><strong>สถานะ:</strong> ${p.status}</p>
              ${(job.status==='open' && p.status==='pending')?`<button data-proposal-id="${p.id}" class="accept-proposal mt-2 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">ยอมรับข้อเสนอ</button>`:''}
            </li>
          `).join('')}</ul>` : '<p class="text-gray-500">ยังไม่มีข้อเสนอสำหรับงานนี้</p>'}
        `;
        container.addEventListener('click', async (e)=>{
          const btn = e.target.closest('.accept-proposal');
          if (!btn) return;
          const pid = btn.getAttribute('data-proposal-id');
          await api(`/api/job-posts/${id}/proposals/${pid}/accept/`, {method:'POST'});
          location.reload();
        });
      } else if (me && me.user) {
        if (job.status === 'open'){
          document.getElementById('proposal-form').innerHTML = `
            <h3 class="text-xl font-semibold mb-4 text-blue-600">ส่งข้อเสนอของคุณ</h3>
            <form id="proposalSubmit" class="space-y-4">
              <div>
                <label class="block text-gray-700 font-semibold mb-2">ข้อความ</label>
                <textarea name="message" rows="3" class="w-full border rounded p-2"></textarea>
              </div>
              <div>
                <label class="block text-gray-700 font-semibold mb-2">อัตราที่เสนอ</label>
                <input name="proposed_rate" type="number" step="0.01" required class="w-full border rounded p-2" />
              </div>
              <button class="mt-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">ส่งข้อเสนอ</button>
            </form>`;
          document.getElementById('proposalSubmit').addEventListener('submit', async (e)=>{
            e.preventDefault();
            const fd = new FormData(e.target);
            const payload = Object.fromEntries(fd.entries());
            await api(`/api/job-posts/${id}/proposals/`, {method:'POST', body: JSON.stringify(payload)});
            location.reload();
          });
        } else {
          document.getElementById('proposal-form').innerHTML = '<p class="text-gray-500">ไม่สามารถส่งข้อเสนอได้ ณ ขณะนี้ (งานถูกปิดแล้ว)</p>';
        }
      }
    }catch(_){}
  }

  // Bookings page
  async function renderBookings(){
    const ownerContainer = document.getElementById('owner-bookings');
    const caregiverContainer = document.getElementById('caregiver-bookings');
    if (!ownerContainer && !caregiverContainer) return;
    const data = await api('/api/bookings/');
    if (ownerContainer){
      ownerContainer.innerHTML = (data.owner_bookings||[]).map(b=>`
        <div class="bg-white p-4 shadow rounded mb-4">
          <p><strong>Job:</strong> ${b.proposal?.job_post?.title || ''}</p>
          <p><strong>Pet:</strong> ${b.pet?.name || ''}</p>
          <p><strong>Caregiver:</strong> ${b.caregiver_profile_id ? `<a class="text-green-700" href="/caregiver-profile/${b.caregiver_profile_id}/">${b.caregiver?.username || ''}</a>` : (b.caregiver?.username || '')}</p>
          <p><strong>Status:</strong> ${b.status}</p>
        </div>
      `).join('') || '<p>No bookings as owner.</p>';
    }
    if (caregiverContainer){
      caregiverContainer.innerHTML = (data.caregiver_bookings||[]).map(b=>`
        <div class="bg-white p-4 shadow rounded mb-4">
          <p><strong>Job:</strong> ${b.proposal?.job_post?.title || ''}</p>
          <p><strong>Pet:</strong> ${b.pet?.name || ''}</p>
          <p><strong>Owner:</strong> ${b.owner?.username || ''}</p>
          <p><strong>Status:</strong> ${b.status}</p>
          ${b.status==='C'?`<button data-booking-id="${b.id}" class="complete-booking bg-green-500 text-white px-4 py-2 mt-2 rounded">Mark as Complete</button>`:''}
        </div>
      `).join('') || '<p>No bookings as caregiver.</p>';

      caregiverContainer.addEventListener('click', async (e)=>{
        const btn = e.target.closest('.complete-booking');
        if (!btn) return;
        const bid = btn.getAttribute('data-booking-id');
        await api(`/api/bookings/${bid}/complete/`, {method:'POST'});
        location.reload();
      });
    }
  }

  // My posts
  async function renderMyPosts(){
    const container = document.getElementById('my-posts');
    if (!container) return;
    const data = await api('/api/job-posts/?owner=me');
    container.innerHTML = data.map(post=>`
      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex justify-between items-start">
          <div>
            <h2 class="text-xl font-semibold">${post.title}</h2>
            <p class="text-sm text-gray-600">Posted on ${formatDate(post.created_at)}</p>
          </div>
          <div class="space-x-2">
            <a href="/job-posts/${post.id}/edit/" class="px-3 py-1.5 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm">Edit</a>
            <a href="/job-posts/${post.id}/delete/" class="px-3 py-1.5 bg-red-500 text-white rounded hover:bg-red-600 text-sm">Delete</a>
          </div>
        </div>
        <p class="mt-4 text-gray-700">${post.description || ''}</p>
        <p class="mt-2 text-sm text-gray-500">Location: ${post.location || ''}</p>
        <p class="mt-1 text-sm text-gray-500">Status: ${post.status}</p>
      </div>
    `).join('') || '<p>You have not posted any jobs yet Create a new job post.</p>';
  }

  // My profile
  async function renderMyProfile(){
    const container = document.getElementById('my-profile-root');
    if (!container) return;
    const me = await api('/api/me/');
    // We keep server template mostly; this can be used to progressively enhance.
    // For now, no rewrite; but hook is here if needed.
  }

  async function renderMyProposals(){
    const container = document.getElementById('my-proposals');
    if (!container) return;
    const data = await api('/api/my-proposals/');
    container.innerHTML = data.map(p => `
      <div class="bg-white p-4 shadow rounded">
        <p><strong>Job:</strong> <a href="/job-posts/${p.job_post?.id || ''}/" class="text-blue-600">${p.job_post?.title || ''}</a></p>
        <p><strong>Job Owner:</strong> ${p.job_post?.owner?.username || ''}</p>
        <p><strong>Caregiver:</strong> ${p.caregiver?.username || ''}</p>
        <p><strong>Status:</strong> ${p.status}</p>
        <p><strong>Rate:</strong> ${p.proposed_rate} บาท</p>
        <p><strong>Message:</strong> ${p.message || ''}</p>
      </div>
    `).join('') || '<p>You have not submitted any proposals yet.</p>';
  }

  async function renderBookingHistory(){
    const tbody = document.getElementById('booking-history-body');
    if (!tbody) return;
    const [data, me] = await Promise.all([
      api('/api/booking-history/'),
      api('/api/me/')
    ]);
    tbody.innerHTML = (data||[]).map(b=>`
      <tr class="border-b border-gray-200 hover:bg-gray-50">
        <td class="p-4 text-sm text-gray-700">${b.id}</td>
        <td class="p-4 text-sm text-gray-700">
          <a href="/job-posts/${b.proposal?.job_post?.id || ''}/" class="text-green-600 font-semibold hover:underline">
            ${b.proposal?.job_post?.title || ''}
          </a>
        </td>
        <td class="p-4 text-sm text-gray-700">${b.owner?.username || ''}</td>
        <td class="p-4 text-sm text-gray-700">${b.caregiver?.username || ''}</td>
        <td class="p-4 text-sm text-gray-700">${b.pet?.name || ''} (${b.pet?.species || ''})</td>
        <td class="p-4 text-sm text-gray-700">${formatDate(b.start)}</td>
        <td class="p-4 text-sm text-gray-700">${formatDate(b.end)}</td>
        <td class="p-4 text-sm">${b.status}</td>
        <td class="p-4 text-sm text-gray-700">${
          (b.status==='D' && me?.user?.id !== b.caregiver?.id && !b.has_review)
          ? `<a href="/write_review/${b.id}/" class="text-green-600 font-semibold hover:text-green-700 transition-all">Write a Review</a>`
          : (b.status==='D' && b.has_review ? '<span class="text-green-600 text-sm">Reviewed</span>' : '')
        }</td>
      </tr>
    `).join('') || '<tr class="text-gray-500 text-[14px] text-center"><td colspan="9" class="p-4">No booking history yet.</td></tr>';
  }

  document.addEventListener('DOMContentLoaded', ()=>{
    renderHome();
    renderJobPostDetail();
    renderBookings();
    renderMyPosts();
    renderMyProfile();
    renderMyProposals();
    renderBookingHistory();
  });
})();

// frontend/public/js/main.js

// ห่อโค้ดเดิมทั้งหมดไว้ในฟังก์ชันชื่อ setupNavbar
function setupNavbar() {
    const token = localStorage.getItem('accessToken');
    const guestLinks = document.getElementById('nav-guest-links');
    const userLinks = document.getElementById('nav-user-links');
    const usernameSpan = document.getElementById('nav-username');
    const logoutButton = document.getElementById('logout-button');
    const userMenuButton = document.getElementById('user-menu-button');
    const userDropdown = document.getElementById('user-dropdown');

    // ตรวจสอบว่า element ทั้งหมดพร้อมใช้งานหรือไม่ (สำคัญมาก)
    if (!guestLinks || !userLinks) {
        console.error("Navbar elements not found. Make sure nav.html is included correctly.");
        return;
    }

    if (token) {
        guestLinks.style.display = 'none';
        userLinks.classList.remove('hidden');
        userLinks.style.display = 'block';

        // ดึงข้อมูล User (ผ่าน API Gateway)
        fetch('/api/me/', {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(res => res.ok ? res.json() : Promise.reject(res))
        .then(user => {
            if (usernameSpan) usernameSpan.textContent = user.username;
        }).catch(() => { // ถ้า token หมดอายุ
            localStorage.clear();
            window.location.reload();
        });

        if (logoutButton) {
            logoutButton.addEventListener('click', () => {
                localStorage.clear();
                window.location.href = '/login.html';
            });
        }
        
        if (userMenuButton) {
            userMenuButton.addEventListener('click', () => {
                if (userDropdown) userDropdown.classList.toggle('hidden');
            });
        }

    } else {
        guestLinks.style.display = 'flex';
        userLinks.style.display = 'none';
    }
}
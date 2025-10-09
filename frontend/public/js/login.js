// frontend/public/js/login.js
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorContainer = document.getElementById('form-errors');

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        errorContainer.textContent = '';
        errorContainer.classList.add('hidden');

        const formData = new FormData(loginForm);
        const data = Object.fromEntries(formData.entries());

        try {
            // ยิง API ไปที่ user_service เพื่อขอ Token
            const response = await fetch('http://localhost:8001/api/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const tokens = await response.json();
                // ถ้าสำเร็จ, บันทึก Token ไว้ใน Local Storage
                localStorage.setItem('accessToken', tokens.access);
                localStorage.setItem('refreshToken', tokens.refresh);
                // ไปหน้า My Profile
                window.location.href = '/myprofile.html';
            } else {
                errorContainer.textContent = 'Invalid username or password.';
                errorContainer.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Login failed:', error);
            errorContainer.textContent = 'An error occurred during login.';
            errorContainer.classList.remove('hidden');
        }
    });
});
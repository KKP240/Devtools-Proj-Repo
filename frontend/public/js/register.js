// frontend/public/js/register.js
document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    const errorContainer = document.getElementById('form-errors');

    registerForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        errorContainer.textContent = '';
        errorContainer.classList.add('hidden');

        const formData = new FormData(registerForm);
        const data = Object.fromEntries(formData.entries());

        try {
            // ยิง API ไปที่ user_service
            const response = await fetch('http://localhost:8001/api/register/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                // ถ้าสมัครสำเร็จ, ไปหน้า login
                window.location.href = '/login.html';
            } else {
                // ถ้าไม่สำเร็จ, แสดง Error
                const errorData = await response.json();
                let errorMessage = '';
                for (const key in errorData) {
                    errorMessage += `${key}: ${errorData[key].join(', ')}\n`;
                }
                errorContainer.textContent = errorMessage;
                errorContainer.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Registration failed:', error);
            errorContainer.textContent = 'An unexpected error occurred. Please try again.';
            errorContainer.classList.remove('hidden');
        }
    });
});
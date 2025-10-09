// frontend/public/js/booking_form.js

document.addEventListener('DOMContentLoaded', () => {
    // 1. หาตัวฟอร์มและ element ที่จะใช้แสดงข้อความ
    const bookingForm = document.getElementById('booking-form');
    const formMessage = document.getElementById('form-message');
    const token = localStorage.getItem('accessToken'); // ดึง Token ของผู้ใช้ที่ login อยู่

    // ตรวจสอบว่า login แล้วหรือยัง
    if (!token) {
        // ถ้ายังไม่ login, อาจจะ redirect ไปหน้า login หรือแสดงข้อความ
        formMessage.textContent = 'Please log in to create a booking.';
        formMessage.className = 'text-red-500';
        // ทำให้ฟอร์มใช้งานไม่ได้
        bookingForm.querySelector('button').disabled = true;
        return;
    }

    // 2. ดักจับเหตุการณ์เมื่อผู้ใช้กดปุ่ม 'submit'
    bookingForm.addEventListener('submit', async (event) => {
        // ป้องกันไม่ให้หน้าเว็บ refresh ใหม่
        event.preventDefault();

        formMessage.textContent = ''; // เคลียร์ข้อความเก่า

        // 3. รวบรวมข้อมูลทั้งหมดจากฟอร์ม
        const formData = new FormData(bookingForm);
        const data = {
            caregiver_id: formData.get('caregiver_id'),
            pet_id: formData.get('pet_id'),
            start: formData.get('start'),
            end: formData.get('end'),
            // owner_id และ status จะถูกกำหนดโดย Backend API โดยอัตโนมัติ
        };

        // 4. แสดงข้อความว่ากำลังทำงาน
        formMessage.textContent = 'Submitting your booking...';
        formMessage.className = 'text-blue-500';

        try {
            // 5. ยิง API Request แบบ POST ไปยัง booking_service
            const response = await fetch('http://localhost:8003/api/bookings/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` // ส่ง Token ไปด้วยเพื่อยืนยันตัวตน
                },
                body: JSON.stringify(data) // แปลงข้อมูล JavaScript object ให้เป็น JSON string
            });

            // 6. ตรวจสอบผลลัพธ์ที่ได้จาก API
            if (response.ok) {
                // ถ้าสำเร็จ (Status 201 Created)
                formMessage.textContent = 'Booking created successfully!';
                formMessage.className = 'text-green-500';
                bookingForm.reset(); // ล้างข้อมูลในฟอร์ม
                // อาจจะ redirect ไปหน้า booking history หลังจากผ่านไป 2 วินาที
                setTimeout(() => {
                    window.location.href = '/booking_history.html';
                }, 2000);
            } else {
                // ถ้าไม่สำเร็จ ให้แสดง Error
                const errorData = await response.json();
                formMessage.textContent = `Error: ${JSON.stringify(errorData)}`;
                formMessage.className = 'text-red-500';
            }

        } catch (error) {
            console.error('Failed to submit booking form:', error);
            formMessage.textContent = 'An unexpected error occurred. Please check the console.';
            formMessage.className = 'text-red-500';
        }
    });
});
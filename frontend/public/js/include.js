// frontend/public/js/include.js
document.addEventListener('DOMContentLoaded', async () => {
    // ฟังก์ชันสำหรับดึง "ชิ้นส่วน" HTML เข้ามาแปะ
    async function includeHTML() {
        const elements = document.querySelectorAll('[include-html]');
        for (let element of elements) {
            const file = element.getAttribute('include-html');
            if (file) {
                try {
                    const response = await fetch(file);
                    if (response.ok) {
                        element.innerHTML = await response.text();
                    } else {
                        element.innerHTML = 'Error: Component not found.';
                    }
                } catch (error) {
                    console.error('Could not include HTML:', error);
                    element.innerHTML = 'Error loading component.';
                }
                element.removeAttribute('include-html');
            }
        }
    }

    // --- กระบวนการทำงาน ---
    // 1. รอให้โหลด "ชิ้นส่วน" HTML (เช่น Navbar) ทั้งหมดให้เสร็จก่อน
    await includeHTML(); 
    
    // 2. หลังจากโหลดเสร็จแล้ว ค่อยสั่งให้ main.js เริ่มทำงานกับ Navbar ที่เพิ่งโหลดเข้ามา
    if (typeof setupNavbar === 'function') {
        setupNavbar();
    }
});
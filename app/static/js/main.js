document.addEventListener('DOMContentLoaded', function() {
    const baziForm = document.getElementById('baziForm');
    if (baziForm) {
        baziForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                year: document.querySelector('input[name="year"]').value,
                month: document.querySelector('input[name="month"]').value,
                day: document.querySelector('input[name="day"]').value,
                time: document.querySelector('input[name="time"]').value,
                model: document.querySelector('select[name="model"]').value
            };
            
            try {
                const response = await fetch('/bazi', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                document.getElementById('baziResult').textContent = data.bazi;
                document.getElementById('fortuneReading').textContent = data.reading;
                document.getElementById('result').classList.remove('hidden');
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }
});

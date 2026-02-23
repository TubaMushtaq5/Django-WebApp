// script.js

document.addEventListener('DOMContentLoaded', function () {
    // 1️⃣ Form submit confirmation
    const form = document.querySelector('.datetime-form-container form');

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const title = document.getElementById('title').value;
            const region = document.getElementById('region').value.toUpperCase();

            const confirmed = confirm(`Do you want to save the following?\n\nTitle: "${title}"\nRegion: ${region}`);

            if (confirmed) {
                form.submit();
            }
        });
    }

    // 2️⃣ Datetime auto-fill based on region
    const regionSelect = document.getElementById('region');
    const dtField = document.getElementById('datetime'); // make sure this input exists

    function updateDatetime() {
        const now = new Date();

        if (!dtField) return; // stop if input doesn't exist

        if (regionSelect.value === 'pst') {
            const pstDate = new Date(now.toLocaleString("en-US", { timeZone: "America/Los_Angeles" }));
            dtField.value = pstDate.toISOString().slice(0,16);
        } else {
            dtField.value = now.toISOString().slice(0,16);
        }
    }

    // Run on page load
    updateDatetime();

    // Run whenever region changes
    if (regionSelect) {
        regionSelect.addEventListener('change', updateDatetime);
    }
});
// load after DOMContentLoaded
document.addEventListener("DOMContentLoaded", function () {
    // Follow Button interaction on profile page
    const button = document.querySelector('#follow-button');
    button.addEventListener('click', async () => {
        const userId = button.dataset.userId;
        const response = await fetch(`/follow/${userId}/`, { method: 'POST' });
        const data = await response.json();
    if (response.ok) {
        button.dataset.following = data.followed ? 'True' : 'False';
        button.textContent = data.followed ? 'Unfollow' : 'Follow';
    } else {
        console.error(data.error);
    }
});
})
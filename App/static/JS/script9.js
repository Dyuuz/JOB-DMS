// Toggle Sidebar Navigation and Blur Effect
const navToggle = document.getElementById('nav-toggle');
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('main-content');

navToggle.addEventListener('click', () => {
  sidebar.classList.toggle('active');
  mainContent.classList.toggle('active');
});

// Close Sidebar When Clicking Outside on Smaller Screens
document.addEventListener('click', (event) => {
  if (!sidebar.contains(event.target) && window.innerWidth <= 768) {
    sidebar.classList.remove('active');
    mainContent.classList.remove('active');
  }
});

// Close Sidebar When Arrow left icon is clicked
const arrowLeft = document.querySelector('.arrowleft-button');
arrowLeft.addEventListener('click', () => {
  sidebar.classList.remove('active');
  mainContent.classList.remove('active');
});

// Automatically Adjust Layout on Screen Resize
window.addEventListener('resize', () => {
  if (window.innerWidth > 768) {
    // Ensure sidebar is visible and blur effect is removed
    sidebar.classList.remove('active');
    mainContent.classList.remove('active');
  } else {
    // Hide sidebar by default on smaller screens
    sidebar.classList.remove('active');
    mainContent.classList.remove('active');
  }
});

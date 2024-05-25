// Initialize swiper.js for project slider

const swiper = new Swiper(".card-slider", {
  // Default parameters
  slidesPerView: 1,
  spaceBetween: 30,
  loop: true,
  navigation: {
    nextEl: ".nextArrowBtn",
    prevEl: ".prevArrowBtn",
  },
  // Responsive breakpoints
  breakpoints: {
    // when window width is >= 576px
    576: {
      slidesPerView: 2,
    },
    // when window width is >= 768px
    768: {
      slidesPerView: 3,
      spaceBetween: 30,
    },
  },
});

// Scroll to top

const limit = 200;
const scrollTopBtn = document.querySelector("#scroll-top-btn");
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}
document.addEventListener("scroll", function () {
  scrollTopBtn.classList.toggle("visible", window.scrollY >= limit);
});


//Popular Destinations
document.addEventListener('DOMContentLoaded', function() {
  const observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: 0.1
  };

  const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
          if (entry.isIntersecting) {
              const delayElements = entry.target.querySelectorAll('.delay-1, .delay-2, .delay-3, .delay-4, .delay-5, .delay-6');
              delayElements.forEach(el => el.classList.add('fly-in'));
              observer.unobserve(entry.target);
          }
      });
  }, observerOptions);

  const target = document.querySelector('#destinations');
  observer.observe(target);
});


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
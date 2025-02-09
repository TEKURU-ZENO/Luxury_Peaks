// Mobile Menu Toggle
const menuBtn = document.getElementById("menu-btn");
const navLinks = document.getElementById("nav-links");
const menuBtnIcon = menuBtn.querySelector("i");

menuBtn.addEventListener("click", () => {
  navLinks.classList.toggle("open");
  const isOpen = navLinks.classList.contains("open");
  menuBtnIcon.setAttribute("class", isOpen ? "ri-close-line" : "ri-menu-line");
});

// Close Menu on Link Click (Mobile)
navLinks.addEventListener("click", () => {
  navLinks.classList.remove("open");
  menuBtnIcon.setAttribute("class", "ri-menu-line");
});

// ScrollReveal Animations
const scrollRevealOption = {
  origin: "bottom",
  distance: "50px",
  duration: 1000,
};

ScrollReveal().reveal(".header__image img", {
  ...scrollRevealOption,
  origin: "right",
});
ScrollReveal().reveal(".header__content p", {
  ...scrollRevealOption,
  delay: 300,
});
ScrollReveal().reveal(".header__content h1", {
  ...scrollRevealOption,
  delay: 600,
});
ScrollReveal().reveal(".header__btns", {
  ...scrollRevealOption,
  delay: 900,
});

// Product Card Animations
ScrollReveal().reveal(".product-card", {
  ...scrollRevealOption,
  interval: 400,
});

// Flip Card Animations
ScrollReveal().reveal(".flip-card", {
  ...scrollRevealOption,
  interval: 300,
});

// Showcase Section Animations
ScrollReveal().reveal(".showcase__image img", {
  ...scrollRevealOption,
  origin: "left",
});
ScrollReveal().reveal(".showcase__content h4", {
  ...scrollRevealOption,
  delay: 300,
});
ScrollReveal().reveal(".showcase__content p", {
  ...scrollRevealOption,
  delay: 600,
});
ScrollReveal().reveal(".showcase__btn", {
  ...scrollRevealOption,
  delay: 900,
});

// Testimonials Carousel (Swiper Configuration)
const swiper = new Swiper(".swiper", {
  slidesPerView: 1,
  spaceBetween: 20,
  loop: true,
  autoplay: {
    delay: 5000,
    disableOnInteraction: false,
  },
  breakpoints: {
    640: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    1024: {
      slidesPerView: 3,
    },
  },
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});

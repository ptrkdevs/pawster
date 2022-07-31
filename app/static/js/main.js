

const flash = document.querySelector('.flash-message')


if (document.contains(flash)) {
    setTimeout(() => {
        flash.remove()
    }, 2000)
}


const openMenuBtn = document.querySelector('.openMenu')
const closeMenuBtn = document.querySelector('.closeMenu')
const navbarLinks = document.querySelector('.navbar--links')



openMenuBtn.addEventListener('click', (e) => {

   
    navbarLinks.style.top = '0';
    navbarLinks.style.display = 'flex'
})

closeMenuBtn.addEventListener('click', (e) => {
    navbarLinks.style.top = '-100%';
})

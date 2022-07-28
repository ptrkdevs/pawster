

const flash = document.querySelector('.flash-message')


if (document.contains(flash)) {
    setTimeout(() => {
        flash.remove()
    }, 2000)
}
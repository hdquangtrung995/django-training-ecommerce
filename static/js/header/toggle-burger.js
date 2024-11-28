$(function () {
    $(document).on('click', function (e) {
        if (!$(e.target).closest('li.categoryItem').length) {
            $('li.categoryItem ul').removeClass('openBurgerItem').removeAttr('style');
            $('li.categoryItem i.fa-minus').removeClass('fa-minus').addClass('fa-plus');
        }
    });

    $('li.categoryItem').on('click', '.dropdown-burger-button', function (e) {
        e.stopPropagation();

        const subMenu = $(this).closest('li').find('ul:first');
        subMenu.toggleClass('openBurgerItem');

        const icon = $(this).find('i')
        if (subMenu.hasClass('openBurgerItem')) {
            subMenu.css({'margin': '1rem 0'})
            setTimeout(() => icon.removeClass('fa-plus').addClass('fa-minus'), 450)
        } else {
            subMenu.removeAttr('style')
            setTimeout(() => icon.removeClass('fa-minus').addClass('fa-plus'), 450)
        }
    });

    $('#openBurger, #closeBurger').on('click', () => {
        $('#menuBurger').toggleClass('fullHeight')
        $('#menuBurgerBackDrop').toggleClass('fullHeight')
        $('#closeBurger').toggleClass('hidden')
    })

    // (() => {
        // console.log('hello')
        // const menuBurger = $('#menuBurger').get(0)
        // const menuBurgerBackDrop = $('#menuBurgerBackDrop').get(0)

        // const resizeObserver = new ResizeObserver((entries) => {
        //     console.log('entries: ', entries);
        // })

        // if (menuBurger) {
        //     resizeObserver.observe(menuBurger)
        // }

    // })()

    // $('#closeBurger').on('click', () => {
    //     $('#menuBurger').toggleClass('hidden')
    //     $('#menuBurgerBackDrop').toggleClass('hidden')
    // })
});

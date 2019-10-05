$(document).ready(function(){

    $('.owl-carousel').owlCarousel({
        // loop:true,
        margin:10,
        // nav:true,
        autoWidth:true,
        items:4,
        responsive:{
            0:{
                items:2
            },
            600:{
                items:3
            },
            1000:{
                items:1
            }
        }
    })

    $(window).scroll(function () { 
        if($(this).scrollTop() > 110){
            $('.bottom-header').addClass("fixed-nav")
        }else{
            $('.bottom-header').removeClass("fixed-nav")
        }
    });

    //Dasboard Actions

    ///Abrir Modal de Vendas
    $('.ver-todos-order').click(function(){
        $('.modal-more-orders').css('display', 'block');
    })

    //Fechar Modal de Vendas
    $('#close-all-orders').click(function(){
        $('.modal-more-orders').css('display', 'none');
    })

    //Signup
    $("#signup").click(function(){
        $('.main-container-login').addClass('right-panel-active');
    })

    //Login
    $("#login").click(function(){
        $('.main-container-login').removeClass('right-panel-active');
        console.log('eae')
    })

    //Open Carrinho de compras
    $('.shopping-cart').click(function(){

        $('.display-shopping-cart').css({
            display: 'block',
            width: '350px',
        });
    })

    $('.closing-menu').click(function(){
        $('.display-shopping-cart').css({
            display: 'none',
            width: '0',
            transition: 'all .5s linear',
        });
    })

})
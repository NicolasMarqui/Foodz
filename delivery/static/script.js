$(document).ready(function(){

    $('.display-choices-products').slick({
        lazyLoad: 'ondemand',
        dots: true,
        infinite: false,
        autoplaySpeed: 3000,
        slidesToShow: 6,
        slidesToScroll: 5,
        responsive: [
          {
            breakpoint: 1024,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 3,
              infinite: true,
              dots: true
            }
          },
          {
            breakpoint: 600,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 2
            }
          },
          {
            breakpoint: 480,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1
            }
          }
        ]
      });

      $('.melhores-rest').slick({
        lazyLoad: 'ondemand',
        dots: true,
        infinite: false,
        autoplaySpeed: 3000,
        slidesToShow: 3,
        slidesToScroll: 3,
        responsive: [
          {
            breakpoint: 1024,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 3,
              infinite: true,
              dots: true
            }
          },
          {
            breakpoint: 600,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 2
            }
          },
          {
            breakpoint: 480,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1
            }
          }
        ]
      });

    $(window).scroll(function () {
        
        let nav;

        if($('.bottom-header').css('display') === 'none'){
            nav = '.header';
        }else{
            nav = '.bottom-header';
        }
        
        if($(this).scrollTop() > 110){
            $(nav).addClass("fixed-nav")
        }else{
            $(nav).removeClass("fixed-nav")
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

    //Fechar Carrinho de Compras
    $('.closing-menu').click(function(){
        $('.display-shopping-cart').css({
            display: 'none',
            width: '0',
            transition: 'all .5s linear',
        });
    })

    //Abrir Menu Mobile
    $('.menu-m i').click(function(){
        $('.menu-mobile-wrapper').css({
            display: 'block',
            opacity: '1',
        })
    })

    //Fecha Menu Mobile
    $('#close-full-menu').click(function(){
        $('.menu-mobile-wrapper').css({
            display: 'none',
            opacity: '0',
        })
    })

})
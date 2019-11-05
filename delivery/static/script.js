$(document).ready(function(){

    $('.display-choices-products').slick({
        lazyLoad: 'ondemand',
        dots: true,
        infinite: false,
        autoplaySpeed: 3000,
        slidesToShow: 5,
        slidesToScroll: 2,
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

    //Open notificação
    $('.open-not').click(function(){

      $('.display-notificacoes').css({
          display: 'block',
          width: '350px',
          zIndex: '6'
      });
  })

  //Fechar Notificação
  $('#close-not').click(function(){
      $('.display-notificacoes').css({
          display: 'none',
          width: '0',
          zIndex: '0',
          transition: 'all .5s linear',
      });
  })

    //Tooltip
    $('[data-toggle="tooltip"]').tooltip();

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

    //Abre carrinho no icone de carrinho para mobilão
    $('.mobile-cart').click(function(){
        $('.display-shopping-cart').css({
            display: 'block',
            width: '350px',
        });
    })

    //Abrir Search Mobile
    $('.search-m i').click(function(){
      $('.search-mobile-wrapper').css({
          display: 'flex',
          opacity: '1',
      })
  })

  //Fecha Search Mobile
  $('#close-full-search').click(function(){
      $('.search-mobile-wrapper').css({
          display: 'none',
          opacity: '0',
      })
  })

  //Add borda vermelha
  $('.search-nav form input[name=query]').blur(function(){
    $(this).css({
      borderBottom: '1px solid red',
    })
  })

  //Menu Dashboard
    // $('.menu-toggle').click(function(){
    //   $('.click_toggle').hide();

    //   $('.sidenav').css({
    //     width: '50px'
    //   });

    //   $('.main-content-dashboard').css({
    //     width: 'calc(100% - 50px)',
    //     marginLeft: '50px'
    //   });

    //   $('.sidenav h1 a span').html('F')

    //   $('.sidenav h1').css({
    //     padding: '24px 8px'
    //   })
    // })

    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

    //Marca notificação como lida
    $('.check').click(function(){
      $.ajax({
        type: "POST",
        url: "/lida",
        data: {
          id: $('.check a').attr('id'),
          csrfmiddlewaretoken: getCookie('csrftoken'),
          lida: 1
        },
        success: function (response) {
          var options = {
            settings: {
              duration: 2000
            }
          };
          iqwerty.toast.Toast('Mensagem Lida!', options);
        }
      });
    })
})
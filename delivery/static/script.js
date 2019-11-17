$(document).ready(function(){

    AOS.init();

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

    function getCarrinhoItems(){

      $.ajax({
        type: "GET",
        url: "/carrinho/todos",
        dataType: "json",
        beforeSend: function(){
          $('.display-shopping-item').loading({
            stoppable: true
          });
        },
        complete: function (response) {
          let produtos = response.responseJSON.produtos;
          let rows = '';
          let info = response.responseJSON.info
          let total = response.responseJSON.total
          let empty = response.responseJSON.empty ? response.responseJSON.empty : false      

          $('.display-shopping-item > ul > li').remove();

          if(!empty){
              produtos.forEach((prod, i) => {
                rows += `
                  <li id="${prod.id}" class="${prod.id_produto_id}">
                    <div class="display">
                      <div class="amount">
                        <p>x <span>${prod.quantidade}</span> </p>
                      </div>
    
                      <div class="info">
                        <h5>${info[i].nome}</h5>
                        <p><strong>Vendido por: </strong> ${info[i].restaurante} </p>
                      </div>
    
                      <div class="preco">
                        <p>R$ <span>${info[i].preco}</span> </p>
                      </div>
                    </div>
                  </li>
                ` 
              });

              $('.total p span').html(total)
    
              $('.display-shopping-item > ul').append(rows);

          }else{
            $('.display-shopping-item > ul > div').remove()
            $('.total').hide();
            $('.go-checkout-info').hide()
            msg = '<div class="no-items"> <p>Você não possui nenhum item no seu carrinho</p> <a href="/produtos">Explorar</a> </div>';
            $('.display-shopping-item > ul').append(msg);
          }

          $('.display-shopping-item').loading('stop');

        }
      });
    }

    function deleteItemCarrinho(id){
        if(id){
            valor_total       = Number($('.total p span').html())
            quantidade        = Number($('.display-shopping-item').find(`ul li#${id} .display .amount p span`).html())
            preco             = Number($('.display-shopping-item').find(`ul li#${id} .display .preco p span`).html())
            quantidade_header = Number($('.amount-cart span').html())

            data = {
              id: id,
              csrfmiddlewaretoken: getCookie('csrftoken'),
            }

            $.ajax({
              type: "POST",
              url: "/carrinho/excluir",
              data: data,
              dataType: "json",

              beforeSend: function(){
                $('body').loading({
                  stoppable: true
                });
              },

              success: function (response) {
                console.log(response)
                if(response.status == 'success'){
                  $('.display-shopping-item').find(`ul li#${id}`).fadeOut(300, function() { $(this).remove()});
                }

                $.toast({
                  heading: 'Removido :(',
                  text: response.msg,
                  showHideTransition: 'slide',
                  icon: 'success'
                })

                $('body').loading('stop');

                $('.total p span').html((valor_total - (quantidade * preco)).toFixed(2));
                $('.price-header span').html((valor_total - (quantidade * preco)).toFixed(2));
                $('.amount-cart span').html(quantidade_header - 1)
                $('.mobile-cart span').html(quantidade_header - 1)
              }

            });
        }
    }

    function deleteItemPage(id){
      if(id){
          valor_total       = Number($('.info-final .preco span').html())
          quantidade        = Number($('.todos-items').find(`div#${id} .quantidade input`).val())
          preco             = Number($('.todos-items').find(`div#${id} .preco p span`).html())
          quantidade_header = Number($('.amount-cart span').html())
          frete             = Number($('.frete span').html())
          final             = Number($('.info-final .final span').html())

          data = {
            id: id,
            csrfmiddlewaretoken: getCookie('csrftoken'),
          }

          $.ajax({
            type: "POST",
            url: "/carrinho/excluir",
            data: data,
            dataType: "json",

            beforeSend: function(){
              $('body').loading({
                stoppable: true
              });
            },

            success: function (response) {
              console.log(response)
              if(response.status == 'success'){
                $('.todos-items').find(`div#${id}`).fadeOut(300, function() { $(this).remove()});
              }

              $.toast({
                heading: 'Removido :(',
                text: response.msg,
                showHideTransition: 'slide',
                icon: 'success'
              })

              $('body').loading('stop');

              $('.info-final .preco span').html((valor_total - (quantidade * preco)).toFixed(2));
              $('.price-header span').html((valor_total - (quantidade * preco)).toFixed(2));
              $('.amount-cart span').html(quantidade_header - 1)
              $('.mobile-cart span').html(quantidade_header - 1)
            }

          });
      }
  }

    $('.deleteFromCart').click(function(){
      id = $(this).attr('id');

      deleteItemPage(id)
    })

    //Open Carrinho de compras
    $('.shopping-cart').click(function(){
        $('.display-shopping-cart').css({
          display: 'block',
          width: '350px',
      });

      getCarrinhoItems();
      
    })

    $('.display-shopping-item').on('click' , 'ul li', function(){
      
        id_carrinho = $(this).attr('id');
        id_produto = $(this).attr('class');

        deleteItemCarrinho(id_carrinho)

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
      if (window.matchMedia("(max-width: 768px)").matches) {
        $('.display-shopping-cart').css({
            display: 'block',
            width: '100%',
        });
      } else {
          $('.display-shopping-cart').css({
            display: 'block',
            width: '350px',
        });
      }

      getCarrinhoItems();
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
            id: $(this).parent().attr('id'),
            csrfmiddlewaretoken: getCookie('csrftoken'),
            lida: 1
          },
          dataType: 'json',
          complete: function (response) {
              if(response.responseJSON.status === 'Success'){
                
                if(response.responseJSON.notificacoes.length){
                  var url = response.responseJSON.notificacoes[0];
                  tem_not = $('.notificacoes').find(`li#${url.id}`).fadeOut(300, function() { $(this).remove()});

                  $('.notificacoes').find(`li#${url.id}`).fadeOut(300, function() { $(this).remove()});

                  $('.total-notificacoes span').html($('.notificacoes li').length - 1)
                  
                  if($('.total-notificacoes span').html() == '0'){
                    $('.notificacoes').append('<p class="read-all">Você leu todas as suas notificações!!<p>')
                  }
                  
                  $.toast({
                    heading: 'Lida :)',
                    text: 'Mensagem lida!',
                    showHideTransition: 'slide',
                    icon: 'success'
                  })
                }
              }else{
                console.log('fudeu');
                
              }

          }
        });
    })

    //Pega os produtos
    $('#load-products').click(function(){

      $('#todos_produtos > tbody > tr').remove()

      $.ajax({
        type: "get",
        url: "/produtos/todos",
        dataType: "json",

        beforeSend: function(){
          $('body').loading({
            stoppable: true
          });
        },
        success: function (data) {
          let produtos;

          data.produtos.forEach(prod => {

            produtos += `
            <tr id="${prod.id}" class="edit-prod">
            <td>${prod.id}</td>
            <td><img src="/media/${prod.foto}" alt="${prod.nome}"></td>
            <td>${prod.nome}</td>
            <td>
              ${prod.descricao.slice(0,7)}...
            </td>
            <td>
              <button class="btn updateBtn" data-id="${prod.id}">Editar</button>
            </td>
            <td>
              <button class="btn deleteBtn btn-danger" data-id="${prod.id}">Deletar</button>
            </td>
          </tr>`;
          });

          $('#todos_produtos > tbody').append(produtos)

          $('body').loading('stop');
        }
      });
    })

    $('#todos_produtos').on('click', $('.updateBtn'), function(){
        $.ajax({
          type: "method",
          url: "get-produto-editar/",
          data: {
            id: id,
            csrfmiddlewaretoken: getCookie('csrftoken'),
          },
          dataType: "dataType",
          success: function (response) {
            
          }
        });
    })

    $('.edit-prod').on('click', function(){

      id = $(this).attr('id')

      $.ajax({
        type: "post",
        url: `get-produto-editar/`,
        data: {
          id: id,
          csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        dataType: "json",
        complete: function (response) {
          modal = response.responseText;

          $(document).find('.open-modal').remove()
          $('.content-produtos').append('<div class="open-modal"><div class="modal-edit" ><div class="header-edit"><i class="fas fa-times" id="close-edit"></i></div><form method="POST" enctype="multipart/form-data">'+ modal +'<button type="submit" id="salvar_editar" value=' + id +'>Salvar</button></form></div></div>')
        }
      });

    });

    $('.content-produtos').on('click', ".header-edit .fa-times" ,function(){
      $('.open-modal').css('display', 'none');
      $('.modal-edit').css('display', 'none');
    })

    $('.content-produtos').on('click', '#salvar_editar' ,function(e){
      e.preventDefault();
      
      data = $('.modal-edit form').serializeArray();
      
      data_JSON = JSON.stringify(data)

      $.ajax({
        type: "POST",
        url: "/save-produto-editar",
        data: {
          data: data_JSON,
          csrfmiddlewaretoken: getCookie('csrftoken'),
          id: $('#salvar_editar').val(),
        },
        dataType: "dataType",
        complete: function (response) {
          var parsed = JSON.parse(response.responseText);

          if(parsed.status == 'success'){
              $.toast({
                heading: 'Atualizado :)',
                text: 'Produto atualizado com sucesso',
                showHideTransition: 'slide',
                icon: 'success'
              });
            };

            $('.open-modal').css('display', 'none');
            $('.modal-edit').css('display', 'none');
          }
      });

    })

    //Add to cart
    $('.infos').on('click', 'a.add-carrinho', function () {
      
      id                  = $(this).attr('id');
      totalCarrinho       = Number($('.amount-cart span').html())
      totalCarrinhoMobile = Number($('.mobile-cart span').html())
      total_preco         = Number($('.price-header span').html())

      data = {
        csrfmiddlewaretoken: getCookie('csrftoken'),
        id: id,
      }
      
      $.ajax({
        type: "POST",
        url: "/carrinho/add",
        data: data,
        dataType: "json",
        beforeSend: function(){
          $('body').loading({
            stoppable: true
          });
        },
        complete: function (response) {
          console.log(response.responseJSON)
          status = response.responseJSON.status
          msg = response.responseJSON.msg
          ja_tem = response.responseJSON.ja_tem ? response.responseJSON.ja_tem : false

          if(status == 'success'){
            if(ja_tem){
              $('.amount-cart span').html(totalCarrinho)
              $('.mobile-cart span').html(totalCarrinho)
            }else{
              $('.amount-cart span').html(totalCarrinho + 1)
              $('.mobile-cart span').html(totalCarrinho + 1)
            }

            $.toast({
              heading: 'Adicionado :)',
              text: msg,
              showHideTransition: 'slide',
              icon: 'success'
            })

            final_cara = total_preco + Number($(`#price-${id} p span`).html())

            $('.price-header span').html(Number(final_cara).toFixed(2)) 
            
            
          }else{
            $.toast({
              heading: 'Ops :)',
              text: msg,
              showHideTransition: 'slide',
              icon: 'error'
            })
          }

          $('.mobile-cart').addClass('infinite slower delay-3s')
          $(this).parents().addClass('slideOutUp')

          $('body').loading('stop');
          
        }
      });
      
    });

    $('#calcularFrete').submit(function(e){
      e.preventDefault();

      $.ajax({
        type: "POST",
        url: "/carrinho/cep",
        data: {
          cep: $('#num_frete').val(),
          csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        dataType: "json",
        beforeSend: function(){
          $('.calcula-frete').loading({
            stoppable: true
          });
        },
        success: function (response) {
          var x2js = new X2JS();
          text = String(response.cep)
          var jsonObj = x2js.xml_str2json( JSON.parse(response.cep) );
          $('.calcula-frete').loading('stop');
        }
      });
    })


    $('.addFavorite').on('click', 'i.addMe', function(){
        id = $(this).attr('id')

        console.log('clciked');
        

        data = {
          csrfmiddlewaretoken: getCookie('csrftoken'),
          id: id,
        }

        $.ajax({
          type: "POST",
          url: "/favoritos/add",
          data: data,
          dataType: "json",
          beforeSend: function(){
            $('.display-choices-products').loading({
              stoppable: true
            });
          },
          success: function (response) {

            if(response.status == 'success'){
              $('.addFavorite').find(`i#${id}`).removeClass('far addMe')
              $('.addFavorite').find(`i#${id}`).addClass('fas removeMe')

              $.toast({
                heading: 'Adicionado :)',
                text: response.msg,
                showHideTransition: 'slide',
                icon: 'success'
              })
            }else{
              $.toast({
                heading: 'Ops :)',
                text: response.msg,
                showHideTransition: 'slide',
                icon: 'error'
              })
            }

            $('.display-choices-products').loading('stop');
          }
        });
    });

    $('.addFavorite').on('click', 'i.removeMe', function(){
      id = $(this).attr('id');

      data = {
        csrfmiddlewaretoken: getCookie('csrftoken'),
        id: id,
      }

      $.ajax({
        type: "POST",
        url: "/favoritos/remove",
        data: data,
        dataType: "json",
        beforeSend: function(){
          $('.display-choices-products').loading({
            stoppable: true
          });
        },
        success: function (response) {
            $('.addFavorite').find(`i#${id}`).removeClass('fas removeMe')
            $('.addFavorite').find(`i#${id}`).addClass('far addMe')
            $.toast({
              heading: 'Removido :(',
              text: response.msg,
              showHideTransition: 'slide',
              icon: 'success'
            })

            $('.display-choices-products').loading('stop');
        }
      });
  });

  //Masks
  var spOptions = {
    onKeyPress: function(val, e, field, options) {
      var mask = "";

      if (val.length === 5) {
        mask = '00.00'
      } else {
        mask = '000.00'
      }
      $('#id_preco').mask(mask, options);
    },
  };

  $('#id_preco').mask('00.00', spOptions);
  $('#id_cpf').mask('000.000.000.00');
  $('#id_telefone').mask('(00) 00000-0000');


  //Card Checkout
  $('.pagamento').card({
      container: '.show-card',
      placeholders: {
        number: '**** **** **** ****',
        name: 'Nome Completo',
        expiry: '**/****',
        cvc: '***'
    }
});


//Checkout
$('#submitPayment').click(function(){
  console.log('clicked')
})
  

})
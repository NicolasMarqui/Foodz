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

    // $(window).scroll(function () { 
    //     if($(this).scrollTop() > 220){
    //         $('header').addClass("fixed-nav")
    //     }else{
    //         $('header').removeClass("fixed-nav")
    //     }
    // });

    $('.ver-todos-order').click(function(){
        $('.modal-more-orders').css('display', 'block');
    })

    $('#close-all-orders').click(function(){
        $('.modal-more-orders').css('display', 'none');
    })
})
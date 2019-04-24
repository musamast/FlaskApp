
(function ($) {
    "use strict";


    /*==================================================================
    [ Focus Contact2 ]*/
    $('.input100').each(function(){
        $(this).on('blur', function(){
            if($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })    
    })
  
  
    /*==================================================================
    [ Validate ]*/
    var name = $('.validate-input input[name="name"]');
    var price = $('.validate-input input[name="price"]');
    var quantity = $('.validate-input input[name="quantity"]');
    var regex=/^[0-9]+$/;
    var category=$('.validate-input select[name="category"]');
    var color=$('.validate-input select[name="color"]');
    var size=$('.validate-input select[name="size"]');
    var type=$('.validate-input select[name="type"]');
    var pic1=$('input[name="name"]');
    $('.validate-form').on('submit',function(){
        var check = true;


        if(!$(price).val().match(regex)){
            showValidate(price);
            check= false;
        }
        if(!$(quantity).val().match(regex)){
            showValidate(quantity);
            check= false;
        }
        if($(category).find(":selected").text()=='Choose Category'){
            showValidate(category);
            check= false;
        }
        if($(color).find(":selected").text()=='Choose Color'){
            showValidate(color);
            check= false;
        }
        // if($(size).find(":selected").text()=='Choose Size'){
        //     showValidate(size);
        //     check= false;
        // }
        if($(type).find(":selected").text()=='Choose Type'){
            showValidate(type);
            check= false;
        }
        if( document.getElementById("file1").files.length == 0 ){
            document.getElementById('nofile').style.display='block';
            check=false;
        }
        else{
            document.getElementById('nofile').style.display='none';
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
       });
    });

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    
    

})(jQuery);
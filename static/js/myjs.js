
(function (jq) {

            function Menuclick(){
                  $('dt#menu').each(function () {
                    $(this).click(function () {
                        var display=$(this).parent().find('dd').css('display');
                        if  (display == 'block'){
                            $(this).parent().find('dd').css({display:"none"});
                            return false;
                        }else {
                            $(this).parent().find('dd').css({display:"block"});
                            $(this).parent().siblings('dl').find('dd').css({display:"none"});
                            return false;
                        }
                    })
                });
            }

    jq.extend({
        'Menu':function (outtag) {
                Menuclick();
        }
    })

})(jQuery);

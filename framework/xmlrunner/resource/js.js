$(document).ready(function(){
    var imgdivx = 0
    $('td.module_name').click(function(){
                var data_tag = $(this).attr('data-tag')
                var txt = $(this).text();
                if(txt == "Open") {
                    $(this).text("Close");
                    $('tr.'+data_tag).show()
                } else {
                    $(this).text("Open");
                    $('tr.'+data_tag).hide()
                    var _td = $('tr.'+data_tag).children('td.module_td_view')
                    for (bottomtd in _td) {
                        var closetr = _td.eq(bottomtd).attr('data-tag')
                        if (typeof(closetr) != "undefined")
                            $(_td.eq(bottomtd)).text("Open")
                            $('.' + closetr).hide()
                    }
                }
            })

    $('td.module_td_view').click(function(){
                var data_tag = 'tr.' + $(this).attr('data-tag')
                var txt = $(this).text();
                if(txt == "Open") {
                    $(this).text("Close");
                    $(data_tag).show()
                } else {
                    $(this).text("Open");
                    $(data_tag).hide()
                }
            })

    $('img.leftbutton').click(function () {

            var imgdivroot = $(this).parent().next()
            var imgdiv = $(imgdivroot).children()
            // var newx = 0
            // for (i = 0; i < imgdiv.length; i++) {
            //     var div = imgdiv[i]
            //     var x = $(div).css("transform").replace(/[^0-9.\-,]/g,'').split(',')[4];
            //     x = parseFloat(x)
            //
            //     if (x == 0){
            //         $(div).css("transform","translate3d(-100%,0px,0px)");
            //     }else {
            //         if (imgdivx == 0){
            //             imgdivx = x
            //         }
            //         newx = x + imgdivx
            //         $(div).css("transform","translate3d(" + newx +"px,0px,0px)");
            //
            //         if(x/(imgdiv.length-1) == imgdivx){
            //             $(div).css("transform","translate3d(0px,0px,0px)");
            //         }else {
            //             newx = x + imgdivx
            //             $(div).css("transform","translate3d(" + newx +"px,0px,0px)");
            //         }
            //
            //     }
            //
            // }
            var newdiv = imgdiv[0]
            $(imgdivroot).append($(newdiv)[0].outerHTML.replace(/translate3d\(([0-9]*px)|translate3d\((-100%)/g,"translate3d(0px"))
            $(imgdivroot).children()[0].remove()

    })
    $('img.rightbutton').click(function () {
            var imgdivroot = $(this).parent().next()
            var imgdiv = $(imgdivroot).children()
            var newdiv = imgdiv[imgdiv.length-1]
            $(imgdivroot).prepend($(newdiv)[0].outerHTML.replace(/translate3d\(([0-9]*px)|translate3d\((-100%)/g,"translate3d(0px"))
            $(imgdivroot).children()[imgdiv.length].remove()

    })
})
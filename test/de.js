 function do_delete() {
        var filename = $("#upload_message").val();
        layui.use(['upload', 'layer'], function () {
            var layer = layui.layer;
            $.ajax({
                url: '/delete?filename=' + filename + "&timestamp=" + new Date().getTime()
                , type: 'GET'
                , success: function (response) {
                    console.log(response)
                    if (response.code == 0) {
                        layer.msg('"' + filename + '"删除成功！');
                        $("#upload_message").val('')
                        $("img_delete").hide()
                    } else {
                        layer.msg('"' + filename + '"删除失败！');
                    }
                }
            })
        })
    }
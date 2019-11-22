 layui.use(['upload', 'layer'], function () {
        var upload = layui.upload;
        var layer = layui.layer;
        upload.render({
            elem: '#upload'
            , url: '/upload'
            , accept: 'file'
            , exts: 'txt'
            , size: 2048
            , done: function (res) {
                console.log(res);
                if (res.code === 0) {
                    layer.msg(res.filename + '上传成功');
                    $("#upload_message").val(res.filename);
                    $("#img_delete").show()
                } else {
                    layer.alert('上传失败');
                    $("#upload_message").val('上传失败！');
                }
            }
        });
    })
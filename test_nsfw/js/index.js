/**
 * Created by 子山 on 17/7/20.
 */
var json_data = {
    "Size": 194.2158203125,
    "Score": "0.66548126936",
    "Error": 0,
    "Status": "性感"
};
$("#demo-json").find('p').html(JSON.stringify(json_data, null, 4));

$("#demo-json").find('p').ajaxStart(function () {
    $(this).html("获取数据中...");
    $('#watermark').remove();
    $('#img_data').append("<div id='watermark' style='width: 100px;height: 100px;top:50%;left: 50%;position:absolute;margin-top:-51px;" +
        "margin-left:-51px;text-align:center;line-height: 100px;border-radius:50px;border:solid #fff 2px;'>" +
        "<span unselectable='on' onselectstart='return false;' style='color:#fff;font-size: 150%;font-weight: bold'>" + "请等待.." + "</span></div>");
});
function validateImage(url) {
    var xmlHttp;
    if (window.ActiveXObject) {
        xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    else if (window.XMLHttpRequest) {
        xmlHttp = new XMLHttpRequest();
    }
    try {
        xmlHttp.open("Get", url, false);
        xmlHttp.send();
    } catch (err) {
        return false;
    }
    if (xmlHttp.status == 404)
        return false;
    else
        return true;
}
$('#scan-photo').click(function () {
    url_test_nsfw($('#demo-photo-url').val(), 0);
});
function url_test_nsfw(url, type) {
    if (url) {
        var imgObjPreview = document.getElementById("preview");
        imgObjPreview.style.backgroundSize = '100% 350px';
        if (validateImage(url)) {
            imgObjPreview.src = url;
            $.ajax({
                url: "test_nsfw.php",
                type: "POST",
                data: {'img_url': url, type: type},
                success: function (data) {
                    var json_data = JSON.parse(data);
                    $("#demo-json").find('p').html(JSON.stringify(json_data, null, 4));
                    $('#watermark').remove();
                    $('#preview').css('-webkit-filter', '.6');
                    //$('#preview').css('filter', 'alpha(-webkit-filter=80)');
                    $('#img_data').append("<div id='watermark' style='width: 100px;height: 100px;top:50%;left: 50%;position:absolute;margin-top:-51px;" +
                        "margin-left:-51px;text-align:center;line-height: 100px;border-radius:50px;border:solid #fff 2px;'>" +
                        "<span unselectable='on' onselectstart='return false;' style='color:#fff;font-size: 250%;font-weight: bold'>" + json_data.Status + "</span><br/><span unselectable='on' onselectstart='return false;' style='font-size: 100%;color: #fff'>评分:" + parseInt(parseFloat(json_data.Score) * 100) +
                        "分</span></div>");

                },
                error: function (data) {
                }
            });
        } else {
            alert('获取图片失败!')
        }
    }
}
document.getElementById('doc').addEventListener('change', function () {
    setImagePreview();
    //document.getElementById('my_form').submit();
    var formData = new FormData();
    formData.append("file", document.getElementById("doc").files[0]);
    //formData.append("img_url", document.getElementById("demo-photo-url").value);
    $.ajax({
        url: "test_nsfw.php",
        type: "POST",
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            var json_data = JSON.parse(data);
            $("#demo-json").find('p').html(JSON.stringify(json_data, null, 4));
            $('#watermark').remove();
            $('#preview').css('-webkit-filter', '.6');
            //$('#preview').css('filter', 'alpha(-webkit-filter=80)');
            $('#img_data').append("<div id='watermark' style='width: 100px;height: 100px;top:50%;left: 50%;position:absolute;margin-top:-51px;" +
                "margin-left:-51px;text-align:center;line-height: 100px;border-radius:50px;border:solid #fff 2px;'>" +
                "<span unselectable='on' onselectstart='return false;' style='color:#fff;font-size: 250%;font-weight: bold'>" + json_data.Status + "</span><br/><span unselectable='on' onselectstart='return false;' style='font-size: 100%;color: #fff'>评分:" + parseInt(parseFloat(json_data.Score) * 100) +
                "分</span></div>");
        },
        error: function (data) {
        }
    });
});
function setImagePreview(avalue) {
    var docObj = document.getElementById("doc");

    var imgObjPreview = document.getElementById("preview");
    if (docObj.files && docObj.files[0]) {
        //imgObjPreview.style.backgroundSize = '590px 350px';
        imgObjPreview.src = window.URL.createObjectURL(docObj.files[0]);
    }
    else {
//IE下，使用滤镜
        docObj.select();
        var imgSrc = document.selection.createRange().text;
        var localImagId = document.getElementById("localImag");
//必须设置初始大小
        localImagId.style.width = "150px";
        localImagId.style.height = "180px";
//图片异常的捕捉，防止用户修改后缀来伪造图片
        try {
            localImagId.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=scale)";
            localImagId.filters.item("DXImageTransform.Microsoft.AlphaImageLoader").src = imgSrc;
        }
        catch (e) {
            alert("您上传的图片格式不正确，请重新选择!");
            return false;
        }
        imgObjPreview.style.display = 'none';
        document.selection.empty();
    }
    return true;
}

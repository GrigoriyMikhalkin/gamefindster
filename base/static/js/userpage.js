$(".modal-header").hide();
$("#id_avatar").attr("onchange","PreviewImage();");

function PreviewImage() {
    var fileReader = new FileReader();
    fileReader.onload = function (img) {
        var image = new Image();
        image.src = img.target.result;

        image.onload = function() {
            var modalHeight = $("body").height();
            var modalWidth = $("#profilepic-body").width();
            var imgHeight = image.height;
            var imgWidth = image.width;

            if (modalHeight < imgHeight){
			      newImgHeight = modalHeight;
			      imgWidth = (newImgHeight*imgWidth)/imgHeight;
			      imgHeight = newImgHeight;
			      }

            if (modalWidth < imgWidth){
			     newImgWidth = modalWidth;
			     imgHeight = (newImgWidth*imgHeight)/imgWidth;
			     imgWidth = newImgWidth;
			     }

	    var style = "width:"+imgWidth+"px;height:"+imgHeight+"px";
	
            $("#img_preview").attr("style", style);
            $("#preview-header").show();
            document.getElementById("img_preview").src = img.target.result;
	};
    };

    var img = document.getElementById("id_avatar").files[0];
    fileReader.readAsDataURL(img);
} 

$("#large-image").click( function(){
    $("#gallery-body").show();
    $("#large-image-header").hide();
});

$(".modal-pic").click( function () {
    $("#gallery-body").hide();
    $("#large-image-header").show();

    var img_src = $(this).data("large");
    $("#large-image").attr("src",img_src);
});

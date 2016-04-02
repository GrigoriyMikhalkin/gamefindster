var sidebar_collapse = $("#sidebar-collapse");
var sidebar_expand = $("#sidebar-expand");

// Init
sidebar_expand.hide();

sidebar_collapse.on("click",function(){
    sidebar_collapse.hide();
    sidebar_expand.show();
});

sidebar_expand.on("click",function(){
    sidebar_expand.hide();
    sidebar_collapse.show();
});

$("#menu-toggle").click( function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("menuDisplayed");
});

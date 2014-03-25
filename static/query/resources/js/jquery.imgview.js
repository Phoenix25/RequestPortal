$.fn.imgview = function(){
	this.each(function(){
		$(this).load(function(){
			var w = $(this).css("width");
			var h = $(this).css('height');
			$(this).parent().append('<div class="imgview-img-overlay" style="top:'+($(this).offset().top-$(this).parent().offset().top)+'px;width:'+w+';height:'+h+';z-index:2;position:absolute;background-color:#FFF;opacity:0.1"><span class="glyphicon glyphicon-search imgview-zoom" style="position:absolute;top:50%;width:50%;text-align:center"></span></div>');
			
		});
	});
}

$(window).load(function(){
	$('.imgview-img-overlay').hover(function(){
		$(this).animate({'opacity':'0.5'},200);
	},function(){
		$(this).animate({'opacity':'0.0'},200);
	});
});
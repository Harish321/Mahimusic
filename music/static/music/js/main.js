
var AlbumsListPage = {
	init: function() {
		this.$container = $('.albums-container');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.btn-favorite', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.glyphicon-star', self).toggleClass('active');
				}
			});

			return false;
		});
	}
};

var SongsListPage = {
	init: function() {
		this.$container = $('.songs-container');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.btn-favorite', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.glyphicon-star', self).toggleClass('active');
				}
			});

			return false;
		});
	}
};

$(document).ready(function() {
	AlbumsListPage.init();
	SongsListPage.init();
});

function replace(link) {
        $(".impor").empty();
        $.ajax({url: link, success: function(result){
                var i = $(result).find(".impo").html();  
                $(".impor").append(i);
                $(result).find("script").each(function(i) {
                    eval($(this).text());
                });
                }
              });
};

function addalbumscript(addlink,refreshlink){
	 $.ajax({
		url: addlink,
	  }).then(()=>{$(".impor").empty();
	  $.ajax({url: refreshlink, success: function(result){
		var i = $(result).find(".impo").html();  
		$(".impor").append(i);
		$(result).find("script").each(function(i) {
			eval($(this).text());
		});
		}
	  })})
	  ; 
}
/*
function deletesong(deletelink,albumlink){
	deletesong;
	if album exist
		replace the album
	else 
		replace homepage
*/

function deletesong(link,albumlink) {
	$.ajax({
		url:link,
		success:function (result) {
			if(result.album == true)
				replace(albumlink);
			else
				replace(albums);
		},
	})
}
function playthisalbum(albumid){
	$.ajax({
		url:'/api/songsurl/'+albumid+'/?format=json',
		success:function(result){
			var array = $.map(result, function(value, index) {
				return [value.audio_file];
			});
			playthislist(array);
		}
	});
}
window.addEventListener('keydown', function(e) {
	if(e.keyCode == 32 && e.target == document.body) {
	  e.preventDefault();
	}
  });
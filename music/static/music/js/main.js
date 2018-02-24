
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
                }
              });
};

var albums_button = $("#albums_button");
var songs_button = $("#songs_button");
var playlists_button = $("#playlists_button");
var users_button = $("#users_button"); 

function ActiveClass(butn) {
    albums_button.removeClass("active");
    songs_button.removeClass("active");
    playlists_button.removeClass("active");
    users_button.removeClass("active");
    butn.addClass("active");
}
albums_button.click(function () {
    replace("http://localhost:8000/music/");
});
songs_button.click(function () {
    replace("http://localhost:8000/music/songs/all/");
});
playlists_button.click(function () {
    replace("http://localhost:8000/music/playlists/");
});
users_button.click(function(){
    replace("http://localhost:8000/music/users/");
})
albums_button.click(function () {
    ActiveClass(albums_button);
});
songs_button.click(function () {
    ActiveClass(songs_button);
});
playlists_button.click(function () {
    console.log("hi")
    ActiveClass(playlists_button);
});
users_button.click(function(){
    ActiveClass(users_button);
})
$(function(){
    // Ajax call for search //
    $('#search').keyup(function(){
        $.ajax({
            type: "POST",
            url: "/search",
            data:{
                'search_text':$('#search').val(),
                'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        })
    })
    // Ajax call for add_song modal //
    $('#addsong').click(function(){
        $.ajax({
            type: "GET",
            url: "/music/create_song/",
            success: putmodal,
            dataType: 'html'
        })
    })

    // Ajax call for add_playlist modal
    $('#addplaylist').click(function () {
        $.ajax({
            type : "GET",
            url :"/music/create_playlist/",
            success: putmodal,
            dataType:'html'
        })
    })
    // Ajax call for add song to database//
    var bar = $('.bar');
    var percent = $('.percent');
    var status = $('#status');
    $('#songfile').ajaxForm({
        url:"/music/create_song/",
        type:'POST',
        beforeSend: function() {
            status.empty();
            var percentVal = '0%';
            bar.width(percentVal);
            percent.html(percentVal);
        },
        uploadProgress: function(event, position, total, percentComplete) {
            var percentVal = percentComplete + '%';
            bar.width(percentVal);
            percent.html(percentVal);
        },
        complete: function(xhr) {
            status.html(xhr.responseText);
            addsongdbSuccess();
            replace(albums);

        }
    });

    //submits form;
    //removes modal;
    //replace playlists page;
    $('#playlistform').ajaxForm({
        url:"/music/create_playlist/",
        type:'POST',
        complete:function() {
            $('#myModal').css('display','none');
            replace(playlists);
        }
    });

});

function searchSuccess(data,textStatus,jqXHR){
    $('#dropdown-content').css('display','block');
    $('#dropdown-content').html(data);
    if($('#search').val().length<1){
        $('#dropdown-content').css('display','none');
    }
}

function putmodal(data,textStatus,jqXHR){
    $('#myModalcontent').html(data);
}
function addsongdbSuccess(data,textStatus,jqXHR){
    $('#myModal').css('display','none');
}
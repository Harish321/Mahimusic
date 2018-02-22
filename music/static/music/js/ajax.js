$(function(){
    $('#search').keyup(function(){
        $.ajax({
            type: "POST",
            url: "search",
            data:{
                'search_text':$('#search').val(),
                'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        })
    })
    $('#addsong').click(function(){
        $.ajax({
            type: "POST",
            url: "/music/create_song/",
            data:{
                'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
            },
            success: addsongSuccess,
            dataType: 'html'
        })
    })
    // $('#addsubmit').click(function(event){
    //     alert('formgetsubmited');
    //     event.preventDefault();
    //     // var $audio_file = ;
    //     var form = $('#songfile')[0];
    //     var data = new FormData(form);
    //     data.append('csrfmiddlewaretoken',$("input[name=csrfmiddlewaretoken]").val());
    //     $.ajax({
    //         type:"POST",
    //         url: "/music/create_song/",
    //         data:data,
    //         success: addsongdbSuccess,
    //         dataType: 'html'
    //     })
        
    // })

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
        }
    })
    
});

function searchSuccess(data,textStatus,jqXHR){
    $('#search_result').html(data);
    // console.log(data);
}

function addsongSuccess(data,textStatus,jqXHR){
    $('#myModalcontent').html(data);
    // console.log(data);
}

function addsongdbSuccess(data,textStatus,jqXHR){
    // alert('song added successfully to database');
    $('#myModal').css('display','none');
}
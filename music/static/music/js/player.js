    /**
    stores url of all songs in list and plays one by one
    */
    var list=[]
    var current = 0;
    var audio = document.getElementById('audio');
    var next  = current +1;    
    function play(item){
        audio.pause();
        audio.src = list[item];
        audio.load();
        audio.play(); 
    }
    function playnext(item){
        next = item+1;
        if(next <= list.length-1)
            current = next;
        else
            current = 0;
        play(current)
    }
    function playall(){ 
        list = listbuffer;
        current = 0;
        play(current)

        audio.addEventListener('ended',function(){
            playnext(current)
        });
    }
    function playthis(url) {
        audio.pause();
        audio.src = url;
        audio.load();
        audio.play();
    }
    function playthislist(l){
        list = l;
        playall();
    }
    window.addEventListener("keydown", handle, true);
    function handle(e) {
        var keyCode = e.keyCode;
        if(keyCode==78) {
            playnext(current)
        }
        if (keyCode == 32) {
            if (audio.paused) {
                audio.play();
            }
            else
                audio.pause();
        }
        if (keyCode == 40) {
            //decreases volume of the player ---- down arrow
            audio.volume = audio.volume - 0.1;
            if ((audio.volume - 0.1 ) < 0){
                audio.volume = 0;
            }
        }
        if (keyCode == 38) {
            //increases  volume of the player ----- up arrow
            audio.volume = audio.volume + 0.1;
        }
        
}
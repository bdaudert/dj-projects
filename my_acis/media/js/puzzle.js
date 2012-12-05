    /*
    (C) www.dhtmlgoodies.com, September 2005
    
    You are free to use this script as long as the copyright message is kept intact
    
    
    Alf Magne Kalleland
    
    */
    var MEDIA_URL = document.getElementById("MEDIA_URL").value;    
    var puzzleImages = [MEDIA_URL +'img/PrismAnnMaxt.png', MEDIA_URL + 'img/PrismAnnPrecip.png', MEDIA_URL + 'img/PrismAnnMint.png'];   // Array of images to choose from
    var rows = 3;
    var cols = 4;
        
    var imageArray = new Array();
    var imageInUse = false;
    var puzzleContainer;
    var activeImageIndicator = false;
    var activeSquare = false;   // Reference to active puzzle square
    var squareArray = new Array(); // Array with references to all the squares

    
    var emptySquare_x;
    var emptySquare_y;
    
    var colWidth;
    var rowHeight;
    
    var gameInProgress = false;
    
    var revealedImage = false;
    
    for(var no=0;no<puzzleImages.length;no++){
        imageArray[no] = new Image();
        imageArray[no].src = puzzleImages[no];  
    }
    
    function initPuzzle()
    {
        gameInProgress = false;
        var tmpInUse = imageInUse;
        imageInUse = imageArray[Math.floor(Math.random() * puzzleImages.length)];
        if(imageInUse==tmpInUse && puzzleImages.length>1)
            initPuzzle();
        else{
            puzzleContainer = document.getElementById('puzzle_container');
            getImageWidth();
        }
    }
    
    function getImageWidth()
    {
        if(imageInUse.width>0){
            startPuzzle();  
        }else{
            setTimeout('getImageWidth()',100);  
        }
    }
    
    function scramble()
    {
        gameInProgress = true;
        var currentRow = cols-1;
        var currentCol = rows-1;
        
        document.getElementById('revealedImage').style.display='none';
        
        for(var no=0;no<rows;no++){
            for(var no2=0;no2<cols;no2++){
                if(no<rows.length || no2<cols.length){
                    var el = document.getElementById('square_' + no2 + '_' + no);
                    if(el){
                        el.style.left = (no2 * colWidth) + (no2) + 'px';
                        el.style.top = (no * rowHeight) + (no) + 'px';  
                    }else{
                        initPuzzle();
                        return;
                    }
                }           
            }
        }       
        
        
        var lastPos=false;
        var countMoves = 0;
        while(countMoves<(50*cols*rows)){
            var dir = Math.floor(Math.random()*4);
            var readyToMove = false;
            if(dir==0 && currentRow>0 && lastPos!=1){   // Moving peice down
                currentRow = currentRow-1;  
                readyToMove = true;
            }               
            if(dir==1 && currentRow<(rows-1) && lastPos!=0){    // Moving peice up
                currentRow = currentRow+1;
                readyToMove = true;
            }   
            if(dir==2 && currentCol>0 && lastPos!=3){   // Moving peice right
                currentCol = currentCol -1;
                readyToMove = true;
            }   
            if(dir==3 && currentCol<(cols-1) && lastPos!=2){    // Moving peice right
                currentCol = currentCol + 1;
                readyToMove = true;
            }
            if(readyToMove){
                activeSquare = document.getElementById('square_' + currentCol + '_' + currentRow);
                moveImage(false,true);  
                lastPos = dir;
                countMoves++;
            }
        }
        
        return;
    }
    
    function gameFinished()
    {
        var string = "";

        var squareWidth = colWidth + 1;
        var squareHeight = rowHeight + 1;       
        var squareCounter = 0;
        var errorsFound = false;
        var correctSquares = 0;
        for(var prop in squareArray){
            var currentCol = squareCounter % cols; 
            var currentRow = Math.floor(squareCounter/cols);
            var correctLeft = currentCol * squareWidth;
            var correctTop = currentRow * squareHeight;
            if(squareArray[prop].style.left.replace('px','') != correctLeft || squareArray[prop].style.top.replace('px','') != correctTop){
                //return;           
            }else{
                correctSquares++;
            }
                
            squareCounter++;    
        }   
        
        if(correctSquares == ((cols * rows) -1)){
            document.getElementById('messageDiv').innerHTML = '<h2>Fantastic! You did it !!</h2>';
            gameInProgress = false;
            revealImage();
            
        }else{
            document.getElementById('messageDiv').innerHTML = 'Currently, you have ' + correctSquares + ' out of ' + ((cols * rows) -1) + ' pieces placed correctly';
        }
        
    }
    
    var currentOpacity = 0;
    function revealImage()
    {
        if(currentOpacity==100)currentOpacity=0;
        var obj = document.getElementById('revealedImage');
        obj.style.display = 'block';
        currentOpacity = currentOpacity +2;
        if(document.all){
            obj.style.filter = 'alpha(opacity='+currentOpacity+')';
        }else{
            obj.style.opacity = currentOpacity/100;
        }
        
        if(currentOpacity<100)setTimeout('revealImage()',10);
        
    }
    function displayActiveImage()
    {
        if(!gameInProgress)return;
        if(!activeImageIndicator){
            activeImageIndicator = document.createElement('DIV');
            activeImageIndicator.className = 'activeImageIndicator';
            puzzleContainer.appendChild(activeImageIndicator);
            activeImageIndicator.onclick = moveImage;
            
        }
        activeImageIndicator.style.display='block';
        activeImageIndicator.style.left = this.offsetLeft +  'px';
        activeImageIndicator.style.top = this.offsetTop + 'px';
        activeImageIndicator.style.width = this.style.width;
        activeImageIndicator.style.height = this.style.height;
        activeImageIndicator.innerHTML = '<span></span>';
        activeSquare = this;
    }
    
    function moveImage(e,fromShuffleFunction)
    {
        if(!activeSquare)return;
        if(!gameInProgress && !fromShuffleFunction){
            alert('You have to shuffle the cards first');
            return;
        }
        var currentLeft = activeSquare.style.left.replace('px','') /1;
        var currentTop = activeSquare.style.top.replace('px','') /1;
        
        var diffLeft = Math.round((currentLeft - emptySquare_x) / colWidth);
        var diffTop = Math.round((currentTop - emptySquare_y) / rowHeight); 
        
        if(((diffLeft==-1 || diffLeft==1) && diffTop==0) || ((diffTop==-1 || diffTop==1) && diffLeft==0)){  // Moving right
            activeSquare.style.left = emptySquare_x + 'px';
            activeSquare.style.top = emptySquare_y + 'px';
            emptySquare_x = currentLeft;
            emptySquare_y = currentTop; 
            activeSquare = false;   
            if(activeImageIndicator)activeImageIndicator.style.display = 'none';
            if(!fromShuffleFunction)gameFinished(); 
        }
    }
    
    function startPuzzle()
    {
        puzzleContainer.innerHTML = '';


        var subDivs = puzzleContainer.getElementsByTagName('DIV');
        for(var no=0;no<subDivs.length;no++){
            subDivs[no].parentNode.removeChild(subDivs[no]);
        }
        activeImageIndicator = false;
        squareArray.length = 0; 

        
        if(document.getElementById('revealedImage')){
            var obj = document.getElementById('revealedImage');
            obj.parentNode.removeChild(obj);
        }
        var revealedImage = document.createElement('DIV');
        revealedImage.style.display='none';
        revealedImage.id='revealedImage';;
        revealedImage.className='revealedImage';;
        var img = document.createElement('IMG');
        img.src = imageInUse.src;
        revealedImage.appendChild(img);
        puzzleContainer.appendChild(revealedImage);
            
        colWidth = Math.round(imageInUse.width / cols)-1;
        rowHeight = Math.round(imageInUse.height / rows)-1;

        puzzleContainer.style.width = colWidth * cols + (cols * 1) + 'px';
        puzzleContainer.style.height = rowHeight * rows + (rows * 1) + 'px';
        
        if(navigator.appVersion.indexOf('5.')>=0 && navigator.userAgent.indexOf('MSIE')>=0){
            puzzleContainer.style.width = colWidth * cols + (cols * 1) + 20 + 'px';
            puzzleContainer.style.height = rowHeight * rows + (rows * 1) + 20 + 'px';           
            
        }
                
        if(!revealedImage){
            revealedImage = document.createElement('DIV');
            revealedImage.style.display='none'; 
            revealedImage.innerHTML = '';
            
        }
        for(var no=0;no<rows;no++){
            for(var no2=0;no2<cols;no2++){
                if(no2==cols-1 && no==rows-1){
                    emptySquare_x = (no2 * colWidth) + (no2);   
                    emptySquare_y = (no * rowHeight) + (no);    
                    break;
                }
                var newDiv = document.createElement('DIV');
                newDiv.id = 'square_' + no2 + '_' + no;
                newDiv.onmouseover = displayActiveImage;
                newDiv.onclick = moveImage;
                newDiv.className = 'square';
                newDiv.style.width = colWidth + 'px';
                newDiv.style.height = rowHeight + 'px'; 
                newDiv.style.left = (no2 * colWidth) + (no2) + 'px';
                newDiv.style.top = (no * rowHeight) + (no) + 'px';
                newDiv.setAttribute('initPosition',(no2 * colWidth) + (no2) + '_' + (no * rowHeight) + (no));
                var img = new Image();
                img.src = imageInUse.src;
                img.style.position = 'absolute';
                img.style.left = 0 - (no2 * colWidth) + 'px';
                img.style.top = 0 - (no * rowHeight) + 'px';
                newDiv.appendChild(img);                
                puzzleContainer.appendChild(newDiv);
                squareArray.push(newDiv);
            }
        }   
        
        
    }
    window.onload = initPuzzle;


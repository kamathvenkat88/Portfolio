let nav = document.getElementById('nav');
let navTop = nav.offsetTop;

audio = new Audio('../static/r u gonna be my girl.mp3');
function play(){
	if(!audio.paused)
		audio.pause();
	else
		audio.play();
	document.getElementById('playButton').classList.toggle('paused');
}

window.onscroll = function(){ // creating a function that runs everytime the user scrolls//
	var currentScroll =window.pageYOffset; // scroll Y position
	let padding = document.getElementsByClassName('padding')[0];
	let part1 = document.getElementsByClassName('part1')[0];
	let head = document.getElementById('head');
	let main = document.getElementById('main');

	if (currentScroll>=20){ 
		part1.style.width = '100vw';
		padding.style.marginLeft = '0';
	}
	else if (currentScroll == 0) 
		main.style.display = 'none';
	

	if(currentScroll > navTop){
		nav.classList.add('fixed');
		document.getElementById('main').style.paddingTop = '40px';
	}
	else{
		nav.classList.remove('fixed');
		document.getElementById('main').style.paddingTop = '0px';
	}
}

let idx = 0;
let portfolios = ['Manager', 'Engineer', 'Owner', 'Analyst', 'Designer', 'Lead'];
let fonts = ['Playfair Display', 'Indie Flower', 'Kanit','Pacifico', 'Caveat', 'Satisfy'];

function shuffle(portfolio){
	var shuffleInterval= setInterval( ()=>{
		let randomPortfolio= portfolios[Math.floor(Math.random()*portfolios.length)];
		let randomFont= fonts[Math.floor(Math.random()*fonts.length)];
		let div= document.getElementById('title2');
		div.innerHTML= randomPortfolio;
		div.style.fontFamily = randomFont;
	}, 100);
	setTimeout(()=>{
		clearInterval(shuffleInterval);
		let div= document.getElementById('title2');
		div.innerHTML= portfolio;
		div.style.fontFamily = fonts[0];
	}, 2000)
}

shuffle(portfolios[idx]);
setInterval(()=>{
	idx+=1;
	idx%=portfolios.length;
	shuffle(portfolios[idx]);
}, 5000);


function show(id){
	document.getElementById(id).style.display = 'block';
}

function active(nav){
	nav.classList.add('active');
}
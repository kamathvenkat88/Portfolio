let idx = 0;// to index the portfolios
let portfolios = ['Manager', 'Engineer', 'Owner', 'Analyst', 'Designer', 'Lead']; //list of portfolios
let fonts = ['Playfair Display', 'Indie Flower', 'Kanit','Pacifico', 'Caveat', 'Satisfy']; //list of fonts		
let nav = document.getElementById('nav'); //extracting element with id nav
let navTop = nav.offsetTop; //Distance from top of the page to the top of the navbar

window.onscroll = function(){ // creating a function that runs everytime the user scrolls
	var currentScroll =window.pageYOffset; // scroll Y position
	let padding = document.getElementsByClassName('padding')[0]; //Padding corresponds to the class with the same name in index.html. 0 Indicates the first element
	let part1 = document.getElementsByClassName('part1')[0];
	let main = document.getElementById('main'); // extracting element with id main

	if (currentScroll >= 20){ //checks if the scroll is greater than 20 points 	
		part1.style.width = '100vw'; //Changes the width of html element with Class part1 to 100%
		padding.style.marginLeft = '0'; //Changes the margin of first (padding[0]) html element with Class padding to 0
	}
	else if (currentScroll == 0) // Check if the scroll is back at the initial position (0)
		main.style.display = 'none'; //Hide the navigation container
	

	if(currentScroll > navTop){ //Check if current scroll position is equal to distance from top of page to the Navbar
		nav.classList.add('fixed');// Add class fixed to the Navbar
		main.style.paddingTop = '40px'; // to prevent content from hiding behind the Navbar
	}
	else{
		nav.classList.remove('fixed'); // remove fixed from Navbar
		main.style.paddingTop = '0px'; //Removes padding from navigation container
	}
}

function shuffle(portfolio){ 
	//font and text changing part
	var shuffleInterval= setInterval( ()=>{
		let randomIndex_01_decimal = Math.random();//random decimal value between 0 and 1
		let randomIndex_06_decimal = randomIndex_01_decimal * portfolios.length; //increasing the range from 0-1 to 0-6
		let randomIndex_06_integral = Math.floor(randomIndex_06_decimal); //flooring the above value to get an integer
		let randomPortfolio= portfolios[randomIndex_06_integral]; //selecting a random portfolio
		let randomFont= fonts[Math.floor(Math.random()*fonts.length)]; //selecting a random font for the portfolio
		let div= document.getElementById('title2'); //selecting the div that holds the portfolio.
		div.innerHTML= randomPortfolio; //setting the portfolio
		div.style.fontFamily = randomFont; //setting the font to the portfolio
	}, 100); // running the above 8 lines of code every 100ms

	setTimeout(()=>{
		clearInterval(shuffleInterval); //stopping the above repeating lines of code
		let div= document.getElementById('title2'); //selecting the div that holds the portfolio.
		div.innerHTML= portfolio; // setting the portfolio specified to be shown in order.
		div.style.fontFamily = fonts[0]; //reset font of the portfolio.(to default)
	}, 2000); //the above 4 lines of code run after 2s.
}

function show(id){
	document.getElementById(id).style.display = 'block'; // display= block means show, display= none means hide
}

function active(nav){
	nav.classList.add('active'); // adding class active to the selected nav tab
}

shuffle(portfolios[idx]); //Calling shuffle with the end string as portfolios[idx]
setInterval(()=>{
	idx+=1; //increment idx
	idx%=portfolios.length; //wraparound idx to 0 when equal to portfolios.length 
	shuffle(portfolios[idx]);
}, 5000);//repeats a functon after a specified interval of time.

'use strict'

$(function()
{
	//INITIALIZATION
	
	function rndNum(from, to)
	{
		return Math.floor((Math.random() * (to - from + 1)) + from);
	}
	
	var screen =
	{
		width:	800,
		height:	400
	};
	
	var paddle = 
	{
		width:	20,
		height:	60,
		speed: 	10
	};
	
	var ball =
	{
		size:		20,
		x:			(screen.width 	/ 2) - 10,
		y:			(screen.height	/ 2) - 10,
		speed:		5,
		velocityX:	5,
		velocityY:	rndNum(1, 15),
		rebound:	function()
					{
						if (ball.velocityX > 0) 		ball.velocityX = -ball.speed;
						else if (ball.velocityX < 0) 	ball.velocityX =  ball.speed;
						
						if (ball.velocityY > 0) 		ball.velocityY =  rndNum(1,15);
						else if (ball.velocityY < 0) 	ball.velocityY = -rndNum(1,15);
						
						ball.speed++;
					},
		intersects:	function(thePaddle)
					{
						if ((ball.x 				>= thePaddle.x && ball.x 				<= thePaddle.x + thePaddle.width &&
							 ball.y 				>= thePaddle.y && ball.y 				<= thePaddle.y + thePaddle.height)
							||
							(ball.x + ball.size 	>= thePaddle.x && ball.x + ball.size 	<= thePaddle.x + thePaddle.width &&
							 ball.y 				>= thePaddle.y && ball.y 				<= thePaddle.y + thePaddle.height)
							||
							(ball.x + ball.size 	>= thePaddle.x && ball.x + ball.size 	<= thePaddle.x + thePaddle.width &&
							 ball.y + ball.size		>= thePaddle.y && ball.y + ball.size	<= thePaddle.y + thePaddle.height)
							||
							(ball.x					>= thePaddle.x && ball.x				<= thePaddle.x + thePaddle.width &&
							 ball.y + ball.size		>= thePaddle.y && ball.y + ball.size	<= thePaddle.y + thePaddle.height)) 
						{
							if (ball.velocityX > 0) ball.x = thePaddle.x - ball.size;
							else					ball.x = thePaddle.x + thePaddle.width;
							ball.rebound();
							$('#screen').animate(
							{
								opacity:	0.95
							}, 200, function() { $(this).animate({opacity: 1.0}) })
						}
					}
	};
	
	function Player(startX, startY)
	{
		this.x			= startX;
		this.y			= startY;
		this.width		= paddle.width;
		this.height		= paddle.height;
		this.speed		= paddle.speed;
		this.velocity	= 0;
		this.score		= 0;
	};
	
	var playerOne = new Player(0, 					(screen.height / 2) - (paddle.height / 2));
	var playerTwo = new Player(screen.width - 20, 	(screen.height / 2) - (paddle.height / 2));
	
	$('body')
	.append('<div id="screen"></div>')
	.append('<div id="scoreboard"></div>')
	.append('<div id="help"></div>')
	.css('position', 'relative');
	
	$('#screen')
	.append('<div id="player_one" class="paddle"></div>')
	.append('<div id="player_two" class="paddle"></div>')
	.append('<div id="ball"></div>')
	.css('width', 	screen.width)
	.css('height', 	screen.height)
	.css('background-color', 'black');
	
	$('#scoreboard')
	.html("PLAYER 1: " + String(playerOne.score) + "</br>PLAYER 2: " + String(playerTwo.score))
	.css('font-size', '2em')
	.css('font-family', 'Arial')
	.css('font-weight', 'bold')
	.css('width', 	300)
	.css('background-color', 'yellow')
	.css('margin-top', '30px')
	.css('padding', '20px')
	.css('border-radius', '20px')
	.css('float', 'left');
	
	$('#help')
	.html("Press Q and A to move player 1. Press P and L for player 2.")
	.css('font-size', '1.2em')
	.css('font-family', 'Arial')
	.css('font-weight', 'bold')
	.css('width', 	300)
	.css('background-color', 'green')
	.css('margin-top', '30px')
	.css('margin-left', '30px')
	.css('padding', '20px')
	.css('border-radius', '20px')
	.css('float', 'left');
	
	$('.paddle')
	.css('width', 	paddle.width)
	.css('height', 	paddle.height)
	.css('background-color', 'grey')
	.css('position', 'absolute');
	
	$('#ball')
	.css('width', 	ball.size)
	.css('height', 	ball.size)
	.css('background-color', 'blue')
	.css('position', 'absolute')
	.css('left', 	ball.x)
	.css('top', 	ball.y)
	.css('border-radius', '50%/50%');
	
	$('#player_one')
	.css('left', 	playerOne.x)
	.css('top', 	playerOne.y);
	
	$('#player_two')
	.css('left', 	playerTwo.x)
	.css('top', 	playerTwo.y);
	
	//INPUT EVENTS
	
	$(document).keydown(function(evt)
	{
		if 		(String.fromCharCode(evt.which) == 'Q' || String.fromCharCode(evt.which) == 'q') playerOne.velocity = -paddle.speed;
		else if (String.fromCharCode(evt.which) == 'A' || String.fromCharCode(evt.which) == 'a') playerOne.velocity =  paddle.speed;
		
		if 		(String.fromCharCode(evt.which) == 'P' || String.fromCharCode(evt.which) == 'p') playerTwo.velocity = -paddle.speed;
		else if (String.fromCharCode(evt.which) == 'L' || String.fromCharCode(evt.which) == 'l') playerTwo.velocity =  paddle.speed;
	});
	
	$(document).keyup(function(evt)
	{
		if (String.fromCharCode(evt.which) == 'Q' || String.fromCharCode(evt.which) == 'A' ||
			String.fromCharCode(evt.which) == 'q' || String.fromCharCode(evt.which) == 'a')
			playerOne.velocity = 0;
		
		if (String.fromCharCode(evt.which) == 'P' || String.fromCharCode(evt.which) == 'L' ||
			String.fromCharCode(evt.which) == 'p' || String.fromCharCode(evt.which) == 'l')
			playerTwo.velocity = 0;
		//alert(String.fromCharCode(evt.which));
	});
	
	alert("Ready?");
	
	//GAME LOOP
	
	var run = function()
	{
		//Update state...
		
		playerOne.y += playerOne.velocity;
		playerTwo.y += playerTwo.velocity;
	
		ball.x += ball.velocityX;
		ball.y += ball.velocityY;
		
		//Check boundaries...
		
		if (playerOne.y > screen.height - playerOne.height) playerOne.y = screen.height - playerOne.height;
		else if (playerOne.y < 0) playerOne.y = 0;
		
		if (playerTwo.y > screen.height - playerTwo.height) playerTwo.y = screen.height - playerTwo.height;
		else if (playerTwo.y < 0) playerTwo.y = 0;
		
		if (ball.y > screen.height - ball.size)
		{
			ball.y = screen.height - ball.size;
			ball.velocityY = -ball.velocityY;
		}
		else if (ball.y < 0)
		{
			ball.y = 0;
			ball.velocityY = -ball.velocityY;
		}
		
		if (ball.x > screen.width - ball.size)
		{
			playerOne.score++;
			reset();
		}
		else if (ball.x < 0)
		{
			playerTwo.score++;
			reset();
		}
		
		//Define reset...
		
		function reset()
		{
			$('#screen').animate(
			{
				opacity:	0.5
			}, 200, function() { $(this).animate({opacity: 1.0}) })
			
			var inversion = 1;
			if (rndNum(0, 1) == 0) inversion = -1;
			
			ball.x = (screen.width 	/ 2) - (ball.size / 2);
			ball.y = (screen.height / 2) - (ball.size / 2);
			ball.speed = 5;
			ball.velocityX = ball.speed * inversion;
			ball.velocityY = rndNum(1, 15);
			
			$('#scoreboard')
			.html("Player 1: " + String(playerOne.score) + "</br>Player 2: " + String(playerTwo.score))
		}
		
		//Check for collision...
		
		ball.intersects(playerOne);
		ball.intersects(playerTwo);
		
		//Render...
		
		$('#ball')
		.css('left', 	ball.x)
		.css('top', 	ball.y);
		
		$('#player_one').css('top', playerOne.y);
		$('#player_two').css('top', playerTwo.y);
	};
	
	setInterval(run, 1000 / 30);
}); //end ready
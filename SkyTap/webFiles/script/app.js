$(document).ready(function(){
	$('.I').click(function() {
		$('img.I').addClass('hide');
		$('p.I').addClass('hide');
		$('table.I').fadeTo('slow', 1);
	});
	$('div.I').mouseleave(function() {
		$('img.I').removeClass('hide');
		$('p.I').removeClass('hide');
	});
	
	$('.II').click(function() {
		$('img.II').addClass('hide');
		$('p.II').addClass('hide');
		$('table.II').fadeTo('slow', 1);
	});
	$('div.II').mouseleave(function() {
		$('img.II').removeClass('hide');
		$('p.II').removeClass('hide');
	});
	
	$('.III').click(function() {
		$('img.III').addClass('hide');
		$('p.III').addClass('hide');
		$('table.III').fadeTo('slow', 1);
	});
	$('div.III').mouseleave(function() {
		$('img.III').removeClass('hide');
		$('p.III').removeClass('hide');
	});
	
	$('.IV').click(function() {
		$('img.IV').addClass('hide');
		$('p.IV').addClass('hide');
		$('table.IV').fadeTo('slow', 1);
	});
	$('div.IV').mouseleave(function() {
		$('img.IV').removeClass('hide');
		$('p.IV').removeClass('hide');
	});
});
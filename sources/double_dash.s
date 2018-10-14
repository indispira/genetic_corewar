.name		"Double_Dash"
.comment	"Oh, yeah! Who's number one now?!"

begin:
	ld		%0, r16
	sti		r1, %:start_dash, %1
	zjmp	%:init

start_dash_up:
	live	%42
	ld		%57675775, r15 #info stockee : st r15, FFxx (-256 avec le 00 qui suit)
	st		r15, -510
	st		r15, -505
	st		r15, -500
	st		r15, -495
	st		r15, -490
	st		r15, -485
	st		r15, -480
	st		r15, -475
	st		r15, -470
	st		r15, -465
	st		r15, -460
	st		r15, -455
	st		r15, -450
	st		r15, -445
	st		r15, -440
	st		r15, -435
	st		r15, -430
	st		r15, -425
	st		r15, -420
	st		r15, -410
	st		r15, -405
	st		r15, -400
	st		r15, -395
	st		r15, -390
	st		r15, -385
	st		r15, -380
	st		r15, -375
	st		r15, -370
	st		r15, -365
	st		r15, -360
	st		r15, -355
	st		r15, -350
	st		r15, -345
	st		r15, -340
	st		r15, -335
	st		r15, -330
	st		r15, -325
	st		r15, -320
	st		r15, -315
	st		r15, -310
	ld		%0, r16
	zjmp	%:start_dash_up

init:
	ldi		%:start_dash, %1, r1
	sti		r1, %:live, %1
	sti		r1, %:speedy_live, %1
	sti		r1, %:start_dash_up, %1
	sti		r1, %:start_dash_down, %1
	sti		r7, %:begin, %11

start_dash:
	live	%42
	fork	%:start_dash_down
	live	%42
	fork	%:start_dash_up
	live	%42
	fork	%:start_dash

live:
	live	%1
	and		%0, %0, r16
	fork	%:start_dash
	live	%1
	fork	%:live
	live	%1
	fork	%:speedy_live
	zjmp	%:live

speedy_live:
	live	%1
	zjmp	%:speedy_live

start_dash_down:
	live	%42
	ld		%57672193, r2 #info stockee : st r2, 01xx (256 avec le 00 qui suit)
	ld		%33554431, r3 #info stockee : live FFFFFFxx
	ld		%57672449, r4 #info stockee : st r3, 01xx
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r2, 256
	st		r4, 256

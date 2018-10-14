#hola

.name	"yop"
.comment "lait"

	live %0
	ld %-5, r2
fork %:bas
	st r1, 11
sti:
	sti r14, r2, r4
	live %0
	zjmp %-74
repeat:
	live %0
	fork %:repeat
	live %0
	fork %:trois
	fork %:deux
un:
	ldi %:sti, r16, r14
	ld %-64, r2
	and r5, r5, r5
	zjmp %:gogo
deux:
	ldi %:sti, %4, r14
	ld %-60, r2
	and r5, r5, r5
	zjmp %:gogo
trois:
	fork %:quatre
	ldi %:sti, %8, r14
	ld %-56, r2
	and r5, r5, r5
	zjmp %:gogo
quatre:
	ldi %:sti, %12, r14
	ld %-52, r2
	and r5, r5, r5
	zjmp %:gogo
gogo:
	live %0
#	fork %:gogo11
	live %0
	fork %:gogo22
	sti r14, %-251, r2
	and r5, r5, r5
	zjmp %-326
gogo11:
	live %0
	fork %:gogo33
	sti r14, %-257, r2
	and r5, r5, r5
	zjmp %-332
gogo22:
	sti r14, %-255, r2
	and r5, r5, r5
	zjmp %-330
gogo33:
	sti r14, %-255, r2
	and r5, r5, r5
	zjmp %-330

bas:
	st r1, 11
basbas:
	sti r1, r2, r4
	live %0
	zjmp %54
repeat123:
	live %0
	fork %:repeat123
	live %0
	fork %:trois123
#	live %0
	fork %:deux123
un123:
	ldi %:basbas, r16, r1
	ld %64, r2
	and r5, r5, r5
	zjmp %:gogo123
deux123:
	ldi %:basbas, %4, r1
	ld %68, r2
	and r5, r5, r5
	zjmp %:gogo123
trois123:
#	live %0
	fork %:quatre123
	ldi %:basbas, %8, r1
	ld %72, r2
	and r5, r5, r5
	zjmp %:gogo123
quatre123:
	ldi %:basbas, %12, r1
	ld %76, r2
	and r5, r5, r5
	zjmp %:gogo123
gogo123:
	live %0
#	fork %:gogo11123
	live %0
	fork %:gogo22123
	sti r1, %:startu, r2
	and r5, r5, r5
	zjmp %117
	aff r2
	aff r2
	aff r2
gogo11123:
	live %0
	fork %:gogo33123
	sti r1, %58, r2
	and r5, r5, r5
	zjmp %111
gogo22123:
	sti r1, %60, r2
	and r5, r5, r5
	zjmp %111
gogo33123:
	sti r1, %62, r2
	and r5, r5, r5
	zjmp %115
startu:

.name "Gatling"
.comment "on en a gros"
start:
    ld %0, r2
    ld %0, r2
protec:
    ld %17367040, r4
    st r4, -15
	sti	r1, %:attac, %1
    fork %:attac
wall_prep:
    ld %656, r2
head:
	ld %57672958, r11
	ld %1342242816, r12
	ld %47185930, r13
	ld %218759152, r14
	st r1, 6
	live %0
	st r11, -106
	st r12, -107
	st r1, -110
	st r13, -111
	st r14, -112
	fork %-131
wall:
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
    st r2, -508
    st r3, -509
    st r4, -510
	st r1, 6
    live %0
    zjmp %:wall
    ld %0, r3
    fork %:wall
new_proc:
    ld %5, r6
livefarm:
    st r1, 6
    live %0
    zjmp %:livefarm
    fork %:livefarm
    ld %0, r5
    zjmp %:livefarm
attac:
	live	%0
	ld  %507, r4
	ld  %507, r6
	ld  %24, r8
	ld  %190055170, r9
	ld  %67699190, r10
	st  r9, 487
	st  r10, 486
	sti	r1, %:proc1, %1
	sti	r1, %:proc2, %1
	fork %:proc2
proc1:
	live %0
	ld  %0, r2
	ld %190055682, r3
	ld %190056194, r5
	ld %190056194, r7
	ld  %0, r16
	zjmp %420
proc2:
	live %0
	ld  %4, r2
	ld %67699190, r3
	ld %134807571, r5
	ld %134807571, r7
	ld  %0, r16
	zjmp %377

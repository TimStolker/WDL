.cpu cortex-m0
.text
.align 4

.global even
.global odd

even:
push    {r7, lr}
add    r7, sp, #0
sub    sp, #4
str    r0, [sp]
ldr    r0, [sp]
cmp    r0, #0
beq    .LBB0_1
b    .LBB0_2

.LBB0_1:
mov    r0, #1
add    sp, #4
pop    {r7, pc}
b    .LBB0_2

.LBB0_2:
ldr    r0, [sp]
mov    r1, #1
sub    r0, r0, r1
str    r0, [sp]
ldr    r0, [sp]
b    odd
add    sp, #4
pop    {r7, pc}

odd:
push    {r7, lr}
add    r7, sp, #0
sub    sp, #4
str    r0, [sp]
ldr    r0, [sp]
cmp    r0, #0
beq    .LBB1_1
b    .LBB1_2

.LBB1_1:
mov    r0, #0
add    sp, #4
pop    {r7, pc}
b    .LBB1_2

.LBB1_2:
ldr    r0, [sp]
mov    r1, #1
sub    r0, r0, r1
str    r0, [sp]
ldr    r0, [sp]
b    even
add    sp, #4
pop    {r7, pc}



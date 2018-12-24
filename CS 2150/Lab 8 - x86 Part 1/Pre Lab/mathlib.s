 
; mathlib.s
;
; Author  : Gabriel Groover
; Date    : March, 28 2016
; Purpose : Product and power implementation
	
	global product

	section .text

;
; product
; Parameter 1  - first number
; Parameter 2  - second number
; Return value - product of two numbers
;

product:
	; Standard prologue
	push  ebp		; Save the old base pointer
	mov   ebp, esp		; Set new value of the base pointer
	push  esi		; Save registers

	xor   eax, eax		; Place zero in EAX. We will keep a running
				; sum of the product

	mov   esi, [ebp+8]	; Put the first number in esi
	mov   ecx, [ebp+12]	; Put the second number in ecx.
				; This will track how many iterations left

	cmp   ecx, 0		; If the second number is 0
	jle   product_done	; skip to the end and return
				; zero (already in EAX).
product_loop:
	mov   edx, esi		
	add   eax, edx		
				
	dec   ecx		; Decrement ECX, the counter of how many
				; left to do.
	cmp   ecx, 0		; if second num is 0
	jg    product_loop	; 

product_done:
	; Standard epilogue
	pop   esi		; Restore registers that we used.
				; Note - no local variables to dealocate.
	pop   ebp		; Restore the caller's base pointer.
	ret			; Return to the caller.

	global power

	section .text

;
; power
; Parameter 1  - base number
; Parameter 2  - power number
; Return value - base^power
;

power:
	; Standard prologue
	push  ebp		; Save the old base pointer
	mov   ebp, esp		; Set new value of the base pointer
	push  esi		; Save registers

	xor   eax, eax		; Place zero in EAX. 
	mov   esi, [ebp+8]	; Put the base number in esi
	mov   ecx, [ebp+12]	; Put the power number in ecx.

	cmp   ecx, 0		; If the power is not 0
	jg power_loop		;recurse	
	inc eax			;else
	jmp   power_done	;skip to the end and return 1
			
power_loop:
	dec ecx			;decrease power
	push ecx		;push parameters
	push esi		
	call power		;call power of n-1
	push eax		;push parameters
	push esi
	call product		;multiply base*power of n-1
			

power_done:
	; Standard epilogue
	pop   esi		; Restore registers that we used.
	mov esp, ebp			
	pop ebp			; Restore the caller's base pointer.
	ret			; Return to the caller.


 
; threexplusone.s
;
; Author  : Gabriel Groover
; Date    : March, 28 2016
; Purpose : Collatz conjecture
;
;Used lea instead of imul
;Used bit shifting instead of divide
;reduced registers on stack



; threexplusone
; Parameter 1  - number
; Return value - number of ops in collatz conjecture
;
global threexplusone
section .text

threexplusone:
	; Standard prologue
	push  ebp		; Save the old base pointer
	mov   ebp, esp		; Set new value of the base pointer

	xor   eax, eax		; Place zero in EAX. 
	mov   ecx, [ebp+8]	; Put the number number in esi
	cmp ecx,1		;check if number is one
	je end			;if so we are done
	and ecx, 1		;check if even
	cmp ecx, 0
	je threeplusloop	;recurse
	
	mov ebx, [ebp+8]	;move value into ebx
	lea ebx, [1+ebx*3]	;x = 3x+1
	push ebx
	call threexplusone
	inc eax			;inc op count
	
	jmp   end		;skip to the end
			
threeplusloop:
	mov ebx, [ebp+8]	;mov num into ebx
	sar ebx, 1
	push ebx		;push parameters		
	call threexplusone	;call threeplus(x/2)
	inc eax			;increase op count
end:
	leave			; Restore the caller's base pointer.
	ret			; Return to the caller.


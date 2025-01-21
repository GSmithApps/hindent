│   ─   ├   ┤   ┬   ┴   ┼   └   ┘   ┌   ┐   

─┐ define
 │ ones
 └──┐ lambda
    └──┐ 
      ─┤ cons 1 ones


- define
  ones
  - lambda
    - 
    - cons 1 ones

(define
 ones
 (lambda
  ()
  (cons 1 ones)))

─┐ car
 └──┐ 
    └──┐ cdr
       └──┐ ones


- car
  - 
    - cdr
      - ones

(car ((cdr (ones))))


─┐ define
 └──┐ counter-first start-num
   ─┤ lambda
    └──┐ 
      ─┤ cons
       │ start-num
       └──┐ counter-first
          └──┐ + start-num 1


┌────
│ define
│ ┌────
  │ counter-first start-num
  ├────
  │ lambda
  │ ┌────
    │ 
    ├────
    │ cons
    │ start-num
    │ ┌────
      │ counter-first
      │ ┌────
        │ + start-num 1


┌────
│ define
│ ┌────
│ │ counter-first start-num
│ ├────
│ │ lambda
│ │ ┌────
│ │ │ 
│ │ ├────
│ │ │ cons
│ │ │ start-num
│ │ │ ┌────
│ │ │ │ counter-first
│ │ │ │ ┌────
│ │ │ │ │ + start-num 1
└─┴─┴─┴─┴────

- define
  - counter-first start-num
  - lambda
    - 
    - cons
      start-num
      - counter-first
        - + start-num 1

(define
 (counter-first start-num)
 (lambda
  ()
  (cons
   start-num
   (counter-first
    (+ start-num 1)))))


- define
  counter
  - lambda
    - start-num
    - lambda
      - 
      - cons
        start-num
        - counter
          - + start-num 1

(define
 counter
 (lambda
  (start-num)
  (lambda
   ()
   (cons
    start-num
    (counter
     (+ start-num 1))))))


- define counter-from-1
  - counter-first 1


(define
 counter-from-1
  (counter-first 1))

-
  - cdr
    - 
      - cdr
        - 
          - counter 1

((cdr ((cdr ((counter 1))))))

-
  - cdr
    - 
      - cdr
        - counter-from-1


((cdr ((cdr (counter-from-1)))))

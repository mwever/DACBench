

(define (problem BW-rand-19)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15 b16 b17 b18 b19 )
(:init
(arm-empty)
(on b1 b10)
(on-table b2)
(on b3 b8)
(on b4 b18)
(on-table b5)
(on b6 b16)
(on b7 b6)
(on b8 b15)
(on b9 b3)
(on b10 b4)
(on b11 b9)
(on b12 b7)
(on b13 b1)
(on b14 b5)
(on b15 b2)
(on-table b16)
(on-table b17)
(on b18 b19)
(on b19 b11)
(clear b12)
(clear b13)
(clear b14)
(clear b17)
)
(:goal
(and
(on b1 b17)
(on b2 b10)
(on b3 b6)
(on b4 b18)
(on b5 b1)
(on b6 b9)
(on b7 b15)
(on b8 b4)
(on b9 b16)
(on b10 b3)
(on b11 b13)
(on b13 b2)
(on b14 b19)
(on b15 b5)
(on b16 b14)
(on b17 b12)
(on b19 b8))
)
)



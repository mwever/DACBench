

(define (problem BW-rand-23)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15 b16 b17 b18 b19 b20 b21 b22 b23 )
(:init
(arm-empty)
(on b1 b19)
(on b2 b21)
(on b3 b20)
(on b4 b22)
(on b5 b9)
(on b6 b5)
(on b7 b6)
(on b8 b7)
(on b9 b12)
(on b10 b13)
(on b11 b3)
(on-table b12)
(on-table b13)
(on b14 b10)
(on b15 b14)
(on b16 b8)
(on b17 b16)
(on-table b18)
(on b19 b23)
(on-table b20)
(on b21 b15)
(on b22 b18)
(on-table b23)
(clear b1)
(clear b2)
(clear b4)
(clear b11)
(clear b17)
)
(:goal
(and
(on b1 b10)
(on b2 b22)
(on b3 b7)
(on b4 b6)
(on b6 b14)
(on b8 b3)
(on b10 b11)
(on b11 b17)
(on b12 b8)
(on b15 b1)
(on b16 b20)
(on b17 b18)
(on b18 b16)
(on b19 b23)
(on b20 b9)
(on b21 b15)
(on b23 b4))
)
)


